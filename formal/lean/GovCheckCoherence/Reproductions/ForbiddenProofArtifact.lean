namespace GovCheckCoherence.Reproductions

/-- Deliberately hostile fixture: a proof accepted only through sorryAx. -/
theorem sorryInjected : True := by
  sorry

/-- Deliberately hostile fixture: a theorem resting on an unapproved axiom. -/
axiom injectedFalse : False

theorem axiomInjected : False := injectedFalse

#print axioms sorryInjected
#print axioms axiomInjected

end GovCheckCoherence.Reproductions
