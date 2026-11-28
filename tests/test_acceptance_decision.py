import hashlib
import shutil
import subprocess
import tempfile
import json
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from pathlib import Path

from govcheck import acceptance_decision as decision
from govcheck import attestation


class AcceptanceDecisionTests(unittest.TestCase):
    def setUp(self):
        self.candidate = {
            "candidate_rev": "c" * 40,
            "base_revision": "b" * 40,
            "content_sha256": "a" * 64,
            "ref": "refs/heads/main",
            "governance_revision": "gov-17",
            "scope_id": "repo:example/project",
        }
        self.report = {"overall": "pass", "candidate": self.candidate, "rules": [{"id": "tests", "result": "pass"}]}
        self.report_bytes = json.dumps(self.report, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.bindings = dict(
            expected_repository_id="repo:12345",
            expected_candidate_revision="c" * 40,
            expected_candidate_content_sha256="a" * 64,
            expected_base_revision="b" * 40,
            expected_ref="refs/heads/main",
            expected_governance_revision="gov-17",
            expected_scope_id="repo:example/project",
        )

    def predicate(self, result="accept", risk=None, report_bytes=None):
        return {
            "schemaVersion": "1",
            "decisionId": "decision-17",
            "repositoryId": "repo:12345",
            "candidateRevision": "c" * 40,
            "candidateContentSha256": "a" * 64,
            "baseRevision": "b" * 40,
            "ref": "refs/heads/main",
            "governanceRevision": "gov-17",
            "scopeId": "repo:example/project",
            "evaluationDigest": decision.evaluation_report_digest(report_bytes if report_bytes is not None else self.report_bytes),
            "result": result,
            "decidedOn": "2026-11-27T12:00:00Z",
            "rationale": "Decision under the current authority regime.",
            "riskAcceptance": risk,
        }

    def test_builds_statement_and_binds_report_digest(self):
        statement = decision.build_statement(
            repository_uri="https://github.com/example/project",
            decision_id="decision-17",
            repository_id="repo:12345",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="b" * 40,
            ref="refs/heads/main",
            governance_revision="gov-17",
            scope_id="repo:example/project",
            evaluation_digest=decision.evaluation_report_digest(self.report_bytes),
            result="accept",
            decided_on="2026-11-27T12:00:00Z",
            rationale="Decision under the current authority regime.",
        )
        self.assertEqual(statement["predicateType"], decision.PREDICATE_TYPE)
        self.assertEqual(statement["subject"][0]["digest"]["sha256"], "a" * 64)
        attestation.validate_statement(statement)

    @unittest.skipUnless(shutil.which("openssl"), "OpenSSL is required for decision signing test")
    def test_sign_decision_from_exact_report_and_verify_authority(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            private_key = root / "authority-private.pem"
            public_key = root / "authority-public.pem"
            openssl = Path(shutil.which("openssl")).resolve()
            subprocess.run([str(openssl), "genpkey", "-algorithm", "ED25519", "-out", str(private_key)], check=True, capture_output=True)
            subprocess.run([str(openssl), "pkey", "-in", str(private_key), "-pubout", "-out", str(public_key)], check=True, capture_output=True)

            def digest(path):
                return hashlib.sha256(Path(path).read_bytes()).hexdigest()

            now = datetime.now(timezone.utc)
            report = {
                "overall": "unknown",
                "candidate": {
                    "candidate_rev": "c" * 40,
                    "base_revision": "b" * 40,
                    "content_sha256": "a" * 64,
                    "ref": "refs/heads/main",
                    "governance_revision": "gov-17",
                    "scope_id": "repo:example/project",
                    "tree": "d" * 40,
                },
                "rules": [{"id": "independent-review", "result": "unknown"}],
            }
            report_bytes = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
            risk = {
                "id": "risk-signing-test",
                "reason": "review evidence unavailable",
                "scope": "repo:example/project",
                "expiresAt": (now + timedelta(days=14)).isoformat(),
                "residualRisk": "review remains unknown",
                "affectedClaims": ["claim:review"],
                "authorizationDigest": hashlib.sha256(b"risk authorization").hexdigest(),
            }
            envelope = decision.sign_decision_from_report(
                report_bytes,
                repository_uri="https://example.invalid/repo",
                repository_id="repo:12345",
                decision_id="decision-sign-test",
                result="accept_with_risk",
                rationale="bounded authority acceptance",
                private_key_path=private_key,
                key_id="authority-key",
                openssl_path=str(openssl),
                risk_acceptance=risk,
                decided_on=now.isoformat(),
            )

            policy = {
                "schemaVersion": "1",
                "policyId": "govcheck.attestation-trust-policy/v1",
                "revision": "policy-sign-test",
                "openssl": {"path": str(openssl), "sha256": digest(openssl)},
                "keys": [{
                    "keyId": "authority-key",
                    "algorithm": "ed25519",
                    "publicKeyPath": public_key.name,
                    "publicKeySha256": digest(public_key),
                    "principalId": "principal:root-authority",
                    "roles": ["governance-authority"],
                    "validFrom": "2000-01-01T00:00:00Z",
                    "validUntil": "2100-01-01T00:00:00Z",
                    "revoked": False,
                }],
            }
            policy_path = root / "trust-policy.json"
            policy_bytes = json.dumps(policy, sort_keys=True, separators=(",", ":")).encode("utf-8")
            policy_path.write_bytes(policy_bytes)
            candidate_root = root / "candidate"
            candidate_root.mkdir()

            result = decision.verify_and_evaluate(
                envelope,
                policy_path,
                hashlib.sha256(policy_bytes).hexdigest(),
                candidate_root,
                report=report,
                report_bytes=report_bytes,
                expected_repository_id="repo:12345",
                expected_candidate_revision="c" * 40,
                expected_candidate_content_sha256="a" * 64,
                expected_base_revision="b" * 40,
                expected_ref="refs/heads/main",
                expected_governance_revision="gov-17",
                expected_scope_id="repo:example/project",
                required_role="governance-authority",
                now=now,
            )
            self.assertEqual(result["result"], "accepted-with-risk")
            self.assertEqual(result["authorityPrincipal"], "principal:root-authority")
            self.assertEqual(result["decisionId"], "decision-sign-test")
            self.assertEqual(result["decidedOn"], now.isoformat())

    def test_accept_requires_evaluation_pass(self):
        predicate = self.predicate()
        report = {"overall": "pass"}
        result = decision.evaluate_decision(predicate, report=self.report, report_bytes=self.report_bytes, **self.bindings)
        self.assertEqual(result["result"], "pass")
        report = {"overall": "unknown", "candidate": self.candidate, "rules": [{"id": "tests", "result": "pass"}]}
        unknown_bytes = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
        unknown_predicate = self.predicate(report_bytes=unknown_bytes)
        result = decision.evaluate_decision(unknown_predicate, report=report, report_bytes=unknown_bytes, **self.bindings)
        self.assertEqual(result["result"], "fail")
        self.assertIn("cannot override", result["reason"])

    def test_decision_cannot_accept_report_for_another_candidate(self):
        report = dict(self.report)
        candidate = dict(self.candidate)
        candidate["candidate_rev"] = "d" * 40
        report["candidate"] = candidate
        report_bytes = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
        predicate = self.predicate(report_bytes=report_bytes)
        result = decision.evaluate_decision(predicate, report=report, report_bytes=report_bytes, **self.bindings)
        self.assertEqual(result["result"], "fail")
        self.assertIn("candidate_rev", result["reason"])

    def test_report_digest_mismatch_fails(self):
        predicate = self.predicate()
        different_bytes = json.dumps(self.report, indent=2).encode("utf-8")
        result = decision.evaluate_decision(predicate, report=self.report, report_bytes=different_bytes, **self.bindings)
        self.assertEqual(result["result"], "fail")
        self.assertIn("evaluationDigest", result["reason"])

    def test_reject_decision_fails_closed(self):
        predicate = self.predicate(result="reject")
        result = decision.evaluate_decision(predicate, report=self.report, report_bytes=self.report_bytes, **self.bindings)
        self.assertEqual(result["result"], "fail")
        self.assertIn("rejected", result["reason"])

    def test_accept_with_risk_requires_complete_current_scoped_record(self):
        risk = {
            "id": "risk-17",
            "reason": "A bounded unresolved verification gap.",
            "scope": "repo:example/project",
            "expiresAt": "2026-12-01T00:00:00Z",
            "residualRisk": "Independent review remains unavailable.",
            "affectedClaims": ["claim:independent-review"],
            "authorizationDigest": "d" * 64,
        }
        unknown_report = {"overall": "unknown", "candidate": self.candidate}
        unknown_bytes = json.dumps(unknown_report, sort_keys=True, separators=(",", ":")).encode("utf-8")
        predicate = self.predicate(result="accept_with_risk", risk=risk, report_bytes=unknown_bytes)
        result = decision.evaluate_decision(
            predicate, report=unknown_report, report_bytes=unknown_bytes,
            now=datetime(2026, 11, 27, tzinfo=timezone.utc), **self.bindings,
        )
        self.assertEqual(result["result"], "accepted-with-risk")
        result = decision.evaluate_decision(
            predicate, report=unknown_report, report_bytes=unknown_bytes,
            now=datetime(2026, 12, 2, tzinfo=timezone.utc), **self.bindings,
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("expired", result["reason"])

    def test_verify_and_evaluate_requires_authenticated_authority_role(self):
        predicate = self.predicate()
        verified = {
            "status": "verified",
            "statement": {"predicate": predicate},
            "signers": [{"principalId": "principal:root-authority"}],
            "policyDigest": "e" * 64,
        }
        with patch("govcheck.attestation_verify.verify_dsse_envelope", return_value=verified) as verifier:
            result = decision.verify_and_evaluate(
                {},
                "trust-policy.json",
                "f" * 64,
                ".",
                report=self.report,
                report_bytes=self.report_bytes,
                required_role="governance-authority",
                **self.bindings,
            )
        self.assertEqual(result["result"], "pass")
        self.assertEqual(result["authorityPrincipal"], "principal:root-authority")
        self.assertEqual(verifier.call_args.kwargs["required_role"], "governance-authority")
        self.assertEqual(verifier.call_args.kwargs["expected_predicate_type"], decision.PREDICATE_TYPE)

    def test_only_governance_authority_role_can_verify_decision(self):
        result = decision.verify_and_evaluate(
            {},
            "trust-policy.json",
            "f" * 64,
            ".",
            report=self.report,
            report_bytes=self.report_bytes,
            required_role="independent-reviewer",
            **self.bindings,
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("governance-authority", result["reason"])

    def test_risk_acceptance_cannot_be_unscoped_or_missing(self):
        predicate = self.predicate(result="accept_with_risk", risk=None)
        with self.assertRaises(decision.AcceptanceDecisionError):
            decision.validate_predicate(predicate)
        risk = {
            "id": "risk-17", "reason": "reason", "scope": "other-scope",
            "expiresAt": "2026-12-01T00:00:00Z", "residualRisk": "residual",
            "affectedClaims": ["claim:x"], "authorizationDigest": "d" * 64,
        }
        unknown_report = {"overall": "unknown", "candidate": self.candidate, "rules": [{"id": "tests", "result": "pass"}]}
        unknown_bytes = json.dumps(unknown_report, sort_keys=True, separators=(",", ":")).encode("utf-8")
        predicate = self.predicate(result="accept_with_risk", risk=risk, report_bytes=unknown_bytes)
        result = decision.evaluate_decision(
            predicate, report=unknown_report, report_bytes=unknown_bytes,
            now=datetime(2026, 11, 27, tzinfo=timezone.utc), **self.bindings,
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("scope", result["reason"])


if __name__ == "__main__":
    unittest.main()
