--------------------------- MODULE GovCheckLifecycle ---------------------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Actors, AuthorizedActors, RequiredApprovals,
  Bases, Candidates, Governances, Specs, Obligations,
  Pass, Fail, Unknown, None

ASSUME AuthorizedActors \subseteq Actors
ASSUME RequiredApprovals \in Nat
ASSUME RequiredApprovals <= Cardinality(AuthorizedActors)
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
  /\ history = <<[kind |-> "Created", tuple |-> CurrentTuple]>>

Prepare ==
  /\ phase = "Proposed"
  /\ phase' = "Prepared"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, [kind |-> "Prepared", tuple |-> CurrentTuple])

PublishEvidence(obligation) ==
  /\ phase \in {"Prepared", "Evaluated", "Reviewable"}
  /\ obligation \in Obligations
  /\ evidence' = evidence \cup {obligation}
  /\ phase' = "Prepared"
  /\ evaluatedTuple' = None
  /\ outcomes' = [o \in Obligations |-> Unknown]
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 approvals, acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history,
       [kind |-> "EvidencePublished", obligation |-> obligation,
        tuple |-> CurrentTuple])

Evaluate ==
  /\ phase \in {"Prepared", "Evaluated", "Reviewable", "Stale"}
  /\ evaluatedTuple' = CurrentTuple
  /\ outcomes' = [o \in Obligations |->
                    IF o \in evidence THEN Pass ELSE Unknown]
  /\ phase' = IF evidence = Obligations THEN "Reviewable" ELSE "Evaluated"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evidence, approvals, acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, [kind |-> "Evaluated", tuple |-> CurrentTuple])

Approve(actor) ==
  /\ phase = "Reviewable"
  /\ actor \in AuthorizedActors
  /\ evaluatedTuple = CurrentTuple
  /\ approvals' = approvals \cup {actor}
  /\ UNCHANGED <<phase, baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history,
       [kind |-> "Approved", actor |-> actor, tuple |-> CurrentTuple])

Accept ==
  /\ phase = "Reviewable"
  /\ evaluatedTuple = CurrentTuple
  /\ outcomes = [o \in Obligations |-> Pass]
  /\ Cardinality(approvals) >= RequiredApprovals
  /\ phase' = "Accepted"
  /\ acceptedTuple' = CurrentTuple
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 appliedCandidateId>>
  /\ history' = Append(history, [kind |-> "Accepted", tuple |-> CurrentTuple])

Apply ==
  /\ phase = "Accepted"
  /\ acceptedTuple = CurrentTuple
  /\ acceptedTuple[2] = candidateId
  /\ phase' = "Applied"
  /\ appliedCandidateId' = candidateId
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals, acceptedTuple>>
  /\ history' = Append(history,
       [kind |-> "Applied", candidate |-> candidateId, tuple |-> CurrentTuple])

ChangeInputs(newBase, newCandidate, newGovernance, newSpec) ==
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
  /\ history' = Append(history,
       [kind |-> "InputsChanged",
        oldTuple |-> CurrentTuple,
        newTuple |-> <<newBase, newCandidate, newGovernance, newSpec>>])

Reject ==
  /\ phase \notin TerminalPhases
  /\ phase' = "Rejected"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, [kind |-> "Rejected", tuple |-> CurrentTuple])

Withdraw ==
  /\ phase \notin TerminalPhases
  /\ phase' = "Withdrawn"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, [kind |-> "Withdrawn", tuple |-> CurrentTuple])

Supersede ==
  /\ phase \notin TerminalPhases
  /\ phase' = "Superseded"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, [kind |-> "Superseded", tuple |-> CurrentTuple])

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
  /\ history \in Seq([kind : STRING])

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
