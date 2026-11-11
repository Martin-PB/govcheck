# GovCheck

**Formal, repository-centred governance for software projects.**

GovCheck aims to make repository development rules explicit, machine-checkable, traceable, and enforceable at change acceptance—independent of coding agent, version-control system, hosting provider, forge, or remote service.

> **Current status:** architecture specifications are ready for maintainer review. GovCheck is not yet an implemented or formally verified system. Do not interpret design intentions as operational guarantees.

## Project principles

- The repository and its change lifecycle are governed; humans and agents are contributors.
- A versioned canonical governance model is the sole normative authority; Markdown is a controlled projection or explanation.
- Formal governance and assurance foundations apply to every repository size.
- A small local executable is the primary interface; no hosted service or mandatory daemon is required. An optional MCP adapter may be assessed later as one adapter among others; it is not part of the core.
- Git and Pijul are first-class and semantically distinct.
- Local-only, team-hosted, self-hosted, and public workflows are in scope.
- VCS, hosting, collaboration, and acceptance are separate concerns.
- Local checks are useful, but shared enforcement belongs at an independently verifiable integration boundary.
- Prefer a small core, declarative profiles, narrow adapters, and reuse of existing project tools.
- Bootstrap and migration follow inspect → plan → apply and must be non-destructive.

## Languages

English is the default. French documentation is maintained alongside it: [README.fr.md](README.fr.md).

## Architecture specifications

The first architecture-design pass is documented in [docs/specifications](docs/specifications/README.md):
1. Canonical Governance Model.
2. Change Lifecycle and Acceptance.
3. VCS and Collaboration Adapter Contracts.
4. Assurance, Claims and Evidence.

Each specification has an English and French version. They define proposed contracts, not implemented behavior.

The design rationale, assurance distinctions, lifecycle-model audit, canonical documentation authority, governance metamodel, development workflow and ecosystem assessments are indexed in [docs/architecture](docs/architecture/README.md).

## Governed work portfolio

The repository-backed [Governed Work Portfolio](docs/work-portfolio/README.md) is the canonical home for work-item identity, lifecycle and traceability. GitHub Issues/Projects remain coordination adapters during migration; see [Architecture 0028](docs/architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.md) and [Architecture 0030](docs/architecture/0030-repository-backed-work-portfolio-and-recoverable-history.md).

## Research library

The durable [Research Register](docs/research/README.md) indexes non-normative studies that may inform future decisions. Each study has a stable ID, source analysis, applicability assessment, limitations, cross-references and decision-traceability guidance. Research records are not implementation tasks or adopted requirements.

## Decisions and next phase

[ADR 0001](docs/decisions/0001-bootstrap-boundaries.md) records the accepted bootstrap boundaries. Remaining decisions include implementation language, canonical serialization/schema, expression language, formal kernel, cryptographic approach, and dependency strategy. These should be resolved through explicit comparative analysis before implementation.

## License

GovCheck is licensed under the [Apache License, Version 2.0](LICENSE). Copyright 2026 Martin Pruvost-Beaurain.

Any redistribution of GovCheck or of a derivative work must include the [LICENSE](LICENSE) and the attribution in the [NOTICE](NOTICE) file. See [ADR 0005](docs/decisions/0005-license-apache-2-0-with-individual-attribution.md) for the decision and its limits.
