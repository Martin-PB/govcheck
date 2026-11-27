#!/usr/bin/env python3
"""Offline tests for the pinned Ed25519 DSSE verification provider."""
from __future__ import annotations

import base64
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from govcheck import attestation as att
from govcheck import attestation_verify as verify
from govcheck import independent_review as independent_review
from govcheck import forge_author_identity as forge_author_identity

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SPEC = importlib.util.spec_from_file_location("attestation_fixture", ROOT / "tests" / "test_attestation.py")
FIXTURE = importlib.util.module_from_spec(FIXTURE_SPEC)
FIXTURE_SPEC.loader.exec_module(FIXTURE)


@unittest.skipUnless(shutil.which("openssl"), "OpenSSL CLI is required for Ed25519 verification tests")
class DetachedVerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.candidate_root = self.root / "candidate"
        self.candidate_root.mkdir()
        self.private_key = self.root / "reviewer-private.pem"
        self.public_key = self.root / "reviewer-public.pem"
        self.openssl_path = Path(shutil.which("openssl")).resolve()
        subprocess.run(["openssl", "genpkey", "-algorithm", "ED25519", "-out", str(self.private_key)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["openssl", "pkey", "-in", str(self.private_key), "-pubout", "-out", str(self.public_key)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        report, context = FIXTURE.valid_inputs()
        self.statement = att.build_statement(report, context)
        self.policy = {
            "schemaVersion": "1",
            "policyId": verify.POLICY_ID,
            "revision": "trust-r1",
            "openssl": {"path": str(self.openssl_path), "sha256": self.file_digest(self.openssl_path)},
            "keys": [{
                "keyId": "review-key-1",
                "algorithm": "ed25519",
                "publicKeyPath": self.public_key.name,
                "publicKeySha256": self.file_digest(self.public_key),
                "principalId": "principal:synthetic-reviewer",
                "roles": ["independent-reviewer", "verifier", "forge-authority"],
                "validFrom": "2000-01-01T00:00:00Z",
                "validUntil": "2100-01-01T00:00:00Z",
                "revoked": False,
            }],
        }
        self.policy_path = self.root / "trust-policy.json"
        self.write_policy()
        self.envelope = self.sign_statement(self.statement)

    @staticmethod
    def file_digest(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def write_policy(self):
        raw = json.dumps(self.policy, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.policy_path.write_bytes(raw)
        self.policy_digest = hashlib.sha256(raw).hexdigest()

    def sign_statement(self, statement):
        payload = att.canonical_statement_bytes(statement)
        pae = att.dsse_pae(att.DSSE_PAYLOAD_TYPE, payload)
        message = self.root / "pae.bin"
        signature = self.root / "signature.bin"
        message.write_bytes(pae)
        subprocess.run(["openssl", "pkeyutl", "-sign", "-inkey", str(self.private_key),
                        "-rawin", "-in", str(message), "-out", str(signature)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return att.build_dsse_envelope(statement, [{
            "keyid": "review-key-1",
            "sig": base64.b64encode(signature.read_bytes()).decode("ascii"),
        }])

    def verify(self, **kwargs):
        options = {
            "required_role": "independent-reviewer",
            "expected_candidate_revision": "c" * 40,
            "expected_governance_revision": "gov-17",
            "expected_scope_id": "repo:example/project",
            "expected_base_revision": "e" * 40,
            "expected_content_sha256": "a" * 64,
            "now": datetime(2026, 11, 27, tzinfo=timezone.utc),
        }
        options.update(kwargs)
        return verify.verify_dsse_envelope(
            self.envelope, self.policy_path, self.policy_digest, self.candidate_root, **options
        )

    def test_valid_signature_and_trust_policy_are_verified(self):
        result = self.verify()
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["signers"][0]["principalId"], "principal:synthetic-reviewer")
        self.assertIn("independent-reviewer", result["signers"][0]["roles"])
        self.assertEqual(result["predicateType"], att.PREDICATE_TYPE)

    def test_detached_independent_review_predicate_verifies_exact_bindings(self):
        statement = independent_review.build_statement(
            repository_uri="https://github.com/example/project",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="e" * 40,
            governance_revision="gov-17",
            scope_id="repo:example/project",
            reviewed_on="2026-11-27T12:00:00Z",
            outcome="accepted",
            claims_reviewed=["claim:security"],
            observations=["Review scoped to the declared claims."],
            limitations=["No trusted timestamp was asserted."],
        )
        self.envelope = self.sign_statement(statement)
        result = self.verify(
            expected_predicate_type=independent_review.PREDICATE_TYPE,
            forbidden_principal="principal:candidate-author",
        )
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["predicateType"], independent_review.PREDICATE_TYPE)
        self.assertEqual(result["signers"][0]["principalId"], "principal:synthetic-reviewer")

    def test_independent_review_rejects_reviewer_equal_to_author(self):
        statement = independent_review.build_statement(
            repository_uri="https://github.com/example/project",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="e" * 40,
            governance_revision="gov-17",
            scope_id="repo:example/project",
            reviewed_on="2026-11-27T12:00:00Z",
            outcome="accepted",
            claims_reviewed=["claim:security"],
            observations=["Review scoped to the declared claims."],
            limitations=["No trusted timestamp was asserted."],
        )
        self.envelope = self.sign_statement(statement)
        result = self.verify(
            expected_predicate_type=independent_review.PREDICATE_TYPE,
            forbidden_principal="principal:synthetic-reviewer",
        )
        self.assertEqual(result["status"], "invalid")
        self.assertIn("not independent", result["reason"])

    def test_independent_review_wrong_binding_is_rejected(self):
        statement = independent_review.build_statement(
            repository_uri="https://github.com/example/project",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="e" * 40,
            governance_revision="gov-17",
            scope_id="repo:example/project",
            reviewed_on="2026-11-27T12:00:00Z",
            outcome="accepted",
            claims_reviewed=["claim:security"],
            observations=["Review scoped to the declared claims."],
            limitations=["No trusted timestamp was asserted."],
        )
        self.envelope = self.sign_statement(statement)
        result = self.verify(
            expected_predicate_type=independent_review.PREDICATE_TYPE,
            expected_candidate_revision="d" * 40,
        )
        self.assertEqual(result["status"], "invalid")
        self.assertIn("candidate revision", result["reason"])

    def test_signed_forge_author_identity_predicate_verifies(self):
        statement = forge_author_identity.build_statement(
            repository_uri="https://github.com/example/project",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="e" * 40,
            governance_revision="gov-17",
            scope_id="repo:example/project",
            author_principal="forge:author-123",
            source_uri="https://forge.example/api/commits/" + "c" * 40 + "/author",
            asserted_on="2026-11-27T12:00:00Z",
        )
        self.envelope = self.sign_statement(statement)
        result = self.verify(
            required_role="forge-authority",
            expected_predicate_type=forge_author_identity.PREDICATE_TYPE,
        )
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["predicateType"], forge_author_identity.PREDICATE_TYPE)
        self.assertEqual(result["statement"]["predicate"]["authorPrincipal"], "forge:author-123")

    def test_forge_author_identity_requires_authorized_provider_role(self):
        statement = forge_author_identity.build_statement(
            repository_uri="https://github.com/example/project",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="e" * 40,
            governance_revision="gov-17",
            scope_id="repo:example/project",
            author_principal="forge:author-123",
            source_uri="https://forge.example/api/commits/" + "c" * 40 + "/author",
            asserted_on="2026-11-27T12:00:00Z",
        )
        self.envelope = self.sign_statement(statement)
        result = self.verify(
            required_role="untrusted-role",
            expected_predicate_type=forge_author_identity.PREDICATE_TYPE,
        )
        self.assertEqual(result["status"], "unknown")

    def test_tampered_payload_fails_signature_verification(self):
        statement = copy.deepcopy(self.statement)
        statement["predicate"]["evaluation"]["result"] = "pass"
        self.envelope = self.sign_statement(self.statement)
        tampered_payload = att.canonical_statement_bytes(statement)
        self.envelope["payload"] = base64.b64encode(tampered_payload).decode("ascii")
        result = self.verify()
        self.assertEqual(result["status"], "invalid")
        self.assertIn("failed", result["reason"])

    def test_unknown_key_id_is_unknown_not_pass(self):
        self.envelope["signatures"][0]["keyid"] = "unregistered-key"
        self.assertEqual(self.verify()["status"], "unknown")

    def test_wrong_role_is_unknown_not_pass(self):
        self.assertEqual(self.verify(required_role="risk-authority")["status"], "unknown")

    def test_wrong_principal_is_unknown_not_pass(self):
        self.assertEqual(self.verify(required_principal="principal:someone-else")["status"], "unknown")

    def test_trust_policy_digest_mismatch_is_rejected(self):
        result = self.verify_dsse(expected_policy_sha256="0" * 64)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("digest", result["reason"])

    def verify_dsse(self, **kwargs):
        options = {
            "required_role": "independent-reviewer",
            "expected_candidate_revision": "c" * 40,
            "expected_governance_revision": "gov-17",
            "expected_scope_id": "repo:example/project",
            "expected_base_revision": "e" * 40,
            "expected_content_sha256": "a" * 64,
            "now": datetime(2026, 11, 27, tzinfo=timezone.utc),
        }
        expected_digest = kwargs.pop("expected_policy_sha256", self.policy_digest)
        options.update(kwargs)
        return verify.verify_dsse_envelope(self.envelope, self.policy_path, expected_digest,
                                            self.candidate_root, **options)

    def test_candidate_binding_mismatch_is_rejected(self):
        result = self.verify(expected_candidate_revision="f" * 40)
        self.assertEqual(result["status"], "invalid")

    def test_expired_key_is_rejected(self):
        self.policy["keys"][0]["validUntil"] = "2020-01-01T00:00:00Z"
        self.write_policy()
        result = self.verify()
        self.assertEqual(result["status"], "invalid")
        self.assertIn("expired", result["reason"])

    def test_revoked_key_is_rejected(self):
        self.policy["keys"][0]["revoked"] = True
        self.write_policy()
        result = self.verify()
        self.assertEqual(result["status"], "invalid")
        self.assertIn("revoked", result["reason"])

    def test_public_key_digest_mismatch_is_rejected(self):
        self.public_key.write_bytes(self.public_key.read_bytes() + b"tamper")
        result = self.verify()
        self.assertEqual(result["status"], "invalid")
        self.assertIn("public key digest mismatch", result["reason"])

    def test_openssl_binary_digest_mismatch_is_rejected(self):
        self.policy["openssl"]["sha256"] = "0" * 64
        self.write_policy()
        result = self.verify()
        self.assertEqual(result["status"], "invalid")
        self.assertIn("OpenSSL executable digest mismatch", result["reason"])

    def test_policy_inside_candidate_tree_is_rejected(self):
        candidate_policy = self.candidate_root / "trust-policy.json"
        candidate_policy.write_bytes(self.policy_path.read_bytes())
        result = verify.verify_dsse_envelope(self.envelope, candidate_policy, self.policy_digest,
                                             self.candidate_root)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("outside", result["reason"])

    def test_candidate_local_symlink_to_external_policy_is_rejected(self):
        link = self.candidate_root / "policy-link.json"
        link.symlink_to(self.policy_path)
        result = verify.verify_dsse_envelope(self.envelope, link, self.policy_digest, self.candidate_root)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("outside", result["reason"])

    def test_naive_verification_time_is_rejected(self):
        result = self.verify(now=datetime(2026, 11, 27))
        self.assertEqual(result["status"], "invalid")
        self.assertIn("timezone", result["reason"])

    def test_public_key_inside_candidate_tree_is_rejected(self):
        candidate_key = self.candidate_root / "reviewer-public.pem"
        candidate_key.write_bytes(self.public_key.read_bytes())
        self.policy["keys"][0]["publicKeyPath"] = str(candidate_key)
        self.write_policy()
        result = self.verify()
        self.assertEqual(result["status"], "invalid")
        self.assertIn("outside", result["reason"])

    def test_package_trust_policy_schema_is_present(self):
        schema_path = ROOT / "govcheck" / "formal" / "schemas" / "attestation-trust-policy-v1.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertIn("openssl", schema["required"])
        self.assertIn("keys", schema["required"])
        self.assertEqual(schema["properties"]["policyId"]["const"], verify.POLICY_ID)

    def test_cli_verifies_a_detached_envelope(self):
        envelope_path = self.root / "envelope.json"
        envelope_path.write_text(json.dumps(self.envelope), encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = verify._main([
                "verify", "--envelope", str(envelope_path),
                "--trust-policy", str(self.policy_path),
                "--trust-policy-sha256", self.policy_digest,
                "--candidate-root", str(self.candidate_root),
                "--required-role", "independent-reviewer",
                "--candidate-revision", "c" * 40,
                "--governance-revision", "gov-17",
                "--scope-id", "repo:example/project",
                "--base-revision", "e" * 40,
                "--content-sha256", "a" * 64,
            ])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "verified")


if __name__ == "__main__":
    unittest.main()
