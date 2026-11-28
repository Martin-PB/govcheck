"""Post-receive receipts for actual protected Git ref updates.

Unlike pre-receive, post-receive runs after refs have been updated. A receipt
failure is therefore an alert/recovery condition, never a claim that the push
was rejected or rolled back.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
from pathlib import Path

try:
    from govcheck.journal import Journal, JournalError, canonical_json_bytes
except ImportError:
    from journal import Journal, JournalError, canonical_json_bytes

OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
GATE_EVENT_TYPE = "govcheck.acceptance.gate-result/v1"
PUBLICATION_EVENT_TYPE = "govcheck.git.ref-publication/v1"


def _protected(ref: str, env: dict[str, str]) -> bool:
    patterns = [p.strip() for p in re.split(r"[,\s]+", env.get("GOVCHECK_PROTECTED_REFS", "refs/heads/main")) if p.strip()]
    return any(fnmatch.fnmatchcase(ref, pattern) for pattern in patterns)


def _append(journal: Journal, scope_id: str, event_id: str, payload: dict, actor_id: str) -> dict:
    key = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    idempotency_key = "git-ref-publication:" + key
    existing = journal.receipt(scope_id, idempotency_key)
    if existing is not None:
        return existing
    event_id = "git-ref-publication:" + key
    for _ in range(3):
        head = journal.head(scope_id)
        result = journal.append(
            scope_id=scope_id,
            expected_position=head["position"],
            expected_digest=head["digest"],
            event_id=event_id,
            event_type=PUBLICATION_EVENT_TYPE,
            schema_version="1",
            payload=payload,
            idempotency_key=idempotency_key,
            actor_id=actor_id,
        )
        if result.get("status") == "committed":
            return result["receipt"]
        if result.get("status") not in {"stale", "unknown"}:
            raise JournalError(result.get("status", "unknown"), str(result.get("reason", "publication receipt append failed")))
    raise JournalError("unknown", "publication receipt append did not commit after bounded retries")


def run_post_receive(input_text: str, env=None) -> tuple[int, list[str]]:
    env = dict(os.environ if env is None else env)
    keys = (
        "GOVCHECK_JOURNAL_DB", "GOVCHECK_JOURNAL_SCOPE_ID", "GOVCHECK_EXPECTED_REPOSITORY_ID",
        "GOVCHECK_JOURNAL_AUTHORITY_ID", "GOVCHECK_JOURNAL_AUTHORITY_REVISION", "GOVCHECK_GOVERNANCE_REVISION",
    )
    configured = [bool(env.get(key, "").strip()) for key in keys]
    if not any(configured):
        return 0, ["publication receipt journal is not configured"]
    missing = [key for key, present in zip(keys, configured) if not present]
    if missing:
        return 1, ["error: partial publication journal configuration; missing " + ", ".join(missing)]
    if not env.get("GIT_DIR"):
        return 1, ["error: GIT_DIR is required for publication receipt journaling"]

    git_dir = Path(env["GIT_DIR"]).expanduser().resolve()
    db_path = Path(env["GOVCHECK_JOURNAL_DB"]).expanduser().resolve()
    try:
        db_path.relative_to(git_dir)
    except ValueError:
        pass
    else:
        return 1, ["error: journal database must be outside the bare repository"]

    scope_id = env["GOVCHECK_JOURNAL_SCOPE_ID"]
    messages = []
    failed = False
    try:
        journal = Journal(db_path)
        genesis = journal.scope_info(scope_id)
        if genesis["authorityId"] != env["GOVCHECK_JOURNAL_AUTHORITY_ID"]:
            raise JournalError("journal genesis authority does not match the configured pin")
        if genesis["authorityRevision"] != env["GOVCHECK_JOURNAL_AUTHORITY_REVISION"]:
            raise JournalError("journal genesis authority revision does not match the configured pin")
        if genesis["governanceRevision"] != env["GOVCHECK_GOVERNANCE_REVISION"]:
            raise JournalError("journal genesis governance revision does not match the configured pin")
        for line_number, line in enumerate(input_text.splitlines(), start=1):
            parts = line.split()
            if len(parts) != 3:
                messages.append("error: malformed post-receive input on line " + str(line_number))
                failed = True
                continue
            old_oid, new_oid, ref = parts
            if not OID_RE.fullmatch(old_oid) or not OID_RE.fullmatch(new_oid) or not ref.startswith("refs/"):
                messages.append("error: invalid object ID or ref on line " + str(line_number))
                failed = True
                continue
            if not _protected(ref, env):
                continue

            gate = journal.find_latest_event(scope_id, GATE_EVENT_TYPE, {
                "repositoryId": env["GOVCHECK_EXPECTED_REPOSITORY_ID"],
                "candidateRevision": new_oid,
                "baseRevision": old_oid,
                "ref": ref,
            })
            gate_event = gate["event"] if gate else None
            gate_payload = gate_event.get("payload", {}) if isinstance(gate_event, dict) else {}
            linked = bool(
                gate
                and gate_payload.get("decisionResult") in {"pass", "accepted-with-risk"}
                and gate_payload.get("verification") == "authenticated-authority"
                and isinstance(gate_payload.get("authorityPrincipal"), str)
                and gate_payload.get("authorityPrincipal")
            )
            payload = {
                "repositoryId": env["GOVCHECK_EXPECTED_REPOSITORY_ID"],
                "scopeId": scope_id,
                "baseRevision": old_oid,
                "candidateRevision": new_oid,
                "ref": ref,
                "publication": "linked-to-verified-acceptance" if linked else "published-without-verified-acceptance",
                "gateReceipt": ({"position": gate["position"], "eventDigest": gate["eventDigest"]} if gate else None),
                "decisionId": gate_payload.get("decisionId") if gate else None,
                "vcsProvenance": gate_payload.get("vcsProvenance") if gate else None,
            }
            try:
                receipt = _append(journal, scope_id, "", payload, "system:govcheck-git-post-receive")
                if linked:
                    messages.append("receipt: published " + ref + " " + new_oid + " (journal position " + str(receipt["position"]) + ")")
                else:
                    messages.append("warning: ref already published without a matching authenticated acceptance receipt: " + ref + " " + new_oid)
                    failed = True
            except JournalError as exc:
                messages.append("error: ref already published but journal receipt failed for " + ref + ": " + str(exc))
                failed = True
    except (OSError, ValueError, TypeError, JournalError) as exc:
        messages.append("error: publication receipt processing failed after ref update: " + str(exc))
        failed = True
    return (1 if failed else 0), messages


def main() -> int:
    import sys
    code, messages = run_post_receive(sys.stdin.read(), os.environ)
    for message in messages:
        print(message, file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
