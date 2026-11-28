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
