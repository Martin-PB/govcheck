# 0008 — Formalization and Conformance Plan

**Status:** Proposed architecture, ready for review. **French:** [0008](0008-formalization-and-conformance.fr.md).

## Purpose

Define a disciplined path from normative governance contracts to formal models and executable conformance tests. This document does not claim GovCheck has an implementation, a verified lifecycle engine, or a completed proof.

The first formal target is the change lifecycle in specification 0003, including evidence freshness and acceptance bound to an exact candidate. VCS-specific semantics remain behind the adapter contract in 0004. The assurance vocabulary in 0005 governs every result.

## Modeling boundary

The abstract model represents one change record and its relevant immutable identities. It does not model Git internals, Pijul graph algorithms, forge APIs, cryptographic primitives, parsers, filesystems, or a concrete database. Those require separate contracts or models.

Preserve these distinctions: a change is not a branch, commit, patch, channel, PR or MR; Accepted is not Applied; evidence is not approval; approval is not acceptance; model checking is not implementation conformance; and an adapter apply result must identify the exact candidate applied.

## Abstract state

Candidate variables for a first finite-state model:

| Variable | Meaning |
|---|---|
| phase | Proposed, Prepared, Evaluated, Reviewable, Accepted, Applied, Rejected, Withdrawn, Stale or Superseded |
| baseId | Exact base descriptor identity |
| candidateId | Exact candidate descriptor identity |
| governanceId | Governance package revision and semantics identity |
| specId | Normative specification revision |
| evaluatedTuple | Tuple (base, candidate, governance, specification) evaluated by the current evaluation |
| evidence | Finite set of evidence records bound to a tuple and declared dependencies |
| approvals | Finite set of approvals bound to candidate/governance identities and an authorized actor |
| requiredApprovals | Policy-derived threshold and roles for this model instance |
| blockingObligations | Finite set of mandatory obligations and outcomes |
| appliedCandidateId | Candidate identity reported by the VCS adapter after application, or None |
| history | Append-only abstract event sequence |

A model instance uses small finite sets for actors, evidence, obligations and identities. These bounds are exploration parameters, not production limits.

## Actions to model

1. Prepare: resolve repository/change identities and impact scope.
2. Evaluate: evaluate mandatory obligations against a pinned tuple.
3. PublishEvidence: add evidence without overwriting history.
4. Approve: record an authorized approval bound to the exact candidate and governance revision.
5. Invalidate: make evidence unusable when a declared dependency changes.
6. ChangeInputs: change base, candidate, governance or specification identity; stale evaluation and invalidate dependent evidence/approvals as required.
7. Accept: transition only if the acceptance predicate holds.
8. Apply: transition only if the adapter confirms it applied the exact accepted candidate.
9. Reject, Withdraw, Supersede: record explicit terminal or exceptional decisions.
10. Reevaluate: create a new evaluation; never erase historical failures or evidence.

Every state-changing action appends an event with actor, reason and before/after references. The model may abstract timestamps and cryptographic authenticity, but must state those abstractions.

## Safety properties (invariants)

The first model should check at least:

- Type correctness: every variable remains in its declared finite domain.
- Acceptance soundness: Accepted implies the acceptance predicate holds for the current exact tuple.
- Application soundness: Applied implies the applied candidate is the candidate previously accepted.
- No stale acceptance: changing an acceptance-relevant identity cannot leave the change Accepted or Applied without a new valid decision path.
- Evidence binding: evidence satisfies an obligation only when its subject tuple and dependencies match the current tuple and it is valid.
- Approval binding: only approvals for the current candidate and governance revision, from authorized actors, count.
- No implicit approval: evaluation success, comments, reactions or application events cannot create an approval.
- No implicit application: acceptance alone cannot imply application.
- Append-only history: actions extend history; they never rewrite or delete prior events.
- Terminal discipline: rejected, withdrawn and superseded changes cannot silently return to an active phase.
- Unknown is not pass: unsupported or indeterminate mandatory obligations cannot satisfy acceptance.

These are properties of the abstraction. Each needs traceability to normative clauses and later implementation conformance evidence.

## Liveness and fairness

Safety is the initial priority. Liveness must be conditional: progress cannot be guaranteed if actors never act or external adapters remain unavailable.

Candidate conditional properties: a valid, sufficiently evidenced and approved Reviewable change can eventually be accepted if acceptance remains enabled and scheduling is fair; an accepted change can eventually be applied if the adapter remains available and confirms the exact candidate; and a stale change can eventually be reevaluated if inputs stabilize and evaluation is scheduled.

Do not assert unconditional progress. Fairness assumptions and environmental availability must be visible in model configuration and reports.

## Model decomposition

Keep the first lifecycle model small. Add separate models only when justified:

- Rule composition/conflicts: precedence, scope, inheritance, ambiguity and conflicting mandatory rules.
- VCS state and acceptance: Git snapshots versus Pijul channel/graph/patch state; preserve native conflict semantics.
- Concurrency: simultaneous approvals, candidate mutation, invalidation and apply races.
- Threat scenarios: forged/stale evidence, unauthorized approval, adapter lies and governance rollback.

Do not combine all dimensions into one state-explosion-prone model. Compose through explicit contracts and shared abstract identities.

## Model checking versus theorem proving

Finite-state model checking (for example TLA+/TLC or an equivalent tool selected by ADR) fits transition systems, concurrency, safety invariants and conditional liveness under finite bounds.

Use theorem proving only where a mathematical proof is warranted: a reusable theorem about a precisely defined acceptance predicate, a refinement theorem, or a verified transformation. A theorem prover does not make an inaccurate model normative or establish implementation conformance.

No formal tool is selected here. TLA+ is a candidate for lifecycle/concurrency exploration, not a predetermined dependency.

## Conformance test vectors

Before implementation, define language-neutral vectors containing initial repository/change descriptors and governance/specification identities; action sequence and actor/authority context; evidence, dependencies and freshness; expected transition result and reason code; expected event-history additions; and expected acceptance/application outcome.

Minimum vector families:

1. Happy path from Proposed through Applied.
2. Missing mandatory evidence.
3. Indeterminate or unsupported mandatory obligation.
4. Evidence invalidated by candidate mutation.
5. Approval invalidated by governance revision change.
6. Approval from an unauthorized actor.
7. Approval for a different candidate.
8. Applied candidate differs from accepted candidate.
9. Concurrent mutation between acceptance and apply.
10. Explicit rejection, withdrawal or supersession.
11. Local-only acceptance with remote-enforcement limitation reported.
12. Git dirty worktree/index identity not collapsed into HEAD.
13. Pijul channel/graph/patch identity and conflict not flattened into Git concepts.

The first eleven lifecycle vectors can be shared across VCS adapters where applicable. The final two are adapter-specific and must retain native semantics.

## Evidence and claim discipline

A TLC run, if adopted, must report model revision, configuration, constants, symmetry/reduction settings, fairness, state/transition counts, completion status and explored bounds. A passing run supports only the checked model/configuration.

Conformance requires a separate relation between implementation behavior and abstract transitions, plus test evidence. Normative fidelity requires traceability from approved specification clauses to model properties and test vectors. Acceptance remains a governance decision for an exact repository candidate.

## Open decisions deliberately deferred

- Formal tool and version.
- State encoding and model configuration format.
- Identity/fingerprint representation.
- Approval revocation versus invalidation policy.
- Exact semantics of supersession and reopening.
- Evidence invalidation as explicit state or derived validity.
- Conformance harness language and interchange format.

Resolve these through focused ADRs after reviewing this plan. None blocks review of the architecture boundary defined here.

## Non-claims

This document does not provide a TLA+ specification, TLC results, theorem proofs, executable tests, cryptographic design, implementation, or assurance that the listed properties currently hold. It is a traceable modeling and test-design plan.