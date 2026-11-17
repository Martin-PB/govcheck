# Repository acceptance-boundary enforcement research

**Status:** research synthesis and design proposal for issue [#45](https://github.com/Martin-PB/govcheck/issues/45). Not an adopted policy, implementation claim or forge configuration change.

## Executive result

The current GovCheck evaluator can produce a fail-closed logical result, but a logical result is not an effective repository boundary. A mandatory gate exists only when every relevant write path to the governed target is intercepted by a trusted adapter that checks the exact candidate and rejects an unaccepted result.

The existing Architecture 0015 already distinguishes the verification core, repository-boundary enforcement and forge-specific integration as separate responsibilities. This research refines the operational boundary without introducing a hosted MCP service or making a forge the normative authority.

**Key finding:** the most portable strong Git boundary is a server-controlled `pre-receive` hook on a bare repository. SaaS forges generally expose platform-specific merge gates (rulesets, protected branches, required checks); these do not necessarily block direct pushes unless branch rules are configured. Pijul's documented local hook currently runs before `pijul record`; the official manual does not document a mandatory remote pre-push/pre-receive hook. The Nest permits authorized direct pushes or attaching changes to a discussion. A mandatory Pijul gate therefore needs a controlled remote/server integration, not merely a local hook. [R-221](../references.md#r-221), [R-222](../references.md#r-222), [R-223](../references.md#r-223), [R-224](../references.md#r-224), [R-225](../references.md#r-225), [R-226](../references.md#r-226)

## 1. Terms that must not be conflated

- **Verification:** GovCheck evaluates a candidate against a specific governance revision and returns evidence and a result.
- **Attestation:** a provenance-bearing statement binding the result to the candidate, base, policy, verifier, inputs and evidence.
- **Acceptance decision:** an authorized decision to permit or reject a repository operation. It may record accepted risk without changing the underlying verification result.
- **Enforcement:** a repository/forge adapter actually prevents the relevant ref/channel update or merge unless the acceptance decision permits it.
- **Observation/reporting:** a result is displayed or stored but does not prevent publication. This is not enforcement.

The enforcement placements below are **different locations and capabilities, not maturity levels**.

## 2. Enforcement placement comparison

| Placement | Can stop the target update? | Trust boundary | Main limitation |
|---|---|---|---|
| Local CLI | No, by itself | User-controlled process | A user can omit the command or invoke VCS directly. |
| Client hook/wrapper | Only for the intercepted client command | User-controlled machine and configuration | Hooks may be absent, replaced or bypassed; they do not control other clients or transports. |
| Forge merge gate | Yes, for merges covered by protected-branch/ruleset policy | Forge policy plus trusted check source | Direct pushes need separate restrictions; administrators and bypass actors remain part of the threat model. |
| Server-side Git `pre-receive` | Yes, for ref updates received by that repository | Server administrator controls hook and verifier | Does not stop direct filesystem/ref changes by a server administrator; requires control of the Git server. |
| Pijul Nest workflow | ACL can restrict who may push; discussions can support review | Nest permissions and repository owner | The documented local hook is only before `record`; no conditional remote acceptance hook is documented. |

### 2.1 GitHub

Rulesets and protected branches can require status checks and pull requests. A required status check can select an expected GitHub App source; this matters because GitHub documents that any person or integration with write permission can set a status. Strict checks bind the branch to the latest base; loose checks reduce rebuilds but can become stale after merge. Bypass permissions must be explicitly reviewed. [R-221](../references.md#r-221)

For GovCheck, a required status name alone is insufficient. The expected source must be a trusted verifier integration, and the result must bind the exact candidate and base. A workflow definition or evaluator taken uncritically from the candidate branch is not a trust root. A merge-queue/test-merge candidate must be verified as the actual candidate being integrated, or re-evaluated after the merge result is formed.

### 2.2 GitLab

Protected branches govern who can push or merge. External status checks are bound to the current merge-request HEAD; stale responses are rejected with HTTP 409 and HMAC authentication is supported. However, failed external checks do not block merges by default: the project must enable **Status checks must succeed**. The external status-check capability is tier-dependent (Ultimate). [R-222](../references.md#r-222)

### 2.3 Gitea

Gitea protected-branch rules are enforced across HTTP(S), SSH, the web editor, API and background auto-merge. The server rejects blocked pushes; rules cover direct push, force-push, approvals and required status checks. Administrator behavior must be configured deliberately. [R-223](../references.md#r-223)

### 2.4 Forgejo

Forgejo's own Actions security guidance warns that branch protection on `main` is not sufficient to make workflow execution trusted: a user able to push to an unprotected branch can add a workflow that executes on that branch. Runner registration scope, workflow provenance, ephemeral execution and isolation are separate controls from merge protection. [R-224](../references.md#r-224)

### 2.5 Controlled Git servers and local bare repositories

Git's server-side `pre-receive` hook runs once for a receive operation, receives every proposed old/new object ID and full ref name, and rejects the proposed ref updates when it exits nonzero. This is the strongest native repository-boundary prototype for a controlled Git server or local/team bare repository. A client-side `pre-push` hook is useful feedback, not an enforceable boundary. [R-225](../references.md#r-225)

The hook and verifier must be installed outside the candidate tree and controlled by the repository/server administrator. A candidate must not be able to replace the verifier that evaluates it. A server administrator or process with direct filesystem/ref access can still bypass or replace the hook; the guarantee must state that assumption.

### 2.6 Pijul and the Nest

The Pijul manual documents repository hooks before `pijul record` and currently says that only the `record` hook is supported. The Nest permits direct push for users with repository permission, or a contribution path that attaches changes to a discussion channel. [R-226](../references.md#r-226)

A local record hook or wrapper cannot enforce remote acceptance: another client can push directly. A mandatory Pijul boundary requires a controlled remote/server adapter that intercepts the channel update or patch application. No such general Nest hook is documented by the cited manual. Until that exists, the Nest integration must be described as review/ACL support, not GovCheck enforcement.

## 3. Proposed decision-envelope contract

The following is a design target, not an adopted schema:

| Field group | Required meaning |
|---|---|
| Subject | VCS kind, repository identity, native candidate identity, content/tree/change-set digest, target ref/channel |
| Base | VCS-native base identity and content digest used for evaluation |
| Governance | Exact governance package/revision/digest and applicable profile |
| Verifier | Verifier identity, version, executable digest, configuration digest and trust basis |
| Outcome | `PASS`, `FAIL`, `UNKNOWN`, `CONFLICT`, or `ACCEPTED_WITH_RISK` |
| Evidence | Evidence identities/digests, method class (test, model check, proof check, inspection, etc.), scope, assumptions and limitations |
| Decision | Stable decision ID, authority identity/provenance, decision time, scope and expiry |
| Risk acceptance | Separate record with reason, affected claim/requirement, scope, residual risk, authority and expiry; absent unless explicitly authorized |
| Provenance | Signature or equivalent authenticated origin, plus the trust root used by the adapter |

Git commit/tree identities and Pijul channel/change-set identities must remain VCS-native. A content digest may aid comparison but must not be treated as semantic equivalence between VCSs without a proven mapping. The envelope must be external to the candidate commit/tree it attests to, or held in an append-only governance journal, to avoid the self-reference defect identified in issue #44.

## 4. Default decision semantics proposed for the prototype

1. `PASS` is emitted only when every mandatory applicable rule passes and the evidence is fresh, correctly scoped and authenticated against the configured verifier.
2. `FAIL`, `UNKNOWN` and `CONFLICT` block by default. An unavailable verifier, missing evidence, stale base, stale policy or untrusted status source is `UNKNOWN`, not `PASS`.
3. An explicit authorized exception or risk acceptance may permit a separately recorded **accepted-with-risk** operation if the governing policy permits it. It must never rewrite the underlying `FAIL` or `UNKNOWN` into `PASS`.
4. Every acceptance binds the exact candidate, base, governance revision, verifier and target ref/channel. Any change to these inputs invalidates the prior gate result.
5. A bypass is a distinct, attributable and auditable event. It is not a successful verification.
6. If the adapter cannot intercept all relevant write paths, its result is advisory and must not be described as effective enforcement.
7. The merge result itself must be checked when it differs from the reviewed head. A stale green check on a different candidate is not transferable evidence.

This is a proposed contract for formalization; it does not adopt a new authority regime or decide who may grant an exception.

## 5. Adapter capability declaration

Every adapter should declare, rather than imply, its capabilities:

- `can_block_merge`
- `can_block_direct_push`
- `can_bind_exact_candidate`
- `can_bind_current_base`
- `can_reject_stale_result`
- `can_pin_trusted_verifier_source`
- `can_record_bypass`
- `can_revalidate_merge_result`
- `can_enforce_all_supported_transports`

A deployment that cannot block direct pushes must say so. A GitHub merge gate, for example, is not automatically a gate on SSH pushes unless branch protection/rulesets deny them. A local CLI is not a mandatory gate. A Pijul Nest discussion is not a server-side policy hook.

## 6. Candidate implementation sequence

1. Formalize the envelope and transition semantics, including stale evidence, exceptions, accepted risk and bypass.
2. Provide a small local GovCheck executable as the verifier core; no hosted MCP server is required.
3. Prototype a Git `pre-receive` adapter for a controlled bare repository. The hook delegates to a trusted, administrator-installed verifier and fails closed on malformed, missing, stale or non-PASS results. It is not installed on this repository by this research.
4. Add forge adapters as separate integrations: GitHub rulesets/expected App, GitLab protected branches plus blocking external status checks, Gitea protected branches, and Forgejo protected branches plus trusted workflow/runner configuration.
5. Treat Pijul remote enforcement as a separate adapter project; do not claim Nest support until a controlled server integration is demonstrated.
6. Verify the actual deployed configuration and demonstrate a rejected update in an isolated test repository before claiming enforcement.

### 6.1 Implemented adapter prototype

The branch now contains a reference Git pre-receive adapter at [scripts/govcheck-git-pre-receive](../../scripts/govcheck-git-pre-receive), an installer at [scripts/install-govcheck-git-pre-receive.py](../../scripts/install-govcheck-git-pre-receive.py), and unit plus end-to-end tests. The installer accepts only a bare Git repository, refuses to overwrite an existing pre-receive hook, requires an administrator environment file outside the repository with mode 0600, and installs the hook outside the candidate worktree.

For protected refs, the hook requires a single executable gate command outside the bare repository and pins the repository identity, executable file digest, verifier identity, and exact policy revision and digest. The command must return a JSON decision envelope bound to the exact old object ID, new object ID and ref. The hook rejects malformed or mismatched envelopes and FAIL/UNKNOWN/CONFLICT; accepted-with-risk is disabled by default and requires an explicit deployment flag plus a structurally complete risk record. The trusted gate command—not this adapter—must validate the risk record's authority, signature, scope and expiry. The executable file digest is pinned, but its runtime/dependency closure remains in the server trust root.

The end-to-end test uses an isolated bare repository and a fake gate executable: a push with UNKNOWN is refused and leaves the target ref unchanged; the same exact update with PASS is accepted. This demonstrates that the Git receive boundary can reject an update. It does **not** demonstrate that the current GovCheck evaluator is already a trusted gate executable. The hook writes to stderr and does not yet append a durable decision to the canonical governance journal. The initial protected ref is bootstrapped out-of-band in the test; the hook rejects implicit protected-ref creation and deletion. The hook is not installed on this repository.

## 7. Threats and residual limitations

- **Candidate-controlled workflow/evaluator:** a pull request can change its own workflow or checker. Use a verifier installed/pinned outside the candidate tree or a trusted integration that runs a protected verifier.
- **Status spoofing:** require a specific trusted App/service source where the forge supports it; do not trust a status context name alone.
- **Stale evidence / TOCTOU:** bind candidate and base; reject stale results; re-evaluate the actual merge result.
- **Direct push / alternate transport:** configure every write path, not only the web merge button.
- **Administrator bypass:** record and scope it; do not claim protection against the administrator who controls the hook/ruleset/server.
- **Local hook bypass:** client hooks are convenience controls only.
- **Pijul remote gap:** local `record` hook does not intercept `pijul push`; a controlled remote is required.
- **Availability:** if the trusted evaluator is unavailable, return `UNKNOWN`; any emergency acceptance must be a distinct authorized risk decision.

## 8. Relationship to existing GovCheck records

- [Architecture 0015](../architecture/0015-governance-conformance-and-validation-plan.md) already separates verification core, repository-boundary enforcement and forge integration; these are responsibilities, not maturity levels.
- [Architecture 0022](../architecture/0022-governance-capability-audit.md) records enforcement boundary and bypass limitations.
- [Architecture 0023](../architecture/0023-bootstrap-governance-authority.md) retains the single root-authority baseline and its explicit residual risks.
- [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.md) supplies the proposed logical journal protocol; this research does not select physical storage.
- [Issue #44](https://github.com/Martin-PB/govcheck/issues/44) covers interoperable, non-circular attestations.
- [Issue #45](https://github.com/Martin-PB/govcheck/issues/45) owns the acceptance-boundary implementation and verification work.

**No branch protection, ruleset, hosted service, authority policy or normative acceptance rule is changed by this research.**
