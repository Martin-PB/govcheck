import GovCheckCoherence.Evidence

namespace GovCheck.Coherence

/-- Stable identity and exact revision of a native source artifact. -/
structure ArtifactRef where
  identity : String
  revision : String
  nativeFormat : String
  semanticProfile : String
  deriving DecidableEq, Repr

/-- A claim interpretation binds a stable source identifier to a Lean proposition. -/
structure ClaimSemantics where
  claimId : String
  meaning : Prop

/-- Evidence plus the semantic/provenance context required to map it. -/
structure MappingSubject where
  evidence : EvidenceRecord
  claim : ClaimSemantics
  artifact : ArtifactRef
  model : ArtifactRef
  scope : String
  assumptions : List String

/-- Coverage is explicit; it is not reduced to a Boolean valid/invalid flag. -/
inductive MappingCoverage where
  | equivalent
  | soundDirectional
  | partialMapping
  | approximate
  | traceabilityOnly
  | unsupported
  deriving DecidableEq, Repr

/-- The formal bridge obligation depends on the declared mapping coverage. -/
inductive SemanticBridge : Prop → Prop → MappingCoverage → Type where
  | equivalent {source target : Prop} :
      (source ↔ target) →
      SemanticBridge source target .equivalent
  | soundDirectional {source target : Prop} :
      (source → target) →
      SemanticBridge source target .soundDirectional
  | partialMapping {source target : Prop} :
      (domain : source → Prop) →
      (∀ h : source, domain h → target) →
      SemanticBridge source target .partialMapping
  | approximate {source target : Prop} :
      (relation : source → target → Prop) →
      (declaredLimitations : List String) →
      SemanticBridge source target .approximate
  | traceabilityOnly {source target : Prop} :
      SemanticBridge source target .traceabilityOnly
  | unsupported {source target : Prop} :
      SemanticBridge source target .unsupported

/-- A derivation carries an actual Lean proof term of the exact target claim.
    Metadata alone cannot construct this value. -/
structure KernelCheckedDerivation (claim : Prop) where
  proof : claim
  premises : List String
  assumptions : List String
  kernelIdentity : String
  kernelVersion : String

/-- Transport preserves epistemic kind. A new theorem-proof kind requires a
    kernel-checked proof of the target claim, not merely a method/status label. -/
inductive KindMappingRule (targetClaim : Prop) :
    EvidenceKind → EvidenceKind → Type where
  | transport (kind : EvidenceKind) :
      KindMappingRule targetClaim kind kind
  | deriveTheoremProof (sourceKind : EvidenceKind)
      (derivation : KernelCheckedDerivation targetClaim) :
      KindMappingRule targetClaim sourceKind .theoremProof

/-- A typed contract between exact source and target model revisions. -/
structure MappingContract where
  sourceModel : ArtifactRef
  targetModel : ArtifactRef
  coverage : MappingCoverage
  assumptions : List String
  declaredLosses : List String
  transformationIdentity : String
  transformationRevision : String

/-- A proof-carrying mapping contract.

    The target status is intentionally not forced to equal the source status:
    a new theorem derivation has its own result. Method class, epistemic kind,
    result status and acceptance remain distinct dimensions.
-/
structure EvidenceMapping (source target : MappingSubject) where
  contract : MappingContract
  sourceModelMatches : contract.sourceModel = source.model
  targetModelMatches : contract.targetModel = target.model
  semanticBridge :
    SemanticBridge source.claim.meaning target.claim.meaning contract.coverage
  methodClassPreserved :
    target.evidence.methodClass = source.evidence.methodClass
  kindRule :
    KindMappingRule target.claim.meaning source.evidence.kind target.evidence.kind
  sourceArtifactIdentityPreserved :
    target.artifact.identity = source.artifact.identity
  sourceArtifactRevisionPreserved :
    target.artifact.revision = source.artifact.revision
  scopePreserved :
    target.scope = source.scope
  assumptionsPreserved :
    ∀ assumption, assumption ∈ source.assumptions →
      assumption ∈ target.assumptions

theorem mapping_preserves_source_revision
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.artifact.revision = source.artifact.revision :=
  mapping.sourceArtifactRevisionPreserved

theorem mapping_preserves_source_identity
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.artifact.identity = source.artifact.identity :=
  mapping.sourceArtifactIdentityPreserved

theorem mapping_preserves_scope
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.scope = source.scope :=
  mapping.scopePreserved

theorem mapping_preserves_assumptions
    {source target : MappingSubject} (mapping : EvidenceMapping source target)
    (assumption : String) (h : assumption ∈ source.assumptions) :
    assumption ∈ target.assumptions :=
  mapping.assumptionsPreserved assumption h

theorem mapping_preserves_method_class
    {source target : MappingSubject} (mapping : EvidenceMapping source target) :
    target.evidence.methodClass = source.evidence.methodClass :=
  mapping.methodClassPreserved

theorem kind_mapping_rule_theorem_proof_requires_derivation
    {targetClaim : Prop} {source target : EvidenceKind}
    (rule : KindMappingRule targetClaim source target)
    (h : target = .theoremProof) :
    source = .theoremProof ∨
      (∃ derivation : KernelCheckedDerivation targetClaim, derivation.proof = derivation.proof) := by
  cases rule with
  | transport => exact Or.inl h
  | deriveTheoremProof derivation =>
      exact Or.inr ⟨derivation, rfl⟩

theorem mapping_target_theorem_proof_requires_derivation
    {source target : MappingSubject} (mapping : EvidenceMapping source target)
    (h : target.evidence.kind = .theoremProof) :
    source.evidence.kind = .theoremProof ∨
      (∃ derivation : KernelCheckedDerivation target.claim.meaning, derivation.proof = derivation.proof) :=
  kind_mapping_rule_theorem_proof_requires_derivation mapping.kindRule h

end GovCheck.Coherence
