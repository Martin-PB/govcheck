# External references

**Status:** consolidated source register for GovCheck's design decisions. English is the default language; the French counterpart is [references (français)](references.fr.md).

This page lists the academic and industry sources used to support the decisions recorded in [ADR 0001](../decisions/0001-bootstrap-boundaries.md), [ADR 0002](../decisions/0002-study-placement.md), [ADR 0003](../decisions/0003-two-level-governance.md), specifications 0002-0005 and architecture records 0006-0021. Each entry names the decision area it supports. A listed source informs a decision; it does not make a proposal implemented or approved.

## Assurance vocabulary and method classes (spec 0005, records 0009, 0010, 0021)

- [SLSA specification](https://slsa.dev/spec/v1) — supply-chain "levels" vocabulary; supports reserving "levels" for the empirical sub-scale in spec 0005.
- [Common Criteria Portal (ISO/IEC 15408, CC:2022)](https://www.commoncriteriaportal.org/cc/index.cfm) — Evaluation Assurance Levels (EAL); cited in spec 0005 as a distinct "levels" axis.
- [RTCA DO-178C](https://www.rtca.org/do-178/) — Design Assurance Levels (DAL) for airborne software; cited in spec 0005 as a third, distinct "levels" axis.
- [in-toto](https://in-toto.io/) — CNCF supply-chain metadata standard; candidate for evidence-integrity statements in record 0007.

## Formal methods (ADR 0001, spec 0005, records 0007, 0008, 0009, 0010)

- [TLA+ home page (Leslie Lamport)](https://lamport.org/tla/tla.html) — specification language and TLC model checker; basis of the `govcheck.lifecycle` and `govcheck.assurance` models (decision D-11).
- [Alloy / Alloy Analyzer](https://alloytools.org/) — bounded relational model checking (Daniel Jackson); candidate in records 0007/0010.
- [SPIN model checker](https://spinroot.com/spin/Doc/Book_extras/index.html) — PROMELA model checking (Gerard Holzmann); named in spec 0005.
- [Lean theorem prover](https://www.microsoft.com/en-us/research/project/lean/) — proof assistant; candidate for proof-critical logic (ADR 0001, record 0010).
- [Coq proof assistant](https://coq.inria.fr/) — named in spec 0005 and record 0007.
- [Isabelle](https://isabelle.in.tum.de/) — generic proof assistant; named in spec 0005 and record 0007.
- [Kani Rust Verifier](https://model-checking.github.io/kani/) — program verification for Rust; named in spec 0005.
- [Verus](https://verus-lang.github.io/verus/guide/) — verified Rust; named in spec 0005.
- [Dafny](https://www.microsoft.com/en-us/research/project/dafny-a-language-and-program-verifier-for-functional-correctness/overview/) — verification-aware language; named in spec 0005.

## Policy engines (record 0010)

- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) — executable policy decisions; assessed as not a theorem prover.
- [Cedar](https://cedarpolicy.com/) — AWS policy language for permissions; assessed likewise.

## Versioning, identity and provenance (record 0017)

- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) — compatibility vocabulary for declared public contracts.
- [1EdTech Versioning Framework 1.0](https://www.imsglobal.org/spec/versioning/v1) — separate versioning for specifications and artifacts.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) — provenance ontology (entities, activities, agents).
- [DataCite Versioning](https://support.datacite.org/docs/versioning) — version vs concept-level identifiers.
- [Scientific Data (2024), dataset versioning framework](https://www.nature.com/articles/s41597-024-03153-y) — domain-specific dataset revision treatment.

## Requirements engineering (record 0013)

- van Lamsde, A. (2009), *Requirements Engineering: From System Goals to UML Models to Software Specifications*, Wiley, ISBN 978-0-470-01270-3 ([publisher page](https://www.wiley.com/en-ie/Requirements+Engineering%3A+From+System+Goals+to+UML+Models+to+Software+Specifications%2C+1st+Edition-p-9780470012703)) — KAOS/GORE-style goal refinement referenced by the governance metamodel.

## Version control (ADR 0001, spec 0004, record 0009)

- [Git](https://git-scm.com/) — first-class VCS adapter target; dirty worktree/index identity in spec 0004.
- [Pijul](https://pijul.org/index.html) — patch-theory-based distributed VCS; first-class, semantically distinct adapter target (decision D-05).

## External projects assessed as fixtures (record 0016; per ADR 0002 these are studies, not dependencies)

- [infinri/Writ](https://github.com/infinri/Writ) — Claude Code workflow-governance runtime; assessed at commit `ebdafe5450b201339f81e717ed104e6bcfd3fe3e`.
- [privateer-agent/privateer-agent](https://github.com/privateer-agent/privateer-agent) — Pi coding-agent distribution; assessed at commit `181a988e443fa6b6b4138fc349d1260c96408ad4`.

## Integration study sources (ADR 0002; study of Cartocortex/MoriNet/SaussuNet)

- [Cartocortex](https://github.com/complexus-lab/cartocortex), [MoriNet](https://github.com/lejeunecedric/MoriNet), [SaussuNet](https://github.com/lejeunecedric/SaussuNet) — the three repositories of the integration study that motivated ADR 0002.
- [CRDTs overview (crdt.tech)](https://crdt.tech/) — conflict-free replicated data types considered for real-time co-editing.
- [RFC 5766 (TURN)](https://datatracker.ietf.org/doc/html/rfc5766.html) and STUN (RFC 5389), [WebRTC](https://webrtc.org/) — transport options studied for real-time collaboration.

## Reading rules

- Sources are cited with their canonical public URL; repository assessments also record the exact commit reviewed.
- A source supports reasoning; it never replaces an authorized GovCheck decision, and it is not evidence that any control is implemented.
- New sources backing a new decision are added here in the same change as the decision record.
