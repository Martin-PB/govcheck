# STUDY-004 — Multi-disciplinary specifications, plural viewpoints and formal deliberation

**Status:** research and design direction to investigate. This record is not an architecture decision, an adopted requirement or authorization to implement.

## 1. Origin and intent

This dossier faithfully preserves the direction expressed in the 11 November 2026 conversation: a GovCheck-governed repository should be able to receive specifications from different sources, disciplines and business domains, preserve their meaning and provenance, and provide a formal, computable way to relate those specifications — including where their concepts, definitions, scopes or claims diverge or contradict one another.

The goal is not to force semantic convergence or prematurely manufacture a common vocabulary. It is to give the participating domains structured, traceable and analyzable material for discussion, to understand the consequences of divergences, and to enable an informed decision by the competent authority. Once a decision is made, its authorized consequences can be translated into requirements, target specifications, design decisions and implementation work, with explicit lineage back to the sources and arbitration.

The motivating example is the vocabulary of “prospect”, “customer”, “opportunity”, “account” and “third party”: these may denote partially overlapping or different realities in marketing, sales, contract management and accounting. Conversely, the same object or actor may be named differently by different disciplines. Such differences are not necessarily errors; they may reflect distinct purposes, decompositions, temporalities, responsibilities or scopes.

## 2. Central direction to investigate

> GovCheck should enable heterogeneous specifications to be ingested, preserved, structured, related and confronted, providing formal, traceable and computable material for stakeholder deliberation and decisions by the competent authority. Adopted decisions should then be transformable into requirements, specifications and implementation work while preserving their lineage to the source specifications and the arbitrations from which they result.

This is a proposed capability to investigate, not an already adopted decision.

## 3. Envisaged functional lifecycle

### 3.1 Ingesting diverse sources

Potential sources include business-domain documents, regulatory and normative requirements, contracts, conventions, data models, ontologies, processes, functional and technical specifications, external-tool documents and stakeholder contributions.

Ingestion should distinguish and preserve:
- the original source, identity, provenance, author/issuer, authority and version;
- extracted or imported content;
- the structured representation created in GovCheck;
- transformations, normalizations and interpretations applied;
- information that was lost, ambiguous, not understood or not represented;
- links between every structured element and its location in the source.

Cautionary principle: ingestion must not silently discard information or present automated interpretation as domain validation. Preservation of source documents and traceability of transformations require investigation, including for non-text formats and changing sources.

### 3.2 Preserving context and viewpoint

Depending on the specification, useful context may include:
- business domain, discipline, community or function;
- author, producer, sponsor and approving authority;
- purpose, concerns and decisions it is intended to support;
- scope, population, objects, processes and temporal context;
- vocabulary, definitions, conventions and units;
- assumptions, constraints, exclusions and validity limits;
- status, version, effective date and relationships to earlier versions.

These are research dimensions, not mandatory metadata for every document. A viewpoint should not be reduced to its author's identity: it may be collective, institutional, disciplinary, situated or contested.

### 3.3 Structuring without merging

The tooling should represent meaningful elements of specifications without requiring all of them to be immediately converted into one canonical model. Source formulations and concepts should be preservable alongside structured representations and explicit interpretations.

Different disciplines may decompose the same reality differently. The problem is therefore not always synonym alignment: objects, events, roles, states, boundaries and identity criteria may themselves differ.

### 3.4 Relating and analyzing specifications

Candidate relations to investigate, not to adopt as normative vocabulary:
- identity or declared equivalence within an explicit context;
- exact or partial correspondence;
- proximity, overlap or intersection;
- specialization and generalization;
- translation or projection from one concept into another vocabulary;
- dependency, presupposition or derivation;
- complementarity;
- differences of scope, temporality or purpose;
- incompatibility, contradiction or conflict;
- no known correspondence, ambiguity or undetermined relation.

Business-domain translation must be more than a synonym table. A translation may be partial, asymmetric, conditional and context-dependent. It may need to state source and target concepts, validity context, preserved elements, losses or refinements, assumptions, transformation rules, provenance and the authority that validated it.

At minimum, distinguish:
- same term, different meanings;
- different terms, same or partially shared reality/concept;
- overlapping concepts that are not equivalent;
- different decompositions of the domain;
- logical contradiction under identical assumptions and scopes;
- apparent divergence caused by different contexts, temporalities or purposes.

### 3.5 Formal and computable material for deliberation

Relations and divergences should be able to feed, as appropriate, concept and dependency graphs, correspondence matrices, coverage analyses, sets of incompatible claims, assumptions, consequences, gaps and unresolved questions.

Automated processing may detect candidate correspondences, inconsistencies, dependencies or conflicts. It must expose the rules, assumptions, versions, limits and supporting material behind its results.

Critical distinction: a computed conflict is not yet a qualified business-domain conflict; a contradiction detected under one interpretation does not show that the sources are globally incompatible; failure to detect a conflict does not prove complete consistency. Computation prepares and informs discussion; it does not replace domain judgment.

### 3.6 Deliberation, authority and decision

Stakeholders should be able to examine source specifications, correspondences, divergences, arguments, consequences and uncertainties. Disagreements must not be automatically erased or all treated as defects.

A decision record should preserve:
- the competent authority, its mandate and scope of competence;
- stakeholders consulted and positions expressed;
- sources, versions, evidence and analyses considered;
- interpretations and assumptions selected;
- options, consequences and trade-offs considered;
- rejected options and reasons;
- accepted risks, conditions and limits;
- disagreements or questions left open;
- whether the decision is conditional, temporary, revisable or final.

A decision does not retroactively rewrite source documents or necessarily declare a discipline wrong. It establishes what is authorized or selected within a given governance context.

### 3.7 Derivation into implementation and assurance

An adopted decision may lead to requirements, target specifications, business rules, interface contracts, models, architecture decisions and implementation work. These artifacts need not be produced in one step and are not identical to the decision.

Lineage must remain navigable: derived artifact → decision → arbitration and arguments → analyses and relations → source specifications and versions. Verification and assurance evidence must state which interpretations, requirements, scopes and assumptions they cover. A passing test for one interpretation of “customer” does not automatically establish another interpretation.

## 4. Two related spaces that must not be conflated

The direction suggests distinguishing analytically:

1. **Plurality and confrontation space:** original sources, imported specifications, viewpoints, vocabularies, interpretations, alignments, divergences, contradictions, analyses and deliberations.
2. **Governance and realization space:** authorities, adopted decisions, derived requirements and specifications, work, implementations and assurance.

They must be strongly linked but not merged. An ingested source is not automatically adopted; a computed correspondence is not automatically validated; a detected conflict is not automatically non-conformance; a decision is not proof of successful implementation.

This separation is an architectural hypothesis to investigate, not a decided structure.

## 5. Cautionary principles and limits

- Do not impose a universal ontology or default semantic convergence.
- Do not conflate term, concept, domain object, representation and identifier.
- Do not equate translation, correspondence, equivalence and identity.
- Do not conflate logical inconsistency, business disagreement, scope difference and governance conflict.
- Do not let an algorithm decide the legitimacy of a viewpoint or the authority of an arbitration.
- Do not turn an ingested specification into an approved requirement.
- Do not lose source formulations, provenance, versions or applied transformations.
- Do not claim that a formal model exhausts the real domain.
- Do not turn GovCheck into a universal ontology-modelling or business-facilitation tool: it may govern sources, relations, translations, decisions and assurance while relying on specialist tools where appropriate.

## 6. Research questions

1. Which formats and ingestion mechanisms support faithful preservation, structured extraction and traceability of transformations?
2. Which existing structures adequately represent viewpoint, concern, context, specification, vocabulary and authority?
3. How can multiple domain models and semantic decompositions coexist without reduction to one canonical model?
4. Which formalisms express exact, partial, contextual, asymmetric and contestable alignments?
5. How should equivalence, implication, compatibility, contradiction, overlap and absence of correspondence be distinguished formally?
6. How can contradictions be detected without false positives caused by context, time, modality or scope differences?
7. How can every computed result be tied to its rules, assumptions, versions, evidence and limits?
8. How should business-domain translations be validated and evolved under governance?
9. How can multi-party deliberation be organized, disagreements preserved and decisions linked to the competent authority?
10. How can decisions produce realization artifacts without losing lineage to sources and arbitrations?
11. How does this capability relate to the existing metamodel, requirements, intentions, objectives, decisions, models, arguments, claims and assurance?
12. Which capabilities belong in GovCheck, exchange formats, specialist tools or external organizational processes?
13. What applicability conditions, prerequisites and limits should GovCheck explain to organizations with multiple disciplines or heterogeneous specifications?

## 7. Research families to examine

The study should compare at least:
- Domain-Driven Design, bounded contexts, context mapping and translations between models;
- architecture viewpoints/views and stakeholder concerns;
- metadata registries and data semantics (including ISO/IEC 11179);
- ontology alignment, SKOS, OWL and the limits of these formalisms;
- plural conceptual models and deliberation (including Soft Systems Methodology);
- multi-stakeholder requirements, goal-oriented requirements and conflict management;
- SACM and structured argumentation for linking claims, arguments, evidence and decisions;
- specification formats and domain standards, including provenance, versioning and evolution mechanisms.

References R-187 to R-192 are bibliographic leads to verify and investigate; their inclusion is neither adoption nor proof that they satisfy all needs.

## 8. Relationships to other studies

- **STUDY-003** provides the epistemological context: plural viewpoints, model limits, irreducibility and situated validity. STUDY-004 turns these questions into a capability hypothesis for ingestion, relating specifications and deliberation.
- **STUDY-001** informs quality, testing, TDD and development assurance.
- **STUDY-002** informs applicability, enforcement boundaries and external prerequisites.
- Existing research on ontologies, semantic interoperability, metamodel coherence and SACM must be revisited; STUDY-004 should not duplicate its results but identify what is missing for the complete lifecycle described here.

## 9. Status and decision discipline

- This study records an important direction expressed by the user; it is not a formal adoption decision.
- No new metamodel concept, canonical format, language, reasoning engine or alignment tool is adopted.
- This dossier creates no implementation work.
- Any subsequent decision must cite STUDY-004 and exact R-entries, explain options and counterarguments, applicability limits, the competent authority and consequences for the existing model.
- The central research success criterion is to enable formal and computable confrontation without artificial semantic convergence, while preserving lineage among sources, deliberation, decision, realization and assurance.

## References

Central catalogue: [R-187](../references.md#r-187) · [R-188](../references.md#r-188) · [R-189](../references.md#r-189) · [R-190](../references.md#r-190) · [R-191](../references.md#r-191) · [R-192](../references.md#r-192). Also see [R-51](../references.md#r-51)–[R-61](../references.md#r-61), [R-83](../references.md#r-83)–[R-86](../references.md#r-86), [R-115](../references.md#r-115)–[R-127](../references.md#r-127) and [R-178](../references.md#r-178)–[R-182](../references.md#r-182).
