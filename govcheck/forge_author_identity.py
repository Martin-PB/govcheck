"""Detached forge-author identity assertion for GovCheck.

The predicate is signed by a trusted forge identity provider. The asserted
author is not inferred from Git commit metadata or a free-form reviewer field.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "urn:govcheck:attestation:forge-author-identity:v1"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


class ForgeAuthorIdentityError(ValueError):
    """Raised when a forge-author identity predicate is malformed."""


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ForgeAuthorIdentityError(label + " must be a non-empty string")
    return value.strip()


def _uri(value: Any, label: str) -> str:
    text = _text(value, label)
    parsed = urlparse(text)
    if not parsed.scheme or (parsed.scheme in {"http", "https"} and not parsed.netloc):
        raise ForgeAuthorIdentityError(label + " must be an absolute URI")
    return text


def _timestamp(value: Any) -> str:
    text = _text(value, "assertedOn")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ForgeAuthorIdentityError("assertedOn must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise ForgeAuthorIdentityError("assertedOn must include a timezone")
    return text


def validate_predicate(predicate: dict) -> dict:
    if not isinstance(predicate, dict):
        raise ForgeAuthorIdentityError("predicate must be an object")
    required = {
        "schemaVersion", "candidateRevision", "candidateContentSha256",
        "baseRevision", "governanceRevision", "scopeId", "authorPrincipal",
        "sourceUri", "assertedOn",
    }
    if set(predicate) != required:
        raise ForgeAuthorIdentityError("predicate fields must match the forge-author-identity/v1 schema exactly")
    if predicate["schemaVersion"] != "1":
        raise ForgeAuthorIdentityError("schemaVersion must be '1'")
    digest = _text(predicate["candidateContentSha256"], "candidateContentSha256")
    if not HEX64_RE.fullmatch(digest):
        raise ForgeAuthorIdentityError("candidateContentSha256 must be lowercase SHA-256")
    return {
        "schemaVersion": "1",
        "candidateRevision": _text(predicate["candidateRevision"], "candidateRevision"),
        "candidateContentSha256": digest,
        "baseRevision": _text(predicate["baseRevision"], "baseRevision"),
        "governanceRevision": _text(predicate["governanceRevision"], "governanceRevision"),
        "scopeId": _text(predicate["scopeId"], "scopeId"),
        "authorPrincipal": _text(predicate["authorPrincipal"], "authorPrincipal"),
        "sourceUri": _uri(predicate["sourceUri"], "sourceUri"),
        "assertedOn": _timestamp(predicate["assertedOn"]),
    }


def build_statement(
    *,
    repository_uri: str,
    candidate_revision: str,
    candidate_content_sha256: str,
    base_revision: str,
    governance_revision: str,
    scope_id: str,
    author_principal: str,
    source_uri: str,
    asserted_on: str,
) -> dict:
    repository_uri = _uri(repository_uri, "repository_uri")
    predicate = validate_predicate({
        "schemaVersion": "1",
        "candidateRevision": candidate_revision,
        "candidateContentSha256": candidate_content_sha256,
        "baseRevision": base_revision,
        "governanceRevision": governance_revision,
        "scopeId": scope_id,
        "authorPrincipal": author_principal,
        "sourceUri": source_uri,
        "assertedOn": asserted_on,
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
