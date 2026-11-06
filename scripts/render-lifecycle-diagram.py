#!/usr/bin/env python3
"""Render the explanatory lifecycle diagram and check transition/operator coverage.

This intentionally does not parse TLA+ semantics. It checks that each registry
operator has a top-level definition in the TLA+ module and that every modeled
lifecycle action is represented. Guard/effect fidelity still requires review.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "formal/lifecycle-transitions.json"
ACTION_NAMES = {
    "Prepare", "PublishEvidence", "Evaluate", "Approve", "Accept", "Apply",
    "ChangeInputs", "Reject", "Withdraw", "Supersede",
}
DEFINITION = re.compile(r"^([A-Za-z][A-Za-z0-9_]*)(?:\\([^\\n]*\\))?\\s*==", re.MULTILINE)


def render(data: dict) -> str:
    lines = ["stateDiagram-v2", "  direction TB"]
    for state in data["states"]:
        if state["id"] in {"Applied", "Rejected", "Withdrawn", "Superseded"}:
            lines.append(f'  state "{state["label"]}" as {state["id"]} <<end>>')
        else:
            lines.append(f'  state "{state["label"]}" as {state["id"]}')
    for transition in data["transitions"]:
        label = transition["label"].replace('"', "'")
        for source in transition["from"]:
            lines.append(f'  {source} --> {transition["to"]} : {label} [{transition["operator"]}]')
    lines.extend([
        "",
        "  note right of Reviewable",
        "    Approval is distinct from evidence and acceptance.",
        "    Acceptance is distinct from application.",
        "  end note",
        "",
        "  %% Generated from formal/lifecycle-transitions.json.",
        "  %% Explanatory view only; TLA+ remains authoritative.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated diagram is stale")
    args = parser.parse_args()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    model_path = ROOT / data["model"]
    diagram_path = ROOT / data["diagram"]
    model = model_path.read_text(encoding="utf-8")
    definitions = set(DEFINITION.findall(model))
    registry_ops = {item["operator"] for item in data["transitions"]}
    missing_definitions = registry_ops - definitions
    missing_registry = ACTION_NAMES - registry_ops
    unknown_ops = registry_ops - ACTION_NAMES
    if missing_definitions or missing_registry or unknown_ops:
        if missing_definitions:
            print("Missing TLA+ definitions:", ", ".join(sorted(missing_definitions)))
        if missing_registry:
            print("Lifecycle actions missing from registry:", ", ".join(sorted(missing_registry)))
        if unknown_ops:
            print("Unexpected registry operators:", ", ".join(sorted(unknown_ops)))
        return 1
    generated = render(data)
    if args.check:
        if not diagram_path.exists() or diagram_path.read_text(encoding="utf-8") != generated:
            print(f"Stale generated diagram: {diagram_path.relative_to(ROOT)}")
            return 1
        print("Lifecycle transition coverage and generated diagram: PASS")
        return 0
    diagram_path.parent.mkdir(parents=True, exist_ok=True)
    diagram_path.write_text(generated, encoding="utf-8")
    print(f"Generated {diagram_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
