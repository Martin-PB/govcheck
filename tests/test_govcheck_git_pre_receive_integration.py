#!/usr/bin/env python3
"""End-to-end proof that a bare Git receive hook rejects UNKNOWN and accepts PASS."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "install_govcheck_git_pre_receive",
    ROOT / "scripts" / "install-govcheck-git-pre-receive.py",
)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class GitPreReceiveIntegrationTests(unittest.TestCase):
    def run_git(self, *args, cwd=None, check=True):
        return subprocess.run(
            ["git", *map(str, args)],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check,
        )

    def test_bare_repository_rejects_unknown_then_accepts_exact_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bare = root / "remote.git"
            work = root / "work"
            self.run_git("init", "--bare", bare)
            self.run_git("init", "-b", "main", work)

            self.run_git("config", "user.name", "GovCheck fixture", cwd=work)
            self.run_git("config", "user.email", "fixture@example.invalid", cwd=work)
            (work / "README.md").write_text("initial\n", encoding="utf-8")
            self.run_git("add", "README.md", cwd=work)
            self.run_git("commit", "-m", "bootstrap", cwd=work)
            initial = self.run_git("rev-parse", "HEAD", cwd=work).stdout.strip()

            # Bootstrap is deliberately out-of-band; the hook rejects implicit
            # creation of a protected ref and does not claim to secure this step.
            self.run_git("--git-dir", bare, "update-ref", "refs/heads/main", initial)
            self.run_git("--git-dir", bare, "symbolic-ref", "HEAD", "refs/heads/main")
            self.run_git("remote", "add", "origin", str(bare), cwd=work)

            (work / "README.md").write_text("candidate\n", encoding="utf-8")
            self.run_git("commit", "-am", "candidate", cwd=work)
            candidate = self.run_git("rev-parse", "HEAD", cwd=work).stdout.strip()

            gate = root / "trusted-gate"
            gate.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "def arg(name): return sys.argv[sys.argv.index(name) + 1]\n"
                "print(json.dumps({"
                "'schema':'govcheck.acceptance-decision/v0',"
                "'base':arg('--base'),'candidate':arg('--candidate'),'ref':arg('--ref'),"
                "'result':os.environ['GOVCHECK_TEST_RESULT'],"
                "'decision_id':'fixture-' + arg('--candidate')[:8],"
                "'policy_revision':os.environ['GOVCHECK_EXPECTED_POLICY_REVISION'],"
                "'evidence_digest':'sha256:' + 'a'*64,"
                "'verifier':{'identity':os.environ['GOVCHECK_EXPECTED_VERIFIER_IDENTITY'],"
                "'digest':os.environ['GOVCHECK_EXPECTED_VERIFIER_DIGEST']}}))\n",
                encoding="utf-8",
            )
            gate.chmod(0o755)
            gate_digest = "sha256:" + hashlib.sha256(gate.read_bytes()).hexdigest()
            env_file = root / "govcheck-hook.env"

            def write_env(result):
                env_file.write_text(
                    "export GOVCHECK_GATE_COMMAND=" + shlex.quote(str(gate)) + "\n"
                    "export GOVCHECK_EXPECTED_VERIFIER_IDENTITY=fixture-verifier\n"
                    "export GOVCHECK_EXPECTED_VERIFIER_DIGEST=" + gate_digest + "\n"
                    "export GOVCHECK_EXPECTED_POLICY_REVISION=fixture-policy-1\n"
                    "export GOVCHECK_PROTECTED_REFS=refs/heads/main\n"
                    "export GOVCHECK_TEST_RESULT=" + result + "\n"
                    "export GOVCHECK_GATE_TIMEOUT_SECONDS=10\n",
                    encoding="utf-8",
                )
                env_file.chmod(0o600)

            write_env("unknown")
            installer.install_hook(bare, env_file)

            rejected = self.run_git("push", "origin", "main:main", cwd=work, check=False)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("UNKNOWN is not accepted", rejected.stderr)
            remote_after_rejection = self.run_git("--git-dir", bare, "rev-parse", "refs/heads/main").stdout.strip()
            self.assertEqual(remote_after_rejection, initial)

            write_env("pass")
            accepted = self.run_git("push", "origin", "main:main", cwd=work, check=False)
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            remote_after_acceptance = self.run_git("--git-dir", bare, "rev-parse", "refs/heads/main").stdout.strip()
            self.assertEqual(remote_after_acceptance, candidate)


if __name__ == "__main__":
    unittest.main()
