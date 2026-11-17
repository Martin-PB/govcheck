import GovCheckCoherence.Composition

namespace GovCheck.Coherence

/-- One exact transformation step. Identity and revision are kept together:
    composition must preserve the ordered provenance chain rather than invent
    a synthetic identifier or revision for a multi-step transformation. -/
structure MappingTransformationStep where
  identity : String
  revision : String
  deriving DecidableEq, Repr

/-- A composed evidence mapping is represented as an ordered chain of the
    original mappings. It is deliberately not collapsed into one
    EvidenceMapping/MappingContract: GovCheck has not yet defined a canonical
    algebra for composing transformation identities, revisions, assumptions
    and loss declarations. -/
structure EvidenceMappingChain (source middle target : MappingSubject) where
  first : EvidenceMapping source middle
  second : EvidenceMapping middle target
  intermediateModelAgreement :
    first.contract.targetModel = second.contract.sourceModel
  semanticCoverage : MappingCoverage
  semanticBridge :
    SemanticBridge source.claim.meaning target.claim.meaning semanticCoverage

/-- Compose two complete EvidenceMapping records while preserving their exact
    intermediate model identity and retaining both transformation/loss/
    assumption declarations as an ordered chain. The returned value is not a
    flattened EvidenceMapping because no canonical flattening rule has been
    adopted for transformation identity or revision. -/
def composeEvidenceMappings
    {source middle target : MappingSubject}
    (first : EvidenceMapping source middle)
    (second : EvidenceMapping middle target) :
    EvidenceMappingChain source middle target := by
  let semantic := composeSemanticBridges first.semanticBridge second.semanticBridge
  exact {
    first := first
    second := second
    intermediateModelAgreement :=
      first.targetModelMatches.trans second.sourceModelMatches.symm
    semanticCoverage := semantic.1
    semanticBridge := semantic.2
  }

/-- The chain is pinned to the exact source and target model revisions. -/
theorem evidence_mapping_chain_binds_endpoint_models
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    chain.first.contract.sourceModel = source.model ∧
      chain.second.contract.targetModel = target.model :=
  ⟨chain.first.sourceModelMatches, chain.second.targetModelMatches⟩

/-- The intermediate model revision must agree exactly; matching only a model
    name or semantic profile is insufficient. -/
theorem evidence_mapping_chain_binds_intermediate_model
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    chain.first.contract.targetModel = chain.second.contract.sourceModel :=
  chain.intermediateModelAgreement

/-- Artifact identity and exact revision are preserved end-to-end. -/
theorem evidence_mapping_chain_preserves_artifact
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    target.artifact.identity = source.artifact.identity ∧
      target.artifact.revision = source.artifact.revision :=
  ⟨chain.second.sourceArtifactIdentityPreserved.trans
      chain.first.sourceArtifactIdentityPreserved,
    chain.second.sourceArtifactRevisionPreserved.trans
      chain.first.sourceArtifactRevisionPreserved⟩

/-- Scope is preserved end-to-end; a mapping chain cannot silently widen or
    narrow the source subject's declared scope. -/
theorem evidence_mapping_chain_preserves_scope
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    target.scope = source.scope :=
  chain.second.scopePreserved.trans chain.first.scopePreserved

/-- Every source assumption remains present after both mapping steps. -/
theorem evidence_mapping_chain_preserves_assumptions
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target)
    (assumption : String) (present : assumption ∈ source.assumptions) :
    assumption ∈ target.assumptions :=
  chain.second.assumptionsPreserved assumption
    (chain.first.assumptionsPreserved assumption present)

/-- The method class is not silently changed at either mapping boundary. -/
theorem evidence_mapping_chain_preserves_method_class
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    target.evidence.methodClass = source.evidence.methodClass :=
  chain.second.methodClassPreserved.trans
    chain.first.methodClassPreserved

/-- A theorem-proof target in a composed chain still requires a kernel-checked
    derivation of the exact final target proposition. -/
theorem evidence_mapping_chain_theorem_proof_requires_derivation
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target)
    (isTheoremProof : target.evidence.kind = .theoremProof) :
    Nonempty (KernelCheckedDerivation target.claim.meaning) :=
  kind_mapping_rule_theorem_proof_requires_derivation chain.second.kindRule isTheoremProof

/-- Declared assumptions from both steps, retained in order. -/
def EvidenceMappingChain.declaredAssumptions
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) : List String :=
  chain.first.contract.assumptions ++ chain.second.contract.assumptions

/-- Loss declarations from both steps, retained in order. -/
def EvidenceMappingChain.declaredLosses
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) : List String :=
  chain.first.contract.declaredLosses ++ chain.second.contract.declaredLosses

/-- Transformation provenance is the ordered pair of exact source steps. -/
def EvidenceMappingChain.transformationSteps
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    List MappingTransformationStep := [
      ⟨chain.first.contract.transformationIdentity,
        chain.first.contract.transformationRevision⟩,
      ⟨chain.second.contract.transformationIdentity,
        chain.second.contract.transformationRevision⟩
    ]

/-- Both assumptions lists are retained in order. -/
theorem evidence_mapping_chain_retains_assumption_declarations
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    chain.declaredAssumptions =
      chain.first.contract.assumptions ++ chain.second.contract.assumptions :=
  rfl

/-- Loss declarations from both steps are retained in order. -/
theorem evidence_mapping_chain_retains_loss_declarations
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    chain.declaredLosses =
      chain.first.contract.declaredLosses ++ chain.second.contract.declaredLosses :=
  rfl

/-- The transformation lineage preserves both exact identities and revisions. -/
theorem evidence_mapping_chain_retains_transformation_lineage
    {source middle target : MappingSubject}
    (chain : EvidenceMappingChain source middle target) :
    chain.transformationSteps = [
      ⟨chain.first.contract.transformationIdentity,
        chain.first.contract.transformationRevision⟩,
      ⟨chain.second.contract.transformationIdentity,
        chain.second.contract.transformationRevision⟩
    ] :=
  rfl

end GovCheck.Coherence

