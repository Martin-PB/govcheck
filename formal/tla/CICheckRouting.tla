-------------------------- MODULE CICheckRouting --------------------------
EXTENDS FiniteSets

Categories ==
  {"LifecycleSource", "LifecycleConfig", "LifecycleSemantics",
   "AssuranceSource", "AssuranceConfig", "AssuranceSemantics",
   "AuthoritySource", "AuthorityConfig", "AuthoritySemantics",
   "LifecycleWorkflow", "AssuranceWorkflow", "AuthorityWorkflow",
   "SharedTLCWorkflow", "UnrelatedArchitecture", "OrdinaryDocumentation"}

ModelSpecific ==
  {"LifecycleSource", "LifecycleConfig", "LifecycleSemantics",
   "AssuranceSource", "AssuranceConfig", "AssuranceSemantics",
   "AuthoritySource", "AuthorityConfig", "AuthoritySemantics"}

VARIABLE changed
vars == <<changed>>

Init == changed \in SUBSET Categories
Next == UNCHANGED vars
Spec == Init /\ [][Next]_vars

LifecycleInputs ==
  {"LifecycleSource", "LifecycleConfig", "LifecycleSemantics", "LifecycleWorkflow"}
AssuranceInputs ==
  {"AssuranceSource", "AssuranceConfig", "AssuranceSemantics", "AssuranceWorkflow"}
AuthorityInputs ==
  {"AuthoritySource", "AuthorityConfig", "AuthoritySemantics", "AuthorityWorkflow"}

RunLifecycle == changed \cap (LifecycleInputs \cup {"SharedTLCWorkflow"}) # {}
RunAssurance == changed \cap (AssuranceInputs \cup {"SharedTLCWorkflow"}) # {}
RunAuthority == changed \cap (AuthorityInputs \cup {"SharedTLCWorkflow"}) # {}

TypeOK == changed \subseteq Categories

NoUnrelatedDocumentationTriggersTLC ==
  changed \subseteq {"UnrelatedArchitecture", "OrdinaryDocumentation"}
  => ~RunLifecycle /\ ~RunAssurance /\ ~RunAuthority

LifecycleIsolation ==
  changed \subseteq LifecycleInputs /\ changed # {}
  => RunLifecycle /\ ~RunAssurance /\ ~RunAuthority

AssuranceIsolation ==
  changed \subseteq AssuranceInputs /\ changed # {}
  => RunAssurance /\ ~RunLifecycle /\ ~RunAuthority

AuthorityIsolation ==
  changed \subseteq AuthorityInputs /\ changed # {}
  => RunAuthority /\ ~RunLifecycle /\ ~RunAssurance

SharedRunnerInvalidatesAll ==
  "SharedTLCWorkflow" \in changed
  => RunLifecycle /\ RunAssurance /\ RunAuthority

LifecycleCoverage ==
  changed \cap LifecycleInputs # {} => RunLifecycle
AssuranceCoverage ==
  changed \cap AssuranceInputs # {} => RunAssurance
AuthorityCoverage ==
  changed \cap AuthorityInputs # {} => RunAuthority

THEOREM Spec => []TypeOK
THEOREM Spec => []NoUnrelatedDocumentationTriggersTLC
THEOREM Spec => []LifecycleIsolation
THEOREM Spec => []AssuranceIsolation
THEOREM Spec => []AuthorityIsolation
THEOREM Spec => []SharedRunnerInvalidatesAll
THEOREM Spec => []LifecycleCoverage
THEOREM Spec => []AssuranceCoverage
THEOREM Spec => []AuthorityCoverage

=============================================================================
