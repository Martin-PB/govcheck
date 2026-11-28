#!/usr/bin/env python3
"""Audit GitHub Actions workflow path-filter symmetry and reusable-workflow routing.

This deliberately parses only the small YAML subset used by GitHub Actions
trigger path filters and local reusable-workflow references. It does not claim
to be a general YAML parser or to prove semantic coverage of TLA+ categories.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")
EVENTS = ("pull_request", "push")
PATH_ITEM = re.compile(r"""^      -\s+(?:"([^"]+)"|'([^']+)'|([^\s#]+))\s*(?:#.*)?$""")
USES_ITEM = re.compile(r"""^\s{4}uses:\s*['"]?(\./\.github/workflows/[^\s'"]+\.ya?ml)['"]?\s*(?:#.*)?$""")
GLOB_POLICY_FILE = Path("docs/ci-routing-glob-policy.json")
GLOB_PATTERN = re.compile(r"[*?\[\]{}!]")
CATEGORY_POLICY_FILE = Path("docs/ci-routing-category-policy.json")
TLC_WORKFLOWS = {
    ".github/workflows/tla-lifecycle.yml",
    ".github/workflows/tla-assurance.yml",
    ".github/workflows/tla-authority.yml",
}


class WorkflowParseError(ValueError):
    pass


def _event_block(lines: list[str], event: str) -> list[str] | None:
    start = None
    for index, line in enumerate(lines):
        if line == f"  {event}:":
            start = index + 1
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start, len(lines)):
        line = lines[index]
        if line and not line.startswith(" ") and not line.startswith("#"):
            end = index
            break
        if re.match(r"^  [A-Za-z0-9_-]+:\s*(?:#.*)?$", line):
            end = index
            break
    return lines[start:end]


def _paths_for_event(lines: list[str], event: str, workflow: str) -> set[str] | None:
    block = _event_block(lines, event)
    if block is None:
        return None
    paths_index = None
    for index, line in enumerate(block):
        if re.match(r"^    paths-ignore\s*:", line):
            raise WorkflowParseError(
                f"{workflow}: {event}.paths-ignore is not supported by this audit; refusing to omit its routing semantics"
            )
        if re.match(r"^    paths\s*:", line):
            if not re.match(r"^    paths:\s*(?:#.*)?$", line):
                raise WorkflowParseError(
                    f"{workflow}: inline or malformed {event}.paths syntax is unsupported: {line.strip()}"
                )
            paths_index = index
            break
    if paths_index is None:
        return None
    result: set[str] = set()
    for line in block[paths_index + 1:]:
        if line and not line.startswith("      "):
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = PATH_ITEM.match(line)
        if not match:
            raise WorkflowParseError(f"{workflow}: unsupported entry under {event}.paths: {line.strip()}")
        value = next(group for group in match.groups() if group is not None)
        if value in result:
            raise WorkflowParseError(f"{workflow}: duplicate {event}.paths entry: {value}")
        result.add(value)
    return result


def inspect_workflow(path: Path, root: Path) -> dict:
    try:
        text = (root / path).read_text(encoding="utf-8")
    except OSError as exc:
        raise WorkflowParseError(f"{path}: {exc}") from exc
    lines = text.splitlines()
    result = {"workflow": path.as_posix(), "events": {}, "reusable_workflows": []}
    for event in EVENTS:
        paths = _paths_for_event(lines, event, path.as_posix())
        if paths is not None:
            result["events"][event] = sorted(paths)
    for line in lines:
        match = USES_ITEM.match(line)
        if match:
            target = match.group(1).removeprefix("./")
            if not (root / target).is_file():
                raise WorkflowParseError(f"{path}: reusable workflow does not exist: {target}")
            result["reusable_workflows"].append(target)
    result["reusable_workflows"] = sorted(set(result["reusable_workflows"]))
    return result


def load_glob_policy(root: Path) -> set[str]:
    path = root / GLOB_POLICY_FILE
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowParseError(f"glob policy cannot be read: {path}: {exc}") from exc
    if not isinstance(document, dict) or document.get("format") != "govcheck.ci-routing-glob-policy/v1":
        raise WorkflowParseError(f"{path}: unsupported or missing policy format")
    entries = document.get("patterns")
    if not isinstance(entries, list):
        raise WorkflowParseError(f"{path}: patterns must be an array")
    patterns: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise WorkflowParseError(f"{path}: each pattern entry must be an object")
        pattern = entry.get("pattern")
        rationale = entry.get("rationale")
        if not isinstance(pattern, str) or not pattern or not GLOB_PATTERN.search(pattern):
            raise WorkflowParseError(f"{path}: policy pattern must be a non-empty glob")
        if not isinstance(rationale, str) or not rationale.strip():
            raise WorkflowParseError(f"{path}: glob {pattern!r} requires a non-empty rationale")
        if pattern in patterns:
            raise WorkflowParseError(f"{path}: duplicate glob justification: {pattern}")
        patterns.add(pattern)
    return patterns


def _read_tla_set(model_text: str, set_name: str, model_path: Path) -> set[str]:
    pattern = re.compile(
        "^" + re.escape(set_name) + r"\s*==\s*\{(.*?)\}",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(model_text)
    if match is None:
        raise WorkflowParseError(f"{model_path}: cannot find TLA+ set {set_name}")
    return set(re.findall(r'"([^"]+)"', match.group(1)))


def audit_category_policy(root: Path, reports: list[dict]) -> tuple[dict, list[dict]]:
    policy_path = root / CATEGORY_POLICY_FILE
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkflowParseError(f"category policy cannot be read: {policy_path}: {exc}") from exc
    if not isinstance(policy, dict) or policy.get("format") != "govcheck.ci-routing-category-policy/v1":
        raise WorkflowParseError(f"{policy_path}: unsupported or missing policy format")
    model_path_value = policy.get("model")
    if not isinstance(model_path_value, str) or not model_path_value:
        raise WorkflowParseError(f"{policy_path}: model must be a non-empty path")
    model_path = root / model_path_value
    try:
        model_text = model_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise WorkflowParseError(f"TLA+ routing model cannot be read: {model_path}: {exc}") from exc
    model_categories = _read_tla_set(model_text, "Categories", model_path)
    model_specific = _read_tla_set(model_text, "ModelSpecific", model_path)

    entries = policy.get("categories")
    if not isinstance(entries, list):
        raise WorkflowParseError(f"{policy_path}: categories must be an array")
    mapped: dict[str, dict] = {}
    findings: list[dict] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise WorkflowParseError(f"{policy_path}: each category entry must be an object")
        name = entry.get("name")
        paths = entry.get("paths")
        workflows = entry.get("workflows")
        model_specific_flag = entry.get("modelSpecific")
        if not isinstance(name, str) or not name:
            raise WorkflowParseError(f"{policy_path}: category name must be a non-empty string")
        if name in mapped:
            raise WorkflowParseError(f"{policy_path}: duplicate category: {name}")
        if not isinstance(paths, list) or not all(isinstance(item, str) and item for item in paths):
            raise WorkflowParseError(f"{policy_path}: category {name} paths must be an array of non-empty strings")
        if not isinstance(workflows, list) or not all(isinstance(item, str) and item for item in workflows):
            raise WorkflowParseError(f"{policy_path}: category {name} workflows must be an array of non-empty strings")
        if not isinstance(model_specific_flag, bool):
            raise WorkflowParseError(f"{policy_path}: category {name} modelSpecific must be boolean")
        mapped[name] = entry

    policy_categories = set(mapped)
    if policy_categories != model_categories:
        findings.append({
            "kind": "model-category-inventory-mismatch",
            "missing_from_policy": sorted(model_categories - policy_categories),
            "not_in_model": sorted(policy_categories - model_categories),
        })
    policy_model_specific = {
        name for name, entry in mapped.items() if entry["modelSpecific"]
    }
    if policy_model_specific != model_specific:
        findings.append({
            "kind": "model-specific-inventory-mismatch",
            "missing_from_policy": sorted(model_specific - policy_model_specific),
            "not_in_model": sorted(policy_model_specific - model_specific),
        })

    report_by_path = {report["workflow"]: report for report in reports}
    for name, entry in mapped.items():
        paths = entry["paths"]
        workflows = entry["workflows"]
        if name in model_specific and (not paths or not workflows):
            findings.append({
                "kind": "model-specific-category-unmapped",
                "category": name,
                "message": "Model-specific categories require source/config/semantics paths and expected workflows.",
            })
        for source_path in paths:
            if not (root / source_path).is_file():
                findings.append({
                    "kind": "category-source-path-missing",
                    "category": name,
                    "path": source_path,
                })
            if workflows:
                for workflow in workflows:
                    report = report_by_path.get(workflow)
                    if report is None:
                        findings.append({
                            "kind": "category-workflow-missing",
                            "category": name,
                            "workflow": workflow,
                        })
                        continue
                    for event in EVENTS:
                        if event not in report["events"] or source_path not in set(report["events"][event]):
                            findings.append({
                                "kind": "model-category-path-missing",
                                "category": name,
                                "path": source_path,
                                "workflow": workflow,
                                "event": event,
                            })
            else:
                for report in reports:
                    if report["workflow"] not in TLC_WORKFLOWS:
                        continue
                    if any(source_path in report["events"].get(event, []) for event in EVENTS):
                        findings.append({
                            "kind": "non-tlc-category-routed-to-tlc",
                            "category": name,
                            "path": source_path,
                            "workflow": report["workflow"],
                        })
    return {
        "model": model_path_value,
        "model_categories": sorted(model_categories),
        "model_specific_categories": sorted(model_specific),
        "policy_categories": sorted(policy_categories),
        "policy_model_specific_categories": sorted(policy_model_specific),
    }, findings


def audit_workflows(root: str | Path) -> dict:
    root = Path(root).resolve()
    directory = root / WORKFLOW_DIR
    if not directory.is_dir():
        raise WorkflowParseError(f"workflow directory does not exist: {directory}")
    reports = []
    for path in sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml")):
        reports.append(inspect_workflow(path.relative_to(root), root))
    findings = []
    workflow_globs = {
        path_pattern
        for report in reports
        for event_paths in report["events"].values()
        for path_pattern in event_paths
        if GLOB_PATTERN.search(path_pattern)
    }
    policy_globs = load_glob_policy(root)
    for pattern in sorted(workflow_globs - policy_globs):
        findings.append({
            "kind": "unjustified-glob",
            "pattern": pattern,
            "message": "Workflow wildcard has no exact-pattern rationale in docs/ci-routing-glob-policy.json",
        })
    for pattern in sorted(policy_globs - workflow_globs):
        findings.append({
            "kind": "stale-glob-justification",
            "pattern": pattern,
            "message": "Glob rationale is not used by any workflow path filter",
        })
    category_policy_report, category_findings = audit_category_policy(root, reports)
    findings.extend(category_findings)
    for report in reports:
        events = report["events"]
        pr_paths = set(events.get("pull_request", []))
        push_paths = set(events.get("push", []))
        if "pull_request" in events and "push" in events:
            missing = sorted(pr_paths - push_paths)
            extra = sorted(push_paths - pr_paths)
            if missing or extra:
                findings.append({
                    "kind": "event-path-asymmetry",
                    "workflow": report["workflow"],
                    "missing_from_push": missing,
                    "push_only": extra,
                })
        for target in report["reusable_workflows"]:
            for event in EVENTS:
                configured = set(events.get(event, []))
                if event in events and target not in configured:
                    findings.append({
                        "kind": "reusable-workflow-not-routed",
                        "workflow": report["workflow"],
                        "event": event,
                        "required_path": target,
                    })
    return {
        "format": "govcheck.ci-workflow-routing-audit/v1",
        "workflow_count": len(reports),
        "finding_count": len(findings),
        "findings": findings,
        "workflow_globs": sorted(workflow_globs),
        "justified_globs": sorted(policy_globs),
        "category_policy": category_policy_report,
        "workflows": reports,
        "scope": [
            "GitHub Actions pull_request/push paths symmetry",
            "local reusable-workflow file existence and path routing",
            "exact-pattern justification for wildcard path filters",
            "TLA+ category inventory and declared source/config/semantics-to-workflow routing",
        ],
        "limitations": [
            "This is a constrained parser, not a general YAML implementation.",
            "Path-filter symmetry is a review signal; intentional asymmetry may require an explicit policy exception.",
            "The category policy is manually maintained and does not prove semantic dependencies beyond declared paths.",
            "Required-check liveness and model-to-required-status-check configuration are not yet evaluated.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = audit_workflows(args.root)
    except WorkflowParseError as exc:
        print(f"CI workflow routing audit could not complete: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if report["finding_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
