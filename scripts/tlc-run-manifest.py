#!/usr/bin/env python3
"""Create and verify a run-scoped manifest for TLA+ model-checking reports.

This is an unsigned integrity/freshness record, not an authenticated attestation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


class ManifestError(ValueError):
    pass


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def safe_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ManifestError(f"path escapes repository: {relative}")
    return candidate


def blob_id(root: Path, relative: str) -> str:
    safe_path(root, relative)
    try:
        return git(root, "rev-parse", f"HEAD:{relative}")
    except subprocess.CalledProcessError as exc:
        raise ManifestError(f"tracked source is absent at HEAD: {relative}") from exc


def report_record(root: Path, relative: str) -> dict[str, Any]:
    path = safe_path(root, relative)
    if not path.is_file():
        return {"path": relative, "present": False, "sha256": None, "bytes": None}
    data = path.read_bytes()
    return {
        "path": relative, "present": True,
        "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
    }


def caller_workflow_path(workflow_ref: str) -> str | None:
    match = re.search(r"(\.github/workflows/[^@]+)@", workflow_ref)
    return match.group(1) if match else None


def build_manifest(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    model_path = f"formal/tla/{args.model}.tla"
    config_path = f"formal/tla/{args.config}"
    reusable_path = ".github/workflows/tla-model-reusable.yml"
    workflow_ref = args.workflow_ref or ""
    sources = {
        "model": {"path": model_path, "gitBlob": blob_id(root, model_path)},
        "configuration": {"path": config_path, "gitBlob": blob_id(root, config_path)},
        "reusableWorkflow": {"path": reusable_path, "gitBlob": blob_id(root, reusable_path)},
        "formalTlaTree": {"path": "formal/tla", "gitBlob": blob_id(root, "formal/tla")},
    }
    caller_path = caller_workflow_path(workflow_ref)
    if caller_path and safe_path(root, caller_path).is_file():
        sources["callerWorkflow"] = {
            "path": caller_path, "gitBlob": blob_id(root, caller_path)
        }
    event = {}
    if args.event_path and Path(args.event_path).is_file():
        try:
            payload = json.loads(Path(args.event_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ManifestError(f"cannot parse GitHub event payload: {exc}") from exc
        pr = payload.get("pull_request") or {}
        event = {
            "pullRequestHeadSha": (pr.get("head") or {}).get("sha"),
            "pullRequestBaseSha": (pr.get("base") or {}).get("sha"),
        }
    reports = [
        report_record(root, f"sany-{args.model}.txt"),
        report_record(root, f"tlc-{args.model}-{Path(args.config).stem}.txt"),
        report_record(root, "tla2tools.sha256"),
    ]
    return {
        "format": "govcheck.tlc-run-manifest/v1",
        "trust": "unsigned-integrity-record-not-an-authenticated-attestation",
        "run": {
            "id": args.run_id or None, "attempt": args.run_attempt or None,
            "eventName": args.event_name or None, "workflowRef": workflow_ref or None,
            "workflowSha": args.workflow_sha or None,
            "checkoutCommit": git(root, "rev-parse", "HEAD"), **event,
        },
        "invocation": {
            "model": args.model, "configuration": args.config, "workers": 4,
            "javaVersion": args.java_version or None, "tlcToolVersion": "1.7.4",
            "tlcToolSha256": "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88",
            "sanyOutcome": args.sany_outcome, "tlcOutcome": args.tlc_outcome,
        },
        "sources": sources, "reports": reports,
    }


def verify_manifest(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("format") != "govcheck.tlc-run-manifest/v1":
        return ["unsupported manifest format"]
    try:
        actual_commit = git(root, "rev-parse", "HEAD")
    except (OSError, subprocess.CalledProcessError) as exc:
        return [f"cannot resolve checkout commit: {exc}"]
    if (manifest.get("run") or {}).get("checkoutCommit") != actual_commit:
        errors.append("checkout commit differs from manifest")
    sources = manifest.get("sources") or {}
    for key in ("model", "configuration", "reusableWorkflow", "formalTlaTree", "callerWorkflow"):
        record = sources.get(key)
        if key == "callerWorkflow" and record is None:
            continue
        if not record or not record.get("path"):
            errors.append(f"missing source path: {key}")
            continue
        try:
            actual_blob = blob_id(root, record["path"])
        except (ManifestError, OSError):
            errors.append(f"source is missing or untracked: {key}")
            continue
        if record.get("gitBlob") != actual_blob:
            errors.append(f"source blob differs from manifest: {key}")
    for record in manifest.get("reports") or []:
        relative = record.get("path")
        if not relative:
            errors.append("report record has no path")
            continue
        try:
            path = safe_path(root, relative)
        except ManifestError:
            errors.append(f"report path escapes repository: {relative}")
            continue
        present = path.is_file()
        if record.get("present") is not present:
            errors.append(f"report presence differs from manifest: {relative}")
        elif present:
            data = path.read_bytes()
            if record.get("sha256") != hashlib.sha256(data).hexdigest() or record.get("bytes") != len(data):
                errors.append(f"report digest or size differs from manifest: {relative}")
    return errors


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path.cwd())
    p.add_argument("--output", type=Path)
    p.add_argument("--verify", type=Path)
    p.add_argument("--model")
    p.add_argument("--config")
    p.add_argument("--run-id", default=os.getenv("GITHUB_RUN_ID"))
    p.add_argument("--run-attempt", default=os.getenv("GITHUB_RUN_ATTEMPT"))
    p.add_argument("--event-name", default=os.getenv("GITHUB_EVENT_NAME"))
    p.add_argument("--workflow-ref", default=os.getenv("GITHUB_WORKFLOW_REF"))
    p.add_argument("--workflow-sha", default=os.getenv("GITHUB_WORKFLOW_SHA"))
    p.add_argument("--event-path", default=os.getenv("GITHUB_EVENT_PATH"))
    p.add_argument("--java-version", default=os.getenv("JAVA_VERSION"))
    p.add_argument("--sany-outcome", default=os.getenv("SANY_OUTCOME", "unknown"))
    p.add_argument("--tlc-outcome", default=os.getenv("TLC_OUTCOME", "unknown"))
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.verify:
            manifest = json.loads(args.verify.read_text(encoding="utf-8"))
            errors = verify_manifest(root, manifest)
            print(json.dumps({"status": "invalid" if errors else "valid", "errors": errors}, indent=2))
            return 1 if errors else 0
        if not args.model or not args.config:
            raise ManifestError("--model and --config are required when creating a manifest")
        manifest = build_manifest(root, args)
        rendered = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0
    except (ManifestError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"TLC manifest error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
