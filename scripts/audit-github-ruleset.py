#!/usr/bin/env python3
"""Read-only audit of a GitHub repository ruleset.

This reports the effective configuration returned by GitHub's public REST API.
It does not modify repository settings and does not prove that a trusted
acceptance check actually rejects a protected-ref update.
"""
from __future__ import annotations

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_REPOSITORY = "Martin-PB/govcheck"
DEFAULT_RULESET_ID = "28251664"
API_VERSION = "2022-11-28"


class RulesetAuditError(ValueError):
    pass


def _rule_map(document: dict) -> dict[str, dict]:
    rules = document.get("rules")
    if not isinstance(rules, list):
        raise RulesetAuditError("ruleset rules must be an array")
    result = {}
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("type"), str):
            raise RulesetAuditError("ruleset contains a malformed rule")
        result[rule["type"]] = rule
    return result


def audit_ruleset(
    document: dict,
    *,
    repository: str = DEFAULT_REPOSITORY,
    ruleset_id: str | int = DEFAULT_RULESET_ID,
    expected_approvals: int = 0,
) -> dict:
    if not isinstance(document, dict):
        raise RulesetAuditError("ruleset response must be an object")
    if document.get("id") != int(ruleset_id):
        raise RulesetAuditError("ruleset ID does not match the requested ID")
    if document.get("source") != repository:
        raise RulesetAuditError("ruleset source does not match the requested repository")

    findings = []
    if document.get("enforcement") != "active":
        findings.append({"kind": "ruleset-not-active", "actual": document.get("enforcement")})

    conditions = document.get("conditions")
    ref_condition = conditions.get("ref_name") if isinstance(conditions, dict) else None
    includes = ref_condition.get("include", []) if isinstance(ref_condition, dict) else []
    default_branch_scoped = "~DEFAULT_BRANCH" in includes
    if not default_branch_scoped:
        findings.append({
            "kind": "default-branch-not-explicitly-protected",
            "include": includes,
        })

    rules = _rule_map(document)
    if "deletion" not in rules:
        findings.append({"kind": "branch-deletion-not-blocked"})
    if "non_fast_forward" not in rules:
        findings.append({"kind": "force-push-not-blocked"})

    pr_rule = rules.get("pull_request")
    pr_parameters = pr_rule.get("parameters", {}) if isinstance(pr_rule, dict) else {}
    pr_required = isinstance(pr_rule, dict)
    if not pr_required:
        findings.append({"kind": "pull-request-not-required"})
    approval_count = pr_parameters.get("required_approving_review_count")
    if approval_count != expected_approvals:
        findings.append({
            "kind": "approval-count-mismatch",
            "expected": expected_approvals,
            "actual": approval_count,
        })

    bypass_actors = document.get("bypass_actors")
    if not isinstance(bypass_actors, list):
        findings.append({"kind": "bypass-actors-malformed"})
        bypass_actors = []
    elif bypass_actors:
        findings.append({"kind": "bypass-actors-configured", "actors": bypass_actors})
    if document.get("current_user_can_bypass") != "never":
        findings.append({
            "kind": "current-user-bypass-not-prohibited",
            "actual": document.get("current_user_can_bypass"),
        })

    required_rule = rules.get("required_status_checks")
    required_parameters = required_rule.get("parameters", {}) if isinstance(required_rule, dict) else {}
    required_checks = required_parameters.get("required_status_checks", [])
    if not isinstance(required_checks, list):
        findings.append({"kind": "required-status-checks-malformed"})
        required_checks = []
    if required_checks:
        findings.append({
            "kind": "required-check-liveness-unverified",
            "checks": required_checks,
            message: "Required contexts need a trusted source and path/liveness mapping.",
        })

    acceptance_gate = "not-established"
    gate_reasons = []
    if not pr_required:
        gate_reasons.append("pull requests are not required")
    if not required_checks:
        gate_reasons.append("no required status checks are configured")
    gate_reasons.append("ruleset configuration alone does not demonstrate a trusted GovCheck decision or a real protected-ref refusal")
    return {
        "format": "govcheck.github-ruleset-audit/v1",
        "repository": repository,
        "ruleset_id": int(ruleset_id),
        "ruleset_name": document.get("name"),
        "enforcement": document.get("enforcement"),
        "default_branch_scoped": default_branch_scoped,
        "pull_request_required": pr_required,
        "required_approving_review_count": approval_count,
        "required_status_checks": required_checks,
        "required_check_liveness": (
            "not_applicable_no_required_status_checks"
            if not required_checks else "unverified_requires_trusted_source_and_path_mapping"
        ),
        "bypass_actors": bypass_actors,
        "current_user_can_bypass": document.get("current_user_can_bypass"),
        "deletion_blocked": "deletion" in rules,
        "force_push_blocked": "non_fast_forward" in rules,
        "effective_govcheck_acceptance_gate": acceptance_gate,
        "gate_reasons": gate_reasons,
        "finding_count": len(findings),
        "findings": findings,
        "limitations": [
            "Read-only API audit; no ruleset, secret, app, or key is changed.",
            "A ruleset snapshot does not prove a trusted status source or a real protected-ref rejection.",
            "No required status checks are currently configured in the inspected ruleset.",
        ],
    }


def fetch_ruleset(repository: str, ruleset_id: str | int, *, opener=urlopen, timeout: int = 20) -> dict:
    url = f"https://api.github.com/repos/{repository}/rulesets/{ruleset_id}"
    request = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "GovCheck-read-only-ruleset-audit",
    })
    try:
        with opener(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RulesetAuditError("GitHub ruleset API request failed: " + str(exc)) from exc


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--ruleset-id", default=DEFAULT_RULESET_ID)
    parser.add_argument("--expected-approvals", type=int, default=0)
    args = parser.parse_args(argv)
    try:
        document = fetch_ruleset(args.repository, args.ruleset_id)
        report = audit_ruleset(
            document,
            repository=args.repository,
            ruleset_id=args.ruleset_id,
            expected_approvals=args.expected_approvals,
        )
    except RulesetAuditError as exc:
        print("GitHub ruleset audit could not complete: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 1 if report["finding_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
