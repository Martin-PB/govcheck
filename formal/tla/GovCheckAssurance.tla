-------------------------- MODULE GovCheckAssurance --------------------------
EXTENDS Naturals

CONSTANTS
  Claims, Evidence, Dependencies, Versions, Actors, AuthorizedReviewers,
  RootClaim, LeafClaim, RootEvidence, LeafEvidence,
  CandidateDependency, PolicyDependency, InitialVersion,
  ProducerActor, ReviewerActor, MaxTime, NoSnapshot

EvidenceOutcomes ==
  {"Supports", "Refutes", "Unknown", "Unsupported", "NotRun",
   "Incomplete", "Conflict"}

ASSUME Claims # {}
ASSUME Evidence # {}
ASSUME Dependencies # {}
ASSUME Versions # {}
ASSUME Actors # {}
ASSUME RootClaim \in Claims
ASSUME LeafClaim \in (Claims \ {RootClaim})
ASSUME RootEvidence \in Evidence
ASSUME LeafEvidence \in (Evidence \ {RootEvidence})
ASSUME CandidateDependency \in Dependencies
ASSUME PolicyDependency \in Dependencies
ASSUME InitialVersion \in Versions
ASSUME ProducerActor \in Actors
ASSUME ReviewerActor \in Actors
ASSUME AuthorizedReviewers \subseteq Actors
ASSUME MaxTime \in Nat

ClaimEvidence ==
  [c \in Claims |-> IF c = RootClaim THEN {RootEvidence} ELSE {LeafEvidence}]

ClaimEvidenceClosure ==
  [c \in Claims |->
     IF c = RootClaim THEN {RootEvidence, LeafEvidence} ELSE {LeafEvidence}]

ClaimClosure ==
  [c \in Claims |->
     IF c = RootClaim THEN {RootClaim, LeafClaim} ELSE {LeafClaim}]

ClaimRank ==
  [c \in Claims |-> IF c = RootClaim THEN 1 ELSE 0]

Children(c) ==
  IF c = RootClaim THEN {LeafClaim} ELSE {}

ClaimDependencies ==
  [c \in Claims |->
     IF c = RootClaim
     THEN {CandidateDependency, PolicyDependency}
     ELSE {CandidateDependency}]

ClaimProducer == [c \in Claims |-> ProducerActor]
ClaimReviewer == [c \in Claims |-> ReviewerActor]

EvidenceDependencies ==
  [e \in Evidence |->
     IF e = RootEvidence
     THEN {PolicyDependency}
     ELSE {CandidateDependency}]

InitialVersions == [d \in Dependencies |-> InitialVersion]

InitialEvidenceVersions ==
  [e \in Evidence |-> [d \in Dependencies |-> InitialVersion]]

InitialEvidenceOutcomes ==
  [e \in Evidence |-> "Supports"]

InitialEvidenceExpiry == [e \in Evidence |-> MaxTime]

ASSUME \A c \in Claims :
  \A child \in Children(c) : ClaimRank[child] < ClaimRank[c]
ASSUME \A c \in Claims :
  ClaimEvidenceClosure[c] =
    ClaimEvidence[c] \cup
      UNION {ClaimEvidenceClosure[child] : child \in Children(c)}
ASSUME \A c \in Claims :
  ClaimClosure[c] =
    {c} \cup UNION {ClaimClosure[child] : child \in Children(c)}
ASSUME \A c \in Claims :
  ClaimDependencies[c] =
    UNION {EvidenceDependencies[e] : e \in ClaimEvidenceClosure[c]}

VARIABLES
  currentVersions, evidenceOutcomes, evidenceVersions, evidenceExpiry,
  revokedEvidence, reviewedClaims, now, accepted, acceptedDependencyVersions

vars ==
  <<currentVersions, evidenceOutcomes, evidenceVersions, evidenceExpiry,
    revokedEvidence, reviewedClaims, now, accepted, acceptedDependencyVersions>>

EvidenceStale(e) ==
  \/ e \in revokedEvidence
  \/ now > evidenceExpiry[e]
  \/ \E d \in EvidenceDependencies[e] :
       evidenceVersions[e][d] # currentVersions[d]

EvidenceCurrent(e) ==
  /\ ~EvidenceStale(e)
  /\ evidenceOutcomes[e] \in {"Supports", "Refutes", "Conflict"}

CurrentSupporting(c) ==
  {e \in ClaimEvidenceClosure[c] :
     /\ ~EvidenceStale(e)
     /\ evidenceOutcomes[e] = "Supports"}

CurrentRefuting(c) ==
  {e \in ClaimEvidenceClosure[c] :
     /\ ~EvidenceStale(e)
     /\ evidenceOutcomes[e] = "Refutes"}

CurrentConflicting(c) ==
  {e \in ClaimEvidenceClosure[c] :
     /\ ~EvidenceStale(e)
     /\ evidenceOutcomes[e] = "Conflict"}

ClaimStatus(c) ==
  IF CurrentConflicting(c) # {}
     \/ (CurrentSupporting(c) # {} /\ CurrentRefuting(c) # {})
  THEN "Conflict"
  ELSE IF \E e \in ClaimEvidenceClosure[c] : EvidenceStale(e)
  THEN "Stale"
  ELSE IF CurrentRefuting(c) # {}
  THEN "Refuted"
  ELSE IF \E e \in ClaimEvidenceClosure[c] :
            evidenceOutcomes[e] = "Incomplete"
  THEN "Incomplete"
  ELSE IF \E e \in ClaimEvidenceClosure[c] :
            evidenceOutcomes[e] = "Unsupported"
  THEN "Unsupported"
  ELSE IF \E e \in ClaimEvidenceClosure[c] :
            evidenceOutcomes[e] = "NotRun"
  THEN "NotRun"
  ELSE IF \E e \in ClaimEvidenceClosure[c] :
            evidenceOutcomes[e] = "Unknown"
  THEN "Unknown"
  ELSE IF ClaimEvidenceClosure[c] # {}
          /\ \A e \in ClaimEvidenceClosure[c] :
               /\ EvidenceCurrent(e)
               /\ evidenceOutcomes[e] = "Supports"
  THEN IF ClaimClosure[c] \subseteq reviewedClaims
          /\ \A reviewedClaim \in ClaimClosure[c] :
               /\ ClaimReviewer[reviewedClaim] \in AuthorizedReviewers
               /\ ClaimReviewer[reviewedClaim] # ClaimProducer[reviewedClaim]
       THEN "Supported"
       ELSE "NotIndependentlyReviewed"
  ELSE "Unknown"

Init ==
  /\ currentVersions = InitialVersions
  /\ evidenceOutcomes = InitialEvidenceOutcomes
  /\ evidenceVersions = InitialEvidenceVersions
  /\ evidenceExpiry = InitialEvidenceExpiry
  /\ revokedEvidence = {}
  /\ reviewedClaims = {}
  /\ now = 0
  /\ accepted = FALSE
  /\ acceptedDependencyVersions = NoSnapshot

PublishEvidence(e, outcome, expiry) ==
  /\ e \in Evidence
  /\ outcome \in EvidenceOutcomes
  /\ expiry \in 0..MaxTime
  /\ expiry >= now
  /\ evidenceOutcomes' = [evidenceOutcomes EXCEPT ![e] = outcome]
  /\ evidenceVersions' = [evidenceVersions EXCEPT ![e] = currentVersions]
  /\ evidenceExpiry' = [evidenceExpiry EXCEPT ![e] = expiry]
  /\ revokedEvidence' = revokedEvidence \ {e}
  /\ reviewedClaims' =
       {c \in reviewedClaims : e \notin ClaimEvidenceClosure[c]}
  /\ accepted' =
       IF e \in ClaimEvidenceClosure[RootClaim] THEN FALSE ELSE accepted
  /\ acceptedDependencyVersions' =
       IF e \in ClaimEvidenceClosure[RootClaim]
       THEN NoSnapshot ELSE acceptedDependencyVersions
  /\ UNCHANGED <<currentVersions, now>>

ChangeDependency(dep, version) ==
  /\ dep \in Dependencies
  /\ version \in Versions
  /\ version # currentVersions[dep]
  /\ currentVersions' = [currentVersions EXCEPT ![dep] = version]
  /\ reviewedClaims' =
       {c \in reviewedClaims : dep \notin ClaimDependencies[c]}
  /\ accepted' =
       IF dep \in ClaimDependencies[RootClaim] THEN FALSE ELSE accepted
  /\ acceptedDependencyVersions' =
       IF dep \in ClaimDependencies[RootClaim]
       THEN NoSnapshot ELSE acceptedDependencyVersions
  /\ UNCHANGED <<evidenceOutcomes, evidenceVersions, evidenceExpiry,
                 revokedEvidence, now>>

RevokeEvidence(e) ==
  /\ e \in Evidence
  /\ e \notin revokedEvidence
  /\ revokedEvidence' = revokedEvidence \cup {e}
  /\ reviewedClaims' =
       {c \in reviewedClaims : e \notin ClaimEvidenceClosure[c]}
  /\ accepted' =
       IF e \in ClaimEvidenceClosure[RootClaim] THEN FALSE ELSE accepted
  /\ acceptedDependencyVersions' =
       IF e \in ClaimEvidenceClosure[RootClaim]
       THEN NoSnapshot ELSE acceptedDependencyVersions
  /\ UNCHANGED <<currentVersions, evidenceOutcomes, evidenceVersions,
                 evidenceExpiry, now>>

ReviewClaim(c, actor) ==
  /\ c \in Claims
  /\ actor = ClaimReviewer[c]
  /\ actor \in AuthorizedReviewers
  /\ actor # ClaimProducer[c]
  /\ ClaimEvidenceClosure[c] # {}
  /\ \A e \in ClaimEvidenceClosure[c] :
       /\ EvidenceCurrent(e)
       /\ evidenceOutcomes[e] = "Supports"
  /\ reviewedClaims' = reviewedClaims \cup {c}
  /\ UNCHANGED <<currentVersions, evidenceOutcomes, evidenceVersions,
                 evidenceExpiry, revokedEvidence, now, accepted,
                 acceptedDependencyVersions>>

Tick ==
  /\ now < MaxTime
  /\ now' = now + 1
  /\ reviewedClaims' =
       {c \in reviewedClaims :
          \A e \in ClaimEvidenceClosure[c] : now + 1 <= evidenceExpiry[e]}
  /\ accepted' =
       IF \E e \in ClaimEvidenceClosure[RootClaim] :
            now + 1 > evidenceExpiry[e]
       THEN FALSE ELSE accepted
  /\ acceptedDependencyVersions' =
       IF \E e \in ClaimEvidenceClosure[RootClaim] :
            now + 1 > evidenceExpiry[e]
       THEN NoSnapshot ELSE acceptedDependencyVersions
  /\ UNCHANGED <<currentVersions, evidenceOutcomes, evidenceVersions,
                 evidenceExpiry, revokedEvidence>>

AcceptRoot ==
  /\ accepted = FALSE
  /\ ClaimStatus(RootClaim) = "Supported"
  /\ accepted' = TRUE
  /\ acceptedDependencyVersions' = currentVersions
  /\ UNCHANGED <<currentVersions, evidenceOutcomes, evidenceVersions,
                 evidenceExpiry, revokedEvidence, reviewedClaims, now>>

Next ==
  \/ \E e \in Evidence, outcome \in EvidenceOutcomes,
       expiry \in 0..MaxTime : PublishEvidence(e, outcome, expiry)
  \/ \E d \in Dependencies, v \in Versions : ChangeDependency(d, v)
  \/ \E e \in Evidence : RevokeEvidence(e)
  \/ \E c \in Claims, actor \in Actors : ReviewClaim(c, actor)
  \/ Tick
  \/ AcceptRoot

TypeOK ==
  /\ currentVersions \in [Dependencies -> Versions]
  /\ evidenceOutcomes \in [Evidence -> EvidenceOutcomes]
  /\ evidenceVersions \in [Evidence -> [Dependencies -> Versions]]
  /\ evidenceExpiry \in [Evidence -> 0..MaxTime]
  /\ revokedEvidence \subseteq Evidence
  /\ reviewedClaims \subseteq Claims
  /\ now \in 0..MaxTime
  /\ accepted \in BOOLEAN
  /\ (acceptedDependencyVersions = NoSnapshot
      \/ acceptedDependencyVersions \in [Dependencies -> Versions])

ArgumentGraphWellFormed ==
  /\ \A c \in Claims :
       \A child \in Children(c) : ClaimRank[child] < ClaimRank[c]
  /\ \A c \in Claims :
       ClaimEvidenceClosure[c] =
         ClaimEvidence[c] \cup
           UNION {ClaimEvidenceClosure[child] : child \in Children(c)}
  /\ \A c \in Claims :
       ClaimClosure[c] =
         {c} \cup UNION {ClaimClosure[child] : child \in Children(c)}
  /\ \A c \in Claims :
       ClaimDependencies[c] =
         UNION {EvidenceDependencies[e] : e \in ClaimEvidenceClosure[c]}

ReviewBinding ==
  \A c \in reviewedClaims :
    /\ ClaimReviewer[c] \in AuthorizedReviewers
    /\ ClaimReviewer[c] # ClaimProducer[c]
    /\ \A e \in ClaimEvidenceClosure[c] :
         /\ EvidenceCurrent(e)
         /\ evidenceOutcomes[e] = "Supports"

ClaimStatusSoundness ==
  \A c \in Claims :
    ClaimStatus(c) = "Supported" =>
      /\ ClaimEvidenceClosure[c] # {}
      /\ ClaimClosure[c] \subseteq reviewedClaims
      /\ \A e \in ClaimEvidenceClosure[c] :
           /\ EvidenceCurrent(e)
           /\ evidenceOutcomes[e] = "Supports"
      /\ \A reviewedClaim \in ClaimClosure[c] :
           /\ ClaimReviewer[reviewedClaim] \in AuthorizedReviewers
           /\ ClaimReviewer[reviewedClaim] # ClaimProducer[reviewedClaim]

AcceptedImpliesSupported ==
  accepted => ClaimStatus(RootClaim) = "Supported"

AcceptedDependencySnapshotCurrent ==
  accepted =>
    \A d \in ClaimDependencies[RootClaim] :
      acceptedDependencyVersions[d] = currentVersions[d]

RevokedEvidenceNotCurrent ==
  \A e \in revokedEvidence : ~EvidenceCurrent(e)

AcceptedDiscipline ==
  [] (accepted => ClaimStatus(RootClaim) = "Supported")

Spec ==
  Init /\ [][Next]_vars

=============================================================================
