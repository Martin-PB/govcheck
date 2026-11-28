# GovCheck typed-relation candidate matrix

**Status:** research candidate, not an adopted metamodel or evaluator rule. This addendum responds to the semantic-coverage work in issue #73. It proposes typed relations rather than a single lifecycle chain; it does not declare external ontology terms equivalent by name.

**Semantic audit:** [2026-11-28 relation-mapping audit](semantic-mapping-audit-2026-11-28.md) evaluates source-native semantics and non-equivalences; it does not adopt any mapping.

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


## 7. Source-grounded crosswalk (version-pinned, candidate only)

| Source baseline | Native structure/relations | Candidate GovCheck use | Non-equivalence guard |
|---|---|---|---|
| SACM 2.3 formal; SACM 2.4 Beta 1 (R-34, R-73) | Claims, argumentation, evidence/artifact references; 2.4 beta adds/clarifies assertion and inference structures. | Assurance subgraph and typed claim/evidence/argument mapping. | Preserve source version and native structure; 2.4 remains beta. An SACM claim/argument link is not automatically a GovCheck requirement, proof or authorization. |
| GSN Community Standard v3 (R-04) | Goals, Strategies, Context, Assumptions, Justifications, Solutions and defined argument links. | Candidate mapping of claim decomposition, rationale, context, assumption and evidence references. | GSN is an argument notation/standard, not a lifecycle or governance authority. Do not call it “GSN 3.0”; use the SCSC v3 source. |
| SysML v2.0 (R-95, R-119) | Formal systems-modeling language with requirements, structure, behavior, analysis and verification semantics. | Typed engineering artifacts and candidate requirement/property/component relations. | Do not infer `satisfies`, `realizes` or `refines` from matching labels; preserve model semantics and transformation profile. |
| ReqIF 1.2 (R-95) | Requirements interchange objects, attributes and relations. | Import/export of requirement records and source-native links. | Exchange-format relations are not automatically assurance, authority or satisfaction claims. |
| W3C PROV-O (R-24, R-102) | Entity, Activity, Agent and provenance properties such as derivation, use, generation and association. | Provenance assertions for artifact/revision/process/agent relationships. | `wasDerivedFrom` is provenance, not semantic refinement, entailment or truth. |
| OASIS OSLC Core 3.0 and Resource Shape (R-234, R-235) | Linked-data resource/service interoperability and structural shape constraints. | Navigation/interoperability links and structural validation of exchange payloads. | URI links and shape conformance do not establish assurance semantics, authority, evidence authenticity or sufficiency. |

## 8. Required mapping-profile record

Before any source-native relation becomes operative, its mapping profile must record: exact source specification/version; source relation identifier and domain/range; GovCheck candidate relation; direction and cardinality; semantic preservation or explicit loss; unmapped constructs; source-native payload retention; revision and applicability; provenance; authority if normative; and positive/negative fixtures.

A label match is not a mapping proof. A profile that cannot justify the mapping remains a candidate/unsupported relation and must not feed the evaluator. See the [reference catalogue](../references.md#r-234) and [semantic-coverage audit](metamodel-semantic-coverage-audit.md).


Crosswalk sources: [R-4](../references.md#r-04) · [R-24](../references.md#r-24) · [R-34](../references.md#r-34) · [R-73](../references.md#r-73) · [R-95](../references.md#r-95) · [R-102](../references.md#r-102) · [R-119](../references.md#r-119) · [R-234](../references.md#r-234) · [R-235](../references.md#r-235).
