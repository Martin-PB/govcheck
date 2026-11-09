--------------------- MODULE GovCheckGovernanceApplicability ---------------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Principals, RootPrincipal, GovernanceRevisions, Candidates,
  EvaluationIds, DecisionIds, HistoryLimit

ASSUME RootPrincipal \in Principals
ASSUME HistoryLimit >= 2

VARIABLES currentAuthority, currentGovernance, position,
          governanceHistory, evaluations, decisions, pendingPublication
vars == <<currentAuthority, currentGovernance, position,
          governanceHistory, evaluations, decisions, pendingPublication>>

GenesisRecord ==
  [ revision |-> CHOOSE r \in GovernanceRevisions : TRUE,
    predecessor |-> "NoRevision",
    authority |-> RootPrincipal,
    effectivePosition |-> 0,
    decision |-> "NoDecision",
    kind |-> "Genesis" ]

Init ==
  /\ GovernanceRevisions # {}
  /\ DecisionIds # {}
  /\ currentAuthority = RootPrincipal
  /\ currentGovernance = GenesisRecord.revision
  /\ position = 0
  /\ governanceHistory = <<GenesisRecord>>
  /\ evaluations = <<>>
  /\ decisions = <<>>
  /\ pendingPublication = "NoDecision"

ApplicableIndex(atPosition) ==
  CHOOSE i \in 1..Len(governanceHistory) :
    /\ governanceHistory[i].effectivePosition <= atPosition
    /\ \A j \in 1..Len(governanceHistory) :
         governanceHistory[j].effectivePosition <= atPosition => i >= j
ApplicableGovernance(atPosition) == governanceHistory[ApplicableIndex(atPosition)].revision
ApplicableAuthority(atPosition) == governanceHistory[ApplicableIndex(atPosition)].authority
AvailableDecisionIds == DecisionIds \ {decisions[i].id : i \in 1..Len(decisions)}

Evaluate(evalId, candidate, resultingRevision) ==
  /\ Len(evaluations) < HistoryLimit
  /\ evalId \in EvaluationIds
  /\ candidate \in Candidates
  /\ resultingRevision \in GovernanceRevisions \cup {"NoRevision"}
  /\ evalId \notin {evaluations[i].id : i \in 1..Len(evaluations)}
  /\ (resultingRevision = "NoRevision" \/
       resultingRevision \notin {governanceHistory[i].revision : i \in 1..Len(governanceHistory)})
  /\ evaluations' = Append(evaluations,
       [id |-> evalId, candidate |-> candidate,
        baseGovernance |-> currentGovernance,
        resultingGovernance |-> resultingRevision,
        evaluatedAt |-> position + 1])
  /\ position' = position + 1
  /\ UNCHANGED <<currentAuthority, currentGovernance, governanceHistory,
                 decisions, pendingPublication>>

Authorize(evalId, actor) ==
  /\ Len(decisions) < HistoryLimit
  /\ AvailableDecisionIds # {}
  /\ pendingPublication = "NoDecision"
  /\ evalId \in {evaluations[i].id : i \in 1..Len(evaluations)}
  /\ actor \in Principals
  /\ actor = currentAuthority
  /\ LET e == CHOOSE i \in 1..Len(evaluations) : evaluations[i].id = evalId
     IN
       /\ e.baseGovernance = currentGovernance
       /\ e.resultingGovernance # "NoRevision"
       /\ e.resultingGovernance \notin {governanceHistory[i].revision : i \in 1..Len(governanceHistory)}
       /\ evalId \notin {decisions[i].evaluationId : i \in 1..Len(decisions)}
       /\ decisions' = Append(decisions,
            [id |-> CHOOSE d \in AvailableDecisionIds : TRUE,
             evaluationId |-> e.id, candidate |-> e.candidate,
             governanceAtDecision |-> currentGovernance,
             resultingGovernance |-> e.resultingGovernance,
             actor |-> actor, decisionPosition |-> position + 1,
             outcome |-> "Authorized"])
       /\ pendingPublication' = CHOOSE d \in AvailableDecisionIds : TRUE
  /\ position' = position + 1
  /\ UNCHANGED <<currentAuthority, currentGovernance, governanceHistory, evaluations>>

Publish ==
  /\ Len(governanceHistory) < HistoryLimit
  /\ pendingPublication # "NoDecision"
  /\ pendingPublication \in {decisions[i].id : i \in 1..Len(decisions)}
  /\ LET d == CHOOSE i \in 1..Len(decisions) : decisions[i].id = pendingPublication
     IN
       /\ d.governanceAtDecision = currentGovernance
       /\ d.resultingGovernance \notin {governanceHistory[i].revision : i \in 1..Len(governanceHistory)}
       /\ governanceHistory' = Append(governanceHistory,
            [revision |-> d.resultingGovernance,
             predecessor |-> currentGovernance,
             authority |-> currentAuthority,
             effectivePosition |-> position + 1,
             decision |-> d.id, kind |-> "Amendment"])
       /\ currentGovernance' = d.resultingGovernance
  /\ position' = position + 1
  /\ pendingPublication' = "NoDecision"
  /\ UNCHANGED <<currentAuthority, evaluations, decisions>>

Next ==
  \/ \E e \in EvaluationIds, c \in Candidates,
        r \in GovernanceRevisions \cup {"NoRevision"} : Evaluate(e, c, r)
  \/ \E e \in EvaluationIds, a \in Principals : Authorize(e, a)
  \/ Publish

TypeOK ==
  /\ currentAuthority \in Principals
  /\ currentGovernance \in GovernanceRevisions
  /\ position \in Nat
  /\ governanceHistory \in Seq([revision : GovernanceRevisions,
       predecessor : GovernanceRevisions \cup {"NoRevision"}, authority : Principals,
       effectivePosition : Nat, decision : DecisionIds \cup {"NoDecision"},
       kind : {"Genesis", "Amendment"}])
  /\ Len(governanceHistory) >= 1
  /\ evaluations \in Seq([id : EvaluationIds, candidate : Candidates,
       baseGovernance : GovernanceRevisions,
       resultingGovernance : GovernanceRevisions \cup {"NoRevision"}, evaluatedAt : Nat])
  /\ decisions \in Seq([id : DecisionIds, evaluationId : EvaluationIds,
       candidate : Candidates, governanceAtDecision : GovernanceRevisions,
       resultingGovernance : GovernanceRevisions, actor : Principals,
       decisionPosition : Nat, outcome : {"Authorized"}])
  /\ pendingPublication \in DecisionIds \cup {"NoDecision"}
  /\ governanceHistory[1] = GenesisRecord
  /\ governanceHistory[Len(governanceHistory)].revision = currentGovernance
  /\ governanceHistory[Len(governanceHistory)].authority = currentAuthority
  /\ governanceHistory[Len(governanceHistory)].effectivePosition <= position

UniqueGovernanceRevisions ==
  \A i, j \in 1..Len(governanceHistory) : i # j => governanceHistory[i].revision # governanceHistory[j].revision
GovernanceChainIsContinuous ==
  \A i \in 2..Len(governanceHistory) :
    /\ governanceHistory[i].predecessor = governanceHistory[i-1].revision
    /\ governanceHistory[i].effectivePosition > governanceHistory[i-1].effectivePosition
OnlyApplicableAuthorityCanAuthorize ==
  \A i \in 1..Len(decisions) : decisions[i].actor = ApplicableAuthority(decisions[i].decisionPosition)
DecisionUsesApplicablePriorGovernance ==
  \A i \in 1..Len(decisions) : decisions[i].governanceAtDecision = ApplicableGovernance(decisions[i].decisionPosition)
NoSelfAuthorization ==
  \A i \in 1..Len(decisions) :
    ~\E j \in 1..Len(governanceHistory) :
      /\ governanceHistory[j].revision = decisions[i].resultingGovernance
      /\ governanceHistory[j].effectivePosition <= decisions[i].decisionPosition
PublishedOnlyAfterAuthorization ==
  \A i \in 2..Len(governanceHistory) :
    \E j \in 1..Len(decisions) :
      /\ decisions[j].id = governanceHistory[i].decision
      /\ decisions[j].resultingGovernance = governanceHistory[i].revision
      /\ decisions[j].decisionPosition < governanceHistory[i].effectivePosition
HistoricalDecisionsRemainBound == DecisionUsesApplicablePriorGovernance
EvaluationAuthorizationBinding ==
  \A i \in 1..Len(decisions) :
    \E j \in 1..Len(evaluations) :
      /\ evaluations[j].id = decisions[i].evaluationId
      /\ evaluations[j].candidate = decisions[i].candidate
      /\ evaluations[j].baseGovernance = decisions[i].governanceAtDecision
      /\ evaluations[j].resultingGovernance = decisions[i].resultingGovernance
      /\ evaluations[j].evaluatedAt < decisions[i].decisionPosition
HistoriesAreAppendOnly ==
  /\ Len(governanceHistory') >= Len(governanceHistory)
  /\ SubSeq(governanceHistory', 1, Len(governanceHistory)) = governanceHistory
  /\ Len(decisions') >= Len(decisions)
  /\ SubSeq(decisions', 1, Len(decisions)) = decisions
AppendOnly == [][HistoriesAreAppendOnly]_vars
Spec == Init /\ [][Next]_vars

THEOREM Spec => []TypeOK
THEOREM Spec => []UniqueGovernanceRevisions
THEOREM Spec => []GovernanceChainIsContinuous
THEOREM Spec => []OnlyApplicableAuthorityCanAuthorize
THEOREM Spec => []DecisionUsesApplicablePriorGovernance
THEOREM Spec => []NoSelfAuthorization
THEOREM Spec => []PublishedOnlyAfterAuthorization
THEOREM Spec => []HistoricalDecisionsRemainBound
THEOREM Spec => []EvaluationAuthorizationBinding
THEOREM Spec => AppendOnly

=============================================================================
