"""Local journal observer for Pijul-native channel provenance.

This adapter records an observation made by a trusted local collector. It is
not a Pijul remote acceptance hook and does not claim that a push was accepted.
"""
from __future__ import annotations

import hashlib
from typing import Any

try:
    from govcheck.journal import Journal, JournalError, canonical_json_bytes
except ImportError:
    from journal import Journal, JournalError, canonical_json_bytes

CONFIG_KEYS = (
    "GOVCHECK_JOURNAL_DB",
    "GOVCHECK_JOURNAL_SCOPE_ID",
    "GOVCHECK_JOURNAL_AUTHORITY_REVISION",
)
EVENT_TYPE = "govcheck.pijul.provenance-observed/v1"
OBSERVATION_KINDS = {"channel-state-observed", "push-attempt-observed"}


class PijulJournalError(Exception):
    pass


def _validate_record(env: dict[str, str], record: dict[str, Any]) -> None:
    if not isinstance(record, dict) or record.get("schemaVersion") != "1":
        raise PijulJournalError("provenance record must use schemaVersion 1")
    vcs = record.get("vcs")
    target = record.get("target")
    repository = record.get("repository")
    governance = record.get("governance")
    candidate = record.get("candidate")
    change_set = record.get("changeSet")
    if not isinstance(vcs, dict) or vcs.get("kind") != "pijul":
        raise PijulJournalError("record must preserve native Pijul identity")
    if not isinstance(target, dict) or target.get("kind") != "channel":
        raise PijulJournalError("Pijul provenance target must be a channel")
    if not isinstance(repository, dict) or repository.get("id") != env.get("GOVCHECK_EXPECTED_REPOSITORY_ID"):
        raise PijulJournalError("provenance repository ID does not match the pinned repository")
    if repository.get("uri") != env.get("GOVCHECK_REPOSITORY_URI"):
        raise PijulJournalError("provenance repository URI does not match the pinned URI")
    if not isinstance(governance, dict):
        raise PijulJournalError("provenance governance binding is missing")
    expected = {
        "scopeId": env.get("GOVCHECK_JOURNAL_SCOPE_ID"),
        "revision": env.get("GOVCHECK_GOVERNANCE_REVISION"),
        "digest": env.get("GOVCHECK_GOVERNANCE_DIGEST"),
    }
    for key, value in expected.items():
        if governance.get(key) != value:
            raise PijulJournalError("provenance governance binding mismatch: " + key)
    if not isinstance(candidate, dict) or not isinstance(candidate.get("nativeRevision"), str) or not candidate["nativeRevision"]:
        raise PijulJournalError("Pijul channel candidate identity is missing")
    if not isinstance(change_set, dict) or not isinstance(change_set.get("nativeIds"), list) or not change_set["nativeIds"]:
        raise PijulJournalError("Pijul native change-set identities are missing")
    if not isinstance(change_set.get("digest"), str) or not change_set["digest"].startswith("sha256:"):
        raise PijulJournalError("Pijul change-set digest is missing")


def append_pijul_observation(
    env: dict[str, str],
    provenance_record: dict[str, Any],
    *,
    observation_kind: str = "channel-state-observed",
) -> dict[str, Any] | None:
    """Append a Pijul-native local observation, never a remote acceptance claim."""
    configured = [bool(env.get(key, "").strip()) for key in CONFIG_KEYS]
    if not any(configured):
        return None
    missing = [key for key, present in zip(CONFIG_KEYS, configured) if not present]
    if missing:
        raise PijulJournalError("partial journal configuration; missing " + ", ".join(missing))
    if observation_kind not in OBSERVATION_KINDS:
        raise PijulJournalError("unsupported Pijul observation kind; remote acceptance is not represented here")

    required = (
        "GOVCHECK_JOURNAL_AUTHORITY_ID",
        "GOVCHECK_JOURNAL_AUTHORITY_REVISION",
        "GOVCHECK_GOVERNANCE_REVISION",
        "GOVCHECK_EXPECTED_REPOSITORY_ID",
        "GOVCHECK_REPOSITORY_URI",
        "GOVCHECK_GOVERNANCE_DIGEST",
    )
    missing = [key for key in required if not env.get(key, "").strip()]
    if missing:
        raise PijulJournalError("missing Pijul journal pins: " + ", ".join(missing))

    _validate_record(env, provenance_record)
    scope_id = env["GOVCHECK_JOURNAL_SCOPE_ID"]
    try:
        journal = Journal(env["GOVCHECK_JOURNAL_DB"])
        genesis = journal.scope_info(scope_id)
    except (JournalError, OSError) as exc:
        raise PijulJournalError("journal genesis verification failed: " + str(exc)) from exc
    if genesis["authorityId"] != env["GOVCHECK_JOURNAL_AUTHORITY_ID"]:
        raise PijulJournalError("journal genesis authority does not match the configured pin")
    if genesis["authorityRevision"] != env["GOVCHECK_JOURNAL_AUTHORITY_REVISION"]:
        raise PijulJournalError("journal genesis authority revision does not match the configured pin")
    if genesis["governanceRevision"] != env["GOVCHECK_GOVERNANCE_REVISION"]:
        raise PijulJournalError("journal genesis governance revision does not match the configured pin")

    payload = {
        "repositoryId": env["GOVCHECK_EXPECTED_REPOSITORY_ID"],
        "scopeId": scope_id,
        "governanceRevision": env["GOVCHECK_GOVERNANCE_REVISION"],
        "observationKind": observation_kind,
        "observationResult": "observed",
        "authorityStatus": "not-established-by-vcs-observation",
        "vcsProvenance": provenance_record,
    }
    try:
        digest = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
        key = "pijul-provenance:" + digest
        head = journal.head(scope_id)
        result = journal.append(
            scope_id=scope_id,
            expected_position=head["position"],
            expected_digest=head["digest"],
            event_id="pijul-provenance:" + digest,
            event_type=EVENT_TYPE,
            schema_version="1",
            payload=payload,
            idempotency_key=key,
            actor_id="system:govcheck-pijul-provenance-observer",
        )
    except JournalError as exc:
        raise PijulJournalError("Pijul provenance journal append failed: " + str(exc)) from exc
    if result.get("status") != "committed":
        raise PijulJournalError("Pijul provenance receipt did not commit: " + str(result.get("reason", result.get("status"))))
    return result["receipt"]
