# Portfolio event journal

**Policy:** append-only. This is a logical journal, not a tamper-proof storage mechanism. Never edit or delete an earlier event; corrections are new events.

## References used

- [R-05 — TLA+ and TLC](../references.md#r-05) — bounded formal-model evidence recorded in the journal.
- [R-107 — GitHub Actions workflow location and syntax](../references.md#r-107) — source-catalogue provenance for workflow-location references in the integration audit.
- [R-22 — Native Git and Pijul semantics](../references.md#r-22) — distinction between VCS observations and normative journal order.
- [R-142 — Linearizability](../references.md#r-142) — the single linearization point for concurrent appends.
- [R-143 — ARIES write-ahead logging and recovery](../references.md#r-143) — durable commit and recovery boundary.
- [R-144 — RFC 9110 idempotent methods](../references.md#r-144) — safe retry semantics after a lost response.

## WP-EVT-000001 — Initial issue-to-registry import

- **Subject:** govcheck.work-portfolio
- **Event type:** initial-import
- **Recorded:** 2026-11-09
- **Actor/provenance:** maintainer-directed repository migration, prepared by an automated assistant through the GitHub repository integration.
- **Base:** main at 93024d4d0e61a9dcac93510cd607098094e12238.
- **Candidate:** branch work/governed-work-portfolio-registry; exact resulting commit is preserved by the PR and repository history.
- **Scope:** create the repository-backed portfolio; map issues #33, #41–#77 and #86 where relevant; preserve issue numbers as adapter provenance; retain open issues during transition; delete no source discussions.
- **Disposition:** candidate import for maintainer review. This event does not authorize execution of imported work and does not adopt Architecture 0028 before the required governance decision.
- **Rationale:** GitHub issues are forge-specific mutable coordination records. The repository needs a forge-independent, revision-addressable portfolio and must not rely on issue-editor discipline to preserve prior accepted states.
- **Related records:** README.md, work-items.md, Architecture 0028 and Specification 0003.
- **Known limitations:** no machine-enforced append-only storage, independent backup, signature policy, automatic adapter synchronization or local edit interception is implemented by this migration.

 
## WP-EVT-000002 — Adapter pointers and migration cross-references updated

- **Subject:** govcheck.work-portfolio
- **Event type:** adapter-mapping-updated
- **Recorded:** 2026-11-09
- **Actor/provenance:** maintainer-directed migration, prepared by an automated assistant through the GitHub repository integration.
- **Base:** main at 90f155489e2ff0138e0270e181f509d72124429b (the branch was synchronized with this mainline before final review).
- **Candidate:** current head of work/governed-work-portfolio-registry; see PR #89 for the exact candidate revision.
- **Scope:** prepend canonical registry pointers to GitHub issues #40 and #78–#85 without deleting their existing bodies; map atomic issue #33 to its stable work ID; record #46 as completed pending closure after registry acceptance; link #75 to the pending adoption proposal.
- **Disposition:** adapter updates only. All referenced issues remain open. No issue closure, work authorization or Architecture 0028 adoption is implied.
- **Rationale:** make the transition discoverable while preserving the existing GitHub coordination dossiers and their histories.
- **Related records:** PR #89; work-items.md; README.md; Architecture 0030.
- **Known limitations:** issue edits are still performed through GitHub's native mutable API; no automatic synchronization, tamper-proof issue history or registry enforcement is claimed.


## WP-EVT-000003 — Governance revision applicability specification and model prepared

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** specification-and-model-prepared
- **Recorded:** 2026-11-09
- **Actor/provenance:** maintainer instruction to proceed with the #86 work item; technical artifacts prepared by an automated assistant through the GitHub repository integration.
- **Base:** main after merge of PR #89; exact branch base is recorded in the pull request comparison.
- **Candidate:** branch work/governance-revision-applicability; exact commits are preserved by branch and PR history.
- **Scope:** add Specification 0006 in English/French; refine Specification 0003; add a separate bounded governance-applicability TLA+ module/configuration; add the reusable package counterpart; integrate catalogue backlinks, indexes and scoped TLC workflow.
- **Disposition:** proposed technical contract and model for review. This event does not adopt the specification, amend Architecture 0023, or authorize a governance regime change. Decision #41 remains reserved to the designated authority.
- **Rationale:** the existing authority and lifecycle models did not bind a decision position to the unique governance revision effective at that position. The new model isolates this missing temporal applicability contract without claiming that either existing model already provides it.
- **Related records:** Issues #41 and #86; Specification 0006; formal/tla/GovCheckGovernanceApplicability.tla; Architecture 0023; PR for work/governance-revision-applicability.
- **Known limitations:** TLC has not yet been executed for this candidate; the model is finite and does not establish cryptographic identity, distributed consensus, implementation refinement, complete multi-writer concurrency, delegation or forge enforcement.


## WP-EVT-000004 — Governance applicability model checked successfully

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** model-checking-completed
- **Recorded:** 2026-11-09
- **Actor/provenance:** hosted GitHub Actions run authorized for this public repository; workflow executed automatically on PR #90.
- **Source commit:** 3a8d0176bff8783e25103a4603bb4eea06664cee.
- **Merge-test commit:** e226461 (PR merge test against base d04a6dd02d5bdda0b40e4aa740475a8e554e63d7).
- **Model/configuration:** formal/tla/GovCheckGovernanceApplicability.tla and .cfg; blob SHAs 43743eac208f9faf9a844ae35c55ceb6e2b74239 and 54d7387bfe577c5bd9152c7427fc5410c4a00db2.
- **Toolchain:** SANY 2.1; TLC 2.19; Java Temurin 17.0.21+9; tla2tools v1.7.4 SHA-256 936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88; 4 workers.
- **Result:** no error/counterexample; 20,785 states generated, 18,067 distinct states, zero states remaining. Configured invariants and temporal property AppendOnly completed.
- **Evidence:** [workflow run](https://github.com/Martin-PB/govcheck/actions/runs/42659943881), [job report artifact](https://github.com/Martin-PB/govcheck/actions/runs/42659943881/artifacts/13693473469), Architecture 0031 EN/FR.
- **Disposition:** finite model-checking evidence only. It does not prove unbounded correctness, theorem validity, implementation refinement, cryptographic identity, distributed consensus or operational enforcement. Authority #41 and normative adoption of Specification 0006 remain open.
- **Correction history:** the initial TLC attempt exposed a CHOOSE/indexing defect after SANY passed; the model was corrected and this event records only the subsequent successful run.


## WP-EVT-000005 — Final PR-head model-checking revalidation

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** final-candidate-model-checking-revalidated
- **Recorded:** 2026-11-09
- **Candidate source commit:** e2f1b638a79c2a2f04b90d2ef85e6dd761a611eb.
- **Merge-test commit:** 9fbeb85, merged against base d04a6dd02d5bdda0b40e4aa740475a8e554e63d7.
- **Workflow/job:** [run 42660278801](https://github.com/Martin-PB/govcheck/actions/runs/42660278801), job 129309691476.
- **Result:** SANY/TLC success; 20,785 generated states, 18,067 distinct states, 0 remaining; no error found. The model/configuration blobs are unchanged from the first successful run.
- **Artifact:** [final-head report](https://github.com/Martin-PB/govcheck/actions/runs/42660278801/artifacts/13693439123).
- **Disposition:** confirms the formal result on the final PR candidate; the same finite-model and non-implementation-proof limits apply.


## WP-EVT-000006 — Latest PR-head verification recorded

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** final-head-model-checking-revalidated
- **Recorded:** 2026-11-09
- **Candidate source commit:** ff4a1457335d7a2600f2bb12850b74926ba6304b.
- **Merge-test commit:** 7cd7732, merged against base d04a6dd02d5bdda0b40e4aa740475a8e554e63d7.
- **Workflow/job:** [run 42660448408](https://github.com/Martin-PB/govcheck/actions/runs/42660448408), job 129310275465.
- **Result:** SANY/TLC success; 20,785 generated states, 18,067 distinct states, 0 remaining; no error found.
- **Artifact:** [latest TLC report](https://github.com/Martin-PB/govcheck/actions/runs/42660448408/artifacts/13694860086).
- **Disposition:** same model/configuration blobs and finite-state result; no additional assurance claim beyond bounded model checking.


## WP-EVT-000007 — PR #90 merged into main

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** technical-proposal-merged
- **Recorded:** 2026-11-09
- **Actor/provenance:** GitHub merge record for [PR #90](https://github.com/Martin-PB/govcheck/pull/90).
- **Base:** `main`; merge commit `5af21e58ef597480061a2712aaf94a3e2980ba7f`.
- **Candidate:** `work/governance-revision-applicability`, final PR head `4aeb1b6ff1088e95dc6346452491eee4dd1c750d`.
- **Scope:** merge Specification 0006 EN/FR, refinement of Specification 0003, bounded applicability model/configuration, package copies, indexes, reference backlinks and Architecture 0031 EN/FR.
- **Disposition:** technical proposal merged. Merge does not adopt Specification 0006, decide issue #41, or claim implementation. The recorded TLC result remains limited to the exact finite model/configuration described by Architecture 0031.
- **Related records:** PR #90; Issues #41 and #86; Specifications 0003 and 0006; Architecture 0031.
- **Known limitations:** issue #86 and issue #41 bodies still require synchronization; the model's documented limits remain in force.

## WP-EVT-000008 — Issue #41 arbitration session choices recorded

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** authority-arbitration-session-recorded
- **Recorded:** 2026-11-10
- **Actor/provenance:** explicit selections by the project owner in the guided arbitration session for issue #41; full bilingual record in [Decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md) and its [French counterpart](../decisions/0008-governance-applicability-arbitration-session.fr.md).
- **Scope:** eleven selected outcomes covering canonical journal ordering, VCS adapter role, publication effect, evaluator transition, revocation/requalification, exceptions, unknown/conflict, stale evaluations, concurrent publication, rollback and logical act separation.
- **Disposition:** session choices recorded for technical formalization. This event is not a normative adoption event, does not amend Architecture 0023 and does not authorize implementation beyond the separate task/PR review process.
- **Related records:** Issue #41; Issue #86; Specifications 0003 and 0006; session record 0008.
- **Known limitations:** the current bounded TLA+ model does not cover all eleven selected outcomes. Additional modeling, local verification and implementation/conformance evidence remain outstanding.


## WP-EVT-000009 — Canonical publication model added (verification pending)

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** formal-design-model-added
- **Recorded:** 2026-11-10
- **Actor/provenance:** technical formalization of the eleven user-selected arbitration outcomes recorded in decision-session record 0008.
- **Artifact:** `formal/tla/GovCheckCanonicalPublication.tla`, configuration `formal/tla/GovCheckCanonicalPublication.cfg`, stable artifact ID `govcheck.canonical-publication` in `formal/artifacts.json`.
- **Scope:** finite compare-and-append against a captured canonical head; evaluation, authorization and publication as distinct actions; stale-base authorization rejection; unique revision identities; predecessor continuity; one publication per canonical predecessor; authorization/evaluation binding; append-only temporal property.
- **CI routing:** the governance-applicability TLC workflow now invokes both the prior applicability model and this model when the relevant model inputs change. No workflow was triggered by this change.
- **Verification status:** not yet parsed or checked by TLC. No state-space count, pass result or model-checking claim is made for this artifact.
- **Known exclusions:** evaluator replacement/comparison, revocation and historical requalification, exceptions, unknown/conflict resolution, rollback content restoration, VCS replica reconciliation, crash recovery and implementation refinement remain outside this model.
- **Disposition:** design artifact added for review only. It does not adopt the arbitration choices, implement a journal or establish production enforcement.


## WP-EVT-000010 — Canonical publication model checked by TLC

- **Subject:** govcheck.canonical-publication
- **Event type:** bounded-formal-model-checking-completed
- **Recorded:** 2026-11-10
- **Workflow:** GitHub Actions run [42815445104](https://github.com/Martin-PB/govcheck/actions/runs/42815445104), job `canonical-publication / TLC — GovCheckCanonicalPublication` (job ID `129827237434`).
- **Checked revision:** commit `8c77aeac1ef89e2c6dc7463a65af0f9151fa1bb9`; model Git blob `8daef42732223b10142df1c899fc789361ac35ea`; configuration Git blob `c535470350360c7e4e54b7026144a23943affb1a`.
- **Toolchain:** SANY 2.1; TLC 2.19; tla2tools v1.7.4 (SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`); Temurin Java 17.0.21+9; four workers.
- **Result:** SANY parse/semantic check passed; TLC reported no error. 84,307 states generated, 56,895 distinct states, zero remaining; complete graph depth 9. Eight configured invariants and temporal property `AppendOnly` passed.
- **Report:** [Architecture 0032](../architecture/0032-canonical-publication-model-checking.md). Uploaded artifact ID `13763874296`, SHA-256 `eeb439ae60fa0c251a349d19cb89e65f7bd55aa856be29f86fd379aea3e83981`.
- **Interpretation:** bounded model-checking evidence only for the exact finite model/configuration and toolchain. It is not theorem proof, implementation verification, or evidence for unbounded/distributed behavior. Normative adoption of the eleven arbitration choices remains pending.


## WP-EVT-000011 — Governance controls model checked by TLC

- **Subject:** `govcheck.governance-controls`
- **Event type:** `bounded-formal-model-checking-completed`
- **Recorded:** 2026-11-10
- **Workflow:** GitHub Actions run [42825118727](https://github.com/Martin-PB/govcheck/actions/runs/42825118727), job `governance-controls / TLC — GovCheckGovernanceControls` (job ID `129860312738`).
- **Checked PR head:** `86713a99574c085ee5a41a71e70f93ab7ce4a831`; CI merge checkout `1f387b8f6019db545ccd50d55fd9c7cc0d704d80`.
- **Exact source identities:** module Git blob `b237fa3bc939c711f0510c4aeca1346c8e50264f`; configuration Git blob `9e8f48d409eeb31adaf22890bbb8ff90674aa96a`.
- **Toolchain:** SANY 2.1; TLC 2.19; tla2tools v1.7.4 (SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`); Temurin Java 17.0.21+9; four workers.
- **Result:** 2,826,117 states generated, 1,026,484 distinct, zero remaining; complete graph depth 12. Nine invariants and temporal property `AppendOnly` passed; no error found.
- **Report:** [Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.md). Uploaded artifact ID `13769345897`, SHA-256 `66e3537f1f2df50711436c8244d9406d8bc01714536f523a10fe075ab4b875eb`.
- **Interpretation:** bounded model-checking evidence only for the exact finite model/configuration and toolchain. It does not prove implementation refinement, unbounded concurrency, durable storage, crash recovery, distributed behavior or normative adoption. The one-evaluation/one-authorization bound and other limits are explicit in Architecture 0033.


## WP-EVT-000012 — Canonical journal recovery and rollback model checked

- **Subject:** `govcheck.journal-recovery`
- **Event type:** `bounded-formal-model-checking-completed`
- **Recorded:** 2026-11-10
- **Workflow:** GitHub Actions run [42848709804](https://github.com/Martin-PB/govcheck/actions/runs/42848709804), job `journal-recovery / TLC — GovCheckJournalRecovery` (job ID `129943126960`).
- **Checked PR head:** `a5c9845b1df7a36c9b1f23af0a28bdabdd4300f3`.
- **Exact source identities:** module Git blob `f99b33f510f3350f7ee1dc2ecc4b13a216d64ab6`; configuration Git blob `43102a4fc3c17a0656ccfe71d34642457d85737a`.
- **Toolchain:** SANY 2.1; TLC 2.19; tla2tools v1.7.4 (SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`); Temurin Java 17.0.21+9; four workers.
- **Result:** 178,549 states generated, 38,434 distinct, zero remaining; complete graph depth 9. Six invariants and temporal property `AppendOnly` passed.
- **Report:** [Architecture 0034](../architecture/0034-canonical-journal-recovery-model.md). Uploaded artifact ID `13778403717`, SHA-256 `0fe3148982524a25336674718505b02fd786953bd000d9b06ae016ec4987d00b`.
- **Scope/limits:** finite two-event trace with one serialized writer, one durable journal, crash-before/after-commit transitions, recovery-to-head action, rollback restoring earlier content under a new event/revision, and passive Git/Pijul replica observations. This is bounded safety/model-checking evidence only; authorization is abstracted by upstream models, and eventual recovery, storage-engine durability, torn writes, multi-writer consensus, divergent-replica reconciliation and implementation refinement are not established.
- **Disposition:** technical model-checking evidence; no implementation claim, normative adoption or issue closure.


## WP-EVT-000012 — Canonical journal recovery and rollback model checked

- **Subject:** `govcheck.journal-recovery`
- **Event type:** `bounded-formal-model-checking-completed`
- **Recorded:** 2026-11-10
- **Workflow:** GitHub Actions run [42848709804](https://github.com/Martin-PB/govcheck/actions/runs/42848709804), job `journal-recovery / TLC — GovCheckJournalRecovery` (job ID `129943126960`).
- **Checked PR head:** `a5c9845b1df7a36c9b1f23af0a28bdabdd4300f3`.
- **Exact source identities:** module Git blob `f99b33f510f3350f7ee1dc2ecc4b13a216d64ab6`; configuration Git blob `43102a4fc3c17a0656ccfe71d34642457d85737a`.
- **Toolchain:** SANY 2.1; TLC 2.19; tla2tools v1.7.4 (SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`); Temurin Java 17.0.21+9; four workers.
- **Result:** 178,549 states generated, 38,434 distinct, zero remaining; complete graph depth 9. Six invariants and temporal property `AppendOnly` passed.
- **Report:** [Architecture 0034](../architecture/0034-canonical-journal-recovery-model.md). Uploaded artifact ID `13778403717`, SHA-256 `0fe3148982524a25336674718505b02fd786953bd000d9b06ae016ec4987d00b`.
- **Scope/limits:** finite two-event trace with one serialized writer, one durable journal, crash-before/after-commit transitions, recovery-to-head action, rollback restoring earlier content under a new event/revision, and passive Git/Pijul replica observations. This is bounded safety/model-checking evidence only; authorization is abstracted by upstream models, and eventual recovery, storage-engine durability, torn writes, multi-writer consensus, divergent-replica reconciliation and implementation refinement are not established.
- **Disposition:** technical model-checking evidence; no implementation claim, normative adoption or issue closure.


## WP-EVT-000013 — Canonical journal and VCS adapter protocol specification proposed

- **Subject:** `govcheck.spec.canonical-journal-protocol`
- **Event type:** `technical-contract-proposed`
- **Recorded:** 2026-11-10
- **Candidate:** PR #100, branch `work/issue-86-journal-protocol-spec`, based on PR #99.
- **Scope:** bilingual Specification 0007 defines technology-neutral event identity/envelopes, compare-and-append linearization, durable commit/idempotent retry, crash recovery, distinct evaluation/authorization/publication acts, VCS provenance-only adapters, replica reconciliation, blocking result vocabulary and twelve conformance scenarios.
- **Authority boundary:** the specification elaborates the eleven owner-selected design inputs without re-arbitration. It is a proposal only; no normative adoption, database/serialization/crypto/consensus choice, production implementation or issue closure is inferred.
- **Related records:** Specifications 0006/0007; Architectures 0032–0034; [R-05](../references.md#r-05) and [R-22](../references.md#r-22).
- **Known limits:** protocol semantics and conformance targets only. No storage engine, adapter, executable conformance harness or implementation refinement is delivered by this event.


## WP-EVT-000014 — Journal protocol review clarifications prepared

- **Subject:** `govcheck.spec.canonical-journal-protocol`
- **Event type:** `technical-review-clarifications-proposed`
- **Recorded:** 2026-11-10
- **Candidate:** [PR #104](https://github.com/Martin-PB/govcheck/pull/104), branch `work/issue-86-journal-protocol-review-fixes`, stacked on PR #100.
- **Scope:** clarify stable journal-scope identity without choosing its repository/domain cardinality; bind genesis to the initial authority/governance baseline and explicit trust anchor; state algorithm-neutral integrity/authenticity requirements; define idempotency-key scope, exact-request binding, retention and genesis exception; add [R-142](../references.md#r-142), [R-143](../references.md#r-143) and [R-144](../references.md#r-144) on linearizability, write-ahead logging/recovery and idempotent retries; correct Architecture 0034's recovery-fairness wording and section numbering in EN/FR.
- **Disposition:** proposed technical/documentary clarification only. Specification 0007 remains proposed; the eleven owner-selected outcomes remain pending formal normative adoption. No storage engine, cryptographic suite or consensus protocol is selected.
- **Related records:** PR #100; PR #104; Specification 0007 EN/FR; Architecture 0034 EN/FR; references R-142–R-144.
- **Known limits:** no new TLA+ model or implementation is added; no production journal, genesis mechanism, adapter, durability guarantee or implementation refinement is claimed.

## WP-EVT-000015 — Duplicate portfolio event identifier detected

- **Subject:** `govcheck.work-portfolio`
- **Event type:** `append-only-journal-integrity-observation`
- **Recorded:** 2026-11-10
- **Observation:** `WP-EVT-000012` appears twice verbatim in this journal, with the same subject, workflow run, model/configuration identities and artifact digest.
- **Interpretation:** the two textual occurrences describe one model-checking event, not two independent events. The duplication is a journal-document integrity defect; it does not alter the underlying TLC result or its provenance.
- **Disposition:** prior entries are preserved under the append-only policy. This new event records the correction without deleting or rewriting either occurrence. Future event-ID uniqueness checks should detect this class of duplication.
- **Related records:** WP-EVT-000012; Architecture 0034; PR #99.

## WP-EVT-000016 — Issue #41/#86 GitHub integration state reconciled

- **Subject:** `govcheck.work.governance-revision-temporal-applicability`
- **Event type:** `technical-integration-status-reconciled`
- **Recorded:** 2026-11-11
- **Actor/provenance:** read-back of current GitHub PR, branch, merge and workflow-run metadata; this entry records repository facts, not a governance decision.
- **Main head inspected:** `a9ea85796e9864296bef4c0ff33d174d63dc3b75`.
- **Integrated PRs:** #90 merged into main at `5af21e58ef597480061a2712aaf94a3e2980ba7f`; #96 merged at `934000a73aa0f34acd9b692b072d29b7877a8f2b`; #98 merged at `a9ea85796e9864296bef4c0ff33d174d63dc3b75`.
- **PR #99:** GitHub reports it merged into `work/issue-86-governance-controls-model` at `4fa84e4675f8d62fe725e6dbd3c412c84f3e684a`, not into main. Its head `e9a57ad63f223a2d934e9ec44f272b4684499dbd` compares with main as diverged (48 ahead / 1 behind; merge base `502e43d4ea55a4a5beec07573dab80c69a6796a0`). Architecture 0034 and the journal-recovery model therefore were not in main before the current integration candidate.
- **Open stack:** PR #100 remains open/non-draft, based on `work/issue-86-journal-recovery-model`, head `1be58c4a550cb5041573d704f64ef2baa7701097`; PR #104 remains open/non-draft, based on `work/issue-86-journal-protocol-spec`, head `91edf52fd4fe67815eace4db30f577b50069d53f`.
- **Latest recorded PR #104 validation:** reference-integrity run [42891011411](https://github.com/Martin-PB/govcheck/actions/runs/42891011411) failed with 17 errors / 8 warnings; package alignment and report-only GovCheck checks passed. The reference errors concerned R-142–R-144 thematic indexing/backlinks and bilingual citations, stale [R-107](../references.md#r-107) backlinks, and unlinked portfolio mentions. This candidate repairs those documentary findings. No new Actions run was triggered.
- **Disposition:** factual synchronization and integration preparation only. #41 and #86 remain open; the eleven owner-selected choices remain pending formal normative adoption. No issue closure, adoption, implementation or production enforcement is implied.
- **Related records:** Issues #41/#86; PRs #90/#96/#98/#99/#100/#104; Specifications 0003/0006/0007; Architectures 0023/0031–0034; decision-session record 0008; [R-05](../references.md#r-05), [R-22](../references.md#r-22), [R-142](../references.md#r-142), [R-143](../references.md#r-143) and [R-144](../references.md#r-144).
- **Known limits:** no new TLA+ run, implementation or conformance result is claimed; existing model-checking evidence remains limited to each exact finite model/configuration and its documented assumptions.
