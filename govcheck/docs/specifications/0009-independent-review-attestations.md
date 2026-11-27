# Specification 0009 — Detached independent-review attestations

**Status:** implementation contract for issue #160; proposed for review, not a new authority rule or a claim that a real independent review exists. **French:** [0009](0009-independent-review-attestations.fr.md).

## 1. Purpose and boundary

Define a detached, authenticated review record that can be consumed by GovCheck without treating a free-form reviewer name, a Git author string, a signature alone, or a test fixture as proof of human independence.

The review record is evidence. It does not itself authorize a merge, accept risk, or change the governance authority model. With only one available contributor, GovCheck must continue to report independent review as unavailable/UNKNOWN.

## 2. Statement and predicate

The review is an in-toto Statement v1 using predicate type:

`urn:govcheck:attestation:independent-review:v1`

The strict JSON Schema is `../../formal/schemas/independent-review-v1.schema.json`. The separate forge-author identity predicate schema is `../../formal/schemas/forge-author-identity-v1.schema.json`. The review predicate binds:

- candidate revision and candidate content SHA-256;
- exact base revision;
- governance revision and scope ID;
- reviewer-asserted `reviewedOn` timestamp;
- outcome `accepted` or `changes_requested`;
- non-empty list of reviewed claim identifiers;
- observations and non-empty limitations.

The Statement subject digest must equal `candidateContentSha256`. The predicate deliberately has no reviewer identity field.

## 3. Candidate content digest

The evaluator computes a deterministic snapshot SHA-256 over the candidate checkout. Files are ordered by normalized relative POSIX path; directories and any path containing a `.git` component are excluded. Regular-file payload is its exact byte content. Symlink payload is UTF-8 `symlink:` followed by the link target.

For each file, the digest stream receives an unsigned 64-bit big-endian length and the path bytes, followed by an unsigned 64-bit big-endian length and payload bytes. SHA-256 of the resulting stream is the candidate content digest.

The checkout must be clean (tracked and untracked files) and `HEAD` must equal the full candidate revision. Otherwise the independent-review rule cannot pass. This prevents a review of working-tree extras from being attributed to a different commit.

## 4. Identity and trust

The reviewer principal is derived only from the verified DSSE signer and the operator-pinned trust policy's key-ID/principal/role mapping. The required reviewer role is `independent-reviewer`. The authenticated reviewer principal must differ from the author principal.

The author principal and source URI are carried by a detached `forge-author-identity/v1` Statement signed by a forge identity provider. Its signer must be authorized by the operator-pinned trust policy under an explicit forge-identity role. The predicate binds the candidate revision/content, base, governance and scope. The evaluator verifies this envelope, requires its signed `sourceUri` to equal the operator-pinned expected source URI, and derives `authorPrincipal` from the signed predicate; `--author-principal` is only an optional consistency check. The CLI does not itself authenticate a forge API: the provider signature and trust-policy mapping are the trust boundary. Git author metadata alone is not an authenticated principal.

The assurance Statement is separately detached and verified under an explicit trust-policy role. Its `independentReview.status` must be `attested`, and its `independentReview.reference.digest.sha256` must equal SHA-256 of the exact review-envelope file bytes. Both envelopes and the trust policy must be outside the candidate tree.

`reviewedOn` is a signed reviewer assertion, not trusted timestamp evidence. No production key or reviewer account is created by this specification.

## 5. Evaluator semantics

- **PASS:** review and assurance DSSE envelopes are verified; required roles are authorized; reviewer differs from author; all candidate/base/governance/scope/content bindings match; assurance references the exact review envelope; outcome is `accepted`.
- **FAIL:** malformed or invalid signature/evidence, binding mismatch, reviewer/author collision, assurance-reference mismatch, or `changes_requested`.
- **UNKNOWN:** missing detached evidence, trust policy, role, full revisions, clean candidate checkout, or independently trusted author identity/source.

The rule is fail-closed. A verified signature authenticates the signer of the statement; it does not prove that the review was thorough or that its claims are correct.

## 6. Interoperability and non-claims

DSSE authenticates the payload type and exact payload bytes through PAE. `keyid` is only a lookup hint. GovCheck's role and principal mapping remain external trust-policy decisions.

This specification does not define trusted time, production key lifecycle, forge API authentication, review quality scoring, or an authority decision. It does not claim that synthetic tests constitute a real second-person review.

## References

- [R-06 — in-toto](../references.md#r-06)
