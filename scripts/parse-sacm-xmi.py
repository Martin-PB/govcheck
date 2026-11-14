#!/usr/bin/env python3
"""Build a loss-aware structural inventory of the pinned OMG SACM XMI source.

This parser inventories UML/XMI constructs and reference edges, and applies a
narrow, version-pinned UML 2.5 interpretation of multiplicity bounds. It does
not implement full UML/MOF semantics, evaluate OCL, validate SACM conformance,
or map SACM to GovCheck. The original source bytes remain authoritative.
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



def interpret_multiplicity_bound(raw: dict[str, Any] | None, side: str) -> dict[str, Any]:
    """Interpret only the UML 2.5 literal/default cases used by the pinned SACM XMI.

    UML 2.5 §7.8.8.7 defines the lowerBound()/upperBound() fallback as 1
    when the corresponding ValueSpecification is absent or has no value.
    UML 2.5 §8.6.9.4 gives LiteralInteger.value and
    §8.6.14.4 gives LiteralUnlimitedNatural.value a metamodel default of 0.
    Unsupported expressions remain unresolved; no evaluator is implied.
    """
    if side not in {"lower", "upper"}:
        raise ValueError(f"Unknown multiplicity bound side: {side}")
    fallback_rule = (
        "UML 2.5 §7.8.8.7 MultiplicityElement.lowerBound() fallback"
        if side == "lower"
        else "UML 2.5 §7.8.8.7 MultiplicityElement.upperBound() fallback"
    )
    if raw is None:
        return {"value": 1, "kind": "finite", "status": "multiplicity-element-fallback", "rule": fallback_rule}
    xmi_type = raw.get("xmiType")
    value = raw.get("value")
    source_id = raw.get("elementId")
    if xmi_type == "uml:LiteralNull":
        return {"value": 1, "kind": "finite", "status": "null-value-fallback", "rule": fallback_rule, "sourceElementId": source_id}
    expected_type = "uml:LiteralInteger" if side == "lower" else "uml:LiteralUnlimitedNatural"
    if xmi_type != expected_type:
        return {"value": None, "kind": "unknown", "status": "unresolved-value-specification", "rule": None, "sourceElementId": source_id}
    if side == "upper" and value == "*":
        return {"value": "*", "kind": "unlimited", "status": "explicit-unlimited", "rule": "explicit UML 2.5 UnlimitedNatural literal", "sourceElementId": source_id}
    if value is None:
        default_rule = (
            "UML 2.5 §8.6.9.4 LiteralInteger.value default = 0"
            if side == "lower"
            else "UML 2.5 §8.6.14.4 LiteralUnlimitedNatural.value default = 0"
        )
        return {"value": 0, "kind": "finite", "status": "literal-default", "rule": default_rule, "sourceElementId": source_id}
    try:
        number = int(value)
    except (TypeError, ValueError):
        return {"value": None, "kind": "unknown", "status": "invalid-literal-value", "rule": None, "sourceElementId": source_id}
    if number < 0:
        return {"value": None, "kind": "unknown", "status": "invalid-negative-bound", "rule": None, "sourceElementId": source_id}
    return {"value": number, "kind": "finite", "status": "explicit-literal", "rule": "explicit UML literal value", "sourceElementId": source_id}


def interpret_multiplicity(lower: dict[str, Any] | None, upper: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "standard": "OMG UML 2.5",
        "lower": interpret_multiplicity_bound(lower, "lower"),
        "upper": interpret_multiplicity_bound(upper, "upper"),
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
            lower = value_child(e, "lowerValue")
            upper = value_child(e, "upperValue")
            record["propertyShape"] = {
                "typeRef": e.get("type"),
                "associationRef": e.get("association"),
                "lower": lower,
                "upper": upper,
                "effectiveMultiplicity": interpret_multiplicity(lower, upper),
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
        "inventoryFormat": "govcheck.sacm-xmi-structural-inventory/v2",
        "generator": {"path": "scripts/parse-sacm-xmi.py", "implementation": "Python standard-library ElementTree", "version": "2"},
        "source": {
            "authority": "Object Management Group (OMG)",
            "specification": "SACM 2.4 Beta 1",
            "fileId": SOURCE_ID,
            "revision": SOURCE_REVISION,
            "nativeFormat": "OMG XMI 20131001 / UML 20131001 export",
            "umlSemanticBasis": {"specification": "OMG UML 2.5", "document": "formal/2015-03-01", "machineReadableFileId": "ptc/13-08-17"},
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
            "This is a source-revision-bound structural inventory of XMI/UML elements and explicit references, "
            "with a narrowly scoped UML 2.5 interpretation of MultiplicityElement bounds for absent bounds, "
            "LiteralInteger, LiteralUnlimitedNatural and LiteralNull. It does not implement full UML/MOF semantics, "
            "evaluate OCL or arbitrary ValueSpecifications, validate SACM conformance, resolve external UML metamodel "
            "imports, establish parser refinement, or map SACM to GovCheck. Unknown constructs remain represented "
            "in the element records and authoritative raw XML."
        ),
    }


def build_summary(inventory: dict[str, Any]) -> dict[str, Any]:
    elements = inventory["elements"]
    enumerations = []
    by_id = {e["id"]: e for e in elements}
    properties = inventory["semanticIndex"]["properties"]
    bound_status = {"lower": Counter(), "upper": Counter()}
    for prop in properties:
        effective = prop.get("effectiveMultiplicity", {})
        for side in ("lower", "upper"):
            bound_status[side][effective.get(side, {}).get("status", "missing")] += 1
    selected_keys = {
        ("Claim", "value"), ("Claim", "whole"), ("Claim", "subject"),
        ("SACMElement", "abstraction"), ("AssertedRelationship", "isCounter"),
        ("AssertedEvidence", "evidence"), ("Assertion", "assertionDeclarationRule"),
    }
    selected_properties = []
    for prop in properties:
        owner = by_id.get(prop.get("ownerId"), {})
        key = (owner.get("name"), prop.get("name"))
        if key not in selected_keys:
            continue
        type_ref = prop.get("typeRef")
        if type_ref and type_ref in by_id:
            type_info = {"kind": "internal-xmi-id",
                         "targetName": by_id[type_ref].get("name"),
                         "targetXmiType": by_id[type_ref].get("xmiType")}
        else:
            href = next((edge.get("value") for edge in inventory["referenceEdges"]
                         if edge.get("sourceId") == prop.get("id")
                         and edge.get("attribute") == "href"), None)
            type_info = {"kind": "external-href", "href": href} if href else {"kind": "not-resolved"}
        effective = prop.get("effectiveMultiplicity", {})
        compact_effective = {
            "standard": effective.get("standard"),
            "lower": {k: v for k, v in effective.get("lower", {}).items() if k != "sourceElementId"},
            "upper": {k: v for k, v in effective.get("upper", {}).items() if k != "sourceElementId"},
        }
        selected_properties.append({
            "owner": owner.get("name"), "property": prop.get("name"),
            "type": type_info, "effectiveMultiplicity": compact_effective,
        })
    selected_properties.sort(key=lambda x: (x["owner"] or "", x["property"] or ""))
    multiplicity_semantics = {
        "standard": "OMG UML 2.5",
        "namespace": "http://www.omg.org/spec/UML/20131001",
        "normativeDocument": "formal/2015-03-01",
        "machineReadableFileId": "ptc/13-08-17",
        "rules": [
            "§7.8.8.7: absent lowerValue/upperValue falls back to 1",
            "§8.2.2: LiteralInteger.value defaults to 0",
            "§8.2.2: LiteralUnlimitedNatural.value defaults to 0",
            "unsupported or non-literal ValueSpecifications remain unresolved",
        ],
        "boundStatusCounts": {side: dict(sorted(counts.items())) for side, counts in bound_status.items()},
        "selectedProperties": selected_properties,
    }
    for enum in [e for e in elements if e.get("xmiType") == "uml:Enumeration"]:
        literals = [e.get("name") for e in elements
                    if e.get("ownerId") == enum["id"] and e.get("xmiType") == "uml:EnumerationLiteral"]
        enumerations.append({"name": enum.get("name"),
                             "qualifiedName": "/".join(enum["containmentPath"]), "literals": literals})
    return {
        "summaryFormat": "govcheck.sacm-xmi-structural-inventory-summary/v2",
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
        "multiplicitySemantics": multiplicity_semantics,
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
