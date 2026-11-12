# Metamodel coherence prototype — execution record

**Status:** first executable slice built; finite lifecycle abstraction model-checked.  
**Date:** 2026-11-12.  
**Related work:** issue [#73](https://github.com/Martin-PB/govcheck/issues/73), [prototype contract](metamodel-coherence-prototype-contract.md), [English/French verification report](metamodel-coherence-verification.md).

## 1. What has actually been executed

### Lean epistemic core

- Source: `formal/lean/GovCheckEpistemic/Evidence.lean`
- Toolchain: Lean 4.19.0, pinned in `formal/lean/lean-toolchain`.
- Workflow: `Lean epistemic core`.
- Successful run: [43209380453](https://github.com/Martin-PB/govcheck/actions/runs/43209380453).
- Result: `lake update` and `lake build` completed successfully.

The core separates evidence method class from result status and represents a mapping as either same-kind transport or a distinct theorem-proving derivation backed by an explicit `KernelCheckedDerivation`. The checked declarations establish transport kind preservation, the admissible routes to a theorem-proving result, and status preservation.

**Scope limit:** this is a kernel-checked result about the definitions in this Lean module. It does not prove that the definitions are the final GovCheck semantics, that a SACM mapping is correct, or that an importer/exporter conforms to the model.

### TLA+ evidence freshness model

- Source: `formal/tla/GovCheckEvidenceFreshness.tla`
- Configuration: `formal/tla/GovCheckEvidenceFreshness.cfg`
- Toolchain: SANY 2.1, TLC 2.19, tla2tools 1.7.4 (checksum pinned), Temurin Java 17.
- Successful run: [43209535512](https://github.com/Martin-PB/govcheck/actions/runs/43209535512).
- Result: SANY parsed the model; TLC found no counterexample in the finite configured state space.
- Exploration: 132 states generated, 20 distinct states, 0 remaining, depth 4.
- Checked invariants: `TypeOK`, `AcceptedImpliesFresh`, `NonPassingEvidenceCannotBeAccepted`.

This is bounded model-checking evidence for a two-revision abstraction, not a theorem proof and not a proof of implementation conformance.

## 2. A useful counterexample was found and corrected

The first TLC execution found a real model defect: `ReevaluateEvidence` could change an already accepted evidence result to `Failed` while leaving `accepted = TRUE`. TLC produced the trace:

1. initial evidence at revision v0 is Passed;
2. source revision changes to v1;
3. evidence is re-evaluated at v1 and remains Passed;
4. the evidence is accepted;
5. re-evaluation changes its status to Failed without clearing acceptance.

The invariant `NonPassingEvidenceCannotBeAccepted` failed. The transition was corrected so every re-evaluation clears the previous acceptance decision. The subsequent TLC run completed without counterexample.

This illustrates the intended distinction: the first run was not “a failed proof”; it was a bounded model-checking counterexample exposing an inconsistency in the transition model. The corrected run provides bounded evidence only for the corrected finite model.

## 3. Integration and repository governance

- Both verification workflows are explicitly classified as meta-level-only in `scripts/check-package-alignment.py`; they are not copied into the adopter template package.
- The Lean core and TLA+ model are registered in `formal/artifacts.json`, including exact toolchain, run, commit, result, bounds and limitations.
- The prototype is tracked on [PR #115](https://github.com/Martin-PB/govcheck/pull/115).
- The original decision/research dossier remains on [PR #106](https://github.com/Martin-PB/govcheck/pull/106).

## 4. Remaining proof and validation gaps

The current results do not yet establish:

- preservation of provenance, source revision, assumptions and claim scope across actual mappings;
- safe composition of mappings or conservativity with respect to source ontologies;
- authority-preserving translation of approvals and delegations;
- SACM 2.4 Beta 1 semantic coverage or lossless XMI/XML round-tripping;
- conformance of executable parsers, serializers or repository enforcement to the Lean model;
- unbounded temporal properties beyond the finite TLC configuration;
- whether CSLib definitions should be imported for any specific obligation.

Next, extend the Lean core and fixtures from epistemic non-promotion to provenance and scope preservation. Then test a concrete SACM-to-GovCheck mapping against native SACM semantics, and audit CSLib imports by exact definition, commit, transitive dependencies and trusted base. Do not generalize this small success into a claim that the metamodel as a whole is coherent.
