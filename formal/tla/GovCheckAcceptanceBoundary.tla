---- MODULE GovCheckAcceptanceBoundary ----
EXTENDS Naturals

CONSTANTS
    Candidates, Bases, Policies, Verifiers, Results,
    BoundaryMode, RootAuthority,
    InitialBase, InitialPolicy, InitialVerifier, NoValue,
    EvalNone, EvalReady, EvalStale,
    OverrideNone, OverrideActive, OverrideExpired,
    DecisionNone, DecisionPass, DecisionBlocked, DecisionRisk, DecisionStale,
    PublicationNone, PublicationPublished,
    KindNone, KindVerified, KindRiskAccepted, KindUncontrolled,
    BypassNone, BypassRecorded,
    Pass, Fail, Unknown, Conflict,
    Enforced, Advisory, AdminBypassable,
    RiskAcceptanceIds, RiskReasons, BypassActors,
    AdvisoryBypassReason, AdminBypassReason, MaxTick

VARIABLES
    currentBase,
    currentPolicy,
    currentVerifier,
    tick,
    evaluation,
    risk,
    decision,
    publication,
    bypass

vars == << currentBase, currentPolicy, currentVerifier, tick,
           evaluation, risk, decision, publication, bypass >>

NoEvaluation ==
    [ status |-> EvalNone,
      candidate |-> NoValue,
      base |-> NoValue,
      policy |-> NoValue,
      verifier |-> NoValue,
      result |-> NoValue,
      trusted |-> FALSE ]

NoRisk ==
    [ status |-> OverrideNone,
      id |-> NoValue,
      candidate |-> NoValue,
      base |-> NoValue,
      policy |-> NoValue,
      verifier |-> NoValue,
      authority |-> NoValue,
      reason |-> NoValue,
      expiresAt |-> 0 ]

NoDecision ==
    [ status |-> DecisionNone,
      candidate |-> NoValue,
      base |-> NoValue,
      policy |-> NoValue,
      verifier |-> NoValue,
      result |-> NoValue,
      authority |-> NoValue,
      riskId |-> NoValue ]

NoPublication ==
    [ status |-> PublicationNone,
      candidate |-> NoValue,
      base |-> NoValue,
      policy |-> NoValue,
      verifier |-> NoValue,
      kind |-> KindNone,
      result |-> NoValue ]

NoBypass ==
    [ status |-> BypassNone,
      candidate |-> NoValue,
      actor |-> NoValue,
      reason |-> NoValue ]

Init ==
    /\ currentBase = InitialBase
    /\ currentPolicy = InitialPolicy
    /\ currentVerifier = InitialVerifier
    /\ tick = 0
    /\ evaluation = NoEvaluation
    /\ risk = NoRisk
    /\ decision = NoDecision
    /\ publication = NoPublication
    /\ bypass = NoBypass

ValidEvaluationContext ==
    /\ evaluation.base = currentBase
    /\ evaluation.policy = currentPolicy
    /\ evaluation.verifier = currentVerifier

ValidRiskOverride ==
    /\ risk.status = OverrideActive
    /\ risk.candidate = evaluation.candidate
    /\ risk.base = currentBase
    /\ risk.policy = currentPolicy
    /\ risk.verifier = currentVerifier
    /\ risk.authority = RootAuthority
    /\ risk.reason \in RiskReasons
    /\ risk.expiresAt \in 0..MaxTick
    /\ tick < risk.expiresAt

EvaluateFor(candidate, result, trusted) ==
    /\ publication.status = PublicationNone
    /\ evaluation.status \in {EvalNone, EvalReady, EvalStale}
    /\ decision.status \in {DecisionNone, DecisionBlocked, DecisionStale}
    /\ candidate \in Candidates
    /\ result \in Results
    /\ trusted \in BOOLEAN
    /\ evaluation' =
        [ status |-> EvalReady,
          candidate |-> candidate,
          base |-> currentBase,
          policy |-> currentPolicy,
          verifier |-> currentVerifier,
          result |-> result,
          trusted |-> trusted ]
    /\ risk' = NoRisk
    /\ decision' = NoDecision
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier, tick,
                    publication, bypass >>

Evaluate ==
    \E candidate \in Candidates, result \in Results, trusted \in BOOLEAN:
        EvaluateFor(candidate, result, trusted)

GrantRiskAcceptanceFor(id, reason, lifetime) ==
    /\ publication.status = PublicationNone
    /\ evaluation.status = EvalReady
    /\ ValidEvaluationContext
    /\ evaluation.result \in {Fail, Unknown, Conflict}
    /\ risk.status \in {OverrideNone, OverrideExpired}
    /\ id \in RiskAcceptanceIds
    /\ reason \in RiskReasons
    /\ lifetime \in {1, 2}
    /\ tick + lifetime <= MaxTick
    /\ risk' =
        [ status |-> OverrideActive,
          id |-> id,
          candidate |-> evaluation.candidate,
          base |-> currentBase,
          policy |-> currentPolicy,
          verifier |-> currentVerifier,
          authority |-> RootAuthority,
          reason |-> reason,
          expiresAt |-> tick + lifetime ]
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier, tick,
                    evaluation, decision, publication, bypass >>

GrantRiskAcceptance ==
    \E id \in RiskAcceptanceIds, reason \in RiskReasons, lifetime \in {1, 2}:
        GrantRiskAcceptanceFor(id, reason, lifetime)

GatePass ==
    /\ publication.status = PublicationNone
    /\ evaluation.status = EvalReady
    /\ ValidEvaluationContext
    /\ evaluation.result = Pass
    /\ evaluation.trusted = TRUE
    /\ decision.status \in {DecisionNone, DecisionBlocked, DecisionStale}
    /\ decision' =
        [ status |-> DecisionPass,
          candidate |-> evaluation.candidate,
          base |-> currentBase,
          policy |-> currentPolicy,
          verifier |-> currentVerifier,
          result |-> Pass,
          authority |-> NoValue,
          riskId |-> NoValue ]
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier, tick,
                    evaluation, risk, publication, bypass >>

GateWithRiskAcceptance ==
    /\ publication.status = PublicationNone
    /\ evaluation.status = EvalReady
    /\ ValidEvaluationContext
    /\ evaluation.result \in {Fail, Unknown, Conflict}
    /\ ValidRiskOverride
    /\ decision.status \in {DecisionNone, DecisionBlocked, DecisionStale}
    /\ decision' =
        [ status |-> DecisionRisk,
          candidate |-> evaluation.candidate,
          base |-> currentBase,
          policy |-> currentPolicy,
          verifier |-> currentVerifier,
          result |-> evaluation.result,
          authority |-> RootAuthority,
          riskId |-> risk.id ]
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier, tick,
                    evaluation, risk, publication, bypass >>

GateBlock ==
    /\ publication.status = PublicationNone
    /\ evaluation.status = EvalReady
    /\ decision.status \in {DecisionNone, DecisionBlocked, DecisionStale}
    /\ ~(evaluation.result = Pass /\ evaluation.trusted = TRUE /\ ValidEvaluationContext)
    /\ ~ValidRiskOverride
    /\ decision' =
        [ status |-> DecisionBlocked,
          candidate |-> evaluation.candidate,
          base |-> evaluation.base,
          policy |-> evaluation.policy,
          verifier |-> evaluation.verifier,
          result |-> evaluation.result,
          authority |-> NoValue,
          riskId |-> NoValue ]
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier, tick,
                    evaluation, risk, publication, bypass >>

Publish ==
    /\ publication.status = PublicationNone
    /\ decision.status \in {DecisionPass, DecisionRisk}
    /\ decision.candidate = evaluation.candidate
    /\ decision.base = currentBase
    /\ decision.policy = currentPolicy
    /\ decision.verifier = currentVerifier
    /\ publication' =
        [ status |-> PublicationPublished,
          candidate |-> decision.candidate,
          base |-> decision.base,
          policy |-> decision.policy,
          verifier |-> decision.verifier,
          kind |-> IF decision.status = DecisionPass
                    THEN KindVerified ELSE KindRiskAccepted,
          result |-> decision.result ]
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier, tick,
                    evaluation, risk, decision, bypass >>

DirectPublishFor(candidate, actor) ==
    /\ BoundaryMode \in {Advisory, AdminBypassable}
    /\ publication.status = PublicationNone
    /\ candidate \in Candidates
    /\ actor \in BypassActors
    /\ (BoundaryMode = AdminBypassable => actor = "administrator")
    /\ publication' =
        [ status |-> PublicationPublished,
          candidate |-> candidate,
          base |-> currentBase,
          policy |-> currentPolicy,
          verifier |-> currentVerifier,
          kind |-> KindUncontrolled,
          result |-> Unknown ]
    /\ bypass' =
        [ status |-> BypassRecorded,
          candidate |-> candidate,
          actor |-> actor,
          reason |-> IF BoundaryMode = Advisory
                       THEN AdvisoryBypassReason ELSE AdminBypassReason ]
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier, tick,
                    evaluation, risk, decision >>

DirectPublish ==
    \E candidate \in Candidates, actor \in BypassActors:
        DirectPublishFor(candidate, actor)

AdvanceBaseTo(newBase) ==
    /\ publication.status = PublicationNone
    /\ newBase \in Bases
    /\ newBase # currentBase
    /\ currentBase' = newBase
    /\ evaluation' =
        IF evaluation.status = EvalReady
        THEN [evaluation EXCEPT !.status = EvalStale] ELSE evaluation
    /\ risk' =
        IF risk.status = OverrideActive
        THEN [risk EXCEPT !.status = OverrideExpired] ELSE risk
    /\ decision' =
        IF decision.status \in {DecisionPass, DecisionRisk, DecisionBlocked}
        THEN [decision EXCEPT !.status = DecisionStale] ELSE decision
    /\ UNCHANGED << currentPolicy, currentVerifier, tick, publication, bypass >>

AdvanceBase ==
    \E newBase \in Bases: AdvanceBaseTo(newBase)

ChangePolicyTo(newPolicy) ==
    /\ publication.status = PublicationNone
    /\ newPolicy \in Policies
    /\ newPolicy # currentPolicy
    /\ currentPolicy' = newPolicy
    /\ evaluation' =
        IF evaluation.status = EvalReady
        THEN [evaluation EXCEPT !.status = EvalStale] ELSE evaluation
    /\ risk' =
        IF risk.status = OverrideActive
        THEN [risk EXCEPT !.status = OverrideExpired] ELSE risk
    /\ decision' =
        IF decision.status \in {DecisionPass, DecisionRisk, DecisionBlocked}
        THEN [decision EXCEPT !.status = DecisionStale] ELSE decision
    /\ UNCHANGED << currentBase, currentVerifier, tick, publication, bypass >>

ChangePolicy ==
    \E newPolicy \in Policies: ChangePolicyTo(newPolicy)

ChangeVerifierTo(newVerifier) ==
    /\ publication.status = PublicationNone
    /\ newVerifier \in Verifiers
    /\ newVerifier # currentVerifier
    /\ currentVerifier' = newVerifier
    /\ evaluation' =
        IF evaluation.status = EvalReady
        THEN [evaluation EXCEPT !.status = EvalStale] ELSE evaluation
    /\ risk' =
        IF risk.status = OverrideActive
        THEN [risk EXCEPT !.status = OverrideExpired] ELSE risk
    /\ decision' =
        IF decision.status \in {DecisionPass, DecisionRisk, DecisionBlocked}
        THEN [decision EXCEPT !.status = DecisionStale] ELSE decision
    /\ UNCHANGED << currentBase, currentPolicy, tick, publication, bypass >>

ChangeVerifier ==
    \E newVerifier \in Verifiers: ChangeVerifierTo(newVerifier)

Tick ==
    /\ tick < MaxTick
    /\ tick' = tick + 1
    /\ risk' =
        IF risk.status = OverrideActive /\ tick + 1 >= risk.expiresAt
        THEN [risk EXCEPT !.status = OverrideExpired] ELSE risk
    /\ decision' =
        IF decision.status = DecisionRisk
           /\ publication.status = PublicationNone
           /\ tick + 1 >= risk.expiresAt
        THEN [decision EXCEPT !.status = DecisionStale] ELSE decision
    /\ UNCHANGED << currentBase, currentPolicy, currentVerifier,
                    evaluation, publication, bypass >>

Next ==
    \/ Evaluate
    \/ GrantRiskAcceptance
    \/ GatePass
    \/ GateWithRiskAcceptance
    \/ GateBlock
    \/ Publish
    \/ DirectPublish
    \/ AdvanceBase
    \/ ChangePolicy
    \/ ChangeVerifier
    \/ Tick

Spec ==
    Init /\ [][Next]_vars

BypassSpec ==
    Init /\ [][DirectPublish]_vars /\ WF_vars(DirectPublish)

TypeOKCore ==
    /\ currentBase \in Bases
    /\ currentPolicy \in Policies
    /\ currentVerifier \in Verifiers
    /\ tick \in 0..MaxTick

TypeOKEvaluation ==
    /\ evaluation.status \in {EvalNone, EvalReady, EvalStale}
    /\ evaluation.candidate \in Candidates \cup {NoValue}
    /\ evaluation.base \in Bases \cup {NoValue}
    /\ evaluation.policy \in Policies \cup {NoValue}
    /\ evaluation.verifier \in Verifiers \cup {NoValue}
    /\ evaluation.result \in Results \cup {NoValue}
    /\ evaluation.trusted \in BOOLEAN

TypeOKRisk ==
    /\ risk.status \in {OverrideNone, OverrideActive, OverrideExpired}
    /\ risk.id \in RiskAcceptanceIds \cup {NoValue}
    /\ risk.candidate \in Candidates \cup {NoValue}
    /\ risk.base \in Bases \cup {NoValue}
    /\ risk.policy \in Policies \cup {NoValue}
    /\ risk.verifier \in Verifiers \cup {NoValue}
    /\ risk.authority \in {RootAuthority, NoValue}
    /\ risk.reason \in RiskReasons \cup {NoValue}
    /\ risk.expiresAt \in 0..MaxTick

TypeOKDecision ==
    /\ decision.status \in {DecisionNone, DecisionPass, DecisionBlocked, DecisionRisk, DecisionStale}
    /\ decision.candidate \in Candidates \cup {NoValue}
    /\ decision.base \in Bases \cup {NoValue}
    /\ decision.policy \in Policies \cup {NoValue}
    /\ decision.verifier \in Verifiers \cup {NoValue}
    /\ decision.result \in Results \cup {NoValue}
    /\ decision.authority \in {RootAuthority, NoValue}
    /\ decision.riskId \in RiskAcceptanceIds \cup {NoValue}

TypeOKPublicationStatus ==
    publication.status \in {PublicationNone, PublicationPublished}

TypeOKPublicationCandidate ==
    publication.candidate \in Candidates \cup {NoValue}

TypeOKPublicationBase ==
    publication.base \in Bases \cup {NoValue}

TypeOKPublicationPolicy ==
    publication.policy \in Policies \cup {NoValue}

TypeOKPublicationVerifier ==
    publication.verifier \in Verifiers \cup {NoValue}

TypeOKPublicationKind ==
    publication.kind \in {KindNone, KindVerified, KindRiskAccepted, KindUncontrolled}

TypeOKPublicationResult ==
    publication.result \in Results \cup {NoValue}

TypeOKPublication ==
    TypeOKPublicationStatus
    /\ TypeOKPublicationCandidate
    /\ TypeOKPublicationBase
    /\ TypeOKPublicationPolicy
    /\ TypeOKPublicationVerifier
    /\ TypeOKPublicationKind
    /\ TypeOKPublicationResult

TypeOKBypass ==
    /\ bypass.status \in {BypassNone, BypassRecorded}
    /\ bypass.candidate \in Candidates \cup {NoValue}
    /\ bypass.actor \in BypassActors \cup {NoValue}
    /\ bypass.reason \in {AdvisoryBypassReason, AdminBypassReason, NoValue}

TypeOK ==
    (TypeOKCore)
    /\ (TypeOKEvaluation)
    /\ (TypeOKRisk)
    /\ (TypeOKDecision)
    /\ (TypeOKPublication)
    /\ (TypeOKBypass)

NoFalsePass ==
    decision.status = DecisionPass =>
        /\ evaluation.status = EvalReady
        /\ evaluation.result = Pass
        /\ evaluation.trusted = TRUE
        /\ decision.candidate = evaluation.candidate
        /\ decision.base = currentBase
        /\ decision.policy = currentPolicy
        /\ decision.verifier = currentVerifier

UnknownNeverPass ==
    (evaluation.status = EvalReady /\ evaluation.result \in {Unknown, Conflict})
        => decision.status # DecisionPass

RiskIsNotPass ==
    decision.status = DecisionRisk =>
        /\ evaluation.result \in {Fail, Unknown, Conflict}
        /\ decision.riskId = risk.id
        /\ decision.authority = RootAuthority
        /\ decision.result = evaluation.result
        /\ (publication.status = PublicationNone => risk.status = OverrideActive)
        /\ (publication.status = PublicationPublished => publication.kind = KindRiskAccepted)

FreshDecision ==
    decision.status \in {DecisionPass, DecisionRisk} =>
        /\ decision.base = currentBase
        /\ decision.policy = currentPolicy
        /\ decision.verifier = currentVerifier

RiskOverrideScoped ==
    risk.status = OverrideActive =>
        /\ evaluation.status = EvalReady
        /\ risk.candidate = evaluation.candidate
        /\ risk.base = currentBase
        /\ risk.policy = currentPolicy
        /\ risk.verifier = currentVerifier
        /\ risk.authority = RootAuthority
        /\ risk.reason \in RiskReasons
        /\ tick < risk.expiresAt

PublicationBound ==
    publication.status = PublicationPublished =>
        /\ publication.base = currentBase
        /\ publication.policy = currentPolicy
        /\ publication.verifier = currentVerifier
        /\ IF publication.kind = KindVerified
           THEN
               /\ decision.status = DecisionPass
               /\ publication.candidate = decision.candidate
               /\ publication.result = Pass
           ELSE IF publication.kind = KindRiskAccepted
                THEN
                    /\ decision.status = DecisionRisk
                    /\ publication.candidate = decision.candidate
                    /\ publication.result = decision.result
                ELSE
                    /\ publication.kind = KindUncontrolled
                    /\ BoundaryMode # Enforced
                    /\ bypass.status = BypassRecorded
                    /\ bypass.candidate = publication.candidate

NoSilentBypass ==
    publication.kind = KindUncontrolled =>
        /\ bypass.status = BypassRecorded
        /\ bypass.candidate = publication.candidate
        /\ bypass.actor \in BypassActors
        /\ (BoundaryMode = AdminBypassable => bypass.actor = "administrator")
        /\ (BoundaryMode = Advisory => bypass.reason = AdvisoryBypassReason)
        /\ (BoundaryMode = AdminBypassable => bypass.reason = AdminBypassReason)

NoUncontrolledWhenEnforced ==
    BoundaryMode = Enforced => publication.kind # KindUncontrolled

UncontrolledPublicationReachable ==
    <> (publication.status = PublicationPublished /\ publication.kind = KindUncontrolled)

====
