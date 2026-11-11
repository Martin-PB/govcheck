/-
GovCheck metamodel coherence prototype — evidence epistemics slice.

This module intentionally has no CSLib imports in its first iteration.
The goal is to make the smallest semantic boundary kernel-checkable before
introducing external definitions. The absence of external imports is not a
claim that CSLib is unsuitable; imports require a separate trust/fit audit.
-/

namespace GovCheck.Coherence

/-- Evidence methods answer different questions; this is not an assurance ranking. -/
inductive EvidenceKind where
  | testimony
  | modelChecking
  | programVerification
  | theoremProof
  | inspection
  | observation
  | other
  deriving DecidableEq, Repr

/-- Outcome status is independent of the method used to obtain it. -/
inductive EvidenceStatus where
  | notRun
  | notApplicable
  | unsupported
  | incomplete
  | failed
  | passed
  | inconclusive
  | stale
  deriving DecidableEq, Repr

/-- Minimal record used by this first semantic slice. -/
structure EvidenceRecord where
  kind : EvidenceKind
  status : EvidenceStatus
  deriving DecidableEq, Repr

/-- A pure transport/mapping operation only re-expresses a record. -/
def transport (record : EvidenceRecord) : EvidenceRecord := record

/-- Transport preserves the evidence method class. -/
theorem transport_preserves_kind (record : EvidenceRecord) :
    (transport record).kind = record.kind := by
  rfl

/-- Transport preserves the result status without inferring it from the method. -/
theorem transport_preserves_status (record : EvidenceRecord) :
    (transport record).status = record.status := by
  rfl

/-- A proof transfer is either already a theorem-proof record or a new
kernel-checked derivation is explicitly supplied. -/
inductive DerivationOrigin where
  | carried
  | kernelChecked
  deriving DecidableEq, Repr

def admissibleTargetKind
    (source target : EvidenceKind) (origin : DerivationOrigin) : Prop :=
  match target with
  | .theoremProof =>
      source = .theoremProof ∨ origin = .kernelChecked
  | _ => True

/-- A test testimony cannot become a theorem proof by transport alone. -/
theorem testimony_cannot_be_promoted_by_transport :
    ¬ admissibleTargetKind .testimony .theoremProof .carried := by
  simp [admissibleTargetKind]

/-- A model-checking result cannot become a theorem proof by transport alone. -/
theorem model_checking_cannot_be_promoted_by_transport :
    ¬ admissibleTargetKind .modelChecking .theoremProof .carried := by
  simp [admissibleTargetKind]

/-- A theorem-proof record may be carried as such, but this proposition does
not authenticate the source proof or establish freshness. Those are separate
obligations for a later layer. -/
theorem theorem_proof_may_be_carried :
    admissibleTargetKind .theoremProof .theoremProof .carried := by
  simp [admissibleTargetKind]

/-- A new theorem-proof claim requires an explicitly identified kernel-checked
derivation. This predicate records the gate; a later module must bind the
derivation to exact premises, conclusion, assumptions and kernel identity. -/
theorem new_theorem_proof_requires_kernel_derivation
    (source : EvidenceKind) :
    admissibleTargetKind source .theoremProof .kernelChecked := by
  simp [admissibleTargetKind]

/-- Passing status does not change the evidence method class. -/
def passingTestimony : EvidenceRecord :=
  ⟨.testimony, .passed⟩

theorem passing_testimony_is_not_a_theorem_proof :
    passingTestimony.kind ≠ .theoremProof := by
  decide

end GovCheck.Coherence
