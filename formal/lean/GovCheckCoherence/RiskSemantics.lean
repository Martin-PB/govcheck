namespace GovCheck.Coherence.Risk

/-- Exact non-negative rational represented without floating-point rounding. -/
structure NonnegativeRational where
  numerator : Nat
  denominator : Nat
  denominatorPositive : 0 < denominator
  deriving Repr

/-- A rational constrained to the unit interval. The numerator/denominator
    representation is exact; it is not a floating-point percentage. -/
structure UnitInterval where
  numerator : Nat
  denominator : Nat
  denominatorPositive : 0 < denominator
  bounded : numerator ≤ denominator
  deriving Repr

structure ProbabilityPoint where
  value : UnitInterval
  eventIdentity : String
  conditioningContext : String
  timeHorizon : String
  interpretation : String
  deriving Repr

structure ProbabilityInterval where
  lower : UnitInterval
  upper : UnitInterval
  ordered :
    lower.numerator * upper.denominator ≤
      upper.numerator * lower.denominator
  eventIdentity : String
  conditioningContext : String
  timeHorizon : String
  interpretation : String
  deriving Repr

/-- A finite distribution uses integer weights over one exact denominator.
    The outcome space and the normalization equation are explicit. -/
structure FiniteProbabilityDistribution (Outcome : Type) where
  outcomeSpace : List Outcome
  denominator : Nat
  weights : List (Outcome × Nat)
  denominatorPositive : 0 < denominator
  normalized :
    weights.foldl (fun total item => total + item.2) 0 = denominator

/-- A fuzzy grade is tied to a concept and membership-function revision. -/
structure FuzzyMembership where
  degree : UnitInterval
  conceptIdentity : String
  universeIdentity : String
  membershipFunctionIdentity : String
  membershipFunctionRevision : String
  deriving Repr

/-- A nondeterministic possibility is a non-empty set/list of outcomes with
    no probability weights implied by its representation. -/
structure NondeterministicPossibility (Outcome : Type) where
  outcomes : List Outcome
  nonempty : outcomes ≠ []

structure TransitionRate where
  rate : NonnegativeRational
  timeUnit : String
  processModelIdentity : String
  processModelRevision : String
  deriving Repr

structure ArgumentConfidence where
  judgment : String
  argumentIdentity : String
  argumentRevision : String
  methodIdentity : String
  assessorIdentity : String
  calibrationRecord : Option String
  deriving Repr

structure CostValue where
  amount : NonnegativeRational
  unit : String
  deriving Repr

structure UtilityValue where
  amount : NonnegativeRational
  scaleIdentity : String
  deriving Repr

structure PriorityValue where
  rank : Nat
  scaleIdentity : String
  deriving Repr

structure EmpiricalFrequency where
  occurrences : Nat
  observations : Nat
  populationIdentity : String
  observationPeriod : String
  observationsPositive : 0 < observations
  occurrencesBounded : occurrences ≤ observations
  deriving Repr

/-- The sum type makes uncertainty semantics explicit. No coercions between
    constructors are declared. Equal numeric payloads do not make their
    interpretations interchangeable. -/
inductive TypedUncertaintyValue where
  | probabilityPoint (value : ProbabilityPoint)
  | probabilityInterval (value : ProbabilityInterval)
  | probabilityDistribution (value : FiniteProbabilityDistribution String)
  | fuzzyMembership (value : FuzzyMembership)
  | nondeterministicPossibility (value : NondeterministicPossibility String)
  | transitionRate (value : TransitionRate)
  | argumentConfidence (value : ArgumentConfidence)
  | cost (value : CostValue)
  | utility (value : UtilityValue)
  | priority (value : PriorityValue)
  | empiricalFrequency (value : EmpiricalFrequency)

/-- Availability/disposition of an assessment is independent of its
    mathematical value family. Unknown, unassessed, non-quantifiable,
    inapplicable, quantified and inconclusive are separate constructors. -/
inductive EpistemicAvailability where
  | notAssessed
  | unknown (reason : String)
  | notQuantifiable (reason : String)
  | notApplicable (reason : String)
  | quantified (value : TypedUncertaintyValue)
  | inconclusive (reason : String)

/-- PEAK inputs remain separately inspectable rather than collapsed into one
    score or confidence field. -/
structure DecisionInputs where
  problem : String
  experience : String
  assumptions : List String
  knowledge : List String
  deriving Repr

structure DecisionSolution where
  identity : String
  statement : String
  deriving Repr

/-- PEAK's assumed-risk output is a first-class decision output. It is not a
    risk scenario, quantitative assessment, treatment or acceptance. -/
structure AssumedRisk where
  identity : String
  decisionIdentity : String
  revision : String
  statement : String
  deriving Repr

structure DecisionOutcome where
  decisionIdentity : String
  solution : DecisionSolution
  assumedRisk : AssumedRisk
  deriving Repr

structure RiskScenario where
  identity : String
  revision : String
  adverseOutcome : String
  context : String
  consequences : List String
  deriving Repr

structure RiskAssessment where
  identity : String
  revision : String
  scenarioIdentity : String
  methodIdentity : String
  modelRevision : String
  dataRevision : String
  assumptions : List String
  result : EpistemicAvailability

structure RiskTreatment where
  identity : String
  revision : String
  scenarioIdentity : String
  actions : List String
  residualExposureIdentity : String

/-- A risk acceptance records its authority, scope, exact assessment and
    policy revisions, and a validity interval. This record alone does not
    prove that the named actor is authorized; that requires a separate
    authority contract. -/
structure RiskAcceptance where
  identity : String
  revision : String
  scenarioIdentity : String
  assessmentRevision : String
  authorityIdentity : String
  scope : String
  policyRevision : String
  rationale : String
  validFrom : Nat
  validUntil : Nat

/-- A binding keeps the scenario and assessment present alongside acceptance,
    and pins acceptance to their exact identities/revisions. -/
structure RiskAcceptanceBinding
    (scenario : RiskScenario) (assessment : RiskAssessment) where
  acceptance : RiskAcceptance
  scenarioPinned :
    acceptance.scenarioIdentity = scenario.identity
  assessmentPinned :
    acceptance.assessmentRevision = assessment.revision
  assessmentScenarioPinned :
    assessment.scenarioIdentity = scenario.identity

/-- Distinct risk objects remain distinct in a single typed envelope. -/
inductive DecisionRiskObject where
  | assumedRisk (value : AssumedRisk)
  | scenario (value : RiskScenario)
  | assessment (value : RiskAssessment)
  | treatment (value : RiskTreatment)
  | acceptance (value : RiskAcceptance)

theorem probability_point_is_not_fuzzy_membership
    (probability : ProbabilityPoint) (fuzzy : FuzzyMembership) :
    TypedUncertaintyValue.probabilityPoint probability ≠
      TypedUncertaintyValue.fuzzyMembership fuzzy := by
  intro h
  cases h

theorem probability_distribution_is_not_nondeterminism
    (probability : FiniteProbabilityDistribution String)
    (possibilities : NondeterministicPossibility String) :
    TypedUncertaintyValue.probabilityDistribution probability ≠
      TypedUncertaintyValue.nondeterministicPossibility possibilities := by
  intro h
  cases h

theorem transition_rate_is_not_probability
    (rate : TransitionRate) (probability : ProbabilityPoint) :
    TypedUncertaintyValue.transitionRate rate ≠
      TypedUncertaintyValue.probabilityPoint probability := by
  intro h
  cases h

theorem argument_confidence_is_not_probability
    (confidence : ArgumentConfidence) (probability : ProbabilityPoint) :
    TypedUncertaintyValue.argumentConfidence confidence ≠
      TypedUncertaintyValue.probabilityPoint probability := by
  intro h
  cases h

theorem cost_is_not_utility
    (cost : CostValue) (utility : UtilityValue) :
    TypedUncertaintyValue.cost cost ≠ TypedUncertaintyValue.utility utility := by
  intro h
  cases h

theorem priority_is_not_frequency
    (priority : PriorityValue) (frequency : EmpiricalFrequency) :
    TypedUncertaintyValue.priority priority ≠
      TypedUncertaintyValue.empiricalFrequency frequency := by
  intro h
  cases h

theorem not_assessed_is_not_unknown (reason : String) :
    EpistemicAvailability.notAssessed ≠
      EpistemicAvailability.unknown reason := by
  intro h
  cases h

theorem unknown_is_not_not_quantifiable (reason : String) :
    EpistemicAvailability.unknown reason ≠
      EpistemicAvailability.notQuantifiable reason := by
  intro h
  cases h

theorem unknown_is_not_not_applicable (reason : String) :
    EpistemicAvailability.unknown reason ≠
      EpistemicAvailability.notApplicable reason := by
  intro h
  cases h

theorem unknown_is_not_inconclusive (reason : String) :
    EpistemicAvailability.unknown reason ≠
      EpistemicAvailability.inconclusive reason := by
  intro h
  cases h

theorem quantified_is_not_unknown
    (value : TypedUncertaintyValue) (reason : String) :
    EpistemicAvailability.quantified value ≠
      EpistemicAvailability.unknown reason := by
  intro h
  cases h

theorem assumed_risk_is_not_scenario
    (assumed : AssumedRisk) (scenario : RiskScenario) :
    DecisionRiskObject.assumedRisk assumed ≠
      DecisionRiskObject.scenario scenario := by
  intro h
  cases h

theorem assumed_risk_is_not_assessment
    (assumed : AssumedRisk) (assessment : RiskAssessment) :
    DecisionRiskObject.assumedRisk assumed ≠
      DecisionRiskObject.assessment assessment := by
  intro h
  cases h

theorem assumed_risk_is_not_acceptance
    (assumed : AssumedRisk) (acceptance : RiskAcceptance) :
    DecisionRiskObject.assumedRisk ≠
      DecisionRiskObject.acceptance acceptance := by
  intro h
  cases h

theorem acceptance_is_pinned_to_scenario_and_assessment
    {scenario : RiskScenario} {assessment : RiskAssessment}
    (binding : RiskAcceptanceBinding scenario assessment) :
    binding.acceptance.scenarioIdentity = scenario.identity ∧
      binding.acceptance.assessmentRevision = assessment.revision ∧
      assessment.scenarioIdentity = scenario.identity :=
  ⟨binding.scenarioPinned, binding.assessmentPinned,
    binding.assessmentScenarioPinned⟩

theorem acceptance_records_authority_scope_and_validity
    (acceptance : RiskAcceptance) :
    (acceptance.authorityIdentity, acceptance.scope,
      acceptance.policyRevision, acceptance.validFrom,
      acceptance.validUntil) =
    (acceptance.authorityIdentity, acceptance.scope,
      acceptance.policyRevision, acceptance.validFrom,
      acceptance.validUntil) :=
  rfl

theorem decision_outcome_keeps_assumed_risk
    (outcome : DecisionOutcome) :
    outcome.assumedRisk.decisionIdentity = outcome.decisionIdentity ∧
      outcome.assumedRisk.identity = outcome.assumedRisk.identity :=
  ⟨rfl, rfl⟩

end GovCheck.Coherence.Risk
