import json
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit-ci-workflow-routing.py"
SPEC = importlib.util.spec_from_file_location("ci_workflow_routing_audit", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class CIWorkflowRoutingAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".github" / "workflows").mkdir(parents=True)
        policy_dir = self.root / "docs"
        policy_dir.mkdir()
        (policy_dir / "ci-routing-glob-policy.json").write_text(
            json.dumps({
                "format": "govcheck.ci-routing-glob-policy/v1",
                "patterns": [{"pattern": "src/**", "rationale": "Test-only source glob."}],
            }),
            encoding="utf-8",
        )
        model_dir = self.root / "formal" / "tla"
        model_dir.mkdir(parents=True)
        (model_dir / "CICheckRouting.tla").write_text(
            'Categories == {"TestCategory"}\nModelSpecific == {}\n',
            encoding="utf-8",
        )
        self.write_category_policy([{
            "name": "TestCategory", "modelSpecific": False, "paths": [], "workflows": [],
        }])

    def write_category_policy(self, categories):
        (self.root / "docs" / "ci-routing-category-policy.json").write_text(
            json.dumps({
                "format": "govcheck.ci-routing-category-policy/v1",
                "model": "formal/tla/CICheckRouting.tla",
                "categories": categories,
            }),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        path = self.root / ".github" / "workflows" / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_symmetric_event_paths_pass(self):
        self.write("shared.yml", """name: shared
on:
  pull_request:
    paths:
      - 'src/**'
      - '.github/workflows/shared.yml'
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '.github/workflows/shared.yml'
jobs:
  test:
    runs-on: ubuntu-latest
    steps: []
""")
        report = AUDIT.audit_workflows(self.root)
        self.assertEqual(report["finding_count"], 0)

    def test_asymmetric_paths_are_reported(self):
        (self.root / "docs" / "ci-routing-glob-policy.json").write_text(
            json.dumps({"format": "govcheck.ci-routing-glob-policy/v1", "patterns": []}),
            encoding="utf-8",
        )
        self.write("asymmetric.yml", """name: asymmetric
on:
  pull_request:
    paths:
      - 'formal/model.tla'
      - 'formal/model.cfg'
  push:
    branches: [main]
    paths:
      - 'formal/model.tla'
""")
        report = AUDIT.audit_workflows(self.root)
        self.assertEqual(report["finding_count"], 1)
        finding = report["findings"][0]
        self.assertEqual(finding["kind"], "event-path-asymmetry")
        self.assertEqual(finding["missing_from_push"], ["formal/model.cfg"])

    def test_reusable_workflow_must_exist_and_be_routed(self):
        self.write("reusable.yml", """name: reusable
on:
  workflow_call:
jobs:
  verify:
    runs-on: ubuntu-latest
""")
        self.write("caller.yml", """name: caller
on:
  pull_request:
    paths:
      - 'src/**'
  push:
    paths:
      - 'src/**'
jobs:
  verify:
    uses: ./.github/workflows/reusable.yml
""")
        report = AUDIT.audit_workflows(self.root)
        findings = [item for item in report["findings"] if item["kind"] == "reusable-workflow-not-routed"]
        self.assertEqual({item["event"] for item in findings}, {"pull_request", "push"})
        self.assertTrue(all(item["required_path"] == ".github/workflows/reusable.yml" for item in findings))

    def test_missing_reusable_workflow_is_rejected(self):
        self.write("caller.yml", """name: caller
on:
  pull_request:
    paths:
      - '.github/workflows/missing.yml'
jobs:
  verify:
    uses: ./.github/workflows/missing.yml
""")
        with self.assertRaises(AUDIT.WorkflowParseError):
            AUDIT.audit_workflows(self.root)

    def test_paths_ignore_is_rejected_not_silently_omitted(self):
        self.write("ignored.yml", """name: ignored
on:
  pull_request:
    paths-ignore:
      - 'docs/**'
""")
        with self.assertRaisesRegex(AUDIT.WorkflowParseError, "paths-ignore is not supported"):
            AUDIT.audit_workflows(self.root)

    def test_inline_paths_list_is_rejected_not_silently_omitted(self):
        self.write("inline.yml", """name: inline
on:
  pull_request:
    paths: ['src/**']
""")
        with self.assertRaisesRegex(AUDIT.WorkflowParseError, "inline or malformed"):
            AUDIT.audit_workflows(self.root)

    def test_unjustified_workflow_glob_is_reported(self):
        (self.root / "docs" / "ci-routing-glob-policy.json").write_text(
            json.dumps({"format": "govcheck.ci-routing-glob-policy/v1", "patterns": []}),
            encoding="utf-8",
        )
        self.write("glob.yml", """name: glob
on:
  pull_request:
    paths:
      - 'docs/**'
  push:
    paths:
      - 'docs/**'
""")
        report = AUDIT.audit_workflows(self.root)
        findings = [item for item in report["findings"] if item["kind"] == "unjustified-glob"]
        self.assertEqual([item["pattern"] for item in findings], ["docs/**"])

    def test_stale_glob_justification_is_reported(self):
        (self.root / "docs" / "ci-routing-glob-policy.json").write_text(
            json.dumps({
                "format": "govcheck.ci-routing-glob-policy/v1",
                "patterns": [{"pattern": "unused/**", "rationale": "No longer used."}],
            }),
            encoding="utf-8",
        )
        self.write("plain.yml", """name: plain
on:
  pull_request:
    paths:
      - 'src/file.py'
  push:
    paths:
      - 'src/file.py'
""")
        report = AUDIT.audit_workflows(self.root)
        findings = [item for item in report["findings"] if item["kind"] == "stale-glob-justification"]
        self.assertEqual([item["pattern"] for item in findings], ["unused/**"])

    def test_tla_category_inventory_is_checked_against_policy(self):
        report = AUDIT.audit_workflows(self.root)
        self.assertEqual(report["category_policy"]["model_categories"], ["TestCategory"])
        self.assertEqual(report["category_policy"]["policy_categories"], ["TestCategory"])

    def test_tla_model_category_drift_is_reported(self):
        (self.root / "formal" / "tla" / "CICheckRouting.tla").write_text(
            'Categories == {"NewCategory"}\nModelSpecific == {}\n',
            encoding="utf-8",
        )
        report = AUDIT.audit_workflows(self.root)
        self.assertIn("model-category-inventory-mismatch", {item["kind"] for item in report["findings"]})

    def test_model_specific_category_paths_must_route_to_workflow(self):
        (self.root / "formal" / "tla" / "CICheckRouting.tla").write_text(
            'Categories == {"TestCategory"}\nModelSpecific == {"TestCategory"}\n',
            encoding="utf-8",
        )
        self.write_category_policy([{
            "name": "TestCategory",
            "modelSpecific": True,
            "paths": ["formal/model.tla"],
            "workflows": [".github/workflows/model.yml"],
        }])
        self.write("model.yml", """name: model
on:
  pull_request:
    paths:
      - 'other/**'
  push:
    paths:
      - 'other/**'
""")
        (self.root / "formal" / "model.tla").write_text("---- MODULE Model ----\n", encoding="utf-8")
        report = AUDIT.audit_workflows(self.root)
        findings = [item for item in report["findings"] if item["kind"] == "model-category-path-missing"]
        self.assertEqual({item["event"] for item in findings}, {"pull_request", "push"})

    def test_unsupported_path_entry_is_rejected_not_ignored(self):
        self.write("bad.yml", """name: bad
on:
  pull_request:
    paths:
      - 'src/**'
      - key: value
""")
        with self.assertRaises(AUDIT.WorkflowParseError):
            AUDIT.audit_workflows(self.root)


if __name__ == "__main__":
    unittest.main()
