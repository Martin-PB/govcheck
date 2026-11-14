import GovCheckCoherence.Mapping
import GovCheckCoherence.UML25Multiplicity

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

/-- Normative/informative status is kept distinct from source-view identity. -/
def declarationFragmentStatus : DeclarationSourceFragment → String
  | .pdfClause13_6 => "normative"
  | .pdfAnnexG6Item6 => "informative"
  | .pdfClause15_2_1 => "informative"
  | .normativeMetamodelXML => "normative"

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
  decide

theorem pdf_clause13_6_does_not_list_byRule :
    AssertionDeclarationKind.byRule ∉ declarationLiteralsForFragment .pdfClause13_6 := by
  decide

theorem pdf_annex_g6_item6_lists_three_declarations :
    declarationLiteralsForFragment .pdfAnnexG6Item6 =
      [.axiomatic, .assumed, .asserted] := rfl

theorem pdf_clause15_2_1_includes_byRule :
    AssertionDeclarationKind.byRule ∈ declarationLiteralsForFragment .pdfClause15_2_1 := by
  decide

theorem xml_model_includes_byRule :
    AssertionDeclarationKind.byRule ∈ declarationLiteralsForFragment .normativeMetamodelXML := by
  decide

/-- The fragment lists differ. Clause 13.6 is normative; Annex G.6 and
    Clause 15.2.1 are informative. The later byRule listing is described as an
    addition; its omission of needsSupport is not treated as a deletion rule. -/
theorem pdf_assertion_declaration_fragments_disagree :
    AssertionDeclarationKind.needsSupport ∈ declarationLiteralsForFragment .pdfClause13_6 ∧
    AssertionDeclarationKind.needsSupport ∉ declarationLiteralsForFragment .pdfClause15_2_1 ∧
    AssertionDeclarationKind.byRule ∉ declarationLiteralsForFragment .pdfClause13_6 ∧
    AssertionDeclarationKind.byRule ∈ declarationLiteralsForFragment .pdfClause15_2_1 := by
  decide

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
  disposition : ClaimDisposition
  declarationPreserved :
    disposition = mapAssertionDeclaration (effectiveDeclaration claim)
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
    mapping.disposition = mapAssertionDeclaration (effectiveDeclaration claim) :=
  mapping.declarationPreserved

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


/-- A multiplicity interval transcribed from a particular SACM source fragment.
    none as upper bound means unbounded. XML multiplicities below are interpreted
    using the narrow UML 2.5 rules in UML25Multiplicity; this does not prove
    that the parser extracted the serialized source values correctly. -/
structure SourceMultiplicity where
  lower : Nat
  upper : Option Nat
  deriving DecidableEq, Repr


/-- Convert the supported UML 2.5 multiplicity result into the source-register
    interval convention (an absent upper value means unbounded). -/
def sourceMultiplicityFromUML25 (m : UML25Multiplicity.Multiplicity) : SourceMultiplicity :=
  { lower := m.lower
    upper := match m.upper with
      | .finite value => some value
      | .unlimited => none }

/-- Interpret the manually transcribed XMI ValueSpecification shape. This
    projection is checked against the source inventory by workflow tests; the
    Lean theorems prove the UML 2.5 default interpretation, not XML parsing. -/
def interpretXmlMultiplicity
    (lower : Option UML25Multiplicity.LowerValueSpecification)
    (upper : Option UML25Multiplicity.UpperValueSpecification) :
    Option SourceMultiplicity :=
  (UML25Multiplicity.interpretMultiplicity lower upper).map sourceMultiplicityFromUML25

namespace SourceFacts


/-- Normative PDF Figure 13.1 (printed page 41) shows Claim.value as MultiLangString. -/
def normativePdfFigure13_1ClaimValueType : String := "MultiLangString"

/-- Informative PDF Figure 15.1.1 (printed page 59) shows Claim.value as ExpressionLangString. -/
def informativePdfFigure15_1_1ClaimValueType : String := "ExpressionLangString"

/-- The normative machine-readable metamodel XML declares Claim.value as ExpressionLangString. -/
def xmlClaimValueType : String := "ExpressionLangString"

/-- R-128 reports MultiLangString for Clause 13.9; this value agrees with the normative
    Figure 13.1, but the exact Clause 13.9 locator remains a separate transcription check. -/
def r128ReportedClaimValueType : String := "MultiLangString"
/-- PDF Clause 13.9, printed page 45, explicitly gives the Claim value type. -/
def normativePdfClause13_9ClaimValueType : String := "MultiLangString"

theorem pdf_clause13_9_matches_normative_figure13_1 :
    normativePdfClause13_9ClaimValueType = normativePdfFigure13_1ClaimValueType := by
  decide

theorem pdf_clause13_9_conflicts_informative_figure15_1_1 :
    normativePdfClause13_9ClaimValueType ≠ informativePdfFigure15_1_1ClaimValueType := by
  decide

theorem pdf_normative_figure13_1_vs_informative_figure15_1_1_claim_value_conflict :
    normativePdfFigure13_1ClaimValueType ≠ informativePdfFigure15_1_1ClaimValueType := by
  decide

theorem pdf_normative_figure13_1_vs_xml_claim_value_conflict :
    normativePdfFigure13_1ClaimValueType ≠ xmlClaimValueType := by
  decide

theorem claim_value_type_agrees_in_informative_pdf_figure15_1_1_and_xml :
    informativePdfFigure15_1_1ClaimValueType = xmlClaimValueType := by
  decide

theorem r128_reported_claim_value_type_matches_normative_pdf_figure13_1 :
    r128ReportedClaimValueType = normativePdfFigure13_1ClaimValueType := by
  decide

/-- PDF Clause 13.13 text gives AssertedEvidence.evidence a 0..* multiplicity. -/
def pdfClause13_13AssertedEvidenceEvidence : SourceMultiplicity := ⟨0, none⟩

/-- Normative PDF Figure 13.1 shows the evidence end as 1..*. -/
def pdfFigure13_1AssertedEvidenceEvidence : SourceMultiplicity := ⟨1, none⟩

/-- The normative metamodel XML declares the evidence end as 1..*. -/
def xmlAssertedEvidenceEvidence : SourceMultiplicity := ⟨1, none⟩

theorem pdf_clause13_13_vs_figure13_1_asserted_evidence_conflict :
    pdfClause13_13AssertedEvidenceEvidence ≠ pdfFigure13_1AssertedEvidenceEvidence := by
  decide

theorem pdf_figure13_1_and_xml_asserted_evidence_agree :
    pdfFigure13_1AssertedEvidenceEvidence = xmlAssertedEvidenceEvidence := by
  decide

theorem pdf_clause13_13_vs_xml_asserted_evidence_conflict :
    pdfClause13_13AssertedEvidenceEvidence ≠ xmlAssertedEvidenceEvidence := by
  decide

/-- PDF clause 9.2 versus the normative metamodel XML. -/
def pdfSACMElementAbstraction : SourceMultiplicity := ⟨0, some 1⟩
def pdfFigure9_1SACMElementAbstraction : SourceMultiplicity := ⟨0, none⟩
def xmlSACMElementAbstraction : SourceMultiplicity := ⟨0, none⟩

theorem sacm_element_abstraction_multiplicity_conflict :
    pdfSACMElementAbstraction ≠ xmlSACMElementAbstraction := by
  decide

theorem pdf_clause9_2_vs_figure9_1_abstraction_multiplicity_conflict :
    pdfSACMElementAbstraction ≠ pdfFigure9_1SACMElementAbstraction := by
  decide

theorem pdf_figure9_1_abstraction_multiplicity_matches_xml :
    pdfFigure9_1SACMElementAbstraction = xmlSACMElementAbstraction := by
  decide

/-- PDF clause 13.11 versus the normative metamodel XML. -/
def pdfAssertedRelationshipIsCounter : SourceMultiplicity := ⟨1, some 1⟩
def xmlAssertedRelationshipIsCounter : SourceMultiplicity := ⟨0, some 1⟩

theorem asserted_relationship_isCounter_multiplicity_conflict :
    pdfAssertedRelationshipIsCounter ≠ xmlAssertedRelationshipIsCounter := by
  decide

/-- Normative PDF Figure 13.1 shows isCounter as required, matching Clause 13.11. -/
def pdfFigure13_1AssertedRelationshipIsCounter : SourceMultiplicity := ⟨1, some 1⟩

theorem pdf_figure13_1_isCounter_matches_clause13_11 :
    pdfFigure13_1AssertedRelationshipIsCounter = pdfAssertedRelationshipIsCounter := by
  decide

theorem pdf_figure13_1_vs_xml_isCounter_conflict :
    pdfFigure13_1AssertedRelationshipIsCounter ≠ xmlAssertedRelationshipIsCounter := by
  decide

/-- The PDF diagram labels the subject association end at its target type. -/
def pdfFigure13_1SubjectEndType : String := "SACMElement"
def pdfFigure13_1SubjectMultiplicity : SourceMultiplicity := ⟨0, none⟩

/-- XML declares Claim.subject as an owned property whose type is SACMElement. -/
def xmlClaimSubjectType : String := "SACMElement"
def xmlClaimSubjectMultiplicity : SourceMultiplicity := ⟨0, none⟩

/-- The PDF diagram labels the whole association end at its target type. -/
def pdfFigure13_1WholeEndType : String := "SACMModel"
def pdfFigure13_1WholeMultiplicity : SourceMultiplicity := ⟨0, none⟩

/-- XML declares Claim.whole as an owned property whose type is SACMModel. -/
def xmlClaimWholeType : String := "SACMModel"
def xmlClaimWholeMultiplicity : SourceMultiplicity := ⟨0, none⟩

/-- Figure 13.1 and the XML agree on the target type of Claim.subject. -/
theorem claim_subject_target_type_agrees_between_pdf_figure13_1_and_xml :
    pdfFigure13_1SubjectEndType = xmlClaimSubjectType := by
  decide

theorem claim_subject_multiplicity_agrees_between_pdf_figure13_1_and_xml :
    pdfFigure13_1SubjectMultiplicity = xmlClaimSubjectMultiplicity := by
  decide

/-- Figure 13.1 and the XML agree on the target type of Claim.whole. -/
theorem claim_whole_target_type_agrees_between_pdf_figure13_1_and_xml :
    pdfFigure13_1WholeEndType = xmlClaimWholeType := by
  decide

theorem claim_whole_multiplicity_agrees_between_pdf_figure13_1_and_xml :
    pdfFigure13_1WholeMultiplicity = xmlClaimWholeMultiplicity := by
  decide

/- The PDF diagram records navigable association ends; it does not by itself
   expose the XML-specific ownedAttribute representation. No ownership conflict
   is inferred from the diagram's role-label placement. -/

/-- PDF clauses 10.5 and 11.3 give incompatible BindingPackage superclass
    statements; the XML agrees with clause 10.5. -/
def pdfBindingPackageClause10_5 : List String :=
  ["ScopedPackage", "SACMPackageWithBinding"]
def pdfBindingPackageClause11_3 : List String := ["ModelElement"]
def xmlBindingPackage : List String :=
  ["ScopedPackage", "SACMPackageWithBinding"]

theorem binding_package_pdf_fragments_conflict :
    pdfBindingPackageClause10_5 ≠ pdfBindingPackageClause11_3 := by
  decide

theorem xml_binding_package_matches_pdf_clause10_5 :
    xmlBindingPackage = pdfBindingPackageClause10_5 := rfl

/-- Clause 9.10 explicitly names ModelElement as the SACMModel superclass. -/
def pdfSACMModelClause9_10 : List String := ["ModelElement"]

/-- Annex G.6 item 5 is prose ("A SACMModel ... can be an Assertion"), not a
    complete enumeration of direct superclasses; it is not normalized as one. -/
def pdfSACMModelAnnexG6Item5Text : String :=
  "A SACMModel (Group, Package, Diagram) can be an Assertion"

def xmlSACMModel : List String :=
  ["ModelElement", "Assertion", "Assessment"]

theorem xml_sacm_model_includes_assertion :
    "Assertion" ∈ xmlSACMModel := by
  decide

theorem xml_sacm_model_includes_assessment :
    "Assessment" ∈ xmlSACMModel := by
  decide

/-- Additional XML generalizations not stated in the corresponding PDF clauses. -/
def pdfSACMDependencyClause9_11 : List String := ["DirectedRelationship"]
def xmlSACMDependency : List String := ["DirectedRelationship", "BaseElement"]
def pdfRuleClause15_2_3 : List String := ["BaseElement"]
def xmlRule : List String := ["ModelElement", "BaseElement"]

theorem sacm_dependency_xml_adds_base_element :
    pdfSACMDependencyClause9_11 ≠ xmlSACMDependency := by
  decide

theorem rule_xml_adds_model_element :
    pdfRuleClause15_2_3 ≠ xmlRule := by
  decide

/-- Clause 15.2.1 declares the feature assertionDeclarationRule, matching XML. -/
def pdfAssertionDeclarationRuleFeature : String := "assertionDeclarationRule"
def xmlAssertionDeclarationRuleFeature : String := "assertionDeclarationRule"

/-- The same PDF clause's OCL constraint refers to assertionRule instead of the
    declared assertionDeclarationRule feature. This is an internal PDF reference
    mismatch, not a PDF/XML feature rename. -/
def pdfAssertionRuleOclReference : String := "assertionRule"

theorem pdf_xml_assertion_declaration_rule_feature_name_agrees :
    pdfAssertionDeclarationRuleFeature = xmlAssertionDeclarationRuleFeature := by
  decide

theorem pdf_assertion_rule_ocl_reference_differs_from_declared_feature :
    pdfAssertionRuleOclReference ≠ pdfAssertionDeclarationRuleFeature := by
  decide

/-- XML source shapes below preserve the distinction between an absent
    ValueSpecification and a present LiteralInteger with an omitted value.
    These are manually transcribed from the generated XMI inventory. -/
def xmlClaimValueMultiplicity : SourceMultiplicity := ⟨0, some 1⟩
def xmlClaimValueMultiplicityFromUML25 : Option SourceMultiplicity :=
  interpretXmlMultiplicity (some (.literalInteger none)) none

def xmlClaimWholeMultiplicityFromUML25 : Option SourceMultiplicity :=
  interpretXmlMultiplicity (some (.literalInteger none))
    (some (.literalUnlimitedNatural (some .unlimited)))

def xmlClaimSubjectMultiplicityFromUML25 : Option SourceMultiplicity :=
  interpretXmlMultiplicity (some (.literalInteger none))
    (some (.literalUnlimitedNatural (some .unlimited)))

def xmlSACMElementAbstractionMultiplicityFromUML25 : Option SourceMultiplicity :=
  interpretXmlMultiplicity (some (.literalInteger none))
    (some (.literalUnlimitedNatural (some .unlimited)))

def xmlAssertedRelationshipIsCounterMultiplicityFromUML25 : Option SourceMultiplicity :=
  interpretXmlMultiplicity (some (.literalInteger none)) none

def xmlAssertedEvidenceEvidenceMultiplicityFromUML25 : Option SourceMultiplicity :=
  interpretXmlMultiplicity none
    (some (.literalUnlimitedNatural (some .unlimited)))

def xmlAssertionDeclarationRuleMultiplicity : SourceMultiplicity := ⟨0, none⟩
def xmlAssertionDeclarationRuleMultiplicityFromUML25 : Option SourceMultiplicity :=
  interpretXmlMultiplicity (some (.literalInteger none))
    (some (.literalUnlimitedNatural (some .unlimited)))

theorem xml_claim_value_multiplicity_matches_uml25 :
    xmlClaimValueMultiplicityFromUML25 = some xmlClaimValueMultiplicity := rfl

theorem xml_claim_whole_multiplicity_matches_uml25 :
    xmlClaimWholeMultiplicityFromUML25 = some xmlClaimWholeMultiplicity := rfl

theorem xml_claim_subject_multiplicity_matches_uml25 :
    xmlClaimSubjectMultiplicityFromUML25 = some xmlClaimSubjectMultiplicity := rfl

theorem xml_sacm_element_abstraction_multiplicity_matches_uml25 :
    xmlSACMElementAbstractionMultiplicityFromUML25 = some xmlSACMElementAbstraction := rfl

theorem xml_asserted_relationship_isCounter_multiplicity_matches_uml25 :
    xmlAssertedRelationshipIsCounterMultiplicityFromUML25 = some xmlAssertedRelationshipIsCounter := rfl

theorem xml_asserted_evidence_evidence_multiplicity_matches_uml25 :
    xmlAssertedEvidenceEvidenceMultiplicityFromUML25 = some xmlAssertedEvidenceEvidence := rfl

theorem xml_assertion_declaration_rule_multiplicity_matches_uml25 :
    xmlAssertionDeclarationRuleMultiplicityFromUML25 = some xmlAssertionDeclarationRuleMultiplicity := rfl


end SourceFacts

end GovCheck.Coherence.SACM24
