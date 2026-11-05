# GovCheck

**Formal, repository-centred governance for software projects.**

GovCheck is being bootstrapped in the open. Its purpose is to make a repository's development rules explicit, machine-checkable, traceable, and enforceable at the point where changes are accepted—without making the governance depend on a particular coding agent, version-control system, hosting provider, or remote service.

> **Bootstrap status:** GovCheck is not yet an implemented or formally verified system. This repository currently records the project's intended boundaries and bootstrap decisions. Do not interpret design intentions as implemented guarantees.

## Project principles

- The repository is the object being governed; agents and developers are participants.
- A canonical, versioned governance model is the normative authority. Human-readable documents must remain consistent with it.
- The governance and assurance model applies to every project, regardless of project size. Formal assurance is not an optional maturity tier.
- A small local executable is the primary user interface. No hosted GovCheck service, mandatory daemon, or MCP server is required.
- Git and Pijul are first-class version-control systems. Local-only, team-hosted, self-hosted, and public hosting workflows are in scope.
- Version control, hosting, collaboration, and acceptance are separate concerns.
- Local checks are useful, but acceptance must be independently verifiable at the integration boundary where the hosting or team infrastructure can enforce it.
- Reuse established tools through narrow adapters; do not rebuild entire ecosystems inside GovCheck.
- Bootstrap and migration operations must be inspectable, planned, explicit, and non-destructive.

## Languages

The default project language is **English**. French documentation is provided alongside it.

- English: start with this README.
- Français : see [README.fr.md](README.fr.md).

## Current status

This is the initial bootstrap. The first milestone is to define and review the canonical governance contract, lifecycle model, assurance vocabulary, and adapter boundaries before committing to an implementation language or a large dependency stack.

See [the bootstrap decisions](docs/decisions/0001-bootstrap-boundaries.md) (English) and [leur traduction française](docs/decisions/0001-bootstrap-boundaries.fr.md).

## License

No license has been selected yet. Until one is added, the repository should not be assumed to grant permission to reuse, modify, or redistribute its contents.
