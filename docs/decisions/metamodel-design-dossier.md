# GovCheck metamodel decision dossier

**Status:** decision dossier for review; no final metamodel adoption is made by this document.  
**Prepared:** 2026-11-10.  
**Decision authority:** the current GovCheck normative authority, as recorded in Architecture 0023.  
**French counterpart:** [Dossier de décision sur le métamodèle](metamodel-design-dossier.fr.md).

## 1. Executive summary

GovCheck needs a coherent semantic foundation for governing a software repository across its lifecycle. The problem is not to invent one universal ontology that replaces every mature engineering, assurance, risk or decision standard. Nor is it to assemble a collection of unrelated documents and tools.

The candidate direction is a **typed, versioned, many-to-many semantic graph**, with:

1. a small canonical GovCheck governance core;
2. specialized domain models where mature standards or methods exist;
3. explicit cross-model contracts and mappings;
4. native representations, exchange formats, validators and analysis tools behind adapters;
5. an epistemic/assurance layer that records what is claimed, why, by which method, with what evidence, assumptions, limitations and authority.

This direction is consistent with Architecture 0013, Architecture 0027 and Specification 0005, but those records remain design proposals. This dossier consolidates the evidence, alternatives and decision questions needed before adoption.

**Recommended decision posture:** adopt the architectural principles only after review; do not yet freeze the complete ontology, serialization, graph technology, rule language, logic, proof assistant or model checker. Define and validate a minimal semantic kernel and its cross-model contracts first.



**Ontology-reuse reassessment:** see the dedicated [ontology reuse and CSLib assessment](../research/metamodel-ontology-reuse-assessment.md) and [French counterpart](../research/metamodel-ontology-reuse-assessment.fr.md). It identifies SEON/ReqON as the strongest candidate found, recommends against a comprehensive bespoke ontology on current evidence, and treats a small governance kernel plus explicit mappings as provisional—not adopted.



**Coherence verification:** see the [formal verification assessment](../research/metamodel-coherence-verification.md) and [French counterpart](../research/metamodel-coherence-verification.fr.md). It recommends mandatory assurance obligations for critical semantic mappings, using a heterogeneous toolchain and a formally specified Lean bridge, with source-native reasoners/validators and temporal model checking. This is a proposal for review, not an adopted toolchain.

## 2. Decision to be made

Decide the architecture and boundaries of GovCheck's metamodel, including:

- what belongs to the canonical governance core;
- which domain semantics remain specialized and authoritative in their own scope;
- how objects and relationships are typed, versioned, scoped and temporally applicable;
- how intent, goals, stakeholder needs, requirements, decisions, specifications, properties, architecture, models, implementations and assurance relate;
- how claims, arguments, assumptions, observations, evidence, tests, model checking, formal proofs, probability and fuzzy reasoning are represented without semantic collapse;
- how authority, provenance, uncertainty, invalidation and change affect those relationships;
- how external models are imported/exported without silent semantic loss;
- which parts are core, optional profiles, adapters or external tool responsibilities.

This is a metamodel decision, not a decision to mandate every method or tool for every adopting repository.

## 3. Decision context and repository baseline

### 3.1 Existing repository design

The repository already contains substantial candidate architecture:

- [Architecture 0013 — Governance metamodel](../architecture/0013-governance-metamodel.md) distinguishes goals, requirements, norms, properties, contracts, architecture elements, models, implementation artifacts, methods, evidence, claims, arguments and authorized decisions. It explicitly leaves ontology vocabulary, serialization, graph representation and logic open.
- [Architecture 0027 — Domain semantic standards, decision models and bootstrap commitments](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md) proposes a layered architecture: canonical governance, specialized semantics, cross-model relationships, and adapters/representations/tools.
- [Specification 0002 — Canonical Governance Model](../specifications/0002-canonical-governance-model.md) defines a conceptual governance package but states that no canonical schema or evaluator is implemented.
- [Specification 0005 — Assurance, Claims and Evidence](../specifications/0005-assurance-model.md) explicitly distinguishes empirical testing, model checking, program verification, theorem proving, implementation conformance, normative fidelity and acceptance.
- [Architecture 0022 — Governance capability audit](../architecture/0022-governance-capability-audit.md) records gaps between design and implementation. It warns against claiming that proposed schemas, authority resolution or evaluators are already operational.
- [Architecture 0023 — Bootstrap governance authority](../architecture/0023-bootstrap-governance-authority.md) records the current authority arrangement for GovCheck itself. This must not be generalized as the default authority model for adopter repositories.

### 3.2 Current research and backlog anchors

- [Issue #73](https://github.com/Martin-PB/govcheck/issues/73) is the primary verification work item for semantic contracts across intent, requirements, architecture, lifecycle, assurance and authority.
- [Issue #69](https://github.com/Martin-PB/govcheck/issues/69) covers claim-justification chains and preservation of methods, assumptions and limitations.
- [Issue #74](https://github.com/Martin-PB/govcheck/issues/74) covers reference status, provenance and machine-checkable traceability.
- [Issue #79](https://github.com/Martin-PB/govcheck/issues/79) is the assurance/evaluation portfolio container; its children remain individually scoped.
- [Issue #81](https://github.com/Martin-PB/govcheck/issues/81) is the formal-methods/lifecycle portfolio container.
- [Issue #56](https://github.com/Martin-PB/govcheck/issues/56) compares existing governance and assurance mechanisms.
- The canonical work portfolio is maintained in [work-items.md](../work-portfolio/work-items.md), with portfolio context in [work-portfolio/README.md](../work-portfolio/README.md).

These items are related but not interchangeable. #73 is the main metamodel-contract work item; #69, #74, #79 and #81 cover adjacent assurance, reference and formalization concerns. This dossier does not create a duplicate epic or silently change their priority/status.

## 4. Requirements for a sound metamodel

The metamodel should satisfy the following candidate decision criteria.

| ID | Criterion | Rationale / test |
|---|---|---|
| MM-01 | Preserve semantic distinctions | Intent, need, goal, requirement, constraint, decision, specification, property, model, implementation, claim, evidence and acceptance must not collapse into generic nodes. |
| MM-02 | Typed relationships | Relations need defined source/target types, direction, cardinality, semantics and qualifiers; a generic `traces-to` edge is insufficient. |
| MM-03 | Many-to-many and non-linear | Permit multiple sources/supports, alternatives, conflicts, cycles where meaningful, and partial/unresolved links. |
| MM-04 | Bidirectional traceability | Explain both why an artifact exists and what it motivates, constrains, realizes or supports. |
| MM-05 | Identity and evolution | Stable identities, immutable revisions, supersession, provenance, validity intervals and impact/invalidation. |
| MM-06 | Context and applicability | Scope by repository, component, lifecycle stage, environment, profile, risk and other declared context; never infer legal or safety status from labels alone. |
| MM-07 | Authority is explicit | Separate authorship, production, technical review, normative authority, approval, execution privilege and risk acceptance. |
| MM-08 | Epistemic integrity | Preserve assertion, hypothesis, assumption, observation, evidence, testimony, inference, argument, proof, counterevidence, unknown and limitation. |
| MM-09 | Method pluralism | Tests, model checking, formal proof, inspection, simulation, measurement and operational observation remain distinct methods/results. |
| MM-10 | Quantitative semantic integrity | Distinguish probability, fuzzy membership, nondeterminism, transition rates, costs/rewards and qualitative judgments. |
| MM-11 | Interoperability without loss | Map external standards explicitly; preserve native content and report unmapped/ambiguous constructs rather than silently dropping them. |
| MM-12 | Incremental adoption | Projects select applicable profiles and capabilities; no universal maturity ladder and no mandatory proof tool. |
| MM-13 | Machine-checkable contracts | Define invariants, conformance vectors, negative cases and explicit unknown/unsupported outcomes. |
| MM-14 | Explainability and reproducibility | Every evaluation result links to exact subject/model/policy revisions, method, inputs, tool version, assumptions, limits and provenance. |
| MM-15 | Independence from a single toolchain | No mandatory RDF store, graph database, Lean, TLA+, SACM parser, hosted service or forge. |

## 5. Candidate conceptual architecture

### 5.1 Four cooperating layers

**A. Canonical GovCheck governance core**

Owns repository-wide governance semantics: repository/project identity; intent and context; authorities and delegations; normative commitments and applicability; decisions and exceptions; lifecycle/change state; artifact identity/revision; approval and acceptance; governance policy and its evolution.

**B. Specialized domain semantic models**

Retain full domain semantics where mature models exist. Candidates include SACM for assurance cases; GSN/Assurance 2.0 patterns; DMN for decision logic; BPMN/CMMN for processes/cases; RAAML for risk analysis; SysML v2/KerML for systems engineering; ReqIF for requirements exchange; ISO 25010 for product-quality vocabulary; GQM/SMM for measurement; PROV for provenance; SPDX/CycloneDX for software/component inventories.

These are candidate capabilities, not blanket adoption commitments. A domain model remains authoritative for its own concepts within an explicitly adopted scope.

**C. Cross-model relationship and contract layer**

Defines typed, version-aware relations among the core and specialized models. It does not flatten their object types. A mapping records source model/version, target model/version, mapping rule, coverage, loss/ambiguity, assumptions, authority and validation status.

**D. Representation, exchange and tool adapters**

Own native files, serialization, parsers, validators, query/evaluation engines, editors, import/export and VCS/forge adapters. A syntax or serialization is not the semantic model; parser success is not semantic conformance.

### 5.2 Why not one universal metamodel?

A universal ontology risks erasing the distinctions that make specialist standards useful, while creating a proprietary superset too broad to implement or validate. A pure federation without a common core risks inconsistent identity, authority, scope, versioning and cross-model traceability. The layered approach aims to keep a small common governance kernel and preserve specialized semantics.

## 6. Candidate semantic object families

The following is a discovery inventory, not a final class hierarchy. Exact names, inheritance, cardinalities and required fields remain to be designed.

### 6.1 Intent, needs and engineering

- Project / system / repository context
- Stakeholder / actor / role / concern
- Intent / purpose / value proposition
- Need / expectation / stakeholder requirement
- Goal / objective / desired outcome
- Measure / indicator / metric / target
- Requirement / constraint / obligation / prohibition / permission
- Decision / alternative / rationale / assumption / accepted risk
- Architecture element / interface / boundary / allocation
- Specification / contract / model / property / invariant
- Implementation artifact / component / configuration / deployment

Do not assume a single linear chain. Requirements may originate in laws, contracts, standards, stakeholder needs, incidents, threats, defects, interfaces, operations and interoperability constraints—not only project intent. Goals, observable outcomes and measurements are distinct.

### 6.2 Epistemic and assurance objects

- Claim / assertion / hypothesis
- Argument / argumentation strategy / inference
- Assumption / context / justification
- Observation / incident / indicator / evaluation
- Evidence / testimony / witness / artifact
- Method / procedure / tool / configuration
- Test result / inspection result / simulation result
- Model-checking result / counterexample / explored-state report
- Formal proof / theorem / axiom / trusted-base declaration
- Refutation / defeater / counterargument / contradiction
- Unknown / undecidability / unsupported semantics
- Limitation / scope / freshness / confidence statement
- Acceptance decision / residual risk

These should be aligned with SACM where applicable, without making SACM the entire GovCheck metamodel.

### 6.3 Quantitative and transition-model objects

- Transition system / state / initial-state predicate / transition relation
- Transition semantics: deterministic, nondeterministic, probabilistic, timed or hybrid
- Typed transition weight: probability, rate, cost, reward, priority or empirical estimate
- Parameter / prior / observation dataset / estimation method
- Analysis specification / property / horizon / scheduler assumptions
- Analysis result / witness / counterexample / sensitivity analysis

A finite-state machine is not automatically probabilistic. A Markov chain adds a Markov assumption and a transition distribution/rate semantics. Fuzzy membership is not probability. A model checker validates a supplied abstraction, not its fidelity to the real system. See the probabilistic/fuzzy/state-transition research discussion in [PR #105](https://github.com/Martin-PB/govcheck/pull/105); the primary mathematical reference includes [R-05](../references.md#r-05) and the PRISM/UPPAAL documentation cited there.

## 7. Candidate relationship families

Do not create a generic edge with overloaded semantics. Candidate relation families:

| Family | Examples | Key semantics to define |
|---|---|---|
| Derivation/refinement | derives-from, refines, decomposes-into | Source authority, rationale, completeness, refinement relation |
| Goal/requirement | contributes-to, operationalizes, requires, constrains | Direction, satisfaction meaning, applicability |
| Architecture/realization | allocated-to, implemented-by, realizes, conforms-to | Allocation vs implementation vs conformance |
| Decision | selects, rejects, supersedes, justified-by, assumes | Alternatives, authority, decision scope and effective time |
| Verification/validation | verified-by, validated-by, evaluated-by | Method, subject, property, context and result |
| Assurance | supports, refutes, challenges, contextualizes, argues-for | Evidence polarity, inference, defeaters, argument structure |
| Provenance | generated-by, derived-from, attributed-to, sourced-from | Entity/activity/agent, lineage and trust |
| Governance | authorized-by, delegated-by, applies-to, waives, accepts-risk | Authority, scope, validity, expiry and revocation |
| Temporal/evolution | supersedes, invalidates, revalidates, effective-during | Revision binding, interval and impact propagation |
| Interoperability | maps-to, imports-from, exports-to | Mapping version, coverage, loss and validation |

Relations may be many-to-many. Cycles may be legitimate in some descriptive, causal or dependency graphs; acyclicity must be specified per relation family or analysis, not imposed globally. The semantics of each relation must define whether it is normative, descriptive, causal, justificatory, evidential or provenance-related.

## 8. Epistemic status, evidence and assurance

The model must answer: what is asserted; about which exact subject and scope; why it is asserted; what supports or contradicts it; how each supporting item was produced; what inference is licensed; who is accountable; when it is valid; and what remains unknown.

Non-interchangeable method/result distinctions:

- **Testimony/test:** reports behavior observed in executions under defined cases and conditions; not a theorem proof.
- **Model checking:** reports analysis of a formal model against properties, with assumptions, configuration, bounds, completion and possible counterexample.
- **Formal proof:** a derivation checked in a formal system, with axioms, assumptions, imports and trusted base recorded.
- **Inspection/review:** expert judgment with reviewer competence, scope, checklist and rationale.
- **Simulation/measurement/production observation:** empirical information with sampling, environment, instruments, data lineage and limitations.
- **Acceptance:** an authorized decision that a declared acceptance predicate is met; not a proof that every underlying claim is true.

Avoid one generic `verified` flag and avoid one universal numeric `confidence` field.

## 9. Probability, fuzzy logic and state-transition models

These methods may be useful in bounded domains, not as universal foundations.

- Probability models uncertainty over events/outcomes/parameters. Bayesian results depend on priors, likelihoods, data quality and dependency assumptions.
- Fuzzy logic models graded membership in imprecise concepts and can help with vague requirements or linguistic trade-offs. A membership degree is not a probability.
- Finite-state transition systems express possible states and transitions without requiring probabilities.
- DTMC/CTMC/MDP and probabilistic timed automata add different stochastic, action and time semantics.
- Transition weights must be typed: probability, rate, cost, reward, preference and empirical frequency are not interchangeable.
- Parameter uncertainty, stochastic variability and fuzzy imprecision must remain separate.

Recommendation: represent specialist method definitions, parameters, results, provenance and limitations through optional profiles/adapters. Do not require GovCheck's core evaluator to implement Bayesian inference, fuzzy inference or probabilistic model checking. Whether GovCheck should validate specialist assumptions or delegate that validation to trusted engines remains open.

## 10. External standards and methods: comparison and role

The reference catalogue is the canonical source register. This section summarizes roles and boundaries; it is not a substitute for the detailed catalogue entries.

| Source family | What it contributes | What it does not settle for GovCheck |
|---|---|---|
| ISO/IEC/IEEE 15288, 12207, 29148, 15289 | Lifecycle, processes, requirements and information items | GovCheck ontology, exact authority and executable semantics |
| ISO/IEC/IEEE 42010; SysML v2/KerML | Architecture descriptions and systems models | Repository-wide governance and approval authority |
| KAOS, i*, GRL, Tropos | Goal/actor-oriented requirements relationships | Full assurance, provenance and governance lifecycle |
| OMG SACM 2.3 / 2.4 Beta 1; GSN; Assurance 2.0 | Claims, arguments, evidence, contexts and assurance-case structures | All lifecycle, requirements, authority and repository governance semantics |
| OMG DMN, BPMN, CMMN | Decision logic, process flow and adaptive case work | Why a decision is authorized or whether its assumptions are justified |
| OMG RAAML; ISO 31000 / ISO 23894; NIST risk guidance | Risk-analysis structures and processes | Authority to accept risk and proof that mitigations work |
| W3C PROV-DM/PROV-O; PPMN | Provenance and lineage | Normative approval or truth of source content |
| ReqIF; OSLC RM | Requirements exchange/integration | Complete semantic equivalence between all requirement models |
| SPDX; CycloneDX; SLSA; in-toto | Component inventories, provenance and supply-chain attestations | Overall product correctness or complete governance |
| ISO/IEC 25010; GQM; OMG SMM | Product-quality characteristics and measurement concepts | Universal metric validity or automatic quality acceptance |
| NIST SSDF; NIST SP 800-160; AI RMF; ISO/IEC 42001 | Lifecycle practices and risk/governance guidance | A ready-made GovCheck metamodel or executable policy |

### Key source catalogue anchors

- [R-05 — TLA+ and TLC](../references.md#r-05)
- [R-33–R-34 — Assurance-case metamodels and related foundations](../references.md#r-33)
- [R-44 — KAOS and goal-oriented requirements engineering](../references.md#r-44)
- [R-51–R-55 — Knowledge representation, RDF, SKOS, OWL and SHACL](../references.md#r-51)
- [R-71 — Assurance 2.0](../references.md#r-71)
- [R-73 — OMG SACM 2.4 Beta 1](../references.md#r-73)
- [R-74 — PEAK project-decision model](../references.md#r-74)
- [R-88 and R-93 — Policy-model verification and deontic logic](../references.md#r-88)
- [R-92 — iStar 2.0](../references.md#r-92)
- [R-94–R-98 — OMG semantic models, ISO architecture, requirements and quality references](../references.md#r-94)
- [R-102 — W3C PROV family](../references.md#r-102)

The source catalogue records status and limitations. Presence in the catalogue is not adoption. In particular, SACM 2.4 Beta 1 is an engineering target for full semantic coverage and interoperability, not a claim that the beta is a final standard or that SACM replaces the GovCheck core.

## 11. Architecture alternatives

| Option | Description | Strengths | Risks / weaknesses | Assessment |
|---|---|---|---|---|
| A. One universal GovCheck ontology | Model every domain in one proprietary class/relationship system | One apparent schema; centralized validation | Semantic flattening, excessive scope, proprietary duplication, difficult standards fidelity | Not recommended |
| B. Documents plus informal links | Keep separate documents and generic traceability links | Low initial cost, familiar tooling | Weak semantics, ambiguous edges, poor impact analysis and machine validation | Insufficient as target |
| C. Directly adopt one external metamodel (e.g. SACM, RDF/OWL, SysML) | Make one existing model the whole foundation | Mature vocabulary/tooling in its own domain | Scope mismatch; forces unrelated domains into one semantics; authority/lifecycle gaps | Not recommended |
| D. Federated specialized models with no common core | Keep each standard independent, connect ad hoc | Maximum local fidelity | Inconsistent identity, authority, scope, versioning and cross-model reasoning | Incomplete |
| E. Small canonical core + specialized models + typed contracts + adapters | Layered architecture described in §5 | Balances common governance, specialist fidelity and incremental adoption | Requires rigorous mapping/contract semantics and governance of profiles | Recommended candidate |

## 12. Candidate decisions and current decision status

This section separates existing repository decisions/design commitments from decisions that remain for the competent authority.

### 12.1 Already established in repository design (but check each record's status)

- GovCheck is intended to govern the full software-repository lifecycle, not security alone (Architecture 0027).
- A canonical governance model is intended to be the normative authority for a governed repository, with human-readable documents as controlled projections (Specification 0002; proposed design contract).
- GovCheck itself has a current explicit authority arrangement (Architecture 0023); adopter repositories must define their own.
- Claims, arguments, assumptions, evidence, methods, limitations and acceptance are distinct (Specification 0005).
- Testimony, model checking, theorem proof, implementation conformance, normative fidelity and acceptance must not collapse into one status (Specification 0005).
- Specialized models should retain their own domain semantics, linked through explicit relationships (Architecture 0027).
- SACM 2.4 Beta 1 is the discussed engineering target for SACM capability, with full semantic coverage/interoperability as the objective (R-73 and Architecture 0027); this is not adoption of SACM as the global metamodel.

These are repository design statements, not all implemented capabilities. Where a record is marked proposed, conceptual or not implemented, that status controls.

### 12.2 Provisional recommendations for authority review

1. Adopt the layered architecture in §5 as the preferred direction.
2. Adopt a typed semantic graph as the cross-model relationship abstraction, without requiring a graph database or RDF.
3. Keep a minimal canonical core for identity, authority, scope, applicability, revision, decisions, lifecycle and cross-model contracts.
4. Keep assurance, requirements, architecture, risk, decision, measurement, provenance and supply-chain models specialized where appropriate.
5. Preserve epistemic/method distinctions and never turn tests into proofs or model checking into theorem proving.
6. Permit probabilistic, fuzzy and Markov/state-transition profiles where justified; make none mandatory.
7. Defer serialization, ontology language, graph storage/query technology and evaluator language until contract requirements and conformance cases are established.
8. Require explicit mapping coverage and loss reports for every import/export adapter.

These recommendations are not adopted merely by appearing here. They require an explicit decision by the current GovCheck authority.

### 12.3 Decisions deliberately left open

- Exact ontology/class hierarchy and canonical identifiers.
- Whether to use RDF/OWL/SHACL, JSON-LD, typed JSON/YAML, relational schemas, or a hybrid.
- Whether to expose a graph query language and which one.
- Exact relation catalogue, cardinalities and inference rules.
- Which standards become first-class profiles and which remain import/export adapters.
- Full SACM 2.4 Beta 1 coverage strategy and treatment of future version changes.
- Probabilistic/fuzzy semantics and validation boundaries.
- Markov/MDP/automata profile boundaries and quantitative model-checking integration.
- Required formalization and proof obligations for the metamodel itself.
- Canonical exchange package, migration and loss-accounting strategy.

## 13. Decision options and requested authority response

The authority review should record one of: **approve**, **approve with conditions**, **defer**, **reject**, or **request further evidence**. It should identify the exact dossier revision, selected option, rationale, scope, conditions, owner and review trigger.

The central question is:

> Should GovCheck adopt a small canonical governance core connected to specialized domain semantic models by typed, versioned and auditable contracts, rather than one universal metamodel or a purely document-based approach?

Recommended answer: **approve with conditions**, subject to:
- a reviewed minimum core vocabulary and relation catalogue;
- a mapping/coverage matrix for the first selected profiles;
- explicit non-goals and tool independence;
- conformance examples and negative cases;
- a migration/interoperability policy that exposes semantic loss;
- an assurance argument for the metamodel and its implementation boundary.

No approval is implied by this recommendation.

## 14. Backlog and delivery sequence

The existing portfolio should remain the source of work-item identity and status. The following sequence maps the dossier to existing work; it does not silently create new commitments.

| Order | Existing work item | Expected contribution | Dependency / exit condition |
|---|---|---|---|
| 1 | [#73 — Inter-model contract conformance](https://github.com/Martin-PB/govcheck/issues/73) | Define object/relationship types, semantics, cardinalities, provenance, authority, scope and temporal validity; validate contracts among lifecycle, assurance and authority models. | Primary metamodel work item; no refinement claim without evidence. |
| 2 | [#56 — Governance/assurance ecosystem comparison](https://github.com/Martin-PB/govcheck/issues/56) | Compare reusable capabilities, interfaces and gaps using primary academic/industry sources. | Feed a source-to-concept/decision matrix; catalogue sources EN/FR. |
| 3 | [#69 — Claim justification chain](https://github.com/Martin-PB/govcheck/issues/69) | Formalize epistemic and assurance relationships, including proof/test/model-checking boundaries, assumptions and defeaters. | Reuse the core relation vocabulary; keep method semantics distinct. |
| 4 | [#74 — Reference status and provenance](https://github.com/Martin-PB/govcheck/issues/74) | Make source status, adoption, provenance and bidirectional citation machine-checkable. | Ensure source claims and adoption status cannot be conflated. |
| 5 | [#81 — Formal models and lifecycle](https://github.com/Martin-PB/govcheck/issues/81) | Verify selected cross-model invariants and temporal/invalidation contracts. | Model only after semantics and assumptions are explicit. |
| 6 | [#79 — Evaluation and assurance portfolio](https://github.com/Martin-PB/govcheck/issues/79) | Connect the metamodel to evaluation, evidence and an executable vertical slice. | Do not implement before minimum contracts and status semantics are stable. |

Potential additional work should be created only when a gap is confirmed and cannot be assigned to an existing atomic work item. Candidate gaps to reassess during #73: relation taxonomy/cardinality semantics; specialized-profile mapping and loss accounting; quantitative-model profile contracts; conformance corpus. Do not split them prematurely.

### Proposed milestones

- **M0 — Evidence baseline:** source catalogue and existing design audit are complete enough to identify candidate concepts and conflicts.
- **M1 — Conceptual kernel:** typed object families, relation families, identity, scope, authority, provenance and time are specified.
- **M2 — Mapping matrix:** compare the kernel and candidate profiles to selected standards; record coverage, extension and loss.
- **M3 — Assurance/epistemic contract:** define claims, methods, results, evidence, assumptions, defeaters, unknowns and invalidation.
- **M4 — Formal contracts:** define selected invariants and cross-model test/model-checking cases with explicit assumptions.
- **M5 — Conformance corpus and prototype:** validate positive/negative examples and at least one end-to-end profile without freezing a universal toolchain.

## 15. Risks and mitigations

| Risk | Consequence | Mitigation |
|---|---|---|
| Ontology overreach | Unimplementable, proprietary universal model | Small core; specialist profiles; staged scope |
| Premature technology choice | Tool dictates semantics | Define contracts and examples first |
| Semantic loss in adapters | False equivalence/conformance claims | Mapping coverage, loss reports, round-trip tests |
| Epistemic collapse | Tests, proofs, probabilities and opinions conflated | Typed method/result semantics and assurance arguments |
| Authority leakage | Imported model or tool gains unintended normative force | Explicit adoption and authority links |
| Temporal drift | Stale evidence/decisions treated as current | Revision binding, validity intervals and invalidation |
| False completeness | Empty or generic links satisfy traceability checks | Profile-specific completeness rules and semantic validation |
| Standard-version churn | Silent change in meaning | Pin versions, record status and migration decisions |
| Quantitative false precision | Unsupported global confidence/risk scores | Keep assumptions, calibration, sensitivity and limits explicit |

## 16. Definition of a decision-ready metamodel package

The metamodel should not be declared ready for adoption until the package contains:

- a glossary and object-type definitions;
- typed relation catalogue with domains, ranges, cardinalities and semantics;
- identity, revision, provenance, authority, scope and temporal contracts;
- distinction between normative, descriptive, causal, justificatory, evidential and provenance relations;
- source-to-concept and standards-to-profile mapping matrices;
- import/export coverage and semantic-loss statements;
- positive and negative conformance examples;
- selected formal invariants and validation results with assumptions/limits;
- explicit non-goals, unsupported constructs and open questions;
- a decision record authorized by the current GovCheck authority;
- synchronized English/French documents and reference links.

Until then, the metamodel remains a proposal under research and verification, not an adopted normative specification.

## 17. References

All external sources must be maintained in the central [reference catalogue](../references.md), with EN/FR coverage, stable identifiers, source status, limitations and bidirectional citations. This dossier deliberately points to catalogue anchors rather than creating a parallel bibliography.

Internal design records: Architecture 0013, 0022, 0023, 0027; Specifications 0002 and 0005; ADRs in `docs/decisions/`; formal models in `docs/formal/`; portfolio register in `docs/work-portfolio/`.



## Complete source-catalogue links

[R-05](../references.md#r-05) · [R-33](../references.md#r-33) · [R-34](../references.md#r-34) · [R-44](../references.md#r-44) · [R-51](../references.md#r-51) · [R-52](../references.md#r-52) · [R-53](../references.md#r-53) · [R-54](../references.md#r-54) · [R-55](../references.md#r-55) · [R-71](../references.md#r-71) · [R-73](../references.md#r-73) · [R-74](../references.md#r-74) · [R-88](../references.md#r-88) · [R-92](../references.md#r-92) · [R-93](../references.md#r-93) · [R-94](../references.md#r-94) · [R-95](../references.md#r-95) · [R-96](../references.md#r-96) · [R-97](../references.md#r-97) · [R-98](../references.md#r-98) · [R-99](../references.md#r-99) · [R-100](../references.md#r-100) · [R-102](../references.md#r-102)
