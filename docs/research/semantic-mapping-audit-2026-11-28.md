# Semantic mapping audit of typed metamodel relation candidates

**Status:** source-grounded semantic audit of a research crosswalk; not a canonical metamodel, normative mapping profile or adoption decision.  
**Audit target:** main at `3490c1b576bb155723818a43b24482a6015e9ff5`.  
**Parent:** [Issue #73](https://github.com/Martin-PB/govcheck/issues/73).  
**French:** [Audit sémantique des correspondances entre relations](semantic-mapping-audit-2026-11-28.fr.md).  
**Candidate crosswalk:** [Typed metamodel relation candidate](typed-metamodel-relation-candidate.md).

## 1. Executive conclusion

The bilingual crosswalk merged in PR #217 is a useful **source-grounded candidate catalogue**. It is not evidence that the source standards' relations are semantically equivalent to GovCheck's candidate relation names.

The audit finds recurring non-equivalences:

- an **asserted argument relation** is not a theorem proof;
- an **evidential support relation** is not proof of evidence sufficiency or truth;
- a **provenance derivation** is not semantic refinement, logical derivation or entailment;
- a **requirements interchange link** may be generic and source-type dependent;
- a **verification activity or model relation** is not itself a successful verification result;
- a **resource-shape validation** establishes structural conformance, not assurance validity or authority.

The safe default is to preserve source-native elements, types, directions, endpoint constraints and version identifiers. A GovCheck relation should remain a candidate correspondence until a version-pinned mapping profile states its semantic rule, domain/range, assumptions, information loss and proof obligations. No relation in this audit is promoted to the canonical metamodel.

## 2. Levels of correspondence

| Level | Meaning | Permitted claim |
|---|---|---|
| L0 — source preservation | Retain source-native payload, type, direction, endpoints and version. | “This source element was imported/preserved.” |
| L1 — generic link | Preserve a navigation/interoperability link without assigning GovCheck semantics. | “These resources are linked in the source.” |
| L2 — candidate semantic correspondence | Propose a typed GovCheck relation while retaining the source-native relation and mapping rationale. | “This is a candidate mapping for this source version/profile.” |
| L3 — operative mapping | A version-pinned mapping rule, endpoint/domain constraints, scope and required evidence are defined and validated. | “This mapping is operative within the declared profile and scope.” |
| L4 — proof or authority | A separate proof object or authorized decision establishes a specific claim/action. | Only the exact proof or decision is claimed; it is not inferred from L0–L3. |

L3 does not automatically imply L4. A mapping can be structurally and semantically well-defined without proving that the mapped claim is true. An asserted relationship is not an independently verified fact.

## 3. Source-native semantic findings

| Source relation / construct | Native meaning and constraints | Safe GovCheck treatment | Non-equivalence / required guard |
|---|---|---|---|
| SACM 2.3 — AssertedInference | A user-declared inference relationship between assertions/claims. It records that the argument author asserts an inferential connection. | Preserve as an argument-structure relation; candidate mapping to a qualified argument-inference relation. | Not a Lean theorem, logical entailment proof or independently validated inference. Preserve source/target types, direction and SACM version. |
| SACM 2.3 — AssertedEvidence | A declaration that an artifact, cited through ArtifactReference, provides information that helps establish a claim. SACM 2.3 includes an OCL constraint requiring ArtifactReference as source. | Candidate evidential-support relation with the referenced artifact and claim kept distinct. | Does not establish evidence authenticity, relevance, sufficiency, freshness or truth. The relation itself is an assertion by the argument author. |
| SACM 2.3 — AssertedContext | A relationship that provides context in which an argument element is interpreted. | Preserve as typed context relation; candidate mapping to a context association. | Not automatically an assumption, justification, premise, constraint or risk acceptance. Preserve the native endpoint types and direction. |
| SACM 2.3 — ArgumentReasoning | An optional descriptive element explaining reasoning associated with asserted relationships. | Preserve as a reasoning annotation/reference, not as a proof object. | The OMG issue tracker records ambiguity in how ArgumentReasoning is connected in diagrams to AssertedRelationship/AssertedInference. Until resolved, do not infer a normative edge from diagram proximity alone. |
| GSN v3 — SupportedBy | An argument-notation link between GSN elements that structures how a goal is supported by subgoals/solutions/strategies. | Candidate argument-support relation, preserving GSN element kinds and link direction. | Not a formal implication, proof term or guarantee that the supporting argument is sound. |
| GSN v3 — InContextOf | A contextual link used for context, assumption or justification elements in a GSN argument. | Preserve the concrete GSN element kind and contextual role. | Do not collapse context, assumption and justification into one GovCheck relation without a typed mapping rule. |
| SysML v2 — SatisfyRequirementUsage | A typed model relationship expressing a satisfaction claim between a requirement and a subject/model element. | Candidate satisfaction claim with requirement, subject, model revision and declared scope retained. | The model relation alone does not demonstrate satisfaction or provide test/proof evidence. The relation is not an acceptance decision. |
| SysML v2 — VerificationCase / verdict | A verification case has a subject and objective; its verdict distinguishes Pass, Fail, Inconclusive and Error. | Map the verification record as evidence with method, subject, requirements, assumptions and verdict. | Do not collapse Inconclusive or Error into Pass/Fail. A model relation to a verification case is not the verdict or its supporting evidence. |
| ReqIF 1.2 — SpecRelation / SpecRelationType | SpecRelation links two SpecObject instances and refers to a SpecRelationType. The standard leaves the relation generic; source/target type restrictions were proposed but taken out of scope for compatibility. | Preserve the relation type and endpoints as source-native interchange data. | Do not infer satisfies, derives, refines or supports from the existence of a SpecRelation or a human-readable label alone. |
| PROV-O — wasDerivedFrom | A provenance derivation: transformation, update or construction of one entity based on a pre-existing entity. | Map only to provenance lineage between entities. | Not semantic derivation of a requirement, proof derivation, refinement or entailment. |
| PROV-O — wasGeneratedBy / used / wasAttributedTo | Provenance relations between Entity, Activity and Agent describing generation, use and attribution. | Map to provenance events/agents with exact source identifiers. | Not a normative authorization, a verification result or proof of correctness. |
| OSLC Core 3.0 — resource links | Linked-data resources and domain-specific links provide interoperability and navigation; relation semantics are defined by the relevant OSLC domain vocabulary. | Preserve as source-specific links; map typed domain links only when the domain specification defines their meaning. | Generic URI linkage is not assurance semantics, authority or evidence sufficiency. |
| OSLC Resource Shape | Declares constraints and property descriptions for resources; supports structural validation of exchanged resources. | Map to shape/profile validation evidence, including shape version and validation result. | Shape conformance does not establish semantic truth, assurance adequacy or authorization. |

### 3.1 SACM 2.3 requires special care

SACM 2.3 distinguishes AssertedInference, AssertedEvidence and AssertedContext as specializations of AssertedRelationship. The source semantics differ:

- AssertedInference records an asserted inferential relationship between assertions.
- AssertedEvidence records that a referenced artifact is said to help establish a claim; its source is constrained to ArtifactReference.
- AssertedContext supplies interpretation context.
- ArgumentReasoning describes reasoning; it is not itself the proof or the asserted relationship.

The OMG issue tracker records an ambiguity between the prose describing AssertedInference sources and the machine-readable/profile-level type structure, and a diagrammatic ambiguity around ArgumentReasoning. This issue-tracker material is not a normative amendment. The mapping profile must preserve the native SACM 2.3 structure and record the ambiguity; it must not silently resolve it in GovCheck.

### 3.2 ReqIF 1.2 demonstrates why generic links must stay generic

ReqIF SpecRelation links SpecObject to SpecObject and carries a SpecRelationType. The OMG issue REQIF12-3 proposed source/target type constraints on SpecRelationType, but the proposal was taken out of scope because it would require a breaking XML schema change and impair interoperability. Consequently, a GovCheck importer cannot assume that a SpecRelation has typed semantic endpoints merely because a tool displays a label such as “derive”, “satisfy” or “refine”. The relation type's source-native definition and tool profile must be preserved.

### 3.3 SysML verification verdicts must remain distinct

SysML v2 distinguishes Pass, Fail, Inconclusive and Error as verification verdicts. GovCheck should preserve all four states and the verification context. Inconclusive is not Pass; Error is not evidence that the subject fails the requirement. A mapping to GovCheck's evaluation vocabulary needs an explicit conversion rule and must retain the original verdict.

## 4. Audit of candidate GovCheck relation families

| Candidate relation | Mapping status | Minimum obligation before operative use |
|---|---|---|
| derives | **Not one universal relation.** Distinguish logical/requirement derivation from PROV-O entity lineage. | Declare derivation kind, source/target types, rule/rationale, direction and whether a proof of the derived proposition is supplied. |
| refines | **Candidate only.** Similar labels across standards do not establish semantic refinement. | Define the refinement relation and profile; state preserved properties, assumptions, coverage domain and proof/testimony required. |
| supports | **Must be split by source semantics.** Argument support, evidential support and logical inference are different. | Retain relation subtype, evidence/claim endpoints, direction, source standard and whether support is merely asserted or independently assessed. |
| satisfies | **Claim, not evidence.** SysML satisfaction links are model assertions. | Identify requirement, subject, configuration, scope, criterion and method-appropriate evidence; keep decision separate. |
| verifies | **Method-qualified evidence relation.** A verification case and its verdict are distinct artifacts. | Record method, tool/version, subject, requirement/objective, assumptions, verdict and evidence digest. |
| assumes | **Source-role-sensitive.** Context, assumption, justification and accepted risk are not interchangeable. | Preserve source element type, owner, scope, rationale, review/expiry and any separate risk-acceptance decision. |
| wasDerivedFrom | **Provenance only.** | Keep within Entity/Activity/Agent lineage; never use it as a substitute for semantic derivation or proof. |
| justifies | **Candidate only.** A rationale relation does not itself authorize a decision. | Preserve rationale and evidence; require a separate authenticated authority decision where adoption/publication is involved. |

## 5. Required mapping-profile record

For each source-to-GovCheck relation mapping, require:

1. source standard, exact version, element/relation identifier and source-native definition;
2. source endpoint types, multiplicities, direction, constraints and relevant OCL/shape rules;
3. semantic force: asserted, normative, descriptive, observed, derived or proven;
4. candidate GovCheck relation and its domain/range, including partiality and coverage conditions;
5. mapping function, assumptions, information loss and round-trip behavior;
6. required evidence, proof obligations and the exact proposition/property being established;
7. positive, negative and counterexample fixtures bound to the exact source/profile version;
8. preservation of the original source payload and a report of unsupported/unmapped constructs;
9. separate authorization/adoption record if the mapping is made normative.

If a source relation's semantics are ambiguous or a mapping obligation is unproved, preserve the source-native relation and classify the GovCheck correspondence as candidate/unknown. Do not silently coerce it into an operative typed relation.

## 6. Relation to the Lean partial-mapping counterexample

Issue #210 records that a partial mapping can be vacuous when its declared domain is empty. The follow-on design must also account for composition: two non-empty partial domains may have an empty intersection, and a sound-directional first mapping does not necessarily provide a preimage for a witness in the second mapping's domain.

Therefore a future operative mapping profile must carry an inhabited-domain witness or a separately typed coverage claim, and composition must require an explicit witness for the composed domain. This is a proof obligation, not a property that can be inferred from two input mappings. The design options and regression requirements are recorded in #210; no Lean API change is adopted by this audit.

## 7. Disposition

- The PR #217 crosswalk remains a source-grounded research catalogue, not the canonical GovCheck metamodel.
- Source-native preservation is the default for all imported relations.
- Generic links (ReqIF SpecRelation, generic OSLC links) must not be assigned GovCheck semantics without a source-specific mapping profile.
- Argument/evidence relations (SACM, GSN) must not be promoted to proof or truth.
- Provenance relations (PROV-O) must not be conflated with semantic derivation/refinement.
- Model satisfaction/verification relations (SysML) must remain separate from evidence verdicts and authority decisions.
- Issue #73 remains open until relation-level mapping obligations and negative fixtures are complete. No ontology or standard is adopted by this report.

## 8. Sources

- [R-04 — GSN Community Standard v3](../references.md#r-04)
- [R-24 — W3C PROV](../references.md#r-24)
- [R-34 — SACM 2.3](../references.md#r-34)
- [R-73 — SACM 2.4 Beta](../references.md#r-73)
- [R-95 — SysML and ReqIF sources](../references.md#r-95)
- [R-102 — W3C PROV-O](../references.md#r-102)
- [R-234 — OSLC Core](../references.md#r-234) and [R-235 — OSLC Resource Shape](../references.md#r-235)
- [R-243 — SACM 2.3 open issue tracker](../references.md#r-243)
- [R-244 — ReqIF 1.2 source/target type issue](../references.md#r-244)
- [R-245 — SysML 2.1 requirement-satisfaction grammar issue](../references.md#r-245)
- [Issue #210 — Lean partial-mapping domain](https://github.com/Martin-PB/govcheck/issues/210)
