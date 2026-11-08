# 0029 — Concern-scoped CI and formal verification boundaries

**Status:** proposed architecture decision, implemented by the accompanying CI workflow change pending review and merge.  
**Scope:** repository CI orchestration and the trigger policy for GovCheck's formal models.  
**Decision:** a verification job runs only when an input within its declared verification boundary changes. Shared verifier changes invalidate all affected model runs; unrelated documentation does not.

## 1. Problem

The former `.github/workflows/tla-check.yml` mixed four independent concerns: TLC model checking, lifecycle-diagram drift, and version-governance validator tests. Its broad path filters included all architecture and specification documents, all formal schemas and fixtures, and several unrelated scripts. A change to an unrelated architecture record therefore launched every TLC model and unrelated checks.

This coupling made CI expensive and obscured what a green result actually established.

## 2. Decision and principles

CI is partitioned by the property being checked, not by a broad directory or a generic notion of repository change.

1. **Model-local verification:** each TLA+ model has its own trigger boundary, covering its source, TLC configuration and explicitly associated semantic documentation.
2. **Shared verifier invalidation:** a change to the reusable TLC runner triggers each model workflow because it can affect every model's verification result.
3. **Independent generated-artifact checks:** lifecycle diagram consistency is checked only when its transition registry, generator, generated diagram or workflow changes.
4. **Independent validator checks:** version-governance validator tests run only when the validator, its tests, its schemas/catalogue inputs or its workflow changes.
5. **No directory-wide inference:** a file's location under `docs/architecture/`, `docs/specifications/` or `formal/` does not alone establish a dependency on every formal model.
6. **Explicit semantic dependency:** if a normative or explanatory document is an input to a model's meaning, that exact document must be listed in that model's trigger paths. The mapping is reviewed when the model's abstraction or semantic dependencies change.
7. **Policy changes are verified:** edits to a model-specific workflow or the shared runner trigger the affected verification. The CI routing model is checked only when its own source, configuration or workflow changes.

## 3. Verification boundaries

| Concern | Inputs that trigger it | Check performed |
|---|---|---|
| Lifecycle model | `GovCheckLifecycle.tla`, its `.cfg`, lifecycle model documentation (EN/FR), lifecycle workflow, shared TLC runner | SANY + TLC for lifecycle only |
| Assurance model | `GovCheckAssurance.tla`, its `.cfg`, Architecture 0021 (EN/FR), assurance workflow, shared TLC runner | SANY + TLC for assurance only |
| Authority model | `GovCheckAuthority.tla`, its `.cfg`, Architecture 0023 (EN/FR), authority workflow, shared TLC runner | SANY + TLC for authority only |
| Lifecycle diagram | transition registry, diagram generator, generated diagram, diagram workflow | deterministic generation/drift check |
| Version governance | validator, validator tests, relevant schemas/catalogue, validator workflow | unit tests + Python compilation |
| CI routing policy | `CICheckRouting.tla`, its `.cfg`, routing-model workflow | SANY + TLC for routing policy |

The reusable TLC workflow pins TLA+ Tools v1.7.4 and verifies its SHA-256 before execution. Each model run publishes its own report artifact.

## 4. Formal routing properties

`formal/tla/CICheckRouting.tla` abstracts the changed-file set into concern categories and checks:

- unrelated architecture/documentation changes trigger no TLC model;
- a lifecycle-only input triggers lifecycle TLC and not assurance/authority TLC;
- an assurance-only input triggers assurance TLC and not lifecycle/authority TLC;
- an authority-only input triggers authority TLC and not lifecycle/assurance TLC;
- a change to the shared TLC runner triggers all three model checks;
- every model-specific input triggers its corresponding model check.

The routing model is intentionally separate from the product lifecycle, assurance and authority models. It verifies the declared dispatch policy, not the semantic correctness of those models or the fidelity of every GitHub Actions path expression. The workflow path lists remain executable policy and must be reviewed against this model when changed.

## 5. Invariants and interpretation

The governing invariants are **coverage**, **isolation**, **shared-runner invalidation** and **non-interference of unrelated documentation**. A skipped model is not reported as newly verified; it means no declared input to that model's verification boundary changed in the candidate.

A green TLC result establishes only that the selected finite model/configuration completed with its checked properties. It does not prove implementation refinement, semantic fidelity between prose and TLA+, or correctness of the GitHub Actions trigger engine.

## 6. Change-control rule

When adding or changing a formal model:

1. identify its source, configuration, semantic documentation and shared execution dependencies;
2. update its dedicated trigger paths;
3. update the routing abstraction if the dependency categories or isolation policy change;
4. run the routing model when that policy changes;
5. retain a model-specific report and verify that unrelated changes do not schedule it.

When a document changes the meaning of a model, the corresponding model trigger must include that document. Purely editorial or unrelated architecture changes must not be added as broad wildcard dependencies.

## 7. Consequences and limits

This design intentionally allows a small workflow dispatch to occur for changes in a model's own semantic documentation, while avoiding expensive unrelated TLC runs. It uses native GitHub Actions path filters and reusable workflows; it adds no third-party path-filter action or external service.

The trigger mapping is an explicit, reviewable dependency declaration, not an automatic semantic-diff engine. A missed dependency is a governance defect; a broad wildcard is not an acceptable substitute for dependency analysis.
