# 0008 — Governance applicability arbitration session record

**Record status:** user-expressed arbitration choices, pending incorporation and formal normative adoption through GovCheck's applicable authority process. This record is not itself an adoption instrument, does not amend Architecture 0023, and does not claim implementation or verification.
**Authority/provenance:** choices explicitly selected by the project owner in the GovCheck discussion on 2026-11-10, in response to the eleven guided arbitration questions for issue [#41](https://github.com/Martin-PB/govcheck/issues/41).
**Technical companion:** [Specification 0006](../specifications/0006-governance-revision-applicability.md) and proposed [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.md); bounded models [GovCheckGovernanceApplicability](../../formal/tla/GovCheckGovernanceApplicability.tla), [GovCheckCanonicalPublication](../../formal/tla/GovCheckCanonicalPublication.tla), [GovCheckGovernanceControls](../../formal/tla/GovCheckGovernanceControls.tla) and [GovCheckJournalRecovery](../../formal/tla/GovCheckJournalRecovery.tla); model-checking records [Architectures 0031–0035](../architecture/README.md).
**French:** [0008 — compte rendu de séance d'arbitrage](0008-governance-applicability-arbitration-session.fr.md).

## 1. Status and interpretation

This document records the exact choices made by the designated project authority during a guided arbitration session. It preserves provenance and makes the selected direction reviewable. It does **not** convert the session into a formally adopted normative policy merely by being committed or merged.

The choices below are inputs to the technical formalization. Before any normative requirement is treated as adopted, the applicable governance process must record the adoption, authority basis, exact governance revision, decision position and effective publication event. Until then, Specification 0006 remains a proposed contract and implementation must not claim these choices as adopted policy.

Architecture 0023 remains the source for the currently recorded root-authority regime. Nothing in this record changes the identity, scope or succession of that authority.

## 2. Selected arbitration outcomes

### A-01 — Canonical event order: serialized logical journal with concurrency control

**Selected:** B.

GovCheck is to use a canonical logical event journal. Candidates may be prepared concurrently, but definitive registration is serialized with predecessor/base validation. An event whose expected predecessor is no longer current cannot be appended as if it were current; it must be rejected as stale or explicitly reconciled and re-evaluated. This selection does not choose a consensus protocol or a concrete storage engine.

### A-02 — VCS role: transport and provenance adapters

**Selected:** B.

Git, Pijul and other VCS/forges transport governed artifacts and events and provide native provenance references. Their native commit/patch graph does not determine normative event order. Divergent logical histories must be detected and explicitly resolved; a successful native merge is not itself a governance resolution.

### A-03 — Effective point: publication event

**Selected:** B.

The candidate is evaluated and its publication authorized under the previously applicable governance revision. A distinct publication event establishes the resulting revision's effective position and is the first event governed by that resulting revision. The publication event itself is authorized under the prior revision. No candidate-proposed rule may authorize its own publication.

### A-04 — Evaluator transition: dual execution, prior evaluator authoritative

**Selected:** C.

The evaluator recognized by the prior applicable governance revision remains the sole authoritative evaluator for the transition. A proposed replacement evaluator may run in parallel for comparison, migration analysis and evidence collection, but its output cannot authorize its own adoption. Evaluator identity, version, configuration, semantics and relevant dependencies must be bound to the authoritative evaluation. Divergence must be visible and explained.

### A-05 — Revocation and historical decisions

**Selected:** C.

Revocation is prospective from its explicit effective event. It does not erase or silently rewrite decisions made under the previously applicable revision. Historical decisions may undergo a separate, explicit requalification that records the affected decisions, rationale, authority, evidence and outcome while preserving their original records.

### A-06 — Exceptions

**Selected:** C.

Exceptions are explicit, justified, scoped, time- or condition-bounded, attributable, traceable and revocable/reviewable. They record the rule and candidate scope, granting authority, rationale, residual risk and acceptance, compensating measures where applicable, expiry/termination condition and revocation/review conditions. Some requirements are non-derogable. An exception is a distinct authorization/decision, not evidence that the underlying requirement was satisfied.

### A-07 — Unknown and conflict

**Selected:** C.

`unknown` (insufficient or unresolved information) and `conflict` (incompatible claims or histories) are distinct blocking states. Both prevent normative transition. Resolution must be explicit, attributable and traceable. A conflict cannot be bypassed by an exception or silently resolved by VCS merge order, branch preference or implementation default.

### A-08 — Stale evaluations

**Selected:** C.

An evaluation that becomes stale is retained as historical evidence of what was evaluated and when, but cannot support a new authorization/publication. A fresh evaluation is required against the current candidate, base, governance revision, authority chain, evaluator/specification/profile and relevant evidence dependencies. Staleness is distinct from a negative evaluation and its cause must be recorded.

### A-09 — Concurrent publications

**Selected:** B.

At most one governance publication may succeed from a given canonical predecessor/base position. Other candidates prepared or evaluated against that base become stale for publication and must be re-evaluated against the newly current governance revision. They are not automatically rejected solely because they lost the race.

### A-10 — Rollback

**Selected:** B.

Rollback always creates a new governance revision and event. Its content may restore the content of an earlier revision, but it has a new immutable identity, predecessor, authorization, provenance and effective position. Historical positions and identities are never reused or rewound.

### A-11 — Evaluation, authorization and publication acts

**Selected:** C.

Evaluation, authorization and publication are three distinct logical acts with separately identifiable records and relations. An adapter may execute them within one atomic technical transaction, provided that atomic execution preserves each act's identity, semantic distinction, inputs, outputs, ordering/causal relation and recoverability. Evaluation is not authorization; authorization is not publication.

## 3. Cross-cutting consequences for technical formalization

The selected outcomes imply that the technical contract and its future executable realization must address at least:

- logical event identity, predecessor identity and monotonically ordered canonical position;
- compare-and-append / serialized publication with stale-base rejection;
- VCS-native identifiers as provenance, not normative ordering keys;
- evaluation binding to exact candidate, base, prior governance, authority chain, authoritative evaluator, specification/profile and evidence dependencies;
- a separate comparative evaluator result that cannot substitute for the authoritative result;
- explicit authorization and publication acts, including atomic adapter execution without semantic collapse;
- prospective effective positions and immutable revision identities;
- explicit revocation and historical requalification events;
- exception scope, non-derogable requirements, expiry and revocation;
- distinct fail-closed `unknown` and `conflict` outcomes;
- stale-evaluation retention and mandatory re-evaluation;
- single-winner publication from a predecessor and retry/recovery semantics;
- rollback as a new revision.

These are formalization requirements derived from the recorded selections; they are not claims that the current bounded TLA+ model already covers them.

## 4. Coverage of the bounded formal models and explicit gaps

The formal artifacts are **separate finite abstractions**, not one integrated model and not a refinement proof:

- **Applicability and prior authority — [Architecture 0031](../architecture/0031-first-tlc-governance-applicability.md), PR #90:** decision/effective-position binding, prior applicable authority and bounded historical preservation; 20,785 generated / 18,067 distinct states.
- **Canonical publication — [Architecture 0032](../architecture/0032-canonical-publication-model-checking.md), PR #96:** captured-head evaluation, authorization binding, distinct publication effect, stale-authorization rejection, revision/predecessor uniqueness and one publication per canonical predecessor; 84,307 generated / 56,895 distinct states, eight invariants and `AppendOnly` passed.
- **Evaluator/exception/revocation controls — [Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.md), PR #98:** prior evaluator authority, comparative-only shadow results, distinct blocking `Unknown`/`Conflict`, bounded/revocable exceptions and non-derogable requirements, prospective revocation, separate historical requalification and stale-authorization rejection; 2,826,117 generated / 1,026,484 distinct states, nine invariants and `AppendOnly` passed.
- **Journal recovery/rollback — [Architecture 0035](../architecture/0035-canonical-journal-recovery-model.md), PR #99:** abstract durable-append commit point, crash before/after commit, replay-to-head, rollback as a new event/revision restoring earlier content, and passive Git/Pijul replica observations; 178,549 generated / 38,434 distinct states, six invariants and `AppendOnly` passed. It assumes one serialized writer and abstracts upstream authorization; its weak-fairness assumption is not a checked eventual-recovery liveness result.

[Specification 0007](../specifications/0007-canonical-governance-journal-protocol.md) is a proposed semantic contract for compare-and-append, linearization, durable receipts, idempotent retry, journal scope/genesis, VCS provenance-only adapters, replica reconciliation and twelve conformance scenarios. It is not itself model-checked as a whole or implemented.

**Integration status:** PRs #90, #96 and #98 are merged into `main`. GitHub marked PR #99 merged into the former PR #98 work branch, not into `main`; PRs #100 and #104 remain open and stacked. The journal-recovery model and Specification 0007 must therefore not be described as already integrated into `main`. This review candidate carries that work toward `main`.

### Remaining gaps

Unbounded/distributed multi-writer linearizability and consensus; concrete storage-engine durability, torn writes and operational recovery; actual VCS adapter mappings and divergent-replica resolution; full dependency-based stale-evaluation invalidation and re-evaluation; arbitrary evaluator succession, cryptographic identity and delegation; complete exception risk-acceptance and real-time expiry; explicit resolution workflows for `unknown`/`conflict`; concrete atomic execution preserving the three logical acts across interruption; multiple rollback sequences; executable conformance tests, implementation refinement and production enforcement. Specification 0007 describes proposed obligations but does not supply their implementation or verification.

No finite model-checking result, specification edit or PR merge establishes implementation conformance or normative adoption. The eleven choices remain owner-selected design inputs until a separate adoption event under the applicable prior governance revision is recorded.

## 5. Adoption and implementation boundary

- This session record records user choices; it is not a normative adoption event.
- Specification 0006 may describe the selected direction as an authority-selected proposal pending formal adoption, but must not silently upgrade its status.
- A later adoption record must bind the adopted contract to the prior governance revision and an explicit decision/publication event.
- A merged PR, green CI, issue label or repository permission is not normative adoption.
- No implementation, enforcement boundary, distributed consensus, cryptographic provenance or VCS adapter behavior is claimed by this record.

## 6. Traceability

- Decision parent: [Issue #41](https://github.com/Martin-PB/govcheck/issues/41).
- Technical companion: [Issue #86](https://github.com/Martin-PB/govcheck/issues/86).
- Prior authority regime: [Architecture 0023](../architecture/0023-bootstrap-governance-authority.md).
- Lifecycle contract: [Specification 0003](../specifications/0003-change-lifecycle.md).
- Applicability contract: [Specification 0006](../specifications/0006-governance-revision-applicability.md).
- Proposed journal protocol: [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.md).
- Bounded models: [applicability](../../formal/tla/GovCheckGovernanceApplicability.tla), [canonical publication](../../formal/tla/GovCheckCanonicalPublication.tla), [governance controls](../../formal/tla/GovCheckGovernanceControls.tla), [journal recovery](../../formal/tla/GovCheckJournalRecovery.tla).
- Model-checking records: [Architecture 0031](../architecture/0031-first-tlc-governance-applicability.md), [0032](../architecture/0032-canonical-publication-model-checking.md), [0033](../architecture/0033-governance-evaluator-exception-revocation-model.md) and [0035](../architecture/0035-canonical-journal-recovery-model.md).
- Formal-methods and VCS references: [R-05](../references.md#r-05), [R-22](../references.md#r-22), [R-194](../references.md#r-194), [R-195](../references.md#r-195) and [R-196](../references.md#r-196).

External references inform technical methods; they do not determine or authorize the user's selected governance policy.
