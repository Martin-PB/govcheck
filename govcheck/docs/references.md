# GovCheck package — external reference catalogue

This catalogue is shipped with the reusable GovCheck package. It contains only sources directly relevant to the generic assurance and VCS contracts; repository-specific research remains in the meta-level catalogue at the repository root.

Inclusion is descriptive, not adoption. A cited method or standard does not imply that GovCheck selects it, implements it, or has verified a project against it.

<a id="r-05"></a>
## R-05 — TLA+ and TLC
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md), [Specification 0006](specifications/0006-governance-revision-applicability.md), [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md), [formal models README](formal/README.md)

- **Primary sources:** [Lamport's TLA publications](https://www.microsoft.com/en-us/research/people/lamport/publications/) · [TLA+ project and documentation](https://lamport.azurewebsites.net/tla/tla.html) · [TLA paper DOI](https://doi.org/10.1145/177492.177726)
- **Use:** state-transition specifications, invariants, temporal properties and model checking.
- **Limit:** TLC results apply only to the recorded model, configuration, assumptions and explored bounds; they do not prove implementation refinement or normative fidelity.

<a id="r-06"></a>
## R-06 — in-toto software supply-chain integrity
- **Cited by:** no current package document cites this source.

- **Primary sources:** [in-toto project](https://in-toto.io/) · [USENIX Security 2019 paper](https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf)
- **Use:** provenance of process steps, materials and products.
- **Limit:** provenance does not establish that a recorded step was semantically correct or authorized.

<a id="r-07"></a>
## R-07 — SLSA
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary source:** [SLSA specification](https://slsa.dev/spec/)
- **Use:** build provenance and software supply-chain integrity.
- **Limit:** SLSA does not define GovCheck's governance authority, exception lifecycle or complete assurance case.

<a id="r-20"></a>
## R-20 — Lean
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary source:** [Lean language reference](https://lean-lang.org/doc/reference/latest/)
- **Use:** theorem proving and proof-term checking under explicit definitions, axioms and hypotheses.
- **Limit:** a theorem does not establish that its predicate captures approved policy or that an executable refines it.

<a id="r-22"></a>
## R-22 — Native Git and Pijul semantics
- **Cited by:** [formal models README](formal/README.md), [Specification 0006](specifications/0006-governance-revision-applicability.md), [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md)

- **Primary sources:** [Git documentation](https://git-scm.com/docs) · [Pijul theory](https://pijul.org/manual/theory) · [Pijul channels](https://pijul.org/manual/workflows/channels) · [Pijul conflicts](https://pijul.org/manual/conflicts.html)
- **Use:** preserve snapshot/commit semantics for Git and change/patch-graph, channel and conflict semantics for Pijul.
- **Limit:** documentation does not establish that a GovCheck adapter is implemented; adapters still require native contracts and conformance tests.

<a id="r-35"></a>
## R-35 — Common Criteria / ISO/IEC 15408
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary sources:** [Common Criteria Portal](https://www.commoncriteriaportal.org/) · [CC:2022 and CEM:2022 publications](https://www.commoncriteriaportal.org/cc/index.cfm)
- **Use:** context for security evaluation and Evaluation Assurance Levels.
- **Limit:** EALs are evaluation packages, not generic software maturity grades or GovCheck assurance tiers.

<a id="r-36"></a>
## R-36 — RTCA DO-178C / EUROCAE ED-12C
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary sources:** [FAA AC 20-115D](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D) · [RTCA overview](https://www.rtca.org/do-178/)
- **Use:** aviation-specific software life-cycle objectives, verification and certification evidence.
- **Limit:** this is a sector-specific assurance standard in an airworthiness certification context, not a general software regulation.

<a id="r-37"></a>
## R-37 — Alloy
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary sources:** [Alloy project and documentation](https://alloytools.org/) · [Analyzer source](https://github.com/AlloyTools/org.alloytools.alloy)
- **Use:** relational modeling, bounded analysis and counterexample search.
- **Limit:** results depend on scopes and assumptions; they do not establish implementation conformance.

<a id="r-38"></a>
## R-38 — SPIN / Promela
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary source:** [SPIN manual](https://spinroot.com/spin/Man/Manual.html)
- **Use:** modeling and verification of concurrent/distributed systems and temporal properties.
- **Limit:** results apply to the Promela abstraction and search configuration.

<a id="r-39"></a>
## R-39 — Kani
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary source:** [Kani documentation](https://model-checking.github.io/kani/)
- **Use:** bounded model checking of Rust programs and proof harnesses.
- **Limit:** supported Rust features and concurrency coverage are bounded; results depend on harnesses, bounds and toolchain.

<a id="r-40"></a>
## R-40 — Verus
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary source:** [Verus tutorial and reference](https://verus-lang.github.io/verus/guide/)
- **Use:** static functional-correctness verification for Rust.
- **Limit:** not all Rust features/libraries are supported; the verifier and compiler toolchain remain part of the trust base.

<a id="r-41"></a>
## R-41 — Dafny
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary source:** [Dafny Reference Manual](https://dafny.org/dafny/DafnyRef/DafnyRef)
- **Use:** specifications, pre/postconditions, invariants and static program verification.
- **Limit:** verified claims are relative to the Dafny specification and trusted verifier/backend.

<a id="r-42"></a>
## R-42 — Coq / Rocq
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary sources:** [Rocq documentation](https://rocq-prover.org/docs) · [versioned Coq documentation](https://docs.rocq-prover.org/)
- **Use:** machine-checked theorem proving in dependent type theory.
- **Limit:** results depend on definitions, axioms, imported results and kernel/toolchain assumptions.

<a id="r-43"></a>
## R-43 — Isabelle
- **Cited by:** [Specification 0005](specifications/0005-assurance-model.md)

- **Primary source:** [Isabelle documentation](https://www.isabelle.in.tum.de/documentation.html)
- **Use:** interactive theorem proving and formal specification.
- **Limit:** results depend on the selected logic, theory imports, axioms and prover environment.


## Journal canonique, concurrence et reprise

<a id="r-142"></a>
### R-142 — Linearizability: A Correctness Condition for Concurrent Objects
- **Cited by:** [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md)
- **Primary source:** Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM Transactions on Programming Languages and Systems*, 12(3), 1990, pp. 463–492. [DOI](https://doi.org/10.1145/78969.78972) · [Author-hosted paper](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf)
- **Relevant concepts:** concurrent operations appear to take effect at one point between invocation and response while respecting a legal sequential specification.
- **Use in GovCheck:** provides the formal concurrency concept behind the journal's single linearization point for compare-and-append.
- **Limit:** linearizability is a correctness condition, not a storage implementation or a proof that a particular journal satisfies it.

<a id="r-143"></a>
### R-143 — ARIES write-ahead logging and transaction recovery
- **Cited by:** [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md)
- **Primary source:** C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM Transactions on Database Systems*, 17(1), 1992. [IBM Research publication](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging)
- **Relevant concepts:** write-ahead logging, durable transaction recovery, redo/undo and restart recovery.
- **Use in GovCheck:** informs the distinction between volatile preparation, durable commit and reconstruction after interruption.
- **Limit:** ARIES is a database recovery algorithm; citing it does not select a database, imply direct adoption, or prove the GovCheck journal's durability.

<a id="r-144"></a>
### R-144 — RFC 9110, HTTP Semantics: idempotent methods
- **Cited by:** [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md)
- **Primary source:** [RFC 9110 §9.2.2 — Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
- **Relevant concepts:** repeatable requests have the same intended effect as one request, enabling safe retry after a lost response when the operation semantics are idempotent.
- **Use in GovCheck:** informs the protocol distinction between retrying an exact append request and accidentally creating a second normative event.
- **Limit:** HTTP method semantics do not define GovCheck's idempotency-key namespace, journal retention or append protocol; those remain specified locally.
