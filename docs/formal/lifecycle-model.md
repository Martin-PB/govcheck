# GovCheck lifecycle model — TLA+

**Status:** initial bounded specification; not yet model-checked. This model is an executable formalization candidate for architecture document 0008, not an implementation or proof of production behavior.

## Identity and versioning

The model has the stable logical identifier `govcheck.lifecycle`. Its source path is `formal/tla/GovCheckLifecycle.tla`; the path is not a release number. Git history records revisions to this artifact. A release tag identifies the exact repository commit containing the version used for that release. Do not create a new copy or rename this file solely because a release is published.

The bilingual explanation is maintained at this stable path. The exact source revision used by a release is identified by its tag/commit, not by a `v1` suffix in the filename.

## Scope

The model covers one abstract change and the exact identity tuple:

`(baseId, candidateId, governanceId, specId)`.

It models evidence for a finite set of mandatory obligations, approvals by authorized actors, acceptance, exact-candidate application, input mutation, terminal decisions, and an append-only event sequence.

It deliberately does not model Git internals, Pijul patch/channel semantics, cryptographic authenticity, filesystem races, forge behavior, or the implementation of an adapter.

## State and transitions

The lifecycle is also shown in the [generated state diagram](lifecycle-diagram.mmd). Its transition registry and generator are linked from the [formal-model index](README.md). The diagram is explanatory, not normative: the TLA+ module remains the semantic authority.

- `phase`: lifecycle phase.
- `evaluatedTuple`: exact tuple evaluated.
- `evidence`: obligations for which an evidence record has been published against the current tuple.
- `evidenceOutcomes`: the latest published outcome for each obligation.
- `outcomes`: the outcomes bound to the latest evaluation. `PublishEvidence(obligation, outcome)` can publish `Pass`, `Fail`, `Unknown`, `Unsupported`, `NotRun` or `Incomplete`. Missing evidence evaluates to `Unknown`. The lifecycle reaches `Reviewable` only when every obligation has evidence and every outcome is `Pass`; all other outcomes remain `Evaluated` and cannot be accepted. Publishing or replacing evidence clears prior approvals and forces a fresh evaluation/review. This models status propagation, not evidence truth or sufficiency.
- `approvals`: set of authorized actors approving the current tuple.
- `acceptedTuple`: exact tuple accepted.
- `appliedCandidateId`: candidate identity reported as applied.
- `history`: sequence extended by every modeled state-changing action. Its length is bounded by `HistoryLimit` (12 in the TLC configuration) so the explored state space remains finite; reaching the cap disables further state-changing actions. This is an exploration bound, not a production retention policy.

Transitions are `Prepare`, `PublishEvidence`, `Evaluate`, `Approve`, `Accept`, `Apply`, `ChangeInputs`, `Reject`, `Withdraw`, and `Supersede`.

## State invariants configured for TLC

| Invariant | What it checks |
|---|---|
| `TypeOK` | Every state variable remains in its declared domain. |
| `AcceptanceSoundness` | An accepted change is bound to the current tuple, a current evaluation, passing obligations, and the required approval count. |
| `ApplicationSoundness` | Applied means the recorded applied candidate is exactly the candidate in the accepted tuple and current tuple. |
| `NoStaleEvaluation` | Reviewable, Accepted, and Applied states cannot rely on an evaluation for an older tuple. |
| `EvidenceBinding` | Reviewable requires all modeled obligations to have evidence and a `Pass` outcome for the current evaluation. |
| `EvaluationOutcomeBinding` | Evaluated and later phases use the published outcome for each evidenced obligation; missing evidence remains `Unknown`. |
| `FailedOrUnresolvedEvidenceBlocksAcceptance` | Any non-`Pass` obligation outcome prevents Accepted and Applied phases. |
| `ApprovalBinding` | Accepted and Applied states contain only approvals from the configured authorized actor set. |
| `NoImplicitApplication` | Before the Applied phase, no applied-candidate identity is recorded. |
| `NoApprovalInPreparedPhase` | Prepared carries no approval from before a new evidence publication. |
| `HistoryNonEmpty` | The event sequence contains its initial creation event. |

The TLC configuration also checks the temporal property `TerminalDiscipline`: once a phase is terminal (`Applied`, `Rejected`, `Withdrawn`, or `Superseded`), it cannot transition out of that phase.

The TLA+ module also states corresponding theorem obligations from `Spec`. TLC configuration is bounded to two values for each identity dimension, two actors, two obligations, and at most 12 history events.

## Important limitations and next refinements

1. Evidence truth, provenance, freshness dependencies, revocation, and independent verification are abstracted away. The model accepts a published `Pass` value as an input; it does not verify that value.
2. The model now propagates explicit `Fail`, `Unknown`, `Unsupported`, `NotRun` and `Incomplete` outcomes. It still abstracts away the richer evidence-record status and method semantics defined in Specification 0005.
3. The model does not yet represent concurrent operations, adapter unavailability, TOCTOU races, or a malicious adapter.
4. The event sequence is extended by the modeled actions, but this version does not yet define a separate temporal history-integrity property or actor/reason metadata for every event.
5. `ChangeInputs` is disabled after terminal phases, including Applied. A production policy for post-application remediation/reopening requires a separate decision.
6. No TLC result is claimed. Before treating this model as checked, run it with a pinned TLC version and record the exact tool version, configuration, explored state/transition counts, completion status, and any counterexample.

## Reproducibility and release evidence

Run TLC against `GovCheckLifecycle.tla` with `GovCheckLifecycle.cfg` using a locally pinned TLA+ Tools distribution. Do not interpret a successful bounded run as implementation conformance, theorem proof, or normative fidelity.

A release may attach a generated verification report and a release manifest. The manifest must identify the release tag and commit, stable artifact ID, exact path and content digest, TLC/tool version, configuration digest, execution status, and state/transition counts when available. Generated reports are release assets, not manually renamed source files. The manifest format is defined by `formal/schemas/release-manifest.schema.json`; the stable artifact catalogue is `formal/artifacts.json`.
