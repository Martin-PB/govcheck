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
- [Stable artifact catalogue](../../formal/artifacts.json)
- [Release evidence manifest schema](../../formal/schemas/release-manifest.schema.json)

The lifecycle model is a source artifact with a stable logical identifier, `govcheck.lifecycle`. Its revisions are tracked by Git. A release tag binds the exact source tree and commit; it does not require copies of source files with release-specific names. Generated verification reports and their manifest belong to the corresponding GitHub Release.

The diagram is generated from `formal/lifecycle-transitions.json`. The registry records explanatory labels and links each displayed transition to a top-level TLA+ operator. Run `python3 scripts/render-lifecycle-diagram.py` to regenerate it, or add `--check` to detect drift. The checker verifies operator-name coverage and generated-file freshness; it does **not** parse TLA+ semantics or prove that the explanatory guards/effects faithfully describe the operators. Review those together whenever a transition changes.

The initial model covers one abstract change, tuple-bound evaluation, evidence publication, authorized approvals, acceptance, exact-candidate application, input mutation, and terminal decisions.

**Verification status:** specification and TLC configuration added; no TLC execution or proof result is claimed. See the model document for abstraction limits and required next refinements.
