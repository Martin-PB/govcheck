# Architecture 0038 — Local canonical journal implementation profile

**Status:** proposed implementation profile for issue #155. It is not a normative adoption of Specification 0007 and does not claim that a local database is tamper-proof or distributed-consensus capable. **French:** [0038](0038-local-canonical-journal-implementation.fr.md).

## 1. Decision under evaluation

Use Python's standard-library SQLite binding as the first local journal backend, with a single database file per explicit journal scope (or a database containing multiple explicitly identified scopes). Keep the logical journal contract independent of this backend. The implementation is an embedded library/CLI; it does not start a hosted service, MCP server or daemon.

This choice is based on the first implementation's requirements: transactional compare-and-append, serialized writers, idempotency lookup, atomic event/receipt/head updates, crash recovery and offline tests. SQLite provides transactions and a BEGIN IMMEDIATE mode that obtains the write transaction before reading/updating the head. WAL mode allows readers and a writer to proceed concurrently, but still serializes writers and requires all processes to use the database on the same host.

## 2. Storage alternatives

| Option | Advantages | Costs/risks |
|---|---|---|
| Append-only JSONL/file journal | Human-inspectable; simple export; easy to copy | Atomic multi-record update of event, head and receipt is not portable; cross-process locking differs by OS; partial writes, fsync ordering, compaction and crash recovery become custom code. |
| SQLite (stdlib) | Embedded, no server/dependency; transactional uniqueness and compare-and-append; recovery handled by SQLite; readers can coexist with a writer in WAL mode | One writer at a time; WAL is same-host only and unsuitable for network filesystems; durability depends on PRAGMA settings, VFS, filesystem and hardware; administrators can still replace or rewrite the database. |

The initial profile chooses SQLite to avoid inventing a portable file-locking/transaction protocol. This does not select SQLite as the only possible backend for all GovCheck deployments.

## 3. SQLite operational profile

The first implementation MUST:
- open the database in a local filesystem path and reject or clearly document unsupported network/shared filesystems;
- use PRAGMA journal_mode=WAL, PRAGMA synchronous=FULL, PRAGMA foreign_keys=ON and a bounded busy timeout;
- use explicit BEGIN IMMEDIATE for append so the writer reservation is acquired before comparing the expected head;
- update the event, idempotency index, durable receipt and scope head in one SQLite transaction;
- return a committed receipt only after COMMIT succeeds;
- if the caller loses the response after commit, allow a retry with the same idempotency key and exact request to recover the original receipt;
- reject reuse of an idempotency key with a different request as conflict;
- keep committed event and receipt rows immutable through database constraints/triggers, while treating those triggers as guardrails rather than a security boundary;
- verify the full event hash chain and receipts independently of the mutable head projection.

WAL mode permits concurrent readers while a writer is active, but does not permit multiple simultaneous writers. BEGIN IMMEDIATE makes writer contention explicit; busy/locked or ambiguous I/O outcomes must never be treated as success. WAL's same-host restriction is a deployment constraint. synchronous=FULL asks SQLite's VFS to sync commit data; it cannot compensate for a filesystem, storage controller or hardware that violates its durability contract.

## 4. Canonical event and receipt profile

The initial envelope is defined by the package schemas [journal-event-v1](../../govcheck/formal/schemas/journal-event-v1.schema.json) and [journal-receipt-v1](../../govcheck/formal/schemas/journal-receipt-v1.schema.json). It uses:
- explicit journal scope ID;
- monotonically increasing position (genesis at position 0);
- event ID, event type and schema revision;
- payload plus payload SHA-256;
- predecessor event digest;
- actor/principal attribution as data (not authenticated by this profile);
- optional idempotency key for ordinary append requests;
- informational UTC timestamp (never an ordering authority);
- event digest over the canonical envelope excluding the digest field itself.

The receipt binds scope, position, event ID, predecessor digest and event digest. It is persisted in the same transaction as the event and updated head. A receipt is returned only after the commit point. Reconstructing the receipt from the journal after an ambiguous client outcome is idempotent.

The serialized event and receipt identify the canonicalization profile as govcheck.jcs-safe-integer/v1. For hashable JSON, use a restricted RFC 8785 JCS-compatible profile: valid Unicode strings, object keys sorted by UTF-16 code-unit order, arrays kept in order, no duplicate object keys, no floating-point numbers, and integer values restricted to the exactly representable IEEE-754 safe-integer range. Exact rationals, decimals and larger integers are encoded as strings or typed records. This subset avoids an ad-hoc non-standard canonicalizer while remaining implementable with the standard library.

## 5. Append and recovery semantics

Append algorithm:
1. Validate the request envelope and compute its canonical request digest.
2. Start BEGIN IMMEDIATE.
3. Look up the idempotency key. Same key and same request digest returns the original receipt; same key and different digest returns conflict.
4. Read the current scope head and compare both expected position and digest. A mismatch returns stale or conflict; no automatic rebase is allowed.
5. Construct the next immutable event, receipt and new head.
6. Insert event and receipt, update the head projection, and commit atomically.
7. Only then return the durable receipt.

If the process crashes before commit, SQLite recovery must expose none of the event/receipt/head transaction. If the commit succeeds but the response is lost, retry returns the original receipt. If the client cannot determine whether commit occurred and cannot recover a receipt, the outcome is unknown; it must not retry with a new idempotency key.

Genesis is an explicit bootstrap operation requiring scope, initial authority identity/revision and initial governance revision. Append MUST fail closed if genesis is absent or ambiguous. A branch name, repository URL or forge default cannot create a journal scope or genesis implicitly.

## 6. Integrity, authority and limitations

A SHA-256 hash chain detects accidental modification, deletion, reordering and payload substitution when the verifier has a trusted checkpoint. It does not authenticate the actor, prove authority, prevent an administrator from replacing the database and recomputing the chain, or establish semantic correctness. SQLite triggers prevent accidental mutation through the ordinary API but are not an adversarial security boundary.

The first profile does not implement signatures, key management, distributed consensus, multi-host writers, replication or forge/VCS ordering. A later authenticated receipt may be DSSE-wrapped under issue #44; that does not make the database itself a trusted identity provider. Git/Pijul identities remain adapter-supplied provenance fields and do not determine canonical journal order.

## 7. References and related records

- [R-230 — SQLite transactions, WAL and durability](../references.md#r-230)
- [R-231 — RFC 8785 JSON Canonicalization Scheme](../references.md#r-231)
- [Specification 0007 — Canonical Governance Journal](../specifications/0007-canonical-governance-journal-protocol.md)
- [Architecture 0035 — Journal recovery model](0035-canonical-journal-recovery-model.md)
- Issue #155 — Local journal implementation
- Related: #45 acceptance boundary, #44 detached attestations, #86 governance revision applicability.

**This is a proposed first implementation profile. It does not adopt SQLite as a universal backend, prove actor authority, or claim protection against a privileged database administrator.**


The initial implementation verifies the full chain before append and before returning head/receipt data. This is O(n) in the number of events and intentionally favors fail-closed behavior over throughput for the first local profile. A future checkpoint/index optimization must preserve verification against a trusted checkpoint and be separately tested; a mutable head row alone is not a trusted checkpoint.
