# 0031 — First TLC execution of the governance-applicability model

**Status:** execution record for the proposed [Specification 0006](../specifications/0006-governance-revision-applicability.md). This records model-checking evidence only; it does not adopt the specification or establish implementation conformance. **French:** [0031](0031-first-tlc-governance-applicability.fr.md).

## 1. Purpose

Record the first completed SANY/TLC execution of the separate governance revision applicability model. The model addresses the temporal gap identified by [Architecture 0023](0023-bootstrap-governance-authority.md): the original authority-transition model did not encode effective positions or preserve historical decision applicability.

## 2. Exact subject

- **Repository:** `Martin-PB/govcheck`
- **PR:** [#90 — Specify temporal governance revision applicability](https://github.com/Martin-PB/govcheck/pull/90)
- **Branch:** `work/governance-revision-applicability`
- **Source commit:** `3a8d0176bff8783e25103a4603bb4eea06664cee`
- **PR merge-test commit checked out by the runner:** `e226461` (merge of the source commit into base `d04a6dd02d5bdda0b40e4aa740475a8e554e63d7`)
- **Model:** `formal/tla/GovCheckGovernanceApplicability.tla`
- **Model blob SHA:** `43743eac208f9faf9a844ae35c55ceb6e2b74239`
- **Configuration:** `formal/tla/GovCheckGovernanceApplicability.cfg`
- **Configuration blob SHA:** `54d7387bfe577c5bd9152c7427fc5410c4a00db2`
- **Workflow:** [TLC — governance revision applicability model](https://github.com/Martin-PB/govcheck/actions/runs/42659943881)
- **Job:** `129308483397`
- **Artifact:** [SANY/TLC report and tool checksum](https://github.com/Martin-PB/govcheck/actions/runs/42659943881/artifacts/13693473469)

## 3. Toolchain and configuration

- SANY: version 2.1 (24 February 2014).
- TLC: version 2.19 (8 August 2024, revision `5a47802`).
- Java: Temurin 17.0.21+9.
- tla2tools: pinned v1.7.4; SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`.
- TLC workers: 4.
- Configuration: 2 principals, 3 governance revisions, 2 candidates, 3 evaluation IDs, 3 decision IDs, history bound 3; genesis revision `gov0`, root principal `alice`.

The finite configuration permits at most two governance amendments after genesis and at most three evaluation/decision records. The actors and revisions are abstract model values, not production identities.

## 4. Result

<badge>Model checked — finite configuration</badge>

- SANY parsing and semantic processing completed successfully.
- TLC completed with: **“Model checking completed. No error has been found.”**
- **20,785 states generated; 18,067 distinct states; 0 states left on queue.**
- The configured invariants and temporal property `AppendOnly` completed without a counterexample.

The checked invariants cover type correctness, unique governance revisions, predecessor/effective-position continuity, authorization by the authority applicable at the decision position, use of the applicable prior governance revision, no self-authorization, publication strictly after authorization, preservation of historical decision bindings, and evaluation-to-decision binding. The temporal property checks prefix preservation of governance and decision histories.

## 5. Final PR-head revalidation

The final PR head was checked again after the evidence record and portfolio journal were added, and the run below is the latest recorded revalidation:

- **Final source commit:** `ff4a1457335d7a2600f2bb12850b74926ba6304b`.
- **Merge-test commit:** `7cd7732` (merged with base `d04a6dd02d5bdda0b40e4aa740475a8e554e63d7`).
- **Workflow/job:** [run 42660448408](https://github.com/Martin-PB/govcheck/actions/runs/42660448408), job `129310275465`.
- **Result:** SANY and TLC passed again with the same complete finite state-space result: 20,785 generated, 18,067 distinct, 0 remaining; no error found.
- **Artifact:** [final-head TLC report](https://github.com/Martin-PB/govcheck/actions/runs/42660448408/artifacts/13694860086).

The original successful execution below remains the first recorded run. This revalidation binds the same model/configuration blobs to the final PR candidate.

## 6. Failed first attempt and correction

The first TLC attempt on source commit `eba2a74ec790c013e65f4301a203063d22885943` failed after SANY succeeded. TLC exposed a model-expression defect: a `CHOOSE` expression selected an evaluation/decision index, but the model then attempted to read a record field directly from that integer. The model was corrected to index the corresponding sequence explicitly. The successful execution above checks the corrected source commit `3a8d0176...`.

This correction is preserved in branch history; the failed run is not represented as a passing result.

## 7. Interpretation and limits

This is **model-checking evidence**, not a theorem proof. It establishes that TLC explored the complete reachable state graph of this finite model/configuration without finding a violation of the configured properties. It does not prove:
- correctness for unbounded histories, principal sets, candidates or governance revisions;
- cryptographic authenticity, secure key custody or identity binding;
- distributed consensus or fault-tolerant event ordering;
- full multi-writer concurrency, interruption recovery or every revocation/exception lifecycle;
- refinement or conformance of a future implementation;
- non-bypassable enforcement by Git, Pijul, a forge or a deployment boundary;
- correctness or adoption of the normative policy itself.

The model deliberately holds the root authority constant. Authority succession/delegation and emergency recovery require separate decisions and extensions. The canonical event-order mechanism and persistent publication protocol also remain open.

## 8. Related records

- [Specification 0006 — Governance revision applicability](../specifications/0006-governance-revision-applicability.md)
- [Specification 0003 — Change lifecycle](../specifications/0003-change-lifecycle.md)
- [Architecture 0023 — Bootstrap governance authority](0023-bootstrap-governance-authority.md)
- [Issue #86 — Technical specification work](https://github.com/Martin-PB/govcheck/issues/86)
- [Issue #41 — Parent authority decision](https://github.com/Martin-PB/govcheck/issues/41)


## Subsequent authority arbitration record

The project owner's eleven selections for issue #41 are recorded in [Decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md). They do not retroactively expand the model checked for this report or change its recorded result. The additional selected properties and the model's remaining coverage gaps are enumerated in that session record and in Specification 0006 §7. No new TLC run is claimed here.
