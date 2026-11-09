# Governed Work Portfolio

**Status:** initial repository-backed registry proposed for maintainer review. This establishes the canonical documentary home and migration baseline; it does not claim that a registry engine, event store, automatic issue synchronizer, immutable storage service or enforcement boundary is implemented.  
**Language:** English is the default; see [French](README.fr.md).

## Purpose and lifecycle

The Governed Work Portfolio is the repository's tool-independent canonical record of proposed and authorized work. It belongs to the repository, not to GitHub Issues, GitHub Projects or another forge-specific object.

It covers:
- **Intake:** a signal or subject awaiting qualification.
- **Candidate backlog:** work retained for possible future execution; retention is not authorization.
- **Committed work:** a bounded work item explicitly authorized by the competent authority.
- **Execution and closure:** progress, evidence, result, acceptance, rejection, withdrawal or supersession, each with distinct semantics.

The word *backlog* names the candidate stage, not the whole portfolio. *Work item* names a bounded unit. *Work portfolio* names the governed collection across all stages.

## Authority and related artefacts

The canonical semantics are governed by the canonical governance model and applicable specifications. This portfolio records work objects and relationships; it does not create a competing policy authority.

- This directory is the canonical repository-backed register of GovCheck work items and portfolio-level records.
- [Architecture 0028](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.md) defines the lifecycle and issue-tracker boundary.
- Specifications 0002–0005 define related governance, change-lifecycle, adapter and assurance contracts.
- Decisions/ADRs remain authoritative for adopted decisions; requirements remain in their governing specifications; evidence and results remain separately identified artefacts.
- GitHub Issues, Projects, other forge work items and local interfaces are adapters/projections. They may coordinate discussion but do not define canonical identity, authority, commitment or acceptance.

An issue link is provenance and an adapter mapping, not delegation of authority to that issue.

## Current register

- [Work-item register](work-items.md) — initial import of issues #33, #41–#77 and #86, with stable IDs, source mappings and dispositions.
- [Portfolio event journal](events.md) — append-only logical change record.
- [French overview](README.fr.md).

The initial representation is human-readable Markdown. No JSON/YAML/RDF/database or expression language is selected. A machine-readable representation requires a separate semantic and technology decision with lossless mapping and migration tests.

## Identity and revision

Each logical work item receives a stable GovCheck ID (govcheck.work.<slug>), independent of title, path, issue number, forge or VCS. Descriptive fields may change; IDs are never recycled. Splitting, merging, replacement and supersession are explicit relations and may require new IDs.

Each published repository revision is identified by the native VCS identity and exact path/content. Git commit/tree/blob identities and Pijul patch/channel identities are complementary; GovCheck must not fabricate Git-shaped identifiers for Pijul. Content digests may supplement them but do not prove semantic equivalence, truth or authorization. See Architecture 0017 and ADR 0004.

## Change safety and history

The intended invariant is that an ordinary edit must not erase the last accepted state or silently rewrite a decision. The initial workflow is:

1. Edit on a dedicated change branch/channel, not directly in the accepted baseline.
2. Produce a reviewable change bound to an exact base and candidate.
3. Append a journal entry describing the proposed transition and provenance; never edit or delete an earlier event.
4. Review and accept the exact candidate under the applicable governance revision.
5. Preserve the accepted repository revision and native VCS history. Correction, rollback and supersession are new changes/events, not edits to old events.

**Important limitation:** ordinary Git/Pijul history is version history, not by itself a tamper-proof audit service or independent backup. A privileged actor or compromised forge may rewrite history. This document does not claim to prevent that. Independent integrity protection, protected refs, signatures, replication, recovery and local edit interception remain design/implementation work. Until then, the accepted mainline revision and its review/merge record are the practical recovery point; uncommitted working-tree edits are not protected.

GovCheck must ultimately make unsafe operations difficult or blocked, detect bypasses, preserve prior accepted states and support recovery without relying on editor discipline. The human/agent editor is not the integrity control.

## Event journal semantics

The events file is append-only by policy. Each entry has a stable event ID, subject ID, event type, actor/provenance, base and resulting revision (when available), time, rationale, authority/decision reference and related evidence. A correction is a new event explicitly correcting or superseding an earlier one. Never silently edit an old event.

The journal is currently a repository document, not a dedicated protected append-only store or machine-enforced invariant. This limitation remains until controls are demonstrated.

## Work-item record contract

Each item should identify, as applicable: stable logical ID and title; source signal and provenance; intended outcome, scope and non-goals; work nature and domain; lifecycle state; priority and rationale separate from authority; assumptions, unknowns and risks; requirements, decisions and dependencies; completion criteria and verification method; accountable actor and authorizing decision for committed work; linked changes, evidence, results and acceptance events; adapter mappings; revision and event history.

Unknown information stays explicitly unknown. Missing fields are not silently satisfied. Parent grouping does not confer priority, dependency, authority, commitment or acceptance.

## Adapter policy and transition

GitHub remains useful during migration:
- Issues remain open where they coordinate active candidate work or discussion.
- #40 and #78–#85 become navigation/coordination views pointing to this register.
- Existing issue numbers remain external adapter IDs and historical provenance.
- No issue is closed merely because content was imported. Closure requires a recorded resolution and successor/canonical location.
- Migration is additive: no issue, comment or source discussion is deleted.
- Synchronization is initially explicit/manual; drift is reported rather than silently reconciled. Authority flows from repository register to adapter projection.

This is not yet a live synchronization implementation. Adapter contracts, lossless export/import tests and deterministic drift checks remain required.

## Required future controls

This initial registry is a controlled document, not an executable service. Future work must specify and validate: immutable revision/event identities across Git and Pijul; atomic updates and concurrency; append-only enforcement and tamper detection; recovery points, independent replication and restore drills; authorization and prospective governance-revision applicability; forge adapters with lossless mappings; deterministic checks for transitions, provenance, links, stale evidence and adapter drift; and threat scenarios including accidental overwrite, malicious editor, compromised forge, force-push, deletion, concurrent edits and rollback.

No prevention, immutability or enforcement is claimed until tests and/or formal verification demonstrate the property within a stated threat model.

## GovCheck references

- [Architecture 0028](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.md).
- [Specification 0002](../specifications/0002-canonical-governance-model.md).
- [Specification 0003](../specifications/0003-change-lifecycle.md).
- [Specification 0004](../specifications/0004-vcs-collaboration-contracts.md).
- [Architecture 0017](../architecture/0017-artifact-identity-revision-and-versioning.md) and [ADR 0004 / Architecture 0018](../architecture/0018-version-governance-and-compatibility-authority.md).
- [Architecture 0012](../architecture/0012-normative-authority-and-documentation.md).
- [Reference catalogue](../references.md), notably R-24 (PROV provenance vocabulary), where applicable.

A reference does not imply adoption, implementation or assurance.
