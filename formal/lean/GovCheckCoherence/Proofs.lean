import GovCheckCoherence.Evidence
import GovCheckCoherence.SchemaBoundary
import GovCheckCoherence.CslibBridge

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

/-- The current schema's method class and result status do not determine the
epistemic kind: the same pair admits distinct interpretations. -/
theorem schema_method_and_status_do_not_determine_epistemic_kind :
    theoremProvingTestimony.methodClass =
        candidateTheoremProofClassification.methodClass ∧
    theoremProvingTestimony.status =
        candidateTheoremProofClassification.status ∧
    theoremProvingTestimony.kind ≠
        candidateTheoremProofClassification.kind := by
  decide

/-- CSLib LTS transitions preserve the evidence method class. -/
theorem evidence_lifecycle_transition_preserves_method_class
    {before after : EvidenceLifecycleState} {event : EvidenceLifecycleEvent}
    (h : evidenceLifecycle.Tr before event after) :
    before.evidence.methodClass = after.evidence.methodClass := h.1

/-- CSLib LTS transitions preserve epistemic kind. -/
theorem evidence_lifecycle_transition_preserves_kind
    {before after : EvidenceLifecycleState} {event : EvidenceLifecycleEvent}
    (h : evidenceLifecycle.Tr before event after) :
    before.evidence.kind = after.evidence.kind := h.2.1

/-- Any finite CSLib LTS execution preserves epistemic kind end-to-end. -/
theorem evidence_lifecycle_multistep_preserves_kind
    {before after : EvidenceLifecycleState} {events : List EvidenceLifecycleEvent}
    (h : evidenceLifecycle.MTr before events after) :
    before.evidence.kind = after.evidence.kind := by
  induction h with
  | refl => rfl
  | stepL hstep hrest ih =>
      exact (evidence_lifecycle_transition_preserves_kind hstep).trans ih


end GovCheck.Coherence
