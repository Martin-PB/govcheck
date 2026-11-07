# Architecture specifications

These specifications complete the initial architecture-design pass. English is the default; each document has a French counterpart.

1. [0002 — Canonical Governance Model](0002-canonical-governance-model.md) · [Français](0002-canonical-governance-model.fr.md)
2. [0003 — Change Lifecycle and Acceptance](0003-change-lifecycle.md) · [Français](0003-change-lifecycle.fr.md)
3. [0004 — VCS and Collaboration Adapter Contracts](0004-vcs-collaboration-contracts.md) · [Français](0004-vcs-collaboration-contracts.fr.md)
4. [0005 — Assurance, Claims and Evidence](0005-assurance-model.md) · [Français](0005-assurance-model.fr.md)

Threat analysis and technology-selection process: [Architecture design](../architecture/README.md) · [Français](../architecture/README.fr.md).

## Status and boundaries

These are proposed architecture contracts for maintainer review, not implemented behavior. They intentionally do not select an implementation language, serialization format, expression language, formal kernel, cryptographic scheme, license, or mandatory dependency stack.

The specifications define semantics and conformance targets. They do not claim that GovCheck currently has an evaluator, lifecycle engine, Git/Pijul adapters, forge enforcement, model checking, theorem proofs, or implementation-conformance evidence.

The next engineering phase should derive executable conformance tests and formal models, then resolve technology choices using the architecture decision framework.

External standards, methods and project sources are indexed in the [central reference catalogue](../references.md) ([French](../references.fr.md)). Follow the [reference-integrity maintenance guide](../reference-integrity.md) and run the offline checker before changing references; inclusion does not imply adoption.