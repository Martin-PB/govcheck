import importlib.util
import json
import unittest
from unittest.mock import patch
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

    def test_disabled_opt_in_neutralizes_existing_pending_check(self):
        event = {"pull_request": {"number": 7, "head": {"sha": self.head}, "base": {"sha": self.base}}}
        external_id = "govcheck-pr-7-base-" + self.base
        with patch.object(CHECK, "github_api", return_value={"check_runs": [{"id": 99, "external_id": external_id, "status": "in_progress"}]}), patch.object(CHECK, "complete_check_run") as complete:
            self.assertEqual(CHECK.disable_pr_event(event, "token", "Martin-PB/govcheck"), 0)
        complete.assert_called_once()
        self.assertEqual(complete.call_args.args[2:4], (99, "neutral"))

    def test_comment_requires_command_and_strict_single_json_envelope(self):
        envelope = {"payloadType": "application/vnd.in-toto+json", "payload": "e30=", "signatures": [{"keyid": "k", "sig": "YQ=="}]}
        body = "/govcheck-receipt\n\n```json\n" + json.dumps(envelope) + "\n```"
        self.assertEqual(CHECK.extract_envelope_comment(body), envelope)
        with self.assertRaises(CHECK.CheckError):
            CHECK.extract_envelope_comment("```json\n{}\n```")
        duplicate = '/govcheck-receipt\n```json\n{"x":1,"x":2}\n```'
        with self.assertRaises(CHECK.CheckError):
            CHECK.extract_envelope_comment(duplicate)


    def test_completed_success_is_not_reused_for_a_new_receipt_attempt(self):
        completed = {
            "id": 41,
            "external_id": "govcheck-pr-7-base-" + self.base,
            "status": "completed",
            "conclusion": "success",
        }
        created = {"id": 42}
        with patch.object(CHECK, "github_api", side_effect=[{"check_runs": [completed]}, created]) as api:
            result = CHECK.ensure_check_run(
                "token", "Martin-PB/govcheck", self.head, self.base, 7,
                "https://github.com/Martin-PB/govcheck/actions/runs/1",
            )
        self.assertEqual(result, 42)
        self.assertEqual(api.call_count, 2)
        self.assertEqual(api.call_args_list[1].args[2:4], ("POST", "/check-runs"))
        payload = api.call_args_list[1].args[4]
        self.assertEqual(payload["head_sha"], self.head)
        self.assertEqual(payload["external_id"], "govcheck-pr-7-base-" + self.base)
        self.assertEqual(payload["status"], "in_progress")

    def test_pending_check_is_reused_only_for_the_exact_pr_base(self):
        matching = {
            "id": 51,
            "external_id": "govcheck-pr-7-base-" + self.base,
            "status": "in_progress",
        }
        with patch.object(CHECK, "github_api", return_value={"check_runs": [matching]}) as api:
            result = CHECK.ensure_check_run(
                "token", "Martin-PB/govcheck", self.head, self.base, 7, "https://example.invalid"
            )
        self.assertEqual(result, 51)
        api.assert_called_once()
        self.assertEqual(api.call_args.args[2:4], (
            "GET",
            "/commits/" + self.head + "/check-runs?check_name=" +
            CHECK.urllib.parse.quote(CHECK.CHECK_NAME) + "&filter=latest&per_page=100",
        ))

    def test_pr_lifecycle_creates_pending_check_bound_to_head_and_base(self):
        event = {"pull_request": {
            "number": 7,
            "head": {"sha": self.head},
            "base": {"sha": self.base},
        }}
        with patch.object(CHECK, "ensure_check_run", return_value=73) as ensure:
            result = CHECK.invalidate_pr_event(
                event, "token", "Martin-PB/govcheck", "https://example.invalid"
            )
        self.assertEqual(result, 0)
        ensure.assert_called_once_with(
            "token", "Martin-PB/govcheck", self.head, self.base, 7, "https://example.invalid"
        )


if __name__ == "__main__":
    unittest.main()
