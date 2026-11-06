# 0011 — Lifecycle model: assertion-by-assertion reading and verification status

**Status:** source-level analysis of the current repository artifact. This is not a TLC result, theorem proof or implementation-conformance report. **French:** [0011 (français)](0011-lifecycle-model-assertion-audit.fr.md).

## 1. What exists

PR #4 added:
- `formal/tla/GovCheckLifecycle.tla`;
- `formal/tla/GovCheckLifecycle.cfg`;
- bilingual explanations under `docs/formal/`;
- `formal/lifecycle-transitions.json`;
- generated `docs/formal/lifecycle-diagram.mmd`;
- `scripts/render-lifecycle-diagram.py`;
- `formal/artifacts.json` and the release-manifest JSON Schema.

The TLA+ module is the semantic authority. The JSON transition registry and Mermaid diagram are explanatory. The Python script checks structural coverage and generated-file drift; it does not prove semantic equivalence between registry and TLA+.

## 2. Abstract identity and state

The modeled change is tied to:

`CurrentTuple = <<baseId, candidateId, governanceId, specId>>`

The tuple deliberately makes base, candidate, governance and specification revisions relevant to evaluation and acceptance. It does not yet include every real-world identity (repository ID, evaluator build, environment, dependency set, approval policy, external facts); those are refinements still required.

State variables:
- `phase`: Proposed, Prepared, Evaluated, Reviewable, Accepted, Applied, Rejected, Withdrawn, Superseded or Stale;
- `baseId`, `candidateId`, `governanceId`, `specId`;
- `evaluatedTuple`;
- `outcomes` for a finite obligation set;
- `evidence`, currently a set of obligation identifiers;
- `approvals`, currently a set of authorized actor identifiers;
- `acceptedTuple`;
- `appliedCandidateId`;
- `history`, an abstract event-label sequence.

The configured instance has two values per identity dimension, two actors, two obligations and `HistoryLimit = 12`. The finite sets and history limit are exploration parameters, not production constraints.

## 3. Actions and their meaning

- `Prepare`: Proposed → Prepared; records preparation.
- `PublishEvidence(obligation)`: records an obligation identifier, returns to Prepared and invalidates the evaluated tuple/outcomes.
- `Evaluate`: evaluates the current tuple; every obligation with a published identifier becomes Pass, otherwise Unknown. All present → Reviewable; otherwise Evaluated.
- `Approve(actor)`: adds an authorized actor while phase is Reviewable and evaluated tuple is current.
- `Accept`: requires Reviewable, current evaluation, all Pass and sufficient approval-set cardinality; records the current tuple as accepted.
- `Apply`: requires Accepted and accepted tuple still current; records its candidate ID as applied.
- `ChangeInputs`: changes base/candidate/governance/specification, marks Stale, clears evaluation/evidence/approvals/acceptance/application.
- `Reject`, `Withdraw`, `Supersede`: record terminal decisions.
- `Next`: disjunction of these actions, with existential choices for obligation, actor and new tuple.

The model's state-changing actions append a label to `history`, subject to the history limit.

## 4. Every configured invariant, precisely

| Name | Exact question answered | Important limit |
|---|---|---|
| `TypeOK` | Do variables stay within declared domains and history bounds? | Type/domain discipline, not business correctness. |
| `AcceptanceSoundness` | If Accepted, does acceptedTuple=currentTuple, evaluatedTuple=currentTuple, all outcomes=Pass, and approval count meet threshold? | Only as strong as the simplified evidence and approval variables. |
| `ApplicationSoundness` | If Applied, does appliedCandidateId equal the candidate in the accepted/current tuple? | Does not model a real adapter or prove an external VCS applied it. |
| `NoStaleEvaluation` | In Reviewable/Accepted/Applied, is evaluatedTuple current? | Only the four modeled tuple dimensions are covered. |
| `EvidenceBinding` | In Reviewable, is evaluation current and evidence set equal to modeled obligations? | Evidence is not a provenance-bearing object and is not individually tuple-bound. |
| `ApprovalBinding` | In Accepted/Applied, are approval IDs members of AuthorizedActors? | No per-approval tuple, signature, role, timestamp, reason or revocation record. |
| `NoImplicitApplication` | Outside Applied, is appliedCandidateId None? | Does not establish external application behavior. |
| `HistoryNonEmpty` | Does history contain at least its initial event? | Not a full append-only/prefix/integrity property. |

## 5. Temporal property and theorem declarations

`TerminalDiscipline` is configured under TLC `PROPERTIES`, not `INVARIANTS`. It says that once phase is Applied, Rejected, Withdrawn or Superseded, the next phase remains the same.

The module also contains `THEOREM Spec => []Property` declarations. They record intended theorem obligations. Their presence is not evidence that a theorem prover discharged them. SANY parsing, structural source checks, TLC invariant/property exploration and theorem proving are distinct operations. A report must name the actual operation executed.

## 6. Source-level limitations and concrete refinement work

1. **Evidence identity:** `evidence` stores obligation names, not evidence objects with subject, method, producer, tool, result, digest, validity, provenance and dependency identities.
2. **Evidence truth/adequacy:** `Evaluate` maps published evidence directly to Pass. It models no independent verifier, claim/evidence argument or source trust.
3. **Failure states:** Fail is declared but no action produces it. A future model must distinguish failed, unknown, unsupported, not-run, incomplete, stale and conflict.
4. **Approval binding:** approvals are actor IDs in a set, not signed records bound individually to candidate/governance/approval policy. Membership in AuthorizedActors is weaker than full authorization evidence.
5. **Approval invalidation:** ChangeInputs clears approvals, but PublishEvidence does not. Since PublishEvidence is enabled in Reviewable and returns to Prepared, a refinement must decide whether changed evidence invalidates existing approvals.
6. **Concurrency:** no simultaneous approval, evidence publication, input mutation, acceptance or apply race is modeled.
7. **Application:** Apply is an abstract state transition. It does not invoke or verify a real Git/Pijul adapter, its capabilities, preconditions, partial failure or actual applied state.
8. **History:** actions append labels, but HistoryNonEmpty does not prove history-prefix preservation, authenticity, actor/reason metadata or tamper evidence.
9. **External trust:** no cryptographic key, signature, revocation, external source freshness, compromised tool or malicious adapter is represented.
10. **VCS semantics:** Git dirty worktree/index/submodule identity and Pijul patch/channel/graph/conflict semantics are outside this model.
11. **Terminal remediation:** ChangeInputs is disabled after terminal phases, including Applied. Reopening/remediation after application needs a policy decision.
12. **Finite trace:** HistoryLimit=12 eventually disables state-changing actions. This is a state-space bound, not a retention rule.

These limitations define the current abstraction's contribution; they do not erase the value of the initial lifecycle model.

## 7. What PR #4 actually verified

PR #4 reported structural checks:
- transition registry parses as JSON;
- ten actions in `Next` are represented in the registry;
- registry operators have top-level TLA+ definitions;
- state-changing actions include the history bound;
- committed Mermaid content matches the registry rendering rules.

The report explicitly did **not** claim:
- that the Python generator had been executed in a repository checkout;
- SANY syntax validation or TLC model checking;
- a theorem proof;
- implementation-to-model conformance;
- a local test suite or schema validator;
- hosted CI execution.

A structural check of a model source is not model checking. A TLC run is not theorem proving. Neither is implementation conformance.

## 8. Required next verification sequence

1. Pin TLA+ Tools/TLC and Java versions; record binary/distribution digests.
2. Run SANY/parser validation and record exact command/output.
3. Run TLC against the committed configuration; capture completion, state/transition counts, deadlocks and counterexamples.
4. Review every counterexample; distinguish model defect from design defect.
5. Refine evidence objects and dependency freshness; model explicit Fail/Unknown/Unsupported/NotRun/Incomplete/Conflict.
6. Bind approvals individually to candidate, governance revision, policy, role, actor and revocation state.
7. Add concurrency and apply-race models, preferably as separate composable models.
8. Define language-neutral conformance vectors and a refinement relation for the implementation.
9. Only then report the specific assurance claims supported by the resulting artifacts.

No step in this sequence should be described as completed until its execution evidence is committed or attached to the corresponding release.
