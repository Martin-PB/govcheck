import base64
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from govcheck import attestation, attestation_verify
from govcheck.journal import Journal
from govcheck.journal_attestation import (
    JournalAttestationError,
    build_journal_receipt_statement,
    sign_journal_receipt,
)
from govcheck.vcs_provenance import build_git_provenance


@unittest.skipUnless(shutil.which("openssl"), "OpenSSL CLI is required for Ed25519 receipt tests")
class JournalReceiptAttestationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repository"
        self.repo.mkdir()
        self.db = self.root / "journal.sqlite"
        self.private_key = self.root / "authority-private.pem"
        self.public_key = self.root / "authority-public.pem"
        self.openssl = Path(shutil.which("openssl")).resolve()
        subprocess.run(["openssl", "genpkey", "-algorithm", "ED25519", "-out", str(self.private_key)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.chmod(self.private_key, 0o600)
        subprocess.run(["openssl", "pkey", "-in", str(self.private_key), "-pubout", "-out", str(self.public_key)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.scope = "repo:example/project"
        self.journal = Journal(self.db)
        self.journal.initialize(self.scope, "principal:root", "authority-rev-3", "gov-17")
        provenance = build_git_provenance(
            repository_id="repo:12345",
            repository_uri="https://example.invalid/repo",
            target_ref="refs/heads/main",
            candidate_commit="c" * 40,
            candidate_content_digest="sha256:" + "a" * 64,
            base_commit="b" * 40,
            base_content_digest="sha256:" + "b" * 64,
            governance_scope_id=self.scope,
            governance_revision="gov-17",
            governance_digest="sha256:" + "c" * 64,
            adapter_id="govcheck.git-acceptance-gate",
            adapter_version="1",
            observed_at="2026-11-28T12:00:00Z",
        )
        payload = {
            "repositoryId": "repo:12345",
            "scopeId": self.scope,
            "candidateRevision": "c" * 40,
            "baseRevision": "b" * 40,
            "ref": "refs/heads/main",
            "governanceRevision": "gov-17",
            "vcsProvenance": provenance,
        }
        head = self.journal.head(self.scope)
        self.journal.append(
            self.scope, head["position"], head["digest"], "gate-event-1",
            "govcheck.acceptance.gate-result/v1", "1", payload,
            "gate-key-1", "principal:root",
        )
        self.event_record = self.journal.event_at(self.scope, 1)
        self.key_id = "root-key-1"
        self.policy = {
            "schemaVersion": "1",
            "policyId": attestation_verify.POLICY_ID,
            "revision": "trust-r1",
            "openssl": {"path": str(self.openssl), "sha256": self.file_digest(self.openssl)},
            "keys": [{
                "keyId": self.key_id,
                "algorithm": "ed25519",
                "publicKeyPath": self.public_key.name,
                "publicKeySha256": self.file_digest(self.public_key),
                "principalId": "principal:root",
                "roles": ["governance-authority"],
                "validFrom": "2000-01-01T00:00:00Z",
                "validUntil": "2100-01-01T00:00:00Z",
                "revoked": False,
            }],
        }
        self.policy_path = self.root / "trust-policy.json"
        raw = json.dumps(self.policy, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.policy_path.write_bytes(raw)
        self.policy_digest = hashlib.sha256(raw).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def file_digest(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def test_receipt_statement_binds_event_and_chain_head(self):
        statement = build_journal_receipt_statement(self.event_record)
        predicate = statement["predicate"]
        self.assertEqual(statement["predicateType"], "urn:govcheck:attestation:journal-receipt:v1")
        self.assertEqual(predicate["receipt"]["eventDigest"], predicate["event"]["eventDigest"])
        self.assertEqual(predicate["journal"]["integrityStatus"], "valid")
        self.assertEqual(predicate["candidate"]["revision"], "c" * 40)

    def test_external_openssl_signing_self_verifies_and_exports_dsse(self):
        output = self.root / "receipt.dsse.json"
        envelope = sign_journal_receipt(
            database=self.db, scope_id=self.scope, position=1,
            private_key=self.private_key, key_id=self.key_id,
            openssl_path=self.openssl, openssl_sha256=self.file_digest(self.openssl),
            trust_policy_path=self.policy_path, trust_policy_sha256=self.policy_digest,
            repository_root=self.repo, output_path=output,
        )
        self.assertTrue(output.is_file())
        self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o644)
        result = attestation_verify.verify_dsse_envelope(
            envelope, self.policy_path, self.policy_digest, self.repo,
            required_role="governance-authority",
            expected_candidate_revision="c" * 40,
            expected_governance_revision="gov-17",
            expected_scope_id=self.scope,
            expected_base_revision="b" * 40,
            expected_content_sha256="a" * 64,
            expected_predicate_type="urn:govcheck:attestation:journal-receipt:v1",
        )
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["signers"][0]["principalId"], "principal:root")

    def test_refuses_key_or_output_inside_candidate_repository(self):
        key_inside = self.repo / "private.pem"
        key_inside.write_bytes(self.private_key.read_bytes())
        os.chmod(key_inside, 0o600)
        with self.assertRaises(JournalAttestationError):
            sign_journal_receipt(
                database=self.db, scope_id=self.scope, position=1,
                private_key=key_inside, key_id=self.key_id,
                openssl_path=self.openssl, openssl_sha256=self.file_digest(self.openssl),
                trust_policy_path=self.policy_path, trust_policy_sha256=self.policy_digest,
                repository_root=self.repo, output_path=self.root / "receipt.json",
            )
        with self.assertRaises(JournalAttestationError):
            sign_journal_receipt(
                database=self.db, scope_id=self.scope, position=1,
                private_key=self.private_key, key_id=self.key_id,
                openssl_path=self.openssl, openssl_sha256=self.file_digest(self.openssl),
                trust_policy_path=self.policy_path, trust_policy_sha256=self.policy_digest,
                repository_root=self.repo, output_path=self.repo / "receipt.json",
            )

    def test_tampered_event_is_rejected_before_signing(self):
        record = dict(self.event_record)
        event = dict(record["event"])
        event["payload"] = dict(event["payload"], decisionResult="fail")
        record["event"] = event
        with self.assertRaises((JournalAttestationError, attestation.AttestationError)):
            build_journal_receipt_statement(record)


if __name__ == "__main__":
    unittest.main()
