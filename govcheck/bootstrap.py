#!/usr/bin/env python3
"""Bootstrap the GovCheck governance package into a repository.

Legacy mode (new, empty repository):
  python3 bootstrap.py TARGET_DIR
    copy the whole package into an empty target; refuses non-empty targets.

Existing-repository contract (inspect -> plan -> apply -> rollback):
  python3 bootstrap.py inspect TARGET [--out report.json]
  python3 bootstrap.py plan TARGET [--capabilities a,b] [--out plan.json]
  python3 bootstrap.py apply TARGET [--capabilities a,b] [--plan plan.json] [--out result.json]
  python3 bootstrap.py rollback TARGET [--out result.json]

inspect and plan never mutate the target. apply writes only missing files,
never overwrites existing content (conflicts are preserved and reported), is
idempotent, and records a package-owned marker (.govcheck-bootstrap.json) with
the package version, the package digest and the installed files; rollback
removes exactly the installed files whose content still matches the recorded
digest. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {"__pycache__", ".git"}
MARKER_NAME = ".govcheck-bootstrap.json"
TOOL = "govcheck-bootstrap"

# Installable capabilities: capability name -> top-level package entries.
CAPABILITIES = {
    "readme": ("README.md", "README.fr.md"),
    "check": ("check.py",),
    "forge": ("forge.py",),
    "decisions": ("decisions",),
    "docs": ("docs",),
    "formal": ("formal",),
    "scripts": ("scripts",),
    "workflows": (".github",),
}
DEFAULT_CAPABILITIES = tuple(sorted(CAPABILITIES))
SUBCOMMANDS = ("inspect", "plan", "apply", "rollback")


def package_version() -> str:
    """Version label of the package, read from the sibling check.py."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("govcheck_check_version", PACKAGE_ROOT / "check.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return str(getattr(mod, "VERSION", "unknown"))
    except Exception:
        return "unknown"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def package_files() -> list:
    """Sorted relative posix paths of all installable package files."""
    entries = sorted({e for values in CAPABILITIES.values() for e in values})
    out = []
    for entry in entries:
        p = PACKAGE_ROOT / entry
        if p.is_file():
            out.append(entry)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if any(part in SKIP_DIRS for part in f.parts):
                    continue
                if f.is_file():
                    out.append(f.relative_to(PACKAGE_ROOT).as_posix())
    return sorted(set(out))


def package_digest() -> str:
    """SHA-256 over the sorted (path, content digest) pairs of the package."""
    h = hashlib.sha256()
    for rel in package_files():
        h.update(rel.encode("utf-8"))
        h.update(bytes([0]))
        h.update(sha256_bytes((PACKAGE_ROOT / rel).read_bytes()).encode("ascii"))
        h.update(bytes([10]))
    return h.hexdigest()


def parse_capabilities(text):
    if text is None or not text.strip():
        return list(DEFAULT_CAPABILITIES)
    caps = sorted({c.strip() for c in text.split(",") if c.strip()})
    unknown = [c for c in caps if c not in CAPABILITIES]
    if unknown:
        raise SystemExit("unknown capabilities: " + ", ".join(unknown) + "; available: " + ", ".join(DEFAULT_CAPABILITIES))
    return caps


def selected_files(capabilities) -> list:
    wanted = {e for c in capabilities for e in CAPABILITIES[c]}
    out = []
    for rel in package_files():
        if rel in wanted or rel.split("/", 1)[0] in wanted:
            out.append(rel)
    return out


def compute_actions(target: Path, capabilities) -> list:
    actions = []
    for rel in selected_files(capabilities):
        src = PACKAGE_ROOT / rel
        dst = target / rel
        rec = {"path": rel, "source_sha256": sha256_file(src)}
        if dst.is_symlink():
            rec["action"] = "conflict"
            rec["reason"] = "symlink"
        elif dst.exists() and not dst.is_file():
            rec["action"] = "conflict"
            rec["reason"] = "existing non-file path"
        elif not dst.exists():
            rec["action"] = "create"
        elif sha256_file(dst) == rec["source_sha256"]:
            rec["action"] = "identical"
        else:
            rec["action"] = "conflict"
            rec["existing_sha256"] = sha256_file(dst)
        actions.append(rec)
    return actions


def build_plan(target: Path, capabilities) -> dict:
    actions = compute_actions(target, capabilities)
    summary = {}
    for a in actions:
        summary[a["action"]] = summary.get(a["action"], 0) + 1
    return {
        "tool": TOOL,
        "package_version": package_version(),
        "package_digest": package_digest(),
        "target": str(target),
        "capabilities": list(capabilities),
        "actions": actions,
        "summary": summary,
    }


def read_marker(target: Path):
    mp = target / MARKER_NAME
    if not mp.is_file():
        return None
    try:
        return json.loads(mp.read_text(encoding="utf-8"))
    except ValueError:
        return {"unparsable": True}


def inspect_target(target: Path) -> dict:
    conflicts = [a["path"] for a in compute_actions(target, list(DEFAULT_CAPABILITIES)) if a["action"] == "conflict"]
    present = sorted({e for c in DEFAULT_CAPABILITIES for e in CAPABILITIES[c] if (target / e).exists()})
    return {
        "tool": TOOL,
        "package_version": package_version(),
        "package_digest": package_digest(),
        "package_file_count": len(package_files()),
        "target": str(target),
        "exists": target.exists(),
        "empty": (not target.exists()) or (target.is_dir() and not any(target.iterdir())),
        "is_git_repo": (target / ".git").exists(),
        "present_top_level": present,
        "conflicts": conflicts,
        "marker": read_marker(target),
    }


def apply_plan(target: Path, capabilities, plan_path=None):
    plan = build_plan(target, capabilities)
    if plan_path is not None:
        loaded = json.loads(Path(plan_path).read_text(encoding="utf-8"))
        if loaded.get("package_digest") != plan["package_digest"] or loaded.get("actions") != plan["actions"]:
            return {"tool": TOOL, "target": str(target), "error": "stale plan: target or package changed since the plan was produced; run plan again"}, 2
    target.mkdir(parents=True, exist_ok=True)
    created = []
    conflicts = []
    identical = 0
    for a in plan["actions"]:
        dst = target / a["path"]
        if a["action"] == "create":
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes((PACKAGE_ROOT / a["path"]).read_bytes())
            created.append({"path": a["path"], "sha256": a["source_sha256"]})
        elif a["action"] == "identical":
            identical += 1
        else:
            conflicts.append(a["path"])
    installed = [{"path": a["path"], "sha256": a["source_sha256"]} for a in plan["actions"] if a["action"] in ("create", "identical")]
    marker = {
        "tool": TOOL,
        "package_version": plan["package_version"],
        "package_digest": plan["package_digest"],
        "capabilities": plan["capabilities"],
        "installed": installed,
        "conflicts": sorted(conflicts),
    }
    (target / MARKER_NAME).write_text(json.dumps(marker, indent=2, ensure_ascii=False) + chr(10), encoding="utf-8")
    result = {
        "tool": TOOL,
        "package_version": plan["package_version"],
        "package_digest": plan["package_digest"],
        "target": str(target),
        "created": created,
        "created_count": len(created),
        "already_present": identical,
        "conflicts_preserved": sorted(conflicts),
        "marker": MARKER_NAME,
    }
    return result, 0


def rollback_target(target: Path):
    mp = target / MARKER_NAME
    marker = read_marker(target)
    if marker is None:
        return {"tool": TOOL, "target": str(target), "error": "no bootstrap marker " + MARKER_NAME + "; nothing to roll back"}, 1
    removed = []
    for entry in marker.get("installed", []):
        p = target / str(entry.get("path", ""))
        if p.is_file() and not p.is_symlink() and sha256_file(p) == entry.get("sha256"):
            p.unlink()
            removed.append(entry["path"])
    dirs = sorted({target.joinpath(r).parent for r in removed}, key=lambda d: len(d.parts), reverse=True)
    for d in dirs:
        try:
            if d != target and d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        except OSError:
            pass
    mp.unlink()
    return {"tool": TOOL, "target": str(target), "removed": sorted(removed), "removed_count": len(removed), "marker": MARKER_NAME}, 0


def emit(report, out_path, lines) -> None:
    for line in lines:
        print(line)
    if out_path:
        Path(out_path).write_text(json.dumps(report, indent=2, ensure_ascii=False) + chr(10), encoding="utf-8")
        print("report written to " + str(out_path))


def legacy_main(argv) -> int:
    parser = argparse.ArgumentParser(description="Generate the governance tree of a governed repository from the GovCheck package (empty targets only).")
    parser.add_argument("target", type=Path, help="target repository root (created if missing)")
    args = parser.parse_args(argv)
    target = args.target.resolve()
    if target.exists() and any(target.iterdir()):
        print("Target " + str(target) + " is not empty; refusing to overwrite.")
        print("Use the inspect, plan and apply subcommands to adopt GovCheck in an existing repository.")
        return 1
    target.mkdir(parents=True, exist_ok=True)
    for rel in selected_files(list(DEFAULT_CAPABILITIES)):
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PACKAGE_ROOT / rel, dst)
    print("Governance tree generated in " + str(target))
    return 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in SUBCOMMANDS:
        return legacy_main(argv)
    command = argv[0]
    parser = argparse.ArgumentParser(prog="python3 bootstrap.py " + command)
    parser.add_argument("target", type=Path, help="target repository root")
    if command in ("plan", "apply"):
        parser.add_argument("--capabilities", default=None, help="comma-separated subset of: " + ", ".join(DEFAULT_CAPABILITIES))
    if command == "apply":
        parser.add_argument("--plan", default=None, help="plan JSON produced by the plan subcommand; apply aborts if stale")
    parser.add_argument("--out", default=None, help="write the JSON report here")
    args = parser.parse_args(argv[1:])
    target = args.target.resolve()
    caps = parse_capabilities(getattr(args, "capabilities", None))
    if command == "inspect":
        report = inspect_target(target)
        lines = [
            "inspect " + str(target),
            "  package " + report["package_version"] + " digest " + report["package_digest"][:12] + " (" + str(report["package_file_count"]) + " files)",
            "  target exists=" + str(report["exists"]) + " empty=" + str(report["empty"]) + " git=" + str(report["is_git_repo"]),
            "  present: " + (", ".join(report["present_top_level"]) or "-"),
            "  conflicts: " + (", ".join(report["conflicts"]) or "none"),
            "  marker: " + ("present" if report["marker"] else "none"),
        ]
        emit(report, args.out, lines)
        return 0
    if command == "plan":
        report = build_plan(target, caps)
        s = report["summary"]
        lines = [
            "plan " + str(target) + " (package " + report["package_version"] + ", digest " + report["package_digest"][:12] + ")",
            "  create=" + str(s.get("create", 0)) + " identical=" + str(s.get("identical", 0)) + " conflict=" + str(s.get("conflict", 0)),
        ]
        emit(report, args.out, lines)
        return 0
    if command == "apply":
        report, code = apply_plan(target, caps, plan_path=getattr(args, "plan", None))
        if code != 0:
            print("apply aborted: " + str(report.get("error")))
            return code
        lines = [
            "apply " + str(target) + " (package " + report["package_version"] + ", digest " + report["package_digest"][:12] + ")",
            "  created=" + str(report["created_count"]) + " already_present=" + str(report["already_present"]) + " conflicts_preserved=" + str(len(report["conflicts_preserved"])),
            "  marker written: " + report["marker"],
        ]
        for c in report["conflicts_preserved"]:
            lines.append("    conflict preserved: " + c)
        emit(report, args.out, lines)
        return 0
    report, code = rollback_target(target)
    if code != 0:
        print("rollback failed: " + str(report.get("error")))
        return code
    emit(report, args.out, ["rollback " + str(target) + ": removed " + str(report["removed_count"]) + " installed file(s)"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
