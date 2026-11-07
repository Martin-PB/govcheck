# 0012 — Canonical normative authority and documentation conformity

**Status:** architecture contract proposed for maintainer approval. No governance engine, parser, generator or enforcement mechanism is claimed to exist. **French:** [0012](0012-normative-authority-and-documentation.fr.md).

## Principle

A repository must not acquire competing normative authorities merely because humans and agents consume several instruction files. GovCheck is intended to interpret one versioned, machine-readable governance authority. Human-facing files explain or project that authority; they do not silently create a second policy.

Design invariant:

`For every controlled document d: NormativeContent(d) ⊆ AuthorizedRules(GovCheck)`

This is a target invariant, not a claim that current documents have already been checked.

## Source hierarchy

1. **Approved governance source:** canonical, versioned, machine-readable rules with authority and provenance.
2. **Governance semantics/evaluator:** defined interpretation of rule types, scope, applicability, composition, exceptions and transitions.
3. **Controlled human-readable projections:** generated or mechanically checked sections in `AGENTS.md`, `GOVERNANCE.md`, `SECURITY.md`, `CONTRIBUTING.md` and repository-specific equivalents.
4. **Explanatory material:** tutorials, examples, rationale, architecture notes and discussion. It may explain but cannot silently add obligations.

The canonical serialization, schema technology, expression language and file layout remain open. This ADR selects no language, format, policy engine or proof tool.

## Document content classes

Each controlled section is classified as:
- **Normative projection:** faithful rendering of canonical rule IDs, with traceability metadata or an equivalent mapping.
- **Operational instruction:** procedure for using a tool or performing a task. If it constrains required behavior, it references an authorized rule; otherwise it is explicitly optional guidance.
- **Explanatory content:** rationale, examples, background or advice; it is not an unregistered obligation.

A document may mix classes, but boundaries must be explicit. Generated normative sections are distinguishable from maintained explanations. A file does not become authoritative merely because an agent convention gives it practical influence.

## Identity and traceability

Each rule has a stable, immutable ID, evolution history, normative force, applicability, typed parameters and provenance to an approved decision/source. IDs are never recycled. Semantic changes create traceable revisions, replacement or supersession relations.

Every normative projection maps statements to rule IDs. The reverse mapping identifies where each rule is projected, or explicitly says it is not. A translation projects the same rule; it is not an independently editable policy. Translation drift is a conformity defect.

## Required documentation controls

A future Documentation Conformance Tool should:
1. Discover the canonical package and controlled documents.
2. Validate IDs, references, versions and projection metadata.
3. Detect normative-looking instructions without authorized rule references.
4. Detect missing, duplicated, stale or semantically divergent projections.
5. Compare English/French projections without treating either as a second authority.
6. Report unclassified sections and ambiguous normative language as indeterminate.
7. Produce traceable findings by document, section, rule and source revision.
8. Support read-only inspection and a plan before generated-file updates.

Text search can identify candidates but cannot establish semantic equivalence. Semantic review is a separately recorded assurance activity. AI cannot silently promote explanatory prose into binding policy.

## Governance change protocol

Propose a rule/decision change with rationale and authority; validate identity, force, scope, references and composition; obtain approval from the designated authority; update the canonical source; regenerate/update projections; run mechanical drift checks and required semantic review; record exact governance revision and evidence.

Changing Markdown first while leaving the canonical source unchanged is not a valid policy change. An urgent temporary instruction must be approved, scoped, time-bounded and tracked for reconciliation.

## Failure semantics and limits

Missing source, duplicate IDs, unresolved references, ambiguous normative text, contradictory projections or unsupported semantics are not success. Mandatory unresolved cases are indeterminate and fail closed unless a valid bounded exception applies. Bootstrap remains non-destructive: inspect → plan → apply, with reviewable diff and rollback.

Open: canonical format/encoding/signatures; Markdown markers; which sections are generated; implementation language; use of Lean/OPA/Cedar; semantic classifier; need for remote authority. These require focused prototypes.

## Bibliographic references

- [R-09 — Open Policy Agent policy-decision engine](../references.md#r-09)
- [R-10 — Cedar authorization language](../references.md#r-10)
- [R-13 — JSON Schema structural contracts](../references.md#r-13)
- [R-17 — typed governance metadata and traceable relationships](../references.md#r-17)
