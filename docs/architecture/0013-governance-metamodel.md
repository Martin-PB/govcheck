# 0013 — Governance metamodel: goals, requirements, norms and assurance links

**Status:** conceptual metamodel proposed for review; no serialization or implementation is selected. **French:** [0013](0013-governance-metamodel.fr.md).

## Why a metamodel

Repository governance is more than shell commands and agent instructions. It expresses why a project exists, what it must achieve, which constraints apply, how its architecture is organized, what properties must hold and what evidence supports claims about the result.

The metamodel preserves distinctions between intent, obligation, property, implementation and evidence. Otherwise a failed check cannot be interpreted reliably.

## Core vocabulary

| Concept | Meaning | Not the same as |
|---|---|---|
| Goal/objective | Desired outcome or value | Executable check |
| Requirement | Statement the system/process must satisfy | Test or implementation task |
| Norm/rule | Directive with explicit deontic force and scope | Informal advice |
| Property | Predicate over states, traces, structures or behavior | Requirement prose alone |
| Contract | Assumptions, guarantees and obligations at a boundary | Global proof |
| Architecture element | Component, interface, trust boundary or relation | Requirement |
| Model | Abstraction with variables, transitions and assumptions | Implementation |
| Implementation artifact | Source, binary, configuration or deployed component | Proof of its own correctness |
| Check/method | Procedure examining a claim | The claim itself |
| Witness/evidence | Observation, artifact or derivation relevant to a claim | Truth merely because it exists |
| Claim | Precise proposition about subject and scope | Generic status badge |
| Argument | Reasoning from claims, assumptions and evidence | Test report alone |
| Decision/authority | Authorized resolution with provenance and scope | Contributor preference |

A requirement can refine into sub-requirements and link to properties. Properties are examined by methods; methods produce evidence; claims depend on evidence and assumptions. Relations are explicit, not inferred from document proximity or naming.

Decision records should make their reasoning inputs inspectable. The PEAK model provides one useful scaffold: Problem, Experience, Assumptions and Knowledge are recorded separately before a Solution and its Assumed Risk are recorded. The assumed-risk output should be linked to the relevant assumptions, observations and claims, with scope, rationale, accountable owner and review/expiry conditions. It is not itself authorization to accept the risk; acceptance remains a separate governed decision by the authorized principal. PEAK complements the metamodel's typed links between decisions, assumptions, claims and evidence; it is not a risk score or an assurance argument. Assumptions remain falsifiable and observations may challenge them. See [R-74](../references.md#r-74).

Do not collapse **PEAK Assumed Risk**, a **risk scenario**, a **risk assessment**, **risk treatment**, **residual risk** and **risk acceptance**. The assumed-risk output records what may not work as envisioned; an assessment is a separate method-bound analysis; treatment changes exposure; acceptance is an authorized disposition. Quantitative probability, fuzzy membership, nondeterminism, transition rates, costs and confidence also retain distinct semantics. See [R-193](../references.md#r-193) and the [decision/risk research clarification](../research/decision-and-assumed-risk-crosscutting-2026-11.md).

## Normative force

Distinguish obligation, prohibition, explicit permission, invariant/constraint, evidence requirement, process/approval requirement and non-binding recommendation. Absence of prohibition is not permission. A recommendation does not block acceptance. Defeasible rules require explicit priority/exception semantics; conflicts and unresolved precedence remain visible.

Deontic logic can formalize modalities such as obligation, permission and prohibition, but it does not supply the authority, scope, priority, delegation, exception, effective-time, evidence or enforcement semantics of a governance system. Access-control policy/model verification should separately examine consistency, completeness and safety properties before an evaluator or enforcement point is tested. See [R-93](../references.md#r-93) and [R-88](../references.md#r-88).

## Scope, refinement and realizability

Every object needs stable identity, evolution history, scope, provenance, owner/authority and typed relations. Applicability may depend on change type, affected components, threat class, deployment context, VCS capabilities or project profile. Profiles select obligations; they are not assurance tiers based on repository size.

Relations may include refines, derives-from, satisfies, constrains, conflicts-with, supersedes, depends-on, verified-by, evidenced-by and approved-by. Each relation needs defined semantics.

Consistency is not realizability: a logically consistent requirement set may still be impossible under resource, platform, timing or interface constraints. Analysis must distinguish contradiction, scope/precedence conflict, missing/circular refinement, infeasibility, underspecification and unsupported semantics.

The metamodel should accommodate goal-oriented requirements (including KAOS/GORE-style refinement and iStar 2.0 actor/goal modeling), deontic logic, temporal logic, predicate/relational logic and assume-guarantee contracts. These are conceptual families, not a commitment to one logic or toolchain. See [R-92](../references.md#r-92) for iStar.

## Assurance traceability graph and transversal decisions

A representative **traceability path** (not a mandatory lifecycle and not a decision sequence) is:

`Intent/Source → Goal/Need → Requirement/Norm → Property/Contract → Model → Implementation → Check/Method → Evidence/Witness → Claim → Argument`

Not every project needs identical granularity, and the graph is not required to be acyclic globally. Missing links, unjustified jumps, contradictions, unsupported mappings and circular support must be visible. Requirements may have multiple origins; decisions and evidence may relate to multiple nodes. A test unlinked to a claim does not establish project conformity. A formal property without an approved normative source is not automatically a project obligation.

**Decision is a transversal first-class object, not the final node of this path.** A decision may create, select, refine, justify, authorize, reject, constrain, suspend, supersede or revoke any node or relation: intent, goal, requirement, property, model, implementation, verification method, evidence/claim, assurance argument, exception, deployment or another decision. The graph must preserve the decision's authority, context, scope, rationale, alternatives, conditions, effective governance revision, provenance, temporal validity and review/revocation conditions. An acceptance decision is one particular decision kind that may follow an assurance assessment; it does not make decision-making a terminal stage.

Keep separate the evidence/assurance that supports a claim, the authority that may decide, and the decision actually made. A decision can accept incomplete assurance or residual exposure only if the missing evidence, assumptions, limitations and accepted risk remain explicit. Such a decision does not convert testimony into proof or make an uncertain scenario impossible.

The graph should answer both directions: why an artifact or rule exists and which decisions authorize or constrain it; which goals a property supports; which components are affected; which evidence supports/refutes a claim; what is unknown/stale/unsupported; and who authorized an exception or risk acceptance, for what scope, under which policy revision and until when.

## Interpretation pipeline

A future evaluator should: parse and canonicalize without ambiguous encodings/duplicate identities; resolve versions, references and authority; determine applicability; compose rules/profiles; detect conflicts, ambiguity and unsupported constructs; derive obligations/properties/evidence requirements; explain each result back to source rules; evaluate claims without treating absence as success; and apply acceptance only after mandatory conditions and authority checks.

This is a design target, not an implemented evaluator.

## Candidate GovCheck assurance requirements

The discussion identified four candidate tracking IDs. They are proposals, not approved rules:

- `GOV-ASSURANCE-001`: no normative rule is silently lost between approved source, canonical representation, evaluator semantics and controlled projections.
- `GOV-ASSURANCE-002`: every formal interpretation is traceable to its source, version, rationale and authorized approval.
- `GOV-ASSURANCE-003`: GovCheck correctness properties are formalized and verified within a declared scope and trust base.
- `GOV-ASSURANCE-004`: every conformity result has an independently reviewable assurance argument bound to the exact subject and relevant revisions.

Maintainers must adopt and register these IDs before they become binding rules.

## Open choices

Ontology vocabulary, serialization, graph representation, formal logic, query language, proof assistant and validation algorithm remain open. Prototype stable identity, typed relations, provenance, scope, composition, explanation traces and deterministic failure behavior before selecting a large ontology or proof stack.


## Bibliographic references

- [R-01 — NIST SP 800-53 security and privacy controls](../references.md#r-01)
- [R-09 — Open Policy Agent policy-decision engine](../references.md#r-09)
- [R-10 — Cedar authorization language](../references.md#r-10)
- [R-13 — JSON Schema structural contracts](../references.md#r-13)
- [R-44 — KAOS and goal-oriented requirements engineering](../references.md#r-44)
- [R-74 — PEAK project-decision model](../references.md#r-74)
- [R-193 — probabilistic, fuzzy and state-transition modelling](../references.md#r-193)
- [R-88 — NIST SP 800-192 access-control policy/model verification](../references.md#r-88)
- [R-92 — iStar 2.0 goal-oriented requirements modeling](../references.md#r-92)
- [R-93 — deontic logic and normative modalities](../references.md#r-93)
