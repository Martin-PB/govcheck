# 0025 — Runtime observations, PEAK decision traceability and SACM assessment

**Status:** research and architecture recommendation for review; no runtime observation pipeline, PEAK decision engine, SACM serializer or production threat-model updater is implemented by this record.  
**Language:** English is the default; see the [French counterpart](0025-runtime-observations-peak-and-sacm.fr.md).

## 1. Executive conclusion

GovCheck should connect production observations, threat-model evolution, assurance arguments and governed risk decisions through a shared, typed semantic model. PEAK and SACM are complementary inputs, not competing ontologies:

- **PEAK** is a decision-analysis lens: Problem, Experience, Assumptions and Knowledge are examined as inputs to a decision process; the process yields a solution and an assumed risk [R-74](../references.md#r-74).
- **SACM** is a structured assurance-case metamodel for claims, argumentation, evidence references, artifacts and terminology [R-34](../references.md#r-34).
- **GovCheck** must retain the domain semantics neither provides as a complete package: threats, attack paths, controls, operational observations, evidence freshness, risk treatment, authority and acceptance decisions.

**Recommendation:** adopt neither PEAK nor SACM as GovCheck's canonical governance ontology. Use PEAK as a projection/view over governed decision records. Use SACM as a candidate interchange and assurance-case representation, with a GovCheck profile/extension and a loss-aware mapping. Preserve SACM 2.3 as the current formal compatibility baseline while evaluating 2.4 Beta 1; do not freeze the internal model to the beta.

An observation can change what we know about a system and challenge an assumption; it does not, by itself, prove an attack, establish a threat scenario, determine risk acceptability or authorize a mitigation.

## 2. Existing GovCheck foundations

This proposal should extend, not duplicate, existing concepts:

- Architecture 0013 already distinguishes goals, requirements, norms, properties, contracts, models, implementation artifacts, methods, witnesses/evidence, claims, arguments and decisions/authority. It requires typed relations rather than inference from document proximity.
- Specification 0005 and the proposed evidence record already separate an evidence record from the claim it may support/refute, the argument that interprets it, and the acceptance decision. An evidence record binds an observation, execution or derivation to exact subjects, method, context, provenance, limitations and invalidation dependencies.
- Architecture 0021 defines claims, arguments, evidence, assumptions, dependencies and decisions; it distinguishes evidence outcome from admissibility, freshness and authenticity. It requires immutable historical evidence and new observations for revalidation.
- Architecture 0017 distinguishes an evidence item/observation as an immutable instance/event, not a SemVer-versioned logical artifact.
- Architecture 0006 supplies the threat and trust foundations; Architecture 0024 introduces threat-led assurance and risk treatment.

These foundations already provide much of the required semantic substrate. The important missing connection is a first-class operational observation lifecycle and an explicit decision-input/decision-output projection.

## 3. PEAK: decision traceability, not another assurance ontology

The PEAK decision model in Hoover, Rosso-Llopart and Taran identifies four input dimensions:

| PEAK element | Meaning | GovCheck projection |
|---|---|---|
| **P — Problem** | The issue to be resolved, with requirements and constraints | Decision question, affected system/asset, stakeholder concerns, scope, objectives and constraints |
| **E — Experience** | Skills and experience brought to the decision | Relevant prior incidents, operational history, lessons learned, expertise and their provenance/context |
| **A — Assumptions** | Premises accepted for the decision | Explicit assumption records, with owner, scope, rationale, confidence, validity, monitorability and falsification/review conditions |
| **K — Knowledge** | Environment and facts available to decision-makers | Versioned architecture/configuration facts, standards, threat intelligence, observations and admissible evidence |

The process produces at least:
- **Solution:** the selected alternative, implementation/action plan, rejected alternatives and rationale.
- **Assumed risk:** the exposure and uncertainty accepted by selecting that alternative, including residual risk and any conditions.

PEAK does not prescribe a schema, authorization model, risk formula or threat vocabulary. It should therefore be represented as a **decision view** over native GovCheck objects, not by making P/E/A/K four new disconnected record silos.

### 3.1 Decision record requirements

A governed decision should bind:
- the problem statement, scope, affected subjects and constraints;
- alternatives considered, including do-nothing/defer where relevant;
- relevant experience and knowledge, with sources and dates;
- assumptions relied upon, including unresolved and disputed assumptions;
- expected benefits, costs, trade-offs, uncertainty and consequences;
- selected solution and implementation conditions;
- risk treatment and residual-risk statement;
- decision owner, authority basis, reviewers, rationale and decision time;
- scope, validity/expiry, review date and reassessment triggers;
- evidence and observations that later confirm, challenge or invalidate the decision.

The decision is an immutable event. A changed context, new evidence or changed authority creates a new assessment/decision or a superseding event; it does not rewrite the historical rationale. Risk acceptance is an explicit authorized disposition, not a claim that risk is absent or the system is safe.

### 3.2 PEAK and assurance are different questions

PEAK asks: **what inputs informed this decision, what solution was selected, and what risk was assumed?**

An assurance case asks: **what claim is being made, why should it be believed, what evidence and assumptions support it, and what could defeat it?**

A single decision can reference several assurance cases. An assurance case can inform multiple decisions. Keep the relation many-to-many and time/context-bound.

## 4. Production observations as feedback into threat and assurance models

NIST continuous-monitoring guidance explicitly connects ongoing visibility into assets, threats, vulnerabilities and deployed-control effectiveness with risk decisions [R-75](../references.md#r-75). Rushby's runtime-certification work goes further: assumptions used by an assurance argument can be made explicit and monitored during operation; observations can expose violated assumptions or anomalous behavior [R-76](../references.md#r-76). The ACCESS research demonstrates a SACM-based approach in which engineering artifacts and assurance cases co-evolve and assurance can be evaluated using runtime data [R-70](../references.md#r-70). Ericsson provides an industry example of runtime telemetry feeding evolving threat models and control analysis [R-72](../references.md#r-72).

GovCheck should support this feedback cycle:

1. **Observe:** collect a raw event/observation from a named sensor, monitor, operator or external source.
2. **Bind:** identify the exact system, deployment/configuration, component, time window and collection context.
3. **Assess observation quality:** establish source provenance, integrity, clock quality, coverage, collection health, completeness and uncertainty.
4. **Interpret:** correlate the observation with assets, trust boundaries, existing threats, attack paths, weaknesses, controls and assumptions.
5. **Form a hypothesis:** record a candidate indicator, anomaly, exposure change, threat scenario or control degradation. Preserve alternative explanations and counterevidence.
6. **Evaluate impact:** determine which assumptions, claims, controls, risk assessments and accepted-risk decisions may be challenged or invalidated.
7. **Decide:** an authorized actor chooses investigation, monitoring, mitigation, recovery, risk re-assessment or no action, with rationale.
8. **Validate response:** capture subsequent observations showing whether the action changed exposure or control effectiveness; preserve the before/after context.

The loop should be event-driven but not self-authorizing. Automated detection may propose a hypothesis or response. It must not silently amend the normative threat model, declare an incident confirmed, accept residual risk or apply a consequential control without the applicable authority and policy.

### 4.1 Do not collapse these semantic stages

| Stage | Meaning | Must not be confused with |
|---|---|---|
| Event | Something reported to have happened | A verified fact or attack |
| Observation | A source-bound record of what a collector/operator perceived | The interpretation of that data |
| Indicator/anomaly | A feature or deviation derived from observations | A confirmed threat |
| Hypothesis | A candidate explanation, such as a threat scenario or control failure | A proven causal explanation |
| Assessment | A reasoned evaluation of plausibility, impact, control effectiveness and uncertainty | A raw observation or authorized decision |
| Incident/confirmed finding | A conclusion reached under an explicit investigation/confirmation procedure | A model-generated suspicion |
| Decision | An authorized choice about treatment or operation | The assessment itself |

A missing alert is not evidence of absence unless sensor coverage, collection health, detection logic and the relevant time window are themselves established. A noisy or compromised sensor can produce misleading observations. A production observation can challenge a design assumption, but it may also reveal an unmodelled benign condition.

### 4.2 Observation record: minimum semantic envelope

The existing evidence record is suitable for observations used as evidence for claims, but it should not be overloaded as the sole raw telemetry/event schema. Consider two linked record types:

**Operational observation/event record**
- stable event/observation ID and schema version;
- source/sensor/collector identity, version, configuration and trust/provenance;
- event time, observed time, ingestion time, clock source/quality and ordering/correlation metadata;
- exact subject binding: logical asset, deployment instance, component, configuration revision and environment;
- observation type, collection method, scope, raw payload or immutable reference plus digest;
- integrity/authenticity status, completeness, coverage, known blind spots and collection-health evidence;
- uncertainty/confidence and limitations, without pretending that a confidence number is calibrated;
- privacy/data classification, access policy, retention and redaction metadata;
- links to related events, observations, incidents, claims, assumptions, threats and controls.

**Derived assessment/evidence record**
- exact input observation IDs and transformation/model/rule revision;
- inference method (rule, statistical model, analyst assessment, correlation or investigation);
- candidate hypothesis, alternative explanations and counterevidence;
- scope, assumptions, uncertainty, limitations and result state;
- claims, threat scenarios, attack paths, controls and decisions potentially affected;
- reviewer/authority requirements and resulting invalidation/reassessment events.

This split preserves raw testimony and makes interpretation reproducible. A derived assessment never rewrites its source observation. The existing evidence record can reference both as evidence artifacts and bind the resulting claim support/refutation to exact revisions.

## 5. SACM 2.3: what it gives GovCheck

SACM 2.3 is substantially richer than a simple claim/evidence list. The official metamodel defines four main compliance points and separates packages for assurance cases, argumentation, artifacts and terminology [R-34](../references.md#r-34).

### 5.1 Useful constructs

| SACM 2.3 construct | Contribution | GovCheck use |
|---|---|---|
| AssuranceCasePackage | Exchangeable top-level container for argumentation, artifacts and terminology | Package a governed assurance case and its vocabulary/artifact references |
| Claim / Assertion | Explicit propositions, including declared/assumed/needs-support/axiomatic/defeated states | Represent assurance claims and explicit undeveloped/defeated states |
| ArgumentReasoning | Description of the reasoning behind relationships | Preserve inference rationale and argument method |
| AssertedInference | Connect premises and conclusions | Map typed inference edges |
| AssertedEvidence | Relate artifact references to claims/argumentation | Map evidence-to-claim support or counterevidence |
| AssertedContext | Attach contextual premises | Map system context, assumptions and constraints |
| ArtifactReference / Artifact | Refer to external evidence and engineering artifacts | Link exact GovCheck artifacts, configurations, models, reports and observations |
| Event | Record events in an artifact lifecycle | Potential representation of lifecycle events and observations, with GovCheck extensions |
| Activity / Technique / Participant / Resource | Describe work, methods, actors and tangible resources | Represent evidence production context and provenance participants |
| ArtifactAssetRelationship | Link artifact assets with named/description-bearing relationships | Provide a general artifact relationship bridge |
| TerminologyPackage | Define controlled terms and expressions | Publish GovCheck vocabulary and PEAK/SACM mappings |
| Package interfaces/bindings | Modular exchange and relationships between packages | Separate assurance cases by project/component and bind them explicitly |

The model is not merely diagram notation: it has a normative machine-readable XMI representation. SACM 2.3 explicitly includes Event for artifact lifecycle happenings and ArtifactAssetRelationship for links between artifact assets. Its claim declaration vocabulary distinguishes assumed, asserted, needs-support, axiomatic and defeated claims. These features make it a serious candidate for interchange and structured argument representation.

### 5.2 Where SACM is richer than the current GovCheck proposal

SACM contributes mature, explicit assurance-case structures that GovCheck's current 0013/0021 proposal does not fully define:
- reusable modular assurance-case packages and package interfaces/bindings;
- distinct terminology, artifact and argumentation packages;
- explicit assertion/inference/evidence/context relationship types;
- explicit defeated/counterevidence and incomplete/needs-support states;
- first-class artifact, event, activity, technique, participant and resource concepts;
- a published interchange format and conformance points.

GovCheck should not recreate these concepts casually. A mapping or implementation should reuse their semantics where they fit, and document deliberate differences.

### 5.3 What SACM 2.3 does not supply for GovCheck

SACM is an assurance-case metamodel, not a complete security, operational-risk or governance ontology. In particular, it does not by itself provide:

- a domain threat model: adversary capabilities, threat sources, attack techniques, attack paths, preconditions, exposure and vulnerability semantics;
- a security-control lifecycle: planned, implemented, configured, tested, independently reviewed, monitored, degraded and retired;
- a runtime telemetry contract with sensor identity, clock quality, collection coverage, integrity, privacy classification and raw-event retention;
- a defined distinction between event, observation, indicator, hypothesis, assessed threat, confirmed incident and risk;
- risk assessment and treatment semantics, residual-risk acceptance, accountable risk owner, approval authority, expiry and reassessment triggers;
- the full PEAK decision-input model and decision-outcome/risk-assumption traceability;
- GovCheck's exact subject/revision binding, evidence freshness, dependency invalidation and lifecycle acceptance semantics;
- cryptographic provenance verification, trust policy or enforcement behavior.

SACM's generic Event and ArtifactAssetRelationship are useful extension points, not substitutes for these domain semantics. Similarly, an assumed Claim declaration is not a complete assumption governance record with owner, scope, validity, monitor, falsification criteria and consequences.

### 5.4 SACM 2.4 Beta changes the assessment

As of this record, OMG lists SACM 2.4 Beta 1 (September 2026) as an in-process beta, while 2.3 remains the formal version [R-73](../references.md#r-73). The beta issue tracker shows proposed/resolved changes addressing several important 2.3 gaps, including:
- typed structured values and strength-related data (SACM24-80);
- assessment-related constructs (SACM24-75);
- joins for combining assertions/evidence (SACM24-76);
- whole-concept references (SACM24-73);
- a needsDevelopment marker (SACM24-74);
- package structure and domain ownership (SACM24-56);
- more precise inference/evidence targets (SACM24-82).

This is significant: some things that might otherwise become GovCheck extensions are being considered by the SACM revision itself. But beta issue dispositions are not a final normative contract. GovCheck should track the 2.4 evolution and reassess when a formal release and machine-readable model are published.

## 6. Proposed semantic architecture

Use a **GovCheck domain graph** as the authoritative semantic layer, with adapters/projections for PEAK and SACM.

### 6.1 Core domain concepts

At minimum, keep stable identities and typed relations for:

- **System context:** project, asset, component, deployment instance, environment, configuration snapshot and trust boundary.
- **Threat model:** threat source/actor, capability, threat event, scenario, attack technique/path, precondition, weakness, exposure and consequence.
- **Control:** control definition, implementation/configuration instance, owner, lifecycle state, test/assessment and monitoring status.
- **Operational testimony:** event, observation, sensor/collector, indicator, anomaly, hypothesis, incident/finding and derived assessment.
- **Assurance:** claim, subclaim, argument/reasoning, assumption, evidence, counterevidence/defeater, method, scope, limitation, review and assurance status.
- **Risk and decisions:** risk assessment, treatment option, residual risk, acceptance decision, authority, owner, alternatives, rationale, validity, expiry and reassessment trigger.
- **Provenance:** producer/participant, activity, tool, source, timestamp, exact revisions, digest, integrity/authenticity, derivation and supersession.

### 6.2 Important typed relations

The relation vocabulary should include, at least:

- observedOn, collectedBy, derivedFrom, correlatedWith;
- indicates, hypothesizes, confirms, refutes, challenges;
- threatens, enables, requiresPrecondition, followsAttackStep;
- mitigatedBy, implementedAs, configuredBy, testedBy, monitoredBy;
- supports, refutes, contextualizes, assumes, inferredFrom;
- affectsClaim, invalidatesEvidence, invalidatesReview, triggersReassessment;
- assessedBy, treatedBy, acceptsResidualRisk, authorizedBy;
- supersedes, derivedFrom, revalidates.

Relations must carry their own identity, provenance, scope and (where relevant) validity interval. A generic untyped edge or a textual label is insufficient for normative interpretation.

### 6.3 Projection rules

- **PEAK projection:** render a decision and its linked Problem, Experience, Assumptions and Knowledge inputs, then its selected Solution and Assumed Risk. Each displayed item links to its canonical GovCheck identity and revision.
- **SACM projection:** map claims, reasoning, inference, evidence, context, artifacts and terminology into SACM packages. Preserve GovCheck-only semantics in a namespaced extension/profile or explicit linked records. Round-trip tests must detect any dropped or weakened semantics.
- **Threat-model projection:** display design-time scenarios and attack paths alongside observation-derived indicators/hypotheses, clearly distinguishing modeled possibilities from observed facts and confirmed findings.
- **Operational projection:** show the current system/deployment snapshot, observation coverage, control state, outstanding hypotheses, affected assurance claims and decisions requiring review.

The projection is not the source of truth. A user editing a PEAK or SACM view must produce explicit GovCheck domain changes with validation and authority checks.

## 7. Semantic invariants and safety constraints

1. Raw observations are immutable; corrections or reinterpretations create new records linked to the original.
2. An observation is not automatically a fact, indicator, hypothesis, incident, threat or risk assessment.
3. A hypothesis retains alternative explanations, confidence basis, uncertainty and counterevidence.
4. No observation absence implies absence of a threat unless monitoring coverage and sensor health support that inference.
5. Assumptions are first-class governed premises, distinct from evidence and from assumed risk.
6. Monitorable assumptions link to explicit predicates, monitor identity, coverage and response policy; not every assumption is monitorable.
7. A violated assumption challenges only the claims/decisions whose argument closure depends on it; impact must be traced, not guessed globally.
8. A threat-model update is versioned and reviewed. An observation can propose a new scenario or revise plausibility, but does not silently change the normative baseline.
9. Control effectiveness is scoped to the tested/observed deployment, configuration, method and time window.
10. A risk acceptance decision does not improve assurance status, validate a control or erase counterevidence.
11. A production action requires explicit policy and authority; recommendations and predictions are not authorization.
12. Historical decisions, observations, assessments and assurance states remain auditable after supersession or invalidation.

## 8. Adoption recommendation and staged work

### Recommendation

- Keep GovCheck's domain graph and governance authority semantics canonical.
- Adopt PEAK as a required **decision-traceability view** for material governance/security/risk decisions, not as a separate ontology or automatic decision rule.
- Treat SACM 2.3 as the first **interchange target** for assurance-case structures, not as the entire GovCheck metamodel.
- Track SACM 2.4 Beta 1 and avoid finalizing mappings for areas currently changing until a formal 2.4 release is available.
- Add GovCheck profile/extension semantics only where the SACM base cannot represent the required domain meaning; keep mappings explicit and loss-aware.

### Proposed sequence

1. **Semantic mapping specification:** map GovCheck 0013/0021 and evidence records to PEAK and SACM 2.3; record unmapped concepts and cardinalities.
2. **Observation contract:** define a versioned operational observation/event schema separately from the derived evidence/assessment record; include provenance, exact subject, clock/coverage, integrity, uncertainty and privacy.
3. **Threat-feedback contract:** define the transition from observation to indicator/hypothesis, threat-model proposal, review and versioned update.
4. **Decision contract:** define PEAK input links, alternatives, solution, assumed/residual risk, authority, expiry and reassessment triggers.
5. **SACM interoperability prototype:** export/import a representative assurance case; test claims, assumptions, contexts, counterevidence, artifacts, events, package bindings and GovCheck extensions for round-trip loss.
6. **Formal checks:** model invalidation/reassessment and decision authorization separately from detection. Do not combine all runtime threat reasoning into one state-explosion-prone model.
7. **Operational pilot:** use synthetic observations first, then a bounded non-sensitive telemetry source. Do not automate consequential mitigation before false-positive handling, rollback, authorization and evidence preservation are demonstrated.

## 9. Limits and non-decisions

This record does not adopt SACM as the canonical GovCheck ontology, select a graph database, prescribe a risk score, define a production telemetry platform, authorize autonomous remediation or claim that runtime threat modeling is implemented. PEAK remains a decision-analysis framework; SACM remains an assurance-case metamodel. Their roles are deliberately distinct.

The immediate design question is not “which single model replaces the others?” It is “what canonical semantics allow us to project the same governed facts and decisions into threat, runtime, PEAK and SACM views without losing provenance, uncertainty, authority or meaning?”
