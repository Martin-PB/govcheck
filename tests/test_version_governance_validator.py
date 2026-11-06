import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-version-governance.py"
SPEC = importlib.util.spec_from_file_location("version_governance_validator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def revision(native_id):
    return {"vcs": "git", "nativeId": native_id}


def authorized_decision():
    return {
        "schemaVersion": 1,
        "decisionId": "decision:initial:001",
        "artifactId": "govcheck.example-contract",
        "contractId": "govcheck.example",
        "previous": None,
        "candidateRevision": revision("a" * 40),
        "proposedContractVersion": "1.0.0",
        "contractScope": {"summary": "Synthetic public contract.", "consumerClasses": ["test-consumer"]},
        "compatibility": {
            "classification": "initial-publication",
            "rationale": "Synthetic test case.",
            "changedGuarantees": []
        },
        "decision": {"outcome": "authorized", "decidedAt": "2026-01-01T00:00:00Z", "conditions": []},
        "roles": {
            "proposer": {"actorId": "person-a", "actorType": "person"},
            "authorizer": {"actorId": "authority-a", "actorType": "person"}
        },
        "authority": {"authorityId": "authority-a", "basis": "test only", "scope": "test contract"},
        "provenance": {
            "recordedAt": "2026-01-01T00:00:00Z",
            "recordedBy": {"actorId": "test", "actorType": "service"}
        }
    }


def bundle():
    return {
        "schemaVersion": 1,
        "revisions": [
            {"artifactId": "govcheck.example-contract", "revision": revision("a" * 40)},
            {"artifactId": "govcheck.example-proof", "revision": revision("b" * 40)}
        ],
        "decisions": [authorized_decision()],
        "dependencies": [{
            "schemaVersion": 1,
            "edgeId": "edge:proof:contract",
            "relation": "verifies",
            "source": {"artifactId": "govcheck.example-proof", "revision": revision("b" * 40)},
            "target": {"artifactId": "govcheck.example-contract", "revision": revision("a" * 40)},
            "validity": {"status": "active"},
            "provenance": {"recordedAt": "2026-01-01T00:00:00Z", "recordedBy": "synthetic-test"}
        }]
    }


class ValidatorTests(unittest.TestCase):
    def test_authorized_record_is_unknown_not_asserted_valid(self):
        result = MODULE.validate_bundle(bundle())
        self.assertEqual(result["status"], "unknown")
        self.assertIn("decision.authority-not-resolved", {x["code"] for x in result["findings"]})
        self.assertFalse(result["scope"]["authority_delegation_verified"])

    def test_orphan_candidate_revision_is_invalid(self):
        data = bundle()
        data["decisions"][0]["candidateRevision"] = revision("c" * 40)
        result = MODULE.validate_bundle(data)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("decision.candidate-missing", {x["code"] for x in result["findings"]})

    def test_orphan_dependency_endpoint_is_invalid(self):
        data = bundle()
        data["dependencies"][0]["target"]["revision"] = revision("c" * 40)
        result = MODULE.validate_bundle(data)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("edge.endpoint-missing", {x["code"] for x in result["findings"]})

    def test_stale_edge_is_not_reported_current(self):
        data = bundle()
        data["dependencies"][0]["validity"] = {"status": "revoked"}
        result = MODULE.validate_bundle(data)
        self.assertEqual(result["status"], "stale")
        self.assertIn("edge.not-current", {x["code"] for x in result["findings"]})

    def test_missing_edge_validity_is_unknown_not_active(self):
        data = bundle()
        data["dependencies"][0].pop("validity")
        result = MODULE.validate_bundle(data)
        self.assertEqual(result["status"], "unknown")
        self.assertIn("edge.validity-unresolved", {x["code"] for x in result["findings"]})

    def test_impact_cannot_call_revoked_edge_unaffected(self):
        data = bundle()
        data["dependencies"][0]["validity"] = {"status": "revoked"}
        data["decisions"][0]["dependencyImpact"] = [
            {"edgeId": "edge:proof:contract", "assessment": "unaffected"}
        ]
        result = MODULE.validate_bundle(data)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("decision.impact-contradiction", {x["code"] for x in result["findings"]})

    def test_duplicate_decision_ids_are_invalid(self):
        data = bundle()
        duplicate = dict(data["decisions"][0])
        data["decisions"].append(duplicate)
        result = MODULE.validate_bundle(data)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("decision.duplicate", {x["code"] for x in result["findings"]})

    def test_blocked_decision_does_not_claim_authority_resolution(self):
        data = bundle()
        decision = data["decisions"][0]
        decision["decision"] = {
            "outcome": "blocked", "decidedAt": "2026-01-01T00:00:00Z",
            "conditions": ["Authority not established."]
        }
        decision["compatibility"]["classification"] = "undetermined"
        decision["proposedContractVersion"] = None
        decision.pop("roles")
        decision.pop("authority")
        result = MODULE.validate_bundle(data)
        self.assertEqual(result["status"], "valid")


if __name__ == "__main__":
    unittest.main()
