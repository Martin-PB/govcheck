#!/usr/bin/env python3
"""First executable GovCheck slice: deterministic rule evaluation on a repository tree.

Usage:
  python3 govcheck/check.py [--tree PATH] [--out REPORT.json] [--list-rules]
  python3 govcheck/check.py --tree PATH --base REV --candidate REV

Each rule returns pass, fail or unknown. The overall result is fail if any rule
fails, otherwise unknown if any rule is unknown, otherwise pass (fail-closed:
unknown is never a success). The exit code is 0 only when the overall result is
pass.

The JSON report is language-independent (stable rule ids and result codes); the
stdout text is a human-readable projection. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TOOL = "govcheck"
VERSION = "0.1.0-slice"

ANCHOR_RE = re.compile(r'<a id="r-(\d{2,3})"></a>', re.I)
MENTION_RE = re.compile(r"\bR-(\d{2,3})\b")
REF_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]*references(?:\.fr)?\.md#r-(\d{2,3})[^)]*)\)", re.I)

LICENSE_NAMES = ("LICENSE", "LICENSE.md", "LICENCE", "LICENCE.md")
CATALOGUES = ("docs/references.md", "docs/references.fr.md")


class Ctx:
    def __init__(self, tree: Path, changed):
        self.tree = tree
        self.changed = changed

    def read(self, rel: str) -> str:
        return (self.tree / rel).read_text(encoding="utf-8")


def rule_license(ctx: Ctx):
    found = [n for n in LICENSE_NAMES if (ctx.tree / n).is_file()]
    if found:
        return ("pass", True, ["license file present at the root: " + found[0]])
    return ("fail", True, ["no LICENSE/LICENCE file at the repository root"])


def rule_bilingual_decisions(ctx: Ctx):
    d = ctx.tree / "docs" / "decisions"
    if not d.is_dir():
        return ("pass", False, ["no docs/decisions directory; rule not applicable"])
    problems = []
    for p in sorted(d.iterdir()):
        if p.suffix != ".md" or not p.is_file():
            continue
        if p.name.endswith(".fr.md"):
            twin = p.with_name(p.name[:-6] + ".md")
        else:
            twin = p.with_name(p.name[:-3] + ".fr.md")
        if not twin.is_file():
            problems.append(p.name + " has no bilingual twin " + twin.name)
    if problems:
        return ("fail", True, problems)
    return ("pass", True, ["every decision document has an EN/FR twin"])


def rule_manifest_pairs(ctx: Ctx):
    m = ctx.tree / "docs" / "template-manifest.json"
    if not m.is_file():
        return ("fail", True, ["missing docs/template-manifest.json; the package/meta pairs are not declared"])
    try:
        manifest = json.loads(m.read_text(encoding="utf-8"))
    except ValueError as e:
        return ("fail", True, ["docs/template-manifest.json is not valid JSON: " + str(e)])
    problems = []
    for key in sorted(manifest.get("pairs", {})):
        if not (ctx.tree / key).is_file():
            problems.append("manifest pair missing at the meta level: " + key)
        pkg = ctx.tree / "govcheck" / key
        if not pkg.is_file():
            problems.append("manifest pair missing in the govcheck/ package: " + key)
    if problems:
        return ("fail", True, problems)
    return ("pass", True, ["every manifest-declared pair exists at both levels"])


def rule_reference_integrity(ctx: Ctx):
    docs = ctx.tree / "docs"
    if not docs.is_dir():
        return ("pass", False, ["no docs/ directory; rule not applicable"])
    cat_ids = {}
    for rel in CATALOGUES:
        p = ctx.tree / rel
        if not p.is_file():
            return ("fail", True, ["missing reference catalogue: " + rel])
        cat_ids[rel] = {"R-" + n for n in ANCHOR_RE.findall(ctx.read(rel))}
    problems = []
    en_ids = cat_ids[CATALOGUES[0]]
    fr_ids = cat_ids[CATALOGUES[1]]
    if en_ids != fr_ids:
        problems.append("EN/FR catalogue id sets differ: only-EN=" + str(sorted(en_ids - fr_ids)) + " only-FR=" + str(sorted(fr_ids - en_ids)))
    ids = en_ids | fr_ids
    for p in sorted(docs.rglob("*.md")):
        rel = p.relative_to(ctx.tree).as_posix()
        if rel in CATALOGUES:
            continue
        text = p.read_text(encoding="utf-8")
        for n in sorted(set(MENTION_RE.findall(text))):
            rid = "R-" + n
            if rid not in ids:
                problems.append(rel + ": mentions " + rid + " without a catalogue entry")
        for mm in REF_LINK_RE.finditer(text):
            rid = "R-" + mm.group(2)
            if rid not in ids:
                problems.append(rel + ": links to missing catalogue entry " + rid)
    if problems:
        return ("fail", True, problems)
    return ("pass", True, ["all R-xx mentions and links resolve to catalogue entries, EN/FR id sets equal"])


def rule_tla_freshness(ctx: Ctx):
    if ctx.changed is not None:
        applies = any(c.startswith("formal/tla/") for c in ctx.changed)
    else:
        applies = (ctx.tree / "formal" / "tla").is_dir()
    if not applies:
        return ("pass", False, ["no formal/tla/ changes; rule not applicable"])
    return ("unknown", True, ["changes under formal/tla/ require fresh TLC evidence bound to the candidate revision; not verifiable offline"])


def rule_independent_review(ctx: Ctx):
    if ctx.changed is None or not ctx.changed:
        return ("pass", False, ["no candidate diff supplied; rule not applicable"])
    return ("unknown", True, ["acceptance requires a recorded human attestation by an identity distinct from the author; not machine-checkable"])


RULES = [
    {"id": "license-present", "class": "decidable", "fn": rule_license},
    {"id": "bilingual-decisions", "class": "decidable", "fn": rule_bilingual_decisions},
    {"id": "manifest-pairs", "class": "decidable", "fn": rule_manifest_pairs},
    {"id": "reference-integrity", "class": "decidable", "fn": rule_reference_integrity},
    {"id": "tla-evidence-freshness", "class": "not-verifiable-offline", "fn": rule_tla_freshness},
    {"id": "independent-review", "class": "attested", "fn": rule_independent_review},
]


def evaluate(tree: Path, changed=None) -> dict:
    ctx = Ctx(tree, changed)
    rules = []
    for r in RULES:
        result, applies, reasons = r["fn"](ctx)
        rules.append({"id": r["id"], "class": r["class"], "result": result, "applies": applies, "reasons": reasons})
    if any(x["result"] == "fail" for x in rules):
        overall = "fail"
    elif any(x["result"] == "unknown" for x in rules):
        overall = "unknown"
    else:
        overall = "pass"
    return {
        "tool": TOOL,
        "version": VERSION,
        "candidate": {"tree": str(tree), "changed_files": sorted(changed) if changed is not None else None},
        "overall": overall,
        "rules": rules,
    }


def git_changed(tree: Path, base: str, candidate: str):
    proc = subprocess.run(
        ["git", "-C", str(tree), "diff", "--name-only", base + "..." + candidate],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit("git diff failed: " + proc.stderr.strip())
    return set(proc.stdout.split())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="First executable GovCheck slice.")
    parser.add_argument("--tree", default=".")
    parser.add_argument("--base")
    parser.add_argument("--candidate")
    parser.add_argument("--out")
    parser.add_argument("--list-rules", action="store_true")
    args = parser.parse_args(argv)
    if args.list_rules:
        for r in RULES:
            print(r["id"] + " (" + r["class"] + ")")
        return 0
    if (args.base is None) != (args.candidate is None):
        print("error: --base and --candidate must be used together", file=sys.stderr)
        return 2
    tree = Path(args.tree).resolve()
    changed = git_changed(tree, args.base, args.candidate) if args.base else None
    report = evaluate(tree, changed)
    report["candidate"]["base"] = args.base
    report["candidate"]["candidate_rev"] = args.candidate
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text + "
", encoding="utf-8")
    print("govcheck " + VERSION + " -- overall: " + report["overall"].upper())
    for x in report["rules"]:
        line = "  [" + x["result"].upper() + "] " + x["id"] + " (" + x["class"] + ")"
        if not x["applies"]:
            line += " [not applicable]"
        print(line)
        for reason in x["reasons"]:
            print("      - " + reason)
    if args.out:
        print("report written to " + args.out)
    return 0 if report["overall"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
