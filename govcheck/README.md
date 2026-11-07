# GovCheck governance package

**Français :** [README.fr.md](README.fr.md)

This folder is the **only** part of the GovCheck repository meant to be copied into another repository to govern it. Run `python3 govcheck/bootstrap.py TARGET_DIR` (or copy govcheck/ as-is into the target repository's root) and follow the bootstrap policy.

## Independent release versions

The repository release, the GovCheck product release and the reusable **govcheck/** governance-package release are distinct identities. The product and package have independent SemVer contracts; a product release may pin a package release but does not assign or increment its version. The planned first GovCheck product baseline is **0.1.0**, not yet published or authorized. The reusable package's first version is independent and remains unassigned until its own initial-publication decision and immutable release manifest exist. See the repository's ADR 0004 and Architecture 0017–0018.


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