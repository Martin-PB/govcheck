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
with the source schema's result status.

The first module deliberately imports no CSLib modules. This isolates the
proposition and gives us a baseline against which candidate CSLib definitions
can later be compared. It does **not** imply that CSLib is unsuitable or that
the assurance obligation for critical mappings is optional.

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
first created. A GitHub Actions build has been configured, but no compilation
or theorem-check result is claimed until its run completes successfully.
A successful Git commit is not a Lean verification result.
