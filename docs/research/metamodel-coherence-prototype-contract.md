# Metamodel coherence prototype contract — first vertical slice

**Status:** proposed engineering contract; not an adopted metamodel or executable Lean development.  
**Date:** 2026-11-11.  
**Parent research:** [Metamodel coherence verification](metamodel-coherence-verification.md).  
**French counterpart:** [Contrat du prototype de cohérence du métamodèle](metamodel-coherence-prototype-contract.fr.md).

## 1. Purpose and boundary

This contract turns the first recommended experiment into falsifiable obligations. It does not attempt to formalize all of SACM, SEON/ReqON, OWL, or GovCheck at once. It tests one initial semantic boundary: **an interoperability mapping must not strengthen the epistemic status of evidence merely by translating it**. This is only the first falsifiable slice of the universal GovCheck requirement: every semantic correspondence used in reasoning must have a verified formal demonstration of the exact relation claimed. This prototype does not discharge the obligation for all other mapping classes.

The prototype is deliberately split into three artifacts:

1. a small Lean semantic core defining evidence kinds, evidence records, mapping contracts and admissible derivations;
2. source fixtures representing SACM-like assurance evidence and GovCheck evidence records, with explicit source identity/revision and provenance;
3. a TLA+ lifecycle abstraction checking when evidence and proof reports remain applicable after source, mapping, assumption or authority changes.

CSLib is a candidate source of reusable definitions/lemmas only after an import-by-import fit assessment. The prototype must compile and prove its own core without relying on unreviewed CSLib translation code. A Lean kernel-checked theorem is the target for the static semantic obligations; CSLib is not itself the trusted kernel and does not supply GovCheck's ontology.

## 2. Minimal semantic vocabulary

The initial Lean model should define at least:

- `EvidenceKind`: `Testimony`, `ModelChecking`, `ProgramVerification`, `TheoremProof`, `Inspection`, `Observation`, and `Other`. These are distinct classes, not a total ranking.
- `EvidenceStatus`: `Passed`, `Failed`, `Inconclusive`, `Unknown`, `Unsupported`, `NotRun`, and `Stale`. Status is not method class.
- `ArtifactRef`: stable artifact identity, exact revision/fingerprint, native format and declared semantic profile.
- `EvidenceRecord`: subject, claim, method class, status, assumptions, scope, provenance, tool/checker identity, bounds where applicable, and invalidation dependencies.
- `MappingContract`: source/target model identities and revisions, direction, coverage class, assumptions, supported constructs, explicit losses, transformation identity and declared preservation obligations.
- `KernelCheckedDerivation`: a derivation checked by the declared proof kernel, with exact premises and conclusion. It is not an ordinary imported report or a string saying `proof=true`.

A mapping's coverage must be one of: `Equivalent`, `SoundDirectional`, `Partial`, `Approximate`, `TraceabilityOnly`, or `Unsupported`. These values are not interchangeable and must not be collapsed into a Boolean.

## 3. First proof obligations

The first Lean development should target the following statements. The names are stable proposal identifiers, not adopted normative rule IDs.

### VC-EPI-01 — Translation does not promote evidence

A transport/mapping operation that only re-expresses a source evidence record preserves its `EvidenceKind`. In particular, a test report remains testimony and a finite model-checking report remains model-checking evidence.

A target theorem-proof record is admissible only if either:
- the source is already a theorem-proof record and the mapping contract proves preservation of its proof identity and dependencies; or
- a separate `KernelCheckedDerivation` is supplied, checked against the exact premises, assumptions, conclusion and kernel identity.

The proof must not rely on an ordering such as “theorem proof is always stronger than model checking”; the classes answer different epistemic questions and are not a single scale.

### VC-EPI-02 — Status is not inferred from method class

No constructor may infer `Passed` from `TheoremProof`, `ModelChecking` from `Passed`, or `Passed` from successful parsing. Method, result status and acceptance decision remain separate fields. A theorem can be false, a proof obligation can be unproved, and a checker can return unknown/error.

### VC-MAP-01 — Provenance preservation

For every supported mapping, source identity, exact source revision/fingerprint, source-native identifier, transformation identity/version and provenance chain are preserved or an explicit loss record is emitted. An absent provenance field must not be silently synthesized.

### VC-MAP-02 — Scope and assumption preservation

A mapped claim/evidence record cannot enlarge its subject scope, temporal validity, environment, assumptions or applicability conditions. A mapping may narrow scope, but must declare that narrowing. Any unresolved scope translation yields `Unknown` or `Unsupported`, never implicit success.

### VC-MAP-03 — Composition

If mapping A→B and B→C both satisfy a declared preservation class, the composed A→C mapping may claim only the strongest preservation class justified by a proved composition law and compatible assumptions. It cannot inherit `Equivalent` merely because both component mappings exist.

### VC-MAP-04 — No silent loss

Every source construct is classified as mapped, preserved natively, explicitly unsupported, or explicitly transformed with a loss/approximation statement. Round-trip tests are necessary but do not alone prove semantic equivalence.

### VC-AUTH-01 — Authority is not amplified

Mapping a decision, approval or delegation cannot increase the principal's authority, domain, target scope, privilege, effective interval or validity. Any unresolved authority translation blocks the dependent transition.

## 4. Adversarial fixtures

The first fixture corpus must include, at minimum:

| Fixture | Expected outcome | Obligation exercised |
|---|---|---|
| Unit test report mapped into an assurance case | Still `Testimony`; never a theorem proof | VC-EPI-01 |
| TLC invariant report mapped into an assurance case | Still `ModelChecking`; bounds/configuration retained | VC-EPI-01 |
| Theorem proof with an unrecorded axiom or admitted goal | Rejected or explicitly marked with trusted-base limitation | VC-EPI-01 / VC-EPI-02 |
| Mapping drops source revision | Fail or explicit loss; never silently pass | VC-MAP-01 |
| Mapping broadens a claim from one component to the whole repository | Fail proof obligation | VC-MAP-02 |
| Two individually valid mappings have incompatible assumptions | Composition is blocked or weakened | VC-MAP-03 |
| Unknown source metaclass is omitted during export | Explicit `Unsupported`/loss report | VC-MAP-04 |
| Delegation mapped with broader scope or later expiry | Fail proof obligation | VC-AUTH-01 |

Positive fixtures are required too: a lossless mapping of a supported evidence record, a valid theorem-proof transfer with dependencies preserved, and a mapping that safely narrows scope.

## 5. Temporal obligations: keep TLA+ in its proper role

TLA+ should model the lifecycle of the evidence/mapping package, not replace the static semantic proofs. Candidate state variables include source revision, mapping revision, assumption revision, proof-bundle revision, status, validity interval, authority revision and invalidation set.

Required temporal properties:

- A change to any declared dependency makes the previous result stale for new acceptance decisions until re-evaluated.
- Historical evidence remains append-only and inspectable.
- A stale proof may be retained as history but cannot authorize a current transition.
- Revoked or expired authority cannot authorize a new mapping adoption.
- `Unknown`, `Unsupported` and `Inconclusive` remain blocking under the closed-world failure policy; no missing result defaults to success.
- A new proof result is bound to the exact source, mapping, assumption and checker revisions it checked.

TLC results remain bounded model-checking evidence for the stated finite abstraction. General semantic preservation belongs in Lean proofs; implementation conformance requires a separate refinement/conformance argument.

## 6. CSLib assessment protocol

Do not decide “CSLib mandatory” by reputation or breadth. For each candidate import:

1. identify the exact CSLib commit and Lean toolchain;
2. inspect the definition and all transitive dependencies;
3. identify axioms, `sorry`, `admit`, `unsafe`, native/oracle boundaries and generated translation code;
4. decide whether the definition matches GovCheck's intended semantics, not merely its name;
5. prove a small bridge theorem from the imported definition to the GovCheck contract;
6. record the trusted base and reproducible build command.



### Current CSLib/toolchain compatibility constraint

The inspected CSLib main commit is `f8acdb37c713b0124ad36b863f50c200a5f1cdba`, which pins Lean 4.36.0-rc2 and Mathlib commit `887bb849a9f64e1c66499fd5ff8523c864e78941`. This prototype pins Lean 4.19.0. A direct dependency therefore cannot be added without a toolchain change. The next experiment must either identify a CSLib revision compatible with Lean 4.19 or isolate a separate CSLib-backed profile with its own pinned toolchain. Do not silently upgrade the verified core.

If CSLib provides a sound and reusable formalization for a required semantic concept, reuse should be preferred to an independent duplicate. If it does not, define the smallest GovCheck-specific concept and prove its relation to the relevant source model. **The formal-demonstration obligation applies to every semantic correspondence used in GovCheck reasoning, not only to mappings labelled critical.** The library, proof assistant and verifier choices remain evidence-driven and must satisfy the declared trusted-base requirements.

## 7. Prototype completion gate

The first slice is complete only when:

- the Lean project builds from a pinned toolchain;
- the positive theorems are kernel-checked with no unreviewed axioms/admissions;
- each adversarial fixture is rejected for the expected reason;
- at least one deliberately invalid mapping produces a concrete counterexample or failed proof obligation;
- source revisions, assumptions, provenance and proof dependencies are preserved;
- a bounded TLA+ model demonstrates stale-evidence rejection after dependency change;
- the evidence bundle records exact commits, commands, outputs, limits and trusted base;
- the distinction among proof, model checking, validation, test testimony and acceptance is machine-readable.

No implementation should claim that this gate has passed until the Lean build, fixture runner and TLC run have actually been executed and their outputs recorded.



## 9. Existing evidence-schema boundary (explicit gap)

The current `formal/schemas/evidence-record.schema.json` defines `method.methodClass` and `result.status`, but it has no separate typed `epistemicKind` field and no dedicated typed kernel-checked derivation object. The Lean `EvidenceKind` in the prototype is therefore an **additional semantic interpretation**, not a lossless field-for-field projection of the current JSON schema.

Consequences:

- `methodClass = theorem-proving` plus `status = passed` is not enough to infer `EvidenceKind.theoremProof`.
- A method label and a result status cannot authenticate a derivation. The exact theorem statement, premises, assumptions, kernel/checker identity and version, imports, axioms, admitted obligations, unsafe features and oracle boundaries must be bound to a verifiable derivation artifact.
- Until a typed mapping/extension is authorized, a schema record without that derivation must map to an unresolved/non-proof epistemic classification; it must not be promoted to theorem proof.
- The small JSON files under `formal/lean/fixtures/` are **semantic fixtures**, not complete records valid against the production evidence JSON Schema. They must not be fed to the schema validator as if they were production fixtures.

This is a concrete cross-artifact gap for #73/#79, not authorization to change the production schema. A later decision must choose whether epistemic kind and derivation metadata belong in the core record, a typed extension, or a separately referenced proof artifact, and specify round-trip behavior.

## 10. Decision still reserved

This contract is a proposed experiment. It does not select Lean/CSLib as a universal adopter dependency, does not adopt a GovCheck ontology, does not replace SACM's native semantics, and does not authorize a downgrade of proof obligations. The universal obligation to prove every semantic correspondence used in reasoning is a settled design requirement for this proposal; the authority still has to decide the trusted verifier, proof profile, packaging, reproducibility and distribution model after reviewing the prototype's actual cost, coverage and trusted base.


## Actual prototype outcomes

The Lean 4.19.0 core passed its build and theorem axiom audit in [PR #108 run 43049890363](https://github.com/Martin-PB/govcheck/actions/runs/43049890363). A separate CSLib LTS experiment on Lean 4.36.0-rc2 passed build and theorem axiom audit in [PR #109 run 43052136331](https://github.com/Martin-PB/govcheck/actions/runs/43052136331). The CSLib experiment proves preservation of method class and epistemic kind over individual transitions and finite LTS executions. It remains an abstract lifecycle model, not an external ontology mapping proof. Both PRs remain unmerged; PR #109 is stacked on PR #108.

The schema ambiguity is no longer only a prose observation: the Lean core includes `schema_method_and_status_do_not_determine_epistemic_kind`, which constructs two records with identical `methodClass=theorem-proving` and `status=passed` but different epistemic kinds. The theorem compiled and its axiom report showed no axiom dependencies in [run 43053084946](https://github.com/Martin-PB/govcheck/actions/runs/43053084946), tested code head `5599a3efcddcadeb6b80465c360d180f803b902b).