# 0037 — Repository acceptance boundary and enforcement adapters

**Status:** proposal for issue [#45](https://github.com/Martin-PB/govcheck/issues/45). Not adopted as a normative policy. No forge configuration or branch-protection rule is changed by this record.

## 1. Problem

GovCheck can evaluate a candidate and produce a result, but an evaluation result does not itself prevent a repository update. A report-only workflow, local CLI invocation or client hook is not an effective acceptance boundary if a contributor can push the same candidate through another path.

This record refines the three responsibilities already distinguished by Architecture 0015:

1. **Verification core:** evaluates exact candidate evidence against a governance revision.
2. **Repository-boundary enforcement:** prevents a protected repository operation unless a valid acceptance decision exists.
3. **Forge/VCS integration:** maps native VCS identities and platform-specific capabilities to the boundary contract.

These are separate responsibilities, not assurance or maturity levels. GovCheck remains the normative governance authority; a forge is an enforcement mechanism, not the source of governance semantics.

## 2. Design constraints

- A small local executable remains the verification core. No hosted MCP server is required.
- The enforcement boundary is the repository/deposit operation, not the coding-agent harness.
- The logical contract must be VCS-neutral, but candidate identity remains VCS-native. Git commit/tree identities must not be conflated with Pijul channel/change-set identities without a proven semantic mapping.
- A local hook is cooperative unless all relevant writes are intercepted by a controlled repository/server boundary.
- Platform status checks are signals from an adapter; a status context name alone is not a proof or an authority.
- Tests, model-checking results, proof-checking results and inspections retain their distinct method classes.
- FAIL, UNKNOWN and CONFLICT are not PASS. An authorized risk acceptance remains a distinct decision and must not rewrite the underlying result.
- Stale evidence is invalid when the candidate, base, governance revision, verifier or relevant inputs change.
- Bypass authority and limitations must be explicit, attributable and auditable.
- No architecture here configures the current GovCheck repository's GitHub branch protection or accepts a new authority regime.

## 3. Proposed acceptance-decision envelope

The adapter contract should consume a structured decision envelope, produced by the local verifier or a trusted server-side execution. The exact serialization remains open.

| Group | Required binding |
|---|---|
| Repository subject | Repository identity, VCS kind, target ref/channel |
| Candidate | Native candidate identity and content/tree/change-set digest |
| Base | Native base identity and content digest used during evaluation |
| Governance | Exact governance package, revision, digest and applicable profile |
| Verifier | Identity, version, executable digest, configuration digest and trust basis |
| Result | PASS, FAIL, UNKNOWN, CONFLICT or ACCEPTED_WITH_RISK |
| Evidence | Evidence IDs/digests, method class, scope, assumptions and limitations |
| Decision | Stable decision ID, authority identity/provenance, time, scope and expiry |
| Risk acceptance | Separate authorized record, if any; never inferred from a PASS |
| Provenance | Authenticated origin/signature or a trusted local execution boundary |

The attestation must not be embedded in the same candidate commit whose final hash it claims to attest. Store it out-of-band or in a separately governed append-only journal. This directly addresses the self-reference defect tracked by issue #44.

A candidate identity is adapter-specific. For Git, the adapter binds the full object ID and the exact tree/commit under evaluation. For Pijul, it binds the native channel and change-set identity. A content digest is supplementary; it does not establish semantic equivalence across VCSs.

## 4. Acceptance semantics

The following is the proposed default contract to formalize and test; adoption remains open.

- **PASS:** all mandatory applicable rules pass, evidence is fresh and scoped to the exact candidate/base/policy, and the verifier source is trusted.
- **FAIL:** one or more mandatory claims are contradicted or requirements fail.
- **UNKNOWN:** required evidence is missing, stale, unavailable, unauthenticated or outside the verifier's competence.
- **CONFLICT:** incompatible evidence or unresolved concurrent state prevents a determinate result.
- **ACCEPTED_WITH_RISK:** a distinct authorized decision permits a bounded operation despite an underlying FAIL/UNKNOWN/CONFLICT, with reason, scope, affected claims, authority, residual risk and expiry recorded.

Default behavior: only PASS is automatically accepted. Other outcomes block unless an explicit policy-authorized exception/risk decision permits a distinct accepted-with-risk path. Such a path must never relabel UNKNOWN as PASS. A gate outage is UNKNOWN, not success.

The current root-authority baseline in Architecture 0023 remains unchanged. This proposal does not invent a second approver or imply that a free-form reviewer name proves independent authority.

## 5. Enforcement adapters

| Adapter | Effective boundary | Required configuration/trust | Residual limitation |
|---|---|---|---|
| Local CLI | None by itself | Exact local candidate evaluation | User can omit it or invoke VCS directly. |
| Client hook/wrapper | Intercepts one client path | Installed hook and trusted verifier | Other clients/transports and local administrators can bypass it. |
| GitHub | Merge into protected refs | Ruleset/protected branch, required PR/check, expected trusted App source, current-base check, reviewed bypass list | Direct pushes must also be blocked; App/workflow trust and administrator bypass remain. |
| GitLab | Merge request into protected refs | Protected branch plus “Status checks must succeed”; external check bound to current HEAD and authenticated | External checks are tier-dependent and require a service endpoint. |
| Gitea | Push/merge to protected refs | Protected-branch rule, required status contexts, administrator behavior configured | Platform-specific; trusted source of status must still be established. |
| Forgejo | Push/merge to protected refs and trusted workflow execution | Branch protection plus controlled write access, runner scope, workflow provenance and isolation | A protected main branch alone does not prevent arbitrary workflow execution from unprotected branches. |
| Git pre-receive | Every receive operation updating protected refs | Server-installed hook and verifier outside candidate tree; fail-closed decision | Server administrator/direct filesystem access can bypass or replace it. |
| Pijul remote | Channel/patch application | Controlled remote/server adapter intercepting the remote operation | The cited Nest/manual documents only local record hooks, not a mandatory remote policy hook. |

A deployment must declare capabilities rather than imply them:

- can_block_merge
- can_block_direct_push
- can_bind_exact_candidate
- can_bind_current_base
- can_reject_stale_result
- can_pin_trusted_verifier_source
- can_record_bypass
- can_revalidate_merge_result
- can_enforce_all_supported_transports

If an adapter cannot intercept every relevant write path, its result is advisory and must not be described as effective enforcement.

## 6. Git server prototype boundary

The first reference adapter should be a Git pre-receive hook for a controlled bare repository:

1. Git supplies each proposed old_oid, new_oid and ref_name tuple.
2. The hook filters only explicitly protected refs; deletion and unconfigured initial creation fail closed.
3. It invokes an administrator-installed verifier executable. The verifier and policy are outside the candidate tree and are pinned by the server operator.
4. The verifier returns a structured decision bound to the exact old/new object IDs, ref, governance revision and verifier identity.
5. The hook validates the envelope and returns nonzero for missing, malformed or stale evidence, FAIL, UNKNOWN or CONFLICT.
6. An ACCEPTED_WITH_RISK result is accepted only when the deployment explicitly enables that path and the envelope contains an authorized, scoped, unexpired risk-decision record. It remains accepted-with-risk, never PASS.
7. The hook logs the decision ID and result. If any protected ref update in the receive operation is rejected, Git rejects the receive operation.

The prototype is implemented as scripts/govcheck-git-pre-receive with installer scripts/install-govcheck-git-pre-receive.py. It consumes a govcheck.acceptance-decision/v0 JSON envelope and requires the server operator to pin the repository identity, single gate executable path and its SHA-256 digest, verifier identity, and exact policy revision and SHA-256 digest outside the candidate repository. The environment file must be outside the bare repository and mode 0600; the installer refuses to overwrite an existing pre-receive hook. The hook rejects missing/malformed/mismatched/stale outcomes, FAIL, UNKNOWN and CONFLICT. Accepted-with-risk is disabled by default; if enabled, the trusted gate executable must itself validate the authority, signature, scope and expiry of the risk record. The hook only checks that the record is structurally complete.

The integration test creates an isolated bare repository, bootstraps its initial protected ref out-of-band, then proves that a push returning UNKNOWN is rejected and a push returning PASS for the exact old/new/ref tuple is accepted. The fixture uses a fake trusted gate executable: this proves the Git receive-boundary mechanics, not the semantic correctness of the current GovCheck evaluator. The hook writes its decision to stderr; this is not yet an append-only canonical governance journal. The runtime/dependency closure of the pinned executable and administrator bypass remain in the trust boundary. Nothing is installed on this GovCheck remote.

## 7. Pijul boundary

Pijul is not to be forced into Git commit semantics. The documented local record hook does not intercept pijul push; the Nest offers direct push by ACL or attaching changes to a discussion. Therefore:

- a local wrapper is advisory and bypassable;
- Nest discussion/review is not equivalent to a conditional server-side GovCheck gate;
- mandatory enforcement requires a controlled Pijul remote/server adapter that validates the native channel/change-set before applying it;
- until that adapter exists and is tested, the Pijul capability declaration must say can_block_direct_push = false for the Nest and must not claim enforcement.

## 8. Trust and bypass assumptions

- Candidate-controlled workflow/evaluator files are not a trust root. Use a verifier pinned outside the candidate tree or a separately trusted integration.
- Status spoofing is mitigated by expected source identity where the platform supports it.
- A result is invalidated when candidate, base, governance revision, verifier or relevant evidence changes.
- Merge queues/test-merge commits must be evaluated as the actual candidate to be integrated.
- Administrators who control branch rules, hooks, server files or the verifier remain trusted/bypass-capable actors. Their actions must be visible as bypass/override events, not silently described as successful verification.
- Local-only and client-side enforcement cannot be called mandatory when the repository owner can bypass the client.

## 9. Formalization and verification plan

The acceptance-boundary model should check:

- no PASS from FAIL/UNKNOWN/CONFLICT;
- exact candidate/base/governance/verifier binding;
- stale evidence invalidation after base or policy change;
- explicit accepted-with-risk distinct from PASS;
- no silent bypass;
- publication only after a valid gate decision in enforced mode;
- advisory mode can be bypassed, but the resulting publication is marked uncontrolled.

The model's trust input is an assumption, not a theorem about real identities or binary integrity. A separate integration test must exercise the Git pre-receive adapter with a fake verifier: PASS accepted; FAIL/UNKNOWN/malformed/mismatched/stale decisions rejected; accepted-with-risk rejected by default and accepted only when explicitly enabled with a complete record.

## 10. Open decisions

- Exact envelope serialization and signature/trust-root scheme.
- Which authority may issue risk acceptance and whether UNKNOWN is ever waivable for a given claim class.
- Whether the GitHub deployment should use a GitHub App, a protected reusable workflow or another trusted status provider.
- Which GitLab/Gitea/Forgejo versions and deployment profiles are supported.
- Whether a controlled Pijul server adapter is in scope, and how it authenticates the server-side verifier.
- How emergency bypass is authorized, expired and reconciled into the canonical journal.

No choice above is adopted by this proposal.

## 11. References and related records

External platform sources are catalogued in [R-221](../references.md#r-221), [R-222](../references.md#r-222), [R-223](../references.md#r-223), [R-224](../references.md#r-224), [R-225](../references.md#r-225), [R-226](../references.md#r-226). Related records: [Architecture 0015](0015-governance-conformance-and-validation-plan.md), [Architecture 0022](0022-governance-capability-audit.md), [Architecture 0023](0023-bootstrap-governance-authority.md), [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.md), [research synthesis](../research/acceptance-boundary-enforcement-2026-11.md), [issue #45](https://github.com/Martin-PB/govcheck/issues/45).

**This record is a proposal. It does not enable branch protection, install hooks, select a forge or adopt a normative acceptance policy.**
