#!/usr/bin/env python3
"""Cross-record checks for GovCheck version-governance bundles.

This deliberately does not replace Draft 2020-12 JSON Schema validation and
cannot authenticate authority delegation, prove compatibility, resolve VCS
objects, or establish evidence freshness.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
OUTCOMES = {"proposed", "authorized", "rejected", "blocked", "withdrawn", "superseded"}
CLASSIFICATIONS = {
    "initial-publication", "major", "minor", "patch", "no-contract-change", "undetermined"
}
EDGE_STATES = {"active", "review-required", "stale-invalid", "superseded", "revoked"}


def revision_key(artifact_id: str, revision: dict[str, Any]) -> tuple[str, str, str]:
    return artifact_id, str(revision.get("vcs", "")), str(revision.get("nativeId", ""))


def add(findings: list[dict[str, str]], level: str, code: str, message: str) -> None:
    findings.append({"level": level, "code": code, "message": message})


def validate_bundle(bundle: Any) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    if not isinstance(bundle, dict):
        return {"status": "invalid", "findings": [
            {"level": "error", "code": "bundle.type", "message": "Bundle root must be an object."}
        ]}
    if type(bundle.get("schemaVersion")) is not int or bundle.get("schemaVersion") != 1:
        add(findings, "error", "bundle.schema-version", "Unsupported bundle schemaVersion; expected 1.")

    for key in ("revisions", "decisions", "dependencies"):
        if not isinstance(bundle.get(key), list):
            add(findings, "error", f"bundle.{key}.type", f"'{key}' must be an array.")
    revisions = bundle.get("revisions", [])
    decisions = bundle.get("decisions", [])
    dependencies = bundle.get("dependencies", [])
    if not all(isinstance(x, list) for x in (revisions, decisions, dependencies)):
        return _result(findings)

    revision_index: dict[tuple[str, str, str], dict[str, Any]] = {}
    for i, item in enumerate(revisions):
        if not isinstance(item, dict) or not isinstance(item.get("artifactId"), str) or not isinstance(item.get("revision"), dict):
            add(findings, "error", "revision.shape", f"revisions[{i}] needs artifactId and revision object.")
            continue
        key = revision_key(item["artifactId"], item["revision"])
        if not key[1] or not key[2]:
            add(findings, "error", "revision.identity", f"revisions[{i}] has an incomplete native revision identity.")
        if key in revision_index:
            add(findings, "error", "revision.duplicate", f"Duplicate revision inventory entry for {key[0]} ({key[1]}:{key[2]}).")
        revision_index[key] = item

    decision_index: dict[str, dict[str, Any]] = {}
    for i, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            add(findings, "error", "decision.shape", f"decisions[{i}] must be an object.")
            continue
        if type(decision.get("schemaVersion")) is not int or decision.get("schemaVersion") != 1:
            add(findings, "error", "decision.schema-version", f"Decision at index {i} has unsupported schemaVersion; expected integer 1.")
        decision_id = decision.get("decisionId")
        if not isinstance(decision_id, str) or not decision_id:
            add(findings, "error", "decision.id", f"decisions[{i}] has no decisionId.")
            continue
        if decision_id in decision_index:
            add(findings, "error", "decision.duplicate", f"Duplicate decisionId '{decision_id}'.")
        decision_index[decision_id] = decision

        artifact_id = decision.get("artifactId")
        candidate = decision.get("candidateRevision")
        if isinstance(artifact_id, str) and isinstance(candidate, dict):
            if revision_key(artifact_id, candidate) not in revision_index:
                add(findings, "error", "decision.candidate-missing",
                    f"Decision '{decision_id}' candidate revision is absent from the revision inventory.")
        else:
            add(findings, "error", "decision.candidate-shape",
                f"Decision '{decision_id}' needs artifactId and candidateRevision.")

        outcome = (decision.get("decision") or {}).get("outcome") if isinstance(decision.get("decision"), dict) else None
        classification = (decision.get("compatibility") or {}).get("classification") if isinstance(decision.get("compatibility"), dict) else None
        if outcome not in OUTCOMES:
            add(findings, "error", "decision.outcome", f"Decision '{decision_id}' has an unknown outcome.")
        if classification not in CLASSIFICATIONS:
            add(findings, "error", "decision.classification", f"Decision '{decision_id}' has an unknown compatibility classification.")

        previous = decision.get("previous")
        proposed = decision.get("proposedContractVersion")
        if outcome == "authorized":
            roles = decision.get("roles")
            authority = decision.get("authority")
            authorizer = roles.get("authorizer") if isinstance(roles, dict) else None
            if not isinstance(authorizer, dict) or not authorizer.get("actorId") or not isinstance(authority, dict):
                add(findings, "error", "decision.authorization-record",
                    f"Authorized decision '{decision_id}' lacks the schema-required authorizer or authority record.")
            if (decision.get("decision") or {}).get("conditions"):
                add(findings, "error", "decision.open-conditions",
                    f"Authorized decision '{decision_id}' still has open conditions.")
            if classification == "undetermined":
                add(findings, "error", "decision.undetermined-authorized",
                    f"Undetermined decision '{decision_id}' cannot be authorized.")
            if classification == "initial-publication":
                if "previous" not in decision or previous is not None or "proposedContractVersion" not in decision or not isinstance(proposed, str) or not SEMVER.fullmatch(proposed):
                    add(findings, "error", "decision.initial-publication",
                        f"Initial publication '{decision_id}' needs previous=null and a SemVer contract version.")
            elif classification == "no-contract-change":
                if "proposedContractVersion" not in decision or proposed is not None:
                    add(findings, "error", "decision.no-contract-change",
                        f"No-contract-change decision '{decision_id}' must not assign a new contract version.")
            elif classification in {"major", "minor", "patch"}:
                if not isinstance(previous, dict) or not isinstance(previous.get("revision"), dict):
                    add(findings, "error", "decision.previous-required",
                        f"Increment decision '{decision_id}' needs a previous revision.")
                elif revision_key(artifact_id, previous["revision"]) not in revision_index:
                    add(findings, "error", "decision.previous-missing",
                        f"Decision '{decision_id}' previous revision is absent from the revision inventory.")
                if not isinstance(proposed, str) or not SEMVER.fullmatch(proposed):
                    add(findings, "error", "decision.semver",
                        f"Increment decision '{decision_id}' needs a valid SemVer contract version.")
            # The record shape is not proof that the named authority delegated this scope.
            add(findings, "unknown", "decision.authority-not-resolved",
                f"Delegation and subject scope for authority on '{decision_id}' require the canonical governance authority registry; this bundle cannot establish them.")

        impact = decision.get("dependencyImpact", [])
        if isinstance(impact, list):
            for entry in impact:
                if isinstance(entry, dict) and entry.get("edgeId"):
                    # Checked against the complete edge set below.
                    pass

    edge_index: dict[str, dict[str, Any]] = {}
    for i, edge in enumerate(dependencies):
        if not isinstance(edge, dict):
            add(findings, "error", "edge.shape", f"dependencies[{i}] must be an object.")
            continue
        if type(edge.get("schemaVersion")) is not int or edge.get("schemaVersion") != 1:
            add(findings, "error", "edge.schema-version", f"Edge at index {i} has unsupported schemaVersion; expected integer 1.")
        edge_id = edge.get("edgeId")
        if not isinstance(edge_id, str) or not edge_id:
            add(findings, "error", "edge.id", f"dependencies[{i}] has no edgeId.")
            continue
        if edge_id in edge_index:
            add(findings, "error", "edge.duplicate", f"Duplicate edgeId '{edge_id}'.")
        edge_index[edge_id] = edge
        for endpoint_name in ("source", "target"):
            endpoint = edge.get(endpoint_name)
            if not isinstance(endpoint, dict) or not isinstance(endpoint.get("artifactId"), str) or not isinstance(endpoint.get("revision"), dict):
                add(findings, "error", "edge.endpoint-shape", f"Edge '{edge_id}' has an invalid {endpoint_name} endpoint.")
                continue
            key = revision_key(endpoint["artifactId"], endpoint["revision"])
            if key not in revision_index:
                add(findings, "error", "edge.endpoint-missing",
                    f"Edge '{edge_id}' {endpoint_name} endpoint is absent from the revision inventory.")
        validity = edge.get("validity")
        if not isinstance(validity, dict) or "status" not in validity:
            state = None
            add(findings, "unknown", "edge.validity-unresolved",
                f"Edge '{edge_id}' has no explicit validity status; it cannot be treated as active.")
        else:
            state = validity.get("status")
            if state not in EDGE_STATES:
                add(findings, "error", "edge.validity", f"Edge '{edge_id}' has an unknown validity status.")
            elif state in {"review-required", "stale-invalid", "superseded", "revoked"}:
                add(findings, "stale", "edge.not-current", f"Edge '{edge_id}' is marked '{state}', not active.")

    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        decision_id = decision.get("decisionId", "<unknown>")
        impact = decision.get("dependencyImpact", [])
        if not isinstance(impact, list):
            continue
        seen_impact: set[str] = set()
        for item in impact:
            if not isinstance(item, dict) or not isinstance(item.get("edgeId"), str):
                add(findings, "error", "decision.impact-shape", f"Decision '{decision_id}' has malformed dependencyImpact.")
                continue
            edge_id = item["edgeId"]
            if edge_id in seen_impact:
                add(findings, "error", "decision.impact-duplicate", f"Decision '{decision_id}' repeats edge '{edge_id}' in dependencyImpact.")
            seen_impact.add(edge_id)
            if edge_id not in edge_index:
                add(findings, "error", "decision.impact-orphan", f"Decision '{decision_id}' references missing edge '{edge_id}'.")
            elif item.get("assessment") == "unaffected":
                validity = edge_index[edge_id].get("validity")
                state = validity.get("status") if isinstance(validity, dict) else None
                if state != "active":
                    add(findings, "error", "decision.impact-contradiction",
                        f"Decision '{decision_id}' calls edge '{edge_id}' unaffected while its status is '{state}'.")

    # Supersession links must resolve and stay within the same contract identity.
    supersession_graph: dict[str, str] = {}
    for decision_id, decision in decision_index.items():
        d = decision.get("decision") or {}
        target = d.get("supersedesDecisionId") if isinstance(d, dict) else None
        if target:
            if target not in decision_index:
                add(findings, "error", "decision.supersedes-orphan", f"Decision '{decision_id}' supersedes missing decision '{target}'.")
            else:
                other = decision_index[target]
                if (decision.get("artifactId"), decision.get("contractId")) != (other.get("artifactId"), other.get("contractId")):
                    add(findings, "error", "decision.supersedes-scope", f"Decision '{decision_id}' supersedes a different artifact/contract.")
                supersession_graph[decision_id] = target
    for start in supersession_graph:
        seen: set[str] = set()
        node = start
        while node in supersession_graph:
            if node in seen:
                add(findings, "error", "decision.supersedes-cycle", f"Supersession cycle includes '{node}'.")
                break
            seen.add(node)
            node = supersession_graph[node]

    # More than one current authorization for the same exact contract candidate is ambiguous.
    authorized: dict[tuple[str, str, tuple[str, str, str]], list[str]] = {}
    for decision_id, decision in decision_index.items():
        d = decision.get("decision") or {}
        if isinstance(d, dict) and d.get("outcome") == "authorized" and isinstance(decision.get("candidateRevision"), dict):
            key = (decision.get("artifactId", ""), decision.get("contractId", ""),
                   revision_key(decision.get("artifactId", ""), decision["candidateRevision"]))
            authorized.setdefault(key, []).append(decision_id)
    for ids in authorized.values():
        if len(ids) > 1:
            add(findings, "error", "decision.multiple-authorizations",
                f"Multiple authorized decisions target the same artifact/contract/revision: {', '.join(sorted(ids))}.")

    return _result(findings)


def _result(findings: list[dict[str, str]]) -> dict[str, Any]:
    levels = {item["level"] for item in findings}
    status = "invalid" if "error" in levels else "stale" if "stale" in levels else "unknown" if "unknown" in levels else "valid"
    return {"status": status, "summary": dict(Counter(x["level"] for x in findings)),
            "findings": findings,
            "scope": {
                "structural_cross_record_checks": True,
                "authority_delegation_verified": False,
                "vcs_revision_existence_verified": False,
                "semantic_compatibility_verified": False,
                "evidence_freshness_verified": False,
                "json_schema_validation_performed": False
            }}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="JSON bundle containing schemaVersion, revisions, decisions and dependencies")
    parser.add_argument("--pretty", action="store_true", help="pretty-print the JSON report")
    args = parser.parse_args()
    try:
        bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "findings": [{"level": "error", "code": "input.read", "message": str(exc)}]}))
        return 1
    result = validate_bundle(bundle)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return {"valid": 0, "unknown": 2, "stale": 3, "invalid": 1}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
