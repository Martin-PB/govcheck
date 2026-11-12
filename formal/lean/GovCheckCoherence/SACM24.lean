import GovCheckCoherence.Mapping

namespace GovCheck.Coherence.SACM24

/-- The two conflicting SACM 2.4 Beta 1 source views must remain distinct. -/
inductive SourceView where
  | specificationText
  | normativeMetamodelXML
  deriving DecidableEq, Repr

/-- The PDF text uses gid; the machine-readable metamodel uses elementId. -/
inductive ElementIdentityField where
  | gid
  | elementId
  deriving DecidableEq, Repr

def identityFieldForSourceView : SourceView → ElementIdentityField
  | .specificationText => .gid
  | .normativeMetamodelXML => .elementId

/-- Union of declaration literals found across the two Beta 1 source views. -/
inductive AssertionDeclarationKind where
  | asserted
  | assumed
  | axiomatic
  | needsSupport
  | byRule
  deriving DecidableEq, Repr

/-- GovCheck preserves each declaration literal as a distinct disposition. -/
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

/-- A literal is accepted only against the Beta 1 source view that defines it. -/
def declarationSupportedBySourceView :
    SourceView → AssertionDeclarationKind → Bool
  | .specificationText, .byRule => false
  | .normativeMetamodelXML, .needsSupport => false
  | _, _ => true

theorem text_needsSupport_is_supported :
    declarationSupportedBySourceView .specificationText .needsSupport = true := rfl

theorem text_byRule_is_not_supported :
    declarationSupportedBySourceView .specificationText .byRule = false := rfl

theorem xml_byRule_is_supported :
    declarationSupportedBySourceView .normativeMetamodelXML .byRule = true := rfl

theorem xml_needsSupport_is_not_supported :
    declarationSupportedBySourceView .normativeMetamodelXML .needsSupport = false := rfl

theorem text_identity_field_is_gid :
    identityFieldForSourceView .specificationText = .gid := rfl

theorem xml_identity_field_is_elementId :
    identityFieldForSourceView .normativeMetamodelXML = .elementId := rfl

theorem sacm_axiomatic_remains_declaration :
    mapAssertionDeclaration .axiomatic = .axiomaticDeclared := rfl

theorem sacm_assumed_remains_assumption :
    mapAssertionDeclaration .assumed = .assumed := rfl

/-- Optional source subject reference, including the identity field and exact
    model revision used by the selected source view. -/
structure SACMElementRef where
  identity : String
  identityField : ElementIdentityField
  metaclass : String
  modelRevision : String
  deriving DecidableEq, Repr

/-- Minimal Claim/Assertion slice. Raw values/rule references are retained
    opaquely; they are not full encodings of the SACM value/rule metaclasses. -/
structure SACMClaim where
  identity : String
  identityField : ElementIdentityField
  sourceView : SourceView
  value : Option String
  subject : Option SACMElementRef
  declaration : AssertionDeclarationKind
  isTrue : Option Bool
  assertionValue : Option String
  assertionRule : Option String
  deriving DecidableEq, Repr

/-- The proposition is an explicit interpretation supplied by a mapping
    authority. The source text/value is not silently parsed into Lean truth.
    The constructor obligations reject source-view/literal mismatches. -/
structure SACMClaimInterpretation
    (claim : SACMClaim) (interpretation : ClaimSemantics) where
  sourceModel : ArtifactRef
  mappedSubject : Option SACMElementRef
  disposition : ClaimDisposition
  declarationPreserved : disposition = mapAssertionDeclaration claim.declaration
  declarationConsistentWithSourceView :
    declarationSupportedBySourceView claim.sourceView claim.declaration = true
  identityFieldMatchesSourceView :
    claim.identityField = identityFieldForSourceView claim.sourceView
  claimIdentityPreserved : interpretation.claimId = claim.identity
  subjectPreserved : mappedSubject = claim.subject
  subjectIdentityFieldMatchesSourceView :
    ∀ subject, mappedSubject = some subject →
      subject.identityField = identityFieldForSourceView claim.sourceView
  subjectRevisionMatchesModel :
    ∀ subject, mappedSubject = some subject →
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
    mapping.disposition = mapAssertionDeclaration claim.declaration :=
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

theorem claim_subject_revision_is_pinned
    {claim : SACMClaim} {interpretation : ClaimSemantics}
    (mapping : SACMClaimInterpretation claim interpretation)
    (subject : SACMElementRef) (h : mapping.mappedSubject = some subject) :
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
