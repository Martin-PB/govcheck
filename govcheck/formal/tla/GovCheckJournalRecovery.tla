---------------- MODULE GovCheckJournalRecovery ----------------
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS InitialContent, Contents, RevisionIds, EventIds, MaxEvents, ReplicaIds
ASSUME InitialContent \in Contents
ASSUME MaxEvents \in Nat

VARIABLES journal, pending, appliedPosition, replicaObservations, crashed
vars == <<journal, pending, appliedPosition, replicaObservations, crashed>>

Genesis ==
  [position |-> 0, eventId |-> "genesis", revisionId |-> "rev0",
   predecessor |-> "NoRevision", content |-> InitialContent,
   kind |-> "genesis", source |-> "authority"]

Init ==
  /\ journal = <<Genesis>>
  /\ pending = "None"
  /\ appliedPosition = 0
  /\ replicaObservations = [r \in ReplicaIds |-> 0]
  /\ crashed = FALSE

JournalHead == journal[Len(journal)]
HeadPosition == Len(journal) - 1
ContentAt(position) == journal[position + 1].content

Prepare(eventId, revisionId, content, source) ==
  /\ ~crashed /\ pending = "None"
  /\ Len(journal) - 1 < MaxEvents
  /\ eventId \in EventIds /\ revisionId \in RevisionIds
  /\ content \in Contents
  /\ source \in {"authority", "git", "pijul", "other"}
  /\ ~\E i \in 1..Len(journal) :
       journal[i].eventId = eventId \/ journal[i].revisionId = revisionId
  /\ pending' = [eventId |-> eventId, revisionId |-> revisionId,
                  predecessor |-> JournalHead.revisionId, content |-> content,
                  kind |-> "change", source |-> source]
  /\ UNCHANGED <<journal, appliedPosition, replicaObservations, crashed>>

CommitDurably ==
  /\ ~crashed /\ pending # "None"
  /\ journal' = Append(journal,
       [position |-> HeadPosition + 1, eventId |-> pending.eventId,
        revisionId |-> pending.revisionId, predecessor |-> pending.predecessor,
        content |-> pending.content, kind |-> pending.kind, source |-> pending.source])
  /\ pending' = "None"
  /\ UNCHANGED <<appliedPosition, replicaObservations, crashed>>

ApplyCommitted ==
  /\ ~crashed /\ appliedPosition < HeadPosition
  /\ appliedPosition' = HeadPosition
  /\ UNCHANGED <<journal, pending, replicaObservations, crashed>>

Crash ==
  /\ ~crashed
  /\ crashed' = TRUE
  /\ pending' = "None"
  /\ UNCHANGED <<journal, appliedPosition, replicaObservations>>

Recover ==
  /\ crashed
  /\ crashed' = FALSE
  /\ appliedPosition' = HeadPosition
  /\ pending' = "None"
  /\ UNCHANGED <<journal, replicaObservations>>

ObserveReplica(replica, position) ==
  /\ ~crashed /\ replica \in ReplicaIds
  /\ position \in 0..HeadPosition
  /\ replicaObservations' = [replicaObservations EXCEPT ![replica] = position]
  /\ UNCHANGED <<journal, pending, appliedPosition, crashed>>

Rollback(eventId, revisionId, source, targetPosition) ==
  /\ ~crashed /\ pending = "None"
  /\ Len(journal) - 1 < MaxEvents
  /\ targetPosition \in 0..HeadPosition
  /\ eventId \in EventIds /\ revisionId \in RevisionIds
  /\ ~\E i \in 1..Len(journal) :
       journal[i].eventId = eventId \/ journal[i].revisionId = revisionId
  /\ source \in {"authority", "git", "pijul", "other"}
  /\ journal' = Append(journal,
       [position |-> HeadPosition + 1, eventId |-> eventId,
        revisionId |-> revisionId, predecessor |-> JournalHead.revisionId,
        content |-> ContentAt(targetPosition), kind |-> "rollback", source |-> source])
  /\ UNCHANGED <<pending, appliedPosition, replicaObservations, crashed>>

Next ==
  \/ \E e \in EventIds, r \in RevisionIds, c \in Contents,
        s \in {"authority", "git", "pijul", "other"} : Prepare(e, r, c, s)
  \/ CommitDurably
  \/ ApplyCommitted
  \/ Crash
  \/ Recover
  \/ \E replica \in ReplicaIds, p \in 0..HeadPosition : ObserveReplica(replica, p)
  \/ \E e \in EventIds, r \in RevisionIds,
        s \in {"authority", "git", "pijul", "other"}, p \in 0..HeadPosition :
        Rollback(e, r, s, p)

Spec == Init /\ [][Next]_vars /\ WF_vars(Recover)

TypeOK ==
  /\ journal \in Seq([position : Nat, eventId : EventIds \cup {"genesis"},
       revisionId : RevisionIds \cup {"rev0"},
       predecessor : RevisionIds \cup {"NoRevision"}, content : Contents,
       kind : {"genesis", "change", "rollback"},
       source : {"authority", "git", "pijul", "other"}])
  /\ (pending = "None" \/ pending \in
       [eventId : EventIds, revisionId : RevisionIds, predecessor : RevisionIds,
        content : Contents, kind : {"change", "rollback"},
        source : {"authority", "git", "pijul", "other"}])
  /\ appliedPosition \in 0..HeadPosition
  /\ replicaObservations \in [ReplicaIds -> 0..HeadPosition]
  /\ crashed \in BOOLEAN

AppendOnly ==
  [][Len(journal') >= Len(journal) /\
     SubSeq(journal', 1, Len(journal)) = journal]_vars

UniqueEventAndRevisionIds ==
  \A i, j \in 1..Len(journal) :
    i # j => journal[i].eventId # journal[j].eventId /\
             journal[i].revisionId # journal[j].revisionId

PositionAndPredecessorContinuity ==
  \A i \in 2..Len(journal) :
    /\ journal[i].position = i - 1
    /\ journal[i].predecessor = journal[i-1].revisionId

RollbackRestoresContentAsNewEvent ==
  \A i \in 2..Len(journal) :
    journal[i].kind = "rollback" =>
      /\ journal[i].position > 0
      /\ \E j \in 1..i-1 : journal[i].content = journal[j].content

VCSObservationIsNonAuthoritative ==
  \A r \in ReplicaIds : replicaObservations[r] <= HeadPosition

AppliedStateIsDurable ==
  appliedPosition <= HeadPosition

=============================================================================
