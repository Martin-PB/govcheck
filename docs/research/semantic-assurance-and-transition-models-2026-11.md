# Research discussion: semantic assurance and quantitative transition models

**Status:** research record, not an adopted architecture decision. **Date:** 2026-11-10.

## Purpose

This record consolidates the discussion on GovCheck's semantic foundations and the place of epistemic, probabilistic, fuzzy and state-transition approaches in assurance. GovCheck is a general-purpose repository-governance system, not a security-only framework. No single standard, logic, proof assistant or model checker should define its whole ontology.

## 1. Semantic relationships

The model must relate, without collapsing, intentions, goals, stakeholder needs, requirements, decisions, specifications, properties, architecture, models, implementations and assurance. These form a typed, many-to-many, evolving graph rather than a linear document hierarchy. A decision may address several requirements; a property may refine several goals; evidence may support several claims; a change may invalidate downstream reasoning or evidence. Relations need type, direction, rationale, authority, scope and temporal applicability.

Intent is not the sole source of requirements: law, standards, contracts, stakeholder needs, operational observations, threats, defects, interfaces and interoperability constraints can also generate them. A goal is not itself an observable outcome, and a measurement is not automatically evidence of goal achievement.

## 2. External landscape examined

Candidate foundations include:

- **Lifecycle and requirements:** ISO/IEC/IEEE 15288, 12207, 29148 and 15289.
- **Architecture and systems modelling:** ISO/IEC/IEEE 42010, SysML v2/KerML.
- **Goal-oriented requirements:** KAOS, i*, GRL and Tropos.
- **Decision/process modelling:** OMG DMN and BPMN.
- **Assurance cases:** SACM (engineering target discussed: 2.4 Beta 1), GSN, ISO/IEC/IEEE 15026-2 and Assurance 2.0 research.
- **Provenance and exchange:** W3C PROV-DM/PROV-O, ReqIF, in-toto, SLSA, SPDX and CycloneDX.
- **Risk, security and AI governance:** NIST SP 800-160 Rev. 1, ISO/IEC 23894, ISO/IEC 42001 and NIST AI RMF.
- **Quality and measurement:** ISO/IEC 25010 and Goal-Question-Metric (GQM).
- **Decision/risk reasoning:** PEAK, which must not be conflated with SACM.

These sources are complementary, not interchangeable. SACM is an important assurance/interoperability profile, not GovCheck's complete ontology. Full semantic preservation and lossless interchange are important goals when importing/exporting SACM.

Further research gaps: organizational authority and delegation; deontic logic (obligation, permission, prohibition); decision theory and multi-criteria arbitration; sociotechnical factors; AI/agent assurance; temporal validity, freshness and invalidation.

## 3. Epistemic status and justification

The earlier generic “uncertainty” grouping was judged inadequate. The preferred working concept is **epistemic status and justification** (or “knowledge and justification”). GovCheck should express what is asserted, why it is accepted, what supports or contradicts it, how supporting material was produced, what conclusion is licensed, and the scope, freshness and limitations.

Recovered vocabulary from earlier GovCheck work includes Claim/Assertion, Hypothesis, Argument, ArgumentReasoning, AssertedInference, AssertedEvidence, Context, Observation, Indicator, Evaluation, Incident and Decision. Related metadata may include evidence strength, confidence, provenance, temporal scope, counterarguments/defeaters, undecidability, unknowns, limitations, assumptions and residual accepted risk.

Tests, model checking and proofs are different:

- A **test result** is testimony/evidence about an execution under specified conditions, not a theorem proof.
- **Model checking** analyses a formal model against properties and may produce satisfaction evidence or a counterexample. Conclusions are bounded by the model, semantics, configuration and explored state space.
- A **formal proof** is a derivation checked within a formal system and its assumptions; it does not automatically prove that the formalization matches reality.
- Reviews/inspections and production observations produce other evidence types, each with its own method and limitations.

These are methods and result types linked to claims and arguments, not subtypes of uncertainty. An illustrative path such as Observation → Hypothesis → Threat → Control → Evidence → Assertion → Argument → Decision → Accepted Risk is one possible pattern, not a mandatory workflow.

Candidate cross-cutting concerns, subject to overlap review: epistemic status/justification; authority/responsibility; provenance/traceability; context/applicability; time/freshness; risk/uncertainty; method/compliance; evolution/invalidation; observation/measurement.

## 4. Probability and fuzzy logic

**Probability** represents uncertainty about events, outcomes or parameters. Bayesian methods combine prior information with observations, but prior assumptions, likelihood models and dependencies matter. Potential uses include reliability, failure probability, risk estimation, operational evidence and sensitivity analysis. Any probability attached to a claim should identify the event, conditioning assumptions, population, time horizon, data/parameter sources, estimation method, dependence assumptions and uncertainty of the estimate.

**Fuzzy logic** represents graded membership in concepts with imprecise boundaries (for example, “low/medium/high” maintainability) and can help with vague or conflicting requirements. A membership degree of 0.8 in “high maintainability” is **not** an 80% probability that the product is maintainable. Membership functions, rule bases and expert judgments need justification and validation.

Keep separate: classical/formal truth and derivation; probability over events/parameters; fuzzy membership and linguistic vagueness; qualitative assurance arguments. They may coexist, but combination/aggregation rules must be explicit. Do not introduce a universal numeric confidence field or unexplained global score.

Provisional recommendation: a generic core for claims, assumptions, arguments, evidence, methods, results, limitations and conclusions, with optional specialist profiles/engines for formal, probabilistic, fuzzy and qualitative methods. The core can represent specialist results and assumptions; specialist evaluation may be delegated. Whether GovCheck itself should validate probabilistic/fuzzy assumptions remains open.

### Sources on probability, fuzzy logic and assurance confidence

- Graydon & Holloway, “An investigation of proposed techniques for quantifying confidence in assurance arguments,” *Safety Science* 92 (2017): https://doi.org/10.1016/j.ssci.2016.09.014. Reviews quantitative confidence techniques and cautions about implausible results and insufficient empirical validation for general critical-decision use.
- “A probabilistic model of belief in safety cases,” *Safety Science* 138 (2021), 105187: https://doi.org/10.1016/j.ssci.2021.105187. Illustrates a Bayesian-network approach, not universal suitability.
- NIST Engineering Statistics Handbook, Bayesian reliability evaluation: https://www.itl.nist.gov/div898/handbook/apr/section1/apr1a.htm.
- Johanyák & Zlatko (2025), “A comprehensive survey on Fuzzy logic applications in software requirements engineering”: https://doi.org/10.47833/2025.2.CSC.008.
- Yen, Tiao & Liu (1996), “A Systematic Tradeoff Methodology for Acquiring and Validating Imprecise Requirements”: https://doi.org/10.1109/FUZZY.1996.551766.
- Salako & Zhao (2023), “The Unnecessity of Assuming Statistically Independent Tests in Bayesian Software Reliability Assessments”: https://doi.org/10.1109/TSE.2022.3233802.
- Salako & Zhao (2024), “Demonstrating Software Reliability using Possibly Correlated Tests”: https://doi.org/10.1002/qre.3460.
- NIST, “Software Assurance Using Structured Assurance Case Models”: https://pmc.ncbi.nlm.nih.gov/articles/PMC4548534/.

## 5. Finite-state machines, weighted transitions and Markov models

These model families are relevant, but transition-weight semantics must be explicit.

- **Finite-state machine / transition system:** defines possible states and permitted transitions; it may be deterministic or nondeterministic and need not be probabilistic.
- **Discrete-time Markov chain (DTMC):** the next-state distribution depends on the current state; outgoing probabilities form a distribution.
- **Continuous-time Markov chain (CTMC):** transitions have rates, not direct probabilities for a fixed step; time semantics and units matter.
- **Markov decision process (MDP):** combines action/nondeterministic choices with probabilistic transitions, supporting strategy analysis.
- **Probabilistic timed automata / hybrid models:** add clocks, timing constraints or continuous variables.

The Markov property is an assumption: the current state must contain sufficient information to determine the conditional distribution of the next state. If history matters, encode relevant history in the state or choose another model family.

A numeric edge weight is not necessarily a probability. It may be a probability, transition rate, cost, reward/utility, priority/preference or empirical frequency/estimated parameter. These meanings are not interchangeable. A transition rate is not a probability; a cost must not be normalized as one without an explicit model.

Potential uses: reliability over a time horizon; reachability/probability of compromised states; CI/CD transitions among proposed, checked, rejected, deployed and rolled-back; maintenance states; agent governance trajectories; probability of adverse events before detection/mitigation. Governance/authorization models should first express permitted transitions and authorities. Add probability only where stochastic behaviour, empirical frequencies, time or quantitative risk warrants it.

Distinguish (1) stochasticity represented in the model, (2) epistemic uncertainty about probabilities/rates, and (3) linguistic imprecision about qualitative risk. Interval probabilities and interval MDPs can express parameter uncertainty and bound outcomes; they are not fuzzy membership grades.

A model checker can establish a quantitative result for the supplied model and parameters, not that the model faithfully represents reality. Quantitative assurance therefore needs data and parameter provenance, model rationale, assumptions, horizon, dependencies, sensitivity and limitations. The result is evidence in an assurance argument, not an automatic real-world guarantee.

### Candidate generic contract

A common transition-model contract could describe:

- `TransitionSystem`: states, initial-state definition, transitions and invariants;
- `TransitionSemantics`: deterministic, nondeterministic, probabilistic, timed or hybrid;
- `TransitionWeight`: typed value, unit, domain, constraints and interpretation;
- `ParameterJustification`: provenance, observations, assumptions, estimation method and validity interval;
- `AnalysisSpecification`: property/objective, horizon, scheduler/adversary assumptions and analysis semantics;
- `AnalysisResult`: result, tool/version, configuration, explored bounds, witness/counterexample, limitations and reproducibility data;
- assurance links from results to claims, arguments, decisions and residual risks.

This is conceptual, not an adopted schema. Do not force automata, Petri nets, Markov chains and other formalisms into one representation. Prefer a common contract for semantics, parameters, analysis and result provenance, with domain-specific profiles and native formats.

### Sources on transition systems and probabilistic model checking

- Baier & Katoen, *Principles of Model Checking*, MIT Press (2008): https://is.ifmo.ru/books/_principles_of_model_checking.pdf.
- PRISM official manual: https://www.prismmodelchecker.org/manual/Main/Introduction; tutorials: https://www.prismmodelchecker.org/tutorial/; case studies: https://www.prismmodelchecker.org/casestudies/.
- UPPAAL semantics documentation: https://docs.uppaal.org/language-reference/system-description/semantics/.

PRISM and UPPAAL are candidate analysis tools/reference implementations, not GovCheck dependencies or normative authorities.

## 6. Provisional guidance and open questions

Working guidance, not yet an ADR:

1. Use a typed semantic graph with explicit many-to-many and temporal relationships.
2. Keep the core independent of a single standard, logic, model checker or proof assistant.
3. Represent testimony, evidence, formal proof, model-checking results, observations and expert judgments as distinct types with method and scope.
4. Keep probability, fuzzy membership, nondeterminism, transition rates, costs and rewards semantically distinct.
5. Allow specialist profiles/tools without making formal proof, probabilistic analysis or fuzzy logic mandatory.
6. Preserve assumptions, unknowns, counterevidence, limitations and accepted risks rather than hiding them behind one score.
7. Treat standards/tool formats as domain profiles, not the entire GovCheck metamodel.
8. Trace computed conclusions to model, parameters, data, method, tool version and validity scope.

Open questions: smallest coherent core ontology; formal typing of relations among intent/goals/needs/requirements/decisions/specifications/properties/models/implementations/assurance; whether the core only represents or also validates probabilistic/fuzzy assumptions; which transition semantics need first-class support versus extension profiles; how to distinguish stochasticity, parameter/model uncertainty and fuzzy imprecision; how to compare results with different abstractions, horizons, assumptions and units; which transversal dimensions are orthogonal.

## 7. Decision status

This record does not adopt a particular logic, standard, model checker, proof assistant, serialization or quantitative confidence method. It preserves the discussion for the next academic/industry research and metamodel-design pass.


Catalogue de références : [R-193](../references.md#r-193).
