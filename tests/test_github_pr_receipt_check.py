import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "github-pr-receipt-check.py"
SPEC = importlib.util.spec_from_file_location("github_pr_receipt_check", SCRIPT)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class GitHubPrReceiptCheckTests(unittest.TestCase):
    def setUp(self):
        self.head = "c" * 40
        self.base = "b" * 40
        self.content_digest = "a" * 64
        self.scope = "repo:example/project"
        self.repo_uri = "https://github.com/Martin-PB/govcheck"
        self.governance_digest = "sha256:" + "d" * 64
        self.policy_digest = "sha256:" + "e" * 64
        target_ref = "refs/heads/feature"
        provenance = {
            "repository": {"id": "repo:12345", "uri": self.repo_uri},
            "vcs": {"kind": "git"},
            "target": {"kind": "ref", "name": target_ref},
            "base": {"nativeRevision": self.base, "contentDigest": "sha256:" + "b" * 64},
            "candidate": {"nativeRevision": self.head, "contentDigest": "sha256:" + self.content_digest},
            "governance": {"scopeId": self.scope, "revision": "gov-17", "digest": self.governance_digest},
        }
        payload = {
            "repositoryId": "repo:12345",
            "candidateRevision": self.head,
            "baseRevision": self.base,
            "ref": target_ref,
            "governanceRevision": "gov-17",
            "policyDigest": self.policy_digest,
            "decisionResult": "pass",
            "verification": "authenticated-authority",
            "authorityPrincipal": "principal:root",
            "riskAcceptance": None,
            "vcsProvenance": provenance,
        }
        self.statement = {
            "predicateType": CHECK.PREDICATE_TYPE,
            "predicate": {
                "repository": {"uri": self.repo_uri, "vcsKind": "git"},
                "candidate": {"revision": self.head, "contentDigest": {"sha256": self.content_digest}},
                "base": {"revision": self.base, "reference": target_ref},
                "governance": {"scopeId": self.scope, "revision": "gov-17", "digest": {"sha256": self.governance_digest.removeprefix("sha256:")}},
                "event": {"eventType": "govcheck.acceptance.gate-result/v1", "payload": payload},
                "receipt": {"scopeId": self.scope},
            },
        }
        self.pr = {
            "state": "open",
            "head": {"sha": self.head, "ref": "feature", "repo": {"full_name": "Martin-PB/govcheck"}},
            "base": {"sha": self.base, "ref": "main", "repo": {"full_name": "Martin-PB/govcheck"}},
        }
        self.config = {
            "GITHUB_REPOSITORY": "Martin-PB/govcheck",
            "GOVCHECK_PROTECTED_BASE_REF": "main",
            "GOVCHECK_REPOSITORY_URI": self.repo_uri,
            "GOVCHECK_JOURNAL_SCOPE_ID": self.scope,
            "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
            "GOVCHECK_GOVERNANCE_DIGEST": self.governance_digest,
            "GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:12345",
            "GOVCHECK_EXPECTED_POLICY_DIGEST": self.policy_digest,
        }

    def test_exact_head_base_ref_content_and_authority_bindings_pass(self):
        result = CHECK.validate_pr_bindings(self.statement, self.pr, self.content_digest, self.config)
        self.assertEqual(result["headSha"], self.head)
        self.assertEqual(result["baseSha"], self.base)
        self.assertEqual(result["principal"], "principal:root")

    def test_stale_candidate_or_base_is_rejected(self):
        statement = json.loads(json.dumps(self.statement))
        statement["predicate"]["candidate"]["revision"] = "f" * 40
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(statement, self.pr, self.content_digest, self.config)
        statement = json.loads(json.dumps(self.statement))
        statement["predicate"]["base"]["revision"] = "f" * 40
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(statement, self.pr, self.content_digest, self.config)

    def test_content_digest_or_target_ref_mismatch_is_rejected(self):
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(self.statement, self.pr, "f" * 64, self.config)
        statement = json.loads(json.dumps(self.statement))
        statement["predicate"]["base"]["reference"] = "refs/heads/main"
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(statement, self.pr, self.content_digest, self.config)

    def test_only_authenticated_pass_without_risk_acceptance_is_allowed(self):
        statement = json.loads(json.dumps(self.statement))
        statement["predicate"]["event"]["payload"]["decisionResult"] = "accepted-with-risk"
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(statement, self.pr, self.content_digest, self.config)
        statement = json.loads(json.dumps(self.statement))
        statement["predicate"]["event"]["payload"]["verification"] = "unverified-gate-attempt"
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(statement, self.pr, self.content_digest, self.config)

    def test_fork_and_wrong_repository_or_governance_pins_are_rejected(self):
        pr = json.loads(json.dumps(self.pr))
        pr["head"]["repo"]["full_name"] = "contributor/fork"
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(self.statement, pr, self.content_digest, self.config)
        config = dict(self.config, GOVCHECK_GOVERNANCE_REVISION="gov-18")
        with self.assertRaises(CHECK.CheckError):
            CHECK.validate_pr_bindings(self.statement, self.pr, self.content_digest, config)

    def test_comment_requires_command_and_strict_single_json_envelope(self):
        envelope = {"payloadType": "application/vnd.in-toto+json", "payload": "e30=", "signatures": [{"keyid": "k", "sig": "YQ=="}]}
        body = "/govcheck-receipt\n\n```json\n" + json.dumps(envelope) + "\n```"
        self.assertEqual(CHECK.extract_envelope_comment(body), envelope)
        with self.assertRaises(CHECK.CheckError):
            CHECK.extract_envelope_comment("```json\n{}\n```")
        duplicate = '/govcheck-receipt\n```json\n{"x":1,"x":2}\n```'
        with self.assertRaises(CHECK.CheckError):
            CHECK.extract_envelope_comment(duplicate)


if __name__ == "__main__":
    unittest.main()
