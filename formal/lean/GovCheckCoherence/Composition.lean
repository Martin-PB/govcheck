import GovCheckCoherence.Mapping

namespace GovCheck.Coherence

/-- Compose two proposition-level semantic bridges.

    Total bridges compose to a total bridge. Equivalence is retained only when
    both inputs are equivalences; otherwise the strongest justified total
    result is sound-directional. If either input is partial, the result remains
    partial. Two partial bridges compose over the explicitly witnessed
    intersection of their domains. -/
def composeSemanticBridges
    {source middle target : Prop}
    {firstCoverage secondCoverage : MappingCoverage}
    (first : SemanticBridge source middle firstCoverage)
    (second : SemanticBridge middle target secondCoverage) :
    Σ coverage : MappingCoverage, SemanticBridge source target coverage := by
  cases first with
  | equivalent firstForward =>
    cases second with
    | equivalent secondForward =>
        exact ⟨.equivalent, .equivalent (Iff.trans firstForward secondForward)⟩
    | soundDirectional secondForward =>
        exact ⟨.soundDirectional,
          .soundDirectional (fun sourceProof => secondForward (firstForward.mp sourceProof))⟩
    | partialMapping secondDomain secondProof =>
        exact ⟨.partialMapping,
          .partialMapping
            (fun sourceProof => secondDomain (firstForward.mp sourceProof))
            (by
              intro sourceProof domainProof
              exact secondProof (firstForward.mp sourceProof) domainProof)⟩
  | soundDirectional firstForward =>
    cases second with
    | equivalent secondForward =>
        exact ⟨.soundDirectional,
          .soundDirectional (fun sourceProof => secondForward.mp (firstForward sourceProof))⟩
    | soundDirectional secondForward =>
        exact ⟨.soundDirectional,
          .soundDirectional (fun sourceProof => secondForward (firstForward sourceProof))⟩
    | partialMapping secondDomain secondProof =>
        exact ⟨.partialMapping,
          .partialMapping
            (fun sourceProof => secondDomain (firstForward sourceProof))
            (by
              intro sourceProof domainProof
              exact secondProof (firstForward sourceProof) domainProof)⟩
  | partialMapping firstDomain firstProof =>
    cases second with
    | equivalent secondForward =>
        exact ⟨.partialMapping,
          .partialMapping firstDomain
            (by
              intro sourceProof domainProof
              exact secondForward.mp (firstProof sourceProof domainProof))⟩
    | soundDirectional secondForward =>
        exact ⟨.partialMapping,
          .partialMapping firstDomain
            (by
              intro sourceProof domainProof
              exact secondForward (firstProof sourceProof domainProof))⟩
    | partialMapping secondDomain secondProof =>
        let composedDomain : source → Prop :=
          fun sourceProof =>
            ∃ firstDomainProof : firstDomain sourceProof,
              secondDomain (firstProof sourceProof firstDomainProof)
        exact ⟨.partialMapping,
          .partialMapping composedDomain
            (by
              intro sourceProof domainProof
              rcases domainProof with ⟨firstDomainProof, secondDomainProof⟩
              exact secondProof
                (firstProof sourceProof firstDomainProof)
                secondDomainProof)⟩

/-- Composition may retain equivalence only when both input bridges are
    equivalences. A one-way or partial relation is never upgraded merely by
    composition. -/
theorem compose_equivalent_iff_both_equivalent
    {source middle target : Prop}
    {firstCoverage secondCoverage : MappingCoverage}
    (first : SemanticBridge source middle firstCoverage)
    (second : SemanticBridge middle target secondCoverage) :
    (composeSemanticBridges first second).1 = .equivalent ↔
      firstCoverage = .equivalent ∧ secondCoverage = .equivalent := by
  cases first <;> cases second <;> simp [composeSemanticBridges]

/-- A partial first bridge keeps the composite partial, regardless of the
    coverage of the second bridge. -/
theorem compose_partial_first_remains_partial
    {source middle target : Prop}
    {secondCoverage : MappingCoverage}
    (first : SemanticBridge source middle .partialMapping)
    (second : SemanticBridge middle target secondCoverage) :
    (composeSemanticBridges first second).1 = .partialMapping := by
  cases first <;> cases second <;> rfl

/-- A partial second bridge keeps the composite partial, regardless of the
    coverage of the first bridge. -/
theorem compose_partial_second_remains_partial
    {source middle target : Prop}
    {firstCoverage : MappingCoverage}
    (first : SemanticBridge source middle firstCoverage)
    (second : SemanticBridge middle target .partialMapping) :
    (composeSemanticBridges first second).1 = .partialMapping := by
  cases first <;> cases second <;> rfl

end GovCheck.Coherence
