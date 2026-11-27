# Architecture 0039 — Detached DSSE verification and pinned trust policy

**Status:** proposed first verification-provider profile for issue #158. It does not adopt a universal PKI, key-management policy or independent-review requirement. **French:** [0039](0039-detached-dsse-trust-policy.fr.md).

## 1. Purpose

Specification 0008 defines the in-toto Statement/DSSE envelope and structural validation. Structural validity is not signature authenticity. This profile adds an optional local verifier for Ed25519 signatures, delegating cryptographic operations to an explicitly pinned OpenSSL executable. It is a provider, not a mandatory GovCheck dependency.

## 2. Trust boundary

The verifier consumes three distinct inputs:
1. a detached DSSE envelope (potentially candidate-supplied and therefore untrusted);
2. a trust-policy file supplied out-of-band, outside the candidate tree, whose exact byte digest is pinned by the operator;
3. a candidate root used to reject trust-policy, key and verifier paths located inside candidate-controlled content.

The trust policy shape is defined by [attestation-trust-policy-v1.schema.json](../../govcheck/formal/schemas/attestation-trust-policy-v1.schema.json). The trust policy pins:
- policy identifier and revision;
- OpenSSL executable path and SHA-256 digest;
- each key ID, Ed25519 algorithm, public-key path and SHA-256 digest;
- stable principal ID and authorized roles;
- key validity interval and revocation state.

The policy digest is passed separately to the verifier. A policy cannot authenticate itself. Public keys and the OpenSSL executable are also byte-pinned. The operator must protect the policy and key files; path/digest checks do not protect against a privileged operator who can change the expected digest or the verifier process.

## 3. Signature verification

The verifier:
1. structurally decodes the DSSE envelope and validates the in-toto Statement;
2. checks the exact payload type and expected predicate type/candidate/policy bindings;
3. computes the DSSE v1 pre-authentication encoding (PAE) over the exact payload bytes;
4. resolves each signature key ID through the pinned trust policy;
5. checks the key and OpenSSL binary digests, key validity/revocation, required role and optional required principal;
6. invokes OpenSSL Ed25519 verification over the PAE bytes without a shell;
7. returns a verified signer identity/role only after successful cryptographic verification.

Unknown key IDs, unavailable OpenSSL, missing policy, digest mismatch, unsupported algorithms or unavailable trust data are UNKNOWN/invalid outcomes and never PASS. A structurally valid but unsigned/untrusted envelope is not trusted evidence.

## 4. Time and identity limits

The key validity interval is evaluated against the verifier's current system clock. DSSE does not provide a trusted signing timestamp here. The signed statement's own evaluation timestamp is signer-asserted; it cannot prove when the signature was created. Historical validation after key expiry/revocation requires a trusted timestamp or a separately governed archival policy, which is out of scope.

A key ID mapped to a principal/role authenticates possession of the corresponding private key under the configured trust policy. It does not prove a real-world person's identity, employment, availability or independence. The policy operator remains responsible for key-to-principal binding and role authorization.

The current project has one available contributor. Therefore the verifier must not manufacture a second reviewer. The independent-review claim remains UNKNOWN unless an actual distinct authenticated principal with the required role provides a matching detached review attestation. Synthetic test keys prove only the cryptographic mechanism.

## 5. First provider profile

- Algorithm: Ed25519 only.
- Crypto implementation: OpenSSL CLI pkeyutl; no custom cryptographic primitive and no Python crypto dependency.
- Trust-policy and public-key files: local, operator-controlled and outside the candidate root.
- OpenSSL binary: absolute path and SHA-256 pinned in the policy.
- DSSE key ID: exact map lookup; no implicit key discovery.
- Roles: explicit strings such as independent-reviewer, verifier or risk-authority; role membership is not itself a GovCheck decision.
- Output states: verified, invalid, unknown.
- CLI: local command; no network calls or hosted service.

Implementation: [attestation_verify.py](../../govcheck/attestation_verify.py) and [trust-policy schema](../../govcheck/formal/schemas/attestation-trust-policy-v1.schema.json). This provider is optional. If OpenSSL is absent or does not match the pinned digest, the result is UNKNOWN. Other providers/algorithms can implement the same verifier contract later.

## 6. Non-goals

No X.509 certificate chain, PKI, Sigstore/Fulcio/Rekor, online revocation, trusted timestamp authority, key generation/rotation service, key escrow, multi-signature quorum, or automatic authority delegation is implemented. No private key is stored in the repository. No cryptographic verification is performed by the structural builder in attestation.py.

## 7. References and related records

- [R-232 — OpenSSL pkeyutl](../references.md#r-232)
- [R-233 — RFC 8032 EdDSA/Ed25519](../references.md#r-233)
- [Specification 0008 — Interoperable assurance attestations](../specifications/0008-interoperable-assurance-attestations.md)
- [Issue #158 — Detached DSSE verifier](https://github.com/Martin-PB/govcheck/issues/158)
- Related: #44 attestations, #60 single-authority residual risk, #155 canonical journal, #45 acceptance boundary.

**This profile authenticates a signature under an operator-pinned key policy. It does not prove human identity, independent review, authority correctness or trusted signing time.**
