# Specification 0010 — Authenticated acceptance decisions

**Status:** proposed implementation contract for issue #45; not a new authority regime and not a claim that the forge currently enforces it. **French:** [0010](0010-authenticated-acceptance-decisions.fr.md).

## 1. Purpose

Separate an evaluation result from an authority's acceptance decision. A report records evidence and retains its own `pass`, `fail`, `unknown` or `conflict` result. A decision is a distinct, authenticated governance act bound to one exact candidate and evaluation.

A green CI check, signed evaluation or local journal receipt is not itself an authority decision.

## 2. Statement and predicate

The decision is an in-toto Statement v1 with predicate type:

`urn:govcheck:attestation:acceptance-decision:v1`

The strict JSON Schema is `../../formal/schemas/acceptance-decision-v1.schema.json`. The predicate binds repository ID, candidate revision/content digest, base revision, protected ref, governance revision, scope, exact evaluation-report digest, decision ID, decision time assertion and rationale.

The decision signer is authenticated by DSSE and mapped to the required `governance-authority` role in an operator-pinned trust policy. There is no free-form authority-principal field; the authority principal comes from the verified signer.

## 3. Evaluation report binding

`evaluationDigest` is SHA-256 of the exact serialized evaluation-report file bytes supplied to the gate. The verifier must parse those same bytes and compare the parsed report object with the object being evaluated; it must not accept a separately supplied report object that differs from the signed digest input.

The decision additionally binds the full candidate revision, candidate content digest, base revision, ref, governance revision and scope. Any mismatch or stale report is rejected.

## 4. Decision semantics

- **`accept`:** permitted only when the bound evaluation report has overall result `pass`.
- **`reject`:** denies acceptance regardless of evaluation result.
- **`accept_with_risk`:** a separate scoped authority act for a report that is not `pass`. It requires a complete risk record: identifier, reason, scope, expiry, residual risk, affected claims and authorization-record digest.

Risk acceptance must match the candidate scope and must not be expired at verification time. It does not rewrite the report's `fail`, `unknown` or `conflict` result as `pass`. The decision remains historical evidence and is not a test, proof or independent review.

## 5. Failure and uncertainty

Missing envelope, trust policy, role, signer mapping, report bytes or exact bindings produce `unknown` or `fail`; they never produce PASS. Invalid signatures, rejected decisions, stale report digests, mismatched candidate/base/ref/policy/scope, incomplete or expired risk records are rejected.

`decidedOn` is a signed assertion, not trusted timestamp evidence. Key validity is checked against the verifier's current time; no historical signing-time proof is provided.

## 6. Enforcement boundary

This predicate is a portable authority-decision contract. The local Git pre-receive adapter still requires a separately installed and digest-pinned gate executable, and its v0 output protocol is an adapter boundary. The read-only GitHub ruleset audit does not itself enforce this decision.

A completed acceptance boundary additionally requires:
- a trusted gate executable and its runtime closure installed outside the candidate tree;
- a forge ruleset requiring PRs and exact status checks from a trusted source;
- re-evaluation of the actual merge candidate/base;
- a real protected-ref update test that demonstrates rejection of FAIL/UNKNOWN/stale evidence;
- documented administrator and alternate-transport bypass limits.

No repository ruleset is changed by this specification.

## References

- [R-06 — in-toto](../references.md#r-06)
- [R-232 — OpenSSL pkeyutl](../references.md#r-232)
- [R-233 — RFC 8032 / EdDSA](../references.md#r-233)
