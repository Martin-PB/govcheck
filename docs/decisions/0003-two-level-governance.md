# ADR 0003 — Two-level governance: meta level and portable package

**Status:** proposed. **French:** [0003 (français)](0003-two-level-governance.fr.md).

## Context

GovCheck must govern its own repository (meta level: architecture records, decision register, deliberations) while also providing a ready-to-copy governance package for any other repository. Copying the whole repository would mix these two levels and leak GovCheck-specific history into governed repositories.

## Decision

Split the repository into two levels:

1. **Meta level (repository root, not copied):** GovCheck's own governance history — docs/architecture/ records, docs/decisions/ ADRs, root README and AGENTS files.
2. **Portable package (governance/, the only folder copied into a governed repository):** normative specifications, formal model and schemas, executable checks (CI workflow template, drift-check script), bootstrap policy, and guides/templates for the governed repository's own registers.

Anti-duplication rules:

- Normative and executable content has a single source of truth in governance/; the meta level references it by link, never by copy.
- The package's decisions/ contains only a guide and a template for the governed repository's own decision register; GovCheck's ADRs stay at the meta level.
- Exception: GitHub requires workflows at the repository root .github/workflows/. The root workflow and governance/.github/workflows/tla-check.yml are kept in sync by a check, with governance/ as the canonical source.

## Migration

Phased, to avoid conflicts with open PRs #11/#12: this ADR and the package skeleton land first; docs/specifications/, docs/formal/, formal/, scripts/, docs/BOOTSTRAP_GOVERNANCE* and the CI workflow template are moved into governance/ once #11/#12 are merged, with internal links updated and the workflow sync check added.

## Consequences

- Governing a new repository means copying exactly one folder: governance/.
- The governed repository gets its own decision register (guided by the package template), independent of GovCheck's history.