import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ingest-sacm-metamodel.py"
SPEC = importlib.util.spec_from_file_location("ingest_sacm_metamodel", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SacmNativeIngestionTests(unittest.TestCase):
    def test_captures_exact_source_bytes_and_structural_events(self):
        source = (
            b'<?xml version="1.0" encoding="UTF-8"?>\n'
            b'<xmi:XMI xmlns:xmi="urn:xmi" xmlns:s="urn:sacm" version="2.4">'
            b'<!-- retained comment -->'
            b'<s:Claim xmi:id="claim-1" z="last"><s:value><![CDATA[alpha < beta]]></s:value>'
            b'<?review keep this?>&#38;</s:Claim></xmi:XMI>\n'
        )
        digest = MODULE.sha256(source)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_path = root / "source.xml"
            output = root / "out"
            source_path.write_bytes(source)
            manifest = MODULE.ingest(
                source_path, output, expected_sha256=digest,
                retrieved_at="2026-11-13T00:00:00Z"
            )
            self.assertEqual((output / "source.xml").read_bytes(), source)
            self.assertEqual(manifest["source"]["actualSha256"], digest)
            self.assertTrue(manifest["capture"]["rawBytesPreserved"])
            self.assertEqual(manifest["semanticMappings"], [])
            index = json.loads((output / "index.json").read_text(encoding="utf-8"))
            kinds = [event["kind"] for event in index["events"]]
            self.assertIn("comment", kinds)
            self.assertIn("processingInstruction", kinds)
            self.assertIn("startCdata", kinds)
            self.assertIn("endCdata", kinds)
            claim = next(e for e in index["events"]
                         if e["kind"] == "startElement" and e["name"] == "s:Claim")
            self.assertEqual(claim["attributes"], [["xmi:id", "claim-1"], ["z", "last"]])

    def test_rejects_digest_mismatch_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.xml"
            output = root / "out"
            source.write_bytes(b"<root/>")
            with self.assertRaisesRegex(MODULE.IngestionError, "SHA-256 mismatch"):
                MODULE.ingest(source, output, expected_sha256="0" * 64)
            self.assertFalse(output.exists())

    def test_rejects_malformed_xml(self):
        with self.assertRaises(MODULE.IngestionError):
            MODULE.build_index(b"<root><broken></root>")

    def test_rejects_external_doctype(self):
        source = b'<!DOCTYPE root SYSTEM "https://example.invalid/external.dtd"><root/>'
        with self.assertRaisesRegex(MODULE.IngestionError, "External DTDs"):
            MODULE.build_index(source)

    def test_reports_source_only_not_a_semantic_mapping(self):
        index = MODULE.build_index(b'<s:Model xmlns:s="urn:sacm"><s:Claim/></s:Model>')
        self.assertIn("not a SACM metamodel interpreter", index["interpretationBoundary"])


if __name__ == "__main__":
    unittest.main()
