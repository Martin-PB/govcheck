import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from govcheck.journal import Journal
from govcheck.vcs_provenance import build_git_provenance


class RealGitPostReceivePublicationTests(unittest.TestCase):
    def git(self, cwd, *args, env=None):
        merged_env = dict(os.environ)
        if env:
            merged_env.update(env)
        return subprocess.run(
            ["git", *args], cwd=cwd, env=merged_env,
            text=True, capture_output=True, check=True,
        ).stdout.strip()

    def test_real_bare_repo_records_verified_and_bypassed_publications(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            bare = root / "repo.git"
            work = root / "work"
            db = root / "journal.sqlite"
            self.git(root, "init", "--bare", str(bare))
            self.git(root, "init", str(work))
            self.git(work, "config", "user.name", "GovCheck test")
            self.git(work, "config", "user.email", "govcheck-test@example.invalid")
            (work / "tracked.txt").write_text("base\n", encoding="utf-8")
            self.git(work, "add", "tracked.txt")
            self.git(work, "commit", "-m", "base")
            self.git(work, "branch", "-M", "main")
            self.git(work, "remote", "add", "origin", str(bare))
            self.git(work, "push", "origin", "main:refs/heads/main")
            old = self.git(work, "rev-parse", "HEAD")

            scope = "repo:example/project"
            journal = Journal(db)
            journal.initialize(scope, "principal:root", "authority-rev-3", "gov-17")
            env_values = {
                "GIT_DIR": str(bare),
                "PYTHONPATH": str(Path(__file__).resolve().parents[1]),
                "GOVCHECK_JOURNAL_DB": str(db),
                "GOVCHECK_JOURNAL_SCOPE_ID": scope,
                "GOVCHECK_EXPECTED_REPOSITORY_ID": "repo:12345",
                "GOVCHECK_JOURNAL_AUTHORITY_ID": "principal:root",
                "GOVCHECK_JOURNAL_AUTHORITY_REVISION": "authority-rev-3",
                "GOVCHECK_GOVERNANCE_REVISION": "gov-17",
                "GOVCHECK_PROTECTED_REFS": "refs/heads/main",
            }
            hook = bare / "hooks" / "post-receive"
            exports = "\n".join("export " + key + "=" + subprocess.list2cmdline([value]) for key, value in env_values.items())
            hook.write_text(
                "#!/bin/sh\n" + exports + "\nexec python3 -m govcheck.git_publication_receipt\n",
                encoding="utf-8",
            )
            hook.chmod(0o755)

            (work / "tracked.txt").write_text("accepted candidate\n", encoding="utf-8")
            self.git(work, "commit", "-am", "accepted candidate")
            candidate = self.git(work, "rev-parse", "HEAD")
            provenance = build_git_provenance(
                repository_id="repo:12345", repository_uri="https://example.invalid/repo",
                target_ref="refs/heads/main", candidate_commit=candidate,
                candidate_content_digest="sha256:" + "a" * 64,
                base_commit=old, base_content_digest="sha256:" + "b" * 64,
                governance_scope_id=scope, governance_revision="gov-17",
                governance_digest="sha256:" + "c" * 64,
                adapter_id="govcheck.git-acceptance-gate", adapter_version="1",
                observed_at="2026-11-28T12:00:00Z",
            )
            gate_payload = {
                "repositoryId": "repo:12345",
                "candidateRevision": candidate,
                "baseRevision": old,
                "ref": "refs/heads/main",
                "decisionResult": "pass",
                "verification": "authenticated-authority",
                "authorityPrincipal": "principal:root",
                "decisionId": "decision-real-hook-1",
                "vcsProvenance": provenance,
            }
            head = journal.head(scope)
            journal.append(
                scope, head["position"], head["digest"], "gate-real-hook-1",
                "govcheck.acceptance.gate-result/v1", "1", gate_payload,
                "gate-real-hook-key-1", "principal:root",
            )
            self.git(work, "push", "origin", "main:refs/heads/main")
            published = journal.find_latest_event(scope, "govcheck.git.ref-publication/v1", {
                "candidateRevision": candidate,
                "baseRevision": old,
                "ref": "refs/heads/main",
            })
            self.assertEqual(published["event"]["payload"]["publication"], "linked-to-verified-acceptance")

            old = candidate
            (work / "tracked.txt").write_text("bypassed candidate\n", encoding="utf-8")
            self.git(work, "commit", "-am", "bypassed candidate")
            candidate = self.git(work, "rev-parse", "HEAD")
            pushed = subprocess.run(
                ["git", "push", "origin", "main:refs/heads/main"],
                cwd=work, env=dict(os.environ), text=True, capture_output=True,
            )
            self.assertEqual(pushed.returncode, 0, pushed.stderr)
            self.assertEqual(self.git(bare, "rev-parse", "refs/heads/main"), candidate)
            unverified = journal.find_latest_event(scope, "govcheck.git.ref-publication/v1", {
                "candidateRevision": candidate,
                "baseRevision": old,
                "ref": "refs/heads/main",
            })
            self.assertEqual(unverified["event"]["payload"]["publication"], "published-without-verified-acceptance")
            self.assertEqual(journal.verify(scope)["status"], "valid")


if __name__ == "__main__":
    unittest.main()
