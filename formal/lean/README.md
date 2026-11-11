# Lean coherence prototype

**Status:** experimental first slice; not an adopted GovCheck metamodel.

## Scope

This package formalizes one narrow cross-model invariant: pure evidence
transport cannot promote the epistemic nature of an evidence record. The
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
JSON Schema. See the bilingual prototype contract for this identified #73/#79
decision gap.

## Toolchain and commands

Pinned toolchain: Lean 4.19.0.

From this directory:

```sh
lake env lean GovCheckCoherence.lean
lake build
```

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
