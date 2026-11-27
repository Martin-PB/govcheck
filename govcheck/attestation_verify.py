#!/usr/bin/env python3
"""Optional local DSSE verifier: Ed25519 via an operator-pinned OpenSSL binary."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .attestation import (
        AttestationError,
        DSSE_PAYLOAD_TYPE,
        PREDICATE_TYPE,
        decode_dsse_envelope,
        dsse_pae,
    )
except ImportError:  # standalone file installed by GovCheck bootstrap
    from attestation import (
        AttestationError,
        DSSE_PAYLOAD_TYPE,
        PREDICATE_TYPE,
        decode_dsse_envelope,
        dsse_pae,
    )

POLICY_ID = "govcheck.attestation-trust-policy/v1"
POLICY_SCHEMA_VERSION = "1"
SUPPORTED_ALGORITHM = "ed25519"


class VerificationError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VerificationError("invalid", label + " must be a non-empty string")
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
        raise VerificationError("invalid", label + " contains an invalid Unicode surrogate")
    return value


def _digest(value: Any, label: str) -> str:
    value = _string(value, label)
    if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise VerificationError("invalid", label + " must be a lowercase SHA-256 digest")
    return value


def _reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError("invalid", "duplicate JSON object key: " + key)
        result[key] = value
    return result


def _load_json(path: Path) -> tuple[bytes, dict]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise VerificationError("unknown", "cannot read JSON file: " + str(exc)) from exc
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_pairs,
                           parse_float=lambda _: (_ for _ in ()).throw(VerificationError("invalid", "floating-point values are not allowed in trust policy JSON")),
                           parse_constant=lambda _: (_ for _ in ()).throw(VerificationError("invalid", "non-finite JSON values are not allowed")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError("invalid", "invalid UTF-8 JSON: " + str(exc)) from exc
    if not isinstance(value, dict):
        raise VerificationError("invalid", "JSON document must be an object")
    return raw, value


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                h.update(chunk)
    except OSError as exc:
        raise VerificationError("unknown", "cannot read pinned file: " + str(exc)) from exc
    return h.hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _outside_candidate(path: Path, candidate_root: Path, label: str) -> Path:
    expanded = path.expanduser()
    lexical = expanded if expanded.is_absolute() else expanded.absolute()
    if _is_within(lexical, candidate_root):
        raise VerificationError("invalid", label + " path must be outside the candidate-controlled tree")
    resolved = expanded.resolve()
    if _is_within(resolved, candidate_root):
        raise VerificationError("invalid", label + " resolved path must be outside the candidate-controlled tree")
    if not resolved.is_file():
        raise VerificationError("unknown", label + " is not a readable regular file")
    return resolved


def _timestamp(value: Any, label: str) -> datetime:
    value = _string(value, label)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise VerificationError("invalid", label + " must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise VerificationError("invalid", label + " must include a timezone")
    return parsed.astimezone(timezone.utc)


def _load_policy(policy_path: str | Path, expected_digest: str, candidate_root: str | Path,
                 now: datetime | None = None) -> dict:
    expected_digest = _digest(expected_digest, "expected_policy_sha256")
    root = Path(candidate_root).expanduser().resolve()
    if not root.is_dir():
        raise VerificationError("invalid", "candidate_root must be an existing directory")
    policy_file = _outside_candidate(Path(policy_path), root, "trust policy")
    raw, policy = _load_json(policy_file)
    actual_digest = hashlib.sha256(raw).hexdigest()
    if actual_digest != expected_digest:
        raise VerificationError("invalid", "trust policy digest does not match the operator-pinned digest")
    if set(policy) != {"schemaVersion", "policyId", "revision", "openssl", "keys"}:
        raise VerificationError("invalid", "trust policy has missing or unknown top-level fields")
    if policy.get("schemaVersion") != POLICY_SCHEMA_VERSION or policy.get("policyId") != POLICY_ID:
        raise VerificationError("invalid", "unsupported trust policy schema or policy ID")
    revision = _string(policy.get("revision"), "policy.revision")

    openssl = policy.get("openssl")
    if not isinstance(openssl, dict) or set(openssl) != {"path", "sha256"}:
        raise VerificationError("invalid", "policy.openssl must contain only path and sha256")
    openssl_path_value = _string(openssl.get("path"), "policy.openssl.path")
    openssl_path = Path(openssl_path_value).expanduser()
    if not openssl_path.is_absolute():
        raise VerificationError("invalid", "policy.openssl.path must be absolute")
    openssl_path = _outside_candidate(openssl_path, root, "OpenSSL executable")
    openssl_digest = _digest(openssl.get("sha256"), "policy.openssl.sha256")
    if _sha256_file(openssl_path) != openssl_digest:
        raise VerificationError("invalid", "OpenSSL executable digest mismatch")
    if not os.access(openssl_path, os.X_OK):
        raise VerificationError("unknown", "pinned OpenSSL executable is not executable")

    entries = policy.get("keys")
    if not isinstance(entries, list) or not entries:
        raise VerificationError("invalid", "policy.keys must be a non-empty array")
    keys = {}
    for index, entry in enumerate(entries):
        label = "policy.keys[" + str(index) + "]"
        if not isinstance(entry, dict):
            raise VerificationError("invalid", label + " must be an object")
        required = {"keyId", "algorithm", "publicKeyPath", "publicKeySha256", "principalId",
                    "roles", "validFrom", "validUntil", "revoked"}
        if set(entry) != required:
            raise VerificationError("invalid", label + " has missing or unknown fields")
        key_id = _string(entry.get("keyId"), label + ".keyId")
        if key_id in keys:
            raise VerificationError("invalid", "duplicate keyId in trust policy: " + key_id)
        algorithm = _string(entry.get("algorithm"), label + ".algorithm").lower()
        if algorithm != SUPPORTED_ALGORITHM:
            raise VerificationError("invalid", "unsupported key algorithm for " + key_id)
        key_path_value = _string(entry.get("publicKeyPath"), label + ".publicKeyPath")
        key_path = Path(key_path_value).expanduser()
        if not key_path.is_absolute():
            key_path = policy_file.parent / key_path
        key_path = _outside_candidate(key_path, root, "public key " + key_id)
        key_digest = _digest(entry.get("publicKeySha256"), label + ".publicKeySha256")
        if _sha256_file(key_path) != key_digest:
            raise VerificationError("invalid", "public key digest mismatch for " + key_id)
        principal_id = _string(entry.get("principalId"), label + ".principalId")
        roles = entry.get("roles")
        if not isinstance(roles, list) or not roles:
            raise VerificationError("invalid", label + ".roles must be a non-empty array")
        roles = [_string(role, label + ".roles") for role in roles]
        if len(set(roles)) != len(roles):
            raise VerificationError("invalid", label + ".roles contains duplicates")
        if not isinstance(entry.get("revoked"), bool):
            raise VerificationError("invalid", label + ".revoked must be boolean")
        valid_from = _timestamp(entry.get("validFrom"), label + ".validFrom")
        valid_until = _timestamp(entry.get("validUntil"), label + ".validUntil")
        if valid_from > valid_until:
            raise VerificationError("invalid", label + " validity interval is inverted")
        keys[key_id] = {
            "keyId": key_id,
            "algorithm": algorithm,
            "publicKeyPath": str(key_path),
            "principalId": principal_id,
            "roles": roles,
            "validFrom": valid_from,
            "validUntil": valid_until,
            "revoked": entry["revoked"],
        }
    if now is None:
        current = datetime.now(timezone.utc)
    else:
        if now.tzinfo is None:
            raise VerificationError("invalid", "verification time must include a timezone")
        current = now.astimezone(timezone.utc)
    for key in keys.values():
        if key["revoked"]:
            key["eligibility"] = "revoked"
        elif current < key["validFrom"]:
            key["eligibility"] = "not-yet-valid"
        elif current > key["validUntil"]:
            key["eligibility"] = "expired"
        else:
            key["eligibility"] = "valid"
    return {
        "policyId": POLICY_ID,
        "revision": revision,
        "digest": actual_digest,
        "opensslPath": str(openssl_path),
        "opensslSha256": openssl_digest,
        "keys": keys,
    }


def _openssl_verify(openssl_path: str, public_key_path: str, pae: bytes,
                    signature: bytes, timeout_seconds: float) -> tuple[bool, str]:
    try:
        with tempfile.TemporaryDirectory(prefix="govcheck-dsse-") as directory:
            root = Path(directory)
            message_file = root / "pae.bin"
            signature_file = root / "signature.bin"
            message_file.write_bytes(pae)
            signature_file.write_bytes(signature)
            result = subprocess.run(
                [openssl_path, "pkeyutl", "-verify", "-pubin", "-inkey", public_key_path,
                 "-rawin", "-in", str(message_file), "-sigfile", str(signature_file)],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=timeout_seconds,
                shell=False,
            )
    except FileNotFoundError as exc:
        return False, "pinned OpenSSL executable is unavailable: " + str(exc)
    except subprocess.TimeoutExpired:
        return False, "OpenSSL verification timed out"
    except OSError as exc:
        return False, "OpenSSL could not be executed: " + str(exc)
    if result.returncode == 0:
        return True, "signature verified"
    detail = result.stderr.decode("utf-8", errors="replace").strip()
    return False, detail or "OpenSSL rejected the signature"


def verify_dsse_envelope(
    envelope: dict,
    trust_policy_path: str | Path,
    expected_policy_sha256: str,
    candidate_root: str | Path,
    required_role: str | None = None,
    required_principal: str | None = None,
    expected_candidate_revision: str | None = None,
    expected_governance_revision: str | None = None,
    expected_scope_id: str | None = None,
    expected_base_revision: str | None = None,
    expected_content_sha256: str | None = None,
    expected_predicate_type: str | None = None,
    forbidden_principal: str | None = None,
    now: datetime | None = None,
    openssl_timeout_seconds: float = 10.0,
) -> dict:
    """Verify one DSSE envelope against an operator-pinned trust policy."""
    try:
        if not isinstance(envelope, dict):
            raise VerificationError("invalid", "DSSE envelope must be an object")
        if set(envelope) != {"payloadType", "payload", "signatures"}:
            raise VerificationError("invalid", "DSSE envelope has missing or unknown top-level fields")
        if not isinstance(envelope.get("signatures"), list):
            raise VerificationError("invalid", "DSSE signatures must be an array")
        for index, item in enumerate(envelope["signatures"]):
            if not isinstance(item, dict) or set(item) - {"keyid", "sig"}:
                raise VerificationError("invalid", "signature[" + str(index) + "] has unknown fields")
        payload, statement = decode_dsse_envelope(envelope)
        if envelope.get("payloadType") != DSSE_PAYLOAD_TYPE:
            raise VerificationError("invalid", "unsupported DSSE payload type")
        predicate_type = statement["predicateType"]
        if expected_predicate_type is not None and predicate_type != expected_predicate_type:
            raise VerificationError("invalid", "predicate type does not match the expected type")
        predicate = statement["predicate"]
        if predicate_type == "urn:govcheck:attestation:independent-review:v1":
            bindings = {
                "candidate_revision": predicate["candidateRevision"],
                "governance_revision": predicate["governanceRevision"],
                "scope_id": predicate["scopeId"],
                "base_revision": predicate["baseRevision"],
                "content_sha256": predicate["candidateContentSha256"],
            }
        elif predicate_type == "urn:govcheck:attestation:forge-author-identity:v1":
            bindings = {
                "candidate_revision": predicate["candidateRevision"],
                "governance_revision": predicate["governanceRevision"],
                "scope_id": predicate["scopeId"],
                "base_revision": predicate["baseRevision"],
                "content_sha256": predicate["candidateContentSha256"],
            }
        else:
            bindings = {
                "candidate_revision": predicate["candidate"]["revision"],
                "governance_revision": predicate["governance"]["revision"],
                "scope_id": predicate["governance"]["scopeId"],
                "base_revision": predicate["base"]["revision"],
                "content_sha256": predicate["candidate"]["contentDigest"]["sha256"],
            }
        for expected, actual, label in (
            (expected_candidate_revision, bindings["candidate_revision"], "candidate revision"),
            (expected_governance_revision, bindings["governance_revision"], "governance revision"),
            (expected_scope_id, bindings["scope_id"], "scope"),
            (expected_base_revision, bindings["base_revision"], "base revision"),
        ):
            if expected is not None and actual != expected:
                raise VerificationError("invalid", label + " does not match the expected binding")
        if expected_content_sha256 is not None:
            _digest(expected_content_sha256, "expected_content_sha256")
            if bindings["content_sha256"] != expected_content_sha256:
                raise VerificationError("invalid", "candidate content digest does not match the expected content")

        policy = _load_policy(trust_policy_path, expected_policy_sha256, candidate_root, now=now)
        pae = dsse_pae(envelope["payloadType"], payload)
        valid_signers = []
        rejected = []
        unknown = []
        for index, signature_item in enumerate(envelope.get("signatures", [])):
            if not isinstance(signature_item, dict):
                rejected.append("signature[" + str(index) + "] is not an object")
                continue
            key_id = signature_item.get("keyid")
            if not isinstance(key_id, str) or not key_id:
                unknown.append("signature[" + str(index) + "] has no keyid")
                continue
            key = policy["keys"].get(key_id)
            if key is None:
                unknown.append("no trusted key for keyid " + key_id)
                continue
            if key["eligibility"] != "valid":
                rejected.append("key " + key_id + " is " + key["eligibility"])
                continue
            if required_role is not None and required_role not in key["roles"]:
                unknown.append("key " + key_id + " is not authorized for role " + required_role)
                continue
            if required_principal is not None and key["principalId"] != required_principal:
                unknown.append("key " + key_id + " is not mapped to required principal " + required_principal)
                continue
            try:
                signature = base64.b64decode(signature_item.get("sig", ""), validate=True)
            except (ValueError, TypeError) as exc:
                rejected.append("signature for key " + key_id + " is invalid base64: " + str(exc))
                continue
            if not signature:
                rejected.append("signature for key " + key_id + " is empty")
                continue
            ok, reason = _openssl_verify(policy["opensslPath"], key["publicKeyPath"], pae, signature, openssl_timeout_seconds)
            if ok:
                valid_signers.append({
                    "keyId": key_id,
                    "principalId": key["principalId"],
                    "roles": key["roles"],
                    "algorithm": key["algorithm"],
                })
            else:
                rejected.append("signature for key " + key_id + " failed: " + reason)
        if valid_signers:
            if forbidden_principal is not None:
                _string(forbidden_principal, "forbidden_principal")
                if any(signer["principalId"] == forbidden_principal for signer in valid_signers):
                    return {"status": "invalid", "reason": "authenticated reviewer principal is not independent from the candidate author"}
                if len({signer["principalId"] for signer in valid_signers}) != 1:
                    return {"status": "invalid", "reason": "independent-review envelope has multiple authenticated reviewer principals"}
            return {
                "status": "verified",
                "policyId": policy["policyId"],
                "policyRevision": policy["revision"],
                "policyDigest": policy["digest"],
                "payloadType": envelope["payloadType"],
                "predicateType": statement["predicateType"],
                "signers": valid_signers,
                "rejectedSignatures": rejected,
                "unknownSignatures": unknown,
                "statement": statement,
                "verifier": {"implementation": "openssl-pkeyutl-ed25519/v1", "path": policy["opensslPath"], "sha256": policy["opensslSha256"]},
            }
        if rejected:
            return {"status": "invalid", "reason": "; ".join(rejected), "unknownSignatures": unknown}
        return {"status": "unknown", "reason": "; ".join(unknown) or "no eligible trusted signature"}
    except VerificationError as exc:
        return {"status": exc.status, "reason": str(exc)}
    except AttestationError as exc:
        return {"status": "invalid", "reason": "invalid DSSE statement/envelope: " + str(exc)}
    except (KeyError, TypeError, ValueError) as exc:
        return {"status": "invalid", "reason": "malformed DSSE envelope or trust policy: " + str(exc)}


def _main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify a detached GovCheck DSSE envelope using an operator-pinned Ed25519 trust policy.")
    sub = parser.add_subparsers(dest="command", required=True)
    verify = sub.add_parser("verify", help="verify DSSE signature, trust policy and candidate bindings")
    verify.add_argument("--envelope", required=True)
    verify.add_argument("--trust-policy", required=True)
    verify.add_argument("--trust-policy-sha256", required=True)
    verify.add_argument("--candidate-root", required=True)
    verify.add_argument("--required-role")
    verify.add_argument("--required-principal")
    verify.add_argument("--candidate-revision")
    verify.add_argument("--governance-revision")
    verify.add_argument("--scope-id")
    verify.add_argument("--base-revision")
    verify.add_argument("--content-sha256")
    verify.add_argument("--expected-predicate-type")
    verify.add_argument("--forbidden-principal", help="Reject a signer principal matching the trusted candidate-author principal")
    args = parser.parse_args(argv)
    try:
        envelope_path = Path(args.envelope).expanduser().resolve()
        _, envelope = _load_json(envelope_path)
        result = verify_dsse_envelope(
            envelope,
            args.trust_policy,
            args.trust_policy_sha256,
            args.candidate_root,
            required_role=args.required_role,
            required_principal=args.required_principal,
            expected_candidate_revision=args.candidate_revision,
            expected_governance_revision=args.governance_revision,
            expected_scope_id=args.scope_id,
            expected_base_revision=args.base_revision,
            expected_content_sha256=args.content_sha256,
            expected_predicate_type=args.expected_predicate_type,
            forbidden_principal=args.forbidden_principal,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") == "verified" else 2
    except VerificationError as exc:
        print(json.dumps({"status": exc.status, "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except OSError as exc:
        print(json.dumps({"status": "unknown", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(_main())
