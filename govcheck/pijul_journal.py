"""Local journal observer for Pijul-native channel provenance.

This adapter records an observation made by a trusted local collector. It is
not a Pijul remote acceptance hook and does not claim that a push was accepted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
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
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
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
    if any(ch.isspace() for ch in candidate["nativeRevision"]):
        raise PijulJournalError("Pijul channel candidate identity must be an opaque token")
    if not isinstance(candidate.get("contentDigest"), str) or not SHA256_RE.fullmatch(candidate["contentDigest"]):
        raise PijulJournalError("Pijul candidate content digest is invalid")
    if not isinstance(change_set, dict) or not isinstance(change_set.get("nativeIds"), list) or not change_set["nativeIds"]:
        raise PijulJournalError("Pijul native change-set identities are missing")
    if not isinstance(change_set.get("digest"), str) or not SHA256_RE.fullmatch(change_set["digest"]):
        raise PijulJournalError("Pijul change-set digest is missing or invalid")
    native_ids = change_set["nativeIds"]
    if any(not isinstance(value, str) or not value or any(ch.isspace() for ch in value) for value in native_ids):
        raise PijulJournalError("Pijul native change hashes must be opaque tokens")
    if len(set(native_ids)) != len(native_ids):
        raise PijulJournalError("Pijul native change hashes must be unique")
    base = record.get("base")
    if base is not None:
        if not isinstance(base, dict) or not isinstance(base.get("nativeRevision"), str) or not base["nativeRevision"]:
            raise PijulJournalError("Pijul base channel binding is malformed")
        if not isinstance(base.get("contentDigest"), str) or not SHA256_RE.fullmatch(base["contentDigest"]):
            raise PijulJournalError("Pijul base content digest is invalid")


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
        "GOVCHECK_REPOSITORY_PATH",
        "GOVCHECK_GOVERNANCE_DIGEST",
    )
    missing = [key for key in required if not env.get(key, "").strip()]
    if missing:
        raise PijulJournalError("missing Pijul journal pins: " + ", ".join(missing))

    _validate_record(env, provenance_record)
    repository_path = Path(env["GOVCHECK_REPOSITORY_PATH"]).expanduser().resolve()
    db_path = Path(env["GOVCHECK_JOURNAL_DB"]).expanduser().resolve()
    try:
        db_path.relative_to(repository_path)
    except ValueError:
        pass
    else:
        raise PijulJournalError("journal database must be outside the Pijul working tree")
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
        integrity = journal.verify(scope_id)
        if integrity.get("status") != "valid":
            raise PijulJournalError("journal verification failed before idempotent lookup")
        existing = journal.receipt(scope_id, key)
        if existing is not None:
            return existing
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

def _reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key: " + key)
        result[key] = value
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Append a Pijul-native local provenance observation to the GovCheck journal.")
    parser.add_argument("--provenance-json", type=Path, required=True, help="trusted adapter-produced provenance record, stored outside the Pijul worktree")
    parser.add_argument("--observation-kind", choices=sorted(OBSERVATION_KINDS), default="channel-state-observed")
    args = parser.parse_args(argv)
    env = dict(os.environ)
    try:
        repository_path = Path(env["GOVCHECK_REPOSITORY_PATH"]).expanduser().resolve()
        source_path = args.provenance_json.expanduser().resolve()
        if not source_path.is_file():
            raise PijulJournalError("provenance JSON file does not exist")
        try:
            source_path.relative_to(repository_path)
        except ValueError:
            pass
        else:
            raise PijulJournalError("provenance JSON must be outside the Pijul working tree")
        try:
            record = json.loads(source_path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_pairs,
                                parse_constant=lambda value: (_ for _ in ()).throw(ValueError("invalid JSON constant " + value)))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise PijulJournalError("cannot read strict provenance JSON: " + str(exc)) from exc
        receipt = append_pijul_observation(env, record, observation_kind=args.observation_kind)
        if receipt is None:
            raise PijulJournalError("journal is not configured; no provenance receipt was written")
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, KeyError, PijulJournalError, ValueError) as exc:
        print("pijul provenance observation failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
