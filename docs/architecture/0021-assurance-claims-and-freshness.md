# 0021 — Assurance claims, arguments and evidence freshness

**Status:** proposed formal semantics for review; its presence does not make it an approved normative rule. It refines Specification 0005 and the governance metamodel in record 0013. **Français:** [0021](0021-assurance-claims-and-freshness.fr.md).

## 1. Purpose

Define the computable meaning of an assurance case: which claims are supported, by which evidence and assumptions; when evidence becomes unusable; how invalidation propagates through the argument; and when the case may support an acceptance decision.

The model does not turn a status into truth. It computes a status relative to a subject, declared dependencies, method, provenance and review authority. External truth and semantic adequacy remain separate questions.

## 2. Objects and relations

- **Claim:** a falsifiable, stable-identity proposition with subject, scope, normative source, admissible method, producer, reviewer, assumptions, limitations and falsification criteria.
- **Argument:** decomposition of a claim into subclaims and evidence. The initial composition is conjunctive: every required leaf must be supported. Alternative strategies (OR), weighting and probabilistic aggregation are outside this first model.
- **Evidence:** a method result, observation, attestation or derivation. Its outcome is distinct from admissibility, freshness and authenticity.
- **Dependency:** a versioned identity on which evidence relies: candidate/base, governance, specification, model, tool, configuration, environment, external source, identity or key, depending on the method.
- **Assumption:** a declared premise with source, owner, scope, validity and falsification conditions. An assumption is not evidence. The first TLA+ model does not yet compute its justification; this remains an explicit limitation.
- **Decision:** an act by a competent authority over an exact subject and a specific time/context.

Relations are typed and identified: decomposesInto, supportedBy, refutedBy, dependsOn, assumes, verifiedBy, reviewedBy, and supersedes. No relation is inferred from document proximity.

## 3. Argument graph

The subclaim graph must be acyclic. A claim cannot support itself, directly or through a cycle. Each claim has a transitive closure of required evidence: directly attached evidence plus evidence from every subclaim. The closure may be computed by the implementation or supplied by a verified index; it must be checked against the graph edges.

The initial composition is conservative:
- every required leaf is present;
- every required evidence item is current and favorable;
- no current refutation or contradiction is ignored;
- required assumptions are explicit and satisfied under an approved policy;
- every claim in the closure is explicitly reviewed by its designated authorized actor, distinct from its producer. The TLA+ ReviewClaim action records this review; evidence/dependency changes and expiry invalidate it.

A favorable result on one leaf does not make the whole argument favorable. Missing, unknown, not-run, unsupported or incomplete evidence never defaults to success.

## 4. Freshness: identity, dependencies and time

Freshness is not merely a maximum age. For evidence e, it depends at least on:

1. **Subject binding:** repository, base, candidate, native VCS state and target match the exact evaluated subject.
2. **Version binding:** for every declared dependency d, the revision observed by e is the current revision.
3. **Temporal validity:** the declared validity window has not expired, under an explicit clock and policy.
4. **Revocation:** neither the evidence nor a relevant identity, key or authority has been revoked.
5. **Integrity and provenance:** content and production chain are verifiable under declared trust assumptions.

The bounded model represents dependencies as versioned identifiers, expiry as a logical integer, and revocation explicitly. Signatures, producer trust, real clocks and VCS-binding proofs are outside this model.

Evidence may remain historically true while becoming unusable for a current decision. Invalidation does not delete the evidence or its former outcome: it changes admissibility for the current evaluation. Revalidation creates a new observation bound to current versions; it does not silently rewrite the old one.

## 5. Invalidation propagation

Changing a dependency makes evidence that declares it stale. The consequence propagates to every claim whose transitive closure contains that evidence. Affected reviews are invalidated too and must be repeated after publication/revalidation. Propagation is deterministic and transitive; it does not depend on manual intervention or claim display order.

Computed status precedence:
1. Conflict if current evidence contradicts or current evidence explicitly reports conflict;
2. Stale if any required evidence has expired, been revoked or is bound to an older version;
3. Refuted if current evidence refutes the claim;
4. Incomplete, Unsupported, NotRun or Unknown if required evidence cannot support a favorable conclusion;
5. Supported only if every required item is current and favorable and independent review is valid;
6. NotIndependentlyReviewed if evidence appears favorable but the independence requirement is not met.

A contradiction is not resolved by arbitrarily selecting the newest or most favorable evidence. Its resolution policy must be explicitly governed.

An acceptance decision is a snapshot. If a dependency, evidence item or its temporal validity later changes, the current decision is invalidated when that change affects the root claim's closure. History retains the former decision and its invalidation; it does not rewrite it.

## 6. Contract with the existing lifecycle model

govcheck.lifecycle remains responsible for phase, the (baseId, candidateId, governanceId, specId) tuple, approvals, acceptance and exact-candidate application. It already clears abstract evaluation/evidence on ChangeInputs, but it does not know individual evidence dependencies or the argument graph.

The new govcheck.assurance model is deliberately separate and composable:
- it computes the root claim status from the graph and evidence freshness;
- it permits assurance acceptance only while the root claim is Supported;
- changing a relevant dependency, revoking or republishing evidence, or expiry invalidates the acceptance snapshot;
- the lifecycle model should consume this result as a precondition to Accept, without merging native Git/Pijul identities or confusing approval with evidence.

The integration bridge to implement next is a refinement relation: Lifecycle.Accept is enabled only if Assurance.ClaimStatus(root) = Supported, and every claim dependency identity is included in the evaluation context. This proposal does not claim that this bridge already exists in the lifecycle module.

## 7. TLA+ assertions

formal/tla/GovCheckAssurance.tla and its bounded configuration check:

| Assertion | Meaning |
|---|---|
| TypeOK | Versions, statuses, clock, revocations and acceptance snapshot remain in their domains. |
| ArgumentGraphWellFormed | Subclaims strictly decrease in rank; closure contains direct and descendant evidence; dependencies match that closure. |
| ReviewBinding | Every recorded review belongs to an authorized reviewer distinct from the producer and still covers current favorable evidence. |
| ClaimStatusSoundness | A claim computed as Supported contains only current favorable evidence and all required reviews. |
| AcceptedImpliesSupported | A recorded acceptance implies that the root claim remains supported. |
| AcceptedDependencySnapshotCurrent | Relevant dependency versions have not changed since acceptance. |
| RevokedEvidenceNotCurrent | Revoked evidence cannot be considered current. |
| AcceptedDiscipline | Temporal property: every present acceptance remains supported in every reached state. |

The configuration contains one root claim, one subclaim, two evidence items and two dependencies. It explores ReviewClaim actions, version changes, publication/revalidation, revocation, expiry and acceptance. Reviewing the root claim also requires review of every subclaim. This bound is intended to find counterexamples in this abstraction; it does not prove production graph completeness or implementation conformance.

## 8. Limits and undecided choices

The model does not yet cover external source truth; cryptographic authenticity and key revocation; governed assumptions and waivers; alternative argument strategies; tool trust/independence; distributed clocks; concurrency among publication, revocation, acceptance and application; append-only history integrity; evidence confidentiality/retention; or refinement to real storage and evaluator behavior.

It selects no canonical format, ontology, policy engine or proof assistant. It creates no assurance tiers based on repository size.

## 9. Verification status

The module and configuration are proposed formal source artifacts. They must be parsed by SANY and explored by TLC with a pinned version. No SANY/TLC result is claimed by this proposal. Structural tests and source review do not replace TLC execution. Hosted CI is not triggered by this contribution; checks must be run according to maintainer authorization and repository instructions.

## Bibliographic references

- [R-05 — TLA+ and TLC state-transition modeling](../references.md#r-05)
- [R-09 — Open Policy Agent policy-decision engine](../references.md#r-09)
- [R-18 — Writ source-based assessment](../references.md#r-18)
- [R-22 — Native Git and Pijul semantics](../references.md#r-22)
