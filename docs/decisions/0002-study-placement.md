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

## Bibliographic references

The integration study and its external technical sources are catalogued separately so the study is not mistaken for an implementation or adoption decision:

- [R-18 — Writ source-based assessment](../references.md#r-18)
- [R-19 — Privateer source-based assessment](../references.md#r-19)
- [R-37 — CRDT foundations](../references.md#r-37)
- [R-38 — Yjs and Yrs](../references.md#r-38)
- [R-39 — Automerge](../references.md#r-39)
- [R-40 — Loro CRDT](../references.md#r-40)
- [R-41 — WebRTC transports](../references.md#r-41)
- [R-42 — ICE, STUN and TURN](../references.md#r-42)
- [R-43 — Open Knowledge Format (OKF) v0.2](../references.md#r-43)
- [R-44 — RDF 1.1](../references.md#r-44)
- [R-45 — SKOS](../references.md#r-45)
- [R-46 — OWL 2](../references.md#r-46)
- [R-47 — SHACL](../references.md#r-47)
- [R-48 — Dublin Core Metadata Terms](../references.md#r-48)
- [R-49 — Bibliographic Ontology (BIBO)](../references.md#r-49)
- [R-50 — DCAT 3](../references.md#r-50)
- [R-51 — W3C Web Annotation](../references.md#r-51)
- [R-52 — ActivityStreams 2.0](../references.md#r-52)
- [R-53 — P-Plan ontology](../references.md#r-53)
- [R-54 — Cartocortex, MoriNet and SaussuNet repositories and PRs #27/#28](../references.md#r-54)
- [R-55 — Mind-map and graph interchange formats](../references.md#r-55)
