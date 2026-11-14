# Ontology reuse and CSLib assessment for GovCheck

**Status:** research addendum; provisional recommendation, not an adopted architecture. **Date:** 2026-11-11.  
**French counterpart:** [Évaluation du réemploi des ontologies et de CSLib](metamodel-ontology-reuse-assessment.fr.md).  
**Parent dossier:** [GovCheck metamodel decision dossier](../decisions/metamodel-design-dossier.md).

## 1. Finding

The evidence does **not** justify creating a comprehensive, self-contained GovCheck ontology now. A relevant software-engineering ontology network (SEON) already exists, alongside mature models for requirements, assurance, provenance, roles, policies, decisions, architecture, lifecycle and software artifacts.

The best-supported candidate is to **reuse existing domain models in their own scope**, define only a **small GovCheck-specific governance vocabulary where a documented gap remains**, and connect models through explicit, versioned mappings and conformance contracts. CSLib is a candidate formalization/proof-support library, not the canonical ontology, interchange format or an RDF/SHACL engine. Its use is not what makes the proof obligation optional: every semantic correspondence used in GovCheck reasoning must be formally demonstrated by a trusted verification chain, whether CSLib, another library or a smaller GovCheck-specific formalization supplies the definitions.

This does not mean “no GovCheck model.” GovCheck still needs precise repository-governance semantics and explicit inter-model contracts. It means those semantics must be derived from a gap analysis rather than invented wholesale. PR #106 remains unmerged; this report adopts no metamodel.

## 2. Strongest ontology-reuse candidate: SEON

The Software Engineering Ontology Network (SEON) is the most directly relevant discovery in this pass. Its published network includes:

- **SPO:** software processes, activities, resources, people, artifacts and procedures;
- **ReqON:** reference software requirements (RSRO), goal-oriented requirements (GORO), requirements-development process (RDPO) and runtime requirements (RRO);
- **SwO:** software domain concepts;
- **ROoST:** software testing; **QAPO:** quality-assurance processes; **RSMO:** software measurement;
- additional ontologies for design, coding, project management and configuration management;
- **UFO** as a foundational ontology used to ground distinctions across the network.

SEON describes itself as a network of reference ontologies with integration mechanisms and consistent semantics across concepts and relations. This is a much stronger starting point than inventing all lifecycle, requirements and engineering concepts from scratch.

**Maturity caveat:** the public site displays version 1.0.5 and documentation that appears several years old. This pass did not establish active maintenance, uniform licensing, implementation conformance or operational readiness as a mandatory dependency. Treat SEON as a high-value reference and alignment candidate until those questions are checked.

SEON does not by itself settle repository-specific normative authority, delegation/revocation, adoption of decisions, exception expiry, forge-neutral enforcement, or all distinctions between tests, model-checking reports, theorem proofs, accepted risk and real-world observations.

Sources: [R-115](../references.md#r-115), [SEON](../references.md#r-204), [ReqON](../references.md#r-204), [SPO](../references.md#r-204).

Related catalogue sources: [R-04](../references.md#r-04) · [R-33](../references.md#r-33) · [R-34](../references.md#r-34) · [R-71](../references.md#r-71) · [R-73](../references.md#r-73) · [R-88](../references.md#r-88) · [R-92](../references.md#r-92) · [R-93](../references.md#r-93) · [R-94](../references.md#r-94) · [R-95](../references.md#r-95) · [R-96](../references.md#r-96) · [R-97](../references.md#r-97) · [R-98](../references.md#r-98) · [R-99](../references.md#r-99) · [R-100](../references.md#r-100) · [R-102](../references.md#r-102) · [R-115](../references.md#r-115) · [R-116](../references.md#r-116) · [R-117](../references.md#r-117) · [R-118](../references.md#r-118) · [R-119](../references.md#r-119) · [R-120](../references.md#r-120)

## 3. Coverage map: reuse without conflating models

| Concern | Existing candidate(s) | Reusable coverage | Boundary / gap |
|---|---|---|---|
| Intent, goals and requirements | SEON ReqON/RSRO/GORO/RDPO; ISO/IEC/IEEE 29148; ReqIF; OSLC RM | Requirements concepts, work products, exchange and traceability | No single model covers the full intent-to-assurance lifecycle or repository authority |
| Lifecycle and engineering work products | SEON SPO; OMG Essence; ISO/IEC/IEEE 15288 | Processes, activities, artifacts, lifecycle and method-independent engineering-kernel concepts | Process states/Essence alphas are not automatically governance decisions or proof of conformance |
| Claims, arguments and evidence | SACM 2.4 Beta 1 (engineering target); SACM 2.3 formal | Assurance-case structures, claims, reasoning, evidence references and asserted relations | SACM is an assurance metamodel, not the whole governance model; beta and formal versions differ |
| Provenance | W3C PROV/PROV-O | Entities, activities, agents, derivation, attribution and generation | Provenance does not establish truth, integrity, sufficiency or authorization |
| Organizations and roles | W3C ORG; PROV-O agents | Organizations, roles and attribution | ORG does not fully capture control, accountability, empowerment or repository-specific delegation |
| Permissions and duties | W3C ODRL; deontic logic; policy-as-code | Typed permissions, prohibitions, duties and policy rules | ODRL is not a complete repository-governance constitution or authority-resolution system |
| Decisions and motivation | OMG BMM; DMN | Motivation, objectives, decision requirements and decision logic | A decision model does not itself authorize adoption |
| Architecture and behavior | ISO/IEC/IEEE 42010; SysML v2/KerML; TLA+ | Architecture descriptions, structural/behavioral models and properties | Specialized models; model analysis does not prove fidelity to reality |
| Ontology representation and validation | OWL 2, RDF, SKOS, SHACL; OMG ODM | Ontology language, graph exchange, vocabulary mapping, graph constraints and model mappings | RDF/OWL is a technology choice, not a prerequisite for semantic interoperability; SHACL is not theorem proving |
| Software artifacts and supply chain | SPDX, CycloneDX | Component, dependency, package and build metadata | Valid format/inventory does not prove completeness, safety or license compliance |
| Formal semantics and proof | Lean and CSLib | Typed definitions, operational semantics, transition systems, logics and machine-checked theorems where formalized | CSLib is not a domain ontology, repository database, RDF/SHACL engine or automatic proof bridge from arbitrary code |

This is a coverage map, not a claim that all candidates are adopted or are even the same kind of artifact. The set contains ontologies, metamodels, exchange formats, standards, modeling languages, policy languages and proof libraries; their roles must remain distinct.

## 4. CSLib: capability and boundary

The official CSLib repository describes a Lean library for formalizing computer-science theories and tools, with reusable APIs for formalization, software verification and certified software. Its published organization includes foundations and data structures; operational semantics and labeled transition systems (LTS); bisimilarity and trace equivalence; Hoare logic and linear temporal logic; languages/calculi including Boole, CCS, lambda calculus and pi calculus; and automata/computability theory.

This is relevant to **formalizing selected GovCheck semantics**: a lifecycle transition system, temporal property, refinement relation or theorem about a finite inter-model contract. CSLib's contributor guidance specifically favors reusing existing abstractions such as LTS instead of duplicating them.

It does **not** provide:
- a ready-made ontology of intent, goals, requirements, decisions, authority, evidence or assurance cases;
- an RDF/OWL store, SPARQL engine, SKOS alignment tool or SHACL validator;
- a human/agent-readable repository exchange format or automatic preservation of SACM XML/XMI and other native artifacts;
- a completed, fully foundational pipeline from arbitrary mainstream code to verified Lean semantics.

CSLib's Boole direction is evolving. Its contributor documentation says source translations may initially be ad hoc and trusted; proving semantic preservation is a longer-term goal, and the deep-embedding backend is not fully foundational. A proof establishes a theorem from the supplied formal definitions, axioms and assumptions; it does not prove that the model faithfully represents the repository, policy, deployed implementation or real world.

**Recommendation:** do not make CSLib a universal dependency merely by default. However, schema/contract tests cannot replace the formal demonstration required for every semantic correspondence used in reasoning. Where CSLib provides a fitting, audited formalization, prefer reuse; otherwise develop the smallest suitable formalization in a trusted system. Pin revisions and record toolchain, imports, axioms, assumptions and trusted base.

Sources: [R-118](../references.md#r-118), [CSLib repository](https://github.com/leanprover/cslib), [organization](https://github.com/leanprover/cslib/blob/main/ORGANISATION.md), [contributor guidance](https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md), [roadmap](../references.md#r-205).

## 5. Ontologies, metamodels, constraints and proof libraries are different things

- **Domain ontology/vocabulary:** concepts and relations in a domain, e.g. SEON or PROV-O.
- **Metamodel:** constructs and structural rules for models, e.g. SACM, ReqIF or SysML.
- **Exchange format:** machine-readable interchange structure, e.g. ReqIF XML; syntax is not all of the semantics.
- **Constraint language:** validation of instances, e.g. SHACL over RDF graphs.
- **Decision/policy language:** expression/evaluation of decisions or permissions, e.g. DMN or ODRL.
- **Formal proof library:** definitions and theorems checked by a proof assistant, e.g. CSLib in Lean.

OMG's Ontology Definition Metamodel (ODM) is relevant as a method: it defines metamodels, profiles and mappings among ontology and modeling standards, including UML/MOF. It is not a ready-made GovCheck lifecycle ontology. OWL 2 can express formal ontologies; RDF provides graph representation; SKOS supports concept schemes and mappings; SHACL validates graph structure against declared constraints. These technologies may be an implementation profile, but GovCheck should not equate its semantics with RDF or mandate this stack before a separate decision.

Sources: [R-116](../references.md#r-116), [R-117](../references.md#r-117), [OWL 2](https://www.w3.org/TR/owl-overview/), [SKOS](https://www.w3.org/TR/skos-reference/), [SHACL](https://www.w3.org/TR/shacl/), [OMG ODM](../references.md#r-206).

## 6. Recommended candidate: federate first, extend only with evidence

### Small governance kernel (candidate only)

The current sources do not jointly provide sufficient repository-governance semantics for:
- governed repository/project scope and stable artifact identity/revision;
- normative authority, role, delegation, scope, effective period, revocation and succession;
- decision, alternative, rationale, adoption status, exception/waiver, residual-risk acceptance and expiry;
- applicability of a policy/model/decision to an exact repository revision, component, environment and period;
- typed, versioned model mappings/contracts, including coverage, ambiguity, unsupported constructs and semantic-loss reporting;
- evaluation statuses distinguishing pass, fail, inconclusive, unsupported, not evaluated and stale;
- invalidation/revalidation when a source, assumption, model, policy or implementation changes.

These are candidate gaps, not an approved class hierarchy. Keep a concept only if a competency question and survey show that reuse, profiling or mapping cannot express it faithfully.

### Minimum mapping contract

Each mapping should declare exact source/target model versions and artifact revisions; mapping-rule identity/revision and responsible authority; mapping class (exact, equivalent, narrower, broader, partial, ambiguous or unsupported); mapped/unmapped/transformed constructs; assumptions; round-trip behavior and known loss; validation method, fixtures and result; validity period and invalidation conditions.

Never silently turn “unknown” into “false”, “not applicable”, “passed” or “proven”; never infer equivalence from matching labels alone.

### Evidence required before creating a GovCheck-specific concept

Record a concrete competency question/invariant; candidate concepts in SEON and domain standards; whether direct reuse, profiling, specialization or linking works; semantic mismatch and why mapping is insufficient; whether the gap belongs in core/profile/mapping/adapter; positive and adversarial fixtures; and the authorized decision adopting it.

## 7. Options and recommendation

| Option | Assessment |
|---|---|
| A. Invent a comprehensive GovCheck ontology | **Not recommended on current evidence:** duplicates mature models, increases maintenance, risks semantic drift and false equivalence |
| B. Link existing models with no GovCheck-specific semantics | Insufficient alone: authority, applicability, revision, mapping validity and evaluation status remain underspecified |
| C. Small governance kernel + domain-model federation + typed contracts | **Recommended candidate for authority review:** reuses specialist semantics while defining the minimum repository-governance and interoperability contract |
| D. Make CSLib/Lean the canonical ontology | Not recommended: poor fit for general interchange and non-Lean adopters; optional formal-verification profile may be useful |

## 8. Backlog and exit criteria

No duplicate epic is created. Use existing work:
1. **#56:** extend the comparison to SEON/ReqON, ODM, W3C semantic-web components, OSLC RM and CSLib.
2. **#73:** define competency questions, coverage matrix, mapping semantics and positive/adversarial fixtures before fixing the core class inventory.
3. **#74:** record source/version, maturity, license, machine-readable artifact and reverse citations.
4. **#79:** distinguish test, model checking, proof, observation and acceptance in evaluation results.
5. **#81:** prototype a small Lean/CSLib contract only if justified against executable schema/contract tests.

Exit criteria: every concept is classified as reused, profiled, mapped, adapter-owned, a demonstrated GovCheck-specific gap or out of scope; native models are preserved; unsupported content is surfaced; mappings have versioned contracts and adversarial fixtures; and the authorized decision explicitly approves the kernel boundary. No ontology technology or proof tool is mandated by this research.

## 9. Traceability

Central catalogue entries: [R-115 SEON/ReqON](../references.md#r-115), [R-116 OWL/RDF/SKOS/SHACL](../references.md#r-116), [R-117 OMG ODM](../references.md#r-117), [R-118 CSLib](../references.md#r-118), [R-119 Essence](../references.md#r-119), [R-120 OSLC RM](../references.md#r-120). Existing sources include SACM (R-04, R-33–R-34, R-71, R-73), engineering/domain models (R-92, R-94–R-100), PROV (R-102) and policy/logic references (R-88, R-93).

Internal records: [Architecture 0013](../architecture/0013-governance-metamodel.md), [Architecture 0027](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [Specification 0002](../specifications/0002-canonical-governance-model.md), [Specification 0005](../specifications/0005-assurance-model.md), and the [metamodel decision dossier](../decisions/metamodel-design-dossier.md).
