--------------------------- MODULE GovCheckLifecycle ---------------------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Actors, AuthorizedActors, RequiredApprovals,
  Bases, Candidates, Governances, Specs, Obligations,
  Pass, Fail, Unknown, None, HistoryLimit

ASSUME AuthorizedActors \subseteq Actors
ASSUME RequiredApprovals \in Nat
ASSUME RequiredApprovals <= Cardinality(AuthorizedActors)
ASSUME HistoryLimit >= 1
ASSUME Pass # Fail
ASSUME Pass # Unknown
ASSUME Fail # Unknown

Phases ==
  {"Proposed", "Prepared", "Evaluated", "Reviewable", "Accepted",
   "Applied", "Rejected", "Withdrawn", "Superseded", "Stale"}

Outcomes == {Pass, Fail, Unknown}
TerminalPhases == {"Applied", "Rejected", "Withdrawn", "Superseded"}

VARIABLES
  phase, baseId, candidateId, governanceId, specId,
  evaluatedTuple, outcomes, evidence, approvals,
  acceptedTuple, appliedCandidateId, history

vars ==
  <<phase, baseId, candidateId, governanceId, specId,
    evaluatedTuple, outcomes, evidence, approvals,
    acceptedTuple, appliedCandidateId, history>>

CurrentTuple ==
  <<baseId, candidateId, governanceId, specId>>

Init ==
  /\ phase = "Proposed"
  /\ baseId \in Bases
  /\ candidateId \in Candidates
  /\ governanceId \in Governances
  /\ specId \in Specs
  /\ evaluatedTuple = None
  /\ outcomes = [o \in Obligations |-> Unknown]
  /\ evidence = {}
  /\ approvals = {}
  /\ acceptedTuple = None
  /\ appliedCandidateId = None
  /\ history = <<"Created">>

Prepare ==
  /\ Len(history) < HistoryLimit
  /\ phase = "Proposed"
  /\ phase' = "Prepared"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Prepared")

PublishEvidence(obligation) ==
  /\ Len(history) < HistoryLimit
  /\ phase \in {"Prepared", "Evaluated", "Reviewable"}
  /\ obligation \in Obligations
  /\ evidence' = evidence \cup {obligation}
  /\ phase' = "Prepared"
  /\ evaluatedTuple' = None
  /\ outcomes' = [o \in Obligations |-> Unknown]
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 approvals, acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "EvidencePublished")

Evaluate ==
  /\ Len(history) < HistoryLimit
  /\ phase \in {"Prepared", "Evaluated", "Reviewable", "Stale"}
  /\ evaluatedTuple' = CurrentTuple
  /\ outcomes' = [o \in Obligations |->
                    IF o \in evidence THEN Pass ELSE Unknown]
  /\ phase' = IF evidence = Obligations THEN "Reviewable" ELSE "Evaluated"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evidence, approvals, acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Evaluated")

Approve(actor) ==
  /\ Len(history) < HistoryLimit
  /\ phase = "Reviewable"
  /\ actor \in AuthorizedActors
  /\ evaluatedTuple = CurrentTuple
  /\ approvals' = approvals \cup {actor}
  /\ UNCHANGED <<phase, baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Approved")

Accept ==
  /\ Len(history) < HistoryLimit
  /\ phase = "Reviewable"
  /\ evaluatedTuple = CurrentTuple
  /\ outcomes = [o \in Obligations |-> Pass]
  /\ Cardinality(approvals) >= RequiredApprovals
  /\ phase' = "Accepted"
  /\ acceptedTuple' = CurrentTuple
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 appliedCandidateId>>
  /\ history' = Append(history, "Accepted")

Apply ==
  /\ Len(history) < HistoryLimit
  /\ phase = "Accepted"
  /\ acceptedTuple = CurrentTuple
  /\ acceptedTuple[2] = candidateId
  /\ phase' = "Applied"
  /\ appliedCandidateId' = candidateId
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals, acceptedTuple>>
  /\ history' = Append(history, "Applied")

ChangeInputs(newBase, newCandidate, newGovernance, newSpec) ==
  /\ Len(history) < HistoryLimit
  /\ phase \notin TerminalPhases
  /\ newBase \in Bases
  /\ newCandidate \in Candidates
  /\ newGovernance \in Governances
  /\ newSpec \in Specs
  /\ <<newBase, newCandidate, newGovernance, newSpec>> # CurrentTuple
  /\ baseId' = newBase
  /\ candidateId' = newCandidate
  /\ governanceId' = newGovernance
  /\ specId' = newSpec
  /\ phase' = "Stale"
  /\ evaluatedTuple' = None
  /\ outcomes' = [o \in Obligations |-> Unknown]
  /\ evidence' = {}
  /\ approvals' = {}
  /\ acceptedTuple' = None
  /\ appliedCandidateId' = None
  /\ history' = Append(history, "InputsChanged")

Reject ==
  /\ Len(history) < HistoryLimit
  /\ phase \notin TerminalPhases
  /\ phase' = "Rejected"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Rejected")

Withdraw ==
  /\ Len(history) < HistoryLimit
  /\ phase \notin TerminalPhases
  /\ phase' = "Withdrawn"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Withdrawn")

Supersede ==
  /\ Len(history) < HistoryLimit
  /\ phase \notin TerminalPhases
  /\ phase' = "Superseded"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Superseded")

Next ==
  \/ Prepare
  \/ \E obligation \in Obligations : PublishEvidence(obligation)
  \/ Evaluate
  \/ \E actor \in AuthorizedActors : Approve(actor)
  \/ Accept
  \/ Apply
  \/ \E b \in Bases, c \in Candidates, g \in Governances, s \in Specs :
       ChangeInputs(b, c, g, s)
  \/ Reject
  \/ Withdraw
  \/ Supersede

TypeOK ==
  /\ phase \in Phases
  /\ baseId \in Bases
  /\ candidateId \in Candidates
  /\ governanceId \in Governances
  /\ specId \in Specs
  /\ evaluatedTuple \in {None} \cup
       (Bases \X Candidates \X Governances \X Specs)
  /\ outcomes \in [Obligations -> Outcomes]
  /\ evidence \subseteq Obligations
  /\ approvals \subseteq AuthorizedActors
  /\ acceptedTuple \in {None} \cup
       (Bases \X Candidates \X Governances \X Specs)
  /\ appliedCandidateId \in {None} \cup Candidates
  /\ history \in Seq(STRING)
  /\ Len(history) <= HistoryLimit

AcceptanceSoundness ==
  phase = "Accepted" =>
    /\ acceptedTuple = CurrentTuple
    /\ evaluatedTuple = CurrentTuple
    /\ outcomes = [o \in Obligations |-> Pass]
    /\ Cardinality(approvals) >= RequiredApprovals

ApplicationSoundness ==
  phase = "Applied" =>
    /\ acceptedTuple = CurrentTuple
    /\ appliedCandidateId = acceptedTuple[2]
    /\ appliedCandidateId = candidateId

NoStaleEvaluation ==
  phase \in {"Reviewable", "Accepted", "Applied"} =>
    evaluatedTuple = CurrentTuple

EvidenceBinding ==
  phase = "Reviewable" =>
    /\ evaluatedTuple = CurrentTuple
    /\ evidence = Obligations

ApprovalBinding ==
  phase \in {"Accepted", "Applied"} =>
    approvals \subseteq AuthorizedActors

NoImplicitApplication ==
  phase # "Applied" => appliedCandidateId = None

TerminalDiscipline ==
  phase \in TerminalPhases =>
    phase' = phase

HistoryNonEmpty == Len(history) >= 1

Spec == Init /\ [][Next]_vars

THEOREM Spec => []TypeOK
THEOREM Spec => []AcceptanceSoundness
THEOREM Spec => []ApplicationSoundness
THEOREM Spec => []NoStaleEvaluation
THEOREM Spec => []EvidenceBinding
THEOREM Spec => []ApprovalBinding
THEOREM Spec => []NoImplicitApplication
THEOREM Spec => []HistoryNonEmpty

=============================================================================
