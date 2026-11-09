# GovCheck governance package

**Fran`"ais :** [README.fr.md](README.fr.md)

This folder is the **only** part of the GovCheck repository meant to be copied into another repository to govern it. Run `python3 govcheck/bootstrap.py TARGET_DIR` (or copy govcheck/ as-is into the target repository's root) and follow the bootstrap policy.

## Independent release versions

The repository release, the GovCheck product release and the reusable **govcheck/** governance-package release are distinct identities. The product and package have independent SemVer contracts; a product release may pin a package release but does not assign or increment its version. The planned first GovCheck product baseline is **0.1.0**, not yet published or authorized. The reusable package's first version is independent and remains unassigned until its own initial-publication decision and immutable release manifest exist. See the repository's ADR 0004 and Architecture 0017`2013`0018.


## Contents (planned layout)

- specifications/ `2014` normative governance specifications (bilingual, English default)
- formal/ `2014` lifecycle model (TLA+), transition registry, artifact catalogue, JSON schemas
- docs/formal/ `2014` lifecycle model documentation and generated diagram
- scripts/ `2014` deterministic diagram generator and drift check
- .github/workflows/ `2014` CI workflow template (kept in sync with the meta repository by a check)
- BOOTSTRAP_GOVERNANCE.md `2014` temporary bootstrap policy
- decisions/ `2014` guide and template for the **target repository's own** decision register (no GovCheck decisions here)
- docs/architecture/ `2014` guide for the target repository's own architecture records

## Two levels

GovCheck's own governance history (architecture records, ADRs, deliberations) lives at the meta level of the GovCheck repository and is deliberately **not** part of this package. See ADR 0003 in the GovCheck repository.

## Checking a repository (first executable slice)

`govcheck/check.py` is the first executable GovCheck command. It evaluates a fixed rule set on a repository tree and emits a deterministic, language-independent JSON report:

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Each rule returns `pass`, `fail` or `unknown`. The overall result is `fail` if any rule fails, otherwise `unknown` if any rule is unknown, otherwise `pass` (fail-closed: `unknown` never counts as a success). The exit code is 0 only when the overall result is `pass`. The rules span the three assurance classes: decidable (license presence, bilingual decision pairs, manifest-declared package pairs, reference-catalogue integrity), attested (independent review) and not verifiable offline (TLC evidence freshness). Unit tests live in `tests/test_govcheck_check.py`.


### Recorded attestations (independent review)

In git mode (`--base/--candidate`), the `independent-review` rule becomes `pass` when a JSON record in `docs/attestations/*.json` carries `"decision": "accept"`, the exact full SHA of the candidate revision in `candidate_rev`, and a `reviewer` identity distinct from the candidate commit author. Otherwise the rule stays `unknown` (fail-closed).
