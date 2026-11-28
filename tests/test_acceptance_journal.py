import hashlib
import json
import sqlite3
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
            "GOVCHECK_REPOSITORY_URI": "https://example.invalid/repo",
            "GOVCHECK_GOVERNANCE_DIGEST": "sha256:" + "c" * 64,
            "GOVCHECK_SCOPE_ID": self.scope,
            "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
        }
        self.payload = {
            "decision_id": "decision-42",
            "decision_time": "2026-11-28T12:00:00Z",
            "result": "pass",
            "authority_principal": "principal:root",
            "policy_digest": "sha256:" + "a" * 64,
            "evidence_digest": "sha256:" + "b" * 64,
            "repository_id": "repo:12345",
            "candidate": "c" * 40,
            "base": "b" * 40,
            "candidate_content_digest": "sha256:" + "a" * 64,
            "base_content_digest": "sha256:" + "b" * 64,
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

    def test_receipt_embeds_exact_typed_git_provenance(self):
        receipt = acceptance_journal.append_verified_decision(self.env, self.payload)
        with sqlite3.connect(self.db) as connection:
            row = connection.execute("SELECT envelope_json FROM journal_events WHERE position=?", (receipt["position"],)).fetchone()
        event = json.loads(row[0])
        provenance = event["payload"]["vcsProvenance"]
        self.assertEqual(provenance["vcs"]["kind"], "git")
        self.assertEqual(provenance["candidate"]["nativeRevision"], "c" * 40)
        self.assertEqual(provenance["base"]["nativeRevision"], "b" * 40)
        self.assertEqual(provenance["candidate"]["contentDigest"], "sha256:" + "a" * 64)
        self.assertEqual(provenance["target"]["name"], "refs/heads/main")

    def test_missing_repository_uri_or_governance_digest_fails_closed(self):
        self.env.pop("GOVCHECK_REPOSITORY_URI")
        with self.assertRaises(acceptance_journal.AcceptanceJournalError):
            acceptance_journal.append_verified_decision(self.env, self.payload)
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 1)

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

    def test_unverified_unknown_gate_attempt_is_recorded_as_system_attribution(self):
        self.env["GOVCHECK_JOURNAL_AUTHORITY_ID"] = "principal:root"
        self.payload.update({
            "decision_id": "unavailable",
            "result": "unknown",
            "authority_principal": "",
            "reason": "signature verification unavailable",
        })
        receipt = acceptance_journal.append_verified_decision(self.env, self.payload)
        with sqlite3.connect(self.db) as connection:
            row = connection.execute("SELECT envelope_json FROM journal_events WHERE position=?", (receipt["position"],)).fetchone()
        event = json.loads(row[0])
        self.assertEqual(event["actorId"], "system:govcheck-gate")
        self.assertEqual(event["eventType"], "govcheck.acceptance.gate-result/v1")
        self.assertEqual(event["payload"]["verification"], "unverified-gate-attempt")
        self.assertEqual(self.journal.verify(self.scope)["status"], "valid")

    def test_journal_inside_bare_repository_is_rejected(self):
        self.env["GOVCHECK_JOURNAL_DB"] = str(self.git_dir / "journal.sqlite")
        with self.assertRaises(acceptance_journal.AcceptanceJournalError):
            acceptance_journal.append_verified_decision(self.env, self.payload)


if __name__ == "__main__":
    unittest.main()
