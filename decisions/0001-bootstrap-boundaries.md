# ADR 0001: Product boundaries and bootstrap architecture

- **Status:** Accepted as the initial baseline; changes require a superseding ADR.
- **Date:** 2026-11-05
- **Scope:** Product identity, normative authority, runtime footprint, VCS/hosting, assurance, and maintainability.

## Context

GovCheck governs software repositories and their development lifecycle. It is not primarily an agent sandbox, tool-call gateway, hosted control plane, CI replacement, or scanner bundle. This repository is at initial bootstrap: no executable, canonical policy engine, formal proof, or forge enforcement exists. This ADR records design decisions, not implemented guarantees.

## Decisions

1. **Repository-centred governance.** The repository and change lifecycle are governed. Developers and agents are contributors. GovCheck will provide project context, applicable requirements, change planning, decisions, deviations, evaluations, evidence, and acceptance conditions.
2. **One normative authority.** A versioned, machine-readable canonical governance model interpreted by GovCheck will be authoritative. Markdown (including AGENTS.md, GOVERNANCE.md, SECURITY.md, and CONTRIBUTING.md) is a controlled projection or explanation and must not silently introduce conflicting rules. Its semantics remain to be designed.
3. **Formal foundations for every repository.** Governance and assurance foundations apply regardless of repository size. Project-specific requirements and evidence vary; the existence of the formal model does not.
4. **Local executable, no mandatory MCP or hosted service.** A small local executable is the primary interface for people, scripts, CI, and agents that can run commands. No hosted service, resident daemon, or MCP server is required. Machine-readable output is expected. Direct local file edits cannot be universally prevented by a portable executable; acceptance must independently validate evidence.
5. **Separate VCS, hosting, collaboration, and acceptance.** Git and Pijul are first-class and semantically distinct. Local-only, team-hosted, self-hosted, and public hosting are in scope. Pijul patches, dependencies, channels, and conflicts must be represented natively, not flattened into Git commits and branches.
6. **Small core and narrow adapters.** Prefer a small governance/assurance core, declarative profiles, and narrow adapters to a dynamic plugin framework. Reuse existing project tools; assume no large mandatory toolchain.
7. **Non-destructive bootstrap.** Initialization and migration follow inspect → plan → apply, preserve existing files, detect conflicts, and require review for destructive or normative changes.
8. **English default, French in parallel.** English is the default landing and canonical presentation language. User-facing documentation and architecture decisions have French counterparts that preserve the meaning and status of the English text.
9. **Formal methods are foundational.** Governance semantics and lifecycle must be designed for formal analysis. Lean is a candidate for proof-critical logic; TLA+ or other methods may suit transition and distributed-process properties. No implementation language or formal tool is selected here.
10. **Evidence precision.** Distinguish ordinary check execution, model checking, proof checking, and implementation conformance. Evidence identifies subject, scope, assumptions, tool/version, and exact repository and governance state. A model result is not automatically a claim about implementation.

## Consequences

- The core must not hard-code GitHub concepts.
- VCS adapters preserve native Git and Pijul identity/state semantics.
- Forge enforcement is an adapter concern; local-only use remains complete.
- The executable is the primary interface; MCP is not required.
- The first implementation milestone is the canonical governance contract and lifecycle semantics, not numerous integrations.
- Temporary bootstrap policy remains until the canonical engine can evaluate and enforce the model.
- Documentation is bilingual, English first/default.

## Open decisions

Implementation language and distribution; canonical data/rule format; formalization strategy and trusted computing base; local acceptance and bypass resistance; Git/Pijul adapter contracts and state fingerprints; collaboration/forge capability model; license; reference checks and platform matrix.

Changes to these boundaries require a superseding ADR. Do not silently rewrite this historical decision.

French: [ADR 0001 (français)](0001-bootstrap-boundaries.fr.md).