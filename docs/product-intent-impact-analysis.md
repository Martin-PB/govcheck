# Product-intent impact analysis — governance constitution and lifecycle

**Status:** working design audit for maintainer review; not an ADR, adoption event or implementation contract.  
**Parent:** [GovCheck product intent](product-intent.md). **French:** [version française](product-intent-impact-analysis.fr.md).

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

Primary internal sources: ADRs 0001, 0003 and 0007; Architectures 0012–0015, 0018 and 0021–0027; Specifications 0002–0006; and the parent product-intent record. Each source's own status controls how strongly it supports a conclusion.

External references remain in the single catalogue docs/references.md: authority/separation of duties (R-01–R-03), assurance cases/SACM (R-04, R-33–R-34, R-71, R-73), evidence provenance (R-06–R-08), policy evaluation/model verification (R-09, R-10, R-88), PEAK (R-74), agent instruction conventions (R-104), domain semantics (R-94–R-103) and normative modalities (R-93). No competing catalogue is introduced and citation does not imply adoption as a dependency.

This document is an impact-analysis baseline. It does not amend existing decisions, adopt proposed architecture contracts, assign authority to a QA team inside GovCheck, select technologies or claim implementation/verification. GovCheck's current root authority remains that recorded in Architecture 0023. Each adopter chooses its own authority structure through its own authorized bootstrap decisions. Update this audit as artifacts are inspected. Any normative change still requires the applicable authority decision and adoption event.
