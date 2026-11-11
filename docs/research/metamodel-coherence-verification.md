# Verifying GovCheck metamodel coherence: formal methods and toolchain assessment

**Status:** research proposal for authority review; no architecture adopted. **Date:** 2026-11-11.  
**French counterpart:** [Vérifier la cohérence du métamodèle GovCheck](metamodel-coherence-verification.fr.md).  
**Parent dossier:** [Metamodel decision dossier](../decisions/metamodel-design-dossier.md).

## 1. Mission and conclusion

The objective is not merely to lint ontology files. GovCheck needs defensible evidence that (a) each source model is internally coherent under its declared semantics, (b) mappings preserve the meaning they claim to preserve, (c) integration introduces no unintended contradictions or consequences, and (d) temporal governance rules remain valid as artifacts, assumptions, authorities and decisions change.

**Recommendation:** use a layered verification architecture, with machine-checked formal contracts for critical semantic bridges as a required assurance objective—not one monolithic tool for every check. Lean is the candidate proof kernel for the bridge's theorems; CSLib should be reused wherever its formalizations fit, not assumed to contain the whole GovCheck theory. OWL reasoners, SHACL, executable contract tests, counterexample search and temporal model checking complement the proof layer. The exact mandatory toolchain remains for authority decision after a prototype.

For critical interoperability claims, proof obligations should be mandatory. Whether every adopter must install Lean locally is a separate distribution decision: an adopter may consume a pinned, reproducible and independently checkable proof bundle, but must not silently downgrade a required proof to a test.

## 2. Decompose coherence into explicit obligations

| ID | Property | Candidate method | Meaning of result |
|---|---|---|---|
| VC-1 | Source artifact is well-formed and preserved | Parser/schema/native-format round-trip tests | Known content is not silently dropped by parsing or serialization |
| VC-2 | Source ontology is logically consistent | OWL 2 DL reasoner, when applicable | A model exists under the ontology's declared semantics |
| VC-3 | Instances satisfy structural constraints | SHACL, schema validation, EVL, executable checks | Instance satisfies declared constraints, not a general theorem about its meaning |
| VC-4 | Integrated theory is consistent | Source reasoners and a formalized common semantic layer | Result applies only to exact assumptions and formalized scope |
| VC-5 | Mappings preserve declared meaning | Lean proof of mapping/interpretation properties, plus tests | A specific preservation theorem holds for the formalized mapping |
| VC-6 | Mapping composition is coherent | Lean composition laws; counterexample search | Composition preserves declared properties |
| VC-7 | Extension is conservative where intended | Conservative-extension/non-interference obligations | Adding GovCheck does not alter specified source-vocabulary consequences except as authorized |
| VC-8 | Governance transitions preserve invariants | TLA+ model checking; Lean proofs for general claims | Invariants hold within the checked model or formal proof assumptions |
| VC-9 | Time-dependent rules reject stale evidence | Temporal model checking and explicit invalidation rules | Decisions, mappings and proofs are used only within declared validity |
| VC-10 | Results are trustworthy and reproducible | Pinned inputs/tools, proof checking, negative fixtures, replay | Result is tied to exact artifacts and a declared trusted base |

“Coherent” must never mean merely “the command exited successfully.” Every result records property, scope, source revisions, semantic profile, assumptions, checker/version, proof/report identity, resource bounds and status. Distinguish proved, model-checked, validated, tested, counterexample found, inconclusive, unsupported, not run and stale.

## 3. What each formalism contributes

### 3.1 OWL 2 and description-logic reasoners: consistency within a source formalism

OWL 2 has formally defined model-theoretic semantics. Under a selected profile, a reasoner can check ontology consistency, class satisfiability, subsumption and entailment. This is appropriate for a source ontology expressed in a supported OWL profile.

Limitations:
- An ontology may be consistent but wrong, incomplete or misaligned with intent.
- Individually consistent ontologies can become inconsistent when mappings/imports are combined.
- OWL's open-world semantics means missing assertions are not automatically false.
- Supported expressivity and decidability profiles matter.
- Equivalence mappings may be stronger than intended and cause unwanted inferences.

Use reasoners for source ontologies and OWL mapping profiles, not as universal verifiers for every model or for the correctness of mapping intent.

Sources: [OWL 2 overview](https://www.w3.org/TR/owl-overview/), [OWL 2 Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/), [OWL 2 conformance](https://www.w3.org/TR/owl2-conformance/).

### 3.2 SHACL and schema/contract validation: executable structural obligations

SHACL validates RDF graphs against declared shapes and produces a report. It can check required identifiers, mapping metadata, allowed statuses and provenance fields where those concepts are represented in the graph and constraint language.

It is not a theorem prover for arbitrary ontology mappings. A passing report establishes conformance to the declared shapes, not general logical consistency or semantic preservation. Schema and contract tests must also cover native XML/XMI, JSON, Markdown metadata and other formats. Do not flatten native artifacts into RDF if that loses information.

Source: [W3C SHACL](https://www.w3.org/TR/shacl/).

### 3.3 Lean and CSLib: proof of the semantic bridge

Lean can define GovCheck's semantic domains and prove theorems about mappings. CSLib offers reusable formalizations of computer-science foundations, operational semantics, labeled transition systems, equivalences and logics; its documented interests include temporal logic. Reuse those definitions when appropriate, and formalize missing GovCheck-specific semantics rather than reimplementing every source ontology.



**Concrete CSLib compatibility finding (2026-11-11):** the inspected CSLib `main` snapshot is commit [`f8acdb37c713b0124ad36b863f50c200a5f1cdba`](https://github.com/leanprover/cslib/commit/f8acdb37c713b0124ad36b863f50c200a5f1cdba). Its `lean-toolchain` pins Lean **4.36.0-rc2**, and its Lake manifest pins Mathlib commit `887bb849a9f64e1c66499fd5ff8523c864e78941`. GovCheck's first verified slice currently pins Lean **4.19.0**. Therefore the current CSLib snapshot is not directly import-compatible with the verified GovCheck package. Do not upgrade the GovCheck proof profile solely to import CSLib. First either identify and test a historical CSLib revision compatible with Lean 4.19, or isolate a separate CSLib-backed proof profile on its own pinned toolchain. The inspected CSLib modules do provide useful LTS, simulation, trace-equivalence and basic temporal-logic foundations; they do not provide a general ontology-alignment or GovCheck assurance metamodel.

The inspected CSLib Basic Temporal Logic module (`Cslib.Logics.BTL.Basic`) supplies future/past modalities and a satisfaction semantics over a relation `r`. Its own documentation explicitly imposes **no order properties** on that relation: reflexivity determines whether the present is included, and transitivity is needed to model a flow of time. Therefore BTL is a reusable formal language/semantics, not by itself a declaration that a model is linear time, nor a state-space model checker. GovCheck must state the frame assumptions and use TLC (or another model checker) when finite-state exploration and counterexample generation are required.

For each source formalism, define or import a semantic interpretation (or explicitly weaker abstraction) and a mapping into GovCheck's semantic domain. State obligations such as:

- **Well-definedness:** every supported source construct maps to a well-typed target construct.
- **Constraint preservation:** source-valid instances satisfy corresponding target constraints after mapping.
- **Epistemic preservation:** test evidence and model-checking evidence cannot become theorem proofs by mapping alone.
- **Authority preservation:** mapping a decision or delegation cannot increase its authority, scope or validity.
- **Provenance preservation:** source identity, revision, origin and transformation history survive mapping.
- **Composition:** composable mappings preserve the declared properties when composed.
- **No silent loss:** unsupported, discarded or approximated constructs are reported explicitly.
- **Conservativity/non-interference:** adding GovCheck vocabulary does not add conclusions in a source vocabulary beyond explicitly authorized consequences.

These are obligations to define precisely, not theorems already supplied by adopting Lean or CSLib. The theorem depends on whether a mapping is exact, sound but incomplete, partial, approximate or merely traceability. “Preserves semantics” is too vague to be a theorem statement.

CSLib's Boole/code-verification path is not the primary ontology bridge. Its contributor guidance says early source translations may be ad hoc and trusted; semantic-preservation proofs are a longer-term goal. GovCheck must not base trust on an unproved translator. Pin CSLib and record Lean version, imports, axioms, trusted code, proof dependencies and replay instructions.

Sources: [CSLib repository](https://github.com/leanprover/cslib), [organization](https://github.com/leanprover/cslib/blob/main/ORGANISATION.md), [contributor guidance](https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md).

### 3.4 Temporal logic and model checking: evolution, not general static ontology coherence

TLA+ models states and transitions and can check invariants and temporal properties of a finite-state abstraction. It is appropriate for decision adoption/revocation, delegation validity, assurance expiry, source-version changes, mapping invalidation, approval/release ordering and stale-proof rejection.

Example properties:
- a revoked delegation is never accepted for a new decision;
- a decision cannot become effective before adoption and required approvals;
- a source ontology change invalidates dependent mappings/proofs until revalidation;
- a proof report applies only to the exact artifact revisions and assumptions it checked;
- no transition promotes test or model-checking evidence to theorem-proof status;
- accepted residual risk expires or triggers review at its declared time.

TLC explores the specified finite-state model; conclusions depend on state space, constraints and abstraction. TLAPS mechanically checks proof steps, but its current documented release does not perform general temporal reasoning for all TLA+ constructs. Do not claim an unbounded theorem from a finite model-checking result.

Thus temporal logic complements Lean: Lean for semantic definitions and mapping-preservation theorems; TLA+/TLC for governance-state evolution and temporal properties; stronger general claims need proof or refinement arguments.

Sources: [TLA+ Proof System](https://proofs.tlapl.us/doc/web/content/Home.html), [TLC documentation](https://github.com/tlaplus/tlaplus/blob/master/general/docs/tlcgui.txt).

### 3.5 Model-transformation verification and counterexample search

Research on model-driven engineering treats transformation verification as the combination of transformation rules, properties of interest and verification techniques. Epsilon EVL supports constraints on models and intra-/inter-model consistency checks. Alloy can search finite scopes for relational counterexamples. These tools find errors early, but bounded search is not an unbounded proof.

Use them to create counterexamples and regression fixtures before or alongside proof development. For critical mapping laws, turn the property into a Lean theorem or a sound exhaustive result with explicit bounds and scope.

Sources: [Calegari & Szasz, transformation-verification survey](https://doi.org/10.1016/j.entcs.2013.02.002), [Epsilon EVL](https://eclipse.dev/epsilon/doc/evl/), [Alloy Analyzer](https://alloy.readthedocs.io/en/latest/tooling/analyzer.html).

## 4. Every mapping needs a semantic contract

For each mapping declare:
1. Exact source/target model identifiers, versions, artifact revisions and semantic profiles.
2. Direction: source-to-target, target-to-source, equivalence or traceability only.
3. Coverage: exact, equivalent, sound-but-incomplete, narrower, broader, partial, approximate, ambiguous or unsupported.
4. Interpretation of source constructs and relations in the target, including abstraction.
5. A precise preservation theorem, assumptions and quantified scope.
6. Round-trip behavior and known losses.
7. Counterexamples and adversarial fixtures.
8. Mapping version, validity interval and invalidation conditions.
9. Typed evidence: Lean theorem/proof, reasoner report, model-checking report, tests or a combination.
10. Trusted base: parser, translator, checker, imported axioms and external dependencies.

Do not require every mapping to be an equivalence. A sound one-way abstraction may be the honest claim. Without a semantic interpretation, label the link as traceability/association, not semantic equivalence.

## 5. Proposed verification architecture

    Native source artifacts: SACM XML/XMI, OWL/RDF, requirements, lifecycle, authority, GovCheck model
       ↓
    1. Parse, fingerprint, preserve; validate native schemas
       ↓
    2. Source-native checks: OWL reasoner | SHACL | native schema | executable constraints
       ↓
    3. Typed mapping contracts: versions | coverage | assumptions | losses | invalidation
       ↔ counterexample search, fixtures and bounded analysis
       ↓
    4. Formal semantic bridge: Lean core + suitable CSLib reuse
       - well-definedness, preservation, composition, non-interference
       ↓
    5. Temporal governance model: TLA+/TLC invariants, expiry, revocation, invalidation
       ↓
    6. Evidence ledger: exact inputs, toolchain, scope, status, proof/report, trusted base

This is a candidate architecture, not an adopted design. Keep native source formats and semantic engines; do not assume every ontology can be losslessly translated to one representation. Formalize only the common semantics and mappings on which GovCheck's guarantees depend.

## 6. Prototype that can falsify the proposal

Start with three small vertical slices rather than formalizing every ontology.

### Slice A — Assurance epistemics (first)

Connect a minimal GovCheck claim/evidence model to SACM concepts and one provenance model. Formalize distinctions among test evidence, model-checking evidence and theorem proof; source claims and supporting evidence; source revision and proof applicability; unknown, unsupported, inconclusive, failed and passed.

Required counterexample: no valid mapping may turn a test or model-checking report into a theorem proof without a separately proved inference rule and its assumptions.

### Slice B — Intent/requirement/decision mapping

Map a small set of intent, goal, requirement, decision and property concepts against SEON/ReqON and a relevant requirements model. Declare each mapping equivalent, directional, partial or traceability-only. Check that the GovCheck layer introduces no unintended source-vocabulary entailments.

### Slice C — Authority and temporal validity

Model decision adoption, delegation, revocation, scope, effective periods and source/mapping/proof revisions. Check temporal properties in TLA+; formalize general authority-preservation theorems in Lean once semantics are stable.

### Acceptance criteria

- Every theorem has explicit definitions, assumptions and scope; no hidden axioms or trusted translators.
- Deliberately inconsistent source fixtures are detected by the appropriate checker.
- Invalid mappings produce counterexamples or fail proof obligations.
- Valid mappings pass their exact obligations and preserve source identity/provenance.
- Unsupported constructs and round-trip losses are reported, never silently discarded.
- Stale proof reports become unusable after relevant input/assumption changes.
- Results distinguish theorem proof, model checking, constraint validation and tests.
- Replaying pinned inputs is reproducible.
- Cost and proof burden are measured; infeasible proof obligations can only be downgraded by an authorized decision that records the residual gap.

## 7. Recommendation for authority review

| Question | Recommendation |
|---|---|
| Must critical semantic coherence be assured? | **Yes.** Make it a first-class assurance requirement. |
| Must every check use Lean? | No. Use the strongest method suited to each property; critical mapping obligations should be explicit and machine-checked where feasible. |
| Is CSLib the whole solution? | No. Reuse relevant formalizations and prove the missing GovCheck semantics. |
| Is temporal logic the whole solution? | No. Use it for state evolution, temporal validity and invalidation, not as a universal static semantic checker. |
| Should OWL/SHACL be replaced by Lean? | No. Retain source-native reasoners/validators and prove critical cross-model claims at the bridge. |
| Can tests replace a missing proof? | Tests are evidence, not proof. Any downgrade must disclose the residual gap and be authorized. |
| Is the architecture adopted? | No. This report proposes a prototype and proof-obligation model for review. |

The strongest practical approach is **heterogeneous verification with a formally specified bridge**: source reasoners and validators, counterexample search and regression fixtures, Lean/CSLib proofs for critical mapping laws, and temporal model checking for governance evolution. No single tool establishes every kind of coherence.

## 8. Existing backlog and exit criteria

No duplicate epic is proposed:
- **#73:** define semantic contracts, mapping classes, competency questions and proof obligations.
- **#56:** evaluate the toolchain and source-model formalisms.
- **#74:** version evidence, source fingerprints, mapping rules and checker/proof dependencies.
- **#79:** type assurance results and status semantics.
- **#81:** formalize lifecycle and invalidation properties.
- **#83:** preserve reference provenance, source versions and backlinks.

First-prototype exit criteria: three vertical slices; source-specific checks; at least one Lean theorem about a real cross-model invariant; at least one deliberate counterexample; temporal stale-evidence/invalidation checks; reproducible evidence bundle; documented trusted base; and an authority decision on mandatory proof obligations.

## 9. Concrete first-slice contract

The proposed engineering contract now specifies the initial evidence-epistemics slice, its Lean proof obligations (VC-EPI-01/02, VC-MAP-01–04 and VC-AUTH-01), adversarial fixtures, temporal invalidation properties, CSLib import audit protocol and completion gate: [Metamodel coherence prototype contract](metamodel-coherence-prototype-contract.md) / [French version](metamodel-coherence-prototype-contract.fr.md). This is a design contract, not an executed or compiled prototype.

## 10. References and traceability

Central catalogue: [R-121 OWL 2 semantics](../references.md#r-121), [R-122 SHACL](../references.md#r-122), [R-123 CSLib](../references.md#r-123), [R-124 TLA+/TLAPS](../references.md#r-124), [R-125 model-transformation verification](../references.md#r-125), [R-126 EVL/Alloy](../references.md#r-126), [R-127 ontology alignment and conservativity](../references.md#r-127).

Related internal records: [metamodel decision dossier](../decisions/metamodel-design-dossier.md), [ontology reuse assessment](metamodel-ontology-reuse-assessment.md), [Architecture 0013](../architecture/0013-governance-metamodel.md), [Architecture 0027](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [Specification 0002](../specifications/0002-canonical-governance-model.md), [Specification 0005](../specifications/0005-assurance-model.md).
