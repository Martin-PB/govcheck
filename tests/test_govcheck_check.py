#!/usr/bin/env python3
"""Tests for the first GovCheck executable slice (govcheck/check.py)."""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from pathlib import Path

from govcheck import attestation as attestation
from govcheck import forge_author_identity
from govcheck import independent_review

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("govcheck_check", ROOT / "govcheck" / "check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

FIXTURE_SPEC = importlib.util.spec_from_file_location("attestation_fixture", ROOT / "tests" / "test_attestation.py")
FIXTURE = importlib.util.module_from_spec(FIXTURE_SPEC)
FIXTURE_SPEC.loader.exec_module(FIXTURE)


def build_tree(root: Path) -> None:
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
    dec = root / "docs" / "decisions"
    dec.mkdir(parents=True)
    (dec / "README.md").write_text("# Decisions\n", encoding="utf-8")
    (dec / "README.fr.md").write_text("# D\u00e9cisions\n", encoding="utf-8")
    (dec / "0001-a.md").write_text("# A\n\n## References\n\n- [R-01](../references.md#r-01)\n", encoding="utf-8")
    (dec / "0001-a.fr.md").write_text("# A\n\n## R\u00e9f\u00e9rences\n\n- [R-01](../references.fr.md#r-01)\n", encoding="utf-8")
    specs = root / "docs" / "specifications"
    specs.mkdir(parents=True)
    (specs / "0001-a.md").write_text("# Spec\n\nSee [R-01](../references.md#r-01).\n", encoding="utf-8")
    pkg = root / "govcheck" / "docs" / "specifications"
    pkg.mkdir(parents=True)
    (pkg / "0001-a.md").write_text("# Spec\n", encoding="utf-8")
    (root / "docs" / "template-manifest.json").write_text(
        json.dumps({"pairs": {"docs/specifications/0001-a.md": {}}}), encoding="utf-8"
    )
    for name in ("references.md", "references.fr.md"):
        (root / "docs" / name).write_text(
            '# Catalogue\n\n<a id="r-01"></a>\n### R-01 \u2014 Example\n\n- **Source:** https://example.org\n',
            encoding="utf-8",
        )


def add_attestation(root: Path, reviewer="Bob <bob@example.org>", rev="deadbeef" * 5, decision="accept") -> None:
    d = root / "docs" / "attestations"
    d.mkdir(parents=True, exist_ok=True)
    (d / "0001.json").write_text(json.dumps({
        "decision": decision,
        "candidate_rev": rev,
        "reviewer": reviewer,
        "date": "2026-11-09",
        "sources": ["https://example.org/review-notes"],
    }), encoding="utf-8")


class EvaluateTests(unittest.TestCase):
    def run_cli(self, root, extra=None):
        buf = io.StringIO()
        argv = ["--tree", str(root)] + (extra or [])
        with redirect_stdout(buf):
            code = check.main(argv)
        return code, buf.getvalue()

    def test_passing_tree_exits_zero(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "pass")
            code, out = self.run_cli(root)
            self.assertEqual(code, 0)
            self.assertIn("PASS", out)

    def test_missing_license_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "LICENSE").unlink()
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "license-present")
            self.assertEqual(rule["result"], "fail")
            code, _ = self.run_cli(root)
            self.assertEqual(code, 1)

    def test_missing_fr_twin_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "docs" / "decisions" / "0001-a.fr.md").unlink()
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "bilingual-decisions")
            self.assertEqual(rule["result"], "fail")

    def test_unknown_reference_mention_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            p = root / "docs" / "specifications" / "0001-a.md"
            p.write_text(p.read_text(encoding="utf-8") + "Also R-99.\n", encoding="utf-8")
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "reference-integrity")
            self.assertEqual(rule["result"], "fail")

    def test_manifest_pair_missing_in_package_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "govcheck" / "docs" / "specifications" / "0001-a.md").unlink()
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "manifest-pairs")
            self.assertEqual(rule["result"], "fail")

    def test_tla_presence_is_unknown_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            tla = root / "formal" / "tla"
            tla.mkdir(parents=True)
            (tla / "Spec.tla").write_text("---- MODULE Spec ----\n", encoding="utf-8")
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "unknown")
            code, out = self.run_cli(root)
            self.assertEqual(code, 1)
            self.assertIn("UNKNOWN", out)

    def test_out_writes_json_report(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            out = root / "report.json"
            code, _ = self.run_cli(root, ["--out", str(out)])
            self.assertEqual(code, 0)
            report = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(report["tool"], "govcheck")
            self.assertEqual(report["overall"], "pass")
            self.assertEqual(len(report["rules"]), 8)

    def _detached_review_inputs(self, root, outcome="accepted"):
        evidence = root.parent / "detached-review.json"
        assurance = root.parent / "detached-assurance.json"
        author_identity = root.parent / "forge-author-identity.json"
        policy = root.parent / "trust-policy.json"
        evidence.write_text(json.dumps({"payloadType": "application/vnd.in-toto+json", "payload": "e30=", "signatures": [{"keyid": "test", "sig": "AA=="}]}), encoding="utf-8")
        assurance.write_text(json.dumps({"payloadType": "application/vnd.in-toto+json", "payload": "e30=", "signatures": [{"keyid": "test", "sig": "AA=="}]}), encoding="utf-8")
        author_identity.write_text(json.dumps({"payloadType": "application/vnd.in-toto+json", "payload": "e30=", "signatures": [{"keyid": "test", "sig": "AA=="}]}), encoding="utf-8")
        policy.write_text("{}", encoding="utf-8")
        config = {
            "envelope_path": str(evidence),
            "assurance_envelope_path": str(assurance),
            "assurance_role": "assurance-evaluator",
            "author_identity_envelope_path": str(author_identity),
            "author_identity_role": "forge-authority",
            "trust_policy_path": str(policy),
            "trust_policy_sha256": "0" * 64,
            "author_principal": "forge:author-1",
            "author_principal_source": "https://forge.example/api/author/1",
            "governance_revision": "gov-17",
            "scope_id": "repo:example/project",
        }
        git = {"candidate_rev": "c" * 40, "base_rev": "b" * 40, "head_rev": "c" * 40, "worktree_clean": True}
        author_result = {"status": "verified", "statement": {"predicate": {"authorPrincipal": "forge:author-1", "sourceUri": "https://forge.example/api/author/1"}}}
        result = {
            "status": "verified",
            "statement": {"predicate": {"outcome": outcome}},
        }
        assurance_result = {
            "status": "verified",
            "statement": {"predicate": {"independentReview": {
                "status": "attested",
                "reference": {"digest": {"sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()}},
            }}},
        }
        return config, git, [author_result, result, assurance_result]

    def test_detached_review_config_can_satisfy_rule_when_verifier_confirms(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "candidate"
            root.mkdir()
            build_tree(root)
            config, git, verified = self._detached_review_inputs(root)
            with patch("govcheck.attestation_verify.verify_dsse_envelope", side_effect=verified) as verifier:
                report = check.evaluate(root, changed={"docs/a.md"}, git=git, independent_review=config)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "pass")
            self.assertEqual(verifier.call_args_list[0].kwargs["required_role"], "forge-authority")
            self.assertEqual(verifier.call_args_list[1].kwargs["required_role"], "independent-reviewer")
            self.assertEqual(verifier.call_args_list[2].kwargs["required_role"], "assurance-evaluator")
            self.assertEqual(verifier.call_args_list[1].kwargs["expected_content_sha256"], check.candidate_content_digest(root))
            self.assertEqual(verifier.call_args_list[1].kwargs["forbidden_principal"], "forge:author-1")
            self.assertEqual(verifier.call_count, 3)

    def test_signed_forge_author_source_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "candidate"
            root.mkdir()
            build_tree(root)
            config, git, results = self._detached_review_inputs(root)
            config["author_principal_source"] = "https://untrusted.example/author"
            with patch("govcheck.attestation_verify.verify_dsse_envelope", side_effect=results):
                report = check.evaluate(root, changed={"docs/a.md"}, git=git, independent_review=config)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "fail")
            self.assertIn("source URI", rule["reasons"][0])

    def test_detached_review_changes_requested_fails_rule(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "candidate"
            root.mkdir()
            build_tree(root)
            config, git, verified = self._detached_review_inputs(root, outcome="changes_requested")
            with patch("govcheck.attestation_verify.verify_dsse_envelope", side_effect=verified):
                report = check.evaluate(root, changed={"docs/a.md"}, git=git, independent_review=config)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "fail")
            self.assertIn("requested changes", rule["reasons"][0])

    def test_detached_review_evidence_inside_candidate_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "candidate"
            root.mkdir()
            build_tree(root)
            evidence = root / "review.json"
            evidence.write_text("{}", encoding="utf-8")
            policy = Path(d) / "policy.json"
            assurance = Path(d) / "assurance.json"
            author_identity = Path(d) / "author-identity.json"
            policy.write_text("{}", encoding="utf-8")
            assurance.write_text("{}", encoding="utf-8")
            author_identity.write_text("{}", encoding="utf-8")
            config = {
                "envelope_path": str(evidence),
                "assurance_envelope_path": str(assurance),
                "assurance_role": "assurance-evaluator",
                "author_identity_envelope_path": str(author_identity),
                "author_identity_role": "forge-authority",
                "trust_policy_path": str(policy),
                "trust_policy_sha256": "0" * 64,
                "author_principal": "forge:author-1",
                "author_principal_source": "https://forge.example/api/author/1",
                "governance_revision": "gov-17",
                "scope_id": "repo:example/project",
            }
            git = {"candidate_rev": "c" * 40, "base_rev": "b" * 40, "head_rev": "c" * 40, "worktree_clean": True}
            report = check.evaluate(root, changed={"docs/a.md"}, git=git, independent_review=config)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "fail")
            self.assertIn("outside the candidate tree", rule["reasons"][0])

    @unittest.skipUnless(shutil.which("openssl"), "OpenSSL CLI is required for end-to-end detached attestation tests")
    def test_end_to_end_detached_review_assurance_and_forge_identity(self):
        with tempfile.TemporaryDirectory() as d:
            parent = Path(d)
            root = parent / "candidate"
            root.mkdir()
            build_tree(root)
            openssl = Path(shutil.which("openssl")).resolve()
            forge_private, forge_public = parent / "forge-private.pem", parent / "forge-public.pem"
            reviewer_private, reviewer_public = parent / "reviewer-private.pem", parent / "reviewer-public.pem"
            for private, public in ((forge_private, forge_public), (reviewer_private, reviewer_public)):
                subprocess.run(["openssl", "genpkey", "-algorithm", "ED25519", "-out", str(private)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(["openssl", "pkey", "-in", str(private), "-pubout", "-out", str(public)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            def file_digest(path):
                return hashlib.sha256(Path(path).read_bytes()).hexdigest()

            def sign(statement, private_key, key_id):
                payload = attestation.canonical_statement_bytes(statement)
                pae = attestation.dsse_pae(attestation.DSSE_PAYLOAD_TYPE, payload)
                pae_path, signature_path = parent / "pae.bin", parent / "signature.bin"
                pae_path.write_bytes(pae)
                subprocess.run(["openssl", "pkeyutl", "-sign", "-inkey", str(private_key), "-rawin", "-in", str(pae_path), "-out", str(signature_path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return attestation.build_dsse_envelope(statement, [{"keyid": key_id, "sig": base64.b64encode(signature_path.read_bytes()).decode("ascii")}])

            candidate_rev, base_rev = "c" * 40, "b" * 40
            content_digest = check.candidate_content_digest(root)
            source_uri = "https://forge.example/api/commits/" + candidate_rev + "/author"
            identity_statement = forge_author_identity.build_statement(
                repository_uri="https://forge.example/org/repo",
                candidate_revision=candidate_rev,
                candidate_content_sha256=content_digest,
                base_revision=base_rev,
                governance_revision="gov-17",
                scope_id="repo:example/project",
                author_principal="forge:user:alice",
                source_uri=source_uri,
                asserted_on="2026-11-27T12:00:00Z",
            )
            identity_envelope = sign(identity_statement, forge_private, "forge-key")
            identity_path = parent / "author-identity.dsse.json"
            identity_path.write_text(json.dumps(identity_envelope, sort_keys=True, separators=(",", ":")), encoding="utf-8")

            review_statement = independent_review.build_statement(
                repository_uri="https://forge.example/org/repo",
                candidate_revision=candidate_rev,
                candidate_content_sha256=content_digest,
                base_revision=base_rev,
                governance_revision="gov-17",
                scope_id="repo:example/project",
                reviewed_on="2026-11-27T12:00:00Z",
                outcome="accepted",
                claims_reviewed=["claim:security", "claim:tests"],
                observations=["Reviewed the declared claims."],
                limitations=["No trusted timestamp was asserted."],
            )
            review_envelope = sign(review_statement, reviewer_private, "review-key")
            review_path = parent / "independent-review.dsse.json"
            review_path.write_text(json.dumps(review_envelope, sort_keys=True, separators=(",", ":")), encoding="utf-8")
            review_digest = file_digest(review_path)

            report, context = FIXTURE.valid_inputs()
            context["candidate"]["contentDigest"] = {"sha256": content_digest}
            context["candidate"]["revision"] = candidate_rev
            context["base"]["revision"] = base_rev
            context["governance"]["revision"] = "gov-17"
            context["governance"]["scopeId"] = "repo:example/project"
            context["independentReview"] = {
                "status": "attested",
                "reference": {
                    "uri": "https://evidence.example/reviews/" + review_digest,
                    "digest": {"sha256": review_digest},
                },
            }
            assurance_statement = attestation.build_statement(report, context)
            assurance_envelope = sign(assurance_statement, forge_private, "forge-key")
            assurance_path = parent / "assurance.dsse.json"
            assurance_path.write_text(json.dumps(assurance_envelope, sort_keys=True, separators=(",", ":")), encoding="utf-8")

            policy = {
                "schemaVersion": "1",
                "policyId": "govcheck.attestation-trust-policy/v1",
                "revision": "integration-test-policy",
                "openssl": {"path": str(openssl), "sha256": file_digest(openssl)},
                "keys": [
                    {
                        "keyId": "forge-key",
                        "algorithm": "ed25519",
                        "publicKeyPath": forge_public.name,
                        "publicKeySha256": file_digest(forge_public),
                        "principalId": "forge:identity-provider",
                        "roles": ["forge-authority", "assurance-evaluator"],
                        "validFrom": "2000-01-01T00:00:00Z",
                        "validUntil": "2100-01-01T00:00:00Z",
                        "revoked": False,
                    },
                    {
                        "keyId": "review-key",
                        "algorithm": "ed25519",
                        "publicKeyPath": reviewer_public.name,
                        "publicKeySha256": file_digest(reviewer_public),
                        "principalId": "forge:user:bob",
                        "roles": ["independent-reviewer"],
                        "validFrom": "2000-01-01T00:00:00Z",
                        "validUntil": "2100-01-01T00:00:00Z",
                        "revoked": False,
                    },
                ],
            }
            policy_path = parent / "trust-policy.json"
            policy_path.write_text(json.dumps(policy, sort_keys=True, separators=(",", ":")), encoding="utf-8")
            config = {
                "envelope_path": str(review_path),
                "assurance_envelope_path": str(assurance_path),
                "assurance_role": "assurance-evaluator",
                "author_identity_envelope_path": str(identity_path),
                "author_identity_role": "forge-authority",
                "trust_policy_path": str(policy_path),
                "trust_policy_sha256": file_digest(policy_path),
                "author_principal_source": source_uri,
                "governance_revision": "gov-17",
                "scope_id": "repo:example/project",
            }
            git = {
                "candidate_rev": candidate_rev,
                "base_rev": base_rev,
                "head_rev": candidate_rev,
                "worktree_clean": True,
            }
            result = check.evaluate(root, changed={"docs/a.md"}, git=git, independent_review=config)
            rule = next(item for item in result["rules"] if item["id"] == "independent-review")
            self.assertEqual(rule["result"], "pass", rule["reasons"])

    def test_review_unknown_without_attestation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            git = {"candidate_rev": "a" * 40, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"docs/specifications/0001-a.md"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "unknown")
            self.assertEqual(rule["applies"], True)

    def test_in_tree_attestation_never_satisfies_independent_review(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            rev = "a" * 40
            add_attestation(root, reviewer="Bob <bob@example.org>", rev=rev)
            git = {"candidate_rev": rev, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"x.md"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "unknown")
            self.assertIn("candidate-tree attestation record", rule["reasons"][0])
            self.assertIn("DSSE", rule["reasons"][0])

    def test_review_ignores_attestation_by_the_author(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            rev = "a" * 40
            add_attestation(root, reviewer="Alice <alice@example.org>", rev=rev)
            git = {"candidate_rev": rev, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"x.md"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "unknown")

    def test_review_ignores_attestation_for_other_revision(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            add_attestation(root, reviewer="Bob <bob@example.org>", rev="b" * 40)
            git = {"candidate_rev": "a" * 40, "author": "Alice <alice@example.org>"}
            report = check.evaluate(root, changed={"x.md"}, git=git)
            rule = next(r for r in report["rules"] if r["id"] == "independent-review")
            self.assertEqual(rule["result"], "unknown")


    def test_decision_without_references_section_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "docs" / "decisions" / "0001-a.md").write_text("# A\n", encoding="utf-8")
            report = check.evaluate(root)
            self.assertEqual(report["overall"], "fail")
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "fail")

    def test_numbered_references_heading_is_recognized(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "docs" / "decisions" / "0001-a.md").write_text(
                "# A\n\n## 17. References\n\n### Complete source catalogue\n\n- [R-01](../references.md#r-01)\n",
                encoding="utf-8",
            )
            (root / "docs" / "decisions" / "0001-a.fr.md").write_text(
                "# A\n\n## 17. Références\n\n### Catalogue complet\n\n- [R-01](../references.fr.md#r-01)\n",
                encoding="utf-8",
            )
            report = check.evaluate(root)
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "pass")

    def test_references_section_without_source_link_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            (root / "docs" / "decisions" / "0001-a.md").write_text(
                "# A\n\n## References\n\n- [internal](0001-a.fr.md)\n", encoding="utf-8"
            )
            report = check.evaluate(root)
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "fail")

    def test_attestation_without_sources_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            att = root / "docs" / "attestations"
            att.mkdir(parents=True)
            (att / "0001.json").write_text(json.dumps({
                "decision": "accept",
                "candidate_rev": "a" * 40,
                "reviewer": "Bob <bob@example.org>",
            }), encoding="utf-8")
            report = check.evaluate(root)
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "fail")

    def test_sources_present_not_applicable_without_decisions(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            build_tree(root)
            shutil.rmtree(root / "docs" / "decisions")
            report = check.evaluate(root)
            rule = next(r for r in report["rules"] if r["id"] == "sources-present")
            self.assertEqual(rule["result"], "pass")
            self.assertEqual(rule["applies"], False)


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_marker(root, installed=None, digest="0" * 64, conflicts=None, raw=None):
    marker = root / ".govcheck-bootstrap.json"
    if raw is not None:
        marker.write_text(raw, encoding="utf-8")
        return marker
    payload = {
        "tool": "govcheck-bootstrap",
        "package_version": "0.4.0-slice",
        "package_digest": digest,
        "capabilities": ["check"],
        "installed": installed if installed is not None else [],
        "conflicts": conflicts if conflicts is not None else [],
    }
    marker.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return marker


class BootstrapIntegrityTests(unittest.TestCase):
    def _rule(self, root):
        report = check.evaluate(root)
        return next(r for r in report["rules"] if r["id"] == "bootstrap-integrity")

    def test_not_applicable_without_marker(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "decision.md").write_text("# d\n", encoding="utf-8")
            rule = self._rule(root)
            self.assertEqual(rule["result"], "pass")
            self.assertEqual(rule["applies"], False)

    def test_valid_marker_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            f = root / "check.py"
            f.write_text("print(1)\n", encoding="utf-8")
            add_marker(root, installed=[{"path": "check.py", "sha256": sha256_of(f)}])
            rule = self._rule(root)
            self.assertEqual(rule["result"], "pass")
            self.assertEqual(rule["applies"], True)

    def test_drifted_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            f = root / "check.py"
            f.write_text("print(1)\n", encoding="utf-8")
            add_marker(root, installed=[{"path": "check.py", "sha256": "0" * 64}])
            rule = self._rule(root)
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("drifted" in r for r in rule["reasons"]))

    def test_missing_installed_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            add_marker(root, installed=[{"path": "gone.txt", "sha256": "0" * 64}])
            rule = self._rule(root)
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("missing" in r for r in rule["reasons"]))

    def test_invalid_json_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            add_marker(root, raw="{not json")
            rule = self._rule(root)
            self.assertEqual(rule["result"], "fail")

    def test_unsafe_path_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            add_marker(root, installed=[{"path": "../evil", "sha256": "0" * 64}])
            rule = self._rule(root)
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("unsafe" in r for r in rule["reasons"]))

    def test_bad_package_digest_field_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            add_marker(root, digest="xyz")
            rule = self._rule(root)
            self.assertEqual(rule["result"], "fail")
            self.assertTrue(any("package_digest" in r for r in rule["reasons"]))


if __name__ == "__main__":
    unittest.main()
