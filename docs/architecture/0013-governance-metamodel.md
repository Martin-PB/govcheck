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

## Normative force

Distinguish obligation, prohibition, explicit permission, invariant/constraint, evidence requirement, process/approval requirement and non-binding recommendation. Absence of prohibition is not permission. A recommendation does not block acceptance. Defeasible rules require explicit priority/exception semantics; conflicts and unresolved precedence remain visible.

## Scope, refinement and realizability

Every object needs stable identity, evolution history, scope, provenance, owner/authority and typed relations. Applicability may depend on change type, affected components, threat class, deployment context, VCS capabilities or project profile. Profiles select obligations; they are not assurance tiers based on repository size.

Relations may include refines, derives-from, satisfies, constrains, conflicts-with, supersedes, depends-on, verified-by, evidenced-by and approved-by. Each relation needs defined semantics.

Consistency is not realizability: a logically consistent requirement set may still be impossible under resource, platform, timing or interface constraints. Analysis must distinguish contradiction, scope/precedence conflict, missing/circular refinement, infeasibility, underspecification and unsupported semantics.

The metamodel should accommodate goal-oriented requirements (including KAOS/GORE-style refinement), deontic logic, temporal logic, predicate/relational logic and assume-guarantee contracts. These are conceptual families, not a commitment to one logic or toolchain.

## Assurance traceability graph

A representative chain is:

`Decision/Authority → Goal → Requirement/Norm → Property/Contract → Model → Implementation → Check/Method → Evidence/Witness → Claim → Argument → Acceptance decision`

Not every project needs identical granularity, but missing links, unjustified jumps and circular support must be visible. A requirement without a verification strategy remains visible. A test unlinked to a claim does not prove project conformity. A formal property without an approved normative source is not automatically a project obligation.

The graph should answer both directions: why a rule exists and who authorized it; which goals a property supports; which components are affected; which evidence supports/refutes a claim; what is unknown/stale/unsupported; and who authorized an exception, for what scope and expiry.

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

External references used in this record: [R-01 — NIST SP 800-53 security and privacy controls](../references.md#r-01), [R-09 — Open Policy Agent policy-decision engine](../references.md#r-09), [R-10 — Cedar authorization language](../references.md#r-10), [R-13 — JSON Schema structural contracts](../references.md#r-13).