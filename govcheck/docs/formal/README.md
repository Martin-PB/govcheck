# Formal models

GovCheck's formal work is developed incrementally and remains separate from implementation claims.

## Lifecycle

- [Lifecycle model — English](lifecycle-model.md)
- [Modèle du cycle de vie — français](lifecycle-model.fr.md)
- [Generated lifecycle state diagram](lifecycle-diagram.mmd)
- [Transition registry](../../formal/lifecycle-transitions.json)
- [Diagram generator and drift check](../../scripts/render-lifecycle-diagram.py)
- [TLA+ module](../../formal/tla/GovCheckLifecycle.tla)
- [TLC configuration](../../formal/tla/GovCheckLifecycle.cfg)

## Assurance

- Assurance claims and freshness records live at the meta level (niveau méta).
- [TLA+ module](../../formal/tla/GovCheckAssurance.tla)
- [TLC configuration](../../formal/tla/GovCheckAssurance.cfg)

The assurance model is a separate, composable formal artifact with stable logical identifier govcheck.assurance. It models a finite acyclic claim graph, the transitive closure of required evidence, versioned evidence dependencies, expiry, revocation, independent review and an acceptance snapshot. A dependency change makes affected evidence stale; the computed claim status propagates that result through the closure. Revalidation publishes a new result bound to current dependency versions.

The model records independent reviews with ReviewClaim; evidence republication, dependency changes, revocation and expiry invalidate affected reviews. The root claim can be supported only after all claims in its closure have been reviewed by authorized actors distinct from their producers.

The closure is an explicit model input and is checked against the child-claim graph. The first model uses conjunctive arguments only. It does not model external truth, cryptographic provenance, assumption discharge, distributed clocks, concurrency or implementation refinement.

## Shared release evidence

- [Stable artifact catalogue](../../formal/artifacts.json)
- [Release evidence manifest schema](../../formal/schemas/release-manifest.schema.json)

The lifecycle model is a source artifact with stable identifier govcheck.lifecycle; the assurance model uses govcheck.assurance. Their revisions are tracked by Git. A release tag binds the exact source tree and commit; generated verification reports and their manifest belong to the corresponding GitHub Release.

The lifecycle diagram is generated from formal/lifecycle-transitions.json. The checker verifies operator-name coverage and generated-file freshness; it does not parse TLA+ semantics or prove that explanatory guards/effects faithfully describe operators.

**Verification status:** both modules and TLC configurations are source artifacts. No SANY/TLC execution or proof result is claimed for the new assurance model. See each model document for scope, abstraction limits and required refinements.

## Bibliographic references

- [R-05 — TLA+ and TLC](../references.md#r-05)
- [R-20 — Lean theorem prover](../references.md#r-20)
- [R-22 — Native Git and Pijul semantics](../references.md#r-22)
