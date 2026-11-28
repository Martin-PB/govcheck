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
        self.assertEqual(report["schemas_checked"], 5)
        self.assertEqual(report["fixtures_checked"], 7)
        self.assertEqual(report["finding_count"], 0)

    def test_each_schema_rejects_missing_required_property(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        for schema_name, schema in schemas.items():
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

    def test_malformed_fixture_format_is_rejected(self):
        schemas, registry = MODULE.load_schemas(ROOT)
        schema = schemas["release-manifest.schema.json"]
        fixture = MODULE._read_json(ROOT / "formal/fixtures/release-manifest.example.json")
        invalid = copy.deepcopy(fixture)
        invalid["release"]["publishedAt"] = "not-a-date"
        findings = MODULE.validate_instance(invalid, schema, registry, "bad-release")
        self.assertTrue(findings)


if __name__ == "__main__":
    unittest.main()
