import GovCheckCoherence.Evidence
import GovCheckCoherence.SchemaBoundary
import GovCheckCoherence.Mapping
import GovCheckCoherence.SACM24

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

/-- Testimony cannot be mapped to theorem-proof status without an actual
    proof term of the exact target proposition. -/
theorem testimony_mapping_to_theorem_proof_requires_derivation
    {claim : Prop}
    (rule : KindMappingRule claim .testimony .theoremProof) :
    ∃ derivation : KernelCheckedDerivation claim,
      derivation.proof = derivation.proof :=
  kind_mapping_rule_theorem_proof_requires_derivation rule rfl

/-- A model-checking result cannot be mapped to theorem-proof status without
    an actual proof term of the exact target proposition. -/
theorem model_checking_mapping_to_theorem_proof_requires_derivation
    {claim : Prop}
    (rule : KindMappingRule claim .modelCheckingResult .theoremProof) :
    ∃ derivation : KernelCheckedDerivation claim,
      derivation.proof = derivation.proof :=
  kind_mapping_rule_theorem_proof_requires_derivation rule rfl

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

/-- A theorem-proof target always carries an actual Lean proof term of the
exact target claim; a source kind label is never sufficient. -/
theorem evidence_mapping_theorem_proof_requires_derivation
    {source target : MappingSubject} (mapping : EvidenceMapping source target)
    (h : target.evidence.kind = .theoremProof) :
    ∃ derivation : KernelCheckedDerivation target.claim.meaning,
      derivation.proof = derivation.proof :=
  mapping_target_theorem_proof_requires_derivation mapping h

/-- Unknown (no determinate result) is not the same as inconclusive
    (a method ran but did not settle pass/fail). -/
theorem unknown_status_is_distinct_from_inconclusive :
    EvidenceStatus.unknown ≠ EvidenceStatus.inconclusive := by
  decide

/-- SACM assertion declarations preserve their distinct GovCheck dispositions. -/
theorem sacm_assertion_disposition_is_injective :
    ∀ a b, SACM24.mapAssertionDeclaration a = SACM24.mapAssertionDeclaration b → a = b :=
  SACM24.mapAssertionDeclaration_injective

/-- SACM probable inference cannot be silently interpreted as classical entailment. -/
theorem sacm_probable_inference_requires_probability_semantics
    (premises : List Prop) (conclusion : Prop) :
    ¬ Nonempty (SACM24.InferenceBridge premises conclusion .probable) :=
  SACM24.probable_inference_has_no_classical_bridge premises conclusion

/-- SACM necessary inference is represented in the reverse implication direction. -/
theorem sacm_necessary_inference_direction
    {premise conclusion : Prop}
    (bridge : SACM24.InferenceBridge [premise] conclusion .necessary) :
    conclusion → premise :=
  SACM24.necessary_inference_is_reverse_entailment bridge

/-- SACM sufficient inference is represented in the forward implication direction. -/
theorem sacm_sufficient_inference_direction
    {premise conclusion : Prop}
    (bridge : SACM24.InferenceBridge [premise] conclusion .sufficient) :
    premise → conclusion :=
  SACM24.sufficient_inference_is_forward_entailment bridge

/-- SACM collective inference preserves the joint-premise equivalence. -/
theorem sacm_collective_inference_semantics
    {premises : List Prop} {conclusion : Prop}
    (bridge : SACM24.InferenceBridge premises conclusion .collective) :
    SACM24.AllPremises premises ↔ conclusion :=
  SACM24.collective_inference_is_joint_equivalence bridge

/-- SACM Claim identity is bound to the GovCheck claim interpretation. -/
theorem sacm_claim_interpretation_preserves_identity
    {claim : SACM24.SACMClaim} {target : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim target) :
    target.claimId = claim.identity :=
  SACM24.claim_interpretation_preserves_identity mapping

/-- SACM explicit subject references are preserved by the interpretation. -/
theorem sacm_claim_interpretation_preserves_subject
    {claim : SACM24.SACMClaim} {target : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim target) :
    mapping.mappedSubject = claim.subject :=
  SACM24.claim_interpretation_preserves_subject mapping

/-- A SACM subject reference is tied to the exact source model revision. -/
theorem sacm_claim_subject_revision_is_pinned
    {claim : SACM24.SACMClaim} {target : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim target)
    (subject : SACM24.SACMElementRef) (h : subject ∈ mapping.mappedSubject.getD []) :
    subject.modelRevision = mapping.sourceModel.revision :=
  SACM24.claim_subject_revision_is_pinned mapping subject h

/-- SACM Claim identity is carried into the source GovCheck interpretation. -/
theorem sacm_mapping_preserves_claim_identity
    {sacmClaim : SACM24.SACMClaim} {source target : MappingSubject}
    (mapping : SACM24.SACMClaimMapping sacmClaim source target) :
    source.claim.claimId = sacmClaim.identity :=
  SACM24.sacm_claim_mapping_preserves_claim_identity mapping

/-- The explicit SACM subject remains attached to the mapped claim. -/
theorem sacm_mapping_preserves_subject
    {sacmClaim : SACM24.SACMClaim} {source target : MappingSubject}
    (mapping : SACM24.SACMClaimMapping sacmClaim source target) :
    mapping.sourceInterpretation.mappedSubject = sacmClaim.subject :=
  SACM24.sacm_claim_mapping_preserves_subject mapping

/-- The SACM subject is bound to the exact source model revision. -/
theorem sacm_mapping_uses_exact_source_model
    {sacmClaim : SACM24.SACMClaim} {source target : MappingSubject}
    (mapping : SACM24.SACMClaimMapping sacmClaim source target) :
    mapping.sourceInterpretation.sourceModel = source.model :=
  SACM24.sacm_claim_mapping_uses_exact_source_model mapping

/-- The SACM-to-GovCheck claim mapping carries its declared semantic bridge. -/
theorem sacm_mapping_has_semantic_bridge
    {sacmClaim : SACM24.SACMClaim} {source target : MappingSubject}
    (mapping : SACM24.SACMClaimMapping sacmClaim source target) :
    Nonempty (SemanticBridge source.claim.meaning target.claim.meaning
      mapping.evidenceMapping.contract.coverage) :=
  SACM24.sacm_claim_mapping_has_semantic_bridge mapping

/-- SACM assertion declaration remains distinct in the GovCheck claim disposition. -/
theorem sacm_mapping_preserves_assertion_declaration
    {sacmClaim : SACM24.SACMClaim} {source target : MappingSubject}
    (mapping : SACM24.SACMClaimMapping sacmClaim source target) :
    mapping.sourceInterpretation.disposition =
      SACM24.mapAssertionDeclaration (SACM24.effectiveDeclaration sacmClaim) :=
  SACM24.claim_interpretation_preserves_declaration mapping.sourceInterpretation

/-- PDF Clause 13.6 includes needsSupport; this is a fragment-level fact,
not a PDF-wide declaration rule. -/
theorem sacm_pdf_clause13_6_includes_needsSupport :
    SACM24.AssertionDeclarationKind.needsSupport ∈
      SACM24.declarationLiteralsForFragment .pdfClause13_6 :=
  SACM24.pdf_clause13_6_includes_needsSupport

/-- PDF Clause 13.6 does not list byRule; Clause 15.2.1 is modelled separately. -/
theorem sacm_pdf_clause13_6_omits_byRule :
    SACM24.AssertionDeclarationKind.byRule ∉
      SACM24.declarationLiteralsForFragment .pdfClause13_6 :=
  SACM24.pdf_clause13_6_does_not_list_byRule

/-- The XML source view does not list the PDF-only needsSupport literal. -/
theorem sacm_xml_omits_needsSupport :
    SACM24.AssertionDeclarationKind.needsSupport ∉
      SACM24.declarationLiteralsForFragment .normativeMetamodelXML := by
  simp [SACM24.declarationLiteralsForFragment]

/-- The normative XML and PDF Clause 15.2.1 both list byRule. -/
theorem sacm_xml_and_pdf_clause15_2_1_include_byRule :
    SACM24.AssertionDeclarationKind.byRule ∈
      SACM24.declarationLiteralsForFragment .normativeMetamodelXML ∧
    SACM24.AssertionDeclarationKind.byRule ∈
      SACM24.declarationLiteralsForFragment .pdfClause15_2_1 := by
  exact ⟨SACM24.xml_model_includes_byRule, SACM24.pdf_clause15_2_1_includes_byRule⟩

/-- The PDF itself contains incompatible declaration fragments. -/
theorem sacm_pdf_declaration_fragments_disagree :
    SACM24.AssertionDeclarationKind.needsSupport ∈
        SACM24.declarationLiteralsForFragment .pdfClause13_6 ∧
    SACM24.AssertionDeclarationKind.needsSupport ∉
        SACM24.declarationLiteralsForFragment .pdfClause15_2_1 ∧
    SACM24.AssertionDeclarationKind.byRule ∉
        SACM24.declarationLiteralsForFragment .pdfClause13_6 ∧
    SACM24.AssertionDeclarationKind.byRule ∈
        SACM24.declarationLiteralsForFragment .pdfClause15_2_1 :=
  SACM24.pdf_assertion_declaration_fragments_disagree

/-- The PDF clause 9.2 identity field is gid. -/
theorem sacm_pdf_clause9_2_identity_is_gid :
    SACM24.identityFieldForFragment .pdfClause9_2 = .gid :=
  SACM24.pdf_clause9_2_uses_gid

/-- PDF Figure 9.1 uses elementId; the PDF view therefore cannot be collapsed
into one document-wide identity-field rule. -/
theorem sacm_pdf_figure9_1_identity_is_elementId :
    SACM24.identityFieldForFragment .pdfFigure9_1 = .elementId :=
  SACM24.pdf_figure9_1_uses_elementId

/-- The normative metamodel XML uses elementId. -/
theorem sacm_xml_identity_is_elementId :
    SACM24.identityFieldForFragment .normativeMetamodelXML = .elementId :=
  SACM24.xml_model_uses_elementId

/-- The PDF itself contains incompatible identity fragments. -/
theorem sacm_pdf_identity_fragments_disagree :
    SACM24.identityFieldForFragment .pdfClause9_2 =
        SACM24.ElementIdentityField.gid ∧
    SACM24.identityFieldForFragment .pdfFigure9_1 =
        SACM24.ElementIdentityField.elementId ∧
    SACM24.identityFieldForFragment .pdfClause9_2 ≠
        SACM24.identityFieldForFragment .pdfFigure9_1 :=
  SACM24.pdf_identity_fragments_disagree

/-- A mapped Claim must cite a specific source fragment for its declaration. -/
theorem sacm_claim_mapping_requires_source_fragment_consistency
    {claim : SACM24.SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim interpretation) :
    SACM24.effectiveDeclaration claim ∈
      SACM24.declarationLiteralsForFragment mapping.declarationFragment :=
  mapping.declarationConsistentWithFragment

/-- A mapped Claim must cite the exact identity fragment whose field it uses. -/
theorem sacm_claim_mapping_requires_identity_fragment_consistency
    {claim : SACM24.SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim interpretation) :
    claim.identityField = SACM24.identityFieldForFragment mapping.identityFragment :=
  mapping.identityFieldMatchesFragment

/-- A mapped Claim must bind the fragment to its document-level source view. -/
theorem sacm_claim_mapping_requires_declaration_fragment_view
    {claim : SACM24.SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim interpretation) :
    SACM24.declarationSourceView mapping.declarationFragment = claim.sourceView :=
  mapping.declarationFragmentMatchesView

/-- The identity fragment must belong to the declared document-level view,
without imposing a single identity field across all PDF fragments. -/
theorem sacm_claim_mapping_requires_identity_fragment_view
    {claim : SACM24.SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim interpretation) :
    SACM24.identitySourceView mapping.identityFragment = claim.sourceView :=
  mapping.identityFragmentMatchesView

/-- The native source format must match the selected document-level view. -/
theorem sacm_claim_source_format_matches_view
    {claim : SACM24.SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACM24.SACMClaimInterpretation claim interpretation) :
    mapping.sourceModel.nativeFormat = SACM24.nativeFormatForSourceView claim.sourceView :=
  mapping.sourceFormatMatchesView

end GovCheck.Coherence
