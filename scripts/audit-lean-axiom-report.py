#!/usr/bin/env python3
"""Fail-closed parser for Lean '#print axioms' reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


def parse_axiom_report(report: str) -> list[dict[str, Any]]:
    declarations: list[dict[str, Any]] = []
    for line in report.splitlines():
        if "depends on axioms:" not in line:
            continue
        prefix, suffix = line.split("depends on axioms:", 1)
        suffix = suffix.strip()
        if not (suffix.startswith("[") and suffix.endswith("]")):
            continue
        body = suffix[1:-1].strip()
        axioms = sorted({item.strip() for item in body.split(",") if item.strip()})
        declaration = prefix.strip().strip("'\"")
        declarations.append({"declaration": declaration, "axioms": axioms})
    return declarations


def audit_report(report: str, allowed: set[str] | None = None) -> dict[str, Any]:
    allowlist = allowed or set()
    declarations = parse_axiom_report(report)
    findings: list[dict[str, str]] = []
    if not declarations:
        findings.append({
            "declaration": "",
            "axiom": "",
            "reason": "no '#print axioms' declaration report found; refusing to treat missing output as clean",
        })
    for declaration in declarations:
        for axiom in declaration["axioms"]:
            if axiom not in allowlist:
                findings.append({
                    "declaration": declaration["declaration"],
                    "axiom": axiom,
                    "reason": "axiom is not in the explicit allow-list",
                })
    return {
        "format": "govcheck.lean-axiom-report-audit/v1",
        "status": "rejected" if findings else "accepted",
        "declarations": declarations,
        "allowList": sorted(allowlist),
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--allow", action="append", default=[])
    parser.add_argument("--expect-rejected", action="store_true")
    parser.add_argument("--require-forbidden", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        report = args.input.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read Lean axiom report: {exc}", file=sys.stderr)
        return 2
    result = audit_report(report, set(args.allow))
    found = {
        item["axiom"]
        for item in result["findings"]
        if item["axiom"]
    }
    missing = [
        required for required in args.require_forbidden
        if not any(name == required or name.endswith("." + required) for name in found)
    ]
    result["requiredForbiddenAxioms"] = args.require_forbidden
    result["missingRequiredForbiddenAxioms"] = missing
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    if args.expect_rejected:
        return 0 if result["status"] == "rejected" and not missing else 1
    return 1 if result["status"] == "rejected" else 0


if __name__ == "__main__":
    raise SystemExit(main())
