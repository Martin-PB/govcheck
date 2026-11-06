# Formal JSON Schemas

**Status:** schemas are design artifacts pending governance adoption and validator integration. A valid JSON instance is not, by itself, evidence of authorization, semantic correctness or conformance.

| Schema | Purpose | Its `schemaVersion` identifies |
|---|---|---|
| [release-manifest.schema.json](release-manifest.schema.json) | Binds a repository release to source artifacts and generated evidence | Release-manifest serialization format |
| [version-decision.schema.json](version-decision.schema.json) | Records an immutable version/compatibility decision event | Version-decision record format |
| [dependency-edge.schema.json](dependency-edge.schema.json) | Records a typed relation between exact artifact revisions | Dependency-edge record format |

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

The examples deliberately use reserved `example.invalid` references and synthetic revision IDs. They are schema illustrations, not GovCheck history or evidence.

## Validation boundary

JSON Schema validates record shape, required fields, enumerations and syntax. A future evaluator must additionally resolve authority and delegation, verify revision existence/integrity, assess compatibility semantics, compute dependency impact and determine evidence freshness. Unknown authority and undetermined compatibility block authorization.

See [Architecture 0017](../../docs/architecture/0017-artifact-identity-revision-and-versioning.md) and [Architecture 0018](../../docs/architecture/0018-version-governance-and-compatibility-authority.md).
