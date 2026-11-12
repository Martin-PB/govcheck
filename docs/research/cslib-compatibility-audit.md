# CSLib compatibility and semantic-fit audit

**Audit date:** 2026-11-12  
**Repository:** [leanprover/cslib](https://github.com/leanprover/cslib)  
**Inspected commit:** `70e25828d89a3916e41c9d84cfffd7e6093bb1a0`  
**GovCheck Lean core:** Lean 4.19.0

## 1. Executive finding

CSLib is relevant to GovCheck's formalization problem, but its strongest demonstrated fit is **formal semantics of systems and temporal/transition reasoning**, not a ready-made ontology-alignment or evidence-governance metamodel.

The inspected CSLib HEAD is not directly compatible with the current GovCheck Lean project: CSLib pins `leanprover/lean4:v4.36.0-rc2`, while the GovCheck epistemic core pins Lean 4.19.0. CSLib also pins Mathlib at `887bb849a9f64e1c66499fd5ff8523c864e78941`. Do not add CSLib as a dependency to the Lean 4.19 package without a deliberate toolchain migration or a separately isolated compatibility project.

## 2. Relevant formalizations found

| CSLib area | Inspected module | Relevance to GovCheck | Boundary |
|---|---|---|---|
| Basic Temporal Logic (BTL) | `Cslib/Logics/BTL/Basic.lean` | Future/past modalities, model/frame semantics, satisfaction relation, temporal properties | BTL is a basic modal temporal language with F/P; it is not automatically equivalent to every LTL formalism |
| Infinite sequences | `Cslib/Foundations/Data/OmegaSequence/Temporal.lean` | `Step`, `LeadsTo`, transitivity and recurring/eventual properties over infinite executions | Useful for temporal lifecycle claims; requires an explicit mapping from GovCheck state traces |
| Labelled transition systems | `Cslib/Foundations/Semantics/LTS/Basic.lean` | State transitions, finite traces, boundedness, termination, finite-state properties | Good foundation for operational semantics; not a governance ontology |
| Modal semantics | `Cslib/Logics/Modal/Semantics.lean` | Models, frames, valuations and satisfaction semantics | A formal semantic substrate, not a mapping specification for SACM/OWL/SEON |

The BTL source explicitly leaves the accessibility relation unconstrained by default: reflexivity determines whether the present is included, and transitivity determines whether the relation models a flow of time. GovCheck would therefore have to state and prove the frame assumptions appropriate to each lifecycle property; importing BTL alone does not supply them.

## 3. Compatibility finding

At inspected HEAD:

- CSLib Lean toolchain: `leanprover/lean4:v4.36.0-rc2`.
- CSLib Mathlib dependency: exact Git revision `887bb849a9f64e1c66499fd5ff8523c864e78941`.
- GovCheck epistemic core: Lean 4.19.0.

Consequences:

1. The current CSLib HEAD cannot be imported into the existing Lean 4.19 Lake package as-is.
2. A toolchain upgrade to a release candidate solely to consume CSLib would be an unjustified coupling at this stage.
3. A separate compatibility package could test CSLib on its pinned toolchain without changing the trusted build of the GovCheck semantic core.
4. Alternatively, a historical CSLib commit compatible with Lean 4.19 could be investigated, but it must be identified from repository history and tested—not guessed.

## 4. Preliminary trusted-base source scan

A repository code-search pass at the inspected commit found:

- no indexed matches for `sorry`;
- no indexed matches for `run_tac`, `implemented_by` or `extern`;
- matches for `axiom` primarily describe axioms as objects of the modal/propositional logics being formalized, rather than Lean kernel axioms;
- matches for `unsafe` were in test comments, not identified declarations;
- several `opaque` declarations are type tags such as `InferenceSystem.Default`, `MLL` and `ND`, not by themselves evidence of an unsound proof boundary.

This is a preliminary search, not a trusted-base certification: GitHub code search is not a complete static audit, and transitive Mathlib dependencies and generated/compiled artifacts still need inspection. The isolated build is the next step; before importing any definition into a critical GovCheck theorem, inspect the full transitive dependency closure and audit its axioms with Lean's `#print axioms` or an equivalent reproducible audit.

## 5. Does CSLib solve the metamodel coherence problem?

No single CSLib module inspected provides the missing GovCheck-specific semantics for:

- evidence method class versus result status and acceptance;
- provenance and source revision preservation across mappings;
- semantic coverage classes and explicit information loss;
- scope/assumption preservation;
- authority and delegation non-amplification;
- conservative extension or non-interference when adding GovCheck concepts to source ontologies;
- SACM 2.4 Beta 1 import/export fidelity.

Lean remains the proof assistant and kernel-checking environment in which GovCheck can state these obligations. CSLib can provide reusable formal definitions for selected mathematical structures and semantic machinery. It is not a substitute for the GovCheck bridge contracts.

## 6. Recommended integration strategy

Do not add CSLib to the core package yet. Instead:

1. Keep the small epistemic core on its pinned Lean 4.19 toolchain while it remains dependency-free.
2. Create a separate, isolated CSLib compatibility experiment pinned to the exact CSLib commit and its Mathlib revision.
3. Formalize one GovCheck lifecycle property in the GovCheck core and one in CSLib's BTL or `ωSequence` setting.
4. State an explicit semantic relation between the two representations and prove preservation in both directions where equivalence is claimed; otherwise declare the direction and coverage precisely.
5. Compare the CSLib result with the existing TLA+ model. Do not treat translation between TLA+ and Lean/CSLib as trusted unless its semantic preservation is established.
6. Only after the experiment succeeds should we decide whether CSLib is a direct dependency, an isolated proof backend, or simply a reference formalization.

## 7. Conclusion

CSLib should be treated as a serious candidate formalization library for lifecycle semantics, transition systems, temporal reasoning and related computer-science theories. The inspected current HEAD is not a drop-in dependency for GovCheck's Lean 4.19 core, and it does not provide the ontology-mapping guarantees GovCheck needs.

A separately pinned compatibility probe is now present under `formal/cslib-compat/`; it imports BTL and infinite-sequence temporal modules without changing the GovCheck core toolchain. Its CI result is pending. This is an API/build compatibility experiment, not a semantic refinement proof. It is not a toolchain upgrade of the GovCheck core and does not imply that temporal logic alone establishes static metamodel coherence.
