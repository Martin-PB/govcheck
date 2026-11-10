# Research survey: formal relationships from intent to assurance

- **Status:** research and design analysis; non-normative.
- **Work item:** [Issue #73](https://github.com/Martin-PB/govcheck/issues/73).
- **Depends on:** [ADR 0009 — repository intent record and canonical naming](../decisions/0009-intent-record-and-authority.md).
- **Purpose:** establish the external state of practice and a candidate relationship vocabulary before any GovCheck metamodel is adopted.
- **Authority:** no relation, cardinality, mandatory field, serialization, notation or tool is adopted by this report.

## 1. Executive findings

The reviewed standards and research do **not** provide one universal, end-to-end metamodel that covers repository intent, stakeholder needs, goals/outcomes, requirements, decisions, architecture/specifications, implementation, verification/validation and assurance.

Instead, they provide complementary partial models:

- lifecycle standards describe processes and information exchanges;
- requirements standards define requirements-engineering information, derivation, allocation and traceability;
- goal-oriented methods connect stakeholder concerns and goals to requirements and operational alternatives;
- architecture-description standards connect stakeholders, concerns, viewpoints, models, correspondences and architecture rationale;
- decision-rationale research relates requirements, constraints, assumptions, alternatives, choices and consequences;
- systems-modeling and requirements-interchange standards represent typed model elements and relationships;
- assurance-case standards structure claims, arguments, assumptions, context and evidence;
- provenance vocabularies describe derivation, attribution, activities, agents and invalidation;
- traceability research shows that pre-requirements traceability and maintaining links across changing artefacts remain difficult problems.

The strongest conclusion is therefore not “adopt standard X as the GovCheck graph”. It is: **GovCheck needs a typed, many-to-many, versioned relationship graph with explicit semantics, while allowing external profiles and mappings for specialized standards.**

A single generic `traces-to` edge is insufficient. Conversely, a rigid linear chain is also insufficient: requirements may originate in regulation, standards, risks, incidents or architecture constraints; decisions may create or amend requirements; assurance claims may concern several levels; runtime evidence may challenge earlier assumptions.

## 2. Scope and terminology

This survey considers the following concept families. They must remain distinct even where a particular external method combines them.

| Concept | Working meaning for this survey |
|---|---|
| Intent | Durable statement of why the repository exists, the problem/context, boundaries, stakeholders or beneficiaries, intended outcomes, assumptions and open questions. |
| Stakeholder need / expectation | A concern, need or expectation expressed by an interested party; it may be incomplete, conflicting or unvalidated. |
| Goal / objective | A desired state or condition that refines intent; goals may be qualitative, conflicting, decomposable or only partially operationalizable. |
| Outcome | An observable effect or result by which the value or validity of a goal may be assessed. |
| Requirement | A governed statement of a necessary capability, condition, constraint or quality; its origin may be internal or external. |
| Decision | An authorized selection, interpretation, constraint, deferral, exception or change among alternatives, with rationale and consequences. |
| Architecture element | A component, relation, boundary, interface, deployment element or other element of the system's architecture. |
| Specification | A structured description of required or intended system properties, behavior, interfaces or constraints. It is not necessarily normative merely because it is written. |
| Property | A predicate or condition about an artefact, model, implementation or execution, with declared scope and assumptions. |
| Implementation / realization | A concrete artefact or activity intended to realize a design or satisfy a requirement. |
| Verification / validation | Distinct activities: verification assesses conformance to specified conditions; validation assesses fitness for intended use and stakeholder outcomes. |
| Assurance claim | An assertion about a system, process, property or governance state that requires an argument appropriate to its type. |
| Argument / rationale | Reasoning that explains, justifies, decomposes or challenges a decision or assurance claim. |
| Evidence | An artefact or observation used to support or challenge an assertion. A test result is testimony/evidence, not a proof; model checking is model-validation evidence, not theorem proof. |
| Provenance | Information about who/what produced, changed, derived, reviewed or invalidated an artefact or assertion, when and from which inputs. |

The same word can have different meanings in different methods. Any GovCheck metamodel must define its own terms and mappings rather than assume homonymy implies semantic equivalence.

## 3. Academic and industrial findings

### 3.1 Lifecycle and requirements engineering

**ISO/IEC/IEEE 15288:2023** provides a lifecycle-process framework spanning conception through retirement and supports iterative/recursive application. It does not prescribe one lifecycle model or repository document structure. It establishes that requirements, realization, verification, validation and operation belong to the lifecycle as a whole, not a one-time sequence.

**ISO/IEC/IEEE 29148:2018** provides requirements-engineering processes and information items. Its relevance includes requirements derivation, allocation, validation, verification and traceability. The third-edition DIS visible in 2026 is a draft under enquiry, not an adopted International Standard.

**NASA Systems Engineering Handbook** makes stakeholder expectations, ConOps, requirements, design decisions, verification and validation explicit and emphasizes bidirectional traceability. This supports upward and downward navigation, consistency checking and iterative reconciliation, rather than a one-way transformation.

**Pre-requirements traceability research** is particularly relevant. Mucha, Kaufmann and Riehle's 2024 systematic review examines 77 papers from 1992–2022 and identifies links from requirements back to their origins, such as stakeholder interviews, meeting records and legacy systems. The authors report that this area has received less attention than post-requirements traceability. This is a direct warning against beginning the graph only at the requirement node.

A separate 2018 systematic review of requirements-traceability technologies analyzed 114 papers (2006–2016), assessed 83 empirical studies, and identified ten challenges and multiple technology categories. It supports treating traceability as a difficult lifecycle capability requiring explicit method selection and evaluation, not merely adding hyperlinks.

### 3.2 Goals, intent and outcomes

Goal-oriented Requirements Engineering (GORE) approaches such as **KAOS, iStar, GRL and Tropos** share capabilities including goals, AND/OR refinement, tasks or operationalization, actors and dependencies. They differ in emphasis: formal goal definitions, qualitative/soft goals, actor dependencies and agent-oriented reasoning.

The 2026 reflection on the systematic mapping of 246 GORE publications notes both the common modeling capabilities and persistent industrial adoption barriers and uneven empirical evaluation. GovCheck should therefore study and selectively map these concepts, not mandate a single GORE notation.

This research supports at least three distinct relations:
- intent motivates or frames goals;
- goals refine into sub-goals and may be operationalized by requirements/tasks;
- outcomes provide a basis for evaluating whether goals were achieved.

A goal is not automatically a requirement; a requirement is not automatically a measurable outcome. Qualitative goals and conflicting goals must remain representable.

### 3.3 Architecture, specification and decision rationale

**ISO/IEC/IEEE 42010:2022** specifies the structure and expression of architecture descriptions. It distinguishes the architecture itself from the description of that architecture and defines concepts and relationships involving stakeholders, concerns, viewpoints, views, model kinds and correspondences. It also recognizes architecture rationale and decisions, but does not prescribe a modeling method, notation, process or storage format.

**SysML v2** is a candidate source for typed model relationships among requirements, structure, behavior, analysis and verification. It is a systems-modeling language, not a repository-governance metamodel.

**ReqIF 1.2** provides a standardized requirements-interchange format and machine-readable schema. It is useful for exchange of requirement objects and associated relations/attributes, but it does not define the complete semantics of GovCheck's intent, authority or assurance lifecycle.

Architecture decision research is especially important because decisions are not merely a stage after requirements:
- the AREL (Architecture Rationale and Elements Linkage) model relates requirements, constraints and assumptions to architecture elements through decisions and rationale, supporting impact analysis;
- formal work on the semantics of architectural decisions identifies explicit relations among decision elements;
- empirical studies report that practitioners value design rationale but face barriers to capturing it consistently;
- a 2024 feature/specification/evidence framework emphasizes reasons, alternatives, trade-offs and argumentation as parts of rationale.

This supports representing a decision as an object with context, alternatives, selection, rationale, authority, consequences and links to affected artefacts. A decision may satisfy, constrain, reinterpret, defer, waive or create requirements. It is not just a directed edge between a requirement and a specification.

### 3.4 Assurance cases and evidence

**OMG SACM 2.3** supplies a standardized metamodel for claims, argumentation, artefact references, evidence, context and reasoning. **GSN v3** supplies a community standard for structuring engineering arguments, including goals/claims, strategies, contexts, assumptions, justifications and solutions/evidence.

These are complementary assurance structures, not complete lifecycle metamodels. GovCheck must not infer that an evidence node proves a claim merely because a link exists. The argument, method, scope, assumptions, provenance, freshness and possible rebuttal remain relevant.

Assurance is also not simply the final node of a linear chain. Claims may concern intent adequacy, requirements coverage, decision acceptability, architecture properties, implementation behavior, operational performance or the governance process itself.


### 3.6 Goal measurement and product quality

The **Goal-Question-Metric (GQM)** paradigm provides a disciplined way to connect goals to questions that operationalize assessment and then to measures/observations interpreted in context. This supports outcome observability without reducing every goal to a universal KPI: the question and measurement model must be derived from the goal and context.

**ISO/IEC 25010:2023** supplies a product-quality model whose characteristics can inform quality requirements, design objectives, testing objectives, quality criteria, acceptance criteria and measurement throughout the lifecycle. It is a quality taxonomy, not a goal model; characteristics must be selected and interpreted for the product and stakeholders.

### 3.7 Security engineering as a lifecycle relationship test

**NIST SP 800-160 Vol. 1 Rev. 1** treats systems security engineering as a lifecycle discipline connecting protection needs and stakeholder concerns to security requirements, risk, architecture/design, implementation, verification, validation and assurance. It is a useful stress test for GovCheck because security requirements may derive from threats, risks and operational context, not solely from product intent. The relationship model must preserve those origins and the authority/risk decisions that accept or treat them.

### 3.8 Architecture processes, information items and configuration management

**ISO/IEC/IEEE 42020:2019** complements ISO 42010 by defining architecture governance/management and architecting processes throughout the architecture lifecycle. This makes architecture decisions and change processes first-class lifecycle activities.

**ISO/IEC/IEEE 15289:2019** specifies the purpose and content of lifecycle information items. It organizes information items by generic document types and purpose, and does not define a universal filename or media. This is relevant to GovCheck's separation between semantic artifact identity and file naming: a canonical name is a repository convention, not automatically a standards-derived requirement. The 2019 edition was confirmed current in 2025, while a revision project is active.

**ISO 10007:2017** provides configuration-management guidance from conception to retirement, including configuration identification, change control, status accounting and audit. This supports binding relations, specifications and evidence to explicit baselines and revisions, while preserving change history.

### 3.5 Relationship exchange and provenance

**OASIS OSLC Requirements Management 2.1** represents relationships to other resources as RDF properties/triples. This demonstrates the value of explicit predicates and interoperable resource links, while remaining an integration specification for requirements-management resources rather than a full semantics of lifecycle governance.

**W3C PROV-O** provides provenance classes and properties for entities, activities and agents, including derivation, attribution, association, generation, usage and invalidation. It is a useful provenance layer. It should not be mistaken for the domain semantics of goals, requirements, decisions or assurance.

These sources suggest separating:
1. the domain relation (for example, a requirement is derived from a goal);
2. the provenance of the assertion that this relation holds (who asserted it, from what source, using what method);
3. the temporal applicability of that relation to a repository revision or governance revision.


### 3.9 Safety engineering and safety cases

Functional-safety practice provides another strong lifecycle example. The UK Health and Safety Executive's guidance describes deriving risk-reduction requirements from hazard/risk assessment, allocating those requirements to safety instrumented systems or other measures, specifying and designing the system, validating it, then operating, maintaining, modifying and decommissioning it. It demonstrates why origin, allocation, verification/validation and operational-change relations must be connected. It is domain-specific and must not be generalized into a mandatory process for every software repository.

A 2021 systematic literature review of **51 security-assurance-case papers** finds that security assurance cases provide structured argument and evidence for reasoning about a system's security posture, but that practitioner support, validation and tool support remain immature. This is a warning against assuming that the existence of GSN/SACM notation alone solves assurance-case construction or maintenance.

### 3.10 Goal alignment beyond a single repository

**GQM+Strategies** extends goal-question-metric reasoning by making links among organizational goals, strategies, software goals, context factors, assumptions, scenarios and measurement goals explicit. It is relevant where a repository contributes to a larger system or organizational purpose. GovCheck must not assume every repository has a commercial/business goal hierarchy; the useful transferable concepts are explicit context, assumptions and traceable goal alignment.

## 4. Candidate relationship families

The following vocabulary is a research proposal for discussion, not an adopted GovCheck vocabulary. Names and directions must be finalized only after semantic analysis and examples.

| Family | Candidate relation | Typical source → target | Meaning and cautions |
|---|---|---|---|
| Motivation | `motivates` | Intent / need → goal | The source provides purpose or reason for the goal; does not imply acceptance of the goal. |
| Decomposition | `refines` | Goal → sub-goal; requirement → sub-requirement | Narrows or decomposes meaning; acyclicity may be required within a refinement hierarchy. |
| Operationalization | `operationalizedBy` | Goal → requirement / task / operational capability | Identifies how a goal may be pursued; does not prove achievement. |
| Origin / derivation | `derivedFrom` | Requirement → goal / need / regulation / risk / standard / incident / decision | Records origin; multiple origins are allowed and external origins need not pass through intent. |
| Allocation | `allocatedTo` | Requirement → architecture element / subsystem | Assigns responsibility or scope; does not establish satisfaction. |
| Decision | `addresses` | Decision → concern / requirement / risk / goal | States what the decision responds to. |
| Selection | `selects` / `rejects` | Decision → alternative | Records the selected and rejected alternatives; alternatives and trade-offs must remain identifiable. |
| Constraint | `constrains` | Decision / constraint → specification / architecture element | Limits permitted design choices; authority and applicability must be explicit. |
| Justification | `justifiedBy` | Decision → rationale / argument | Links the choice to reasoning, evidence, assumptions and consequences. |
| Specification | `specifiedBy` | Requirement / property → specification element | Identifies where a requirement/property is described; not proof of implementation. |
| Realization | `realizedBy` | Requirement / specification → implementation / system element | Identifies an intended realization; satisfaction remains separately evaluated. |
| Satisfaction | `satisfiedBy` | Requirement / property → implementation / system element | Asserts a satisfaction relationship with a defined assessment status; must not be inferred from realization alone. |
| Verification | `verifiedBy` | Requirement / property / specification → verification case / method / result | Tests conformance to specified conditions; method and result are distinct. |
| Validation | `validatedBy` | Goal / outcome / intended use → validation case / observation | Assesses fitness for intended use or achievement of outcomes; not interchangeable with verification. |
| Assurance decomposition | `decomposedInto` | Claim → sub-claims | Structures an assurance argument; relation semantics follow the selected assurance profile. |
| Evidence support | `supportedBy` | Claim → argument / evidence | Records support within a declared scope; existence of a link is not proof. |
| Challenge | `challengedBy` | Claim / decision → counter-argument / counter-evidence | Preserves rebuttal and defeaters rather than hiding contradictory evidence. |
| Assumption | `dependsOnAssumption` | Claim / decision / model → assumption | Makes conditionality explicit; assumptions may be challenged or invalidated. |
| Provenance | `generatedBy`, `derivedFrom`, `attributedTo` | Artefact / assertion → activity / input / agent | Records production and derivation history; can map to PROV-O. |
| Temporal change | `invalidatedBy`, `supersededBy` | Relation / artefact → change event / successor | Preserves historical truth and records prospective validity; never silently deletes history. |

### 4.1 Relation families must not be collapsed

- `realizedBy` is not `satisfiedBy`.
- `satisfiedBy` is not `verifiedBy`.
- `verifiedBy` is not `validatedBy`.
- `supportedBy` is not `provedBy`.
- `justifiedBy` is not `authorizedBy`.
- `derivedFrom` is not `approvedBy`.
- `tracesTo` may be useful as a navigational convenience, but cannot replace a typed semantic predicate.

## 5. Candidate relationship record

A relationship may need its own identity and metadata, rather than being an unqualified hyperlink. Candidate fields to investigate:

- stable relation ID and relation type;
- subject and object identities, with declared object types;
- source and target repository revisions / governance revisions;
- assertion status (proposed, accepted, rejected, disputed, invalidated, superseded);
- author/asserting agent, authority basis and approval event where required;
- provenance source, method and rationale;
- validity interval or applicability condition;
- scope, assumptions, qualifiers and confidence/uncertainty where meaningful;
- evidence or argument supporting the assertion;
- change event and supersession/invalidation history.

The relation's assertion status must not be confused with the status of either endpoint. A requirement can remain accepted while one proposed allocation is rejected; a decision can remain historically valid while its current applicability is superseded.

## 6. Candidate global properties and constraints

These are hypotheses for later formalization, not adopted invariants:

1. **Typed endpoints:** each relation type defines permitted source and target types.
2. **Explicit origin:** each accepted requirement has a recorded origin class and a traceable origin, or an explicit declaration that the origin is unknown or not yet resolved.
3. **Decision completeness:** an accepted decision identifies the concern/context, authority, outcome, rationale and affected artefacts; the depth of alternatives analysis may be proportionate and must be stated.
4. **No semantic implication by adjacency:** realization does not imply satisfaction; satisfaction does not imply verification; verification does not imply validation; evidence support does not imply proof.
5. **Authority separation:** a relation or evidence item cannot grant authority merely by existing.
6. **Revision binding:** claims about satisfaction, verification, validation and assurance are bound to an exact subject revision, method and input scope.
7. **Historical preservation:** invalidation and supersession are recorded as new events; prior accepted relationships remain inspectable.
8. **Impact propagation:** changing an upstream object triggers impact analysis of relevant descendants, but does not automatically invalidate every descendant without relation-specific rules.
9. **Profile-scoped completeness:** required links depend on object type, assurance profile, risk and lifecycle context; no universal all-to-all completeness rule.
10. **Relation-specific cycle rules:** some relations (such as decomposition/refinement) may require acyclicity; the overall graph must not be assumed acyclic because dependencies and rationale may legitimately form cycles.
11. **Bidirectional navigation:** each asserted relation is traversable from both endpoints, with the same identity and semantics.
12. **Provenance of assertions:** the system distinguishes an asserted relation from an inferred or tool-generated candidate relation.

## 7. Important counterexamples and scenarios

A complete model must handle at least these cases:

- A requirement derives directly from a regulation or external standard, without a direct intent-to-requirement path.
- A security requirement is derived from a threat/risk analysis or incident observation.
- One goal is operationalized by several requirements; one requirement contributes to several goals.
- Two goals conflict and a decision selects a compromise while recording rejected alternatives and accepted residual risk.
- A decision creates a new constraint or requirement rather than merely resolving an existing one.
- One requirement is allocated to several architecture elements; one element contributes to multiple requirements.
- A specification describes a requirement, but implementation does not yet realize it.
- An implementation realizes a requirement, but verification fails.
- A test passes, but the test does not validate the intended outcome.
- A formal proof covers an abstract model but not the implementation.
- A model-checking result validates a bounded model under assumptions but does not prove a theorem or implementation refinement.
- An assurance claim is supported by evidence that later becomes stale or is challenged by a production incident.
- A relation is valid for one governance revision and not another.
- A relation graph contains a dependency cycle while its refinement subgraph remains acyclic.
- An accepted decision is made by the competent authority but lacks independent review under a single-authority regime; the residual risk must remain visible.

## 8. External mappings and limits

| External model | Potential mapping | What it does not supply |
|---|---|---|
| ISO 29148 | Requirements, derivation, allocation, verification/validation traceability | Complete intent/decision/assurance graph semantics |
| GORE (KAOS/iStar/GRL/Tropos) | Goals, refinements, tasks, actors, dependencies, softgoals | Universal repository governance, authority and assurance semantics |
| ISO 42010 | Stakeholders, concerns, viewpoints, views, models, correspondences, architecture rationale | A mandated architecture process or repository file format |
| SysML v2 | Requirements and system model relations | GovCheck's governance authority and provenance model |
| ReqIF | Requirement object interchange and attributes | Intent and assurance semantics, decision authority |
| OSLC RM | Inter-resource links and lifecycle tool integration | Full semantics of each relation outside the RM domain |
| SACM / GSN | Claims, argument structures, context, assumptions, evidence | Full upstream lifecycle derivation and implementation traceability |
| PROV-O | Entity/activity/agent provenance, derivation and invalidation | Domain-specific meaning of requirements, decisions or assurance claims |

A mapping profile must declare semantic equivalence, narrower/broader meaning, unsupported constructs and information loss. Serialization compatibility alone is not semantic compatibility.

## 9. Proposed next design sequence

1. Agree a glossary and concept boundaries.
2. Extract the exact relationship semantics from each external source and record where sources agree or diverge.
3. Define candidate node types and relation signatures, including cardinality and temporal qualifiers.
4. Define status/authority/provenance as orthogonal dimensions, not overloaded relation labels.
5. Define completeness profiles and diagnostic conditions.
6. Create positive and negative conformance scenarios.
7. Model the core lifecycle and assurance contracts in an appropriate formalism, selected per claim and without mandating one tool.
8. Compare external mappings and run loss-detection tests.
9. Only then propose a GovCheck specification and associated architecture decision for owner review.

## 10. Research limitations

This is a targeted survey, not a systematic literature review over all relevant databases. It uses selected standards, official specifications, systematic reviews and peer-reviewed studies identified as directly relevant. The next iteration should broaden the search to decision theory, goal/outcome measurement, safety engineering, security assurance, data provenance, configuration management, model-based systems engineering and product-management practices.

No candidate relation or property in this document is normative. No external format is selected as the canonical GovCheck serialization. No formal refinement or implementation assurance is claimed.

## Reference catalogue links

- [R-114](../references.md#r-114)
- [R-115](../references.md#r-115)
- [R-116](../references.md#r-116)
- [R-117](../references.md#r-117)
- [R-118](../references.md#r-118)
- [R-119](../references.md#r-119)
- [R-120](../references.md#r-120)
- [R-121](../references.md#r-121)
- [R-123](../references.md#r-123)
- [R-124](../references.md#r-124)
- [R-125](../references.md#r-125)
- [R-126](../references.md#r-126)
- [R-127](../references.md#r-127)
- [R-128](../references.md#r-128)
- [R-129](../references.md#r-129)
- [R-130](../references.md#r-130)
- [R-131](../references.md#r-131)
- [R-132](../references.md#r-132)
- [R-133](../references.md#r-133)
- [R-134](../references.md#r-134)
- [R-135](../references.md#r-135)
- [R-136](../references.md#r-136)
- [R-137](../references.md#r-137)
- [R-138](../references.md#r-138)
- [R-139](../references.md#r-139)
- [R-140](../references.md#r-140)
- [R-141](../references.md#r-141)

## 11. Coverage assessment and remaining gaps

### 11.1 Coverage map

| Concern | Main sources covered | Assessment |
|---|---|---|
| Repository intent and originating context | Anthropic intent practice; NASA stakeholder expectations; pre-requirements traceability review | Good conceptual coverage; file naming is not a normative standard. |
| Lifecycle processes and information items | ISO 15288, 42020, 15289 | Good process/documentation coverage; not a unified graph metamodel. |
| Goals, objectives and outcomes | GORE; GQM; GQM+Strategies; ISO 25010 | Good candidate methods; outcome evaluation remains context-dependent. |
| Requirements and traceability | ISO 29148; ReqIF; OSLC RM; traceability reviews | Strong standards and research coverage; automated maintenance and pre-requirements traceability remain difficult. |
| Architecture and specifications | ISO 42010/42020; SysML v2 | Good architecture-description and model coverage; no repository-governance semantics. |
| Decisions and rationale | UK ADR guidance; AREL; formal decision semantics; design-rationale framework | Multiple complementary approaches; no single universal decision metamodel. |
| Assurance and evidence | SACM; GSN; NIST SSE; security assurance-case review; functional safety guidance | Strong specialist coverage; assurance-case construction/maintenance tooling remains immature. |
| Provenance and temporal applicability | PROV-O; configuration management guidance | Good provenance/configuration concepts; mapping to authority and repository revisions needs GovCheck-specific semantics. |
| Quality, risk and security | ISO 25010; NIST SP 800-160; functional-safety lifecycle | Good quality/security examples; domain-specific profiles remain necessary. |

### 11.2 Areas not yet covered sufficiently

The current source set is broad enough to derive a candidate relationship model, but it is **not an exhaustive systematic literature review**. Remaining gaps include:

- formal decision theory, multi-criteria decision analysis, value-based engineering and explicit trade-off calculus;
- human factors, user-centered design, accessibility and stakeholder participation beyond systems-engineering ConOps;
- privacy, data governance, AI/agentic-system assurance and software supply-chain assurance;
- additional safety domains (rail, aviation, medical devices, nuclear) and their sector-specific assurance/certification relationships;
- legal/regulatory obligations and the semantics of external normative sources;
- product/service management practices for non-commercial, research, infrastructure and internal repositories;
- model-based systems engineering beyond SysML v2, including architecture frameworks and semantic web/linked-data profiles;
- formal semantics of relation assertions, defeasible reasoning, uncertainty, deontic constraints and authority changes.

The next research pass should select these areas according to GovCheck's general-purpose scope, identify primary sources and systematic reviews, and record why any area is included, deferred or out of scope. It should not attempt to collect every domain standard indiscriminately.

### 11.3 Search and inclusion method

This was a targeted cross-domain search, not a registered systematic review. Search areas included lifecycle engineering, requirements traceability, goal-oriented requirements engineering, architecture description/processes, decision rationale, assurance cases, provenance, configuration management, quality measurement, security engineering and functional safety. Sources were prioritized in this order: current standards and official specifications; official government/agency guidance; systematic literature reviews; peer-reviewed research; then industry practice documents where they directly informed the intent-record question.

The search is sufficient to show that no single external standard covers the complete relationship graph and to identify the major complementary families. It is not sufficient to claim exhaustive coverage of every relevant discipline or domain-specific standard.
