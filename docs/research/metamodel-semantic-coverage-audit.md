# GovCheck metamodel semantic-coverage audit — baseline 2026-11-13

**Status:** engineering/research audit of the current repository baseline; not an adopted metamodel, conformance claim or normative decision.  
**Scope:** issue [#73](https://github.com/Martin-PB/govcheck/issues/73), existing ontology-reuse research, the Lean coherence prototype, SACM 2.4 Beta 1 mapping slice, and the lifecycle/assurance/authority models.  
**French counterpart:** [Audit de couverture sémantique du métamodèle GovCheck](metamodel-semantic-coverage-audit.fr.md).

## 1. Executive finding

GovCheck already has a substantial *documentary* semantic landscape and several useful formal artifacts. It does **not** yet have a complete, machine-executable cross-domain metamodel, nor a demonstrated semantic integration of the candidate ontologies.

The strongest existing coverage is:
- a small Lean vocabulary separating evidence method, epistemic kind and result status;
- a typed proof-carrying mapping contract;
- a source-view-qualified SACM 2.4 Beta 1 Claim/Assertion/inference slice;
- separate TLA+ lifecycle, assurance, authority, governance-applicability and journal models;
- a documented reuse strategy for SEON/ReqON, SACM, PROV-O, requirements/architecture standards, decision models and other specialist semantics.

The main finding from this audit is a **proof-boundary defect in the previous Lean mapping API**. Its old `SemanticBridge` admitted `approximate`, `traceabilityOnly` and `unsupported` constructors without a theorem relating source and target propositions. Those values could nevertheless inhabit `EvidenceMapping`. Its old `KindMappingRule.transport` also allowed a `theoremProof` label to be carried without a proof term for the target proposition.

This PR closes those two type-level paths:
- operative `EvidenceMapping` now admits only equivalence, sound directional preservation, or domain-restricted partial preservation, each with its corresponding proof obligation;
- approximate, traceability-only and unsupported candidates are represented separately as `MappingProposal`, which has no semantic bridge and cannot inhabit `EvidenceMapping`;
- every target `theoremProof` mapping requires a Lean proof term of the exact target proposition, including when the source record was already labelled `theoremProof`.

This is a correction to the prototype's *type boundary*, not proof that a source ontology, importer, exporter or production GovCheck implementation is correct.

## 2. Status vocabulary used by this audit

| Status | Meaning |
|---|---|
| **Formalized (local)** | A source-independent definition or theorem exists in the current Lean/TLA+ package. |
| **Model-checked** | A finite transition-system model/configuration has been explored; conclusions remain bounded by that model. |
| **Documented target** | A standard, ontology or domain model is identified and its desired coverage is described, but not implemented or proved. |
| **Candidate mapping** | A possible semantic relation has been identified; it is not an operative premise until its exact relation is proved. |
| **Not yet covered** | No adequate formal representation or verified mapping has been found in the inspected repository baseline. |
| **Source conflict / unresolved** | The sources disagree, or source semantics/identity is not yet established; both views must be retained. |

These labels describe repository evidence, not a ranking of the external standards. A documented target is not an adoption; a passing model check is not a theorem proof; a Lean theorem about a supplied proposition does not prove that the proposition faithfully interprets a source artifact.

## 3. Coverage matrix

| Semantic area | Existing repository basis | Current coverage | Principal gap |
|---|---|---|---|
| **Intent, stakeholder needs, goals and outcomes** | Intent record and impact analysis; ISO/IEC/IEEE 15288/29148; NASA systems engineering; GORE/iStar; SEON/ReqON reuse assessment. | Documented target and research coverage. | No complete canonical type system or formal semantics for these concepts and their many-to-many relations. No verified mapping from source requirements/goal models into a common GovCheck semantic domain. |
| **Requirements and constraints** | Requirements research; ReqIF and OSLC candidates; ISO/IEC/IEEE 29148; ReqON/SEON. | Documented target. | No source-native instance fixture, parser, full construct inventory or proven preservation contract. A requirement is not automatically a goal, claim, rule or decision. |
| **Decisions, rationale and accepted risk** | PEAK research and Architecture 0025; DMN/BMM candidates; decision-session records and governance authority models. | Documented target; some governance transitions model-checked. | No formal semantic bridge from PEAK/DMN decision objects into GovCheck decisions, assumptions, knowledge, alternatives and accepted-risk records. Decision logic does not itself confer authority to adopt a result. |
| **Architecture, specifications and system models** | ISO/IEC/IEEE 42010; SysML v2/KerML; Architecture 0027; TLA+ lifecycle and governance models. | Documented target; selected transition properties model-checked. | No full inventory of architecture/model constructs or proof of correspondence between architecture descriptions, specifications, implementation and repository governance. |
| **Assurance claims, arguments and evidence** | SACM 2.3 formal baseline; SACM 2.4 Beta 1 target; Assurance 2.0 and ACCESS research; Architecture 0021. | Partial formalization: evidence epistemics and a SACM Claim/Assertion/inference slice. | No full SACM coverage, no lossless native instance interchange, no proof that natural-language claims are faithfully interpreted, and no complete formal treatment of defeaters, assessments, artifacts, terminology, packages, views and diagrams. |
| **Evidence epistemics** | `Evidence.lean`, `Mapping.lean`, evidence-record JSON Schema and assurance model. | Formalized locally: method class, epistemic kind and result status are distinct; target theorem-proof mappings require an exact proof term. | The production schema still lacks an explicit epistemic-kind field and typed derivation object. Proof dependency metadata is not yet mechanically tied to the proof term's transitive dependency closure. |
| **Provenance and artifact identity** | PROV family candidate; artifact catalogue; source/target model revision binding in Lean; VCS protocol Specification 0007. | Partial formalization and documented target. | No proven source-native PROV-O mapping, no production importer/exporter conformance, and no complete preservation/composition theorem for provenance across transformations. |
| **Authority, permissions and normative force** | Architecture 0023; governance-control/applicability TLA+ models; deontic logic and ODRL candidates. | Governance transition models exist and have bounded model-checking evidence. | No complete semantic integration between authority/delegation, deontic modalities, external policy models and domain-specific decisions. A mapping must never amplify authority. |
| **Lifecycle, freshness and change invalidation** | `GovCheckLifecycle.tla`, `GovCheckAssurance.tla`, governance applicability/publication/control/journal models; Specifications 0006/0007. | Several separate finite models model-checked. | No machine-checked refinement/composition proof connecting the TLA+ models to the Lean mapping semantics or a production implementation. |
| **Ontology representation and logical consistency** | OWL 2, RDF, SKOS, SHACL and ODM research; ontology-reuse assessment. | Documented target and candidate tools. | No pinned common semantic layer, no source-ontology consistency run registered as GovCheck evidence, no conservative-extension/non-interference theorem and no proven cross-ontology alignment. |
| **Software quality, testing, risk and supply chain** | ISO/IEC 25010, RAAML, UTP, SPDX, CycloneDX, NIST and OMG engineering models. | Documented specialist capability candidates. | No end-to-end formal coverage inventory or proved mappings for these specialist models. They must remain separate semantic capabilities rather than being collapsed into generic evidence or requirement objects. |
| **Formal semantics infrastructure** | Lean 4.19 core; isolated CSLib compatibility package; TLA+/TLC. | Lean core and CSLib API/build compatibility are evidenced separately. | CSLib compatibility is not a GovCheck↔CSLib semantic refinement proof. No toolchain or formalism has been selected as the universal metamodel engine. |

## 4. Source reuse is not semantic integration

The repository's ontology-reuse assessment correctly distinguishes several artifact families:
- **domain ontologies/vocabularies**, such as SEON/ReqON and PROV-O;
- **metamodels**, such as SACM, ReqIF and SysML;
- **exchange/serialization formats**, which may preserve syntax without preserving meaning;
- **constraint/validation languages**, such as SHACL;
- **decision and process models**, such as DMN, BPMN and BMM;
- **formal proof libraries**, such as CSLib.

These cannot be treated as interchangeable “ontologies”. Their constructs, semantics, authorities, lifecycle and conformance rules differ. GovCheck should preserve each source model in its own identity/revision and declared semantic profile, then add explicit mappings only for the relations actually justified.

In particular:
- SEON/ReqON is a high-value reuse candidate, not yet a proven dependency or a complete repository-governance ontology.
- SACM is a specialist assurance capability, not the whole GovCheck metamodel.
- PEAK contributes a decision-review model; it is not an assurance-case metamodel or authorization mechanism.
- PROV describes provenance; provenance does not prove truth, sufficiency or authority.
- OWL consistency and SHACL conformance answer different questions from semantic preservation in Lean.
- CSLib contributes reusable formal semantics; it is not an ontology alignment engine.

See the [ontology-reuse assessment](metamodel-ontology-reuse-assessment.md), [domain semantic standards architecture](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), and [semantic assurance/transition research](semantic-assurance-and-transition-models-2026-11.md).

## 5. Formal boundary correction in this change

### 5.1 Before

The former `SemanticBridge` included constructors for:
- `approximate`, which accepted an arbitrary relation and limitation strings but did not establish a preservation property;
- `traceabilityOnly`, which established no proposition relation;
- `unsupported`, which established no proposition relation.

Because `EvidenceMapping` accepted all three as its `semanticBridge`, the type system did not prevent such records from being mistaken for operative semantic correspondences.

The former `KindMappingRule.transport` also admitted every epistemic kind, including `theoremProof`, without requiring a proof term of the target proposition.

### 5.2 After

The operative coverage type is deliberately narrower:
- **equivalent:** a proof of `source ↔ target`;
- **soundDirectional:** a proof of `source → target`;
- **partialMapping:** a declared source domain and a proof that every source proposition in that domain implies the target proposition.

The proposal type separately retains:
- **approximate;**
- **traceabilityOnly;**
- **unsupported.**

A proposal can be recorded, investigated, revised or rejected. It is not an `EvidenceMapping`, does not contain a `SemanticBridge`, and cannot be consumed through the current typed mapping interface as an established premise.

A target `theoremProof` kind can only be constructed by `deriveTheoremProof`, which carries a proof term of the exact target proposition. The generic kind-transport constructor explicitly excludes `theoremProof`.

### 5.3 What this still does not prove

- that the Lean proposition supplied for a source claim is a faithful interpretation of the source's natural-language or native semantics;
- that parser/importer/serializer/exporter implementations construct only valid mapping values;
- that the strings recording premises, assumptions, kernel identity and kernel version match the proof term's complete dependency closure;
- that mappings compose while preserving their declared properties;
- that scope restriction, authority non-amplification and conservative extension hold for arbitrary models;
- that a TLA+ model refines a Lean model or a production implementation;
- that any full ontology or metamodel is coherent.

The theorem proves the proposition represented by its Lean type under Lean's trusted kernel and imported axioms. It does not authenticate the source interpretation, source data, authority or implementation automatically.

## 6. SACM 2.4 Beta 1: present vertical slice and remaining source work

The existing `GovCheckCoherence.SACM24` module formalizes a limited source-view-qualified slice:
- PDF text and normative metamodel XML remain distinct source views;
- the selected view binds native format and identity field (`gid` versus `elementId`);
- source-view-specific declaration literals are checked rather than silently unioned;
- `axiomatic` remains a declaration, not a theorem proof;
- necessary, sufficient, necessary-and-sufficient and collective inference have correctly directed formal bridges;
- `probable` has no classical implication bridge;
- Claim identity and explicit subject are bound to the exact source model revision.

It does **not** yet provide full SACM 2.4 conformance or source-instance fidelity. The next SACM-specific work should pin and compare the official PDF/XML artifacts, resolve the remaining multiplicity/value/inheritance conflicts, obtain a portable instance fixture, and only then bind real `AssertedInference`/`AssertedEvidence` relationships and their counter-evidence flags.

## 7. Prioritized residual work

| Priority | Work | Exit condition |
|---|---|---|
| **P0** | Prove the mapping API cannot admit unproved semantic proposals or label-only theorem proofs. | Lean build and axiom audit pass on the tightened API; negative theorem statements cover testimony and model-checking promotion. |
| **P1** | Complete one real SACM source-native vertical slice. | Pinned source fixture, explicit parser/view identity, typed mapping and proof obligations for Claim, AssertedInference and AssertedEvidence; unsupported fields/losses reported. |
| **P1** | Specify the cross-model lifecycle/assurance/authority contract. | Exact relations, direction, scope, assumptions, authority and revision bindings stated; TLA+ and Lean responsibilities separated; composition/refinement claims only where proved. |
| **P2** | Audit SEON/ReqON and requirements/architecture/decision models construct-by-construct. | Source revisions and licensing/maturity established; coverage matrix records preserved, transformed, unsupported and conflicting constructs; each operative mapping has its exact proof obligation. |
| **P2** | Define proof-dependency and assumption provenance. | Proof reports bind the transitive dependency closure, imported axioms, Lean kernel/toolchain and exact source/target model revisions. |
| **P2** | Define mapping composition and conservative extension. | Composition laws and non-interference/conservativity claims are precisely stated and machine-checked for declared profiles. |
| **P3** | Decide the role of CSLib in the proof architecture. | At least one useful GovCheck lifecycle property is mapped to a pinned CSLib formalization with a proved relation; otherwise retain isolated reuse only. |

## 8. Disposition and authority boundary

This audit is an engineering baseline and a research work product for issue #73. It:
- does not adopt a complete GovCheck metamodel;
- does not select CSLib, Lean, OWL, RDF or any serialization as the universal technology;
- does not claim conformance to SEON, SACM, ReqIF, SysML, PROV-O or any other external model;
- does not turn an unproved candidate mapping into an operative relation;
- does not change the normative authority or close issue #73.

The current correction narrows what the Lean prototype can represent as an *operative* semantic mapping. It is a safety improvement to the proof boundary, not a normative adoption of the broader metamodel.

## 9. References

- [R-20 — Lean and proof-kernel boundary](../references.md#r-20)
- [R-34 — OMG SACM 2.3](../references.md#r-34)
- [R-73 — OMG SACM 2.4 Beta 1](../references.md#r-73)
- [R-74 — PEAK project-decision model](../references.md#r-74)
- [R-115 — ISO/IEC/IEEE 15288 lifecycle processes](../references.md#r-115)
- [R-116 — ISO/IEC/IEEE 29148 requirements engineering](../references.md#r-116)
- [R-128 — independent SACM 2.4 Beta 1 implementation-impact audit](../references.md#r-128)
- [Ontology reuse and CSLib assessment](metamodel-ontology-reuse-assessment.md)
- [Domain semantic standards, decision models and bootstrap commitments](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md)
- [Formal coherence methods and toolchain assessment](metamodel-coherence-verification.md)
