import GovCheckCoherence.Evidence
import Cslib.Foundations.Semantics.LTS.Basic

namespace GovCheck.Coherence

/-- Freshness is separate from the evidence result status. -/
inductive EvidenceFreshness where
  | current
  | stale
  deriving DecidableEq, Repr

/-- Minimal lifecycle state for the CSLib LTS integration experiment. -/
structure EvidenceLifecycleState where
  evidence : EvidenceRecord
  freshness : EvidenceFreshness
  deriving DecidableEq, Repr

/-- Lifecycle events affect status/freshness, never method class or epistemic kind. -/
inductive EvidenceLifecycleEvent where
  | reportResult (status : EvidenceStatus)
  | dependencyChanged
  | revalidated
  deriving DecidableEq, Repr

/-- A labelled transition system for evidence lifecycle changes. -/
def evidenceLifecycle : Cslib.LTS EvidenceLifecycleState EvidenceLifecycleEvent where
  Tr before event after :=
    before.evidence.methodClass = after.evidence.methodClass ∧
    before.evidence.kind = after.evidence.kind ∧
    match event with
    | .reportResult status =>
        after.evidence.status = status ∧ after.freshness = .current
    | .dependencyChanged =>
        before.freshness = .current ∧
        after.evidence.status = before.evidence.status ∧
        after.freshness = .stale
    | .revalidated =>
        before.freshness = .stale ∧
        after.evidence.status = before.evidence.status ∧
        after.freshness = .current

end GovCheck.Coherence
