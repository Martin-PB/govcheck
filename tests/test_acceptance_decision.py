import hashlib
import json
import unittest
from unittest.mock import patch
from datetime import datetime, timezone

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

    def test_accept_requires_evaluation_pass(self):
        predicate = self.predicate()
        report = {"overall": "pass"}
        result = decision.evaluate_decision(predicate, report=report, report_bytes=self.report_bytes, **self.bindings)
        self.assertEqual(result["result"], "pass")
        report = {"overall": "unknown", "candidate": self.candidate, "rules": [{"id": "tests", "result": "pass"}]}
        unknown_bytes = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
        unknown_predicate = self.predicate(report_bytes=unknown_bytes)
        result = decision.evaluate_decision(unknown_predicate, report=report, report_bytes=unknown_bytes, **self.bindings)
        self.assertEqual(result["result"], "fail")
        self.assertIn("cannot override", result["reason"])

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

    def test_risk_acceptance_cannot_be_unscoped_or_missing(self):
        predicate = self.predicate(result="accept_with_risk", risk=None)
        with self.assertRaises(decision.AcceptanceDecisionError):
            decision.validate_predicate(predicate)
        risk = {
            "id": "risk-17", "reason": "reason", "scope": "other-scope",
            "expiresAt": "2026-12-01T00:00:00Z", "residualRisk": "residual",
            "affectedClaims": ["claim:x"], "authorizationDigest": "d" * 64,
        }
        unknown_report = {"overall": "unknown"}
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
