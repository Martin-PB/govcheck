"""VCS-native provenance records for Git and Pijul journal payloads.

These records preserve native identities. Their optional content digests aid
snapshot comparison but do not assert semantic equivalence between VCSs.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

try:
    from govcheck.journal import canonical_json_bytes
except ImportError:
    from journal import canonical_json_bytes

GIT_OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class VcsProvenanceError(ValueError):
    pass


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VcsProvenanceError(label + " must be a non-empty string")
    if any(ord(ch) < 0x20 or 0xD800 <= ord(ch) <= 0xDFFF for ch in value):
        raise VcsProvenanceError(label + " contains a control character or invalid Unicode")
    return value


def _uri(value: str) -> str:
    value = _text(value, "repository_uri")
    parsed = urlparse(value)
    if not parsed.scheme:
        raise VcsProvenanceError("repository_uri must be an absolute URI")
    return value


def _digest(value: str, label: str) -> str:
    value = _text(value, label)
    if not SHA256_RE.fullmatch(value):
        raise VcsProvenanceError(label + " must be sha256:<64 lowercase hex>")
    return value


def _timestamp(value: str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    value = _text(value, "observed_at")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise VcsProvenanceError("observed_at must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise VcsProvenanceError("observed_at must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _change_set_digest(kind: str, native_ids: list[str]) -> str:
    material = {"vcsKind": kind, "nativeIds": native_ids}
    return "sha256:" + hashlib.sha256(canonical_json_bytes(material)).hexdigest()


def _base(base_revision: str | None, base_content_digest: str | None, kind: str) -> dict | None:
    if base_revision is None and base_content_digest is None:
        return None
    if base_revision is None or base_content_digest is None:
        raise VcsProvenanceError("base revision and content digest must be supplied together")
    if kind == "git" and not GIT_OID_RE.fullmatch(base_revision):
        raise VcsProvenanceError("Git base revision must be a lowercase SHA-1 or SHA-256 object ID")
    return {
        "nativeRevision": _text(base_revision, "base_revision"),
        "contentDigest": _digest(base_content_digest, "base_content_digest"),
    }


def build_git_provenance(
    *,
    repository_id: str,
    repository_uri: str,
    target_ref: str,
    candidate_commit: str,
    candidate_content_digest: str,
    base_commit: str | None,
    base_content_digest: str | None,
    governance_scope_id: str,
    governance_revision: str,
    governance_digest: str,
    adapter_id: str,
    adapter_version: str,
    observed_at: str | None = None,
) -> dict:
    """Build a record whose native candidate and change-set identity is a Git commit OID."""
    if not GIT_OID_RE.fullmatch(candidate_commit):
        raise VcsProvenanceError("Git candidate revision must be a lowercase SHA-1 or SHA-256 object ID")
    target_ref = _text(target_ref, "target_ref")
    if not target_ref.startswith("refs/"):
        raise VcsProvenanceError("Git target must be a full refs/... name")
    native_ids = [candidate_commit]
    return {
        "schemaVersion": "1",
        "repository": {"id": _text(repository_id, "repository_id"), "uri": _uri(repository_uri)},
        "vcs": {"kind": "git", "adapterId": _text(adapter_id, "adapter_id"), "adapterVersion": _text(adapter_version, "adapter_version")},
        "target": {"kind": "ref", "name": target_ref},
        "base": _base(base_commit, base_content_digest, "git"),
        "candidate": {"nativeRevision": candidate_commit, "contentDigest": _digest(candidate_content_digest, "candidate_content_digest")},
        "changeSet": {"nativeIds": native_ids, "digest": _change_set_digest("git", native_ids)},
        "governance": {
            "scopeId": _text(governance_scope_id, "governance_scope_id"),
            "revision": _text(governance_revision, "governance_revision"),
            "digest": _digest(governance_digest, "governance_digest"),
        },
        "observedAt": _timestamp(observed_at),
    }


def build_pijul_provenance(
    *,
    repository_id: str,
    repository_uri: str,
    target_channel: str,
    candidate_channel_hash: str,
    candidate_content_digest: str,
    base_channel_hash: str | None,
    base_content_digest: str | None,
    native_change_hashes: list[str],
    governance_scope_id: str,
    governance_revision: str,
    governance_digest: str,
    adapter_id: str,
    adapter_version: str,
    observed_at: str | None = None,
) -> dict:
    """Build a record preserving the native Pijul channel and change hashes as opaque IDs."""
    target_channel = _text(target_channel, "target_channel")
    candidate_channel_hash = _text(candidate_channel_hash, "candidate_channel_hash")
    if any(ch.isspace() for ch in candidate_channel_hash):
        raise VcsProvenanceError("Pijul channel hash must be an opaque token without whitespace")
    if not isinstance(native_change_hashes, list) or not native_change_hashes:
        raise VcsProvenanceError("native_change_hashes must be a non-empty list")
    native_ids = [_text(value, "native_change_hash") for value in native_change_hashes]
    if any(any(ch.isspace() for ch in value) for value in native_ids):
        raise VcsProvenanceError("Pijul change hashes must be opaque tokens without whitespace")
    if len(set(native_ids)) != len(native_ids):
        raise VcsProvenanceError("native_change_hashes must not contain duplicates")
    # Pijul change-set identity is a set of native change hashes; sort only
    # the serialized set for deterministic digesting, never to imply patch order.
    native_ids = sorted(native_ids)
    base = None
    if base_channel_hash is not None or base_content_digest is not None:
        if base_channel_hash is None or base_content_digest is None:
            raise VcsProvenanceError("base channel hash and content digest must be supplied together")
        base = {
            "nativeRevision": _text(base_channel_hash, "base_channel_hash"),
            "contentDigest": _digest(base_content_digest, "base_content_digest"),
        }
    return {
        "schemaVersion": "1",
        "repository": {"id": _text(repository_id, "repository_id"), "uri": _uri(repository_uri)},
        "vcs": {"kind": "pijul", "adapterId": _text(adapter_id, "adapter_id"), "adapterVersion": _text(adapter_version, "adapter_version")},
        "target": {"kind": "channel", "name": target_channel},
        "base": base,
        "candidate": {"nativeRevision": candidate_channel_hash, "contentDigest": _digest(candidate_content_digest, "candidate_content_digest")},
        "changeSet": {"nativeIds": native_ids, "digest": _change_set_digest("pijul", native_ids)},
        "governance": {
            "scopeId": _text(governance_scope_id, "governance_scope_id"),
            "revision": _text(governance_revision, "governance_revision"),
            "digest": _digest(governance_digest, "governance_digest"),
        },
        "observedAt": _timestamp(observed_at),
    }
