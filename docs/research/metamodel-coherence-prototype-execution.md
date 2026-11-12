# Metamodel coherence prototype — integrated execution record

**Status:** proof-carrying mapping contract added to the existing Lean coherence core; Lean build and axiom audit passed. CSLib compatibility probe separately verified.  
**Date:** 2026-11-12.  
**Related work:** issue [#73](https://github.com/Martin-PB/govcheck/issues/73), [metamodel coherence research](https://github.com/Martin-PB/govcheck/blob/docs/metamodel-decision-dossier-2026-11/docs/research/metamodel-coherence-verification.md), [SACM 2.4 integration proposal](../architecture/0026-sacm-24-conformance-and-govcheck-integration.md).

## 1. Integration strategy

The initial evidence-coherence slice was already merged to `main` by PR #108. The CSLib LTS experiment was developed on its stacked branch by PR #109. This work extends the existing `GovCheckCoherence` package rather than introducing a competing Lean package or a second definition of evidence kind.

The existing core keeps three independent dimensions:

- `EvidenceMethodClass`: how the evidence was produced;
- `EvidenceKind`: what epistemic nature the evidence has (testimony, model-checking result, theorem proof, etc.);
- `EvidenceStatus`: the outcome of the method.

The current production schema has method class and result status but no explicit epistemic-kind or typed derivation field. The Lean kind is therefore an additional assurance interpretation, not a lossless projection of the current JSON schema. The existing theorem `schema_method_and_status_do_not_determine_epistemic_kind` captures that gap.

## 2. Proof-carrying mapping contract

The integrated Lean 4.19.0 build and axiom audit passed in [run 43212610129](https://github.com/Martin-PB/govcheck/actions/runs/43212610129), checked commit `b6c4bd8aff7e80b9921361529a46f01f14ed6468`. The explicit axiom report states that each of the seven new mapping theorem declarations depends on no axioms.

Added `formal/lean/GovCheckCoherence/Mapping.lean`, imported by the existing `GovCheckCoherence` library and theorem axiom report.

The contract introduces:

- `ArtifactRef`: stable identity, exact revision, native format and semantic profile;
- `ClaimSemantics`: stable claim identifier bound to a Lean proposition;
- `MappingSubject`: evidence record, interpreted claim, provenance artifact, semantic model revision, scope and assumptions;
- `MappingCoverage`: equivalent, sound-directional, partial, approximate, traceability-only and unsupported;
- `SemanticBridge`: coverage-indexed proof obligations (equivalence, directional implication, domain-restricted partial preservation, explicit approximate relation, or traceability/unsupported declaration);
- `KernelCheckedDerivation`: an actual Lean proof term of the exact target proposition, plus provenance metadata;
- `EvidenceMapping`: exact source/target model binding, method-class preservation, typed epistemic-kind rule, provenance identity/revision preservation, exact scope preservation and retention of source assumptions.

A new theorem-proof kind cannot be obtained merely by changing a label. The mapping rule either carries an existing theorem-proof kind or supplies a `KernelCheckedDerivation` containing a proof term of the target claim. Target result status remains independent; a newly derived theorem has its own result status rather than automatically inheriting the source test's `passed` status.

The first profile deliberately requires exact scope equality. It does not yet define a scope partial order or permit scope narrowing. The `premises`, `assumptions`, `kernelIdentity` and `kernelVersion` fields on a derivation are currently metadata; the proof term itself is kernel checked, but those metadata are not yet mechanically tied to its transitive dependency closure.

## 3. Evidence status alignment

The existing evidence-record schema distinguished `unknown` and `inconclusive` in the TLA assurance model but did not expose `unknown` in the JSON status enum. The schema, its governed-package copy, bilingual status documentation and synthetic fixture now include `unknown`.

- `unknown`: no determinate result is available from the current inputs;
- `inconclusive`: a method ran, but did not establish pass or fail;
- `stale`: not a result status; it is derived separately from revision dependencies, expiry and invalidation.

The Lean `EvidenceStatus` now includes `unknown`. A synthetic `evidence-record-unknown.example.json` fixture exists at both meta and package levels.

## 4. Temporal lifecycle: reuse the existing model

No duplicate freshness model was added. The existing `formal/tla/GovCheckAssurance.tla` already models evidence outcomes including `Unknown`, stale evidence caused by dependency revision mismatch, expiry and revocation, claim status, independent review, acceptance and accepted dependency snapshots. Its `AcceptedImpliesSupported` and `AcceptedDependencySnapshotCurrent` invariants are the appropriate existing temporal foundation.

TLC remains bounded model-checking evidence for its configured finite model. It does not prove the static semantic bridge between two ontologies; that is the purpose of the Lean mapping contract.

## 5. CSLib compatibility result

An isolated package under `formal/cslib-compat/` was built against exact CSLib commit `70e25828d89a3916e41c9d84cfffd7e6093bb1a0`, Lean `4.36.0-rc2` and CSLib's pinned Mathlib revision. [Run 43210543930](https://github.com/Martin-PB/govcheck/actions/runs/43210543930) completed 1,779 build jobs and checked the BTL model/satisfaction API plus omega-sequence `Step` and `LeadsTo`.

This establishes API/build compatibility in an isolated package only. It does not prove a GovCheck↔CSLib semantic refinement and does not change the existing Lean 4.19.0 core toolchain. See the bilingual [CSLib compatibility audit](cslib-compatibility-audit.md) / [audit français](cslib-compatibility-audit.fr.md).

## 6. Remaining obligations

The current contract does not yet prove:

- that source-native SACM 2.4 Beta 1, OWL or SEON/ReqON semantics are correctly interpreted by the supplied Lean propositions;
- that real parsers, serializers or import/export adapters construct only valid `EvidenceMapping` values;
- conservative extension/non-interference for source ontologies;
- mapping composition and transitive assumption/provenance preservation;
- scope narrowing under a formally defined scope order;
- binding of derivation metadata to the proof term's complete dependency closure;
- authority/delegation preservation across actual model mappings.

The next concrete vertical slice should bind one small SACM assurance concept and one GovCheck evidence claim to source-native identifiers, formal interpretations and a typed `SemanticBridge`; then prove the mapping law and test deliberate invalid mappings. Do not generalize the small Lean and CSLib build results into a claim that the whole metamodel is coherent.
