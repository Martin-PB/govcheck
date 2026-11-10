# ADR 0006 — VCS and forge portability of the GovCheck decision

**Status:** proposed; records the transposability analysis of 2026-11-10 answering the owner's question: "is our decision easily portable to the Pijul ecosystem, or even outside GitHub?" Pending explicit owner decision. **French:** [0006 (français)](0006-vcs-forge-portability.fr.md).

## Context

The adopted design has four pillars: (1) the repository-backed governed work portfolio is the source of truth, with forge issues as a coordination adapter only (Architecture 0028, 0030); (2) a human-controlled acceptance boundary: no merge without explicit maintainer approval, and fail-closed evaluation where unknown is never a success (`govcheck check`, PRs #38 and #87); (3) independent-review attestations recorded in `docs/attestations/*.json` and bound to the exact candidate revision (full 40-hex git SHA in `candidate_rev`); (4) the two-level `govcheck/` package (ADR 0003).

The current executable slice (`govcheck/check.py`, v0.2.0-slice) is coupled to git and GitHub at three points: it shells out to the git CLI (`diff --name-only base...candidate`, `rev-parse`, `log -1 --format=...`), attestations pin a 40-hex SHA-1, and the dogfooding pipeline is a GitHub Actions workflow (`.github/workflows/govcheck-check.yml`, meta-only; hosted CI authorized in issue #88).

The project principles (README) already commit to being "independent of coding agent, version-control system, hosting provider, forge" and state that "Git and Pijul are first-class and semantically distinct"; Specification 0004 defines VCS and collaboration adapter contracts. This ADR answers whether the adopted pillars hold beyond git/GitHub, and what must change.

## Decision (proposed)

Keep three layers strictly separate:

1. **VCS/forge-agnostic core, portable as-is.** The `govcheck/` package, the manifest-declared pairs (ADR 0003), the decidable rules (`license-present`, `bilingual-decisions`, `manifest-pairs`, `reference-integrity`), the fail-closed semantics (fail > unknown > pass; exit code 0 only on pass), the JSON report, and the attestation records in `docs/attestations/`. The human/agent acceptance boundary is a written policy, not code.
2. **VCS adapter: small interface, one implementation per VCS.** `check.py` resolves revisions through a `VcsAdapter` with exactly three operations: `list_changed(base, candidate) -> [paths]`, `resolve_rev(rev) -> rev_id`, `author_of(rev) -> identity`. `GitAdapter` is the reference implementation today. A `PijulAdapter` maps them to `pijul diff --channel <CHANNEL>`, `pijul log --output-format json` and `pijul change <HASH>`. Attestation binding generalizes from a bare 40-hex SHA to a typed revision reference `{"vcs": "git" | "pijul" | ..., "rev": "<native id>"}`.
3. **Forge adapter: tracker mirror, CI, identity.** The tracker remains the repository-backed portfolio; the forge adapter only mirrors coordination (issues/PRs/discussions) and runs CI. The CI pipeline itself (blocking unit tests + report-only `govcheck check` + uploaded report artifact) is portable; only the workflow syntax changes (GitHub Actions, GitLab CI, Forgejo Actions or Woodpecker, builds.sr.ht, or local hooks).

### Transposability matrix

| Element | git + GitHub (today) | Other git forges | Pijul | Fossil / Mercurial |
|---|---|---|---|---|
| `govcheck/` package, decidable rules, fail-closed, JSON report | as-is | as-is | as-is | as-is |
| Attestations `docs/attestations/*.json` | as-is | as-is | schema: `candidate_rev` becomes typed `{vcs, rev}` | same schema change |
| Human acceptance boundary (policy) | as-is | as-is | as-is | as-is |
| Revision access in `check.py` | git CLI | git CLI | `pijul diff --channel`, `pijul log --output-format json`, `pijul change` | `fossil diff --from` / `fossil info`; `hg` equivalents |
| Tracker as source of truth | issues/PRs API + branch protection | GitLab issues/MRs + approvals; Forgejo/Gitea GitHub-compatible API | nest discussions; no native required-check | Fossil tickets; SourceHut mailing-list patch review |
| Blocking check + demonstrated refusal | required status check | pipeline must succeed / MR approval | nest CI job + explicit channel rule | external CI + ticket status |
| CI workflow | Actions YAML | GitLab CI / Woodpecker / Forgejo Actions / builds.sr.ht | Woodpecker or external CI | external CI |
| Identity | forge login | forge login / signed commits | SSH keys | Fossil user / SSH |

### Pijul specifics

- Pijul is patch-based, not commit-based: there is no SHA-1. Changes have base32 IDs (e.g. `TQU67HU5...`), addressable by unambiguous prefix; `pijul change <HASH>` shows author and date.
- Channels are the analogue of branches but are mutable (rebasable): an attestation must pin the exact change ID, never the channel name, exactly as git mode pins the commit SHA.
- `pijul diff --channel <CHANNEL>` compares against another channel (or the working copy); `pijul log --output-format json` gives machine-readable history.
- nest.pijul.com hosts code, discussions and CI jobs, but has no GitHub-style "required status check on a pull request": the blocking-check pattern maps to a nest CI job plus an explicit rule in the channel discussions.
- Identity is SSH-key based, not login based.

## Consequences

- `check.py` keeps its CLI (`--tree/--base/--candidate/--out`) and detects the VCS (git today; explicit `--vcs pijul` later); the core must not import VCS-specific code outside the adapter.
- Attestation schema v2: `candidate_rev` becomes `{"vcs": ..., "rev": ...}`; the legacy bare 40-hex string stays accepted during the 0.x slice for backward compatibility.
- The adapter interface is deliberately limited to three operations: each additional VCS is a new adapter, never a change to the core.
- No migration of this repository is implied; the ADR makes the design portable, it does not move the project.
- Works with no forge at all: `govcheck check --tree .` runs locally and the in-repo attestations remain valid; only the external coordination mirror disappears, and the repository-backed portfolio is already the canonical tracker.

## Out of scope (follow-up work)

- Implementing `PijulAdapter` (issue #58 already explores git/Pijul collaboration semantics; Specification 0004 defines the contracts).
- Choosing or adding a second forge for this repository.
- Migrating the govcheck repository itself to Pijul, Fossil or Mercurial.
- Contribution sign-off (DCO) and cryptographic signing of attestations.

## References

- [Specification 0004 — VCS and collaboration adapter contracts](../specifications/0004-vcs-collaboration-contracts.md)
- [ADR 0003 — two-level governance](0003-two-level-governance.md); [ADR 0005 — license (Pijul already listed as an external GPL tool)](0005-license-apache-2-0-with-individual-attribution.md)
- [Architecture 0028 — governed work portfolio and issue-tracker boundary](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.md)
- [Pijul manual — channels](https://pijul.org/manual/workflows/channels.html); [pijul diff](https://pijul.org/manual/reference/diff.html); [pijul change](https://pijul.org/manual/reference/change.html)
- [Pijul discourse — `pijul log --output-format json`](https://discourse.pijul.org/t/how-to-efficiently-query-dependencies-for-all-changes/862)
- [nest.pijul.com](https://nest.pijul.com/)
- [GitLab Docs — SLSA level 3](https://docs.gitlab.com/ci/pipeline_security/slsa/level_3/)
- [Woodpecker CI — Forgejo configuration](https://woodpecker-ci.org/docs/next/administration/configuration/forges/forgejo)
- [SourceHut](https://sourcehut.org/); [Fossil web interface](https://fossil-scm.org/home/doc/2026-06-23/www/webui.wiki)
- Issues #58 (git/Pijul semantics), #88 (hosted CI authorization), #92 (tracking issue for this ADR)
