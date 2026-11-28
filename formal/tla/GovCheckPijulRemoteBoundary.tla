---- MODULE GovCheckPijulRemoteBoundary ----
EXTENDS Naturals

CONSTANTS
    ChannelVersions, ChangeSets, Policies, Results,
    BoundaryMode, RootAuthority, InitialChannel, InitialPolicy, NoValue,
    PendingNone, PendingReady,
    EvalNone, EvalReady, EvalStale,
    DecisionNone, DecisionAccepted, DecisionRisk, DecisionBlocked, DecisionStale,
    AppliedNone, Applied,
    ReceiptNone, ReceiptCommitted, ReceiptFailed,
    BypassNone, BypassRecorded,
    Pass, Fail, Unknown, Conflict,
    Enforced, Advisory, AdminBypassable, BypassActors

VARIABLES
    currentChannel, currentPolicy,
    pending, evaluation, decision,
    applied, receipt, bypass

vars == << currentChannel, currentPolicy, pending, evaluation, decision,
           applied, receipt, bypass >>

NoPending ==
    [ status |-> PendingNone,
      changeSet |-> NoValue,
      candidate |-> NoValue,
      base |-> NoValue ]

NoEvaluation ==
    [ status |-> EvalNone,
      changeSet |-> NoValue,
      candidate |-> NoValue,
      base |-> NoValue,
      policy |-> NoValue,
      result |-> NoValue,
      trusted |-> FALSE ]

NoDecision ==
    [ status |-> DecisionNone,
      changeSet |-> NoValue,
      candidate |-> NoValue,
      base |-> NoValue,
      policy |-> NoValue,
      result |-> NoValue,
      authority |-> NoValue ]

NoApplied ==
    [ status |-> AppliedNone,
      changeSet |-> NoValue,
      candidate |-> NoValue,
      base |-> NoValue,
      kind |-> NoValue ]

NoReceipt ==
    [ status |-> ReceiptNone,
      changeSet |-> NoValue,
      candidate |-> NoValue,
      base |-> NoValue,
      outcome |-> NoValue ]

NoBypass ==
    [ status |-> BypassNone,
      changeSet |-> NoValue,
      actor |-> NoValue,
      reason |-> NoValue ]

Init ==
    /\ currentChannel = InitialChannel
    /\ currentPolicy = InitialPolicy
    /\ pending = NoPending
    /\ evaluation = NoEvaluation
    /\ decision = NoDecision
    /\ applied = NoApplied
    /\ receipt = NoReceipt
    /\ bypass = NoBypass

ReceiveChangeSetFor(changeSet, candidate) ==
    /\ applied.status = AppliedNone
    /\ pending.status \in {PendingNone, PendingReady}
    /\ changeSet \in ChangeSets
    /\ candidate \in ChannelVersions
    /\ candidate # currentChannel
    /\ pending' =
        [ status |-> PendingReady,
          changeSet |-> changeSet,
          candidate |-> candidate,
          base |-> currentChannel ]
    /\ evaluation' = NoEvaluation
    /\ decision' = NoDecision
    /\ UNCHANGED << currentChannel, currentPolicy, applied, receipt, bypass >>

ReceiveChangeSet ==
    \E changeSet \in ChangeSets, candidate \in ChannelVersions:
        ReceiveChangeSetFor(changeSet, candidate)

EvaluateFor(result, trusted) ==
    /\ pending.status = PendingReady
    /\ result \in Results
    /\ trusted \in BOOLEAN
    /\ evaluation' =
        [ status |-> EvalReady,
          changeSet |-> pending.changeSet,
          candidate |-> pending.candidate,
          base |-> pending.base,
          policy |-> currentPolicy,
          result |-> result,
          trusted |-> trusted ]
    /\ decision' = NoDecision
    /\ UNCHANGED << currentChannel, currentPolicy, pending, applied, receipt, bypass >>

Evaluate ==
    \E result \in Results, trusted \in BOOLEAN:
        EvaluateFor(result, trusted)

ContextFresh ==
    /\ pending.status = PendingReady
    /\ evaluation.status = EvalReady
    /\ evaluation.changeSet = pending.changeSet
    /\ evaluation.candidate = pending.candidate
    /\ evaluation.base = currentChannel
    /\ evaluation.base = pending.base
    /\ evaluation.policy = currentPolicy

AuthorizePass ==
    /\ applied.status = AppliedNone
    /\ ContextFresh
    /\ evaluation.result = Pass
    /\ evaluation.trusted = TRUE
    /\ decision' =
        [ status |-> DecisionAccepted,
          changeSet |-> evaluation.changeSet,
          candidate |-> evaluation.candidate,
          base |-> evaluation.base,
          policy |-> evaluation.policy,
          result |-> Pass,
          authority |-> RootAuthority ]
    /\ UNCHANGED << currentChannel, currentPolicy, pending, evaluation, applied, receipt, bypass >>

AuthorizeRisk ==
    /\ applied.status = AppliedNone
    /\ ContextFresh
    /\ evaluation.result \in {Fail, Unknown, Conflict}
    /\ decision' =
        [ status |-> DecisionRisk,
          changeSet |-> evaluation.changeSet,
          candidate |-> evaluation.candidate,
          base |-> evaluation.base,
          policy |-> evaluation.policy,
          result |-> evaluation.result,
          authority |-> RootAuthority ]
    /\ UNCHANGED << currentChannel, currentPolicy, pending, evaluation, applied, receipt, bypass >>

Block ==
    /\ applied.status = AppliedNone
    /\ evaluation.status = EvalReady
    /\ decision.status \in {DecisionNone, DecisionBlocked, DecisionStale}
    /\ ~(ContextFresh /\ evaluation.result = Pass /\ evaluation.trusted = TRUE)
    /\ decision' =
        [ status |-> DecisionBlocked,
          changeSet |-> evaluation.changeSet,
          candidate |-> evaluation.candidate,
          base |-> evaluation.base,
          policy |-> evaluation.policy,
          result |-> evaluation.result,
          authority |-> NoValue ]
    /\ UNCHANGED << currentChannel, currentPolicy, pending, evaluation, applied, receipt, bypass >>

ApplyAccepted ==
    /\ applied.status = AppliedNone
    /\ pending.status = PendingReady
    /\ decision.status \in {DecisionAccepted, DecisionRisk}
    /\ decision.changeSet = pending.changeSet
    /\ decision.candidate = pending.candidate
    /\ decision.base = currentChannel
    /\ decision.base = pending.base
    /\ decision.policy = currentPolicy
    /\ applied' =
        [ status |-> Applied,
          changeSet |-> pending.changeSet,
          candidate |-> pending.candidate,
          base |-> pending.base,
          kind |-> IF decision.status = DecisionAccepted
                    THEN "verified" ELSE "accepted-with-risk" ]
    /\ currentChannel' = pending.candidate
    /\ pending' = NoPending
    /\ receipt' = NoReceipt
    /\ UNCHANGED << currentPolicy, evaluation, decision, bypass >>

DirectApplyFor(changeSet, candidate, actor) ==
    /\ BoundaryMode \in {Advisory, AdminBypassable}
    /\ applied.status = AppliedNone
    /\ changeSet \in ChangeSets
    /\ candidate \in ChannelVersions
    /\ candidate # currentChannel
    /\ actor \in BypassActors
    /\ (BoundaryMode = AdminBypassable => actor = "administrator")
    /\ applied' =
        [ status |-> Applied,
          changeSet |-> changeSet,
          candidate |-> candidate,
          base |-> currentChannel,
          kind |-> "uncontrolled" ]
    /\ currentChannel' = candidate
    /\ pending' = NoPending
    /\ receipt' = NoReceipt
    /\ bypass' =
        [ status |-> BypassRecorded,
          changeSet |-> changeSet,
          actor |-> actor,
          reason |-> IF BoundaryMode = Advisory
                       THEN "no-enforcement-boundary"
                       ELSE "administrator-bypass" ]
    /\ UNCHANGED << currentPolicy, evaluation, decision >>

DirectApply ==
    \E changeSet \in ChangeSets, candidate \in ChannelVersions, actor \in BypassActors:
        DirectApplyFor(changeSet, candidate, actor)

PostReceiveReceipt ==
    /\ applied.status = Applied
    /\ receipt.status \in {ReceiptNone, ReceiptFailed}
    /\ receipt' =
        [ status |-> ReceiptCommitted,
          changeSet |-> applied.changeSet,
          candidate |-> applied.candidate,
          base |-> applied.base,
          outcome |-> applied.kind ]
    /\ UNCHANGED << currentChannel, currentPolicy, pending, evaluation, decision, applied, bypass >>

ReceiptFailure ==
    /\ applied.status = Applied
    /\ receipt.status = ReceiptNone
    /\ receipt' =
        [ status |-> ReceiptFailed,
          changeSet |-> applied.changeSet,
          candidate |-> applied.candidate,
          base |-> applied.base,
          outcome |-> "receipt-unavailable" ]
    /\ UNCHANGED << currentChannel, currentPolicy, pending, evaluation, decision, applied, bypass >>

AdvanceChannel(newChannel) ==
    /\ applied.status = AppliedNone
    /\ newChannel \in ChannelVersions
    /\ newChannel # currentChannel
    /\ currentChannel' = newChannel
    /\ evaluation' = IF evaluation.status = EvalReady
                      THEN [evaluation EXCEPT !.status = EvalStale]
                      ELSE evaluation
    /\ decision' = IF decision.status \in {DecisionAccepted, DecisionRisk, DecisionBlocked}
                    THEN [decision EXCEPT !.status = DecisionStale]
                    ELSE decision
    /\ UNCHANGED << currentPolicy, pending, applied, receipt, bypass >>

AdvanceChannelAction ==
    \E newChannel \in ChannelVersions: AdvanceChannel(newChannel)

ChangePolicy(newPolicy) ==
    /\ applied.status = AppliedNone
    /\ newPolicy \in Policies
    /\ newPolicy # currentPolicy
    /\ currentPolicy' = newPolicy
    /\ evaluation' = IF evaluation.status = EvalReady
                      THEN [evaluation EXCEPT !.status = EvalStale]
                      ELSE evaluation
    /\ decision' = IF decision.status \in {DecisionAccepted, DecisionRisk, DecisionBlocked}
                    THEN [decision EXCEPT !.status = DecisionStale]
                    ELSE decision
    /\ UNCHANGED << currentChannel, pending, applied, receipt, bypass >>

Next ==
    \/ ReceiveChangeSet
    \/ Evaluate
    \/ AuthorizePass
    \/ AuthorizeRisk
    \/ Block
    \/ ApplyAccepted
    \/ DirectApply
    \/ PostReceiveReceipt
    \/ ReceiptFailure
    \/ AdvanceChannelAction
    \/ \E newPolicy \in Policies: ChangePolicy(newPolicy)

Spec == Init /\ [][Next]_vars

TypeOK ==
    /\ currentChannel \in ChannelVersions
    /\ currentPolicy \in Policies
    /\ pending.status \in {PendingNone, PendingReady}
    /\ pending.changeSet \in ChangeSets \cup {NoValue}
    /\ pending.candidate \in ChannelVersions \cup {NoValue}
    /\ pending.base \in ChannelVersions \cup {NoValue}
    /\ evaluation.status \in {EvalNone, EvalReady, EvalStale}
    /\ evaluation.changeSet \in ChangeSets \cup {NoValue}
    /\ evaluation.candidate \in ChannelVersions \cup {NoValue}
    /\ evaluation.base \in ChannelVersions \cup {NoValue}
    /\ evaluation.policy \in Policies \cup {NoValue}
    /\ evaluation.result \in Results \cup {NoValue}
    /\ evaluation.trusted \in BOOLEAN
    /\ decision.status \in {DecisionNone, DecisionAccepted, DecisionRisk, DecisionBlocked, DecisionStale}
    /\ decision.changeSet \in ChangeSets \cup {NoValue}
    /\ decision.candidate \in ChannelVersions \cup {NoValue}
    /\ decision.base \in ChannelVersions \cup {NoValue}
    /\ decision.policy \in Policies \cup {NoValue}
    /\ decision.result \in Results \cup {NoValue}
    /\ decision.authority \in {RootAuthority, NoValue}
    /\ applied.status \in {AppliedNone, Applied}
    /\ applied.changeSet \in ChangeSets \cup {NoValue}
    /\ applied.candidate \in ChannelVersions \cup {NoValue}
    /\ applied.base \in ChannelVersions \cup {NoValue}
    /\ applied.kind \in {"verified", "accepted-with-risk", "uncontrolled", NoValue}
    /\ receipt.status \in {ReceiptNone, ReceiptCommitted, ReceiptFailed}
    /\ receipt.changeSet \in ChangeSets \cup {NoValue}
    /\ receipt.candidate \in ChannelVersions \cup {NoValue}
    /\ receipt.base \in ChannelVersions \cup {NoValue}
    /\ receipt.outcome \in {"verified", "accepted-with-risk", "uncontrolled", "receipt-unavailable", NoValue}
    /\ bypass.status \in {BypassNone, BypassRecorded}
    /\ bypass.changeSet \in ChangeSets \cup {NoValue}
    /\ bypass.actor \in BypassActors \cup {NoValue}
    /\ bypass.reason \in {"no-enforcement-boundary", "administrator-bypass", NoValue}

NoFalseAcceptedDecision ==
    decision.status = DecisionAccepted =>
        /\ evaluation.status = EvalReady
        /\ evaluation.result = Pass
        /\ evaluation.trusted = TRUE
        /\ decision.changeSet = evaluation.changeSet
        /\ decision.candidate = evaluation.candidate
        /\ decision.base = evaluation.base
        /\ decision.policy = evaluation.policy
        /\ (applied.status = Applied => applied.base = decision.base)
        /\ (applied.status = AppliedNone => decision.base = currentChannel)

RiskDoesNotRewriteResult ==
    decision.status = DecisionRisk =>
        /\ evaluation.result \in {Fail, Unknown, Conflict}
        /\ decision.result = evaluation.result
        /\ decision.authority = RootAuthority

AppliedRequiresExactDecision ==
    applied.status = Applied =>
        IF applied.kind = "verified"
        THEN
            /\ decision.status = DecisionAccepted
            /\ applied.changeSet = decision.changeSet
            /\ applied.candidate = decision.candidate
            /\ applied.base = decision.base
            /\ decision.policy = currentPolicy
        ELSE IF applied.kind = "accepted-with-risk"
        THEN
            /\ decision.status = DecisionRisk
            /\ applied.changeSet = decision.changeSet
            /\ applied.candidate = decision.candidate
            /\ applied.base = decision.base
        ELSE
            /\ applied.kind = "uncontrolled"
            /\ BoundaryMode # Enforced
            /\ bypass.status = BypassRecorded
            /\ bypass.changeSet = applied.changeSet

NoSilentBypass ==
    applied.kind = "uncontrolled" =>
        /\ bypass.status = BypassRecorded
        /\ bypass.changeSet = applied.changeSet
        /\ bypass.actor \in BypassActors

NoUncontrolledInEnforcedMode ==
    BoundaryMode = Enforced => applied.kind # "uncontrolled"

ReceiptBound ==
    receipt.status = ReceiptCommitted =>
        /\ applied.status = Applied
        /\ receipt.changeSet = applied.changeSet
        /\ receipt.candidate = applied.candidate
        /\ receipt.base = applied.base
        /\ receipt.outcome = applied.kind

PostReceiveCannotUndo ==
    receipt.status = ReceiptFailed =>
        /\ applied.status = Applied
        /\ currentChannel = applied.candidate
        /\ receipt.outcome = "receipt-unavailable"

====
