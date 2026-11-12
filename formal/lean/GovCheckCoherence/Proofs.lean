import GovCheckCoherence.Evidence
import GovCheckCoherence.SchemaBoundary
import GovCheckCoherence.Mapping

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


/-- The mapping bridge binds the exact source and target semantic model revisions. -/
theorem evidence_mapping_binds_model_revisions
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    mapping.contract.sourceModel = source.model ∧
      mapping.contract.targetModel = target.model :=
  ⟨mapping.sourceModelMatches, mapping.targetModelMatches⟩

/-- A mapped evidence record retains the exact native artifact revision. -/
theorem evidence_mapping_preserves_revision
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.artifact.revision = source.artifact.revision :=
  mapping_preserves_source_revision mapping

/-- A mapped evidence record retains the source artifact identity. -/
theorem evidence_mapping_preserves_identity
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.artifact.identity = source.artifact.identity :=
  mapping_preserves_source_identity mapping

/-- The first contract requires exact scope preservation. -/
theorem evidence_mapping_preserves_scope
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.scope = source.scope :=
  mapping_preserves_scope mapping

/-- Every source assumption remains explicit in the mapped target. -/
theorem evidence_mapping_preserves_assumptions
    {source target : MappingSubject} (mapping : EvidenceMapping source target)
    (assumption : String) (h : assumption ∈ source.assumptions) :
    assumption ∈ target.assumptions :=
  mapping_preserves_assumptions mapping assumption h

/-- Method-class changes are not silently introduced by this first mapping profile. -/
theorem evidence_mapping_preserves_method_class
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.evidence.methodClass = source.evidence.methodClass :=
  mapping_preserves_method_class mapping

/-- A theorem-proof target is carried from an existing theorem proof or has
    an actual Lean proof term for the target claim. -/
theorem evidence_mapping_theorem_proof_requires_derivation
    {source target : MappingSubject} (mapping : EvidenceMapping source target)
    (h : target.evidence.kind = .theoremProof) :
    source.evidence.kind = .theoremProof ∨
      (∃ derivation : KernelCheckedDerivation target.claim.meaning, derivation.proof = derivation.proof) :=
  mapping_target_theorem_proof_requires_derivation mapping h

/-- Unknown (no determinate result) is not the same as inconclusive
    (a method ran but did not settle pass/fail). -/
theorem unknown_status_is_distinct_from_inconclusive :
    EvidenceStatus.unknown ≠ EvidenceStatus.inconclusive := by
  decide

end GovCheck.Coherence
