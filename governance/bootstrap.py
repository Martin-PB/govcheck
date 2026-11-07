#!/usr/bin/env python3
"""Bootstrap script: generate the governance tree of a new repository
from the GovCheck product package (the governance/ folder).

Usage: python3 bootstrap.py TARGET_DIR
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {"__pycache__", ".git"}

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the governance tree of a governed repository from the GovCheck package.")
    parser.add_argument("target", type=Path, help="target repository root (created if missing)")
    args = parser.parse_args()

    target = args.target.resolve()
    if target.exists() and any(target.iterdir()):
        print(f"Target {target} is not empty; refusing to overwrite.")
        return 1
    target.mkdir(parents=True, exist_ok=True)

    for item in PACKAGE_ROOT.iterdir():
        if item.name in SKIP_DIRS or item.name == "bootstrap.py":
            continue
        dest = target / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    print(f"Governance tree generated in {target}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())