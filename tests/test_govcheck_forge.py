#!/usr/bin/env python3
"""Offline tests for the forge-native adapter (govcheck/forge.py, Architecture 0034)."""
from __future__ import annotations

import importlib.util
import io
import json
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("govcheck_forge", ROOT / "govcheck" / "forge.py")
forge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(forge)


class FakeResponse:
    def __init__(self, status, payload, headers=None):
        self.status = status
        self._body = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        self.headers = headers or {}

    def read(self):
        return self._body


class FakeOpener:
    def __init__(self, handler):
        self.handler = handler
        self.requests = []

    def __call__(self, req):
        self.requests.append(req)
        return self.handler(req)


def http_error(code, payload=None):
    body = json.dumps(payload or {"message": "boom"}).encode("utf-8")
    return urllib.error.HTTPError("https://api.github.com/x", code, "error", {}, io.BytesIO(body))


def make_client(handler, token="tok-secret-123"):
    opener = FakeOpener(handler)
    client = forge.GitHubClient("octo", "repo", token=token, opener=opener)
    return client, opener


class CapabilityTests(unittest.TestCase):
    def test_declaration_lists_read_write_verify(self):
        caps = forge.declare_capabilities()
        self.assertEqual(caps["forges"], ["github"])
        self.assertIn("list_check_runs", caps["verify"])
        self.assertIn("create_issue", caps["write"])
        self.assertIn("list_issues", caps["read"])

    def test_unsupported_forge(self):
        with self.assertRaises(forge.ForgeError) as cm:
            forge.make_client(forge="gitlab", owner="o", repo="r", env={})
        self.assertEqual(cm.exception.kind, "unsupported")

    def test_missing_owner_repo(self):
        with self.assertRaises(forge.ForgeError) as cm:
            forge.make_client(forge="github", owner=None, repo=None, env={})
        self.assertEqual(cm.exception.kind, "malformed")


class TokenTests(unittest.TestCase):
    def test_precedence_govcheck_over_github(self):
        env = {"GITHUB_TOKEN": "g", "GOVCHECK_FORGE_TOKEN": "v"}
        self.assertEqual(forge.resolve_token(env), "v")

    def test_fallback_github_token(self):
        self.assertEqual(forge.resolve_token({"GITHUB_TOKEN": "g"}), "g")

    def test_none_when_absent_or_blank(self):
        self.assertIsNone(forge.resolve_token({}))
        self.assertIsNone(forge.resolve_token({"GOVCHECK_FORGE_TOKEN": "  "}))


class ReadTests(unittest.TestCase):
    def test_list_issues_paginates_and_filters_pull_requests(self):
        page1 = [
            {"number": 1, "title": "a", "state": "open", "body": "Registry ID: govcheck.work.alpha\n\nhi", "labels": [{"name": "b"}, {"name": "a"}], "html_url": "u1"},
            {"number": 2, "title": "pr", "state": "open", "body": "", "labels": [], "pull_request": {}},
        ]
        page2 = [{"number": 3, "title": "c", "state": "open", "body": "", "labels": [], "html_url": "u3"}]
        def handler(req):
            if "page=2" in req.full_url:
                return FakeResponse(200, page2)
            link = '<https://api.github.com/repos/octo/repo/issues?state=open&per_page=100&page=2>; rel="next"'
            return FakeResponse(200, page1, {"Link": link})
        client, opener = make_client(handler)
        issues = forge.list_issues(client)
        self.assertEqual(len(opener.requests), 2)
        self.assertEqual([i["number"] for i in issues], [1, 3])
        self.assertEqual(issues[0]["labels"], ["a", "b"])
        self.assertEqual(issues[0]["registry_id"], "govcheck.work.alpha")

    def test_get_issue_not_found(self):
        def handler(req):
            raise http_error(404, {"message": "Not Found"})
        client, _ = make_client(handler)
        with self.assertRaises(forge.ForgeError) as cm:
            forge.get_issue(client, 99)
        self.assertEqual(cm.exception.kind, "not-found")

    def test_auth_error_is_expurgated(self):
        def handler(req):
            raise http_error(401, {"message": "Bad credentials"})
        client, _ = make_client(handler, token="tok-secret-123")
        with self.assertRaises(forge.ForgeError) as cm:
            forge.list_labels(client)
        self.assertEqual(cm.exception.kind, "auth")
        self.assertNotIn("tok-secret-123", str(cm.exception))

    def test_unavailable_on_503(self):
        def handler(req):
            raise http_error(503, {"message": "down"})
        client, _ = make_client(handler)
        with self.assertRaises(forge.ForgeError) as cm:
            forge.list_labels(client)
        self.assertEqual(cm.exception.kind, "unavailable")

    def test_conflict_on_422_and_stale_on_409(self):
        def h422(req):
            raise http_error(422, {"message": "Validation Failed"})
        def h409(req):
            raise http_error(409, {"message": "conflict"})
        c1, _ = make_client(h422, token="t")
        with self.assertRaises(forge.ForgeError) as cm:
            forge.create_issue(c1, "t", "b")
        self.assertEqual(cm.exception.kind, "conflict")
        c2, _ = make_client(h409, token="t")
        with self.assertRaises(forge.ForgeError) as cm:
            forge.update_issue(c2, 1, title="x")
        self.assertEqual(cm.exception.kind, "stale")

    def test_malformed_on_invalid_json(self):
        def handler(req):
            return FakeResponse(200, b"{not json")
        client, _ = make_client(handler)
        with self.assertRaises(forge.ForgeError) as cm:
            forge.get_issue(client, 1)
        self.assertEqual(cm.exception.kind, "malformed")


class WriteTests(unittest.TestCase):
    def test_writes_require_token_and_send_no_request_without_it(self):
        opener = FakeOpener(lambda req: FakeResponse(200, []))
        client = forge.GitHubClient("octo", "repo", token=None, opener=opener)
        calls = [lambda: forge.create_issue(client, "t"), lambda: forge.update_issue(client, 1, title="x"), lambda: forge.add_comment(client, 1, "b")]
        for fn in calls:
            with self.assertRaises(forge.ForgeError) as cm:
                fn()
            self.assertEqual(cm.exception.kind, "auth")
        self.assertEqual(len(opener.requests), 0)

    def test_create_issue_posts_registry_id_and_returns_record(self):
        captured = {}
        def handler(req):
            captured["method"] = req.get_method()
            captured["url"] = req.full_url
            captured["body"] = json.loads(req.data.decode("utf-8"))
            captured["auth"] = req.headers.get("Authorization")
            return FakeResponse(201, {"number": 7, "title": "T", "state": "open", "body": captured["body"]["body"], "labels": [{"name": "x"}], "html_url": "u7"})
        client, opener = make_client(handler, token="tok-secret-123")
        rec = forge.create_issue(client, "T", "hello", labels=["x"], registry_id="govcheck.work.beta")
        self.assertEqual(captured["method"], "POST")
        self.assertTrue(captured["url"].endswith("/repos/octo/repo/issues"))
        self.assertEqual(captured["auth"], "Bearer tok-secret-123")
        self.assertIn("Registry ID: govcheck.work.beta", captured["body"]["body"])
        self.assertEqual(rec["number"], 7)
        self.assertEqual(rec["registry_id"], "govcheck.work.beta")

    def test_update_issue_without_fields_is_malformed(self):
        client, _ = make_client(lambda req: FakeResponse(200, {}), token="t")
        with self.assertRaises(forge.ForgeError) as cm:
            forge.update_issue(client, 1)
        self.assertEqual(cm.exception.kind, "malformed")


class RoundTripTests(unittest.TestCase):
    def test_registry_id_round_trip_is_lossless(self):
        body = forge.issue_body("govcheck.work.gamma", "original body")
        self.assertTrue(body.startswith("Registry ID: govcheck.work.gamma"))
        rec = forge.issue_record({"number": 1, "title": "t", "state": "open", "labels": [{"name": "z"}, {"name": "a"}], "body": body, "html_url": "u"})
        self.assertEqual(rec["registry_id"], "govcheck.work.gamma")
        self.assertEqual(rec["labels"], ["a", "z"])
        again = forge.issue_body(rec["registry_id"], "original body")
        self.assertEqual(again, body)
        self.assertEqual(forge.registry_id_from_text(rec["body"]), "govcheck.work.gamma")
        self.assertIsNone(forge.registry_id_from_text("no id here"))


class VerifyTests(unittest.TestCase):
    def test_list_check_runs_maps_fields(self):
        def handler(req):
            return FakeResponse(200, {"check_runs": [
                {"name": "ci", "status": "completed", "conclusion": "success", "html_url": "u"},
                {"name": "lint", "status": "in_progress", "conclusion": None, "html_url": "v"},
            ]})
        client, _ = make_client(handler)
        runs = forge.list_check_runs(client, "abc123")
        self.assertEqual([r["name"] for r in runs], ["ci", "lint"])
        self.assertEqual(runs[0]["conclusion"], "success")

    def test_branch_protection_reports_required_checks(self):
        def handler(req):
            return FakeResponse(200, {
                "required_status_checks": {"contexts": ["lint", "ci"]},
                "enforce_admins": {"enabled": True},
                "required_pull_request_reviews": {"required_approving_review_count": 1},
            })
        client, _ = make_client(handler)
        prot = forge.get_branch_protection(client, "main")
        self.assertEqual(prot["required_checks"], ["ci", "lint"])
        self.assertTrue(prot["enforce_admins"])
        self.assertEqual(prot["required_approving_reviews"], 1)

    def test_branch_protection_rejects_missing_or_malformed_metadata(self):
        malformed_payloads = [
            {"required_status_checks": None, "required_pull_request_reviews": None},
            {"required_status_checks": {"contexts": "not-a-list"}, "required_pull_request_reviews": None,
             "enforce_admins": {"enabled": False}},
            {"required_status_checks": None, "required_pull_request_reviews": {"required_approving_review_count": True},
             "enforce_admins": {"enabled": False}},
            {"required_status_checks": None, "required_pull_request_reviews": None,
             "enforce_admins": {"enabled": "false"}},
        ]
        for payload in malformed_payloads:
            client, _ = make_client(lambda req, payload=payload: FakeResponse(200, payload))
            with self.subTest(payload=payload):
                with self.assertRaises(forge.ForgeError) as cm:
                    forge.get_branch_protection(client, "main")
                self.assertEqual(cm.exception.kind, "malformed")

    def test_branch_protection_accepts_explicitly_disabled_optional_rules(self):
        payload = {
            "required_status_checks": None,
            "required_pull_request_reviews": None,
            "enforce_admins": {"enabled": False},
        }
        client, _ = make_client(lambda req: FakeResponse(200, payload))
        protection = forge.get_branch_protection(client, "main")
        self.assertEqual(protection["required_checks"], [])
        self.assertEqual(protection["required_approving_reviews"], 0)
        self.assertFalse(protection["enforce_admins"])

    def ruleset(self, **overrides):
        value = {
            "id": 28251664,
            "name": "Protection Main",
            "target": "branch",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "rules": [
                {"type": "deletion"},
                {"type": "non_fast_forward"},
                {"type": "pull_request", "parameters": {"required_approving_review_count": 0}},
                {"type": "required_status_checks", "parameters": {
                    "required_status_checks": [
                        {"context": "govcheck-check", "integration_id": 15368},
                        {"context": "package-alignment", "integration_id": 15368},
                        {"context": "reference-integrity", "integration_id": 15368},
                    ],
                    "strict_required_status_checks_policy": True,
                }},
            ],
            "bypass_actors": [],
            "current_user_can_bypass": "never",
        }
        value.update(overrides)
        return value

    def test_ruleset_audit_passes_exact_pr_checks_source_and_no_bypass(self):
        result = forge.audit_ruleset_payload(self.ruleset(), ["govcheck-check", "package-alignment", "reference-integrity"], 15368)
        self.assertEqual(result["result"], "pass")
        self.assertEqual(result["observed_checks"], ["govcheck-check", "package-alignment", "reference-integrity"])
        self.assertFalse(result["boundary_demonstrated"])
        self.assertEqual(result["bypass_actors"], [])

    def test_ruleset_audit_fails_missing_pull_request_and_required_checks(self):
        ruleset = self.ruleset(rules=[{"type": "deletion"}, {"type": "non_fast_forward"}])
        result = forge.audit_ruleset_payload(ruleset, ["govcheck-check"], 15368)
        self.assertEqual(result["result"], "fail")
        self.assertIn("pull-request requirement is missing", result["findings"])
        self.assertIn("required-status-checks rule is missing", result["findings"])

    def test_ruleset_audit_fails_wrong_source_non_strict_and_bypass(self):
        rules = self.ruleset()["rules"]
        rules[-1]["parameters"]["required_status_checks"][0]["integration_id"] = 999
        rules[-1]["parameters"]["strict_required_status_checks_policy"] = False
        result = forge.audit_ruleset_payload(
            self.ruleset(rules=rules, bypass_actors=[{"actor_id": 1, "actor_type": "Team", "bypass_mode": "always"}]),
            ["govcheck-check", "package-alignment", "reference-integrity"], 15368,
        )
        self.assertEqual(result["result"], "fail")
        self.assertTrue(any("source integration" in finding for finding in result["findings"]))
        self.assertIn("strict required-status-check freshness is disabled", result["findings"])
        self.assertIn("ruleset has bypass actors", result["findings"])

    def test_ruleset_audit_fails_when_bypass_metadata_is_missing(self):
        ruleset = self.ruleset()
        del ruleset["bypass_actors"]
        result = forge.audit_ruleset_payload(
            ruleset, ["govcheck-check", "package-alignment", "reference-integrity"], 15368
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("ruleset bypass-actor configuration is missing or malformed", result["findings"])

        ruleset = self.ruleset()
        del ruleset["current_user_can_bypass"]
        result = forge.audit_ruleset_payload(
            ruleset, ["govcheck-check", "package-alignment", "reference-integrity"], 15368
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("current identity bypass capability is not explicitly disabled", result["findings"])

    def test_ruleset_audit_fails_on_malformed_bypass_metadata(self):
        ruleset = self.ruleset(bypass_actors=None)
        result = forge.audit_ruleset_payload(
            ruleset, ["govcheck-check", "package-alignment", "reference-integrity"], 15368
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("ruleset bypass-actor configuration is missing or malformed", result["findings"])

    def test_ruleset_audit_rejects_non_default_branch_scope(self):
        ruleset = self.ruleset(conditions={"ref_name": {"include": ["refs/heads/release"], "exclude": []}})
        result = forge.audit_ruleset_payload(ruleset, ["govcheck-check", "package-alignment", "reference-integrity"], 15368)
        self.assertEqual(result["result"], "fail")
        self.assertIn("ruleset is not exclusively scoped to the default branch", result["findings"])

    def test_ruleset_audit_fails_unexpected_approval_count(self):
        rules = self.ruleset()["rules"]
        rules[2]["parameters"]["required_approving_review_count"] = 1
        result = forge.audit_ruleset_payload(
            self.ruleset(rules=rules),
            ["govcheck-check", "package-alignment", "reference-integrity"],
            15368,
            expected_approvals=0,
        )
        self.assertEqual(result["result"], "fail")
        self.assertIn("required approving-review count does not match the expected value", result["findings"])

    def test_render_ruleset_payload_is_exact_and_has_no_bypass(self):
        payload = forge.render_ruleset_payload(
            "Protection Main",
            ["govcheck-check", "package-alignment", "reference-integrity"],
            15368,
            required_approvals=0,
        )
        self.assertEqual(payload["target"], "branch")
        self.assertEqual(payload["enforcement"], "active")
        self.assertEqual(payload["conditions"]["ref_name"]["include"], ["~DEFAULT_BRANCH"])
        self.assertEqual(payload["bypass_actors"], [])
        pr_rule = next(rule for rule in payload["rules"] if rule["type"] == "pull_request")
        self.assertEqual(pr_rule["parameters"]["required_approving_review_count"], 0)
        status_rule = next(rule for rule in payload["rules"] if rule["type"] == "required_status_checks")
        self.assertEqual(
            [item["context"] for item in status_rule["parameters"]["required_status_checks"]],
            ["govcheck-check", "package-alignment", "reference-integrity"],
        )
        self.assertTrue(status_rule["parameters"]["strict_required_status_checks_policy"])

    def test_list_rulesets_reads_collection(self):
        client, opener = make_client(lambda req: FakeResponse(200, [{"id": 1, "name": "main"}]))
        result = forge.list_rulesets(client)
        self.assertEqual(result, [{"id": 1, "name": "main"}])
        self.assertTrue(opener.requests[0].full_url.endswith("/repos/octo/repo/rulesets?per_page=100"))

    def test_audit_ruleset_fetches_configuration_read_only(self):
        ruleset = self.ruleset()
        client, opener = make_client(lambda req: FakeResponse(200, ruleset))
        result = forge.audit_ruleset(client, 28251664, ["govcheck-check", "package-alignment", "reference-integrity"], 15368)
        self.assertEqual(result["result"], "pass")
        self.assertEqual(opener.requests[0].get_method(), "GET")
        self.assertTrue(opener.requests[0].full_url.endswith("/repos/octo/repo/rulesets/28251664"))

class CliTests(unittest.TestCase):
    def test_ruleset_payload_cli_is_offline(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = forge.main([
                "ruleset-payload",
                "--required-checks", "govcheck-check,package-alignment,reference-integrity",
                "--check-source-id", "15368",
                "--required-approvals", "0",
            ], env={})
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["bypass_actors"], [])

    def test_cli_list_issues_prints_json(self):
        opener = FakeOpener(lambda req: FakeResponse(200, [{"number": 5, "title": "t", "state": "open", "body": "", "labels": [], "html_url": "u"}]))
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = forge.main(["--owner", "octo", "--repo", "repo", "list-issues"], opener=opener, env={"GOVCHECK_FORGE_TOKEN": "t"})
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data[0]["number"], 5)

    def test_cli_error_path_returns_one_without_token_leak(self):
        opener = FakeOpener(lambda req: (_ for _ in ()).throw(http_error(401)))
        err = io.StringIO()
        with redirect_stderr(err):
            code = forge.main(["--owner", "octo", "--repo", "repo", "list-labels"], opener=opener, env={"GOVCHECK_FORGE_TOKEN": "tok-secret-123"})
        self.assertEqual(code, 1)
        self.assertIn("[auth]", err.getvalue())
        self.assertNotIn("tok-secret-123", err.getvalue())

    def test_cli_audit_ruleset_returns_nonzero_for_missing_gate(self):
        payload = {
            "id": 1,
            "target": "branch",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}],
            "bypass_actors": [],
            "current_user_can_bypass": "never",
        }
        opener = FakeOpener(lambda req: FakeResponse(200, payload))
        out = io.StringIO()
        with redirect_stdout(out):
            code = forge.main(
                ["--owner", "octo", "--repo", "repo", "audit-ruleset", "--id", "1",
                 "--required-checks", "govcheck-check", "--check-source-id", "15368"],
                opener=opener, env={"GOVCHECK_FORGE_TOKEN": "t"},
            )
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out.getvalue())["result"], "fail")
        self.assertEqual(opener.requests[0].get_method(), "GET")

    def test_check_module_never_imports_the_adapter(self):
        src = (ROOT / "govcheck" / "check.py").read_text(encoding="utf-8")
        for line in src.splitlines():
            s = line.strip()
            if s.startswith("import ") or s.startswith("from "):
                self.assertNotIn("forge", s)


if __name__ == "__main__":
    unittest.main()
