# Formal models

GovCheck's formal work is developed incrementally and remains separate from implementation claims.

## Lifecycle

- [Lifecycle model v1 — English](lifecycle-model-v1.md)
- [Modèle du cycle de vie v1 — français](lifecycle-model-v1.fr.md)
- [TLA+ module](../../formal/tla/GovCheckLifecycle.tla)
- [TLC configuration](../../formal/tla/GovCheckLifecycle.cfg)

The initial model covers one abstract change, tuple-bound evaluation, evidence publication, authorized approvals, acceptance, exact-candidate application, input mutation, and terminal decisions.

**Verification status:** specification and TLC configuration added; no TLC execution or proof result is claimed. See the model document for abstraction limits and required next refinements.
