# Source-level triage of external critique #129

**Status:** preliminary source inspection; not an independently reproduced execution report. **Date:** 2026-11-13. **Work item:** [#130](https://github.com/Martin-PB/govcheck/issues/130). **Source critique:** [#129](https://github.com/Martin-PB/govcheck/issues/129).

## 1. Revision identity and method boundary

The GitHub comparison of `main` with the work branch at triage time reported that `main` was at `24760fbfd747fc64f6261b53182f4ed8fdbd4467`, the same commit identified by the external critique. The findings below therefore concern the same source revision, not a later mainline correction.

This pass inspected source files through the repository integration. It did **not** execute Python tests, TLC, Lean builds, axiom audits or the CSLib compatibility profile. It is source-level triage only. No GitHub Actions workflow was triggered.

## 2. Findings 6.1–6.7

| Critique finding | Source-level disposition | Current evidence and qualification |
|---|---|---|
| 6.1 — no executable canonical model/schema | **Confirmed** | Specification 0002 explicitly states that it is a proposed architecture/design contract and that no schema or evaluator is implemented. Markdown remains the practical repository representation. |
| 6.2 — bootstrap/adoption circularity | **Partly confirmed; refined by later specification** | Specification 0007 now defines a technology-neutral logical journal protocol, genesis trust-anchor requirements, compare-and-append, durable commit and recovery semantics. It is still explicitly proposed and not implemented. The critique's claim that the project has no specified journal protocol is therefore incomplete; the adoption/bootstrap path remains an unresolved implementation and authority problem. |
| 6.3 — separation of duties | **Confirmed as a declared governance limitation, not necessarily an accidental inconsistency** | Architecture 0023 explicitly says the current single principal may propose and authorize a governance change and that the system must not claim two-person authorization. It distinguishes normative authorization, technical assessment/optional independent review and execution. The assurance model's distinct reviewer is a separate technical-assessment property, not proof of a second normative authority. The residual risk and prospective multi-principal evolution remain open in #60/#71. |
| 6.4 — independent-review attestation | **Structural defect confirmed by source inspection; execution still required** | `rule_independent_review` reads `docs/attestations/*.json`, requires `candidate_rev` to equal the full candidate revision and compares a reviewer string with the Git author string. The workflow invokes the checker on `HEAD`. A file committed inside the candidate tree cannot ordinarily contain the SHA of the commit whose tree contains that file without a self-reference problem. The reviewer field is not authenticated by this code. The inspected unit tests inject a synthetic candidate SHA and author directly into the evaluator, then create an attestation containing that supplied value; they do not exercise a real commit whose tree contains its own attestation. A redesigned external/sidecar attestation and authenticated identity contract is needed. |
| 6.5 — fail-closed disabled in CI | **Confirmed for the current CI enforcement path** | The workflow is explicitly named report-only; the GovCheck step has `continue-on-error: true` and ends with `|| true`. Unit tests are a separate blocking step. Thus the evaluator's fail-closed result semantics do not currently make the overall CI workflow an acceptance gate. |
| 6.6 — partial mapping may have empty coverage | **Confirmed** | `SemanticBridge.partialMapping` accepts a domain predicate and proves the target only for source propositions in that domain. It does not require the domain to be inhabited. An empty domain therefore satisfies the constructor without establishing any non-empty coverage. This is not a proof of False from True; it is a missing coverage/non-vacuity guarantee. |
| 6.7 — journal requires separate infrastructure | **Overstated; semantic concern valid, physical conclusion not established** | Specification 0007 deliberately separates the logical normative order from VCS-native order, but does not mandate a physically separate database or service. It leaves storage engine and deployment choices open. Any backing store must still demonstrate the required atomic compare-and-append, durable commit, recovery and idempotency properties. Semantic separation does not imply physical separation. |

## 3. Deeper formal and implementation limitations

### 3.1 Safety versus conditional liveness

The lifecycle model contains safety invariants around acceptance, staleness, evidence and application. Its `NoUnexpectedNonterminalDeadlock` condition is not a useful guarantee that a legitimate candidate eventually reaches `Applied`: the model can retain rejection/withdrawal paths. A meaningful progress claim needs explicit assumptions about authority availability, evidence production, fair scheduling, dependencies and the possibility of rejection. Unconditional acceptance liveness would be unsafe.

### 3.2 Separate models are not a refinement proof

Specification 0007 itself characterizes the TLA+ models as separate bounded slices and says they are composable design evidence, not one integrated implementation model. No end-to-end refinement relation from lifecycle/authority/journal models to the Python checker or a production implementation is established by that statement.

### 3.3 Lean theorem strength

The inspected mapping code includes projection-style results and a theorem whose witness is accompanied by the reflexive equality `derivation.proof = derivation.proof`. Such a theorem establishes existence of the carried derivation object, not an additional semantic property of the source mapping. The type-level proof obligations may still be useful, but theorem names and claims must match the actual proposition established.

### 3.4 Executable scope

The eight rules in `govcheck/check.py` cover license presence, bilingual decision files, manifest pairs, reference integrity, source presence, bootstrap integrity, freshness of TLA evidence and independent-review attestation. They do not implement the canonical lifecycle, authority registry, journal protocol, risk/decision semantics or the cross-model assurance contracts. This confirms a substantial implementation-conformance gap; it does not imply the existing slice has no value.

## 4. What remains to reproduce

The following work is still required under #130:

- run the complete Python unit-test suite on the exact commit and report command, interpreter version and result;
- run SANY/TLC for each checked-in model and configuration, recording exact tool digest, Java version, state counts, bounds, invariants and temporal properties;
- build the Lean coherence package, run its axiom report and separately inspect/build `formal/cslib-compat` under its own Lean 4.36.0-rc2 toolchain (the main Lean profile pins 4.19.0);
- inspect all model configurations and CI path filters, and establish which checks are actually required at the acceptance boundary;
- construct minimal negative examples for the empty-domain mapping and attestation identity/revision problem;
- classify each finding after execution as confirmed, refuted, partial, superseded, non-reproducible or requiring authority arbitration.

The current network/runtime could not clone the repository for local execution. The above commands have not been run in this pass. No Actions credits were used.

## 5. Disposition

This triage narrows the external critique rather than accepting it wholesale. Findings 6.1, 6.4, 6.5 and 6.6 are supported by source inspection; 6.2 and 6.3 need the stated qualifications; 6.7's physical-infrastructure conclusion is not supported by Specification 0007. The deeper safety/liveness, model-composition and implementation-conformance concerns remain important.

No specification, Lean/TLA+ model, acceptance rule or authority decision was changed by this report. Corrective implementation remains gated by the exact reproducibility and design work tracked in #130 and by existing work items where applicable.
