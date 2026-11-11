# Lean coherence prototype

**Status:** experimental first slice; not an adopted GovCheck metamodel.

## Scope

This package formalizes one narrow cross-model invariant: a pure evidence
transport operation cannot promote test testimony or model-checking evidence
into a theorem-proof record. Evidence method class and result status are
separate dimensions.

The first module deliberately uses only Lean's core language and imports no
CSLib modules. This isolates the proposition and gives us a baseline against
which candidate CSLib definitions can later be compared. It does **not** imply
that CSLib is optional for critical obligations or unsuitable for reuse.

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

The theorem `new_theorem_proof_requires_kernel_derivation` currently checks
only the explicit gate represented by `DerivationOrigin.kernelChecked`.
The next refinement must replace this Boolean-like tag with a typed derivation
object whose exact statement is kernel checked and whose dependency set is
bound to source fingerprints.

## Verification status

No Lean executable was available in the authoring environment when this
package was added. Therefore no compilation or theorem-check result is
claimed. A successful Git commit is not a Lean verification result.
