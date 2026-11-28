# Fixture and bundle validation contract

**Status:** executable implementation contract; it clarifies validator boundaries but does not adopt the proposed version-governance records as normative.

## Validation units

GovCheck intentionally retains both unit-record and bundle validation. Unit fixtures are not converted into bundles merely to satisfy the cross-record validator.

| Unit | Command | Contract |
|---|---|---|
| One schema instance / unit record | `python3 scripts/validate-formal-fixtures.py --root .` | Each `*.example.json` maps to one Draft 2020-12 schema. All registered schema IDs are available for declared `$ref` resolution. |
| Version-governance bundle | `python3 scripts/validate-version-governance.py path/to/bundle.json --pretty` | The input is an envelope with integer `schemaVersion: 1` and arrays `revisions`, `decisions`, `dependencies`. The validator checks cross-record identities and relationships. |
| Release manifest | Validate the manifest instance against `formal/schemas/release-manifest.schema.json` using the unit-schema validator. | A manifest is a unit schema instance unless a separately specified bundle explicitly embeds it. |
| External references | Unit-schema validator registers the repository's schema `$id` resources together. | Schema references are structural references, not authority or evidence references. |

## Result and exit-code contract

### Unit JSON Schema fixtures

- `valid`, exit 0: schemas and mapped fixtures passed structural validation.
- `invalid`, exit 1: a schema/fixture finding exists.
- Setup failure, exit 2: schema directory, schema resource, or fixture mapping could not be loaded.

### Cross-record bundle

| State | Exit | Meaning |
|---|---:|---|
| `valid` | 0 | No detected cross-record contradiction; not an authorization claim. |
| `invalid` | 1 | Structural or cross-record contradiction. |
| `unknown` | 2 | An external authority fact remains unresolved. |
| `stale` | 3 | A dependency is explicitly not current. |

Errors take precedence over stale, and stale over unknown.

## Invariants and limits

- A unit record must not be passed to the bundle validator as if it were a bundle.
- A bundle envelope must not be passed to an individual record schema.
- JSON Schema validation does not perform cross-record checks.
- The bundle validator does not perform JSON Schema validation; the two tools are complementary.
- Neither tool proves delegated authority, VCS object existence, semantic compatibility, evidence freshness, signatures, or operational behavior.
- All repository fixtures are synthetic schema-conformance examples, not evidence.

## Regression tests

The test suite verifies that a unit dependency-edge fixture is rejected as a bundle and that a bundle envelope is rejected by the dependency-edge schema. It also exercises both validators' positive and negative cases.

Run from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_formal_fixture_validation.py' -v
python3 -m unittest discover -s tests -p 'test_version_governance_validator.py' -v
```
