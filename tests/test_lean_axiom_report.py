import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit-lean-axiom-report.py"
SPEC = importlib.util.spec_from_file_location("lean_axiom_report_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class LeanAxiomReportTests(unittest.TestCase):
    def test_sorry_axiom_is_rejected(self):
        report = "'GovCheckCoherence.Reproductions.sorryInjected' depends on axioms: [sorryAx]\n"
        result = MODULE.audit_report(report)
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["findings"][0]["axiom"], "sorryAx")

    def test_unapproved_named_axiom_is_rejected(self):
        report = "'GovCheckCoherence.Reproductions.axiomInjected' depends on axioms: [GovCheckCoherence.Reproductions.injectedFalse]\n"
        result = MODULE.audit_report(report)
        self.assertEqual(result["status"], "rejected")
        self.assertTrue(any("injectedFalse" in item["axiom"] for item in result["findings"]))

    def test_explicitly_allowlisted_axioms_are_accepted(self):
        report = "'GovCheck.Coherence.valid' depends on axioms: [Classical.choice, propext, Quot.sound]\n"
        result = MODULE.audit_report(report, {"Classical.choice", "propext", "Quot.sound"})
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["findings"], [])

    def test_missing_axiom_report_fails_closed(self):
        result = MODULE.audit_report("Lean build succeeded.\n")
        self.assertEqual(result["status"], "rejected")
        self.assertIn("no '#print axioms' declaration report found", result["findings"][0]["reason"])

    def test_parser_handles_multiple_declarations_and_empty_axiom_sets(self):
        report = (
            "'GovCheck.Coherence.clean' depends on axioms: []\n"
            "'GovCheck.Coherence.bad' depends on axioms: [sorryAx]\n"
        )
        parsed = MODULE.parse_axiom_report(report)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["axioms"], [])
        self.assertEqual(parsed[1]["axioms"], ["sorryAx"])


if __name__ == "__main__":
    unittest.main()
