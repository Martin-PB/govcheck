"""Authenticated, candidate-bound governance acceptance decision statements."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import re
import subprocess
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "urn:govcheck:attestation:acceptance-decision:v1"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
DECISIONS = {"accept", "reject", "accept_with_risk"}
EVALUATION_RESULTS = {"pass", "fail", "unknown", "conflict"}
RISK_FIELDS = {"id", "reason", "scope", "expiresAt", "residualRisk", "affectedClaims", "authorizationDigest"}


class AcceptanceDecisionError(ValueError):
    """Raised when an acceptance decision is malformed or inapplicable."""


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AcceptanceDecisionError(label + " must be a non-empty string")
    return value.strip()


def _digest(value: Any, label: str) -> str:
    text = _text(value, label)
    if not HEX64_RE.fullmatch(text):
        raise AcceptanceDecisionError(label + " must be lowercase SHA-256")
    return text


def _timestamp(value: Any, label: str) -> datetime:
    text = _text(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AcceptanceDecisionError(label + " must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise AcceptanceDecisionError(label + " must include a timezone")
    return parsed.astimezone(timezone.utc)


def _uri(value: Any, label: str) -> str:
    text = _text(value, label)
    parsed = urlparse(text)
    if not parsed.scheme or (parsed.scheme in {"http", "https"} and not parsed.netloc):
        raise AcceptanceDecisionError(label + " must be an absolute URI")
    return text


def evaluation_report_digest(raw_bytes: bytes) -> str:
    """Digest the exact serialized report bytes supplied to the gate."""
    if not isinstance(raw_bytes, bytes) or not raw_bytes:
        raise AcceptanceDecisionError("evaluation report bytes must be non-empty")
    return hashlib.sha256(raw_bytes).hexdigest()


def validate_predicate(predicate: dict) -> dict:
    if not isinstance(predicate, dict):
        raise AcceptanceDecisionError("predicate must be an object")
    required = {
        "schemaVersion", "decisionId", "repositoryId", "candidateRevision",
        "candidateContentSha256", "baseRevision", "ref", "governanceRevision",
        "scopeId", "evaluationDigest", "result", "decidedOn", "rationale",
        "riskAcceptance",
    }
    if set(predicate) != required:
        raise AcceptanceDecisionError("predicate fields must match acceptance-decision/v1 exactly")
    if predicate["schemaVersion"] != "1":
        raise AcceptanceDecisionError("schemaVersion must be '1'")
    result = _text(predicate["result"], "result")
    if result not in DECISIONS:
        raise AcceptanceDecisionError("result must be accept, reject or accept_with_risk")
    risk = predicate["riskAcceptance"]
    if result == "accept_with_risk":
        if not isinstance(risk, dict) or set(risk) != RISK_FIELDS:
            raise AcceptanceDecisionError("accept_with_risk requires a complete riskAcceptance record")
        claims = risk["affectedClaims"]
        if not isinstance(claims, list) or not claims or not all(isinstance(x, str) and x.strip() for x in claims):
            raise AcceptanceDecisionError("riskAcceptance.affectedClaims must be a non-empty list")
        claims = [x.strip() for x in claims]
        if len(set(claims)) != len(claims):
            raise AcceptanceDecisionError("riskAcceptance.affectedClaims must be unique")
        risk = {
            "id": _text(risk["id"], "riskAcceptance.id"),
            "reason": _text(risk["reason"], "riskAcceptance.reason"),
            "scope": _text(risk["scope"], "riskAcceptance.scope"),
            "expiresAt": _timestamp(risk["expiresAt"], "riskAcceptance.expiresAt").isoformat(),
            "residualRisk": _text(risk["residualRisk"], "riskAcceptance.residualRisk"),
            "affectedClaims": claims,
            "authorizationDigest": _digest(risk["authorizationDigest"], "riskAcceptance.authorizationDigest"),
        }
    elif risk is not None:
        raise AcceptanceDecisionError("riskAcceptance must be null unless result is accept_with_risk")
    return {
        "schemaVersion": "1",
        "decisionId": _text(predicate["decisionId"], "decisionId"),
        "repositoryId": _text(predicate["repositoryId"], "repositoryId"),
        "candidateRevision": _text(predicate["candidateRevision"], "candidateRevision"),
        "candidateContentSha256": _digest(predicate["candidateContentSha256"], "candidateContentSha256"),
        "baseRevision": _text(predicate["baseRevision"], "baseRevision"),
        "ref": _text(predicate["ref"], "ref"),
        "governanceRevision": _text(predicate["governanceRevision"], "governanceRevision"),
        "scopeId": _text(predicate["scopeId"], "scopeId"),
        "evaluationDigest": _digest(predicate["evaluationDigest"], "evaluationDigest"),
        "result": result,
        "decidedOn": _timestamp(predicate["decidedOn"], "decidedOn").isoformat(),
        "rationale": _text(predicate["rationale"], "rationale"),
        "riskAcceptance": risk,
    }


def build_statement(
    *,
    repository_uri: str,
    decision_id: str,
    repository_id: str,
    candidate_revision: str,
    candidate_content_sha256: str,
    base_revision: str,
    ref: str,
    governance_revision: str,
    scope_id: str,
    evaluation_digest: str,
    result: str,
    decided_on: str,
    rationale: str,
    risk_acceptance: dict | None = None,
) -> dict:
    repository_uri = _uri(repository_uri, "repository_uri")
    predicate = validate_predicate({
        "schemaVersion": "1",
        "decisionId": decision_id,
        "repositoryId": repository_id,
        "candidateRevision": candidate_revision,
        "candidateContentSha256": candidate_content_sha256,
        "baseRevision": base_revision,
        "ref": ref,
        "governanceRevision": governance_revision,
        "scopeId": scope_id,
        "evaluationDigest": evaluation_digest,
        "result": result,
        "decidedOn": decided_on,
        "rationale": rationale,
        "riskAcceptance": risk_acceptance,
    })
    return {
        "_type": STATEMENT_TYPE,
        "subject": [{
            "name": repository_uri,
            "digest": {"sha256": predicate["candidateContentSha256"]},
        }],
        "predicateType": PREDICATE_TYPE,
        "predicate": predicate,
    }


def sign_statement(statement: dict, private_key_path: str | Path, key_id: str, openssl_path: str = "openssl", timeout_seconds: float = 10.0) -> dict:
    """Create a DSSE Ed25519 envelope using the operator's private key."""
    try:
        from govcheck import attestation
    except ImportError:
        import attestation
    payload = attestation.canonical_statement_bytes(statement)
    pae = attestation.dsse_pae(attestation.DSSE_PAYLOAD_TYPE, payload)
    try:
        with tempfile.TemporaryDirectory(prefix="govcheck-sign-decision-") as directory:
            root = Path(directory)
            pae_path = root / "pae.bin"
            signature_path = root / "signature.bin"
            pae_path.write_bytes(pae)
            result = subprocess.run(
                [str(openssl_path), "pkeyutl", "-sign", "-inkey", str(Path(private_key_path).expanduser()),
                 "-rawin", "-in", str(pae_path), "-out", str(signature_path)],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=timeout_seconds,
                shell=False,
            )
            if result.returncode != 0:
                detail = result.stderr.decode("utf-8", errors="replace").strip()
                raise AcceptanceDecisionError("OpenSSL could not sign the decision: " + (detail or "signing failed"))
            signature = signature_path.read_bytes()
    except subprocess.TimeoutExpired as exc:
        raise AcceptanceDecisionError("OpenSSL decision signing timed out") from exc
    except OSError as exc:
        raise AcceptanceDecisionError("cannot execute OpenSSL or read the signing key: " + str(exc)) from exc
    return attestation.build_dsse_envelope(statement, [{
        "keyid": _text(key_id, "key_id"),
        "sig": base64.b64encode(signature).decode("ascii"),
    }])


def sign_decision_from_report(
    report_bytes: bytes,
    *,
    repository_uri: str,
    repository_id: str,
    decision_id: str,
    result: str,
    rationale: str,
    private_key_path: str | Path,
    key_id: str,
    openssl_path: str = "openssl",
    risk_acceptance: dict | None = None,
    decided_on: str | None = None,
) -> dict:
    """Build and sign a decision bound to the exact report bytes from the gate."""
    try:
        report = json.loads(report_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcceptanceDecisionError("evaluation report must be valid UTF-8 JSON") from exc
    if not isinstance(report, dict) or report.get("overall") not in EVALUATION_RESULTS:
        raise AcceptanceDecisionError("evaluation report is malformed")
    candidate = report.get("candidate")
    if not isinstance(candidate, dict):
        raise AcceptanceDecisionError("evaluation report has no candidate bindings")
    fields = {
        "candidateRevision": candidate.get("candidate_rev"),
        "candidateContentSha256": candidate.get("content_sha256"),
        "baseRevision": candidate.get("base_revision"),
        "ref": candidate.get("ref"),
        "governanceRevision": candidate.get("governance_revision"),
        "scopeId": candidate.get("scope_id"),
    }
    if not all(isinstance(value, str) and value for value in fields.values()):
        raise AcceptanceDecisionError("evaluation report is missing candidate/base/ref/governance/scope bindings")
    if result == "accept" and report["overall"] != "pass":
        raise AcceptanceDecisionError("accept can only be signed for an overall PASS report")
    if result == "accept_with_risk" and report["overall"] == "pass":
        raise AcceptanceDecisionError("accept_with_risk is not applicable to an overall PASS report")
    statement = build_statement(
        repository_uri=repository_uri,
        decision_id=decision_id or str(uuid.uuid4()),
        repository_id=repository_id,
        candidate_revision=fields["candidateRevision"],
        candidate_content_sha256=fields["candidateContentSha256"],
        base_revision=fields["baseRevision"],
        ref=fields["ref"],
        governance_revision=fields["governanceRevision"],
        scope_id=fields["scopeId"],
        evaluation_digest=evaluation_report_digest(report_bytes),
        result=result,
        decided_on=decided_on or datetime.now(timezone.utc).isoformat(),
        rationale=rationale,
        risk_acceptance=risk_acceptance,
    )
    return sign_statement(statement, private_key_path, key_id, openssl_path)


def evaluate_decision(
    predicate: dict,
    *,
    report: dict,
    report_bytes: bytes,
    expected_repository_id: str,
    expected_candidate_revision: str,
    expected_candidate_content_sha256: str,
    expected_base_revision: str,
    expected_ref: str,
    expected_governance_revision: str,
    expected_scope_id: str,
    now: datetime | None = None,
) -> dict:
    """Check a verified authority decision against one exact evaluation."""
    predicate = validate_predicate(predicate)
    expected = {
        "repositoryId": expected_repository_id,
        "candidateRevision": expected_candidate_revision,
        "candidateContentSha256": expected_candidate_content_sha256,
        "baseRevision": expected_base_revision,
        "ref": expected_ref,
        "governanceRevision": expected_governance_revision,
        "scopeId": expected_scope_id,
        "evaluationDigest": evaluation_report_digest(report_bytes),
    }
    for field, value in expected.items():
        if predicate[field] != value:
            return {"result": "fail", "reason": "decision binding mismatch: " + field}
    try:
        decoded_report = json.loads(report_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"result": "unknown", "reason": "evaluation report bytes are not valid UTF-8 JSON"}
    if decoded_report != report:
        return {"result": "fail", "reason": "evaluation report object does not match the exact report bytes"}
    if not isinstance(report, dict) or report.get("overall") not in EVALUATION_RESULTS:
        return {"result": "unknown", "reason": "evaluation report is malformed or has an unknown result"}
    candidate = report.get("candidate")
    if not isinstance(candidate, dict):
        return {"result": "unknown", "reason": "evaluation report has no candidate binding metadata"}
    report_bindings = {
        "candidate_rev": expected_candidate_revision,
        "base_revision": expected_base_revision,
        "content_sha256": expected_candidate_content_sha256,
        "ref": expected_ref,
        "governance_revision": expected_governance_revision,
        "scope_id": expected_scope_id,
    }
    for field, value in report_bindings.items():
        if candidate.get(field) != value:
            return {"result": "fail", "reason": "evaluation report candidate binding mismatch: " + field}
    decision = predicate["result"]
    if decision == "reject":
        return {"result": "fail", "reason": "governance authority rejected this candidate"}
    if decision == "accept":
        if report["overall"] != "pass":
            return {"result": "fail", "reason": "accept decision cannot override evaluation result " + report["overall"]}
        return {"result": "pass", "reason": "authenticated governance decision accepts a passing evaluation"}
    if report["overall"] == "pass":
        return {"result": "fail", "reason": "accept_with_risk is not applicable to an already passing evaluation"}
    risk = predicate["riskAcceptance"]
    current = datetime.now(timezone.utc) if now is None else now
    if current.tzinfo is None:
        return {"result": "unknown", "reason": "decision verification time must include a timezone"}
    if _timestamp(risk["expiresAt"], "riskAcceptance.expiresAt") <= current.astimezone(timezone.utc):
        return {"result": "fail", "reason": "risk acceptance has expired"}
    if risk["scope"] != expected_scope_id:
        return {"result": "fail", "reason": "risk acceptance scope does not match the candidate scope"}
    return {"result": "accepted-with-risk", "reason": "authenticated scoped risk acceptance " + risk["id"]}

def verify_and_evaluate(
    envelope: dict,
    trust_policy_path,
    expected_policy_sha256: str,
    candidate_root,
    *,
    report: dict,
    report_bytes: bytes,
    expected_repository_id: str,
    expected_candidate_revision: str,
    expected_candidate_content_sha256: str,
    expected_base_revision: str,
    expected_ref: str,
    expected_governance_revision: str,
    expected_scope_id: str,
    required_role: str,
    now: datetime | None = None,
) -> dict:
    """Authenticate an authority decision then evaluate it against the exact report."""
    if required_role != "governance-authority":
        return {"result": "fail", "reason": "acceptance decisions require the governance-authority trust-policy role"}
    try:
        from govcheck.attestation_verify import verify_dsse_envelope
    except ImportError:
        from attestation_verify import verify_dsse_envelope
    verified = verify_dsse_envelope(
        envelope,
        trust_policy_path,
        expected_policy_sha256,
        candidate_root,
        required_role=required_role,
        expected_candidate_revision=expected_candidate_revision,
        expected_governance_revision=expected_governance_revision,
        expected_scope_id=expected_scope_id,
        expected_base_revision=expected_base_revision,
        expected_content_sha256=expected_candidate_content_sha256,
        expected_predicate_type=PREDICATE_TYPE,
        now=now,
    )
    if verified.get("status") == "unknown":
        return {"result": "unknown", "reason": verified.get("reason", "authority trust is unknown")}
    if verified.get("status") != "verified":
        return {"result": "fail", "reason": verified.get("reason", "authority decision is invalid")}
    signers = verified.get("signers", [])
    principals = {item.get("principalId") for item in signers if isinstance(item, dict) and item.get("principalId")}
    if len(principals) != 1:
        return {"result": "fail", "reason": "acceptance decision must have exactly one authenticated authority principal"}
    predicate = verified.get("statement", {}).get("predicate", {})
    decision = evaluate_decision(
        predicate,
        report=report,
        report_bytes=report_bytes,
        expected_repository_id=expected_repository_id,
        expected_candidate_revision=expected_candidate_revision,
        expected_candidate_content_sha256=expected_candidate_content_sha256,
        expected_base_revision=expected_base_revision,
        expected_ref=expected_ref,
        expected_governance_revision=expected_governance_revision,
        expected_scope_id=expected_scope_id,
        now=now,
    )
    decision["decisionId"] = predicate.get("decisionId")
    decision["riskAcceptance"] = predicate.get("riskAcceptance")
    decision["authorityPrincipal"] = next(iter(principals))
    decision["policyDigest"] = verified.get("policyDigest")
    return decision


def _main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify a detached GovCheck governance acceptance decision.")
    sub = parser.add_subparsers(dest="command", required=True)
    sign = sub.add_parser("sign", help="sign an authority decision bound to an exact evaluation report")
    sign.add_argument("--report", required=True, help="exact report JSON bytes produced by the gate")
    sign.add_argument("--repository-uri", required=True)
    sign.add_argument("--repository-id", required=True)
    sign.add_argument("--decision-id", default="")
    sign.add_argument("--result", choices=sorted(DECISIONS), required=True)
    sign.add_argument("--rationale", required=True)
    sign.add_argument("--risk-acceptance", help="JSON file containing the complete riskAcceptance object")
    sign.add_argument("--private-key", required=True)
    sign.add_argument("--key-id", required=True)
    sign.add_argument("--openssl", default="openssl")
    verify = sub.add_parser("verify", help="verify DSSE authority decision and exact evaluation bindings")
    verify.add_argument("--envelope", required=True)
    verify.add_argument("--report", required=True)
    verify.add_argument("--trust-policy", required=True)
    verify.add_argument("--trust-policy-sha256", required=True)
    verify.add_argument("--candidate-root", required=True)
    verify.add_argument("--repository-id", required=True)
    verify.add_argument("--candidate-revision", required=True)
    verify.add_argument("--content-sha256", required=True)
    verify.add_argument("--base-revision", required=True)
    verify.add_argument("--ref", required=True)
    verify.add_argument("--governance-revision", required=True)
    verify.add_argument("--scope-id", required=True)
    verify.add_argument("--required-role", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "sign":
            report_bytes = Path(args.report).expanduser().resolve().read_bytes()
            risk = None
            if args.risk_acceptance:
                risk = json.loads(Path(args.risk_acceptance).expanduser().resolve().read_text(encoding="utf-8"))
            envelope = sign_decision_from_report(
                report_bytes,
                repository_uri=args.repository_uri,
                repository_id=args.repository_id,
                decision_id=args.decision_id,
                result=args.result,
                rationale=args.rationale,
                private_key_path=args.private_key,
                key_id=args.key_id,
                openssl_path=args.openssl,
                risk_acceptance=risk,
            )
            print(json.dumps(envelope, indent=2, ensure_ascii=False))
            return 0
        root = Path(args.candidate_root).expanduser().resolve()
        for label, value in (("envelope", args.envelope), ("report", args.report)):
            path = Path(value).expanduser().resolve()
            if path == root or root in path.parents:
                raise AcceptanceDecisionError(label + " must be stored outside the candidate tree")
        report_path = Path(args.report).expanduser().resolve()
        report_bytes = report_path.read_bytes()
        report = json.loads(report_bytes.decode("utf-8"))
        envelope = json.loads(Path(args.envelope).expanduser().resolve().read_text(encoding="utf-8"))
        result = verify_and_evaluate(
            envelope,
            args.trust_policy,
            args.trust_policy_sha256,
            root,
            report=report,
            report_bytes=report_bytes,
            expected_repository_id=args.repository_id,
            expected_candidate_revision=args.candidate_revision,
            expected_candidate_content_sha256=args.content_sha256,
            expected_base_revision=args.base_revision,
            expected_ref=args.ref,
            expected_governance_revision=args.governance_revision,
            expected_scope_id=args.scope_id,
            required_role=args.required_role,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("result") in {"pass", "accepted-with-risk"} else 2
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"result": "unknown", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(_main())
