# GovCheck governance package

**Fran`"ais :** [README.fr.md](README.fr.md)

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

## Checking a repository (first executable slice)

`govcheck/check.py` is the first executable GovCheck command. It evaluates a fixed rule set on a repository tree and emits a deterministic, language-independent JSON report:

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Each rule returns `pass`, `fail` or `unknown`. The overall result is `fail` if any rule fails, otherwise `unknown` if any rule is unknown, otherwise `pass` (fail-closed: `unknown` never counts as a success). The exit code is 0 only when the overall result is `pass`. The rules span the three assurance classes: decidable (license presence, bilingual decision pairs, manifest-declared package pairs, reference-catalogue integrity, mandatory sources on decisions and attestations), attested (independent review) and not verifiable offline (TLC evidence freshness). Unit tests live in `tests/test_govcheck_check.py`.


### Recorded attestations (independent review)

In git mode (`--base/--candidate`), the `independent-review` rule becomes `pass` when a JSON record in `docs/attestations/*.json` carries `"decision": "accept"`, the exact full SHA of the candidate revision in `candidate_rev`, and a `reviewer` identity distinct from the candidate commit author. Otherwise the rule stays `unknown` (fail-closed).

### Mandatory sources (ADR 0007)

The `sources-present` rule (decidable) requires every non-guide `docs/decisions/*.md` to carry a `## References` (or `## Références`) section containing at least one source link: a reference-catalogue anchor (`docs/references.md#r-xx`) or an external URL. Every attestation record in `docs/attestations/*.json` must also carry a non-empty `"sources"` list of strings, listing the evidence the reviewer relied on. Guide files (`README*`, `TEMPLATE*`) are exempt. Without this, an agent could state a decision without any evidence; the rule makes "no source, no decision" enforceable offline.
