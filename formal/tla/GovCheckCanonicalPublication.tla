---------------- MODULE GovCheckCanonicalPublication ----------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS Principals, RootPrincipal, InitialRevision, GovernanceRevisions,
          Candidates, EvaluationIds, AuthorizationIds

ASSUME RootPrincipal \in Principals
ASSUME InitialRevision \in GovernanceRevisions

VARIABLES log, evaluations, authorizations, published
vars == <<log, evaluations, authorizations, published>>

Genesis ==
  [revision |-> InitialRevision, predecessor |-> "NoRevision",
   publicationId |-> "Genesis", actor |-> RootPrincipal]

UnusedEvaluation ==
  [status |-> "Unused", candidate |-> CHOOSE c \in Candidates : TRUE,
   baseRevision |-> InitialRevision, basePosition |-> 0]

UnusedAuthorization ==
  [status |-> "Unused", evaluationId |-> CHOOSE e \in EvaluationIds : TRUE,
   actor |-> RootPrincipal, baseRevision |-> InitialRevision,
   basePosition |-> 0, newRevision |-> InitialRevision]

Init ==
  /\ log = <<Genesis>>
  /\ evaluations = [e \in EvaluationIds |-> UnusedEvaluation]
  /\ authorizations = [a \in AuthorizationIds |-> UnusedAuthorization]
  /\ published = {}

HeadRevision == log[Len(log)].revision
HeadPosition == Len(log) - 1

Evaluate(candidate, evaluationId) ==
  /\ candidate \in Candidates
  /\ evaluationId \in EvaluationIds
  /\ evaluations[evaluationId].status = "Unused"
  /\ evaluations' = [evaluations EXCEPT
       ![evaluationId] = [status |-> "Ready", candidate |-> candidate,
                          baseRevision |-> HeadRevision,
                          basePosition |-> HeadPosition]]
  /\ UNCHANGED <<log, authorizations, published>>

Authorize(evaluationId, authorizationId, actor, newRevision) ==
  /\ evaluationId \in EvaluationIds
  /\ evaluations[evaluationId].status = "Ready"
  /\ authorizationId \in AuthorizationIds
  /\ authorizations[authorizationId].status = "Unused"
  /\ actor = RootPrincipal
  /\ newRevision \in GovernanceRevisions
  /\ newRevision # HeadRevision
  /\ ~\E i \in 1..Len(log) : log[i].revision = newRevision
  /\ evaluations[evaluationId].baseRevision = HeadRevision
  /\ evaluations[evaluationId].basePosition = HeadPosition
  /\ authorizations' = [authorizations EXCEPT
       ![authorizationId] = [status |-> "Authorized", evaluationId |-> evaluationId,
                             actor |-> actor,
                             baseRevision |-> HeadRevision,
                             basePosition |-> HeadPosition,
                             newRevision |-> newRevision]]
  /\ UNCHANGED <<log, evaluations, published>>

Publish(authorizationId, publicationId) ==
  /\ authorizationId \in AuthorizationIds
  /\ authorizations[authorizationId].status = "Authorized"
  /\ publicationId \in {"pub0", "pub1"}
  /\ publicationId \notin published
  /\ authorizations[authorizationId].baseRevision = HeadRevision
  /\ authorizations[authorizationId].basePosition = HeadPosition
  /\ Len(log) < 3
  /\ log' = Append(log,
       [revision |-> authorizations[authorizationId].newRevision,
        predecessor |-> HeadRevision,
        publicationId |-> publicationId,
        actor |-> authorizations[authorizationId].actor])
  /\ published' = published \cup {publicationId}
  /\ UNCHANGED <<evaluations, authorizations>>

Next ==
  \/ \E c \in Candidates, e \in EvaluationIds : Evaluate(c, e)
  \/ \E e \in EvaluationIds, a \in AuthorizationIds,
        p \in Principals, r \in GovernanceRevisions :
        Authorize(e, a, p, r)
  \/ \E a \in AuthorizationIds, p \in {"pub0", "pub1"} :
        Publish(a, p)

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ log \in Seq([revision : GovernanceRevisions,
                   predecessor : GovernanceRevisions \cup {"NoRevision"},
                   publicationId : {"Genesis", "pub0", "pub1"},
                   actor : Principals])
  /\ evaluations \in [EvaluationIds ->
       [status : {"Unused", "Ready"}, candidate : Candidates,
        baseRevision : GovernanceRevisions, basePosition : Nat]]
  /\ authorizations \in [AuthorizationIds ->
       [status : {"Unused", "Authorized"}, evaluationId : EvaluationIds,
        actor : Principals, baseRevision : GovernanceRevisions,
        basePosition : Nat, newRevision : GovernanceRevisions]]
  /\ published \subseteq {"pub0", "pub1"}

HistoriesAreAppendOnly ==
  /\ Len(log') >= Len(log)
  /\ SubSeq(log', 1, Len(log)) = log

AppendOnly == [][HistoriesAreAppendOnly]_vars

UniqueRevisions ==
  \A i, j \in 1..Len(log) : i # j => log[i].revision # log[j].revision

ContinuousPredecessors ==
  \A i \in 2..Len(log) : log[i].predecessor = log[i-1].revision

OnePublicationPerCanonicalPosition ==
  \A i, j \in 2..Len(log) : i # j => log[i].predecessor # log[j].predecessor

AuthorizationBoundToEvaluation ==
  \A a \in AuthorizationIds :
    authorizations[a].status = "Authorized" =>
      /\ evaluations[authorizations[a].evaluationId].status = "Ready"
      /\ evaluations[authorizations[a].evaluationId].baseRevision =
           authorizations[a].baseRevision
      /\ evaluations[authorizations[a].evaluationId].basePosition =
           authorizations[a].basePosition

PublicationIsEffectPoint ==
  \A i \in 2..Len(log) : log[i].publicationId \in published

PublishedOnlyIfAuthorized ==
  \A i \in 2..Len(log) :
    \E a \in AuthorizationIds :
      /\ authorizations[a].status = "Authorized"
      /\ authorizations[a].newRevision = log[i].revision
      /\ authorizations[a].baseRevision = log[i].predecessor

NoStalePublication ==
  \A i \in 2..Len(log) :
    \E a \in AuthorizationIds :
      /\ authorizations[a].status = "Authorized"
      /\ authorizations[a].newRevision = log[i].revision
      /\ authorizations[a].basePosition = i - 2

=============================================================================
