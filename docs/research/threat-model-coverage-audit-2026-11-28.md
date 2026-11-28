# Threat-model coverage audit — 2026-11-28

**Status:** source-grounded coverage audit; not a new threat model, security certification or adoption decision.  
**Audit target:** `main` at merge commit `451d1e1ff929946274edba8e844e08d74fdd306f`.  
**Parent work item:** [#70 — threat-model coverage audit](https://github.com/Martin-PB/govcheck/issues/70).  
**French:** [Audit de couverture du modèle de menace](threat-model-coverage-audit-2026-11-28.fr.md).

## 1. Executive result

Architecture 0006 remains a useful threat-and-trust baseline. Its threat categories are still relevant, but its status sentence saying that *no security controls are implemented* is no longer accurate as a description of the repository: several bounded prototypes now exist for detached signature verification, authenticated acceptance decisions, a local Git pre-receive gate and a durable local journal.

Those implementations do **not** amount to a generally deployed or complete security boundary. The decisive distinction is:

1. a threat or mitigation is described in Architecture 0006;
2. a mechanism exists in source code;
3. a test exercises a stated property;
4. the mechanism is installed and enforced in a real deployment against the relevant adversary.

The audit finds multiple examples at levels 2–3, but does not establish level 4 for the repository's actual GitHub merge boundary. A local Git pre-receive prototype is tested against an isolated bare repository; it is not installed as GitHub's enforcement mechanism. The read-only forge ruleset audit reports configuration conformance only and explicitly does not demonstrate a real protected-ref rejection.

This audit is source inspection of the exact `main` revision above. It did not trigger Actions, execute the test suite, run TLC or compile Lean. References to test files establish the existence and scope of test cases, not a fresh successful execution in this audit.

## 2. Classification

- **Documented:** the threat or intended treatment appears in Architecture 0006 or a linked design record.
- **Implemented:** code exists for at least one bounded profile.
- **Tested:** a named test exercises the stated property. This audit does not claim that the test was rerun.
- **Operationally demonstrated:** the control is installed and has successfully blocked the relevant real deployment path. This is the strongest category and is not inferred from unit tests or configuration inspection.
- **Gap / residual risk:** a missing control, incomplete scope, unverified deployment, or adversary outside the mechanism's trust boundary.

## 3. Coverage matrix

| Architecture 0006 threat / objective | Repository evidence | Coverage assessment | Residual risk / follow-up |
|---|---|---|---|
| Weaken or delete a governance rule | PR-based source changes; repository branch protection configured by the maintainer; local Git pre-receive prototype in `scripts/govcheck-git-pre-receive`; Architecture 0037 | **Partial; prototype tested.** The Git hook can reject protected ref updates when installed on a controlled bare server. The actual GitHub acceptance path is not demonstrated by this hook. | #45 remains open: verify the live ruleset, required trusted checks, direct-push restrictions, administrator bypass and an actual rejection. The precise current GitHub configuration was not re-read as part of this audit. |
| Ambiguous or conflicting rules | `govcheck/check.py` returns distinct pass/fail/unknown outcomes; acceptance decision and gate reject fail/unknown/conflict outcomes | **Partial.** Fail-closed outcomes exist in the executable slice and acceptance adapter. | This does not establish a complete, general policy-conflict resolver or coverage of every normative rule. |
| Scope confusion / profile shadowing | Acceptance decision binds repository, candidate, base, protected ref, governance revision and scope; gate checks pinned repository and ref configuration | **Partial; bounded binding implemented.** | General profile inheritance, precedence and non-derogable foundations are not shown to be completely enforced by one canonical evaluator. |
| Malicious policy expression | Architecture 0006 recommends data over executable policy; no general expression language is selected | **Design constraint only.** No arbitrary policy language is currently required by the slice. | If executable policy or repository-authored expressions are introduced, they need a separate bounded-language and execution threat assessment. |
| Path traversal / symlink escape | `attestation_verify.py` rejects trust policy, key and verifier paths inside the candidate-controlled tree, including resolved paths | **Partial; targeted path checks implemented.** | This is not a repository-wide proof of safe path handling for all commands, archives, build tools or VCS adapters. |
| Parser / canonicalization differential | Detached verifier rejects duplicate JSON keys, floats and non-finite values; journal defines `govcheck.jcs-safe-integer/v1`, rejects duplicate keys/floats and uses UTF-16 property ordering | **Partial; strict profiles implemented.** | The same canonicalization contract is not established for every JSON consumer (including the first check slice). Cross-implementation conformance vectors and size/depth limits remain relevant. |
| Evidence replay | Specification 0010 binds a signed decision to exact candidate revision/content digest, base, ref, policy, scope, verifier and evaluation-report digest; detached DSSE verifier checks signature and role | **Implemented in the optional local profile.** | The provider is not enabled automatically. Trusted timestamps and historical verification after key expiry/revocation are not provided. |
| Candidate mutation after approval / stale evidence | Git gate receives exact old/new/ref tuple; decision verifier checks exact candidate, base, policy, scope and report digest; integration tests include stale-decision rejection | **Implemented and integration-tested in an isolated Git repository.** | The actual GitHub merge candidate/base and post-merge protected-ref path are not bound to this local adapter today. |
| Forged approval / signer attribution | Architecture 0039; optional Ed25519 DSSE verifier using operator-pinned OpenSSL binary, public-key digests, key IDs, principals and roles | **Implemented as an optional provider; synthetic cryptographic fixtures exist.** | A valid signature proves possession of a configured key, not a real-world identity, employment or independence. Operator trust-policy custody remains critical. |
| Compromised or revoked signing key | Trust policy supports validity intervals and revocation state; policy, key and OpenSSL executable are digest-pinned | **Partial.** Verification checks configured validity/revocation state. | No full key issuance, custody, rotation, incident response or trusted timestamp service is supplied. The operator can change the trust root and expected digest. |
| VCS adapter lies or loses semantics | Git pre-receive hook and `git_acceptance_gate.py`; integration test creates an isolated bare Git repository and exercises accepted/rejected pushes | **Partial; Git prototype tested.** | No mandatory Pijul remote/server adapter is implemented or demonstrated. A local Pijul hook is not equivalent to remote enforcement. |
| Forge bypass / optional checks | `govcheck/forge.py audit-ruleset` reads ruleset scope, required checks/source and bypass configuration; acceptance research explicitly sets `boundary_demonstrated=false` | **Read-only audit implemented; enforcement not demonstrated.** | A ruleset audit is not a merge gate. #45 remains the canonical work item. Branch protection and required-check settings must be inspected live and bypass-tested; no claim is made here that the current GitHub configuration enforces GovCheck. |
| Malicious project check scripts / dependencies | Architecture 0006 identifies project scripts/builds/scanners as untrusted and calls for explicit execution policy, least privilege and resource limits | **Gap confirmed.** The acceptance gate separates its trusted verifier from the candidate tree, but does not sandbox arbitrary project-controlled build/test/scanner commands. | New candidate work item [#218](https://github.com/Martin-PB/govcheck/issues/218) specifies execution isolation, secret exposure and resource budgets without selecting a universal sandbox. |
| Resource exhaustion | SQLite journal uses a bounded busy timeout; some parsers have strict input handling | **Partial / not general.** | No repository-wide time, memory, process, disk, network or output budget is demonstrated for untrusted checks and parsing. Tracked with #218. |
| Secret leakage | Forge adapter reads tokens from environment and documents that tokens are not persisted in reports/logs; check workflow uses `contents: read` | **Partial.** | No comprehensive proof of secret non-exposure by arbitrary project commands, subprocesses, test output, artifacts or third-party actions. Tracked with #218 and workflow-specific review. |
| TOCTOU / concurrent update | SQLite journal uses transactional `BEGIN IMMEDIATE`, expected-head compare-and-append, idempotency and durable receipts; Git gate checks exact ref update tuple | **Implemented and covered by targeted tests.** | Local journal integrity does not authenticate actors or resist a privileged database administrator. A live forge merge race is not demonstrated. |
| Compromised forge/server administrator | Architecture 0006 explicitly treats local/admin access and forge bypass as trust-boundary limits; local gate executable and policy are installed outside candidate tree | **Threat documented; limitation explicit.** | A server administrator can replace the hook/runtime or alter configuration. A GitHub administrator or bypass actor may alter rules. No independent control currently removes this trust assumption. |
| Auditability / history integrity | SQLite hash-chain journal, immutable event/receipt triggers, chain verification and durable receipts; Architecture 0038 | **Implemented as a local integrity profile.** | A hash chain is not actor authentication or tamper-proof storage. A privileged administrator can rewrite the database and recompute the chain absent an external trusted checkpoint. |

## 4. Consolidated findings

### 4.1 Real progress

The repository has moved beyond the original Architecture 0006 statement that no security controls exist:

- **Detached evidence verification:** an optional Ed25519/DSSE verifier checks canonical payload structure, exact bindings, key IDs/roles, validity/revocation state and pinned OpenSSL/key digests (Architecture 0039; `govcheck/attestation_verify.py`).
- **Acceptance decision:** Specification 0010 separates evaluation from an authenticated authority decision and binds that decision to the exact candidate, base, policy, scope, verifier and report digest.
- **Git enforcement prototype:** a server-installed pre-receive hook delegates to an externally installed and digest-pinned gate; the isolated integration tests exercise PASS acceptance and rejection of UNKNOWN/stale or mismatched decisions.
- **Local journal:** the SQLite profile provides transactional append, expected-head concurrency control, idempotent retry, durable receipts and hash-chain verification (Architecture 0038).

These are bounded implementation increments, not evidence that every repository deployment has them installed.

### 4.2 Principal gaps

1. **No demonstrated GitHub enforcement boundary.** The repository has a read-only ruleset auditor and a local Git server prototype, but no demonstrated GitHub App/check source that is required for the exact merge candidate, no real protected-ref rejection test on GitHub, and no complete bypass test. This remains #45.
2. **No sandbox contract for repository-controlled checks.** The threat model names this risk, but the code does not establish isolation, secret minimization or resource budgets for arbitrary project scripts/build tools. This is now tracked as candidate issue #218.
3. **Trust-root lifecycle is incomplete.** Key-to-principal mapping, revocation state and pinned digests exist, but key custody, rotation, compromise response and trusted historical timestamps remain deployment responsibilities. Continue under #44 and the related trust-policy work.
4. **No remote Pijul enforcement.** The Git prototype must not be generalized to Pijul or to all VCS adapters.
5. **No protection against a fully privileged administrator.** Local database, gate, trust policy, forge rules and server runtime remain inside explicit administrative trust assumptions.

### 4.3 No invented independent reviewer

The current single-contributor situation remains a material residual risk, not a reason to synthesize an approval. A cryptographic signature from a key assigned a role does not create independent review unless the key is genuinely controlled by a distinct authorized principal. See #60 and #71.

## 5. Work-item disposition

| Work item | Audit result |
|---|---|
| #44 — interoperable attestations | Continue: trust-root lifecycle, real identity and detached independent-review semantics remain open. |
| #45 — acceptance boundary | Continue: actual GitHub enforcement and bypass/rejection demonstrations remain open. |
| #60 — single-authority residual risk | Keep explicit; do not claim separation of duties. |
| #70 — this audit | Coverage matrix completed by this proposal; close only after this report is reviewed/merged and the issue is updated with the remaining follow-ups. |
| #72 — adversarial candidate corpus | Continue: use the threat categories above to add exact-candidate positive and negative fixtures. |
| #218 — execution isolation | New candidate backlog item for the confirmed sandbox/resource/secret-exposure gap. |

## 6. Scope and limitations

This report is not a penetration test, independent security review, certification, formal proof of implementation correctness or confirmation of live forge configuration. It does not change Architecture 0006's threat assumptions, adopt an enforcement policy, activate a sandbox, change branch protection or assert that the local gate is deployed.

The report's status distinctions should be preserved in subsequent documentation: documented, implemented, tested and operationally demonstrated are separate claims.

## 7. Repository evidence inspected

- [Architecture 0006 — Threat and Trust Model](../architecture/0006-threat-and-trust-model.md) and its French counterpart.
- [Architecture 0037 — Acceptance Boundary and Enforcement Adapters](../architecture/0037-acceptance-boundary-and-enforcement-adapters.md).
- [Architecture 0038 — Local Canonical Journal Implementation Profile](../architecture/0038-local-canonical-journal-implementation.md).
- [Architecture 0039 — Detached DSSE Verification and Pinned Trust Policy](../architecture/0039-detached-dsse-trust-policy.md).
- [Specification 0008 — Interoperable Assurance Attestations](../specifications/0008-interoperable-assurance-attestations.md).
- [Specification 0009 — Independent Review Attestations](../specifications/0009-independent-review-attestations.md).
- [Specification 0010 — Authenticated Acceptance Decisions](../specifications/0010-authenticated-acceptance-decisions.md).
- [Acceptance-boundary enforcement research](acceptance-boundary-enforcement-2026-11.md).
- Source: `govcheck/attestation_verify.py`, `govcheck/git_acceptance_gate.py`, `govcheck/forge.py`, `govcheck/journal.py`, `scripts/govcheck-git-pre-receive`.
- Tests: `tests/test_attestation_verify.py`, `tests/test_git_acceptance_gate.py`, `tests/test_pre_receive_acceptance_integration.py`, journal tests.
- [Work-item register](../work-portfolio/work-items.md), issues #44, #45, #60, #70, #72 and #218.
