# 0027 — Domain semantic standards, decision models and bootstrap commitments

**Status:** proposed architecture and product-design record for review. It establishes a discovery and integration target; it does not adopt every listed standard, implement parsers or engines, or claim conformance.
**Language:** English is the default; see the [French counterpart](0027-domain-semantic-standards-decisions-and-bootstrap.fr.md).

## 1. Purpose

GovCheck governs a software repository across its entire lifecycle. Its scope includes project intent, requirements, architecture, implementation, maintainability, testing, verification and proof, dependencies and supply chain, security, privacy, safety, documentation, compliance, build and release, operation, maintenance and retirement.

The guided bootstrap must therefore do more than select tools or generate directories. It must help the project owner make explicit, reviewable commitments about:

- which lifecycle and engineering domains apply;
- which methods and decision processes will be used in those domains;
- which standards, metamodels, vocabularies and exchange formats are adopted, and at what exact versions;
- which semantic model is authoritative for each kind of artifact or decision;
- how those models relate to GovCheck's canonical governance model and to one another;
- which conformance, validation, provenance and migration obligations follow;
- who has authority to approve, waive, review or change each commitment.

The result is a governed, versioned **project semantic profile**, not a maturity score and not a mandatory catalogue of every possible standard.

## 2. Architectural principle: one governance system, multiple specialized semantics

GovCheck must not replace mature domain models with a single proprietary universal metamodel. Nor should it flatten distinct domain concepts into generic records merely because they participate in the same lifecycle.

The architecture has four cooperating layers:

1. **Canonical GovCheck governance:** project identity and intent; authority and delegation; goals and requirements; applicability; decisions and exceptions; change lifecycle; artifact identity and revision; approvals; policy; and repository-wide governance.
2. **Specialized semantic capabilities:** complete, versioned models for domains where a suitable standard or well-defined method exists (for example SACM for assurance, DMN for decision logic, RAAML for risk analysis, or SysML v2 for systems modelling).
3. **Cross-model relationships:** explicit, typed, version-aware links among objects without conflating their meanings or transferring authority implicitly.
4. **Adapters, representations and tools:** native model files, exchange formats, validators, evaluators, editors and external tools. A serialization format is not itself the semantic model, and an adapter is not a substitute for semantic coverage.

Each adopted model remains authoritative for the concepts it defines within its declared scope. GovCheck remains authoritative for repository-wide governance and for the project's explicit adoption, applicability, authority and lifecycle decisions.

## 3. Decisions to make during project bootstrap

The bootstrap should discover which decisions matter in the project's context. It must not force every project through an exhaustive questionnaire. For every decision, support at least: **selected**, **not applicable** (with rationale), **deferred** (with owner and due/review condition), and **unknown/not yet assessed**. Do not silently turn unknown into false, not applicable or accepted.

### 3.1 Project context and intent

- purpose, intended outcomes, stakeholders, users and operating environment;
- product/system/software type, boundaries, components and external services;
- criticality and consequences of failure;
- data classes, sensitivity, privacy and security exposure;
- deployment, update, support and retirement model;
- legal, regulatory, contractual, sectoral and organizational obligations as declared by an accountable owner;
- contributor population, collaboration model, VCS, hosting and trust boundaries.

A project label or profile must not be used to infer legal compliance, acceptable risk, criticality or authority without supporting facts and an accountable decision.

### 3.2 Governance and authority

- who owns the project and who may set or amend normative policy;
- decision authority, delegation, separation of duties and independent review;
- change and release approval requirements;
- requirements and traceability policy;
- exception/deviation authority, scope, rationale, expiry and compensating controls;
- risk ownership and risk-acceptance authority;
- evidence retention, provenance and publication expectations;
- dispute, appeal, escalation and policy-change routes.

Authority, execution privilege, technical capability, review and approval are distinct. A tool or CI identity must not gain normative authority merely because it can write to a repository or merge a change.

### 3.3 Engineering and lifecycle domains

At minimum, the capability catalogue should assess applicability across:

| Domain | Bootstrap decisions and possible outputs |
|---|---|
| Requirements and stakeholder needs | Requirement types, sources, stable identities, baselines, allocation, traceability, change and verification strategy. |
| Architecture and design | Architecture description framework, stakeholders/concerns, viewpoints/views, model kinds, design decisions, interfaces and constraints. |
| Implementation and maintainability | Coding/build conventions, static analysis, type checking, complexity and maintainability measures, technical debt and remediation policy. |
| Testing and verification | Test levels, test design, model-based testing, coverage interpretation, static/dynamic analysis, formal verification where justified, independent review. |
| Assurance and evidence | Assurance claims, arguments, evidence, contexts, assumptions, defeaters, evaluation, freshness, provenance and conformance. |
| Risk, safety and security | Risk method, hazard/threat analysis, safety/security objectives, controls, residual risk, monitoring and authorized acceptance. |
| Privacy and data governance | Data inventory/classification, processing purposes, retention, access, privacy risk and evidence obligations. |
| Dependencies and supply chain | Component identity, SBOM, licenses, provenance, vulnerability/advisory intake, attestations, build inputs and supplier assurance. |
| Documentation and compliance | Required information items, controlled documents, normative references, compliance obligations, records and review cycles. |
| Build, release and deployment | Reproducibility, build provenance, artifact attestations, release identity, deployment configuration and rollback. |
| Operations and maintenance | Observability, incidents, service objectives, backup/recovery, maintenance, reassessment triggers and retirement. |
| Knowledge and decision management | Decisions, rationale, experience, assumptions, knowledge, uncertainty, lessons learned and accepted risk. |
| Process and collaboration | Human/agent roles, workflows, approvals, hand-offs, case management, escalation and collaboration protocols. |
| Measurement and improvement | Metric definitions, measurement methods, units, baselines, interpretation, quality objectives and improvement decisions. |

Security is one specialized domain among these, not the universal template for the others. Formal methods are also selected per claim and context; no formal-method capability is mandatory for every project.

### 3.4 Method, standard and model commitments

For each applicable domain, the bootstrap should establish:

- the problem, claim, need or outcome the method is intended to address;
- the chosen method and any alternatives considered;
- the standard/metamodel/vocabulary and exact version/profile;
- its status (formal, draft, beta, withdrawn, organization-specific or project-defined);
- the scope of adoption and explicit exclusions;
- native representation and exchange/serialization formats;
- toolchain, validators, evaluators and their trust assumptions;
- conformance target and evidence required to claim it;
- responsible owner, approval authority and review cadence;
- dependencies, conflicts, migration policy and version-update triggers;
- typed links to GovCheck governance objects and other adopted models.

A standard's presence in the catalogue is not adoption. A standard's adoption does not imply that every project must use every optional feature. A tool's ability to parse a file does not prove semantic completeness or conformance.

## 4. Candidate semantic standards and methods

The following is an initial, deliberately broad discovery inventory, not an adoption decision or a claim that every candidate is equally mature. The catalogue must be maintained with primary-source links, version/status, scope, machine-readable artifacts, licensing/access constraints, implementation maturity, known gaps and last-reviewed date.

| Domain | Candidate | Nature and potential GovCheck role | Important boundary / status to verify |
|---|---|---|---|
| Assurance cases | OMG SACM | Full semantic model for assurance cases: claims, arguments, evidence, artifacts, terminology, contexts and supporting constructs. | Dedicated assurance capability; target full semantic coverage, not a repository-wide governance model. Pin exact version; 2.4 Beta 1 is an engineering target, 2.3 remains formal at this record's research point. |
| Decision logic | OMG DMN | Decision Requirements Graphs, decision tables, expressions and FEEL logic; makes decision logic explicit, inspectable and potentially executable. | Models how a result is determined, not the complete rationale, authority or lifecycle approval for choosing/accepting that result. DMN 1.6 formal; 1.7 Beta 1 in the September 2026 OMG catalogue. |
| Process orchestration | OMG BPMN | Standard process notation/model for activities, events, gateways, messages, roles/lanes and process flows. | Models how work proceeds; does not replace DMN decision logic or GovCheck authority. BPMN 2.0.2 is formal. Do not require a workflow engine. |
| Adaptive case work | OMG CMMN | Case model for less pre-scripted, information-centred work where knowledge workers decide next actions. | Potential fit for investigations, incidents, exceptions and assurance reviews; distinct from BPMN's more predefined process flow. CMMN 1.1 is formal. |
| Decision rationale | PEAK | Problem, Experience, Assumptions and Knowledge inform a decision; the record exposes Solution and Assumed Risk. | Decision reasoning and traceability, not an executable decision-table language and not an assurance-case metamodel. Keep PEAK distinct from DMN and SACM. |
| Risk analysis | OMG RAAML | Structured modelling for risk-analysis approaches, with profiles/libraries for methods such as FMEA, FTA, STPA and related safety/security analyses. | Risk-analysis semantics, not risk authority or risk acceptance. RAAML 1.1 formal; 1.2 Beta 1 appears in the September 2026 OMG catalogue. |
| Requirements engineering | ISO/IEC/IEEE 29148; OMG ReqIF | Requirements engineering processes/information items; ReqIF supports structured requirements exchange. | 29148 is process/information guidance, ReqIF is an exchange format; neither alone supplies the whole GovCheck authority and decision lifecycle. Check the current 29148 edition/status (a third-edition DIS was listed in 2026). |
| Architecture description | ISO/IEC/IEEE 42010 | Architecture-description structure, stakeholders, concerns, viewpoints, views, model kinds and framework requirements. | A framework for architecture descriptions, not a single universal architecture modelling language. 42010:2022 is published. |
| Systems modelling | OMG SysML v2 and KerML | Precise textual/graphical modelling of requirements, structure, behavior, analysis and verification, with API-based interoperability. | Broad systems-engineering language; may be excessive for ordinary software repositories. SysML 2.0 formal (September 2025 catalogue). |
| Test modelling | OMG UML Testing Profile 2 (UTP 2) | Model-based test specification and structured test artifacts linked to system models and requirements. | Distinguish UTP 2 from the older UTP 1.x; the OMG page lists UTP 2.3 Beta 1, so maturity and implementation support require review. |
| Product quality | ISO/IEC 25010:2023 | Product-quality characteristics/subcharacteristics used to specify, measure and evaluate quality. | A quality vocabulary/model, not a complete quality-management process or metric system. |
| Measurement | OMG SMM and/or project-defined measurement models | Formal OMG metamodel (SMM 1.2) for structured representation of measures, measurement methods and results. | Formal publication status is verified; suitability, semantic coverage and implementation/tool support still require project-specific review. No adoption is implied. |
| Provenance | OMG PPMN; W3C PROV family | Provenance/pedigree models for entities, activities, agents, derivations and responsibility across artifacts and processes. | PPMN and PROV are complementary candidates, not assumed substitutes. OMG catalog lists PPMN 1.0 formal (September 2026); W3C PROV includes PROV-DM, PROV-O, PROV-XML and constraints. |
| Supply-chain inventory | SPDX; CycloneDX | Machine-readable software/component inventories, licenses, relationships, vulnerabilities, services and related supply-chain information. | Choose formats according to use cases and ecosystem; SBOM presence is not proof of component safety or complete provenance. SPDX 3.0 is current in its specification catalogue; pin CycloneDX version separately. |
| Secure development | NIST SSDF (SP 800-218) | Secure-development practices and outcomes across the software lifecycle. | Practice framework, not a complete machine-readable metamodel or executable policy language. |
| Open-source compliance | OpenChain ISO/IEC 5230; ISO/IEC 18974 | Formal program requirements for open-source license compliance and security assurance. | Organizational/process standards; program scope and verification materials matter. Conformance claims require evidence; see [R-103](../references.md#r-103). |
| Semantic governance and constraints | RDF, OWL 2, SKOS, SHACL, JSON-LD, W3C PROV | Vocabularies, ontologies, constraints and linked-data representations for cross-domain semantic integration. | Use only where their graph/ontology semantics add value; do not impose an RDF knowledge graph as a prerequisite. |
| Business motivation and rules | OMG BMM, SBVR and DMN | Motivation/goals/influencers, business vocabulary/rules, and decision logic. | Complementary layers; do not conflate motivation, policy authority, vocabulary and executable decision logic. |

This inventory is intentionally extensible. It should be expanded through domain-by-domain research rather than treated as a closed list. Candidate standards must be compared by semantic scope, maturity, openness, machine-readable artifacts, interoperability, implementation ecosystem, maintenance burden and fit to GovCheck's lifecycle—not by brand recognition alone.

## 5. PEAK, DMN, BPMN, CMMN and SACM: complementary, not competing

These models can concern the same governed decision while answering different questions.

| Model | Primary question | GovCheck responsibility it can support |
|---|---|---|
| PEAK | Why was this decision made, based on which Problem, Experience, Assumptions and Knowledge, and what Solution and Assumed Risk were recorded? | Human-readable decision rationale, epistemic traceability, uncertainty and assumed-risk record. |
| DMN | Given declared inputs and decision requirements, which result follows from the specified rules/expressions? | Explicit, testable and potentially executable decision logic, including dependent decisions and decision tables. |
| BPMN | Which activities, events, roles, hand-offs and process paths carry the work from trigger to outcome? | Process/workflow description, approval routing and operational sequencing. |
| CMMN | How is a case of evolving information, tasks and human judgement managed when the next step is not fully predetermined? | Investigations, incidents, exceptions, assurance reviews and adaptive case work. |
| SACM | What assurance claim is made, what argument supports it, what evidence/context/assumptions are involved, and how is it assessed? | Structured assurance case and its full argument/evidence semantics. |
| GovCheck governance | Who is authorized to decide or approve, what policy applies, what is the governed subject/revision, and what lifecycle effect does the decision have? | Normative authority, applicability, approval, exception, change and repository lifecycle control. |

### 5.1 Example: selecting a governance profile at bootstrap

Suppose GovCheck needs to determine whether a repository should activate a privacy-governance capability.

- **DMN** can model the decision requirements and rules using declared inputs such as data classification, processing purpose, exposure and declared jurisdiction. Its result is a recommendation or computed applicability result under the model's assumptions.
- **PEAK** records the problem, relevant experience, assumptions and knowledge, the selected solution, uncertainty and assumed risk. It records why the accountable owner accepted or rejected the recommendation.
- **GovCheck** binds the decision to the project and profile revision, checks the decision-maker's authority, records approval and governs its effect on the repository.
- **BPMN**, if useful, describes the workflow of collecting context, running the decision, reviewing it, obtaining approval and applying the profile.
- **SACM**, when assurance is needed, can structure the argument and evidence supporting claims about the resulting profile or its controls.

No one model silently assumes the responsibility of another. A DMN output is not an approval; a PEAK record is not an authorization; a BPMN task completion is not proof; a SACM assessment is not permission to change repository policy.

### 5.2 Example: change acceptance

A change may trigger a DMN decision about required reviews based on change type, affected assets, risk and policy. BPMN may describe the review and approval sequence. PEAK may record a non-routine decision or an accepted trade-off. SACM may support assurance claims about the changed system. GovCheck binds all of these to the exact change candidate and revision, checks authority, and records the normative acceptance outcome.

### 5.3 Do not over-automate

DMN can be executable, but not every decision should be automated. Some decisions require human judgement, deliberation, negotiation or accountable acceptance of uncertainty. A DMN model may return "manual assessment required", "insufficient information" or "escalate". The model must make missing inputs and assumptions explicit.

BPMN is a process model, not a requirement to install or run a workflow engine. CMMN is a case model, not a reason to turn every governance interaction into a case-management system. GovCheck may initially validate and publish these models without executing them.

## 6. Typed cross-model relationships

Cross-model integration must be explicit and typed. Similar labels do not establish semantic equivalence.

Examples of relationships include:

- a GovCheck project goal **motivates** a requirement;
- a requirement **constrains** an architecture element;
- a DMN decision **determines/recommends** an applicability result from declared inputs;
- a PEAK record **justifies** an accountable decision and records assumptions/assumed risk;
- a BPMN process **orchestrates** activities that collect inputs, evaluate decisions and obtain approvals;
- a CMMN case **organizes** evolving evidence, tasks and judgement;
- a RAAML analysis **identifies/assesses** a risk scenario or hazard under a declared method;
- a control **mitigates/responds to** a risk scenario;
- a test or measurement **evaluates** a property or control under a declared scope;
- a SACM claim **asserts** a bounded proposition and its argument **is supported by** evidence;
- a PPMN/PROV record **derives from / was generated by / was attributed to** specific entities, activities and agents;
- an SPDX/CycloneDX component record **identifies** a supply-chain component or relationship.

Every relationship type must define source and target kinds, cardinality, direction, version applicability, provenance, lifecycle behavior and invalidation/reassessment effects. No cross-model link may silently:
- turn an observation into an incident, risk, proof or approval;
- turn a recommendation into an obligation;
- turn a DMN result into an authorized decision;
- turn an assumed risk into an accepted risk;
- turn an assurance claim into a requirement;
- transfer normative authority from GovCheck to an external model or tool.

## 7. Project semantic profile and repository artifacts

The bootstrap should produce a versioned, machine-readable profile containing:

- project context and explicit unknowns;
- selected, not-applicable and deferred domains;
- adopted models/standards, exact versions and status;
- scope and feature/profile selections for each model;
- native file and exchange formats;
- validation/conformance obligations and toolchain references;
- authority, ownership, review and change policy;
- cross-model mapping and relationship registry;
- dependency/conflict information and migration rules;
- rationale and decision-record links (including PEAK where used);
- evidence/provenance requirements and profile revision identity.

The repository may expose native model artifacts alongside GovCheck's canonical governance data, for example:

```text
governance/
  profile/
  decisions/
  mappings/
models/
  assurance/       # SACM models, when selected
  decisions/       # DMN models, when selected
  processes/       # BPMN models, when selected
  cases/           # CMMN models, when selected
  risks/           # RAAML models, when selected
  architecture/    # 42010 descriptions / SysML models, when selected
  requirements/    # ReqIF or other selected representation
  provenance/      # PPMN / PROV representations, when selected
supply-chain/
  sbom/
quality/
  measures/
  test-models/
```

This is illustrative, not a fixed directory contract. The profile's stable capability/model identifiers and ownership metadata are authoritative for planning. A project should not receive empty directories or pretend integrations merely because a standard appears in a catalogue.

For each adopted model, GovCheck should aim to maintain native, tool-consumable artifacts where the standard defines an interchange or serialization format. Import/export must preserve the complete semantics of the adopted version; the specific conformance target and machine-readable schema/metamodel must be pinned. This follows the SACM 0026 principle: full semantic coverage, not opaque preservation as a substitute for understanding.

## 8. Conformance, versions and lifecycle

For each adopted model, distinguish:

1. **Semantic coverage:** GovCheck can represent and understand all constructs in the adopted scope.
2. **Serialization/interchange conformance:** files are valid against the exact schemas/metamodel and serialization rules.
3. **Behavioral conformance:** any evaluator or execution engine follows the standard's specified behavior.
4. **Round-trip fidelity:** import/export preserves identities and semantics.
5. **Tool interoperability:** independent tools can consume and exchange the artifacts.
6. **Project adoption:** the project has explicitly adopted the model and declared its scope.
7. **Operational use:** the project actually uses the model and its controls/processes.

Do not infer one level from another. A syntactically valid file is not proof of complete semantic coverage; a conformance report is not proof that a project has correctly applied the model.

Every version update must be an explicit governed migration: compare normative and machine-readable artifacts, identify semantic changes and deprecations, produce a migration plan, preserve original inputs and provenance, report compatibility/loss, and require approval before changing the active profile. Beta/draft versions must be labelled as such and must not be represented as formal standards.

The project can adopt one model at a time, defer others, or use project-defined methods where no suitable standard exists. GovCheck must preserve the reason and scope of such choices and make future reassessment possible.

## 9. Implementation and research sequence

1. **Bootstrap decision inventory:** expand Architecture 0024 with the domain and commitment dimensions in this record; define unknown/not-applicable/deferred semantics.
2. **Standards catalogue:** create a versioned catalogue with primary sources, status, machine-readable artifacts, scope, mappings, implementation ecosystem and review date.
3. **Semantic coverage matrices:** for each selected standard, inventory all constructs and constraints and map them to first-class GovCheck concepts, as required for SACM in Architecture 0026.
4. **Decision-model prototype:** evaluate PEAK record structure alongside DMN models; demonstrate one bootstrap decision with explicit inputs, rules, rationale, authority and approval. Do not require a DMN engine in the core.
5. **Process-model assessment:** determine whether BPMN and/or CMMN adds value for actual GovCheck workflows before selecting any runtime or engine.
6. **Cross-model relation contract:** define typed links, identity, provenance, invalidation and lifecycle semantics.
7. **Native artifact interoperability:** validate representative models with independent tools and test round trips.
8. **Governed adoption:** only an explicit project decision may activate a standard/version/profile as normative for that repository.

## 10. Decisions deliberately left open

This record does not adopt DMN, BPMN, CMMN, RAAML, SysML, UTP, PPMN, ReqIF, SPDX, CycloneDX or any other candidate for every repository. It does not select an execution engine, workflow engine, graph database, universal serialization, ontology stack or mandatory formal method. It does not make PEAK executable or replace PEAK with DMN. It establishes the architecture and bootstrap questions needed to make those decisions deliberately and traceably.

## 11. Primary references and version-status snapshots

The primary sources consulted for this record are registered in the central bilingual reference catalogue. The identifiers below are stable catalogue references; the entries contain the official source links, scope, relevance and limitations. Version/status is a dated research snapshot, not a promise to follow a moving “latest” URL.

- **OMG decision, motivation and process models:** [R-94](../references.md#r-94) (DMN, BPMN, CMMN, BMM and SBVR; includes the OMG catalogue and version-specific specifications).
- **OMG engineering and domain models:** [R-95](../references.md#r-95) (RAAML, SysML v2, UTP 2, ReqIF, SMM and PPMN; includes the OMG catalogue and official specification pages).
- **Architecture description:** [R-96](../references.md#r-96) (ISO/IEC/IEEE 42010:2022).
- **Requirements engineering:** [R-97](../references.md#r-97) (ISO/IEC/IEEE 29148:2018 and the third-edition DIS status in 2026).
- **Product quality:** [R-98](../references.md#r-98) (ISO/IEC 25010:2023).
- **Software supply-chain inventory:** [R-99](../references.md#r-99) (SPDX 3.0) and [R-100](../references.md#r-100) (CycloneDX).
- **Secure development practices:** [R-02](../references.md#r-02) (NIST SP 800-218 SSDF).
- **Provenance:** [R-24](../references.md#r-24) (W3C PROV family).
- **Open-source compliance and security assurance:** [R-103](../references.md#r-103) (ISO/IEC 5230 and ISO/IEC 18974).

See [the central reference catalogue](../references.md) and its [French counterpart](../references.fr.md). The catalogue entries distinguish formal specifications from beta/draft versions and explain the limits of what each source establishes.

## 12. Relationships to existing GovCheck records

This record refines and connects, without replacing:

- Specification 0002 — canonical governance authority and composition;
- Specification 0005 — assurance, claims, evidence, methods and trust;
- Architecture 0013 — repository-wide governance metamodel;
- Architecture 0017 — artifact identity, revision and versioning;
- Architecture 0021 — assurance claims, arguments, freshness and invalidation;
- Architecture 0024 — guided bootstrap and domain capability profiles;
- Architecture 0025 — lifecycle observations and PEAK/SACM relationships;
- Architecture 0026 — complete SACM semantic coverage and native interoperability.

The governing rule is: **specialized models retain their own semantics; GovCheck governs their adoption, authority, lifecycle and typed relationships.**
