# Architecture 0032 — Canonical governance publication model-checking report

**Status:** recorded model-checking evidence for one bounded TLA+ design model. This report is not a normative adoption decision, an implementation claim, or a proof of production behavior.

## 1. Subject and purpose

This report records the first successful SANY and TLC execution of [GovCheckCanonicalPublication](../../formal/tla/GovCheckCanonicalPublication.tla), introduced alongside the eleven arbitration choices recorded in [decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md).

The model isolates a bounded logical publication protocol: evaluate a candidate against a captured canonical head; authorize only while that evaluated base remains current; publish as a distinct append/effect action; and reject an authorization whose base became stale after another publication.

## 2. Exact model and configuration

- **TLA+ module:** `formal/tla/GovCheckCanonicalPublication.tla`
- **TLC configuration:** `formal/tla/GovCheckCanonicalPublication.cfg`
- **Git blob object ID — module:** `8daef42732223b10142df1c899fc789361ac35ea`
- **Git blob object ID — configuration:** `c535470350360c7e4e54b7026144a23943affb1a`
- **Repository commit checked:** `8c77aeac1ef89e2c6dc7463a65af0f9151fa1bb9`
- **PR:** [#96](https://github.com/Martin-PB/govcheck/pull/96)
- **Workflow run:** [42815445104](https://github.com/Martin-PB/govcheck/actions/runs/42815445104)
- **TLC job:** `canonical-publication / TLC — GovCheckCanonicalPublication` (job ID `129827237434`)

The configuration uses two principals in the finite universe (one designated as the root principal), three governance revisions, two candidates, three evaluation identifiers and three authorization identifiers. The logical journal is bounded to at most three entries including genesis. The publication identifiers are finite. These bounds are part of the checked abstraction, not claims about unbounded production operation.

## 3. Toolchain and execution

- **SANY:** 2.1
- **TLC:** 2.19 (8 August 2024, revision `5a47802`)
- **tla2tools:** v1.7.4
- **tla2tools SHA-256:** `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88` (download checksum verified by the workflow)
- **Java:** Eclipse Temurin 17.0.21+9
- **Search:** breadth-first; four workers on four cores
- **Result:** SANY parsing and semantic processing succeeded; TLC reported “Model checking completed. No error has been found.”
- **State-space statistics:** 84,307 states generated; 56,895 distinct states; zero states remaining; complete graph depth 9.
- **Fingerprint collision estimate:** optimistic probability (8.5 \times 10^{-11}).

## 4. Checked invariants and temporal property

The TLC configuration checked all of the following without counterexample:

1. `TypeOK` — variables remain within the declared finite state types.
2. `UniqueRevisions` — no two journal entries use the same governance revision identity.
3. `ContinuousPredecessors` — each non-genesis entry names the immediately preceding revision.
4. `OnePublicationPerCanonicalPosition` — no two entries append against the same canonical predecessor.
5. `AuthorizationBoundToEvaluation` — an authorization remains bound to the evaluation and its captured base.
6. `PublicationIsEffectPoint` — each non-genesis journal entry's publication identifier is present in the published-event set.
7. `PublishedOnlyIfAuthorized` — each published entry corresponds to an authorization.
8. `NoStalePublication` — a published entry's authorization base position matches the entry's predecessor position.

The temporal property `AppendOnly` was also checked: every non-stuttering transition preserves the existing journal prefix and does not shorten the journal.

## 5. Interpretation and limits

This is model-checking evidence for the exact finite TLA+ module, configuration and toolchain recorded above. It establishes that TLC found no violation in the explored finite state space. It does **not** prove the TLA+ model correct, prove a theorem, prove an implementation, or establish behavior for unbounded or distributed executions.

The model does not yet represent durable storage, crash recovery, replica convergence, independent VCS provenance, evaluator replacement/comparison, revocation and historical requalification, exceptions, unknown/conflict resolution, rollback content restoration, or refinement to executable code. Its publication action is an abstract logical append; it does not establish a database transaction or a production compare-and-swap implementation.

The earlier [Architecture 0031](0031-first-tlc-governance-applicability.md) result remains a separate run on the original applicability model. The complementary evaluator/exception controls and journal recovery slices are recorded in [Architecture 0033](0033-governance-evaluator-exception-revocation-model.md) and [Architecture 0034](0034-canonical-journal-recovery-model.md); their proposed protocol contract is [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.md). These are separate bounded artifacts, not a composed proof. Neither report adopts the eleven choices. Their normative status remains pending the applicable governance adoption event.

## 6. Provenance and reproducibility

The workflow uploaded artifact `tlc-report-GovCheckCanonicalPublication` (artifact ID `13763874296`, SHA-256 digest `eeb439ae60fa0c251a349d19cb89e65f7bd55aa856be29f86fd379aea3e83981`). It contains the SANY report, TLC report and tla2tools checksum. GitHub reports an artifact expiry of 2027-02-08; the run and source revision remain the primary execution references.

This record is linked to [R-05 — TLA+ and TLC](../references.md#r-05) and [R-22 — Native Git and Pijul semantics](../references.md#r-22). The source catalogue remains the central reference authority.
