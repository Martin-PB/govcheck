#!/usr/bin/env python3
"""Build and inspect the GovCheck in-toto assurance-evaluation statement.

This module deliberately does not implement cryptographic signing or trust-root
verification. It produces interoperable payloads and DSSE serialization only.
A structurally valid envelope is not an authenticated attestation.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "urn:govcheck:attestation:assurance-evaluation:v1"
DSSE_PAYLOAD_TYPE = "application/vnd.in-toto+json"
RESULTS = {"pass", "fail", "unknown", "conflict"}
METHOD_KINDS = {"test", "model_check", "proof_check", "inspection", "analysis", "other"}
HEX_RE = re.compile(r"^[0-9a-fA-F]+$")


class AttestationError(ValueError):
    """Raised when a GovCheck statement or DSSE envelope is malformed."""


def _object(value: Any, label: str) -> dict:
    if not isinstance(value, dict):
        raise AttestationError(label + " must be an object")
    return value


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AttestationError(label + " must be a non-empty string")
    return value.strip()


def _decode_base64(value: str, label: str) -> bytes:
    if not isinstance(value, str) or not value:
        raise AttestationError(label + " must be a non-empty base64 string")
    padded = value + "=" * (-len(value) % 4)
    for altchars in (None, b"-_"):
        try:
            return base64.b64decode(padded, altchars=altchars, validate=True)
        except (binascii.Error, ValueError):
            continue
    raise AttestationError(label + " is not valid base64")


def _uri(value: Any, label: str) -> str:
    uri = _string(value, label)
    parsed = urlparse(uri)
    if not parsed.scheme or (parsed.scheme in {"http", "https"} and not parsed.netloc):
        raise AttestationError(label + " must be an absolute URI")
    return uri


def _digest(value: Any, label: str) -> dict:
    digest = _object(value, label)
    if "sha256" not in digest:
        raise AttestationError(label + " must include a sha256 digest")
    for algorithm, encoded in digest.items():
        if not isinstance(algorithm, str) or not algorithm:
            raise AttestationError(label + " has an invalid digest algorithm")
        if not isinstance(encoded, str) or not HEX_RE.fullmatch(encoded):
            raise AttestationError(label + " has a non-hex digest value")
    if len(digest["sha256"]) != 64:
        raise AttestationError(label + " sha256 must contain exactly 64 hexadecimal characters")
    return dict(digest)


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise AttestationError(label + " must be an array of strings")
    return value


def _resource(value: Any, label: str) -> dict:
    resource = _object(value, label)
    result = {"digest": _digest(resource.get("digest"), label + ".digest")}
    for key in ("name", "uri", "mediaType"):
        if key in resource:
            result[key] = _string(resource[key], label + "." + key)
    return result


def _validate_method(method: Any, index: int) -> dict:
    item = _object(method, "methods[" + str(index) + "]")
    kind = _string(item.get("kind"), "method.kind")
    if kind not in METHOD_KINDS:
        raise AttestationError("unsupported assurance method kind: " + kind)
    result = _string(item.get("result"), "method.result")
    if result not in RESULTS:
        raise AttestationError("unsupported assurance method result: " + result)
    normalized = {
        "id": _string(item.get("id"), "method.id"),
        "kind": kind,
        "result": result,
        "scope": _string(item.get("scope"), "method.scope"),
        "assumptions": _string_list(item.get("assumptions", []), "method.assumptions"),
        "limitations": _string_list(item.get("limitations", []), "method.limitations"),
    }
    if "evidence" in item:
        if not isinstance(item["evidence"], list):
            raise AttestationError("method.evidence must be an array")
        normalized["evidence"] = [_resource(x, "method.evidence") for x in item["evidence"]]
    if "tool" in item:
        normalized["tool"] = _object(item["tool"], "method.tool")
    return normalized


def build_statement(report: dict, context: dict) -> dict:
    """Build an in-toto Statement v1 from a GovCheck report and explicit context.

    The subject digest is a deterministic content-snapshot digest supplied by
    the caller; native VCS identifiers are preserved separately in the
    predicate. No authority decision or signature is inferred.
    """
    report = _object(report, "report")
    context = _object(context, "context")
    evaluation_result = _string(report.get("overall"), "report.overall")
    if evaluation_result not in RESULTS:
        raise AttestationError("report.overall must be pass, fail, unknown or conflict")
    rules = report.get("rules")
    if not isinstance(rules, list):
        raise AttestationError("report.rules must be an array")
    normalized_rules = []
    for index, rule in enumerate(rules):
        rule = _object(rule, "report.rules[" + str(index) + "]")
        result = _string(rule.get("result"), "rule.result")
        if result not in RESULTS:
            raise AttestationError("unsupported rule result: " + result)
        if not isinstance(rule.get("applies"), bool):
            raise AttestationError("rule.applies must be boolean")
        normalized_rules.append({
            "id": _string(rule.get("id"), "rule.id"),
            "class": _string(rule.get("class"), "rule.class"),
            "result": result,
            "applies": rule["applies"],
            "reasons": _string_list(rule.get("reasons", []), "rule.reasons"),
        })

    repository = _object(context.get("repository"), "repository")
    repository_uri = _uri(repository.get("uri"), "repository.uri")
    vcs_kind = _string(repository.get("vcsKind"), "repository.vcsKind")
    candidate = _object(context.get("candidate"), "candidate")
    candidate_revision = _string(candidate.get("revision"), "candidate.revision")
    candidate_digest = _digest(candidate.get("contentDigest"), "candidate.contentDigest")
    base = _object(context.get("base"), "base")
    base_revision = _string(base.get("revision"), "base.revision")
    base_reference = _string(base.get("reference"), "base.reference")
    report_candidate = _object(report.get("candidate"), "report.candidate")
    report_candidate_revision = _string(report_candidate.get("candidate_rev"), "report.candidate.candidate_rev")
    report_base_reference = _string(report_candidate.get("base"), "report.candidate.base")
    if report_candidate_revision != candidate_revision:
        raise AttestationError("report candidate revision does not match the attestation subject context")
    if report_base_reference != base_reference:
        raise AttestationError("report base reference does not match the attestation context")
    governance = _object(context.get("governance"), "governance")
    verifier = _object(context.get("verifier"), "verifier")

    review = _object(context.get("independentReview"), "independentReview")
    review_status = _string(review.get("status"), "independentReview.status")
    if review_status not in {"unavailable", "not_performed", "attested", "unknown"}:
        raise AttestationError("unsupported independentReview.status")
    if "reviewer" in review or "reviewerName" in review:
        raise AttestationError("free-form reviewer identity is forbidden; use a detached authenticated review statement")
    normalized_review = {"status": review_status}
    if "reason" in review:
        normalized_review["reason"] = _string(review["reason"], "independentReview.reason")
    if review_status == "attested":
        if "reference" not in review:
            raise AttestationError("attested independent review requires a detached statement reference")
        normalized_review["reference"] = _resource(review["reference"], "independentReview.reference")
    elif "reference" in review:
        normalized_review["reference"] = _resource(review["reference"], "independentReview.reference")

    methods = context.get("methods")
    if not isinstance(methods, list):
        raise AttestationError("context.methods must be an array")
    normalized_methods = [_validate_method(m, i) for i, m in enumerate(methods)]

    predicate = {
        "schemaVersion": "1",
        "evaluation": {
            "id": _string(context.get("evaluationId"), "evaluationId"),
            "evaluatedOn": _string(context.get("evaluatedOn"), "evaluatedOn"),
            "result": evaluation_result,
            "rules": normalized_rules,
        },
        "repository": {"uri": repository_uri, "vcsKind": vcs_kind},
        "candidate": {
            "revision": candidate_revision,
            "contentDigest": candidate_digest,
        },
        "base": {"revision": base_revision, "reference": base_reference},
        "governance": {
            "scopeId": _string(governance.get("scopeId"), "governance.scopeId"),
            "revision": _string(governance.get("revision"), "governance.revision"),
            "digest": _digest(governance.get("digest"), "governance.digest"),
        },
        "verifier": {
            "id": _uri(verifier.get("id"), "verifier.id"),
            "version": _string(verifier.get("version"), "verifier.version"),
            "digest": _digest(verifier.get("digest"), "verifier.digest"),
            "configDigest": _digest(verifier.get("configDigest"), "verifier.configDigest"),
        },
        "methods": normalized_methods,
        "independentReview": normalized_review,
    }
    for key in ("tree", "channel", "changeSet"):
        if key in candidate:
            predicate["candidate"][key] = _string(candidate[key], "candidate." + key)
    for key in ("tree", "channel", "changeSet"):
        if key in base:
            predicate["base"][key] = _string(base[key], "base." + key)
    if "profile" in governance:
        predicate["governance"]["profile"] = _string(governance["profile"], "governance.profile")
    for key in ("decisionReferences", "riskReferences"):
        if key in context:
            if not isinstance(context[key], list):
                raise AttestationError("context." + key + " must be an array")
            predicate[key] = [_resource(x, "context." + key) for x in context[key]]

    statement = {
        "_type": STATEMENT_TYPE,
        "subject": [{"name": repository_uri, "digest": candidate_digest}],
        "predicateType": PREDICATE_TYPE,
        "predicate": predicate,
    }
    validate_statement(statement)
    return statement


def validate_statement(statement: dict) -> None:
    statement = _object(statement, "statement")
    if statement.get("_type") != STATEMENT_TYPE:
        raise AttestationError("unsupported in-toto Statement type")
    subjects = statement.get("subject")
    if not isinstance(subjects, list) or not subjects:
        raise AttestationError("in-toto Statement requires at least one subject")
    for index, subject in enumerate(subjects):
        subject = _object(subject, "subject[" + str(index) + "]")
        _digest(subject.get("digest"), "subject.digest")
    if statement.get("predicateType") != PREDICATE_TYPE:
        raise AttestationError("unsupported GovCheck predicate type")
    predicate = _object(statement.get("predicate"), "predicate")
    if predicate.get("schemaVersion") != "1":
        raise AttestationError("unsupported GovCheck predicate schema version")

    evaluation = _object(predicate.get("evaluation"), "evaluation")
    _string(evaluation.get("id"), "evaluation.id")
    _string(evaluation.get("evaluatedOn"), "evaluation.evaluatedOn")
    if evaluation.get("result") not in RESULTS:
        raise AttestationError("invalid evaluation result")
    rules = evaluation.get("rules")
    if not isinstance(rules, list):
        raise AttestationError("evaluation.rules must be an array")
    for index, rule in enumerate(rules):
        rule = _object(rule, "evaluation.rules[" + str(index) + "]")
        _string(rule.get("id"), "rule.id")
        _string(rule.get("class"), "rule.class")
        if rule.get("result") not in RESULTS or not isinstance(rule.get("applies"), bool):
            raise AttestationError("invalid evaluation rule result or applies value")
        _string_list(rule.get("reasons", []), "rule.reasons")

    repository = _object(predicate.get("repository"), "repository")
    repository_uri = _uri(repository.get("uri"), "repository.uri")
    _string(repository.get("vcsKind"), "repository.vcsKind")
    candidate = _object(predicate.get("candidate"), "candidate")
    _string(candidate.get("revision"), "candidate.revision")
    candidate_digest = _digest(candidate.get("contentDigest"), "candidate.contentDigest")
    if not any(subject.get("digest") == candidate_digest and subject.get("name") == repository_uri for subject in subjects):
        raise AttestationError("in-toto subject digest/name does not match the candidate/repository binding")
    base = _object(predicate.get("base"), "base")
    _string(base.get("revision"), "base.revision")
    _string(base.get("reference"), "base.reference")
    governance = _object(predicate.get("governance"), "governance")
    _string(governance.get("scopeId"), "governance.scopeId")
    _string(governance.get("revision"), "governance.revision")
    _digest(governance.get("digest"), "governance.digest")
    verifier = _object(predicate.get("verifier"), "verifier")
    _uri(verifier.get("id"), "verifier.id")
    _string(verifier.get("version"), "verifier.version")
    _digest(verifier.get("digest"), "verifier.digest")
    _digest(verifier.get("configDigest"), "verifier.configDigest")

    methods = predicate.get("methods")
    if not isinstance(methods, list):
        raise AttestationError("predicate.methods must be an array")
    for i, method in enumerate(methods):
        _validate_method(method, i)
    review = _object(predicate.get("independentReview"), "independentReview")
    if review.get("status") not in {"unavailable", "not_performed", "attested", "unknown"}:
        raise AttestationError("invalid independentReview.status")
    if "reviewer" in review or "reviewerName" in review:
        raise AttestationError("free-form reviewer identity is forbidden")
    if review.get("status") == "attested":
        if "reference" not in review:
            raise AttestationError("attested review requires a detached reference")
        _resource(review["reference"], "independentReview.reference")
    elif "reference" in review:
        _resource(review["reference"], "independentReview.reference")


def canonical_statement_bytes(statement: dict) -> bytes:
    validate_statement(statement)
    return json.dumps(statement, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def dsse_pae(payload_type: str, payload: bytes) -> bytes:
    """Return DSSE v1 pre-authentication encoding for external signers."""
    payload_type = _string(payload_type, "payload_type")
    if not isinstance(payload, bytes):
        raise AttestationError("DSSE payload must be bytes")
    type_bytes = payload_type.encode("utf-8")
    return (
        b"DSSEv1 " + str(len(type_bytes)).encode("ascii") + b" " + type_bytes
        + b" " + str(len(payload)).encode("ascii") + b" " + payload
    )


def build_dsse_envelope(statement: dict, signatures: list[dict]) -> dict:
    """Wrap a Statement with externally produced DSSE signatures.

    This serializes signatures; it does not verify them or establish trust.
    """
    if not isinstance(signatures, list) or not signatures:
        raise AttestationError("a DSSE envelope requires at least one external signature")
    normalized = []
    for i, item in enumerate(signatures):
        item = _object(item, "signatures[" + str(i) + "]")
        sig = _string(item.get("sig"), "signature.sig")
        decoded = _decode_base64(sig, "signature.sig")
        if not decoded:
            raise AttestationError("signature.sig must not be empty")
        normalized_item = {"sig": sig}
        if "keyid" in item:
            normalized_item["keyid"] = _string(item["keyid"], "signature.keyid")
        normalized.append(normalized_item)
    payload = canonical_statement_bytes(statement)
    return {
        "payloadType": DSSE_PAYLOAD_TYPE,
        "payload": base64.b64encode(payload).decode("ascii"),
        "signatures": normalized,
    }


def decode_dsse_envelope(envelope: dict) -> tuple[bytes, dict]:
    """Decode and structurally validate a DSSE envelope without authenticating it."""
    envelope = _object(envelope, "envelope")
    if envelope.get("payloadType") != DSSE_PAYLOAD_TYPE:
        raise AttestationError("unsupported DSSE payloadType")
    encoded = _string(envelope.get("payload"), "envelope.payload")
    payload = _decode_base64(encoded, "envelope.payload")
    if not payload:
        raise AttestationError("envelope.payload must not be empty")
    signatures = envelope.get("signatures")
    if not isinstance(signatures, list) or not signatures:
        raise AttestationError("DSSE envelope requires at least one signature")
    for i, signature in enumerate(signatures):
        signature = _object(signature, "signatures[" + str(i) + "]")
        sig = _string(signature.get("sig"), "signature.sig")
        decoded = _decode_base64(sig, "signature.sig")
        if not decoded:
            raise AttestationError("signature.sig must not be empty")
    try:
        statement = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise AttestationError("DSSE payload is not valid UTF-8 JSON") from exc
    validate_statement(statement)
    return payload, statement


def _main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a GovCheck in-toto assurance Statement.")
    parser.add_argument("--report", required=True, help="GovCheck JSON evaluation report")
    parser.add_argument("--context", required=True, help="JSON file containing explicit candidate/governance/verifier context")
    parser.add_argument("--out", required=True, help="Output path for the in-toto Statement payload")
    args = parser.parse_args(argv)
    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        context = json.loads(Path(args.context).read_text(encoding="utf-8"))
        statement = build_statement(report, context)
        Path(args.out).write_bytes(canonical_statement_bytes(statement) + b"\n")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("govcheck attestation: " + str(exc), file=sys.stderr)
        return 2
    print("Unsigned in-toto Statement payload written; no DSSE signature or signer identity has been verified.")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
