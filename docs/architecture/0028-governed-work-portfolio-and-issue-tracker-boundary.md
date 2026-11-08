# 0028 — Governed work portfolio and issue-tracker boundary

**Status:** architecture proposal for review; no backlog registry, GitHub Project configuration, workflow automation or conformance control is implemented by this record.  
**Language:** English is the default; see the [French counterpart](0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md).

## 1. Purpose

Define how GovCheck discovers, qualifies, retains, prioritizes, authorizes, executes and closes proposed work without confusing an issue-tracker record with a decision, requirement, commitment or completed result.

The architecture is tool-independent. GitHub Issues and Projects are the initial operational adapter, not the canonical governance model. Another forge, a local-first interface or a future adapter must preserve the same semantics.

The design responds to a recurring failure mode: creating an issue is mistaken for accepting its proposal; assigning a priority is mistaken for authorizing work; closing an issue is mistaken for proving its intended result.

## 2. Architectural decision

Adopt a **three-stage governed work portfolio**:

1. **Intake:** a signal or subject has been recorded for qualification. It is not yet accepted into the retained backlog.
2. **Candidate backlog:** the subject has been examined and explicitly retained as a candidate for future work. Retention is not authorization to execute.
3. **Committed work:** a bounded item has been authorized and is sufficiently specified to enter an execution plan.

These are governance states, not three mandatory databases or repositories. They may be presented as views over one issue tracker, provided the state and its transition history are explicit and auditable.

A GitHub issue may serve as:
- an intake record;
- the coordination dossier for a candidate;
- the coordination dossier for committed work;
- a parent/container linking independently traceable work items.

The issue is not itself the canonical representation of a decision, requirement, assurance claim, evidence item, implementation result or acceptance event. Those remain typed project artifacts linked by stable identity and revision.

## 3. Concepts and boundaries

| Concept | Meaning | Canonical representation |
|---|---|---|
| Signal | Observation, request, idea, defect report, question or external recommendation | Source observation or intake record |
| Work subject | A topic requiring qualification or possible action | Governed portfolio entry |
| Work item | A bounded outcome to be delivered and verified | Work-item record; may be coordinated by an issue |
| Decision | Authorized selection, rejection, deferral or constraint | Decision record / ADR with authority and scope |
| Requirement | Normative or contractual condition | Versioned specification or governance rule |
| Plan | Ordered/dependent proposal for carrying out work | Versioned plan or execution dossier |
| Evidence | Information admissible for a scoped claim | Evidence record or immutable artifact reference |
| Result | Produced change or verified outcome | Commit, PR, release, report or other versioned artifact |
| Acceptance | Authorized determination against an exact candidate and applicable governance | Acceptance event bound to exact identities |

An issue can link to any of these; it must not collapse them into one prose body or comment thread. Comments are discussion history, not authoritative decision records unless an explicit governance rule defines a typed, attributable decision event.

A parent issue is an organizational container. It does not automatically become an epic with inherited priority, authority or acceptance. Child work items retain their own scope, owner, criteria, status and traceability.

## 4. Portfolio lifecycle

### 4.1 Intake

Any contributor may submit a signal, subject to repository policy. Intake should preserve:
- origin, reporter/producer and creation time;
- the observed/requested fact, clearly separated from interpretation;
- source links and supplied evidence, with provenance and limitations;
- affected project/domain when known;
- duplicate/similar-item links;
- uncertainty and missing information.

Intake is deliberately permissive. A low-quality or unverified report can be recorded without being represented as a confirmed defect, risk, requirement or commitment.

### 4.2 Qualification

A triage decision classifies the subject, at minimum, as one of:
- retain for research or investigation;
- retain as a candidate work item;
- split into independently deliverable subjects;
- merge/link as duplicate or related;
- defer pending evidence or a decision;
- reject as out of scope, invalid or not worth pursuing;
- close as already covered, superseded or no longer relevant.

The resolution, rationale, authority where required, and links to the resulting records must be retained. Rejection is not deletion; a later new signal may reopen the question with new evidence.

### 4.3 Candidate backlog

A candidate is retained for possible future execution. It must state, proportionately:
- intended outcome and beneficiary/problem;
- scope and explicit non-goals;
- current understanding, assumptions and unresolved questions;
- work nature and affected domains;
- expected deliverable(s) and observable completion conditions;
- known dependencies, constraints and risks;
- relevant decisions, requirements, architecture records and evidence;
- why it remains a candidate and what would cause reconsideration.

A candidate may be deliberately underspecified when research or a decision is the work. It must not be disguised as implementation-ready.

### 4.4 Commitment and execution

A candidate becomes committed only through an explicit authorization by the competent authority, according to the project's governance regime. Commitment requires a bounded execution unit with:
- a defined outcome and scope;
- acceptance/completion criteria;
- applicable requirements and decisions resolved, or explicitly listed as prerequisites;
- dependencies and sequencing understood sufficiently for execution;
- verification/evidence approach proportionate to impact;
- responsible actor(s), review/approval roles and constraints;
- an execution window or planning context when the project uses one.

Commitment is distinct from assigning an issue, adding it to a Project, setting a priority, assigning a milestone or moving it to an “In progress” column. Tool operations may represent a commitment only when a defined, attributable governance transition authorizes them.

Changes to scope, requirements, dependencies, candidate identity or governance authority may invalidate the commitment or return it to qualification. The history is preserved; invalidation does not erase prior authorization.

## 5. Work-item decomposition and relationships

Decompose a subject when it contains independently deliverable outcomes, distinct decisions, separate authorities, materially different verification, or work that can be accepted separately. Keep a single item when the parts cannot meaningfully be delivered or accepted independently.

Model relations explicitly and directionally where semantics require:
- `derived-from` / `reported-by`;
- `refines` / `decomposes-into`;
- `depends-on` / `blocks`;
- `related-to` / `duplicates);
- `implements` / `satisfies`;
- `changes` / `supersedes);
- `verified-by) / `evidenced-by`;
- `authorized-by) / `accepted-by).

Relations must identify the relevant artifact revision or event when a mutable target would make a bare link ambiguous. Cycles in dependency relations must be detected; cycles in ordinary related-to links are not inherently errors. A parent-child relation must not imply dependency unless explicitly stated.

The portfolio must support bidirectional traceability:
- from goal, decision, requirement or finding to candidate, committed work, change and verification;
- from every work item and delivered result back to its originating rationale, authority, scope and applicable governance.

## 6. Classification, stage and priority

Classification dimensions answer different questions and must not be overloaded.

### 6.1 Work nature

Use one primary work nature per active work item:
- decision;
- audit;
- research;
- specification;
- implementation;
- verification;
- integration;
- maintenance.

Documentation is normally a deliverable of one of these work natures, not a universal work nature. Create a separate documentation class only if the project demonstrates an independently governed documentation workflow.

### 6.2 Domain

Use zero or more domain areas when they materially help navigation (for example governance, assurance, authority, evaluation, bootstrap, formal methods, distribution, references, integrations or operations). Avoid one label per architecture record, tool or external standard.

### 6.3 Stage

Stage represents portfolio maturity or execution state, not normative acceptance:
- needs-triage;
- needs-evidence;
- needs-decision;
- needs-specification;
- ready;
- in-progress;
- blocked;
- validation.

A stage transition must be supported by the item dossier. “Done” is represented by closure and a recorded resolution, not a permanent stage label. A decision being accepted is a separate decision event.

### 6.4 Priority

Priority expresses relative urgency/value within a declared planning context. It is not effort, confidence, maturity, severity alone or authorization. If priority cannot be justified, leave it unassigned pending triage rather than inventing P2.

Use a small ordered scale (P0–P3) only with published criteria and periodic review. P0 is reserved for immediate threats to governance integrity, safety/security or a critical delivery gate; P1 for a material prerequisite/blocker; P2 for planned normal work; P3 for deferrable improvement. Priority changes require rationale and preserve history.

### 6.5 Risk and decision facets

Risk labels identify material cross-cutting attention (e.g. security, breaking change, governance, data loss, external dependency); they do not replace a risk record or assessment.

Decision facets (normative, architecture, technology, policy, scope) apply only when an actual decision is required. A research task that may inform a future decision is not automatically a decision task.

## 7. GitHub Issues and Projects adapter

GitHub is the initial adapter. Use:
- **Issues** for intake and work coordination, discussion, references and decomposition;
- **Projects** for portfolio views, grouping, sorting, planning and structured fields;
- **labels** for stable, reusable classification dimensions;
- **milestones/iterations** only for explicit planning windows or deliverable groupings;
- **PRs, commits and releases** for change/result identities, linked back to work items.

Prefer structured Project fields for portfolio stage, priority, target window, ownership and commitment where available. Labels are best for multi-dimensional classification and filtering, not for encoding every mutable workflow fact. GitHub label prefixes are conventions, not enforced mutually exclusive types; any one-value-per-family rule must be checked by process or automation.

The adapter must not infer:
- candidate status merely from an open issue;
- commitment from a priority, assignee, milestone or Project membership;
- approval from a PR review unless the governance authority and exact candidate binding are satisfied;
- completion or assurance from issue closure;
- normative truth from comments, labels or board columns.

The adapter must preserve stable links and, where possible, native IDs plus repository identity. Portability requires an export/import mapping that does not lose identity, relation direction, decision history, provenance or state-transition rationale.

## 8. Closure, supersession and history

An item may close with a typed resolution:
- delivered and verified to stated criteria;
- decision made (with decision-record link);
- rejected/out of scope;
- duplicate (with canonical item link);
- superseded (with successor link);
- no longer relevant;
- withdrawn by originator/authority.

“Delivered” requires links to actual results and verification evidence appropriate to the claim. It does not automatically mean the change was accepted, released or deployed; those are separate lifecycle events.

Reopening creates a new qualification of changed circumstances or new evidence; it must not rewrite the old resolution. Superseded items remain addressable. Retention and privacy follow repository policy; do not retain sensitive material in public issue bodies when a controlled evidence store is required.

## 9. Governance invariants

The following are architecture-level requirements proposed for later specification and conformance checks:

1. **Creation is not acceptance:** an intake record creates no obligation to execute.
2. **Priority is not authority:** priority and scheduling cannot authorize normative or operational action.
3. **Open is not backlog membership:** issue state alone does not establish candidate retention.
4. **Candidate is not commitment:** retained work is not authorized execution.
5. **Commitment is explicit:** authorization identifies actor/authority, scope, time and governance revision.
6. **Unknown is visible:** missing scope, rationale, authority, dependencies or criteria remain unknown/blocked, never silently satisfied.
7. **Decision is a typed artifact:** material decisions are not inferred from discussion or merge.
8. **Traceability is bidirectional:** work and results link to rationale; rationale links to work and evidence.
9. **Closure is not proof:** closure resolution and result evidence are distinct.
10. **History is append-preserving:** state changes, priority changes, decisions, invalidations and resolutions remain attributable.
11. **Decomposition is semantic:** parentage does not imply dependency, shared authority or inherited acceptance.
12. **Adapter neutrality:** forge-specific fields and behavior do not become canonical semantics.

## 10. Operational policy and review cadence

At triage, identify the subject, its provenance, work nature, area, next information/decision needed and provisional disposition. Do not force a priority before there is enough context.

At backlog refinement, review candidate value, rationale, duplicates, decomposition, dependencies, stale assumptions, decision prerequisites and whether the subject still merits retention. A candidate without a plausible outcome or reconsideration trigger should be closed or rewritten.

Before commitment, verify the readiness conditions in §4.4. At execution review, check scope drift, dependency changes, blockers and evidence freshness. At closure, record typed resolution and link results.

The cadence is project-defined; the architecture does not mandate Scrum, sprints, story points, velocity, estimates or a particular planning methodology. Small projects may use lightweight manual review. Automation should enforce only deterministic invariants and must not manufacture semantic judgments.

## 11. Application to current GovCheck discussion

The recent analysis issues illustrate why intake and commitment must be separated:

- **Issue #23 — “Analyse Claude”:** an analytical intake/candidate concerning conceptual gaps and research directions. Its recommendations are not all accepted requirements. Retain only the resulting bounded subjects after reconciliation with existing Specifications 0005/0015 and Architecture Records 0022–0027; avoid maintaining a permanent umbrella issue as a substitute for traceable work.
- **Issue #26 — “perplexity”:** an analytical intake with a more concrete proposed execution sequence. Its backlog list is not an authorized plan. The base-governance-revision question identified in its P0 proposal requires an explicit decision and specification before dependent implementation is committed.

The issue discussions and their comments remain source material. This architecture does not retroactively convert their recommendations into approved policy or claim that labels, Projects fields or automation have been configured.

## 12. Adoption and implementation sequence

1. Review and authorize this architecture; reconcile terminology with Specifications 0002–0005 and Architectures 0013–0015, 0022–0027.
2. Define the minimal work-item and transition records in the canonical governance model; decide which fields are normative and which are adapter metadata.
3. Configure GitHub Project fields and views as an adapter; establish labels only for stable classification dimensions.
4. Qualify a representative sample of open issues, including #23 and #26, without assuming that all open issues belong to the retained backlog.
5. Add deterministic checks for required classification, invalid stage combinations, missing links and transition evidence only after the semantics are specified.
6. Test export/import and a second adapter or neutral fixture to demonstrate that the model is not GitHub-shaped.
7. Add formal models or mutation tests only for identified high-consequence transition and concurrency properties; do not claim that this architecture itself is formally verified.

## 13. Non-goals and limitations

This record does not select a product-management methodology, mandate Scrum, prescribe estimation, create a new database, require a graph database, make GitHub normative, define a complete project-management schema, authorize any current issue, or claim an implemented backlog engine. It does not replace the repository change lifecycle, decision framework, assurance model or artifact identity/versioning policies.
