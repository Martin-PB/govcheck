# Decision and assumed risk as cross-cutting governance dimensions

**Status:** research clarification for issues [#73](https://github.com/Martin-PB/govcheck/issues/73) and [#131](https://github.com/Martin-PB/govcheck/issues/131); not an adopted metamodel or architecture decision. **Date:** 2026-11-13.

## 1. Correction: the traceability path is not a lifecycle chain ending in a decision

The sequence

`Intention → Requirement → Property → Model → Implementation → Conformance Verification → Assurance`

may be useful as one traceability path. It is not a universal, strictly linear lifecycle and must not terminate in `Decision`.

GovCheck's semantic structure is a typed, many-to-many, evolving graph. Its nodes and relations can be created, revised, disputed, invalidated, superseded or left unresolved. Inputs to requirements and decisions may originate in law, standards, contracts, stakeholder needs, architecture constraints, operational observations, defects, incidents, threats, interoperability obligations and other sources—not only in an initial intention.

A decision is a first-class transversal governance object. It may act at any point in the graph: establish or revise an intention; select, refine or reject requirements; choose properties or models; authorize, constrain or reject implementation; accept or reject verification results; accept, qualify or refuse an assurance argument; authorize publication or deployment; suspend, revoke or trigger reassessment. Decisions may also govern relations between artifacts, not only artifacts themselves.

The graph must therefore represent decision context, authority, scope, rationale, alternatives, conditions, consequences, effective time, applicable governance revision, provenance and review/revocation conditions. A decision is not synonymous with approval or success: it may record disagreement, unresolved contradiction, deferral, rejection, conditional acceptance or explicit risk acceptance.

## 2. Assurance is not a decision, and a decision is not proof

Keep distinct:

- **Evidence/assurance:** what is supported, by which method, against which claim, under which assumptions and limitations.
- **Decision:** what an authorized actor chooses or commits to do in a declared context.
- **Authority:** why that actor is entitled to make that decision, for that scope and time.
- **Risk acceptance:** an authorized commitment concerning exposure and consequences that remain; it does not erase the risk or strengthen the evidence.

A decision may rely on strong assurance and still accept residual risk. It may also proceed with incomplete assurance, but the missing evidence, assumptions, dissent, uncertainty and accepted exposure must remain explicit. Authorization cannot turn a test into a theorem proof, a model-checking result into implementation conformance, or an unsupported assumption into knowledge.

A decision can change the object being assured. Such a change may invalidate models, evidence, mappings, approvals or prior decisions; those dependencies and re-evaluation obligations must be explicit and temporally scoped.

## 3. Risk and assumed risk are first-class objects

Do not represent risk as a boolean field such as `accepted_risk: true`, a free-text note alone, or a universal numeric score. At minimum, distinguish:

1. A risk scenario or uncertain adverse outcome.
2. Consequences and affected objectives/assets/stakeholders.
3. Observations, experience, evidence and source provenance.
4. Assumptions, unknowns, disagreements and model limitations.
5. Risk analysis/evaluation method and its applicability.
6. Quantitative or qualitative estimates, including their semantics and uncertainty.
7. Treatment options, controls, mitigations and residual exposure.
8. A decision that accepts, rejects, transfers, tolerates, mitigates or defers the exposure.
9. The authority, scope, rationale, conditions, validity period, review triggers and revocation/expiry rules for that decision.

The risk object and its evaluation must be independently identifiable and versioned. A decision references the exact risk assessment revision it considered. Reassessment may produce a new evaluation without rewriting the historical basis of an earlier decision.

PEAK means **Problem, Experience, Assumptions, Knowledge**. These four inputs feed a decision process with two distinct outputs: the **solution** and the **assumed risk** (what may not work as envisioned). The assumed risk is not an afterthought or merely the risk remaining after controls; it is part of the decision record from the outset. The four inputs and two outputs must remain separately inspectable:

| PEAK element | Role in the decision record |
|---|---|
| Problem | The problem to resolve, including requirements and constraints |
| Experience | Relevant prior experience and its applicability |
| Assumptions | What is taken as true without sufficient evidence, and what is deliberately excluded from consideration |
| Knowledge | Facts and contextual knowledge actually available at decision time |
| Solution | The chosen response/approach |
| Assumed Risk | What may not work as envisioned, including what the decision-maker is knowingly exposing the project to |

Do not conflate three different concepts: **PEAK assumed risk** (the explicit second output of the decision process), **risk assessment** (a separate analysis that may estimate likelihoods, consequences and uncertainty), and **risk acceptance** (an authorized disposition concerning exposure). **Residual risk** is yet another concept: exposure remaining after specified treatments or controls. A PEAK assumed risk may be unquantified, may not yet have been mitigated, and may later be evaluated or treated. The decision record should preserve the original assumed risk even when later assessments or controls change. PEAK can therefore help structure problem framing, experience, assumptions and knowledge, while requiring the decision-maker to state both what is chosen and what may fail. It must not be merged artificially with SACM, threat modelling or the GovCheck metamodel as a whole. PEAK contributes a decision/risk reasoning perspective; SACM contributes an assurance-case perspective; neither alone supplies governance authority.

## 4. Preserve mathematical and epistemic distinctions

The metamodel must not collapse the following:

- **Classical/formal truth or satisfaction:** relative to a declared language, semantics, model and assumptions.
- **Probability:** uncertainty over events, outcomes or parameters, with an explicitly stated interpretation.
- **Fuzzy membership:** degree to which an object belongs to a vague concept; a membership degree of 0.8 is not an 80% probability.
- **Nondeterminism:** a set of possible transitions or choices without an implied probability distribution.
- **Transition rate:** a time-dependent rate, not a probability for an unspecified interval.
- **Cost, reward/utility, priority, preference and empirical frequency:** typed quantities with different meanings and units.
- **Confidence in an argument:** an epistemic/assessment judgement whose semantics and method must be declared; it is not automatically a probability or proof strength.
- **Unknown or non-quantifiable:** absence of justified knowledge; never silently coerce it to zero, a midpoint, a pass or a score.

For probabilistic evaluations, preserve the event, conditioning assumptions, population, time horizon, data and parameter provenance, estimation method, dependencies, distribution/interval, sensitivity and validity. For fuzzy evaluations, preserve the linguistic concept, membership function, rule base, expert judgements and validation. For either, preserve what the method does not establish.

A formula such as probability × impact may be useful under a particular risk method and scale, but it is not a universal definition of risk. Aggregation across unlike units, scenarios, uncertainties or value judgements requires an explicit, justified decision model; GovCheck must not invent one.

## 5. Consequences for the semantic graph and formal contracts

Candidate relations include:

- `informsDecision`, `justifiesDecision`, `authorizesDecision`, `constrainsDecision`, `supersedesDecision`, `revokesDecision`;
- `identifiesRisk`, `evaluatesRisk`, `treatsRisk`, `acceptsRisk`, `reassessesRisk`;
- `supports`, `challenges`, `assumes`, `dependsOn`, `invalidates`, `isApplicableUnder`.

These names are illustrative, not an adopted vocabulary. Each relation needs a typed signature, direction, semantics, cardinality, provenance, authority requirements, scope and temporal validity. The graph may contain cycles where justified; no blanket acyclicity constraint is implied.

## 5.1 Candidate typed object boundaries

The following separation is a candidate modelling contract, not a selected serialization or final class hierarchy:

| Candidate object | Responsibility | Must not be conflated with |
|---|---|---|
| `DecisionRecord` | Identity/revision, decision kind/status, context, authority, scope, rationale, alternatives, conditions, effective/expiry positions, provenance and supersession/revocation | A PR approval, CI result or unqualified boolean |
| `DecisionInputs` | PEAK Problem, Experience, Assumptions and Knowledge, each with source and time/context | One undifferentiated confidence score |
| `DecisionSolution` | Chosen response and its selected alternatives/constraints | Evidence that the solution works |
| `AssumedRisk` | PEAK's explicit statement of what may not work as envisioned | A quantified probability, residual risk or formal risk acceptance |
| `RiskScenario` | Uncertain adverse event/state, causal/contextual description and consequences | The estimate of its likelihood |
| `RiskAssessment` | Method-specific analysis of a scenario, with model, assumptions, data, parameters, horizon, results and limitations | The scenario itself or the authority to accept it |
| `RiskTreatment` | Avoidance, reduction, transfer/sharing, monitoring, contingency and resulting residual exposure | A decision record unless it carries the required authority and rationale |
| `RiskAcceptance` | Authorized, scoped and time-bounded disposition of a specified exposure, tied to exact assessment and policy revisions | Proof that the risk is absent or acceptable in every context |

A decision record may reference zero or more assumptions, knowledge items, alternatives, solutions and assumed-risk statements. One assumed-risk statement may concern multiple scenarios; one scenario may be assessed by several methods or under several contexts. These cardinalities must be justified by use cases rather than fixed prematurely.

The key identity chain is not a single linear pipeline. It is a set of typed references:

- decision → exact inputs and source revisions;
- decision → selected solution and explicit assumed-risk outputs;
- risk scenario → one or more assessments;
- assessment → exact model, data, parameters, assumptions and method/tool revision;
- treatment → scenario and assessment revisions it addresses;
- acceptance → exact residual exposure, authority, policy revision, scope and validity interval;
- later observation/reassessment → the prior decision/assessment it challenges or triggers for review.

A PEAK assumed-risk output can exist before quantitative analysis. A later probabilistic or fuzzy assessment enriches the record but must not overwrite what was originally assumed. A risk acceptance may refer to a residual exposure after treatment; it is a separate authorized act.

### Negative examples that the model must reject

- Treating fuzzy membership 0.8 as an 80% event probability.
- Treating a missing probability estimate as probability zero.
- Treating a transition rate as a probability without a time interval and conversion semantics.
- Treating an unweighted nondeterministic transition as equiprobable.
- Treating an expert confidence score as a theorem proof or calibrated probability without a justified interpretation.
- Treating a recorded PEAK assumed risk as if it had already been assessed or formally accepted.
- Treating risk acceptance as evidence that the scenario cannot occur.
- Reusing an expired/revoked acceptance after its scope, policy, assessment or assumptions have changed.

Formal obligations should include, where applicable:

- a decision cannot acquire authority, scope or duration from a semantic mapping;
- risk acceptance cannot imply that the risk is absent, the scenario impossible or the estimate proven;
- probability, fuzzy membership, nondeterminism, rates, costs and confidence cannot be interchanged by an untyped conversion;
- an assessment or decision is bound to exact revisions of its model, parameters, evidence, assumptions and governing policy;
- changes to those dependencies invalidate or trigger review of affected evaluations and decisions according to declared rules;
- a decision's historical rationale and accepted exposure remain inspectable after supersession, expiry or revocation.

These are candidate proof/validation obligations to refine in #73 and #131, not claims that current GovCheck code already enforces them.

## 6. Existing research and references

This addendum refines rather than replaces [Research: semantic assurance and transition models](semantic-assurance-and-transition-models-2026-11.md). In particular, preserve the distinction already documented there between probability, fuzzy membership, nondeterminism, transition rates, costs and rewards. See catalogue [R-193](../references.md#r-193) for probabilistic, fuzzy and transition-model sources, and [R-74](../references.md#r-74) for the PEAK decision-model source.

## 7. Status and boundaries

This document is a research clarification. It does not adopt a canonical serialization, universal risk calculus, probability/fuzzy engine, PEAK, SACM, a specific decision model or a normative GovCheck metamodel. It does not change the current authority regime. Proposals must be specified, checked against source semantics and submitted through the repository's governance process before normative adoption.
