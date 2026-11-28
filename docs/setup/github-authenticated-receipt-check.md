# Activate the authenticated GitHub receipt check

This guide configures the check source merged in PR #185. It does **not** configure branch protection automatically.

## 1. Commit a trusted public-key policy

Create a trust-policy JSON file on protected `main`, for example:

`govcheck/formal/github-pr-receipt-trust-policy.json`

It must use the existing GovCheck trust-policy schema and contain:

- `schemaVersion: "1"` and `policyId: "urn:govcheck:trust-policy:v1"`;
- a governance-controlled `revision`;
- `openssl.path` as an absolute executable path and `openssl.sha256` as its raw 64-hex SHA-256;
- at least one active `ed25519` public key with `keyId`, `publicKeyPath`, `publicKeySha256`, `principalId` and the required `governance-authority` role (or another configured role).

Only public keys belong in the repository. Keep the corresponding private key outside the repository with mode 0600. Pin the OpenSSL binary and each public key digest.

## 2. Set repository variables

Use the repository's GitHub CLI context (verify with `gh repo view`). These are **public configuration variables**, not secrets:

```sh
gh variable set GOVCHECK_TRUST_POLICY_PATH --body "govcheck/formal/github-pr-receipt-trust-policy.json"
gh variable set GOVCHECK_TRUST_POLICY_SHA256 --body "$(sha256sum govcheck/formal/github-pr-receipt-trust-policy.json | cut -d' ' -f1)"

gh variable set GOVCHECK_JOURNAL_SCOPE_ID --body "<exact journal scope ID>"
gh variable set GOVCHECK_REPOSITORY_URI --body "<exact canonical repository URI>"
gh variable set GOVCHECK_GOVERNANCE_REVISION --body "<governance revision>"
gh variable set GOVCHECK_GOVERNANCE_DIGEST --body "sha256:<64-hex governance package digest>"
gh variable set GOVCHECK_EXPECTED_REPOSITORY_ID --body "<exact repository ID used by the gate>"
gh variable set GOVCHECK_EXPECTED_POLICY_DIGEST --body "sha256:<64-hex acceptance policy digest>"

gh variable set GOVCHECK_REQUIRED_ROLE --body "governance-authority"
gh variable set GOVCHECK_PROTECTED_BASE_REF --body "main"
```

The journal scope, repository ID/URI, governance revision/digest and acceptance-policy digest must be the same values used by the trusted local acceptance gate. Do not guess or substitute the trust-policy digest for the governance or acceptance-policy digest.

## 3. Run the preflight

Export the same values locally (or retrieve them with `gh variable get`) and run:

```sh
python scripts/validate-github-receipt-check-config.py --repository-root .
```

The preflight checks required variables, trust-policy file pin, OpenSSL executable pin, public-key file digests and presence of an active key for the required role. It does not expose private material.

## 4. Require the check in the ruleset

In GitHub repository Settings → Rules → Rulesets, configure the protected base branch to:

1. Require a pull request.
2. Require status check **GovCheck authenticated acceptance receipt**, sourced from GitHub Actions.
3. Require the PR branch to be up to date before merging.
4. Restrict bypass actors and direct pushes to the protected branch.

Do not treat the workflow as enforcement until this ruleset is active. The check source itself does not change repository rulesets.

## 5. Submit a receipt

On the PR, post a comment containing the standalone command and the signed envelope:

````text
/govcheck-receipt
```json
<signed DSSE envelope>
```
````

Only an authenticated `pass` decision with exact current head/base and content digest bindings can complete the check successfully. Fork PRs are not supported by this initial adapter.
