# ADR 0004 — Semantic versioning for GovCheck product and governance package

**Status:** adopted; records the project owner's explicit decision to adopt category-specific SemVer on 2026-11-07. **French:** [0004 (français)](0004-semantic-versioning-contracts.fr.md).

## Context

GovCheck needs semantic versioning, but not one global version string for every file, model, decision, test, proof, report or release. Architecture 0017 already defines a category-specific compatibility policy; Architecture 0018 defines the authority and decision process. Both still describe themselves as proposals, which no longer reflects the project decision to adopt semantic versioning.

The repository also contains two distinct deliverables: the GovCheck product and the reusable governance package under **govcheck/**. ADR 0003 describes their separate product/meta roles. Their versions must not be conflated.

## Decision

1. **Adopt SemVer 2.0.0 as GovCheck's versioning standard wherever a declared compatibility contract makes MAJOR.MINOR.PATCH meaningful.** The category-specific applicability and compatibility rules in Architecture 0017 are adopted. SemVer is not a universal artifact revision scheme.
2. **Maintain two independent release contracts:**
   - **govcheck.product**: the GovCheck product and its declared public interfaces.
   - **govcheck.governance-package**: the reusable **govcheck/** package and its declared governance/package interfaces.
   They have independent version sequences and compatibility assessments. A product release may pin a package release, but one version never implies or increments the other.
3. **Use complete SemVer identifiers.** **0.1** may be informal shorthand in discussion; it is not a complete release identifier. A complete identifier has three numeric components, e.g. **0.1.0**. This ADR does not declare **0.1.0** as a published release; it records that value only as the planned first product baseline.
4. **Respect pre-1.0 semantics.** Until a contract reaches 1.0.0, it is in initial development and its public API is not promised stable under SemVer. Breaking changes to an already declared pre-1.0 contract must nevertheless be explicit, documented and reflected by a MINOR increment; they must not be hidden in PATCH releases.
5. **Preserve the category-specific regimes in Architecture 0017.** SemVer applies to a product/package/API/schema/model/profile/rule-set contract only when its consumer, scope, guarantees, compatibility relation and authorizing authority are declared. Individual rules, ADRs, decisions, exceptions, approvals, test executions, proof runs, observations, evidence items, reports and manifests are not independently assigned SemVer by default; they retain stable identities, immutable revisions/instances and provenance.
6. **Keep all version axes separate.** Repository Git tags/commits identify repository releases/revisions. Product/package SemVer identifies compatibility contracts. JSON **schemaVersion** and **catalogueVersion** identify their respective serialization/registry formats. They are not interchangeable.
7. **Require an explicit initial-publication decision.** Do not infer a first version from a branch, commit, date, package directory, schema marker or previous informal label. Do not invent historical versions or retroactive approvals. Bind each published version to an immutable revision and release manifest.
8. **Apply Architecture 0018's governance process.** Every increment is assessed against the previously approved published contract and declared consumers. Compatibility uncertainty is **undetermined**, never an automatic PATCH. Authorization follows the subject-scoped authority regime in [Architecture 0023](../architecture/0023-bootstrap-governance-authority.md); repository, merge and CI permissions alone do not confer normative authority.
9. **Keep the reusable package and GovCheck's meta-history aligned.** Normative package changes must update the generic package contract and the corresponding GovCheck meta-level record in the same pull request, without copying GovCheck-specific decisions into governed repositories.

## Consequences

- This ADR adopts Architecture 0017 and 0018 as the category-specific versioning and version-governance policies; their former proposed status is resolved.
- Specification 0002 now explicitly distinguishes the reusable governance-package contract from the GovCheck product release contract. This does not adopt the whole canonical governance model or claim an evaluator exists.
- Existing **catalogueVersion: 1**, **schemaVersion: 1**, Git tags and historical revisions retain their current meanings. No existing value is renamed or retroactively converted to SemVer.
- The planned first GovCheck product baseline is **0.1.0**; this is not a published or authorized release. The reusable governance package has an independent version sequence and no version is assigned here. Each first release requires its own initial-publication decision, declared contract, authority approval and immutable release binding.
- The version-decision/dependency schemas and validator remain separate implementation work. Their structural validity cannot establish semantic compatibility or authority.
- PR #21 has been merged. Its [Architecture 0023](../architecture/0023-bootstrap-governance-authority.md) record is now present on main and provides the authority basis for review of this ADR.

## References

- [Architecture 0017 — Artifact identity, revision and versioning](../architecture/0017-artifact-identity-revision-and-versioning.md).
- [Architecture 0018 — Version governance, compatibility and approval authority](../architecture/0018-version-governance-and-compatibility-authority.md).
- [Architecture 0019 — Artifact catalogue and release-manifest evolution](../architecture/0019-catalogue-and-release-manifest-migration.md).
- [Specification 0002 — Canonical Governance Model](../specifications/0002-canonical-governance-model.md).
- [ADR 0003 — Two-level governance](0003-two-level-governance.md).
- [R-14 — Semantic Versioning 2.0.0](../references.md#r-14).
- [R-15 — Git tags and GitHub releases](../references.md#r-15).
- [R-23 — 1EdTech Versioning Framework](../references.md#r-23).
- [R-21 — Research software release and reproducibility guidance](../references.md#r-21).
- [R-24 — W3C PROV-O](../references.md#r-24).
- [R-25 — DataCite versioning recommendations](../references.md#r-25).
- [R-26 — Scientific Data versioning study (2024)](../references.md#r-26).
