# GovCheck lifecycle model — TLA+ v1

**Status:** initial bounded specification; not yet model-checked. This model is an executable formalization candidate for architecture document 0008, not an implementation or proof of production behavior.

## Scope

The model covers one abstract change and the exact identity tuple:

`(baseId, candidateId, governanceId, specId)`.

It models evidence for a finite set of mandatory obligations, approvals by authorized actors, acceptance, exact-candidate application, input mutation, terminal decisions, and an append-only event sequence.

It deliberately does not model Git internals, Pijul patch/channel semantics, cryptographic authenticity, filesystem races, forge behavior, or the implementation of an adapter.

## State and transitions

- `phase`: lifecycle phase.
- `evaluatedTuple`: exact tuple evaluated.
- `evidence`: obligations for which evidence has been published against the current tuple.
- `outcomes`: `Pass`, `Fail`, or `Unknown`. In this first abstraction, missing evidence yields `Unknown`; published evidence yields `Pass`. This is an explicit simplifying assumption, not a claim that evidence is truthful or sufficient in a real system.
- `approvals`: set of authorized actors approving the current tuple.
- `acceptedTuple`: exact tuple accepted.
- `appliedCandidateId`: candidate identity reported as applied.
- `history`: sequence extended by every modeled state-changing action.

Transitions are `Prepare`, `PublishEvidence`, `Evaluate`, `Approve`, `Accept`, `Apply`, `ChangeInputs`, `Reject`, `Withdraw`, and `Supersede`.

## Checked state invariants

| Invariant | What it checks |
|---|---|
| `TypeOK` | Every state variable remains in its declared finite domain. |
| `AcceptanceSoundness` | An accepted change is bound to the current tuple, a current evaluation, passing obligations, and the required approval count. |
| `ApplicationSoundness` | Applied means the recorded applied candidate is exactly the candidate in the accepted tuple and current tuple. |
| `NoStaleEvaluation` | Reviewable, Accepted, and Applied states cannot rely on an evaluation for an older tuple. |
| `EvidenceBinding` | Reviewable requires all modeled obligations to have evidence for the current evaluation. |
| `ApprovalBinding` | Accepted and Applied states contain only approvals from the configured authorized actor set. |
| `NoImplicitApplication` | Before the Applied phase, no applied-candidate identity is recorded. |
| `HistoryNonEmpty` | The event sequence contains its initial creation event. |

The TLA+ module also states corresponding theorem obligations from `Spec`. TLC configuration is bounded to two values for each identity dimension, two actors, and two obligations.

## Important limitations and next refinements

1. Evidence truth, provenance, freshness dependencies, revocation, and independent verification are abstracted away. The current model treats publication as sufficient evidence for its obligation.
2. `Fail` is in the outcome domain but no transition currently produces it. A later refinement should model explicit failed checks and distinguish failed, unknown, unsupported, and not-run outcomes.
3. The model does not yet represent concurrent operations, adapter unavailability, TOCTOU races, or a malicious adapter.
4. The event sequence is extended by the modeled actions, but this version does not yet define a separate temporal history-integrity property or actor/reason metadata for every event.
5. `ChangeInputs` is disabled after terminal phases, including Applied. A production policy for post-application remediation/reopening requires a separate decision.
6. No TLC result is claimed. Before treating this model as checked, run it with a pinned TLC version and record the exact tool version, configuration, explored state/transition counts, completion status, and any counterexample.

## Reproducibility

Run TLC against `GovCheckLifecycle.tla` with `GovCheckLifecycle.cfg` using a locally pinned TLA+ tools distribution. Do not interpret a successful bounded run as implementation conformance, theorem proof, or normative fidelity.
