# GovCheck typed-relation candidate matrix

**Status:** research candidate, not an adopted metamodel or evaluator rule. This addendum responds to the semantic-coverage work in issue #73. It proposes typed relations rather than a single lifecycle chain; it does not declare external ontology terms equivalent by name.

## 1. Relation assertion, not a bare edge

A relation assertion should carry at least:

- immutable source and target artifact references (identifier, revision and optional fragment);
- relation type and versioned semantic profile;
- scope and applicability interval/event;
- provenance for how the assertion was created;
- authority record when the relation changes normative state;
- evidence reference and freshness state when the relation is evidential;
- status: candidate, active, unknown, conflict, stale, invalidated or rejected.

The assertion itself is an artifact that can be revised, superseded or invalidated. A link in a document is not automatically a semantic relation.

## 2. Candidate relation families

All relations are directed and many-to-many unless a profile states otherwise. The table gives candidate domain/range types, not universal cardinality rules.

| Relation | Source → target | Candidate meaning and guard |
|---|---|---|
| `adopts` | AuthorityDecision → Model/SpecificationRevision | Normative adoption; requires authenticated authority, scope and publication event. |
| `authorizes` | AuthorityGrant → Action/Publication | Permission within explicit actor, object, operation and time scope. |
| `obligates` / `prohibits` / `permits` | Norm/Policy → Actor/Action | Deontic relations; never inferred from descriptive evidence alone. |
| `decomposes` | Goal/Requirement → Subgoal/Subrequirement | Structural decomposition; completeness is a separate claim. |
| `derives` | Rationale/Claim/Requirement → DerivedClaim/Requirement | Derivation with a recorded justification or rule. |
| `refines` | Model/Requirement → RefinedModel/Requirement | Semantic refinement; operative only with a preservation/coverage argument for its profile. |
| `allocates` | Requirement/Property → Component/Subsystem | Allocation; does not by itself establish satisfaction. |
| `realizes` | Implementation/Design → Model/Requirement/Property | Realization claim; requires trace and configuration context. |
| `satisfies` | Implementation/AssuranceClaim → Requirement/Property | Satisfaction claim; must be supported by method-appropriate evidence. |
| `verifies` | Test/ModelCheck/Proof → Claim/Property | Verification relation qualified by method, assumptions, bounds and result. |
| `validates` | Need/Intent/StakeholderClaim → System/Requirement | Validation against an identified stakeholder context and acceptance criterion. |
| `supports` / `defeats` | Evidence/Observation → Claim | Evidential support or defeater; includes provenance, scope and freshness. |
| `justifies` | Rationale/Evidence → Decision/Claim | Reason-giving relation; the decision remains a separate authorized act. |
| `assumes` | Model/Decision → Assumption/Risk | Explicit assumption; linked to owner, residual risk and review/expiry. |
| `wasDerivedFrom` | ArtifactRevision/Activity → SourceRevision/Agent | Provenance, not semantic equivalence or truth. |
| `supersedes` | Revision/Decision → PreviousRevision/Decision | Version succession; must not rewrite prior history. |
| `invalidates` | Change/RevocationEvent → Claim/Evidence/Evaluation | Prospective invalidation with scope and effective event. |
| `observes` | Observation/Measurement → State/Claim | Descriptive observation with instrument, context and time. |
| `contradicts` | Claim/Evidence → Claim | Conflict relation; conflict remains blocking until an authorized resolution. |

## 3. Type and cycle constraints

- There is no global DAG requirement. The lifecycle contains feedback, decisions, defeaters and revisions.
- Acyclicity should be imposed only on relation families where it is meaningful (for example, revision `supersedes` and strict decomposition within one revision).
- A cycle in `supports`, `justifies` or `refines` is not automatically valid or invalid; it needs a relation-specific rule and must not bootstrap its own authority or evidence.
- `refines`, `realizes` and `satisfies` are distinct. A design may refine a requirement, an implementation may realize a design, and evidence may support a satisfaction claim; these are not interchangeable.
- `verifies` is method-qualified: a test, bounded model check and theorem proof provide different assurance types. A passing test is evidence, not proof.
- `wasDerivedFrom` records provenance only. It must not be interpreted as `sameAs`, logical entailment or semantic preservation.

## 4. Candidate crosswalk to existing standards

- SACM: preserve Claim, Argument, Evidence and their source-native structure; map only relation types with an explicit profile.
- GSN: Goal, Strategy, Context, Assumption, Justification and Solution may be mapped to candidate artifact types, but a GSN link label alone does not establish GovCheck semantics.
- SysML v2 / ReqIF: requirements, properties, behaviors and allocations can supply typed source artifacts; their source-native relation semantics must remain available.
- PROV-O: derivation, activity and agent relations are provenance candidates, not normative justification or verification.
- OSLC: link types can support navigation/interoperability, but a URI link is not automatically a typed assurance claim.

No standard is selected as the sole canonical ontology by this matrix. Source-native content should remain preservable.

## 5. Operative versus candidate relations

A relation is **candidate** until its type, source/target revisions, profile and required evidence/authority are resolved. An evaluator must not use a candidate relation to authorize publication or to claim satisfaction.

For an operative semantic mapping, the profile must state its domain and coverage obligation. An empty-domain partial mapping is not an operative coverage relation; see corrective issue #210. Unknown, conflict and stale relations remain distinct and blocking where they affect the evaluated claim.

## 6. Non-adoption boundary

This matrix is a research artifact for issue #73. It does not update the canonical metamodel, alter SACM/GSN/SysML semantics, or authorize implementation claims. Adoption requires a separate decision under #41 after review of the semantic-coverage dossier and formal obligations.
