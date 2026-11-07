# 0024 — Project bootstrap, governance choices and assurance profiles

**Status:** proposed product and architecture design for review; no interactive bootstrapper, profile schema, template engine or repository mutation command is implemented by this record.  
**Language:** English is the default; see the [French counterpart](0024-project-bootstrap-and-assurance-profiles.fr.md).

## 1. Purpose

A new repository should not begin with a generic, fully populated governance tree. GovCheck should guide the project owner through consequential governance and assurance decisions, explain the trade-offs, and then prepare a repository structure that reflects the choices actually made.

The bootstrap experience has three responsibilities:

1. **Decide:** elicit context and explain governance and assurance options, consequences, costs and limitations.
2. **Plan:** translate explicit decisions into a deterministic, reviewable repository plan.
3. **Apply:** create only the selected structure, without overwriting existing content or silently changing normative policy.

This is an assistant for project formation, not merely a directory generator and not a maturity-scoring questionnaire.

## 2. Relationship to existing foundations

This design supplements, and does not silently amend, ADR 0001, Specification 0002 (Canonical Governance Model), Specification 0005 (Assurance, Claims and Evidence), and Architecture 0015 (Governance Conformance Tool and Validation Plan).

The following distinction is mandatory:

- **GovCheck governance foundations are invariant.** Every governed repository has a canonical governance identity/profile, explicit applicability and decision semantics, and the ability to record assurance claims, evidence, provenance and uncertainty. Profiles may add constraints but cannot remove these foundations.
- **Project assurance methods are configurable.** A project may select empirical tests, static analysis, model checking, program verification, theorem proving, implementation-conformance work, or combinations appropriate to its claims. Selecting no project-specific formal method is valid.
- **A method is not a maturity tier.** Do not classify repositories as bronze/silver/gold or low/medium/high assurance based on size. Method selection is claim-, risk-, domain- and consequence-driven. Different claims in one repository may require different methods.
- **No proof method is presumed superior for every claim.** Tests, static analysis, model checking, program verification and theorem proving establish different things. The bootstrap must explain what each method can and cannot establish, its assumptions, operating cost and maintenance burden.

Consequently, a project that selects no formal verification still receives GovCheck's governance/assurance foundations, but does not receive project-specific Lean, TLA+, proof-source, proof-build or formal-toolchain directories and configuration merely for appearance.

## 3. Guided decision process

The CLI is the primary initial interface, consistent with ADR 0001. It should be usable interactively by a human and non-interactively by scripts/agents through explicit machine-readable answers. A graphical interface may later consume the same decision model; it must not create a second policy evaluator.

The dialogue should be staged and contextual, not a flat list of unexplained toggles.

### 3.1 Project context

Collect only facts that influence recommendations or generated obligations, with explicit unknown/not-provided states:

- project purpose, users and operational context;
- software type and critical components;
- data sensitivity and security exposure;
- consequences of failure and recovery expectations;
- applicable legal, contractual, sector or organizational constraints, when declared by the owner;
- deployment and update model;
- contributors, decision authority, review capacity and external collaboration;
- VCS and hosting/collaboration context (Git or Pijul; local, team-hosted, self-hosted or public).

GovCheck must not infer legal compliance or risk acceptance from a project label. Recommendations must identify the facts and assumptions on which they depend.

### 3.2 Governance decisions

Explain and let the owner decide, as applicable:

- authority and delegation: individual, named maintainers, team or organization;
- change approval and separation of duties;
- decision records and the situations that require them;
- requirements and traceability expectations;
- contribution and review policy;
- exception/deviation authority, scope, expiry and compensating controls;
- release, provenance and evidence-retention expectations;
- security and incident-response governance.

A choice such as "individual project" must not automatically imply that all changes are self-approved if the owner selects independent review. Authority and review are separate decisions.

### 3.3 Assurance claims and methods

Start with the properties the project wants to establish, not with a tool shopping list. For each claim or claim family, ask what evidence would be persuasive and proportionate.

| Method family | What it can support | Important limitation to explain |
|---|---|---|
| Unit/integration tests | Observed behavior for executed cases and paths | Does not establish behavior outside tested cases |
| Property-based/fuzz testing | Behavior over generated or fuzzed inputs | Sampling is not a mathematical proof |
| Static analysis/type checking | Detection or exclusion of selected defect classes under tool assumptions | Does not establish all runtime behavior |
| Model checking (e.g. TLA+/TLC) | Properties of an explicit model within its state space, bounds and assumptions | Does not by itself establish implementation conformance |
| Program verification (e.g. Dafny, Verus, Kani) | Specified program properties within the verifier and trusted assumptions | Scope and trust base are tool- and language-dependent |
| Theorem proving (e.g. Lean, Coq, Isabelle) | Derivations accepted by a specified logical kernel and its assumptions | Does not choose the right requirements or prove an unconnected implementation correct |
| Implementation/specification conformance | A justified relation between implementation and specification | Requires an explicit refinement/conformance argument and evidence |

Methods can be combined. For example, tests may validate integration behavior while TLA+ explores concurrency properties; neither result substitutes for the other. A theorem prover is not automatically appropriate for ordinary business logic, and a green test suite must never be described as a formal proof.

The user may explicitly select **no project-specific formal verification**. This is not a failure or a reduced GovCheck governance foundation. The resulting profile records the decision and its scope so that later claims do not imply that formal properties were established.

### 3.4 Recommendation quality

For each recommendation, show:

- the project fact, claim or consequence that triggered it;
- the proposed method or governance control;
- what it can establish and what it cannot;
- expected maintenance/tooling burden and dependencies;
- assumptions, uncertainty and any human decision still required.

Recommendations are advisory unless an applicable legal/contractual constraint or an authorized project policy makes a control mandatory. GovCheck must distinguish owner choice, GovCheck recommendation, and normative obligation.

### 3.5 Threat-led assurance and traceability

The bootstrap must connect project context and assurance choices to an explicit threat/risk analysis. It must not ask users to select tools in isolation.

Maintain traceable, typed relations across at least:

- assets and business/operational interests;
- security and safety objectives;
- threat sources/actors, capabilities and motivations where known;
- threat events and threat scenarios;
- attack techniques, preconditions, paths and reachable trust boundaries;
- vulnerabilities, weaknesses and exposure conditions;
- preventive, detective, responsive and recovery controls;
- control implementation/configuration instances and responsible owners;
- assurance claims, assumptions, evidence, limitations and review decisions;
- residual risks, treatment decisions, risk owners and review triggers.

Use precise terminology in the user interface. A **threat** is a potential cause of harm; a **threat scenario** describes how a threat source/event could affect an asset in a context; an **attack path** is a feasible sequence through components, privileges or trust boundaries; a **vulnerability/weakness** is a condition that can enable or amplify an event. These concepts are related but must not be collapsed into one binary field.

The traceability graph must work in both directions. From a threat scenario, users can inspect paths, weaknesses, controls, verification activities, evidence, residual risk and accountable decisions. From a control or evidence item, users can see which scenarios and claims it addresses, under which assumptions and scope. A control with no stated objective or scenario prompts a rationale; it is not automatically invalid, since controls may be defense-in-depth or address obligations outside the current threat set.

Coverage is not a single percentage and must not be presented as proof of security. Highlight at least:
- scenarios with no proposed treatment;
- paths with no effective control at one or more critical steps;
- controls planned but not implemented;
- controls implemented but not tested or otherwise assured;
- evidence that does not cover the relevant deployment/configuration;
- claims whose assumptions are unverified or unsupported;
- evidence that is stale, incomplete, disputed or produced by an untrusted component;
- risks accepted without a competent owner, rationale, scope or review condition.

A control is not "effective" merely because it is documented or generated by bootstrap. Distinguish proposed, implemented, configured, tested/observed, independently reviewed and operationally monitored states. A test of a control supports only the tested scope and conditions.

### 3.6 Assumptions, inference and limits

Every assurance argument must make its reasoning inspectable:

- **Assumption:** a premise taken as given for a bounded argument, with source, owner, scope, confidence, validity period and falsification/review conditions.
- **Evidence:** an observation, test result, analysis, attestation or proof produced under declared conditions.
- **Inference:** the explicit reasoning that connects assumptions and evidence to a claim.
- **Conclusion:** the bounded claim supported by that argument, not a broader guarantee.
- **Limitation/unknown:** what was not examined, is not established, or depends on an unresolved premise.

Show users what is assumed and what follows from it. For example: "Given that the host kernel and administrator account are trusted, this sandbox policy restricts the worker's declared filesystem and network access" is materially narrower than "the worker is contained". If the host administrator is in the threat model, the same argument does not establish protection against that adversary.

Assumptions are not silently promoted to facts. Their provenance and confidence must be visible; critical assumptions should have validation actions or explicit acceptance by an authorized risk owner. Unknown is not false, and an unverified assumption cannot be displayed as established evidence. The bootstrap should identify the trusted computing base and external dependencies for each assurance method, including check runners, compilers, model checkers, proof kernels, build systems, identity providers and enforcement points where applicable.

Model checking or theorem proving can establish properties of a model or derivation under its formalization and trusted assumptions. It does not automatically establish that the model captures every relevant threat, that the implementation conforms to the model, that deployment matches the analyzed configuration, or that the assumptions hold in operation. Tests, static analysis, operational monitoring and external attestations have their own scopes and trust dependencies. The user interface must display this chain rather than rank methods by prestige.

## 4. Risk assessment and treatment

Risk is contextual and graded, not a Boolean property. GovCheck must not equate "threat exists" with "unacceptable risk", nor "no threat recorded" with "safe".

For each scenario, support a documented assessment of:
- likelihood/plausibility, including the basis and uncertainty of the estimate;
- impact across relevant dimensions (confidentiality, integrity, availability, safety, privacy, financial, legal, operational or reputational);
- exposure, attacker capability, required preconditions and opportunity;
- existing controls and their demonstrated effectiveness within scope;
- inherent risk before controls and residual risk after controls;
- confidence in the assessment and important unknowns.

Do not force false numerical precision. Projects may use qualitative scales, calibrated ordinal scales or quantitative methods where defensible. The chosen scale, definitions, aggregation rules and uncertainty must be explicit and versioned. Avoid multiplying arbitrary ordinal labels and presenting the result as a mathematically meaningful risk score. Risk ratings prioritize decisions; they are not objective measurements of truth.

For each risk, guide the owner through treatment choices:
- **avoid:** change or remove the activity/asset/exposure that creates the risk;
- **mitigate:** introduce or improve controls, then assess their implementation and effectiveness;
- **transfer/share:** allocate part of the financial or operational consequence through a contract or service, while making clear that accountability and all consequences do not necessarily transfer;
- **accept/retain:** consciously retain the residual risk under an authorized decision.

Acceptance is not a default for missing controls. Record the risk owner, decision authority, rationale, affected assets/scenarios, residual-risk level and uncertainty, compensating controls, scope, date, expiry or review date, and triggers for reassessment (architecture/dependency/threat changes, incidents, new exposure, failed controls, changed assumptions or regulatory obligations). An acceptance may be time-bounded or conditional. A person may accept only within their recorded authority and delegated scope. GovCheck must not infer acceptance from silence, a green check, a merge or lack of remediation.

The tool should help users compare treatment options and their costs, operational burden and residual exposure. It may recommend additional controls or escalation, but must distinguish advisory guidance from mandatory obligations and the authorized risk decision. A high residual risk may be consciously accepted where authority permits; the UI must not conceal it or describe the project as risk-free. Conversely, a low or uncertain rating must not be used to suppress a serious low-likelihood/high-impact scenario without explicit rationale.

Risk acceptance does not make a threat disappear, validate a control, or turn unsupported claims into supported ones. It records a governed decision to operate with a known residual exposure. Assurance status and risk disposition must therefore remain separate but linked.

## 5. Profile and generated tree

The outcome is a versioned, machine-readable project profile plus a deterministic bootstrap plan. The profile records selected capabilities, explicit non-selections where relevant, rationale, context/assumptions, authority and profile/schema revisions. It is not a second normative source: normative rules remain in the canonical governance package.

The generator uses capability declarations and dependencies rather than a single all-or-nothing template. Illustrative mapping:

| Selected capability | Candidate generated content |
|---|---|
| Governance core (always) | canonical profile/configuration, governance explanation/projection, decision and change-lifecycle entry points |
| Decision records | `docs/decisions/` and decision template |
| Requirements traceability | `requirements/`, stable-ID conventions and traceability metadata |
| Unit/integration testing | `tests/`, selected test layout and documented commands |
| Property-based testing | property-test structure and tool configuration |
| Static analysis | selected analyzer configuration and check declarations |
| TLA+ model checking | `formal/tla/`, model/configuration skeleton and pinned invocation |
| Lean theorem proving | `formal/lean/`, project/toolchain skeleton and proof-check command |
| Other program verification | only the selected verifier's source/configuration and reproducible command |
| Threat modeling | `security/threat-models/` and a scoped threat-model template |
| Release provenance | release/evidence manifest structure and provenance instructions |

The table is illustrative, not a frozen directory contract. The final mapping must be maintained in a versioned template catalogue with explicit dependencies, conflicts, generated-file ownership and migration behavior.

Rules:

1. Do not create a method-specific directory, toolchain, workflow or placeholder README when that method is not selected.
2. Do not create an empty `formal/` directory if no project-specific formal method is selected.
3. Shared evidence and provenance foundations belong to the governance/assurance core; method-specific evidence schemas or runners are included only when required.
4. A selected capability must generate a usable, documented starting point—not an empty directory that suggests an operational control exists.
5. Never claim that a generated skeleton is a functioning test suite, proof, security control or CI gate until it has been configured and executed.
6. Directory names are an implementation detail. The profile's stable capability identifiers and typed artifact relationships are authoritative for planning.

## 5. Capability dependencies and composition

Capabilities form a typed dependency graph, not a set of independent booleans. Examples:

- a TLA+ model-checking capability depends on a model artifact, a configuration, a pinned TLC invocation and a result-recording contract;
- Lean theorem proving depends on a Lean project/toolchain declaration, proof sources, dependency pinning and a reproducible check command;
- a requirement-to-test traceability capability depends on stable requirement/claim identities and typed evidence relations;
- a release-provenance capability depends on exact source/release identity and a manifest/evidence record.

The resolver must detect missing dependencies, incompatible selections, unsupported combinations and cycles. It must explain the reason and propose a resolution; it must not silently enable extra capabilities. A capability may declare mandatory prerequisites, optional recommendations and conflicts separately.

No project-specific formal method is a prerequisite of the governance core.

## 6. Bootstrap lifecycle: inspect → decide → plan → review → apply → verify

The bootstrap must preserve ADR 0001's non-destructive lifecycle and make the decision stage explicit:

1. **Inspect:** identify VCS, existing files, project metadata and existing GovCheck profile, if any. Preserve native Git/Pijul semantics.
2. **Decide:** conduct the guided dialogue or validate supplied answers. Unknown answers remain unknown; do not guess.
3. **Plan:** resolve capability dependencies and produce a deterministic file/operation plan, including rationale, omissions, conflicts and expected tool requirements.
4. **Review:** show the proposed tree and every file to be created, modified, preserved or skipped. Explain normative changes separately.
5. **Apply:** require explicit confirmation; never overwrite unowned files. Existing-file conflicts stop or require a separately reviewed merge.
6. **Verify:** validate profile/schema, generated projections, expected files, dependency closure and available local checks. Report unexecuted checks honestly.

The plan must support preview/dry-run, machine-readable output, deterministic regeneration, idempotent re-run and a stable plan digest. Applying the same profile to the same inspected state should produce the same plan. A changed profile produces a new plan and a migration diff; it must not delete previously generated or user-owned content automatically.

For existing repositories, bootstrap is a migration assistant, not a reset command. It must detect drift and preserve user edits. Destructive cleanup requires a distinct, explicit operation and review.

## 7. Evolution after bootstrap

The profile is not a one-time questionnaire result. A project may later add or retire capabilities as its claims, risks, team or deployment context change.

A profile change must:

- create a revision-bound decision/change record;
- show additions, removals and changed obligations;
- identify generated artifacts that become unused, stale or invalid;
- preserve history and user-owned content;
- require review before removing files or weakening obligations;
- re-evaluate affected claims/evidence under Architecture 0021's freshness model.

Removing a formal method from the active profile does not erase historical proof artifacts or decisions. It changes future applicability and acceptance expectations only through an authorized, prospective decision.

## 8. CLI and machine interface sketch

The precise command names remain open, but the workflow should support equivalents of:

- `govcheck init` — start guided bootstrap;
- `govcheck init --answers <file>` — non-interactive, schema-validated decisions;
- `govcheck plan` — inspect and render the deterministic plan;
- `govcheck apply` — apply a reviewed plan;
- `govcheck profile show|validate` — inspect and validate the active profile;
- `govcheck plan --format json` — machine-readable plan for scripts/agents.

These are interface sketches, not implemented commands or an approved CLI contract. Exact syntax, serialization and profile schema require a separate specification and prototype.

## 9. Acceptance scenarios for a first prototype

A prototype should demonstrate at least:

1. A small local library selecting governance core, unit/integration tests and static analysis, with no `formal/` tree.
2. A project explicitly selecting no tests and no project-specific formal methods; the plan explains the consequence and creates no corresponding directories.
3. A concurrent/distributed service selecting tests plus TLA+; the generated tree contains a usable model/configuration/check entry point.
4. A proof-oriented component selecting Lean; the tree includes a pinned toolchain and reproducible proof-check entry point.
5. An existing repository with user-owned `tests/` or `formal/` content; preview detects conflicts and apply preserves them.
6. A profile change adding or removing a capability; the migration plan preserves historical evidence and never silently deletes source files.
7. Unknown project risk/context; recommendations expose uncertainty rather than silently selecting a high-assurance or low-assurance preset.
8. The same answers and inspected state produce byte-for-byte stable plan output.
9. Git and Pijul contexts preserve their native identities and status semantics.
10. Machine-supplied answers are validated; unknown capability IDs, missing dependencies and contradictory decisions fail closed with actionable explanations.
11. Threat scenarios can be traced through attack paths, weaknesses, controls, assurance claims, assumptions, evidence and residual-risk decisions in both directions.
12. The prototype distinguishes unassessed, untreated, planned, implemented, tested, reviewed and monitored controls; it exposes uncovered paths and unsupported assumptions.
13. Risk can be accepted only by an authorized owner with recorded rationale, scope, residual assessment and review/expiry conditions; acceptance never changes evidence status.

## 10. Delivery sequence

1. Review this decision model and resolve terminology against Specifications 0002/0005 and Architecture 0013/0015/0021.
2. Define stable capability identifiers, profile schema, dependency semantics and template-catalogue contract.
3. Prototype a local CLI with inspect/answers/plan only; do not mutate repositories yet.
4. Add safe apply, conflict detection, idempotence and migration behavior.
5. Validate representative Git/Pijul, small/large, test-only and formal-method project fixtures.
6. Add generated documentation/projections and optional forge/CI adapters only after local semantics are stable.

Do not begin with a large GUI, hosted service, mandatory MCP server, plugin marketplace or a universal project template. The local executable remains the primary interface.

## 11. Limits and status

This record defines a proposed experience and its safety properties. It does not select an implementation language, serialization format, concrete CLI syntax, test framework, theorem prover, model checker, directory catalogue or default project profile. It does not claim that any bootstrap functionality exists.

The architecture must be reconciled with the existing canonical governance authority before any profile becomes normative. A generated repository tree is not proof of governance conformance; verification must evaluate the actual profile, files, tools, executions and exact repository state.
