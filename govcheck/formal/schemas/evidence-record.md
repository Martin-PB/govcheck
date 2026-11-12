# Evidence record schema

**Status:** proposed Draft 2020-12 record contract, pending adoption of Specifications 0003/0005 and the canonical governance model. It is not yet a production acceptance gate.

## Purpose

`evidence-record.schema.json` gives a stable machine-readable shape to the evidence obligations in Specification 0005. It records one observation, execution or derivation and binds it to exact subjects, claims, governance semantics, method, execution context, result, provenance and declared invalidation dependencies.

It deliberately keeps these concepts separate:

- **Evidence record:** what was observed or derived, by which method, on which exact subject and under which context.
- **Claim:** the scoped proposition that the evidence may support, refute or leave inconclusive.
- **Argument:** the reasoning that connects claims, assumptions and evidence.
- **Acceptance decision:** an authorized lifecycle decision over an exact candidate; not implied by a passing evidence record.

## Required bindings

- Stable `evidenceId` and one or more stable `claimIds`.
- Subject kind, stable `artifactId`, exact native revision and optional repository/base/candidate bindings.
- Governance package revision and evaluator-semantics version.
- Optional exact specification/model revision.
- Method class, scope, assumptions, limitations and bounds; empirical execution additionally records its sublevel (unit, integration, property or static analysis).
- For executed methods: tool name/version, invocation, environment, configuration digest and external inputs with retrieval times.
- Result state and either an inline raw result or a URI plus SHA-256 digest. Non-execution states (`not-run`, `not-applicable`, `unsupported`) do not fabricate execution payloads.
- Producer, record time, source references, integrity metadata and explicit invalidation dependencies.

## Status semantics

The result vocabulary preserves the distinctions required by Specification 0005:

| Status | Meaning |
|---|---|
| `not-run` | No method execution or derivation was performed |
| `not-applicable` | The method does not apply to this claim/subject |
| `unsupported` | The evaluator cannot handle the method or required construct |
| `incomplete` | The activity began but did not reach its declared completion criterion |
| `failed` | The method completed and reported a negative result |
| `passed` | The method completed and reported its scoped positive result |
| `unknown` | No reliable result is available, or the evaluator cannot determine the result from the available inputs |
| `inconclusive` | The method completed, but its result does not establish pass or fail |

Synthetic illustrations are provided in [evidence-record-passed.example.json](../fixtures/evidence-record-passed.example.json), [evidence-record-not-run.example.json](../fixtures/evidence-record-not-run.example.json) and [evidence-record-unknown.example.json](../fixtures/evidence-record-unknown.example.json). They are examples only, not repository evidence.

`unknown` and `inconclusive` are distinct: the former means no determinate result is available; the latter means a method ran but did not settle the claim. `stale` is not a result status: freshness/applicability is derived separately from exact dependency revisions and validity conditions.

A `passed` record is testimony from the declared method, not a universal proof. Its meaning remains bounded by method class, scope, assumptions, tool, configuration, environment and trust base.

## Validation boundary

JSON Schema checks shape and syntax only. It does not:

- resolve whether claim IDs exist or whether the claims are authorized;
- prove the subject revision exists or that its digest matches the VCS object;
- authenticate the producer, tool, authority or signatures;
- verify the raw result or reproduce the invocation;
- infer evidence freshness from timestamps;
- compute transitive invalidation across dependency edges;
- prove semantic compatibility or normative fidelity;
- authorize acceptance.

A future evaluator must join evidence records to claim/argument records, the canonical authority model, exact revision inventory and dependency graph. Missing or unresolved dependencies must not be treated as current. Historical evidence remains immutable; revalidation creates a new evidence event rather than overwriting the old one.

## Local structural check

The repository has no selected JSON Schema runtime dependency. This PR adds the schema and documentation only; it does not silently add a dependency or claim validator execution. Once a Draft 2020-12 implementation is selected, add pinned positive and negative conformance fixtures and test the external references as a registered schema set.
