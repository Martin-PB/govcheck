import copy
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-formal-fixtures.py"
SPEC = importlib.util.spec_from_file_location("formal_fixture_validation", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

ROOT = Path(__file__).resolve().parents[1]


class FormalFixtureValidationTests(unittest.TestCase):
    def test_all_schemas_and_mapped_fixtures_validate(self):
        report = MODULE.audit(ROOT)
        self.assertTrue(report["json_schema_validation_performed"])
        self.assertEqual(report["status"], "valid", report["findings"])
        self.assertEqual(report["schemas_checked"], 20)
        self.assertEqual(report["formal_schemas_checked"], 5)
        self.assertEqual(report["package_schemas_checked"], 14)
        self.assertEqual(report["documentation_schemas_checked"], 1)
        self.assertEqual(report["fixtures_checked"], 20)
        self.assertEqual(report["fixture_schema_validations"], 23)
        self.assertEqual(report["package_schemas_fixture_covered"], 13)
        self.assertEqual(report["package_only_schemas_fixture_covered"], 8)
        self.assertEqual(report["documentation_schemas_fixture_covered"], 1)
        self.assertEqual(report["finding_count"], 0)

    def test_each_schema_rejects_missing_required_property(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        for schema_name, schema in schemas.items():
            if not schema_name.startswith("formal/schemas/"):
                continue
            with self.subTest(schema=schema_name):
                fixture_path = next(
                    path for path in (ROOT / "formal/fixtures").glob("*.example.json")
                    if MODULE.fixture_schema_name(path.name) == schema_name
                )
                instance = MODULE._read_json(fixture_path)
                required = schema.get("required", [])
                self.assertTrue(required, schema_name)
                invalid = copy.deepcopy(instance)
                invalid.pop(required[0], None)
                findings = MODULE.validate_instance(invalid, schema, registry, schema_name)
                self.assertTrue(findings, f"{schema_name} accepted missing {required[0]}")

    def test_each_schema_rejects_unknown_top_level_property(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        for schema_name, schema in schemas.items():
            if not schema_name.startswith("formal/schemas/"):
                continue
            with self.subTest(schema=schema_name):
                fixture_path = next(
                    path for path in (ROOT / "formal/fixtures").glob("*.example.json")
                    if MODULE.fixture_schema_name(path.name) == schema_name
                )
                instance = MODULE._read_json(fixture_path)
                invalid = copy.deepcopy(instance)
                invalid["__unexpected_govcheck_test_property__"] = True
                findings = MODULE.validate_instance(invalid, schema, registry, schema_name)
                self.assertTrue(findings, f"{schema_name} accepted an unknown top-level property")

    def test_nested_types_enums_cardinalities_and_schema_references_are_enforced(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        fixtures = ROOT / "formal/fixtures"

        cases = [
            ("formal/schemas/evidence-record.schema.json", "evidence-record-passed.example.json",
             lambda value: value["claimIds"].append(value["claimIds"][0])),
            ("formal/schemas/dependency-edge.schema.json", "dependency-edge.example.json",
             lambda value: value.__setitem__("relation", "unknown-relation")),
            ("formal/schemas/version-decision.schema.json", "version-decision-blocked.example.json",
             lambda value: value["compatibility"].__setitem__("classification", "unknown-classification")),
            ("formal/schemas/release-manifest.schema.json", "release-manifest.example.json",
             lambda value: value["release"].__setitem__("commit", 42)),
            ("formal/schemas/version-governance-bundle.schema.json", "version-governance-bundle.example.json",
             lambda value: value["decisions"].append({
                 "schemaVersion": 2,
                 "decisionId": "invalid:decision:001"
             })),
        ]
        for schema_name, fixture_name, mutate in cases:
            with self.subTest(schema=schema_name):
                instance = MODULE._read_json(fixtures / fixture_name)
                invalid = copy.deepcopy(instance)
                mutate(invalid)
                findings = MODULE.validate_instance(invalid, schemas[schema_name], registry, fixture_name)
                self.assertTrue(findings, f"{schema_name} accepted an invalid nested value")

    def test_bundle_resolves_external_record_schema_references(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        bundle = {
            "schemaVersion": 1,
            "revisions": [],
            "decisions": [{
                "schemaVersion": 2,
                "decisionId": "bad:decision:001"
            }],
            "dependencies": [{
                "schemaVersion": 1,
                "edgeId": "bad:edge:001",
                "relation": "not-a-relation",
                "source": {},
                "target": {},
                "provenance": {}
            }]
        }
        findings = MODULE.validate_instance(
            bundle, schemas["formal/schemas/version-governance-bundle.schema.json"], registry, "bad-bundle"
        )
        self.assertTrue(findings)
        messages = " ".join(item["message"] for item in findings)
        self.assertIn("was expected", messages)

    def test_package_only_independent_review_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/independent-review-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/independent-review.example.json")
        self.assertEqual(
            MODULE.validate_instance(fixture, schema, registry, "independent-review.example.json"),
            [],
        )
        invalid = copy.deepcopy(fixture)
        invalid["reviewer"] = "untrusted free-form identity"
        findings = MODULE.validate_instance(invalid, schema, registry, "invalid-independent-review")
        self.assertTrue(findings)

    def test_package_only_vcs_provenance_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/vcs-provenance-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/vcs-provenance.example.json")
        self.assertEqual(
            MODULE.validate_instance(fixture, schema, registry, "vcs-provenance.example.json"),
            [],
        )
        invalid = copy.deepcopy(fixture)
        invalid["vcs"]["kind"] = "unknown-vcs"
        findings = MODULE.validate_instance(invalid, schema, registry, "invalid-vcs-provenance")
        self.assertTrue(findings)

    def test_package_only_acceptance_decision_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/acceptance-decision-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/acceptance-decision.example.json")
        self.assertEqual(MODULE.validate_instance(fixture, schema, registry, "acceptance-decision.example.json"), [])
        invalid = copy.deepcopy(fixture)
        invalid["result"] = "approved"
        self.assertTrue(MODULE.validate_instance(invalid, schema, registry, "invalid-acceptance-decision"))

    def test_package_only_forge_author_identity_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/forge-author-identity-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/forge-author-identity.example.json")
        self.assertEqual(MODULE.validate_instance(fixture, schema, registry, "forge-author-identity.example.json"), [])
        invalid = copy.deepcopy(fixture)
        invalid["authorPrincipal"] = ""
        self.assertTrue(MODULE.validate_instance(invalid, schema, registry, "invalid-forge-author-identity"))

    def test_package_only_trust_policy_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/attestation-trust-policy-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/attestation-trust-policy.example.json")
        self.assertEqual(MODULE.validate_instance(fixture, schema, registry, "attestation-trust-policy.example.json"), [])
        invalid = copy.deepcopy(fixture)
        invalid["keys"][0]["algorithm"] = "rsa"
        self.assertTrue(MODULE.validate_instance(invalid, schema, registry, "invalid-trust-policy"))

    def test_package_only_journal_receipt_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/journal-receipt-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/journal-receipt.example.json")
        self.assertEqual(MODULE.validate_instance(fixture, schema, registry, "journal-receipt.example.json"), [])
        invalid = copy.deepcopy(fixture)
        invalid["position"] = -1
        self.assertTrue(MODULE.validate_instance(invalid, schema, registry, "invalid-journal-receipt"))

    def test_package_only_journal_receipt_attestation_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/journal-receipt-attestation-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/journal-receipt-attestation.example.json")
        self.assertEqual(MODULE.validate_instance(fixture, schema, registry, "journal-receipt-attestation.example.json"), [])
        invalid = copy.deepcopy(fixture)
        invalid["predicate"]["journal"]["integrityStatus"] = "unknown"
        self.assertTrue(MODULE.validate_instance(invalid, schema, registry, "invalid-journal-receipt-attestation"))

    def test_package_only_assurance_evaluation_fixture_is_strict(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["govcheck/formal/schemas/assurance-evaluation-v1.schema.json"]
        fixture = MODULE._read_json(ROOT / "govcheck/formal/fixtures/assurance-evaluation.example.json")
        self.assertEqual(MODULE.validate_instance(fixture, schema, registry, "assurance-evaluation.example.json"), [])
        docs_schema = schemas["docs/schemas/govcheck-assurance-evaluation-v1.schema.json"]
        self.assertEqual(MODULE.validate_instance(fixture, docs_schema, registry, "assurance-evaluation-docs"), [])
        invalid = copy.deepcopy(fixture)
        invalid["evaluation"]["result"] = "verified"
        self.assertTrue(MODULE.validate_instance(invalid, schema, registry, "invalid-assurance-evaluation"))

    def test_malformed_fixture_format_is_rejected(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["formal/schemas/release-manifest.schema.json"]
        fixture = MODULE._read_json(ROOT / "formal/fixtures/release-manifest.example.json")
        invalid = copy.deepcopy(fixture)
        invalid["release"]["publishedAt"] = "not-a-date"
        findings = MODULE.validate_instance(invalid, schema, registry, "bad-release")
        self.assertTrue(findings)


if __name__ == "__main__":
    unittest.main()
