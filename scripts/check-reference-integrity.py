#!/usr/bin/env python3
"""Offline integrity check for GovCheck's bilingual reference catalogue.

Run from the repository root:
  python3 scripts/check-reference-integrity.py
  python3 scripts/check-reference-integrity.py --external
"""
from __future__ import annotations
import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CATALOGUES = {"en": DOCS / "references.md", "fr": DOCS / "references.fr.md"}
ANCHOR_RE = re.compile(r'<a id="r-(\d{2})"></a>')
REF_LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+references(?:\.fr)?\.md#r-(\d{2})[^)]*)\)', re.I)
LINK_RE = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')
URL_RE = re.compile(r'https?://[^\s)<>]+')
CITED_RE = {
    "en": re.compile(r'^- \*\*Cited by:\*\*\s*(.*)$', re.M),
    "fr": re.compile(r'^- \*\*Cité par :\*\*\s*(.*)$', re.M),
}
ERRORS: list[str] = []
WARNINGS: list[str] = []

def error(message: str) -> None:
    ERRORS.append(message)

def warning(message: str) -> None:
    WARNINGS.append(message)

def logical_doc(path: Path) -> str:
    rel = path.relative_to(DOCS).as_posix()
    return rel[:-6] + ".md" if rel.endswith(".fr.md") else rel

def catalogue_entries(path: Path, lang: str) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r'(?=<a id="r-\d{2}"></a>)', text)
    entries: dict[str, str] = {}
    for part in parts:
        match = ANCHOR_RE.search(part)
        if not match:
            continue
        ref_id = f"R-{match.group(1)}"
        if ref_id in entries:
            error(f"{path.relative_to(ROOT)}: duplicate entry {ref_id}")
        entries[ref_id] = part
        if len(CITED_RE[lang].findall(part)) != 1:
            error(f"{path.relative_to(ROOT)}: {ref_id} must have exactly one Cited by field")
        if not re.search(r'https?://', part):
            error(f"{path.relative_to(ROOT)}: {ref_id} has no external source URL")
    return entries

def markdown_targets(text: str):
    for match in LINK_RE.finditer(text):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        yield raw

def heading_anchors(text: str) -> set[str]:
    anchors = set(re.findall(r'<a id="([^"]+)"></a>', text, re.I))
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug = heading.strip().lower()
        slug = re.sub(r'[^\w\- ]', '', slug, flags=re.UNICODE)
        slug = re.sub(r'\s+', '-', slug)
        anchors.add(slug)
    return anchors

def check_local_links(markdown_files: list[Path]) -> None:
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for raw in markdown_targets(text):
            parsed = urllib.parse.urlsplit(raw)
            if parsed.scheme or parsed.netloc or raw.startswith("//"):
                continue
            rel = urllib.parse.unquote(parsed.path)
            target = source if not rel else (source.parent / rel).resolve()
            if not target.exists():
                error(f"{source.relative_to(ROOT)}: broken local link target {raw}")
                continue
            if parsed.fragment and target.suffix.lower() in {".md", ".markdown"}:
                anchors = heading_anchors(target.read_text(encoding="utf-8"))
                if urllib.parse.unquote(parsed.fragment) not in anchors:
                    error(f"{source.relative_to(ROOT)}: missing anchor #{parsed.fragment} in {target.relative_to(ROOT)}")

def check_references(external: bool) -> int:
    en = catalogue_entries(CATALOGUES["en"], "en")
    fr = catalogue_entries(CATALOGUES["fr"], "fr")
    if set(en) != set(fr):
        error(f"Catalogue IDs differ: EN-only={sorted(set(en)-set(fr))}; FR-only={sorted(set(fr)-set(en))}")
    markdown_files = sorted(DOCS.rglob("*.md"))
    source_docs = [p for p in markdown_files if p not in CATALOGUES.values()]
    citations: dict[str, set[str]] = defaultdict(set)
    document_links: dict[str, dict[str, set[str]]] = defaultdict(dict)
    linked_urls: set[str] = set()
    for path in source_docs:
        text = path.read_text(encoding="utf-8")
        logical = logical_doc(path)
        linked_ids = {f"R-{m.group(2)}" for m in REF_LINK_RE.finditer(text)}
        lang = "fr" if path.name.endswith(".fr.md") else "en"
        document_links[logical][lang] = linked_ids
        mentioned_ids = {f"R-{n}" for n in re.findall(r'\bR-(\d{2})\b', text)}
        for ref_id in sorted(mentioned_ids - linked_ids):
            error(f"{path.relative_to(ROOT)}: mentions {ref_id} without a catalogue link")
        for ref_id in linked_ids:
            if ref_id not in en or ref_id not in fr:
                error(f"{path.relative_to(ROOT)}: link to missing entry {ref_id}")
            citations[ref_id].add(logical)
    for logical, by_language in document_links.items():
        if "en" in by_language and "fr" in by_language and by_language["en"] != by_language["fr"]:
            error(
                f"{logical}: EN/FR citation mismatch; "
                f"EN={sorted(by_language['en'])}, FR={sorted(by_language['fr'])}"
            )
    for lang, entries in (("en", en), ("fr", fr)):
        catalogue = CATALOGUES[lang]
        for ref_id, block in entries.items():
            line = CITED_RE[lang].search(block)
            assert line is not None
            declared: set[str] = set()
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', line.group(1)):
                parsed = urllib.parse.urlsplit(target)
                if lang == "en" and parsed.path.endswith(".fr.md"):
                    error(f"{catalogue.relative_to(ROOT)}: English backlink uses French document path {target}")
                if lang == "fr" and not parsed.path.endswith(".fr.md"):
                    error(f"{catalogue.relative_to(ROOT)}: French backlink uses English document path {target}")
                path = (DOCS / urllib.parse.unquote(parsed.path)).resolve()
                if not path.exists():
                    error(f"{catalogue.relative_to(ROOT)}: {ref_id} backlinks to missing document {target}")
                    continue
                declared.add(logical_doc(path))
            expected = citations.get(ref_id, set())
            if declared != expected:
                error(f"{catalogue.relative_to(ROOT)}: {ref_id} backlink mismatch; declared={sorted(declared)}, actual={sorted(expected)}")
            linked_urls.update(URL_RE.findall(block))
    check_local_links(markdown_files)
    if external:
        for url in sorted(linked_urls):
            request = urllib.request.Request(url, headers={"User-Agent": "GovCheck-reference-check/1.0"}, method="HEAD")
            try:
                with urllib.request.urlopen(request, timeout=12) as response:
                    if response.status >= 400:
                        warning(f"external URL returned HTTP {response.status}: {url}")
            except urllib.error.HTTPError as exc:
                if exc.code in {403, 405, 501}:
                    try:
                        get_request = urllib.request.Request(url, headers={"User-Agent": "GovCheck-reference-check/1.0", "Range": "bytes=0-0"})
                        with urllib.request.urlopen(get_request, timeout=12) as response:
                            if response.status >= 400:
                                warning(f"external URL returned HTTP {response.status}: {url}")
                    except Exception as retry_exc:
                        warning(f"external URL could not be verified ({retry_exc}): {url}")
                else:
                    warning(f"external URL returned HTTP {exc.code}: {url}")
            except Exception as exc:
                warning(f"external URL could not be verified ({exc}): {url}")
    print(f"Reference integrity: {len(en)} entries; {len(citations)} cited entries; {len(source_docs)} Markdown documents scanned.")
    for item in WARNINGS:
        print(f"WARNING: {item}")
    for item in ERRORS:
        print(f"ERROR: {item}")
    if ERRORS:
        print(f"FAILED: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s).")
        return 1
    print(f"PASS: {len(WARNINGS)} warning(s).")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", action="store_true", help="probe external URLs; requires network access")
    return check_references(parser.parse_args().external)

if __name__ == "__main__":
    sys.exit(main())
