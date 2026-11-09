# 0030 — Repository-backed governed work portfolio and recoverable revision history

**Status:** architecture proposal for maintainer review; the initial Markdown register is created on this branch, but no machine-enforced append-only store, recovery service, forge synchronizer or edit-interception control is implemented.  
**Language:** English is the default; see [French](0030-repository-backed-work-portfolio-and-recoverable-history.fr.md).

## 1. Context and problem

Architecture 0028 correctly separates intake, candidate backlog and committed work, and correctly treats GitHub Issues/Projects as an operational adapter rather than governance authority. Its unresolved weakness was the absence of a repository-backed canonical register and a sufficiently strong revision/recovery contract.

An issue body is mutable and forge-specific. GitHub activity history is useful provenance, but it is not a portable canonical revision model, a guaranteed lossless document history, or an independent recovery mechanism. Requiring humans or agents to remember not to overwrite prior content transfers the integrity obligation to the editor and contradicts GovCheck's preventive, recoverable-by-default philosophy.

GovCheck must let an editor make mistakes without silently destroying the last accepted governance state. It should prevent unsafe transitions where it can, detect bypasses where prevention is outside its boundary, preserve prior states, and support recovery.

## 2. Architectural decision proposed

Establish a **repository-backed Governed Work Portfolio Registry** under docs/work-portfolio/ as the canonical documentation record of GovCheck work items and their relations. The registry is independent of forge and VCS-specific work-item objects.

The initial repository artefacts are:
- README.md / README.fr.md — purpose, semantics, lifecycle and operating contract;
- work-items.md — stable work-item identities, canonical outcome summaries, classification and source mappings;
- events.md — append-only-by-policy logical event journal.

The register is a portfolio artefact, not a competing normative policy engine. Its semantics are constrained by the canonical governance model, lifecycle specification, artifact identity policy and adopted decisions.

The initial Markdown representation is deliberately provisional. This decision does not select JSON, YAML, RDF, a database, event-sourcing product, expression language or storage service. A machine-readable form requires a separate decision after the semantic contract and lossless migration tests are established.

## 3. Vocabulary and scope

- **Work portfolio:** governed collection of work across its lifecycle.
- **Backlog:** candidate stage only, not the entire portfolio.
- **Work item:** bounded unit with an intended outcome and independently assessable completion.
- **Registry:** canonical repository-backed collection and its identity/revision metadata.
- **Adapter:** forge, project board, local UI or collaboration system that presents or coordinates registry objects without becoming their authority.
- **Event:** immutable logical occurrence describing a state transition, decision, correction, authorization, invalidation or result.

Lifecycle states remain those of Architecture 0028: Intake → Candidate backlog → Committed work, with execution, blocking, validation and typed terminal resolutions. Priority, assignment, issue openness, project membership and parentage never authorize work.

## 4. Canonical identity and adapter mapping

Every logical work item MUST have a stable ID independent of title, filename, forge, issue number and VCS. IDs are never recycled. Splits, merges, duplicates, successors and supersessions are explicit typed relations. An issue number is stored only as an external adapter mapping and provenance reference.

The registry record SHOULD include: outcome, scope/non-goals, source/provenance, work nature/domain, lifecycle state, priority and rationale, assumptions/unknowns, risks, requirements, decisions, dependencies, completion criteria, verification method, responsible actor, authorizing decision for committed work, result/evidence links, adapter mappings and revision/event history.

A parent portfolio grouping is organizational only. It does not imply dependency, inherited priority, authority, commitment or acceptance.

## 5. Revision, events and recovery

The design separates three things:

1. **Current register projection:** readable current state of each work item.
2. **Logical event history:** append-preserving sequence of changes and decisions; corrections add new events.
3. **Native repository history:** exact VCS revisions that preserve the accepted document states.

The initial repository journal adopts append-only semantics by policy. Each event SHOULD identify event ID, subject ID, type, actor/provenance, time, base/resulting revision where available, rationale, authority/decision reference and related evidence. A correction or rollback is a new event, never an edit to an earlier event.

The accepted repository revision is the practical initial recovery point. Changes are prepared on a dedicated branch/channel and reviewed against an exact base/candidate. An uncommitted working-tree edit is not a protected revision.

**Critical limitation:** Git and Pijul history alone do not provide a complete tamper-proof audit or independent backup guarantee. A privileged actor or compromised hosting service may rewrite or delete history. An append-only Markdown file is not physically append-only merely because its policy says so. Until enforcement exists, the architecture MUST describe this honestly and MUST NOT claim immutability or prevention.

Future controls must assess protected refs/channels, independent replication, signatures/attestations, content digests, immutable snapshots, local edit interception, authorization, concurrent updates, recovery and restore tests. The technology choice must preserve Git and Pijul semantics and must not make a hosted forge mandatory.

## 6. Safety properties and threat cases

The implementation contract must ultimately demonstrate:

- **No silent loss:** an accepted prior state remains recoverable after an ordinary edit, rejected change, rollback or supersession.
- **No event rewriting:** corrections and revocations are new events; old events remain addressable.
- **Exact binding:** decisions and evidence refer to exact item, governance and candidate revisions.
- **No implicit authorization:** editing a record, changing priority, assigning an issue or moving a board card cannot commit work.
- **Concurrency safety:** competing edits cannot silently overwrite one another; stale candidates require rebase/re-evaluation.
- **Adapter non-authority:** forge-side mutation cannot silently overwrite the canonical registry.
- **Visible uncertainty:** missing provenance, unknown state or unavailable history blocks or remains explicitly indeterminate.
- **Recoverability:** a documented restore procedure can reconstruct a prior accepted state and its traceability.

Threat scenarios include accidental editor overwrite, malicious contributor, compromised maintainer/forge, force-push or channel rewrite, deletion, concurrent edits, stale adapter synchronization, corrupted journal, compromised signing key and incomplete backup. Each property must be scoped to an explicit threat model; no single mechanism is assumed to solve all cases.

## 7. Adapter transition

GitHub Issues #40 and #78–#85 remain open during migration as navigation and coordination views. Work issues #41–#77 and #86 remain mapped by their source numbers. Issue #33 remains an atomic candidate. Historical source issues and comments are preserved and linked as provenance.

The migration is additive:
- no issue or comment is deleted;
- an issue is not closed merely because its contents are imported;
- completed, duplicate or superseded work receives an explicit disposition and successor/result link;
- the repository register is authoritative; issue edits are not automatically authoritative;
- synchronization is initially explicit/manual, with drift reported rather than silently resolved.

A live adapter requires a separate contract and round-trip tests for IDs, relations, provenance, event history, lifecycle state and decisions. Import/export must not lose or invent semantics.

## 8. Relationship to existing architecture

This record elaborates Architecture 0028 and is constrained by:
- Specification 0002 — Canonical Governance Model;
- Specification 0003 — Change Lifecycle and Acceptance;
- Specification 0004 — VCS and Collaboration Adapter Contracts;
- Architecture 0012 — Canonical Normative Authority and Documentation Conformity;
- Architecture 0017 and ADR 0004 — Artifact Identity, Revision and Versioning;
- Architecture 0018 — Version Governance, Compatibility and Approval Authority.

Specification 0003 already requires auditable transitions and append-only logical history. Architecture 0017 distinguishes logical identity, immutable revision identity, contract version and event/instance identity. This record applies those distinctions to the work portfolio; it does not replace those contracts.

## 9. Migration baseline

The initial register at docs/work-portfolio/work-items.md imports the active candidates from issues #41–#77 and #86 and the atomic issue #33. It retains #40 and #78–#85 as adapter views. Historical issues #23, #26, #30, #35 and #37 remain provenance sources; #61 is mapped as a duplicate predecessor of #62. Issue #46 is recorded as completed against merged PR #39 / ADR 0005, with source closure deferred until this registry change is accepted. Issue #75 remains open pending formal adoption.

The import captures stable identity, intended outcome, source mapping, classification and disposition. It does not copy every conversational comment into the canonical register; source discussions remain accessible and are not silently elevated to adopted decisions.

## 10. Implementation sequence

1. Review and adopt the registry semantics and migration baseline.
2. Define a machine-checkable work-item/event contract without prematurely choosing a storage technology.
3. Define append-only enforcement, atomic update, concurrency and recovery guarantees.
4. Define Git and Pijul native revision bindings and a neutral adapter contract.
5. Implement deterministic integrity/drift checks and negative tests for overwrite, deletion, stale update and unauthorized transition.
6. Add independent replication and restore exercises according to the threat model.
7. Only then migrate from manually maintained adapter views to controlled synchronization.

## 11. Non-claims

This architecture does not claim that the current Markdown journal is tamper-proof, that GitHub issue edits are blocked, that backups/signatures/replication exist, that all historical comments have been imported, or that the future registry engine is implemented or formally verified. The initial migration is a documented, reviewable baseline and a step toward the required guarantees, not the guarantees themselves.
