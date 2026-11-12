#!/usr/bin/env python3
"""Tests for the first GovCheck executable slice (govcheck/check.py)."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("govcheck_check", ROOT / "govcheck" / "check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def build_tree(root: Path) -> None:
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
    dec = root / "docs" / "decisions"
    dec.mkdir(parents=True)
    (dec / "README.md").write_text("# Decisions\n", encoding="utf-8")
    (dec / "README.fr.md").write_text("# D\u00e9cisions\n", encoding="utf-8")
    (dec / "0001-a.md").write_text("# A\n\n## References\n\n- [R-01](../references.md#r-01)\n", encoding="utf-8")
    (dec / "0001-a.fr.md").write_text("# A\n\n## R\u00e9f\u00e9rences\n\n- [R-01](../references.fr.md#r-01)\n", encoding="utf-8")
    specs = root / "docs" / "specifications"
    specs.mkdir(parents=True)
    (specs / "0001-a.md").write_text("# Spec\n\nSee [R-01](../references.md#r-01).\n", encoding="utf-8")
    pkg = root / "govcheck" / "docs" / "specifications"
    pkg.mkdir(parents=True)
    (pkg / "0001-a.md").write_text("# Spec\n", encoding="utf-8")
    (root / "docs" / "template-manifest.json").write_text(
        json.dumps({"pairs": {"docs/specifications/0001-a.md": {}}}), encoding="utf-8"
    )
    for name in ("references.md", "references.fr.md"):
        (root / "docs" / name).write_text(
            '# Catalogue\n\n<a id="r-01"></a>\n### R-01 \u2014 Example\n\n- **Source:** https://example.org\n',
            encoding="utf-8",
        )


def add_attestation(root: Path, reviewer="Bob <bob@example.org>", rev="deadbeef" * 5, decision="accept") -> None:
    d = root / "docs" / "attestations"
    d.mkdir(parents=True, exist_ok=True)
    (d / "000
1.json").write_text(json.dumps({
        "decision": decision,
        "candidate_rev": rev,
        "reviewer": reviewer,
        "date": "2026-11-09",
        "sources": ["https://example.org/review-notes"],
    }), encoding="utf-8")


class EvaluateTests(unittest.TestCase):
    def run_cli(self, root, extra=None):
        buf = io.StringIO()
        argv = ["--tree", str(root)] + (extra or [])
        with redirect_stdout(buf):
            code = check.main(argv)
        return code, buf.getvalue()

    def test_passing_tree_exits_zero(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "pass")
            code, out = self.run_cli(root)
            self.assertEqual(code, 0)
            self.assertIn("PASS", out)

    def test_missing_license_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "LICENSE").unlink()
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "license-present")
            self.assertEqual(rule["result"], "fail")
            code, _ = self.run_cli(root)
            self.assertEqual(code, 1)

    def test_missing_fr_twin_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "docs" / "decisions" / "0001-a.fr.md").unlink()
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "bilingual-decisions")
            self.assertEqual(rule["result"], "fail")

    def test_unknown_reference_mention_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
          
  p = root / "docs" / "specifications" / "0001-a.md"
            p.write_text(p.read_text(encoding="utf-8") + "Also R-99.\n", encoding="utf-8")
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "reference-integrity")
            self.assertEqual(rule["result"], "fail")

    def test_manifest_pair_missing_in_package_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "govcheck" / "docs" / "specifications" / "0001-a.md").unlink()
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "manifest-pairs")
            self.assertEqual(rule["result"], "fail")

    def test_tla_presence_is_unknown_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            tla = root / "formal" / "tla"
            tla.mkdir(parents=True)
            (tla / "Spec.tla").write_text("---- MODULE Spec ----\n", encoding="utf-8")
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "unknown")
            code, out = self.run_cli(root)
            self.assertEqual(code, 1)
            self.assertIn("UNKNOWN", out)

    def test_out_writes_json_report(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            out = root / "report.json"
            code, _ = self.run_cli(root, ["--out", str(out)])
            self.assertEqual(code, 0)
            report = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(report["tool"], "govcheck")
            self.assertEqual(report["overall"], "pass")
            self.assertEqual(len(report["rules"]), 8)

    def test_review_unknown_without_attestation(self):
        
with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            git = {"candidate_rev": "a" * 40, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"docs/specifications/0001-a.md"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "unknown")
            self.assertEqual(rule["applies"], True)

    def test_review_passes_with_distinct_reviewer_attestation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            rev = "a" * 40
            add_attestation(root, reviewer="Bob <bob@example.org>", rev=rev)
            git = {"candidate_rev": rev, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"x.md"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "pass")

    def test_review_ignores_attestation_by_the_author(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            rev = "a" * 40
            add_attestation(root, reviewer="Alice <alice@example.org>", rev=rev)
            git = {"candidate_rev": rev, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"x.md"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "unknown")

    def test_review_ignores_attestation_for_other_revision(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            add_attestation(root, reviewer="Bob <bob@example.org>", rev="b" * 40)
            git = {"candidate_rev": "a" * 40, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"x.m
d"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "unknown")


    def test_decision_without_references_section_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "docs" / "decisions" / "0001-a.md").write_text("# A\n", encoding="utf-8")
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "fail")

    def test_references_section_without_source_link_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "docs" / "decisions" / "0001-a.md").write_text(
                "# A\n\n## References\n\n- [internal](0001-a.fr.md)\n", encoding="utf-8"
            )
            report = check.evaluate(root)
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "fail")

    def test_attestation_without_sources_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            att = root / "docs" / "attestations"
            att.mkdir(parents=True)
            (att / "0001.json").write_text(json.dumps({
                "decision": "accept",
                "candidate_rev": "a" * 40,
                "reviewer": "Bob <bob@example.org>",
            }), encoding="utf-8")
            report = check.evaluate(root)
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "fail")

    def test_sources_present_not_applicable_without_decisions(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
 
           shutil.rmtree(root / "docs" / "decisions")
            report = check.evaluate(root)
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "pass")
            self.assertEqual(rule["applies"], False)


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_marker(root, installed=None, digest="0" * 64, conflicts=None, raw=None):
    marker = root / ".govcheck-bootstrap.json"
    if raw is not None:
        marker.write_text(raw, encoding="utf-8")
        return marker
    payload = {
        "tool": "govcheck-bootstrap",
        "package_version": "0.4.0-slice",
        "package_digest": digest,
        "capabilities": ["check"],
        "installed": installed if installed is not None else [],
        "conflicts": conflicts if conflicts is not None else [],
    }
    marker.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return marker


class BootstrapIntegrityTests(unittest.TestCase):
    def _report(self, root):
        ctx = mod.Ctx(tree=root)
        return mod.evaluate([mod.find_rule("bootstrap-integrity")], ctx)

    def test_not_applicable_without_marker(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root / "decision.md").write_text("# d\n", encoding="utf-8")
            report = self._report(root)
            rule = report["rules"][0]
            self.assertEqual(rule["result"], "pass")
            self.assertEqual(rule["applies"], False)

    def test_valid_marker_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            f = root / "check.py"
            f.write_text("print(1)\n", encoding="utf-8")
            add_marker(root, installed=[{"path": "check.py", "sha256": sha256_of(f)}])
            report = self._report(root)
            rule = report["rules"][0]
            self.assertEqual(rule["result"], "pass")
            self.assertEqual(rule["applies"], True)

    def test_drifted_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            f = root / "check.py"
            f.write_text("print(1)\n", encoding="utf-8")
            add_marker(root, installed=[{"path": "check.py", "sha256": "0" * 64}])
            report = self._report(root)
            rule = report["rules"][0]
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("drifted" in r for r in rule["reasons"]))

    def test_missing_installed_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            add_marker(root, installed=[{"path": "gone.txt", "sha256": "0" * 64}])
            report = self._report(root)
            rule = report["rules"][0]
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("missing" in r for r in rule["reasons"]))

    def test_invalid_json_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            add_marker(root, raw="{not json")
            report = self._report(root)
            rule = report["rules"][0]
            self.assertEqual(rule["result"], "fail")

    def test_unsafe_path_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            add_marker(root, installed=[{"path": "../evil", "sha256": "0" * 64}])
            report = self._report(root)
            rule = report["rules"][0]
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("unsafe" in r for r in rule["reasons"]))

    def test_bad_package_digest_field_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            add_marker(root, digest="xyz")
            report = self._report(root)
            rule = report["rules"][0]
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("package_digest" in r for r in rule["reasons"]))


if __name__ == "__main__":
    unittest.main()
