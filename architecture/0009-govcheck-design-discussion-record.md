# 0009 — GovCheck design discussion record and consolidated decision log

**Status:** Consolidated design record; it records decisions and proposals discussed on 5–6 November 2026. It does not itself make every proposed contract implemented or approved.  
**Language:** English is the default; the French counterpart is maintained at [0009 (français)](0009-govcheck-design-discussion-record.fr.md).  
**Related baseline:** ADR 0001; specifications 0002–0005; architecture documents 0006–0008; formal model `govcheck.lifecycle`.

## 1. Purpose, provenance and reading rules

This document consolidates the GovCheck design discussion into a durable repository record. It is intended to preserve the reasoning, decisions, constraints, unresolved questions and follow-up work that would otherwise remain scattered across conversation turns and pull-request descriptions. It is a synthesis, not a verbatim transcript. Where a later decision supersedes an earlier exploration, the current decision is stated and the earlier alternative is retained only to explain the design history.

The record is deliberately explicit about epistemic status:

- **Decision** means a product or architectural boundary the discussion settled.
- **Proposed contract** means a normative design target documented for review, not an implemented guarantee.
- **Current artifact** means a file or model present in the repository.
- **Observed verification** means a check actually executed and reported with its scope.
- **Open question** means no decision has been made; implementations must not silently choose a default.

The repository and PR history remain the authoritative record of source changes. This document explains why those changes exist and how they fit together; it does not replace the specifications or silently amend their normative semantics.

## 2. Product definition and boundaries

GovCheck is repository-centred software governance: it governs a software repository and the lifecycle of changes proposed against it. Developers and coding agents are contributors subject to repository governance; GovCheck is not primarily a governance system for agents themselves.

GovCheck is not:
- an agent sandbox or tool-call gateway;
- a hosted control plane or mandatory SaaS;
- a mandatory MCP server, resident daemon or network service;
- a replacement for project build systems, tests, scanners, CI providers or VCS tools;
- a bundle of scanners whose output is treated as governance by itself.

The intended primary interface is a small local executable usable by people, scripts, CI jobs and agents that can invoke local commands. It should provide machine-readable output. Local-only operation is a complete and first-class deployment mode. Shared or remote enforcement is an optional integration capability, not a prerequisite for the core product.

No three-tier model based on repository size is to be introduced. The formal governance and assurance foundations apply to every repository. Profiles and project-specific policies may vary the applicable obligations, evidence and execution commands; they do not remove the common semantic foundations.

## 3. Normative authority and documentation

The intended system has one normative authority: a versioned, machine-readable canonical governance model interpreted by GovCheck. Markdown files such as `AGENTS.md`, `GOVERNANCE.md`, `SECURITY.md` and `CONTRIBUTING.md` are controlled projections or explanatory material. They must not become competing sources of normative rules.

The canonical model is expected to express:
- package identity and semantic version;
- stable, immutable rule identifiers;
- typed rules and explicit normative force;
- applicability scopes and typed parameters;
- explicit relations such as dependency, refinement, supersession and incompatibility;
- repository profiles and bounded exceptions;
- projection metadata for generated or checked human-readable documents.

Rule kinds must distinguish obligations, prohibitions, permissions, invariants/constraints, evidence requirements, process/approval requirements and advisory guidance. Advisory guidance is explicitly non-normative. The absence of a prohibition is not permission. Precedence is an explicit partial relation, not file order or “last wins”.

Rule IDs are never recycled. Semantic changes require review and traceability; removed rules remain addressable through tombstones or supersession records. Contradictions, ambiguous precedence, malformed scopes, unsupported semantics and unresolved references are governance errors. Mandatory indeterminacy fails closed for acceptance.

English is the default presentation and landing language. French counterparts must preserve normative meaning and status. A translation discrepancy is documentation non-conformance, not an alternative policy source.

## 4. VCS, hosting, collaboration and acceptance are separate

Four dimensions must remain independent:

1. **Version control:** Git, Pijul and possible future VCSs.
2. **Hosting:** local, team-hosted, self-hosted or public.
3. **Collaboration:** individual work, shared work, review, patch exchange and integration requests.
4. **Acceptance/application:** the governance decision and the operation that applies an accepted candidate.

A Git branch, commit, worktree, pull request, Pijul patch, channel or Nest request is not itself the GovCheck change. These are native objects exposed by adapters. A PR/MR is a collaboration object, not the change record or the acceptance authority.

The governance core must not hard-code GitHub or any forge. Hosting and collaboration adapters may target GitHub, GitLab, Forgejo, Gitea, Nest or future systems, including local and team-operated deployments. A forge can transport reviews and enforce a gate only to the extent its declared capabilities allow.

### 4.1 Git

Git identity must account for more than HEAD when the candidate includes staged, unstaged or untracked content. Descriptors should distinguish commit/tree identity from index/worktree snapshots and account for submodules. A commit alone must not be presented as the complete candidate when the working tree differs.

### 4.2 Pijul

Pijul is first-class and semantically distinct, not a Git compatibility mode. Preserve native patch identities and dependencies, channel identity/state, graph semantics and native conflicts. Do not flatten Pijul into synthetic commits/branches or infer native conflicts from an unrelated textual merge tool. If an adapter cannot establish a required property, report unsupported/indeterminate rather than success.

### 4.3 Local and shared enforcement

Local hooks and wrappers can be bypassed by a user with filesystem or administrative access. A local executable cannot universally prevent direct file edits, replacement of the executable or bypass of hooks. Local acceptance must still apply the same predicate and state its enforcement limitations.

Strong shared enforcement requires a trusted team authority or forge integration that checks a decision bound to the exact repository candidate and governance revision at the integration boundary. Missing gate capability or administrator bypass must be visible; it must never be silently reported as a pass.

## 5. Canonical change lifecycle

A change is an identified proposal to move a repository from an exact base state to an exact candidate state. Its identity binds at least:

`(repository, base, candidate, governance revision/semantics, specification revision, change ID)`

The abstract lifecycle is:

`Proposed → Prepared → Evaluated → Reviewable → Accepted → Applied`

Additional states include `Stale`, `Rejected`, `Withdrawn` and `Superseded`. Implementations may add substates without changing the underlying distinctions.

Key separations:
- evaluation is not approval;
- evidence is not approval;
- approval is not acceptance;
- acceptance is not application;
- a model result is not implementation conformance;
- an adapter apply acknowledgement must identify the exact candidate applied.

Every transition is an explicit auditable event with actor, time, reason, provenance and before/after references. No transition is inferred from branch names, PR labels, CI status, comments, reactions or chat messages. Approval authority comes from governance and verifiable identity, not forge convention.

### 5.1 Evidence freshness and acceptance

Evidence binds to the exact subject and relevant dependencies: base/candidate fingerprints, governance and specification revisions, evaluator/tool versions, configuration, assumptions, environment and external facts. If a declared dependency changes, affected evidence and approvals become stale for the new tuple. Historical evidence remains in the audit record; it is not erased or silently reused.

Acceptance is derived, not an editable flag. It requires:
- exact repository/base/candidate/governance/specification identities;
- evaluation of all applicable mandatory obligations;
- no blocking failure, conflict or indeterminate/unsupported result;
- valid evidence bound to the current tuple and dependencies;
- authentic approvals from authorized actors in the required number/roles;
- valid, narrow, in-scope and unexpired exceptions;
- an adapter able to identify the candidate and verify exact application.

`Accepted` is a decision about an exact candidate. `Applied` is a subsequent VCS/collaboration operation. The adapter must recheck preconditions and confirm that the exact accepted candidate was applied. Concurrent mutation or a TOCTOU race must fail closed.

## 6. Assurance vocabulary: no generic “verified”

GovCheck must report exactly what a method establishes, for which subject and scope, under which assumptions. The following classes are not interchangeable:

| Class | What it can establish | What it does not establish by itself |
|---|---|---|
| Empirical execution (tests, builds, linters, scans) | Observed outcome for the executed inputs/environment | General correctness, model validity or proof |
| Model checking | Properties of a formal model under its bounds, configuration and assumptions | That the implementation conforms to the model |
| Theorem proving | A derivation accepted by a specified logic/kernel, relative to axioms and imports | That the chosen theorem/model is the right requirement or that code implements it |
| Implementation conformance | A justified relation between implementation behavior and specification/model | Normative approval of the specification |
| Normative fidelity | Traceability from approved rules to formal properties, tests and human-readable projections | Truth of external evidence or correctness of every implementation |
| Acceptance | A governance decision for one exact candidate under a defined predicate | Universal truth of all claims or absence of all defects |

Tests are **testimony**: evidence that a particular execution produced an observed result. Model checking validates a model within its declared assumptions and explored bounds. A theorem proof is valid relative to its logic, kernel, axioms and imports. Conformance between a model and implementation requires its own explicit refinement relation and evidence. These distinctions must survive in names, schemas, reports and user interfaces.

Evidence records should bind claim/rule IDs, subject identity, repository and exact state fingerprints, governance/specification/model revisions, method and scope, tool/version/configuration/invocation, environment and assumptions, raw result or integrity-protected reference, outcome/time/producer/provenance, limitations and invalidation dependencies. A bare exit code proves only the outcome of that invocation.

For TLA+/TLC, record the model revision, configuration/constants, reductions, fairness, bounds, tool version, state/transition counts, completion status and counterexamples. A bounded run is not called exhaustive. For theorem proving, record the logic, kernel/checker version, axioms, imported theorems, admitted obligations and any unsafe features or oracles. For implementation conformance, identify the implementation/specification revisions, abstraction boundary and refinement relation.

## 7. Threat model and trust boundaries

The design considers malicious or compromised contributors and agents, malicious repository content, compromised dependencies/build tools, forged or revoked identities, compromised forges/team servers, stale external facts, buggy parsers/evaluators/adapters, operator error, races and partial failures.

Assets include canonical governance and its history; repository and candidate identity; change records and approvals; evidence/provenance; keys and identities; evaluator/adapter binaries and configuration; acceptance decisions; and private repository data or credentials encountered by checks.

Security objectives are integrity, authenticity/authority, exact-state binding, freshness, availability, confidentiality and auditability.

Trust boundaries include:
1. untrusted normative input until parsed and validated;
2. parser, canonicalizer, evaluator and rule-composition engine as core TCB;
3. project checks/scripts and their dependencies, which may be malicious;
4. VCS adapters interpreting native state;
5. evidence producers, verifiers, signatures and external facts;
6. local operator/admin, who can bypass local controls;
7. shared acceptance authority and its administrators/credentials;
8. generated Markdown projections, which may drift and are not normative.

Required safe outcomes include rejecting ambiguous encodings and duplicate keys; explicit scope/conflict handling; bounded parsing and evaluation; path/symlink escape protection; replay-resistant evidence bound to exact state; rechecking candidate fingerprints before apply; authenticated and authorized approvals with revocation policy; explicit adapter capability/failure reporting; least-privilege execution of project checks; privacy-aware evidence storage and redaction; and compare-and-swap/precondition checks for races.

GovCheck alone cannot guarantee tamper-proof, hermetic or zero-trust operation. A signature can establish integrity/origin only under key assumptions; it does not prove correctness, authority or truth. A forge gate is not independent if an administrator can disable it. These limitations must be explicit.

## 8. Formalization and conformance strategy

The formal foundations are common to all repositories. The initial formal target is the change lifecycle and acceptance predicate, not a full model of every VCS, forge, parser, filesystem or threat scenario.

The lifecycle model should be small and finite. Separate models/contracts are appropriate for rule composition, Git/Pijul state semantics, concurrency and threat scenarios. Do not create one monolithic state-explosion-prone model.

The common safety targets include type correctness; acceptance soundness; exact-candidate application; no stale acceptance; evidence and approval binding; no implicit approval/application; append-only history; terminal-state discipline; and “unknown is not pass”. Liveness is conditional on actors acting, inputs stabilizing, adapters remaining available and fair scheduling. Unconditional progress must not be claimed.

Conformance test vectors must be language-neutral and include the initial descriptors, identities, actors/authority, action sequence, evidence/dependencies, expected transition and reason, expected history additions, and expected acceptance/application outcome. Required families include happy path; missing/indeterminate evidence; stale evidence after candidate or governance mutation; unauthorized or wrong-candidate approval; mismatched applied candidate; concurrent mutation between accept and apply; terminal decisions; local-only limitation; dirty Git state; and Pijul-native graph/patch/conflict preservation.

## 9. Current formal artifact: `govcheck.lifecycle`

PR #4 added the initial bounded TLA+ model `formal/tla/GovCheckLifecycle.tla`, TLC configuration, bilingual explanations, transition registry, generated Mermaid diagram, Python generator/checker, stable artifact catalogue and release-manifest schema. The PR was merged into `main` on 6 November 2026.

The model binds one abstract change to the tuple:

`(baseId, candidateId, governanceId, specId)`

Its variables cover phase, tuple identities, evaluated tuple, obligation outcomes, evidence, approvals, accepted tuple, applied candidate and event history. Its modeled actions are `Prepare`, `PublishEvidence`, `Evaluate`, `Approve`, `Accept`, `Apply`, `ChangeInputs`, `Reject`, `Withdraw` and `Supersede`.

The TLC configuration uses two values per identity dimension, two actors, two obligations and a history limit of 12. That limit exists only to keep the explored state space finite; it is not a production retention policy.

Configured state invariants:
- `TypeOK`: variables remain in declared domains.
- `AcceptanceSoundness`: Accepted is bound to the current tuple, current evaluation, passing obligations and required approval count.
- `ApplicationSoundness`: Applied identifies exactly the candidate in the accepted/current tuple.
- `NoStaleEvaluation`: Reviewable, Accepted and Applied cannot rely on an older tuple evaluation.
- `EvidenceBinding`: Reviewable requires evidence for all modeled obligations.
- `ApprovalBinding`: accepted/applied states contain approvals from authorized actors.
- `NoImplicitApplication`: no applied-candidate identity exists before Applied.
- `HistoryNonEmpty`: the initial creation event remains present.

The temporal property `TerminalDiscipline` states that Applied, Rejected, Withdrawn and Superseded cannot transition out. The module also states theorem obligations from `Spec`; their presence in source is not evidence that a theorem prover has discharged them.

### 9.1 Model limitations that must remain visible

The current abstraction treats published evidence as sufficient and passing. It does not establish evidence truth, provenance, freshness dependencies, revocation or independent verification. `Fail` exists in the outcome domain but no current transition produces it. Concurrency, adapter unavailability, malicious adapters, cryptographic authenticity, Git internals, Pijul-native semantics and filesystem races are not modeled. The event sequence is appended to, but there is not yet a separate temporal history-integrity property or complete actor/reason metadata. `ChangeInputs` is disabled after terminal states, including Applied; post-application remediation/reopening remains a policy decision.

The transition registry and Mermaid diagram are explanatory metadata. TLA+ is the semantic authority. The Python checker checks structural action/operator coverage and generated-file freshness; it does not parse TLA+ semantics or prove that registry guards/effects faithfully describe the model.

### 9.2 Verification status at the time of the PR

The PR report documented successful structural checks: JSON registry parsing, coverage of ten `Next` actions, top-level operator definitions, history bounds on state-changing actions and diagram/rendering consistency. It explicitly did **not** claim that the generator had been executed in a repository checkout, that TLC or SANY had run, that theorem proving or implementation conformance had occurred, or that GitHub Actions had run. Those are distinct follow-up tasks, not implied by merge.

Before describing the model as model-checked, run a pinned TLA+ Tools/TLC version and record the exact tool and configuration digests, completion status, explored states/transitions and any counterexample. A successful bounded TLC run still does not establish implementation conformance.

## 10. Artifact and release versioning

Source artifacts retain stable paths; Git history records revisions. A release tag identifies the exact commit/tree. Do not create duplicate `-v1`, `-v2` source copies merely because a release is published.

Stable logical `artifactId` values survive renames; update the catalogue in the same change when a path changes. Generated verification reports are release-specific assets attached to the corresponding GitHub Release, not renamed source files. A release manifest binds tag/commit, artifact ID, path, content digest, tool/version, configuration digest, execution status and available result counts. Never fabricate a report or status when execution did not occur.

The initial lifecycle artifact ID is `govcheck.lifecycle`. Its catalogue is `formal/artifacts.json`; the manifest schema is `formal/schemas/release-manifest.schema.json`.

## 11. Technology decisions intentionally deferred

No implementation language, canonical serialization, schema technology, rule expression language, formal kernel, cryptographic format, license or mandatory dependency stack has been selected. Candidate families in architecture 0007 include Rust, Go, OCaml, Haskell, Kotlin/JVM and Python; JSON/JSON Schema, YAML subsets, TOML, CBOR and canonical encodings; fixed typed predicates versus a restricted DSL; TLA+, Alloy, PlusCal and theorem provers; hashes, signed attestations and transparency mechanisms; local executable packaging; forge adapters; and native Pijul integration.

Candidates must first pass hard gates: preserve Git/Pijul semantics; work locally without hosted service/daemon/MCP; support deterministic bounded evaluation and explicit unknown/error states; avoid arbitrary repository policy execution; support reproducible distribution; and preserve assurance distinctions. Weighted scores are secondary to gates and evidence. “Unknown” is not a pass or an assumed zero.

## 12. Decision register

| ID | Decision / constraint | Status |
|---|---|---|
| D-01 | GovCheck governs repositories and change lifecycles, not agent tool calls | Settled in ADR 0001 |
| D-02 | One machine-readable canonical normative authority; Markdown is projection/explanation | Settled as design contract |
| D-03 | Formal foundations apply to every repository size; no size-based assurance tiers | Settled |
| D-04 | Small local executable; no mandatory MCP, daemon or hosted service | Settled |
| D-05 | Git and Pijul are first-class, native and semantically distinct | Settled |
| D-06 | VCS, hosting, collaboration and acceptance/application remain separate | Settled |
| D-07 | English default with French counterpart documentation | Settled |
| D-08 | Unknown/unsupported/indeterminate cannot satisfy mandatory acceptance | Settled as target |
| D-09 | Tests, model checking, theorem proving, conformance, normative fidelity and acceptance are distinct | Settled |
| D-10 | Stable source paths and artifact IDs; releases bind exact commits and generated evidence manifests | Established by PR #4 |
| D-11 | TLA+ is used for the first lifecycle model; it does not preselect the whole formal stack | Current initial artifact; broader tool strategy open |
| D-12 | No language, serialization, DSL, crypto format, license or mandatory dependency selected | Deliberately open |

## 13. Open questions and ordered follow-up work

The following are not resolved by this discussion record and must be handled through focused ADRs/specifications and evidence:

1. **Canonical data and semantics:** serialization, canonical bytes, duplicate-key handling, schema evolution, semantic versioning and typed rule representation.
2. **Rule composition:** precise precedence/refinement, contradiction detection, profile composition, exception semantics and deterministic evaluation.
3. **Evidence lifecycle:** provenance, dependency freshness, revocation, independent verification, failed/unknown/unsupported/not-run distinctions and privacy/retention.
4. **Identity and approvals:** actor identity, authority, signatures, key rotation/revocation, approval invalidation and role/threshold policy.
5. **Lifecycle refinement:** explicit failed checks, reopening/remediation after application, history integrity and actor/reason fields, concurrency and fairness.
6. **Formal verification:** pinned TLA+ Tools version, SANY/TLC execution, counterexample review, model refinements and separate theorem-proving targets if justified.
7. **Implementation conformance:** executable reference semantics, language-neutral test-vector format, refinement relation and test harness.
8. **VCS adapters:** exact Git dirty-state/submodule descriptors and Pijul patch/channel/graph/conflict contracts, each validated natively.
9. **Execution boundary:** least privilege, resource/time limits, malicious project scripts, output handling and secret redaction.
10. **Shared enforcement:** forge/team capability negotiation, exact-state gate protocol, bypass reporting and administrator trust.
11. **Distribution and maintenance:** local executable packaging, reproducible builds, supported platforms, licensing and dependency policy.
12. **Documentation fidelity:** projection generation/checking, translation consistency and traceability from rule IDs to specifications, models, tests and release evidence.

Recommended order: refine semantic identities and evidence assumptions; validate the current lifecycle model with a pinned TLC toolchain; add conformance vectors and explicit failed/unknown states; model concurrency and adapter boundaries separately; prototype canonical serialization and evaluator semantics; then compare implementation and packaging technologies against the now-testable contracts. Do not implement broad integrations before the core semantics and conformance boundary are clear.

## 14. Repository map

- `docs/decisions/0001-bootstrap-boundaries.md`: accepted product boundary and bootstrap ADR.
- `docs/specifications/0002-canonical-governance-model.md`: normative model contract.
- `docs/specifications/0003-change-lifecycle.md`: lifecycle and acceptance.
- `docs/specifications/0004-vcs-collaboration-contracts.md`: Git/Pijul and collaboration adapters.
- `docs/specifications/0005-assurance-model.md`: claims, evidence and assurance vocabulary.
- `docs/architecture/0006-threat-and-trust-model.md`: threat model and trust boundaries.
- `docs/architecture/0007-technology-decision-framework.md`: technology gates and comparison process.
- `docs/architecture/0008-formalization-and-conformance.md`: formalization and conformance plan.
- `docs/formal/lifecycle-model.md` and `.fr.md`: explanation of the current lifecycle model.
- `formal/tla/GovCheckLifecycle.tla` and `.cfg`: model and TLC configuration.
- `formal/lifecycle-transitions.json`, `docs/formal/lifecycle-diagram.mmd`, `scripts/render-lifecycle-diagram.py`: explanatory transition registry, generated diagram and structural drift checker.
- `formal/artifacts.json`, `formal/schemas/release-manifest.schema.json`: artifact identity and release evidence manifest.

## 15. Change control for this record

This document is a consolidated rationale and decision index, not a second normative specification. If a design decision changes, update the relevant ADR/specification/model first and then update this record and its French counterpart. Do not silently change historical decisions: supersede them with a dated ADR or explicit specification revision. Keep implementation status and verification claims synchronized with actual repository evidence.
