# 0022 — Governance capability audit and implementation gaps

**Status:** repository audit and implementation proposal; not a normative policy, adoption decision, or implementation claim.  
**Scope:** governance capabilities in GovCheck only. This record audits the repository state after the merge of PR #19. **Français:** [0022](0022-governance-capability-audit.fr.md).

## 1. Executive finding

GovCheck already contains a substantial governance design: a canonical-governance concept, a governance metamodel, normative-authority and documentation-conformity rules, actor responsibilities, version-governance procedures, structured version-decision/dependency records, and lifecycle/assurance TLA+ models.

The principal gap is not a missing catalogue or another abstract governance vocabulary. It is the distance between those design records and an adopted, machine-readable governance authority whose rules, scopes, authorities, exceptions and transitions are evaluated consistently.

The repository itself repeatedly marks the relevant architecture and schemas as proposals or design artifacts. In particular, Specification 0002 says no canonical governance schema or evaluator is implemented; Architecture 0012 says no governance engine/parser/generator/enforcement is claimed; the formal schema README says schemas await governance adoption and validator integration. These status statements must be preserved.

**Conclusion:** do not add a parallel governance catalogue. Close the normative-authority and execution gap in small, reviewable steps.

## 2. Evidence examined

This audit is based on the default-branch source files and model text, not on product claims:

- Specification 0002 — Canonical Governance Model.
- Architecture 0012 — Canonical normative authority and documentation conformity.
- Architecture 0013 — Governance metamodel.
- Architecture 0014 — Governed development workflow and actor responsibilities.
- Architecture 0015 — Governance Conformance Tool and validation plan.
- Architectures 0017–0019 — artifact identity/versioning, approval authority and catalogue/release-manifest evolution.
- `formal/schemas/version-decision.schema.json`, `dependency-edge.schema.json`, `version-governance-bundle.schema.json` and the schema README.
- `formal/tla/GovCheckLifecycle.tla` and `GovCheckAssurance.tla`, with their TLC configurations.
- PR #19, merged as commit `8018cf769b17bd89f86e194e5361c57a9a465936`.

This is a source audit. It does not claim that every workflow, validator or CI path was executed in this audit.

## 3. Capability matrix

| Governance capability | Repository evidence | Assessment |
|---|---|---|
| Canonical normative source | Specification 0002 and Architecture 0012 define one authority and controlled projections | **Designed; not implemented/adopted** |
| Typed rules and normative force | Architecture 0013 distinguishes obligations, prohibitions, permissions, invariants and recommendations | **Designed; no canonical rule schema/evaluator** |
| Applicability and profiles | 0002/0013 describe scopes, profiles and typed parameters | **Designed; no demonstrated profile resolution** |
| Ownership and authority | 0013/0018 describe owners, authorities, scoped delegation and blocking on unknown authority | **Partially represented; no adopted authority registry or delegation resolver** |
| Approval workflow | 0014/0018 describe proposer, assessor and authorizer; version-decision schema records roles and authority basis | **Partially represented; version-specific record only** |
| Separation of duties | 0014/0018 and Assurance model require independent review in scoped cases | **Partially formalized; lifecycle model does not bind approval to proposer/role** |
| Exceptions / waivers | 0002/0010/0015 describe scoped, authorized, expiring exceptions | **Conceptual only; no dedicated record schema or transition model found** |
| Policy lifecycle | 0012 describes propose, validate, approve, publish and project; 0018 covers version decisions | **Procedure described; no general policy lifecycle model** |
| Auditability | Version-decision schema has provenance and supersession; TLA models keep bounded history/state | **Partial; no general typed append-only governance event contract** |
| Dependency and impact | Dependency-edge schema and version-governance bundle bind exact revisions | **Schema exists; semantic graph/impact evaluation remains incomplete** |
| Evidence freshness | Assurance model covers version drift, expiry, revocation and review invalidation | **Formally modelled in a bounded fixture; integration with lifecycle is explicitly pending** |
| Documentation conformity | Architecture 0012 defines projection and drift requirements | **Designed; no conformance engine claimed** |
| Conflict handling | 0013/0002 require explicit conflict/indeterminate outcomes | **Semantics proposed; no complete rule-composition evaluator** |
| Enforcement and bypass | 0015 distinguishes local audit from operational enforcement and records bypass limits | **Requirements documented; deployment enforcement not established** |

## 4. Concrete gaps found in the current formal boundary

### 4.1 Lifecycle approvals are not yet a governance authority model

In `GovCheckLifecycle.tla`, `Approve(actor)` checks membership in `AuthorizedActors`, and `Accept` checks a cardinality threshold. The state does not identify a proposer, approval role, authority basis, delegation, decision ID or approval revocation. The current TLC configuration authorizes both fixture actors and requires one approval. Therefore this model does not establish proposer/approver separation or scoped authority.

This is not a defect in the model's stated narrow lifecycle abstraction; it is a limit that must not be mistaken for complete governance authorization.

### 4.2 Assurance independence is fixed to the fixture

`GovCheckAssurance.tla` checks that the designated reviewer is authorized and differs from the producer. This is useful, but the fixture has fixed producer/reviewer constants and a two-claim graph. It does not model role assignment, delegation chains, authority scope, suspension/revocation of a reviewer, or policy changes that alter required reviewers.

### 4.3 Exceptions have no first-class lifecycle

The design records require exceptions to be scoped, justified, authorized, time-bounded and revocable. No dedicated exception schema or TLA+ transition model was found among the audited governance artifacts. An exception must not be encoded as a successful check outcome or free-text comment.

### 4.4 The canonical governance package remains conceptual

Specification 0002 describes package identity, stable rule IDs, typed rules, applicability, relations, parameters, exceptions, profiles and projection metadata, but explicitly leaves serialization and evaluator selection open. The existing JSON schemas concern version decisions, dependency edges, bundles, evidence or release manifests; they are not a canonical policy-package schema.

### 4.5 The validator boundary is intentionally incomplete

The schema documentation states that structural validation does not establish authority or semantic correctness, and that authorized version decisions remain `unknown` until delegation can be resolved against an adopted authority registry. This is the correct fail-closed posture, but it means approval is not yet operationally decidable from the current records alone.

## 5. What to take from Knowledge Catalog — narrowly

The useful transferable pattern is **type-specific mandatory governance metadata**, not Google's data-catalog product architecture.

For GovCheck, apply that pattern to governance objects themselves:

- A **rule** must identify stable ID, normative force, scope, source/authority, revision and lifecycle state.
- A **profile** must identify its governed subject, selected rules, parameters, composition rules and authorizing authority.
- An **authority/delegation** must identify issuer, delegate, scope, allowed actions, validity interval and revocation/supersession.
- An **exception** must identify the exact subject/rules waived, reason, compensating controls, authorizer, expiry and revocation state.
- A **decision** must bind actor/role, authority basis, exact policy revision, exact subject revision, outcome, rationale and prior decision where superseded.
- A **control result** must bind the exact rule revision, subject, evaluator/tool revision, inputs, outcome, limitations and evidence.

Required fields must depend on object type and decision outcome. Do not introduce arbitrary user-defined metadata that can weaken mandatory controls. Unknown mandatory semantics must remain indeterminate/blocked.

## 6. Recommended implementation sequence

These are proposed work packages, not approved policy changes.

### G0 — Adopt and identify the normative authority

**Initial decision now recorded in Architecture 0023:** one principal, `Martin-PB`, currently holds normative authority and may amend the authority regime itself. No authority is inferred from repository ownership, PR merge or CI status. The decision is versioned, prospective and explicitly amendable by its holder.

This decision still needs translation into canonical records, validation and a formal model. Architecture 0023 also distinguishes normative authorization, technical review and execution, and makes explicit that the initial regime does not provide separation of persons for adoption.

### G1 — Define the minimal canonical governance records

Specify and validate a minimal set: governance package, rule, profile, authority/delegation, exception, decision and typed governance event. Reuse stable identities and revision binding already defined in 0017–0019. Keep the format declarative; no arbitrary policy scripts.

### G2 — Make authority and exceptions decidable

Add cross-record validation for authority scope, delegation validity, actor-role compatibility, separation of duties, exception scope/expiry/revocation and supersession. Missing or ambiguous authority must block authorization.

### G3 — Formalize the governance lifecycle

Add a bounded TLA+ model for propose → assess → authorize/reject → publish → supersede/revoke, including scoped delegation, independent review, expiring exceptions and concurrent/stale decisions. Add explicit invariants for no self-authorization where prohibited, no out-of-scope authorization, no expired/revoked exception, and no retroactive mutation of a published policy.

### G4 — Connect governance to assurance and application

Make lifecycle acceptance consume the exact adopted governance package/profile revision and its resolved obligations. Revalidate the same identities immediately before application. Keep evidence invalidation and governance-policy invalidation distinct but composable.

### G5 — Test the semantics, not just the schema

Add language-neutral positive and negative conformance vectors for missing authority, invalid delegation, self-approval, wrong scope, expired/revoked exception, conflicting rules, unknown applicability, superseded policy, concurrent update and stale approval. JSON Schema success alone is not governance success.

## 7. Explicit non-goals

- Do not clone Google Knowledge Catalog or build a generic metadata platform.
- Do not add a second catalogue alongside `formal/artifacts.json`.
- Do not treat labels, PR approvals, green CI, comments or repository admin status as normative authority by themselves.
- Do not turn all governance records into SemVer artifacts.
- Do not equate an exception with evidence, or an approved exception with proof of conformity.
- Do not claim enforcement merely because local validation reports success.

## 8. Audit conclusion

GovCheck has already designed much of the governance vocabulary and documented several important safety principles. The next substantial capability is not another broad metamodel: it is a small canonical governance package plus explicit authority/delegation and exception semantics, validated across records and formally modelled through its lifecycle.

The first implementation decision is therefore governance authority and adoption—not the choice of a catalogue UI, ontology platform or generic workflow engine.
