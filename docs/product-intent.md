# GovCheck product intent — governed constitution and evolution

**Record type:** product-intent and design-direction record; not an ADR and not an adoption of implementation choices.  
**Status:** owner-stated intent captured for systematic architecture review. The repository owner retains decision authority; recommendations in this record are not approved policy merely by being written here.  
**Language:** English is the default; see the [French counterpart](product-intent.fr.md).

## 1. Purpose of this record

This record captures the product-intent evolution discussed while reconsidering the package bootstrap and the apparent need for two `AGENTS.md` files. It deliberately preserves the reasoning from the initial concern through its refinement:

1. A reusable GovCheck package and the GovCheck repository itself both need agent instructions, but their instructions cannot be the same: the repository's root `AGENTS.md` governs work on GovCheck itself, whereas a governed repository's `AGENTS.md` must reflect that repository's own approved governance.
2. A package cannot supply one universally canonical, ready-to-copy `AGENTS.md`. At most, GovCheck supplies reusable instruction structures, fragments, decision logic and generation mechanisms.
3. Bootstrapping is not merely copying a directory or rendering templates. It is the beginning of a governed process in which maintainers establish the repository's governance, authority, obligations, assurance expectations and applicable capabilities.
4. That process is progressive. It begins with a small set of foundational decisions and revisits further decisions when new concerns, changes, risks or evidence make them relevant.
5. Decisions are contextualized by sources, criteria and explicit reasoning. GovCheck may guide the decision deterministically, present raw material, or make that material available to an assisting agent; the authorized human or organizational authority remains responsible for approval.
6. Governance authority can be distributed by domain and category of decision. People implementing changes need not have authority to weaken the requirements against which those changes are assessed.
7. The initial governance model is restrictive and fail-closed. A block may be relaxed only through an explicit, traceable decision by the competent authority, within its authority and scope.

This is a product-intent baseline for subsequent impact analysis. It does not silently replace, amend or approve existing ADRs, specifications, architecture records, formal models or implementation contracts.

## 2. Product definition

**GovCheck is a system for constituting, expressing, justifying, governing, applying and evolving the governance and assurance of software repositories.**

It helps the people responsible for a repository to:

- establish a repository-specific governance model from an initially restrictive baseline;
- define authorities, roles, responsibilities, delegations and decision rights;
- identify the decisions required by the repository's context and lifecycle;
- discover and consult relevant sources and knowledge at the point of decision;
- reason about requirements, properties, risks and suitable assurance methods;
- record decisions, their authority, rationale, alternatives, assumptions, sources, scope and validity;
- translate approved decisions into applicable obligations and controlled human/agent-facing projections;
- evaluate proposed changes against those obligations and the required evidence;
- govern exceptions, risk acceptance, compensating controls and policy changes;
- revisit decisions when context, architecture, threats, requirements, evidence or organizational authority changes.

GovCheck is therefore more than a policy checker, bootstrapper, document generator, CI action or agent instruction set. Conformance checking is one important part of a larger decision and governance lifecycle.

The governed subject is the repository and its software lifecycle. Humans and coding agents are contributors within that governance. GovCheck is not primarily an agent sandbox, tool-call gateway, hosted approval service or replacement for a forge.

## 3. The package provides a framework, not a universal repository policy

The reusable GovCheck package defines the concepts, semantics, capabilities, source material, decision-support mechanisms, validation rules and generation facilities needed to construct and operate a repository-specific governance model.

It must not preselect every repository's:

- authority structure or separation of duties;
- decision categories and approval thresholds;
- domain capabilities or applicable standards;
- assurance methods for individual claims or properties;
- risk appetite, exception authority or release conditions;
- human/agent workflow or generated instruction content.

These are repository-specific decisions, subject to GovCheck's invariant semantic foundations and any explicitly applicable external obligations.

There is no package-level canonical `AGENTS.md` whose contents can be copied unchanged as the policy of every governed repository. GovCheck may ship generic templates, reusable fragments, explanatory guidance and rendering logic. The actual `AGENTS.md` is a repository-specific projection generated or checked from that repository's approved governance decisions, selected capabilities, applicable obligations and agent-facing operational needs.

The root `AGENTS.md` and `AGENTS.fr.md` in the GovCheck development repository remain specific to developing and governing GovCheck. They must not be confused with templates or outputs intended for repositories that use the product. A template filename such as `AGENTS.md.tmpl` is one possible packaging technique, not a settled implementation requirement.

The same principle applies to `GOVERNANCE.md`, `SECURITY.md`, `CONTRIBUTING.md`, CI configuration, policy bundles and other projections: they are derived or controlled representations, not independent normative authorities.

## 4. Progressive constitution: bootstrap is the beginning, not the whole process

### 4.1 Inspect before asking

For an existing repository, GovCheck should inspect the repository's observable state and available governance material before asking questions. For a new or empty repository, it should start from the information supplied by its maintainers.

Inspection results are observations, not approved decisions. GovCheck must distinguish observed facts, user-provided facts, inferred hypotheses, unknowns and approved governance choices. It must not silently convert a detected workflow, branch rule, document or tool configuration into an authorized policy.

### 4.2 Ask only the foundational questions initially

The initial journey should establish enough to operate safely, not force users through every possible governance topic. Depending on context, foundational questions include:

- Who is establishing the initial governance and what authority do they hold?
- What is the governed repository and what is its intended purpose and operating context?
- Who may make, approve, review or revoke governance decisions?
- What initial change-acceptance boundary must be protected?
- Which minimum records, provenance and evidence are required?
- Which decisions may be deferred, and what operations must remain blocked until they are made?

The exact initial questionnaire, mandatory fields and bootstrap state machine remain to be designed. An unanswered question must remain explicitly unanswered; it must not be assigned a permissive default.

### 4.3 Progressive and event-driven decisions

The governance model is expected to grow as the repository and organization evolve. New decisions may be triggered by, for example:

- a new requirement, claim, property, component or domain;
- a change in architecture, deployment, data sensitivity or threat context;
- a proposed dependency, integration or external interface;
- a new assurance gap, failure, incident or contradictory observation;
- a change in applicable law, contract, standard or source publication;
- a change in team structure, authority, delegation or responsibility;
- a change to an assurance method, verification tool or trusted base;
- an attempted operation blocked because a required decision or evidence is missing.

GovCheck should identify the affected decisions, explain why they are needed and request only the decisions relevant to the current context. It should not repeatedly ask users to decide matters already covered by valid, applicable, approved rules. Nor may it silently infer a new decision from prior behavior.

A decision may be deferred, but the model must represent its state, owner/authority, trigger or review condition, and the operations blocked while it remains unresolved.

## 5. Decision authority is distributed by domain and decision category

Authority is not necessarily concentrated in one maintainer or one role. A repository may delegate distinct decision categories to maintainers, architecture, quality assurance, security, operations, product owners, a committee or named individuals.

For example, a quality-assurance authority may decide which properties require empirical tests, model checking, program verification, formal proof or a combination. Developers may propose and implement changes and supply evidence, while remaining unable to unilaterally weaken those assurance requirements. On submission of a change, GovCheck evaluates it against the currently applicable QA decisions.

The governance model must be able to express at least:

- the subject, domain and category of a decision;
- the authority holder (person, role, team, committee or organization);
- the exact powers granted and their limits;
- the scope, conditions and effective period of authority;
- delegation and sub-delegation, including whether further delegation is allowed;
- proposal, review, approval, rejection, revocation and appeal responsibilities;
- separation-of-duty and conflict-of-interest constraints;
- required quorum, independence or multiple approvals where applicable;
- succession, unavailability and authority-revocation behavior;
- provenance and evidence that an actor was authorized at the time of decision.

Authority is semantic governance data, not merely a GitHub permission, branch-protection setting, account membership or agent capability. Forge controls may enforce parts of a decision but do not define its normative authority. A delegate cannot grant powers they do not possess, and a decision cannot be accepted merely because an integration reports success.

## 6. Sources and contextual decision support are product capabilities

### 6.1 Sources are presented when relevant

GovCheck's reference work is not only internal design bibliography. The product must be able to present relevant knowledge and sources to users in the context of the decision being considered.

Potential source classes include standards, laws and regulations, contracts, academic publications, government guidance, industry specifications, official tool documentation, project records, incident/operational observations and repository-specific evidence. Their authority and applicability differ; they must not be flattened into an undifferentiated list of citations.

A decision-support view should, where relevant, expose:

- the question and decision category;
- the repository facts, claims, requirements and properties involved;
- relevant source passages and stable source identities/revisions;
- source type, issuing body, publication/version/date and applicability;
- whether a source is normative, contractual, advisory, empirical, academic or merely informative;
- the claims or criteria supported by each source, and the limits of that support;
- contradictions, superseded publications, uncertainty and missing sources;
- existing repository decisions and comparable precedents;
- alternatives, consequences, costs, assumptions and residual uncertainty.

Sources inform a decision; they do not automatically make the decision or grant authority. Inclusion in a catalogue does not mean adoption, applicability or proof of conformity.

### 6.2 Preserve the reasoning chain in both directions

The intended traceability includes, as applicable:

`Source → supported assertion / observation → criterion → recommendation / argument → decision → rule / requirement → property → verification method → evidence → evaluation / acceptance`

Each link must be explicit enough to distinguish direct support from interpretation or inference. The reverse navigation matters too: from a source to the decisions and rules that rely on it, and from a failed check to the requirement, decision, argument and sources behind it.

The product should preserve source identity, version or revision, retrieval/provenance data, relevant passage or locator, applicability, trust classification and freshness. Corrections or supersession of a source should make affected decisions discoverable for review; they must not silently rewrite historical decisions.

### 6.3 Multiple decision-support modes

GovCheck should support three complementary modes:

1. **Deterministic guidance:** explicit criteria, rules, questionnaires and decision trees whose version and rationale are governed and testable.
2. **Agent-assisted deliberation:** an agent receives the decision context, applicable governance, source material, criteria, uncertainty and authority boundary, and can explain alternatives, ask questions, compare evidence and draft a reasoned proposal.
3. **Direct expert decision:** an authorized person can inspect the underlying material and record a decision without following a wizard or using an agent.

An agent may summarize sources or recommend an option, but it must identify uncertainty and source limitations. It cannot approve a decision unless a separately authorized governance rule explicitly grants that decision power to the agent under controlled conditions. Human/organizational authority remains the default decision authority.

Decision trees and recommendations are themselves governed artifacts: they need stable identity, versioning, source provenance, applicability, limitations and validation. A decision tree must not disguise a contested judgment as an objective fact.

## 7. Assurance is selected for claims and properties, not by tool preference or maturity tier

GovCheck should start from what a repository needs to establish, not from a preferred tool or a universal ladder of assurance.

For each claim, requirement or property, it should help determine which methods are suitable, complementary or insufficient. Candidate methods include empirical tests, property-based/fuzz testing, static analysis, inspection, runtime observation, model checking, program verification, theorem proving, implementation/specification conformance and structured assurance arguments.

For each candidate method, explain:

- what it can establish and what it cannot;
- the subject to which the result applies (model, implementation, process, artifact or operational system);
- assumptions, bounds, environment and trusted base;
- completeness and coverage limitations;
- required skills, tools, reproducibility and maintenance cost;
- expected evidence and how that evidence can become stale or be invalidated;
- residual gaps and complementary methods.

Methods are not interchangeable. A test is empirical testimony about executed cases, not a theorem proof. Model checking supplies results about a declared model, configuration, bounds and assumptions, not automatic proof of implementation correctness. A checked formal derivation is distinct from model-checking evidence. Program verification and implementation conformance also require their own explicit scope and trust arguments. An assurance argument structures claims and evidence but does not make unsupported premises true.

No formal method is mandatory merely because GovCheck is used, and no formal method is categorically superior for every claim. A single repository may use different methods for different properties, or combine methods for one property. The decision and its rationale belong to the authority assigned to that decision category.

A quality-assurance team is one possible authority for assurance-method requirements. It can prescribe the evidence required for a class of properties independently of the developers who implement changes. GovCheck then checks submitted changes against those requirements; it does not ask each developer to renegotiate them.

## 8. Fail-closed by default; relaxation is an explicit governed decision

### 8.1 Restrictive initial baseline

The initial governance model should be as restrictive as is reasonably necessary to avoid implicit authorization. Missing, ambiguous, conflicting, stale, unsupported or unverifiable mandatory information must not be interpreted as permission, approval, satisfaction or successful assurance.

At minimum, the intended semantics are:

- undefined authority does not authorize a decision;
- missing approval does not count as approval;
- an unresolved mandatory decision remains unresolved and blocks dependent operations;
- missing required evidence does not satisfy an evidence requirement;
- an absent, failed, partial, stale or unsupported check is not a pass;
- an unrecorded assumption cannot silently support a claim;
- an unknown or conflicting evaluation cannot authorize acceptance;
- an undeclared delegation grants no power;
- an expired, revoked, out-of-scope or state-mismatched exception is invalid;
- inability to perform a required check does not itself waive the requirement;
- a recommendation, agent response, CI success or forge permission is not an approval unless the governance model explicitly says so.

States such as unknown, not assessed, not applicable, not run, unsupported, incomplete, failed, conflicting and passed must remain distinct. In particular, absence of a decision is not a negative decision, and not-applicable is not the same as satisfied.

### 8.2 Block only the dependent scope

Fail-closed does not mean indiscriminately freezing an entire repository. A missing decision or failed requirement should block the operation, transition, artifact or release that depends on it. Unrelated work may continue where the governance model establishes that it is independent and safe to do so.

The dependency and impact analysis must be explicit. If GovCheck cannot establish that an operation is outside the blocked scope, uncertainty must not be used to bypass the block.

### 8.3 Relaxation is a governed decision, never an “ignore” shortcut

When a block occurs, GovCheck should identify the blocking rule/requirement, its origin decision, the affected scope, the competent authority, the missing or failed condition, and the consequences of relaxation. The authority may maintain the block, request more evidence, grant a bounded exception, accept a residual risk, require compensating controls, amend the policy prospectively, or change the assurance strategy.

At least four semantically distinct mechanisms are required:

- **Waiver:** a scoped exception to an otherwise applicable requirement, if that requirement is waivable.
- **Risk acceptance:** explicit acceptance by the authorized risk owner of a described residual risk; this does not turn failed evidence into passing evidence.
- **Policy amendment:** a prospective change to the general rule by the authority competent to amend it.
- **Compensating control:** an alternative control that may meet an objective through a different mechanism, with its own adequacy assessment.

These mechanisms are not interchangeable. Replacing a proof requirement with tests, for example, changes the assurance basis and leaves different limitations; it must not be represented as equivalent proof.

Every relaxation must record the authority and authorization basis, reason, exact requirements/rules, repository and artifact scope, validity interval or review trigger, risk and consequences, alternatives considered, supporting sources/arguments, compensating controls, residual gaps, required approvals and revocation/expiry conditions. A relaxation cannot exceed the authority's scope or duration, and cannot be silently generalized.

### 8.4 Preserve history and authority boundaries

Relaxations do not erase prior failures, evidence or decisions. Policy amendments are prospective unless a separate, explicit and valid rule defines otherwise. Expired or revoked exceptions cease to authorize future operations. Historical records remain addressable and may require separate requalification.

No person or agent may relax a requirement without the relevant authority. Delegation cannot exceed the delegator's own powers. If the competent authority is unavailable or cannot be established, the restrictive behavior remains in force. Separation-of-duty constraints continue to apply to exception and policy-amendment decisions.

## 9. Change evaluation applies decisions made by the proper authorities

A proposed change is evaluated against the governance revision and decisions applicable to its exact context. GovCheck should:

1. identify the candidate change and affected repository artifacts/properties;
2. resolve applicable requirements, rules, profiles and decision records;
3. establish the authority, scope, validity and provenance of those decisions;
4. determine the expected checks, evidence, reviews and approvals;
5. evaluate supplied evidence against the specified method and exact subject/state;
6. report pass, fail, indeterminate, conflict, unsupported and evidence gaps distinctly;
7. enforce the acceptance predicate, including valid exceptions and compensating controls;
8. identify any new decision that must be made by a competent authority.

Developers can propose changes to requirements or assurance strategy, but cannot weaken them merely by changing code, tests, generated documents or CI configuration. Changes to governance follow the governance decision lifecycle and are themselves subject to authority, review and traceability.

## 10. Product capability map

The product intent implies at least these cooperating capabilities:

| Capability | Responsibility |
|---|---|
| Governance modelling | Express governance concepts, authority, roles, powers, scopes, rules, obligations, prohibitions, permissions and lifecycle states. |
| Repository discovery | Inspect existing state and distinguish observations, assertions, assumptions and approved decisions. |
| Progressive constitution | Ask contextual questions and establish the initial repository governance without requiring an exhaustive first-run questionnaire. |
| Authority and delegation | Resolve who may propose, decide, approve, delegate, revoke or accept risk for each decision category. |
| Knowledge and source management | Catalogue, qualify, version, retrieve and contextualize sources and source-derived assertions. |
| Decision support | Present criteria, alternatives, decision trees, arguments, uncertainty and agent-assisted deliberation. |
| Decision management | Record proposals, approvals, rationale, assumptions, validity, review, supersession and provenance. |
| Assurance management | Relate claims and properties to suitable methods, evidence, assumptions, limitations and freshness. |
| Policy and model validation | Detect inconsistency, incompleteness, conflict, unsafe composition, invalid delegation and unsafe relaxation. |
| Projection generation/conformance | Generate or verify repository-specific `AGENTS.md` and other human/agent-facing projections from approved governance. |
| Change conformance | Evaluate changes and enforce the acceptance boundary against applicable approved decisions. |
| Exception and risk governance | Manage waivers, risk acceptance, policy amendments, compensating controls, expiry and revocation. |
| History and audit | Preserve append-only decision/evidence provenance and reconstruct why a result was reached. |

These are conceptual responsibilities, not a commitment to a monolith, service topology, command structure or plugin architecture.

## 11. Trust and authority boundaries

- The repository's approved, versioned canonical governance model remains the sole normative authority for that repository, interpreted under explicitly identified semantics/evaluator.
- GovCheck's product metamodel defines what can be represented; it does not itself choose every repository's policy.
- Repository maintainers and delegated authorities make repository-specific decisions within their recorded powers.
- Sources inform decisions but do not themselves grant authority or prove applicability.
- Agents can assist with discovery, explanation and proposal; they cannot silently approve or relax policy.
- VCS, forge, CI and local executable results are evidence or enforcement mechanisms within stated trust boundaries, not substitutes for normative authority.
- Human-readable documents and agent instructions are controlled projections or explanations. They do not create competing policy.
- GovCheck must not claim implementation, enforcement, proof or conformance that has not been demonstrated for the exact scope and state.

## 12. Relationship to existing GovCheck design

This intent builds on and requires a systematic impact review of, at least:

- ADR 0001 — bootstrap boundaries and repository-centred governance;
- ADR 0003 — product package versus GovCheck's own meta-level history;
- Architecture 0012 — canonical normative authority and documentation conformity;
- Architecture 0013 — governance metamodel;
- Architecture 0014 — governed development workflow and actor responsibilities;
- Architecture 0015 — conformance tool and validation plan;
- Architecture 0018 — version governance and approval authority;
- Architecture 0021 — assurance claims, arguments and evidence freshness;
- Architecture 0022 — governance capability audit;
- Architecture 0023 — initial bootstrap governance authority;
- Architecture 0024 — project bootstrap, governance choices and assurance profiles;
- Architecture 0025–0027 — lifecycle observations, SACM capability, domain semantics and decision models;
- Specification 0002 — canonical governance model;
- Specification 0003 — change lifecycle;
- Specification 0005 — assurance model;
- Specification 0006 — governance revision applicability;
- the formal lifecycle, applicability, publication, evaluator, exception, revocation and journal models;
- the reference catalogue and its bidirectional citation/backlink integrity;
- the package bootstrapper, templates, manifests, generated projections, CI and conformance checks.

This list is a starting impact inventory, not a claim that every listed artifact is inconsistent or must be rewritten. Existing useful semantics should be preserved where compatible. Conflicts, omissions and duplicate concepts must be identified explicitly before implementation.

## 13. Intended next work

The next work should proceed in controlled stages:

1. **Capture and reconcile:** retain this intent as a first-class design record and map every statement to existing decisions, specifications, architecture records, references, issues and code.
2. **Impact analysis:** classify existing material as compatible, complementary, incomplete, conflicting, superseded or requiring a decision. Identify duplicated or missing concepts and both English/French drift.
3. **Conceptual model:** specify decision categories, authority/delegation, contextual sources, decision-support artifacts, progressive questions, assurance selection, fail-closed semantics, scoped blocks and relaxation mechanisms.
4. **Authority and semantics:** identify which matters are already owner-decided, which are design proposals and which still require the owner's explicit decision. Do not infer adoption from this intent record.
5. **Formalization:** define safety properties and transition semantics; select verification methods based on the claims and abstraction, without making a particular formal tool mandatory for all users.
6. **Architecture and specification evolution:** update or supersede existing records with traceable rationale and bilingual counterparts; keep the single central reference catalogue and complete backlinks.
7. **Implementation planning:** only after the model is reconciled, decompose the work into atomic issues and dependency-aware changes, then implement in reviewable increments with evidence.

The package/bootstrap and `AGENTS.md` generation design should not be implemented in isolation before these semantics are understood.

## 14. Explicit non-goals and unresolved choices

This intent does not select:

- a canonical serialization, schema technology, expression language or policy engine;
- a particular theorem prover, model checker or proof assistant as a mandatory GovCheck dependency;
- an interactive UI framework, agent harness, MCP server, hosted service or remote authority;
- a fixed number of governance roles or decision domains;
- a universal assurance score or maturity tier;
- one universal decision tree for all domains;
- a universal default `AGENTS.md` policy;
- an assumption that every repository needs every domain capability or every assurance method.

These require separate, evidence-based design and explicit authority decisions where normative.

## 15. Foundational product invariants to formalize

The following are proposed invariant statements for the impact analysis and subsequent formalization. Their inclusion here records intent; it does not claim they have already been adopted into the executable canonical model or verified.

1. **Single repository normative authority:** no projection, agent, CI configuration or source catalogue silently becomes a competing policy authority.
2. **Authority-bound decision:** every normative decision is attributable to an authority competent for its category, scope and time.
3. **No implicit permission:** absence, ambiguity, unknown, failure or inability is never silently interpreted as permission or approval.
4. **Fail-closed acceptance:** mandatory unresolved, conflicting, unsupported or unsatisfied conditions cannot yield acceptance.
5. **Scoped blocking:** a block applies to all dependent operations and no unrelated operation unless dependency cannot safely be excluded.
6. **Explicit relaxation:** every relaxation is a valid, traceable decision by a competent authority and is bounded by scope, time and conditions.
7. **No authority escalation:** delegation and exception powers cannot exceed the authority that grants them.
8. **Evidence is not decision:** evidence, recommendation, test result, model-checking result, proof result and acceptance decision remain distinct record types and meanings.
9. **Method non-substitutability:** assurance methods retain their distinct semantics, assumptions and limitations; substitution requires an explicit decision and records the changed assurance basis.
10. **Source provenance:** source-derived recommendations and decisions retain source identity, revision, applicability and reasoning links.
11. **No silent adoption:** a recommendation, template, discovered configuration or this intent record does not become approved policy without the required decision.
12. **History preservation:** policy changes, waivers, revocations and requalification preserve prior decisions and evidence rather than rewriting history.
13. **Progressive constitution:** unresolved decisions remain explicit; new decisions are requested when relevant, while valid existing decisions are reused within scope.
14. **Projection fidelity:** generated or checked human/agent-facing documents faithfully reflect approved rules and cannot add, remove or weaken normative content.

## 16. Status and interpretation

This record is a detailed statement of product intent and a basis for architecture refactoring. It is not itself an ADR, a normative repository policy, an approved implementation plan or evidence that any capability exists. The current governance authority process remains applicable. The repository owner alone may approve changes to the product's normative direction under the current project arrangement.

All future changes derived from this intent must preserve the distinction between owner decisions, design proposals, recommendations, external source claims, formal model results and implemented behavior.

## Impact analysis

See the companion [product-intent impact analysis](product-intent-impact-analysis.md) ([French](product-intent-impact-analysis.fr.md)) for the first reconciliation of this intent with existing ADRs, architecture records, specifications and product boundaries. It is a working audit, not an adoption decision.
