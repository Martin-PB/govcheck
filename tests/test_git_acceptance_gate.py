import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from govcheck import git_acceptance_gate as gate


class GitAcceptanceGateTests(unittest.TestCase):
    def args(self, git_dir):
        return SimpleNamespace(
            repository_id="repo:12345",
            vcs_kind="git",
            base="b" * 40,
            candidate="c" * 40,
            ref="refs/heads/main",
            git_dir=str(git_dir),
        )

    def environment(self, root):
        policy_bytes = json.dumps({"revision": "gov-policy-17"}, sort_keys=True, separators=(",", ":")).encode("utf-8")
        policy_digest = hashlib.sha256(policy_bytes).hexdigest()
        (root / "trust-policy.json").write_bytes(policy_bytes)
        values = {
            "GIT_DIR": str(root / "repo.git"),
            "GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:12345",
            "GOVCHECK_EXPECTED_POLICY_REVISION": "gov-policy-17",
            "GOVCHECK_EXPECTED_POLICY_DIGEST": "sha256:" + policy_digest,
            "GOVCHECK_EXPECTED_VERIFIER_IDENTITY": "govcheck-gate-v1",
            "GOVCHECK_EXPECTED_VERIFIER_DIGEST": "sha256:" + "b" * 64,
            "GOVCHECK_TRUST_POLICY_PATH": str(root / "trust-policy.json"),
            "GOVCHECK_TRUST_POLICY_SHA256": policy_digest,
            "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
            "GOVCHECK_SCOPE_ID": "repo:example/project",
            "GOVCHECK_ACCEPTANCE_DECISION_ENVELOPE": str(root / "decision.json"),
            "GOVCHECK_REVIEW_ENVELOPE_PATH": str(root / "review.json"),
            "GOVCHECK_ASSURANCE_ENVELOPE_PATH": str(root / "assurance.json"),
            "GOVCHECK_ASSURANCE_ROLE": "assurance-evaluator",
            "GOVCHECK_AUTHOR_IDENTITY_ENVELOPE_PATH": str(root / "author-identity.json"),
            "GOVCHECK_AUTHOR_IDENTITY_ROLE": "forge-authority",
            "GOVCHECK_AUTHOR_PRINCIPAL_SOURCE": "https://forge.example/api/author",
        }
        for name in ("decision.json", "review.json", "assurance.json", "author-identity.json"):
            (root / name).write_text("{}", encoding="utf-8")
        (root / "repo.git").mkdir()
        return values

    def test_missing_trusted_configuration_returns_unknown_protocol(self):
        args = self.args(Path("/tmp/repo.git"))
        code, result = gate.run_gate(args, env={"GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:12345"})
        self.assertEqual(code, 0)
        self.assertEqual(result["schema"], "govcheck.acceptance-decision/v0")
        self.assertEqual(result["result"], "unknown")
        self.assertIn("missing trusted gate configuration", result["reason"])

    def test_gate_rejects_policy_revision_or_digest_not_matching_pre_receive_pin(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            env = self.environment(root)
            env["GOVCHECK_EXPECTED_POLICY_DIGEST"] = "sha256:" + "0" * 64
            code, result = gate.run_gate(self.args(root / "repo.git"), env=env)
            self.assertEqual(code, 0)
            self.assertEqual(result["result"], "unknown")
            self.assertIn("policy digest", result["reason"])

    def test_gate_evaluates_exact_candidate_and_emits_pre_receive_v0(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            env = self.environment(root)
            args = self.args(root / "repo.git")

            def runner(command, **kwargs):
                if command[:2] == ["git", "clone"]:
                    Path(command[-1]).mkdir()
                return subprocess.CompletedProcess(command, 0, "", "")

            report = {"overall": "pass", "candidate": {}, "rules": []}
            decision = {
                "result": "pass",
                "decisionId": "decision-17",
                "authorityPrincipal": "principal:root",
                "policyDigest": "d" * 64,
                "riskAcceptance": None,
                "reason": "verified authority decision accepts the passing report",
            }
            with (
                patch.object(gate.check_module, "git_full_sha", side_effect=lambda tree, rev: rev),
                patch.object(gate.check_module, "candidate_content_digest", return_value="e" * 64),
                patch.object(gate.check_module, "git_changed", return_value={"src/main.py"}),
                patch.object(gate.check_module, "git_worktree_clean", return_value=True),
                patch.object(gate.check_module, "evaluate", return_value=report) as evaluator,
            ):
                code, result = gate.run_gate(args, env=env, runner=runner, decision_verifier=lambda *a, **k: decision)

            self.assertEqual(code, 0)
            self.assertEqual(result["result"], "pass")
            self.assertEqual(result["decision_id"], "decision-17")
            self.assertEqual(result["repository_id"], "repo:12345")
            self.assertEqual(result["base"], "b" * 40)
            self.assertEqual(result["candidate"], "c" * 40)
            self.assertEqual(result["ref"], "refs/heads/main")
            self.assertEqual(result["policy_revision"], "gov-policy-17")
            self.assertEqual(result["verifier"]["identity"], "govcheck-gate-v1")
            self.assertTrue(result["evidence_digest"].startswith("sha256:"))
            self.assertEqual(evaluator.call_args.args[1], {"src/main.py"})

    def test_accepted_with_risk_is_mapped_to_hook_schema(self):
        result = {
            "result": "accepted-with-risk",
            "decisionId": "risk-decision-1",
            "authorityPrincipal": "principal:root",
            "riskAcceptance": {
                "id": "risk-1",
                "reason": "bounded uncertainty",
                "scope": "repo:example/project",
                "expiresAt": "2026-12-01T00:00:00+00:00",
                "residualRisk": "independent review unavailable",
                "affectedClaims": ["claim:review"],
                "authorizationDigest": "f" * 64,
            },
        }
        mapped = gate._risk_v0(result)
        self.assertEqual(mapped["authority"], "principal:root")
        self.assertEqual(mapped["authorization_digest"], "sha256:" + "f" * 64)
        self.assertEqual(mapped["affected_claims"], ["claim:review"])


if __name__ == "__main__":
    unittest.main()
