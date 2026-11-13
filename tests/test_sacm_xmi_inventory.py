import importlib.util
import hashlib
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "parse-sacm-xmi.py"
SPEC = importlib.util.spec_from_file_location("parse_sacm_xmi", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

XMI = "http://www.omg.org/spec/XMI/20131001"
UML = "http://www.omg.org/spec/UML/20131001"


def fixture():
    return f'''<?xml version="1.0"?>
<xmi:XMI xmlns:xmi="{XMI}" xmlns:uml="{UML}">
  <uml:Model xmi:type="uml:Model" xmi:id="model" name="M">
    <packagedElement xmi:type="uml:Package" xmi:id="pkg" name="P">
      <packagedElement xmi:type="uml:Class" xmi:id="class-a" name="A">
        <ownedAttribute xmi:type="uml:Property" xmi:id="property-a" name="b" type="class-b">
          <lowerValue xmi:type="uml:LiteralInteger" xmi:id="lower-a" value="0"/>
          <upperValue xmi:type="uml:LiteralUnlimitedNatural" xmi:id="upper-a" value="*"/>
        </ownedAttribute>
        <generalization xmi:type="uml:Generalization" xmi:id="gen-a" general="class-b"/>
      </packagedElement>
      <packagedElement xmi:type="uml:Class" xmi:id="class-b" name="B"/>
      <packagedElement xmi:type="uml:Association" xmi:id="association-a">
        <memberEnd xmi:idref="property-a"/>
      </packagedElement>
      <packagedElement xmi:type="uml:Constraint" xmi:id="constraint-a" name="C">
        <constrainedElement xmi:idref="class-a"/>
        <specification xmi:type="uml:OpaqueExpression" xmi:id="expr-a">
          <language>OCL</language><body>A.b->notEmpty()</body>
        </specification>
      </packagedElement>
    </packagedElement>
  </uml:Model>
</xmi:XMI>'''.encode()


class SacmXmiInventoryTests(unittest.TestCase):
    def inventory(self, data=None):
        data = fixture() if data is None else data
        return MODULE.build_inventory(data, hashlib.sha256(data).hexdigest())

    def test_indexes_uml_constructs_and_internal_references(self):
        result = self.inventory()
        self.assertEqual(result["document"]["identifiedElementCount"], 11)
        counts = result["summary"]["xmiTypeCounts"]
        self.assertEqual(counts["uml:Class"], 2)
        self.assertEqual(counts["uml:Property"], 1)
        self.assertEqual(counts["uml:Association"], 1)
        self.assertEqual(counts["uml:Constraint"], 1)
        self.assertEqual(result["summary"]["unresolvedReferenceCount"], 0)
        prop = next(x for x in result["semanticIndex"]["properties"] if x["id"] == "property-a")
        self.assertEqual(prop["typeRef"], "class-b")
        self.assertEqual(prop["lower"]["value"], "0")
        self.assertEqual(prop["upper"]["value"], "*")
        assoc = result["semanticIndex"]["associations"][0]
        self.assertEqual(assoc["memberEndRefs"], ["property-a"])
        constraint = result["semanticIndex"]["constraints"][0]
        self.assertEqual(constraint["constrainedElementRefs"], ["class-a"])

    def test_preserves_idless_children_and_exporter_documentation(self):
        data = fixture().replace(b'<uml:Model', b'<xmi:documentation xmi:type="xmi:Documentation"><xmi:exporter>Tool</xmi:exporter></xmi:documentation>\n  <uml:Model', 1)
        result = self.inventory(data)
        docs = [x for x in result["document"]["topLevelNodes"] if x.get("tag", "").endswith("documentation")]
        self.assertEqual(len(docs), 1)
        self.assertTrue(any("exporter" in str(node) for node in docs))

    def test_rejects_duplicate_xmi_ids(self):
        data = fixture().replace(b'xmi:id="class-b"', b'xmi:id="class-a"')
        with self.assertRaisesRegex(MODULE.InventoryError, "Duplicate xmi:id"):
            self.inventory(data)

    def test_rejects_unresolved_internal_references(self):
        data = fixture().replace(b'general="class-b"', b'general="missing-class"')
        result = self.inventory(data)
        self.assertEqual(result["summary"]["unresolvedReferenceCount"], 1)
        self.assertEqual(result["unresolvedReferences"][0]["value"], "missing-class")

    def test_summary_is_derived_from_full_inventory(self):
        result = self.inventory()
        summary = MODULE.build_summary(result)
        self.assertEqual(summary["summaryFormat"], "govcheck.sacm-xmi-structural-inventory-summary/v1")
        self.assertEqual(summary["document"]["identifiedElementCount"], 11)
        self.assertEqual(summary["counts"]["resolvedInternalReferenceCount"], 4)
        self.assertEqual(summary["packages"][0]["name"], "P")

    def test_rejects_digest_mismatch(self):
        with self.assertRaisesRegex(MODULE.InventoryError, "SHA-256 mismatch"):
            MODULE.build_inventory(fixture(), "0" * 64)

    def test_rejects_dtd_and_malformed_xml(self):
        data = b'<!DOCTYPE xmi:XMI [<!ENTITY e "bad">]><xmi:XMI xmlns:xmi="urn:xmi">&e;</xmi:XMI>'
        with self.assertRaisesRegex(MODULE.InventoryError, "DTD/entity"):
            self.inventory(data)
        with self.assertRaises(MODULE.InventoryError):
            self.inventory(b'<xmi:XMI xmlns:xmi="urn:xmi"><broken></xmi:XMI>')


if __name__ == "__main__":
    unittest.main()
