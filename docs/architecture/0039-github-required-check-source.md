# 0039 — GitHub required-check source for authenticated acceptance receipts

**Status:** implementation slice under [#45](https://github.com/Martin-PB/govcheck/issues/45); trust configuration and ruleset adoption remain pending.

## 1. Decision

Provide a repository-specific GitHub Actions check source named **`GovCheck authenticated acceptance receipt`**. The workflow:

- Creates a pending check run on the exact PR head SHA when the PR opens, synchronizes, reopens, changes base, or becomes ready for review.
- Accepts a signed journal receipt only through a PR comment containing the standalone command `/govcheck-receipt` and one fenced DSSE JSON envelope.
- Runs the verifier from trusted `main`; it checks out the candidate into a separate directory with credentials disabled and never executes candidate code.
- Verifies the DSSE signature against a pinned trust-policy file and required signer role, then binds the signed gate event to the current PR head SHA, current base SHA, target branch, candidate content digest, repository URI/ID, governance scope/revision/digest and acceptance-policy digest.
- Requires an authenticated authority decision with result `pass`; risk-accepted outcomes and unverified attempts do not satisfy this check.
- Re-fetches the PR before completing the check and fails if head, base or state changed during verification.

The check source is an enforcement signal only when the repository administrator selects the exact check name and trusted GitHub Actions source in the branch ruleset. GovCheck does not modify the ruleset. Direct-push prevention, bypass restrictions and the “require branch to be up to date” setting remain administrator-controlled. See [R-225](../references.md#r-225) and [R-227](../references.md#r-227).

## 2. Configuration boundary

The workflow reads public repository variables for the trusted policy path and digest, journal scope, canonical repository URI/ID, governance revision/digest, acceptance-policy digest, required signer role and protected base branch. The trust-policy file pins the OpenSSL executable path/digest and signer public keys. These are configuration, not secrets; the only secret is the workflow's short-lived GitHub token.

If any pin is absent or mismatched, the check fails closed. Fork PRs are not supported by this initial check source. The check is intentionally limited to Git and authenticated PASS decisions.

## 3. Assurance and residual risks

The check verifies a signed receipt and its exact bindings; it does not turn a signature into proof of the underlying decision's correctness. The signed journal statement attests to chain integrity verified at signing time, not the database's future immutability. The candidate tree is hashed by trusted GovCheck code but never executed.

The workflow creates a pending check on PR lifecycle events. To ensure base-branch movement invalidates old results, the ruleset must also require the PR branch to be up to date. A status check alone does not block direct pushes unless the ruleset enforces it. No forge configuration is changed by this ADR.


Configuration and activation steps are maintained in the [authenticated receipt check setup guide](../setup/github-authenticated-receipt-check.md), including a local preflight command.
