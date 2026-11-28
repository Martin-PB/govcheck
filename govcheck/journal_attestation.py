"""DSSE signing/export for canonical journal receipts using external OpenSSL.

Private-key operations are delegated to the operator-pinned OpenSSL executable;
this module does not implement cryptography or generate/manage keys.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from govcheck import attestation
    from govcheck.journal import Journal, JournalError, digest_json
except ImportError:
    import attestation
    from journal import Journal, JournalError, digest_json

PREDICATE_TYPE = "urn:govcheck:attestation:journal-receipt:v1"
SCHEMA_VERSION = "1"


class JournalAttestationError(Exception):
    pass


def _object(value: Any, label: str) -> dict:
    if not isinstance(value, dict):
        raise JournalAttestationError(label + " must be an object")
    return value


def validate_predicate(predicate: dict) -> dict:
    predicate = _object(predicate, "journal receipt predicate")
    if predicate.get("schemaVersion") != SCHEMA_VERSION:
        raise JournalAttestationError("unsupported journal receipt predicate schema")
    receipt = _object(predicate.get("receipt"), "receipt")
    event = _object(predicate.get("event"), "event")
    journal = _object(predicate.get("journal"), "journal")
    repository = _object(predicate.get("repository"), "repository")
    candidate = _object(predicate.get("candidate"), "candidate")
    base = _object(predicate.get("base"), "base")
    governance = _object(predicate.get("governance"), "governance")

    required_receipt = ("scopeId", "position", "eventId", "previousDigest", "eventDigest", "idempotencyKey", "committedAt", "receiptDigest")
    if any(key not in receipt for key in required_receipt):
        raise JournalAttestationError("receipt is missing required fields")
    if isinstance(receipt["position"], bool) or not isinstance(receipt["position"], int) or receipt["position"] < 0:
        raise JournalAttestationError("receipt position must be a non-negative integer")
    for key in ("scopeId", "eventId", "eventDigest", "idempotencyKey", "committedAt", "receiptDigest"):
        if not isinstance(receipt[key], str) or not receipt[key]:
            raise JournalAttestationError("receipt." + key + " must be a non-empty string")

    event_digest = event.get("eventDigest")
    if event_digest != receipt["eventDigest"]:
        raise JournalAttestationError("event and receipt eventDigest differ")
    event_without_digest = dict(event)
    event_without_digest.pop("eventDigest", None)
    if digest_json(event_without_digest) != event_digest:
        raise JournalAttestationError("event digest does not match canonical event bytes")
    if digest_json(event.get("payload")) != event.get("payloadDigest"):
        raise JournalAttestationError("event payload digest does not match")
    receipt_without_digest = dict(receipt)
    receipt_without_digest.pop("receiptDigest", None)
    if digest_json(receipt_without_digest) != receipt["receiptDigest"]:
        raise JournalAttestationError("receipt digest does not match canonical receipt bytes")

    for key, event_key in (
        ("scopeId", "scopeId"), ("position", "position"), ("eventId", "eventId"),
        ("previousDigest", "previousDigest"), ("eventDigest", "eventDigest"),
        ("idempotencyKey", "idempotencyKey"),
    ):
        if receipt[key] != event.get(event_key):
            raise JournalAttestationError("receipt/event binding mismatch: " + key)
    if event.get("canonicalization") != "govcheck.jcs-safe-integer/v1":
        raise JournalAttestationError("unsupported journal canonicalization profile")
    if event.get("scopeId") != receipt["scopeId"]:
        raise JournalAttestationError("event scope does not match receipt scope")

    if journal.get("integrityStatus") != "valid":
        raise JournalAttestationError("journal integrity status must be valid")
    head_position = journal.get("verifiedHeadPosition")
    head_digest = journal.get("verifiedHeadDigest")
    if isinstance(head_position, bool) or not isinstance(head_position, int) or head_position < receipt["position"]:
        raise JournalAttestationError("verified journal head does not cover the receipt")
    if not isinstance(head_digest, str) or not head_digest:
        raise JournalAttestationError("verified journal head digest is missing")
    if head_position == receipt["position"] and head_digest != event_digest:
        raise JournalAttestationError("receipt does not match the verified journal head")

    payload = _object(event.get("payload"), "event.payload")
    provenance = _object(payload.get("vcsProvenance"), "event.payload.vcsProvenance")
    provenance_repository = _object(provenance.get("repository"), "vcsProvenance.repository")
    provenance_vcs = _object(provenance.get("vcs"), "vcsProvenance.vcs")
    provenance_target = _object(provenance.get("target"), "vcsProvenance.target")
    provenance_candidate = _object(provenance.get("candidate"), "vcsProvenance.candidate")
    provenance_base = provenance.get("base")
    provenance_governance = _object(provenance.get("governance"), "vcsProvenance.governance")
    if provenance_vcs.get("kind") not in {"git", "pijul"}:
        raise JournalAttestationError("unsupported VCS provenance kind")
    if not isinstance(provenance_candidate.get("nativeRevision"), str) or not provenance_candidate["nativeRevision"]:
        raise JournalAttestationError("native candidate revision is missing")
    candidate_digest = provenance_candidate.get("contentDigest")
    if not isinstance(candidate_digest, str) or not candidate_digest.startswith("sha256:") or len(candidate_digest) != 71:
        raise JournalAttestationError("candidate content digest is malformed")
    if provenance_governance.get("scopeId") != receipt["scopeId"]:
        raise JournalAttestationError("provenance scope does not match receipt")
    if payload.get("scopeId") not in {None, receipt["scopeId"]}:
        raise JournalAttestationError("event payload scope does not match receipt")

    expected_repository = {
        "uri": provenance_repository.get("uri"),
        "vcsKind": provenance_vcs.get("kind"),
    }
    if repository != expected_repository:
        raise JournalAttestationError("statement repository binding differs from event provenance")
    if candidate.get("revision") != provenance_candidate["nativeRevision"]:
        raise JournalAttestationError("statement candidate revision differs from event provenance")
    if candidate.get("contentDigest") != {"sha256": candidate_digest.removeprefix("sha256:")}:
        raise JournalAttestationError("statement candidate content digest differs from event provenance")
    if not isinstance(base.get("revision"), str) or not base.get("revision"):
        raise JournalAttestationError("statement base revision is missing")
    expected_base_revision = provenance_base.get("nativeRevision") if isinstance(provenance_base, dict) else "bootstrap"
    if base.get("revision") != expected_base_revision:
        raise JournalAttestationError("statement base revision differs from event provenance")
    if base.get("reference") != provenance_target.get("name"):
        raise JournalAttestationError("statement base reference differs from event provenance")
    if governance.get("scopeId") != provenance_governance.get("scopeId") or governance.get("revision") != provenance_governance.get("revision"):
        raise JournalAttestationError("statement governance binding differs from event provenance")
    governance_digest = provenance_governance.get("digest")
    if governance.get("digest") != {"sha256": str(governance_digest).removeprefix("sha256:")}:
        raise JournalAttestationError("statement governance digest differs from event provenance")

    return predicate


def build_journal_receipt_statement(event_record: dict) -> dict:
    event_record = _object(event_record, "event_record")
    event = _object(event_record.get("event"), "event_record.event")
    receipt = _object(event_record.get("receipt"), "event_record.receipt")
    integrity = _object(event_record.get("integrity"), "event_record.integrity")
    payload = _object(event.get("payload"), "event.payload")
    provenance = _object(payload.get("vcsProvenance"), "event.payload.vcsProvenance")
    repository = _object(provenance.get("repository"), "vcsProvenance.repository")
    vcs = _object(provenance.get("vcs"), "vcsProvenance.vcs")
    target = _object(provenance.get("target"), "vcsProvenance.target")
    candidate = _object(provenance.get("candidate"), "vcsProvenance.candidate")
    base = provenance.get("base")
    governance = _object(provenance.get("governance"), "vcsProvenance.governance")
    content_digest = candidate.get("contentDigest")
    if not isinstance(content_digest, str) or not content_digest.startswith("sha256:"):
        raise JournalAttestationError("candidate provenance requires a SHA-256 content digest")
    base_revision = base.get("nativeRevision") if isinstance(base, dict) else "bootstrap"

    subject_name = "urn:govcheck:journal-receipt:" + receipt["scopeId"] + ":" + str(receipt["position"])
    statement = {
        "_type": attestation.STATEMENT_TYPE,
        "subject": [{
            "name": subject_name,
            "digest": {"sha256": receipt["eventDigest"]},
        }],
        "predicateType": PREDICATE_TYPE,
        "predicate": {
            "schemaVersion": SCHEMA_VERSION,
            "repository": {"uri": repository["uri"], "vcsKind": vcs["kind"]},
            "candidate": {
                "revision": candidate["nativeRevision"],
                "contentDigest": {"sha256": content_digest.removeprefix("sha256:")},
            },
            "base": {
                "revision": base_revision,
                "reference": target["name"],
            },
            "governance": {
                "scopeId": governance["scopeId"],
                "revision": governance["revision"],
                "digest": {"sha256": governance["digest"].removeprefix("sha256:")},
            },
            "receipt": receipt,
            "event": event,
            "journal": {
                "integrityStatus": integrity.get("status"),
                "verifiedHeadPosition": event_record.get("verifiedHeadPosition"),
                "verifiedHeadDigest": event_record.get("verifiedHeadDigest"),
            },
        },
    }
    attestation.validate_statement(statement)
    return statement


def _outside(path: Path, repository_root: Path, label: str) -> Path:
    path = path.expanduser().resolve()
    try:
        path.relative_to(repository_root)
    except ValueError:
        pass
    else:
        raise JournalAttestationError(label + " must be outside the repository")
    return path


def sign_journal_receipt(
    *,
    database: str | Path,
    scope_id: str,
    position: int,
    private_key: str | Path,
    key_id: str,
    openssl_path: str | Path,
    openssl_sha256: str,
    trust_policy_path: str | Path,
    trust_policy_sha256: str,
    repository_root: str | Path,
    output_path: str | Path,
    required_role: str = "governance-authority",
) -> dict:
    repository_root = Path(repository_root).expanduser().resolve()
    key_path = _outside(Path(private_key), repository_root, "private key")
    policy_path = _outside(Path(trust_policy_path), repository_root, "trust policy")
    output = _outside(Path(output_path), repository_root, "output envelope")
    openssl = _outside(Path(openssl_path), repository_root, "OpenSSL executable")
    if not openssl.is_file() or not os.access(openssl, os.X_OK):
        raise JournalAttestationError("pinned OpenSSL executable is missing or not executable")
    actual_openssl_digest = hashlib.sha256(openssl.read_bytes()).hexdigest()
    if actual_openssl_digest != openssl_sha256:
        raise JournalAttestationError("OpenSSL executable digest does not match the pin")
    if not key_path.is_file():
        raise JournalAttestationError("private key file does not exist")
    if stat.S_IMODE(key_path.stat().st_mode) & 0o077:
        raise JournalAttestationError("private key must not be accessible by group or other users (use mode 0600)")
    if output.exists():
        raise FileExistsError("output envelope already exists; refusing to overwrite")

    database_path = _outside(Path(database), repository_root, "journal database")
    journal = Journal(database_path)
    event_record = journal.event_at(scope_id, position)
    if event_record is None:
        raise JournalAttestationError("journal event position does not exist")
    statement = build_journal_receipt_statement(event_record)
    payload = attestation.canonical_statement_bytes(statement)
    pae = attestation.dsse_pae(attestation.DSSE_PAYLOAD_TYPE, payload)

    with tempfile.TemporaryDirectory(prefix="govcheck-journal-sign-") as directory:
        root = Path(directory)
        message_file = root / "pae.bin"
        signature_file = root / "signature.bin"
        message_file.write_bytes(pae)
        signed = subprocess.run(
            [str(openssl), "pkeyutl", "-sign", "-rawin", "-inkey", str(key_path),
             "-in", str(message_file), "-out", str(signature_file)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, timeout=30, shell=False,
        )
        if signed.returncode != 0:
            detail = signed.stderr.decode("utf-8", errors="replace").strip()
            raise JournalAttestationError("OpenSSL signing failed: " + (detail or "non-zero exit"))
        envelope = attestation.build_dsse_envelope(statement, [{
            "keyid": key_id,
            "sig": base64.b64encode(signature_file.read_bytes()).decode("ascii"),
        }])

    try:
        from govcheck import attestation_verify
    except ImportError:
        import attestation_verify
    verified = attestation_verify.verify_dsse_envelope(
        envelope, policy_path, trust_policy_sha256, repository_root,
        required_role=required_role,
        expected_candidate_revision=statement["predicate"]["candidate"]["revision"],
        expected_governance_revision=statement["predicate"]["governance"]["revision"],
        expected_scope_id=statement["predicate"]["governance"]["scopeId"],
        expected_base_revision=statement["predicate"]["base"]["revision"],
        expected_content_sha256=statement["predicate"]["candidate"]["contentDigest"]["sha256"],
        expected_predicate_type=PREDICATE_TYPE,
    )
    if verified.get("status") != "verified":
        raise JournalAttestationError("self-verification of signed receipt failed: " + str(verified.get("reason", verified.get("status"))))

    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".govcheck-receipt-", dir=str(output.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(envelope, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp_name, 0o644)
        os.link(temp_name, output)  # atomic no-overwrite publication
        os.unlink(temp_name)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return envelope


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Export a canonical journal receipt as a locally signed DSSE envelope.")
    parser.add_argument("--database", required=True)
    parser.add_argument("--scope-id", required=True)
    parser.add_argument("--position", type=int, required=True)
    parser.add_argument("--private-key", required=True)
    parser.add_argument("--key-id", required=True)
    parser.add_argument("--openssl", required=True)
    parser.add_argument("--openssl-sha256", required=True)
    parser.add_argument("--trust-policy", required=True)
    parser.add_argument("--trust-policy-sha256", required=True)
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--required-role", default="governance-authority")
    args = parser.parse_args(argv)
    try:
        sign_journal_receipt(
            database=args.database, scope_id=args.scope_id, position=args.position,
            private_key=args.private_key, key_id=args.key_id,
            openssl_path=args.openssl, openssl_sha256=args.openssl_sha256,
            trust_policy_path=args.trust_policy, trust_policy_sha256=args.trust_policy_sha256,
            repository_root=args.repository_root, output_path=args.output,
            required_role=args.required_role,
        )
        print("signed journal receipt written: " + args.output)
        return 0
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired, JournalError, JournalAttestationError) as exc:
        print("journal receipt signing failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
