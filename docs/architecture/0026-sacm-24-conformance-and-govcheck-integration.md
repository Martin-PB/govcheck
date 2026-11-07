# 0026 — SACM 2.4-conformant assurance capability and GovCheck integration

**Status:** architecture proposal for maintainer review. It establishes a target for semantic coverage and conformance; it does not claim that SACM 2.4, a parser, serializer or evaluator is implemented or formally conformant.  
**Language:** English is the default; see the [French counterpart](0026-sacm-24-conformance-and-govcheck-integration.fr.md).

## 1. Decision to be examined

GovCheck should be able to represent, preserve, validate and operate on the complete assurance-case semantics defined by the pinned SACM 2.4 Beta 1 specification, including its normative metamodel and its explicitly identified non-normative supporting constructs.

This is stronger than offering a lossy import/export adapter. The target is a **SACM-conformant assurance capability inside GovCheck**: every SACM concept, relationship, multiplicity, constraint, enumeration, package rule and supported view/diagram construct must have a faithful representation in GovCheck. GovCheck must also be able to express its own repository-governance concepts and connect them to SACM without forcing them into SACM classes that do not mean the same thing.

SACM 2.4 Beta 1 was adopted as an in-process OMG specification in September 2026; SACM 2.3 remains the formal version at the time of this record. The beta is therefore a pinned design target, not a claim that the final 2.4 standard is already formal. The normative PDF and machine-readable metamodel are published from the [OMG SACM specification page](https://www.omg.org/spec/SACM). The 2.4 change history is available in the [OMG issue tracker](https://issues.omg.org/issues/spec/SACM?view=CLOSED).

## 2. Architectural placement in GovCheck

SACM is a domain metamodel for structured assurance cases. GovCheck is the governance system for a software repository over its full lifecycle. These scopes are related but not interchangeable.

The proposed composition is:

1. **GovCheck canonical governance foundation** — project identity, authority, goals, requirements, normative rules, applicability, profiles, lifecycle, changes, approvals, exceptions, provenance, artifact identity and controlled projections.
2. **SACM-conformant assurance capability** — a faithful semantic submodel for SACM's Foundation, Argumentation, Artifact, Terminology, Packaging and applicable View/Diagram constructs, including the Beta 1 additions.
3. **GovCheck domain capabilities** — requirements, architecture, implementation, maintainability, tests, formal methods, dependencies, documentation, security, privacy, safety, build/release, operations and maintenance. Each capability can produce or consume assurance material without being reduced to an assurance case.
4. **Cross-model relations** — explicit, typed, versioned links between GovCheck concepts and SACM elements.

The canonical GovCheck model remains responsible for repository-wide governance and authority. The SACM capability is authoritative for the semantics of an assurance case represented as SACM. Neither replaces the other.

Do not make every GovCheck artifact an SACM Artifact, every requirement an SACM Claim, every finding an Assessment, or every decision an Argument. Map only where the meanings genuinely correspond; otherwise create an explicit GovCheck-side relation or extension with declared semantics.

## 3. Coverage requirement: no silent semantic subset

The conformance target is the complete pinned SACM 2.4 Beta 1 metamodel, not a hand-picked subset. The implementation plan must derive its inventory directly from the OMG normative machine-readable metamodel and specification, rather than relying only on this summary.

At minimum, the coverage audit must account for:

### 3.1 Foundation and common modeling semantics

- SACM model and element identity, ownership, containment, namespace and package membership;
- common base classes, abstractness, inheritance and redefinitions;
- association ends, direction, ownership, multiplicities, ordering, uniqueness, subsets and unions;
- constraints and their evaluation/validation semantics;
- names, values, comments, constraints, external references and language-aware expressions;
- explicit model identity and model-level organization.

SACM 2.4's Foundation and MOF-alignment work is material: the implementation must preserve the actual association and ownership semantics, not merely serialize class names and edges.

### 3.2 Argumentation

Represent the complete normative Argumentation package, including the SACM claim/assertion, argument, reasoning, inference, evidence, context, relationship, citation/abstraction, defeater and other constructs exactly as defined by the pinned metamodel.

Preserve:
- asserted versus inferred relationships and their exact direction/meaning;
- claim subjects and the explicit subject mechanism introduced in 2.4;
- argument context and the additional non-normative context support;
- reasoning names and values as distinct where the model permits;
- inference type and declared logic/notation;
- defeaters, defeation mechanisms/rules and unresolved objections;
- evidence/context references and their relationship semantics;
- advanced argument descriptors, including strength, truth-value and undecidability concepts, while retaining their non-normative status where specified.

Do not replace SACM argument semantics with GovCheck 0021's current simplified conjunctive claim graph. GovCheck's evaluator may impose a particular acceptance policy, but the underlying assurance model must preserve the richer SACM graph and logic without loss.

### 3.3 Artifact

Represent the full Artifact package and its lifecycle/provenance constructs, including artifacts, artifact references, events, activities, techniques, participants, resources and artifact-asset relationships as specified.

Preserve exact external/internal reference targets, relevant locations within external artifacts, dates and temporal information, artifact relationships and the distinction between an artifact and an assertion/evidence item about it.

A repository file, Git/Pijul revision, test run, proof object, build, release, dependency, deployed component or observation may be referenced as a GovCheck subject. It must not be coerced into an Artifact subclass if the semantics do not fit. A typed binding maps its stable GovCheck identity and immutable revision/instance identity to the corresponding SACM reference.

### 3.4 Terminology

Represent terminology assets, categories, terms, definitions, relationships and language-aware values. Preserve language tags and structured expression values. GovCheck's own vocabulary and domain-specific glossaries may link to SACM terminology assets, but must not silently redefine them.

### 3.5 Packaging, modularity and reuse

Preserve SACM model/package identity, package kinds, ownership, imports/dependencies, interfaces and bindings, and all package constraints in 2.4. The package refactoring and removal/renaming of 2.3 constructs must be reflected exactly; do not carry forward obsolete 2.3 packaging semantics as if they were 2.4.

### 3.6 Assessments, joins, advanced arguments, views and diagrams

The 2.4 beta includes additional constructs/issues for:
- **Assessment**, including assessment identity, nested assessments, rules and gaps;
- **Join**, including declared join type/rule and source-selection semantics;
- **advanced argument support**, including argument strengths, inference kinds, truth values and undecidability;
- **SACM views and diagrams**, including diagram/diagram-element structures and visual information.

The OMG issue dispositions identify some of these as non-normative supporting constructs. GovCheck must preserve their status metadata and must not silently promote them into normative requirements or normative metamodel obligations. Where the specification's conformance clause distinguishes normative and non-normative elements, GovCheck must implement and report those conformance points separately.

## 4. GovCheck-to-SACM integration contract

The integration should be based on explicit mappings and stable cross-identities, not class-name similarity.

| GovCheck concern | SACM relation | Integration rule |
|---|---|---|
| Goal, stakeholder need, project outcome | Often context or referenced artifact; sometimes subject of a claim | Keep the GovCheck goal as the canonical project-governance object; link to SACM context/claim subject where justified. |
| Requirement, norm, policy obligation | May be claim subject, context or referenced artifact | A requirement is not automatically a claim. Preserve normative force and authority in GovCheck. |
| Property, contract, invariant, model | Usually referenced artifacts and/or claim subjects | Preserve exact specification/model revision and scope. |
| Source, configuration, build, test, proof, release, deployment | SACM Artifact/ArtifactReference/ArtifactAssetRelationship as appropriate | Bind to stable GovCheck artifact ID plus immutable revision or execution ID. |
| Observation, test result, attestation, proof result | May be AssertedEvidence or referenced artifact depending on semantics | Preserve producer, method, provenance, scope, outcome, time, limitations and invalidation dependencies in GovCheck. |
| Assurance claim and argument | Direct SACM mapping | Preserve complete SACM structure and logic. |
| Assumption, context, defeater, counterevidence | SACM context/argumentation constructs where semantically appropriate | Keep source, owner, validity, uncertainty and review/falsification semantics explicit. |
| PEAK decision record | Related GovCheck decision, not a SACM replacement | Link relevant assurance cases and SACM elements; do not model PEAK as a SACM argument by default. |
| Authorization, approval, exception, acceptance | GovCheck authority/lifecycle semantics | SACM evidence or claims can inform the decision; they do not themselves grant repository authority. |
| Repository change, candidate, VCS state | GovCheck lifecycle subject and SACM referenced artifact | Bind assurance case and its assessments to the exact candidate and governance revision. |

Each mapping must state: source/target metaclasses; cardinality; direction; identity mapping; semantic preservation; allowed loss (normally none for SACM-native constructs); validation rules; version applicability; and provenance.

## 5. Two complementary identity and version axes

GovCheck must preserve both:
- the stable GovCheck logical identity, immutable revision/instance identity and optional contract version (Architecture 0017);
- the SACM model/package/element identity and the exact SACM metamodel version/profile.

An imported SACM element must retain its original identifier and source model identity. A GovCheck element linked to it must not overwrite or impersonate that identity. Revisions, migrations, supersession and external references must be explicit.

The target is lossless round-trip for the pinned SACM version:
`SACM model → GovCheck representation → SACM model`
must preserve every normative SACM element, relationship, value, multiplicity, constraint, package, supported diagram/view and extension status. Serialization ordering or formatting may be canonicalized only where the specification permits it; semantic content and stable identities must remain unchanged.

Unknown future SACM elements or extensions must be preserved as opaque, typed, versioned content or cause an explicit unsupported/indeterminate result. They must never be silently discarded.

## 6. Relationship with existing GovCheck assurance semantics

Specification 0005 and Architecture 0021 already define important GovCheck constraints: exact subject binding, method and scope, provenance, assumptions, limitations, evidence freshness, dependency invalidation, review and acceptance discipline.

These remain valid GovCheck requirements. However, Architecture 0021's initial TLA+ abstraction currently uses a finite acyclic claim graph, conjunctive evidence composition and a limited status vocabulary. It explicitly excludes alternative argument strategies and other advanced constructs. That abstraction is not the canonical representation of all SACM arguments.

Required evolution:
1. retain 0021's freshness, subject-binding, invalidation and authorized-review responsibilities;
2. replace the assumption that its conjunctive graph is the complete assurance argument model with a projection/evaluation profile over the richer SACM-conformant structure;
3. define policy-specific evaluation semantics for AND/OR/XOR, joins, defeaters, assessments, inference kinds and strengths without pretending that all logics reduce to one Boolean status;
4. keep raw SACM model semantics separate from any GovCheck assessment/acceptance policy;
5. refine the TLA+ model incrementally, preserving explicit bounds and stating which SACM constructs are abstracted or outside each model.

A claim status is a governed assessment relative to a policy, subject, scope, model revision, evidence and assumptions—not an intrinsic truth value supplied by SACM or GovCheck.

## 7. Conformance and verification strategy

Conformance must be demonstrated, not asserted because a JSON document resembles SACM.

### 7.1 Normative metamodel conformance

- Pin the exact OMG 2.4 Beta 1 PDF, machine-readable metamodel and UML profile artifacts by version and digest.
- Generate a complete metaclass/enum/association/constraint inventory from the normative machine-readable model.
- Check every class, superclass, property, association end, multiplicity, ordering/uniqueness constraint, subset/redefinition, enum literal, package rule and OCL constraint.
- Check model/package/interface/binding constraints and required identifiers.
- Keep normative conformance points separate from non-normative supporting constructs.

### 7.2 Serialization and round-trip

- Import representative valid SACM models and reject or explicitly classify invalid ones.
- Export GovCheck-native assurance cases to SACM where the mapping is defined.
- Require lossless round-trip for all SACM-native constructs.
- Preserve unknown extensions, external references, multilingual values and view/diagram metadata.
- Test 2.3-to-2.4 migration against the OMG Annex G guidance; preserve original source and migration provenance.

### 7.3 Semantic and cross-domain validation

- Test that GovCheck links to requirements, repository revisions, test executions, proof objects and decisions do not alter SACM semantics.
- Test that a requirement is not automatically converted into a claim, a check result is not automatically accepted as evidence, and an assurance assessment is not an authorization.
- Test argument cycles, unsupported inference semantics, defeaters, contradictory evidence, missing context, stale references, unresolved subjects and incomplete models.
- Verify that the evaluation policy identifies unsupported or indeterminate cases instead of silently simplifying them.

### 7.4 Conformance report

A conformance report must identify exact SACM version/digests, GovCheck model/evaluator revision, covered metaclasses and constraints, excluded/unsupported constructs, test corpus, round-trip results, migration results, known semantic deviations and reviewer/authority. It must not say “SACM conformant” while any required normative construct is unimplemented or lossy.

## 8. Version strategy

- Treat **SACM 2.4 Beta 1 (September 2026)** as a pinned engineering target for the prototype.
- Keep SACM 2.3 import compatibility and a documented 2.3-to-2.4 migration path where useful.
- Track changes until SACM 2.4 becomes formal. Do not silently track a moving beta URL.
- When the final 2.4 release appears, compare its machine-readable metamodel and conformance clauses with the pinned beta, produce an explicit migration/impact report, and update the supported profile only through an authorized change.
- Preserve the distinction between normative SACM elements and non-normative supporting additions.

## 9. Staged work

1. **Metamodel inventory:** derive the full 2.4 Beta 1 coverage matrix from OMG XMI/PDF; classify normative and non-normative constructs.
2. **Semantic mapping:** map every SACM metaclass and relation to GovCheck's assurance capability or a lossless dedicated submodel; identify cross-links to 0002, 0005, 0013, 0017 and 0021.
3. **Conformance profile:** specify identity, serialization, version pinning, constraints, unknown-extension behavior and conformance report.
4. **Prototype:** parser/serializer and lossless round-trip corpus; no mandatory graph database or hosted service.
5. **Formal integration:** revise the assurance abstraction and TLA+ properties to cover selected argument-composition and invalidation semantics; explicitly scope each abstraction.
6. **Review and adoption:** human review of the semantic coverage matrix and implementation evidence before any normative conformance claim.

## 10. Decisions deliberately not made

This record does not select a graph database, mandate UML tooling, require every GovCheck project to author SACM cases, make SACM the repository-wide governance metamodel, replace GovCheck authority/lifecycle/requirements semantics, or claim current implementation conformance. It does establish complete SACM 2.4 Beta 1 expressibility and preservation as the target for GovCheck's assurance capability.

## 11. Primary sources

- [OMG SACM specification catalogue, including SACM 2.4 Beta 1 and machine-readable metamodel](https://www.omg.org/spec/SACM).
- [OMG SACM 2.4 issue tracker — closed issues and dispositions](https://issues.omg.org/issues/spec/SACM?view=CLOSED).
- [OMG SACM 2.4 issue tracker — all issues](https://issues.omg.org/issues/spec/SACM?view=ALL).
- [OMG SACM 2.3 formal specification](https://www.omg.org/spec/SACM/2.3).

## 12. Relationship to existing GovCheck records

This record refines, but does not supersede:
- Specification 0002 — canonical governance authority and composition;
- Specification 0005 — assurance vocabulary, method classes, evidence and trust;
- Architecture 0013 — repository-wide goals/requirements/norms/properties/assurance metamodel;
- Architecture 0017 — stable identity, revisions and provenance;
- Architecture 0021 — freshness, invalidation and acceptance discipline;
- Architecture 0024 — project bootstrap and selectable domain capabilities;
- Architecture 0025 — lifecycle observations and PEAK decision traceability.

The SACM capability must remain connected to all these foundations without absorbing their distinct responsibilities.
