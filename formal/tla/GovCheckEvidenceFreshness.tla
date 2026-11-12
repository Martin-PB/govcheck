---------------------- MODULE GovCheckEvidenceFreshness ----------------------
EXTENDS Naturals

CONSTANTS Revisions, InitialRevision, NextRevision

ASSUME Revisions = {InitialRevision, NextRevision}
ASSUME InitialRevision # NextRevision

VARIABLES currentRevision, evidenceRevision, evidenceStatus, accepted

vars == <<currentRevision, evidenceRevision, evidenceStatus, accepted>>

EvidenceFresh == evidenceRevision = currentRevision

Init ==
  /\ currentRevision = InitialRevision
  /\ evidenceRevision = InitialRevision
  /\ evidenceStatus = "Passed"
  /\ accepted = FALSE

ChangeSourceRevision ==
  /\ currentRevision = InitialRevision
  /\ currentRevision' = NextRevision
  /\ accepted' = FALSE
  /\ UNCHANGED <<evidenceRevision, evidenceStatus>>

ReevaluateEvidence ==
  /\ evidenceRevision' = currentRevision
  /\ evidenceStatus' \in {"Passed", "Failed", "Inconclusive", "Unknown", "Unsupported", "NotRun"}
  /\ UNCHANGED <<currentRevision, accepted>>

Accept ==
  /\ EvidenceFresh
  /\ evidenceStatus = "Passed"
  /\ accepted' = TRUE
  /\ UNCHANGED <<currentRevision, evidenceRevision, evidenceStatus>>

Next ==
  \/ ChangeSourceRevision
  \/ ReevaluateEvidence
  \/ Accept

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ currentRevision \in Revisions
  /\ evidenceRevision \in Revisions
  /\ evidenceStatus \in
       {"Passed", "Failed", "Inconclusive", "Unknown", "Unsupported", "NotRun"}
  /\ accepted \in BOOLEAN

AcceptedImpliesFresh ==
  accepted => (EvidenceFresh /\ evidenceStatus = "Passed")

NonPassingEvidenceCannotBeAccepted ==
  evidenceStatus # "Passed" => accepted = FALSE

=============================================================================
