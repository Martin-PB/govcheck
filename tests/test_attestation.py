#!/usr/bin/env python3
"""Tests for GovCheck's in-toto assurance attestation profile."""
from __future__ import annotations

import base64
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("govcheck_attestation", ROOT / "govcheck" / "attestation.py")
att = importlib.util.module_from_spec(spec)
spec.loader.exec_module(att)


def valid_inputs():
    report = {
        "overall": "unknown",
        "candidate": {"candidate_rev": "c" * 40, "base": "main"},
        "rules": [
            {"id": "unit-tests", "class": "decidable", "result": "pass", "applies": True, "reasons": ["127 tests passed"]},
            {"id": "independent-review", "class": "attested", "result": "unknown", "applies": True, "reasons": ["no second contributor is available"]},
        ],
    }
    digest = {"sha256": "a" * 64}
    context = {
        "evaluationId": "eval-2026-11-27-001",
        "evaluatedOn": "2026-11-27T18:00:00Z",
        "repository": {"uri": "https://github.com/example/project", "vcsKind": "git"},
        "candidate": {"revision": "c" * 40, "tree": "d" * 40, "contentDigest": digest},
        "base": {"reference": "main", "revision": "e" * 40, "tree": "f" * 40},
        "governance": {"scopeId": "repo:example/project", "revision": "gov-17", "digest": {"sha256": "1" * 64}},
        "verifier": {"id": "https://example.org/govcheck/verifier", "version": "0.5.0", "digest": {"sha256": "2" * 64}, "configDigest": {"sha256": "3" * 64}},
        "methods": [
            {"id": "tests-127", "kind": "test", "result": "pass", "scope": "tests/", "assumptions": [], "limitations": ["tests do not prove absence of defects"], "tool": {"id": "python-unittest", "version": "3.12"}},
            {"id": "lifecycle-tlc", "kind": "model_check", "result": "pass", "scope": "GovCheckLifecycle at bounded constants", "assumptions": ["finite model constants"], "limitations": ["bounded model; no implementation refinement claim"]},
        ],
        "independentReview": {"status": "unavailable", "reason": "only one contributor is currently available"},
    }
    return report, context


class StatementTests(unittest.TestCase):
    def test_builds_in_toto_statement_and_preserves_unknown(self):
        report, context = valid_inputs()
        statement = att.build_statement(report, context)
        self.assertEqual(statement["_type"], att.STATEMENT_TYPE)
        self.assertEqual(statement["predicateType"], att.PREDICATE_TYPE)
        self.assertEqual(statement["predicate"]["evaluation"]["result"], "unknown")
        self.assertEqual(statement["predicate"]["independentReview"]["status"], "unavailable")
        self.assertEqual(statement["predicate"]["methods"][0]["kind"], "test")
        self.assertEqual(statement["predicate"]["methods"][1]["kind"], "model_check")
        self.assertEqual(statement["subject"][0]["digest"]["sha256"], "a" * 64)

    def test_free_form_reviewer_is_rejected(self):
        report, context = valid_inputs()
        context["independentReview"]["reviewer"] = "Bob"
        with self.assertRaisesRegex(att.AttestationError, "free-form reviewer"):
            att.build_statement(report, context)

    def test_attested_review_requires_detached_statement_reference(self):
        report, context = valid_inputs()
        context["independentReview"] = {"status": "attested", "reason": "review completed"}
        with self.assertRaisesRegex(att.AttestationError, "detached statement reference"):
            att.build_statement(report, context)

    def test_attested_review_accepts_digest_reference_not_reviewer_string(self):
        report, context = valid_inputs()
        context["independentReview"] = {
            "status": "attested",
            "reference": {"uri": "https://evidence.example.org/reviews/review-statement.json", "digest": {"sha256": "4" * 64}},
        }
        statement = att.build_statement(report, context)
        self.assertEqual(statement["predicate"]["independentReview"]["status"], "attested")
        self.assertNotIn("reviewer", statement["predicate"]["independentReview"])

    def test_report_candidate_must_match_attestation_context(self):
        report, context = valid_inputs()
        report["candidate"]["candidate_rev"] = "9" * 40
        with self.assertRaisesRegex(att.AttestationError, "candidate revision does not match"):
            att.build_statement(report, context)

    def test_report_base_reference_must_match_attestation_context(self):
        report, context = valid_inputs()
        report["candidate"]["base"] = "release"
        with self.assertRaisesRegex(att.AttestationError, "base reference does not match"):
            att.build_statement(report, context)

    def test_pijul_candidate_requires_native_channel_and_change_set(self):
        report, context = valid_inputs()
        context["repository"]["vcsKind"] = "pijul"
        context["candidate"].update({"channel": "main", "changeSet": "pijul-change-set-id"})
        context["base"].update({"channel": "main", "changeSet": "pijul-base-change-set"})
        statement = att.build_statement(report, context)
        self.assertEqual(statement["predicate"]["candidate"]["channel"], "main")
        self.assertEqual(statement["predicate"]["candidate"]["changeSet"], "pijul-change-set-id")

    def test_pijul_candidate_without_change_set_is_rejected(self):
        report, context = valid_inputs()
        context["repository"]["vcsKind"] = "pijul"
        context["candidate"]["channel"] = "main"
        with self.assertRaisesRegex(att.AttestationError, "candidate.changeSet"):
            att.build_statement(report, context)

    def test_missing_sha256_is_rejected(self):
        report, context = valid_inputs()
        context["candidate"]["contentDigest"] = {"gitCommit": "a" * 40}
        with self.assertRaisesRegex(att.AttestationError, "sha256 digest"):
            att.build_statement(report, context)

    def test_invalid_result_is_rejected(self):
        report, context = valid_inputs()
        report["overall"] = "accepted-with-risk"
        with self.assertRaisesRegex(att.AttestationError, "overall"):
            att.build_statement(report, context)

    def test_decision_is_not_inferred_from_evaluation(self):
        report, context = valid_inputs()
        statement = att.build_statement(report, context)
        self.assertNotIn("authorityDecision", statement["predicate"])
        self.assertNotIn("riskAcceptance", statement["predicate"])

    def test_dsse_pae_uses_exact_utf8_lengths(self):
        payload_type = "http://example.com/HelloWorld"
        payload = b"hello world"
        self.assertEqual(
            att.dsse_pae(payload_type, payload),
            b"DSSEv1 29 http://example.com/HelloWorld 11 hello world",
        )

    def test_dsse_envelope_round_trip_is_structural_only(self):
        report, context = valid_inputs()
        statement = att.build_statement(report, context)
        envelope = att.build_dsse_envelope(statement, [{"keyid": "synthetic-key", "sig": base64.b64encode(b"fake-signature").decode("ascii")}])
        payload, decoded = att.decode_dsse_envelope(envelope)
        self.assertEqual(decoded, statement)
        self.assertEqual(json.loads(payload.decode("utf-8")), statement)
        # A structural round trip must not claim that the synthetic signature was verified.

    def test_empty_signature_list_is_rejected(self):
        report, context = valid_inputs()
        statement = att.build_statement(report, context)
        with self.assertRaisesRegex(att.AttestationError, "at least one external signature"):
            att.build_dsse_envelope(statement, [])

    def test_malformed_envelope_payload_is_rejected(self):
        with self.assertRaisesRegex(att.AttestationError, "payload is not valid base64"):
            att.decode_dsse_envelope({"payloadType": att.DSSE_PAYLOAD_TYPE, "payload": "!", "signatures": [{"sig": "YQ=="}]})

    def test_unsupported_payload_type_is_rejected(self):
        with self.assertRaisesRegex(att.AttestationError, "unsupported DSSE payloadType"):
            att.decode_dsse_envelope({"payloadType": "application/json", "payload": "e30=", "signatures": [{"sig": "YQ=="}]})


if __name__ == "__main__":
    unittest.main()
