#!/usr/bin/env python3
"""Tests for the bootstrap inspect/plan/apply/rollback contract (govcheck/bootstrap.py)."""
from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("govcheck_bootstrap", ROOT / "govcheck" / "bootstrap.py")
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)

ALL = list(bootstrap.DEFAULT_CAPABILITIES)


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name) / "repo"

    def test_package_identity_is_stable(self):
        self.assertEqual(bootstrap.package_digest(), bootstrap.package_digest())
        self.assertTrue(bootstrap.package_version())
        files = bootstrap.package_files()
        self.assertIn("check.py", files)
        self.assertNotIn("bootstrap.py", files)

    def test_inspect_does_not_mutate_missing_target(self):
        rep = bootstrap.inspect_target(self.target)
        self.assertFalse(self.target.exists())
        self.assertFalse(rep["exists"])
        self.assertTrue(rep["empty"])
        self.assertEqual(rep["conflicts"], [])
        self.assertIsNone(rep["marker"])

    def test_plan_is_deterministic_and_side_effect_free(self):
        p1 = bootstrap.build_plan(self.target, ALL)
        p2 = bootstrap.build_plan(self.target, ALL)
        self.assertEqual(json.dumps(p1), json.dumps(p2))
        self.assertFalse(self.target.exists())
        self.assertGreater(len(p1["actions"]), 5)
        self.assertTrue(all(a["action"] == "create" for a in p1["actions"]))

    def test_apply_then_idempotent(self):
        r1, code = bootstrap.apply_plan(self.target, ALL)
        self.assertEqual(code, 0)
        self.assertGreater(r1["created_count"], 5)
        self.assertTrue((self.target / "check.py").is_file())
        self.assertTrue((self.target / bootstrap.MARKER_NAME).is_file())
        r2, code2 = bootstrap.apply_plan(self.target, ALL)
        self.assertEqual(code2, 0)
        self.assertEqual(r2["created_count"], 0)
        self.assertEqual(r2["already_present"], r1["created_count"])
        self.assertEqual(r2["conflicts_preserved"], [])

    def test_apply_preserves_conflicting_user_content(self):
        victim_dir = self.target / "docs" / "specifications"
        victim_dir.mkdir(parents=True)
        f = victim_dir / "0002-canonical-governance-model.md"
        f.write_text("# my own spec" + chr(10), encoding="utf-8")
        r, code = bootstrap.apply_plan(self.target, ALL)
        self.assertEqual(code, 0)
        self.assertIn("docs/specifications/0002-canonical-governance-model.md", r["conflicts_preserved"])
        self.assertEqual(f.read_text(encoding="utf-8"), "# my own spec" + chr(10))

    def test_apply_with_stale_plan_aborts_without_writing(self):
        plan_path = Path(self.tmp.name) / "plan.json"
        plan = bootstrap.build_plan(self.target, ALL)
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        self.target.mkdir(parents=True)
        (self.target / "check.py").write_text("tampered" + chr(10), encoding="utf-8")
        r, code = bootstrap.apply_plan(self.target, ALL, plan_path=str(plan_path))
        self.assertEqual(code, 2)
        self.assertEqual((self.target / "check.py").read_text(encoding="utf-8"), "tampered" + chr(10))
        self.assertFalse((self.target / bootstrap.MARKER_NAME).exists())

    def test_apply_with_matching_plan_applies(self):
        plan_path = Path(self.tmp.name) / "plan.json"
        plan = bootstrap.build_plan(self.target, ALL)
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        r, code = bootstrap.apply_plan(self.target, ALL, plan_path=str(plan_path))
        self.assertEqual(code, 0)
        self.assertGreater(r["created_count"], 0)

    def test_capabilities_subset_creates_only_selected_parts(self):
        r, code = bootstrap.apply_plan(self.target, ["check"])
        self.assertEqual(code, 0)
        self.assertEqual([a["path"] for a in r["created"]], ["check.py"])
        self.assertFalse((self.target / "docs").exists())

    def test_inspect_reports_previous_marker(self):
        bootstrap.apply_plan(self.target, ["check"])
        rep = bootstrap.inspect_target(self.target)
        self.assertIsNotNone(rep["marker"])
        self.assertEqual(rep["marker"]["package_digest"], bootstrap.package_digest())
        self.assertIn("check.py", rep["present_top_level"])
        self.assertFalse(rep["empty"])

    def test_rollback_removes_only_installed_files(self):
        self.target.mkdir(parents=True)
        user = self.target / "my-notes.txt"
        user.write_text("keep me" + chr(10), encoding="utf-8")
        bootstrap.apply_plan(self.target, ["check"])
        r, code = bootstrap.rollback_target(self.target)
        self.assertEqual(code, 0)
        self.assertEqual(r["removed"], ["check.py"])
        self.assertFalse((self.target / "check.py").exists())
        self.assertFalse((self.target / bootstrap.MARKER_NAME).exists())
        self.assertEqual(user.read_text(encoding="utf-8"), "keep me" + chr(10))

    def test_rollback_without_marker_fails(self):
        self.target.mkdir(parents=True)
        r, code = bootstrap.rollback_target(self.target)
        self.assertEqual(code, 1)

    def test_legacy_init_refuses_non_empty_target(self):
        self.target.mkdir(parents=True)
        (self.target / "x.txt").write_text("x" + chr(10), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = bootstrap.main([str(self.target)])
        self.assertEqual(code, 1)
        self.assertIn("not empty", buf.getvalue())

    def test_legacy_init_empty_target(self):
        with redirect_stdout(io.StringIO()):
            code = bootstrap.main([str(self.target)])
        self.assertEqual(code, 0)
        self.assertTrue((self.target / "check.py").is_file())
        self.assertFalse((self.target / "bootstrap.py").exists())

    def test_cli_plan_then_apply(self):
        out = Path(self.tmp.name) / "plan.json"
        with redirect_stdout(io.StringIO()):
            c1 = bootstrap.main(["plan", str(self.target), "--capabilities", "check", "--out", str(out)])
            c2 = bootstrap.main(["apply", str(self.target), "--capabilities", "check", "--plan", str(out)])
        self.assertEqual((c1, c2), (0, 0))
        self.assertTrue((self.target / "check.py").is_file())
        self.assertTrue(out.is_file())



class ForgeCapabilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name) / "repo"

    def test_forge_py_is_a_package_file(self):
        self.assertIn("forge.py", bootstrap.package_files())

    def test_forge_capability_installs_only_forge_py(self):
        r, code = bootstrap.apply_plan(self.target, ["forge"])
        self.assertEqual(code, 0)
        self.assertEqual([a["path"] for a in r["created"]], ["forge.py"])
        self.assertTrue((self.target / "forge.py").is_file())

if __name__ == "__main__":
    unittest.main()
