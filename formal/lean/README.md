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

## Mapping contract

`GovCheckCoherence.Mapping` binds a source and target claim identifier to Lean propositions and declares the mapping coverage (`equivalent`, `soundDirectional`, `partial`, `approximate`, `traceabilityOnly`, `unsupported`). The corresponding `SemanticBridge` constructor requires the proof obligation appropriate to that coverage. A mapping also binds exact source/target model revisions and requires preservation of the evidence source identity/revision, exact scope, all source assumptions, and method class.

A new theorem-proof kind requires a `KernelCheckedDerivation` containing an actual Lean proof term of the exact target proposition. A method label or result status cannot construct this proof object. Target result status is deliberately independent: derivation of a new theorem has its own result, not an automatic copy of a source test status.

The first profile requires exact scope equality; it does not yet define a scope partial order or safe scope narrowing. The contract is a typed obligation, not proof that any production importer/exporter satisfies it.

## Explicit limits

This is not yet a complete mapping-contract semantics. In particular, it does
not authenticate an imported theorem proof, bind a derivation to exact
premises/conclusion/axioms/kernel identity, prove source-model semantic
preservation, validate SACM serialization, establish provenance, or check
freshness and authority scope. Those are separate obligations.

The `DerivationOrigin.kernelChecked` constructor currently expresses the
gate that a new derivation must be supplied; it is not yet a proof-object
type. The next refinement must replace it with a typed derivation object whose
exact statement is kernel checked and whose dependency set is bound to source
fingerprints.

## Verification status

The authoring environment did not have Lean installed when this package was
first created. The Lean 4.19.0 build and axiom audit passed: [GitHub Actions run 43049890363](https://github.com/Martin-PB/govcheck/actions/runs/43049890363), source head `473ff33c74c8c04b4766b52de20ac68a9fb20d9b`. The workflow explicitly builds the `GovCheckCoherence` library, audits the theorem module with `leanprover-community/axiom-audit`, and prints each theorem's axiom dependencies. The audit checked 10 declarations under `GovCheckCoherence.Proofs`; all were within the configured standard allowlist. The explicit `#print axioms` report showed that all nine theorem declarations in this slice depend on no axioms. This is a result about this small formal slice only: it is not yet a semantic mapping proof against SACM/OWL/SEON, proof of imported-source fidelity, or implementation conformance. A successful Git commit alone is not a Lean verification result.
