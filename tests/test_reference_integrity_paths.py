#!/usr/bin/env python3
"""Regression tests for repository-wide reference-catalogue document paths."""
from __future__ import annotations

import importlib.util
from contextlib import ExitStack
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_reference_integrity", ROOT / "scripts" / "check-reference-integrity.py"
)
CHECK = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECK)


class RepositoryMarkdownPathTests(unittest.TestCase):
    def test_logical_doc_accepts_formal_document_outside_docs(self):
        path = ROOT / "formal" / "lean" / "README.md"
        self.assertEqual(CHECK.logical_doc(path), "formal/lean/README.md")

    def test_repository_scan_includes_formal_sources(self):
        files = CHECK.repository_markdown_files()
        self.assertIn(ROOT / "formal" / "lean" / "README.md", files)

    def test_repository_scan_excludes_installed_package_mirror(self):
        files = CHECK.repository_markdown_files()
        self.assertFalse(any(path.is_relative_to(ROOT / "govcheck") for path in files))

    def test_bilingual_identity_uses_same_logical_document(self):
        english = ROOT / "formal" / "lean" / "README.md"
        french = ROOT / "formal" / "lean" / "README.fr.md"
        self.assertEqual(CHECK.logical_doc(english), CHECK.logical_doc(french))

    def test_external_source_backlinks_are_checked_repository_wide(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            docs = root / "docs"
            formal = root / "formal" / "lean"
            docs.mkdir(parents=True)
            formal.mkdir(parents=True)

            en_catalogue = """# Catalogue

## Thematic index

| Theme | Entries |
|---|---|
| Formal methods | R-01 |

## Full entries

<a id="r-01"></a>
### R-01 — Example source
- **Cited by:** [Lean README](../formal/lean/README.md)
- **Source:** https://example.org/spec
"""
            fr_catalogue = """# Catalogue

## Index thématique

| Thème | Entrées |
|---|---|
| Méthodes formelles | R-01 |

## Entrées complètes

<a id="r-01"></a>
### R-01 — Source exemple
- **Cité par :** [README Lean](../formal/lean/README.fr.md)
- **Source :** https://example.org/spec
"""
            (docs / "references.md").write_text(en_catalogue, encoding="utf-8")
            (docs / "references.fr.md").write_text(fr_catalogue, encoding="utf-8")
            (formal / "README.md").write_text(
                "# Lean coherence\n\nSee [R-01](../../docs/references.md#r-01).\n",
                encoding="utf-8",
            )
            (formal / "README.fr.md").write_text(
                "# Cohérence Lean\n\nVoir [R-01](../../docs/references.fr.md#r-01).\n",
                encoding="utf-8",
            )

            with ExitStack() as stack:
                stack.enter_context(patch.object(CHECK, "ROOT", root))
                stack.enter_context(patch.object(CHECK, "DOCS", docs))
                stack.enter_context(patch.object(CHECK, "CATALOGUES", {
                    "en": docs / "references.md",
                    "fr": docs / "references.fr.md",
                }))
                stack.enter_context(patch.object(CHECK, "ERRORS", []))
                stack.enter_context(patch.object(CHECK, "WARNINGS", []))
                self.assertEqual(CHECK.check_references(external=False), 0)

                # Once a French counterpart exists, the French catalogue
                # must not keep pointing to the English-only fallback.
                (docs / "references.fr.md").write_text(
                    fr_catalogue.replace(
                        "../formal/lean/README.fr.md",
                        "../formal/lean/README.md",
                    ),
                    encoding="utf-8",
                )
                self.assertEqual(CHECK.check_references(external=False), 1)


    def test_french_catalogue_allows_english_only_source_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            docs = root / "docs"
            formal = root / "formal" / "lean"
            docs.mkdir(parents=True)
            formal.mkdir(parents=True)

            en_catalogue = """# Catalogue

## Thematic index

| Theme | Entries |
|---|---|
| Formal methods | R-01 |

## Full entries

<a id="r-01"></a>
### R-01 — Example source
- **Cited by:** [Lean README](../formal/lean/README.md)
- **Source:** https://example.org/spec
"""
            fr_catalogue = """# Catalogue

## Index thématique

| Thème | Entrées |
|---|---|
| Méthodes formelles | R-01 |

## Entrées complètes

<a id="r-01"></a>
### R-01 — Source exemple
- **Cité par :** [README Lean](../formal/lean/README.md)
- **Source :** https://example.org/spec
"""
            (docs / "references.md").write_text(en_catalogue, encoding="utf-8")
            (docs / "references.fr.md").write_text(fr_catalogue, encoding="utf-8")
            (formal / "README.md").write_text(
                "# Lean coherence\n\nSee [R-01](../../docs/references.md#r-01).\n",
                encoding="utf-8",
            )

            with ExitStack() as stack:
                stack.enter_context(patch.object(CHECK, "ROOT", root))
                stack.enter_context(patch.object(CHECK, "DOCS", docs))
                stack.enter_context(patch.object(CHECK, "CATALOGUES", {
                    "en": docs / "references.md",
                    "fr": docs / "references.fr.md",
                }))
                stack.enter_context(patch.object(CHECK, "ERRORS", []))
                stack.enter_context(patch.object(CHECK, "WARNINGS", []))
                self.assertEqual(CHECK.check_references(external=False), 0)



if __name__ == "__main__":
    unittest.main()
