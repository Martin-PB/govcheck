# Adversarial candidate corpus — version 1.2.0

**Status:** version 1.2.0 corpus catalogue with executable-test pointers; not a claim that every attack has a runnable fixture or that the acceptance boundary is deployed.  
**Snapshot:** corpus v1.2.0 candidate based on source revision `7366914aa347f87b1ce817c90f468cfa9688a45c`; the v1.1.0 baseline was audited against `451d1e1ff929946274edba8e844e08d74fdd306f`.  
**Parent:** [Issue #72](https://github.com/Martin-PB/govcheck/issues/72).  
**French:** [Corpus de candidats adversariaux](adversarial-candidate-corpus-v1.fr.md).  
**Machine-readable manifest:** [`formal/adversarial-candidate-corpus-v1.json`](../../formal/adversarial-candidate-corpus-v1.json).

## 1. Purpose and interpretation

This corpus records positive, adversarial, boundary and currently untested scenarios for the evaluator and acceptance adapters. It is intentionally not a single generic "attack score". Each case states:

- the attack or boundary condition;
- the expected outcome;
- how the candidate and base/policy context are bound;
- the existing test/model/document that supplies evidence;
- the coverage status and residual limitation.

The corpus distinguishes `tested-unit`, `tested-integration`, `model-only`, `planned` and `not-demonstrated`. A test pointer is not a claim that the test was rerun in this change. A model-only case is not an implementation test. A configuration audit is not proof that a forge rejects a real update.

## 2. Binding and provenance

The manifest pins the source snapshot from which its initial test pointers were audited. Unit tests may use deterministic synthetic candidate/base values or generate ephemeral signing keys and policies. The local Git integration tests create exact temporary commit IDs and bind decisions to the old/new/ref tuple at runtime. In each case, the test itself must exercise the exact values it generated or declared; a test result must not be generalized to another candidate or policy.

There is deliberately no shared production trust-policy digest in this corpus. Ephemeral keys and test policies are test material, not GovCheck trust roots. All current entries declare `deploymentStatus: not-demonstrated`: even an isolated Git integration test does not show that the same gate is installed on a production forge.

## 3. Initial coverage map

| Case range | Area | Existing evidence | Current status |
|---|---|---|---|
| AC-001–AC-003 | Acceptance decision, report digest, candidate binding, PASS/risk distinction | `tests/test_acceptance_decision.py` | Unit-tested |
| AC-004–AC-005 | DSSE signature, signer role/principal, key expiry/revocation | `tests/test_attestation_verify.py` | Unit-tested with synthetic keys |
| AC-006–AC-009 | Gate result handling, exact tuple/pins, protected refs and explicit risk path | `tests/test_govcheck_git_pre_receive.py` | Unit-tested |
| AC-010–AC-011 | Stale decision and real local bare-Git receive behavior | `tests/test_pre_receive_acceptance_integration.py`, `tests/test_govcheck_git_pre_receive_integration.py` | Isolated integration-tested |
| AC-012–AC-013 | Forge ruleset configuration and non-applicable refs | `tests/test_govcheck_forge.py`, `tests/test_govcheck_git_pre_receive.py` | Unit-tested; configuration only |
| AC-014–AC-015 | Journal concurrency and canonical JSON parsing | `tests/test_journal.py` | Unit-tested |
| AC-016 | Enforced/advisory/admin-bypass acceptance-boundary abstraction | `formal/tla/GovCheckAcceptanceBoundary.tla` and configurations | Model-only |
| AC-017 | Workflow path-filter symmetry, reusable-workflow routing, unsupported path syntax and model-input routing | `tests/test_ci_workflow_routing_audit.py` | Unit-tested on synthetic repository fixtures; not a forge gate |
| AC-018 | Stale TLC report replay across model/config/workflow/report revisions | `tests/test_tlc_run_manifest.py` | Unit-tested on synthetic Git repositories; unsigned manifest, not hosted-run attestation |
| AC-019 | Lean `sorry`/axiom injection | No corpus-specific executable test yet | Planned |
| AC-020 | Real GitHub protected-ref rejection and bypass | Acceptance-boundary research and live configuration still need verification | Not demonstrated; tracked by #45 |
| AC-023 | Report-only workflow is not a mandatory acceptance check under the live ruleset | Workflow and live ruleset snapshot | Not demonstrated; required-check list is empty; tracked by #45 |
| AC-021 | Pijul remote/Nest enforcement bypass | Platform research only | Planned; no remote enforcement adapter |
| AC-022 | Malicious repository-controlled check execution, secret exfiltration and resource exhaustion | Architecture 0006; candidate issue #218 | Planned; no sandbox selected |

The machine-readable manifest is the source of the case IDs and exact evidence pointers. Version 1.2.0 adds AC-018 source-bound TLC run manifests and synthetic stale-replay tests. The manifest records checkout/run metadata, model/config/reusable-workflow Git blobs, a discoverable caller-workflow blob, and report digests; tests reject drift and replay. It is unsigned and does not bind governance revision/evaluator identity or authenticate GitHub's hosted execution. It is not proof of a mandatory check. AC-017 now maps the existing synthetic workflow-routing tests: asymmetric PR/push path filters, missing or unrouted reusable workflows, unsupported path syntax, unjustified globs and model-input routing. These tests do not prove a live GitHub required-check gate. AC-023 records the distinct live gap: the report-only workflow is not a mandatory check under the current ruleset. `tests/test_adversarial_candidate_corpus.py` checks manifest identity/versioning, unique IDs, required semantics, evidence-file existence and referenced Python test-method names. This integrity test does not itself execute the underlying attacks.

## 4. Important limits

1. **No production enforcement claim.** The current local Git hook prototype is not a GitHub App or a live hosted-merge gate.
2. **No synthesized independent reviewer.** Test keys and fixture principals do not establish an independent human reviewer.
3. **No general Pijul enforcement.** A local hook is not a mandatory remote acceptance boundary.
4. **No arbitrary project-code sandbox.** Execution isolation, secret minimization and resource budgets remain candidate work in #218.
5. **Partial AC-018 coverage only.** Synthetic tests now reject stale model/config/workflow/report inputs. The unsigned manifest does not authenticate the hosted run or bind governance revision/evaluator identity; AC-019's Lean `sorry`/axiom injection remains planned.

## 5. Next increments

- Turn AC-019 (Lean `sorry`/axiom injection) into exact-candidate negative fixtures; expand AC-017 only for workflow-tampering paths not covered by the routing audit.
- Extend the corpus with the specific attack paths and trust assumptions from Architecture 0006.
- Bind any new test report to the corpus revision, test/tool version, exact candidate/base, applicable policy and verifier identity.
- Add a real forge-boundary experiment only when its required configuration and test environment are explicitly authorized and available.

This catalogue does not adopt a new normative rule, modify the branch-protection configuration or claim that a planned case is already tested.
