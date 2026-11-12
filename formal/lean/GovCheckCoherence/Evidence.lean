/- 
GovCheck metamodel coherence prototype — evidence semantic vocabulary.

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

/-- Result statuses aligned with evidence-record.schema.json, including `unknown`.
Freshness (including staleness) is computed separately from result status. -/
inductive EvidenceStatus where
  | notRun
  | notApplicable
  | unsupported
  | incomplete
  | failed
  | passed
  | inconclusive
  | unknown
  deriving DecidableEq, Repr

/-- Minimal record for the first semantic slice. -/
structure EvidenceRecord where
  methodClass : EvidenceMethodClass
  kind : EvidenceKind
  status : EvidenceStatus
  deriving DecidableEq, Repr

/-- Pure transport/mapping only re-expresses the record. -/
def transport (record : EvidenceRecord) : EvidenceRecord := record

/-- A proof transfer is either already a theorem-proof record or a new
kernel-checked derivation is explicitly supplied. -/
inductive DerivationOrigin where
  | carried
  | kernelChecked
  deriving DecidableEq, Repr

def admissibleTargetKind
    (source target : EvidenceKind) (origin : DerivationOrigin) : Prop :=
  target ≠ .theoremProof ∨
    source = .theoremProof ∨ origin = .kernelChecked

/-- A passing empirical execution remains testimony, not a theorem proof. -/
def passingTestimony : EvidenceRecord :=
  ⟨.empiricalExecution, .testimony, .passed⟩

/-- The schema's theorem-proving method label alone does not establish that a
kernel-checked derivation was supplied. The epistemic kind is explicit. -/
def unverifiedTheoremProvingReport : EvidenceRecord :=
  ⟨.theoremProving, .testimony, .passed⟩

end GovCheck.Coherence
