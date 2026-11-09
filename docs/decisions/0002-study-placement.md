# ADR 0002: Placement of studies and comparative assessments

- **Status:** Accepted for the bootstrap; changes require a superseding ADR.
- **Date:** 2026-11-06
- **Scope:** where studies, assessments and comparative analyses of external tools/methods live in a governed repository.

## Context

GovCheck's own design was driven by studies (integration assessment of Cartocortex/MoriNet/SaussuNet, assessment of Writ and Privateer in architecture record 0016). A governed repository must say where such studies live so they are neither lost nor mistaken for normative rules or implemented behavior.

## Decision

Studies, assessments and comparative analyses are **architecture records** placed in docs/architecture/ as sequentially numbered bilingual records (English default, French counterpart), with an explicit status line (study / proposal / assessment) and scope/limits. They are never presented as implemented controls, verified properties, or normative rules. Verification reports, counterexamples and generated evidence are release artifacts attached to releases, not source files with release-specific names. GovCheck applies this rule to itself: record 0016 is an assessment, not a control.

## Consequences

- New studies get the next free number in docs/architecture/.
- The architecture README indexes them with their status.
- Normative content stays in docs/specifications/ and docs/decisions/.

French: [ADR 0002 (français)](0002-study-placement.fr.md).

## Source artifact and evidence boundary

The initial source artifact for this record is **“Évaluer l’intégration des dépôts.pdf”**, dated 6 November 2026, 224 pages. It is retained in the project Library and is not copied into this repository. Its external sources, repositories, pull requests, protocols, vocabularies and format references are preserved in the central catalogue; the directly relevant sources are linked individually below.

The reviewed Cartocortex artifacts have different evidence status: PR #9 is a documentation panorama; PR #27 is an OKF storage/projection study explicitly marked as not executed; PR #28 is a backlog and transport study explicitly marked as not executed. None of these statuses establishes that a proposed adapter, CRDT, transport, cloud sync or format importer is implemented or accepted. See [R-62](../references.md#r-62) and [R-69](../references.md#r-69).

The approximate 10–20% share of sessions expected to require a TURN relay, repeated in the PR #28 study, was not tied to an independently verifiable measurement source in this audit. It is retained as an unvalidated planning assumption, not a general WebRTC statistic or a protocol guarantee; deployment telemetry would be needed to validate it.

The study also names B, Z, CSP, iStar and deontic logic as candidate formalisms, and NIST SP 800-192 as a source for access-control policy/model verification. They are catalogued as distinct alternatives and methods; none is selected or adopted by implication.

## Bibliographic references

The integration study and its external technical sources are catalogued separately so the study is not mistaken for an implementation or adoption decision:

- [R-03 — GitHub protected-branch controls](../references.md#r-03)
- [R-05 — TLA+ specification and TLC model checking](../references.md#r-05)
- [R-06 — in-toto provenance framework](../references.md#r-06)
- [R-07 — SLSA software supply-chain framework](../references.md#r-07)
- [R-08 — OpenSSF Scorecard](../references.md#r-08) · [R-111 — OpenSSF Best Practices Badge](../references.md#r-111)
- [R-09 — Open Policy Agent and Rego](../references.md#r-09)
- [R-10 — Cedar authorization language and verification-guided development](../references.md#r-10)
- [R-18 — Writ source-based assessment](../references.md#r-18)
- [R-19 — Privateer source-based assessment](../references.md#r-19)
- [R-20 — Lean proof assistant](../references.md#r-20)
- [R-21 — Research-software versioning and reproducibility guidance](../references.md#r-21)
- [R-22 — Native Git/Pijul semantics and Nest hosting](../references.md#r-22)
- [R-35 — Common Criteria / ISO/IEC 15408 and EAL evaluation](../references.md#r-35)
- [R-36 — RTCA DO-178C / EUROCAE ED-12C and DAL levels](../references.md#r-36)
- [R-37 — Alloy relational modeling and analysis](../references.md#r-37)
- [R-38 — SPIN / Promela model checking](../references.md#r-38)
- [R-39 — Kani Rust program verification](../references.md#r-39)
- [R-40 — Verus Rust verification](../references.md#r-40)
- [R-41 — Dafny language and verifier](../references.md#r-41)
- [R-42 — Coq / Rocq proof assistant](../references.md#r-42)
- [R-43 — Isabelle theorem prover](../references.md#r-43)
- [R-44 — KAOS and goal-oriented requirements engineering](../references.md#r-44)
- [R-45 — CRDT foundations](../references.md#r-45)
- [R-46 — Yjs and Yrs](../references.md#r-46)
- [R-47 — Automerge](../references.md#r-47)
- [R-48 — Loro CRDT](../references.md#r-48)
- [R-49 — WebRTC transports](../references.md#r-49)
- [R-50 — ICE, STUN and TURN](../references.md#r-50)
- [R-51 — Open Knowledge Format (OKF) v0.2](../references.md#r-51)
- [R-52 — RDF 1.1](../references.md#r-52)
- [R-53 — SKOS](../references.md#r-53)
- [R-54 — OWL 2](../references.md#r-54)
- [R-55 — SHACL](../references.md#r-55)
- [R-56 — Dublin Core Metadata Terms](../references.md#r-56)
- [R-57 — Bibliographic Ontology (BIBO)](../references.md#r-57)
- [R-58 — DCAT 3](../references.md#r-58)
- [R-59 — W3C Web Annotation](../references.md#r-59)
- [R-60 — ActivityStreams 2.0](../references.md#r-60)
- [R-61 — P-Plan ontology](../references.md#r-61)
- [R-62 — Cartocortex, MoriNet and SaussuNet repositories and PRs #27/#28](../references.md#r-62)
- [R-63 — Mind-map and graph interchange formats](../references.md#r-63)
- [R-64 — Cloud storage APIs and S3 interoperability](../references.md#r-64)
- [R-65 — Browser file access, local persistence and WebAssembly](../references.md#r-65)
- [R-66 — Hyperswarm and HyperDHT peer discovery](../references.md#r-66)
- [R-67 — WebDAV, Model Context Protocol and Markdown wiki conventions](../references.md#r-67)
- [R-68 — Related GovCheck ecosystem repositories](../references.md#r-68)
- [R-69 — Cartocortex mind-map format and tool interoperability source inventory](../references.md#r-69)
- [R-77 — Policy-as-code and MCP tool governance](../references.md#r-77)
- [R-78 — NIST OSCAL and Continuous Compliance Framework](../references.md#r-78)
- [R-79 — Agent sandboxing and runtime isolation](../references.md#r-79)
- [R-80 — Matrix protocol and Element X client](../references.md#r-80)
- [R-81 — SearXNG metasearch](../references.md#r-81)
- [R-82 — Microsoft MarkItDown document conversion](../references.md#r-82)
- [R-83 — JSON-LD 1.1 linked-data serialization](../references.md#r-83)
- [R-84 — RDF 1.1 Turtle syntax](../references.md#r-84)
- [R-85 — SIOC online-community ontology](../references.md#r-85)
- [R-86 — Schema.org DigitalDocument vocabulary](../references.md#r-86)
- [R-87 — WebTorrent browser peer-to-peer transport and discovery](../references.md#r-87)
- [R-88 — NIST SP 800-192 verification and testing of access-control policies/models](../references.md#r-88)
- [R-89 — B Method and Atelier B](../references.md#r-89)
- [R-90 — Z formal specification notation](../references.md#r-90)
- [R-91 — Communicating Sequential Processes and FDR](../references.md#r-91)
- [R-92 — iStar 2.0 goal-oriented requirements modeling](../references.md#r-92)
- [R-93 — deontic logic and normative modalities](../references.md#r-93)
- [R-104 — Agent instruction formats and spec-driven workflows](../references.md#r-104)
- [R-105 — Policy-as-code, continuous assurance and agent-governance research](../references.md#r-105)
- [R-106 — OWASP guidance for AI-agent and MCP security](../references.md#r-106)
- [R-106 — OWASP guidance for AI-agent and MCP security](../references.md#r-106)
- [R-108 — GUAC software-supply-chain knowledge graph](../references.md#r-108)
- [R-109 — OpenSSF Security Insights Specification](../references.md#r-109)
- [R-110 — OpenSSF OSPS Baseline](../references.md#r-110)
- [R-111 — OpenSSF Best Practices Badge](../references.md#r-111)
- [R-112 — gittuf forge-independent Git policy](../references.md#r-112)
- [R-113 — SLSA Source Track](../references.md#r-113)
- [R-114 — Gemara GRC Engineering Model](../references.md#r-114)
- [R-115 — Gerrit submit requirements](../references.md#r-115)
- [R-116 — OpenSSF Minder](../references.md#r-116)
- [R-117 — OpenSSF Allstar](../references.md#r-117)
- [R-118 — Conftest policy testing](../references.md#r-118)
- [R-119 — CUE configuration and constraint language](../references.md#r-119)
- [R-120 — OpenSSF Privateer security/compliance evaluator](../references.md#r-120)
- [R-121 — SLSA Verification Summary Attestation](../references.md#r-121)
- [R-122 — Sigstore artifact signing and transparency](../references.md#r-122)
- [R-123 — Symboleo formal contract specification](../references.md#r-123)
- [R-124 — Catala legislative literate programming](../references.md#r-124)
- [R-125 — Event Calculus](../references.md#r-125)
- [R-126 — Runtime verification and trace monitoring](../references.md#r-126)
- [R-127 — GitHub CODEOWNERS and code-owner review](../references.md#r-127)
