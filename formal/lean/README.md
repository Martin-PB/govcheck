# Lean/CSLib coherence experiment

**Status:** stacked experiment against PR #108; not an adopted GovCheck toolchain or metamodel.

## Purpose

This branch tests whether CSLib's formal transition-system abstractions can support GovCheck's evidence lifecycle semantics. It is intentionally separate from the Lean 4.19.0 core in PR #108.

## Pinned compatibility profile

- Lean: `4.36.0-rc2`
- CSLib: commit `f8acdb37c713b0124ad36b863f50c200a5f1cdba`
- CSLib's Mathlib dependency: commit `887bb849a9f64e1c66499fd5ff8523c864e78941`

The exact CSLib commit is pinned in `lakefile.lean`; the toolchain is pinned in `lean-toolchain`. This experiment must not silently change the independently verified Lean 4.19.0 profile from PR #108.

## Experiment

`GovCheckCoherence.CslibBridge` models evidence lifecycle changes as a CSLib labelled transition system (LTS). It keeps method class, epistemic kind and result status distinct, while representing freshness separately. The theorem module tests:

- each transition preserves method class;
- each transition preserves epistemic kind;
- any finite LTS execution preserves epistemic kind end-to-end.

This is a proof of the stated abstract transition relation, not yet proof that an external SACM/OWL/SEON mapping or a runtime implementation refines it. CSLib contributes LTS and multistep-transition foundations; it does not provide a general ontology-alignment system or a model checker equivalent to TLC.

The lifecycle record uses the additional Lean `EvidenceKind` semantic interpretation from PR #108. The current production JSON Schema has no such explicit field and no typed kernel-checked derivation object, so these are not lossless schema projections or schema-valid production fixtures. The core now includes a kernel-checked counterexample showing that two records with the same method class and status can have different epistemic kinds. That gap is recorded in the bilingual prototype contract; no production schema change is made here.

## Commands

From this directory:

```sh
lake update
lake build GovCheckCoherence
lake env axiom-audit --root GovCheckCoherence.Proofs
lake env lean GovCheckCoherence/AxiomReport.lean
```

The GitHub Actions workflow runs the build and theorem-module axiom audit. Results are recorded only after the actual run completes.

## Decision boundary

This experiment does not authorize upgrading GovCheck's primary proof profile to Lean 4.36.0-rc2. The authority should compare the compatibility cost, proof reuse and maintenance burden against a Lean 4.19-compatible historical CSLib revision before selecting any mandatory toolchain.
