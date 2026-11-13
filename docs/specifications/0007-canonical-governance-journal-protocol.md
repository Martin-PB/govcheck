# Specification 0007 — Canonical governance journal and VCS adapter protocol

**Status:** proposed semantic contract for review; not normative adoption and not an implementation claim. No database, serialization, cryptographic suite, consensus product or forge is selected. **French:** [0007](0007-canonical-governance-journal-protocol.fr.md).

## 1. Purpose and scope

This specification refines Specification 0006 by defining protocol obligations around the canonical logical governance journal: append, compare-and-append, durable commit, crash recovery, idempotent retry, replica observation and VCS adapter reconciliation.

The canonical journal is the sole authority for normative event order within its governance scope. Git, Pijul and other VCSs/forges carry candidate content and provenance observations; their native ordering, branch topology, timestamps, merge order or hosting-service state do not allocate normative journal positions.

This is a technology-neutral semantic contract. Storage engine, wire format, hash/signature algorithm, consensus implementation, network protocol, VCS and forge remain implementation choices requiring separate evidence and compatibility analysis.

## 2. Terms and identities

- **Journal scope:** authority domain within which one canonical event sequence is ordered.
- **Journal head:** latest committed position and its integrity identity (for example, a digest or equivalent immutable token).
- **Journal event:** immutable record committed at exactly one position.
- **Append request:** proposed event plus expected predecessor/head and idempotency identity.
- **Commit receipt:** durable evidence that an event occupies a specified canonical position.
- **VCS observation:** native Git/Pijul/other-VCS revision, patch, change, ref, channel, forge event or object observed by an adapter.
- **Adapter:** component translating native VCS/forge observations into candidate/provenance identities; it is not a normative ordering authority.
- **Materialized state:** derived view or projection reconstructed from committed journal events.
- **Unknown commit outcome:** caller cannot determine whether a request crossed the durable commit point.

Event ID, idempotency key, journal position, payload digest, VCS-native revision, candidate identity, evaluation ID, authorization ID and governance-revision identity are distinct and MUST NOT be conflated.


The journal scope MUST have a stable, unambiguous identity. This specification does not decide whether a scope maps one-to-one to a repository, spans multiple repositories under one authority domain, or follows another governance boundary. That mapping MUST be explicitly defined before a deployment treats a journal as canonical; a VCS or forge URL MUST NOT implicitly define the scope.

## 3. Journal identity and event envelope

A journal scope MUST have one canonical logical sequence. Each committed event MUST carry:
1. a stable event ID unique within the scope;
2. a strictly increasing canonical position;
3. exact predecessor position and integrity identity, except for genesis;
4. event type and schema identity/revision;
5. payload identity/integrity bound to the exact event payload;
6. actor/principal and provenance attribution required by the applicable authority policy;
7. relevant candidate, evaluation, authorization, publication or governance-revision identities;
8. an idempotency key for retryable append requests (genesis/bootstrap records are governed by a separate anchor procedure and need not carry one);
9. required rationale, assumptions, limitations and evidence references.

A wall-clock timestamp MAY be recorded as descriptive metadata. It MUST NOT allocate positions, resolve concurrency or determine applicability.

Encoding, canonicalization, digest/signature scheme and schema language remain implementation choices. The choices made MUST provide deterministic identity for the exact committed envelope and MUST be documented with versioning and migration rules.


The genesis record MUST bind the journal-scope identity, the initial authority record/revision, the initial governance revision, and the initial event/schema semantics. Its provenance and trust anchor MUST be explicit and independently verifiable under the deployment's stated trust model. This specification does not select the bootstrap trust mechanism. A missing, ambiguous or unverifiable genesis yields `unknown` and MUST block normative append; it MUST NOT be reconstructed from a VCS branch or forge default.


The selected integrity mechanism MUST make payload and predecessor substitution detectable under the documented threat model. The integrity identity alone MUST NOT be treated as proof of actor authenticity: principal/provenance attribution MUST be validated separately against the applicable authority mechanism. A deployment may use cryptographic commitments, trusted storage integrity, authenticated records, or a combination, but MUST document the guarantees and trust assumptions; no algorithm or suite is selected here.


An idempotency key MUST be unique within its journal scope for as long as the corresponding event can remain authoritative. It MUST be bound to the exact append operation, including event type, event ID, expected head and payload identity. Reuse with the same request envelope returns the original receipt; reuse with any different envelope is `conflict`. Compaction, snapshots and projection rebuilds MUST preserve this lookup guarantee (or an equivalent non-reusable tombstone). Genesis/bootstrap records are governed by the separate genesis procedure and are exempt from ordinary append idempotency keys.

## 4. Compare-and-append and serialization

An append request MUST name the expected journal head by canonical position and integrity identity, or an equivalent unambiguous head token.

The journal MUST provide one linearization point for accepting an append:
- if the expected head matches the current committed head and all applicable preconditions hold, exactly one next position is committed;
- if the expected head is behind the current head, the request is stale and MUST NOT be silently rebased;
- if the expected position matches but the integrity identity differs, the result is conflict or unknown according to whether the journal can establish a definitive inconsistency;
- if the journal cannot establish the current head or required authority state, the operation is blocked as unknown.

At most one event may commit at a given canonical position. Competing requests against the same head cannot both succeed. A displaced request must be re-evaluated and re-authorized against the new head before it is submitted again.

A successful append returns a durable commit receipt binding scope, position, event ID, predecessor identity and event integrity identity. A success response MUST NOT be returned before the durable commit point.

## 5. Evaluation, authorization and publication

Evaluation, authorization and publication are three distinct logical acts with distinct identities and traceable relationships, even if one adapter or persistence implementation executes them inside one atomic technical transaction.

Authorization MUST bind the exact evaluation, candidate, base governance revision and expected journal head. Publication MUST revalidate that binding and applicable exception/revocation/staleness controls immediately before its commit point.

A stale evaluation MUST remain immutable historical evidence with an explicit stale disposition and reason. It MUST NOT be reused to authorize or satisfy a later transition. A new transition requires a fresh evaluation over the current candidate/base/governance/evaluator/specification/evidence inputs; the old evaluation is retained as history and is not rewritten.

The publication event is the effect point: the resulting governance revision applies prospectively from the canonical position occupied by that publication event, not from a Git/Pijul commit, merge, tag, branch update, CI completion, local file write or wall-clock timestamp.

A technical transaction may prepare or record evaluation and authorization before publication, but MUST NOT expose the resulting revision as applicable unless the publication event is durably committed. A failed or aborted transaction MUST leave no partially applicable governance revision.

## 6. Durability, retry and crash recovery

The durable journal append is the commit point. Volatile preparation is not publication.

- **Crash before durable commit:** no event was committed. Volatile pending state may be discarded. Retry may use the same idempotency key and exact payload.
- **Crash after durable commit but before response:** the event remains committed. The caller MUST resolve the outcome by querying the idempotency key/event ID or journal head. It MUST NOT create a new event ID and blindly repeat the operation.
- **Duplicate retry, same key and same payload:** return the original commit receipt without appending a second event.
- **Same key, different payload:** return conflict; never reinterpret the key or overwrite the earlier event.
- **Unknown commit outcome:** return unknown/blocked until a journal read or recovery procedure resolves whether the exact event committed.
- **Committed event, missing materialized projection:** replay from a verified journal position. Projection rebuild MUST be idempotent and MUST NOT create a second normative event.
- **Journal integrity failure, missing predecessor or contradictory committed records:** fail closed as unknown or conflict; do not guess, repair in place or advance the head.

Snapshots and materialized views MAY accelerate recovery, but each MUST be anchored to an exact journal position and integrity identity. The journal remains authoritative. A snapshot cannot erase, reorder or supersede committed history.

External side effects MUST be coordinated so replay cannot silently duplicate a normative action. Implementations MUST use an explicit idempotency/outbox/reconciliation contract or demonstrate an equivalent property; this specification does not prescribe a mechanism.

## 7. VCS adapter and provenance contract

A VCS adapter MAY identify exact native revisions, patches/changes, refs/channels and object/content digests; fetch, publish or transport candidate content; attach forge/VCS event metadata as provenance; report divergence, missing objects, merge conflicts and replication observations; and propose a candidate append to the canonical journal.

A VCS adapter MUST NOT allocate or reorder canonical journal positions; treat commit timestamps, ancestry, branch/channel order, merge order or forge event order as normative governance order; infer authorization from push, merge, tag, protected-branch status or green CI; overwrite a committed journal event; or resolve a governance conflict by choosing a Git/Pijul branch or forge default.

Each VCS observation SHOULD preserve, where available, VCS kind, repository identity, native revision/change/object identity, content digest, ref/channel, observed parent(s), remote/forge identity, observation time (descriptive only) and adapter version. Missing provenance MUST be explicit; it MUST NOT be fabricated from a journal position.

The same logical candidate may have multiple native VCS representations. Adapters MUST bind them to a common candidate identity only when a proof-carrying mapping contract formally demonstrates the exact identity/equivalence relation claimed, for the declared candidate semantics, scope, assumptions and exact native revisions. A matching content digest is an integrity witness for bytes under its hash assumptions; by itself it is not a formal demonstration of semantic equivalence or of common candidate identity. If the relation is not demonstrated, adapters MUST preserve the native identities separately and MUST NOT use the proposed association as an established premise in journal or governance reasoning. Native revision identity and canonical journal identity remain distinct.

## 8. Replica reconciliation

Replicas synchronize by canonical journal scope, position and event integrity identity, not by selecting the newest native VCS revision.

- A replica behind the canonical head is stale and may replay missing committed events.
- A replica reporting the same position and same integrity identity is consistent for that prefix.
- A replica reporting the same position with a different integrity identity is in conflict.
- A missing position, unverifiable predecessor or inaccessible authority chain is unknown.
- Divergent Git branches or Pijul channels are provenance/content divergence; they do not decide which governance event is canonical.
- A VCS event with no corresponding authorized journal event is an observation or candidate only, not a publication.

Reconciliation MUST preserve all conflicting observations and their provenance. Resolution requires an explicit authorized journal event or a separate documented resolution protocol. It MUST NOT rewrite earlier canonical events.

## 9. Failure/result vocabulary

| Result | Meaning | Permitted effect |
|---|---|---|
| committed | Durable event receipt is established | Advance canonical head exactly once |
| stale-base | Expected head no longer matches | No append; re-evaluate and re-authorize |
| unknown | Commit/head/authority cannot be established | Block; recover/query; no inferred success |
| conflict | Contradictory identity, duplicate key with different payload, or inconsistent committed history | Block; explicit traceable resolution |
| rejected | A known policy/authorization precondition failed | No append |
| unavailable | Journal service cannot safely decide | No append; retry only under idempotency contract |

Unknown and conflict are distinct blocking states. Neither may be coerced to Pass, bypassed through an exception, or resolved by VCS ordering.

## 10. Conformance scenarios

| ID | Scenario | Required result |
|---|---|---|
| J-01 | Two append requests use the same expected head | At most one commits at the next position |
| J-02 | Retry after durable commit but lost response, same key/payload | Original receipt returned; no duplicate event |
| J-03 | Same idempotency key with different payload | Conflict; original record preserved |
| J-04 | Crash before commit | No event appears in durable history |
| J-05 | Crash after commit before projection update | Recovery replays committed event exactly once into projection |
| J-06 | Replica has same position but different event identity/digest | Conflict; no automatic winner |
| J-07 | Git/Pijul push/merge/tag without journal publication | No governance effect |
| J-08 | Rollback restores content from an earlier revision | New event and new revision at a later position |
| J-09 | Journal head or predecessor cannot be verified | Unknown; no append |
| J-10 | Evaluation/authorization binds an obsolete head | Publication blocked; full re-evaluation required |
| J-11 | Evaluation, authorization and publication execute atomically | Three logical identities/records remain distinguishable |
| J-12 | VCS adapter reports divergent branches/channels | Preserve observations; do not derive normative order |

These are semantic conformance targets. They do not claim that a production journal or adapter currently exists.

## 11. Formal relationship and limits

This specification complements [Specification 0006](0006-governance-revision-applicability.md), [Architecture 0032](../architecture/0032-canonical-publication-model-checking.md), [Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.md) and [Architecture 0035](../architecture/0035-canonical-journal-recovery-model.md).

Current TLA+ models cover separate bounded slices: applicability and temporal authority; compare-and-append publication; evaluator/exception/revocation controls; and journal crash/recovery/rollback safety. They are composable design evidence, not a single integrated implementation model. The journal-recovery model assumes upstream authorization and a single serialized writer; it does not prove multi-writer consensus, durable filesystem semantics, eventual recovery, adapter correctness, replica reconciliation or implementation refinement.

References: [R-05 — TLA+ and TLC](../references.md#r-05), [R-22 — native Git and Pijul semantics](../references.md#r-22), [R-194 — linearizability](../references.md#r-194), [R-195 — write-ahead logging and crash recovery](../references.md#r-195), [R-196 — idempotent retry semantics](../references.md#r-196).

## 12. Authority boundary

The eleven outcomes in [decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md) remain the owner's settled design inputs. This specification elaborates their engineering consequences and does not reopen them. It is a technical proposal only. Formal normative adoption remains exclusively reserved to the repository's root authority and is not inferred from this document, PR review, merge, CI or model checking.
