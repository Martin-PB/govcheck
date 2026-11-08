# Specification 0002 — Canonical Governance Model

**Status:** Proposed architecture, ready for review. **Normative status:** design contract only; no schema or evaluator is implemented. [French](0002-canonical-governance-model.fr.md).

## Purpose and invariants

The versioned canonical governance model is the sole normative authority for a repository. GovCheck evaluates it. Markdown (AGENTS.md, GOVERNANCE.md, SECURITY.md, CONTRIBUTING.md) is generated or checked projection and explanation, never a competing source of rules. The model is independent of VCS, hosting, forge, CI, language and agent harness. Formal foundations apply to every repository; profiles may add requirements but cannot remove foundations.

## Conceptual structure

A governance package contains: package identity and semantic version; stable rule IDs; typed rules; applicability scopes; explicit relations (dependency, refinement, supersession, incompatibility); typed parameters; bounded exceptions; repository profiles; and projection metadata (document, language, section, generation/check strategy). This is a conceptual contract, not a serialization syntax. Format selection remains open.

A rule ID is immutable and never recycled. Rule wording, translations, scope and predicates may evolve, but semantic changes require review and traceability. Removed rules remain addressable through tombstones or supersession records.

## Package and product version contracts

GovCheck uses two distinct release contracts:

- **GovCheck product** (**govcheck.product**): the complete distributable product and its declared public interfaces, including the executable/CLI and supported integration surfaces when published.
- **Reusable governance package** (**govcheck.governance-package**): the independently consumable package under **govcheck/**, copied or bootstrapped into governed repositories. Its contract is the governance model, rules, profiles, bootstrap behavior and supported package interfaces.

Each contract has its own SemVer sequence, compatibility assessment, authorization and immutable release identity. A product release may include a particular governance-package release, but neither version is inferred from the other. A Git repository tag identifies a repository release/commit; it does not automatically assign either contract version.

The planned first GovCheck product baseline is **0.1.0**; this is a target, not a published or authorized release. The reusable governance package has its own independent version sequence, whose first version remains unassigned. A first publication is an explicit initial-publication decision, not an invented MAJOR/MINOR/PATCH increment. A complete SemVer string has three numeric components (for example, **0.1.0**); shorthand such as **v0.1** is not a complete release identity.

Before 1.0.0, the relevant contract is explicitly in initial development: under SemVer, anything may change and the public API should not be treated as stable. A change that breaks an already declared pre-1.0 contract still requires an explicit compatibility assessment, migration note and MINOR increment rather than a silent PATCH. Once a contract reaches 1.0.0, the normal MAJOR/MINOR/PATCH compatibility rules apply.

The product and package may evolve at different rates. A change to GovCheck's own CLI can increment the product contract without changing the governance package. A change to a normative rule package can increment the governance-package contract without requiring a product increment if the product interface and guarantees are unchanged. Schema-format markers, artifact revisions, ADRs, executions, evidence and decisions remain governed by their own identity rules; they are not assigned SemVer merely because they are part of a release.

## Rule semantics

Distinguish at least: obligation, prohibition, permission, invariant/constraint, evidence requirement, process/approval requirement, and advisory guidance. Advisory guidance is explicitly non-normative. Absence of prohibition is not permission. A permission does not cancel an obligation or prohibition absent an explicit valid precedence relation.

## Applicability and composition

Evaluation context explicitly identifies repository and candidate states, governance revision, change, affected resources, actor class and declared environment facts. Mandatory foundations always apply. Profiles may refine or add constraints. Scoped rules apply only when their predicates match. A narrower scope cannot silently weaken a mandatory rule. Precedence is an explicit partial relation, never file order or "last wins".

Unresolved contradictions, unknown rule kinds, unsupported major semantic versions, malformed scopes, unresolved references and ambiguous precedence are governance errors. Acceptance fails closed on them.

## Exceptions

An exception identifies exact rule IDs and scope, reason, risk owner, approver authority, start/expiry, compensating controls and exact repository/governance state. It is auditable and revocable. Expired, unapproved, out-of-scope or state-mismatched exceptions are invalid. Exceptions cannot waive the existence of formal foundations, erase history or retroactively convert failure to success.

## Evaluation

Evaluation is deterministic for identical canonical inputs and pinned evaluator semantics. It reports applicable rules; satisfied, unsatisfied, indeterminate and conflicting outcomes; evidence gaps; exception validity; explanations and provenance. Aggregate outcomes include pass, fail, blocked/indeterminate and invalid-governance. For acceptance, indeterminate is not satisfied. Advisory findings are separate.

## Documentation projections

A projection records canonical revision and generator/checker version. GovCheck must generate it or verify normative statements and detect drift. Free-form explanation is allowed only when marked non-normative. Projections cannot invent rules, silently omit mandatory rules or change normative force through translation. English is default; French must preserve normative meaning. Translation drift is documentation non-conformance, not a second authority.

## Trust boundary and open choices

The model is data, not executable code. No arbitrary repository policy scripts are executed. Any future expression language must be typed, bounded, deterministic and resource-limited. External facts carry source and freshness; the model does not prove their truth. Serialization, schema technology, expression language, canonicalization, signatures and distribution remain open and require comparative evaluation.

## Conformance targets

An implementation must demonstrate stable IDs, deterministic composition, explicit conflict handling, bounded exceptions, fail-closed indeterminacy, semantic-version pinning, projection drift detection and reproducible explanations. These are targets, not current guarantees.

## Bibliographic references

See the [package reference catalogue](../references.md) for the sources shipped with this package.
