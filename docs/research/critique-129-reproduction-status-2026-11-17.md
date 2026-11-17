# Reproduction status of external critique #129 — 2026-11-17

**Audit target:** `main` at `f27697dac4ceaa6245b6cd796646d7040b12c9b5`  
**Tree:** `3604f0e10765afebef6ea7308f94b488247ba8a8`  
**Parent work item:** [Issue #130](https://github.com/Martin-PB/govcheck/issues/130)  
**Source critique:** [Issue #129](https://github.com/Martin-PB/govcheck/issues/129)

## 1. Scope and evidence classes

This report separates:

1. direct source inspection of the exact `main` tree above;
2. historical GitHub Actions evidence from PR #133's head commit `15372f5ca90f5b454a2ff30fa0c0b0fdddab1639` (not the audit target);
3. a hosted, independent GitHub Actions reproduction on updated `main` after PRs #134 and #135 merged (current `main`: `8e86027297e2d4259403a48842787851e10c9b08`), executed on PR #138's merge checkout `fbbff897bd20d7cecadb9801f1da78d50dda541a` (PR head `1535cc078be3d97592ab94bd48db0688e93d607c`). That checkout adds only the audit workflow and its meta-only package-alignment declaration; it does not change the formal models or runtime implementation under test;
4. local reproduction, which remains **not performed** because this runtime has no repository checkout/toolchains and cannot resolve GitHub DNS.

The historical PR checks below remain historical evidence only. The current-main hosted reproduction is documented in Section 9 and is bound to its exact merge commit. It is not a local reproduction and does not establish refinement from the TLA+ models to the Python checker or a production runtime.

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
| GovCheck evaluator in the same job | **overall FAIL**, while job conclusion was success | The evaluator failed to recognize a qualifying References section in six decision/dossier documents (see the section-recognition qualification above). The report-only step swallowed the evaluator's nonzero exit, confirming the enforcement gap in 6.5. |
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


### Last observed successful TLC executions (historical, not the audit SHA)

All eight configured model pairs have at least one historical successful TLC run in the main-branch workflow history. The logs report TLC 2.19 (revision `5a47802`), Java 17.0.21+9, “Model checking completed. No error has been found”, and zero states left on the queue. The state counts below are **generated / distinct**:

| Model | Run date and source commit | Generated / distinct states | Existing run |
|---|---|---:|---|
| `CICheckRouting` | 2026-11-08, `0f3e402d` | 65,536 / 32,768 | [TLC routing](https://github.com/Martin-PB/govcheck/actions/runs/42486714556) |
| `GovCheckAssurance` | 2026-11-08, `0f3e402d` | 11,069,137 / 347,424 | [TLC assurance](https://github.com/Martin-PB/govcheck/actions/runs/42486714637) |
| `GovCheckLifecycle` | 2026-11-08, `0f3e402d` | 132,412,944 / 24,922,992 | [TLC lifecycle](https://github.com/Martin-PB/govcheck/actions/runs/42486714619) |
| `GovCheckAuthority` | 2026-11-10, `934000a7` | 13 / 13 | [TLC authority](https://github.com/Martin-PB/govcheck/actions/runs/42816437925) |
| `GovCheckGovernanceApplicability` | 2026-11-13, `6c70d4f1` | 20,785 / 18,067 | [TLC applicability workflow](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |
| `GovCheckCanonicalPublication` | 2026-11-13, `6c70d4f1` | 178,549 / 38,434 | [TLC publication workflow](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |
| `GovCheckGovernanceControls` | 2026-11-13, `6c70d4f1` | 2,826,117 / 1,026,484 | [TLC controls workflow](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |
| `GovCheckJournalRecovery` | 2026-11-13, `6c70d4f1` | 84,307 / 56,895 | [TLC journal-recovery workflow](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |

This is meaningful historical model-checking evidence and is stronger than merely having configuration files. It is nevertheless attached to three earlier source revisions, not `f27697d`; it does not show that the exact current models/configurations were checked, and it does not establish implementation refinement or global assurance.


### Last observed Lean and CSLib builds (historical)

- **Lean coherence:** successful on 2026-11-13 at commit `2ae091f5` ([run](https://github.com/Martin-PB/govcheck/actions/runs/43442307871)). The log installs Lean 4.19.0, reports `lake build` success, and audits 36 declarations under `GovCheckCoherence.Proofs` against the configured allowlist `propext, Classical.choice, Quot.sound`. This is evidence for that source revision and that audit root/allowlist, not a whole-repository axiom-freedom claim.
- **CSLib compatibility:** successful on 2026-11-12 at commit `056203bf` ([run](https://github.com/Martin-PB/govcheck/actions/runs/43243377685)). The isolated `CslibCompat` package built with Lean 4.36.0-rc2 against CSLib `70e25828` and Mathlib `887bb849` (1779 build jobs). This establishes API/build compatibility for the probe, not a semantic refinement proof between GovCheck and CSLib.
- **PR #133 Lean extension:** the PR-head run on 2026-11-14 also succeeded ([run](https://github.com/Martin-PB/govcheck/actions/runs/43587576783)); its axiom output includes `propext` on some SACM source-fact declarations under the configured allowlist. It is not a build of current `main`.

No Lean or CSLib check is attached to the exact audit commit `f27697d`. These historical runs must not be conflated with reproduction on that target.

Fairness inspection adds an important qualification: only `GovCheckJournalRecovery` explicitly adds `WF_vars(Recover)`; the other seven `Spec` definitions use `Init /\ [][Next]_vars` without explicit `WF_` or `SF_` assumptions. Consequently, the configured temporal properties should not be paraphrased as general progress guarantees for actions that have no fairness assumption.

**Workflow path-filter finding:** `.github/workflows/ci-routing-model.yml` includes `.github/workflows/tla-model-reusable.yml` in its `pull_request.paths`, but omits it from `push.paths`. A direct push to `main` that changes the shared TLC runner therefore does not trigger the `CICheckRouting` model, although the other model entry workflows include the reusable workflow in both path filters. This is a narrow coverage gap, not evidence that the model itself is wrong. A one-line correction is staged on [`work/fix-ci-routing-reusable-push-trigger`](https://github.com/Martin-PB/govcheck/tree/work/fix-ci-routing-reusable-push-trigger); it has not been run or merged.

This inventory establishes that configurations and named checks exist; it does **not** establish that bounds are adequate, or that the models refine one another or the Python implementation. The eight models have now been reproduced on the updated-main merge checkout documented in Section 9; the finite bounds and absence of cross-model/runtime refinement remain limitations.

## 6. Corrections staged for the two verifier findings

### 6.1 PR #133 reference-check failure — corrected and merged

PR [#134](https://github.com/Martin-PB/govcheck/pull/134) was merged on 2026-11-17 as commit `f435128d1a8bab5684b6c55d025e52050437366d`. It gives authored Markdown documents repository-root-relative identities, scans authored Markdown repository-wide while excluding package/cache trees, applies the EN/FR counterpart/fallback rule, and adds regression coverage. The reference-integrity workflow and full Python suite passed after correcting a faulty negative-test assertion. The fix is now part of current `main`.

### 6.2 Current-main evaluator source-reference recognition — corrected and merged

PR [#135](https://github.com/Martin-PB/govcheck/pull/135) was merged on 2026-11-17 as current-main commit `8e86027297e2d4259403a48842787851e10c9b08`. It recognizes numbered References headings, adds explicit catalogue-backed sections to the 0008/0009 EN/FR records, keeps the metamodel dossier's catalogue links inside its numbered References section, and adds a regression test. The reference-integrity, package-alignment and GovCheck check-slice workflows passed. The six earlier false negatives are gone. The evaluator's overall result on the updated-main audit checkout is `UNKNOWN`, not `PASS`, because no independent-review attestation is present; this is a separate unresolved condition, and the workflow remains report-only.

## 7. Remaining work and open limitations

The independent hosted reproduction is now complete for the current-main source snapshot (Section 9). Remaining work:

- **Attestation (6.4):** design and test non-circular candidate-revision binding and authenticated reviewer identity. No storage/signature/forge-native architecture is selected.
- **Partial mappings (6.6):** PR [#137](https://github.com/Martin-PB/govcheck/pull/137) adds a kernel-checked counterexample proving that the current constructor admits an empty domain, and strengthens theorem-proof mapping to require an inhabited `KernelCheckedDerivation`. Its Lean build and axiom audit pass (37 declarations under the configured allowlist; the explicit report includes the counterexample with no axiom dependencies). The PR is not yet merged. Whether empty partial mappings should be rejected remains a contract decision.
- **Cross-model refinement:** the eight TLA+ models remain separate bounded specifications; no integrated refinement proof connects lifecycle, authority, assurance, governance applicability, journal recovery and the Python implementation.
- **Local reproduction:** hosted Actions reproduction is complete, but a separate local replay was not performed in this environment.
- **Workflow maintainability:** PR [#138](https://github.com/Martin-PB/govcheck/pull/138) adds the reusable end-to-end audit workflow; all checks are green and it remains open for review/merge.

Do not turn these findings into normative policy without an explicit decision by the competent GovCheck authority.

## 8. Disposition

The critique is neither accepted wholesale nor dismissed. The current source supports several material implementation/enforcement gaps; other claims require qualification. The journal specification improves the logical protocol definition but does not implement it. The SACM/Lean work provides useful formalized slices, but it does not close the obligations of global metamodel coherence, parser refinement or runtime conformance.

The hosted reproduction confirms that all eight current TLA+ configurations complete without a TLC counterexample on the updated-main merge checkout, and that the current Lean and CSLib packages build under their separate pinned toolchains. These results do not prove the adequacy of finite bounds, correctness of the abstractions, cross-model refinement or implementation conformance.

No normative specification, architecture decision, formal model or acceptance policy was changed by this audit.

## 9. Independent hosted reproduction on updated `main` — 2026-11-17

### Exact source and runner identity

- Current `main` before the audit PR: `8e86027297e2d4259403a48842787851e10c9b08` (after #134 and #135 merged).
- PR #138 head: `1535cc078be3d97592ab94bd48db0688e93d607c`.
- Exact PR merge checkout: `fbbff897bd20d7cecadb9801f1da78d50dda541a`.
- Full audit: [run 44110921001](https://github.com/Martin-PB/govcheck/actions/runs/44110921001) — **success**.
- GovCheck report-only: [run 44110920731](https://github.com/Martin-PB/govcheck/actions/runs/44110920731) — **success**.
- Package alignment: [run 44110920743](https://github.com/Martin-PB/govcheck/actions/runs/44110920743) — **success**.

The audit PR adds only orchestration and a meta-only workflow declaration; it does not change the formal models or runtime code under test.

### Python and repository checks

| Check | Result |
|---|---|
| Runtime | CPython 3.12.16; Git 2.56.1 |
| Complete Python suite | **91 passed** |
| Repository-wide reference integrity | **PASS — 0 warnings** |
| Package alignment | **PASS** |
| GovCheck check-slice tests | **91 passed** |
| GovCheck evaluator | **overall UNKNOWN**: applicable rules PASS except `independent-review`, UNKNOWN because no independent-review attestation is present |

The evaluator's `UNKNOWN` is not a unit-test failure. Its fail-closed result is preserved, but the workflow remains report-only and is not an acceptance gate. The six earlier source-section false negatives are gone after #135.

### Eight TLA+ model/configuration pairs

All eight SANY parses and TLC runs completed successfully. Each reported “Model checking completed. No error has been found” and zero states left on the queue. Tool identity: TLA+ tools 1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`; TLC 2.19 (revision `5a47802`); Temurin Java 17.0.21+9. Counts are **generated / distinct**:

| Model | Generated / distinct states |
|---|---:|
| `CICheckRouting` | 65,536 / 32,768 |
| `GovCheckAssurance` | 11,069,137 / 347,424 |
| `GovCheckAuthority` | 13 / 13 |
| `GovCheckGovernanceApplicability` | 20,785 / 18,067 |
| `GovCheckCanonicalPublication` | 84,307 / 56,895 |
| `GovCheckGovernanceControls` | 2,826,117 / 1,026,484 |
| `GovCheckJournalRecovery` | 178,549 / 38,434 |
| `GovCheckLifecycle` | 132,412,944 / 24,922,992 (4m15s) |

These are bounded results for the exact finite configurations and merge-checkout source. They do not prove unbounded behavior, bound adequacy, general liveness beyond explicit fairness assumptions, or refinement to the Python implementation.

### Lean 4.19 coherence slice

- Lean 4.19.0, commit `6caaee842e94`; `lake build` succeeded.
- Configured axiom audit: **36 declarations** under `GovCheckCoherence.Proofs`, all within `propext, Classical.choice, Quot.sound`.
- Explicit `AxiomReport.lean`: 42 declarations printed with no axiom dependencies.
- Run: [44110921001](https://github.com/Martin-PB/govcheck/actions/runs/44110921001).

This applies only to the declared package, proof root and allowlist; it is not a whole-repository axiom-freedom claim or implementation-conformance proof.

### Isolated CSLib compatibility probe

- Lean 4.36.0-rc2, commit `b35cb10cf2ced51a2fd1880cfdbf75c71ab7a35a`.
- CSLib `70e25828d89a3916e41c9d84cfffd7e6093bb1a0`; Mathlib `887bb849a9f64e1c66499fd5ff8523c864e78941`.
- `lake build CslibCompat` succeeded (**1,779 build jobs**).
- Non-blocking warning: `lakefile.lean:6` uses unrecognized `PackageConfig.defaultTargets`; explicit target build nevertheless succeeded.
- Run: [44110921001](https://github.com/Martin-PB/govcheck/actions/runs/44110921001).

This establishes build/API compatibility for the isolated probe, not semantic refinement between GovCheck and CSLib.

### Historical state-count correction and follow-up

The independent run confirms the 2026-11-13 historical counts had been transposed between `GovCheckCanonicalPublication` and `GovCheckJournalRecovery`; the historical table above is corrected.

PR [#137](https://github.com/Martin-PB/govcheck/pull/137) adds a kernel-checked counterexample for vacuous partial mappings and strengthens the theorem-proof mapping proposition. Its latest Lean 4.19 build and axiom audit passed: [run 44111542642](https://github.com/Martin-PB/govcheck/actions/runs/44111542642). It remains open for review/merge and does not change current-main mapping semantics.

PR [#138](https://github.com/Martin-PB/govcheck/pull/138) supplies the reusable audit workflow; all checks are green and it remains open for review/merge.
