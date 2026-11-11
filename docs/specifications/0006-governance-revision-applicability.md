# Specification 0006 — Governance revision applicability and temporal authorization

**Status:** proposed contract for maintainer review; it does not adopt or amend the authority decision in Architecture 0023, and it does not claim an implementation. **French:** [0006](0006-governance-revision-applicability.fr.md).

## 1. Purpose and scope

This specification defines how a change evaluation identifies the governance revision that is authorized to evaluate it, especially when the candidate also changes governance, policy, rules, models or evaluators.

It refines [Specification 0003](0003-change-lifecycle.md), [Architecture 0012](../architecture/0012-normative-authority-and-documentation.md), [Architecture 0017](../architecture/0017-artifact-identity-revision-and-versioning.md), [Architecture 0018](../architecture/0018-version-governance-and-compatibility-authority.md), and the current authority regime in [Architecture 0023](../architecture/0023-bootstrap-governance-authority.md).

This is a semantic contract, not a serialization or implementation choice. It does not require wall-clock timestamps, Git commit ancestry, a particular database, forge, Lean, production TLA+, or signature technology.

## 2. Terms

- **Governance revision:** immutable, uniquely identified state of the applicable normative governance package, including the authority and policy semantics needed to resolve a decision.
- **Governance decision:** immutable event authorizing, rejecting, suspending, revoking or superseding a specified governance change.
- **Candidate:** exact proposed repository state, identified independently of its hosting/forge representation.
- **Evaluation:** recorded assessment of an exact candidate under an exact governance revision and evaluator/specification context.
- **Decision position:** position in the canonical governance event order at which an authority decision is recorded.
- **Effective position:** first event position from which a published governance revision is applicable.
- **Base governance revision:** revision under which a proposed governance change is assessed and authorized.
- **Resulting governance revision:** new revision proposed by that change, if any.

Logical artifact ID, content digest, native VCS revision, compatibility version, evaluation/run ID and governance event ID remain distinct identities. SemVer is not a substitute for an immutable governance revision.

## 3. Normative contract proposed for adoption

### 3.1 Immutable governance history

1. Every published governance revision MUST have a stable logical identity and immutable revision identity.
2. Every non-genesis revision MUST identify its predecessor, authorizing decision, authority basis and effective position.
3. Governance history MUST be append-only at the logical level. Correction, revocation, rollback and supersession MUST add explicit events/revisions; they MUST NOT rewrite earlier records.
4. A rollback MUST publish a new revision whose content may correspond to an earlier state. It MUST NOT move event position backwards or erase intervening history.
5. Revision identifiers MUST NOT be reused. Content identity alone does not establish authority.

### 3.2 Deterministic applicability

For any decision or evaluation at canonical event position *p*, the applicable governance revision is the unique published revision whose effective position is the greatest position less than or equal to *p*.

The resolver MUST return the unique applicable revision when exactly one valid chain resolves; `unknown` when history, authority, predecessor, effective position or required semantics are missing/unresolvable; and `conflict` when incompatible revisions claim applicability at the same position or history is inconsistent. `unknown` and `conflict` MUST block normative acceptance.

Implementations MUST NOT fall back to candidate-proposed rules, latest branch contents, wall-clock guesswork, forge defaults or implicit maintainer preference. Event positions MUST be totally ordered within the authority domain and allocated atomically. A monotonic sequence, consensus-backed log position or another justified ordering mechanism may be used. Wall-clock time alone MUST NOT establish ordering or applicability.

### 3.3 Evaluation and authorization of governance-changing candidates

A governance-changing candidate MUST be evaluated against the exact base governance revision applicable at its decision position.

The evaluation record MUST bind at least: repository/native VCS context; exact base and candidate identities; exact base governance revision and authority-chain identity; proposed resulting revision, if any; specification and evaluator identities/revisions; applicable rules/profile and resolved semantics; evidence, assumptions, limitations and result; evaluation event position and provenance.

The authorization decision MUST bind the same candidate and base governance revision as the evaluation. It MUST record decision position, approving principal, authority basis, outcome and rationale.

A candidate MUST NOT be evaluated or authorized under the governance revision it proposes to introduce. The proposed revision becomes applicable only after an explicit authorized publication event at a strictly later effective position.

For a change modifying code and governance together, the prior applicable revision evaluates and authorizes the complete candidate. The resulting revision governs only subsequent events. Merge, push, tag, green CI or file presence does not itself create governance authorization.

### 3.4 Temporal validity and historical decisions

1. Applicability is determined from canonical event history, not by re-resolving old decisions against today's current revision.
2. A historical decision MUST retain the exact governance revision and authority basis applicable at its decision position.
3. A later amendment, revocation or rollback MUST NOT retroactively change the recorded authority basis or validity assessment of an earlier decision.
4. A later event may record that an earlier decision is disputed, invalidated under a previously applicable rule, or affected by new evidence. It MUST preserve the original decision and explain the new event; it MUST NOT rewrite history.
5. Revocation takes effect prospectively at its recorded effective position unless a separately authorized and legally/operationally justified process explicitly records another effect. This specification does not presume retroactive revocation.

### 3.5 Staleness, concurrency and fail-closed behavior

An evaluation or approval is stale if any bound dependency changes, including candidate, base, governance revision, authority chain, applicable profile, specification, evaluator semantics or declared evidence dependency.

Before authorization and again before publication/application, implementation MUST confirm that the evaluated base and governance revision remain current and applicable. A mismatch MUST invalidate the pending evaluation/approval and require re-evaluation; it MUST NOT silently rebase authorization.

Concurrent governance changes MUST serialize at one decision/publication boundary or use an explicit conflict protocol. Two changes evaluated against the same base MUST NOT both publish as if each were the other's successor. The losing/displaced candidate becomes stale and must be re-evaluated against the new base.

Missing authority, ambiguous history, unknown applicability, revoked authority, invalid delegation, stale evidence, conflicting events or unavailable required semantics MUST produce `unknown`, `conflict` or explicit blocked/invalid-governance. None may be coerced to pass.

### 3.6 Authority and separation of concerns

Architecture 0023 currently records one root principal, `Martin-PB`, and explicitly accepts that the same principal may propose and authorize a change. This specification does not change that regime.

Implementations MUST distinguish proposer/producer, technical reviewer/evaluator, normative authorizer and publisher/executor. Where proposer and authorizer may be the same principal, the record MUST disclose this. It MUST NOT claim independent approval or two-person separation. Repository administration, merge permission and CI execution are not normative authority.

Any future delegation MUST be explicit, bounded by action and scope, temporally valid, traceable to its grantor and prospectively revocable. No delegation is inferred.

## 4. Required conformance scenarios

| ID | Scenario | Required result |
|---|---|---|
| GA-01 | Candidate changes policy and attempts to use its new policy for evaluation | Block; evaluate under prior applicable revision |
| GA-02 | Candidate authorized under N publishes N+1 | N+1 applies only after its later effective position |
| GA-03 | Historical decision under N; N+1 later published | Historical decision remains bound to N |
| GA-04 | Revision or authority chain missing/ambiguous/conflicting | `unknown` or `conflict`; no acceptance |
| GA-05 | Evaluation under N, then N+1 published before authorization | Evaluation stale; re-evaluation required |
| GA-06 | Two candidates concurrently target same governance base | At most one publishes from that base; other becomes stale/conflicted |
| GA-07 | Authority revoked before decision position | Block unless valid authority exists under applicable revision |
| GA-08 | Rollback restores old policy content | New event/revision; intervening history retained |
| GA-09 | Proposer and authorizer are same principal under current regime | Permitted only as recorded by authority policy; no independence claim |
| GA-10 | Git/Pijul/forge state changes without matching governance event | No implicit governance publication or authorization |

These are conformance targets. Bounded model checking is evidence about the declared model/configuration only, not theorem proof, implementation proof or operational enforcement.

## 5. Formal model and limits

[GovCheckGovernanceApplicability.tla](../../formal/tla/GovCheckGovernanceApplicability.tla) and its TLC configuration provide a finite transition model for evaluation pinned to current governance; authorization by the authority applicable at the decision position; publication at a strictly later effective position; preservation of historical decision bindings; rejection of stale evaluations; and append-only governance/decision histories.

The model is separate from `GovCheckAuthority.tla` and `GovCheckLifecycle.tla`: it composes their concerns without claiming either existing model already defines temporal applicability. Finite constants and bounded histories do not establish unbounded correctness, cryptographic authenticity, distributed consensus, implementation refinement, complete concurrency behavior or forge enforcement. Delegation, exception lifecycle, detailed revocation and multi-writer consensus remain outside this initial model.

The original applicability model was parsed by SANY and checked by TLC; its exact bounded result and limitations are recorded in Architecture 0031. This is model-checking evidence, not implementation proof.

## 6. Resolved authority selections and remaining implementation obligations

The eleven authority-selected outcomes are recorded in [Decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md). They resolve the design questions that this specification previously left open: canonical serialized logical journal; VCS as transport/provenance rather than normative ordering; publication as the effect point; prior evaluator authority with comparative shadow execution; prospective revocation and separate historical requalification; structured exceptions with non-derogable requirements; distinct blocking `unknown` and `conflict`; historical retention but no reuse of stale evaluations; one successful publication per canonical predecessor; rollback as a new revision; and three distinct logical acts even when technically atomic.

These selections are settled inputs to the technical work. Their formal normative adoption remains reserved to the repository's root authority and is not inferred from this specification, a PR, merge or verification result. The reusable package copy deliberately expresses the authority role generically rather than embedding a repository-specific principal identity.

Remaining implementation/formalization obligations are narrower and concrete: define the trust and failure model for canonical journal durability; specify revision-manifest and authority-chain serialization; define crash-safe atomic append and recovery; define signing/key lifecycle only to the extent required by the selected trust model; map native Git/Pijul identities to logical events without using VCS order as normative order; integrate authority, lifecycle, version-decision and assurance records; and provide an executable resolver, persistence, adapter reconciliation, conformance tests and acceptance-boundary evidence. These are engineering obligations, not unresolved arbitration questions.

## References

- [R-05 — TLA+ and TLC state-transition modeling](../references.md#r-05)
- [R-17 — typed governance metadata and traceable relations](../references.md#r-17)
- [R-22 — native Git and Pijul semantics](../references.md#r-22)
- [R-88 — NIST SP 800-192 policy/model verification](../references.md#r-88)


## 7. Authority-selected arbitration direction — pending formal adoption

The project owner selected the eleven outcomes recorded with provenance in [Decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md). This section records their technical consequences; it does not convert the session into normative adoption. Until a separate adoption event is recorded under the applicable prior governance revision, the requirements below remain an authority-selected proposal.

The selected direction is: (1) a canonical logical journal with serialized append and concurrency control; (2) Git, Pijul and other VCS/forges are transport/provenance adapters, not normative ordering authorities; (3) publication is the first event governed by the resulting revision and is authorized under the prior revision; (4) the prior-governance evaluator remains authoritative while a proposed replacement may run comparatively; (5) revocation is prospective, with separate historical requalification; (6) exceptions are explicit, justified, bounded, attributable, traceable and revocable, while designated requirements are non-derogable; (7) `unknown` and `conflict` are distinct blocking states, both requiring explicit resolution and neither bypassable by exception; (8) stale evaluations remain historical but cannot support a new transition; (9) at most one publication succeeds from a canonical predecessor, and displaced candidates require re-evaluation; (10) rollback creates a new immutable revision even when restoring earlier content; and (11) evaluation, authorization and publication are distinct logical acts even when an adapter executes them in one atomic technical transaction.

### 7.1 Coverage across the bounded formal models and remaining obligations

The previously checked [GovCheckGovernanceApplicability.tla](../../formal/tla/GovCheckGovernanceApplicability.tla) remains limited to its recorded finite applicability abstraction. A separate bounded design model, [GovCheckCanonicalPublication.tla](../../formal/tla/GovCheckCanonicalPublication.tla), has since been added. It models a finite set of prepared evaluations, authorization bound to the captured canonical head, distinct publication as the append/effect action, rejection of stale authorization after the head advances, unique revision identities, predecessor continuity and append-only history. It is routed to the TLC workflow as a separate job.

The canonical-publication model was parsed and checked by TLC; its exact result is recorded in Architecture 0032. The governance-controls model in §7.2 and the separate journal-recovery model in §7.3 complement that coverage for selected A-04 through A-10 semantics. Proposed Specification 0007 defines the related protocol contract. These remain separate finite abstractions: they are not one integrated model or a refinement proof. The cross-model coverage matrix and remaining gaps are recorded in §4 of session record 0008.

The detailed selected outcomes and provenance are maintained in the [English](../decisions/0008-governance-applicability-arbitration-session.md) and [French](../decisions/0008-governance-applicability-arbitration-session.fr.md) session records.


### 7.2 Evaluator, exception and revocation control model

The separate bounded model [GovCheckGovernanceControls.tla](../../formal/tla/GovCheckGovernanceControls.tla), configured by [GovCheckGovernanceControls.cfg](../../formal/tla/GovCheckGovernanceControls.cfg), adds finite transition coverage for the selected A-04 through A-08 semantics:

- only the evaluator recognized under the prior governance revision can create an authoritative evaluation; a proposed replacement can produce comparative shadow results only;
- evaluations distinguish `Pass`, `Fail`, `Unknown` and `Conflict`; the latter two cannot authorize;
- exceptions are explicit, justified, bounded by a logical expiry, revocable, limited to waivable requirements and revalidated at publication; non-derogable requirements cannot be excepted;
- authority revocation is recorded at a later logical position and blocks later publication without deleting earlier decisions;
- historical requalification appends a separate record referring to the original decision and governance revision.

The model deliberately abstracts the authority as one designated prior evaluator/root regime, finite identifiers and requirements, and a bounded number of events. It does not model cryptographic identity, delegation, real-time clocks, durable storage, crash recovery, distributed replicas, or a complete executable exception-risk-acceptance record. It is not an implementation or normative-adoption claim. The exact model/configuration passed SANY 2.1 and TLC 2.19: 2,826,117 states generated, 1,026,484 distinct, zero remaining, depth 12; all nine invariants and `AppendOnly` passed. See [Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.md) for exact model/configuration identities and limits.

### 7.3 Canonical journal protocol, recovery and rollback

[Specification 0007](0007-canonical-governance-journal-protocol.md) proposes the semantic contract for the canonical journal and VCS adapters: stable journal-scope identity, genesis bound to the authority/governance baseline, compare-and-append with one linearization point, durable commit, idempotency keys bound to the exact request, crash recovery, replayable projections, and Git/Pijul adapters limited to transport and provenance. It defines twelve conformance scenarios but selects no storage engine, serialization format, cryptographic algorithm, consensus product, VCS or forge. It remains proposed, not adopted and not implemented.

The bounded [GovCheckJournalRecovery.tla](../../formal/tla/GovCheckJournalRecovery.tla) model and [configuration](../../formal/tla/GovCheckJournalRecovery.cfg) check a single-writer abstraction: durable append as commit point, crash before/after commit, replay-to-head, rollback as a new event/revision restoring earlier content, and passive VCS replica observations. The SANY 2.1/TLC 2.19 run recorded in [Architecture 0034](../architecture/0034-canonical-journal-recovery-model.md) generated 178,549 states, 38,434 distinct, zero remaining; six invariants and `AppendOnly` passed. Weak fairness for `Recover` is assumed, but eventual recovery is not a liveness property checked/reported by TLC.

This model does not establish concrete storage-engine durability, torn-write behavior, multi-writer consensus, divergent-replica convergence/reconciliation, adapter correctness or implementation refinement. The PR #99 recovery model was not on `main`: GitHub marked it merged into the former PR #98 work branch; PRs #100 and #104 remain open and stacked. This review candidate carries the model and Specification 0007 toward `main`, without normative adoption or an implementation claim.
