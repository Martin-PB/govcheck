# 0025 — Cross-domain lifecycle observations, PEAK decision traceability and SACM integration

**Status:** research and architecture recommendation for review. This record proposes semantic connections; it does not claim that runtime collection, a PEAK workflow, SACM import/export or automated reassessment is implemented.  
**Language:** English is the default; see the [French counterpart](0025-runtime-observations-peak-and-sacm.fr.md).

## 1. Purpose and scope

GovCheck is intended to govern a software repository throughout its lifecycle: from project intent and initial structure, through requirements, architecture, implementation, testing, verification, review, change acceptance, release, operation, maintenance and eventual retirement. Its subject is the governed repository and its evolving project state—not security alone, and not a particular engineering method.

The concerns governed by a project may include, as applicable:

- goals, stakeholder needs, functional and non-functional requirements;
- architecture, interfaces, design constraints and technical debt;
- implementation practices, code quality and maintainability;
- tests, static and dynamic analysis, model checking, program verification and theorem proving;
- dependencies, supply chain, reproducibility and build integrity;
- security, privacy, safety and operational resilience;
- documentation, licensing, legal or regulatory obligations;
- change management, reviews, approvals, releases, support and maintenance.

No project is required to adopt every concern or every method. Applicability and depth depend on the project's declared context, profile, obligations and authorized decisions. GovCheck must make selections, omissions, unknowns and their consequences explicit rather than imposing a universal engineering stack.

This record addresses three related but distinct needs:

1. connect observations from the repository lifecycle and, where relevant, deployed operation to the governed project model;
2. use **PEAK** to make the inputs, rationale, solution and assumed risk of decisions traceable;
3. define how the full SACM assurance-case metamodel is represented and governed as a dedicated GovCheck capability, and how it connects to the wider repository-governance model.

PEAK and SACM do not solve the same problem and are not alternatives to one another. Neither is the whole of GovCheck.

## 2. GovCheck foundations to preserve

This work extends the existing architecture; it must not create a parallel governance model.

- **Specification 0002** defines the canonical governance package: stable rule identities, typed rules, scope, applicability, composition, exceptions, profiles and controlled documentation projections.
- **Specification 0003** defines the repository change lifecycle independently of Git, Pijul, a forge or a CI product. Decisions bind exact base/candidate and governance states; acceptance and application are distinct.
- **Specification 0005** distinguishes claims, arguments, evidence, assumptions, context, limitations, method classes and acceptance. Tests, model checking, theorem proving, implementation conformance and normative fidelity are not interchangeable.
- **Architecture 0013** supplies the broad conceptual vocabulary linking goals, requirements, norms, properties, contracts, models, implementation artifacts, methods, evidence, claims, arguments and authorized decisions.
- **Architectures 0017 and 0021** address artifact identity/revision, evidence binding, freshness, dependency invalidation and assurance arguments.
- **Architecture 0024** proposes a guided, non-destructive bootstrap in which projects select capabilities and assurance methods according to their context.

These documents describe a general repository-governance foundation. Security and threat modelling are important domain capabilities within it, not the organizing principle for every other capability.

## 3. PEAK: trace the reasoning behind a decision

PEAK is used here in its decision-analysis sense: **Problem, Experience, Assumptions and Knowledge** are made explicit as inputs to a decision; the decision process records the selected **Solution** and the **Assumed Risk** [R-74](../references.md#r-74). The distinction between assumed risk, risk assessment, treatment and acceptance is informed by [R-193](../references.md#r-193).

A GovCheck decision can expose these dimensions without turning them into four isolated data silos:

| PEAK dimension | Decision-traceability question | Possible GovCheck links |
|---|---|---|
| **P — Problem** | What needs to be decided, and within what scope and constraints? | Goal, requirement, issue, change, affected artifact, stakeholder need |
| **E — Experience** | What relevant experience informs the decision? | Prior decisions, incidents, defects, test history, maintenance experience, operational lessons and expertise |
| **A — Assumptions** | Which premises are being relied upon, and under what conditions? | Explicit assumptions with owner, scope, rationale, validity, confidence and review/falsification conditions |
| **K — Knowledge** | What information is available to the decision-makers? | Specifications, architecture, measurements, test results, proofs, dependency facts, observations, standards and other admissible evidence |
| **Solution** | What option was selected, and why? | Selected alternative, rejected alternatives, rationale, implementation or follow-up plan |
| **Assumed Risk** | What may not work as envisioned, and what exposure is knowingly taken by choosing the solution? | Risk scenarios, assumptions, untested dependencies, possible consequences, uncertainty, accountable owner and review triggers; not synonymous with assessed risk, residual risk or authorized acceptance |

PEAK is not an authorization mechanism, risk formula, assurance-case notation or repository lifecycle model. GovCheck must supply the governance around a decision: identity, authority, scope, participants, time, rationale, evidence links, validity, review and supersession. Keep four concepts distinct: PEAK **Assumed Risk** is a decision output describing what may not work as envisioned; **Risk Assessment** is a separate method-bound analysis; **Risk Treatment** changes exposure; **Residual Risk** is what remains after specified treatment; and **Risk Acceptance** is an authorized, scoped and time-bounded disposition. The original assumed-risk statement remains part of the historical decision record when later assessments or controls change.

The same PEAK structure can be useful for decisions about architecture, maintainability, testing strategy, dependency upgrades, release readiness, security treatment or project governance. Its use should be proportional to the importance and consequences of the decision; it should not become mandatory paperwork for every trivial choice.

A decision and an assurance case answer different questions. A decision record explains what was considered and chosen, including assumed risk. An assurance case explains why a scoped claim should be believed, based on argument, assumptions and evidence. One decision may use several assurance cases; one assurance case may inform several decisions. Their links are many-to-many and must be bound to context and revision.

## 4. Observations as lifecycle feedback

GovCheck should be able to relate observations to the exact project/repository state and to the requirements, assumptions, claims, methods, decisions and risks they may affect. The observation sources are not limited to production telemetry.

Examples include:

- a test failure, regression trend, flaky test or changed coverage;
- a static-analysis finding or a newly detected maintainability issue;
- a build reproducibility failure or a changed toolchain;
- a dependency release, end-of-life notice, vulnerability advisory or license change;
- a review finding, rejected change, defect report or support incident;
- documentation drift or a mismatch between specification and implementation;
- a formal-model counterexample, failed proof obligation or changed proof dependency;
- a runtime alert, deployment drift, service degradation or security incident.

These observations may challenge an assumption, indicate that a requirement is not met, invalidate evidence, reveal a new risk, or trigger a review of a decision. They do not all have the same evidential meaning. A test failure is not automatically proof of a general defect; a static-analysis warning is not automatically a confirmed vulnerability; a metric change is not by itself a governance violation; and a runtime alert is not automatically a confirmed incident.

### 4.1 A general feedback cycle

1. **Observe:** record an event or observation from a tool, repository artifact, reviewer, operator or external source.
2. **Bind:** identify the exact repository, artifact, revision, environment, method and relevant time window.
3. **Assess quality:** record provenance, integrity, completeness, coverage, tool/source health, uncertainty and limitations.
4. **Interpret:** relate the observation to applicable requirements, properties, claims, assumptions, dependencies, risks and decisions.
5. **Derive a finding or hypothesis:** preserve the distinction between raw observation, interpretation, suspected cause and confirmed conclusion.
6. **Assess impact:** identify which evidence, claims, approvals, plans or decisions may need revalidation or review.
7. **Decide:** let the competent authority choose whether to investigate, correct, defer, accept a bounded deviation, change a requirement or take another authorized action.
8. **Verify the response:** record follow-up evidence and whether the intended result was achieved.

This cycle is domain-neutral. Domain-specific interpretation remains with the relevant method or capability. For example, threat-model feedback is one specialized path: operational security observations may challenge threat assumptions or control effectiveness, but they do not silently rewrite the threat model or authorize remediation. Continuous-monitoring guidance, runtime-certification research and industry runtime-threat-modelling work illustrate this security-specific path [R-75](../references.md#r-75) [R-76](../references.md#r-76) [R-72](../references.md#r-72). The ACCESS research also illustrates the use of runtime data in evolving SACM-based assurance cases [R-70](../references.md#r-70). The same general pattern applies to quality, maintainability, tests, dependencies, proof and release governance.

### 4.2 Observation and evidence records

Do not overload one record with raw observation, interpretation and assurance conclusion. A useful separation is:

**Observation/event record**
- stable identity and schema revision;
- source/producer, tool or sensor identity and version;
- event, observation and ingestion times where relevant;
- exact subject binding: repository, artifact, commit/revision, configuration, environment and scope;
- method, invocation/configuration and raw result or immutable reference/digest;
- provenance, integrity, completeness, coverage and source health;
- uncertainty, limitations, privacy/classification and retention metadata;
- links to related artifacts, requirements, claims, assumptions, risks and decisions.

**Derived finding/assessment/evidence record**
- exact input observation IDs and transformation/method revision;
- interpretation method and responsible producer/reviewer;
- finding, hypothesis or conclusion, with alternatives and counterevidence;
- affected scope, requirements, properties, claims, controls or decisions;
- uncertainty, limitations, status and invalidation/reassessment conditions.

An observation can be used as evidence, but it is not automatically admissible evidence for every claim. The existing Specification 0005 and Architecture 0021 semantics govern whether evidence is relevant, sufficiently trustworthy, current and within scope.

## 5. SACM: a complete assurance capability within GovCheck

SACM (Structured Assurance Case Metamodel) defines a structured metamodel for assurance cases. GovCheck should support the full SACM 2.4 Beta 1 semantic scope as a dedicated assurance capability, not merely as a narrow interchange adapter. Architecture 0026 defines the target: complete coverage of SACM's normative metamodel and faithful preservation of the explicitly non-normative supporting constructs, with a pinned version and demonstrated conformance [R-34](../references.md#r-34) [R-73](../references.md#r-73).

SACM is not a competitor to PEAK. PEAK helps expose the reasoning inputs and assumed risk behind a decision; SACM represents structured assurance arguments. GovCheck may use both for different purposes, while retaining its own repository-governance semantics. PEAK decisions may refer to SACM cases and elements, and SACM claims may refer to GovCheck goals, requirements, revisions and evidence through explicit typed links. Research on assurance-case engineering also emphasizes explicit defeaters, counterevidence and the strength of evidence—concerns relevant to how GovCheck evaluates arguments, regardless of whether SACM is used as an interchange format [R-71](../references.md#r-71).

### 5.1 SACM capability scope

The following table is illustrative and uses familiar 2.3-era names; it is not the exhaustive 2.4 coverage inventory. The complete, version-pinned 2.4 Beta 1 metamodel inventory and its normative/non-normative conformance points are specified in Architecture 0026.

| SACM construct | Potential GovCheck use |
|---|---|
| AssuranceCasePackage | Package a structured assurance case and its references |
| Claim / Assertion | Represent scoped claims and explicit states such as assumed, asserted, needing support or defeated |
| ArgumentReasoning / AssertedInference | Represent reasoning and inference relationships |
| AssertedEvidence / AssertedContext | Link evidence and contextual premises to argumentation |
| ArtifactReference / Artifact | Reference exact repository artifacts, specifications, configurations, reports and results |
| Event / Activity / Technique / Participant / Resource | Describe relevant artifact lifecycle events and evidence-production context |
| TerminologyPackage | Exchange controlled terminology |
| Package interfaces and bindings | Relate modular assurance cases |

These constructs may reduce the amount of assurance-case machinery GovCheck needs to invent. They do not establish that a claim is true, that evidence is fresh, that a decision is authorized, or that an implementation conforms to a specification. Those meanings still depend on GovCheck's own scope, provenance, authority, lifecycle and evaluation rules.

This table is illustrative and uses familiar 2.3-era names; it is not the 2.4 coverage inventory. The complete, version-pinned 2.4 Beta 1 metamodel inventory and its normative/non-normative conformance points are specified in Architecture 0026.

### 5.2 Boundary and composition with GovCheck

The scope distinction is architectural, not a comparison or ranking. SACM governs the semantics of the assurance-case capability; GovCheck governs the repository and its full lifecycle.

SACM does not define the complete governance of a software repository across its lifecycle. It does not by itself provide GovCheck's canonical rule authority, repository change/acceptance lifecycle, project bootstrap and capability selection, artifact/version governance, actor authority and delegation, or the domain-specific policies and methods a project may select.

Nor does SACM define all the domain semantics that projects may need, such as maintainability policy, test strategy and adequacy, dependency lifecycle, build/release governance, security threat scenarios, privacy obligations or operational response. It can represent assurance arguments about such matters, but it does not supply those domain models and decision policies.

SACM constructs are therefore first-class within the assurance capability, while cross-domain GovCheck concepts remain first-class in their own right. Mappings must preserve distinctions between claims, assumptions, evidence, inference, observation, requirement, finding, decision and authority. Architecture 0026 specifies the complete SACM coverage target and the cross-model integration contract.

### 5.3 SACM 2.4 Beta 1 as the pinned engineering target

OMG lists SACM 2.4 Beta 1 (September 2026) as an in-process version while 2.3 remains formal [R-73](../references.md#r-73). The beta introduces or clarifies Foundation/MOF alignment, package semantics, explicit claim subjects, argument context, assessments, joins, advanced argument descriptors, typed named values, and views/diagrams. The issue tracker also distinguishes normative metamodel changes from non-normative supporting constructs.

GovCheck should pin the exact Beta 1 PDF and machine-readable metamodel for its prototype, preserve normative status distinctions, and track the final 2.4 release through an explicit migration. The complete coverage and conformance strategy is specified in Architecture 0026.

## 6. GovCheck semantic architecture: a common foundation, multiple domains

The architecture should be **multi-domain and capability-oriented**, not security-centred and not built around one external metamodel.

The canonical GovCheck governance model remains responsible for rules, authority, applicability, lifecycle, decisions and conformance. Domain capabilities add typed concepts, relations, methods and evidence requirements where needed. A project profile selects applicable capabilities and their dependencies; it does not replace the common governance foundation.

Illustrative capability domains include:

- **Product and requirements:** stakeholder needs, goals, functional requirements, acceptance criteria and traceability.
- **Architecture and design:** components, interfaces, constraints, architectural decisions and technical debt.
- **Implementation and maintainability:** code ownership, quality constraints, complexity, modularity, maintainability findings and remediation.
- **Testing and validation:** test plans, cases, suites, environments, coverage, results, regressions and adequacy arguments.
- **Formal methods and proof:** models, properties, assumptions, model-checking runs, proof obligations, proof artifacts and conformance relations.
- **Dependencies and supply chain:** dependency identity, versions, provenance, licenses, vulnerabilities, support status and upgrade decisions.
- **Security, privacy and safety:** assets, threats, attack paths, controls, privacy requirements, hazards and treatment decisions.
- **Documentation and compliance:** normative projections, documentation coverage, obligations, attestations and review records.
- **Build, release and operations:** reproducibility, artifacts, release manifests, deployment state, service observations, support and retirement.

These are candidate domain boundaries, not a mandatory fixed taxonomy. Some projects will combine them; others will need additional domains. The model must permit explicit capability definitions and versioned extensions without making each domain invent its own incompatible identity, provenance, decision and evidence system.

Cross-cutting concepts should include:

- stable identity, revision and lifecycle state;
- goal, requirement, rule, property and contract;
- actor, role, authority, delegation and approval;
- artifact, dependency, relation and exact subject binding;
- method, execution, observation, finding and evidence;
- assumption, uncertainty, limitation and counterevidence;
- claim, argument, assessment, risk and decision;
- applicability, validity, freshness, invalidation and reassessment;
- provenance, audit history and controlled documentation projection.

Typed relations connect the common foundation and domain records: derivesFrom, refines, constrains, appliesTo, implementedBy, verifiedBy, testedBy, evidencedBy, supports, refutes, assumes, dependsOn, affects, invalidates, supersedes, reviewedBy and authorizedBy. Domain-specific relations (for example threatens, mitigatedBy or regresses) are added only with explicit semantics.

### 6.1 Views and integration

- **PEAK view:** expose the Problem, Experience, Assumptions and Knowledge informing a decision, then its Solution and Assumed Risk.
- **SACM assurance capability:** represent and validate the complete pinned SACM metamodel; preserve non-normative supporting constructs and provide lossless import/export/round-trip for SACM-native semantics. Cross-links to GovCheck lifecycle and domain artifacts remain explicit.
- **Domain views:** present the relevant requirements, artifacts, methods, evidence and decisions for testing, maintainability, formal proof, dependencies, security or another selected capability.
- **Lifecycle view:** show how project intent, requirements, architecture, implementation, verification, acceptance, release, operation and maintenance relate over time.
- **Operational feedback view:** show observations, derived findings, affected assumptions/claims/decisions and required reassessments.

These are projections over governed records, not competing sources of truth. Editing a view must result in explicit, validated GovCheck changes with the required authority.

## 7. Cross-domain invariants

1. Every observation, result and decision is bound to its exact subject, revision, method, scope and provenance.
2. Raw observations and historical decisions are preserved; corrections and reinterpretations create linked records rather than silently rewriting history.
3. An observation is not automatically a fact, a finding, evidence for a particular claim, or an authorized decision.
4. Assumptions, evidence, inference, conclusion, uncertainty and limitation remain distinguishable in every domain.
5. A method establishes only what its declared scope, inputs, configuration, execution and trusted base support.
6. Evidence freshness and invalidation follow declared dependencies; a changed artifact, requirement, tool, environment or assumption triggers the appropriate reassessment, not an indiscriminate global reset.
7. A missing result is not a passing result. Unknown, not applicable, not run, unsupported, incomplete, failed and passed remain distinct.
8. A metric or aggregate score must not conceal its underlying evidence, assumptions, uncertainty or domain-specific meaning.
9. A decision records its authority, rationale, scope, alternatives, validity and review conditions. PEAK can make its reasoning legible but does not grant authority.
10. Domain-specific conclusions do not silently alter canonical governance rules. Normative changes follow the governed change lifecycle.
11. GovCheck's SACM capability must preserve every construct in its pinned SACM metamodel and report any unsupported semantics; no normative SACM construct may be silently dropped or simplified.
12. Security-specific rules—such as threat-model review and risk acceptance—apply within their declared domain and do not become universal rules for unrelated project concerns.

## 8. Recommendations and staged work

### Recommendations

- Keep GovCheck's repository-wide governance and lifecycle model as the organizing foundation.
- Treat domain capabilities as composable and selectable; do not make security, formal methods, tests or any single discipline mandatory for every project.
- Use PEAK as a decision-reasoning and traceability method where decision significance warrants it. Do not compare it with SACM.
- Conform to the SACM metamodel within the assurance-case capability. Do not expand SACM's scope to replace GovCheck's repository-wide governance, authority or lifecycle model.
- Preserve the existing distinction between normative governance, domain methods, evidence, assurance arguments and authorized decisions.
- Keep the model extensible and method-neutral. Prefer adapters and explicit mappings to forcing every discipline into one external standard.

### Proposed sequence

1. **Repository-wide capability map:** reconcile the domain list with existing specifications, architecture records, artifact catalogue and bootstrap capabilities. Identify overlaps, omissions, dependencies and ownership.
2. **Cross-domain semantic mapping:** map the common concepts in 0002/0003/0005/0013/0017/0021 to domain-specific records without duplicating identity, provenance, authority or lifecycle semantics.
3. **Decision record and PEAK view:** define how Problem, Experience, Assumptions and Knowledge link to alternatives, Solution, Assumed Risk, authority and later reassessment.
4. **Observation/finding contracts:** define general event/observation and derived finding/evidence records, with exact subject binding, provenance, uncertainty, privacy and invalidation.
5. **Domain feedback patterns:** specify how observations update the relevant domain assessment—such as maintainability, test adequacy, dependency status or threat assumptions—without silently changing normative rules.
6. **SACM conformance prototype:** derive the complete Beta 1 metamodel inventory, implement the semantic coverage matrix, and test lossless import/representation/export/round-trip. Integrate assurance cases with GovCheck goals, requirements, artifacts, evidence, changes and decisions through explicit typed mappings.
7. **Formal models and tests:** verify common lifecycle properties such as authority, invalidation, review and acceptance, then add domain-specific properties where justified.
8. **Bootstrap integration:** expose domain capabilities and their dependencies through the guided profile, with explicit selection, omission, migration and non-destructive behavior.

## 9. Limits and non-decisions

This record does not finalize a universal domain taxonomy, select a graph database or serialization, prescribe a single quality/risk score, mandate PEAK for every decision, make SACM the repository-wide governance metamodel, or claim that observation collection and automated reassessment are implemented. It does not make security or formal verification mandatory for every repository.

The central design question is how GovCheck can govern a repository across its full lifecycle while allowing different engineering domains and methods to coexist: shared identity, authority, provenance, decisions and lifecycle semantics, with domain-specific models and evidence requirements where they are actually needed. PEAK contributes decision traceability; SACM supplies the assurance-case metamodel within its domain. Neither replaces the wider GovCheck governance architecture.
