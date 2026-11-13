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

/-- Only relations with an explicit proof obligation can be operative mappings. -/
inductive MappingCoverage where
  | equivalent
  | soundDirectional
  | partialMapping
  deriving DecidableEq, Repr

/-- Proposals that are useful to retain but cannot yet be consumed as
    established semantic correspondences. They deliberately have no
    SemanticBridge constructor and cannot inhabit EvidenceMapping. -/
inductive MappingProposalDisposition where
  | approximate
  | traceabilityOnly
  | unsupported
  deriving DecidableEq, Repr

/-- A non-operative mapping proposal. This is documentation/triage data,
    not a semantic premise and not an EvidenceMapping. -/
structure MappingProposal where
  sourceModel : ArtifactRef
  targetModel : ArtifactRef
  disposition : MappingProposalDisposition
  relationDescription : String
  declaredLimitations : List String
  transformationIdentity : String
  transformationRevision : String

/-- The formal bridge is indexed only by relations with a corresponding
    machine-checkable obligation. -/
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

/-- A derivation carries an actual Lean proof term of the exact target claim.
    The strings are provenance metadata, not a substitute for the proof term. -/
structure KernelCheckedDerivation (claim : Prop) where
  proof : claim
  premises : List String
  assumptions : List String
  kernelIdentity : String
  kernelVersion : String

/-- Evidence kinds other than theoremProof, so the transport constructor
    cannot be instantiated with a theorem-proof label. -/
abbrev NonTheoremEvidenceKind := { kind : EvidenceKind // kind ≠ .theoremProof }

/-- A target theorem-proof kind always requires a proof term of the exact
    target proposition. Other epistemic kinds may be transported unchanged.
    In particular, an existing theoremProof label cannot be transported by
    this rule without re-establishing the target proposition. -/
inductive KindMappingRule (targetClaim : Prop) :
    EvidenceKind → EvidenceKind → Type where
  | transport (kind : NonTheoremEvidenceKind) :
      KindMappingRule targetClaim kind.val kind.val
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

/-- An operative, proof-carrying mapping contract.

    The target status is intentionally not forced to equal the source status:
    a new theorem derivation has its own result. Method class, epistemic kind,
    result status and acceptance remain distinct dimensions. Approximate,
    traceability-only and unsupported proposals are represented separately
    by MappingProposal and cannot inhabit this type.
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
    ∃ derivation : KernelCheckedDerivation targetClaim,
      derivation.proof = derivation.proof := by
  cases rule with
  | transport kind =>
      exact False.elim (kind.property h)
  | deriveTheoremProof derivation =>
      exact ⟨derivation, rfl⟩

theorem mapping_target_theorem_proof_requires_derivation
    {source target : MappingSubject} (mapping : EvidenceMapping source target)
    (h : target.evidence.kind = .theoremProof) :
    ∃ derivation : KernelCheckedDerivation target.claim.meaning,
      derivation.proof = derivation.proof :=
  kind_mapping_rule_theorem_proof_requires_derivation mapping.kindRule h

end GovCheck.Coherence
