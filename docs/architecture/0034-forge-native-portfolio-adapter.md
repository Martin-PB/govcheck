# Architecture 0034 — Forge-native portfolio adapter (govcheck/forge.py)

**Status:** architecture proposal for review; no adapter code, forge configuration or conformance control is implemented by this record.  
**Language:** English is the default; see the [French counterpart](0034-forge-native-portfolio-adapter.fr.md).

## 1. Subject and purpose

Define a forge-native adapter owned by the repository, `govcheck/forge.py`, so that GovCheck commands can read, and in explicit dedicated commands write, the governed work portfolio on the forge hosting the repository, without depending on any external CLI, SDK or non-stdlib runtime.

This record applies the adapter-neutrality invariant (#12) of [Architecture 0028](0028-governed-work-portfolio-and-issue-tracker-boundary.md) at the tooling layer: forge-specific fields and behavior must not become canonical governance semantics.

## 2. Context and motivation

- Architecture 0028 makes GitHub the initial operational adapter, not the canonical model; issue #63 configures the GitHub side (label taxonomy, Projects views); closed issue #92 already covered forge portability of the decision record.
- The brain.md option (Apache-2.0, npm `@mindmux/brain-md` v0.4.1, repository <https://github.com/mindmuxai/brain.md>) was evaluated and set aside for the agent machine: its zero-dependency Node.js CLI (`bin/brain.mjs`, node >= 18) is unwanted there. This record reuses no brain.md content; if any content is ever reused, it must be attributed in the [reference catalogue](../references.md).
- Issue #118 tracks the implementation of this record.

## 3. Architectural decision

Adopt a single stdlib-only adapter module behind a forge-agnostic contract:

1. **Contract:** `govcheck/forge.py` exposes small functions returning plain dicts: `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_labels`, `add_comment`.
2. **First backend:** GitHub REST v3 over `urllib.request`, with pagination and rate-limit-friendly behavior (minimal requests, no polling loops).
3. **Credentials:** token read only from the environment (`GOVCHECK_FORGE_TOKEN`, falling back to `GITHUB_TOKEN`); never persisted to disk, logs or reports; explicit, redacted error when missing.
4. **Neutrality:** no module outside `forge.py` imports forge-specific code; the `govcheck check` evaluation path stays offline and read-only, with no forge calls.
5. **Testability:** the HTTP transport is injectable, so unit tests run fully offline in CI with a fake opener.
6. **Configuration:** forge type, owner and repo via environment variables or CLI flags.

## 4. Adapter contract

| Function | Main input | Output | Notes |
|---|---|---|---|
| `list_issues(state, labels)` | state filter, label filter | list of issue dicts | paginated |
| `get_issue(number)` | issue number | issue dict | includes body, labels, state |
| `create_issue(title, body, labels)` | title, body, labels | created issue dict | explicit commands only |
| `update_issue(number, ...)` | number, fields to change | updated issue dict | closures are typed resolutions, not raw edits |
| `list_labels()` | none | list of label names | drives taxonomy checks |
| `add_comment(number, body)` | issue number, markdown body | comment dict | comments are discussion history, not decision records |

## 5. Safety and governance boundaries

- The check path never mutates forge state and never requires a token.
- Writes (create/update issue, comment) happen only in explicit commands, with actor identity and rationale recorded in the command output.
- The adapter must not infer candidate status, commitment, approval or completion from labels, states or board columns (Architecture 0028 section 7); it only transports data.
- Export/import mappings must preserve native IDs, repository identity, relation direction and history (Architecture 0028 section 7).

## 6. Non-goals for this slice

- External CLIs or SDKs (no brain.md CLI, no `gh` dependency, no Node.js runtime).
- Non-GitHub forges (GitLab, Gitea, Codeberg): the contract allows them, this slice does not implement them.
- Projects v2 structured-field writes; automatic synchronization between forge and registry.
- Any mutation from `govcheck check`.

## 7. Verification

- `python3 -m unittest discover -s tests -v` passes with new offline tests (fake transport).
- An import scan asserts `govcheck/forge.py` uses only the Python standard library.
- `govcheck/README.md` and `govcheck/README.fr.md` document the contract and the environment variables.
- The `govcheck-check` CI job remains green and offline.

## 8. References

- [Architecture 0028 — Governed work portfolio and issue-tracker boundary](0028-governed-work-portfolio-and-issue-tracker-boundary.md)
- [Issue #118 — Forge-native portfolio adapter: govcheck/forge.py](https://github.com/Martin-PB/govcheck/issues/118)
- [Issue #63 — portfolio GitHub adapter and label taxonomy](https://github.com/Martin-PB/govcheck/issues/63)
- [Issue #92 (closed) — forge portability of the GovCheck decision](https://github.com/Martin-PB/govcheck/issues/92)
- brain.md (evaluated, not adopted): <https://github.com/mindmuxai/brain.md> (Apache-2.0)
- [govcheck package README](../../govcheck/README.md)
