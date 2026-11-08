# ADR 0003 — Two-level governance: product package and meta history

**Status:** proposed. **French:** [0003 (français)](0003-two-level-governance.fr.md).

## Context

GovCheck is itself code under development. The repository must therefore serve two purposes at once: (1) ship a governance package that can be copied into any new repository, and (2) keep the living history of GovCheck's own governance (records, ADRs, deliberations, specifics).

## Decision

Maintain two living levels, updated together in the same pull request:

1. **Product package (`govcheck/`):** the shippable governance code. It evolves with every PR and, at any commit, must form a coherent, self-contained setup for a new repository: specifications, formal model and schemas, executable checks (CI workflow template, drift check), bootstrap policy, decision-register guide and templates. It contains no GovCheck-specific history. A bootstrap script inside the package (`govcheck/bootstrap.py`) generates the target repository's tree from the package.
2. **Meta level (repository root):** GovCheck's own living documents with their specifics — docs/architecture/ records, docs/decisions/ ADRs, root README and AGENTS files. This level records why and how the package evolves.

Duplication rule: when a PR changes a normative document, both levels are updated in that PR — a generic version in govcheck/ (for governed repositories) and the specific living version at the meta level. Structural alignment is declared, not inferred: `docs/template-manifest.json` classifies each section of every paired normative document as `package` (indispensable: present at both levels, same relative order), `optionnel` (may appear on either side) or `meta-only` (meta level only, never copied into the package); any section absent from the manifest defaults to `package`. The CI check (`scripts/check-package-alignment.py`) verifies the manifest against both levels, without requiring identical content. Exception: GitHub requires workflows at the repository root .github/workflows/, so the root workflow is generated from the package template by the bootstrap/sync check.

## Migration

Phased: this ADR, the package skeleton and the bootstrap script land first (PR #20). Existing normative files (docs/specifications/, docs/formal/, formal/, scripts/, docs/BOOTSTRAP_GOVERNANCE*, CI template) are then duplicated into govcheck/ as generic versions, with the meta copies kept at the root; internal links updated; structural alignment check added.

## Consequences

- Setting up governance in a new repository = run the package bootstrap script (or copy govcheck/), which produces the full tree.
- The meta level remains the authoritative history of GovCheck itself and is never copied into governed repositories.

## Bibliographic references

- [R-107 — GitHub Actions workflow location and syntax](../references.md#r-107)
