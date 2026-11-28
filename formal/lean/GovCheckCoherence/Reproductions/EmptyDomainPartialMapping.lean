import GovCheckCoherence.Mapping

namespace GovCheck.Coherence.Reproductions

/--
Known limitation reproduced for external critique #129, finding 6.6.

The source proposition is inhabited (True), the target is uninhabited (False),
but the partial-mapping domain is empty. The constructor still produces a
SemanticBridge because the current contract does not require domain coverage
to be inhabited. This is a counterexample to the intended coverage guarantee,
not an axiom and not a normative decision about the eventual mapping contract.
-/
def emptyDomainPartialBridge : SemanticBridge True False .partialMapping :=
  SemanticBridge.partialMapping
    (fun _ : True => False)
    (by
      intro _ impossible
      exact False.elim impossible)

#check emptyDomainPartialBridge

end GovCheck.Coherence.Reproductions
