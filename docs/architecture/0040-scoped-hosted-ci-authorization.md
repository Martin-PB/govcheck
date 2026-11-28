# 0040 — Scoped authorization for hosted CI in the public GovCheck repository

**Status:** accepted operational authorization, recorded 2026-11-28 from the maintainer's explicit statement of 2026-11-09. This is not a normative governance-model adoption.

## Context

The temporary bootstrap policy prohibits hosted CI without explicit authorization. The maintainer explicitly authorized use of hosted GitHub Actions for the public repository `Martin-PB/govcheck`, stating that the public-repository runs do not consume their personal Actions credit quota and may be used without limit.

## Decision and scope

Until revoked, this authorization permits ChatGPT/agents working on this repository to run GitHub Actions for repository CI, tests, formal-model checks and reproducibility workflows, including validation runs needed to complete repository work.

The authorization applies **only** to the public repository:

- `Martin-PB/govcheck`

It does not extend to other personal or organization repositories.

## Exclusions

This authorization does **not** permit:

- merging a pull request without the maintainer's applicable approval;
- bypassing branch protection or changing rulesets, required checks, secrets, variables or repository permissions;
- creating, installing or configuring a GitHub App or external service on the maintainer's behalf;
- exposing, creating or rotating private keys, credentials or signing secrets;
- running deployment, release-publication or external-account mutation workflows;
- treating a green CI result as normative adoption, independent review, formal proof of implementation or effective protected-ref enforcement.

Only validation/reproduction workflows that are read-only with respect to external services and repository administration are covered. Any workflow with a new external side effect requires separate authorization.

## Revocation and review

The maintainer may revoke or narrow this authorization at any time. Reassess it if the repository becomes private, is transferred, changes ownership/organization, or if the relevant Actions/account settings materially change.

## Source and related records

- Explicit maintainer authorization recorded in issue [#88](https://github.com/Martin-PB/govcheck/issues/88), dated 2026-11-09.
- Temporary bootstrap policy: [BOOTSTRAP_GOVERNANCE.md](../BOOTSTRAP_GOVERNANCE.md).
- Current ruleset and effective acceptance limitations: issue [#45](https://github.com/Martin-PB/govcheck/issues/45).

This record formalizes the existing scoped authorization; it does not create authorization for any other repository or action.
