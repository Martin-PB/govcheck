# 0017 — Artifact identity, revision and versioning policy

**Status:** proposed governance policy for maintainer review. It does not adopt SemVer globally, select a canonical serialization, or claim that versioning controls are implemented.  
**Language:** English is the default; the French counterpart is [0017 (français)](0017-artifact-identity-revision-and-versioning.fr.md).  
**Scope:** all governed artifacts and records in GovCheck, including normative, architectural, formal, implementation, evidence, decision and publication artifacts.

## 1. Purpose and governing principle

GovCheck must distinguish three questions that are often collapsed into one:

1. **Identity:** which logical thing is this?
2. **Revision or instance identity:** which exact immutable state or occurrence is this?
3. **Compatibility version:** what compatibility promise, if any, does this published artifact make to identified consumers?

A version number cannot answer all three questions. A Git commit, content digest, stable `artifactId`, SemVer string, execution identifier and provenance record are complementary identifiers, not alternatives.

**SemVer is a compatibility vocabulary, not a universal identity scheme and not a measure of importance, maturity, correctness or approval.** It is applicable only where an artifact exposes a declared contract to identifiable consumers and the project can define backward compatibility for that contract. Where that test fails, GovCheck MUST use stable logical identity, immutable revisions/instances and explicit provenance instead of inventing MAJOR.MINOR.PATCH semantics.

This document is a policy proposal. It does not itself make a proposed contract binding. Adoption requires an authorized governance decision and any required update to the canonical governance model.

## 2. Terms and distinct identity axes

| Term | Meaning | Typical representation | Mutability |
|---|---|---|---|
| Logical artifact identity | The continuing identity of an artifact across revisions and path changes | Stable `artifactId` | Stable; never recycled |
| Revision identity | One exact content/state revision of a logical artifact | Git commit/tree plus path and content digest; or native VCS identity | Immutable once published |
| Contract version | A compatibility label for a declared public contract | SemVer `MAJOR.MINOR.PATCH`, only when justified | Immutable once released |
| Release identity | One published repository/package release | Release tag plus exact commit/tree and manifest | Immutable |
| Instance/event identity | One execution, observation, approval, decision or other occurrence | Unique event/run/record ID plus timestamp and subject binding | Immutable; corrections are new events |
| Provenance | The entities, activities, agents, inputs and derivations behind an artifact/result | Typed relations and evidence metadata | Append-only history; corrections are explicit |

A logical artifact may have many revisions. A contract may have many releases. One release may contain many artifacts, each with its own identity and revision. A test definition may be versioned while each test execution is a separate instance. A proof object may be revised while its theorem statement remains unchanged. These relations MUST NOT be flattened into one version string.

### 2.1 Stable IDs and immutable revisions

- Every governed logical artifact SHOULD have a stable identifier independent of filename, directory, branch, tag or hosting provider.
- An identifier MUST NOT be reused for a different logical artifact. Retirement, replacement and splitting/merging require explicit relations such as `supersedes`, `derived-from`, `split-from` or `merged-from`.
- Every published revision or result MUST be addressable by an immutable native identity and/or content digest.
- Moving or renaming a file does not, by itself, create a new logical artifact. Update the catalogue in the same change and preserve the ID when continuity of meaning is justified.
- A substantive split, merge or change of subject may require new logical IDs even when content is copied.
- Git history records repository changes; a release tag binds a release to an exact commit/tree. For Pijul, preserve native patch/channel/graph identities rather than fabricating Git-like identifiers.
- Hashes establish content identity/integrity under the selected algorithm; they do not establish semantic equivalence, truth, authority or approval.

### 2.2 Contract version is optional

A contract version MUST be assigned only when all of the following are declared:

1. the artifact's public contract and normative status;
2. its intended consumers and supported use cases;
3. the observable obligations, guarantees, schema, API or semantics exposed to those consumers;
4. the backward-compatibility relation and its direction;
5. the rules for deprecation, removal, migration and support;
6. the authority that approves contract changes.

If any of these is unknown, use revision identity and provenance. Do not use a SemVer-looking number as a substitute for missing policy.

## 3. The compatibility test

For an artifact with a declared contract, assess compatibility against the **previously published contract**, not merely the file diff or author's label.

A new contract version is backward-compatible only if every conforming consumer of the prior contract can continue to conform without changing its existing use, and no previously promised guarantee relied upon by those consumers is silently weakened. The exact test MUST be specialized to the artifact category.

Compatibility is directional and consumer-relative. A schema may remain syntactically compatible while a policy becomes normatively incompatible. A model may preserve an API while adding behaviors that invalidate a safety invariant. Therefore, GovCheck MUST NOT infer compatibility from additive syntax, unchanged filenames, passing tests or the words "bug fix".

### 3.1 SemVer mapping when the compatibility test is satisfied

| Increment | Meaning | GovCheck interpretation |
|---|---|---|
| MAJOR | Backward-incompatible contract change | At least one prior conforming consumer must adapt, re-evaluate or explicitly migrate; or a prior guarantee is withdrawn/changed |
| MINOR | Backward-compatible capability or contract addition | New capability is opt-in/optional or scoped so prior consumers and guarantees remain valid |
| PATCH | Backward-compatible correction | Corrects an implementation or representation defect without changing the approved contract's intended meaning or invalidating prior conforming use |
| No SemVer increment | No contract change | Editorial/explanatory change, regenerated projection, metadata-only correction or source revision that does not alter the declared contract; record the revision normally |

For a stable SemVer contract (MAJOR greater than zero), a published version MUST be immutable. A published version MUST NOT be overwritten. A pre-1.0 version may declare weaker stability, but `0.y.z` MUST NOT be used as an artifact revision counter or to avoid documenting compatibility expectations.

A "patch" is not synonymous with "small", "urgent", "bug fix" or "editorial". A correction that changes the contract actually consumed by users is MAJOR even if the previous text was erroneous. A correction can be PATCH only when the intended approved semantics were already unambiguous and the correction restores that meaning without changing consumer obligations or relied-upon guarantees.

### 3.2 Two compatibility dimensions for governance contracts

Normative packages and profiles require two checks:

- **Consumer obligation compatibility:** does a previously conforming repository remain conforming without changes?
- **Assurance guarantee compatibility:** are all previously promised constraints, protections and evidence guarantees preserved?

A change is backward-compatible only if both hold. A new mandatory obligation is normally MAJOR for an existing profile/package. A relaxation that weakens a relied-upon guarantee can also be MAJOR, even if it makes compliance easier. A new optional rule or a rule restricted to an explicitly opted-in profile can be MINOR. A correction to a normative source that changes actual interpretation is not automatically PATCH.

The format/schema version, metamodel version, rule-package version and repository-profile version are separate contracts. One source change may therefore be PATCH for an explanatory document, MAJOR for a normative package and no change to a serialization schema.

## 4. Artifact taxonomy and default regime

The following matrix is the default classification for GovCheck. "SemVer: yes" means only after the contract declaration in §2.2; it does not authorize assigning versions to every instance. "Revision" means stable logical ID plus immutable revision identity. "Instance" means a unique occurrence/event record. Each row is a starting policy, not a claim that the artifact type is already implemented.

| Artifact category | Examples | Default regime | SemVer scope, if any | Change/compatibility focus |
|---|---|---|---|---|
| Product intent and goals | Product purpose, objectives, non-goals | Revision | Published goal-set contract only | Meaning, scope, approved outcomes and downstream refinements |
| Stakeholder needs | Need statements, user outcomes | Revision | Rarely; only if exposed as a stable external contract | Intended subject and satisfaction conditions |
| Requirements | Functional, quality, security, process requirements | Revision | Requirement-set/package/profile contract | Obligation, applicability, satisfaction and affected consumers |
| Acceptance criteria | Acceptance predicates and scenarios | Revision; test-suite contract may be versioned | Criteria set only when consumed as a contract | Whether previously acceptable outcomes remain acceptable |
| Assumptions | Environmental, trust, platform or operational assumptions | Revision | Usually none | Whether dependent claims/proofs remain valid |
| Scope exclusions | Explicit non-goals and boundaries | Revision | Scope/profile contract if externally consumed | Inclusion/exclusion and affected obligations |
| Risks and threat scenarios | Threats, abuse cases, risk statements | Revision | Threat-model contract if used as a stable boundary | Coverage, adversary capability and security claims |
| Normative metamodel | Concepts, relations, typing and interpretation rules | Revision + contract version | Yes, if public semantics are declared | Structural and semantic compatibility; interpretation |
| Canonical governance model/format | Canonical package structure and encoding | Revision + separate schema/format version | Yes | Parsing, canonicalization, meaning and consumer behavior |
| Normative rule package | Obligations, prohibitions, permissions, invariants | Revision + package contract version | Yes, with dual compatibility test | Conformance impact and preservation of guarantees |
| Individual rule | Stable rule ID and revisions | Revision | Not normally per rule; package owns compatibility | Rule identity, force, scope, semantics and supersession |
| Repository profile | Selected rules, parameters and applicability | Revision + profile contract version | Yes, if consumed by governed repositories | Effective obligation/guarantee set and migration |
| Exception/waiver | Scoped, authorized, time-bounded exception | Instance/event with revisioned terms | No SemVer per exception | Authority, subject, scope, reason, expiry and revocation |
| Technical specification/API | CLI, API, adapter or protocol contract | Revision + contract version | Yes | Observable interface, errors, guarantees and migration |
| Serialization/schema | JSON Schema, report schema, manifest schema | Revision + schema version | Yes | Producer/consumer parsing and semantic interpretation |
| Architecture decision (ADR) | Accepted/rejected design decision | Revision + decision event | No SemVer per ADR | Authority, decision scope, supersession and affected contracts |
| Reference architecture | Components, boundaries and interfaces | Revision | SemVer only for a published architecture contract | Boundary/interface/guarantee compatibility |
| Assume-guarantee contract | Component assumptions and guarantees | Revision + contract version | Yes | Refinement, composition and guarantee preservation |
| Property/invariant | Safety, liveness or conformance predicate | Revision | Only as a public property-set contract | Predicate meaning, domain, assumptions and proof dependencies |
| Formal model | TLA+, Alloy, state machine or abstract model | Revision; optional model contract version | Conditional | State/behavior semantics, abstraction boundary and properties |
| Model-checking configuration | TLC config, constants, bounds, fairness/reductions | Revision, bound to model | No SemVer per run/config by default | Exact question explored and comparability |
| Formal proof statement/theorem | Proposition, theorem interface, axioms | Revision; theorem-library contract if exported | Conditional at library/interface level | Proposition, hypotheses, axioms and imports |
| Proof object/derivation | Lean term, proof script, checked certificate | Revision | No SemVer per individual proof | Exact statement, kernel, dependencies and reproducibility |
| Test definition/suite | Test cases, harness, acceptance vectors | Revision + test-suite contract when consumed | Conditional | Oracle, coverage claim, fixtures and compatibility |
| Individual test case | One assertion and its fixture | Revision | Usually no | Subject, oracle, preconditions and expected result |
| Test execution | One run of one test/suite | Instance/event | Never SemVer | Exact subject, test revision, invocation, environment and outcome |
| Tool/compiler/analyzer | GovCheck executable, TLC, Lean, validator | Tool's own release contract | Yes, for the tool's public API/CLI | Tool compatibility and exact build identity |
| Script/check adapter | Command, arguments, output and resource contract | Revision + adapter contract if consumed | Conditional | CLI/output semantics, failure behavior and trust boundary |
| Implementation/source code | GovCheck source and libraries | Revision + product release contract | Yes, for released software interfaces | Public behavior, CLI/API and supported guarantees |
| Binary/build artifact | Executable, package, container image | Immutable build/release instance | Version inherited from product release; build identity separate | Reproducibility, provenance and exact source/toolchain |
| Deployment configuration | Runtime settings, policy parameters | Revision; config schema may be versioned | Conditional for stable config interface | Effective behavior, defaults, security and migration |
| Dataset/fixture/corpus | Test data, synthetic corpus, benchmark set | Revision; dataset contract may be versioned | Conditional, dataset-specific | Schema, content, distribution, labels, splits and intended use |
| Counterexample/witness | TLC trace, failing input, minimal reproducer | Instance/evidence | No SemVer per witness | Exact model/test/tool and trace provenance |
| Evidence item/observation | Raw output, log, external observation | Instance/event | No SemVer per item | Subject binding, source, time, integrity and limitations |
| Claim/assertion | Scoped proposition about a subject | Revision | No SemVer per individual claim | Proposition, subject, scope, assumptions and support |
| Assurance argument | Claim decomposition and reasoning | Revision | Conditional for a published argument framework/interface | Support graph, defeaters, assumptions and evidence dependencies |
| Verification/evaluation report | Test, TLC, proof or conformity report | Instance; report schema versioned separately | Schema only, not each report | Exact run, status, completion, assumptions and evidence |
| Attestation/signature | Signed statement about a subject | Immutable instance/event | No SemVer | Signer, authority, key, subject, statement and revocation |
| Approval/acceptance/rejection | Authorized decision on exact candidate | Immutable event | No SemVer | Actor authority, candidate tuple, rationale and supersession |
| Release manifest | Manifest for one release | Immutable instance; manifest schema versioned | Schema only, not each manifest | Exact release, artifacts, digests, tools and evidence |
| Normative documentation | Human-readable rule projection | Revision; normative contract belongs to source package | No independent SemVer unless itself the declared contract | Fidelity to canonical authority and translation parity |
| Explanatory documentation | Guides, rationale, examples | Revision | Normally none | Clarity and correctness; no independent normative force |
| Translation | French/English counterpart | Revision linked to source revision | No independent SemVer | Semantic fidelity, status and source-language revision |
| Generated diagram/report projection | Mermaid, HTML, rendered view | Derived revision/instance | Generator or output schema may be versioned | Generator identity and reproducibility; source remains authoritative |
| Publication/release package | Published bundle or repository release | Release identity + immutable manifest | SemVer only for its declared consumer contract | Distribution contract, contents, provenance and support |

### 4.1 Reading the matrix

- The regime is assigned to the **logical artifact or record**, not automatically to every file that contains it.
- A package may have SemVer while its individual rules retain stable IDs and ordinary revisions.
- A TLA+ model may have a revision identity and optionally a model-contract version; every TLC run remains a distinct instance.
- A theorem library may version its exported logical interface; an individual proof term is identified by exact revision and checker context.
- A test suite may expose a versioned oracle/coverage contract; test executions are never versions of that suite.
- A report format may have SemVer; an individual report is a unique, immutable evaluation instance.
- A documentation file may be a controlled projection. Its revision is not a second version of the normative package.

## 5. Category-specific decision rules

### 5.1 Normative packages and profiles

Before release, compute or review the effective obligation and guarantee sets for each supported profile. For each change, record:

- rules added, removed, deprecated, strengthened, weakened or re-scoped;
- repositories/consumers newly affected or no longer affected;
- whether prior conforming consumers remain conforming;
- whether prior guarantees are preserved;
- migration, transition period, exception and re-evaluation requirements.

Typical classifications:

| Change | Default classification |
|---|---|
| Add a mandatory obligation to an existing profile | MAJOR |
| Add a new optional rule that is not selected by existing profiles | MINOR |
| Add a rule only to a new opt-in profile | MINOR for the package/profile family; new profile has its own identity |
| Strengthen an existing obligation or widen its applicability | MAJOR |
| Weaken/remove a guarantee relied upon by consumers | MAJOR |
| Correct spelling without changing meaning | No contract increment |
| Correct a source encoding defect while approved meaning is unambiguous and unchanged | PATCH may apply |
| Correct wording/encoding that changes effective interpretation or conformity outcomes | MAJOR, even if called a correction |
| Change an exception instance or its expiry | New revision/event, not a package SemVer increment |

A normative change requires approval from the authority designated for that rule/package. A SemVer increment cannot authorize the change.

### 5.2 Formal models and properties

For a formal model, record the model revision, semantic subject, abstraction boundary, variables/actions/transition relation, assumptions, invariants/temporal properties and consumer dependencies.

Do not classify changes by syntax alone:

- Comment/formatting change with no semantic effect: revision only; no model contract increment.
- Add a variable or transition that is provably observationally conservative for the declared interface and preserves all promised properties: potentially MINOR.
- Add a behavior that invalidates a previously promised safety/liveness property: MAJOR.
- Remove an invalid behavior: PATCH only if the approved contract already excluded it and the correction restores that exact meaning; otherwise MAJOR or a new model contract.
- Change a property statement, assumptions, fairness, bounds or abstraction: assess as a semantic contract change; never hide it as a tool/config patch.

A change to the TLC configuration creates a new configuration revision and a new run identity. It does not retroactively alter prior model-checking results. State-space counts are comparable only when the relevant model, configuration, tool and environment are sufficiently aligned.

### 5.3 Proofs, tests and evidence

- A proof repair for the same proposition is a new proof revision. It does not necessarily change the theorem/library contract.
- A changed theorem statement is a different proposition; preserve its identity relation and do not describe it as a mere proof repair.
- A test-oracle correction is a test-definition revision. If it changes the accepted behavior of a published test-suite contract, assess compatibility at suite level.
- A test execution, TLC run, proof-check run or external observation is a new instance. Never patch or overwrite its result.
- A report correction produces a new report revision/instance linked to the superseded record, with reason and authority. Preserve the original.
- Evidence invalidation changes its current admissibility/status, not its historical identity or raw content.

### 5.4 Documentation and translations

Distinguish source authority from presentation:

- Normative meaning changes in the canonical source are governed as rule/package changes.
- A projection-only regeneration does not create a new SemVer version of the source contract.
- A translation correction that restores an already-approved meaning is a documentation revision; a translation that changes actual interpretation is a conformance defect requiring correction and impact analysis.
- If a document itself is explicitly declared as a public contract, version that contract separately from editorial revisions, following the same compatibility test.

## 6. Change-impact and invalidation rules

Version classification and evidence freshness are separate decisions. Every changed artifact MUST trigger dependency analysis even when no SemVer increment occurs.

For each dependent claim, proof, test, report, approval and acceptance decision, determine whether the changed element is among its declared inputs or assumptions. Then record one of:

- **Unaffected:** dependency analysis establishes no relevant semantic or identity change.
- **Needs review:** relevance cannot be decided automatically or semantic equivalence is not established.
- **Stale/invalidated:** a required input, assumption, contract or subject changed.
- **Superseded:** a new authorized artifact/decision replaces the prior one.
- **Revoked:** an authority or key invalidates a previously issued attestation/approval.

Do not infer that every downstream artifact is stale merely because a repository commit changed. Conversely, do not infer freshness from unchanged SemVer. Dependency edges and exact revision bindings determine impact.

At minimum, changes to a normative package/profile, model, property, implementation, evaluator, toolchain, configuration, test oracle, external source or trust assumption require an explicit impact assessment against the evidence records that depend on them. Historical results remain available and are excluded from current acceptance when invalidated.

## 7. Required change record for a versioned contract

A release proposal for a SemVer-governed contract SHOULD record:

1. logical artifact ID and contract name;
2. prior and proposed contract versions;
3. exact prior and candidate revisions/digests;
4. declared consumer classes and compatibility direction;
5. public interface/guarantees covered by the version;
6. changes grouped by added, changed, deprecated, removed and corrected;
7. compatibility analysis, including counterexamples or migration cases;
8. effects on normative obligations and assurance guarantees, where relevant;
9. dependent artifacts/evidence requiring review or invalidation;
10. migration/deprecation/support policy;
11. authorized decision and provenance;
12. release tag/commit and immutable manifest.

The change author may propose an increment but MUST NOT be the sole authority for a normative compatibility decision where independent approval is required.

## 8. Worked edge cases

| Scenario | Correct treatment |
|---|---|
| Add an optional JSON field; old readers ignore unknown fields as promised | MINOR for the schema contract; new schema revision and release |
| Add an optional field but old readers reject unknown fields | Not backward-compatible; MAJOR or a separately negotiated format |
| Add a mandatory security rule to an existing repository profile | MAJOR for that profile/package, even if the file schema is unchanged |
| Add a new opt-in strict profile | New profile identity; potentially MINOR addition to a profile catalogue |
| Correct a misspelled comment in TLA+ | Model revision only; no semantic increment |
| Add a TLA+ transition that expands behavior and violates a safety invariant | MAJOR model-contract change; re-evaluate dependent claims |
| Change TLC bound from 10 to 12 | Configuration revision and new run; not a model SemVer increment by itself |
| Repair Lean proof script while theorem statement is identical | New proof revision; theorem interface unchanged |
| Weaken theorem assumptions or conclusion | New proposition/interface; assess as MAJOR for dependent theorem library |
| Fix test expected value because prior test encoded the wrong approved requirement | Test revision; assess suite contract and affected results; rerun, do not rewrite old run |
| Rerun unchanged test suite on a new commit | New execution instance, not PATCH of old report |
| Fix French translation to match approved English normative text | Translation revision; no independent normative SemVer |
| Change the approved rule because both translations were wrong | Normative change with authority decision and compatibility assessment |
| Replace a signing key after compromise | Key/attestation lifecycle event and revocation; not a PATCH to signatures |
| Rebuild identical source with a different compiler | New build instance/provenance; product SemVer may remain unchanged |

## 9. Automation boundary and conformance checks

A future GovCheck implementation may automate structural and mechanical parts of this policy. It MUST NOT claim that a semantic change is compatible merely from a textual diff or a declared version increment.

Candidate checks:

1. Every governed artifact has a unique stable logical ID where required.
2. Published revisions/releases are immutable and resolve to exact VCS/content identities.
3. Every SemVer contract declares its consumer, public contract and compatibility policy.
4. A version increment is accompanied by a categorized change record and compatibility rationale.
5. MAJOR/MINOR/PATCH declarations are checked against machine-observable structural rules where possible.
6. Normative package changes enumerate affected rules/profiles and effective obligation/guarantee deltas.
7. Model changes identify changed actions/properties/assumptions and require impact assessment.
8. Test/evaluation/proof runs have distinct instance IDs and bind exact subjects, definitions, tools, configurations and environments.
9. Reports, attestations and decisions are not overwritten; corrections/supersessions/revocations are explicit events.
10. Dependency changes produce a review set of potentially stale evidence/approvals.
11. Translations and generated projections identify their authoritative source revision.
12. Unsupported semantic compatibility analysis remains explicit and requires authorized human review; unknown is never a pass.

Automation can validate identity, schema shape, linkage, digest binding, declared deltas and workflow completeness. It cannot generally prove that a normative change preserves the intended meaning, that a model abstraction is adequate, or that a correction is semantically backward-compatible without a formalized relation and adequate proof.

## 10. Adoption and migration

This proposal MUST NOT be treated as binding until approved by the designated GovCheck authority and incorporated into the canonical governance authority under the normal change lifecycle.

Adoption should proceed without retroactively inventing SemVer histories:

1. Inventory existing logical artifacts and preserve established IDs, including `govcheck.lifecycle`.
2. Bind current artifacts to exact repository revisions and paths.
3. Classify each artifact using §4; record unresolved classifications as open.
4. Assign contract versions only to artifacts that pass §2.2. Do not manufacture prior MAJOR/MINOR/PATCH history.
5. Preserve the current release rule: Git tags identify exact commits; generated evidence is release-bound by immutable manifests.
6. Add dependency links and evidence invalidation metadata incrementally.
7. Validate the policy against the edge cases in §8 and representative repositories before implementing automated enforcement.
8. Revise the artifact catalogue and release-manifest schema only through separate, reviewed changes once their required fields and semantics are decided.

No serialization format, database, package manager, release service, proof assistant, or additional mandatory dependency is selected by this document.

## 11. Relationship to existing GovCheck contracts

This policy elaborates, but does not silently replace:

- [Specification 0002 — Canonical Governance Model](../specifications/0002-canonical-governance-model.md): canonical package identity, semantic version and stable rule IDs.
- [Specification 0003 — Change Lifecycle and Acceptance](../specifications/0003-change-lifecycle.md): immutable candidate identity, supersession, evidence freshness and append-only events.
- [Specification 0005 — Assurance, Claims and Evidence](../specifications/0005-assurance-model.md): exact subject/revision binding, provenance and invalidation.
- [Architecture 0010 — Assurance, proof and conformance](0010-assurance-proof-and-conformance.md): non-interchangeable evidence and assurance classes.
- [Architecture 0012 — Normative authority and documentation](0012-normative-authority-and-documentation.md): canonical authority and controlled projections.
- [Architecture 0013 — Governance metamodel](0013-governance-metamodel.md): typed artifact categories and relations.
- [Architecture 0015 — Governance conformance and validation plan](0015-governance-conformance-and-validation-plan.md): future validation responsibilities.

If a conflict is found, the existing approved normative authority prevails until an authorized change resolves it. This document remains a proposal until adopted.

## 12. External references

- [Semantic Versioning 2.0.0]([R-14](../references.md#r-14)): requires a declared public API and defines immutable published versions and compatibility-based increments.
- [1EdTech Versioning Framework 1.0]([R-23](../references.md#r-23)): applies SemVer-derived principles separately to specifications, documentation, specification artifacts, data models and software.
- [W3C PROV-O]([R-24](../references.md#r-24)): provenance vocabulary for entities, activities, agents and derivation; it complements rather than replaces versioning.
- [DataCite — Versioning]([R-25](../references.md#r-25)): distinguishes versions, related identifiers and concept-level records; stewards determine what counts as major/minor.
- [Scientific Data (2024), dataset versioning framework]([R-26](../references.md#r-26)): domain-specific treatment of dataset revisions and reproducibility.

These references support the distinction between compatibility versioning, revision identity and provenance. They do not prescribe GovCheck's artifact classifications; those are project-specific proposals above.


## Bibliographic references

External sources cited by this record: [R-14](../references.md#r-14), [R-23](../references.md#r-23), [R-24](../references.md#r-24), [R-25](../references.md#r-25), [R-26](../references.md#r-26).
