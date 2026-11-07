# 0018 — Version governance, compatibility and approval authority

**Status:** proposed governance design for maintainer and governance-authority review. This record does not designate an authority absent from the canonical governance model, adopt Architecture 0017, or claim enforcement exists.  
**Language:** English is the default; see the [French counterpart](0018-version-governance-and-compatibility-authority.fr.md).

## 1. Purpose and relationship to 0017

Architecture 0017 classifies artifact types and defines when MAJOR, MINOR and PATCH are meaningful. This record defines the governance process for proposing, assessing, authorizing and publishing those decisions, including dependency impact and evidence freshness. It operationalizes 0017; it does not supersede it.

Keep six identities distinct:

- **Revision:** exact immutable source state.
- **Contract version:** compatibility promise to declared consumers.
- **Schema version:** structure and semantics of a serialized record format.
- **Catalogue revision:** revision of the registry itself.
- **Release identity:** publication bound to exact source and manifest identities.
- **Instance identity:** one execution, observation, approval or decision.

None measures maturity, assurance, approval or correctness. Until adopted through the canonical governance process, 0017 and this record remain proposals. Merging documentation does not itself confer normative force unless the canonical model explicitly grants that effect and the decision is recorded.

## 2. Authority model

### 2.1 Three distinct responsibilities

1. **Proposer:** identifies the artifact and contract, suggests a classification and supplies the change record.
2. **Compatibility assessor:** evaluates consumer impact, obligation/guarantee deltas, dependencies and evidence freshness. Automated checks provide inputs, not semantic authority.
3. **Authorizing authority:** approves the contract change and published version under the canonical governance model's authority and delegation rules.

A person may combine roles only where canonical governance permits it. Where independent review is required, the proposer cannot be the sole authorizer.

### 2.2 Authority follows the governed subject

| Subject | Authority source |
|---|---|
| Canonical governance model, foundational rules, governance metamodel | Authority designated by the canonical governance model |
| Rule package or repository profile | Authority explicitly delegated for that package/profile and scope |
| Public schema, API, CLI or protocol | Designated interface owner/maintainer, subject to higher governance constraints |
| Formal model/property contract | Domain authority responsible for that contract; normative claims also require the relevant governance authority |
| Tool/product release contract | Product/repository release authority; no power over unrelated normative contracts |
| Evidence, run, approval or attestation instance | Issuer/approver authority for that event; no SemVer authority is implied |

If the canonical model does not identify the responsible authority or delegation, authorization is **blocked**. A maintainer may prepare the proposal but must not fill the gap by self-assigning normative authority. Authority is scoped: approval for one package, profile, interface or release does not authorize another.

An authorization binds at least the authority identity and basis, scope, exact candidate revision, prior/proposed contract versions, decision, rationale, time and provenance. A version increment records an authorized compatibility decision; it does not authorize the underlying change.

## 3. Version decision procedure

For every change to an artifact with a declared contract version:

1. Resolve stable artifact identity, contract identifier and exact prior revision/version.
2. Pin the candidate revision using native VCS identity and content digest where available.
3. Identify the published contract, declared consumers and compatibility direction.
4. Describe observable contract changes, not merely file differences.
5. Compare relevant obligations, guarantees, inputs, outputs, errors, semantics and supported use cases.
6. Enumerate dependencies and downstream claims, tests, proofs, reports, approvals and releases.
7. Classify under 0017; record counterexamples and uncertainty.
8. Obtain required independent assessment and authorization.
9. Publish an immutable contract version bound to the exact revision/release manifest.
10. Record migration, deprecation, support and evidence revalidation actions.

If compatibility cannot be established, the result is **undetermined**, not PATCH by default. Record an ordinary revision without inventing a contract increment, or block publication until review resolves the uncertainty.

## 4. Compatibility decisions

Classification is relative to the previous approved and published contract, its declared consumers and guarantees—not the apparent size of a diff.

| Decision | Required finding | Consequence |
|---|---|---|
| MAJOR | A previously conforming consumer must change, re-evaluate or migrate; or a promised behavior, obligation or guarantee is materially changed/withdrawn | Migration/deprecation plan; review affected consumers and evidence |
| MINOR | New capability is compatible with all declared existing consumers and preserves prior guarantees | Existing consumers remain valid; adoption is optional or safely scoped |
| PATCH | Approved meaning is unchanged; an implementation/representation defect is corrected without changing consumer obligations or relied-upon guarantees | New revision; update affected evidence; no migration implied |
| No contract increment | No contract change: editorial, metadata-only, regenerated projection or implementation change outside the contract | Record ordinary revision; do not manufacture SemVer |
| Undetermined / blocked | Evidence is insufficient, contradictory or outside supported analysis | No compatibility claim; require competent human review |

Initial publication is a distinct authorization event, not a MAJOR/MINOR/PATCH increment: it establishes the first approved baseline contract version where §2.2 of Architecture 0017 is satisfied. There is no prior published contract to compare, but the designated authority is still required. A decision that concludes there is no contract change records no new contract version. Neither case may be silently represented as PATCH.

A correction that changes the meaning consumers actually receive is not automatically PATCH because it is called a bug fix. A security fix is PATCH only if it preserves the declared contract and guarantees. An optional schema field is not automatically MINOR: unknown-field behavior must be part of the contract. Weakening a relied-upon security or assurance guarantee may be MAJOR even if conformance becomes easier. A version number cannot retroactively legitimize an unauthorized normative change.

## 5. Dependencies and evidence freshness

Compatibility and evidence freshness are separate axes. A PATCH can invalidate evidence; a MAJOR change need not invalidate every historical record.

Use typed, directional, revision-bound relations. The initial vocabulary should include:

- **depends-on:** required semantic/structural input;
- **conforms-to:** claimed conformance to a contract;
- **refines:** specialization or implementation of an abstract contract;
- **derived-from:** generated/derived from a source revision;
- **verifies / tests:** a method evaluates a subject or property;
- **supports / refutes:** evidence bears on a claim;
- **supersedes:** authorized successor replaces an earlier artifact/decision;
- **published-with:** artifact is included in a specific release.

Each dependency should identify the exact upstream revision/contract version, not merely a path or latest version. Assess affected dependents as:

- **unaffected:** analysis establishes no relevant dependency change;
- **review-required:** semantic impact is unknown or needs domain judgment;
- **stale/invalid:** required input, assumption, subject or guarantee changed;
- **superseded:** authorized successor replaces the record;
- **revoked:** authorized issuer withdraws an approval, attestation or key-bound statement.

Preserve historical evidence. Invalidated evidence remains auditable but cannot support current acceptance until revalidated. A changed Git commit alone does not invalidate every artifact; unchanged SemVer alone does not preserve evidence validity.

## 6. Existing version-like fields

The repository currently contains fields named catalogueVersion and schemaVersion. Their names do not make them SemVer.

| Field | Intended interpretation | Not to be interpreted as |
|---|---|---|
| formal/artifacts.json: catalogueVersion | Catalogue document/registry format revision marker; currently 1 | Version of each listed artifact, release number or Git revision |
| formal/lifecycle-transitions.json: schemaVersion | Serialized transition-registry structure and machine interpretation version | TLA+ model version, lifecycle contract version or transition-set release |
| release-manifest.schema.json: schemaVersion | Release-manifest serialization contract version | GovCheck product version or version of a manifest instance |
| Git release tag and commit | Repository release identity bound to exact commit (and manifest, if published) | Per-artifact identity or contract version |
| Git commit and content digest | Immutable source/revision identity | Semantic compatibility statement |

The current value 1 is a format marker, not evidence that SemVer compatibility governance has been applied. Do not rename or increment existing fields for cosmetic consistency. Before changing one, define its contract, consumers, migration behavior and authority. A schema-format change and semantic model-contract change may require separate decisions.

This record does not assert a contractVersion for the lifecycle model or any catalogue entry. Do not add one until the declaration requirements in Architecture 0017 §2.2 are satisfied.

## 7. Minimum version-decision record

Record each decision as an immutable event containing: decision ID/time; artifact and contract IDs; prior and candidate revision identities/digests; prior/proposed contract version or explicit absence; contract scope and consumer classes; compatibility direction/classification; changed guarantees/obligations/behaviors and rationale; dependency impact and affected evidence; migration/deprecation/support plan; proposer, assessor(s), authorizing authority and authority basis; outcome, conditions and provenance; and release tag/commit/manifest binding where applicable.

Corrections create a superseding event; they never overwrite the original decision.

## 8. Automation boundary

A future validator may check structural completeness, unique IDs, immutable revision references, version syntax, dependency references, approval records and release-manifest bindings. It may compare machine-readable schemas and enumerate declared dependents.

It must not infer semantic compatibility from a text diff, green tests, a version label or a manually entered compatibility flag. Without a formal compatibility relation, the result is review-required/undetermined. Unknown blocks authorization and remains an explicit state; it is not silently treated as success or mislabeled as a technical failure.

This record does not claim that GovCheck implements a decision engine, dependency graph, invalidation engine, schema validator or approval workflow.

## 9. Adoption and implementation sequence

1. Designate/confirm authorities and delegation boundaries in the canonical governance model.
2. Review and adopt 0017 and this record together, resolving conflicts explicitly.
3. Approve the semantics of existing catalogue/schema version fields; retain current values unless a real format change occurs.
4. Define a machine-readable version-decision record and dependency vocabulary.
5. Extend the artifact catalogue and release manifest in a separate reviewed change, with migration/backward-compatibility treatment.
6. Add validators and negative tests for missing authority, ambiguous compatibility, dangling dependencies, stale evidence and mutable release bindings.
7. Migrate existing records without inventing historical SemVer versions or retroactive approvals.

## 10. Related GovCheck contracts and references

- [Architecture 0017 — Artifact identity, revision and versioning](0017-artifact-identity-revision-and-versioning.md).
- [Specification 0002 — Canonical Governance Model](../specifications/0002-canonical-governance-model.md).
- [Specification 0003 — Change Lifecycle and Acceptance](../specifications/0003-change-lifecycle.md).
- [Specification 0005 — Assurance, Claims and Evidence](../specifications/0005-assurance-model.md).
- [Architecture 0012 — Canonical normative authority](0012-normative-authority-and-documentation.md).
- [Architecture 0013 — Governance metamodel](0013-governance-metamodel.md).
- [Semantic Versioning 2.0.0]([R-14](../references.md#r-14)); [W3C PROV-O]([R-24](../references.md#r-24)); [DataCite Versioning]([R-25](../references.md#r-25)); [1EdTech Versioning Framework 1.0]([R-23](../references.md#r-23)).

External references inform the design; the authority and compatibility rules here are GovCheck proposals, not requirements imposed by those standards.

## Machine-readable design

A non-normative first draft of the machine-readable records is maintained in [formal/schemas/README.md](../../formal/schemas/README.md). It separates version-decision events from revision-bound dependency edges. These schemas remain proposals: they do not establish authority, prove compatibility or implement invalidation.


## Bibliographic references

External sources cited by this record: [R-14](../references.md#r-14), [R-23](../references.md#r-23), [R-24](../references.md#r-24), [R-25](../references.md#r-25).
