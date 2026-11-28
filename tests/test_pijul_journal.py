import tempfile
import unittest
from pathlib import Path

from govcheck.journal import Journal
from govcheck.vcs_provenance import build_pijul_provenance
from govcheck.pijul_journal import PijulJournalError, append_pijul_observation


class PijulJournalObserverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = self.root / "journal.sqlite"
        self.scope = "repo:example/project"
        self.journal = Journal(self.db)
        self.journal.initialize(self.scope, "principal:root", "authority-rev-3", "gov-17")
        self.env = {
            "GOVCHECK_JOURNAL_DB": str(self.db),
            "GOVCHECK_JOURNAL_SCOPE_ID": self.scope,
            "GOVCHECK_JOURNAL_AUTHORITY_ID": "principal:root",
            "GOVCHECK_JOURNAL_AUTHORITY_REVISION": "authority-rev-3",
            "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
            "GOVCHECK_GOVERNANCE_DIGEST": "sha256:" + "c" * 64,
            "GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:12345",
            "GOVCHECK_REPOSITORY_URI": "https://nest.pijul.com/example/project",
        }
        self.record = build_pijul_provenance(
            repository_id="repo:12345",
            repository_uri=self.env["GOVCHECK_REPOSITORY_URI"],
            target_channel="main",
            candidate_channel_hash="3WW3T5GBOOR3OCU2IDEVHHA7GGXMOHJDOYHCH7L5BWUGHUBHHQIQC",
            candidate_content_digest="sha256:" + "a" * 64,
            base_channel_hash="5HWYGVSSDKMEQP43H3JDSURPS7FJB4TXMAGMUAKSKWIFH6QRZN3QC",
            base_content_digest="sha256:" + "b" * 64,
            native_change_hashes=["GBO3OSMXODHKWDCJRYG3SFVKZH6LZLHJY7L7VUPDQKXO2266P3EQC"],
            governance_scope_id=self.scope,
            governance_revision="gov-17",
            governance_digest=self.env["GOVCHECK_GOVERNANCE_DIGEST"],
            adapter_id="govcheck.pijul-local-observer",
            adapter_version="1",
            observed_at="2026-11-28T12:00:00Z",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_records_native_channel_and_change_hashes_with_system_attribution(self):
        receipt = append_pijul_observation(self.env, self.record)
        event = self.journal.receipt(self.scope, receipt["idempotencyKey"])
        self.assertEqual(event, receipt)
        found = self.journal.find_latest_event(self.scope, "govcheck.pijul.provenance-observed/v1", {
            "observationKind": "channel-state-observed",
            "repositoryId": "repo:12345",
        })
        payload = found["event"]["payload"]
        self.assertEqual(payload["vcsProvenance"]["vcs"]["kind"], "pijul")
        self.assertEqual(payload["vcsProvenance"]["target"]["name"], "main")
        self.assertEqual(payload["authorityStatus"], "not-established-by-vcs-observation")
        self.assertEqual(found["event"]["actorId"], "system:govcheck-pijul-provenance-observer")
        self.assertEqual(self.journal.verify(self.scope)["status"], "valid")

    def test_replay_is_idempotent(self):
        first = append_pijul_observation(self.env, self.record)
        second = append_pijul_observation(self.env, self.record)
        self.assertEqual(first["eventDigest"], second["eventDigest"])
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 2)

    def test_mismatched_repository_or_governance_is_rejected(self):
        env = dict(self.env, GOVCHECK_EXPECTED_REPOSITORY_ID="repo:other")
        with self.assertRaises(PijulJournalError):
            append_pijul_observation(env, self.record)
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 1)

    def test_remote_acceptance_claim_is_not_a_supported_observation_kind(self):
        with self.assertRaises(PijulJournalError):
            append_pijul_observation(self.env, self.record, observation_kind="remote-accepted")
        self.assertEqual(self.journal.verify(self.scope)["eventCount"], 1)

    def test_partial_journal_configuration_fails_closed(self):
        with self.assertRaises(PijulJournalError):
            append_pijul_observation({"GOVCHECK_JOURNAL_DB": str(self.db)}, self.record)

    def test_no_journal_configuration_keeps_observer_optional(self):
        self.assertIsNone(append_pijul_observation({}, self.record))


if __name__ == "__main__":
    unittest.main()
