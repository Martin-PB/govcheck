---------------- MODULE GovCheckGovernanceControls ----------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Principals, RootPrincipal, PriorEvaluator, ShadowEvaluator,
  InitialRevision, GovernanceRevisions, Candidates, EvaluationIds,
  AuthorizationIds, ExceptionIds, Requirements, WaivableRequirements,
  NonDerogableRequirements, Contents, CandidateContent, CandidateRequirement,
  RevisionsContent

ASSUME RootPrincipal \in Principals
ASSUME PriorEvaluator \in Principals
ASSUME ShadowEvaluator \in Principals
ASSUME InitialRevision \in GovernanceRevisions
ASSUME WaivableRequirements \subseteq Requirements
ASSUME NonDerogableRequirements \subseteq Requirements
ASSUME WaivableRequirements \cap NonDerogableRequirements = {}

VARIABLES
  head, position, journal, evaluations, shadowEvaluations,
  exceptions, authorizations, authorityRevoked, revocationPosition,
  decisions, requalifications

vars ==
  <<head, position, journal, evaluations, shadowEvaluations,
    exceptions, authorizations, authorityRevoked, revocationPosition,
    decisions, requalifications>>

UnusedEvaluation ==
  [status |-> "Unused", candidate |-> CHOOSE c \in Candidates : TRUE,
   evaluator |-> PriorEvaluator, baseRevision |-> InitialRevision,
   basePosition |-> 0, result |-> "Unknown",
   requirement |-> CHOOSE r \in Requirements : TRUE]

UnusedException ==
  [status |-> "Unused", requirement |-> CHOOSE r \in Requirements : TRUE,
   reason |-> "None", grantedAt |-> 0, expiresAt |-> 0,
   statusDetail |-> "Unused"]

UnusedAuthorization ==
  [status |-> "Unused", evaluationId |-> CHOOSE e \in EvaluationIds : TRUE,
   baseRevision |-> InitialRevision, basePosition |-> 0,
   exceptionId |-> "NoException"]

Init ==
  /\ head = InitialRevision
  /\ position = 0
  /\ journal = <<[kind |-> "Genesis", revision |-> InitialRevision,
                   predecessor |-> "NoRevision", content |-> CHOOSE c \in Contents : TRUE,
                   position |-> 0]>>
  /\ evaluations = [e \in EvaluationIds |-> UnusedEvaluation]
  /\ shadowEvaluations = {}
  /\ exceptions = [x \in ExceptionIds |-> UnusedException]
  /\ authorizations = [a \in AuthorizationIds |-> UnusedAuthorization]
  /\ authorityRevoked = FALSE
  /\ revocationPosition = "NotRevoked"
  /\ decisions = <<>>
  /\ requalifications = <<>>

Evaluate(candidate, evaluationId, result) ==
  /\ candidate \in Candidates
  /\ evaluationId \in EvaluationIds
  /\ result \in {"Pass", "Fail", "Unknown", "Conflict"}
  /\ evaluations[evaluationId].status = "Unused"
  /\ ~authorityRevoked
  /\ evaluations' = [evaluations EXCEPT
       ![evaluationId] = [status |-> "Ready", candidate |-> candidate,
         evaluator |-> PriorEvaluator, baseRevision |-> head,
         basePosition |-> position, result |-> result,
         requirement |-> CandidateRequirement[candidate]]]
  /\ UNCHANGED <<head, position, journal, shadowEvaluations, exceptions,
                  authorizations, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

ShadowEvaluate(candidate, result) ==
  /\ candidate \in Candidates
  /\ result \in {"Pass", "Fail", "Unknown", "Conflict"}
  /\ shadowEvaluations' = shadowEvaluations \cup
       {[candidate |-> candidate, evaluator |-> ShadowEvaluator,
         result |-> result, comparedAt |-> position]}
  /\ UNCHANGED <<head, position, journal, evaluations, exceptions,
                  authorizations, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

GrantException(exceptionId, requirement, reason, lifetime) ==
  /\ exceptionId \in ExceptionIds
  /\ exceptions[exceptionId].statusDetail = "Unused"
  /\ requirement \in WaivableRequirements
  /\ requirement \notin NonDerogableRequirements
  /\ reason # "None"
  /\ lifetime \in {1, 2}
  /\ ~authorityRevoked
  /\ exceptions' = [exceptions EXCEPT
       ![exceptionId] = [status |-> "Active", requirement |-> requirement,
         reason |-> reason, grantedAt |-> position,
         expiresAt |-> position + lifetime, statusDetail |-> "Active"]]
  /\ UNCHANGED <<head, position, journal, evaluations, shadowEvaluations,
                  authorizations, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

RevokeException(exceptionId) ==
  /\ exceptionId \in ExceptionIds
  /\ exceptions[exceptionId].statusDetail = "Active"
  /\ exceptions' = [exceptions EXCEPT
       ![exceptionId].statusDetail = "Revoked"]
  /\ UNCHANGED <<head, position, journal, evaluations, shadowEvaluations,
                  authorizations, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

RevokeAuthority ==
  /\ ~authorityRevoked
  /\ authorityRevoked' = TRUE
  /\ revocationPosition' = position + 1
  /\ position' = position + 1
  /\ journal' = Append(journal,
       [kind |-> "AuthorityRevocation", revision |-> head,
        predecessor |-> head, content |-> journal[Len(journal)].content,
        position |-> position + 1])
  /\ UNCHANGED <<head, evaluations, shadowEvaluations, exceptions,
                  authorizations, decisions, requalifications>>

EvaluationFresh(evaluationId) ==
  /\ evaluations[evaluationId].status = "Ready"
  /\ evaluations[evaluationId].baseRevision = head
  /\ evaluations[evaluationId].basePosition = position
  /\ ~authorityRevoked

ExceptionUsable(exceptionId, requirement) ==
  /\ exceptionId \in ExceptionIds
  /\ exceptions[exceptionId].statusDetail = "Active"
  /\ exceptions[exceptionId].requirement = requirement
  /\ requirement \in WaivableRequirements
  /\ requirement \notin NonDerogableRequirements
  /\ position < exceptions[exceptionId].expiresAt

Authorize(evaluationId, authorizationId, exceptionId) ==
  /\ evaluationId \in EvaluationIds
  /\ authorizationId \in AuthorizationIds
  /\ authorizations[authorizationId].status = "Unused"
  /\ EvaluationFresh(evaluationId)
  /\ (evaluations[evaluationId].result = "Pass"
      \/ (evaluations[evaluationId].result = "Fail"
          /\ ExceptionUsable(exceptionId,
               evaluations[evaluationId].requirement)))
  /\ authorizations' = [authorizations EXCEPT
       ![authorizationId] = [status |-> "Authorized",
         evaluationId |-> evaluationId,
         baseRevision |-> head, basePosition |-> position,
         exceptionId |-> IF evaluations[evaluationId].result = "Pass"
                         THEN "NoException" ELSE exceptionId]]
  /\ UNCHANGED <<head, position, journal, evaluations, shadowEvaluations,
                  exceptions, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

AuthorizeWithoutException(evaluationId, authorizationId) ==
  /\ evaluationId \in EvaluationIds
  /\ authorizationId \in AuthorizationIds
  /\ authorizations[authorizationId].status = "Unused"
  /\ EvaluationFresh(evaluationId)
  /\ evaluations[evaluationId].result = "Pass"
  /\ authorizations' = [authorizations EXCEPT
       ![authorizationId] = [status |-> "Authorized",
         evaluationId |-> evaluationId, baseRevision |-> head,
         basePosition |-> position, exceptionId |-> "NoException"]]
  /\ UNCHANGED <<head, position, journal, evaluations, shadowEvaluations,
                  exceptions, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

Publish(authorizationId, newRevision) ==
  /\ authorizationId \in AuthorizationIds
  /\ authorizations[authorizationId].status = "Authorized"
  /\ ~authorityRevoked
  /\ authorizations[authorizationId].baseRevision = head
  /\ authorizations[authorizationId].basePosition = position
  /\ newRevision \in GovernanceRevisions
  /\ newRevision # head
  /\ ~\E i \in 1..Len(journal) : journal[i].revision = newRevision
  /\ head' = newRevision
  /\ position' = position + 1
  /\ journal' = Append(journal,
       [kind |-> "Publication", revision |-> newRevision,
        predecessor |-> head,
        content |-> CandidateContent[evaluations[authorizations[authorizationId].evaluationId].candidate],
        position |-> position + 1])
  /\ decisions' = Append(decisions,
       [kind |-> "AuthorizedPublication",
        governanceRevision |-> head, resultingRevision |-> newRevision,
        evaluationId |-> authorizations[authorizationId].evaluationId,
        position |-> position + 1])
  /\ UNCHANGED <<evaluations, shadowEvaluations, exceptions, authorizations,
                  authorityRevoked, revocationPosition, requalifications>>

MarkStale(evaluationId) ==
  /\ evaluationId \in EvaluationIds
  /\ evaluations[evaluationId].status = "Ready"
  /\ ~EvaluationFresh(evaluationId)
  /\ evaluations' = [evaluations EXCEPT ![evaluationId].status = "Stale"]
  /\ UNCHANGED <<head, position, journal, shadowEvaluations, exceptions,
                  authorizations, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

RequalifyHistorical(decisionIndex, outcome) ==
  /\ decisionIndex \in 1..Len(decisions)
  /\ outcome \in {"Confirmed", "Disputed", "Invalidated"}
  /\ requalifications' = Append(requalifications,
       [decisionIndex |-> decisionIndex,
        originalGovernanceRevision |-> decisions[decisionIndex].governanceRevision,
        outcome |-> outcome, atPosition |-> position])
  /\ UNCHANGED <<head, position, journal, evaluations, shadowEvaluations,
                  exceptions, authorizations, authorityRevoked,
                  revocationPosition, decisions>>

Tick ==
  /\ position < 3
  /\ position' = position + 1
  /\ UNCHANGED <<head, journal, evaluations, shadowEvaluations, exceptions,
                  authorizations, authorityRevoked, revocationPosition,
                  decisions, requalifications>>

Next ==
  \/ \E c \in Candidates, e \in EvaluationIds,
        r \in {"Pass", "Fail", "Unknown", "Conflict"} : Evaluate(c, e, r)
  \/ \E c \in Candidates, r \in {"Pass", "Fail", "Unknown", "Conflict"} :
        ShadowEvaluate(c, r)
  \/ \E x \in ExceptionIds, r \in WaivableRequirements,
        reason \in {"OperationalNeed", "TemporaryConstraint"}, life \in {1, 2} :
        GrantException(x, r, reason, life)
  \/ \E x \in ExceptionIds : RevokeException(x)
  \/ RevokeAuthority
  \/ \E e \in EvaluationIds, a \in AuthorizationIds, x \in ExceptionIds :
        Authorize(e, a, x)
  \/ \E e \in EvaluationIds, a \in AuthorizationIds :
        AuthorizeWithoutException(e, a)
  \/ \E a \in AuthorizationIds, r \in GovernanceRevisions : Publish(a, r)
  \/ \E e \in EvaluationIds : MarkStale(e)
  \/ \E i \in 1..Len(decisions), o \in {"Confirmed", "Disputed", "Invalidated"} :
        RequalifyHistorical(i, o)
  \/ Tick

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ head \in GovernanceRevisions
  /\ position \in Nat
  /\ journal \in Seq([kind : {"Genesis", "Publication", "AuthorityRevocation"},
      revision : GovernanceRevisions, predecessor : GovernanceRevisions \cup {"NoRevision"},
      content : Contents, position : Nat])
  /\ evaluations \in [EvaluationIds ->
      [status : {"Unused", "Ready", "Stale"}, candidate : Candidates,
       evaluator : Principals, baseRevision : GovernanceRevisions,
       basePosition : Nat, result : {"Pass", "Fail", "Unknown", "Conflict"},
       requirement : Requirements]]
  /\ shadowEvaluations \subseteq
      [candidate : Candidates, evaluator : {ShadowEvaluator},
       result : {"Pass", "Fail", "Unknown", "Conflict"}, comparedAt : Nat]
  /\ exceptions \in [ExceptionIds ->
      [status : {"Unused"}, requirement : Requirements, reason : {"None", "OperationalNeed", "TemporaryConstraint"},
       grantedAt : Nat, expiresAt : Nat, statusDetail : {"Unused", "Active", "Revoked"}]]
  /\ authorizations \in [AuthorizationIds ->
      [status : {"Unused", "Authorized"}, evaluationId : EvaluationIds,
       baseRevision : GovernanceRevisions, basePosition : Nat,
       exceptionId : ExceptionIds \cup {"NoException"}]]
  /\ authorityRevoked \in BOOLEAN
  /\ revocationPosition \in Nat \cup {"NotRevoked"}
  /\ decisions \in Seq([kind : {"AuthorizedPublication"},
       governanceRevision : GovernanceRevisions, resultingRevision : GovernanceRevisions,
       evaluationId : EvaluationIds, position : Nat])
  /\ requalifications \in Seq([decisionIndex : Nat,
       originalGovernanceRevision : GovernanceRevisions,
       outcome : {"Confirmed", "Disputed", "Invalidated"}, atPosition : Nat])

AppendOnly ==
  /\ Len(journal') >= Len(journal)
  /\ SubSeq(journal', 1, Len(journal)) = journal
  /\ Len(decisions') >= Len(decisions)
  /\ SubSeq(decisions', 1, Len(decisions)) = decisions
  /\ Len(requalifications') >= Len(requalifications)
  /\ SubSeq(requalifications', 1, Len(requalifications)) = requalifications

UniquePublishedRevisions ==
  \A i, j \in 1..Len(journal) :
    (journal[i].kind = "Publication" /\ journal[j].kind = "Publication" /\ i # j)
      => journal[i].revision # journal[j].revision

PublicationUsesPriorAuthority ==
  \A i \in 1..Len(decisions) :
    decisions[i].governanceRevision # decisions[i].resultingRevision

ShadowCannotAuthorize ==
  \A e \in EvaluationIds :
    evaluations[e].status = "Ready" => evaluations[e].evaluator = PriorEvaluator

UnknownAndConflictBlock ==
  \A e \in EvaluationIds :
    evaluations[e].result \in {"Unknown", "Conflict"} =>
      ~\E a \in AuthorizationIds :
        authorizations[a].status = "Authorized" /\ authorizations[a].evaluationId = e

NonDerogableNeverExcepted ==
  \A x \in ExceptionIds :
    exceptions[x].statusDetail = "Active" =>
      exceptions[x].requirement \notin NonDerogableRequirements

RevocationIsProspective ==
  authorityRevoked => revocationPosition \in Nat /\ revocationPosition > 0

HistoricalDecisionsPreserved ==
  \A i \in 1..Len(requalifications) :
    requalifications[i].originalGovernanceRevision =
      decisions[requalifications[i].decisionIndex].governanceRevision

NoStaleAuthorization ==
  \A a \in AuthorizationIds :
    authorizations[a].status = "Authorized" =>
      /\ evaluations[authorizations[a].evaluationId].baseRevision =
           authorizations[a].baseRevision
      /\ evaluations[authorizations[a].evaluationId].basePosition =
           authorizations[a].basePosition

=============================================================================
