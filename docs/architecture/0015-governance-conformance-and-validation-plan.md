# 0015 — Governance Conformance Tool and validation plan

**Status:** capability and validation proposal, not an implementation claim. “Governance Conformance Tool” names responsibilities delivered incrementally by GovCheck core/adapters. **French:** [0015](0015-governance-conformance-and-validation-plan.fr.md).

## Six responsibilities

1. **Governance discovery:** identify canonical package, version, applicable profiles, authority and controlled documentation.
2. **Documentation conformity:** verify normative instructions are authorized projections and explanations are not silently promoted to policy.
3. **Change traceability:** link a dossier to exact repository/base/candidate, affected goals/requirements/properties, decisions and native VCS/collaboration objects.
4. **Check execution:** resolve applicable checks, prerequisites, permitted conditions, tool identity/version/configuration and resource limits; record outcomes.
5. **Assurance evaluation:** assess claims against admissible evidence, assumptions, freshness, independence, exceptions and acceptance predicate.
6. **Authority/application:** verify authorized approvals and enforce/revalidate at the strongest available application boundary, exposing bypass limits.

These are responsibilities, not maturity levels. Local inspect/audit without shared enforcement must be reported honestly.

## Three distinct conformity subjects

- **Artifact conformity:** repository governance, documents, code/configuration and declared checks have required structure and traceability.
- **Agent/process behavior:** a particular agent/harness and delegated workflow followed the task contract in a recorded exercise.
- **Operational enforcement:** deployed boundary prevents disallowed application and resists bypass, stale evidence, races and administrative override within its threat model.

Artifact checks do not qualify every agent. Agent qualification does not prove artifact correctness. A local CLI report does not establish operational enforcement.

## Assurance dossier

A report is a dossier, not a generic PASS/FAIL badge or opaque score. It identifies report schema/identity; repository and native VCS identity/capabilities; exact base/candidate including relevant dirty/index/worktree or native Pijul state; governance package/revision/profile; specification/model/evaluator build/config; claims and requirements in scope; checks, exact invocation, tool/version/digest, environment, limits and execution status; raw output or protected content-addressed reference; provenance/freshness/invalidation; assumptions, defeaters, contradictions, unsupported areas and exceptions; producer, independent validator and authority identities/roles; decision, exact subject, time and enforcement boundary; and bypass limitations.

A report is evidence that a defined evaluation occurred, not proof every claim is true.

## Status vocabulary

Candidate method/result labels:
- `NOT_EVALUATED`
- `CHECKED` — a specified mechanical/empirical check ran.
- `MODEL_CHECKED` — model checking completed for the recorded model/configuration.
- `PROOF_CHECKED` — a proof checker accepted an object under recorded assumptions.
- `CONFORMANCE_ESTABLISHED` — a separately justified implementation/specification conformance claim.
- `EXEMPTED` — a valid authority-approved exception applies.
- `FAILED`

These are not ordered grades or interchangeable statuses. They require subject, scope, method, evidence, assumptions and completion metadata. MODEL_CHECKED does not mean implementation conformance; EXEMPTED is a governance decision, not proof. Preserve finer outcomes: unknown, not run, not applicable, unsupported, incomplete, stale/invalidated and conflict.

## Representative repository validation

Before selecting serialization, implementation language, agent adapter or forge integration, validate against at least four contexts:

| Fixture | Challenge |
|---|---|
| Small library | Minimal overhead, local-only, feature/fix, missing governance, stale check |
| Agent-using application | Multiple agents, human review, discovery, uncertainty, no self-approval |
| Unusual technology/VCS | Unsupported check, non-Git state, Pijul identity/conflict preservation where available |
| High-assurance project | TLA+/Lean artifacts, proof/model/test distinctions, refinement limits |

Run the same task classes with more than one agent/harness where available. Record exact revisions/configuration/tool versions. One demonstration does not establish general qualification.

## Acceptance test catalogue (future implementation criteria)

1. Valid governance is discovered; missing governance is reported without invented defaults.
2. Duplicate IDs, unresolved references and unsupported normative constructs fail or become indeterminate.
3. Contradictory mandatory rules are detected; file order does not resolve them.
4. Absence of prohibition is not permission.
5. Markdown adding an unregistered obligation is reported.
6. Stale/divergent English/French projection is reported.
7. Task traces to affected goals, requirements, properties and components.
8. Missing mandatory check is not a pass.
9. Test success is not promoted to mathematical proof or implementation conformance.
10. Model-check report binds exact model/configuration and completion.
11. Proof report identifies kernel, axioms, imports and admitted obligations.
12. Evidence for another candidate/governance revision/dependency set is stale.
13. Producer cannot approve own exception or be sole independent validator where separation is required.
14. PR label/comment/reaction or green CI does not create acceptance.
15. Git dirty/index/worktree/submodule state is not reduced to HEAD.
16. Pijul patch/channel/graph/conflict semantics are not replaced by synthetic Git assumptions.
17. Mutation between acceptance and application triggers revalidation or safe failure.
18. Privileged local bypass is reported, not described as impossible.
19. Exception is scoped, authorized, reasoned, time-bounded and does not turn unknown evidence into proof.
20. Report preserves contradictions, limits, tool failures and partial execution.

These criteria have not been executed by this documentation change.

## Product boundary retained

- Small local executable and documented CLI are the mandatory baseline.
- No mandatory daemon, hosted service, MCP server or agent harness.
- Optional interfaces delegate to the same core semantics; no second normative evaluator.
- Declarative profiles select obligations/checks; they are not repository-size assurance tiers.
- Check adapters declare executable, arguments, prerequisites, timeout/resource limits, result format and tool identity. No arbitrary third-party policy code is loaded into the core.
- Existing build/test/security/formal/VCS tools do specialized work; GovCheck qualifies and records their outputs rather than reimplementing/installing them.
- Git and Pijul remain native, separate adapters. Hosting/forge integrations are separate from governance semantics.
- Bootstrap/migration is non-destructive: inspect → plan → apply, with versioned migrations, drift detection and rollback.

MCP was once considered an optional preferred interface; it is not a required dependency. Lean remains a candidate for a narrowly justified proof-critical core, not a whole-product or governed-repository dependency.

## Phased delivery proposal

**v0.1 — Local governance and dossier:** safe inspect/bootstrap; one versioned canonical source; explicit obligations/prohibitions/permissions/deviations/applicability; change plan/decisions; check declarations and execution records; candidate-bound structured results; controlled human docs; local assurance dossier.

**v0.2 — Agent interoperability:** stable CLI/machine operations to discover requirements, start changes, record decisions, request exceptions and evaluate dossiers; generated/controlled AGENTS.md; representative-agent exercises; optional adapters without normative logic.

**v0.3 — Shared application:** one reference forge/team integration (GitHub first only if selected); pre-application decision bound to exact candidate; attestation checks and stale invalidation; capability/admin-bypass reporting; decision/deviation history.

**v0.4 — Stronger formal assurance:** formalize core semantics and justified components; TLA+ lifecycle/concurrency models and recorded runs where useful; prototype Lean for proof-critical predicates/certificate checking only if justified; conformance vectors and refinement relation; release-bound dossier.

Do not delay a useful first slice until every rule is proven; do not market docs/tests/model declarations as implemented assurance.

## Ecosystem study boundaries

Tools discussed occupy different layers:
- Spec Kit and agent-oriented specification workflows structure intent/specification and implementation steps.
- OPA/Cedar provide executable policy decisions, not normative correctness or non-bypassability.
- in-toto/SLSA address provenance and supply-chain attestations, not repository governance semantics.
- OpenSSF Scorecard provides security-posture signals, not a complete assurance case.
- Lean checks derivations, not requirements selection or unverified executable conformance.
- Writ and Privateer were identified for deeper technical study. No compatibility/adoption conclusion is made without dedicated source/code review.

Compare on complementarity to the six responsibilities, narrow trust boundary, local-first operation, native Git/Pijul semantics, reproducibility and epistemic limits. No global stack is selected.

## Deferred decisions

CLI commands/dossier serialization; profile composition/task schema; first forge/team integration and threat model; agent qualification protocol/independence thresholds; Writ/Privateer adoption; Lean's justified role; operational retention/privacy/protected evidence storage. Each needs a focused ADR/prototype and evidence.
