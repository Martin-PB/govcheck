# Formal JSON Schemas

**Status:** schemas are design artifacts pending governance adoption and validator integration. A valid JSON instance is not, by itself, evidence of authorization, semantic correctness or conformance.

| Schema | Purpose | Its `schemaVersion` identifies |
|---|---|---|
| [release-manifest.schema.json](release-manifest.schema.json) | Binds a repository release to source artifacts and generated evidence | Release-manifest serialization format |
| [version-decision.schema.json](version-decision.schema.json) | Records an immutable version/compatibility decision event | Version-decision record format |\n| [evidence-record.schema.json](evidence-record.schema.json) | Binds an observation, execution or derivation to claims, exact subjects, method, context and provenance | Evidence-record format |
| [dependency-edge.schema.json](dependency-edge.schema.json) | Records a typed relation between exact artifact revisions | Dependency-edge record format |
| [version-governance-bundle.schema.json](version-governance-bundle.schema.json) | Groups an exact-revision inventory, decisions and dependency edges for cross-record checks | Validation-bundle envelope format |

These format versions are independent of the contract versions of artifacts described by the records. They are not GovCheck product versions and do not follow the MAJOR/MINOR/PATCH policy automatically.

## Version-decision event

The decision schema distinguishes:

- `initial-publication`: an authority-approved first baseline contract version; there is no prior contract revision to compare.
- `major`, `minor`, `patch`: compatibility increments relative to a prior approved contract.
- `no-contract-change`: no new contract version is assigned.
- `undetermined`: insufficient information to classify; cannot be authorized.

An authorized event requires a prior revision for an increment, or an explicit initial-publication case; it also requires a contract scope, proposer, authorizer and authority basis. A blocked/proposed record can preserve unresolved information without pretending approval exists.

## Dependency edge

Edges are directed: `source` holds/makes the relation and `target` is what it points to. For `depends-on`, source is the dependent artifact and target is its dependency. For `verifies`, source is the evidence/method and target is the property/model being evaluated. Each endpoint carries a stable artifact ID and an exact native revision identity.

The schemas do not impose one global acyclicity rule: cycle constraints, if any, must be defined per relation type.

## Synthetic examples

- [version-decision-blocked.example.json](../fixtures/version-decision-blocked.example.json)
- [dependency-edge.example.json](../fixtures/dependency-edge.example.json)
- [evidence-record-passed.example.json](../fixtures/evidence-record-passed.example.json)
- [evidence-record-not-run.example.json](../fixtures/evidence-record-not-run.example.json)

The examples deliberately use reserved `example.invalid` references and synthetic revision IDs. They are schema illustrations, not GovCheck history or evidence.

## Cross-record validator

[version-governance-validator.md](version-governance-validator.md) documents the experimental standard-library validator and its bundle contract. The envelope schema references the two record schemas; the validator performs additional cross-record checks. It intentionally returns `unknown` for authorized decisions until delegation can be resolved against an adopted authority registry.

## Executable schema and fixture validation

The Draft 2020-12 schemas and synthetic examples are checked by:

```sh
python3 -m pip install --requirement requirements-validation.txt
python3 scripts/validate-formal-fixtures.py --root .
python3 -m unittest discover -s tests -p 'test_formal_fixture_validation.py' -v
```

The command validates every schema against the Draft 2020-12 meta-schema, validates each mapped `formal/fixtures/*.example.json` instance with format checking enabled, and fails if a schema has no example fixture or a fixture has no explicit schema mapping. The mapping is deliberately explicit in `scripts/validate-formal-fixtures.py`; adding a schema or fixture requires updating it and its tests.

The report sets `json_schema_validation_performed` to `true` only after the schema/instance validation path has actually run. The separate cross-record validator continues to report this field as `false` when it performs only its own structural and semantic checks; it does not silently imply JSON Schema validation.

## Validation boundary

JSON Schema validates record shape, required fields, enumerations and syntax. A future evaluator must additionally resolve authority and delegation, verify revision existence/integrity, assess compatibility semantics, compute dependency impact and determine evidence freshness. Unknown authority and undetermined compatibility block authorization.

See [Architecture 0017](../../docs/architecture/0017-artifact-identity-revision-and-versioning.md) and [Architecture 0018](../../docs/architecture/0018-version-governance-and-compatibility-authority.md).
