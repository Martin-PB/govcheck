import importlib.util
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

INSTALLER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install-govcheck-git-post-receive.py"
SPEC = importlib.util.spec_from_file_location("install_govcheck_git_post_receive", INSTALLER_PATH)
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)
install_hook = INSTALLER.install_hook


class InstallGitPostReceiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.bare = self.root / "repo.git"
        subprocess.run(["git", "init", "--bare", str(self.bare)], check=True, capture_output=True)
        self.env_file = self.root / "govcheck-hook.env"
        self.env_file.write_text("GOVCHECK_JOURNAL_DB=/var/lib/govcheck/journal.sqlite\n", encoding="utf-8")
        os.chmod(self.env_file, 0o600)
        self.package_root = Path(__file__).resolve().parents[1]

    def tearDown(self):
        self.temp.cleanup()

    def test_installs_wrapper_and_helper_outside_candidate_tree(self):
        wrapper, helper = install_hook(self.bare, self.env_file, self.package_root)
        self.assertTrue(wrapper.is_file())
        self.assertTrue(helper.is_file())
        self.assertEqual(stat.S_IMODE(wrapper.stat().st_mode), 0o755)
        self.assertEqual(stat.S_IMODE(helper.stat().st_mode), 0o755)
        text = wrapper.read_text(encoding="utf-8")
        self.assertIn(str(self.env_file), text)
        self.assertIn(str(self.package_root), text)
        self.assertIn("post-receive", text)

    def test_refuses_to_overwrite_existing_post_receive_hook(self):
        hook = self.bare / "hooks" / "post-receive"
        hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            install_hook(self.bare, self.env_file, self.package_root)
        self.assertEqual(hook.read_text(encoding="utf-8"), "#!/bin/sh\nexit 0\n")

    def test_refuses_insecure_environment_file(self):
        os.chmod(self.env_file, 0o644)
        with self.assertRaises(ValueError):
            install_hook(self.bare, self.env_file, self.package_root)

    def test_refuses_environment_file_inside_bare_repository(self):
        inside = self.bare / "hooks" / "govcheck.env"
        inside.parent.mkdir(parents=True, exist_ok=True)
        inside.write_text("GOVCHECK_JOURNAL_DB=/var/lib/govcheck/journal.sqlite\n", encoding="utf-8")
        os.chmod(inside, 0o600)
        with self.assertRaises(ValueError):
            install_hook(self.bare, inside, self.package_root)

    def test_refuses_package_root_inside_bare_repository(self):
        package = self.bare / "package"
        (package / "govcheck").mkdir(parents=True)
        (package / "govcheck" / "git_publication_receipt.py").write_text("", encoding="utf-8")
        with self.assertRaises(ValueError):
            install_hook(self.bare, self.env_file, package)


if __name__ == "__main__":
    unittest.main()
