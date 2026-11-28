import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit-github-ruleset.py"
SPEC = importlib.util.spec_from_file_location("github_ruleset_audit", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def sample_ruleset():
    return {
        "id": 28251664,
        "name": "Protection Main",
        "source": "Martin-PB/govcheck",
        "enforcement": "active",
        "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {"type": "pull_request", "parameters": {
                "required_approving_review_count": 0,
                "require_code_owner_review": False,
                "require_last_push_approval": False,
            }},
            {"type": "required_status_checks", "parameters": {
                "strict_required_status_checks_policy": False,
                "required_status_checks": [],
            }},
        ],
        "bypass_actors": [],
        "current_user_can_bypass": "never",
    }


class GitHubRulesetAuditTests(unittest.TestCase):
    def test_active_single_contributor_ruleset_is_reported_without_overclaim(self):
        report = AUDIT.audit_ruleset(sample_ruleset())
        self.assertEqual(report["finding_count"], 0)
        self.assertTrue(report["pull_request_required"])
        self.assertEqual(report["required_approving_review_count"], 0)
        self.assertEqual(report["required_status_checks"], [])
        self.assertEqual(report["required_check_liveness"], "not_applicable_no_required_status_checks")
        self.assertEqual(report["effective_govcheck_acceptance_gate"], "not-established")

    def test_bypass_actor_is_a_finding(self):
        document = sample_ruleset()
        document["bypass_actors"] = [{"actor_id": 123, "actor_type": "Team", "bypass_mode": "always"}]
        report = AUDIT.audit_ruleset(document)
        self.assertIn("bypass-actors-configured", {item["kind"] for item in report["findings"]})

    def test_required_check_without_liveness_mapping_is_not_pass(self):
        document = sample_ruleset()
        document["rules"][-1]["parameters"]["required_status_checks"] = [
            {"context": "govcheck-check", "app_id": None}
        ]
        report = AUDIT.audit_ruleset(document)
        self.assertEqual(report["required_check_liveness"], "unverified_requires_trusted_source_and_path_mapping")
        self.assertIn("required-check-liveness-unverified", {item["kind"] for item in report["findings"]})

    def test_approval_requirement_can_be_checked_against_solo_policy(self):
        document = sample_ruleset()
        document["rules"][2]["parameters"]["required_approving_review_count"] = 1
        report = AUDIT.audit_ruleset(document)
        self.assertIn("approval-count-mismatch", {item["kind"] for item in report["findings"]})

    def test_pull_request_rule_is_required(self):
        document = sample_ruleset()
        document["rules"] = [rule for rule in document["rules"] if rule["type"] != "pull_request"]
        report = AUDIT.audit_ruleset(document)
        self.assertIn("pull-request-not-required", {item["kind"] for item in report["findings"]})

    def test_fetch_uses_read_only_public_api_endpoint(self):
        captured = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(sample_ruleset()).encode("utf-8")

        def opener(request, timeout):
            captured["url"] = request.full_url
            captured["headers"] = request.headers
            captured["timeout"] = timeout
            return Response()

        result = AUDIT.fetch_ruleset("Martin-PB/govcheck", 28251664, opener=opener)
        self.assertEqual(result["id"], 28251664)
        self.assertEqual(captured["url"], "https://api.github.com/repos/Martin-PB/govcheck/rulesets/28251664")
        self.assertEqual(captured["timeout"], 20)
        self.assertEqual(captured["headers"]["User-agent"], "GovCheck-read-only-ruleset-audit")


if __name__ == "__main__":
    unittest.main()
