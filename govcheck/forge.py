#!/usr/bin/env python3
"""Forge-native adapter for GovCheck (Architecture 0034).

Two roles:
  1. registry mirror: project the repository-canonical work portfolio
     (docs/work-portfolio/, Architecture 0030) onto forge coordination
     objects (issues, pull requests, labels, comments);
  2. forge-side verification: read CI check runs and branch protection so a
     report can state whether a candidate revision is covered by shared,
     not-locally-falsifiable verifications (CI, protected branches, required
     checks).

The forge verifies, it never authorizes: a green check is evidence, not
authority (Specification 0004). The govcheck check path stays offline,
read-only and token-free and never imports this module.

Standard library only. GitHub REST v3 is the first backend; the contract is
forge-neutral so other forges can be added behind the same functions.

Usage:
  python3 govcheck/forge.py list-issues [--state open] [--labels a,b]
  python3 govcheck/forge.py get-issue --number N
  python3 govcheck/forge.py list-labels
  python3 govcheck/forge.py check-runs --ref REF
  python3 govcheck/forge.py branch-protection [--branch main]
  python3 govcheck/forge.py create-issue --title T [--body B] [--labels a,b] [--registry-id govcheck.work.slug]
  python3 govcheck/forge.py update-issue --number N [--title T] [--body B] [--state open|closed] [--labels a,b]
  python3 govcheck/forge.py comment --number N --body B
  python3 govcheck/forge.py capabilities

Configuration comes from the environment only:
  GOVCHECK_FORGE          forge type (default "github")
  GOVCHECK_FORGE_OWNER    repository owner
  GOVCHECK_FORGE_REPO     repository name
  GOVCHECK_FORGE_TOKEN    API token (fallback: GITHUB_TOKEN)
Tokens are never written to disk, logs or reports; error messages are
expurged and never carry the token.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

TOOL = "govcheck-forge"
VERSION = "0.1.0-slice"

SUPPORTED_FORGES = ("github",)
DEFAULT_API_BASE = "https://api.github.com"
MAX_PAGES = 50

REGISTRY_ID_RE = re.compile(r"govcheck\.work\.([a-z0-9][a-z0-9-]*)")

# Failure taxonomy of Specification 0004. A partial failure is never reported
# as an atomic success.
KINDS = ("not-found", "unsupported", "unavailable", "stale", "conflict", "auth", "malformed")

CAPABILITY_DECLARATION = {
    "adapter": "govcheck/forge.py",
    "version": VERSION,
    "forges": list(SUPPORTED_FORGES),
    "read": ["list_issues", "get_issue", "list_labels"],
    "write": ["create_issue", "update_issue", "add_comment"],
    "verify": ["list_check_runs", "get_branch_protection"],
    "never": [
        "mutate the forge from govcheck check",
        "persist a token on disk, in logs or in reports",
        "treat a green check as an authorization",
    ],
}


class ForgeError(Exception):
    """Typed failure per Specification 0004; the message never carries a token."""

    def __init__(self, kind: str, message: str):
        if kind not in KINDS:
            raise ValueError("unknown forge error kind: " + repr(kind))
        super().__init__(message)
        self.kind = kind


def declare_capabilities() -> dict:
    return json.loads(json.dumps(CAPABILITY_DECLARATION))


def resolve_token(env=None):
    """Token from the environment only: GOVCHECK_FORGE_TOKEN, then GITHUB_TOKEN."""
    env = os.environ if env is None else env
    for name in ("GOVCHECK_FORGE_TOKEN", "GITHUB_TOKEN"):
        value = env.get(name)
        if value and value.strip():
            return value.strip()
    return None


def _http_error(status, body) -> ForgeError:
    snippet = ""
    if body:
        try:
            snippet = str(json.loads(body.decode("utf-8")).get("message", ""))[:200]
        except Exception:
            snippet = body[:200].decode("utf-8", "replace")
    if status in (401, 403):
        return ForgeError("auth", "HTTP " + str(status) + " from the forge: authentication or authorization failed; check GOVCHECK_FORGE_TOKEN/GITHUB_TOKEN")
    if status == 404:
        return ForgeError("not-found", "HTTP 404 from the forge: " + snippet)
    if status == 409:
        return ForgeError("stale", "HTTP 409 from the forge (stale state): " + snippet)
    if status == 422:
        return ForgeError("conflict", "HTTP 422 from the forge (validation conflict): " + snippet)
    if status == 429 or status >= 500:
        return ForgeError("unavailable", "HTTP " + str(status) + " from the forge (rate limit or outage): " + snippet)
    return ForgeError("malformed", "HTTP " + str(status) + " from the forge: " + snippet)


class GitHubClient:
    """Minimal GitHub REST v3 client. The transport is injectable for tests."""

    def __init__(self, owner, repo, token=None, opener=None, api_base=DEFAULT_API_BASE):
        if not owner or not repo:
            raise ForgeError("malformed", "owner and repo must be non-empty strings")
        self.owner = owner
        self.repo = repo
        self.token = token
        self.api_base = api_base.rstrip("/")
        self._opener = opener or urllib.request.urlopen

    def require_token(self) -> None:
        if not self.token:
            raise ForgeError("auth", "no token available: set GOVCHECK_FORGE_TOKEN or GITHUB_TOKEN; writes require a token")

    def repo_path(self, suffix: str) -> str:
        return "/repos/" + urllib.parse.quote(self.owner, safe="") + "/" + urllib.parse.quote(self.repo, safe="") + suffix

    def _request(self, method: str, path: str, payload=None, query=None):
        url = path if path.startswith("http") else self.api_base + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": TOOL + "/" + VERSION,
        }
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            resp = self._opener(req)
        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()
            except Exception:
                pass
            raise _http_error(e.code, body) from None
        except urllib.error.URLError as e:
            raise ForgeError("unavailable", "network error contacting the forge: " + str(e.reason)) from None
        status = getattr(resp, "status", 200)
        raw = resp.read()
        if status >= 400:
            raise _http_error(status, raw)
        try:
            parsed = json.loads(raw.decode("utf-8")) if raw else {}
        except (ValueError, UnicodeDecodeError):
            raise ForgeError("malformed", "response from the forge is not valid JSON") from None
        return parsed, getattr(resp, "headers", {})


def _next_link(headers):
    link = headers.get("Link") if headers is not None else None
    if not link:
        return None
    for part in link.split(","):
        seg = part.strip()
        if seg.endswith('rel="next"'):
            m = re.search(r"<([^>]+)>", seg)
            if m:
                return m.group(1)
    return None


def _paginate(client: GitHubClient, path: str, query: dict) -> list:
    out = []
    q = dict(query)
    for _ in range(MAX_PAGES):
        parsed, headers = client._request("GET", path, query=q)
        if not isinstance(parsed, list):
            raise ForgeError("malformed", "expected a JSON list from the forge")
        out.extend(parsed)
        nxt = _next_link(headers)
        if not nxt:
            return out
        u = urllib.parse.urlparse(nxt)
        path = u.path
        q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
    raise ForgeError("unavailable", "pagination exceeded " + str(MAX_PAGES) + " pages")


# --- registry mirror mapping (Architecture 0030: registry ids are canonical) ---

def registry_id_from_text(text):
    m = REGISTRY_ID_RE.search(text or "")
    return "govcheck.work." + m.group(1) if m else None


def issue_body(registry_id, body: str) -> str:
    if registry_id:
        return "Registry ID: " + registry_id + "\n\n" + (body or "")
    return body or ""


def issue_record(d: dict) -> dict:
    labels = sorted(l.get("name", "") for l in d.get("labels", []) if isinstance(l, dict) and l.get("name"))
    body = d.get("body") or ""
    return {
        "number": d.get("number"),
        "title": d.get("title", ""),
        "state": d.get("state", ""),
        "labels": labels,
        "registry_id": registry_id_from_text(body),
        "url": d.get("html_url", ""),
        "body": body,
    }


# --- adapter contract (module-level, client first, plain dicts out) ---

def list_issues(client: GitHubClient, state: str = "open", labels=None) -> list:
    query = {"state": state, "per_page": 100}
    if labels:
        query["labels"] = ",".join(labels)
    items = _paginate(client, client.repo_path("/issues"), query)
    return [issue_record(d) for d in items if isinstance(d, dict) and "pull_request" not in d]


def get_issue(client: GitHubClient, number: int) -> dict:
    parsed, _ = client._request("GET", client.repo_path("/issues/" + str(int(number))))
    if not isinstance(parsed, dict):
        raise ForgeError("malformed", "expected a JSON object for issue " + str(number))
    return issue_record(parsed)


def create_issue(client: GitHubClient, title: str, body: str = "", labels=None, registry_id=None) -> dict:
    client.require_token()
    payload = {"title": title, "body": issue_body(registry_id, body), "labels": list(labels or [])}
    parsed, _ = client._request("POST", client.repo_path("/issues"), payload=payload)
    return issue_record(parsed)


def update_issue(client: GitHubClient, number: int, title=None, body=None, state=None, labels=None) -> dict:
    client.require_token()
    payload = {}
    if title is not None:
        payload["title"] = title
    if body is not None:
        payload["body"] = body
    if state is not None:
        payload["state"] = state
    if labels is not None:
        payload["labels"] = list(labels)
    if not payload:
        raise ForgeError("malformed", "update_issue: no field to update for issue " + str(number))
    parsed, _ = client._request("PATCH", client.repo_path("/issues/" + str(int(number))), payload=payload)
    return issue_record(parsed)


def list_labels(client: GitHubClient) -> list:
    items = _paginate(client, client.repo_path("/labels"), {"per_page": 100})
    return sorted(l.get("name", "") for l in items if isinstance(l, dict) and l.get("name"))


def add_comment(client: GitHubClient, number: int, body: str) -> dict:
    client.require_token()
    parsed, _ = client._request("POST", client.repo_path("/issues/" + str(int(number)) + "/comments"), payload={"body": body})
    return {"id": parsed.get("id"), "url": parsed.get("html_url", ""), "body": parsed.get("body", "")}


# --- forge-side verification (read-only; the forge verifies, never authorizes) ---

def list_check_runs(client: GitHubClient, ref: str) -> list:
    parsed, _ = client._request("GET", client.repo_path("/commits/" + urllib.parse.quote(ref, safe="") + "/check-runs"), query={"per_page": 100})
    runs = parsed.get("check_runs", []) if isinstance(parsed, dict) else []
    return [
        {"name": r.get("name", ""), "status": r.get("status", ""), "conclusion": r.get("conclusion"), "url": r.get("html_url", "")}
        for r in runs
        if isinstance(r, dict)
    ]


def get_branch_protection(client: GitHubClient, branch: str = "main") -> dict:
    parsed, _ = client._request("GET", client.repo_path("/branches/" + urllib.parse.quote(branch, safe="") + "/protection"))
    if not isinstance(parsed, dict):
        raise ForgeError("malformed", "expected a JSON object for branch protection")
    required = parsed.get("required_status_checks") or {}
    reviews = parsed.get("required_pull_request_reviews") or {}
    return {
        "branch": branch,
        "required_checks": sorted(required.get("contexts", []) or []),
        "enforce_admins": bool((parsed.get("enforce_admins") or {}).get("enabled")),
        "required_approving_reviews": reviews.get("required_approving_review_count", 0),
    }


def make_client(forge=None, owner=None, repo=None, token=None, opener=None, env=None):
    env = os.environ if env is None else env
    forge = (forge or env.get("GOVCHECK_FORGE") or "github").strip().lower()
    owner = owner or env.get("GOVCHECK_FORGE_OWNER")
    repo = repo or env.get("GOVCHECK_FORGE_REPO")
    if forge not in SUPPORTED_FORGES:
        raise ForgeError("unsupported", "forge type " + repr(forge) + " is not supported; supported: " + ", ".join(SUPPORTED_FORGES))
    if not owner or not repo:
        raise ForgeError("malformed", "owner/repo required: pass --owner/--repo or set GOVCHECK_FORGE_OWNER/GOVCHECK_FORGE_REPO")
    if token is None:
        token = resolve_token(env)
    if forge == "github":
        return GitHubClient(owner, repo, token=token, opener=opener)
    raise ForgeError("unsupported", "forge type " + repr(forge) + " has no backend yet")


def _split_labels(text):
    if not text:
        return None
    return [p.strip() for p in text.split(",") if p.strip()]


def main(argv=None, opener=None, env=None) -> int:
    env = os.environ if env is None else env
    parser = argparse.ArgumentParser(
        prog="python3 govcheck/forge.py",
        description="Forge-native adapter (Architecture 0034): registry mirror and forge-side verification. Reads work without a token on public repositories; writes require a token from the environment. JSON on stdout; the forge verifies, it never authorizes.",
    )
    parser.add_argument("--forge", default=None, help="forge type (default: env GOVCHECK_FORGE or github)")
    parser.add_argument("--owner", default=None, help="repository owner (default: env GOVCHECK_FORGE_OWNER)")
    parser.add_argument("--repo", default=None, help="repository name (default: env GOVCHECK_FORGE_REPO)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list-issues")
    p.add_argument("--state", default="open")
    p.add_argument("--labels", default=None)
    p = sub.add_parser("get-issue")
    p.add_argument("--number", type=int, required=True)
    sub.add_parser("list-labels")
    p = sub.add_parser("check-runs")
    p.add_argument("--ref", required=True)
    p = sub.add_parser("branch-protection")
    p.add_argument("--branch", default="main")
    p = sub.add_parser("create-issue")
    p.add_argument("--title", required=True)
    p.add_argument("--body", default="")
    p.add_argument("--labels", default=None)
    p.add_argument("--registry-id", default=None)
    p = sub.add_parser("update-issue")
    p.add_argument("--number", type=int, required=True)
    p.add_argument("--title", default=None)
    p.add_argument("--body", default=None)
    p.add_argument("--state", default=None, choices=["open", "closed"])
    p.add_argument("--labels", default=None)
    p = sub.add_parser("comment")
    p.add_argument("--number", type=int, required=True)
    p.add_argument("--body", required=True)
    sub.add_parser("capabilities")

    args = parser.parse_args(argv)
    try:
        client = make_client(args.forge, args.owner, args.repo, opener=opener, env=env)
        if args.command == "capabilities":
            result = declare_capabilities()
        elif args.command == "list-issues":
            result = list_issues(client, state=args.state, labels=_split_labels(args.labels))
        elif args.command == "get-issue":
            result = get_issue(client, args.number)
        elif args.command == "list-labels":
            result = list_labels(client)
        elif args.command == "check-runs":
            result = list_check_runs(client, args.ref)
        elif args.command == "branch-protection":
            result = get_branch_protection(client, args.branch)
        elif args.command == "create-issue":
            result = create_issue(client, args.title, args.body, labels=_split_labels(args.labels), registry_id=args.registry_id)
        elif args.command == "update-issue":
            result = update_issue(client, args.number, title=args.title, body=args.body, state=args.state, labels=_split_labels(args.labels))
        elif args.command == "comment":
            result = add_comment(client, args.number, args.body)
        else:
            raise ForgeError("unsupported", "unknown command " + repr(args.command))
    except ForgeError as e:
        print("forge error [" + e.kind + "]: " + str(e), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
