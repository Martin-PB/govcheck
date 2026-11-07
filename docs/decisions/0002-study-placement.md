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

The initial source artifact for this record is **“Évaluer l’intégration des dépôts.pdf”**, dated 6 November 2026, 224 pages. It is retained in the project Library and is not copied into this repository. Its external sources, repositories, pull requests, protocols, vocabularies and format references are indexed in [R-35–R-69 and R-77–R-87](../references.md) through the central catalogue.

The reviewed Cartocortex artifacts have different evidence status: PR #9 is a documentation panorama; PR #27 is an OKF storage/projection study explicitly marked as not executed; PR #28 is a backlog and transport study explicitly marked as not executed. None of these statuses establishes that a proposed adapter, CRDT, transport, cloud sync or format importer is implemented or accepted. See [R-62](../references.md#r-62) and [R-69](../references.md#r-69).

The approximate 10–20% share of sessions expected to require a TURN relay, repeated in the PR #28 study, was not tied to an independently verifiable measurement source in this audit. It is retained as an unvalidated planning assumption, not a general WebRTC statistic or a protocol guarantee; deployment telemetry would be needed to validate it.

## Bibliographic references

The integration study and its external technical sources are catalogued separately so the study is not mistaken for an implementation or adoption decision:

- [R-18 — Writ source-based assessment](../references.md#r-18)
- [R-19 — Privateer source-based assessment](../references.md#r-19)
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
