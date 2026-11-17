#!/usr/bin/env python3
"""Regression tests for repository-wide reference-catalogue document paths."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

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


if __name__ == "__main__":
    unittest.main()
