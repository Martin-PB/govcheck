# Specification 0004 — VCS and Collaboration Adapter Contracts

**Status:** Proposed architecture, ready for review. **French:** [0004](0004-vcs-collaboration-contracts.fr.md).

## Separation

Keep four dimensions independent: VCS (Git/Pijul/future), hosting (local/team/self-hosted/public), collaboration (individual/shared/review/patch exchange/integration request), and acceptance/application (local/team/forge/native apply). GovCheck core owns governance semantics; adapters translate them. Core must not depend on GitHub, GitLab, Nest or a transport.

## VCS adapter contract

An adapter provides native repository identity, exact repeatable state descriptors/fingerprints, base/candidate comparison, affected resources, native changes/dependencies/conflicts, read-only inspection by default, explicit apply with preconditions, capability declaration and precise unsupported errors. It must not flatten native semantics or pretend every VCS has commits, branches or linear history.

### Git

Identify repository, commit and tree; explicitly account for submodules and worktree/index state. A commit alone may not describe dirty/untracked content. Candidate descriptor states whether it is a commit or index/worktree snapshot. Report Git-native ancestry and conflicts. Apply verifies expected base and candidate before mutation.

### Pijul

Preserve patch identities/dependencies, channel identity/state, graph semantics and native conflicts. Fingerprint relevant channel graph/state, not just channel name or one patch hash. Use native Pijul operations; never synthesize Git commits or infer Pijul conflicts from textual merge tools. Unsupported properties are indeterminate, not successful.

## Hosting and collaboration

Hosting transports/locates state but does not redefine VCS identity. Local-only is a complete deployment. Collaboration adapters map participants, reviews, decisions, approvals, patch exchange and integration requests to GovCheck change IDs and exact candidates. A PR/MR is a collaboration object, not the change itself.

Adapters declare capabilities: read reviews, authenticate reviewers, request approval, block integration, apply candidates and observe bypasses. Missing capability is visible. Comments/reactions are not approvals unless policy explicitly says so and identity is verifiable.

## Enforcement limits

Local hooks/wrappers can be bypassed by users with filesystem access. Strong shared enforcement requires a team server or forge to require a valid decision bound to exact repository state and governance revision. Missing enforcement capability is reported as a limitation, never a pass. Signatures may establish integrity/origin under key assumptions; they do not prove correctness or authority by themselves.

## Failure semantics and conformance

Distinguish not-found, unsupported, unavailable, stale, conflict, authentication/authorization failure and malformed state. Mutations require explicit intent and preconditions; partial failure is never reported as atomic success. Contract tests cover dirty Git state/submodules, exact trees, Pijul graph/patch/conflict preservation, local-only operation, capability negotiation, stale races, apply preconditions and enforcement gaps. No adapters are implemented yet.

## Primary references

- Git and Pijul primary documentation are catalogued under [R-22 in the package reference catalogue](../references.md#r-22).

These sources describe the underlying VCS semantics; they do not establish that GovCheck's adapters are implemented or conformant.
