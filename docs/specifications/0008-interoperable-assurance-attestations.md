# Specification 0008 — Interoperable assurance attestations

**Status:** proposed profile for issue issue #44; not a normative adoption and not a claim that signatures or signer identities are verified by the current runtime. **French:** [0008](0008-interoperable-assurance-attestations.fr.md).

## 1. Purpose

Define a portable representation for GovCheck evaluation evidence that can be transported and authenticated using the in-toto Attestation Framework and DSSE. The profile binds an evaluation to an immutable candidate subject, native VCS identities, the exact governance revision, verifier identity, inputs, assurance methods, limitations and result.

The profile does not make an attestation a proof. It preserves the distinction between tests (observations/evidence), model checking (evidence about a bounded model), proof checking (a proof accepted by a stated kernel), inspection/review, and an authority's decision.

## 2. Interoperability mapping

- **in-toto Statement v1** is the outer semantic statement: `_type`, immutable `subject` digest, `predicateType` and typed `predicate`.
- **GovCheck Assurance Evaluation predicate v1** carries GovCheck-specific evaluation and assurance semantics. Predicate URI: `urn:govcheck:attestation:assurance-evaluation:v1`.
- **DSSE v1** is the recommended authenticated envelope. The payload type is `application/vnd.in-toto+json`; signatures authenticate the exact payload bytes and payload type through DSSE PAE.
- A digest in an in-toto subject identifies the content snapshot. Native Git/Pijul identities remain additional VCS-specific fields; Git commit IDs and Pijul change identities are not interchangeable with a content digest.
- SLSA Verification Summary Attestation (VSA) is not the generic GovCheck predicate. Its `verificationResult` is PASSED/FAILED and its levels describe SLSA tracks. It may be emitted separately when a SLSA level was actually evaluated, but must not encode GovCheck UNKNOWN, CONFLICT, proof status or authority decisions.

## 3. Predicate contract

The complete JSON Schema is `../schemas/govcheck-assurance-evaluation-v1.schema.json`.

Required groups:

| Group | Required meaning |
|---|---|
| `evaluation` | Stable evaluation ID, evaluation time, overall result `pass`, `fail`, `unknown` or `conflict`, and the per-rule results. |
| `repository` | Stable repository URI and VCS kind. |
| `candidate` | Native candidate revision and content/tree identity; for Git, commit and tree IDs; for Pijul, native change-set and channel identities. |
| `base` | Exact native base identity used by the evaluation. |
| `governance` | Governance scope, immutable revision and digest, plus optional profile identity/digest. |
| `verifier` | Verifier URI, version, executable/build digest and configuration digest. |
| `methods` | Zero or more typed assurance activities, their outcomes, scope, inputs/evidence, tools, assumptions and limitations. |
| `independentReview` | Explicit state: `unavailable`, `not_performed`, `attested` or `unknown`. An attested review references a separate review statement by digest. |

Method kinds are `test`, `model_check`, `proof_check`, `inspection`, `analysis` and `other`. Their result is independently typed. A test result is not a proof; a TLC result is evidence about the exact model/configuration/bounds; a proof-check result names the kernel and theorem identity and does not by itself establish implementation refinement.

The predicate records facts and evidence. It does not decide whether a result is acceptable under policy.

## 4. Decision and risk separation

An authority decision is a distinct governance act, not an evaluation result. Risk acceptance is also distinct: it does not rewrite `fail`, `unknown` or `conflict` as `pass`, and must retain authority, rationale, scope, affected claims, residual risk, conditions and expiry. This predicate may reference separate decision/risk records by immutable digest, but must not manufacture them from the evaluation report.

The current authority regime has one root principal. A single-authority decision is not a second-person review. When no second contributor is available, `independentReview.status` is `unavailable`; the evaluator must not infer that a review occurred or treat the absence as a pass.

## 5. Subject binding and detached storage

The attestation must be stored outside the candidate tree it describes (for example as a CI artifact, forge-attached artifact or journal object). It must not be committed into the same candidate whose final commit identity it claims to attest.

The in-toto subject digest identifies a deterministic content snapshot. The predicate additionally binds:
- repository identity;
- VCS kind and native candidate revision;
- candidate tree/content identity;
- exact base revision and identity;
- governance revision and digest;
- verifier build and configuration digests.

Any change to those bindings invalidates reuse. A new candidate/base/policy/verifier/input requires a new evaluation and statement. The evaluation remains historical evidence and is not rewritten.

## 6. Authentication and trust

DSSE signs the payload type and exact payload bytes using PAE. The `keyid` field is an unauthenticated lookup hint, not an identity claim. Consumers must verify signatures against an explicit trust policy and map accepted keys/certificates to stable principal identities and permitted roles.

A valid DSSE signature authenticates the signer of the statement; it does not automatically make that signer an independent reviewer, verifier, governance authority or approver. Consumers must check the signer/verifier pair and role against the relevant trust policy. A free-form `reviewer` field is never sufficient.

The structural Python library builds and validates the in-toto statement payload and DSSE envelope structure, and exposes the DSSE PAE bytes for external signing. It does **not** implement signing or trust-root management. An optional local verifier provider is described by [Architecture 0039](../architecture/0039-detached-dsse-trust-policy.md) and implemented in govcheck/attestation_verify.py: Ed25519 verification is delegated to an OpenSSL executable pinned by absolute path and SHA-256, while the trust-policy file is pinned by an out-of-band digest. This provider is not enabled automatically and does not provide PKI, trusted timestamps or key lifecycle management. Until a trusted verifier adapter is configured, a parsed envelope is structurally valid but unauthenticated and cannot satisfy an attestation gate. The verifier runtime and its trust policy remain part of the trusted computing base.

## 7. SLSA VSA relationship

SLSA VSA is suitable only when GovCheck is summarizing an actual SLSA verification of an artifact against a stated SLSA track/level. Its PASSED/FAILED vocabulary is not a lossless mapping for GovCheck's four-valued evaluation result, and it does not represent GovCheck's authority, decision, risk acceptance or all assurance-method distinctions. A separate VSA may be linked as input evidence; GovCheck must not relabel its own generic result as a SLSA level.

## 8. Conformance and negative cases

A conforming producer/consumer must reject or leave unauthenticated:
- missing or malformed in-toto subject digests;
- unsupported Statement or predicate type;
- missing candidate, base, governance or verifier bindings;
- unknown evaluation/method result codes;
- an `attested` independent-review state without a detached review-statement reference;
- a candidate-tree-local attestation offered as proof of that same candidate's final revision;
- an envelope with missing payload/type/signatures or invalid base64;
- a DSSE envelope whose signature has not been verified by an explicitly trusted verifier;
- a signer identity that is not mapped to the required role;
- stale bindings or evidence.

A valid signature over a structurally valid statement is not proof that the evaluation was correct. It authenticates who signed those bytes under the trust model. The evaluation's method evidence and limitations remain separately assessable.

## 9. Implementation boundary

The first implementation provides a standard-library-only builder/validator for the GovCheck predicate, deterministic JSON serialization, DSSE PAE construction and envelope structure checks. Cryptographic operations are deliberately delegated rather than approximated. Fixtures use synthetic signatures only to test serialization; they do not claim cryptographic validity.

The current `independent-review` checker must not treat a candidate-tree JSON record or a free-form reviewer string as authenticated review. Until an authenticated detached-attestation verifier is integrated, independent review remains `unknown` or `unavailable`.

## 10. References and related records

- [R-227 — DSSE](../references.md#r-227)
- [R-228 — in-toto Attestation Framework v1](../references.md#r-228)
- [R-229 — SLSA Verification Summary Attestation](../references.md#r-229)
- [R-232 — OpenSSL pkeyutl](../references.md#r-232)
- [R-233 — RFC 8032 Ed25519](../references.md#r-233)
- [Architecture 0039 — Detached DSSE verification](../architecture/0039-detached-dsse-trust-policy.md)
- issue #158 — pinned trust-policy verifier
- [R-06 — in-toto project](../references.md#r-06) and [R-07 — SLSA](../references.md#r-07)
- [Specification 0005 — Assurance, Claims and Evidence](0005-assurance-model.md)
- [Specification 0007 — Canonical Governance Journal](0007-canonical-governance-journal-protocol.md)
- [Architecture 0023 — Bootstrap Governance Authority](../architecture/0023-bootstrap-governance-authority.md)
- issue #44, issue #60, issue #131

**This specification is proposed. It does not adopt a trust root, signer policy, cryptographic algorithm or mandatory acceptance rule.**
