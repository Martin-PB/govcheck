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

## Bootstrapping an existing repository (inspect / plan / apply)

`govcheck/bootstrap.py` also adopts GovCheck into an 
existing, non-empty repository without destroying anything:

    python3 govcheck/bootstrap.py inspect TARGET [--out report.json]
    python3 govcheck/bootstrap.py plan TARGET [--capabilities check,docs] [--out plan.json]
    python3 govcheck/bootstrap.py apply TARGET [--capabilities check,docs] [--plan plan.json] [--out result.json]
    python3 govcheck/bootstrap.py rollback TARGET [--out result.json]

- `inspect` reports the package identity (version label plus SHA-256 digest of the package tree), whether the target exists, is empty and is a git repository, which package parts are already present and which paths would conflict. It never mutates the target.
- `plan` produces a deterministic JSON plan of actions (`create`, `identical`, `conflict`) with no side effect; running it twice on an unchanged target yields byte-identical output.
- `apply` writes only `create` actions: existing files are never overwritten, conflicts are preserved and reported. Applying twice is idempotent (the second run creates nothing). With `--plan`, apply first verifies that the plan still matches the target and aborts with exit code 2 otherwise, so only reviewed changes are applied.
- The package identity is recorded in a package-owned marker, `.govcheck-bootstrap.json`, at the target root (version, digest, installed files with digests, preserved conflicts). `rollback` deletes exactly the installed files whose content still matches the recorded digest and then the marker; that is the documented rollback path. Upgrading means re-running `apply` with a newer package: user-modified files are never overwritten and appear as conflicts.
- `--capabilities` selects which package parts to install (`check`, `decisions`, `docs`, `formal`, `readme`, `scripts`, `workflows`; default: all of them).

The legacy form `python3 govcheck/bootstrap.py TARGET_DIR` still initializes an empty repository and refuses non-empty targets. Unit tests live in `tests/test_govcheck_bootstrap.py`.

## Checking a reposito
ry (first executable slice)

`govcheck/check.py` is the first executable GovCheck command. It evaluates a fixed rule set on a repository tree and emits a deterministic, language-independent JSON report:

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Each rule returns `pass`, `fail` or `unknown`. The overall result is `fail` if any rule fails, otherwise `unknown` if any rule is unknown, otherwise `pass` (fail-closed: `unknown` never counts as a success). The exit code is 0 only when the overall result is `pass`. The rules span the three assurance classes: decidable (license presence, bilingual decision pairs, manifest-declared package pairs, reference-catalogue integrity, mandatory sources on decisions and attestations, bootstrap-marker integrity), attested (independent review) and not verifiable offline (TLC evidence freshness). Unit tests live in `tests/test_govcheck_check.py`.


### Recorded attestations (independent review)

In git mode (`--base/--candidate`), the `independent-review` rule becomes `pass` when a JSON record in `docs/attestations/*.json` carries `"decision": "accept"`, the exact full SHA of the candidate revision in `candidate_rev`, and a `reviewer` identity distinct from the candidate commit author. Otherwise the rule stays `unknown` (fail-closed).

### Mandatory sources (ADR 0007)

The `sources-present` rule (decidable) requires every non-guide `docs/decisions/*.md` to carry a `## References` (or `## Références`) section containing at least one source link: a reference-catalogue anchor (`docs/references.md#r-xx`) or an external URL. Every attestation record in `docs/attestations/*.json` must also carry a non-empty `"sources"` list of strings, listing the evidence the reviewer relied on. Guide files (`README*`, `TEMPLATE*`) are exempt. Without this, an agent could state a decision without any evidence; the rule makes "no source, no decision" enforceable offline.

### Bootstrap marker integrity

When the repository root contains the package-owned marker `.govcheck-bootstrap.json` (written by `govcheck/bootstrap.py apply`), the `bootstrap-integrity` rule checks that:

- the marker is valid JSON and a JSON object;
- `tool` equals `govcheck-bootstrap`, `package_version` is a non-empty string and `package_digest` is a 64-character lowercase hex SHA-256;
- `installed` is a list of `{path, sha256}` entries where each path is relative and safe (no absolute path, no backslash, no empty/`.`/`..` segment), each `sha256` is 64-char lowercase hex, and each recorded file exists with exactly that digest (missing file or content drift fails);
- `conflicts` is a list of non-empty strings.

Any problem fails the rule. Without the marker at the tree root the rule is not applicable and reports `pass` with `applies: false`.
