# Specification 0005 — Assurance, Claims and Evidence

**Status:** Proposed architecture, ready for review. **French:** [0005](0005-assurance-model.fr.md).

## Purpose and vocabulary

Report exactly what is established, by which method, for which subject/state and under which assumptions. Never collapse test execution, model checking, theorem proving, implementation conformance, normative fidelity and acceptance into a generic “verified”.

Each record distinguishes claim (falsifiable scoped proposition), argument, evidence (method/tool result), assumption, context, limitation/defeater and authorized decision. A claim about a model is not a claim about implementation without a separate conformance argument.

## Non-interchangeable method classes

1. **Empirical execution:** tests, linters, builds, scans; establishes observed outcomes for executed scope/environment.
2. **Model checking:** explores a formal model under declared bounds/assumptions; says nothing automatically about implementation.
3. **Theorem proving:** checker validates derivation in a specified logic/kernel; record axioms, imports, assumptions and escape hatches.
4. **Implementation conformance:** requires explicit refinement/conformance relation and method between implementation and specification.
5. **Normative fidelity:** establishes traceability from approved normative rules to formal rule IDs and faithful human-readable projections.
6. **Acceptance:** governance decision that required claims/evidence/approvals satisfy the predicate for an exact candidate; not proof that all claims are true.

## Evidence record

Bind stable evidence/claim IDs; subject kind and native immutable identity; repository and exact base/candidate fingerprints; governance package revision/semantics; specification/model revision; method and scope; tool/version/configuration/invocation; environment, assumptions, bounds and external inputs; raw result or integrity-protected reference; outcome/time/producer/provenance; limitations and invalidation dependencies. A bare exit code proves only the outcome of that invocation.

Claims declare acceptable methods, scope, freshness and corroboration. Evidence can support, refute or leave a claim inconclusive. Contradictory evidence remains visible. Assurance arguments decompose top-level claims into subclaims, assumptions and evidence; circular reasoning must not be presented as proof.

## Formal methods and trusted base

For theorem proving, record logic, kernel/checker version, axioms, imported theorems, admitted obligations, unsafe features, oracles and reproducibility. If Lean is selected, account explicitly for sorry, unreviewed axioms, unsafe, native oracles and dependency trust.

For model checking, record model revision, configuration/constants, reductions, fairness, state/transition counts, bounds and completion status. Bounded/partial exploration is never called exhaustive.

For conformance, record implementation/spec revisions, refinement relation, abstraction boundary and method. For normative fidelity, record approvers and source-to-rule-to-projection traceability.

## Provenance, trust and freshness

Hashes/signatures may establish integrity/origin under key assumptions, not semantic correctness, authorization or truth of external data. External facts need source, retrieval time, validity and trust classification. Disclose the trusted computing base: evaluator, parser/canonicalizer, VCS adapters, evidence verifiers, crypto libraries, runtime and remote authorities.

Evidence declares dependencies. Changes, tool/key compromise, source correction or discovered defects may invalidate it. Preserve historical records; exclude invalid evidence from current decisions unless revalidated.

## Reporting and conformance targets

Report claims, status, evidence, assumptions, limitations, state binding, provenance, unresolved defeaters and exact acceptance decision. Distinguish not-run, not-applicable, unsupported, incomplete, failed and passed; avoid unexplained aggregate scores.

A conforming implementation binds evidence to exact states/governance revisions, exposes assumptions/TCB, preserves contradictions and invalidations, distinguishes bounded from exhaustive exploration, accounts for proof axioms/kernel, and requires conformance evidence before implementation-level claims. No engine or proof infrastructure exists yet.
