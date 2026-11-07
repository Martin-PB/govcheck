# 0010 — Assurance, testimony, proof and conformance

**Status:** Detailed reconstruction of the GovCheck discussion of 5–6 November 2026. Complements memory 0009 and specification 0005; does not replace them. **French:** [0010 (français)](0010-assurance-proof-and-conformance.fr.md).

## 1. Foundational problem: self-certification is not verification

GovCheck must do more than run checks. It must prevent the producer of a change—human or agent—from being the sole authority declaring that change compliant.

A contributor may state which requirements they believe apply, which commands ran, which results were observed, which tests passed or failed, their assumptions and requested deviations. These statements are useful inputs, but are not independent verification merely because they are asserted. An agent cannot turn its own narrative, generated report or success verdict into final authority. The same rule applies to a human.

GovCheck independently evaluates the governance contract and submitted evidence. Independence depends on the parser, evaluator, tools, identities, authority sources, adapters and enforcement boundary. It must be argued and documented, not implied by a green check.

The responsibility chain is: approved normative source → interpretation of applicable rules → scoped claim → evidence → argument and assumptions → decision by authorized authority → acceptance of the exact candidate → native application of that exact candidate. No step can be replaced by contributor self-description.

## 2. Three independent assurance questions

### 2.1 Is GovCheck correct relative to its formal specification?

This concerns implementation correctness: parser and canonicalization; rule composition; rejection of mandatory indeterminate results; lifecycle guards; native candidate identity in adapters; refinement of the abstract model.

Possible evidence includes tests, property-based tests, model checking, proofs of components, verified compilation and refinement proofs. These are not equivalent. Tests do not cover all cases; a checked model does not prove the implementation; a theorem about one function does not prove the whole executable.

### 2.2 Does the specification faithfully represent approved governance?

This is normative fidelity. A perfectly verified evaluator can implement an incomplete, ambiguous or normatively wrong specification. Proving that the implementation follows the specification does not prove that the specification expresses the right rules.

Fidelity requires traceability: approved clause/decision → canonical rule ID → explicit normative force and applicability → formal predicate/transition → property/test vector → approval by the competent authority. Markdown projections and translations must preserve meaning. Semantic assistance, including AI, can find ambiguity, contradiction and gaps, but does not become normative authority. An authorized reviewer approves interpretation; an agent cannot approve its own interpretation.

### 2.3 Does the exact project/change comply?

This is subject-level conformance. Evidence must bind exact repository, base, candidate, governance, specification and relevant environment identities. GovCheck correctness does not prove project compliance. A successful build does not cover every obligation. A signature does not prove relevance or truth. An approval does not replace technical evidence.

| Question | Subject | Required bridge | Invalid shortcut |
|---|---|---|---|
| Correctness | GovCheck implementation | Implementation/specification conformance | “Tests pass, therefore the program is correct.” |
| Fidelity | Normative interpretation | Traceability and approval | “The evaluator is proved, therefore the policy is right.” |
| Conformance | Exact candidate | Subject-bound evidence, rules and authority | “GovCheck is verified, therefore this change complies.” |

Effectiveness of the deployed mechanism is a fourth question: a correct local evaluator can be bypassed; a gate can be disabled; a process can fail in operation.

## 3. Test, testimony, evidence, attestation and proof

**A test is execution testimony.** It records that a particular invocation, program, inputs and environment produced an observation. Its record binds exact source/candidate, test suite/data, command/arguments, tool versions, environment, execution identity/time, outputs/exit status, partial/interrupted status, provenance and integrity.

A passing suite establishes that tested cases produced expected observations under recorded conditions. It does not establish correctness for all inputs, absence of untested defects, correctness of the oracle, normative validity of the requirement, truth of unchecked external facts, conformance of another candidate or production bypass resistance. A failure may be a concrete counterexample if the test and observation are trustworthy. A pass is scoped positive evidence, not universal proof. This applies to unit, integration, system, regression, security, fuzz, property-based and end-to-end tests. More tests and coverage improve observation; they do not turn empirical execution into mathematical proof.

**Evidence** is broader than tests: build/scan results, model-checking reports, proof objects/results, attestations, VCS identities/diffs, review decisions, operational measurements, external facts and reproducible derivations. Evidence may support, refute or leave a claim inconclusive. Contradictions remain visible. An item is not true because it is stored, hashed, signed or labelled “verified”.

**An attestation is not proof of its content.** It binds a statement to a producer, subject and context. A signature may establish integrity and origin under key-management assumptions. It does not by itself establish signer authority or independence, actual command execution, runner integrity, input identity, output relevance or external truth. Authenticity, integrity, authority, relevance and truth are distinct.

**A mathematical proof is a checked derivation** relative to a logic, kernel, definitions, axioms, hypotheses and imports. The record identifies theorem, kernel version, axioms/imports, hypotheses, admitted obligations, unsafe features/oracles and dependencies. The kernel establishes derivability in that system; it does not prove that the theorem captures the real requirement or that the program implements it without a formal bridge.

## 4. Model checking, theorem proving and implementation conformance

**Model checking** explores reachable states of a formal system. A completed exhaustive exploration establishes properties for every reachable state of the configured model. Bounded/reduced exploration is limited to its bounds and assumptions. A TLA+/TLC report records model revision/digest, TLC/Java versions, configuration/constants, symmetry/reductions/constraints, fairness, properties, state/transition counts, completion, deadlocks/counterexamples and bounds. A counterexample exhibits a model behavior violating a property. A successful run does not prove the real program.

**Theorem proving** establishes derivability from formal axioms and hypotheses. Proving mathematical properties of the acceptance predicate does not prove that code computes it correctly. Proving that the evaluator follows a specification does not prove the specification's normative fidelity.

**Conformance/refinement** is the bridge from model to executable. It identifies implementation/model revisions, build artifact, abstraction boundary, observable behavior, refinement/simulation relation, assumptions and method. Verified implementation, refinement proof, verified code generation, trace refinement, differential tests and conformance vectors are not equivalent. Passing examples do not prove complete refinement.

**Normative fidelity** concerns the mapping from approved rules to model, predicates, tests and documents. It requires traceability and authority. Formal tools check consistency after meaning is approved; they do not choose meaning for the organization.

## 5. Three assurance dimensions

They are complementary, not interchangeable maturity levels.

- **Mechanical:** schemas/types, canonicalization, duplicate keys, IDs/references, versions, hashes, signatures, exact fingerprints, evidence fields/freshness, documentation drift, reproducible records, deterministic evaluation, adapter guards/preconditions. Success establishes only the declared mechanical predicate, not semantic correctness, external truth or operational effectiveness.
- **Semantically assisted:** interpretation of rule coverage, semantic conflicts, test adequacy, predicate fidelity, translation, hidden/circular assumptions and evidence relevance. Static analysis, expertise, structured argument and AI help find gaps; they do not produce automatic truth. Record reviewer, authority, rationale, sources, uncertainty and objections. Agents cannot self-approve.
- **Operational effectiveness:** real resistance to bypass, gate disabling, wrong-candidate application, stale evidence, revoked keys, races, malicious scripts and outages. Evidence includes adversarial tests, bypass exercises, audits, incidents, independent red-team work, monitoring and integration-boundary verification. Effectiveness depends on context/time; neither a pure-function proof nor a unit test establishes it.

## 6. Operational modes

These describe usage, not proof methods or assurance levels.

- **inspect:** read-only examination; reports present, missing, stale, conflicting, unsupported or indeterminate information; changes nothing and accepts nothing.
- **audit:** structured, traceable assessment of a state/period; records claims, evidence, assumptions, authority, deviations, gaps and limitations. The report attests that an audit occurred, not that every claim is true, and does not automatically block.
- **enforce:** applies the predicate at the acceptance/integration boundary; blocks mandatory failure, conflict, indeterminacy, invalid/stale evidence, missing/unauthorized approval or mismatched tuple; requires authority capable of preventing application and rechecks the exact candidate immediately before apply.

A local executable can inspect, audit and evaluate locally. It cannot alone prevent a privileged local user from editing files or bypassing it. Strong shared enforcement belongs at a trusted integration boundary. Reporting a failure is not enforcing it.

## 7. Evidence statuses

Do not reduce results to a Boolean. Distinguish **Pass/supported**, **Fail/refuted**, **Unknown/inconclusive**, **Not run**, **Not applicable**, **Unsupported**, **Incomplete**, **Stale/invalidated**, and **Conflict**. Unknown, not-run and unsupported are not success. They block mandatory obligations unless an explicit, valid, governed exception applies. An exception does not turn unknown into proof.

Each claim has an ID, precise proposition, subject/target state, normative source, scope, admissible methods, evidence, assumptions/dependencies, limitations/defeaters, producer, independent verifier, status and time. Argument decomposes into subclaims; circular support is not independent corroboration.

## 8. Acceptance is a governance decision

The formal obligation is:

`Accepted(change, target_state) ⇒ GovernanceSatisfied(change, target_state)`

This is a safety requirement on acceptance, not a claim that a change is defect-free. The predicate covers exact repository/base/candidate, target state/scope, governance and specification revisions, all applicable mandatory requirements, admissible evidence bound to the exact subject and fresh dependencies, explicit outcomes (no fail/conflict/unknown/unsupported/not-run/incomplete treated as success), authorized approvals bound to exact change/candidate/governance, deviations with scope/authority/reason/expiry/compensating controls, evaluator/verifier versions and enforcement capability/limitations.

A result for one candidate cannot be reused for another candidate, rebase, Pijul channel state or governance/specification revision without revalidation. Acceptance is derived, never a contributor-supplied Boolean. It is not a test, theorem, signature, CI status, PR label, comment or reaction.

## 9. Tool roles considered

| Family | Role | Does not establish alone |
|---|---|---|
| Unit/integration/property/fuzz/security tests | Empirical behavior and counterexamples | Universal correctness |
| TLA+ / TLC | Transitions, concurrency, invariants, temporal properties in a configuration | Implementation conformance |
| Alloy | Relations and bounded counterexamples | Unbounded theorem |
| Lean / proof assistant | Theorems, proof-critical logic, formalized refinement | Normative fidelity or unverified executable |
| OPA / Cedar | Executable policy decisions | Normative correctness or non-bypassability |
| Signatures/attestations/transparency | Integrity, origin, history under assumptions | Truth, relevance or authority |

TLA+ was used for the first model because the initial target is a transition system. Lean was considered for proof-critical logic, not selected as a dependency. Alloy for relational constraints and bounded counterexamples. OPA/Cedar are policy engines, not theorem provers. None replaces the others; no global stack was selected.

## 10. Scope

This document expands the distinctions in specifications 0002–0005 and architecture 0008. It complements memory 0009; it does not change the proposed status of contracts or claim that an implementation exists.


## References

- [GovCheck governance and assurance reference register](../references/governance-and-assurance.md): GSN assurance arguments, Lamport/TLA+, in-toto provenance and Lean's proof-kernel boundary.
- [French reference register](../references/governance-and-assurance.fr.md).
