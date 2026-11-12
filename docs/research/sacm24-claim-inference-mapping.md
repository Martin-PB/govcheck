# SACM 2.4 Beta 1 — first semantic mapping slice

**Status:** source-native semantic slice formalized in Lean; Lean build and axiom audit passed in [run 43215882124](https://github.com/Martin-PB/govcheck/actions/runs/43215882124).  
**Source baseline:** OMG SACM 2.4 Beta 1, September 2026; normative metamodel XML dated 2026-05-04.  
**Reference:** [R-73](../references.md#r-73).  
**Related formalization:** [GovCheckCoherence.SACM24](../../formal/lean/GovCheckCoherence/SACM24.lean).

## 1. Why this is the first source-native slice

SACM 2.4 Beta 1 introduces semantics directly relevant to GovCheck's epistemic model. An independent implementation audit ([R-128](../references.md#r-128)) also finds contradictions between the specification PDF text and the machine-readable metamodel XML; see the [interoperability-risk report](sacm24-beta1-interoperability-risk.md). The formal slice therefore distinguishes source views rather than treating Beta 1 as one coherent schema:

- an explicit subject for a Claim (issue SACM24-83);
- extended AssertionDeclarationKind values and assertion-value structures;
- richer InferenceTypeKind values, including probable, collective, necessary, sufficient, necessaryAndSufficient and byRule;
- AssertionRule and InferenceRule hooks for user-defined semantics;
- assessment-related constructs (issue SACM24-75) and advanced arguments (issue SACM24-77).

This makes SACM a useful falsification target: a GovCheck mapping must preserve distinctions that SACM itself makes, rather than flattening all assertion/inference content into a generic claim/evidence edge.

## 2. Assertion declaration is not evidence status or theorem proof

The Lean slice models the union of AssertionDeclarationKind literals found across the two source views:

| SACM declaration | GovCheck disposition | What it does **not** mean |
|---|---|---|
| `asserted` (PDF and XML) | `asserted` | Not a passed test or proof |
| `assumed` (PDF and XML) | `assumed` | Not evidence that the proposition is true |
| `axiomatic` (PDF and XML) | `axiomaticDeclared` | Not a Lean-kernel-checked theorem proof |
| `needsSupport` (PDF text only) | `needsSupport` | Not a rule declaration; rejected for the XML source view |
| `byRule` (metamodel XML only) | `ruleDeclared` | Not a validated rule; rejected for the PDF text source view |

The mapping is injective across the union of the two source views: no declaration literal collapses into another GovCheck disposition. The `SourceView` field selects PDF text or normative metamodel XML; a typed predicate rejects `byRule` for the text view and `needsSupport` for the XML view. The same source-view selection pins `gid` (PDF text) versus `elementId` (metamodel XML). The end-to-end `SACMClaimMapping` carries the source claim interpretation, declaration disposition, exact source model and general `EvidenceMapping` semantic bridge.

SACM's optional `isTrue`, `assertionValue`, and `assertionRule` fields remain distinct from declaration kind. In the current Lean slice, the latter two are retained as opaque source payload/reference strings, not yet formalized as their complete SACM metaclasses. An optional Boolean truth value is not a proof object; an assertion value may encode a richer value than Boolean; and a rule reference is not the rule's formal semantics. The Lean record retains these fields separately.

**Critical non-promotion rule:** SACM `axiomatic` must remain an explicit source-declared axiom/assumption in the trust ledger. It cannot be promoted to GovCheck `theoremProof` without an independent Lean proof term and a separate trusted-base/axiom audit.

## 3. Claim subject and formal interpretation

The Lean slice defines a `SACMElementRef` with source identity field, metaclass and model revision. `SACMClaim` carries its source view and identity-field choice. `SACMClaimInterpretation` cannot be constructed unless the declaration literal and identity field are consistent with that selected source view; it binds:

- the exact SACM claim identity to the GovCheck claim identifier;
- the optional explicit SACM subject to the mapped subject;
- the subject reference to the exact source model revision;
- a separately supplied Lean proposition as the formal interpretation.

The `Claim.value` PDF/XML type mismatch is not flattened: the current Lean field is an opaque raw value placeholder, not a formalization of either `MultiLangString` or `ExpressionLangString`. This is intentionally not an automatic conversion of SACM's text/value into Lean logic. The mapping authority must supply and justify the proposition interpretation. The current formal contract checks identity and subject/revision preservation, but does not prove that a human-language claim's chosen proposition is semantically faithful to its text. That remains an explicit interpretation argument and assurance obligation.

## 4. Inference types and directionality

The Lean model formalizes the deterministic fragment with explicit direction:

| SACM InferenceTypeKind | Formal bridge | Interpretation |
|---|---|---|
| `sufficient` | `AllPremises premises → conclusion` | Joint premises are sufficient for the conclusion |
| `necessary` | `conclusion → premise` | The source premise is necessary for the conclusion |
| `necessaryAndSufficient` | `premise ↔ conclusion` | Both directions hold |
| `collective` | `AllPremises premises ↔ conclusion` with a non-empty premise set (enforced by the Lean constructor) | The whole set of premises is jointly necessary and sufficient |
| `byRule` | Explicit rule identity plus proof term | Requires a separately interpreted formal rule |
| `probable` | No classical bridge constructor | Requires a probability semantics; unsupported by this classical fragment |

This avoids a common direction error: a SACM necessary inference is not the same implication as a sufficient inference. The Lean type indexes each bridge by the SACM inference kind, so the direction cannot be silently swapped.

The `probable` case is deliberately not given a classical implication constructor. A probability model, probability space/measure, conditioning assumptions and interpretation of the SACM probability strength must be supplied before a probabilistic bridge can be formalized. Treating `probable` as ordinary implication would be unsound.

## 5. What has been kernel checked

The existing Lean coherence library now imports `GovCheckCoherence.SACM24`. The axiom report includes theorem declarations for:

- injectivity of the SACM assertion-declaration mapping;
- non-availability of a classical bridge for probable inference;
- correct direction for necessary and sufficient inference;
- joint equivalence for collective inference;
- SACM claim identity and explicit-subject preservation;
- pinning the subject reference to the exact model revision.

The build/axiom-audit run for this extension is pending. No result is claimed until CI completes on the commit containing these declarations.

## 6. Limits and next mapping step

This is a deliberately small, source-view-qualified SACM 2.4 Beta 1 slice, not full SACM conformance. It does not resolve the other PDF/XML conflicts documented in the [interoperability-risk report](sacm24-beta1-interoperability-risk.md). It does not yet formalize every Argument, Artifact, Terminology, Package, View, Diagram, Assessment, Strength, AssertionRule or InferenceRule construct; nor does it prove lossless XML/XMI import/export.

Next:
1. bind one real SACM 2.4 Beta 1 XMI/XML fixture to the formal `SACMClaim` and `SACMAssertion` representation;
2. bind one `AssertedInference` and one `AssertedEvidence` relationship, preserving source/target identities and `isCounter`;
3. add explicit `AssertionRule`/`InferenceRule` source identity and proof-dependency binding;
4. add probabilistic semantics without coercing them into classical entailment;
5. test unsupported metaclasses and round-trip loss explicitly.

The purpose is to prove a small, real cross-model mapping law first, then generalize by metaclass and association with coverage declarations—not to claim the entire SACM metamodel has already been formalized.
