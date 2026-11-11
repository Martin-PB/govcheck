# Architecture 0034 — Canonical journal durability, recovery and rollback model

**Status:** bounded TLA+ design model; SANY/TLC checked for the exact finite configuration. This is not implementation evidence, normative adoption, or proof of operational durability. **French:** [0034](0034-canonical-journal-recovery-model.fr.md).

## 1. Purpose

This model isolates the persistence boundary left open by the canonical-publication and governance-controls models. It examines the consequences of a durable append, a crash before or after that append, recovery from the durable journal, rollback as a new event, and VCS replica observations.

It encodes the owner-selected design inputs recorded in decision-session record 0008: the logical journal is the normative ordering authority; Git, Pijul and other VCS systems provide transport/provenance observations; rollback appends a new revision and never rewrites history. It does not re-arbitrate or adopt those choices.

## 2. Model

- Module: [GovCheckJournalRecovery.tla](../../formal/tla/GovCheckJournalRecovery.tla)
- Configuration: [GovCheckJournalRecovery.cfg](../../formal/tla/GovCheckJournalRecovery.cfg)
- Stable artifact ID: `govcheck.journal-recovery`
- Package mirror: `govcheck/formal/tla/GovCheckJournalRecovery.tla` and `.cfg`

The finite model contains a durable append-only journal, a volatile pending record, an applied-position marker, a crash flag and per-replica observed positions. `CommitDurably` is the journal commit point. A crash discards only an uncommitted pending record. Recovery derives the applied position from the durable journal head. A rollback appends a fresh event/revision whose content is selected from an earlier journal position.

Replica observations are constrained to positions that exist in the journal; they cannot append, reorder, select or advance the normative head. A Git/Pijul observation is therefore provenance/replication state, not governance publication.

## 3. Checked properties

- `TypeOK`: state values remain within the declared finite domains.
- `AppendOnly`: every journal transition preserves the prior journal as an exact prefix.
- `UniqueEventAndRevisionIds`: event and revision identities are never reused.
- `PositionAndPredecessorContinuity`: positions increase by one and each event names the immediately preceding revision.
- `RollbackRestoresContentAsNewEvent`: rollback content is drawn from a prior journal state while the rollback itself has a new position and identity.
- `VCSObservationIsNonAuthoritative`: replica observations cannot claim a position beyond the canonical head.
- `AppliedStateIsDurable`: applied state cannot advance beyond the durable journal head.

## 4. Failure model and limits

This is a small finite transition abstraction, not a storage-engine specification. It models one serialized writer and one journal; it does not model torn writes, filesystem ordering, checksums, quorum/consensus, Byzantine actors, disk corruption, backup/restore, key management, concurrent writers, divergent-replica reconciliation protocols, or an actual Git/Pijul adapter. Replica observations are intentionally passive and cannot prove provenance authenticity.

The model's recovery action is an abstract replay-to-head operation. It does not prove that a concrete implementation can reconstruct all materialized state, nor that external side effects are idempotent. The bounded content/revision/event domains do not establish unbounded correctness.

The recorded TLC result is model-checking evidence for the exact checked module/configuration only. It is not theorem proof, implementation verification, or production assurance.



## 5. TLC verification evidence

The exact module/configuration passed SANY 2.1 and TLC 2.19 on PR #99 head `a5c9845b1df7a36c9b1f23af0a28bdabdd4300f3` (CI merge checkout recorded by workflow run [42848709804](https://github.com/Martin-PB/govcheck/actions/runs/42848709804)).

- Module Git blob: `f99b33f510f3350f7ee1dc2ecc4b13a216d64ab6`.
- Configuration Git blob: `43102a4fc3c17a0656ccfe71d34642457d85737a`.
- Result: 178,549 states generated, 38,434 distinct, zero remaining; complete graph depth 9.
- Six configured invariants and temporal property `AppendOnly` passed; no counterexample was found.
- Job: `129943126960`; uploaded report artifact ID `13778403717`, ZIP SHA-256 `0fe3148982524a25336674718505b02fd786953bd000d9b06ae016ec4987d00b`.
- Toolchain: tla2tools v1.7.4 (SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`), SANY 2.1, TLC 2.19, Temurin Java 17.0.21+9, four workers.

This is finite model-checking evidence for these exact source/configuration identities. It is not theorem proof, implementation verification or evidence of storage-engine durability. The model includes weak fairness for the abstract `Recover` action, but the TLC configuration checks safety invariants and `AppendOnly` only; it does not check or report a separate eventual-recovery liveness property. No claim about recovery liveness in a concrete implementation is made. The authorization and evaluator controls are abstracted to the upstream governance/publication models and are not re-proved here.



Final PR-head revalidation: the same module/configuration blobs were rechecked on the final documentation/package head `8ace02658a9f349db57e937c697e66c7b779aaa8` in [workflow run 42849634866](https://github.com/Martin-PB/govcheck/actions/runs/42849634866), job `129946416981`. The result was identical: 178,549 generated / 38,434 distinct states, zero remaining, depth 9; all six invariants and `AppendOnly` passed. Final-head report artifact ID `13778459512`, SHA-256 `8ce7414863ef57725e7ae36e3055d10edb21571feb62c35d9fae68228a96b94c`. All eight configured PR checks passed on that final head.

## 6. Related contract and references

This model complements [Specification 0006](../specifications/0006-governance-revision-applicability.md), proposed [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.md), [Architecture 0032](0032-canonical-publication-model-checking.md), [Architecture 0033](0033-governance-evaluator-exception-revocation-model.md) and [decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md). Its conceptual foundations are catalogued under [R-05 — TLA+ and TLC](../references.md#r-05) and [R-22 — native Git and Pijul semantics](../references.md#r-22).

It does not claim the journal, recovery procedure or VCS adapters are implemented.
