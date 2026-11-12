import GovCheckCoherence.Mapping

namespace GovCheck.Coherence.SACM24

/-- SACM 2.4 Beta 1 AssertionDeclarationKind literals. -/
inductive AssertionDeclarationKind where
  | asserted
  | assumed
  | axiomatic
  | byRule
  deriving DecidableEq, Repr

/-- GovCheck preserves the declaration's nature without treating it as
    evidence method, evidence result, or a theorem-proof status. -/
inductive ClaimDisposition where
  | asserted
  | assumed
  | axiomaticDeclared
  | ruleDeclared
  deriving DecidableEq, Repr

def mapAssertionDeclaration : AssertionDeclarationKind → ClaimDisposition
  | .asserted => .asserted
  | .assumed => .assumed
  | .axiomatic => .axiomaticDeclared
  | .byRule => .ruleDeclared

theorem mapAssertionDeclaration_injective :
    Function.Injective mapAssertionDeclaration := by
  intro a b h
  cases a <;> cases b <;> simp_all [mapAssertionDeclaration]

theorem sacm_axiomatic_remains_declaration :
    mapAssertionDeclaration .axiomatic = .axiomaticDeclared := rfl

theorem sacm_assumed_remains_assumption :
    mapAssertionDeclaration .assumed = .assumed := rfl

/-- Optional source subject reference. SACM 2.4 Beta 1 issue SACM24-83
    introduces SACMElement as a possible explicit subject of a Claim. -/
structure SACMElementRef where
  identity : String
  metaclass : String
  modelRevision : String
  deriving DecidableEq, Repr

/-- Minimal Claim/Assertion slice: textual value and optional subject are
    retained separately from the formal proposition used by a bridge. -/
structure SACMClaim where
  identity : String
  value : Option String
  subject : Option SACMElementRef
  declaration : AssertionDeclarationKind
  isTrue : Option Bool
  assertionValue : Option String
  assertionRule : Option String
  deriving DecidableEq, Repr

/-- The proposition is an explicit interpretation supplied by a mapping
    authority. SACM text is not silently parsed into Lean truth. -/
structure SACMClaimInterpretation
    (claim : SACMClaim) (target : ClaimSemantics) where
  targetModel : ArtifactRef
  mappedSubject : Option SACMElementRef
  claimIdentityPreserved : target.claimId = claim.identity
  subjectPreserved : mappedSubject = claim.subject
  subjectRevisionMatchesModel :
    ∀ subject, mappedSubject = some subject →
      subject.modelRevision = targetModel.revision
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
  | collective proof => exact proof

end GovCheck.Coherence.SACM24
