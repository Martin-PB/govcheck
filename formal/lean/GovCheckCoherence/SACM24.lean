import GovCheckCoherence.Mapping

namespace GovCheck.Coherence.SACM24

/-- Document-level source views. Each document can itself contain conflicting
    fragments; a document label alone is not enough to select one statement. -/
inductive SourceView where
  | specificationText
  | normativeMetamodelXML
  deriving DecidableEq, Repr

/-- Source fragments are kept separate so conflicting PDF clauses, figures and
    annex entries are not collapsed into one fictitious coherent PDF schema. -/
inductive DeclarationSourceFragment where
  | pdfClause13_6
  | pdfAnnexG6Item6
  | pdfClause15_2_1
  | normativeMetamodelXML
  deriving DecidableEq, Repr

def declarationSourceView : DeclarationSourceFragment → SourceView
  | .pdfClause13_6 => .specificationText
  | .pdfAnnexG6Item6 => .specificationText
  | .pdfClause15_2_1 => .specificationText
  | .normativeMetamodelXML => .normativeMetamodelXML

/-- Literal sets transcribed from individual source fragments. These are
    evidence records, not a decision that one fragment overrides another. -/
inductive AssertionDeclarationKind where
  | asserted
  | assumed
  | axiomatic
  | needsSupport
  | byRule
  deriving DecidableEq, Repr

def declarationLiteralsForFragment : DeclarationSourceFragment → List AssertionDeclarationKind
  | .pdfClause13_6 => [.axiomatic, .assumed, .asserted, .needsSupport]
  | .pdfAnnexG6Item6 => [.axiomatic, .assumed, .asserted]
  | .pdfClause15_2_1 => [.axiomatic, .assumed, .asserted, .byRule]
  | .normativeMetamodelXML => [.axiomatic, .assumed, .asserted, .byRule]

theorem pdf_clause13_6_includes_needsSupport :
    AssertionDeclarationKind.needsSupport ∈ declarationLiteralsForFragment .pdfClause13_6 := by
  simp [declarationLiteralsForFragment]

theorem pdf_clause13_6_does_not_list_byRule :
    AssertionDeclarationKind.byRule ∉ declarationLiteralsForFragment .pdfClause13_6 := by
  simp [declarationLiteralsForFragment]

theorem pdf_annex_g6_item6_lists_three_declarations :
    declarationLiteralsForFragment .pdfAnnexG6Item6 =
      [.axiomatic, .assumed, .asserted] := rfl

theorem pdf_clause15_2_1_includes_byRule :
    AssertionDeclarationKind.byRule ∈ declarationLiteralsForFragment .pdfClause15_2_1 := by
  simp [declarationLiteralsForFragment]

theorem xml_model_includes_byRule :
    AssertionDeclarationKind.byRule ∈ declarationLiteralsForFragment .normativeMetamodelXML := by
  simp [declarationLiteralsForFragment]

/-- The PDF is internally inconsistent about this enumeration: clause 13.6
    includes needsSupport and omits byRule, while clause 15.2.1 includes byRule. -/
theorem pdf_assertion_declaration_fragments_disagree :
    AssertionDeclarationKind.needsSupport ∈ declarationLiteralsForFragment .pdfClause13_6 ∧
    AssertionDeclarationKind.needsSupport ∉ declarationLiteralsForFragment .pdfClause15_2_1 ∧
    AssertionDeclarationKind.byRule ∉ declarationLiteralsForFragment .pdfClause13_6 ∧
    AssertionDeclarationKind.byRule ∈ declarationLiteralsForFragment .pdfClause15_2_1 := by
  simp [declarationLiteralsForFragment]

/-- GovCheck preserves every source literal as a distinct disposition. -/
inductive ClaimDisposition where
  | asserted
  | assumed
  | axiomaticDeclared
  | needsSupport
  | ruleDeclared
  deriving DecidableEq, Repr

def mapAssertionDeclaration : AssertionDeclarationKind → ClaimDisposition
  | .asserted => .asserted
  | .assumed => .assumed
  | .axiomatic => .axiomaticDeclared
  | .needsSupport => .needsSupport
  | .byRule => .ruleDeclared

theorem mapAssertionDeclaration_injective :
    ∀ a b, mapAssertionDeclaration a = mapAssertionDeclaration b → a = b := by
  intro a b h
  cases a <;> cases b <;> cases h <;> rfl

/-- A PDF clause/annex/figure is the evidence unit for a declaration. This
    predicate intentionally does not take only SourceView as an argument. -/
def declarationSupportedByFragment
    (fragment : DeclarationSourceFragment) (kind : AssertionDeclarationKind) : Prop :=
  kind ∈ declarationLiteralsForFragment fragment

theorem sacm_axiomatic_remains_declaration :
    mapAssertionDeclaration .axiomatic = .axiomaticDeclared := rfl

theorem sacm_assumed_remains_assumption :
    mapAssertionDeclaration .assumed = .assumed := rfl

/-- Identity evidence also has fragment-level granularity. The PDF clause text
    and its Figure 9.1 do not agree on the field name. -/
inductive IdentitySourceFragment where
  | pdfClause9_2
  | pdfFigure9_1
  | normativeMetamodelXML
  deriving DecidableEq, Repr

def identitySourceView : IdentitySourceFragment → SourceView
  | .pdfClause9_2 => .specificationText
  | .pdfFigure9_1 => .specificationText
  | .normativeMetamodelXML => .normativeMetamodelXML

inductive ElementIdentityField where
  | gid
  | elementId
  deriving DecidableEq, Repr

def identityFieldForFragment : IdentitySourceFragment → ElementIdentityField
  | .pdfClause9_2 => .gid
  | .pdfFigure9_1 => .elementId
  | .normativeMetamodelXML => .elementId

theorem pdf_clause9_2_uses_gid :
    identityFieldForFragment .pdfClause9_2 = .gid := rfl

theorem pdf_figure9_1_uses_elementId :
    identityFieldForFragment .pdfFigure9_1 = .elementId := rfl

theorem xml_model_uses_elementId :
    identityFieldForFragment .normativeMetamodelXML = .elementId := rfl

/-- PDF prose and Figure 9.1 are two incompatible identity statements. -/
theorem pdf_identity_fragments_disagree :
    identityFieldForFragment .pdfClause9_2 = .gid ∧
    identityFieldForFragment .pdfFigure9_1 = .elementId ∧
    identityFieldForFragment .pdfClause9_2 ≠ identityFieldForFragment .pdfFigure9_1 := by
  decide

def nativeFormatForSourceView : SourceView → String
  | .specificationText => "application/pdf"
  | .normativeMetamodelXML => "application/xml"

/-- Opaque value payload with its source metaclass/type label retained. -/
structure RawSourceValue where
  sourceType : String
  payload : String
  deriving DecidableEq, Repr

/-- A source element reference is revision-bound and keeps the source identity
    field. The mapping slice is partial: only references with a usable identity
    can be carried into a GovCheck claim. -/
structure SACMElementRef where
  identity : String
  identityField : ElementIdentityField
  metaclass : String
  modelRevision : String
  deriving DecidableEq, Repr

/-- Minimal normalized Claim/Assertion slice, not a lossless SACM metamodel.
    Option (List ...) distinguishes an absent source feature from a present,
    possibly empty, multi-valued feature. Rule/value payloads remain opaque. -/
structure SACMClaim where
  identity : String
  identityField : ElementIdentityField
  sourceView : SourceView
  value : Option RawSourceValue
  subject : Option (List SACMElementRef)
  whole : Option (List String)
  declaration : Option AssertionDeclarationKind
  isTrue : Option Bool
  assertionValues : List String
  assertionRuleRefs : List String
  strengthRefs : List String
  deriving DecidableEq, Repr

/-- SACM specifies an optional declaration with the default asserted. Preserve
    explicit absence and compute the effective declaration separately. -/
def effectiveDeclaration (claim : SACMClaim) : AssertionDeclarationKind :=
  claim.declaration.getD .asserted

/-- The proposition is an explicit interpretation supplied by a mapping
    authority. The source text/value is not silently parsed into Lean truth.
    Constructor obligations are tied to exact PDF/XML fragments, not a
    coarse document-level label. -/
structure SACMClaimInterpretation
    (claim : SACMClaim) (interpretation : ClaimSemantics) where
  sourceModel : ArtifactRef
  sourceFormatMatchesView : sourceModel.nativeFormat = nativeFormatForSourceView claim.sourceView
  declarationFragment : DeclarationSourceFragment
  declarationFragmentMatchesView :
    declarationSourceView declarationFragment = claim.sourceView
  declarationConsistentWithFragment :
    declarationSupportedByFragment declarationFragment (effectiveDeclaration claim)
  identityFragment : IdentitySourceFragment
  identityFragmentMatchesView : identitySourceView identityFragment = claim.sourceView
  identityFieldMatchesFragment :
    claim.identityField = identityFieldForFragment identityFragment
  claimIdentityNonEmpty : claim.identity ≠ ""
  claimIdentityPreserved : interpretation.claimId = claim.identity
  mappedSubject : Option (List SACMElementRef)
  subjectPreserved : mappedSubject = claim.subject
  subjectIdentityFieldsMatchFragment :
    ∀ subject, subject ∈ mappedSubject.getD [] →
      subject.identityField = identityFieldForFragment identityFragment
  subjectIdentitiesNonEmpty :
    ∀ subject, subject ∈ mappedSubject.getD [] → subject.identity ≠ ""
  subjectRevisionMatchesModel :
    ∀ subject, subject ∈ mappedSubject.getD [] →
      subject.modelRevision = sourceModel.revision
  interpretationBasis : String

/-- Conjunction of all premises in a structured inference. -/
def AllPremises : List Prop → Prop
  | [] => True
  | premise :: rest => premise ∧ AllPremises rest

/-- SACM 2.4 Beta 1 inference type literals. -/
inductive InferenceTypeKind where
  | probable
  | collective
  | necessary
  | sufficient
  | necessaryAndSufficient
  | byRule
  deriving DecidableEq, Repr

/-- Classical fragment of SACM inference semantics.

    probable is intentionally absent: a probability semantics is required.
    byRule requires a concrete rule identity and a proof term. -/
inductive InferenceBridge : List Prop → Prop → InferenceTypeKind → Type where
  | collective {premises : List Prop} {conclusion : Prop} :
      premises ≠ [] →
      (AllPremises premises ↔ conclusion) →
      InferenceBridge premises conclusion .collective
  | necessary {premise conclusion : Prop} :
      (conclusion → premise) →
      InferenceBridge [premise] conclusion .necessary
  | sufficient {premise conclusion : Prop} :
      (premise → conclusion) →
      InferenceBridge [premise] conclusion .sufficient
  | necessaryAndSufficient {premise conclusion : Prop} :
      (premise ↔ conclusion) →
      InferenceBridge [premise] conclusion .necessaryAndSufficient
  | byRule {premises : List Prop} {conclusion : Prop} :
      (ruleIdentity : String) →
      (AllPremises premises → conclusion) →
      InferenceBridge premises conclusion .byRule

theorem probable_inference_has_no_classical_bridge
    (premises : List Prop) (conclusion : Prop) :
    ¬ Nonempty (InferenceBridge premises conclusion .probable) := by
  intro h
  cases h with
  | intro bridge => cases bridge

theorem necessary_inference_is_reverse_entailment
    {premise conclusion : Prop}
    (bridge : InferenceBridge [premise] conclusion .necessary) :
    conclusion → premise := by
  cases bridge with
  | necessary proof => exact proof

theorem sufficient_inference_is_forward_entailment
    {premise conclusion : Prop}
    (bridge : InferenceBridge [premise] conclusion .sufficient) :
    premise → conclusion := by
  cases bridge with
  | sufficient proof => exact proof

theorem collective_inference_is_joint_equivalence
    {premises : List Prop} {conclusion : Prop}
    (bridge : InferenceBridge premises conclusion .collective) :
    AllPremises premises ↔ conclusion := by
  cases bridge with
  | collective _ proof => exact proof

theorem claim_interpretation_preserves_declaration
    {claim : SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACMClaimInterpretation claim interpretation) :
    mapping.disposition = mapAssertionDeclaration (effectiveDeclaration claim) := by
  rfl

theorem claim_interpretation_preserves_identity
    {claim : SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACMClaimInterpretation claim interpretation) :
    interpretation.claimId = claim.identity :=
  mapping.claimIdentityPreserved

theorem claim_interpretation_preserves_subject
    {claim : SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACMClaimInterpretation claim interpretation) :
    mapping.mappedSubject = claim.subject :=
  mapping.subjectPreserved

theorem claim_interpretation_requires_nonempty_identity
    {claim : SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACMClaimInterpretation claim interpretation) :
    claim.identity ≠ "" :=
  mapping.claimIdentityNonEmpty

theorem claim_subject_revision_is_pinned
    {claim : SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACMClaimInterpretation claim interpretation)
    (subject : SACMElementRef) (h : subject ∈ mapping.mappedSubject.getD []) :
    subject.modelRevision = mapping.sourceModel.revision :=
  mapping.subjectRevisionMatchesModel subject h

/-- Full first-slice link from a source-view-qualified SACM Claim through its
    explicit formal interpretation into a GovCheck cross-model mapping. -/
structure SACMClaimMapping
    (sacmClaim : SACMClaim) (source target : MappingSubject) where
  sourceInterpretation : SACMClaimInterpretation sacmClaim source.claim
  evidenceMapping : EvidenceMapping source target
  sourceModelMatches :
    sourceInterpretation.sourceModel = source.model

theorem sacm_claim_mapping_preserves_claim_identity
    {sacmClaim : SACMClaim} {source target : MappingSubject}
    (mapping : SACMClaimMapping sacmClaim source target) :
    source.claim.claimId = sacmClaim.identity :=
  mapping.sourceInterpretation.claimIdentityPreserved

theorem sacm_claim_mapping_preserves_subject
    {sacmClaim : SACMClaim} {source target : MappingSubject}
    (mapping : SACMClaimMapping sacmClaim source target) :
    mapping.sourceInterpretation.mappedSubject = sacmClaim.subject :=
  mapping.sourceInterpretation.subjectPreserved

theorem sacm_claim_mapping_uses_exact_source_model
    {sacmClaim : SACMClaim} {source target : MappingSubject}
    (mapping : SACMClaimMapping sacmClaim source target) :
    mapping.sourceInterpretation.sourceModel = source.model :=
  mapping.sourceModelMatches

theorem sacm_claim_mapping_has_semantic_bridge
    {sacmClaim : SACMClaim} {source target : MappingSubject}
    (mapping : SACMClaimMapping sacmClaim source target) :
    Nonempty (SemanticBridge source.claim.meaning target.claim.meaning
      mapping.evidenceMapping.contract.coverage) :=
  ⟨mapping.evidenceMapping.semanticBridge⟩

end GovCheck.Coherence.SACM24
