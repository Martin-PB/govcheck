"""Durable journal receipt integration for verified acceptance decisions.

The journal is optional for deployments that have not explicitly initialized a
scope. Once any journal setting is present, all settings and genesis bindings
are required; incomplete configuration fails closed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

try:
    from govcheck.journal import Journal, JournalError, canonical_json_bytes
except ImportError:  # standalone GovCheck installation
    from journal import Journal, JournalError, canonical_json_bytes


CONFIG_KEYS = (
    "GOVCHECK_JOURNAL_DB",
    "GOVCHECK_JOURNAL_SCOPE_ID",
    "GOVCHECK_JOURNAL_AUTHORITY_REVISION",
)


class AcceptanceJournalError(Exception):
    pass


def append_verified_decision(env: dict[str, str], gate_payload: dict[str, Any]) -> dict[str, Any] | None:
    """Append a receipt for a verified PASS/accepted-with-risk decision."""
    configured = [bool(env.get(key, "").strip()) for key in CONFIG_KEYS]
    if not any(configured):
        return None
    missing = [key for key, present in zip(CONFIG_KEYS, configured) if not present]
    if missing:
        raise AcceptanceJournalError("partial journal configuration; missing " + ", ".join(missing))

    db_path = Path(env["GOVCHECK_JOURNAL_DB"]).expanduser().resolve()
    git_dir = Path(env.get("GIT_DIR", "")).expanduser().resolve()
    if not env.get("GIT_DIR"):
        raise AcceptanceJournalError("GIT_DIR is required when acceptance journal integration is enabled")
    try:
        db_path.relative_to(git_dir)
    except ValueError:
        pass
    else:
        raise AcceptanceJournalError("journal database must be installed outside the Git repository")

    scope_id = env["GOVCHECK_JOURNAL_SCOPE_ID"]
    expected_scope = env.get("GOVCHECK_SCOPE_ID", "")
    if scope_id != expected_scope:
        raise AcceptanceJournalError("journal scope does not match the pinned gate scope")

    decision_id = gate_payload.get("decision_id")
    authority = gate_payload.get("authority_principal") or None
    policy_digest = gate_payload.get("policy_digest")
    evidence_digest = gate_payload.get("evidence_digest")
    if not all(isinstance(value, str) and value.strip() for value in (decision_id, policy_digest, evidence_digest)):
        raise AcceptanceJournalError("gate result is missing its decision or digest bindings")
    result = gate_payload.get("result")
    if result not in {"pass", "accepted-with-risk", "fail", "unknown", "conflict"}:
        raise AcceptanceJournalError("unsupported gate result for journal receipt: " + repr(result))

    journal = Journal(db_path)
    genesis = journal.scope_info(scope_id)
    expected_authority = env.get("GOVCHECK_JOURNAL_AUTHORITY_ID", authority or "")
    if not expected_authority:
        raise AcceptanceJournalError("GOVCHECK_JOURNAL_AUTHORITY_ID is required to journal an unauthenticated gate attempt")
    if genesis["authorityId"] != expected_authority:
        raise AcceptanceJournalError("journal genesis authority does not match the configured authority pin")
    if authority and authority != expected_authority:
        raise AcceptanceJournalError("verified decision signer does not match the journal authority pin")
    if genesis["authorityRevision"] != env["GOVCHECK_JOURNAL_AUTHORITY_REVISION"]:
        raise AcceptanceJournalError("journal genesis authority revision does not match the configured pin")
    if genesis["governanceRevision"] != env.get("GOVCHECK_GOVERNANCE_REVISION", ""):
        raise AcceptanceJournalError("journal genesis governance revision does not match the gate")

    payload = {
        "decisionId": decision_id,
        "decisionResult": result,
        "authorityPrincipal": authority,
        "verification": "authenticated-authority" if authority else "unverified-gate-attempt",
        "reason": gate_payload.get("reason", ""),
        "policyDigest": policy_digest,
        "repositoryId": gate_payload["repository_id"],
        "candidateRevision": gate_payload["candidate"],
        "baseRevision": gate_payload["base"],
        "ref": gate_payload["ref"],
        "evidenceDigest": evidence_digest,
        "governanceRevision": env["GOVCHECK_GOVERNANCE_REVISION"],
        "scopeId": scope_id,
        "riskAcceptance": gate_payload.get("risk_acceptance"),
    }
    idempotency_key = "acceptance-decision:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    event_id = "acceptance-gate-result:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    head = journal.head(scope_id)
    result = journal.append(
        scope_id=scope_id,
        expected_position=head["position"],
        expected_digest=head["digest"],
        event_id=event_id,
        event_type="govcheck.acceptance.gate-result/v1",
        schema_version="1",
        payload=payload,
        idempotency_key=idempotency_key,
        actor_id=authority,
    )
    if result.get("status") != "committed":
        raise AcceptanceJournalError("journal append did not commit: " + str(result.get("reason", result.get("status"))))
    return result["receipt"]
