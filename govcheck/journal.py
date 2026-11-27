#!/usr/bin/env python3
"""Local append-only GovCheck journal backed by the Python standard-library SQLite.

The journal provides transactional integrity and durable receipts. It does not
authenticate actors, establish authority, provide distributed consensus, or
protect against a privileged administrator who can rewrite the database.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1"
CANONICALIZATION_ID = "govcheck.jcs-safe-integer/v1"
GENESIS_EVENT_TYPE = "govcheck.journal.genesis"
MAX_SAFE_INTEGER = 9007199254740991


class JournalError(Exception):
    def __init__(self, kind: str, message: str):
        super().__init__(message)
        self.kind = kind


def _validate_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise JournalError("malformed", label + " must be a non-empty string")
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
        raise JournalError("malformed", label + " contains an invalid Unicode surrogate")
    return value


def _json_quote(value: str) -> str:
    _validate_string(value, "JSON string")
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _canonical_text(value: Any, path: str = "$") -> str:
    """Restricted JCS-compatible JSON: safe integers only, no floats."""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _json_quote(value)
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise JournalError("malformed", path + " integer exceeds the interoperable safe-integer range; encode it as a string")
        return str(value)
    if isinstance(value, float):
        raise JournalError("malformed", path + " floating-point numbers are not allowed in canonical journal JSON")
    if isinstance(value, list):
        return "[" + ",".join(_canonical_text(item, path + "[" + str(i) + "]") for i, item in enumerate(value)) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise JournalError("malformed", path + " object keys must be strings")
            _validate_string(key, path + " object key")
        ordered = sorted(value.keys(), key=lambda key: key.encode("utf-16be"))
        return "{" + ",".join(_json_quote(key) + ":" + _canonical_text(value[key], path + "." + key) for key in ordered) + "}"
    raise JournalError("malformed", path + " contains a value outside the canonical JSON subset")


def canonical_json_bytes(value: Any) -> bytes:
    return _canonical_text(value).encode("utf-8")


def _validate_digest(value: Any, label: str) -> str:
    digest = _validate_string(value, label)
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise JournalError("malformed", label + " must be a lowercase SHA-256 digest")
    return digest


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_json(value: Any) -> str:
    return sha256(canonical_json_bytes(value))


def _reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise JournalError("malformed", "duplicate JSON object key: " + key)
        result[key] = value
    return result


def load_json(path: str) -> Any:
    try:
        text = Path(path).read_text(encoding="utf-8")
        value = json.loads(text, object_pairs_hook=_reject_duplicate_pairs,
                           parse_float=lambda _: (_ for _ in ()).throw(JournalError("malformed", "floating-point JSON values are not allowed")),
                           parse_constant=lambda _: (_ for _ in ()).throw(JournalError("malformed", "non-finite JSON values are not allowed")))
        canonical_json_bytes(value)
        return value
    except OSError as exc:
        raise JournalError("unavailable", "cannot read JSON input: " + str(exc)) from exc
    except json.JSONDecodeError as exc:
        raise JournalError("malformed", "invalid JSON input: " + str(exc)) from exc


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _without(mapping: dict, key: str) -> dict:
    return {k: v for k, v in mapping.items() if k != key}


def _receipt_object(scope_id: str, position: int, event_id: str,
                    previous_digest: str | None, event_digest: str,
                    idempotency_key: str | None, committed_at: str) -> dict:
    receipt = {
        "schemaVersion": SCHEMA_VERSION,
        "canonicalization": CANONICALIZATION_ID,
        "scopeId": scope_id,
        "position": position,
        "eventId": event_id,
        "previousDigest": previous_digest,
        "eventDigest": event_digest,
        "idempotencyKey": idempotency_key,
        "committedAt": committed_at,
    }
    receipt["receiptDigest"] = digest_json(receipt)
    return receipt


class Journal:
    """A local SQLite journal. Each operation opens its own connection."""

    def __init__(self, database: str | Path, timeout_seconds: float = 5.0):
        raw_database = str(database)
        if raw_database == ":memory:":
            raise JournalError("unsupported", "in-memory databases cannot provide durable journal receipts")
        self.database = str(Path(raw_database).expanduser().resolve())
        self.timeout_seconds = max(0.1, float(timeout_seconds))
        Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def _connect(self):
        try:
            conn = sqlite3.connect(self.database, timeout=self.timeout_seconds, isolation_level=None)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("PRAGMA busy_timeout=" + str(int(self.timeout_seconds * 1000)))
            mode = conn.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            if str(mode).lower() != "wal":
                conn.close()
                raise JournalError("unsupported", "SQLite WAL mode is unavailable for this database/filesystem")
            conn.execute("PRAGMA synchronous=FULL")
            return conn
        except sqlite3.Error as exc:
            raise JournalError("unavailable", "cannot open local journal database: " + str(exc)) from exc

    def _initialize_schema(self):
        conn = self._connect()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS journal_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS journal_scopes (
                    scope_id TEXT PRIMARY KEY,
                    authority_id TEXT NOT NULL,
                    authority_revision TEXT NOT NULL,
                    governance_revision TEXT NOT NULL,
                    genesis_event_id TEXT NOT NULL,
                    head_position INTEGER NOT NULL,
                    head_digest TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS journal_events (
                    scope_id TEXT NOT NULL REFERENCES journal_scopes(scope_id),
                    position INTEGER NOT NULL CHECK(position >= 0),
                    event_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    previous_digest TEXT,
                    payload_digest TEXT NOT NULL,
                    request_digest TEXT NOT NULL,
                    idempotency_key TEXT,
                    envelope_json TEXT NOT NULL,
                    event_digest TEXT NOT NULL,
                    PRIMARY KEY(scope_id, position),
                    UNIQUE(scope_id, event_id),
                    UNIQUE(scope_id, idempotency_key)
                );
                CREATE TABLE IF NOT EXISTS journal_receipts (
                    scope_id TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    event_id TEXT NOT NULL,
                    previous_digest TEXT,
                    event_digest TEXT NOT NULL,
                    idempotency_key TEXT,
                    receipt_json TEXT NOT NULL,
                    PRIMARY KEY(scope_id, position),
                    UNIQUE(scope_id, event_id),
                    UNIQUE(scope_id, idempotency_key),
                    FOREIGN KEY(scope_id, position) REFERENCES journal_events(scope_id, position)
                );
                CREATE TRIGGER IF NOT EXISTS journal_events_no_update
                BEFORE UPDATE ON journal_events BEGIN
                    SELECT RAISE(ABORT, 'journal events are immutable');
                END;
                CREATE TRIGGER IF NOT EXISTS journal_events_no_delete
                BEFORE DELETE ON journal_events BEGIN
                    SELECT RAISE(ABORT, 'journal events are immutable');
                END;
                CREATE TRIGGER IF NOT EXISTS journal_receipts_no_update
                BEFORE UPDATE ON journal_receipts BEGIN
                    SELECT RAISE(ABORT, 'journal receipts are immutable');
                END;
                CREATE TRIGGER IF NOT EXISTS journal_receipts_no_delete
                BEFORE DELETE ON journal_receipts BEGIN
                    SELECT RAISE(ABORT, 'journal receipts are immutable');
                END;
            """)
            row = conn.execute("SELECT value FROM journal_meta WHERE key='schema_version'").fetchone()
            if row is None:
                conn.execute("INSERT INTO journal_meta(key,value) VALUES('schema_version',?)", (SCHEMA_VERSION,))
            elif row["value"] != SCHEMA_VERSION:
                raise JournalError("unsupported", "unsupported journal schema version: " + row["value"])
        finally:
            conn.close()

    def _load_receipt(self, conn, scope_id: str, idempotency_key: str):
        row = conn.execute(
            "SELECT receipt_json FROM journal_receipts WHERE scope_id=? AND idempotency_key=?",
            (scope_id, idempotency_key),
        ).fetchone()
        return json.loads(row["receipt_json"]) if row else None

    def initialize(self, scope_id: str, authority_id: str, authority_revision: str,
                   governance_revision: str) -> dict:
        scope_id = _validate_string(scope_id, "scope_id")
        authority_id = _validate_string(authority_id, "authority_id")
        authority_revision = _validate_string(authority_revision, "authority_revision")
        governance_revision = _validate_string(governance_revision, "governance_revision")
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            existing = conn.execute("SELECT * FROM journal_scopes WHERE scope_id=?", (scope_id,)).fetchone()
            if existing:
                if (existing["authority_id"], existing["authority_revision"], existing["governance_revision"]) != (authority_id, authority_revision, governance_revision):
                    conn.execute("ROLLBACK")
                    raise JournalError("conflict", "journal scope already exists with different genesis authority/governance bindings")
                receipt = conn.execute("SELECT receipt_json FROM journal_receipts WHERE scope_id=? AND position=0", (scope_id,)).fetchone()
                conn.execute("ROLLBACK")
                if not receipt:
                    raise JournalError("unknown", "journal scope exists but its genesis receipt is missing")
                return {"status": "committed", "idempotent": True, "receipt": json.loads(receipt["receipt_json"])}

            created_at = utc_now()
            event_id = "genesis:" + scope_id
            payload = {
                "scopeId": scope_id,
                "initialAuthority": {"id": authority_id, "revision": authority_revision},
                "initialGovernanceRevision": governance_revision,
            }
            payload_digest = digest_json(payload)
            genesis_request_digest = digest_json({
                "scopeId": scope_id,
                "initialAuthority": {"id": authority_id, "revision": authority_revision},
                "initialGovernanceRevision": governance_revision,
            })
            envelope = {
                "schemaVersion": SCHEMA_VERSION,
                "canonicalization": CANONICALIZATION_ID,
                "scopeId": scope_id,
                "position": 0,
                "eventId": event_id,
                "eventType": GENESIS_EVENT_TYPE,
                "eventSchemaVersion": SCHEMA_VERSION,
                "previousDigest": None,
                "expectedHead": None,
                "payload": payload,
                "payloadDigest": payload_digest,
                "actorId": authority_id,
                "requestDigest": genesis_request_digest,
                "idempotencyKey": None,
                "createdAt": created_at,
            }
            event_digest = digest_json(envelope)
            envelope["eventDigest"] = event_digest
            envelope_json = canonical_json_bytes(envelope).decode("utf-8")
            receipt = _receipt_object(scope_id, 0, event_id, None, event_digest, None, created_at)
            receipt_json = canonical_json_bytes(receipt).decode("utf-8")

            conn.execute(
                "INSERT INTO journal_scopes(scope_id,authority_id,authority_revision,governance_revision,genesis_event_id,head_position,head_digest,created_at) VALUES(?,?,?,?,?,?,?,?)",
                (scope_id, authority_id, authority_revision, governance_revision, event_id, -1, None, created_at),
            )
            conn.execute(
                "INSERT INTO journal_events(scope_id,position,event_id,event_type,schema_version,previous_digest,payload_digest,request_digest,idempotency_key,envelope_json,event_digest) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (scope_id, 0, event_id, GENESIS_EVENT_TYPE, SCHEMA_VERSION, None, payload_digest, genesis_request_digest, None, envelope_json, event_digest),
            )
            conn.execute(
                "INSERT INTO journal_receipts(scope_id,position,event_id,previous_digest,event_digest,idempotency_key,receipt_json) VALUES(?,?,?,?,?,?,?)",
                (scope_id, 0, event_id, None, event_digest, None, receipt_json),
            )
            conn.execute("UPDATE journal_scopes SET head_position=0, head_digest=? WHERE scope_id=?", (event_digest, scope_id))
            conn.execute("COMMIT")
            return {"status": "committed", "idempotent": False, "receipt": receipt}
        except sqlite3.IntegrityError as exc:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise JournalError("conflict", "journal genesis conflict: " + str(exc)) from exc
        except sqlite3.Error as exc:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise JournalError("unknown", "journal genesis outcome is uncertain: " + str(exc)) from exc
        finally:
            conn.close()

    def head(self, scope_id: str) -> dict:
        scope_id = _validate_string(scope_id, "scope_id")
        conn = self._connect()
        try:
            row = conn.execute("SELECT head_position,head_digest FROM journal_scopes WHERE scope_id=?", (scope_id,)).fetchone()
            if row is None:
                raise JournalError("unknown", "journal scope has no explicit genesis")
            if row["head_position"] < 0 or not row["head_digest"]:
                raise JournalError("unknown", "journal scope has no committed genesis")
            return {"scopeId": scope_id, "position": row["head_position"], "digest": row["head_digest"]}
        finally:
            conn.close()

    def receipt(self, scope_id: str, idempotency_key: str) -> dict | None:
        scope_id = _validate_string(scope_id, "scope_id")
        idempotency_key = _validate_string(idempotency_key, "idempotency_key")
        conn = self._connect()
        try:
            return self._load_receipt(conn, scope_id, idempotency_key)
        finally:
            conn.close()

    def append(self, scope_id: str, expected_position: int, expected_digest: str,
               event_id: str, event_type: str, schema_version: str,
               payload: Any, idempotency_key: str, actor_id: str) -> dict:
        scope_id = _validate_string(scope_id, "scope_id")
        expected_digest = _validate_digest(expected_digest, "expected_digest")
        event_id = _validate_string(event_id, "event_id")
        event_type = _validate_string(event_type, "event_type")
        schema_version = _validate_string(schema_version, "schema_version")
        idempotency_key = _validate_string(idempotency_key, "idempotency_key")
        actor_id = _validate_string(actor_id, "actor_id")
        if not isinstance(expected_position, int) or isinstance(expected_position, bool) or expected_position < 0 or expected_position >= MAX_SAFE_INTEGER:
            raise JournalError("malformed", "expected_position must be a non-negative safe integer below the maximum")
        payload_bytes = canonical_json_bytes(payload)
        payload_digest = sha256(payload_bytes)
        request = {
            "scopeId": scope_id,
            "expectedHead": {"position": expected_position, "digest": expected_digest},
            "eventId": event_id,
            "eventType": event_type,
            "eventSchemaVersion": schema_version,
            "payload": payload,
            "actorId": actor_id,
            "idempotencyKey": idempotency_key,
        }
        request_digest = digest_json(request)
        conn = self._connect()
        try:
            try:
                conn.execute("BEGIN IMMEDIATE")
            except sqlite3.OperationalError as exc:
                return {"status": "unknown", "reason": "could not acquire serialized writer: " + str(exc)}
            scope = conn.execute("SELECT * FROM journal_scopes WHERE scope_id=?", (scope_id,)).fetchone()
            if scope is None or scope["head_position"] < 0 or not scope["head_digest"]:
                conn.execute("ROLLBACK")
                return {"status": "unknown", "reason": "journal scope has no explicit committed genesis"}
            existing = conn.execute(
                "SELECT e.request_digest,r.receipt_json FROM journal_events e JOIN journal_receipts r USING(scope_id,position) WHERE e.scope_id=? AND e.idempotency_key=?",
                (scope_id, idempotency_key),
            ).fetchone()
            if existing:
                conn.execute("ROLLBACK")
                if existing["request_digest"] == request_digest:
                    return {"status": "committed", "idempotent": True, "receipt": json.loads(existing["receipt_json"])}
                return {"status": "conflict", "reason": "idempotency key was already used for a different request"}
            if scope["head_position"] != expected_position or scope["head_digest"] != expected_digest:
                current = {"position": scope["head_position"], "digest": scope["head_digest"]}
                conn.execute("ROLLBACK")
                return {"status": "stale", "currentHead": current, "reason": "expected head does not match the current journal head"}
            duplicate_event = conn.execute("SELECT 1 FROM journal_events WHERE scope_id=? AND event_id=?", (scope_id, event_id)).fetchone()
            if duplicate_event:
                conn.execute("ROLLBACK")
                return {"status": "conflict", "reason": "event_id is already present in this journal scope"}

            position = expected_position + 1
            previous_digest = expected_digest
            created_at = utc_now()
            envelope = {
                "schemaVersion": SCHEMA_VERSION,
                "scopeId": scope_id,
                "position": position,
                "eventId": event_id,
                "eventType": event_type,
                "eventSchemaVersion": schema_version,
                "previousDigest": previous_digest,
                "expectedHead": {"position": expected_position, "digest": expected_digest},
                "payload": payload,
                "payloadDigest": payload_digest,
                "actorId": actor_id,
                "idempotencyKey": idempotency_key,
                "requestDigest": request_digest,
                "createdAt": created_at,
            }
            event_digest = digest_json(envelope)
            envelope["eventDigest"] = event_digest
            envelope_json = canonical_json_bytes(envelope).decode("utf-8")
            committed_at = utc_now()
            receipt = _receipt_object(scope_id, position, event_id, previous_digest, event_digest, idempotency_key, committed_at)
            receipt_json = canonical_json_bytes(receipt).decode("utf-8")
            conn.execute(
                "INSERT INTO journal_events(scope_id,position,event_id,event_type,schema_version,previous_digest,payload_digest,request_digest,idempotency_key,envelope_json,event_digest) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (scope_id, position, event_id, event_type, schema_version, previous_digest, payload_digest, request_digest, idempotency_key, envelope_json, event_digest),
            )
            conn.execute(
                "INSERT INTO journal_receipts(scope_id,position,event_id,previous_digest,event_digest,idempotency_key,receipt_json) VALUES(?,?,?,?,?,?,?)",
                (scope_id, position, event_id, previous_digest, event_digest, idempotency_key, receipt_json),
            )
            conn.execute("UPDATE journal_scopes SET head_position=?,head_digest=? WHERE scope_id=?", (position, event_digest, scope_id))
            try:
                conn.execute("COMMIT")
            except sqlite3.Error as exc:
                try:
                    conn.execute("ROLLBACK")
                except sqlite3.Error:
                    pass
                try:
                    recovered = self.receipt(scope_id, idempotency_key)
                except JournalError:
                    recovered = None
                if recovered and recovered.get("eventDigest") == event_digest:
                    return {"status": "committed", "idempotent": True, "receipt": recovered}
                return {"status": "unknown", "reason": "commit outcome is ambiguous; retry with the same idempotency key: " + str(exc)}
            return {"status": "committed", "idempotent": False, "receipt": receipt}
        except sqlite3.IntegrityError as exc:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            return {"status": "conflict", "reason": "journal uniqueness/constraint conflict: " + str(exc)}
        except sqlite3.Error as exc:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            return {"status": "unknown", "reason": "journal append outcome is uncertain: " + str(exc)}
        finally:
            conn.close()

    def verify(self, scope_id: str) -> dict:
        scope_id = _validate_string(scope_id, "scope_id")
        conn = self._connect()
        errors = []
        try:
            conn.execute("BEGIN")
            scope = conn.execute("SELECT * FROM journal_scopes WHERE scope_id=?", (scope_id,)).fetchone()
            if scope is None:
                conn.execute("ROLLBACK")
                return {"status": "invalid", "scopeId": scope_id, "errors": ["journal scope has no explicit genesis"]}
            rows = conn.execute("SELECT * FROM journal_events WHERE scope_id=? ORDER BY position", (scope_id,)).fetchall()
            receipts = conn.execute("SELECT * FROM journal_receipts WHERE scope_id=? ORDER BY position", (scope_id,)).fetchall()
            if not rows:
                errors.append("journal has no genesis event")
            previous = None
            for expected_position, row in enumerate(rows):
                if row["position"] != expected_position:
                    errors.append("non-contiguous event position at " + str(row["position"]))
                try:
                    envelope = json.loads(row["envelope_json"], object_pairs_hook=_reject_duplicate_pairs)
                    if not isinstance(envelope, dict):
                        raise JournalError("malformed", "event envelope must be a JSON object")
                    if canonical_json_bytes(envelope).decode("utf-8") != row["envelope_json"]:
                        errors.append("event envelope is not canonically serialized at position " + str(row["position"]))
                    if envelope.get("canonicalization") != CANONICALIZATION_ID:
                        errors.append("unsupported event canonicalization profile at position " + str(row["position"]))
                    if envelope.get("scopeId") != scope_id or envelope.get("position") != row["position"]:
                        errors.append("event scope/position mismatch at position " + str(row["position"]))
                    if envelope.get("previousDigest") != previous or row["previous_digest"] != previous:
                        errors.append("previous digest mismatch at position " + str(row["position"]))
                    if expected_position > 0:
                        expected_head = envelope.get("expectedHead")
                        if not isinstance(expected_head, dict) or expected_head.get("position") != expected_position - 1 or expected_head.get("digest") != previous:
                            errors.append("expected-head binding mismatch at position " + str(row["position"]))
                    elif envelope.get("expectedHead") is not None:
                        errors.append("genesis event must not claim an expected prior head")
                    if digest_json(envelope.get("payload")) != envelope.get("payloadDigest") or envelope.get("payloadDigest") != row["payload_digest"]:
                        errors.append("payload digest mismatch at position " + str(row["position"]))
                    computed = digest_json(_without(envelope, "eventDigest"))
                    if computed != envelope.get("eventDigest") or computed != row["event_digest"]:
                        errors.append("event digest mismatch at position " + str(row["position"]))
                    if (envelope.get("eventId") != row["event_id"]
                            or envelope.get("eventType") != row["event_type"]
                            or envelope.get("eventSchemaVersion") != row["schema_version"]
                            or envelope.get("idempotencyKey") != row["idempotency_key"]
                            or envelope.get("requestDigest") != row["request_digest"]):
                        errors.append("event columns do not match envelope at position " + str(row["position"]))
                    if expected_position == 0:
                        payload = envelope.get("payload")
                        authority = payload.get("initialAuthority", {}) if isinstance(payload, dict) else {}
                        if (envelope.get("eventType") != GENESIS_EVENT_TYPE
                                or row["event_id"] != scope["genesis_event_id"]
                                or payload.get("scopeId") != scope_id
                                or authority.get("id") != scope["authority_id"]
                                or authority.get("revision") != scope["authority_revision"]
                                or payload.get("initialGovernanceRevision") != scope["governance_revision"]):
                            errors.append("genesis payload does not match the journal scope authority/governance bindings")
                    previous = row["event_digest"]
                except (ValueError, JournalError, TypeError, AttributeError) as exc:
                    errors.append("malformed event at position " + str(row["position"]) + ": " + str(exc))
            receipt_by_position = {r["position"]: r for r in receipts}
            if len(receipts) != len(rows):
                errors.append("event/receipt count mismatch")
            for row in rows:
                receipt_row = receipt_by_position.get(row["position"])
                if receipt_row is None:
                    errors.append("missing receipt at position " + str(row["position"]))
                    continue
                try:
                    receipt = json.loads(receipt_row["receipt_json"], object_pairs_hook=_reject_duplicate_pairs)
                    if not isinstance(receipt, dict):
                        raise JournalError("malformed", "receipt must be a JSON object")
                    if receipt.get("canonicalization") != CANONICALIZATION_ID:
                        errors.append("unsupported receipt canonicalization profile at position " + str(row["position"]))
                    if canonical_json_bytes(receipt).decode("utf-8") != receipt_row["receipt_json"]:
                        errors.append("receipt is not canonically serialized at position " + str(row["position"]))
                    computed = digest_json(_without(receipt, "receiptDigest"))
                    if computed != receipt.get("receiptDigest"):
                        errors.append("receipt digest mismatch at position " + str(row["position"]))
                    receipt_columns = {
                        "scopeId": receipt_row["scope_id"],
                        "position": receipt_row["position"],
                        "eventId": receipt_row["event_id"],
                        "eventDigest": receipt_row["event_digest"],
                        "previousDigest": receipt_row["previous_digest"],
                        "idempotencyKey": receipt_row["idempotency_key"],
                    }
                    for key, expected in (("scopeId", scope_id), ("position", row["position"]),
                                          ("eventId", row["event_id"]), ("eventDigest", row["event_digest"]),
                                          ("previousDigest", row["previous_digest"]), ("idempotencyKey", row["idempotency_key"])):
                        if receipt.get(key) != expected or receipt_columns[key] != expected:
                            errors.append("receipt " + key + " mismatch at position " + str(row["position"]))
                except (ValueError, JournalError, TypeError, AttributeError) as exc:
                    errors.append("malformed receipt at position " + str(row["position"]) + ": " + str(exc))
            if rows:
                last = rows[-1]
                if scope["head_position"] != last["position"] or scope["head_digest"] != last["event_digest"]:
                    errors.append("scope head projection does not match the last event")
                first = rows[0]
                if first["position"] != 0 or first["event_type"] != GENESIS_EVENT_TYPE or first["previous_digest"] is not None:
                    errors.append("position zero is not a valid genesis event")
            conn.execute("COMMIT")
            if errors:
                return {"status": "invalid", "scopeId": scope_id, "errors": errors}
            return {"status": "valid", "scopeId": scope_id, "eventCount": len(rows),
                    "head": {"position": scope["head_position"], "digest": scope["head_digest"]}}
        except sqlite3.Error as exc:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            return {"status": "unknown", "scopeId": scope_id, "errors": ["journal verification could not complete: " + str(exc)]}
        finally:
            conn.close()


def _main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Local append-only GovCheck journal (SQLite, standard library only).")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="explicitly create a journal scope and genesis receipt")
    init.add_argument("--db", required=True)
    init.add_argument("--scope-id", required=True)
    init.add_argument("--authority-id", required=True)
    init.add_argument("--authority-revision", required=True)
    init.add_argument("--governance-revision", required=True)
    append = sub.add_parser("append", help="append one event with compare-and-append and idempotency")
    append.add_argument("--db", required=True)
    append.add_argument("--scope-id", required=True)
    append.add_argument("--expected-position", required=True, type=int)
    append.add_argument("--expected-digest", required=True)
    append.add_argument("--event-id", required=True)
    append.add_argument("--event-type", required=True)
    append.add_argument("--schema-version", default=SCHEMA_VERSION)
    append.add_argument("--payload-file", required=True)
    append.add_argument("--idempotency-key", required=True)
    append.add_argument("--actor-id", required=True)
    head = sub.add_parser("head", help="read the current journal head")
    head.add_argument("--db", required=True)
    head.add_argument("--scope-id", required=True)
    verify = sub.add_parser("verify", help="verify the complete event and receipt chain")
    verify.add_argument("--db", required=True)
    verify.add_argument("--scope-id", required=True)
    receipt = sub.add_parser("receipt", help="recover a durable receipt by idempotency key")
    receipt.add_argument("--db", required=True)
    receipt.add_argument("--scope-id", required=True)
    receipt.add_argument("--idempotency-key", required=True)
    args = parser.parse_args(argv)
    try:
        journal = Journal(args.db)
        if args.command == "init":
            result = journal.initialize(args.scope_id, args.authority_id, args.authority_revision, args.governance_revision)
        elif args.command == "append":
            payload = load_json(args.payload_file)
            result = journal.append(args.scope_id, args.expected_position, args.expected_digest,
                                    args.event_id, args.event_type, args.schema_version,
                                    payload, args.idempotency_key, args.actor_id)
        elif args.command == "head":
            result = journal.head(args.scope_id)
        elif args.command == "verify":
            result = journal.verify(args.scope_id)
        else:
            result = journal.receipt(args.scope_id, args.idempotency_key)
            if result is None:
                result = {"status": "unknown", "reason": "no receipt for this idempotency key"}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        status = result.get("status")
        if status in {"stale", "conflict", "unknown", "invalid"}:
            return 2
        return 0
    except JournalError as exc:
        print(json.dumps({"status": exc.kind, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except (OSError, sqlite3.Error) as exc:
        print(json.dumps({"status": "unknown", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(_main())
