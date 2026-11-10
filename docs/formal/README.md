# Formal models

GovCheck's formal work is developed incrementally and remains separate from implementation claims. It draws on [R-05 — TLA+ and TLC](../references.md#r-05) and [R-22 — Native Git and Pijul semantics](../references.md#r-22).

## Lifecycle

- [Lifecycle model — English](lifecycle-model.md)
- [Modèle du cycle de vie — français](lifecycle-model.fr.md)
- [Generated lifecycle state diagram](lifecycle-diagram.mmd)
- [Transition registry](../../formal/lifecycle-transitions.json)
- [Diagram generator and drift check](../../scripts/render-lifecycle-diagram.py)
- [TLA+ module](../../formal/tla/GovCheckLifecycle.tla)
- [TLC configuration](../../formal/tla/GovCheckLifecycle.cfg)

## Assurance

- [Assurance claims and freshness — English](../architecture/0021-assurance-claims-and-freshness.md)
- [Affirmations, arguments et fraîcheur — français](../architecture/0021-assurance-claims-and-freshness.fr.md)
- [TLA+ module](../../formal/tla/GovCheckAssurance.tla)
- [TLC configuration](../../formal/tla/GovCheckAssurance.cfg)

The assurance model is a separate, composable formal artifact with stable logical identifier govcheck.assurance. It models a finite acyclic claim graph, the transitive closure of required evidence, versioned evidence dependencies, expiry, revocation, independent review and an acceptance snapshot. A dependency change makes affected evidence stale; the computed claim status propagates that result through the closure. Revalidation publishes a new result bound to current dependency versions.

The model records independent reviews with ReviewClaim; evidence republication, dependency changes, revocation and expiry invalidate affected reviews. The root claim can be supported only after all claims in its closure have been reviewed by authorized actors distinct from their producers.

The closure is an explicit model input and is checked against the child-claim graph. The first model uses conjunctive arguments only. It does not model external truth, cryptographic provenance, assumption discharge, distributed clocks, concurrency or implementation refinement.

## Governance authority

- [Bootstrap authority decision — English](../architecture/0023-bootstrap-governance-authority.md)
- [Décision d'amorçage de l'autorité — français](../architecture/0023-bootstrap-governance-authority.fr.md)
- [TLA+ authority-transition model](../../formal/tla/GovCheckAuthority.tla)
- [TLC configuration](../../formal/tla/GovCheckAuthority.cfg)

The authority model is a bounded transition model for the initial single-root regime. It checks historical amendment attribution to the immediately preceding authority, continuity of the authority/revision chain, consistency of current state with the last record, and the temporal append-only property (the previous history remains an exact prefix after every transition). The model does not encode effective-time positions, so it does not verify prospective effect or preservation of prior decision validity. It also abstracts principal identity, and does not model delegation records, cryptographic identity, wall-clock validity, exception lifecycles, or integration with the version-governance validator. Its finite TLC fixture is not evidence of production enforcement.

## Governance revision applicability

- [First TLC execution record — Architecture 0031](../architecture/0031-first-tlc-governance-applicability.md) · [French](../architecture/0031-first-tlc-governance-applicability.fr.md)

- [Specification 0006 — Governance revision applicability](../specifications/0006-governance-revision-applicability.md) · [French](../specifications/0006-governance-revision-applicability.fr.md)
- [TLA+ module](../../formal/tla/GovCheckGovernanceApplicability.tla)
- [TLC configuration](../../formal/tla/GovCheckGovernanceApplicability.cfg)

This separate bounded model links each evaluation to the governance revision effective at its event position, requires authorization by the authority recorded for that position, and permits publication only at a later position. It preserves historical decision bindings and rejects stale evaluations at authorization. It does not yet model authority changes/delegation, distributed consensus, cryptographic identity, full multi-writer concurrency or implementation refinement. Its TLC run is evidence about this finite abstraction only.

## Canonical governance publication

- [Governance applicability arbitration record — English](../decisions/0008-governance-applicability-arbitration-session.md) · [French](../decisions/0008-governance-applicability-arbitration-session.fr.md)
- [Canonical publication TLA+ module](../../formal/tla/GovCheckCanonicalPublication.tla)
- [TLC configuration](../../formal/tla/GovCheckCanonicalPublication.cfg)
- [Recorded TLC result — Architecture 0032](../architecture/0032-canonical-publication-model-checking.md)
- [Stable artifact catalogue entry](../../formal/artifacts.json) — `govcheck.canonical-publication`

This bounded design model separates candidate evaluation, authorization and publication. Authorization is bound to the evaluated head revision and position; publication appends only while that base remains current. It expresses revision-identity uniqueness, predecessor continuity, one publication per canonical predecessor, authorization/evaluation binding, publication authorization and stale-base exclusion. The TLC configuration also requests the append-only temporal property. **Verification status corrected:** the exact model/configuration passed TLC; see Architecture 0032 for the checked revision and finite result. Remaining implementation gaps are not covered by that model.


## Governance evaluator and exception controls

- [TLA+ module](../../formal/tla/GovCheckGovernanceControls.tla)
- [TLC configuration](../../formal/tla/GovCheckGovernanceControls.cfg)
- [Stable artifact catalogue](../../formal/artifacts.json) — `govcheck.governance-controls`

This bounded control model makes the prior evaluator the sole authoritative evaluator while a proposed replacement is represented only by comparative/shadow results. It distinguishes `Pass`, `Fail`, `Unknown` and `Conflict`; only a pass or a fail covered by a currently valid, explicitly granted exception for a waivable requirement can be authorized. Non-derogable requirements cannot be excepted, and exception validity is checked again at publication. Authority revocation is recorded at a later logical position and blocks subsequent publication; prior decisions remain append-only and can receive separate requalification records. The model is a finite abstraction and does not establish durable journal storage, distributed consensus, VCS adapter correctness, crash recovery or implementation refinement. TLC evidence will be recorded only after the exact module/configuration is checked.

## Shared release evidence

- [Stable artifact catalogue](../../formal/artifacts.json)
- [Release evidence manifest schema](../../formal/schemas/release-manifest.schema.json)

The lifecycle model is a source artifact with stable identifier govcheck.lifecycle; the assurance model uses govcheck.assurance. Their revisions are tracked by Git. A release tag binds the exact source tree and commit; generated verification reports and their manifest belong to the corresponding GitHub Release.

The lifecycle diagram is generated from formal/lifecycle-transitions.json. The checker verifies operator-name coverage and generated-file freshness; it does not parse TLA+ semantics or prove that explanatory guards/effects faithfully describe operators.

**Verification status:** the lifecycle and assurance modules, and the authority-transition module, are source artifacts checked by the formal workflow. Their TLC results establish properties only within their respective finite configurations; they do not prove implementation refinement or production enforcement. See each model document and its CI report for exact scope, state-space bounds, abstraction limits and required refinements.


## CI verification boundaries

The repository-level verification partition and its formal routing model are documented in [Architecture 0029](../architecture/0029-concern-scoped-ci-and-formal-verification-boundaries.md) ([French](../architecture/0029-concern-scoped-ci-and-formal-verification-boundaries.fr.md)). The CI routing model is `formal/tla/CICheckRouting.tla`; it is checked only when its own policy inputs change. Ordinary documentation changes do not trigger it or the product TLC models unless they are explicitly declared semantic inputs to a model.

## Reference register

For the academic and industrial foundations, including the limitations of model checking and the distinction between provenance, proof and policy authority, see the [governance and assurance reference register](../references.md) and its [French version](../references.fr.md).
