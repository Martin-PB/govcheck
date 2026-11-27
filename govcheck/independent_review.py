"""Detached independent-review predicate builder for GovCheck.

A review statement is evidence, not an authority decision. Reviewer identity is
intentionally absent from the predicate: it must be derived from the verified
DSSE signer and the external trust policy.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any

STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "urn:govcheck:attestation:independent-review:v1"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
OUTCOMES = {"accepted", "changes_requested"}


class IndependentReviewError(ValueError):
    """Raised when an independent-review predicate is malformed."""


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise IndependentReviewError(label + " must be a non-empty string")
    return value.strip()


def _strings(value: Any, label: str, *, non_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise IndependentReviewError(label + " must be an array of non-empty strings")
    result = [item.strip() for item in value]
    if non_empty and not result:
        raise IndependentReviewError(label + " must contain at least one item")
    if len(set(result)) != len(result):
        raise IndependentReviewError(label + " must not contain duplicates")
    return result


def _timestamp(value: Any) -> str:
    text = _text(value, "reviewed_on")
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IndependentReviewError("reviewed_on must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None:
        raise IndependentReviewError("reviewed_on must include a timezone")
    return text


def validate_predicate(predicate: dict) -> dict:
    """Validate and normalize a predicate payload (not its signature or trust)."""
    if not isinstance(predicate, dict):
        raise IndependentReviewError("predicate must be an object")
    required = {
        "schemaVersion", "candidateRevision", "candidateContentSha256",
        "baseRevision", "governanceRevision", "scopeId", "reviewedOn",
        "outcome", "claimsReviewed", "observations", "limitations",
    }
    if set(predicate) != required:
        missing = sorted(required - set(predicate))
        extra = sorted(set(predicate) - required)
        raise IndependentReviewError("predicate fields mismatch; missing=" + repr(missing) + " extra=" + repr(extra))
    if predicate["schemaVersion"] != "1":
        raise IndependentReviewError("schemaVersion must be '1'")
    digest = _text(predicate["candidateContentSha256"], "candidateContentSha256")
    if not HEX64_RE.fullmatch(digest):
        raise IndependentReviewError("candidateContentSha256 must be lowercase SHA-256")
    outcome = _text(predicate["outcome"], "outcome")
    if outcome not in OUTCOMES:
        raise IndependentReviewError("outcome must be accepted or changes_requested")
    return {
        "schemaVersion": "1",
        "candidateRevision": _text(predicate["candidateRevision"], "candidateRevision"),
        "candidateContentSha256": digest,
        "baseRevision": _text(predicate["baseRevision"], "baseRevision"),
        "governanceRevision": _text(predicate["governanceRevision"], "governanceRevision"),
        "scopeId": _text(predicate["scopeId"], "scopeId"),
        "reviewedOn": _timestamp(predicate["reviewedOn"]),
        "outcome": outcome,
        "claimsReviewed": _strings(predicate["claimsReviewed"], "claimsReviewed", non_empty=True),
        "observations": _strings(predicate["observations"], "observations"),
        "limitations": _strings(predicate["limitations"], "limitations", non_empty=True),
    }


def build_statement(
    *,
    repository_uri: str,
    candidate_revision: str,
    candidate_content_sha256: str,
    base_revision: str,
    governance_revision: str,
    scope_id: str,
    reviewed_on: str,
    outcome: str,
    claims_reviewed: list[str],
    observations: list[str],
    limitations: list[str],
) -> dict:
    """Build an in-toto Statement v1 with the independent-review predicate.

    reviewed_on is a reviewer-asserted timestamp, not trusted timestamp evidence.
    The reviewer principal is intentionally resolved from the DSSE signature and
    trust policy, never from a free-form field in this statement.
    """
    repository_uri = _text(repository_uri, "repository_uri")
    if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", repository_uri):
        raise IndependentReviewError("repository_uri must be an absolute URI")
    predicate = validate_predicate({
        "schemaVersion": "1",
        "candidateRevision": candidate_revision,
        "candidateContentSha256": candidate_content_sha256,
        "baseRevision": base_revision,
        "governanceRevision": governance_revision,
        "scopeId": scope_id,
        "reviewedOn": reviewed_on,
        "outcome": outcome,
        "claimsReviewed": claims_reviewed,
        "observations": observations,
        "limitations": limitations,
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
