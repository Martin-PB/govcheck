import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-github-receipt-check-config.py"
SPEC = importlib.util.spec_from_file_location("receipt_config_preflight", SCRIPT)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


class GitHubReceiptConfigPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.policy_dir = self.root / "govcheck" / "formal"
        self.policy_dir.mkdir(parents=True)
        self.policy_path = self.policy_dir / "trust-policy.json"
        self.public_key = self.policy_dir / "root.pub"
        self.public_key.write_bytes(b"test public key material")
        self.openssl = Path(self.temp.name) / "openssl"
        self.openssl.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        self.openssl.chmod(0o755)
        self.file_digest = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
        self.policy = {
            "schemaVersion": "1",
            "policyId": "govcheck.attestation-trust-policy/v1",
            "revision": "trust-r1",
            "openssl": {"path": str(self.openssl), "sha256": self.file_digest(self.openssl)},
            "keys": [{
                "keyId": "root-key", "algorithm": "ed25519",
                "publicKeyPath": "root.pub", "publicKeySha256": self.file_digest(self.public_key),
                "principalId": "principal:root", "roles": ["governance-authority"],
                "validFrom": "2000-01-01T00:00:00Z", "validUntil": "2100-01-01T00:00:00Z",
                "revoked": False,
            }],
        }
        raw = json.dumps(self.policy, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.policy_path.write_bytes(raw)
        self.env = {
            "GOVCHECK_TRUST_POLICY_PATH": "govcheck/formal/trust-policy.json",
            "GOVCHECK_TRUST_POLICY_SHA256": hashlib.sha256(raw).hexdigest(),
            "GOVCHECK_JOURNAL_SCOPE_ID": "repo:example/project",
            "GOVCHECK_REPOSITORY_URI": "https://github.com/example/project",
            "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
            "GOVCHECK_GOVERNANCE_DIGEST": "sha256:" + "a" * 64,
            "GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:12345",
            "GOVCHECK_EXPECTED_POLICY_DIGEST": "sha256:" + "b" * 64,
            "GOVCHECK_REQUIRED_ROLE": "governance-authority",
            "GOVCHECK_PROTECTED_BASE_REF": "main",
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_pinned_policy_and_repository_variables_pass(self):
        result = PREFLIGHT.validate_config(self.root, self.env)
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["activeKeyCount"], 1)
        self.assertEqual(result["scopeId"], "repo:example/project")

    def test_legacy_mismatched_policy_id_fails_closed(self):
        policy = dict(self.policy, policyId="urn:govcheck:trust-policy:v1")
        raw = json.dumps(policy, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.policy_path.write_bytes(raw)
        env = dict(self.env, GOVCHECK_TRUST_POLICY_SHA256=hashlib.sha256(raw).hexdigest())
        with self.assertRaises(PREFLIGHT.ConfigError):
            PREFLIGHT.validate_config(self.root, env)

    def test_missing_repository_variable_fails_closed(self):
        env = dict(self.env)
        env.pop("GOVCHECK_JOURNAL_SCOPE_ID")
        with self.assertRaises(PREFLIGHT.ConfigError):
            PREFLIGHT.validate_config(self.root, env)

    def test_trust_policy_digest_mismatch_fails(self):
        env = dict(self.env, GOVCHECK_TRUST_POLICY_SHA256="0" * 64)
        with self.assertRaises(PREFLIGHT.ConfigError):
            PREFLIGHT.validate_config(self.root, env)

    def test_untrusted_or_revoked_key_cannot_satisfy_required_role(self):
        policy = dict(self.policy)
        policy["keys"] = [dict(self.policy["keys"][0], roles=["observer"], revoked=False)]
        raw = json.dumps(policy, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.policy_path.write_bytes(raw)
        env = dict(self.env, GOVCHECK_TRUST_POLICY_SHA256=hashlib.sha256(raw).hexdigest())
        with self.assertRaises(PREFLIGHT.ConfigError):
            PREFLIGHT.validate_config(self.root, env)

    def test_invalid_governance_digest_fails(self):
        env = dict(self.env, GOVCHECK_GOVERNANCE_DIGEST="sha256:bad")
        with self.assertRaises(PREFLIGHT.ConfigError):
            PREFLIGHT.validate_config(self.root, env)


if __name__ == "__main__":
    unittest.main()
