# Architecture 0007 — Technology Decision Framework

**Status:** Decision framework, not technology selections. **French:** [0007 (fr)](0007-technology-decision-framework.fr.md).

This document defines how to choose technology without prematurely selecting a stack. Every candidate must be evaluated against the same use cases, threat model and conformance suite. Scores alone cannot decide: hard constraints are gates, and evidence/unknowns must accompany any score.

## 1. Decision gates

Reject or defer a candidate if it:
- cannot preserve Git and Pijul semantics behind distinct adapters;
- requires a hosted service, resident daemon, mandatory MCP server or privileged control plane;
- makes local-only operation second-class;
- cannot provide deterministic, bounded evaluation and explicit indeterminate/error states;
- requires arbitrary repository policy code execution;
- prevents reproducible builds/distribution on supported platforms;
- introduces unacceptable mandatory dependencies or licensing constraints;
- conflates tests, model checking, proofs, conformance and acceptance.

## 2. Candidate dimensions

| Decision | Candidate families to compare (illustrative, not exhaustive) | Evaluation criteria |
|---|---|---|
| Implementation language | Rust, Go, OCaml, Haskell, Kotlin/JVM, Python | Static guarantees, portability, binary size, startup, ecosystem, contributors, FFI, supply-chain, long-term maintenance |
| Canonical serialization | JSON + JSON Schema, YAML subset, TOML, CBOR, custom canonical encoding | Determinism, duplicate-key policy, canonical bytes, schema evolution, comments/human authoring, tooling, signature compatibility |
| Rule semantics | Fixed typed predicates, restricted expression DSL, logic/rule engine | Decidability/bounds, explainability, compositionality, safe evaluation, formalization, extensibility |
| Formal analysis | TLA+, Alloy, PlusCal, Lean, Coq, Isabelle, executable state machines | Which claims each method can establish, TCB, automation, contributor skills, reproducibility |
| Evidence integrity | Content hashes, signed attestations, transparency logs, in-toto/SLSA-compatible statements | State binding, identity, revocation, offline use, privacy, interoperability, operational burden |
| Local interface | Single binary, platform packages, source distribution | Installation, reproducibility, offline operation, update trust, platform coverage |
| Forge integration | GitHub/GitLab/Forgejo/Gitea/Bitbucket adapters; generic status/check protocols | Required gate capability, exact state binding, bypass visibility, API stability, self-hosting |
| Pijul integration | Native CLI/library and Nest/team server adapters | Native patch/channel/graph/conflict fidelity, offline use, maturity and maintenance |
| Test orchestration | Existing project commands, standardized evidence protocol | Least privilege, reproducibility, timeouts, output handling, no mandatory project toolchain |

## 3. Weighted evaluation after hard gates

For candidates that pass gates, score 0–5 with written evidence and confidence for: semantic fit (20%), formal analyzability (15%), security/TCB (15%), maintainability (15%), portability/offline use (10%), ecosystem/interoperability (10%), operational cost (10%), migration/reversibility (5%). Weights are provisional and must be reviewed before scoring. A missing fact is “unknown”, not zero or an assumed pass. Publish raw evidence and sensitivity analysis; do not optimize a composite score blindly.

## 4. Required decision record

Each ADR states: question and why now; constraints/gates; alternatives including “defer/no new dependency”; sources and versions/dates; prototype/test evidence; security and TCB impact; Git/Pijul/local-only implications; migration/reversal cost; decision and rejected alternatives; confidence; revisit triggers; bilingual summary.

## 5. Suggested order

1. Specify canonical semantic invariants and threat assumptions (done as proposals, review required).
2. Prototype serialization/canonicalization and parser differential tests.
3. Compare fixed typed rule model against restricted expression languages.
4. Model lifecycle and concurrency in TLA+/Alloy or another suitable method; prove selected kernel properties only after boundaries are clear.
5. Compare implementation languages with a small evaluator/parser prototype.
6. Define evidence statement interoperability and key lifecycle.
7. Prototype Git and Pijul state descriptors independently.
8. Only then select packaging and forge adapters.

No language, serialization, formal kernel, signature format, license or dependency has been selected by this framework.
