import Cslib.Logics.BTL.Basic
import Cslib.Foundations.Data.OmegaSequence.Temporal

/-!
This isolated package checks that GovCheck can consume the inspected CSLib
formalizations without upgrading the Lean 4.19 epistemic core. It is a
compatibility probe, not yet a semantic refinement proof.
-/

#check Cslib.Logic.Modal.BTL.Model
#check Cslib.Logic.Modal.Satisfies.btl_future_always_iff
#check Cslib.ωSequence.Step
#check Cslib.ωSequence.LeadsTo
