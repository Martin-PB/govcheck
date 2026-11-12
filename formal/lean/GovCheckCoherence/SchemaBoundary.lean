import GovCheckCoherence.Evidence

namespace GovCheck.Coherence

/-- A schema-level theorem-proving report with no authenticated derivation. -/
def theoremProvingTestimony : EvidenceRecord :=
  ⟨.theoremProving, .testimony, .passed⟩

/-- A candidate epistemic interpretation of the same method/status pair.
This is intentionally not authenticated by a derivation object. -/
def candidateTheoremProofClassification : EvidenceRecord :=
  ⟨.theoremProving, .theoremProof, .passed⟩

end GovCheck.Coherence
