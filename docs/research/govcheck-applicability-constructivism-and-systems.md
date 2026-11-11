# GovCheck applicability research: constructivism, irreducibility and systemic modelling

**Research ID:** STUDY-003-APP  
**Status:** provisional cross-source applicability assessment; non-normative. No product capability is claimed implemented and no metamodel change is adopted.

## Purpose

This note translates the three sessions in [STUDY-003](le-moigne-colloquium.md) into questions about GovCheck's suitability and limits. It does not turn the colloquium into a product specification. The distinction is between (1) what the research suggests, (2) what the repository governance tool could plausibly support, (3) what requires other methods or external evidence, and (4) what remains an open design question.

## Preliminary fit assessment

### Where GovCheck may be a good fit

GovCheck's intended repository-governance role is relevant when a project needs to make explicit and traceable:

- the purposes and viewpoints behind intentions, objectives, requirements, models and decisions;
- the scope, assumptions, boundaries, exclusions and dependencies of a governance or assurance model;
- the relationship between models, claims, arguments, evidence, verification results and authorized decisions;
- changes to models and assumptions over time, including the impact on prior evidence;
- unresolved uncertainty, known unknowns, unmodelled interactions and accepted residual risk;
- multiple partial models for different concerns, without assuming one representation is exhaustive.

These are candidate areas of fit based on the existing intended product direction. They are not statements that all such capabilities are implemented today.

### Where GovCheck may help, but cannot be sufficient alone

Some needs require complementary approaches:

- **Stakeholder inquiry and deliberation:** a repository can preserve viewpoints, decisions and traceability, but cannot itself facilitate difficult conversations or ensure meaningful participation. Methods such as SSM or collaborative research may be needed.
- **Domain/system modelling:** GovCheck may govern model identity, assumptions, scope, review and evidence; specialist tools and domain expertise may be needed to construct and validate substantive models.
- **Empirical adequacy:** tests, observations, field studies, operational measurements and expert assessment are needed to assess whether a model fits the phenomenon for its intended use.
- **Complexity and uncertainty assessment:** the project must identify which form of uncertainty or irreducibility matters. A generic “complexity” label is insufficient.
- **Formal verification:** proof and model-checking can validate precise formal claims under declared assumptions; they do not by themselves validate the abstraction, its boundary, the legitimacy of the purpose or the truth of external assumptions.

### Where GovCheck alone is a poor fit

GovCheck must not be sold as sufficient when the actual need is to:

- produce a complete or final representation of reality;
- resolve stakeholder disagreement without a deliberative process;
- guarantee that all emergent interactions or unknown unknowns have been modelled;
- replace scientific/domain expertise or empirical observation;
- prove that a formal model is a faithful representation of a socio-technical system;
- convert an uncertain or contested judgment into an objective fact merely by recording it.

The correct product explanation should identify the part GovCheck can support, the complementary methods/evidence needed, the remaining uncertainty and the authority responsible for accepting risk.

## Candidate audit against existing GovCheck concepts

This mapping is deliberately a research checklist, not a new ontology.

| Conceptual concern | Existing GovCheck areas to inspect | Audit question |
|---|---|---|
| Purpose, viewpoint, observer | intention, objective, stakeholder/authority, decision | Can viewpoint and intended use be explicit without confusing a claim author with its decision authority? |
| Model identity and scope | artifact identity/revision, applicability, specification | Can a model declare version, scope, exclusions, environment and intended context? |
| Assumptions and uncertainty | assurance model, claims/arguments, risk | Can assumptions, unknowns, uncertainty type and accepted limitations be represented distinctly? |
| Model validity | verification method, evidence, assurance claim | Can formal consistency be distinguished from empirical/pragmatic adequacy? |
| Plural models | concern-scoped models, linked artifacts, applicability | Can several models address different aspects without forced unification? |
| Evolution and feedback | change lifecycle, evidence freshness, revision applicability | Can model changes invalidate or require review of dependent evidence and decisions? |
| Irreducibility | risk/assumption/limitation/exception concepts | Can irreducible elements be recorded without creating a vague “complexity score”? |
| Deliberation and legitimacy | authority, review, decision, argument | Can GovCheck preserve who participated, who decided and under which mandate? |

## User-facing explanation candidate

> GovCheck is intended for projects that need explicit, traceable governance of repository changes, requirements, decisions, models and assurance evidence. It can help make assumptions, model boundaries, responsibilities and unresolved risks visible. It does not replace domain expertise, stakeholder deliberation, empirical validation or specialist systems-modelling tools. Formal verification can establish properties of a defined model under stated assumptions; it does not alone prove that the model fully represents the real system. Depending on the project, GovCheck may therefore be a central governance layer, a useful complement to other methods, or insufficient as a standalone solution.

This wording is a research candidate only. It must be reviewed against the implemented product scope before publication as product documentation.

## Questions for later decision

1. Should viewpoint/purpose/context be first-class concepts, or can they be represented through existing metadata and relationships?
2. What is the minimum information required to state a model's validity context?
3. How should model evolution affect evidence freshness and prior decisions?
4. Should GovCheck support links to external systemic models, rather than trying to become a systemic-modelling environment?
5. How should the tool distinguish epistemic uncertainty, stochastic uncertainty, computational limits, unknown dependencies and uncontrollability?
6. What evidence is sufficient to claim a model is fit for a particular decision?
7. What mechanisms ensure that multiple stakeholder perspectives remain visible without making all conflicting claims equally authoritative?

## Decision status

No decision is made here. No issue or implementation task is created by this research alone. Future decisions should cite STUDY-003 and the relevant R-166–R-182 sources, record counterarguments and identify the authorized decision-maker.
