import json
import tempfile
import unittest
from pathlib import Path

from govcheck.journal import Journal
from govcheck.git_publication_receipt import run_post_receive


class GitPublicationReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.git_dir = self.root / "repo.git"
        self.git_dir.mkdir()
        self.db = self.root / "journal.sqlite"
        self.scope = "repo:example/project"
        self.journal = Journal(self.db)
        self.journal.initialize(self.scope, "principal:root", "authority-rev-3", "gov-17")
        self.env = {
            "GIT_DIR": str(self.git_dir),
            "GOVCHECK_JOURNAL_DB": str(self.db),
            "GOVCHECK_JOURNAL_SCOPE_ID": self.scope,
            "GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:12345",
            "GOVCHECK_PROTECTED_REFS": "refs/heads/main",
        }
        self.old = "b" * 40
        self.new = "c" * 40

    def tearDown(self):
        self.temp.cleanup()

    def add_gate_receipt(self, result="pass", verification="authenticated-authority"):
        payload = {
            "repositoryId": "repo:12345",
            "candidateRevision": self.new,
            "baseRevision": self.old,
            "ref": "refs/heads/main",
            "decisionResult": result,
            "verification": verification,
            "authorityPrincipal": "principal:root" if verification == "authenticated-authority" else None,
            "decisionId": "decision-55",
        }
        head = self.journal.head(self.scope)
        self.journal.append(
            self.scope, head["position"], head["digest"], "gate-event-55",
            "govcheck.acceptance.gate-result/v1", "1", payload,
            "gate-key-55", "principal:root" if verification == "authenticated-authority" else "system:govcheck-gate",
        )

    def test_post_receive_records_publication_linked_to_verified_acceptance(self):
        self.add_gate_receipt()
        code, messages = run_post_receive(f"{self.old} {self.new} refs/heads/main\n", self.env)
        self.assertEqual(code, 0)
        self.assertTrue(messages[0].startswith("receipt: published"))
        self.assertEqual(self.journal.verify(self.scope)["status"], "valid")
        event = self.journal.find_latest_event(self.scope, "govcheck.git.ref-publication/v1", {
            "candidateRevision": self.new,
            "baseRevision": self.old,
            "ref": "refs/heads/main",
        })
        self.assertEqual(event["event"]["payload"]["publication"], "linked-to-verified-acceptance")

    def test_bypassed_or_unverified_publication_is_recorded_and_reported(self):
        code, messages = run_post_receive(f"{self.old} {self.new} refs/heads/main\n", self.env)
        self.assertEqual(code, 1)
        self.assertIn("already published", messages[0])
        event = self.journal.find_latest_event(self.scope, "govcheck.git.ref-publication/v1", {
            "candidateRevision": self.new,
            "baseRevision": self.old,
            "ref": "refs/heads/main",
        })
        self.assertEqual(event["event"]["payload"]["publication"], "published-without-verified-acceptance")

    def test_post_receive_replay_is_idempotent(self):
        self.add_gate_receipt()
        input_text = f"{self.old} {self.new} refs/heads/main\n"
        self.assertEqual(run_post_receive(input_text, self.env)[0], 0)
        self.assertEqual(run_post_receive(input_text, self.env)[0], 0)
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 3)

    def test_unprotected_ref_is_ignored(self):
        code, messages = run_post_receive(f"{self.old} {self.new} refs/heads/feature\n", self.env)
        self.assertEqual(code, 0)
        self.assertEqual(messages, [])
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 1)


if __name__ == "__main__":
    unittest.main()
