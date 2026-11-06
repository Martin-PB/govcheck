--------------------------- MODULE GovCheckLifecycle ---------------------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Actors, AuthorizedActors, RequiredApprovals,
  Bases, Candidates, Governances, Specs, Obligations,
  Pass, Fail, Unknown, Unsupported, NotRun, Incomplete, NoTuple, NoCandidate, HistoryLimit

ASSUME AuthorizedActors \subseteq Actors
ASSUME RequiredApprovals \in Nat
ASSUME RequiredApprovals <= Cardinality(AuthorizedActors)
ASSUME HistoryLimit >= 1
ASSUME Pass # Fail
ASSUME Pass # Unknown
ASSUME Fail # Unknown
ASSUME Cardinality({Pass, Fail, Unknown, Unsupported, NotRun, Incomplete}) = 6

Phases ==
  {"Proposed", "Prepared", "Evaluated", "Reviewable", "Accepted",
   "Applied", "Rejected", "Withdrawn", "Superseded", "Stale"}

Outcomes == {Pass, Fail, Unknown, Unsupported, NotRun, Incomplete}
TerminalPhases == {"Applied", "Rejected", "Withdrawn", "Superseded"}

VARIABLES
  phase, baseId, candidateId, governanceId, specId,
  evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals,
  acceptedTuple, appliedCandidateId, history

vars ==
  <<phase, baseId, candidateId, governanceId, specId,
    evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals,
    acceptedTuple, appliedCandidateId, history>>

CurrentTuple ==
  <<baseId, candidateId, governanceId, specId>>

Init ==
  /\ phase = "Proposed"
  /\ baseId \in Bases
  /\ candidateId \in Candidates
  /\ governanceId \in Governances
  /\ specId \in Specs
  /\ evaluatedTuple = NoTuple
  /\ outcomes = [o \in Obligations |-> Unknown]
  /\ evidence = {}
  /\ evidenceOutcomes = [o \in Obligations |-> Unknown]
  /\ approvals = {}
  /\ acceptedTuple = NoTuple
  /\ appliedCandidateId = NoCandidate
  /\ history = <<"Created">>

Prepare ==
  /\ Len(history) < HistoryLimit
  /\ phase = "Proposed"
  /\ phase' = "Prepared"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Prepared")

PublishEvidence(obligation, outcome) ==
  /\ Len(history) < HistoryLimit
  /\ phase \in {"Prepared", "Evaluated", "Reviewable"}
  /\ obligation \in Obligations
  /\ outcome \in Outcomes
  /\ evidence' = evidence \cup {obligation}
  /\ evidenceOutcomes' = [evidenceOutcomes EXCEPT ![obligation] = outcome]
  /\ phase' = "Prepared"
  /\ evaluatedTuple' = NoTuple
  /\ outcomes' = [o \in Obligations |-> Unknown]
  /\ approvals' = {}
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "EvidencePublished")

Evaluate ==
  /\ Len(history) < HistoryLimit
  /\ phase \in {"Prepared", "Evaluated", "Reviewable", "Stale"}
  /\ evaluatedTuple' = CurrentTuple
  /\ outcomes' = [o \in Obligations |->
                    IF o \in evidence THEN evidenceOutcomes[o] ELSE Unknown]
  /\ phase' = IF evidence = Obligations /\
                    outcomes' = [o \in Obligations |-> Pass]
                 THEN "Reviewable" ELSE "Evaluated"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evidence, evidenceOutcomes, approvals, acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Evaluated")

Approve(actor) ==
  /\ Len(history) < HistoryLimit
  /\ phase = "Reviewable"
  /\ actor \in AuthorizedActors
  /\ evaluatedTuple = CurrentTuple
  /\ approvals' = approvals \cup {actor}
  /\ UNCHANGED <<phase, baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, evidenceOutcomes,
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
                 evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals,
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
                 evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals, acceptedTuple>>
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
  /\ evaluatedTuple' = NoTuple
  /\ outcomes' = [o \in Obligations |-> Unknown]
  /\ evidence' = {}
  /\ evidenceOutcomes' = [o \in Obligations |-> Unknown]
  /\ approvals' = {}
  /\ acceptedTuple' = NoTuple
  /\ appliedCandidateId' = NoCandidate
  /\ history' = Append(history, "InputsChanged")

Reject ==
  /\ Len(history) < HistoryLimit
  /\ phase \notin TerminalPhases
  /\ phase' = "Rejected"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Rejected")

Withdraw ==
  /\ Len(history) < HistoryLimit
  /\ phase \notin TerminalPhases
  /\ phase' = "Withdrawn"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Withdrawn")

Supersede ==
  /\ Len(history) < HistoryLimit
  /\ phase \notin TerminalPhases
  /\ phase' = "Superseded"
  /\ UNCHANGED <<baseId, candidateId, governanceId, specId,
                 evaluatedTuple, outcomes, evidence, evidenceOutcomes, approvals,
                 acceptedTuple, appliedCandidateId>>
  /\ history' = Append(history, "Superseded")

Next ==
  \/ Prepare
  \/ \E obligation \in Obligations, outcome \in Outcomes : PublishEvidence(obligation, outcome)
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
  /\ evaluatedTuple \in {NoTuple} \cup
       (Bases \X Candidates \X Governances \X Specs)
  /\ outcomes \in [Obligations -> Outcomes]
  /\ evidence \subseteq Obligations
  /\ evidenceOutcomes \in [Obligations -> Outcomes]
  /\ approvals \subseteq AuthorizedActors
  /\ acceptedTuple \in {NoTuple} \cup
       (Bases \X Candidates \X Governances \X Specs)
  /\ appliedCandidateId \in {NoCandidate} \cup Candidates
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
    /\ outcomes = [o \in Obligations |-> Pass]

ApprovalBinding ==
  phase \in {"Accepted", "Applied"} =>
    approvals \subseteq AuthorizedActors

NoImplicitApplication ==
  phase # "Applied" => appliedCandidateId = NoCandidate

NoApprovalInPreparedPhase ==
  phase = "Prepared" => approvals = {}

TerminalStep ==
  phase \in TerminalPhases => UNCHANGED vars

TerminalDiscipline ==
  [][TerminalStep]_vars

EvaluationOutcomeBinding ==
  phase \in {"Evaluated", "Reviewable", "Accepted", "Applied"} =>
    outcomes = [o \in Obligations |->
                  IF o \in evidence THEN evidenceOutcomes[o] ELSE Unknown]

FailedOrUnresolvedEvidenceBlocksAcceptance ==
  (\E o \in Obligations : outcomes[o] # Pass) =>
    phase \notin {"Accepted", "Applied"}

HistoryNonEmpty == Len(history) >= 1

NoUnexpectedNonterminalDeadlock ==
  Len(history) < HistoryLimit /\ phase \notin TerminalPhases =>
    ENABLED Next

Spec == Init /\ [][Next]_vars

THEOREM Spec => []TypeOK
THEOREM Spec => []AcceptanceSoundness
THEOREM Spec => []ApplicationSoundness
THEOREM Spec => []NoStaleEvaluation
THEOREM Spec => []EvidenceBinding
THEOREM Spec => []EvaluationOutcomeBinding
THEOREM Spec => []FailedOrUnresolvedEvidenceBlocksAcceptance
THEOREM Spec => []ApprovalBinding
THEOREM Spec => []NoImplicitApplication
THEOREM Spec => []NoApprovalInPreparedPhase
THEOREM Spec => []HistoryNonEmpty
THEOREM Spec => []NoUnexpectedNonterminalDeadlock

=============================================================================
