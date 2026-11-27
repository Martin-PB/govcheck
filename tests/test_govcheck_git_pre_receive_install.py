#!/usr/bin/env python3
"""Installation tests for the Git pre-receive adapter."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "install_govcheck_git_pre_receive",
    ROOT / "scripts" / "install-govcheck-git-pre-receive.py",
)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bare = self.root / "repo.git"
        subprocess.run(["git", "init", "--bare", str(self.bare)], check=True, capture_output=True)
        self.env_file = self.root / "govcheck-hook.env"
        self.env_file.write_text(
            "export GOVCHECK_GATE_COMMAND=/opt/govcheck/bin/govcheck-gate\n"
            "export GOVCHECK_EXPECTED_VERIFIER_IDENTITY=govcheck-server-verifier\n"
            "export GOVCHECK_EXPECTED_VERIFIER_DIGEST=sha256:" + "a" * 64 + "\n"
            "export GOVCHECK_EXPECTED_POLICY_REVISION=policy-rev-7\n",
            encoding="utf-8",
        )
        self.env_file.chmod(0o600)

    def test_installs_executable_hook_and_external_environment_wrapper(self):
        wrapper, installed = installer.install_hook(self.bare, self.env_file)
        self.assertTrue(wrapper.is_file())
        self.assertTrue(installed.is_file())
        self.assertTrue(os.access(wrapper, os.X_OK))
        self.assertTrue(os.access(installed, os.X_OK))
        content = wrapper.read_text(encoding="utf-8")
        self.assertIn(str(self.env_file), content)
        self.assertIn(str(installed), content)
        self.assertIn("GOVCHECK_EXPECTED_POLICY_REVISION", self.env_file.read_text(encoding="utf-8"))

    def test_refuses_to_overwrite_existing_pre_receive_hook(self):
        hooks = self.bare / "hooks"
        hooks.mkdir(exist_ok=True)
        existing = hooks / "pre-receive"
        existing.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            installer.install_hook(self.bare, self.env_file)
        self.assertEqual(existing.read_text(encoding="utf-8"), "#!/bin/sh\nexit 0\n")

    def test_refuses_non_bare_repository(self):
        worktree = self.root / "worktree"
        subprocess.run(["git", "init", str(worktree)], check=True, capture_output=True)
        with self.assertRaises(ValueError):
            installer.install_hook(worktree, self.env_file)

    def test_refuses_environment_file_inside_bare_repository(self):
        internal = self.bare / "hooks" / "govcheck.env"
        internal.write_text("export GOVCHECK_GATE_COMMAND=/untrusted\n", encoding="utf-8")
        internal.chmod(0o600)
        with self.assertRaises(ValueError):
            installer.install_hook(self.bare, internal)

    def test_refuses_world_readable_environment_file(self):
        self.env_file.chmod(0o644)
        with self.assertRaises(ValueError):
            installer.install_hook(self.bare, self.env_file)


if __name__ == "__main__":
    unittest.main()
