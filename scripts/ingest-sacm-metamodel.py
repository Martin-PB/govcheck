#!/usr/bin/env python3
"""Capture and structurally index the pinned OMG SACM 2.4 Beta 1 metamodel XML.

The original bytes are the authoritative imported source. The event index is a
derived, non-normalizing view: it never replaces or rewrites the source payload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.parsers.expat as expat
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SOURCE_URL = "https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml"
SOURCE_FILE_ID = "ptc/26-05-28"
SOURCE_REVISION = "2026-05-04"
EXPECTED_SHA256 = "0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830"
MAX_SOURCE_BYTES = 32 * 1024 * 1024


class IngestionError(ValueError):
    """Raised when source bytes cannot safely be captured and indexed."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_index(data: bytes) -> dict[str, Any]:
    if not data:
        raise IngestionError("Source XML is empty.")
    if len(data) > MAX_SOURCE_BYTES:
        raise IngestionError(f"Source exceeds the {MAX_SOURCE_BYTES}-byte safety limit.")

    events: list[dict[str, Any]] = []
    element_names: Counter[str] = Counter()
    attribute_names: Counter[str] = Counter()
    stack: list[str] = []
    root_names: list[str] = []
    max_depth = 0
    text_bytes = 0

    parser = expat.ParserCreate()
    parser.ordered_attributes = True
    parser.specified_attributes = True

    def location(kind: str, **values: Any) -> None:
        events.append({
            "kind": kind,
            "byteIndex": parser.CurrentByteIndex,
            "line": parser.CurrentLineNumber,
            "column": parser.CurrentColumnNumber,
            **values,
        })

    def start(name: str, attrs: list[str]) -> None:
        nonlocal max_depth
        pairs = [[attrs[i], attrs[i + 1]] for i in range(0, len(attrs), 2)]
        stack.append(name)
        element_names[name] += 1
        for key, _ in pairs:
            attribute_names[key] += 1
        max_depth = max(max_depth, len(stack))
        if len(stack) == 1:
            root_names.append(name)
        location("startElement", name=name, attributes=pairs, depth=len(stack))

    def end(name: str) -> None:
        if not stack or stack[-1] != name:
            raise IngestionError(f"Parser stack mismatch at element {name!r}.")
        location("endElement", name=name, depth=len(stack))
        stack.pop()

    def characters(value: str) -> None:
        nonlocal text_bytes
        if value:
            text_bytes += len(value.encode("utf-8"))
            location("characters", value=value)

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = characters
    parser.CommentHandler = lambda value: location("comment", value=value)
    parser.ProcessingInstructionHandler = (
        lambda target, value: location("processingInstruction", target=target, value=value)
    )
    parser.StartCdataSectionHandler = lambda: location("startCdata")
    parser.EndCdataSectionHandler = lambda: location("endCdata")

    def doctype(name: str, system_id: str | None, public_id: str | None, has_internal_subset: bool) -> None:
        if system_id or public_id:
            raise IngestionError("External DTDs are not permitted during source ingestion.")
        location("doctype", name=name, hasInternalSubset=bool(has_internal_subset))

    def entity_decl(
        name: str, is_parameter: int, value: str | None, base: str | None,
        system_id: str | None, public_id: str | None, notation_name: str | None
    ) -> None:
        if system_id or public_id:
            raise IngestionError("External entity declarations are not permitted.")
        location("entityDeclaration", name=name, parameter=bool(is_parameter),
                 value=value, notationName=notation_name)

    def external_entity(*_args: Any) -> int:
        raise IngestionError("External entity resolution is disabled.")

    parser.StartDoctypeDeclHandler = doctype
    parser.EntityDeclHandler = entity_decl
    parser.ExternalEntityRefHandler = external_entity
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)

    try:
        parser.Parse(data, True)
    except IngestionError:
        raise
    except expat.ExpatError as exc:
        raise IngestionError(
            f"Malformed or unsupported XML at line {exc.lineno}, column {exc.offset}: {exc}"
        ) from exc

    if stack:
        raise IngestionError("XML ended with unclosed elements.")
    if len(root_names) != 1:
        raise IngestionError(f"Expected exactly one document element, found {len(root_names)}.")

    return {
        "indexFormat": "govcheck.sacm-xml-event-index/v1",
        "parser": {"implementation": "Python xml.parsers.expat", "namespaceProcessing": False,
                   "orderedAttributes": True},
        "documentElement": root_names[0],
        "elementCount": sum(element_names.values()),
        "maxDepth": max_depth,
        "textUtf8ByteCountAfterXMLExpansion": text_bytes,
        "elementNameCounts": dict(sorted(element_names.items())),
        "attributeNameCounts": dict(sorted(attribute_names.items())),
        "events": events,
        "interpretationBoundary": (
            "This is a structural XML event index, not a SACM metamodel interpreter, "
            "conformance validator, GovCheck semantic mapping, or XMI instance importer."
        ),
    }


def ingest(
    source_path: Path,
    output_dir: Path,
    expected_sha256: str = EXPECTED_SHA256,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    data = source_path.read_bytes()
    actual = sha256(data)
    if actual != expected_sha256.lower():
        raise IngestionError(
            f"SHA-256 mismatch: expected {expected_sha256.lower()}, received {actual}."
        )
    index = build_index(data)
    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "source.xml").write_bytes(data)
    (output_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest = {
        "manifestFormat": "govcheck.source-native-import/v1",
        "source": {
            "authority": "Object Management Group (OMG)",
            "specification": "Structured Assurance Case Metamodel (SACM)",
            "version": "2.4 Beta 1",
            "versionStatus": "in-process; informational beta",
            "formalBaseline": "SACM 2.3 (October 2023)",
            "fileId": SOURCE_FILE_ID,
            "revision": SOURCE_REVISION,
            "url": SOURCE_URL,
            "nativeFormat": "application/xml",
            "sourceView": "normativeMetamodelXML",
            "expectedSha256": expected_sha256.lower(),
            "actualSha256": actual,
            "digestVerified": True,
            "retrievedAt": timestamp,
        },
        "capture": {
            "rawPayload": "source.xml",
            "rawPayloadByteLength": len(data),
            "rawPayloadSha256": actual,
            "index": "index.json",
            "indexFormat": index["indexFormat"],
            "rawBytesPreserved": True,
        },
        "semanticMappings": [],
        "unmappedSourcePolicy": "retain-source-native; do-not-infer-equivalence",
        "limitations": [
            "The XML is the OMG machine-readable metamodel, not a SACM assurance-case instance.",
            "The event index preserves XML structure but does not interpret MOF/XMI metaclass semantics.",
            "No mapping to GovCheck domain concepts is asserted by this ingestion.",
            "The PDF specification and metamodel XML are distinct source views with known reported conflicts.",
            "The expected digest is independently rechecked by this run; its initial comparison value is attributed to the R-128 audit."
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--input", required=True, type=Path, help="Downloaded official OMG XML file.")
    cli.add_argument("--output-dir", required=True, type=Path)
    cli.add_argument("--expected-sha256", default=EXPECTED_SHA256)
    cli.add_argument("--retrieved-at", help="Optional fixed UTC timestamp for reproducible manifests.")
    args = cli.parse_args()
    try:
        manifest = ingest(args.input, args.output_dir, args.expected_sha256, args.retrieved_at)
    except (OSError, IngestionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "captured-and-indexed",
        "sourceSha256": manifest["source"]["actualSha256"],
        "bytes": manifest["capture"]["rawPayloadByteLength"],
        "outputDir": str(args.output_dir),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
