import GovCheckCoherence.Evidence

namespace GovCheck.Coherence

/-- Transport preserves the method class, epistemic kind and result status. -/
theorem transport_preserves_method_class (record : EvidenceRecord) :
    (transport record).methodClass = record.methodClass := by
  rfl

theorem transport_preserves_kind (record : EvidenceRecord) :
    (transport record).kind = record.kind := by
  rfl

theorem transport_preserves_status (record : EvidenceRecord) :
    (transport record).status = record.status := by
  rfl

/-- A passed empirical test remains testimony and cannot become a theorem
proof merely by translation. -/
theorem testimony_cannot_be_promoted_by_transport :
    ¬ admissibleTargetKind .testimony .theoremProof .carried := by
  intro h
  rcases h with h | h
  · exact h rfl
  · rcases h with h | h
    · cases h
    · cases h

/-- A model-checking result cannot become a theorem proof by transport alone. -/
theorem model_checking_cannot_be_promoted_by_transport :
    ¬ admissibleTargetKind .modelCheckingResult .theoremProof .carried := by
  intro h
  rcases h with h | h
  · exact h rfl
  · rcases h with h | h
    · cases h
    · cases h

/-- A theorem-proof record may be carried as such. This does not authenticate
its source proof or establish freshness; those are separate obligations. -/
theorem theorem_proof_may_be_carried :
    admissibleTargetKind .theoremProof .theoremProof .carried := by
  right
  left
  rfl

/-- A new theorem-proof target requires an explicitly identified
kernel-checked derivation. A later refinement must bind the derivation to
exact premises, conclusion, assumptions and kernel identity. -/
theorem new_theorem_proof_requires_kernel_derivation
    (source : EvidenceKind) :
    admissibleTargetKind source .theoremProof .kernelChecked := by
  right
  right
  rfl

theorem passing_testimony_is_not_a_theorem_proof :
    passingTestimony.kind ≠ .theoremProof := by
  decide

theorem theorem_proving_label_alone_does_not_authenticate_proof :
    unverifiedTheoremProvingReport.kind ≠ .theoremProof := by
  decide

end GovCheck.Coherence
