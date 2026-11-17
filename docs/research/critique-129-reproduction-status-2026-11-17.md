# Reproduction status of external critique #129 — 2026-11-17

**Audit target:** `main` at `f27697dac4ceaa6245b6cd796646d7040b12c9b5`  
**Tree:** `3604f0e10765afebef6ea7308f94b488247ba8a8`  
**Parent work item:** [Issue #130](https://github.com/Martin-PB/govcheck/issues/130)  
**Source critique:** [Issue #129](https://github.com/Martin-PB/govcheck/issues/129)

## 1. Scope and evidence classes

This report separates:

1. direct source inspection of the exact `main` tree above;
2. historical GitHub Actions evidence from PR #133's head commit `15372f5ca90f5b454a2ff30fa0c0b0fdddab1639` (not the audit target);
3. independent local reproduction, which has **not** been completed.

No GitHub Actions workflow was triggered for this report. The historical PR checks below were already present and were read without rerunning them. No claim is made that a historical PR result verifies the current `main` tree.

## 2. Current-main source findings

| Critique item | Current qualification | Source evidence |
|---|---|---|
| 6.1 Canonical executable model | **Confirmed as a current implementation gap.** Specification 0002 still says it is a proposed architecture and explicitly says no schema or evaluator is implemented. Its guarantees are targets, not operational guarantees. | `docs/specifications/0002-canonical-governance-model.md`, line 3 and line 60. |
| 6.2 Canonical journal | **Partially confirmed; critique needs qualification.** Specification 0007 now defines a detailed technology-neutral semantic contract for append, compare-and-append, durable commit, crash recovery, idempotent retry, replica observation and VCS reconciliation. It explicitly remains proposed, not adopted and not implemented. | `docs/specifications/0007-canonical-governance-journal-protocol.md`, lines 3, 7, 11, 68–87. |
| 6.3 Authority / separation of duties | **Partially confirmed.** The governance-authority design distinguishes normative authorization from technical evaluation/review and execution, but it does not guarantee a two-person separation in every deployment; a single root principal remains an explicit bootstrap trust assumption. Do not describe optional independent review as a universal two-person rule. | `docs/architecture/0023-bootstrap-governance-authority.md`; see also the [source-level triage](critique-129-source-triage.md). |
| 6.4 Independent-review attestation | **Confirmed as a structural weakness in the current executable slice.** `rule_independent_review` reads `docs/attestations/*.json`, compares the record's `candidate_rev` with the exact candidate SHA, and compares a free-form `reviewer` string with the Git author string. The attestation is read from the candidate tree itself. A file embedded in a commit cannot ordinarily contain the SHA of that same containing commit without a self-reference/fixed-point problem. The string comparison does not authenticate the reviewer. | `govcheck/check.py`, lines 282–299; candidate SHA and author are populated at lines 385–393. |
| 6.5 CI acceptance enforcement | **Confirmed.** The GovCheck check-slice workflow is explicitly report-only. Unit tests are blocking, but the evaluator step has `continue-on-error: true` and ends with `|| true`. A fail-closed evaluator is therefore not, by itself, a CI acceptance gate. | `.github/workflows/govcheck-check.yml`, lines 1, 37–42. |
| 6.6 Partial semantic mapping | **Confirmed.** `SemanticBridge.partialMapping` accepts a predicate `domain : source → Prop` and proves the target only for members of that domain. It does not require any source member to inhabit the domain. For example, with source `True`, target `False`, and domain `fun _ => False`, the constructor obligation is vacuously satisfied. This is not a derivation of False from True; it is a mapping with no covered source case. | `formal/lean/GovCheckCoherence/Mapping.lean`, lines 63–66. |
| 6.7 Physical journal separation | **Critique's physical-infrastructure claim is not supported by the current specification.** Specification 0007 separates evaluation, authorization and publication as logical acts, while allowing them to execute in one atomic technical transaction. It specifies durable append as the commit point but does not mandate a separate database or service. | `docs/specifications/0007-canonical-governance-journal-protocol.md`, lines 68–72 and 84–96. |

### Minimal counterexample for 6.6

The constructor accepts:

`SemanticBridge.partialMapping (source := True) (target := False) (domain := fun _ => False) (by intro h hd; exact False.elim hd)`

The second argument is valid because there is no `h : True` for which the declared domain holds. A non-vacuity witness such as `∃ h, domain h` is currently absent. Whether every partial mapping must be non-empty is a contract decision; the current type does not express that condition.

### Attestation identity and revision

The current record format conflates three different concerns:

- **revision binding:** which exact candidate is reviewed;
- **reviewer authentication:** who made the review assertion;
- **attestation transport/storage:** how the assertion is associated with the candidate without requiring the candidate to contain its own final commit identifier.

The current code checks only a string-level approximation of the first two and stores the record in the candidate tree. A detached/signed attestation, forge-native review identity, or separately governed attestation object could address the cycle, but choosing one is an architecture decision and is not silently made here.

## 3. Existing checks on the exact audit target `main`

GitHub already has three push-triggered checks attached to the exact audit commit `f27697dac4ceaa6245b6cd796646d7040b12c9b5` (2026-11-14). These were read from the existing records; they were not rerun for this report.

| Check | Result | Interpretation |
|---|---|---|
| Reference integrity | **PASS — 0 warnings** | The central catalogue/backlink checker passed on this exact `main` commit. |
| Package alignment | **success** | The manifest-declared package/template alignment check passed. |
| GovCheck check slice | **job success**, with **84 unit tests passed** | The blocking unit-test suite passed. However, the evaluator's JSON/stdout says **overall FAIL** because it does not recognize a qualifying References section in six decision/dossier files. This is partly a validator false negative: the 0008 and 0009 documents already contain relevant catalogue links in traceability/header material but not under a recognized heading; the metamodel dossier has a numbered `## 17. References` heading, but the checker accepts only unnumbered headings and stops that section before the separate source-link subsection. The step is report-only (`continue-on-error` and `|| true`), so the workflow's successful conclusion does not mean the candidate passed the evaluator. |

The six documents reported by the evaluator are:

- `0008-governance-applicability-arbitration-session.md` and its French counterpart;
- `0009-intent-record-and-authority.md` and its French counterpart;
- `metamodel-design-dossier.md` and its French counterpart.

**Qualification:** the six findings are failures of the current evaluator's section-recognition rule, not six documents devoid of sources. The 0008 records have the relevant catalogue links in their traceability section; the 0009 ADRs have them in their References metadata line. The metamodel dossier already has `## 17. References`, but the checker rejects numbered headings and the actual catalogue links sit under the following `## Complete source-catalogue links` heading. A correction branch now handles numbered headings and makes the existing sources visible to the rule; see Section 6.

Existing run records:

- [Reference integrity on the audit commit](https://github.com/Martin-PB/govcheck/actions/runs/43591371080/job/132436604521)
- [GovCheck check slice on the audit commit](https://github.com/Martin-PB/govcheck/actions/runs/43591371057/job/132436604528)
- [Package alignment on the audit commit](https://github.com/Martin-PB/govcheck/actions/runs/43591371071/job/132436604617)

The exact-main check set contains no Lean or TLC check run. The historical PR #133 results below must not be substituted for those missing checks.
## 4. Historical checks on PR #133 (not current-main verification)

The following checks were already present for PR #133 head `15372f5ca90f5b454a2ff30fa0c0b0fdddab1639`. They ran on 2026-11-14 and are reported only as evidence about that PR revision.

| Check | Result | Interpretation |
|---|---|---|
| Python unit tests in `govcheck-check` | **90 passed** | The blocking unit-test step passed on the PR merge checkout. |
| GovCheck evaluator in the same job | **overall FAIL**, while job conclusion was success | Six decision/dossier documents lacked a References section. The report-only step swallowed the evaluator's nonzero exit, confirming the enforcement gap in 6.5. |
| Version-governance validator | **13 passed** | This is a focused validator suite, not the full #130 reproduction. |
| Lean coherence | **job success** | The configured axiom audit passed its policy. The log also reports `propext` for several SACM declarations; therefore this must not be paraphrased as “the entire Lean development is axiom-free”. |
| Package alignment | **success** | Package/template alignment check passed on the PR checkout. |
| Pinned OMG source capture | **success** | Source capture/digest check passed on the PR checkout. |
| Reference integrity | **failure** | The checker crashed with `ValueError`: `formal/lean/README.md` is outside `docs/`, but `logical_doc` calls `path.relative_to(DOCS)` while resolving a catalogue backlink. |

Relevant historical runs:

- [Reference-integrity failure](https://github.com/Martin-PB/govcheck/actions/runs/43587576876/job/132425268063)
- [Python unit tests and report-only evaluator](https://github.com/Martin-PB/govcheck/actions/runs/43587576725/job/132425267482)
- [Lean coherence and axiom report](https://github.com/Martin-PB/govcheck/actions/runs/43587576783/job/132425267822)
- [Version-governance validator](https://github.com/Martin-PB/govcheck/actions/runs/43587576734/job/132425267700)
- [Package alignment](https://github.com/Martin-PB/govcheck/actions/runs/43587576727/job/132425267693)
- [OMG source capture](https://github.com/Martin-PB/govcheck/actions/runs/43587576732/job/132425267619)

No TLC run for the eight current TLA+ model/configuration pairs was part of these six PR #133 checks. The PR's changed paths did not establish fresh model-checking evidence for the audit target.

## 5. Formal limits that remain

1. **Safety versus liveness:** invariants and bounded state exploration do not, without suitable fairness and environmental assumptions, establish eventual progress or availability.
2. **Separate TLA+ slices:** the journal, lifecycle, authority, assurance, governance-applicability/control and CI-routing models are separate bounded design models. Specification 0007 itself says they are composable design evidence, not one integrated implementation model. No end-to-end refinement relation to the Python checker or a production runtime is established.
3. **Lean theorem strength:** the generic theorem `kind_mapping_rule_theorem_proof_requires_derivation` concludes that a derivation exists with `derivation.proof = derivation.proof`. That equality is reflexive; the useful content is the existential witness carried by the constructor. The theorem does not independently establish a further semantic property of the derivation. Names and claims must remain aligned with the actual proposition.
4. **Executable scope:** the current `govcheck/check.py` has eight rules for licence presence, bilingual decisions, manifest pairs, reference integrity, source presence, bootstrap integrity, TLA evidence freshness and independent-review attestation. It does not implement the canonical lifecycle, authority registry, journal protocol, risk/decision semantics or the full cross-model assurance contracts.


### Current TLA+ model/configuration inventory (source-level only)

The current tree contains eight `.tla`/`.cfg` pairs. The reusable workflow pins TLA+ tools 1.7.4 by SHA-256 and uses Java 17, runs SANY before TLC, and records model output as an artifact. The model-specific workflows route the eight pairs through five workflow entry points (CI routing, assurance, authority, governance applicability/control/publication/recovery, and lifecycle).

| Model | Finite configuration | Checked properties named in the config |
|---|---|---|
| `CICheckRouting` | 15 change categories; routing policy only | TypeOK; no unrelated-doc trigger; lifecycle/assurance/authority isolation; shared-runner invalidation; per-model coverage. |
| `GovCheckAssurance` | 2 claims, 2 evidence items, 2 dependencies, 2 versions, 2 actors; `MaxTime=2` | 7 invariants for graph well-formedness, review binding, claim soundness, acceptance support/snapshot and revocation; temporal `AcceptedDiscipline`. |
| `GovCheckAuthority` | 2 principals, 3 revisions; history limit 4 | TypeOK; current-authority amendment, continuous chain, no revision reuse; `HistoryIsAppendOnly`. |
| `GovCheckCanonicalPublication` | 2 principals, 3 governance revisions, 2 candidates, 3 evaluation IDs and 3 authorization IDs | TypeOK; unique revisions, predecessor continuity, one publication per position, evaluation/authorization binding, effect point, authorization and stale-publication checks; `AppendOnly`. |
| `GovCheckGovernanceApplicability` | 2 principals, 3 governance revisions, 2 candidates, 3 evaluations and 3 decisions; history limit 3 | TypeOK; unique/continuous governance history, applicable authority, prior-governance decision, no self-authorization, publication authorization, historical binding and evaluation/authorization binding; `AppendOnly`. |
| `GovCheckGovernanceControls` | 3 principals, 2 revisions, 2 candidate contents, 1 evaluation, 1 authorization, 1 exception | TypeOK; revision uniqueness, prior authority, shadow evaluator restriction, unknown/conflict blocking, non-derogability, prospective revocation, historical preservation and stale-authorization checks; `AppendOnly`. |
| `GovCheckJournalRecovery` | 2 contents, 2 revision IDs, 2 event IDs, `MaxEvents=2`, Git and Pijul replicas | TypeOK; unique event/revision IDs, position/predecessor continuity, rollback as a new event, non-authoritative VCS observation and durable applied state; `AppendOnly`. |
| `GovCheckLifecycle` | 2 actors, 1 required approval, history limit 12; 2 bases, candidates, governance revisions and specs; 2 obligation kinds | 12 invariants for type, acceptance/application soundness, freshness, evidence/outcome/approval binding, no implicit application and deadlock discipline; temporal `TerminalDiscipline`. |

Fairness inspection adds an important qualification: only `GovCheckJournalRecovery` explicitly adds `WF_vars(Recover)`; the other seven `Spec` definitions use `Init /\ [][Next]_vars` without explicit `WF_` or `SF_` assumptions. Consequently, the configured temporal properties should not be paraphrased as general progress guarantees for actions that have no fairness assumption. This inventory establishes that configurations and named checks exist; it does **not** establish that SANY/TLC ran successfully on the audit SHA, that bounds are adequate, or that the models refine one another or the Python implementation. The exact-main check-run set has no TLC result, so all eight remain to be reproduced under #130.

## 6. Corrections staged for the two verifier findings

### 6.1 PR #133 reference-check failure

A separate branch, [`work/fix-reference-integrity-repo-wide-markdown`](https://github.com/Martin-PB/govcheck/tree/work/fix-reference-integrity-repo-wide-markdown), was created from PR #133's head. It contains:

- repository-relative Markdown identity, so backlinks to `formal/lean/README.md` no longer raise `ValueError`;
- repository-wide authored Markdown discovery, excluding the installed `govcheck/` package mirror and generated/cache trees, so external source documents are included in reciprocal-citation accounting;
- five regression tests, including an end-to-end temporary-repository fixture that checks an external formal-document backlink through the catalogue validator.

This correction is **staged but not executed**. It has not been merged into PR #133 and no Actions workflow was triggered. The branch is based on PR #133's old head, not current `main`; integration must first account for the PR's divergence from the current base. No green status is claimed.


### 6.2 Current-main evaluator source-reference recognition

A second branch, [`work/fix-govcheck-sources-present-rule`](https://github.com/Martin-PB/govcheck/tree/work/fix-govcheck-sources-present-rule), is based on current `main` and addresses the report-only evaluator's six source-section findings:

- accept numbered Markdown headings such as `## 17. References` as References sections;
- add explicit catalogue-backed References sections to the 0008 and 0009 EN/FR decision records, reusing their existing R-05/R-22/R-194–R-196 and R-114–R-122 sources;
- keep the metamodel dossier's existing complete catalogue-link list inside its numbered References section by making the following heading a subheading;
- add a regression test for a numbered References heading.

The exact regex was sanity-checked locally against five heading forms (unnumbered and numbered English/French); this is **not** a run of the repository test suite. The branch has not been executed as a full candidate, has not been merged and has not triggered Actions.

## 7. Remaining reproduction work

The deliverable requested by #130 is not complete. Still required:

- obtain a local checkout of the exact audit target and record the actual Git tree, Python, Java, TLC and Lean tool versions;
- run the complete Python suite against current `main`, not merely rely on the historical PR #133 run;
- run SANY/TLC for all eight model/configuration pairs, recording tool checksum, Java version, states, bounds, invariants and temporal properties;
- build and audit the pinned Lean 4.19.0 package against the exact current formal source; inspect the full axiom report, not only the configured root;
- separately build and inspect `formal/cslib-compat` with its pinned Lean 4.36.0-rc2 toolchain;
- add executable regression tests for attestation revision/authentication and partial-mapping non-vacuity once the intended contract is decided;
- classify remaining critique claims only after those reproductions.

**Execution status for this report:** source inspection and reading existing GitHub check records only. No local test, TLC run, Lean build, axiom audit or new Actions run was performed. No Actions credits were consumed.

## 8. Disposition

The critique is neither accepted wholesale nor dismissed. The current source supports several material implementation/enforcement gaps; other claims require qualification. The journal specification improves the logical protocol definition but does not implement it. The SACM/Lean work provides useful formalized slices, but it does not close the repository-wide metamodel, parser-refinement or runtime-conformance obligations.

No normative specification, architecture decision, formal model or acceptance policy was changed by this audit.
