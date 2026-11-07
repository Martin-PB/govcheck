# Specification 0003 — Change Lifecycle and Acceptance

**Status:** Proposed architecture, ready for review. **French:** [0003](0003-change-lifecycle.fr.md).

## Principle and identity

GovCheck defines the normative lifecycle. Git branches/commits/PRs, Pijul channels/patches, review platforms, patch exchange and local workflows are mechanisms, not the lifecycle itself. A change is an identified proposal to move a repository from an exact base state to an exact candidate state; it is not synonymous with any native VCS or forge object.

A change record binds repository identity, base and candidate descriptors, governance package revision and semantics, change ID and supersession links, affected resources, intent/risk, participants/decision authorities, evidence and evaluation.

## Abstract states

Proposed → Prepared → Evaluated → Reviewable → Accepted → Applied. Terminal or exceptional states include Rejected, Withdrawn, Stale and Superseded. Implementations may add substates. Accepted and Applied are distinct: acceptance is a decision about an exact candidate; application is a VCS/collaboration operation.

## Transition guards

Every transition is an explicit auditable event with actor, time, input/output state, reason and provenance.
- Proposed → Prepared: identities and impact scope resolve.
- Prepared → Evaluated: evaluation runs on pinned inputs.
- Evaluated → Reviewable: no unresolved invalid-governance condition; required evidence and explanations are available.
- Reviewable → Accepted: all blocking obligations pass, evidence is valid, required approvals are authentic/authorized and exceptions valid.
- Accepted → Applied: adapter confirms the exact accepted candidate was applied.
- Any pre-application state → Stale: a relevant input changes or evidence is invalidated.
- Authorized rejection/withdrawal and explicit supersession are recorded as events.

No transition is inferred from branch names, PR labels, CI status or chat messages. Approval authority comes from governance, not forge convention.

## Evidence freshness

Each evidence item binds claim/rule IDs, subject identity, base/candidate fingerprints, governance revision/semantics, specification revision, method/tool/version/configuration/scope, assumptions/environment/external inputs, result/time/provenance and integrity reference. Changes to a declared dependency (candidate, base, governance, evaluator, tool, assumptions or external facts) invalidate evidence. Old evidence remains in history but cannot support a new state without revalidation. Re-evaluation never erases prior failures.

## Acceptance predicate

Acceptance is derived, not an editable flag. It requires pinned candidate and governance identities; evaluation of all mandatory rules; no blocking failure, conflict or indeterminacy; valid in-scope evidence; required authentic approvals; narrow unexpired exceptions; and an adapter capable of identifying the candidate and verifying subsequent application.

Local-only acceptance uses the same predicate but states that no remote enforcement exists. Shared enforcement requires a team authority or forge integration gate.

## Concurrency, audit and verification

Base changes, rebases and Pijul graph/channel changes require adapter analysis of evidence validity; textual similarity is insufficient. Approvals bind to exact candidate and governance revisions. Logical audit history is append-only; corrections add events.

Future tests and formal models must cover illegal transitions, stale evidence, post-approval mutation, governance changes, exact application, concurrent approvals, local-only acceptance, safety (never accept invalid state) and liveness (valid changes can progress). No lifecycle engine exists yet.

## Bibliographic references

- [R-22 — Native Git and Pijul semantics](../references.md#r-22)
