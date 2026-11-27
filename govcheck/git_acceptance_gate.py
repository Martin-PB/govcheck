"""Pinned local Git acceptance gate adapter.

The executable is installed outside the candidate repository and invoked by
scripts/govcheck-git-pre-receive. It evaluates a detached candidate checkout,
verifies a DSSE governance decision, and emits the hook's v0 decision protocol.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from govcheck import check as check_module
    from govcheck import acceptance_decision
except ImportError:  # standalone GovCheck installation
    import check as check_module
    import acceptance_decision

OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
V0_SCHEMA = "govcheck.acceptance-decision/v0"


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _base_envelope(args, env: dict[str, str]) -> dict:
    return {
        "schema": V0_SCHEMA,
        "repository_id": args.repository_id,
        "vcs_kind": args.vcs_kind,
        "base": args.base,
        "candidate": args.candidate,
        "ref": args.ref,
        "policy_revision": env.get("GOVCHECK_EXPECTED_POLICY_REVISION", ""),
        "policy_digest": env.get("GOVCHECK_EXPECTED_POLICY_DIGEST", ""),
        "decision_id": "unavailable",
        "evidence_digest": "sha256:" + _sha256(b""),
        "verifier": {
            "identity": env.get("GOVCHECK_EXPECTED_VERIFIER_IDENTITY", ""),
            "digest": env.get("GOVCHECK_EXPECTED_VERIFIER_DIGEST", ""),
        },
        "result": "unknown",
        "risk_acceptance": None,
        "reason": "acceptance decision is unavailable",
    }


def _config_error(args, env: dict[str, str]) -> str | None:
    if args.vcs_kind != "git":
        return "unsupported VCS kind"
    if not OID_RE.fullmatch(args.base) or not OID_RE.fullmatch(args.candidate):
        return "base and candidate must be full Git object IDs"
    if not args.ref.startswith("refs/"):
        return "ref must be a fully qualified refs/... name"
    expected_repo = env.get("GOVCHECK_EXPECTED_REPOSITORY_ID", "")
    if not expected_repo or args.repository_id != expected_repo:
        return "repository ID does not match the pinned repository"
    required = [
        "GOVCHECK_TRUST_POLICY_PATH", "GOVCHECK_TRUST_POLICY_SHA256",
        "GOVCHECK_GOVERNANCE_REVISION", "GOVCHECK_SCOPE_ID",
        "GOVCHECK_ACCEPTANCE_DECISION_ENVELOPE",
        "GOVCHECK_EXPECTED_POLICY_REVISION", "GOVCHECK_EXPECTED_POLICY_DIGEST",
        "GOVCHECK_EXPECTED_VERIFIER_IDENTITY", "GOVCHECK_EXPECTED_VERIFIER_DIGEST",
    ]
    missing = [key for key in required if not env.get(key, "").strip()]
    if missing:
        return "missing trusted gate configuration: " + ", ".join(missing)
    if not HEX64_RE.fullmatch(env["GOVCHECK_TRUST_POLICY_SHA256"]):
        return "GOVCHECK_TRUST_POLICY_SHA256 must be lowercase SHA-256"
    if not DIGEST_RE.fullmatch(env["GOVCHECK_EXPECTED_POLICY_DIGEST"]):
        return "pinned policy digest must use sha256:<hex>"
    if not DIGEST_RE.fullmatch(env["GOVCHECK_EXPECTED_VERIFIER_DIGEST"]):
        return "pinned verifier digest must use sha256:<hex>"
    policy_path = Path(env["GOVCHECK_TRUST_POLICY_PATH"]).expanduser().resolve()
    git_dir = Path(args.git_dir or env.get("GIT_DIR", "")).expanduser().resolve()
    try:
        policy_path.relative_to(git_dir)
    except ValueError:
        pass
    else:
        return "trust policy must be installed outside the candidate repository"
    try:
        policy_bytes = policy_path.read_bytes()
        policy = json.loads(policy_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return "cannot read pinned trust policy: " + str(exc)
    actual_policy_digest = _sha256(policy_bytes)
    if actual_policy_digest != env["GOVCHECK_TRUST_POLICY_SHA256"]:
        return "trust policy bytes do not match GOVCHECK_TRUST_POLICY_SHA256"
    if not isinstance(policy, dict) or policy.get("revision") != env["GOVCHECK_EXPECTED_POLICY_REVISION"]:
        return "trust policy revision does not match the pre-receive policy pin"
    if env["GOVCHECK_EXPECTED_POLICY_DIGEST"] != "sha256:" + actual_policy_digest:
        return "trust policy digest does not match the pre-receive policy pin"
    if not env.get("GIT_DIR") and not args.git_dir:
        return "GIT_DIR or --git-dir is required for pre-receive evaluation"
    return None


def _run(command, runner, env, timeout):
    return runner(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )


def _outside_candidate(path_value: str, candidate_root: Path, label: str) -> Path:
    path = Path(path_value).expanduser().resolve()
    root = candidate_root.resolve()
    try:
        path.relative_to(root)
    except ValueError:
        pass
    else:
        raise ValueError(label + " must be outside the candidate tree")
    if not path.is_file():
        raise ValueError(label + " is not a readable regular file")
    return path


def _review_config(env: dict[str, str]) -> dict | None:
    keys = {
        "envelope_path": "GOVCHECK_REVIEW_ENVELOPE_PATH",
        "assurance_envelope_path": "GOVCHECK_ASSURANCE_ENVELOPE_PATH",
        "assurance_role": "GOVCHECK_ASSURANCE_ROLE",
        "author_identity_envelope_path": "GOVCHECK_AUTHOR_IDENTITY_ENVELOPE_PATH",
        "author_identity_role": "GOVCHECK_AUTHOR_IDENTITY_ROLE",
        "trust_policy_path": "GOVCHECK_TRUST_POLICY_PATH",
        "trust_policy_sha256": "GOVCHECK_TRUST_POLICY_SHA256",
        "author_principal_source": "GOVCHECK_AUTHOR_PRINCIPAL_SOURCE",
        "governance_revision": "GOVCHECK_GOVERNANCE_REVISION",
        "scope_id": "GOVCHECK_SCOPE_ID",
    }
    if not all(env.get(value, "").strip() for value in keys.values()):
        return None
    return {key: env[value] for key, value in keys.items()}


def _risk_v0(decision: dict) -> dict | None:
    risk = decision.get("riskAcceptance")
    if decision.get("result") != "accepted-with-risk" or not isinstance(risk, dict):
        return None
    return {
        "id": risk.get("id", ""),
        "authority": decision.get("authorityPrincipal", ""),
        "reason": risk.get("reason", ""),
        "scope": risk.get("scope", ""),
        "expires_at": risk.get("expiresAt", ""),
        "residual_risk": risk.get("residualRisk", ""),
        "affected_claims": risk.get("affectedClaims", []),
        "authorization_digest": "sha256:" + risk.get("authorizationDigest", ""),
    }


def run_gate(args, env=None, runner=subprocess.run, evaluator=None, decision_verifier=None) -> tuple[int, dict]:
    env = dict(os.environ if env is None else env)
    payload = _base_envelope(args, env)
    error = _config_error(args, env)
    if error:
        payload["reason"] = error
        return 0, payload

    git_dir = args.git_dir or env.get("GIT_DIR")
    try:
        timeout = int(env.get("GOVCHECK_GATE_TIMEOUT_SECONDS", "300"))
        if timeout <= 0:
            raise ValueError("timeout must be positive")
    except ValueError as exc:
        payload["reason"] = "invalid gate timeout: " + str(exc)
        return 0, payload
    git_env = dict(env)
    git_env.pop("GIT_DIR", None)
    git_env.pop("GIT_WORK_TREE", None)
    git_env.pop("GIT_COMMON_DIR", None)

    try:
        with tempfile.TemporaryDirectory(prefix="govcheck-gate-") as directory:
            temp_root = Path(directory)
            candidate_root = temp_root / "candidate"
            cloned = _run(
                ["git", "clone", "--shared", "--no-checkout", str(Path(git_dir).resolve()), str(candidate_root)],
                runner, git_env, timeout,
            )
            if cloned.returncode != 0:
                payload["reason"] = "candidate repository clone failed"
                return 0, payload
            checked = _run(
                ["git", "-C", str(candidate_root), "checkout", "--detach", args.candidate],
                runner, git_env, timeout,
            )
            if checked.returncode != 0:
                payload["reason"] = "candidate checkout failed"
                return 0, payload

            base_revision = check_module.git_full_sha(candidate_root, args.base)
            candidate_revision = check_module.git_full_sha(candidate_root, args.candidate)
            content_digest = check_module.candidate_content_digest(candidate_root)
            changed = check_module.git_changed(candidate_root, args.base, args.candidate)
            git = {
                "base": args.base,
                "base_rev": base_revision,
                "candidate_rev": candidate_revision,
                "head_rev": check_module.git_full_sha(candidate_root, "HEAD"),
                "worktree_clean": check_module.git_worktree_clean(candidate_root),
                "ref": args.ref,
                "governance_revision": env["GOVCHECK_GOVERNANCE_REVISION"],
                "scope_id": env["GOVCHECK_SCOPE_ID"],
                "content_sha256": content_digest,
            }
            review = _review_config(env)
            evaluator = evaluator or check_module.evaluate
            report = evaluator(candidate_root, changed, git, review)
            report["candidate"].update({
                "base": args.base,
                "candidate_rev": candidate_revision,
                "base_revision": base_revision,
                "content_sha256": content_digest,
                "ref": args.ref,
                "governance_revision": env["GOVCHECK_GOVERNANCE_REVISION"],
                "scope_id": env["GOVCHECK_SCOPE_ID"],
            })
            report_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
            report_path = temp_root / "evaluation-report.json"
            report_path.write_bytes(report_bytes)

            decision_path = _outside_candidate(
                env["GOVCHECK_ACCEPTANCE_DECISION_ENVELOPE"], candidate_root, "acceptance decision envelope"
            )
            decision_envelope = json.loads(decision_path.read_text(encoding="utf-8"))
            decision_verifier = decision_verifier or acceptance_decision.verify_and_evaluate
            decision = decision_verifier(
                decision_envelope,
                env["GOVCHECK_TRUST_POLICY_PATH"],
                env["GOVCHECK_TRUST_POLICY_SHA256"],
                candidate_root,
                report=report,
                report_bytes=report_bytes,
                expected_repository_id=args.repository_id,
                expected_candidate_revision=candidate_revision,
                expected_candidate_content_sha256=content_digest,
                expected_base_revision=base_revision,
                expected_ref=args.ref,
                expected_governance_revision=env["GOVCHECK_GOVERNANCE_REVISION"],
                expected_scope_id=env["GOVCHECK_SCOPE_ID"],
                required_role="governance-authority",
            )
            payload["decision_id"] = decision.get("decisionId") or "unavailable"
            payload["evidence_digest"] = "sha256:" + _sha256(report_bytes)
            payload["result"] = decision.get("result", "unknown")
            payload["risk_acceptance"] = _risk_v0(decision)
            payload["reason"] = decision.get("reason", "decision verification returned no reason")
            return 0, payload
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired) as exc:
        payload["reason"] = "gate evaluation failed: " + str(exc)
        return 0, payload


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Trusted local Git acceptance gate for GovCheck pre-receive.")
    parser.add_argument("--repository-id", required=True)
    parser.add_argument("--vcs-kind", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--git-dir")
    args = parser.parse_args(argv)
    code, payload = run_gate(args)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
