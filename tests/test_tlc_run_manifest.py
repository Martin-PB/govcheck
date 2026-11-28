import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from argparse import Namespace

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "tlc-run-manifest.py"
SPEC = importlib.util.spec_from_file_location("tlc_run_manifest", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class TlcRunManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        files = {
            "formal/tla/Example.tla": "---- MODULE Example ----\n====\n",
            "formal/tla/Example.cfg": "SPECIFICATION Spec\n",
            ".github/workflows/tla-model-reusable.yml": "name: reusable\n",
            ".github/workflows/example.yml": "name: caller\n",
            "sany-Example.txt": "SANY parsed\n",
            "tlc-Example-Example.txt": "Model checking completed\n",
            "tla2tools.sha256": "abc123  tla2tools.jar\n",
        }
        for name, content in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Manifest test")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.args = Namespace(
            model="Example", config="Example.cfg", workflow_ref="owner/repo/.github/workflows/example.yml@refs/pull/1/merge",
            event_path=None, run_id="123", run_attempt="2", event_name="pull_request",
            workflow_sha="deadbeef", java_version="17.0.12",
            sany_outcome="success", tlc_outcome="success",
        )
        self.manifest = MODULE.build_manifest(self.root, self.args)

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    def commit_change(self, path, content):
        target = self.root / path
        target.write_text(content, encoding="utf-8")
        self.git("add", path)
        self.git("commit", "-qm", "change " + path)

    def test_manifest_binds_run_sources_and_report_digests(self):
        self.assertEqual(self.manifest["format"], "govcheck.tlc-run-manifest/v1")
        self.assertEqual(self.manifest["run"]["id"], "123")
        self.assertEqual(self.manifest["run"]["attempt"], "2")
        self.assertEqual(self.manifest["invocation"]["tlcToolVersion"], "1.7.4")
        self.assertIn("callerWorkflow", self.manifest["sources"])
        self.assertTrue(all(item["present"] for item in self.manifest["reports"]))
        self.assertEqual(MODULE.verify_manifest(self.root, self.manifest), [])

    def test_rejects_stale_model_revision(self):
        self.commit_change("formal/tla/Example.tla", "---- MODULE Example ----\n\* changed\n====\n")
        errors = MODULE.verify_manifest(self.root, self.manifest)
        self.assertTrue(any("model" in error for error in errors))

    def test_rejects_stale_configuration_revision(self):
        self.commit_change("formal/tla/Example.cfg", "SPECIFICATION Other\n")
        errors = MODULE.verify_manifest(self.root, self.manifest)
        self.assertTrue(any("configuration" in error for error in errors))

    def test_rejects_stale_reusable_workflow_revision(self):
        self.commit_change(".github/workflows/tla-model-reusable.yml", "name: changed\n")
        errors = MODULE.verify_manifest(self.root, self.manifest)
        self.assertTrue(any("reusableWorkflow" in error for error in errors))

    def test_rejects_stale_caller_workflow_revision(self):
        self.commit_change(".github/workflows/example.yml", "name: changed caller\n")
        errors = MODULE.verify_manifest(self.root, self.manifest)
        self.assertTrue(any("callerWorkflow" in error for error in errors))

    def test_rejects_replayed_or_modified_report(self):
        report = self.root / "tlc-Example-Example.txt"
        report.write_text("replayed report from another run\n", encoding="utf-8")
        errors = MODULE.verify_manifest(self.root, self.manifest)
        self.assertTrue(any("digest or size" in error for error in errors))

    def test_rejects_missing_report(self):
        (self.root / "sany-Example.txt").unlink()
        errors = MODULE.verify_manifest(self.root, self.manifest)
        self.assertTrue(any("presence differs" in error for error in errors))

    def test_rejects_path_traversal(self):
        malicious = json.loads(json.dumps(self.manifest))
        malicious["reports"][0]["path"] = "../outside.txt"
        errors = MODULE.verify_manifest(self.root, malicious)
        self.assertTrue(any("escapes repository" in error for error in errors))

    def test_unsigned_boundary_is_explicit(self):
        self.assertEqual(
            self.manifest["trust"],
            "unsigned-integrity-record-not-an-authenticated-attestation",
        )


if __name__ == "__main__":
    unittest.main()
