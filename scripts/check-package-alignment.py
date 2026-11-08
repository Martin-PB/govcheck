#!/usr/bin/env python3
"""Structural alignment check between the govcheck/ product package and the meta level.

Implements the alignment rule of ADR 0003 (two-level governance): when a PR changes a
normative document, both levels are updated in the same PR. Structural alignment is
declared in docs/template-manifest.json, not inferred: every section of every paired
normative document is classified as "package" (indispensable: present at both levels,
same relative order), "optionnel" (may appear on either side) or "meta-only" (meta
level only, never copied into the package). Sections absent from the manifest default
to "package". Standard library only; run from anywhere inside the repository checkout.

Checks:
1. govcheck/bootstrap.py and govcheck/README.md exist.
2. Package purity: the string "Martin-PB" appears nowhere under govcheck/.
3. govcheck/decisions/ and govcheck/docs/architecture/ contain only guide/template
   files (README*/TEMPLATE*), never GovCheck-specific numbered records.
4. Paired normative markdown exists with the same file names on both levels
   (docs/specifications/, docs/formal/, docs/BOOTSTRAP_GOVERNANCE*), is fully covered
   by docs/template-manifest.json, and each pair satisfies the manifest: "package"
   sections on both sides in the same relative order, "meta-only" sections never in
   the package, "optionnel" sections allowed on either side.
5. Reference catalogues (docs/references*.md vs govcheck/docs/references*.md) are
   compared by reference ID: every package ID must exist in the meta catalogue.
6. Workflows: every workflow in govcheck/.github/workflows/ has a root counterpart in
   .github/workflows/ whose job IDs are a superset (the root may add meta-level paths,
   jobs or matrix entries). Root-only workflows must be declared in META_ONLY_WORKFLOWS.

Exit code 0 when aligned, 1 otherwise, with one line per violation.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE = REPO_ROOT / "govcheck"
MANIFEST = REPO_ROOT / "docs" / "template-manifest.json"

# Root workflows that intentionally have no package counterpart (meta-level only).
META_ONLY_WORKFLOWS = {\n    "reference-check.yml",\n    "package-alignment.yml",\n    "ci-routing-model.yml",\n    "lifecycle-diagram.yml",\n    "tla-assurance.yml",\n    "tla-authority.yml",\n    "tla-lifecycle.yml",\n    "tla-model-reusable.yml",\n    "version-governance.yml",\n}\n\n# Product-package workflow templates are intentionally not executable at the meta level.\nPACKAGE_TEMPLATE_WORKFLOWS = {"tla-check.yml"}

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
    return title.replace("\u2018", "'").replace("\u2019", "'").replace("\u02bc", "'")


def read(path):
    return path.read_text(encoding="utf-8")


def section_titles(path):
    return [normalize_heading(t) for _, t in headings(read(path))]


def reference_ids(text):
    ids = set()
    for _, title in headings(text):
        m = re.match(r"[Rr]-(\d+)", title)
        if m:
            ids.add("r-" + m.group(1))
    for m in ANCHOR_ID.finditer(text):
        ids.add(m.group(1).lower())
    return ids


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


def actual_pairs(errors):
    """Paired normative markdown: (meta_path, package_path, meta_rel) triples."""
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
            pairs.append((meta / name, pkg / name, meta_dir + "/" + name))
    for name in ("BOOTSTRAP_GOVERNANCE.md", "BOOTSTRAP_GOVERNANCE.fr.md"):
        pairs.append((REPO_ROOT / "docs" / name, PACKAGE / "docs" / name, "docs/" + name))
    return pairs


def check_manifest(errors, pairs):
    if not MANIFEST.is_file():
        errors.append("missing docs/template-manifest.json")
        return
    try:
        manifest = json.loads(read(MANIFEST))
    except (OSError, ValueError) as e:
        errors.append("cannot parse docs/template-manifest.json: " + str(e))
        return
    cfg_pairs = manifest.get("pairs", {})
    actual_rels = {rel for _, _, rel in pairs}
    for rel in sorted(set(cfg_pairs) - actual_rels):
        errors.append("manifest declares a pair that does not exist: " + rel)
    for rel in sorted(actual_rels - set(cfg_pairs)):
        errors.append("paired file missing from docs/template-manifest.json: " + rel)
    for meta_f, pkg_f, rel in pairs:
        cfg = cfg_pairs.get(rel, {})
        meta_only = {normalize_heading(t) for t in cfg.get("meta_only", [])}
        optional = {normalize_heading(t) for t in cfg.get("optional", [])}
        if not meta_f.is_file() or not pkg_f.is_file():
            errors.append("unpaired file: " + rel)
            continue
        pkg_rel = pkg_f.relative_to(REPO_ROOT).as_posix()
        mh = section_titles(meta_f)
        ph = section_titles(pkg_f)
        status = {t: "package" for t in set(mh) | set(ph)}
        for t in meta_only:
            status[t] = "meta-only"
        for t in optional:
            status[t] = "optionnel"
        for t in mh:
            st = status.get(t, "package")
            if st == "package" and t not in ph:
                errors.append(pkg_rel + ": section 'package' missing in package: " + repr(t))
            if st == "meta-only" and t in ph:
                errors.append(pkg_rel + ": section 'meta-only' present in package: " + repr(t))
        for t in ph:
            st = status.get(t, "package")
            if st == "package" and t not in mh:
                errors.append(rel + ": section 'package' absent at meta level: " + repr(t))
            if st == "meta-only":
                errors.append(pkg_rel + ": section 'meta-only' present in package: " + repr(t))
        common_meta = [t for t in mh if t in ph]
        common_pkg = [t for t in ph if t in mh]
        if common_meta != common_pkg:
            errors.append(pkg_rel + ": relative order of shared sections differs from meta level")


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

    # 4. Manifest-declared structural alignment of paired normative markdown.
    check_manifest(errors, actual_pairs(errors))

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
    print("Package alignment check passed (ADR 0003 manifest-declared template).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
