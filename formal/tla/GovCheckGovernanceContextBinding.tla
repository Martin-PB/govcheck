--------------------- MODULE GovCheckGovernanceContextBinding ---------------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Principals, RootPrincipal, InitialGovernanceRevision, GovernanceRevisions,
  Contexts, InitialContext, Bases, Candidates, EvaluationIds, DecisionIds,
  HistoryLimit

ASSUME RootPrincipal \in Principals
ASSUME InitialGovernanceRevision \in GovernanceRevisions
ASSUME InitialContext \in Contexts
ASSUME HistoryLimit >= 2

NoDecision == "NoDecision"

\* The context token resolves to the exact authority/evaluator/specification/
\* profile identities and revisions bound by a governance revision.
ContextData(context) ==
  IF context = "context0"
  THEN [ authorityRevision |-> "authority0",
         evaluatorIdentity |-> "evaluator0",
         evaluatorRevision |-> "evaluatorRevision0",
         specificationIdentity |-> "specification0",
         specificationRevision |-> "specificationRevision0",
         profileIdentity |-> "profile0",
         profileRevision |-> "profileRevision0" ]
  ELSE [ authorityRevision |-> "authority1",
         evaluatorIdentity |-> "evaluator1",
         evaluatorRevision |-> "evaluatorRevision1",
         specificationIdentity |-> "specification1",
         specificationRevision |-> "specificationRevision1",
         profileIdentity |-> "profile1",
         profileRevision |-> "profileRevision1" ]

VARIABLES currentAuthority, currentGovernance, currentContext, position,
          governanceHistory, evaluations, decisions, pendingPublication

vars == <<currentAuthority, currentGovernance, currentContext, position,
          governanceHistory, evaluations, decisions, pendingPublication>>

GenesisRecord ==
  [ revision |-> InitialGovernanceRevision,
    predecessor |-> "NoRevision",
    authority |-> RootPrincipal,
    context |-> InitialContext,
    effectivePosition |-> 0,
    decision |-> NoDecision,
    kind |-> "Genesis" ]

Init ==
  /\ GovernanceRevisions # {}
  /\ Contexts # {}
  /\ Bases # {}
  /\ Candidates # {}
  /\ DecisionIds # {}
  /\ currentAuthority = RootPrincipal
  /\ currentGovernance = GenesisRecord.revision
  /\ currentContext = InitialContext
  /\ position = 0
  /\ governanceHistory = <<GenesisRecord>>
  /\ evaluations = <<>>
  /\ decisions = <<>>
  /\ pendingPublication = NoDecision

ApplicableIndex(atPosition) ==
  CHOOSE i \in 1..Len(governanceHistory) :
    /\ governanceHistory[i].effectivePosition <= atPosition
    /\ \A j \in 1..Len(governanceHistory) :
         governanceHistory[j].effectivePosition <= atPosition => i >= j

ApplicableGovernance(atPosition) ==
  governanceHistory[ApplicableIndex(atPosition)].revision
ApplicableAuthority(atPosition) ==
  governanceHistory[ApplicableIndex(atPosition)].authority
ApplicableContext(atPosition) ==
  governanceHistory[ApplicableIndex(atPosition)].context
ApplicableAuthorityRevision(atPosition) ==
  ContextData(ApplicableContext(atPosition)).authorityRevision
ApplicableEvaluator(atPosition) ==
  ContextData(ApplicableContext(atPosition)).evaluatorIdentity
ApplicableEvaluatorRevision(atPosition) ==
  ContextData(ApplicableContext(atPosition)).evaluatorRevision
ApplicableSpecification(atPosition) ==
  ContextData(ApplicableContext(atPosition)).specificationIdentity
ApplicableSpecificationRevision(atPosition) ==
  ContextData(ApplicableContext(atPosition)).specificationRevision
ApplicableProfile(atPosition) ==
  ContextData(ApplicableContext(atPosition)).profileIdentity
ApplicableProfileRevision(atPosition) ==
  ContextData(ApplicableContext(atPosition)).profileRevision

AvailableDecisionIds ==
  DecisionIds \ {decisions[i].id : i \in 1..Len(decisions)}

Evaluate(evalId, baseId, candidate, resultingRevision, resultingContext) ==
  /\ Len(evaluations) < HistoryLimit
  /\ evalId \in EvaluationIds
  /\ baseId \in Bases
  /\ candidate \in Candidates
  /\ resultingRevision \in GovernanceRevisions
  /\ resultingContext \in Contexts
  /\ evalId \notin {evaluations[i].id : i \in 1..Len(evaluations)}
  /\ resultingRevision \notin {governanceHistory[i].revision : i \in 1..Len(governanceHistory)}
  /\ evaluations' = Append(evaluations,
       [ id |-> evalId,
         baseId |-> baseId,
         candidate |-> candidate,
         governanceId |-> currentGovernance,
         baseContext |-> currentContext,
         specificationIdentity |-> ContextData(currentContext).specificationIdentity,
         specificationRevision |-> ContextData(currentContext).specificationRevision,
         resultingGovernance |-> resultingRevision,
         resultingContext |-> resultingContext,
         evaluatedAt |-> position + 1 ])
  /\ position' = position + 1
  /\ UNCHANGED <<currentAuthority, currentGovernance, currentContext,
                 governanceHistory, decisions, pendingPublication>>

Authorize(evalId, actor) ==
  /\ Len(decisions) < HistoryLimit
  /\ AvailableDecisionIds # {}
  /\ pendingPublication = NoDecision
  /\ evalId \in {evaluations[i].id : i \in 1..Len(evaluations)}
  /\ actor \in Principals
  /\ actor = currentAuthority
  /\ LET e == evaluations[CHOOSE i \in 1..Len(evaluations) : evaluations[i].id = evalId]
     IN
       /\ e.governanceId = currentGovernance
       /\ e.baseContext = currentContext
       /\ e.specificationIdentity = ContextData(currentContext).specificationIdentity
       /\ e.specificationRevision = ContextData(currentContext).specificationRevision
       /\ e.resultingGovernance \notin {governanceHistory[i].revision : i \in 1..Len(governanceHistory)}
       /\ evalId \notin {decisions[i].evaluationId : i \in 1..Len(decisions)}
       /\ decisions' = Append(decisions,
            [ id |-> CHOOSE d \in AvailableDecisionIds : TRUE,
              evaluationId |-> e.id,
              baseId |-> e.baseId,
              candidate |-> e.candidate,
              governanceAtDecision |-> currentGovernance,
              contextAtDecision |-> currentContext,
              specificationIdentityAtDecision |-> ContextData(currentContext).specificationIdentity,
              specificationRevisionAtDecision |-> ContextData(currentContext).specificationRevision,
              resultingGovernance |-> e.resultingGovernance,
              resultingContext |-> e.resultingContext,
              actor |-> actor,
              decisionPosition |-> position + 1,
              outcome |-> "Authorized" ])
       /\ pendingPublication' = CHOOSE d \in AvailableDecisionIds : TRUE
  /\ position' = position + 1
  /\ UNCHANGED <<currentAuthority, currentGovernance, currentContext,
                 governanceHistory, evaluations>>

Publish ==
  /\ Len(governanceHistory) < HistoryLimit
  /\ pendingPublication # NoDecision
  /\ pendingPublication \in {decisions[i].id : i \in 1..Len(decisions)}
  /\ LET d == decisions[CHOOSE i \in 1..Len(decisions) : decisions[i].id = pendingPublication]
     IN
       /\ d.governanceAtDecision = currentGovernance
       /\ d.contextAtDecision = currentContext
       /\ d.resultingGovernance \notin {governanceHistory[i].revision : i \in 1..Len(governanceHistory)}
       /\ governanceHistory' = Append(governanceHistory,
            [ revision |-> d.resultingGovernance,
              predecessor |-> currentGovernance,
              authority |-> currentAuthority,
              context |-> d.resultingContext,
              effectivePosition |-> position + 1,
              decision |-> d.id,
              kind |-> "Amendment" ])
       /\ currentGovernance' = d.resultingGovernance
       /\ currentContext' = d.resultingContext
  /\ position' = position + 1
  /\ pendingPublication' = NoDecision
  /\ UNCHANGED <<currentAuthority, evaluations, decisions>>

Next ==
  \/ \E e \in EvaluationIds, b \in Bases, c \in Candidates,
        r \in GovernanceRevisions, ctx \in Contexts :
       Evaluate(e, b, c, r, ctx)
  \/ \E e \in EvaluationIds, a \in Principals : Authorize(e, a)
  \/ Publish

TypeOK ==
  /\ currentAuthority \in Principals
  /\ currentGovernance \in GovernanceRevisions
  /\ currentContext \in Contexts
  /\ position \in Nat
  /\ governanceHistory \in Seq(
       [ revision : GovernanceRevisions,
         predecessor : GovernanceRevisions \cup {"NoRevision"},
         authority : Principals,
         context : Contexts,
         effectivePosition : Nat,
         decision : DecisionIds \cup {NoDecision},
         kind : {"Genesis", "Amendment"} ])
  /\ Len(governanceHistory) >= 1
  /\ evaluations \in Seq(
       [ id : EvaluationIds, baseId : Bases, candidate : Candidates,
         governanceId : GovernanceRevisions, baseContext : Contexts,
         specificationIdentity : STRING, specificationRevision : STRING,
         resultingGovernance : GovernanceRevisions, resultingContext : Contexts,
         evaluatedAt : Nat ])
  /\ decisions \in Seq(
       [ id : DecisionIds, evaluationId : EvaluationIds, baseId : Bases,
         candidate : Candidates, governanceAtDecision : GovernanceRevisions,
         contextAtDecision : Contexts,
         specificationIdentityAtDecision : STRING,
         specificationRevisionAtDecision : STRING,
         resultingGovernance : GovernanceRevisions, resultingContext : Contexts,
         actor : Principals, decisionPosition : Nat, outcome : {"Authorized"} ])
  /\ pendingPublication \in DecisionIds \cup {NoDecision}
  /\ governanceHistory[1] = GenesisRecord
  /\ governanceHistory[Len(governanceHistory)].revision = currentGovernance
  /\ governanceHistory[Len(governanceHistory)].authority = currentAuthority
  /\ governanceHistory[Len(governanceHistory)].context = currentContext
  /\ governanceHistory[Len(governanceHistory)].effectivePosition <= position

UniqueGovernanceRevisions ==
  \A i, j \in 1..Len(governanceHistory) :
    i # j => governanceHistory[i].revision # governanceHistory[j].revision

GovernanceChainIsContinuous ==
  \A i \in 2..Len(governanceHistory) :
    /\ governanceHistory[i].predecessor = governanceHistory[i-1].revision
    /\ governanceHistory[i].effectivePosition > governanceHistory[i-1].effectivePosition

OnlyApplicableAuthorityCanAuthorize ==
  \A i \in 1..Len(decisions) :
    decisions[i].actor = ApplicableAuthority(decisions[i].decisionPosition)

DecisionUsesApplicablePriorGovernance ==
  \A i \in 1..Len(decisions) :
    decisions[i].governanceAtDecision = ApplicableGovernance(decisions[i].decisionPosition)

EvaluationUsesApplicableContext ==
  \A i \in 1..Len(evaluations) :
    /\ evaluations[i].governanceId = ApplicableGovernance(evaluations[i].evaluatedAt)
    /\ evaluations[i].baseContext = ApplicableContext(evaluations[i].evaluatedAt)
    /\ evaluations[i].specificationIdentity =
         ApplicableSpecification(evaluations[i].evaluatedAt)
    /\ evaluations[i].specificationRevision =
         ApplicableSpecificationRevision(evaluations[i].evaluatedAt)

DecisionUsesApplicableContext ==
  \A i \in 1..Len(decisions) :
    /\ decisions[i].contextAtDecision = ApplicableContext(decisions[i].decisionPosition)
    /\ decisions[i].governanceAtDecision = ApplicableGovernance(decisions[i].decisionPosition)
    /\ decisions[i].actor = ApplicableAuthority(decisions[i].decisionPosition)
    /\ ContextData(decisions[i].contextAtDecision).authorityRevision =
         ApplicableAuthorityRevision(decisions[i].decisionPosition)
    /\ ContextData(decisions[i].contextAtDecision).evaluatorIdentity =
         ApplicableEvaluator(decisions[i].decisionPosition)
    /\ ContextData(decisions[i].contextAtDecision).evaluatorRevision =
         ApplicableEvaluatorRevision(decisions[i].decisionPosition)
    /\ decisions[i].specificationIdentityAtDecision =
         ApplicableSpecification(decisions[i].decisionPosition)
    /\ decisions[i].specificationRevisionAtDecision =
         ApplicableSpecificationRevision(decisions[i].decisionPosition)
    /\ ContextData(decisions[i].contextAtDecision).profileIdentity =
         ApplicableProfile(decisions[i].decisionPosition)
    /\ ContextData(decisions[i].contextAtDecision).profileRevision =
         ApplicableProfileRevision(decisions[i].decisionPosition)

EvaluationAuthorizationBinding ==
  \A i \in 1..Len(decisions) :
    \E j \in 1..Len(evaluations) :
      /\ evaluations[j].id = decisions[i].evaluationId
      /\ evaluations[j].baseId = decisions[i].baseId
      /\ evaluations[j].candidate = decisions[i].candidate
      /\ evaluations[j].governanceId = decisions[i].governanceAtDecision
      /\ evaluations[j].baseContext = decisions[i].contextAtDecision
      /\ evaluations[j].specificationIdentity = decisions[i].specificationIdentityAtDecision
      /\ evaluations[j].specificationRevision = decisions[i].specificationRevisionAtDecision
      /\ evaluations[j].resultingGovernance = decisions[i].resultingGovernance
      /\ evaluations[j].resultingContext = decisions[i].resultingContext
      /\ evaluations[j].evaluatedAt < decisions[i].decisionPosition

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
      /\ decisions[j].resultingContext = governanceHistory[i].context
      /\ decisions[j].governanceAtDecision = governanceHistory[i].predecessor
      /\ decisions[j].decisionPosition < governanceHistory[i].effectivePosition

HistoricalDecisionsRemainBound == DecisionUsesApplicableContext

CurrentContextMatchesHead ==
  /\ governanceHistory[Len(governanceHistory)].revision = currentGovernance
  /\ governanceHistory[Len(governanceHistory)].context = currentContext

HistoriesAreAppendOnly ==
  /\ Len(governanceHistory') >= Len(governanceHistory)
  /\ SubSeq(governanceHistory', 1, Len(governanceHistory)) = governanceHistory
  /\ Len(evaluations') >= Len(evaluations)
  /\ SubSeq(evaluations', 1, Len(evaluations)) = evaluations
  /\ Len(decisions') >= Len(decisions)
  /\ SubSeq(decisions', 1, Len(decisions)) = decisions

AppendOnly == [][HistoriesAreAppendOnly]_vars
Spec == Init /\ [][Next]_vars

THEOREM Spec => []TypeOK
THEOREM Spec => []UniqueGovernanceRevisions
THEOREM Spec => []GovernanceChainIsContinuous
THEOREM Spec => []OnlyApplicableAuthorityCanAuthorize
THEOREM Spec => []DecisionUsesApplicablePriorGovernance
THEOREM Spec => []EvaluationUsesApplicableContext
THEOREM Spec => []DecisionUsesApplicableContext
THEOREM Spec => []EvaluationAuthorizationBinding
THEOREM Spec => []NoSelfAuthorization
THEOREM Spec => []PublishedOnlyAfterAuthorization
THEOREM Spec => []HistoricalDecisionsRemainBound
THEOREM Spec => []CurrentContextMatchesHead
THEOREM Spec => AppendOnly

=============================================================================
