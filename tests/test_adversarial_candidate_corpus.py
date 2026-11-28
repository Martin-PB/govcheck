"""Validate the versioned adversarial-candidate corpus and its evidence pointers."""
import ast
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "formal" / "adversarial-candidate-corpus-v1.json"
SHA_RE = re.compile(r"^[0-9a-f]{40,64}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


class AdversarialCandidateCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_identity_and_source_revision_are_versioned(self):
        self.assertEqual(self.data["corpusId"], "govcheck.adversarial-candidate-corpus")
        self.assertEqual(self.data["schemaVersion"], 1)
        self.assertRegex(self.data["corpusVersion"], SEMVER_RE)
        self.assertRegex(self.data["sourceRevision"], SHA_RE)
        self.assertTrue(self.data["bindingPolicy"]["rule"])

    def test_case_ids_are_unique_and_every_case_declares_expected_semantics(self):
        cases = self.data["cases"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(cases), 20)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertRegex(case["id"], r"^AC-[0-9]{3}$")
                self.assertTrue(case["category"])
                self.assertTrue(case["attack"])
                self.assertTrue(case["expectedOutcome"])
                self.assertTrue(case["candidateBinding"])
                self.assertTrue(case["basePolicyBinding"])
                self.assertTrue(case["limitation"])
                self.assertEqual(case["deploymentStatus"], "not-demonstrated")

    def test_executable_test_evidence_points_to_real_test_methods(self):
        for case in self.data["cases"]:
            if case["coverageStatus"] not in {"tested-unit", "tested-integration"}:
                continue
            self.assertTrue(case["evidence"], case["id"])
            for reference in case["evidence"]:
                if "::" not in reference:
                    continue
                path, symbol = reference.split("::", 1)
                source = ROOT / path
                self.assertTrue(source.is_file(), f"{case['id']}: missing {path}")
                tree = ast.parse(source.read_text(encoding="utf-8"), filename=path)
                names = {
                    node.name for node in ast.walk(tree)
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                }
                self.assertIn(symbol, names, f"{case['id']}: missing {symbol} in {path}")

    def test_model_only_and_planned_cases_are_not_mislabeled_as_executed_tests(self):
        statuses = {case["id"]: case["coverageStatus"] for case in self.data["cases"]}
        self.assertEqual(statuses["AC-016"], "model-only")
        self.assertEqual(statuses["AC-017"], "planned")
        self.assertEqual(statuses["AC-018"], "planned")
        self.assertEqual(statuses["AC-019"], "planned")
        self.assertEqual(statuses["AC-020"], "not-demonstrated")
        self.assertEqual(statuses["AC-021"], "planned")
        self.assertEqual(statuses["AC-022"], "planned")

    def test_every_evidence_path_is_present(self):
        for case in self.data["cases"]:
            for reference in case["evidence"]:
                path = reference.split("::", 1)[0]
                if path.startswith("https://"):
                    continue
                with self.subTest(case=case["id"], path=path):
                    self.assertTrue((ROOT / path).is_file(), f"missing evidence path: {path}")


if __name__ == "__main__":
    unittest.main()
