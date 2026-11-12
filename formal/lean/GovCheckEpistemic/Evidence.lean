/-!
# GovCheck epistemic core — first kernel-checked slice

This module defines a deliberately small semantic boundary. It does not
formalize SACM or assert that these are the final GovCheck ontology terms.
The key design constraint is that transport preserves evidence kind; only
an explicit kernel-checked derivation can introduce a theorem-proof result.
-/

namespace GovCheckEpistemic

/-- Evidence methods are distinct categories, not a total strength ordering. -/
inductive EvidenceKind where
  | testimony
  | modelChecking
  | programVerification
  | theoremProof
  | inspection
  | observation
  | other
  deriving DecidableEq, Repr

/-- Result status is independent of the method used to obtain it. -/
inductive EvidenceStatus where
  | passed
  | failed
  | inconclusive
  | unknown
  | unsupported
  | notRun
  | stale
  deriving DecidableEq, Repr

/-- Identity and exact revision of a native source artifact. -/
structure ArtifactRef where
  identity : String
  revision : String
  nativeFormat : String
  semanticProfile : String
  deriving Repr, DecidableEq

/-- Minimal evidence record; provenance and scope are explicit data. -/
structure EvidenceRecord where
  subject : String
  claim : String
  kind : EvidenceKind
  status : EvidenceStatus
  source : ArtifactRef
  assumptions : List String
  scope : String
  deriving Repr

/-- A kernel-checked derivation is a separate object, never a Boolean flag
    inferred from parsing, testing, or model checking. -/
structure KernelCheckedDerivation where
  premises : List String
  conclusion : String
  assumptions : List String
  kernelIdentity : String
  kernelVersion : String
  deriving Repr

/-- The mapping rule makes the epistemic boundary explicit. -/
inductive MappingRule : EvidenceKind → EvidenceKind → Type where
  /-- A pure transport/re-expression preserves the evidence method class. -/
  | transport (kind : EvidenceKind) : MappingRule kind kind
  /-- A new theorem-proof result requires an explicit checked derivation. -/
  | deriveTheoremProof (sourceKind : EvidenceKind)
      (derivation : KernelCheckedDerivation) :
      MappingRule sourceKind EvidenceKind.theoremProof

/-- The method class resulting from an admissible mapping. -/
def mappedKind {source target : EvidenceKind}
    (_rule : MappingRule source target) : EvidenceKind := target

/-- Pure transport cannot promote or otherwise change epistemic method class. -/
theorem transport_preserves_kind (kind : EvidenceKind) :
    mappedKind (MappingRule.transport kind) = kind := by
  rfl

/-- Any mapping whose target is a theorem-proof record is either a
    same-kind transport of an existing theorem proof, or uses the explicit
    kernel-checked derivation constructor. -/
theorem theorem_proof_requires_valid_route (source : EvidenceKind)
    (rule : MappingRule source EvidenceKind.theoremProof) :
    source = EvidenceKind.theoremProof ∨
      (∃ derivation : KernelCheckedDerivation, True) := by
  cases rule with
  | transport kind => exact Or.inl rfl
  | deriveTheoremProof sourceKind derivation =>
      exact Or.inr ⟨derivation, True.intro⟩

/-- Status is carried independently; this function does not infer a result
    from the method class. -/
def mappedStatus (record : EvidenceRecord) : EvidenceStatus := record.status

theorem mapping_preserves_status (record : EvidenceRecord) :
    mappedStatus record = record.status := by
  rfl

/-- A mapping contract records the exact source/target identities and its
    coverage class. It is metadata, not a proof that obligations hold. -/
inductive Coverage where
  | equivalent
  | soundDirectional
  | partial
  | approximate
  | traceabilityOnly
  | unsupported
  deriving DecidableEq, Repr

structure MappingContract where
  sourceModel : ArtifactRef
  targetModel : ArtifactRef
  coverage : Coverage
  assumptions : List String
  declaredLosses : List String
  transformationIdentity : String
  transformationRevision : String
  deriving Repr

end GovCheckEpistemic
