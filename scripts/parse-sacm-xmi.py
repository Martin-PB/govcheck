#!/usr/bin/env python3
"""Build a loss-aware structural inventory of the pinned OMG SACM XMI source.

This parser inventories UML/XMI constructs and reference edges. It does not
interpret UML semantics, validate SACM conformance, or map SACM to GovCheck.
The original source bytes remain authoritative and must be retained separately.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
import xml.etree.ElementTree as ET
from collections import Counter
from io import BytesIO
from pathlib import Path
from typing import Any

XMI_NS = "http://www.omg.org/spec/XMI/20131001"
EXPECTED_SHA256 = "0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830"
SOURCE_ID = "ptc/26-05-28"
SOURCE_REVISION = "2026-05-04"
MAX_SOURCE_BYTES = 32 * 1024 * 1024

class InventoryError(ValueError):
    pass


def local_name(expanded: str) -> str:
    return expanded.rsplit("}", 1)[-1]


def namespace(expanded: str) -> str | None:
    return expanded[1:].split("}", 1)[0] if expanded.startswith("{") else None


def is_reference_attribute(expanded: str) -> bool:
    local = local_name(expanded)
    ns = namespace(expanded)
    if local in {"idref", "idrefs"}:
        return ns == XMI_NS
    if local == "href":
        return True
    # xmi:type declares an XML metaclass; only an unqualified UML type attribute
    # is a model reference.
    return local in {"general", "type", "association", "base_Package", "client", "supplier"} and ns is None


def attr_map(element: ET.Element) -> dict[str, str]:
    return {k: v for k, v in sorted(element.attrib.items())}


def inline_node(element: ET.Element) -> dict[str, Any]:
    """Preserve id-less XML nodes; id-bearing nodes are linked by stable XMI id."""
    xid = element.get(f"{{{XMI_NS}}}id")
    if xid:
        return {"elementId": xid, "tag": element.tag, "tail": element.tail}
    return {
        "tag": element.tag,
        "attributes": attr_map(element),
        "attributeOrder": list(element.attrib.keys()),
        "text": element.text,
        "tail": element.tail,
        "children": [inline_node(c) for c in list(element)],
    }


def value_child(element: ET.Element, child_local: str) -> dict[str, Any] | None:
    child = next((c for c in list(element) if local_name(c.tag) == child_local), None)
    if child is None:
        return None
    return {
        "xmiType": child.get(f"{{{XMI_NS}}}type"),
        "value": child.get("value"),
        "elementId": child.get(f"{{{XMI_NS}}}id"),
        "text": child.text,
    }


def build_inventory(data: bytes, expected_sha256: str = EXPECTED_SHA256) -> dict[str, Any]:
    if not data or len(data) > MAX_SOURCE_BYTES:
        raise InventoryError("Source is empty or exceeds the configured safety limit.")
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_sha256.lower():
        raise InventoryError(f"SHA-256 mismatch: expected {expected_sha256.lower()}, received {actual}.")
    if re.search(br"<!\s*(DOCTYPE|ENTITY)\b", data, re.IGNORECASE):
        raise InventoryError("DTD/entity declarations are outside this parser's supported boundary.")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise InventoryError(f"Malformed XMI/XML: {exc}") from exc
    if local_name(root.tag) != "XMI" or namespace(root.tag) != XMI_NS:
        raise InventoryError("Expected an OMG XMI document root.")

    all_elements = list(root.iter())
    ids: dict[str, ET.Element] = {}
    parents: dict[int, ET.Element] = {}
    for parent in all_elements:
        for child in list(parent):
            parents[id(child)] = parent
    max_depth = 0
    for e in all_elements:
        depth = 0
        cur = e
        while id(cur) in parents:
            depth += 1
            cur = parents[id(cur)]
        max_depth = max(max_depth, depth)
    if max_depth > 256:
        raise InventoryError(f"XML nesting depth {max_depth} exceeds the 256-level safety limit.")

    for e in all_elements:
        xid = e.get(f"{{{XMI_NS}}}id")
        if xid:
            if xid in ids:
                raise InventoryError(f"Duplicate xmi:id: {xid}")
            ids[xid] = e

    records = []
    ref_edges = []
    type_counts = Counter()
    containment_counts = Counter()
    namespace_declarations = []
    for event, item in ET.iterparse(BytesIO(data), events=("start-ns",)):
        namespace_declarations.append({"prefix": item[0] or "", "uri": item[1]})

    def owner_and_path(e: ET.Element) -> tuple[str | None, list[str]]:
        ancestors = []
        cur = parents.get(id(e))
        owner = None
        while cur is not None:
            cid = cur.get(f"{{{XMI_NS}}}id")
            if cid and owner is None:
                owner = cid
            name = cur.get("name") or cur.get(f"{{{XMI_NS}}}type") or local_name(cur.tag)
            ancestors.append(name)
            cur = parents.get(id(cur))
        return owner, list(reversed(ancestors))

    for xid, e in ids.items():
        xtype = e.get(f"{{{XMI_NS}}}type")
        owner, path = owner_and_path(e)
        name = e.get("name")
        type_counts[xtype or e.tag] += 1
        containment_path = path + ([name] if name else [xtype or local_name(e.tag)])
        record = {
            "id": xid,
            "xmlTag": e.tag,
            "xmiType": xtype,
            "name": name,
            "ownerId": owner,
            "containmentPath": containment_path,
            "attributes": attr_map(e),
            "attributeOrder": list(e.attrib.keys()),
            "directText": e.text,
            "tail": e.tail,
            "children": [inline_node(c) for c in list(e)],
        }
        if xtype == "uml:Property":
            record["propertyShape"] = {
                "typeRef": e.get("type"),
                "associationRef": e.get("association"),
                "lower": value_child(e, "lowerValue"),
                "upper": value_child(e, "upperValue"),
                "aggregation": e.get("aggregation"),
                "visibility": e.get("visibility"),
                "isDerived": e.get("isDerived"),
                "isReadOnly": e.get("isReadOnly"),
                "isOrdered": e.get("isOrdered"),
                "isUnique": e.get("isUnique"),
            }
        if xtype == "uml:Association":
            record["associationShape"] = {
                "memberEnds": [c.get(f"{{{XMI_NS}}}idref") for c in list(e) if local_name(c.tag) == "memberEnd"],
                "ownedEnds": [c.get(f"{{{XMI_NS}}}id") for c in list(e) if local_name(c.tag) == "ownedEnd"],
            }
        if xtype == "uml:Generalization":
            record["generalizationShape"] = {"generalRef": e.get("general")}
        if xtype == "uml:Constraint":
            spec = next((c for c in list(e) if local_name(c.tag) == "specification"), None)
            record["constraintShape"] = {
                "constrainedElementRefs": [c.get(f"{{{XMI_NS}}}idref") for c in list(e) if local_name(c.tag) == "constrainedElement"],
                "specification": inline_node(spec) if spec is not None else None,
            }
        records.append(record)

        # Record explicit reference-like attributes on this object and its id-less
        # descendants. Nested identified objects own their own references.
        def visit_reference_nodes(node: ET.Element, is_root: bool = False) -> None:
            if not is_root and node.get(f"{{{XMI_NS}}}id"):
                return
            for attr, value in node.attrib.items():
                if not is_reference_attribute(attr):
                    continue
                alocal = local_name(attr)
                vals = value.split() if alocal == "idrefs" else [value]
                for val in vals:
                    target = val.split("#", 1)[-1] if alocal == "href" else val
                    if target in ids:
                        resolution = "internal"
                    elif alocal == "href" or ":" in val or val.startswith("//"):
                        resolution = "external-reference"
                    elif alocal == "type":
                        resolution = "external-type-token"
                    else:
                        resolution = "unresolved-reference"
                    ref_edges.append({
                        "sourceId": xid, "sourceNodeTag": node.tag,
                        "attribute": attr, "value": val,
                        "targetId": target if target in ids else None,
                        "resolution": resolution,
                    })
            for descendant in list(node):
                visit_reference_nodes(descendant)
        visit_reference_nodes(e, True)

    top_level = [inline_node(c) for c in list(root)]

    package_records = [r for r in records if r.get("xmiType") in {"uml:Package", "uml:Profile"}]
    package_summaries = []
    for package in package_records:
        package_id = package["id"]
        direct_children = [r for r in records if r.get("ownerId") == package_id]
        counts = Counter(r.get("xmiType") or r["xmlTag"] for r in direct_children)
        package_summaries.append({
            "id": package_id, "name": package.get("name"),
            "containmentPath": package["containmentPath"],
            "directChildTypeCounts": dict(sorted(counts.items())),
            "directChildElementIds": [r["id"] for r in direct_children],
        })

    classifier_summaries = []
    for classifier in [r for r in records if r.get("xmiType") in {"uml:Class", "uml:Enumeration", "uml:DataType"}]:
        classifier_id = classifier["id"]
        direct = [r for r in records if r.get("ownerId") == classifier_id]
        classifier_summaries.append({
            "id": classifier_id, "name": classifier.get("name"),
            "xmiType": classifier.get("xmiType"),
            "containmentPath": classifier["containmentPath"],
            "ownedPropertyIds": [r["id"] for r in direct if r.get("xmiType") == "uml:Property"],
            "generalizationIds": [r["id"] for r in direct if r.get("xmiType") == "uml:Generalization"],
            "ownedRuleIds": [r["id"] for r in direct if r.get("xmiType") == "uml:Constraint"],
            "enumerationLiteralIds": [r["id"] for r in direct if r.get("xmiType") == "uml:EnumerationLiteral"],
        })

    association_summaries = [
        {"id": r["id"], "containmentPath": r["containmentPath"],
         "memberEndRefs": r.get("associationShape", {}).get("memberEnds", []),
         "ownedEndIds": r.get("associationShape", {}).get("ownedEnds", [])}
        for r in records if r.get("xmiType") == "uml:Association"
    ]
    property_summaries = [
        {"id": r["id"], "name": r.get("name"), "ownerId": r.get("ownerId"),
         "containmentPath": r["containmentPath"], "attributeOrder": r["attributeOrder"],
         **r.get("propertyShape", {})}
        for r in records if r.get("xmiType") == "uml:Property"
    ]
    generalization_summaries = [
        {"id": r["id"], "specificOwnerId": r.get("ownerId"),
         "generalRef": r.get("generalizationShape", {}).get("generalRef"),
         "containmentPath": r["containmentPath"]}
        for r in records if r.get("xmiType") == "uml:Generalization"
    ]
    constraint_summaries = [
        {"id": r["id"], "name": r.get("name"), "ownerId": r.get("ownerId"),
         **r.get("constraintShape", {})}
        for r in records if r.get("xmiType") == "uml:Constraint"
    ]

    for e in all_elements:
        xtype = e.get(f"{{{XMI_NS}}}type")
        if xtype:
            containment_counts[xtype] += 1
    unresolved = [r for r in ref_edges if r["resolution"] == "unresolved-reference"]
    return {
        "inventoryFormat": "govcheck.sacm-xmi-structural-inventory/v1",
        "generator": {"path": "scripts/parse-sacm-xmi.py", "implementation": "Python standard-library ElementTree", "version": "1"},
        "source": {
            "authority": "Object Management Group (OMG)",
            "specification": "SACM 2.4 Beta 1",
            "fileId": SOURCE_ID,
            "revision": SOURCE_REVISION,
            "nativeFormat": "OMG XMI 20131001 / UML 20131001 export",
            "sha256": actual,
            "byteLength": len(data),
            "sourceView": "normativeMetamodelXML",
        },
        "document": {
            "rootTag": root.tag,
            "namespaceDeclarations": namespace_declarations,
            "topLevelNodes": top_level,
            "identifiedElementCount": len(records),
            "identifiedElementIdsUnique": True,
            "maximumElementDepth": max_depth,
        },
        "semanticIndex": {
            "packages": package_summaries,
            "classifiers": classifier_summaries,
            "associations": association_summaries,
            "properties": property_summaries,
            "generalizations": generalization_summaries,
            "constraints": constraint_summaries,
        },
        "summary": {
            "xmiTypeCounts": dict(sorted(type_counts.items())),
            "allXmiTypeCountsIncludingIdless": dict(sorted(containment_counts.items())),
            "referenceEdgeCount": len(ref_edges),
            "resolvedInternalReferenceCount": sum(r["resolution"] == "internal" for r in ref_edges),
            "externalReferenceCount": sum(r["resolution"] in {"external-reference", "external-type-token"} for r in ref_edges),
            "unresolvedReferenceCount": len(unresolved),
        },
        "elements": records,
        "referenceEdges": ref_edges,
        "unresolvedReferences": unresolved,
        "interpretationBoundary": (
            "This is a source-revision-bound structural inventory of XMI/UML elements and explicit references. "
            "It does not implement UML/MOF semantic interpretation, validate SACM conformance, "
            "resolve external UML metamodel imports, establish parser refinement, or map SACM to GovCheck. "
            "Unknown constructs remain represented in the element records and authoritative raw XML."
        ),
    }


def build_summary(inventory: dict[str, Any]) -> dict[str, Any]:
    elements = inventory["elements"]
    enumerations = []
    for enum in [e for e in elements if e.get("xmiType") == "uml:Enumeration"]:
        literals = [e.get("name") for e in elements
                    if e.get("ownerId") == enum["id"] and e.get("xmiType") == "uml:EnumerationLiteral"]
        enumerations.append({"name": enum.get("name"),
                             "qualifiedName": "/".join(enum["containmentPath"]), "literals": literals})
    return {
        "summaryFormat": "govcheck.sacm-xmi-structural-inventory-summary/v1",
        "generator": inventory["generator"],
        "source": inventory["source"],
        "document": {
            "rootTag": inventory["document"]["rootTag"],
            "namespaceDeclarations": inventory["document"]["namespaceDeclarations"],
            "identifiedElementCount": inventory["document"]["identifiedElementCount"],
            "identifiedElementIdsUnique": inventory["document"]["identifiedElementIdsUnique"],
            "maximumElementDepth": inventory["document"]["maximumElementDepth"],
        },
        "counts": inventory["summary"],
        "packages": [
            {"name": p.get("name"), "qualifiedName": "/".join(p["containmentPath"]),
             "directChildTypeCounts": p["directChildTypeCounts"]}
            for p in inventory["semanticIndex"]["packages"]
        ],
        "enumerations": enumerations,
        "interpretationBoundary": inventory["interpretationBoundary"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path, help="Full structural inventory JSON.")
    ap.add_argument("--summary-output", type=Path, help="Optional compact, reviewable inventory summary JSON.")
    ap.add_argument("--expected-sha256", default=EXPECTED_SHA256)
    args = ap.parse_args()
    try:
        inventory = build_inventory(args.input.read_bytes(), args.expected_sha256)
    except (OSError, InventoryError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.summary_output:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        summary = build_summary(inventory)
        args.summary_output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status":"inventoried","identifiedElements":inventory["document"]["identifiedElementCount"],**inventory["summary"],"output":str(args.output),"summaryOutput":str(args.summary_output) if args.summary_output else None},indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
