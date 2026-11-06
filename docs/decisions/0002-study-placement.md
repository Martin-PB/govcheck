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
