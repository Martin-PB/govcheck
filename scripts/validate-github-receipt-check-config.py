#!/usr/bin/env python3
"""Preflight the public repository configuration for GovCheck's GitHub receipt check."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

POLICY_ID = "urn:govcheck:trust-policy:v1"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class ConfigError(Exception):
    pass


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError("duplicate trust-policy JSON key: " + key)
        result[key] = value
    return result


def _required(env: dict[str, str], key: str) -> str:
    value = env.get(key, "").strip()
    if not value:
        raise ConfigError("required repository variable is missing: " + key)
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha_digest(value: str, label: str) -> None:
    if not SHA256_RE.fullmatch(value):
        raise ConfigError(label + " must be 64 lowercase hexadecimal characters")


def _prefixed_digest(value: str, label: str) -> None:
    if not DIGEST_RE.fullmatch(value):
        raise ConfigError(label + " must use sha256:<64 lowercase hex>")


def validate_config(repository_root: str | Path, env: dict[str, str]) -> dict:
    root = Path(repository_root).expanduser().resolve()
    if not root.is_dir():
        raise ConfigError("repository root is not a directory")
    required = (
        "GOVCHECK_TRUST_POLICY_PATH",
        "GOVCHECK_TRUST_POLICY_SHA256",
        "GOVCHECK_JOURNAL_SCOPE_ID",
        "GOVCHECK_REPOSITORY_URI",
        "GOVCHECK_GOVERNANCE_REVISION",
        "GOVCHECK_GOVERNANCE_DIGEST",
        "GOVCHECK_EXPECTED_REPOSITORY_ID",
        "GOVCHECK_EXPECTED_POLICY_DIGEST",
    )
    values = {key: _required(env, key) for key in required}
    _sha_digest(values["GOVCHECK_TRUST_POLICY_SHA256"], "GOVCHECK_TRUST_POLICY_SHA256")
    _prefixed_digest(values["GOVCHECK_GOVERNANCE_DIGEST"], "GOVCHECK_GOVERNANCE_DIGEST")
    _prefixed_digest(values["GOVCHECK_EXPECTED_POLICY_DIGEST"], "GOVCHECK_EXPECTED_POLICY_DIGEST")
    parsed_uri = urlparse(values["GOVCHECK_REPOSITORY_URI"])
    if not parsed_uri.scheme or not parsed_uri.netloc:
        raise ConfigError("GOVCHECK_REPOSITORY_URI must be an absolute URI")
    if not values["GOVCHECK_JOURNAL_SCOPE_ID"] or not values["GOVCHECK_GOVERNANCE_REVISION"]:
        raise ConfigError("journal scope and governance revision must be non-empty")

    policy_path = (root / values["GOVCHECK_TRUST_POLICY_PATH"]).resolve()
    try:
        policy_path.relative_to(root)
    except ValueError as exc:
        raise ConfigError("trust-policy path must remain inside the trusted repository checkout") from exc
    if not policy_path.is_file():
        raise ConfigError("trusted policy file does not exist: " + str(policy_path))
    actual_policy_digest = _digest(policy_path)
    if actual_policy_digest != values["GOVCHECK_TRUST_POLICY_SHA256"]:
        raise ConfigError("trust-policy file digest does not match GOVCHECK_TRUST_POLICY_SHA256")
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                            parse_constant=lambda value: (_ for _ in ()).throw(ConfigError("invalid JSON constant " + value)))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ConfigError("cannot parse strict trust policy: " + str(exc)) from exc
    if not isinstance(policy, dict) or policy.get("schemaVersion") != "1" or policy.get("policyId") != POLICY_ID:
        raise ConfigError("trust policy must use schemaVersion 1 and the GovCheck trust-policy ID")
    if not isinstance(policy.get("revision"), str) or not policy["revision"].strip():
        raise ConfigError("trust policy revision is missing")

    openssl = policy.get("openssl")
    if not isinstance(openssl, dict):
        raise ConfigError("trust policy OpenSSL pin is missing")
    raw_openssl_path = Path(str(openssl.get("path", ""))).expanduser()
    if not raw_openssl_path.is_absolute():
        raise ConfigError("pinned OpenSSL path must be absolute")
    openssl_path = raw_openssl_path.resolve()
    if not openssl_path.is_file() or not os.access(openssl_path, os.X_OK):
        raise ConfigError("pinned OpenSSL path must be an executable")
    try:
        openssl_path.relative_to(root)
    except ValueError:
        pass
    else:
        raise ConfigError("pinned OpenSSL executable must be outside the repository checkout")
    _sha_digest(str(openssl.get("sha256", "")), "trust-policy OpenSSL sha256")
    if _digest(openssl_path) != openssl["sha256"]:
        raise ConfigError("pinned OpenSSL executable digest does not match the trust policy")

    required_role = env.get("GOVCHECK_REQUIRED_ROLE", "governance-authority").strip() or "governance-authority"
    keys = policy.get("keys")
    if not isinstance(keys, list) or not keys:
        raise ConfigError("trust policy must contain at least one configured public key")
    key_ids = set()
    eligible = 0
    for key in keys:
        if not isinstance(key, dict):
            raise ConfigError("trust policy key entries must be objects")
        key_id = key.get("keyId")
        if not isinstance(key_id, str) or not key_id or key_id in key_ids:
            raise ConfigError("trust-policy key IDs must be non-empty and unique")
        key_ids.add(key_id)
        if key.get("algorithm") != "ed25519":
            raise ConfigError("GitHub receipt check currently requires Ed25519 trust keys")
        public_path = Path(str(key.get("publicKeyPath", ""))).expanduser()
        if not public_path.is_absolute():
            public_path = (policy_path.parent / public_path).resolve()
        if not public_path.is_file():
            raise ConfigError("trust-policy public key file is missing: " + str(public_path))
        _sha_digest(str(key.get("publicKeySha256", "")), "publicKeySha256 for " + key_id)
        if _digest(public_path) != key["publicKeySha256"]:
            raise ConfigError("public key digest mismatch for " + key_id)
        roles = key.get("roles")
        if key.get("revoked") is not True and isinstance(roles, list) and required_role in roles:
            eligible += 1
    if eligible == 0:
        raise ConfigError("no non-revoked Ed25519 key has the required role: " + required_role)

    return {
        "status": "ready",
        "trustPolicyRevision": policy["revision"],
        "trustPolicySha256": actual_policy_digest,
        "requiredRole": required_role,
        "activeKeyCount": eligible,
        "repositoryUri": values["GOVCHECK_REPOSITORY_URI"],
        "scopeId": values["GOVCHECK_JOURNAL_SCOPE_ID"],
        "governanceRevision": values["GOVCHECK_GOVERNANCE_REVISION"],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        result = validate_config(args.repository_root, dict(os.environ))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, ConfigError, ValueError, KeyError) as exc:
        print("GovCheck receipt-check configuration is not ready: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
