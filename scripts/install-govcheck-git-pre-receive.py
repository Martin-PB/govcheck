#!/usr/bin/env python3
"""Install the reference pre-receive adapter into a controlled Git bare repo."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import shutil
import stat
import subprocess
import sys


def install_hook(repository: Path, environment_file: Path):
    repository = repository.expanduser().resolve()
    environment_file = environment_file.expanduser().resolve()
    if not repository.is_dir():
        raise ValueError("repository path does not exist or is not a directory")
    if not environment_file.is_file():
        raise ValueError("administrator-owned hook environment file does not exist")
    if stat.S_IMODE(environment_file.stat().st_mode) & 0o077:
        raise ValueError("hook environment file must not be accessible by group or other users (use mode 0600)")
    try:
        environment_file.relative_to(repository)
    except ValueError:
        pass
    else:
        raise ValueError("hook environment file must be outside the candidate repository")

    check = subprocess.run(
        ["git", "--git-dir", str(repository), "rev-parse", "--is-bare-repository"],
        capture_output=True, text=True, check=False,
    )
    if check.returncode != 0 or check.stdout.strip() != "true":
        raise ValueError("target must be a Git bare repository")

    hooks_dir = repository / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    pre_receive = hooks_dir / "pre-receive"
    if pre_receive.exists():
        raise FileExistsError("pre-receive hook already exists; refusing to overwrite or chain it implicitly")

    source = Path(__file__).resolve().with_name("govcheck-git-pre-receive")
    if not source.is_file():
        raise FileNotFoundError("reference govcheck-git-pre-receive script is missing")
    installed = hooks_dir / "govcheck-git-pre-receive"
    if installed.exists():
        raise FileExistsError("installed GovCheck hook helper already exists")

    shutil.copyfile(source, installed)
    os.chmod(installed, 0o755)
    wrapper = (
        "#!/bin/sh\n"
        "set -eu\n"
        f". {shlex.quote(str(environment_file))}\n"
        f"exec {shlex.quote(sys.executable)} {shlex.quote(str(installed))}\n"
    )
    pre_receive.write_text(wrapper, encoding="utf-8")
    os.chmod(pre_receive, 0o755)
    return pre_receive, installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bare_repository", type=Path)
    parser.add_argument("administrator_environment_file", type=Path)
    args = parser.parse_args()
    try:
        pre_receive, installed = install_hook(args.bare_repository, args.administrator_environment_file)
    except (OSError, ValueError) as exc:
        print(f"installation refused: {exc}", file=sys.stderr)
        return 1
    print(f"installed pre-receive wrapper: {pre_receive}")
    print(f"installed GovCheck adapter: {installed}")
    print("review the administrator-owned environment file and verifier trust pins before enabling writes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
