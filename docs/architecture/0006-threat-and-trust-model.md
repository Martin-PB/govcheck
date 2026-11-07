# Architecture 0006 — Threat and Trust Model

**Status:** Proposed for review; no security controls are implemented. **French:** [0006 (fr)](0006-threat-and-trust-model.fr.md).

## 1. Assets

Protect: canonical governance package and its history; repository content and exact state identity; change records and approvals; evidence and provenance; signing keys/identities; evaluator and adapter binaries/configuration; local and remote acceptance decisions; user data and credentials encountered by project checks.

## 2. Security objectives

- Integrity: rules, states, evidence and decisions cannot be silently altered.
- Authenticity/authority: approvals and attestations are attributable to authorized principals.
- Binding: every decision/evidence item names the exact repository, candidate and governance semantics.
- Freshness: stale or invalidated evidence cannot authorize a changed candidate.
- Availability: resource exhaustion or unavailable adapters produce explicit blocked/indeterminate outcomes, not false success.
- Confidentiality: secrets and private repository data are not unnecessarily copied into reports, logs or remote services.
- Auditability: corrections append history; they do not erase prior events.

## 3. Adversaries and failure sources

Consider malicious or compromised contributors; compromised coding agents; malicious repository content; compromised dependencies/build tools; forged or revoked identities/keys; compromised forge/team server; stale or malicious external data; buggy parser/evaluator/adapters; accidental operator error; race conditions and partial failures. These are threat scenarios, not assumptions that every environment has the same attacker.

## 4. Trust boundaries

1. **Normative input:** canonical governance, schemas and profiles. Treat repository-supplied content as untrusted until parsed and validated.
2. **Evaluator:** parser, canonicalizer, semantic engine and policy resolution. This is central to the trusted computing base (TCB).
3. **Checks:** project scripts/builds/scanners run with project-specific privileges and may be malicious. GovCheck should orchestrate them only under an explicit execution policy; never imply a portable local CLI makes arbitrary code safe.
4. **VCS adapters:** native state and conflict interpretation must be correct. Adapter output is security-sensitive.
5. **Evidence producers/verifiers:** tool output, signatures, timestamps and external facts have distinct trust properties.
6. **Local operator boundary:** a user with filesystem/admin access can modify files, disable hooks or replace binaries. Local enforcement is advisory against that adversary.
7. **Shared acceptance boundary:** a trusted team service or forge integration can enforce decisions, subject to its own administrator, credential and bypass risks.
8. **Documentation projections:** generated Markdown may drift or be edited; it is not normative input.

## 5. Principal attacks and required treatment

| Threat | Required treatment / safe outcome |
|---|---|
| Weaken or delete a rule | Stable IDs, reviewable semantic diff, history, protected governance changes |
| Ambiguous/conflicting rules | Deterministic conflict detection; fail closed |
| Scope confusion / profile shadowing | Explicit scope and partial precedence; mandatory foundations cannot be weakened |
| Malicious policy expression | Prefer data over executable policy; typed bounded language if ever needed; no arbitrary evaluation |
| Path traversal / symlink escape | Canonical path handling, explicit repository root, reject escapes and ambiguous paths |
| Parser/canonicalization differential | One specified canonicalization; reject duplicate keys/ambiguous encodings; cross-implementation vectors |
| Evidence replay | Bind to exact state, governance revision, evaluator/tool versions and dependencies |
| Candidate mutation after approval | Recompute fingerprint at application boundary; stale decision |
| Forged approval | Authenticated identity, authority check, signature/key lifecycle and revocation policy |
| Compromised signing key | Revocation, rotation, affected-evidence invalidation and incident record |
| VCS adapter lies or loses semantics | Native contract tests; unsupported/unknown is indeterminate |
| Forge bypass/admin override | Declare enforcement capability and bypass visibility; never claim absolute enforcement |
| Malicious check script/dependency | Explicit execution boundary, resource limits and least privilege; out of scope for governance semantics alone |
| Resource exhaustion | Bounded parsing/evaluation, time/memory limits, explicit incomplete result |
| Secret leakage in logs/reports | Redaction policy, data minimization, local-by-default evidence storage |
| TOCTOU / concurrent update | Compare-and-swap preconditions and recheck exact candidate immediately before apply |

## 6. Explicit non-goals and limitations

GovCheck alone cannot prevent a local administrator from editing repository files, replacing the executable, or bypassing hooks. A signature proves neither correctness nor policy authority without trusted identity and key governance. A test result does not establish safety of the test runner. A forge gate cannot protect against an administrator who can disable the gate unless an independent control exists. No claim of tamper-proof, hermetic, or zero-trust operation is made.

## 7. Required design decisions before implementation

Define canonical serialization and duplicate-key handling; evaluator isolation and resource limits; key/identity/approval model; evidence storage and privacy; local execution model for project checks; remote enforcement protocol and bypass reporting; threat-specific security tests. Keep these as explicit decisions, not accidental implementation defaults.


## Bibliographic references

- [R-01 — NIST SP 800-53 security and privacy controls](../references.md#r-01)
- [R-02 — NIST SP 800-218 secure software development practices](../references.md#r-02)
- [R-06 — in-toto software supply-chain provenance](../references.md#r-06)
- [R-07 — SLSA software supply-chain assurance](../references.md#r-07)
- [R-27 — NIST SP 800-30 risk assessment](../references.md#r-27)
- [R-28 — NIST SP 800-160 trustworthy secure-systems engineering](../references.md#r-28)
- [R-29 — ISO 31000 risk-management guidelines](../references.md#r-29)
- [R-30 — MITRE ATT&CK adversary tactics and techniques](../references.md#r-30)
- [R-31 — Microsoft SDL threat-modeling guidance](../references.md#r-31)
- [R-32 — Schneier attack-tree method](../references.md#r-32)
- [R-72 — Runtime threat modeling from production observations](../references.md#r-72)
- [R-75 — NIST continuous security monitoring](../references.md#r-75)
- [R-76 — Runtime certification and monitoring assumptions](../references.md#r-76)
