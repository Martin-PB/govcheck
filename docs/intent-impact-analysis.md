# Intent impact analysis — governance constitution and lifecycle

**Status:** working design audit for maintainer review; not an ADR, adoption event or implementation contract.  
**Parent:** [GovCheck intent](intent.md). **French:** [version française](intent-impact-analysis.fr.md).

## 1. Executive finding

The expanded product intent does not require discarding GovCheck's existing foundations. Architectures 0013–0015 and 0021–0027, together with Specifications 0002–0006, already anticipate much of the required vocabulary and behavior: canonical governance, progressive bootstrap, selectable assurance methods, scoped authority and delegation, source traceability, domain semantics, fail-closed evaluation, bounded exceptions and change conformance.

The principal gap is integration. These elements remain distributed across records with different statuses and levels of maturity. They do not yet constitute one adopted, executable product model. The next phase must reconcile semantics, authority and lifecycle dependencies before implementing a new questionnaire or rewriting the bootstrapper.

GovCheck is to be understood as a **governance constitution, decision-support, assurance and lifecycle-conformance system**. Bootstrap is its first guided constitution process, not a one-time flat questionnaire. Decisions are categorized by domain, owned by competent authorities, informed by contextual sources, and revisited when relevant changes invalidate their basis.

## 2. Status discipline

This analysis distinguishes:
- **Recorded decision:** an explicit decision with its own authority basis (notably Architecture 0023 for GovCheck's current root authority and ADR 0004 for version governance).
- **Proposed design:** architecture/specification material awaiting the applicable adoption event.
- **Implemented or verified capability:** only what repository artifacts and execution evidence demonstrate. A design record or model-checking report does not establish operational capability.
- **Impact finding:** compatibility, gap, ambiguity or required elaboration identified by comparison with the product intent.

This is a first-pass semantic audit, not yet a line-by-line audit of every implementation file, model, test, issue, CI workflow and translation.

## 3. Existing foundations to preserve

| Record | Existing contribution | Impact |
|---|---|---|
| ADR 0001 | Repository-centred governance, one normative authority, local executable, VCS/forge separation, Git and Pijul as distinct systems. | Compatible. Clarify progressive constitution rather than fixed-tree installation. |
| ADR 0003 | Generic product package separated from GovCheck's own meta-level history. | Compatible in principle. Recast package as reusable models, knowledge and generation mechanisms, not a universal adopter policy or blindly copied tree. |
| ADR 0007 | Mandatory capture of sources for GovCheck design decisions. | Compatible. Extend source provenance into each adopting repository and each relevant decision. |
| Architecture 0012 | Canonical authority, controlled projections, stable rule IDs and drift detection. | Compatible. Add explicit category-scoped decision authority and contextual source-derived recommendations. |
| Architecture 0013 | Goals, requirements, norms, properties, contracts, models, methods, evidence, claims, arguments and decisions; PEAK rationale. | Core foundation. Make authority grants and qualified source records first-class linked objects. |
| Architecture 0014 | Contributor, reviewer, assessor, authorizer and governed change dossier. | Compatible. Scope powers by decision category and action, not only workflow stage. |
| Architecture 0015 | Discovery, documentation conformity, traceability, checks, assurance and authority/application. | Compatible but incomplete as product map: constitution and decision support must be explicit capabilities. |
| Architecture 0018 + ADR 0004 | Category-specific identity/versioning and approval authority. | Adopted foundation; preserve. Do not confuse artifact versioning with policy authority. |
| Architecture 0021 | Claims, arguments, evidence, dependencies, invalidation and freshness. | Compatible. Link assurance-method selection and substitution to authority, rationale and consequences. |
| Architecture 0022 | Gap between design vocabulary and an adopted machine-readable authority/evaluator. | Still relevant; refresh its baseline against this expanded intent. |
| Architecture 0023 | One current root authority for GovCheck; delegation only through explicit governed change. | Existing GovCheck decision. Do not impose this single-owner structure on adopters. |
| Architecture 0024 | Staged bootstrap, context, governance choices, selectable domains/methods, inspect-plan-apply. | Strong alignment. Extend its staged dialogue to later change-triggered decisions. |
| Architecture 0025 | Lifecycle observations, PEAK decision rationale and SACM integration. | Compatible. PEAK, SACM and GovCheck authority remain distinct. |
| Architecture 0026 | Dedicated SACM 2.4 capability and semantic coverage target. | Compatible specialized capability; not a universal GovCheck metamodel. |
| Architecture 0027 | Multiple specialized domain models and staged semantic commitments; DMN/BPMN/CMMN/SACM distinctions. | Core foundation for governed, explainable, domain-specific decision trees. |
| Specifications 0002–0006 | Canonical model, change lifecycle, adapters, assurance and temporal authority applicability. | Compatible proposed contracts; add explicit decision-category, source and decision-trigger links. |

## 4. Required semantic integration

### 4.1 Progressive constitution and decision lifecycle

Architecture 0024 already rejects an exhaustive flat questionnaire. The product intent requires a continuous lifecycle:
1. Ask only foundational questions needed to establish repository identity and safe initial authority.
2. Record decisions, deferred matters, unknowns and not-applicable determinations distinctly.
3. During a change, detect new decisions required by affected properties, domains, risks, obligations or governance changes.
4. Request the missing decision from the competent authority, reusing valid decisions already in force.
5. Revisit decisions when their assumptions, sources, scope, validity or dependencies change.

Required concepts include decision trigger, category, state, owner, competent authority, due/review condition, applicability, supersession, reconsideration trigger and dependency on unresolved decisions.

### 4.2 Category-scoped authority and delegation

Existing records provide much of the vocabulary, but GovCheck needs one coherent authority-resolution mechanism. A role label alone is insufficient. Each grant should identify:
- principal/group identity;
- decision categories and permitted actions (propose, assess, decide, approve, delegate, revoke, accept risk);
- repository, artifact, domain and organizational scope;
- validity interval and effective governance revision;
- constraints, separation-of-duty rules and prohibited combinations;
- delegation depth and onward-delegation permission;
- grantor, authorization basis, provenance, revocation and supersession history.

The QA example is a required fixture: a QA authority can determine the assurance method or minimum evidence for a class of properties, while developers propose and implement code changes. Developers cannot weaken the requirement through code, tests or CI changes. On submission, GovCheck resolves the applicable QA decision and evaluates conformance. This must remain one possible organization, not a hard-coded universal role model.

Architecture 0023 governs GovCheck's current root authority only. Each adopting repository constitutes its own authority arrangement through its authorized bootstrap decisions.

### 4.3 Sources as contextual decision inputs

GovCheck's central reference catalogue is the research/provenance register for GovCheck's own design. It is not a substitute for project-specific source registers in governed repositories.

A source record should capture stable identity, publisher/author, title, type and locator; exact revision and dates; relevant section; supported claim or criterion; applicability conditions and scope; limitations, uncertainty, conflicts and superseding sources; and links to questions, options, decision branches, claims, arguments, decisions and requirements.

At decision time, GovCheck should present sources relevant to the actual context, explain why each is shown and what it does or does not support, and preserve the exact source revision used. A source informs but does not grant authority or prove applicability. Discovery, qualification, interpretation, recommendation and authorized decision are separate stages. Agents may assist with summaries and comparison but cannot convert synthesis into approval.

### 4.4 Decision trees and assisted deliberation

Decision trees must be versioned, reviewable artifacts rather than hidden heuristics. They need question/answer semantics, prerequisites and branches, candidate options and consequences, source/claim links, unknown/conflict/not-applicable/deferred paths, competent authority, branch explanations, versions and tests.

A tree may recommend or narrow choices. It must not decide unless an applicable governance rule explicitly authorizes a deterministic decision. An agent is an optional deliberation assistant. The same decision model must be usable by humans, CLI, scripts and other interfaces.

### 4.5 Assurance-method selection per claim/property

Specification 0005 already distinguishes empirical execution, model checking, program verification, theorem proving, implementation conformance, normative fidelity and acceptance. Preserve these non-interchangeable meanings.

For each claim/property, the selection record should bind the exact proposition, subject, scope and failure consequence; applicable obligations and risk context; assumptions and abstraction boundaries; candidate methods and what they establish; admissibility, independence, cost, feasibility and tool constraints; residual uncertainty; competent decision authority; and reassessment triggers.

Do not ask for a new test/proof decision on every change. Reuse a valid decision while its scope and assumptions still apply. Reopen it when absent, invalidated, conflicting, out of scope or materially affected. Replacing proof with tests is not equivalence: tests remain empirical testimony; model checking concerns the recorded model and bounds; proof checking concerns a derivation under assumptions; implementation conformance needs its own relation and evidence.

### 4.6 Fail-closed behavior and governed relaxation

The intent is consistent with fail-closed semantics in Specifications 0002, 0003 and 0006 and Architecture 0024. Apply one rule across bootstrap, decision resolution, assurance, change evaluation and application:
- missing, unknown, ambiguous, conflicting, stale, unsupported or unverifiable mandatory information never grants permission;
- missing evidence never satisfies a requirement;
- agent output, source recommendation, CI success or forge permission is not an authority decision;
- unresolved conditions block dependent operations, not unrelated work whose independence is established;
- uncertainty about dependency scope cannot bypass a block.

A block report identifies the condition, rule and source decision, affected scope and dependencies, competent authority, evidence gap and lawful paths.

Keep four relaxation mechanisms distinct:
1. **Waiver:** bounded exception to a waivable requirement.
2. **Risk acceptance:** authorized acceptance of described residual risk; it does not turn failed evidence into passing evidence.
3. **Policy amendment:** prospective change by the authority competent to amend the rule.
4. **Compensating control:** alternative means whose adequacy is separately assessed.

Every relaxation is explicit, authorized, reasoned, scoped, time/review-bounded, source-linked and revocable. Prior failures and evidence remain in history. No generic ignore, force-pass or silent fallback is acceptable.

## 5. Boundaries that must not be conflated

| Potential ambiguity | Required resolution |
|---|---|
| One canonical governance model vs multiple domain standards | One GovCheck authority governs repository decisions and commitments; specialized domain models retain their semantics and are linked, not flattened. |
| Generic package vs adopter's AGENTS.md | Package supplies reusable projection contracts, templates and generators; adopter-approved governance determines generated content. No universal canonical adopter AGENTS.md policy exists in the package. |
| GovCheck root authority vs adopter's QA/security/release authorities | Architecture 0023 governs GovCheck only. Each adopter establishes its own authority constitution. |
| Formal foundations vs optional formal proof | Every repository has explicit claims, decisions, provenance and uncertainty; no specific prover, model checker or proof obligation is mandatory for every property. |
| Fail-closed vs progressive adoption | Unknown decisions remain unknown and block only dependent actions; staged constitution avoids requiring every decision at first run. |
| Decision-tree recommendation vs authority | Trees and agents explain/recommend; only an authorized actor or explicitly authorized deterministic policy decides. |
| Central catalogue vs project sources | Keep GovCheck's central design catalogue and support independent source registers in each governed repository. |
| Bootstrap vs later assurance changes | Bootstrap establishes initial commitments; later changes use the same decision lifecycle and authority checks. |

## 6. Package, bootstrap and AGENTS.md implications

The package must not ship a universal AGENTS.md purporting to prescribe each adopter's governance choices. It should ship the generic metamodel and decision semantics; source qualification mechanisms and starter references clearly distinguished from adopter sources; versioned decision models and domain decision-support assets; assurance method descriptions and selection criteria; fail-closed and relaxation semantics; projection contracts and generation rules; and deterministic bootstrap/migration mechanisms.

Bootstrap should inspect existing governance (or establish an empty-repository context), gather minimal foundational decisions, identify competent authority and bootstrap powers, present contextual sources, record decisions and uncertainty, derive a deterministic plan containing only applicable capabilities, expose collisions before application, generate repository-specific AGENTS.md and optionally AGENTS.fr.md from approved governance, preserve user content, and record package/model/source/generator revisions.

On each later change, the same engine determines whether a new decision is needed, who owns it and which existing decision remains applicable. This is not a separate questionnaire subsystem.

GovCheck root AGENTS.md and AGENTS.fr.md remain meta-level instructions for GovCheck contributors; they are not copied as adopter instructions.

## 7. Formalization targets

Before implementation, derive and verify at least:
- authority resolution is unique or returns unknown/conflict;
- decisions require authority valid for category, action, scope and time;
- delegation cannot exceed grantor powers or validity;
- missing/unknown never yields implicit permission;
- unresolved mandatory decisions block all and only dependent operations;
- recommendation cannot be mistaken for decision;
- source revisions and applicability survive into decisions;
- decision-tree paths are deterministic and explainable for pinned inputs;
- assurance method choice binds to a claim/property and competent authority;
- method substitution preserves semantic differences and records changed limitations;
- evidence invalidation propagates through dependent claims and decisions;
- relaxation is typed, authorized, bounded and revocable;
- policy amendment is prospective unless an explicit valid temporal rule says otherwise;
- projections faithfully represent approved governance;
- accepted and applied states identify the exact same candidate.

These are targets, not claims that current TLA+ models already cover them. Map existing lifecycle, applicability, assurance, publication and journal models to these properties; record overlap, gaps and model boundaries.

## 8. Repository-wide audit still required

Inspect, rather than assume:
1. all ADRs and decision/provenance records, their status, authority basis and references;
2. all architecture records 0006–0032 and both language versions;
3. Specifications 0002–0006 and French counterparts;
4. all formal/TLA+ models, configurations, assertions, TLC outputs and limitations;
5. schemas, version registries, decision records, manifests and release metadata;
6. govcheck package, bootstrapper, templates, capabilities and tests;
7. root scripts, package-alignment and reference-integrity checks, generated workflows;
8. open issues, governed-work portfolio items and pull requests, including duplicates/dependencies;
9. central reference catalogue and backlinks;
10. root/package agent instructions and their projection status.

For every artifact record identity/path, status, claims, sources, dependencies, language counterpart, intent mapping, compatibility class, gap/conflict, proposed action, required authority and verification evidence.

## 9. Recommended sequence

1. Complete repository-wide artifact and bilingual drift audit.
2. Build a traceability matrix from each intent requirement to records, sources, models, code, tests and work items.
3. Reconcile the metamodel: decision categories, authority grants, source qualification, decision-support artifacts, assurance selection, scoped blocks and relaxation.
4. Update architecture/specifications in dependency order with explicit statuses and reference backlinks.
5. Extend formal models and tests from reconciled semantics; record counterexamples and uncovered properties.
6. Define canonical schema/evaluator boundaries and technology decisions only when justified.
7. Refactor bootstrap and projection generation against approved contracts.
8. Decompose implementation into atomic governed work and reviewable PRs with CI evidence.

Do not begin with a large interactive questionnaire or an isolated rewrite of AGENTS.md templates. First make decision and authority semantics coherent.

## 10. Sources and limits

Primary internal sources: ADRs 0001, 0003 and 0007; Architectures 0012–0015, 0018 and 0021–0027; Specifications 0002–0006; and the parent intent record. Each source's own status controls how strongly it supports a conclusion.

External references remain in the single catalogue docs/references.md: authority/separation of duties (R-01–R-03), assurance cases/SACM (R-04, R-33–R-34, R-71, R-73), evidence provenance (R-06–R-08), policy evaluation/model verification (R-09, R-10, R-88), PEAK (R-74), agent instruction conventions (R-104), domain semantics (R-94–R-103) and normative modalities (R-93). No competing catalogue is introduced and citation does not imply adoption as a dependency.

This document is an impact-analysis baseline. It does not amend existing decisions, adopt proposed architecture contracts, assign authority to a QA team inside GovCheck, select technologies or claim implementation/verification. GovCheck's current root authority remains that recorded in Architecture 0023. Each adopter chooses its own authority structure through its own authorized bootstrap decisions. Update this audit as artifacts are inspected. Any normative change still requires the applicable authority decision and adoption event.

### 6.1 Observed bootstrap implementation (current main)

The current bootstrapper already has an existing-repository path; it would be inaccurate to describe it as empty-repository-only. The actual CLI exposes inspect, plan, apply and rollback. Inspect/plan are read-only; apply creates missing files, preserves differing collisions, is idempotent, records a package marker with package version/digest, selected capabilities and installed-file digests; rollback removes only unchanged files recorded as installed. The legacy one-argument mode is explicitly for empty targets and refuses non-empty targets.

However, this is still a **file-installation/capability-selection mechanism**, not the progressive governance constitution described by the intent. Its capability set is currently a fixed list (readme, check, decisions, docs, formal, scripts, workflows); omitted capability arguments select all of them. It does not yet conduct a contextual questionnaire, discover/qualify project-specific sources, establish repository-specific authority/delegation, record deferred/unknown/not-applicable decisions, choose assurance methods per claim/property, generate an adopter-specific AGENTS.md from approved decisions, or trigger decision reconsideration as later changes evolve. The inspect report also describes basic filesystem/Git presence and collisions, not a semantic inventory of project intent, requirements, risks, properties or existing governance.

**Impact classification:** preserve the safe inspect-plan-apply/rollback and collision protections as valuable bootstrap infrastructure. Evolve the plan input from a manually selected fixed capability list into a deterministic projection of approved, contextual governance decisions. Do not replace safe installation behavior with a questionnaire before the decision model, authority rules and migration contract are specified. The package README and ADR 0003 currently describe copying govcheck/ as-is; this must be reconciled with the intended generated, repository-specific constitution and with the fact that root GovCheck agent instructions are meta-only.

## 11. Existing governed-work portfolio alignment

The intent must be integrated into the repository-backed work portfolio; GitHub issues are coordination/navigation adapters and their presence does not itself authorize execution. The following open items are directly relevant and should be reconciled with the impact matrix before new work is created:

- [#78 — Governance, authority and decisions](https://github.com/Martin-PB/govcheck/issues/78), with child items #41 (governance-revision applicability), #60 (single-authority separation-of-duties risk), #67 (hosted CI authorization), #71 (future threshold/quorum authority evaluation), #75 (portfolio adoption) and #86 (temporal governance applicability). The new intent particularly expands the need for category-scoped grants, delegation and authority resolution; it does not itself authorize a multi-authority regime for GovCheck.
- [#79 — Evaluation and assurance](https://github.com/Martin-PB/govcheck/issues/79), including #52 (unknown causes/resolution policy), #68 (verifiability nature), #69 (claim argumentation), #72 (adversarial corpus) and #43/#44 (vertical implementation and attestations). These are the natural home for claim/property-specific method selection and non-interchangeable assurance semantics.
- [#81 — Formal models and lifecycle](https://github.com/Martin-PB/govcheck/issues/81), including [#73](https://github.com/Martin-PB/govcheck/issues/73) (inter-model contracts) and [#86](https://github.com/Martin-PB/govcheck/issues/86) (temporal authority applicability). Authority delegation, source provenance and scoped relaxation need explicit model coverage or explicit declared exclusions.
- [#82 — Bootstrap, package and distribution](https://github.com/Martin-PB/govcheck/issues/82), including [#62](https://github.com/Martin-PB/govcheck/issues/62) (existing-repository inspect/plan/apply). The current bootstrap implementation already has the non-destructive mechanics described above; the remaining product gap is decision-driven constitution, not merely adding existing-repository support again.
- [#83 — References and provenance](https://github.com/Martin-PB/govcheck/issues/83), including [#74](https://github.com/Martin-PB/govcheck/issues/74) (machine-verifiable reference status and provenance). Extend this work carefully: GovCheck's design catalogue and an adopter's contextual source register are related but distinct.
- [#84 — Multi-agent collaboration and attribution](https://github.com/Martin-PB/govcheck/issues/84): relevant to optional agent-assisted deliberation and attribution, but an agent must remain non-authoritative unless explicitly delegated a bounded decision power.
- [#85 — Schemas, fixtures and documentation quality](https://github.com/Martin-PB/govcheck/issues/85): appropriate for schema/fixture contracts and bilingual documentation integrity.

These portfolio items are not duplicated or automatically re-scoped by this analysis. Their repository-backed records, current status, dependencies and authorization must be inspected before changing them. The impact analysis should become a traceability input to those existing items, not a parallel backlog.

## 12. Formal-model coverage observed in the repository

The formal inventory shows that several requested behaviors already have separate bounded models. The new intent should extend and compose these models rather than create one monolithic governance state machine.

| Model / record | Existing modeled concern | Explicitly uncovered relative to the expanded intent |
|---|---|---|
| GovCheckAuthority.tla / Architecture 0023 | Initial single-root authority, amendment attribution, authority/revision continuity, append-only history. | Principal identity is abstracted; no category-scoped powers, delegation records, effective-position semantics, exception lifecycle or adopter-configurable authority constitution. |
| GovCheckGovernanceApplicability.tla / Specification 0006 / Architecture 0031 | Evaluation bound to the governance revision effective at an event position; later publication; historical decision binding; stale evaluation rejection. | Authority changes/delegation, distributed consensus, cryptographic identity, full multi-writer concurrency and implementation refinement. |
| GovCheckGovernanceControls.tla / Architecture 0033 | Prior evaluator remains authoritative during replacement; Pass/Fail/Unknown/Conflict distinction; bounded waivers for waivable requirements; revocation and append-only history. | Full decision-category authority, source-derived decision rationale, contextual decision trees, claim-specific method selection and implementation-level enforcement. |
| GovCheckAssurance.tla / Architecture 0021 | Finite acyclic claim graph, conjunctive argument closure, evidence dependencies/freshness, revocation/expiry, independent review and acceptance snapshot. | External truth, cryptographic provenance, assumption discharge, alternative argument strategies, method-selection deliberation and implementation refinement. |
| GovCheckLifecycle.tla / Specification 0003 | Change lifecycle and guarded transitions for exact candidates/governance identities. | The lifecycle model does not by itself resolve authority grants or the full semantic link to assurance and publication models; see issue #73. |
| GovCheckCanonicalPublication.tla / Architecture 0032 | Candidate evaluation, authorization and publication binding; stale-base exclusion; append-only publication. | Full organization-specific authority/delegation, source-informed decision support and production adapter/concurrency guarantees. |
| CICheckRouting.tla / Architecture 0029 | Concern-scoped CI routing and separation of verification workloads. | Does not itself decide repository assurance policy or authorize method selection. |

This coverage is grounded in the formal-model index and its stated limits. TLC success is evidence about each recorded finite abstraction only. It does not establish production enforcement, semantic adequacy of a decision, implementation refinement or properties outside the model. The cross-model contract tracked by [issue #73](https://github.com/Martin-PB/govcheck/issues/73) and the temporal authority work tracked by [issue #86](https://github.com/Martin-PB/govcheck/issues/86) are particularly important integration points.
## 10. External academic and industrial comparison

This first comparison informs the next metamodel work. It does not adopt an external lifecycle, notation or tool.

| Source | Established contribution | Relevance to GovCheck | Boundary |
|---|---|---|---|
| Anthropic, AI-native SDLC Playbook (2026), `intent.md` | Versioned, human-readable intent preserves the originating problem, expected outcome, users/systems, constraints and open questions, then feeds downstream specification. | Strong naming and conceptual precedent for the repository-level intent record. | Industry playbook, not a universal file-format standard. Anthropic also uses intent records for individual changes; GovCheck's repository-level intent has broader temporal scope. |
| ISO/IEC/IEEE 15288:2023 | Lifecycle-process framework from conception through retirement, applied iteratively and recursively. | Treats intent, requirements, decisions, realization and assurance as lifecycle concerns, not a one-time bootstrap. | Does not prescribe a particular lifecycle model, method, modeling approach or document name. |
| ISO/IEC/IEEE 29148:2018; DIS edition 3 | Requirements-engineering processes and information items; derivation, allocation, validation, verification and bidirectional traceability. | Distinguishes needs/expectations from requirements and supports derivation and allocation links. | 2018 remained current after 2024 review; the 2026 DIS is a draft under enquiry, not an adopted standard. |
| NASA Systems Engineering Handbook | Stakeholder expectations, ConOps, requirements, design, verification and validation are iteratively reconciled; bidirectional traceability across levels. | Supports consistency and upward/downward traceability across expectations, requirements, design and verification. | Domain-specific systems-engineering guidance, not a universal repository schema. |
| GORE: KAOS, iStar, GRL, Tropos | Goals motivate requirements; models express AND/OR refinement, operationalization, actors, dependencies, quality goals and trade-offs. | Richer relations between intent/goals, actors, alternatives, constraints and requirements. | 2026 reflection on the mapping study reports continuing industrial adoption barriers and uneven empirical evaluation; no single notation should be imposed. |
| OMG SysML v2.0 | Standardized modeling of requirements, behavior, structure, analysis and verification, with model relations and APIs. | Candidate vocabulary for typed derive/satisfy/verify/refine/allocate relations and model interchange. | Systems-modeling language, not GovCheck's repository-governance metamodel or mandatory exchange format. |
| OMG SACM 2.3 | Standardized assurance metamodel for claims, argumentation, artifact references, evidence, context and reasoning. | Useful for the assurance subgraph. | Does not define the full intent-to-requirements-to-decisions-to-specifications lifecycle. |
| UK Government ADR Framework (2025) | Decision records capture context, decision and consequences at appropriate authority levels. | Supports separate, authorized architecture decisions with rationale and consequences. | An ADR records a choice; it does not prove the choice satisfies intent or requirements. |
| IntentDocs `INTENT.md` | Published open format bundling product overview, personas, releases, stories and acceptance criteria. | Useful comparison point for an existing `INTENT.md` convention. | Its bundled model is not adopted because GovCheck keeps intent, requirements and acceptance evidence distinct. |

### 10.1 Preliminary relationship findings

The sources do not support a single linear chain. They support a typed, many-to-many, versioned graph with distinct relation semantics and lifecycle events. The next formal model must investigate at least:

- **Intent ↔ stakeholder needs/expectations:** one intent may summarize multiple needs; expectations may conflict, remain uncertain or lack validation.
- **Intent / needs → goals and outcomes:** goals refine purpose into desired states; outcomes need observable indicators or validation scenarios without assuming universal numeric metrics.
- **Goals → requirements:** requirements may derive from goals, external obligations, risks, standards or design constraints; self-derived requirements must be identified as such.
- **Requirements ↔ decisions:** decisions can create, select, constrain, interpret, defer, waive or amend requirements; requirements may motivate competing decisions.
- **Decisions ↔ architecture/specifications:** decisions select or constrain design alternatives; specifications describe required or intended behavior/properties. One decision may affect many specifications and vice versa.
- **Requirements / specifications / properties → verification and validation:** verification checks specified characteristics; validation asks whether the right system and intended outcomes have been achieved.
- **Claims → arguments → evidence/results:** assurance cases structure claims and reasoning; evidence supports claims only within declared scope, assumptions, provenance and freshness.
- **Implementation / operations ↔ observations and change triggers:** runtime observations, incidents and context changes may challenge assumptions, invalidate evidence and trigger reassessment of intent, goals, requirements or decisions.

These are research-derived candidate relation families, not an adopted GovCheck vocabulary or cardinality model.

### 10.2 Research gaps before adopting a formal relationship model

1. Distinguish purpose/intent, stakeholder need, expectation, goal, objective, outcome, requirement, constraint, decision, rationale, architecture element, specification, property, claim, argument, method, verification case, evidence and acceptance.
2. Define direction, cardinality, composition, provenance, temporal validity and authority for each relation; do not use one generic `traces-to` edge for every meaning.
3. Model alternatives, conflicts, contribution/satisfaction, refinement, derivation, allocation, realization, justification, approval, verification, validation, evidence support, rebuttal and invalidation.
4. Diagnose missing links, unsupported claims, orphan requirements, goals without operationalization, decisions without affected artifacts and evidence without claims.
5. Preserve reverse navigation and change impact: from evidence to the claim/requirement/decision/goal/intent it supports, and from changed intent or source to potentially affected descendants.
6. Compare GORE, ISO 29148/15288, SysML v2, SACM/GSN and industrial ADR/SDLC practices before selecting native GovCheck semantics or external mappings.

No relation, mandatory field, formal notation or external metamodel is adopted by this analysis alone.


## Reference catalogue links

- [R-01](./references.md#r-01)
- [R-03](./references.md#r-03)
- [R-04](./references.md#r-04)
- [R-06](./references.md#r-06)
- [R-08](./references.md#r-08)
- [R-09](./references.md#r-09)
- [R-10](./references.md#r-10)
- [R-33](./references.md#r-33)
- [R-34](./references.md#r-34)
- [R-71](./references.md#r-71)
- [R-73](./references.md#r-73)
- [R-74](./references.md#r-74)
- [R-88](./references.md#r-88)
- [R-93](./references.md#r-93)
- [R-94](./references.md#r-94)
- [R-103](./references.md#r-103)
- [R-104](./references.md#r-104)
- [R-114](./references.md#r-114)
- [R-115](./references.md#r-115)
- [R-116](./references.md#r-116)
- [R-117](./references.md#r-117)
- [R-118](./references.md#r-118)
- [R-119](./references.md#r-119)
- [R-120](./references.md#r-120)
- [R-121](./references.md#r-121)
