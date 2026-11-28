import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from govcheck import acceptance_journal
from govcheck.journal import Journal


class AcceptanceJournalIntegrationTests(unittest.TestCase):
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
            "GOVCHECK_JOURNAL_AUTHORITY_REVISION": "authority-rev-3",
            "GOVCHECK_SCOPE_ID": self.scope,
            "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
        }
        self.payload = {
            "decision_id": "decision-42",
            "result": "pass",
            "authority_principal": "principal:root",
            "policy_digest": "sha256:" + "a" * 64,
            "evidence_digest": "sha256:" + "b" * 64,
            "repository_id": "repo:12345",
            "candidate": "c" * 40,
            "base": "b" * 40,
            "ref": "refs/heads/main",
            "risk_acceptance": None,
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_verified_decision_gets_durable_receipt_and_replay_is_idempotent(self):
        first = acceptance_journal.append_verified_decision(self.env, self.payload)
        second = acceptance_journal.append_verified_decision(self.env, self.payload)
        self.assertEqual(first["eventDigest"], second["eventDigest"])
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 2)
        receipt = self.journal.receipt(self.scope, first["idempotencyKey"])
        self.assertEqual(receipt, first)

    def test_no_journal_configuration_preserves_legacy_optional_mode(self):
        self.assertIsNone(acceptance_journal.append_verified_decision({}, self.payload))

    def test_partial_configuration_fails_closed(self):
        with self.assertRaises(acceptance_journal.AcceptanceJournalError):
            acceptance_journal.append_verified_decision({"GOVCHECK_JOURNAL_DB": str(self.db)}, self.payload)

    def test_wrong_genesis_authority_fails_closed(self):
        self.payload["authority_principal"] = "principal:other"
        with self.assertRaises(acceptance_journal.AcceptanceJournalError):
            acceptance_journal.append_verified_decision(self.env, self.payload)
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 1)

    def test_journal_inside_bare_repository_is_rejected(self):
        self.env["GOVCHECK_JOURNAL_DB"] = str(self.git_dir / "journal.sqlite")
        with self.assertRaises(acceptance_journal.AcceptanceJournalError):
            acceptance_journal.append_verified_decision(self.env, self.payload)


if __name__ == "__main__":
    unittest.main()
