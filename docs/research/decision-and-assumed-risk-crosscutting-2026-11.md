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

## 5.2 Candidate typed quantitative and uncertainty values

These are semantic boundaries for later modelling, not a mandatory numeric engine or a selected risk calculus.

| Type family | Meaning that must be retained | Required context |
|---|---|---|
| `ProbabilityEstimate` | Measure/estimate concerning a specified event or outcome under stated conditions | Event, conditioning assumptions, population/system boundary, time horizon, interpretation (frequentist/Bayesian/elicited/model-derived), method, data/model/parameter revisions, result form, dependencies, sensitivity and validity |
| `ProbabilityPoint` / `ProbabilityInterval` | Point estimate or bounded estimate in [0,1] | Calibration/derivation, lower/upper bounds and whether bounds are epistemic, statistical or decision-based |
| `ProbabilityDistribution` | Distribution over a declared outcome space | Outcome space, sigma-algebra/finite partition, measure/model identity, dependencies and parameter revision |
| `FuzzyMembership` | Degree to which an object belongs to a vague concept | Concept, universe/domain, membership-function identity/revision, linguistic terms, rule base, expert basis and validation |
| `NondeterministicPossibility` | A set of possible states/outcomes or a transition relation, without weights | State space, transition relation, guards and assumptions |
| `TransitionRate` | Rate per declared unit of time for a transition/process | Source/target state, unit, process semantics, model and parameter revision |
| `ArgumentConfidence` | Method-dependent assessment of confidence in an argument or assurance case | Argument revision, assessment method, criteria, assessor, calibration and limitations |
| `Cost`, `Utility`, `Priority`, `Frequency` | Quantities with their own units and semantics | Unit, scale, population/period where applicable, method and provenance |

A numeric value in [0,1] is not self-describing. In particular, `ProbabilityPoint(0.8)` and `FuzzyMembership(0.8)` are different types with different interpretations. The model must not provide an implicit coercion between them. Any explicit cross-domain mapping must name its source/target semantics, assumptions, validation and limitations.

A transition rate cannot be read as a probability until the process model and time interval are specified. An unweighted nondeterministic choice does not imply equiprobability. A confidence judgement about an assurance argument is not automatically a calibrated probability, theorem proof or model-checking result.

### Explicit epistemic availability

A result should distinguish at least:

- `NotAssessed`: no assessment was performed;
- `Unknown(reason)`: an assessment or inquiry exists but the value is unresolved;
- `NotQuantifiable(reason)`: a numeric quantity is not justified or meaningful for this question;
- `NotApplicable(reason)`: the assessment dimension does not apply;
- `Quantified(value)`: a result exists with its type, method and provenance;
- `Inconclusive(reason)`: an assessment ran but did not resolve the stated decision criterion.

These states are not interchangeable. In particular, `Unknown`, `NotAssessed` and `NotQuantifiable` are never converted to zero, a midpoint, a pass or a score by default. A probability of zero is a positive mathematical claim about a specified event/model, not the absence of an estimate.

### Decision/risk separation

- `AssumedRisk` is a PEAK decision output and may exist without any `RiskScenario` decomposition or quantitative `RiskAssessment`.
- `RiskScenario` identifies a possible adverse event/state, its context, causes and consequences.
- `RiskAssessment` evaluates a scenario under a declared technique and binds exact model, data, parameter, assumption, tool and policy revisions.
- `RiskTreatment` records chosen treatment actions and the exposure they address.
- `RiskAcceptance` is a separate authorized decision, bound to a specified residual exposure, authority, scope, policy/assessment revisions and validity interval.

No assessment result automatically creates acceptance authority. No acceptance implies that a scenario is impossible, that an estimate is proven, or that the exposure is acceptable outside the recorded scope and validity interval.

### Candidate proof/validation obligations

1. Distinct value families have no implicit conversion path.
2. A probability result is bound to an event/outcome, conditioning context and time horizon.
3. A fuzzy grade is bound to a concept and membership-function revision.
4. A nondeterministic transition carries no probability unless a separate distribution is supplied.
5. A rate carries a unit and process/time semantics.
6. Unknown, not assessed, not quantifiable, not applicable and inconclusive remain distinct.
7. A PEAK assumed-risk output can exist before assessment and is not overwritten by later estimates.
8. Risk acceptance requires a separate authority-bearing decision and cannot imply absence or impossibility of the risk.

These obligations should be refined into Lean types and negative fixtures in #131. The first implementation should use explicit typed wrappers and small proof obligations; it should not introduce a universal score or force all projects to quantify risk.

## 6. Existing research and references

This addendum refines rather than replaces [Research: semantic assurance and transition models](semantic-assurance-and-transition-models-2026-11.md). In particular, preserve the distinction already documented there between probability, fuzzy membership, nondeterminism, transition rates, costs and rewards. See catalogue [R-193](../references.md#r-193) for probabilistic, fuzzy and transition-model sources, and [R-74](../references.md#r-74) for the PEAK decision-model source. See [R-202](../references.md#r-202) for risk-management and risk-assessment process guidance.

## 7. Status and boundaries

This document is a research clarification. It does not adopt a canonical serialization, universal risk calculus, probability/fuzzy engine, PEAK, SACM, a specific decision model or a normative GovCheck metamodel. It does not change the current authority regime. Proposals must be specified, checked against source semantics and submitted through the repository's governance process before normative adoption.
