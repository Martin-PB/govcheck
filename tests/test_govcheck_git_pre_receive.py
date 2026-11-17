#!/usr/bin/env python3
"""Protocol tests for the Git pre-receive acceptance-boundary adapter."""
from __future__ import annotations

import hashlib
import importlib.util
from importlib.machinery import SourceFileLoader
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
hook_path = ROOT / "scripts" / "govcheck-git-pre-receive"
loader = SourceFileLoader("govcheck_git_pre_receive", str(hook_path))
spec = importlib.util.spec_from_loader(loader.name, loader)
hook = importlib.util.module_from_spec(spec)
loader.exec_module(hook)

BASE = "1" * 40
CANDIDATE = "2" * 40
REF = "refs/heads/main"


def envelope(result="pass", verifier_digest="", verifier_identity="govcheck-server-verifier",
             repository_id="forge://fixture/project", vcs_kind="git",
             policy_revision="policy-rev-7", policy_digest="sha256:" + "d" * 64, **overrides):
    payload = {
        "schema": hook.SCHEMA,
        "base": BASE,
        "candidate": CANDIDATE,
        "ref": REF,
        "repository_id": repository_id,
        "vcs_kind": vcs_kind,
        "result": result,
        "decision_id": "decision-0001",
        "policy_revision": policy_revision,
        "policy_digest": policy_digest,
        "evidence_digest": "sha256:" + "a" * 64,
        "verifier": {
            "identity": verifier_identity,
            "digest": verifier_digest,
        },
    }
    payload.update(overrides)
    return payload


def runner_for(payload=None, returncode=0, stdout=None, stderr=""):
    calls = []

    def runner(args, **kwargs):
        calls.append((args, kwargs))
        output = stdout if stdout is not None else json.dumps(payload)
        return SimpleNamespace(returncode=returncode, stdout=output, stderr=stderr)

    return runner, calls


class PreReceiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.gate = root / "govcheck-gate"
        self.gate.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        self.gate.chmod(0o755)
        self.digest = "sha256:" + hashlib.sha256(self.gate.read_bytes()).hexdigest()
        self.env = {
            "GOVCHECK_GATE_COMMAND": str(self.gate),
            "GOVCHECK_EXPECTED_VERIFIER_IDENTITY": "govcheck-server-verifier",
            "GOVCHECK_EXPECTED_VERIFIER_DIGEST": self.digest,
            "GOVCHECK_EXPECTED_REPOSITORY_ID": "forge://fixture/project",
            "GOVCHECK_EXPECTED_POLICY_REVISION": "policy-rev-7",
            "GOVCHECK_EXPECTED_POLICY_DIGEST": "sha256:" + "d" * 64,
            "GOVCHECK_PROTECTED_REFS": "refs/heads/main,refs/heads/release/*",
            "GIT_DIR": "/srv/git/project.git",
        }

    def input(self, old=BASE, new=CANDIDATE, ref=REF):
        return f"{old} {new} {ref}\n"

    def payload(self, result="pass", **overrides):
        values = {
            "verifier_digest": self.digest,
            "verifier_identity": self.env["GOVCHECK_EXPECTED_VERIFIER_IDENTITY"],
            "repository_id": self.env["GOVCHECK_EXPECTED_REPOSITORY_ID"],
            "policy_revision": self.env["GOVCHECK_EXPECTED_POLICY_REVISION"],
            "policy_digest": self.env["GOVCHECK_EXPECTED_POLICY_DIGEST"],
        }
        values.update(overrides)
        return envelope(result, **values)

    def test_exact_pass_is_accepted_and_git_dir_is_forwarded(self):
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 0)
        self.assertIn("accept:", messages[0])
        args, kwargs = calls[0]
        self.assertEqual(args[args.index("--repository-id") + 1], self.env["GOVCHECK_EXPECTED_REPOSITORY_ID"])
        self.assertEqual(args[args.index("--vcs-kind") + 1], "git")
        self.assertEqual(args[args.index("--base") + 1], BASE)
        self.assertEqual(args[args.index("--candidate") + 1], CANDIDATE)
        self.assertEqual(args[args.index("--ref") + 1], REF)
        self.assertEqual(args[-2:], ["--git-dir", self.env["GIT_DIR"]])

    def test_unknown_fails_closed(self):
        runner, _ = runner_for(self.payload("unknown"))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("UNKNOWN is not accepted", messages[0])

    def test_fail_fails_closed(self):
        runner, _ = runner_for(self.payload("fail"))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("FAIL is not accepted", messages[0])

    def test_conflict_fails_closed(self):
        runner, _ = runner_for(self.payload("conflict"))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("CONFLICT is not accepted", messages[0])

    def test_candidate_mismatch_fails_closed(self):
        runner, _ = runner_for(self.payload("pass", candidate="3" * 40))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("not bound to this candidate", messages[0])

    def test_base_mismatch_fails_closed(self):
        runner, _ = runner_for(self.payload("pass", base="4" * 40))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("not bound to this base", messages[0])

    def test_ref_mismatch_fails_closed(self):
        runner, _ = runner_for(self.payload("pass", ref="refs/heads/other"))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("not bound to this ref", messages[0])

    def test_repository_vcs_and_policy_digest_mismatches_fail_closed(self):
        for payload, expected in (
            (self.payload("pass", repository_id="forge://other/project"), "repository_id"),
            (self.payload("pass", vcs_kind="pijul"), "vcs_kind"),
            (self.payload("pass", policy_digest="sha256:" + "e" * 64), "policy digest"),
        ):
            with self.subTest(expected=expected):
                runner, _ = runner_for(payload)
                code, messages = hook.run_pre_receive(self.input(), self.env, runner)
                self.assertEqual(code, 1)
                self.assertIn(expected, messages[0])

    def test_policy_revision_mismatch_fails_closed(self):
        runner, _ = runner_for(self.payload("pass", policy_revision="policy-rev-old"))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("pinned policy revision", messages[0])

    def test_verifier_identity_or_digest_mismatch_fails_closed(self):
        for payload in (
            self.payload("pass", verifier_identity="untrusted"),
            self.payload("pass", verifier={"identity": "govcheck-server-verifier", "digest": "sha256:" + "c" * 64}),
        ):
            with self.subTest(payload=payload):
                runner, _ = runner_for(payload)
                code, messages = hook.run_pre_receive(self.input(), self.env, runner)
                self.assertEqual(code, 1)
                self.assertIn("trust pin", messages[0])

    def test_gate_binary_digest_is_pinned(self):
        env = {**self.env, "GOVCHECK_EXPECTED_VERIFIER_DIGEST": "sha256:" + "c" * 64}
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive(self.input(), env, runner)
        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertIn("digest does not match", messages[0])

    def test_gate_must_be_outside_candidate_repository(self):
        env = {**self.env, "GIT_DIR": str(self.gate.parent)}
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive(self.input(), env, runner)
        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertIn("outside the candidate repository", messages[0])

    def test_malformed_or_incomplete_envelope_fails_closed(self):
        for payload in ({}, self.payload("pass", evidence_digest="bad")):
            with self.subTest(payload=payload):
                runner, _ = runner_for(payload)
                code, _ = hook.run_pre_receive(self.input(), self.env, runner)
                self.assertEqual(code, 1)

    def test_nonzero_gate_exit_fails_closed(self):
        runner, _ = runner_for(self.payload("pass"), returncode=2, stderr="verifier unavailable")
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("verifier unavailable", messages[0])

    def test_malformed_gate_json_fails_closed(self):
        runner, _ = runner_for(stdout="not-json")
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("malformed JSON", messages[0])

    def test_missing_gate_command_or_trust_pins_fails_closed(self):
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive(self.input(), {}, runner)
        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertIn("not configured", messages[0])

        env = {key: value for key, value in self.env.items() if key != "GOVCHECK_EXPECTED_POLICY_REVISION"}
        code, messages = hook.run_pre_receive(self.input(), env, runner)
        self.assertEqual(code, 1)
        self.assertIn("identity and policy revision", messages[0])

        env = {key: value for key, value in self.env.items() if key != "GOVCHECK_EXPECTED_REPOSITORY_ID"}
        code, messages = hook.run_pre_receive(self.input(), env, runner)
        self.assertEqual(code, 1)
        self.assertIn("repository identity", messages[0])

        env = {key: value for key, value in self.env.items() if key != "GOVCHECK_EXPECTED_POLICY_DIGEST"}
        code, messages = hook.run_pre_receive(self.input(), env, runner)
        self.assertEqual(code, 1)
        self.assertIn("POLICY_DIGEST", messages[0])

    def test_unprotected_ref_is_not_evaluated(self):
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive(
            self.input(ref="refs/heads/feature/topic"), self.env, runner
        )
        self.assertEqual(code, 0)
        self.assertEqual(calls, [])
        self.assertIn("no protected refs", messages[0])

    def test_protected_ref_deletion_is_rejected(self):
        zero = "0" * 40
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive(self.input(new=zero), self.env, runner)
        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertIn("deletion", messages[0])

    def test_initial_protected_ref_creation_requires_bootstrap(self):
        zero = "0" * 40
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive(self.input(old=zero), self.env, runner)
        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertIn("bootstrap decision", messages[0])

    def test_accepted_risk_is_rejected_by_default(self):
        risk = {"id": "risk-1", "authority": "root", "reason": "emergency",
                "scope": "candidate", "expires_at": "2026-11-18T00:00:00Z"}
        runner, _ = runner_for(self.payload("accepted-with-risk", risk_acceptance=risk))
        code, messages = hook.run_pre_receive(self.input(), self.env, runner)
        self.assertEqual(code, 1)
        self.assertIn("disabled", messages[0])

    def test_accepted_risk_requires_complete_record_and_explicit_enablement(self):
        env = {**self.env, "GOVCHECK_ALLOW_ACCEPTED_WITH_RISK": "true"}
        risk = {"id": "risk-1", "authority": "root", "reason": "emergency",
                "scope": "candidate", "expires_at": "2026-11-18T00:00:00Z"}
        runner, _ = runner_for(self.payload("accepted-with-risk", risk_acceptance=risk))
        code, messages = hook.run_pre_receive(self.input(), env, runner)
        self.assertEqual(code, 0)
        self.assertIn("ACCEPTED_WITH_RISK", messages[0])

        runner, _ = runner_for(self.payload("accepted-with-risk", risk_acceptance={"id": "risk-1"}))
        code, messages = hook.run_pre_receive(self.input(), env, runner)
        self.assertEqual(code, 1)
        self.assertIn("incomplete", messages[0])

    def test_any_failed_protected_ref_rejects_entire_receive_operation(self):
        second_candidate = "3" * 40
        calls = []

        def runner(args, **kwargs):
            calls.append(args)
            if args[args.index("--candidate") + 1] == second_candidate:
                payload = self.payload("unknown", candidate=second_candidate, ref="refs/heads/release/1")
            else:
                payload = self.payload("pass")
            return SimpleNamespace(returncode=0, stdout=json.dumps(payload), stderr="")

        updates = self.input() + f"{BASE} {second_candidate} refs/heads/release/1\n"
        code, messages = hook.run_pre_receive(updates, self.env, runner)
        self.assertEqual(code, 1)
        self.assertEqual(len(calls), 2)
        self.assertEqual(sum(message.startswith("reject:") for message in messages), 1)

    def test_malformed_pre_receive_input_is_rejected(self):
        runner, calls = runner_for(self.payload("pass"))
        code, messages = hook.run_pre_receive("not a valid update\n", self.env, runner)
        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertIn("malformed", messages[0])


if __name__ == "__main__":
    unittest.main()
