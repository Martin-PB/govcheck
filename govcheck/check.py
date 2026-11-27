#!/usr/bin/env python3
"""First executable GovCheck slice: deterministic rule evaluation on a repository tree.

Usage:
  python3 govcheck/check.py [--tree PATH] [--out REPORT.json] [--list-rules]
  python3 govcheck/check.py --tree PATH --base REV --candidate REV

Each rule returns pass, fail or unknown. The overall result is fail if any rule
fails, otherwise unknown if any rule is unknown, otherwise pass (fail-closed:
unknown is never a success). The exit code is 0 only when the overall result is
pass.

The JSON report is language-independent (stable rule ids and result codes); the
stdout text is a human-readable projection. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

TOOL = "govcheck"
VERSION = "0.4.0-slice"

ANCHOR_RE = re.compile(r'<a id="r-(\d{2,3})"></a>', re.I)
MENTION_RE = re.compile(r"\bR-(\d{2,3})\b")
REF_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]*references(?:\.fr)?\.md#r-(\d{2,3})[^)]*)\)", re.I)

LICENSE_NAMES = ("LICENSE", "LICENSE.md", "LICENCE", "LICENCE.md")
CATALOGUES = ("docs/references.md", "docs/references.fr.md")
ATTESTATION_DIR = "docs/attestations"
DECISIONS_DIR = "docs/decisions"
GUIDE_BASENAMES = ("README", "TEMPLATE")
MARKER_NAME = ".govcheck-bootstrap.json"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

REFERENCES_HEADING_RE = re.compile(
    r"^##[ \t]+(?:\d+(?:\.\d+)*[.)]?[ \t]+)?"
    r"(References|Bibliographic references|R\u00e9f\u00e9rences|R\u00e9f\u00e9rences bibliographiques)[ \t]*$",
    re.I | re.M,
)
SOURCE_LINK_RE = re.compile(
    r"\[[^\]]*\]\(([^)]*(?:references(?:\.fr)?\.md#r-\d{2,3}|https?://)[^)]*)\)",
    re.I,
)


class Ctx:
    def __init__(self, tree: Path, changed, git=None, independent_review=None):
        self.tree = tree
        self.changed = changed
        self.git = git or {}
        self.independent_review = independent_review or {}

    def read(self, rel: str) -> str:
        return (self.tree / rel).read_text(encoding="utf-8")


def rule_license(ctx: Ctx):
    found = [n for n in LICENSE_NAMES if (ctx.tree / n).is_file()]
    if found:
        return ("pass", True, ["license file present at the root: " + found[0]])
    return ("fail", True, ["no LICENSE/LICENCE file at the repository root"])


def rule_bilingual_decisions(ctx: Ctx):
    d = ctx.tree / "docs" / "decisions"
    if not d.is_dir():
        return ("pass", False, ["no docs/decisions directory; rule not applicable"])
    problems = []
    for p in sorted(d.iterdir()):
        if p.suffix != ".md" or not p.is_file():
            continue
        if p.name.endswith(".fr.md"):
            twin = p.with_name(p.name[:-6] + ".md")
        else:
            twin = p.with_name(p.name[:-3] + ".fr.md")
        if not twin.is_file():
            problems.append(p.name + " has no bilingual twin " + twin.name)
    if problems:
        return ("fail", True, problems)
    return ("pass", True, ["every decision document has an EN/FR twin"])


def rule_manifest_pairs(ctx: Ctx):
    m = ctx.tree / "docs" / "template-manifest.json"
    if not m.is_file():
        return ("fail", True, ["missing docs/template-manifest.json; the package/meta pairs are not declared"])
    try:
        manifest = json.loads(m.read_text(encoding="utf-8"))
    except ValueError as e:
        return ("fail", True, ["docs/template-manifest.json is not valid JSON: " + str(e)])
    problems = []
    for key in sorted(manifest.get("pairs", {})):
        if not (ctx.tree / key).is_file():
            problems.append("manifest pair missing at the meta level: " + key)
        pkg = ctx.tree / "govcheck" / key
        if not pkg.is_file():
            problems.append("manifest pair missing in the govcheck/ package: " + key)
    if problems:
        return ("fail", True, problems)
    return ("pass", True, ["every manifest-declared pair exists at both levels"])


def rule_reference_integrity(ctx: Ctx):
    docs = ctx.tree / "docs"
    if not docs.is_dir():
        return ("pass", False, ["no docs/ directory; rule not applicable"])
    cat_ids = {}
    for rel in CATALOGUES:
        p = ctx.tree / rel
        if not p.is_file():
            return ("fail", True, ["missing reference catalogue: " + rel])
        cat_ids[rel] = {"R-" + n for n in ANCHOR_RE.findall(ctx.read(rel))}
    problems = []
    en_ids = cat_ids[CATALOGUES[0]]
    fr_ids = cat_ids[CATALOGUES[1]]
    if en_ids != fr_ids:
        problems.append("EN/FR catalogue id sets differ: only-EN=" + str(sorted(en_ids - fr_ids)) + " only-FR=" + str(sorted(fr_ids - en_ids)))
    ids = en_ids | fr_ids
    for p in sorted(docs.rglob("*.md")):
        rel = p.relative_to(ctx.tree).as_posix()
        if rel in CATALOGUES:
            continue
        text = p.read_text(encoding="utf-8")
        for n in sorted(set(MENTION_RE.findall(text))):
            rid = "R-" + n
            if rid not in ids:
                problems.append(rel + ": mentions " + rid + " without a catalogue entry")
        for mm in REF_LINK_RE.finditer(text):
            rid = "R-" + mm.group(2)
            if rid not in ids:
                problems.append(rel + ": links to missing catalogue entry " + rid)
    if problems:
        return ("fail", True, problems)
    return ("pass", True, ["all R-xx mentions and links resolve to catalogue entries, EN/FR id sets equal"])


def rule_tla_freshness(ctx: Ctx):
    if ctx.changed is not None:
        applies = any(c.startswith("formal/tla/") for c in ctx.changed)
    else:
        applies = (ctx.tree / "formal" / "tla").is_dir()
    if not applies:
        return ("pass", False, ["no formal/tla/ changes; rule not applicable"])
    return ("unknown", True, ["changes under formal/tla/ require fresh TLC evidence bound to the candidate revision; not verifiable offline"])


def load_attestations(ctx: Ctx):
    """Recorded human attestations in docs/attestations/*.json.

    A record is valid for a candidate revision when it carries that exact
    revision in candidate_rev and a reviewer identity distinct from the
    candidate author.
    """
    d = ctx.tree / ATTESTATION_DIR
    if not d.is_dir():
        return []
    records = []
    for p in sorted(d.glob("*.json")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(rec, dict):
            rec["_file"] = p.name
            records.append(rec)
    return records



def _is_guide_file(name: str) -> bool:
    base = name[:-6] if name.endswith(".fr.md") else name[:-3]
    return base.upper().startswith(GUIDE_BASENAMES)


def rule_sources_present(ctx: Ctx):
    """Decisions and attestations must carry their sources.

    Every non-guide docs/decisions/*.md must contain a References/R\u00e9f\u00e9rences
    heading followed, before the next heading, by at least one source link
    (a reference-catalogue anchor or an external URL). Every attestation
    record must carry a non-empty "sources" list of strings.
    """
    problems = []
    checked = 0
    d = ctx.tree / DECISIONS_DIR
    if d.is_dir():
        for p in sorted(d.iterdir()):
            if p.suffix != ".md" or not p.is_file() or _is_guide_file(p.name):
                continue
            checked += 1
            text = p.read_text(encoding="utf-8")
            m = REFERENCES_HEADING_RE.search(text)
            if not m:
                problems.append(p.name + ": no References/R\u00e9f\u00e9rences section heading")
                continue
            section = text[m.end():]
            nxt = re.search(r"^##[ \t]", section, re.M)
            if nxt:
                section = section[: nxt.start()]
            if not SOURCE_LINK_RE.search(section):
                problems.append(p.name + ": the references section contains no source link (catalogue anchor or external URL)")
    att_checked = 0
    for rec in load_attestations(ctx):
        att_checked += 1
        srcs = rec.get("sources")
        if not isinstance(srcs, list) or not srcs or not all(isinstance(s, str) and s.strip() for s in srcs):
            problems.append(str(rec.get("_file", "attestation")) + ': attestation record has no non-empty "sources" list')
    if checked == 0 and att_checked == 0:
        return ("pass", False, ["no decision documents and no attestation records; rule not applicable"])
    if problems:
        return ("fail", True, problems)
    return ("pass", True, [str(checked) + " decision document(s) and " + str(att_checked) + " attestation record(s) each carry sources"])


def _safe_rel(path: str) -> bool:
    if not path or path.startswith("/") or chr(92) in path:
        return False
    return all(p not in ("", ".", "..") for p in path.split("/"))


def rule_bootstrap_integrity(ctx: Ctx):
    """Installed package files must still match the bootstrap marker digests.

    When the tree root carries the package-owned marker .govcheck-bootstrap.json
    (written by govcheck/bootstrap.py apply), the marker must be valid JSON with
    the expected schema, and every installed file must exist with the recorded
    SHA-256 digest. Without the marker the rule is not applicable.
    """
    mp = ctx.tree / MARKER_NAME
    if not mp.is_file():
        return ("pass", False, ["no " + MARKER_NAME + " at the tree root; rule not applicable"])
    try:
        marker = json.loads(mp.read_text(encoding="utf-8"))
    except ValueError as e:
        return ("fail", True, [MARKER_NAME + " is not valid JSON: " + str(e)])
    if not isinstance(marker, dict):
        return ("fail", True, [MARKER_NAME + " must be a JSON object"])
    problems = []
    if marker.get("tool") != "govcheck-bootstrap":
        problems.append(MARKER_NAME + ': unexpected "tool" value ' + repr(marker.get("tool")))
    pv = marker.get("package_version")
    if not isinstance(pv, str) or not pv.strip():
        problems.append(MARKER_NAME + ': missing non-empty "package_version"')
    pd = marker.get("package_digest")
    if not isinstance(pd, str) or not HEX64_RE.match(pd):
        problems.append(MARKER_NAME + ': "package_digest" must be a 64-char lowercase hex SHA-256')
    installed = marker.get("installed")
    if not isinstance(installed, list):
        problems.append(MARKER_NAME + ': "installed" must be a list of {path, sha256} entries')
        installed = []
    checked = 0
    for entry in installed:
        if not isinstance(entry, dict):
            problems.append(MARKER_NAME + ": installed entry is not an object")
            continue
        rel = entry.get("path")
        sha = entry.get("sha256")
        if not isinstance(rel, str) or not _safe_rel(rel):
            problems.append(MARKER_NAME + ": unsafe installed path " + repr(rel))
            continue
        if not isinstance(sha, str) or not HEX64_RE.match(sha):
            problems.append(rel + ": installed entry has no valid sha256 digest")
            continue
        checked += 1
        f = ctx.tree / rel
        if not f.is_file():
            problems.append(rel + ": file recorded in the marker is missing")
        elif hashlib.sha256(f.read_bytes()).hexdigest() != sha:
            problems.append(rel + ": content drifted from the digest recorded in the marker")
    conflicts = marker.get("conflicts", [])
    if not isinstance(conflicts, list) or not all(isinstance(c, str) and c for c in conflicts):
        problems.append(MARKER_NAME + ': "conflicts" must be a list of non-empty strings')
    if problems:
        return ("fail", True, problems)
    return ("pass", True, [str(checked) + " installed file(s) match the recorded digests of package " + str(pv)])


def candidate_content_digest(tree: Path) -> str:
    """Hash a deterministic snapshot of candidate files, excluding VCS metadata."""
    digest = hashlib.sha256()
    root = tree.resolve()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root)
        if ".git" in rel.parts or path.is_dir():
            continue
        name = rel.as_posix().encode("utf-8")
        if path.is_symlink():
            payload = b"symlink:" + os.readlink(path).encode("utf-8")
        elif path.is_file():
            payload = path.read_bytes()
        else:
            continue
        digest.update(len(name).to_bytes(8, "big"))
        digest.update(name)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def _outside_tree(value, tree: Path, label: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = path.absolute()
    root = tree.resolve()
    resolved = path.resolve()
    for candidate in (path, resolved):
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        raise ValueError(label + " must be stored outside the candidate tree")
    if not resolved.is_file():
        raise ValueError(label + " must be a readable regular file")
    return resolved


def rule_independent_review(ctx: Ctx):
    if ctx.changed is None or not ctx.changed:
        return ("pass", False, ["no candidate diff supplied; rule not applicable"])

    in_tree_records = load_attestations(ctx)
    if in_tree_records:
        return ("unknown", True, [
            str(len(in_tree_records)) + " candidate-tree attestation record(s) found; in-tree reviewer strings "
            "cannot authenticate independent review or DSSE signer identity and cannot bind the final candidate revision"
        ])

    config = ctx.independent_review
    if ctx.git.get("worktree_clean") is not True:
        return ("unknown", True, ["candidate checkout is not proven clean; snapshot digest cannot be safely bound to the named revision"])
    if ctx.git.get("head_rev") != ctx.git.get("candidate_rev"):
        return ("fail", True, ["checked-out HEAD does not equal the candidate revision being evaluated"])
    required = {
        "envelope_path", "assurance_envelope_path", "assurance_role",
        "author_identity_envelope_path", "author_identity_role",
        "trust_policy_path", "trust_policy_sha256", "author_principal_source",
        "governance_revision", "scope_id",
    }
    if not config or not required.issubset(config):
        return ("unknown", True, [
            "detached review evidence, pinned trust policy, trusted author principal/source, governance revision "
            "and scope must all be explicitly supplied"
        ])

    source = config["author_principal_source"]
    parsed_source = urlparse(source) if isinstance(source, str) else None
    if not parsed_source or not parsed_source.scheme or (parsed_source.scheme in {"http", "https"} and not parsed_source.netloc):
        return ("fail", True, ["author principal source must be an absolute URI"])

    try:
        envelope_path = _outside_tree(config["envelope_path"], ctx.tree, "review envelope")
        assurance_path = _outside_tree(config["assurance_envelope_path"], ctx.tree, "assurance envelope")
        author_identity_path = _outside_tree(config["author_identity_envelope_path"], ctx.tree, "author identity envelope")
        policy_path = _outside_tree(config["trust_policy_path"], ctx.tree, "trust policy")
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        assurance_envelope = json.loads(assurance_path.read_text(encoding="utf-8"))
        author_identity_envelope = json.loads(author_identity_path.read_text(encoding="utf-8"))
        review_envelope_digest = hashlib.sha256(envelope_path.read_bytes()).hexdigest()
        content_digest = candidate_content_digest(ctx.tree)
        candidate_revision = ctx.git.get("candidate_rev")
        base_revision = ctx.git.get("base_rev")
        if not candidate_revision or not base_revision:
            return ("unknown", True, ["full candidate and base revisions are required to bind detached evidence"])
        try:
            from govcheck.attestation_verify import verify_dsse_envelope
        except ImportError:
            from attestation_verify import verify_dsse_envelope
        author_result = verify_dsse_envelope(
            author_identity_envelope,
            policy_path,
            config["trust_policy_sha256"],
            ctx.tree,
            required_role=config["author_identity_role"],
            expected_candidate_revision=candidate_revision,
            expected_governance_revision=config["governance_revision"],
            expected_scope_id=config["scope_id"],
            expected_base_revision=base_revision,
            expected_content_sha256=content_digest,
            expected_predicate_type="urn:govcheck:attestation:forge-author-identity:v1",
        )
        if author_result.get("status") == "unknown":
            return ("unknown", True, ["forge author identity trust could not be established: " + str(author_result.get("reason", "unknown"))])
        if author_result.get("status") != "verified":
            return ("fail", True, ["forge author identity attestation verification failed: " + str(author_result.get("reason", "invalid"))])
        author_identity = author_result.get("statement", {}).get("predicate", {})
        author_principal = author_identity.get("authorPrincipal")
        if not author_principal:
            return ("fail", True, ["verified forge identity Statement has no author principal"])
        if author_identity.get("sourceUri") != config["author_principal_source"]:
            return ("fail", True, ["forge author identity source URI does not match the explicitly trusted source"])
        if config.get("author_principal") and config["author_principal"] != author_principal:
            return ("fail", True, ["forge author identity principal does not match the optional expected principal"])
        result = verify_dsse_envelope(
            envelope,
            policy_path,
            config["trust_policy_sha256"],
            ctx.tree,
            required_role="independent-reviewer",
            expected_candidate_revision=candidate_revision,
            expected_governance_revision=config["governance_revision"],
            expected_scope_id=config["scope_id"],
            expected_base_revision=base_revision,
            expected_content_sha256=content_digest,
            expected_predicate_type="urn:govcheck:attestation:independent-review:v1",
            forbidden_principal=author_principal,
        )
        assurance_result = verify_dsse_envelope(
            assurance_envelope,
            policy_path,
            config["trust_policy_sha256"],
            ctx.tree,
            required_role=config["assurance_role"],
            expected_candidate_revision=candidate_revision,
            expected_governance_revision=config["governance_revision"],
            expected_scope_id=config["scope_id"],
            expected_base_revision=base_revision,
            expected_content_sha256=content_digest,
            expected_predicate_type="urn:govcheck:attestation:assurance-evaluation:v1",
        )
    except (OSError, ValueError, TypeError) as exc:
        return ("fail", True, ["cannot load or validate detached independent-review evidence: " + str(exc)])

    if result.get("status") == "unknown":
        return ("unknown", True, ["detached reviewer trust could not be established: " + str(result.get("reason", "unknown"))])
    if result.get("status") != "verified":
        return ("fail", True, ["detached independent-review verification failed: " + str(result.get("reason", "invalid"))])
    if assurance_result.get("status") == "unknown":
        return ("unknown", True, ["assurance Statement trust could not be established: " + str(assurance_result.get("reason", "unknown"))])
    if assurance_result.get("status") != "verified":
        return ("fail", True, ["detached assurance Statement verification failed: " + str(assurance_result.get("reason", "invalid"))])
    assurance_predicate = assurance_result.get("statement", {}).get("predicate", {})
    review_reference = assurance_predicate.get("independentReview", {})
    if review_reference.get("status") != "attested":
        return ("fail", True, ["verified assurance Statement does not declare independentReview.status=attested"])
    reference = review_reference.get("reference", {})
    referenced_digest = reference.get("digest", {}).get("sha256")
    if referenced_digest != review_envelope_digest:
        return ("fail", True, ["assurance detached-review reference digest does not match the exact review envelope bytes"])
    predicate = result.get("statement", {}).get("predicate", {})
    if predicate.get("outcome") == "changes_requested":
        return ("fail", True, ["authenticated independent reviewer requested changes"])
    if predicate.get("outcome") != "accepted":
        return ("fail", True, ["verified review has an unsupported outcome"])
    return ("pass", True, [
        "detached independent-review and assurance DSSE statements verified; assurance reference digest matches the exact review envelope; "
        "reviewer differs from the author principal in the signed forge identity assertion; candidate/base/governance/scope/content bindings match"
    ])


RULES = [
    {"id": "license-present", "class": "decidable", "fn": rule_license},
    {"id": "bilingual-decisions", "class": "decidable", "fn": rule_bilingual_decisions},
    {"id": "manifest-pairs", "class": "decidable", "fn": rule_manifest_pairs},
    {"id": "reference-integrity", "class": "decidable", "fn": rule_reference_integrity},
    {"id": "sources-present", "class": "decidable", "fn": rule_sources_present},
    {"id": "bootstrap-integrity", "class": "decidable", "fn": rule_bootstrap_integrity},
    {"id": "tla-evidence-freshness", "class": "not-verifiable-offline", "fn": rule_tla_freshness},
    {"id": "independent-review", "class": "attested", "fn": rule_independent_review},
]


def evaluate(tree: Path, changed=None, git=None, independent_review=None) -> dict:
    ctx = Ctx(tree, changed, git, independent_review)
    rules = []
    for r in RULES:
        result, applies, reasons = r["fn"](ctx)
        rules.append({"id": r["id"], "class": r["class"], "result": result, "applies": applies, "reasons": reasons})
    if any(x["result"] == "fail" for x in rules):
        overall = "fail"
    elif any(x["result"] == "unknown" for x in rules):
        overall = "unknown"
    else:
        overall = "pass"
    return {
        "tool": TOOL,
        "version": VERSION,
        "candidate": {"tree": str(tree), "changed_files": sorted(changed) if changed is not None else None},
        "overall": overall,
        "rules": rules,
    }


def git_changed(tree: Path, base: str, candidate: str):
    proc = subprocess.run(
        ["git", "-C", str(tree), "diff", "--name-only", base + "..." + candidate],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit("git diff failed: " + proc.stderr.strip())
    return set(proc.stdout.split())


def git_author(tree: Path, rev: str):
    proc = subprocess.run(
        ["git", "-C", str(tree), "log", "-1", "--format=%an <%ae>", rev],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit("git log failed: " + proc.stderr.strip())
    return proc.stdout.strip()


def git_full_sha(tree: Path, rev: str):
    proc = subprocess.run(
        ["git", "-C", str(tree), "rev-parse", rev],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit("git rev-parse failed: " + proc.stderr.strip())
    return proc.stdout.strip()


def git_worktree_clean(tree: Path) -> bool:
    """Return true only for a clean tracked and untracked candidate checkout."""
    proc = subprocess.run(
        ["git", "-C", str(tree), "status", "--porcelain", "--untracked-files=all"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit("git status failed: " + proc.stderr.strip())
    return not proc.stdout.strip()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="First executable GovCheck slice.")
    parser.add_argument("--tree", default=".")
    parser.add_argument("--base")
    parser.add_argument("--candidate")
    parser.add_argument("--ref", help="target ref being evaluated, e.g. refs/heads/main")
    parser.add_argument("--out")
    parser.add_argument("--review-envelope")
    parser.add_argument("--assurance-envelope")
    parser.add_argument("--assurance-role", help="Trust-policy role required for the detached assurance Statement")
    parser.add_argument("--author-identity-envelope")
    parser.add_argument("--author-identity-role", help="Trust-policy role required for the signed forge author-identity assertion")
    parser.add_argument("--trust-policy")
    parser.add_argument("--trust-policy-sha256")
    parser.add_argument("--author-principal")
    parser.add_argument("--author-principal-source")
    parser.add_argument("--governance-revision")
    parser.add_argument("--scope-id")
    parser.add_argument("--list-rules", action="store_true")
    args = parser.parse_args(argv)
    if args.list_rules:
        for r in RULES:
            print(r["id"] + " (" + r["class"] + ")")
        return 0
    if (args.base is None) != (args.candidate is None):
        print("error: --base and --candidate must be used together", file=sys.stderr)
        return 2
    tree = Path(args.tree).resolve()
    changed = git_changed(tree, args.base, args.candidate) if args.base else None
    git = None
    if args.base:
        git = {
            "base": args.base,
            "base_rev": git_full_sha(tree, args.base),
            "candidate_rev": git_full_sha(tree, args.candidate),
            "head_rev": git_full_sha(tree, "HEAD"),
            "worktree_clean": git_worktree_clean(tree),
            "ref": args.ref,
            "governance_revision": args.governance_revision,
            "scope_id": args.scope_id,
            "content_sha256": candidate_content_digest(tree),
            "author": git_author(tree, args.candidate),
        }
    review_values = [
        args.review_envelope, args.assurance_envelope, args.assurance_role,
        args.author_identity_envelope, args.author_identity_role,
        args.trust_policy, args.trust_policy_sha256, args.author_principal_source,
    ]
    review = None
    if any(review_values):
        if not all(review_values) or not args.governance_revision or not args.scope_id:
            parser.error("detached review verification requires all review evidence/trust inputs plus --governance-revision and --scope-id")
        review = {
            "envelope_path": args.review_envelope,
            "assurance_envelope_path": args.assurance_envelope,
            "assurance_role": args.assurance_role,
            "author_identity_envelope_path": args.author_identity_envelope,
            "author_identity_role": args.author_identity_role,
            "trust_policy_path": args.trust_policy,
            "trust_policy_sha256": args.trust_policy_sha256,
            "author_principal": args.author_principal,
            "author_principal_source": args.author_principal_source,
            "governance_revision": args.governance_revision,
            "scope_id": args.scope_id,
        }
    report = evaluate(tree, changed, git, review)
    if git:
        report["candidate"]["base"] = git["base"]
        report["candidate"]["candidate_rev"] = git["candidate_rev"]
        report["candidate"]["base_revision"] = git["base_rev"]
        report["candidate"]["content_sha256"] = git["content_sha256"]
        report["candidate"]["ref"] = git["ref"]
        report["candidate"]["governance_revision"] = git["governance_revision"]
        report["candidate"]["scope_id"] = git["scope_id"]
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print("govcheck " + VERSION + " -- overall: " + report["overall"].upper())
    for x in report["rules"]:
        line = "  [" + x["result"].upper() + "] " + x["id"] + " (" + x["class"] + ")"
        if not x["applies"]:
            line += " [not applicable]"
        print(line)
        for reason in x["reasons"]:
            print("      - " + reason)
    if args.out:
        print("report written to " + args.out)
    return 0 if report["overall"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
