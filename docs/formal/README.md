# Formal models

GovCheck's formal work is developed incrementally and remains separate from implementation claims.

## Lifecycle

- [Lifecycle model — English](lifecycle-model.md)
- [Modèle du cycle de vie — français](lifecycle-model.fr.md)
- [TLA+ module](../../formal/tla/GovCheckLifecycle.tla)
- [TLC configuration](../../formal/tla/GovCheckLifecycle.cfg)
- [Stable artifact catalogue](../../formal/artifacts.json)
- [Release evidence manifest schema](../../formal/schemas/release-manifest.schema.json)

The lifecycle model is a source artifact with a stable logical identifier, `govcheck.lifecycle`. Its revisions are tracked by Git. A release tag binds the exact source tree and commit; it does not require copies of source files with release-specific names. Generated verification reports and their manifest belong to the corresponding GitHub Release.

The initial model covers one abstract change, tuple-bound evaluation, evidence publication, authorized approvals, acceptance, exact-candidate application, input mutation, and terminal decisions.

**Verification status:** specification and TLC configuration added; no TLC execution or proof result is claimed. See the model document for abstraction limits and required next refinements.
