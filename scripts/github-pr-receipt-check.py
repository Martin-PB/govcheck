#!/usr/bin/env python3
"""Trusted GitHub Actions check source for signed GovCheck acceptance receipts.

This script never executes candidate code. It hashes the checked-out candidate
snapshot and verifies a detached DSSE receipt with the trusted GovCheck code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CHECK_NAME = "GovCheck authenticated acceptance receipt"
PREDICATE_TYPE = "urn:govcheck:attestation:journal-receipt:v1"
COMMAND = "/govcheck-receipt"
OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


class CheckError(Exception):
    pass


def _reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CheckError("duplicate JSON object key: " + key)
        result[key] = value
    return result


def extract_envelope_comment(body: str) -> dict:
    if COMMAND not in body.splitlines():
        raise CheckError("comment must contain the standalone command /govcheck-receipt")
    matches = list(re.finditer(r"```json\s*(\{.*?\})\s*```", body, re.DOTALL))
    if len(matches) != 1:
        raise CheckError("comment must contain exactly one fenced JSON DSSE envelope")
    match = matches[0]
    try:
        envelope = json.loads(match.group(1), object_pairs_hook=_reject_duplicate_pairs,
                              parse_constant=lambda value: (_ for _ in ()).throw(CheckError("invalid JSON constant " + value)))
    except (json.JSONDecodeError, ValueError) as exc:
        raise CheckError("comment DSSE envelope is not strict JSON: " + str(exc)) from exc
    if not isinstance(envelope, dict):
        raise CheckError("DSSE envelope must be a JSON object")
    return envelope


def validate_pr_bindings(statement: dict, pr: dict, candidate_content_sha256: str, config: dict[str, str]) -> dict:
    predicate = statement.get("predicate")
    if statement.get("predicateType") != PREDICATE_TYPE or not isinstance(predicate, dict):
        raise CheckError("statement is not a GovCheck journal-receipt attestation")
    event = predicate.get("event")
    receipt = predicate.get("receipt")
    repository = predicate.get("repository")
    candidate = predicate.get("candidate")
    base = predicate.get("base")
    governance = predicate.get("governance")
    if not all(isinstance(value, dict) for value in (event, receipt, repository, candidate, base, governance)):
        raise CheckError("receipt statement is missing required bindings")
    payload = event.get("payload")
    provenance = payload.get("vcsProvenance") if isinstance(payload, dict) else None
    if not isinstance(provenance, dict):
        raise CheckError("signed event has no typed VCS provenance")
    pr_head = pr.get("head", {})
    pr_base = pr.get("base", {})
    head_sha = pr_head.get("sha")
    base_sha = pr_base.get("sha")
    head_ref = pr_head.get("ref")
    head_repo = pr_head.get("repo", {})
    base_ref = pr_base.get("ref")
    base_repo = pr_base.get("repo", {})
    expected_base_ref = config.get("GOVCHECK_PROTECTED_BASE_REF", "main")
    if pr.get("state") != "open":
        raise CheckError("pull request is not open")
    if head_repo.get("full_name") != config.get("GITHUB_REPOSITORY") or base_repo.get("full_name") != config.get("GITHUB_REPOSITORY"):
        raise CheckError("fork pull requests are not enabled for this required check")
    if base_ref != expected_base_ref:
        raise CheckError("pull request base branch does not match the protected branch pin")
    if not isinstance(head_sha, str) or not OID_RE.fullmatch(head_sha):
        raise CheckError("pull request head SHA is malformed")
    if not isinstance(base_sha, str) or not OID_RE.fullmatch(base_sha):
        raise CheckError("pull request base SHA is malformed")
    if not isinstance(head_ref, str) or not head_ref:
        raise CheckError("pull request head branch name is missing")
    target_ref = "refs/heads/" + head_ref

    if receipt.get("scopeId") != config.get("GOVCHECK_JOURNAL_SCOPE_ID"):
        raise CheckError("durable journal receipt scope does not match the configured scope")
    if candidate.get("revision") != head_sha:
        raise CheckError("signed candidate revision does not equal the current PR head")
    if base.get("revision") != base_sha:
        raise CheckError("signed base revision does not equal the current PR base")
    if base.get("reference") != target_ref:
        raise CheckError("signed target ref does not equal the PR head branch")
    if candidate.get("contentDigest") != {"sha256": candidate_content_sha256}:
        raise CheckError("signed candidate content digest does not match the checked-out PR tree")
    if repository.get("uri") != config.get("GOVCHECK_REPOSITORY_URI") or repository.get("vcsKind") != "git":
        raise CheckError("signed repository URI or VCS kind does not match the configured repository")
    if governance.get("scopeId") != config.get("GOVCHECK_JOURNAL_SCOPE_ID"):
        raise CheckError("signed governance scope does not match the configured journal scope")
    if governance.get("revision") != config.get("GOVCHECK_GOVERNANCE_REVISION"):
        raise CheckError("signed governance revision does not match the configured revision")
    if payload.get("candidateRevision") != head_sha or payload.get("baseRevision") != base_sha or payload.get("ref") != target_ref:
        raise CheckError("gate event candidate/base/ref fields do not match the current PR")
    if payload.get("repositoryId") != config.get("GOVCHECK_EXPECTED_REPOSITORY_ID"):
        raise CheckError("signed repository identity does not match the configured repository ID")
    if governance.get("digest") != {"sha256": str(config.get("GOVCHECK_GOVERNANCE_DIGEST", "")).removeprefix("sha256:")}:
        raise CheckError("signed governance digest does not match the configured governance digest")
    if payload.get("governanceRevision") != config.get("GOVCHECK_GOVERNANCE_REVISION"):
        raise CheckError("gate event governance revision does not match the configured revision")
    if payload.get("policyDigest") != config.get("GOVCHECK_EXPECTED_POLICY_DIGEST"):
        raise CheckError("gate event policy digest does not match the configured policy pin")
    if event.get("eventType") != "govcheck.acceptance.gate-result/v1":
        raise CheckError("only a canonical gate-result event can satisfy this check")
    if payload.get("decisionResult") != "pass":
        raise CheckError("only an authenticated PASS decision can satisfy this required check")
    if payload.get("verification") != "authenticated-authority":
        raise CheckError("gate result was not verified as an authenticated authority decision")
    if payload.get("riskAcceptance") is not None:
        raise CheckError("risk-accepted outcomes require a separately configured check policy")
    principal = payload.get("authorityPrincipal")
    if not isinstance(principal, str) or not principal:
        raise CheckError("gate event has no authenticated authority principal")
    if provenance.get("candidate", {}).get("nativeRevision") != head_sha:
        raise CheckError("native VCS candidate does not match the PR head")
    if provenance.get("base", {}).get("nativeRevision") != base_sha:
        raise CheckError("native VCS base does not match the PR base")
    if provenance.get("target", {}).get("name") != target_ref:
        raise CheckError("native VCS target ref does not match the PR branch")
    return {"predicate": predicate, "principal": principal, "headSha": head_sha, "baseSha": base_sha}


def github_api(token: str, repository: str, method: str, endpoint: str, payload: dict | None = None) -> dict:
    url = "https://api.github.com/repos/" + repository + endpoint
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "GovCheck-acceptance-receipt-check",
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise CheckError("GitHub API " + method + " " + endpoint + " failed: " + str(exc.code) + " " + detail) from exc
    return json.loads(raw.decode("utf-8")) if raw else {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure_check_run(token: str, repository: str, head_sha: str, base_sha: str, pr_number: int, details_url: str) -> int:
    external_id = "govcheck-pr-" + str(pr_number) + "-base-" + base_sha
    existing = github_api(token, repository, "GET", "/commits/" + head_sha + "/check-runs?check_name=" + urllib.parse.quote(CHECK_NAME) + "&filter=latest&per_page=100")
    for run in existing.get("check_runs", []):
        if run.get("external_id") == external_id and run.get("status") == "in_progress":
            return run["id"]
    created = github_api(token, repository, "POST", "/check-runs", {
        "name": CHECK_NAME,
        "head_sha": head_sha,
        "status": "in_progress",
        "started_at": _now(),
        "external_id": external_id,
        "details_url": details_url,
        "output": {"title": "GovCheck acceptance receipt pending", "summary": "Awaiting a signed receipt bound to this exact head and base."},
    })
    return created["id"]


def complete_check_run(token: str, repository: str, check_run_id: int, conclusion: str, title: str, summary: str) -> None:
    github_api(token, repository, "PATCH", "/check-runs/" + str(check_run_id), {
        "status": "completed",
        "conclusion": conclusion,
        "completed_at": _now(),
        "output": {"title": title, "summary": summary[:60000]},
    })


def _load_pr(token: str, repository: str, number: int) -> dict:
    return github_api(token, repository, "GET", "/pulls/" + str(number))


def _policy_path(trusted_root: Path, config: dict[str, str]) -> Path:
    relative = config.get("GOVCHECK_TRUST_POLICY_PATH", "").strip()
    if not relative:
        raise CheckError("GOVCHECK_TRUST_POLICY_PATH repository variable is required")
    path = (trusted_root / relative).resolve()
    try:
        path.relative_to(trusted_root.resolve())
    except ValueError:
        raise CheckError("trust policy path must remain inside the trusted checkout")
    return path


def verify_comment_event(event: dict, trusted_root: Path, candidate_root: Path, token: str, repository: str, config: dict[str, str], details_url: str) -> int:
    issue = event.get("issue", {})
    number = issue.get("number")
    if not isinstance(number, int) or not issue.get("pull_request"):
        raise CheckError("issue_comment event is not attached to a pull request")
    pr = _load_pr(token, repository, number)
    head_sha = pr.get("head", {}).get("sha", "")
    base_sha = pr.get("base", {}).get("sha", "")
    check_id = ensure_check_run(token, repository, head_sha, base_sha, number, details_url)
    try:
        body = event.get("comment", {}).get("body", "")
        envelope = extract_envelope_comment(body)
        from govcheck import attestation, attestation_verify, check
        _, statement = attestation.decode_dsse_envelope(envelope)
        content_digest = check.candidate_content_digest(candidate_root)
        bindings = validate_pr_bindings(statement, pr, content_digest, {**config, "GITHUB_REPOSITORY": repository})
        policy_path = _policy_path(trusted_root, config)
        policy_bytes = policy_path.read_bytes()
        policy_digest = hashlib.sha256(policy_bytes).hexdigest()
        pinned_policy_digest = config.get("GOVCHECK_TRUST_POLICY_SHA256", "")
        if not pinned_policy_digest or policy_digest != pinned_policy_digest:
            raise CheckError("trusted policy file digest does not match GOVCHECK_TRUST_POLICY_SHA256")
        verified = attestation_verify.verify_dsse_envelope(
            envelope, policy_path, policy_digest, candidate_root,
            required_role=config.get("GOVCHECK_REQUIRED_ROLE", "governance-authority"),
            expected_candidate_revision=head_sha,
            expected_governance_revision=config["GOVCHECK_GOVERNANCE_REVISION"],
            expected_scope_id=config["GOVCHECK_JOURNAL_SCOPE_ID"],
            expected_base_revision=base_sha,
            expected_content_sha256=content_digest,
            expected_predicate_type=PREDICATE_TYPE,
        )
        if verified.get("status") != "verified":
            raise CheckError("DSSE receipt verification failed: " + str(verified.get("reason", verified.get("status"))))
        signer_principals = [item.get("principalId") for item in verified.get("signers", [])]
        if bindings["principal"] not in signer_principals:
            raise CheckError("authenticated signer principal does not match the gate event authority principal")
        current = _load_pr(token, repository, number)
        if current.get("head", {}).get("sha") != head_sha or current.get("base", {}).get("sha") != base_sha or current.get("state") != "open":
            raise CheckError("PR head/base/state changed during receipt verification; submit a fresh receipt")
        complete_check_run(token, repository, check_id, "success", "Authenticated PASS bound to current PR",
                           "Verified a signed canonical journal receipt for the exact PR head/base, candidate content digest, repository, governance revision and authenticated authority.")
        return 0
    except Exception as exc:
        complete_check_run(token, repository, check_id, "failure", "GovCheck acceptance receipt rejected", str(exc))
        print("GovCheck receipt check failed: " + str(exc), file=sys.stderr)
        return 1


def invalidate_pr_event(event: dict, token: str, repository: str, details_url: str) -> int:
    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        return 0
    head_sha = pr.get("head", {}).get("sha", "")
    base_sha = pr.get("base", {}).get("sha", "")
    number = pr.get("number")
    if not isinstance(number, int) or not OID_RE.fullmatch(head_sha) or not OID_RE.fullmatch(base_sha):
        raise CheckError("pull_request_target event has malformed PR bindings")
    ensure_check_run(token, repository, head_sha, base_sha, number, details_url)
    print("GovCheck acceptance check is pending for this head/base until a matching signed receipt is submitted.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["verify", "invalidate"], required=True)
    parser.add_argument("--event-path", type=Path, required=True)
    parser.add_argument("--trusted-root", type=Path, required=True)
    parser.add_argument("--candidate-root", type=Path)
    args = parser.parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not repository:
        print("GITHUB_TOKEN and GITHUB_REPOSITORY are required", file=sys.stderr)
        return 1
    try:
        event = json.loads(args.event_path.read_text(encoding="utf-8"))
        details_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" + repository + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "")
        if args.mode == "invalidate":
            return invalidate_pr_event(event, token, repository, details_url)
        if args.candidate_root is None:
            raise CheckError("--candidate-root is required in verify mode")
        trusted_root = args.trusted_root.resolve()
        sys.path.insert(0, str(trusted_root))
        return verify_comment_event(event, trusted_root, args.candidate_root.resolve(), token, repository, dict(os.environ), details_url)
    except Exception as exc:
        print("GovCheck PR receipt workflow failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
