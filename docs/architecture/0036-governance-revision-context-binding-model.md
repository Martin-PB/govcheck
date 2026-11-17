# Architecture 0036 — Governance revision context-binding model

**Status:** recorded finite model-checking evidence for a bounded cross-model context-binding contract. This record is not normative adoption, implementation evidence, or proof of production enforcement.

## 1. Subject and purpose

This record documents [GovCheckGovernanceContextBinding](../../formal/tla/GovCheckGovernanceContextBinding.tla), a separate TLA+ model for issue #86. It strengthens the temporal applicability slice by binding each governance revision to the exact authority/evaluator/specification/profile context under which evaluations and decisions occur.

The model treats the following as distinct identities/revisions within a governance context:

- authority-policy revision (distinct from the root-principal identity);
- evaluator identity and evaluator revision;
- specification identity and specification revision;
- assurance/profile identity and profile revision.

An evaluation records its exact base governance revision, context token, lifecycle base/candidate identifiers and specification identity/revision. Authorization is possible only while the captured governance revision and complete context remain current. The decision retains that exact context and the resulting governance/context proposal. Publication establishes the resulting context only at a strictly later logical position.

## 2. Exact model and configuration

- **TLA+ module:** `formal/tla/GovCheckGovernanceContextBinding.tla`
- **TLC configuration:** `formal/tla/GovCheckGovernanceContextBinding.cfg`
- **Git blob — module:** `8a0ae668dab8eb279ed55b39649a326689b5cdac`
- **Git blob — configuration:** `c04a9104c604517c421e765bf22d247b9815a813`
- **Checked PR head:** `fdd6eb3a4d93d15d32e7d837ad25604898e9845d`
- **TLC workflow run:** [44131092595](https://github.com/Martin-PB/govcheck/actions/runs/44131092595)
- **TLC job:** `134208042142`
- **TLA tools:** tla2tools v1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`
- **SANY:** 2.1
- **TLC:** 2.19
- **Java:** Temurin 17

The reusable TLC workflow passed SANY parsing/semantic checking and TLC model checking. TLC reported:

- **486,289** generated states;
- **486,289** distinct states;
- **0** states remaining;
- complete state-graph depth **8**;
- no invariant or temporal-property violation.

All twelve configured invariants passed: `TypeOK`, `UniqueGovernanceRevisions`, `GovernanceChainIsContinuous`, `OnlyApplicableAuthorityCanAuthorize`, `DecisionUsesApplicablePriorGovernance`, `EvaluationUsesApplicableContext`, `DecisionUsesApplicableContext`, `EvaluationAuthorizationBinding`, `NoSelfAuthorization`, `PublishedOnlyAfterAuthorization`, `HistoricalDecisionsRemainBound`, and `CurrentContextMatchesHead`. The temporal property `AppendOnly` also passed.

## 3. Cross-model binding obligations exercised

The model checks the following relations:

1. The governance revision applicable at an evaluation's logical position is the revision recorded in the lifecycle evaluation tuple.
2. The evaluation's base context resolves to the exact authority revision, evaluator identity/revision, specification identity/revision and profile identity/revision selected by that governance revision.
3. The authorization decision is made by the authority principal applicable at its decision position and preserves the evaluation's exact base, candidate, governance and context bindings.
4. A governance-changing candidate cannot authorize itself: the resulting governance revision is not applicable at the decision position.
5. The resulting context is published only after the authorization decision and becomes effective at a later event position.
6. Historical decisions remain bound to the context applicable when they were made, even after a later context is published.
7. The governance, evaluation and decision histories are append-only.

The context token has two finite interpretations in this TLC instance. This is a bounded test fixture, not a selected serialization format or production context schema.

## 4. Deliberate limits

This is a cross-model binding contract, not a fully integrated state machine:

- It does not import/instantiate the complete `GovCheckAuthority`, `GovCheckLifecycle`, `GovCheckCanonicalPublication`, `GovCheckGovernanceControls` and `GovCheckJournalRecovery` modules. Those remain separate finite abstractions.
- The root principal is fixed. The authority-revision token represents a change in authority semantics; it does not model root-principal succession, delegation, cryptographic identity or a complete authority chain.
- The model records lifecycle base/candidate identifiers but does not itself maintain a mutable repository-head variable or prove native Git/Pijul adapter behavior. Captured-head staleness and single-winner publication are addressed by the separate canonical-publication model.
- Evaluator shadow execution, exceptions, unknown/conflict resolution, revocation, rollback, crash recovery, storage durability and distributed consensus remain in their separate models or unimplemented obligations.
- The two hard-coded context interpretations do not define a general manifest, serialization, schema-evolution or compatibility mechanism.

The result is model-checking evidence for this exact finite model/configuration only. It is not theorem proof, implementation refinement, operational enforcement, cryptographic assurance or normative adoption.

## 5. Relationship to Specification 0006

This model provides an executable bounded slice for the identity-binding obligations in Specification 0006: authority revision, evaluator identity/revision, specification identity/revision and profile identity/revision must be captured at evaluation and preserved through authorization; a resulting context becomes applicable only after publication. It does not close the specification's remaining obligations for canonical-journal trust/failure semantics, manifest serialization, durable atomic append, key lifecycle, VCS adapter reconciliation, integrated persistence/resolver behavior, executable conformance suites or implementation refinement.

## 6. References

- [Specification 0006 — governance revision applicability](../specifications/0006-governance-revision-applicability.md)
- [Decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md)
- [Architecture 0023 — bootstrap governance authority](0023-bootstrap-governance-authority.md)
- [Architecture 0031 — initial applicability model](0031-first-tlc-governance-applicability.md)
- [Architecture 0032 — canonical publication model](0032-canonical-publication-model-checking.md)
- [Architecture 0033 — evaluator, exception and revocation model](0033-governance-evaluator-exception-revocation-model.md)
- [Architecture 0035 — journal recovery and rollback model](0035-canonical-journal-recovery-model.md)
- [R-05 — TLA+ and TLC state-transition modeling](../references.md#r-05)
- [R-17 — typed governance metadata and traceable relations](../references.md#r-17)
- [R-22 — native Git and Pijul semantics](../references.md#r-22)
