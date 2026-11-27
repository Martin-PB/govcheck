import base64
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from govcheck import acceptance_decision
from govcheck import attestation
from govcheck import check

ROOT = Path(__file__).resolve().parents[1]
OPENSSL = shutil.which("openssl")
GIT = shutil.which("git")


@unittest.skipUnless(OPENSSL and GIT, "Git and OpenSSL are required for protected-ref integration test")
class PreReceiveAcceptanceIntegrationTests(unittest.TestCase):
    def run_cmd(self, command, *, cwd=None, env=None, check=True):
        return subprocess.run(command, cwd=cwd, env=env, check=check, capture_output=True, text=True)

    def test_real_bare_repo_accepts_scoped_risk_and_rejects_stale_decision(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            work = root / "work"
            bare = root / "repo.git"
            trusted = root / "trusted-gate"
            (trusted / "scripts").mkdir(parents=True)
            work.mkdir()

            shutil.copy2(ROOT / "scripts" / "govcheck-acceptance-gate", trusted / "scripts" / "govcheck-acceptance-gate")
            shutil.copytree(ROOT / "govcheck", trusted / "govcheck")
            (trusted / "scripts" / "govcheck-acceptance-gate").chmod(0o755)

            self.run_cmd([GIT, "init", "-b", "main"], cwd=work)
            self.run_cmd([GIT, "config", "user.name", "Integration Test"], cwd=work)
            self.run_cmd([GIT, "config", "user.email", "integration@example.invalid"], cwd=work)
            (work / "docs").mkdir()
            (work / "docs" / "base.md").write_text("base\n", encoding="utf-8")
            self.run_cmd([GIT, "add", "."], cwd=work)
            self.run_cmd([GIT, "commit", "-m", "base"], cwd=work)
            base = self.run_cmd([GIT, "rev-parse", "HEAD"], cwd=work).stdout.strip()

            self.run_cmd([GIT, "clone", "--bare", str(work), str(bare)])
            (bare / "hooks").mkdir(exist_ok=True)
            shutil.copy2(ROOT / "scripts" / "govcheck-git-pre-receive", bare / "hooks" / "pre-receive")
            (bare / "hooks" / "pre-receive").chmod(0o755)
            self.run_cmd([GIT, "remote", "add", "origin", str(bare)], cwd=work)

            # Place the candidate object on an unprotected staging ref so the
            # gate can inspect it from the bare repository before main advances.
            (work / "docs" / "change.md").write_text("candidate one\n", encoding="utf-8")
            self.run_cmd([GIT, "add", "."], cwd=work)
            self.run_cmd([GIT, "commit", "-m", "candidate one"], cwd=work)
            candidate = self.run_cmd([GIT, "rev-parse", "HEAD"], cwd=work).stdout.strip()
            self.run_cmd([GIT, "push", "origin", f"{candidate}:refs/heads/staging"], cwd=work)

            private_key, public_key = root / "authority-private.pem", root / "authority-public.pem"
            self.run_cmd([OPENSSL, "genpkey", "-algorithm", "ED25519", "-out", str(private_key)])
            self.run_cmd([OPENSSL, "pkey", "-in", str(private_key), "-pubout", "-out", str(public_key)])
            openssl_path = Path(OPENSSL).resolve()

            def digest(path):
                return hashlib.sha256(Path(path).read_bytes()).hexdigest()

            now = datetime.now(timezone.utc)
            policy = {
                "schemaVersion": "1",
                "policyId": "govcheck.attestation-trust-policy/v1",
                "revision": "integration-policy-17",
                "openssl": {"path": str(openssl_path), "sha256": digest(openssl_path)},
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
            policy_digest = hashlib.sha256(policy_bytes).hexdigest()

            gate_path = trusted / "scripts" / "govcheck-acceptance-gate"
            gate_digest = digest(gate_path)
            decision_path = root / "acceptance-decision.json"
            decision_path.write_text("{}", encoding="utf-8")

            env = dict(os.environ)
            env.update({
                "GOVCHECK_PROTECTED_REFS": "refs/heads/main",
                "GOVCHECK_ALLOW_ACCEPTED_WITH_RISK": "true",
                "GOVCHECK_GATE_COMMAND": str(gate_path),
                "GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:integration-test",
                "GOVCHECK_EXPECTED_POLICY_REVISION": policy["revision"],
                "GOVCHECK_EXPECTED_POLICY_DIGEST": "sha256:" + policy_digest,
                "GOVCHECK_EXPECTED_VERIFIER_IDENTITY": "govcheck-integration-gate-v1",
                "GOVCHECK_EXPECTED_VERIFIER_DIGEST": "sha256:" + gate_digest,
                "GOVCHECK_TRUST_POLICY_PATH": str(policy_path),
                "GOVCHECK_TRUST_POLICY_SHA256": policy_digest,
                "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
                "GOVCHECK_SCOPE_ID": "repo:integration-test",
                "GOVCHECK_ACCEPTANCE_DECISION_ENVELOPE": str(decision_path),
                "GOVCHECK_GATE_TIMEOUT_SECONDS": "120",
            })

            # Obtain the exact deterministic report digest from the installed
            # gate before signing the authority decision.
            gate_args = type("Args", (), {
                "repository_id": "repo:integration-test",
                "vcs_kind": "git",
                "base": base,
                "candidate": candidate,
                "ref": "refs/heads/main",
                "git_dir": str(bare),
            })()
            from govcheck import git_acceptance_gate
            code, preliminary = git_acceptance_gate.run_gate(gate_args, env=env)
            self.assertEqual(code, 0)
            self.assertTrue(preliminary["evidence_digest"].startswith("sha256:"))
            report_digest = preliminary["evidence_digest"].removeprefix("sha256:")

            candidate_worktree = root / "candidate-worktree"
            self.run_cmd([GIT, "clone", "--shared", "--no-checkout", str(bare), str(candidate_worktree)])
            self.run_cmd([GIT, "-C", str(candidate_worktree), "checkout", "--detach", candidate])
            content_digest = check.candidate_content_digest(candidate_worktree)
            risk_record = {
                "id": "risk-integration-17",
                "reason": "Independent review evidence is unavailable in this single-contributor test.",
                "scope": "repo:integration-test",
                "expiresAt": (now + timedelta(days=30)).isoformat(),
                "residualRisk": "The review result remains UNKNOWN; this is a scoped authority acceptance.",
                "affectedClaims": ["claim:independent-review"],
                "authorizationDigest": hashlib.sha256(b"integration risk authorization record").hexdigest(),
            }
            statement = acceptance_decision.build_statement(
                repository_uri="https://example.invalid/govcheck",
                decision_id="decision-integration-17",
                repository_id="repo:integration-test",
                candidate_revision=candidate,
                candidate_content_sha256=content_digest,
                base_revision=base,
                ref="refs/heads/main",
                governance_revision="gov-17",
                scope_id="repo:integration-test",
                evaluation_digest=report_digest,
                result="accept_with_risk",
                decided_on=now.isoformat(),
                rationale="Bounded acceptance under the sole configured governance authority.",
                risk_acceptance=risk_record,
            )
            payload = attestation.canonical_statement_bytes(statement)
            pae = attestation.dsse_pae(attestation.DSSE_PAYLOAD_TYPE, payload)
            pae_path, signature_path = root / "pae.bin", root / "signature.bin"
            pae_path.write_bytes(pae)
            self.run_cmd([OPENSSL, "pkeyutl", "-sign", "-inkey", str(private_key), "-rawin", "-in", str(pae_path), "-out", str(signature_path)])
            envelope = attestation.build_dsse_envelope(statement, [{
                "keyid": "authority-key",
                "sig": base64.b64encode(signature_path.read_bytes()).decode("ascii"),
            }])
            decision_path.write_text(json.dumps(envelope, sort_keys=True, separators=(",", ":")), encoding="utf-8")

            accepted = self.run_cmd([GIT, "push", "origin", f"{candidate}:refs/heads/main"], cwd=work, env=env, check=False)
            self.assertEqual(accepted.returncode, 0, accepted.stderr + accepted.stdout)
            main_after_accept = self.run_cmd([GIT, "--git-dir", str(bare), "rev-parse", "refs/heads/main"]).stdout.strip()
            self.assertEqual(main_after_accept, candidate)

            # Reuse the old decision for a new candidate; the exact candidate
            # binding must fail and main must remain unchanged.
            (work / "docs" / "change.md").write_text("candidate two\n", encoding="utf-8")
            self.run_cmd([GIT, "add", "."], cwd=work)
            self.run_cmd([GIT, "commit", "-m", "candidate two"], cwd=work)
            candidate_two = self.run_cmd([GIT, "rev-parse", "HEAD"], cwd=work).stdout.strip()
            self.run_cmd([GIT, "push", "origin", f"{candidate_two}:refs/heads/staging-two"], cwd=work)
            rejected = self.run_cmd([GIT, "push", "origin", f"{candidate_two}:refs/heads/main"], cwd=work, env=env, check=False)
            self.assertNotEqual(rejected.returncode, 0)
            main_after_reject = self.run_cmd([GIT, "--git-dir", str(bare), "rev-parse", "refs/heads/main"]).stdout.strip()
            self.assertEqual(main_after_reject, candidate)


if __name__ == "__main__":
    unittest.main()
