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
  | empiricalExecution
  | modelChecking
  | programVerification
  | theoremProving
  | implementationConformance
  | normativeFidelity
  | acceptance
  deriving DecidableEq, Repr

/-- Result status is independent of the method used to obtain it. -/
inductive EvidenceStatus where
  | passed
  | failed
  | inconclusive
  | unknown
  | incomplete
  | unsupported
  | notRun
  | notApplicable
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
structure KernelCheckedDerivation (claim : Prop) where
  /-- The actual Lean proof term. The kernel checks this term when the
      declaration is elaborated/compiled; metadata alone cannot inhabit it. -/
  proof : claim
  premises : List String
  assumptions : List String
  kernelIdentity : String
  kernelVersion : String

/-- The mapping rule makes the epistemic boundary explicit. -/
inductive MappingRule : EvidenceKind → EvidenceKind → Type where
  /-- A pure transport/re-expression preserves the evidence method class. -/
  | transport (kind : EvidenceKind) : MappingRule kind kind
  /-- A new theorem-proving result requires an explicit checked derivation. -/
  | deriveTheoremProof (sourceKind : EvidenceKind) (claim : Prop)
      (derivation : KernelCheckedDerivation claim) :
      MappingRule sourceKind EvidenceKind.theoremProving

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
    (rule : MappingRule source EvidenceKind.theoremProving) :
    source = EvidenceKind.theoremProving ∨
      (∃ claim : Prop, ∃ derivation : KernelCheckedDerivation claim, True) := by
  cases rule with
  | transport kind => exact Or.inl rfl
  | deriveTheoremProof sourceKind claim derivation =>
      exact Or.inr ⟨claim, derivation, True.intro⟩

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

/-- A concrete cross-model evidence mapping. The proof fields are obligations
    supplied by the mapping implementation or its formal bridge; without
    them, a value of this type cannot be constructed. Exact scope preservation
    is intentionally conservative in this first slice. -/
structure EvidenceMapping (source target : EvidenceRecord) where
  contract : MappingContract
  methodRule : MappingRule source.kind target.kind
  sourceModelMatches : contract.sourceModel = source.source
  targetModelMatches : contract.targetModel = target.source
  sourceIdentityPreserved : target.source.identity = source.source.identity
  sourceRevisionPreserved : target.source.revision = source.source.revision
  methodPreserved : target.kind = source.kind ∨
    (∃ claim : Prop, ∃ derivation : KernelCheckedDerivation claim, True)
  statusPreserved : target.status = source.status
  scopePreserved : target.scope = source.scope
  assumptionsPreserved :
    ∀ assumption, assumption ∈ source.assumptions →
      assumption ∈ target.assumptions

theorem evidenceMapping_preserves_source_revision
    {source target : EvidenceRecord} (mapping : EvidenceMapping source target) :
    target.source.revision = source.source.revision :=
  mapping.sourceRevisionPreserved

theorem evidenceMapping_preserves_source_identity
    {source target : EvidenceRecord} (mapping : EvidenceMapping source target) :
    target.source.identity = source.source.identity :=
  mapping.sourceIdentityPreserved

theorem evidenceMapping_preserves_status
    {source target : EvidenceRecord} (mapping : EvidenceMapping source target) :
    target.status = source.status :=
  mapping.statusPreserved

theorem evidenceMapping_preserves_scope
    {source target : EvidenceRecord} (mapping : EvidenceMapping source target) :
    target.scope = source.scope :=
  mapping.scopePreserved

theorem evidenceMapping_preserves_assumptions
    {source target : EvidenceRecord} (mapping : EvidenceMapping source target)
    (assumption : String) (h : assumption ∈ source.assumptions) :
    assumption ∈ target.assumptions :=
  mapping.assumptionsPreserved assumption h


end GovCheckEpistemic
