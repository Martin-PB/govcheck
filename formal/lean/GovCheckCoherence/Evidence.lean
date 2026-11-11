/-
GovCheck metamodel coherence prototype — evidence epistemics slice.

The vocabulary is aligned with the existing formal/schemas/evidence-record.schema.json:
methodClass and result.status are separate source dimensions. Epistemic kind is
kept explicit because a method label alone must not authenticate a derivation.
This first module deliberately has no CSLib imports; candidate imports require
a separate fit and trusted-base audit.
-/

namespace GovCheck.Coherence

/-- Method classes currently defined by GovCheck's evidence-record schema. -/
inductive EvidenceMethodClass where
  | empiricalExecution
  | modelChecking
  | programVerification
  | theoremProving
  | implementationConformance
  | normativeFidelity
  | acceptance
  deriving DecidableEq, Repr

/-- Epistemic nature of the resulting record; these are not a total ranking. -/
inductive EvidenceKind where
  | testimony
  | modelCheckingResult
  | programVerificationResult
  | theoremProof
  | inspection
  | observation
  | other
  deriving DecidableEq, Repr

/-- Result statuses aligned with evidence-record.schema.json.
Freshness (including staleness) is computed separately from result status. -/
inductive EvidenceStatus where
  | notRun
  | notApplicable
  | unsupported
  | incomplete
  | failed
  | passed
  | inconclusive
  deriving DecidableEq, Repr

/-- Minimal record for the first semantic slice. -/
structure EvidenceRecord where
  methodClass : EvidenceMethodClass
  kind : EvidenceKind
  status : EvidenceStatus
  deriving DecidableEq, Repr

/-- Pure transport/mapping only re-expresses the record. -/
def transport (record : EvidenceRecord) : EvidenceRecord := record

/-- Transport preserves the method class, epistemic kind and result status. -/
theorem transport_preserves_method_class (record : EvidenceRecord) :
    (transport record).methodClass = record.methodClass := by
  rfl

theorem transport_preserves_kind (record : EvidenceRecord) :
    (transport record).kind = record.kind := by
  rfl

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

/-- A passed empirical test remains testimony and cannot become a theorem
proof merely by translation. -/
theorem testimony_cannot_be_promoted_by_transport :
    ¬ admissibleTargetKind .testimony .theoremProof .carried := by
  simp [admissibleTargetKind]

/-- A model-checking result cannot become a theorem proof by transport alone. -/
theorem model_checking_cannot_be_promoted_by_transport :
    ¬ admissibleTargetKind .modelCheckingResult .theoremProof .carried := by
  simp [admissibleTargetKind]

/-- A theorem-proof record may be carried as such. This does not authenticate
its source proof or establish freshness; those are separate obligations. -/
theorem theorem_proof_may_be_carried :
    admissibleTargetKind .theoremProof .theoremProof .carried := by
  simp [admissibleTargetKind]

/-- A new theorem-proof target requires an explicitly identified
kernel-checked derivation. A later refinement must bind the derivation to
exact premises, conclusion, assumptions and kernel identity. -/
theorem new_theorem_proof_requires_kernel_derivation
    (source : EvidenceKind) :
    admissibleTargetKind source .theoremProof .kernelChecked := by
  simp [admissibleTargetKind]

/-- A passing empirical execution remains testimony, not a theorem proof. -/
def passingTestimony : EvidenceRecord :=
  ⟨.empiricalExecution, .testimony, .passed⟩

theorem passing_testimony_is_not_a_theorem_proof :
    passingTestimony.kind ≠ .theoremProof := by
  decide

/-- The schema's theorem-proving method label alone does not establish that a
kernel-checked derivation was supplied. The epistemic kind is explicit. -/
def unverifiedTheoremProvingReport : EvidenceRecord :=
  ⟨.theoremProving, .testimony, .passed⟩

theorem theorem_proving_label_alone_does_not_authenticate_proof :
    unverifiedTheoremProvingReport.kind ≠ .theoremProof := by
  decide

end GovCheck.Coherence
