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

`govcheck/bootstrap.py` also adopts GovCheck into an existing, non-empty repository without destroying anything:

    python3 govcheck/bootstrap.py inspect TARGET [--out report.json]
    python3 govcheck/bootstrap.py plan TARGET [--capabilities check,docs] [--out plan.json]
    python3 govcheck/bootstrap.py apply TARGET [--capabilities check,docs] [--plan plan.json] [--out result.json]
    python3 govcheck/bootstrap.py rollback TARGET [--out result.json]

- `inspect` reports the package identity (version label plus SHA-256 digest of the package tree), whether the target exists, is empty and is a git repository, which package parts are already present and which paths would conflict. It never mutates the target.
- `plan` produces a deterministic JSON plan of actions (`create`, `identical`, `conflict`) with no side effect; running it twice on an unchanged target yields byte-identical output.
- `apply` writes only `create` actions: existing files are never overwritten, conflicts are preserved and reported. Applying twice is idempotent (the second run creates nothing). With `--plan`, apply first verifies that the plan still matches the target and aborts with exit code 2 otherwise, so only reviewed changes are applied.
- The package identity is recorded in a package-owned marker, `.govcheck-bootstrap.json`, at the target root (version, digest, installed files with digests, preserved conflicts). `rollback` deletes exactly the installed files whose content still matches the recorded digest and then the marker; that is the documented rollback path. Upgrading means re-running `apply` with a newer package: user-modified files are never overwritten and appear as conflicts.
- `--capabilities` selects which package parts to install (`check`, `forge`, `decisions`, `docs`, `formal`, `readme`, `scripts`, `workflows`; default: all of them).

The legacy form `python3 govcheck/bootstrap.py TARGET_DIR` still initializes an empty repository and refuses non-empty targets. Unit tests live in `tests/test_govcheck_bootstrap.py`.

## Checking a repository (first executable slice)

`govcheck/check.py` is the first executable GovCheck command. It evaluates a fixed rule set on a repository tree and emits a deterministic, language-independent JSON report:

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Each rule returns `pass`, `fail` or `unknown`. The overall result is `fail` if any rule fails, otherwise `unknown` if any rule is unknown, otherwise `pass` (fail-closed: `unknown` never counts as a success). The exit code is 0 only when the overall result is `pass`. The rules span the three assurance classes: decidable (license presence, bilingual decision pairs, manifest-declared package pairs, reference-catalogue integrity, mandatory sources on decisions and attestations, bootstrap-marker integrity), attested (independent review) and not verifiable offline (TLC evidence freshness). Unit tests live in `tests/test_govcheck_check.py`.


### Recorded attestations (independent review)

In git mode (`--base/--candidate`), the `independent-review` rule becomes `pass` when a JSON record in `docs/attestations/*.json` carries `"decision": "accept"`, the exact full SHA of the candidate revision in `candidate_rev`, and a `reviewer` identity distinct from the candidate commit author. Otherwise the rule stays `unknown` (fail-closed).

### Mandatory sources (ADR 0007)

The `sources-present` rule (decidable) requires every non-guide `docs/decisions/*.md` to carry a `## References` (or `## Références`) section containing at least one source link: a reference-catalogue anchor (`docs/references.md#r-xx`) or an external URL. Every attestation record in `docs/attestations/*.json` must also carry a non-empty `"sources"` list of strings, listing the evidence the reviewer relied on. Guide files (`README*`, `TEMPLATE*`) are exempt. Without this, an agent could state a decision without any evidence; the rule makes "no source, no decision" enforceable offline.

### Bootstrap marker integrity

The `bootstrap-integrity` rule (decidable) checks the package-owned marker `.govcheck-bootstrap.json` written by `govcheck/bootstrap.py apply` at the target root. Without the marker the rule is not applicable (pass, not applicable). With the marker, it must be a JSON object with `"tool": "govcheck-bootstrap"`, a non-empty `"package_version"`, a `"package_digest"` that is a 64-character lowercase hex SHA-256, an `"installed"` list of `{path, sha256}` entries and a `"conflicts"` list of non-empty strings. Each installed path must be relative and safe (no absolute path, no backslash, no `.`/`..`/empty segment), and each installed file must still exist with exactly the recorded SHA-256 digest. Any schema violation, missing file or content drift fails the rule. The marker is a repository document, not a tamper-proof seal: it detects accidental drift, not a malicious editor.


## Forge adapter (govcheck/forge.py)

govcheck/forge.py is the forge-native adapter (Architecture 0034 of the GovCheck repository) with two roles: a **registry mirror** that projects the repository-canonical work portfolio onto forge issues, labels and comments, and **forge-side verification** that reads CI check runs and branch protection so a report can state whether a candidate revision is covered by shared, not-locally-falsifiable verifications. The forge verifies, it never authorizes: a green check is evidence, not authority. The check command stays offline, read-only and token-free and never calls the adapter.

    python3 govcheck/forge.py list-issues [--state open] [--labels a,b]
    python3 govcheck/forge.py get-issue --number N
    python3 govcheck/forge.py list-labels
    python3 govcheck/forge.py check-runs --ref REF
    python3 govcheck/forge.py branch-protection [--branch main]
    python3 govcheck/forge.py create-issue --title T [--body B] [--labels a,b] [--registry-id govcheck.work.slug]
    python3 govcheck/forge.py update-issue --number N [--title T] [--state open|closed]
    python3 govcheck/forge.py comment --number N --body B
    python3 govcheck/forge.py capabilities

Configuration comes from the environment only: GOVCHECK_FORGE (default github), GOVCHECK_FORGE_OWNER, GOVCHECK_FORGE_REPO, and the token GOVCHECK_FORGE_TOKEN (fallback GITHUB_TOKEN). Tokens are never written to disk, logs or reports, and error messages never carry them. Writes (create-issue, update-issue, comment) require a token and are explicit commands only; check never mutates the forge. The adapter is standard library only (GitHub REST v3 first) with an injectable transport, so unit tests run fully offline; failures are typed (not-found, unsupported, unavailable, stale, conflict, auth, malformed) and a partial failure is never reported as an atomic success. Registry ids (govcheck.work.<slug>) stay canonical; lossless round-trip tests are required before any live sync. Unit tests live in tests/test_govcheck_forge.py. The forge bootstrap capability installs forge.py alone.
