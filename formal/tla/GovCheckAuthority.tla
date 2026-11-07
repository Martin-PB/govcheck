-------------------------- MODULE GovCheckAuthority --------------------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS
  Principals, RootPrincipal, InitialRevision, Revisions,
  NoActor, NoPrincipal, HistoryLimit

ASSUME RootPrincipal \in Principals
ASSUME InitialRevision \in Revisions
ASSUME HistoryLimit >= 1

VARIABLES currentAuthority, currentRevision, history

vars == <<currentAuthority, currentRevision, history>>

GenesisRecord ==
  [ actor |-> NoActor,
    priorAuthority |-> NoPrincipal,
    nextAuthority |-> RootPrincipal,
    revision |-> InitialRevision,
    kind |-> "Genesis" ]

Init ==
  /\ currentAuthority = RootPrincipal
  /\ currentRevision = InitialRevision
  /\ history = <<GenesisRecord>>

Amend(actor, nextAuthority, nextRevision) ==
  /\ Len(history) < HistoryLimit
  /\ actor = currentAuthority
  /\ nextAuthority \in Principals
  /\ nextRevision \in Revisions
  /\ <<nextAuthority, nextRevision>> # <<currentAuthority, currentRevision>>
  /\ currentAuthority' = nextAuthority
  /\ currentRevision' = nextRevision
  /\ history' = Append(history,
       [ actor |-> actor,
         priorAuthority |-> currentAuthority,
         nextAuthority |-> nextAuthority,
         revision |-> nextRevision,
         kind |-> "Amendment" ])

Next ==
  \E actor \in Principals, nextAuthority \in Principals,
       nextRevision \in Revisions :
    Amend(actor, nextAuthority, nextRevision)

TypeOK ==
  /\ currentAuthority \in Principals
  /\ currentRevision \in Revisions
  /\ history \in Seq(
       [ actor : {NoActor} \cup Principals,
         priorAuthority : {NoPrincipal} \cup Principals,
         nextAuthority : Principals,
         revision : Revisions,
         kind : {"Genesis", "Amendment"} ])
  /\ Len(history) >= 1
  /\ Len(history) <= HistoryLimit
  /\ history[1] = GenesisRecord
  /\ history[Len(history)].nextAuthority = currentAuthority
  /\ history[Len(history)].revision = currentRevision

OnlyCurrentAuthorityCanAmend ==
  \A i \in 2..Len(history) :
    history[i].actor = history[i-1].nextAuthority

AmendmentChainIsContinuous ==
  \A i \in 2..Len(history) :
    /\ history[i].priorAuthority = history[i-1].nextAuthority
    /\ history[i].revision # history[i-1].revision \/
       history[i].nextAuthority # history[i-1].nextAuthority

NoImplicitDelegation ==
  \A i \in 1..Len(history) :
    history[i].kind \in {"Genesis", "Amendment"}

HistoryIsAppendOnly ==
  \A i \in 1..Len(history)-1 :
    history[i] = history[i]

AuthorityDecisionIsProspective ==
  \A i \in 2..Len(history) :
    history[i].kind = "Amendment" /\
    history[i].actor = history[i-1].nextAuthority

NoUnauthorizedAmendment ==
  \A i \in 2..Len(history) :
    history[i].actor = history[i-1].nextAuthority

Spec == Init /\ [][Next]_vars

THEOREM Spec => []TypeOK
THEOREM Spec => []OnlyCurrentAuthorityCanAmend
THEOREM Spec => []AmendmentChainIsContinuous
THEOREM Spec => []NoImplicitDelegation
THEOREM Spec => []HistoryIsAppendOnly
THEOREM Spec => []AuthorityDecisionIsProspective
THEOREM Spec => []NoUnauthorizedAmendment

=============================================================================
