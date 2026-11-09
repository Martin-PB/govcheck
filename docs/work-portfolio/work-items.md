# GovCheck work-item register

**Status:** initial import for maintainer review. Imported items are candidates unless explicitly stated otherwise. This repository register is canonical; GitHub issue numbers are adapter mappings and historical provenance. Stable IDs use the form govcheck.work.<slug> and are never recycled.

## Portfolio structure

| Portfolio ID | Domain | GitHub coordination view |
|---|---|---|
| govcheck.portfolio.governance | Governance, authority, decisions | [#78](https://github.com/Martin-PB/govcheck/issues/78) |
| govcheck.portfolio.assurance | Vertical slice, evaluation, assurance | [#79](https://github.com/Martin-PB/govcheck/issues/79) |
| govcheck.portfolio.enforcement | Enforcement, CI, operations | [#80](https://github.com/Martin-PB/govcheck/issues/80) |
| govcheck.portfolio.formal | Formal models and lifecycle | [#81](https://github.com/Martin-PB/govcheck/issues/81) |
| govcheck.portfolio.bootstrap | Bootstrap, package, distribution | [#82](https://github.com/Martin-PB/govcheck/issues/82) |
| govcheck.portfolio.research | References, state of the art, provenance | [#83](https://github.com/Martin-PB/govcheck/issues/83) |
| govcheck.portfolio.collaboration | Multi-agent collaboration and attribution | [#84](https://github.com/Martin-PB/govcheck/issues/84) |
| govcheck.portfolio.quality | Schemas, fixtures, documentation quality | [#85](https://github.com/Martin-PB/govcheck/issues/85) |

Grouping is organizational only; it does not imply dependency, inherited priority, authority, commitment or acceptance.

## Imported work items

Source issue descriptions and discussions remain preserved on GitHub and are linked as provenance. This register captures stable identity, intended outcome, classification and disposition. The issue remains a coordination adapter during transition. Priority/stage reproduce the source issue's declaration at import and do not confer authority.

| Stable work ID | Source | Intended outcome | Nature / domain | Priority / stage | Disposition |
|---|---:|---|---|---|---|
| govcheck.work.governance-revision-applicability | [#41](https://github.com/Martin-PB/govcheck/issues/41) | Decide which governance revision evaluates a candidate changing governance itself; prevent self-authorization. | decision / governance | P0, needs-decision | Parent decision track for #86; root-authority decision in Architecture 0023 is not reopened. |
| govcheck.work.minimum-vertical-slice-format | [#42](https://github.com/Martin-PB/govcheck/issues/42) | Decide minimum data format for the first vertical slice without blocking it on a general expression language. | decision / governance-evaluation | P2, needs-decision | Defer general language choice until requirements justify it. |
| govcheck.work.executable-vertical-slice | [#43](https://github.com/Martin-PB/govcheck/issues/43) | Implement local CLI evaluating real repository rules and producing explained pass/fail/unknown. | implementation / evaluation | P1, needs-specification | Depends on #41. |
| govcheck.work.interoperable-attestation | [#44](https://github.com/Martin-PB/govcheck/issues/44) | Produce interoperable attestations bound to candidate, policy, verifier, inputs and result without conflating assurance methods. | implementation / assurance | P2, needs-specification | Evaluate in-toto/SLSA mappings; preserve method limitations. |
| govcheck.work.acceptance-enforcement-boundary | [#45](https://github.com/Martin-PB/govcheck/issues/45) | Demonstrate effective enforcement at the acceptance boundary, including actual forge configuration and bypass limits. | implementation / governance-enforcement | P1, needs-specification | Adapter-neutral; no claim of opposable local controls without evidence. |
| govcheck.work.repository-license-decision | [#46](https://github.com/Martin-PB/govcheck/issues/46) | Choose and record repository license and notices. | decision / governance | P2, completed | Completed by merged PR #39 / ADR 0005 and repository artefacts; close source issue after registry PR acceptance. |
| govcheck.work.fixture-schema-validation | [#47](https://github.com/Martin-PB/govcheck/issues/47) | Validate every JSON fixture against its schema, including expected negative cases. | verification / formal-methods | P2, needs-specification | A claimed-valid fixture must fail when invalid. |
| govcheck.work.fixture-bundle-contract | [#48](https://github.com/Martin-PB/govcheck/issues/48) | Clarify contract between individual records, bundles, manifests and references in fixture validation. | specification / evaluation | P2, needs-specification | Decide supported validation units and explicit error semantics. |
| govcheck.work.package-source-alignment | [#49](https://github.com/Martin-PB/govcheck/issues/49) | Eliminate silent drift between meta-repository source and reusable govcheck/ package. | implementation / bootstrap | P2, needs-specification | Cover trees, manifests, schemas, models, fixtures and workflows. |
| govcheck.work.lifecycle-concurrency-model | [#50](https://github.com/Martin-PB/govcheck/issues/50) | Refine lifecycle model for asynchronous evaluation, stale approvals, revocation and concurrent application. | verification / formal-methods | P1, needs-specification | Preserve bounds/abstraction limits; target specified mutants. |
| govcheck.work.acceptance-invalidation-semantics | [#51](https://github.com/Martin-PB/govcheck/issues/51) | Define invalidation, revocation and historical retention when evidence expires or candidate changes. | decision / assurance | P1, needs-decision | Align Architecture 0021 and lifecycle model; preserve append-only history. |
| govcheck.work.unknown-cause-taxonomy | [#52](https://github.com/Martin-PB/govcheck/issues/52) | Define distinct causes and resolution policies for unknown evaluation results. | specification / evaluation | P2, needs-specification | Unknown must never silently become pass. |
| govcheck.work.durable-model-checking-reports | [#53](https://github.com/Martin-PB/govcheck/issues/53) | Preserve durable, self-contained reports for important model-checking runs. | verification / formal-methods | P2, needs-specification | Bind model/config/tool/bounds/results; do not claim theorem proof. |
| govcheck.work.ci-path-routing-conformance | [#54](https://github.com/Martin-PB/govcheck/issues/54) | Compare actual workflow path filters with CI routing policy and model dependencies. | verification / CI | P2, needs-specification | Locally runnable; no manual Actions triggering required. |
| govcheck.work.aggregate-ci-gate-design | [#55](https://github.com/Martin-PB/govcheck/issues/55) | Design aggregate gate avoiding pending required checks for irrelevant concerns. | design / CI | P2, needs-decision | No hosted workflow execution or Actions spend authorized by this item. |
| govcheck.work.governance-assurance-ecosystem-comparison | [#56](https://github.com/Martin-PB/govcheck/issues/56) | Compare existing governance/assurance mechanisms and identify reusable responsibilities and residual gaps. | research / integrations | P3, needs-evidence | Primary sources; catalogue all sources EN/FR; no aggregator assumption. |
| govcheck.work.openssf-privateer-assessment | [#57](https://github.com/Martin-PB/govcheck/issues/57) | Assess OpenSSF privateerproj as possible compliance integration. | research / integrations | P3, needs-evidence | Keep distinct from privateer-agent; no adoption presumed. |
| govcheck.work.multi-agent-integration-contract | [#58](https://github.com/Martin-PB/govcheck/issues/58) | Specify parallel generation, serialized integration, semantic validation and acceptance guarantees. | specification / integration | P2, needs-specification | Git and Pijul are first-class; textual merge success is not semantic correctness. |
| govcheck.work.producer-provenance | [#59](https://github.com/Martin-PB/govcheck/issues/59) | Record human/agent/mixed production as provenance, never as authorization. | specification / assurance | P3, needs-specification | Bind provenance to exact revision and retain uncertainty. |
| govcheck.work.single-authority-residual-risk | [#60](https://github.com/Martin-PB/govcheck/issues/60) | Make absence of separation of duties visible as residual risk under single-authority regime. | decision / authority | P1, needs-decision | Never claim independent review where none occurred. |
| govcheck.work.existing-repository-bootstrap | [#62](https://github.com/Martin-PB/govcheck/issues/62) | Complete inspect/plan/apply for safe, idempotent adoption and updates in existing repositories. | implementation / bootstrap | P2, needs-specification | Successor to duplicate #61; preserve non-destructive capability selection. |
| govcheck.work.github-portfolio-adapter | [#63](https://github.com/Martin-PB/govcheck/issues/63) | Configure GitHub portfolio views/fields and bounded label taxonomy without making GitHub authoritative. | implementation / portfolio | P2, needs-specification | Preserve identity/history; labels/columns do not imply commitment. |
| govcheck.work.historical-agent-package-manager-identity | [#64](https://github.com/Martin-PB/govcheck/issues/64) | Verify identity of Microsoft Agent Package Manager in historical PDF before cataloguing. | research / references | P3, needs-evidence | Distinguish probable, confirmed and unknown provenance. |
| govcheck.work.historical-epic-acronym | [#65](https://github.com/Martin-PB/govcheck/issues/65) | Resolve exact meaning of EPIC in archived context. | research / references | P3, needs-evidence | Do not choose a homonymous expansion by plausibility. |
| govcheck.work.historical-tarski-reference | [#66](https://github.com/Martin-PB/govcheck/issues/66) | Verify whether Tarski means Alfred Tarski and identify the concept intended. | research / references | P3, needs-evidence | Add reference only if materially relevant. |
| govcheck.work.hosted-ci-authorization-policy | [#67](https://github.com/Martin-PB/govcheck/issues/67) | Record hosted-CI policy and limits, local equivalents and cost boundaries. | decision / CI-operations | unassigned, needs-decision | Authorization record #88 exists; reconcile without inferring broader permission. |
| govcheck.work.rule-verifiability-classification | [#68](https://github.com/Martin-PB/govcheck/issues/68) | Add context-sensitive verifiability dimension independent of method, result and acceptance. | specification / evaluation | P2, needs-specification | Human attestation is not machine proof. |
| govcheck.work.claim-justification-chain | [#69](https://github.com/Martin-PB/govcheck/issues/69) | Preserve methods, assumptions and limits across claims, models, implementation, evidence and decisions. | specification / assurance | P2, needs-specification | Distinguish proof of model claims from differential testing of model-to-code relations. |
| govcheck.work.threat-model-coverage-audit | [#70](https://github.com/Martin-PB/govcheck/issues/70) | Audit Architecture 0006 against concrete attacks; distinguish documented from implemented controls. | audit / security | P2, needs-evidence | Produce coverage matrix; convert only real gaps into work. |
| govcheck.work.threshold-authority-evolution | [#71](https://github.com/Martin-PB/govcheck/issues/71) | Evaluate prospective multiple-principal and threshold/quorum support while preserving single-authority history. | decision / authority | P3, needs-decision | Decide adopt/defer/reject; no retroactive authority changes. |
| govcheck.work.adversarial-candidate-corpus | [#72](https://github.com/Martin-PB/govcheck/issues/72) | Build versioned positive/adversarial candidates for evaluation and acceptance-boundary resistance. | verification / governance | P1, needs-specification | Bind fixtures to exact candidate/base policy; distinguish enforced from tested controls. |
| govcheck.work.intermodel-contract-conformance | [#73](https://github.com/Martin-PB/govcheck/issues/73) | Verify semantic contracts between lifecycle, assurance and authority models. | verification / formal-methods | P2, needs-specification | No refinement claim without demonstration; expose cross-model assumptions. |
| govcheck.work.reference-status-and-provenance | [#74](https://github.com/Martin-PB/govcheck/issues/74) | Make reference status/provenance explicit and machine-checkable with bidirectional links. | verification / references | P2, needs-specification | Reconcile residual after PR #36; do not delete uncited references. |
| govcheck.work.adopt-governed-work-portfolio | [#75](https://github.com/Martin-PB/govcheck/issues/75) | Decide formal adoption of Architecture 0028 and canonical portfolio identity/registry. | decision / portfolio | unassigned, needs-decision | This PR supplies the registry proposal; issue stays open pending authorized adoption. |
| govcheck.work.obsolete-branch-audit | [#76](https://github.com/Martin-PB/govcheck/issues/76) | Audit historical branches and propose only demonstrably safe deletions. | maintenance / operations | P3, needs-evidence | No branch deletion without explicit approval. |
| govcheck.work.architecture-record-justification | [#77](https://github.com/Martin-PB/govcheck/issues/77) | Require traceable, falsifiable rationale and validation limits for new architecture records. | specification / governance | P2, needs-specification | Method depends on claim type; no artificial formal-test mandate. |
| govcheck.work.governance-revision-temporal-applicability | [#86](https://github.com/Martin-PB/govcheck/issues/86) | Bind each evaluation to the immutable governance revision applicable at its decision position. | specification / governance | unassigned, in-progress | Specification 0006 EN/FR and a dedicated bounded TLA+ model/configuration are prepared for review; formal execution and maintainer decision remain pending. #41 remains the parent decision and is not adopted by this technical work. |
| govcheck.work.multilingual-documentation-governance | [#33](https://github.com/Martin-PB/govcheck/issues/33) | Define language primacy, EN/FR synchronization, translation freshness, terminology and safe handling of operational filenames. | specification / governance-documentation | unassigned, needs-specification | Kept atomic; not forced into the former #40 decomposition. |

## Historical and completed mappings

| Source issue | Disposition | Canonical relation |
|---|---|---|
| [#23 — Claude analysis](https://github.com/Martin-PB/govcheck/issues/23) | Closed after triage/transcription | Historical source for #41–#77; recommendations were not automatically adopted. |
| [#26 — Perplexity review](https://github.com/Martin-PB/govcheck/issues/26) | Closed after triage/transcription | Historical source for #41–#77; proposed sequence was not an authorization. |
| [#30 — former work tracker](https://github.com/Martin-PB/govcheck/issues/30) | Closed after consolidation | Historical source for work items and dedicated decisions. |
| [#35 — comprehensive review](https://github.com/Martin-PB/govcheck/issues/35) | Closed after transcription | Historical source for #41–#77. |
| [#37 — provenance clarifications](https://github.com/Martin-PB/govcheck/issues/37) | Closed after transcription | Provenance follow-ups #64–#66. |
| [#61 — existing-repository bootstrap](https://github.com/Martin-PB/govcheck/issues/61) | Closed duplicate/superseded | Duplicate predecessor of #62; preserve as historical record. |
| [#46 — repository license](https://github.com/Martin-PB/govcheck/issues/46) | Completed; closure pending registry PR acceptance | Merged PR #39 and ADR 0005; license and NOTICE are present. |

## Portfolio-level adapter mappings

| GitHub issue | Registry role | Migration disposition |
|---|---|---|
| [#40](https://github.com/Martin-PB/govcheck/issues/40) | Root portfolio index | Keep open during transition; update to point to this register. |
| [#78](https://github.com/Martin-PB/govcheck/issues/78) | Governance/authority view | Keep open; point to canonical register. |
| [#79](https://github.com/Martin-PB/govcheck/issues/79) | Assurance/evaluation view | Keep open; point to canonical register. |
| [#80](https://github.com/Martin-PB/govcheck/issues/80) | Enforcement/operations view | Keep open; point to canonical register. |
| [#81](https://github.com/Martin-PB/govcheck/issues/81) | Formal methods/lifecycle view | Keep open; point to canonical register. |
| [#82](https://github.com/Martin-PB/govcheck/issues/82) | Bootstrap/distribution view | Keep open; point to canonical register. |
| [#83](https://github.com/Martin-PB/govcheck/issues/83) | Research/references view | Keep open; point to canonical register. |
| [#84](https://github.com/Martin-PB/govcheck/issues/84) | Collaboration/provenance view | Keep open; point to canonical register. |
| [#85](https://github.com/Martin-PB/govcheck/issues/85) | Schema/documentation quality view | Keep open; point to canonical register. |

## Import limits

The import captures identity, intent, classification and traceability; it does not copy every comment or intermediate discussion message into canonical records. Those conversations remain at their source URLs as provenance, not adopted decisions. Unresolved recommendations remain candidates or unknown until separately qualified.

This is not yet a live two-way adapter. Mismatches must be reviewed; GitHub must not silently overwrite the repository register.
