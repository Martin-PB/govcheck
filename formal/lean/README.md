# Lean coherence prototype

**Status:** experimental first slice; not an adopted GovCheck metamodel.

## Scope

This package formalizes the first evidence-coherence invariants and a proof-carrying cross-model mapping contract. It keeps `EvidenceMethodClass`, `EvidenceKind` and `EvidenceStatus` as separate dimensions. The
Lean vocabulary mirrors the existing GovCheck evidence schema's
`methodClass` values and result-status values, while keeping the epistemic
kind explicit and separate.

This distinction matters: a record labelled with method class
`theorem-proving` and status `passed` is not, by those labels alone, an
authenticated kernel-checked derivation. A test execution with status
`passed` remains testimony; a model-checking result remains model-checking
evidence. Freshness/staleness is computed separately and is not conflated
with the source schema's result status. The source schema's method-class
vocabulary is represented directly by `EvidenceMethodClass`; the epistemic
kind is an additional assurance interpretation, not a replacement enum.

The first module deliberately imports no CSLib modules. This isolates the
proposition and gives us a baseline against which candidate CSLib definitions
can later be compared. It does **not** imply that CSLib is unsuitable or that
the assurance obligation for critical mappings is optional.

The Lean `EvidenceKind` is an additional semantic interpretation: the current
production `evidence-record.schema.json` has `method.methodClass` and
`result.status`, but no explicit epistemic-kind field or typed kernel-checked
derivation object. Therefore the Lean record is not a lossless projection of
the current JSON schema. The fixtures under `fixtures/` are intentionally
minimal semantic fixtures, **not** full production records valid against the
JSON Schema. The theorem `schema_method_and_status_do_not_determine_epistemic_kind`
constructs two semantic interpretations with identical method class and
status but different epistemic kinds; this is a formal counterexample to
inferring epistemic kind from the current schema dimensions. See the bilingual
prototype contract for this identified #73/#79 decision gap.

## Toolchain and commands

Pinned toolchain: Lean 4.19.0.

From this directory:

```sh
lake env lean GovCheckCoherence.lean
lake build
```

## SACM 2.4 Beta 1 semantic slice

`GovCheckCoherence.SACM24` preserves SACM assertion-declaration distinctions, binds explicit Claim subjects to exact model revisions, and types inference direction. The `probable` inference kind has no classical implication bridge; `byRule` requires a concrete proof term. The thirteen public SACM mapping theorems passed the pinned Lean 4.19.0 build and axiom audit in [run 43215132423](https://github.com/Martin-PB/govcheck/actions/runs/43215132423) with no axioms. See the bilingual [SACM 2.4 mapping study](../../docs/research/sacm24-claim-inference-mapping.md) / [étude française](../../docs/research/sacm24-claim-inference-mapping.fr.md).

## Mapping contract

The status model also proves `unknown_status_is_distinct_from_inconclusive`; both statuses are represented in the JSON Schema, while staleness remains a separate freshness property.

`GovCheckCoherence.Mapping` binds a source and target claim identifier to Lean propositions and declares the mapping coverage (`equivalent`, `soundDirectional`, `partial`, `approximate`, `traceabilityOnly`, `unsupported`). The corresponding `SemanticBridge` constructor requires the proof obligation appropriate to that coverage. A mapping also binds exact source/target model revisions and requires preservation of the evidence source identity/revision, exact scope, all source assumptions, and method class.

A new theorem-proof kind requires a `KernelCheckedDerivation` containing an actual Lean proof term of the exact target proposition. A method label or result status cannot construct this proof object. Target result status is deliberately independent: derivation of a new theorem has its own result, not an automatic copy of a source test status.

The first profile requires exact scope equality; it does not yet define a scope partial order or safe scope narrowing. The `DerivationOrigin.kernelChecked` predicate from the original PR #108 slice remains a coarse abstract placeholder; it is not a proof object and must not be used as the proof-carrying route for new mappings. New mappings use `KindMappingRule` and `KernelCheckedDerivation`. The contract is a typed obligation, not proof that any production importer/exporter satisfies it.

## Explicit limits

This is not yet a complete metamodel coherence proof. In particular, it does
not prove that a production importer/exporter constructs valid mapping values,
that a source-native SACM/OWL/SEON interpretation is correctly bound to the
Lean propositions, that mappings compose conservatively, or that an external
implementation refines the formal contract. Freshness and temporal authority
remain governed by the repository's TLA+ models and require a separate
conformance argument.

The proof term is checked by the pinned Lean kernel, but the `premises`,
`assumptions`, `kernelIdentity` and `kernelVersion` fields are currently
metadata and are not yet mechanically linked to the proof term's dependency
closure. Claim identifiers are paired with Lean propositions in the mapping
subject, but no production parser has yet been proven to preserve that binding.
The `approximate` coverage constructor records a relation and declared
limitations; it does not assert a sound semantic refinement.

## Verification status

The authoring environment did not have Lean installed when this package was
first created. The extended proof-carrying mapping contract also passed the
pinned Lean 4.19.0 build and axiom audit in [run 43213158225](https://github.com/Martin-PB/govcheck/actions/runs/43213158225); all fourteen mapping helper/public theorem declarations and the separate status-distinction theorem reported no axioms. The Lean 4.19.0 build and axiom audit passed: [GitHub Actions run 43049890363](https://github.com/Martin-PB/govcheck/actions/runs/43049890363), source head `473ff33c74c8c04b4766b52de20ac68a9fb20d9b`. The workflow explicitly builds the `GovCheckCoherence` library, audits the theorem module with `leanprover-community/axiom-audit`, and prints each theorem's axiom dependencies. The audit checked 10 declarations under `GovCheckCoherence.Proofs`; all were within the configured standard allowlist. The explicit `#print axioms` report showed that all nine theorem declarations in this slice depend on no axioms. This is a result about this small formal slice only: it is not yet a semantic mapping proof against SACM/OWL/SEON, proof of imported-source fidelity, or implementation conformance. A successful Git commit alone is not a Lean verification result.
