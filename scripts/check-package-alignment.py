#!/usr/bin/env python3
"""Structural alignment check between the govcheck/ product package and the meta level.

Implements the alignment rule of ADR 0003 (two-level governance): when a PR changes a
normative document, both levels are updated in the same PR, and a CI check verifies that
they stay structurally aligned (same template sections) without requiring identical
content. Standard library only; run from anywhere inside the repository checkout.

Checks:
1. govcheck/bootstrap.py and govcheck/README.md exist.
2. Package purity: the string "Martin-PB" appears nowhere under govcheck/.
3. govcheck/decisions/ and govcheck/docs/architecture/ contain only guide/template
   files (README*/TEMPLATE*), never GovCheck-specific numbered records.
4. Paired normative markdown exists with the same file names on both levels
   (docs/specifications/, docs/formal/, docs/BOOTSTRAP_GOVERNANCE*). For each pair, the
   package heading sequence, ignoring reference-register sections, must be an ordered
   subsequence of the meta heading sequence: the meta level may add meta-level sections
   (governance authority, bibliographic references), the package must not invent
   sections absent from the meta level.
5. Reference catalogues (docs/references*.md vs govcheck/docs/references*.md) are
   compared by reference ID: every package ID must exist in the meta catalogue.
6. Workflows: every workflow in govcheck/.github/workflows/ has a root counterpart in
   .github/workflows/ whose job IDs are a superset (the root may add meta-level paths,
   jobs or matrix entries). Root-only workflows must be declared in META_ONLY_WORKFLOWS.

Exit code 0 when aligned, 1 otherwise, with one line per violation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE = REPO_ROOT / "govcheck"

# Root workflows that intentionally have no package counterpart (meta-level only).
META_ONLY_WORKFLOWS = {"reference-check.yml", "package-alignment.yml"}

# Reference-register headings are excluded from the template-section comparison: the
# meta level appends bibliographic references and the package may carry its own
# (smaller) catalogue section.
REFERENCE_HEADING = re.compile(r"reference|bibliograph", re.IGNORECASE)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
ANCHOR_ID = re.compile(r'id="([^"]+)"')
GUIDE_FILE = re.compile(r"^(README|TEMPLATE)(\.fr)?\.md$")


def headings(text):
    out = []
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            out.append((len(m.group(1)), m.group(2)))
    return out


def normalize_heading(title):
    """Normalize typographic apostrophe variants without changing displayed headings."""
    return title.replace("\\u2018", "'").replace("\\u2019", "'").replace("\\u02bc", "'")


def template_headings(text):
    return [
        normalize_heading(title)
        for _, title in headings(text)
        if not REFERENCE_HEADING.search(title)
    ]


def reference_ids(text):
    ids = set()
    for _, title in headings(text):
        m = re.match(r"[Rr]-(\d+)", title)
        if m:
            ids.add("r-" + m.group(1))
    for m in ANCHOR_ID.finditer(text):
        ids.add(m.group(1).lower())
    return ids


def is_subsequence(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)


def read(path):
    return path.read_text(encoding="utf-8")


def job_ids(workflow_text):
    ids = set()
    in_jobs = False
    for line in workflow_text.splitlines():
        if re.match(r"^jobs:\s*$", line):
            in_jobs = True
            continue
        if in_jobs:
            if re.match(r"^\S", line):
                break
            m = re.match(r"^  ([A-Za-z0-9_-]+):", line)
            if m:
                ids.add(m.group(1))
    return ids


def main():
    errors = []

    # 1. Bootstrap entry points.
    for rel in ("govcheck/bootstrap.py", "govcheck/README.md"):
        if not (REPO_ROOT / rel).is_file():
            errors.append("missing " + rel)

    # 2. Package purity.
    if PACKAGE.is_dir():
        for f in sorted(PACKAGE.rglob("*")):
            if f.is_file() and f.suffix in {".md", ".py", ".yml", ".yaml", ".json", ".tla", ".cfg", ".mmd"}:
                try:
                    content = f.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                if "Martin-PB" in content:
                    errors.append("package purity: 'Martin-PB' found in " + str(f.relative_to(REPO_ROOT)))

    # 3. Package decision/architecture folders hold only guides and templates.
    for sub in ("govcheck/decisions", "govcheck/docs/architecture"):
        d = REPO_ROOT / sub
        if not d.is_dir():
            errors.append("missing directory " + sub)
            continue
        for f in sorted(d.iterdir()):
            if f.is_file() and not GUIDE_FILE.match(f.name):
                errors.append(sub + "/ must contain only guide/template files, found " + f.name)

    # 4. Paired normative markdown.
    pairs = []
    for meta_dir, pkg_dir in (
        ("docs/specifications", "govcheck/docs/specifications"),
        ("docs/formal", "govcheck/docs/formal"),
    ):
        meta = REPO_ROOT / meta_dir
        pkg = REPO_ROOT / pkg_dir
        if not meta.is_dir() or not pkg.is_dir():
            errors.append("missing directory pair " + meta_dir + " / " + pkg_dir)
            continue
        meta_files = {f.name for f in meta.iterdir() if f.suffix == ".md"}
        pkg_files = {f.name for f in pkg.iterdir() if f.suffix == ".md"}
        for name in sorted(meta_files - pkg_files):
            errors.append(pkg_dir + "/" + name + " missing (present at meta level)")
        for name in sorted(pkg_files - meta_files):
            errors.append(meta_dir + "/" + name + " missing (present in package)")
        for name in sorted(meta_files & pkg_files):
            pairs.append((meta / name, pkg / name))
    for name in ("BOOTSTRAP_GOVERNANCE.md", "BOOTSTRAP_GOVERNANCE.fr.md"):
        pairs.append((REPO_ROOT / "docs" / name, PACKAGE / "docs" / name))

    for meta_f, pkg_f in pairs:
        if not meta_f.is_file() or not pkg_f.is_file():
            errors.append("unpaired file: " + pkg_f.name)
            continue
        meta_h = template_headings(read(meta_f))
        pkg_h = template_headings(read(pkg_f))
        if not is_subsequence(pkg_h, meta_h):
            errors.append(
                "template mismatch for " + str(pkg_f.relative_to(REPO_ROOT))
                + ": package sections " + repr(pkg_h)
                + " are not an ordered subsequence of meta sections " + repr(meta_h)
            )

    # 5. Reference catalogues compared by ID.
    for name in ("references.md", "references.fr.md"):
        meta_f = REPO_ROOT / "docs" / name
        pkg_f = PACKAGE / "docs" / name
        if not meta_f.is_file() or not pkg_f.is_file():
            errors.append("reference catalogue missing: docs/" + name + " or govcheck/docs/" + name)
            continue
        missing = reference_ids(read(pkg_f)) - reference_ids(read(meta_f))
        if missing:
            errors.append("govcheck/docs/" + name + " uses IDs absent from the meta catalogue: " + str(sorted(missing)))

    # 6. Workflow coverage.
    pkg_wf = PACKAGE / ".github" / "workflows"
    root_wf = REPO_ROOT / ".github" / "workflows"
    pkg_names = set()
    root_names = set()
    if pkg_wf.is_dir():
        pkg_names = {f.name for f in pkg_wf.iterdir() if f.suffix in {".yml", ".yaml"}}
    if root_wf.is_dir():
        root_names = {f.name for f in root_wf.iterdir() if f.suffix in {".yml", ".yaml"}}
    for name in sorted(pkg_names - root_names):
        errors.append("package workflow " + name + " has no root counterpart")
    for name in sorted(root_names - pkg_names):
        if name not in META_ONLY_WORKFLOWS:
            errors.append("root workflow " + name + " has no package counterpart and is not in META_ONLY_WORKFLOWS")
    for name in sorted(pkg_names & root_names):
        extra = job_ids(read(pkg_wf / name)) - job_ids(read(root_wf / name))
        if extra:
            errors.append("workflow " + name + ": package jobs missing at root: " + str(sorted(extra)))

    if errors:
        print("Package alignment check FAILED:")
        for e in errors:
            print(" - " + e)
        return 1
    print("Package alignment check passed (ADR 0003 structural alignment).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
