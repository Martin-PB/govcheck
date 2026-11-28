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

## 9. Current GitHub ruleset observation and audit

A read-only API inspection on 2026-11-27 found repository ruleset `Protection Main` (ID `28251664`):

- enforcement is active and the ruleset targets the default branch;
- deletion and non-fast-forward restrictions are enabled;
- no bypass actors are configured and the current API response reports `current_user_can_bypass=never`;
- the ruleset has no `pull_request` requirement and no `required_status_checks` rule.

The branch-protection endpoint returned HTTP 403 `Resource not accessible by integration`; this is an API permission limitation and is not evidence that branch protection is absent. The ruleset endpoint was readable.

The read-only `govcheck/forge.py audit-ruleset` command checks active default-branch scope, PR requirement, exact required-check contexts, expected GitHub integration/source ID, strict freshness, deletion/non-fast-forward and bypass actors. It reports configuration conformance only and always sets `boundary_demonstrated=false`: a real protected-ref rejection and merge-result freshness still require separate tests.

The GitHub Actions source ID observed on GovCheck check runs is `15368`. The current CI check contexts are `govcheck-check`, `package-alignment` and `reference-integrity`; path-filtered workflows must be made consistently available before all three can be configured as required checks.

**No ruleset or branch-protection setting was changed by this audit.**

## 10. Local authenticated acceptance-gate adapter

The `govcheck/git_acceptance_gate.py` adapter and `scripts/govcheck-acceptance-gate` entry point now bridge the signed `acceptance-decision/v1` verifier to the existing Git pre-receive `govcheck.acceptance-decision/v0` protocol.

For each protected update, the gate:
- clones/checks out the exact candidate from the server Git object store into a temporary directory;
- computes the candidate snapshot and full base/candidate bindings;
- runs the installed GovCheck evaluator with detached review/assurance/forge-identity inputs;
- verifies the authority decision against the exact report bytes and candidate/ref/governance/scope bindings;
- emits a v0 decision envelope with the pinned repository, policy and verifier identity/digests.

The entry point must be installed outside the candidate repository. The pre-receive hook pins the executable file digest; the Python package/runtime closure remains part of the server administrator's immutable trust root. Missing evidence or configuration yields UNKNOWN and is rejected by the hook.

**This is still not an effective forge boundary:** the local hook has not been installed on a real protected bare repository and exercised with accepted/rejected pushes, and the GitHub ruleset still lacks required PR/status checks. The adapter's unit tests are protocol tests, not a protected-ref rejection demonstration.

## 11. Disposable bare-repository integration result

The local integration test `test_real_bare_repo_accepts_scoped_risk_and_rejects_stale_decision` installs the actual pre-receive hook and gate entry point into a temporary bare Git repository.

It demonstrated:
- a candidate update accepted only under a DSSE-signed `accept_with_risk` decision with exact report/candidate/base/ref/governance/scope bindings;
- a second candidate rejected when it reuses the first candidate's decision;
- the protected `main` ref remains at the first accepted commit after the stale decision is rejected.

The test uses synthetic Ed25519 keys and a disposable trust policy. It validates the local hook/gate execution path, including Git object-tree materialization, but is not a production forge installation or a test of GitHub's ruleset/bypass behavior.

## 12. GitHub ruleset payload and remaining external action

The current main-branch check-run names and source were verified directly from GitHub:

- `govcheck-check`
- `package-alignment`
- `reference-integrity`
- GitHub Actions integration ID `15368`

`govcheck/forge.py ruleset-payload` renders a least-bypass default-branch ruleset with PR required, zero approving reviews (the configured authority remains the signed GovCheck decision), deletion/non-fast-forward protection, the three exact checks pinned to integration `15368`, strict freshness and no bypass actors. It does not call or mutate GitHub.

Render the payload:

```sh
python3 govcheck/forge.py ruleset-payload \
  --required-checks govcheck-check,package-alignment,reference-integrity \
  --check-source-id 15368 --required-approvals 0 > govcheck-main-ruleset.json
```

After reviewing the generated JSON, an administrator can update the existing ruleset `28251664` with the GitHub CLI:

```sh
gh api --method PUT /repos/Martin-PB/govcheck/rulesets/28251664 \
  --input govcheck-main-ruleset.json
```

Then audit the live configuration with `audit-ruleset`. This is a user/admin action: the current ChatGPT GitHub integration is read-only and has not applied it.

**Important:** these three checks currently protect CI/package/reference integrity; `govcheck-check` is still report-only. Requiring them does not by itself make GitHub a signed acceptance-decision gate. The local pre-receive adapter is the acceptance gate for Git transports; a trusted GitHub acceptance check and live ruleset configuration remain outstanding.

## 13. Signing a decision from the exact gate report

The gate can now write the exact serialized report bytes to an external path with `GOVCHECK_REPORT_OUTPUT_PATH`. The output digest is the same `evidence_digest` emitted in the decision protocol; it is not reconstructed from a parsed/reformatted JSON object.

The `sign` command builds and signs a decision from those exact bytes:

```sh
python3 -m govcheck.acceptance_decision sign \
  --report govcheck-report.json \
  --repository-uri https://github.com/Martin-PB/govcheck \
  --repository-id 1447286150 \
  --decision-id decision-<unique-id> \
  --result accept_with_risk \
  --rationale "Bounded risk accepted by the governance authority." \
  --risk-acceptance risk-record.json \
  --private-key ~/.config/govcheck/authority-ed25519.pem \
  --key-id govcheck-root-authority \
  --openssl /usr/bin/openssl > acceptance-decision.json
```

For `accept`, the signer refuses an evaluation report whose overall result is not PASS. For `accept_with_risk`, a complete scoped and expiring risk record is required. The private key remains outside the repository.

The signed envelope can be supplied as a detached artifact or other external input to a trusted forge adapter. It must not be committed into the candidate snapshot whose content digest it authorizes, because doing so would create a circular candidate binding.


## 14. Durable journal receipt for a verified acceptance decision

The local Git gate can optionally append an acceptance-decision event to an explicitly initialized GovCheck SQLite journal. This is a separate local receipt, not a forge status check and not a publication receipt.

The integration is enabled only when all three settings are supplied to the gate process:

- `GOVCHECK_JOURNAL_DB`: SQLite database outside the bare repository;
- `GOVCHECK_JOURNAL_SCOPE_ID`: exact scope matching `GOVCHECK_SCOPE_ID`;
- `GOVCHECK_JOURNAL_AUTHORITY_REVISION`: the authority revision pinned by the journal genesis.

Before appending, the integration verifies the complete journal, checks the genesis authority principal against the authenticated DSSE decision signer, checks the authority revision and governance revision, and binds the event to repository, candidate, base, ref, policy, report digest, result and risk record. It uses compare-and-append and a deterministic idempotency key derived from the exact decision payload. A committed receipt can be recovered with the journal's `receipt` command.

Genesis is never created by the gate. Initialize it explicitly outside the repository, using the authenticated authority principal and pinned authority/governance revisions. If any journal setting is present but configuration, genesis or append fails, the gate returns UNKNOWN and the pre-receive adapter rejects the update. If no journal setting is present, the gate retains its previous optional-journal behavior; deployments must not claim journal-backed acceptance until the settings are installed and audited.

This increment records verified acceptance, not failed attempts, bypasses or successful ref publication. The journal's local hash chain is not actor authentication and does not resist a privileged administrator rewriting the database. Those receipt classes and the live GitHub check/ruleset remain open work under #45/#155.


## 15. Journal gate outcomes, including UNKNOWN and rejection

The journal integration now records each completed gate evaluation when journal mode is configured, not only accepted decisions. The event type is `govcheck.acceptance.gate-result/v1` and includes the exact candidate/base/ref/report digest, decision ID/result, policy/governance/scope bindings, reason and risk record.

When a verified authority principal is available, the event is attributed to that principal only after its equality with the journal's configured genesis authority pin is checked. For invalid or unavailable authority evidence, the event actor is the fixed local attribution `system:govcheck-gate` and the payload explicitly labels the result `unverified-gate-attempt`; this is not an authenticated human decision. Such attempts require `GOVCHECK_JOURNAL_AUTHORITY_ID` to match the journal genesis authority.

The journal receipt is written before the pre-receive hook returns. It therefore records the gate outcome/attempt, not whether Git subsequently updated the ref. A later post-receive receipt is needed to establish publication. If the configured journal cannot record the outcome, the gate returns UNKNOWN and the protected update is rejected.


Section 15 extends the earlier optional accepted-decision receipt described in section 14: it records all completed gate outcomes, with explicit distinction between authenticated authority attribution and unauthenticated local gate-attempt attribution.
