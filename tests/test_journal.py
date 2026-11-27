#!/usr/bin/env python3
"""Tests for the local canonical GovCheck journal."""
from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("govcheck_journal", ROOT / "govcheck" / "journal.py")
journal_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(journal_module)


class JournalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / "journal.sqlite"
        self.journal = journal_module.Journal(self.db)
        result = self.journal.initialize("repo:example/project", "principal:root", "authority-r1", "governance-r7")
        self.assertEqual(result["status"], "committed")
        self.genesis = result["receipt"]

    def append(self, **overrides):
        args = {
            "scope_id": "repo:example/project",
            "expected_position": 0,
            "expected_digest": self.genesis["eventDigest"],
            "event_id": "event-1",
            "event_type": "govcheck.decision.recorded",
            "schema_version": "1",
            "payload": {"decision": "accept", "reason": "bounded risk", "rational": "1/3"},
            "idempotency_key": "idem-1",
            "actor_id": "principal:root",
        }
        args.update(overrides)
        return self.journal.append(**args)

    def test_explicit_genesis_and_idempotent_init(self):
        again = self.journal.initialize("repo:example/project", "principal:root", "authority-r1", "governance-r7")
        self.assertTrue(again["idempotent"])
        self.assertEqual(again["receipt"], self.genesis)
        with self.assertRaisesRegex(journal_module.JournalError, "different genesis"):
            self.journal.initialize("repo:example/project", "principal:other", "authority-r1", "governance-r7")

    def test_append_returns_receipt_after_commit_and_verify(self):
        result = self.append()
        self.assertEqual(result["status"], "committed")
        receipt = result["receipt"]
        self.assertEqual(receipt["position"], 1)
        self.assertEqual(receipt["previousDigest"], self.genesis["eventDigest"])
        self.assertEqual(self.journal.head("repo:example/project")["digest"], receipt["eventDigest"])
        self.assertEqual(self.journal.verify("repo:example/project")["status"], "valid")

    def test_idempotent_retry_returns_original_receipt(self):
        first = self.append()
        retry = self.append()
        self.assertEqual(first["receipt"], retry["receipt"])
        self.assertTrue(retry["idempotent"])

    def test_idempotency_key_with_different_request_conflicts(self):
        self.append()
        conflict = self.append(payload={"decision": "reject"}, event_id="event-2")
        self.assertEqual(conflict["status"], "conflict")

    def test_stale_expected_head_does_not_append(self):
        result = self.append(expected_position=9, expected_digest="0" * 64)
        self.assertEqual(result["status"], "stale")
        self.assertEqual(self.journal.head("repo:example/project")["position"], 0)

    def test_missing_genesis_fails_closed(self):
        result = self.journal.append("repo:missing", 0, "0" * 64, "event", "type", "1",
                                     {"x": 1}, "idem", "principal:root")
        self.assertEqual(result["status"], "unknown")

    def test_journal_schemas_are_present_and_versioned(self):
        schemas = ROOT / "govcheck" / "formal" / "schemas"
        event = json.loads((schemas / "journal-event-v1.schema.json").read_text(encoding="utf-8"))
        receipt = json.loads((schemas / "journal-receipt-v1.schema.json").read_text(encoding="utf-8"))
        self.assertIn("canonicalization", event["required"])
        self.assertIn("eventDigest", event["required"])
        self.assertIn("canonicalization", receipt["required"])
        self.assertIn("receiptDigest", receipt["required"])

    def test_invalid_expected_digest_is_rejected(self):
        with self.assertRaisesRegex(journal_module.JournalError, "lowercase SHA-256"):
            self.append(expected_digest="not-a-digest")

    def test_float_is_rejected(self):
        with self.assertRaisesRegex(journal_module.JournalError, "floating-point"):
            self.append(payload={"probability": 0.8})

    def test_large_integer_is_rejected(self):
        with self.assertRaisesRegex(journal_module.JournalError, "safe-integer"):
            journal_module.canonical_json_bytes({"n": 9007199254740992})

    def test_duplicate_json_keys_are_rejected(self):
        path = Path(self.tmp.name) / "duplicate.json"
        path.write_text('{"a":1,"a":2}', encoding="utf-8")
        with self.assertRaisesRegex(journal_module.JournalError, "duplicate JSON"):
            journal_module.load_json(str(path))

    def test_canonical_json_uses_utf16_key_order(self):
        value = {"z": 1, "𐀀": 2, "a": 3}
        canonical = journal_module.canonical_json_bytes(value).decode("utf-8")
        self.assertEqual(canonical, '{"a":3,"z":1,"𐀀":2}')

    def test_event_and_receipt_rows_are_immutable_via_sql(self):
        self.append()
        conn = sqlite3.connect(self.db)
        try:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("UPDATE journal_events SET event_type='tampered' WHERE position=1")
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("DELETE FROM journal_receipts WHERE position=1")
        finally:
            conn.close()

    def test_tampering_is_detected_by_chain_verification(self):
        self.append()
        conn = sqlite3.connect(self.db)
        try:
            conn.execute("DROP TRIGGER journal_events_no_update")
            conn.execute("UPDATE journal_events SET event_digest=? WHERE position=1", ("f" * 64,))
            conn.commit()
        finally:
            conn.close()
        result = self.journal.verify("repo:example/project")
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("event digest mismatch" in e for e in result["errors"]))

    def test_append_fails_closed_when_existing_chain_is_corrupt(self):
        self.append()
        conn = sqlite3.connect(self.db)
        try:
            conn.execute("DROP TRIGGER journal_events_no_update")
            conn.execute("UPDATE journal_events SET event_digest=? WHERE position=1", ("e" * 64,))
            conn.commit()
        finally:
            conn.close()
        head = self.journal.head("repo:example/project")
        result = self.journal.append("repo:example/project", head["position"], head["digest"],
                                     "event-after-corruption", "test.event", "1", {"x": 1},
                                     "idem-after-corruption", "principal:root")
        self.assertEqual(result["status"], "unknown")
        self.assertIn("integrity verification failed", result["reason"])

    def test_receipt_column_tampering_is_detected(self):
        self.append()
        conn = sqlite3.connect(self.db)
        try:
            conn.execute("DROP TRIGGER journal_receipts_no_update")
            conn.execute("UPDATE journal_receipts SET event_digest=? WHERE position=1", ("f" * 64,))
            conn.commit()
        finally:
            conn.close()
        result = self.journal.verify("repo:example/project")
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("receipt eventDigest mismatch" in e for e in result["errors"]))

    def test_uncommitted_transaction_is_rolled_back_on_connection_close(self):
        conn = sqlite3.connect(self.db, isolation_level=None)
        try:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("INSERT INTO journal_meta(key,value) VALUES('crash-fixture','uncommitted')")
        finally:
            conn.close()
        conn = sqlite3.connect(self.db)
        try:
            row = conn.execute("SELECT value FROM journal_meta WHERE key='crash-fixture'").fetchone()
            self.assertIsNone(row)
        finally:
            conn.close()
        self.assertEqual(self.journal.verify("repo:example/project")["status"], "valid")

    def test_retry_after_lost_response_recovers_same_receipt(self):
        first = self.append()
        # Simulate the client losing the response after the database commit.
        recovered = self.append()
        self.assertEqual(first["receipt"]["eventDigest"], recovered["receipt"]["eventDigest"])
        self.assertTrue(recovered["idempotent"])

    def test_concurrent_writers_have_one_winner_and_one_stale_result(self):
        barrier = threading.Barrier(2)
        results = []
        lock = threading.Lock()
        def worker(n):
            barrier.wait()
            result = self.append(event_id="event-" + str(n), idempotency_key="idem-" + str(n))
            with lock:
                results.append(result)
        threads = [threading.Thread(target=worker, args=(n,)) for n in (1, 2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        statuses = sorted(x["status"] for x in results)
        self.assertEqual(statuses, ["committed", "stale"])
        self.assertEqual(self.journal.verify("repo:example/project")["status"], "valid")

    def test_receipt_recovery_by_idempotency_key(self):
        result = self.append()
        receipt = self.journal.receipt("repo:example/project", "idem-1")
        self.assertEqual(receipt, result["receipt"])

    def test_cli_init_append_verify(self):
        db = Path(self.tmp.name) / "cli.sqlite"
        payload = Path(self.tmp.name) / "payload.json"
        payload.write_text('{"kind":"test","result":"pass"}', encoding="utf-8")
        # CLI init is idempotent and prints a genesis receipt.
        code = journal_module._main(["init", "--db", str(db), "--scope-id", "repo:cli",
                                     "--authority-id", "principal:root", "--authority-revision", "a1",
                                     "--governance-revision", "g1"])
        self.assertEqual(code, 0)
        cli_journal = journal_module.Journal(db)
        head = cli_journal.head("repo:cli")
        code = journal_module._main(["append", "--db", str(db), "--scope-id", "repo:cli",
                                     "--expected-position", str(head["position"]), "--expected-digest", head["digest"],
                                     "--event-id", "cli-event", "--event-type", "test.event",
                                     "--payload-file", str(payload), "--idempotency-key", "cli-idem",
                                     "--actor-id", "principal:root"])
        self.assertEqual(code, 0)
        code = journal_module._main(["verify", "--db", str(db), "--scope-id", "repo:cli"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
