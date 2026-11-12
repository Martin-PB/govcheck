# Architecture 0034 — Forge-native adapter (govcheck/forge.py): registry mirror and forge-side verification

**Status:** architecture proposal for review; no adapter code, forge configuration or conformance control is implemented by this record. This record complements [ADR 0006](../decisions/0006-vcs-forge-portability.md) and [Specification 0004](../specifications/0004-vcs-collaboration-contracts.md); it does not replace them.  
**Language:** English is the default; see the [French counterpart](0034-forge-native-portfolio-adapter.fr.md).

## 1. Subject and purpose

Define a forge-native adapter owned by the repository, `govcheck/forge.py`, with two roles:

1. **Registry mirror:** synchronize the canonical repository-backed work portfolio (`docs/work-portfolio/`, [Architecture 0030](0030-repository-backed-work-portfolio-and-recoverable-history.md)) with the coordination objects of the forge hosting the repository (issues, PRs, labels, comments).
2. **Forge-side verification:** read the forge verification state (CI check runs, protected-branch rules, required checks) so that `govcheck` can report whether a candidate is protected by shared, non-locally-falsifiable checks.

Everything canonical stays in the repository: the design is forge-independent, targets several forges, and works with no forge at all. When a forge is present, it adds the shared enforcement boundary that local-only checks cannot provide (Specification 0004: local hooks can be bypassed by anyone with filesystem access; strong shared enforcement requires a forge that requires valid checks bound to exact repository state). The forge verifies; it never authorizes.

## 2. Context and motivation

- Architecture 0028/0030 make the repository-backed registry the canonical tracker; forge issues are adapters/projections, and authority flows from the register to the adapter, never the reverse. Synchronization is initially explicit/manual; drift is reported, not silently reconciled.
- ADR 0006 (proposed) already names the third layer: "forge adapter: tracker mirror, CI, identity", with a portable CI pipeline (only the workflow syntax changes per forge). Specification 0004 defines the adapter contracts and states that no adapters are implemented yet.
- The brain.md option (Apache-2.0, npm `@mindmux/brain-md` v0.4.1, repository <https://github.com/mindmuxai/brain.md>) was evaluated and set aside for the agent machine: its zero-dependency Node.js CLI (`bin/brain.mjs`, node >= 18) is unwanted there. This record reuses no brain.md content; if any content is ever reused, it must be attributed in the [reference catalogue](../references.md).
- Issue #118 tracks the implementation of this record (child of #63).

## 3. Architectural decision

Adopt a single stdlib-only adapter module behind a forge-agnostic contract:

1. **Contract:** `govcheck/forge.py` exposes small functions returning plain dicts: `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_labels`, `add_comment`, `list_check_runs`, `get_branch_protection`.
2. **First backend:** GitHub REST v3 over `urllib.request`, with pagination and rate-limit-friendly behavior (minimal requests, no polling loops).
3. **Credentials:** token read only from the environment (`GOVCHECK_FORGE_TOKEN`, falling back to `GITHUB_TOKEN`); never persisted to disk, logs or reports; explicit, redacted error when missing.
4. **Neutrality:** no module outside `forge.py` imports forge-specific code; the `govcheck check` evaluation path stays offline and read-only, needs no token, and never calls the forge.
5. **Testability:** the HTTP transport is injectable, so unit tests and contract tests run fully offline in CI with a fake opener.
6. **Configuration:** forge type, owner and repo via environment variables or CLI flags.
7. **Registry-first mapping:** stable GovCheck IDs (`govcheck.work.<slug>`) are canonical; forge issue numbers are adapter mappings only. Any live synchronization requires lossless round-trip mapping tests (registry ID, native ID, relation direction, history) before use.
8. **Enforcement role:** the adapter reads forge verification state (check runs, branch protection) so a `govcheck check --forge` report can state whether the candidate is covered by required forge-side checks. Changing protection rules is an explicit, audited command. The CI pipeline itself stays portable: same checks, per-forge workflow syntax (GitHub Actions today; GitLab CI, Woodpecker, Forgejo Actions, builds.sr.ht, or local hooks elsewhere). With no forge, governance still applies locally, but enforcement rests on the accepted mainline revision and its review/merge record (Architecture 0030 limitation).

## 4. Adapter contract

| Function | Main input | Output | Notes |
|---|---|---|---|
| `list_issues(state, labels)` | state filter, label filter | list of issue dicts | paginated; registry mapping included |
| `get_issue(number)` | issue number | issue dict | includes body, labels, state |
| `create_issue(title, body, labels)` | title, body, labels | created issue dict | explicit commands only; mirrors a registry work item |
| `update_issue(number, ...)` | number, fields to change | updated issue dict | closures are typed resolutions, not raw edits |
| `list_labels()` | none | list of label names | drives taxonomy checks |
| `add_comment(number, body)` | issue number, markdown body | comment dict | comments are discussion history, not decision records |
| `list_check_runs(ref)` | ref (branch or SHA) | list of check-run dicts | read-only enforcement evidence |
| `get_branch_protection(branch)` | branch name | protection dict | required checks, review rules |

## 5. Safety and governance boundaries

- The check path never mutates forge state and never requires a token.
- Writes (create/update issue, comment, protection change) happen only in explicit commands, with actor identity and rationale recorded in the command output.
- Authority flows from the repository register to the forge projection; forge-side edits never silently overwrite the registry, and drift is reported rather than automatically reconciled (Architecture 0030 section 7).
- The adapter must not infer candidate status, commitment, approval or completion from labels, states, board columns or even green check runs: a green check is evidence, not authority (Specification 0004: comments/reactions are not approvals unless policy says so; a missing enforcement capability is a visible limitation, never a pass).
- Capability declaration and failure taxonomy per Specification 0004: distinguish not-found, unsupported, unavailable, stale, conflict, authentication/authorization failure and malformed state; a partial failure is never reported as an atomic success.
- Export/import mappings must preserve registry IDs, native forge IDs, repository identity, relation direction and history; round-trip tests are required before any live sync.

## 6. Non-goals for this slice

- External CLIs or SDKs (no brain.md CLI, no `gh` dependency, no Node.js runtime).
- Non-GitHub forges (GitLab, Gitea, Codeberg, Pijul nest): the contract allows them, this slice does not implement them.
- Automatic bidirectional synchronization between registry and forge in this slice; Projects v2 structured-field writes.
- Any mutation from `govcheck check`.
- Treating forge checks as authorization: acceptance remains a typed governance event recorded in the repository.

## 7. Verification

- `python3 -m unittest discover -s tests -v` passes with new offline unit and contract tests (fake transport; capability negotiation, stale races, auth failures, partial failures per Specification 0004).
- An import scan asserts `govcheck/forge.py` uses only the Python standard library.
- `govcheck/README.md` and `govcheck/README.fr.md` document the contract and the environment variables.
- The `govcheck-check` CI job remains green and offline.

## 8. References

- [Architecture 0028 — Governed work portfolio and issue-tracker boundary](0028-governed-work-portfolio-and-issue-tracker-boundary.md)
- [Architecture 0030 — Repository-backed work portfolio and recoverable history](0030-repository-backed-work-portfolio-and-recoverable-history.md)
- [ADR 0006 — VCS and forge portability](../decisions/0006-vcs-forge-portability.md)
- [Specification 0004 — VCS and collaboration adapter contracts](../specifications/0004-vcs-collaboration-contracts.md)
- [Issue #118 — Forge-native adapter: govcheck/forge.py](https://github.com/Martin-PB/govcheck/issues/118)
- [Issue #63 — portfolio GitHub adapter and label taxonomy](https://github.com/Martin-PB/govcheck/issues/63)
- [Issue #92 (closed) — forge portability of the GovCheck decision](https://github.com/Martin-PB/govcheck/issues/92)
- brain.md (evaluated, not adopted): <https://github.com/mindmuxai/brain.md> (Apache-2.0)
- [govcheck package README](../../govcheck/README.md)
