# GovCheck governance package

**Français :** [README.fr.md](README.fr.md)

This folder is the **only** part of the GovCheck repository meant to be copied into another repository to govern it. Run `python3 governance/bootstrap.py TARGET_DIR` (or copy governance/ as-is into the target repository's root) and follow the bootstrap policy.

## Contents (planned layout)

- specifications/ — normative governance specifications (bilingual, English default)
- formal/ — lifecycle model (TLA+), transition registry, artifact catalogue, JSON schemas
- docs/formal/ — lifecycle model documentation and generated diagram
- scripts/ — deterministic diagram generator and drift check
- .github/workflows/ — CI workflow template (kept in sync with the meta repository by a check)
- BOOTSTRAP_GOVERNANCE.md — temporary bootstrap policy
- decisions/ — guide and template for the **target repository's own** decision register (no GovCheck decisions here)
- docs/architecture/ — guide for the target repository's own architecture records

## Two levels

GovCheck's own governance history (architecture records, ADRs, deliberations) lives at the meta level of the GovCheck repository and is deliberately **not** part of this package. See ADR 0003 in the GovCheck repository.