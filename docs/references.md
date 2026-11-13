# GovCheck external reference catalogue

## Thematic index

| Theme | Entries |
|---|---|
| Governance authority, separation of duties and secure development | R-01–R-03, R-11 |
| Risk assessment, threat modeling and attack paths | R-27–R-32 |
| Security assurance cases and metamodels | R-04, R-33–R-34 |
| PEAK decision model | R-74 |
| Continuous monitoring and runtime assurance | R-70, R-72, R-75–R-76 |
| Assurance 2.0, SACM evolution and implementation audits | R-71, R-73, R-128, R-197, R-198, R-199 |
| Assurance regimes and goal-oriented requirements | R-35–R-36, R-44, R-92 |
| Model checking and program-verification alternatives | R-05, R-20, R-37–R-43, R-89–R-91 |
| Evidence provenance and software supply chain | R-06–R-08 |
| Policy engines, authorization and policy-model verification | R-09–R-10, R-88 |
| Normative logic and deontic modalities | R-93 |
| Schemas and interface contracts | R-13, R-16 |
| Artifact identity, versioning, releases and reproducibility | R-14–R-15, R-21, R-23–R-26 |
| Governance metadata and catalogues | R-17 |
| Agent workflow systems assessed as fixtures | R-18–R-19 |
| Version-control semantics | R-22 |
| Alternative VCS, forges and CI platforms (Pijul CLI, GitLab, Woodpecker, SourceHut, Fossil) | R-109–R-113 |
| CRDTs, real-time collaboration and network transport | R-45–R-50, R-66, R-87 |
| Knowledge representation and interoperability | R-51–R-61, R-83–R-86 |
| Integration project repositories and studies | R-62 |
| Integration protocols and document conventions | R-67 |
| Adjacent GovCheck ecosystem repositories | R-68 |
| Mind-map format panorama source inventory | R-69 |
| Mind-map and graph interchange formats | R-63 |
| Agent tool and MCP governance | R-77 |
| Structured compliance models | R-78 |
| Agent sandboxing and isolation | R-79 |
| Matrix communication | R-80 |
| Document search | R-81 |
| Document extraction | R-82 |
| Cloud storage provider APIs | R-64 |
| Browser-local persistence and WebAssembly | R-65 |
| Domain semantic models, product quality and open-source compliance | R-94–R-100, R-102–R-103 |
| Agent-instruction interoperability and spec-driven workflows | R-104 |
| Policy-as-code and runtime agent-governance research | R-105 |
| OWASP guidance for AI-agent and MCP security | R-106 |
| GitHub Actions workflow location and syntax | R-107 |
| Open-source licensing and attribution | R-108 |
| Repository intent, lifecycle and requirements engineering | R-114–R-118, R-121–R-122 |
| System modeling and assurance-case metamodels | R-119–R-120 |
| Metamodel coherence, semantic preservation and formal verification | R-123–R-127 |
| Probabilistic assurance, fuzzy logic and state-transition models | R-193 |
| Concurrent edits, semantic merge conflicts and multi-agent delivery | R-142–R-151 |
| Canonical journal ordering, durable recovery and idempotent retry | R-194–R-196 |

## Full reference entries

## Detailed source register

**Purpose.** This register consolidates academic, standards-body, industrial-documentation and source-code references used to motivate GovCheck's repository-governance design. It is a navigational bibliography, not a normative policy or adoption decision.

**Selection rule.** Prefer primary publications, standards, official project documentation and pinned source revisions. A reference supports only the specific point stated here; it does not establish that GovCheck implements the capability or that a referenced tool is suitable as a dependency.

## How to use these references

- **Normative authority and separation of duties:** R-01, R-02, R-03.
- **Formal models, proofs and assurance arguments:** R-04, R-05, R-89–R-91.
- **Evidence provenance and software supply chain:** R-06, R-07, R-08.
- **Executable policy and authorization:** R-09, R-10.
- **Policy-model verification before enforcement:** R-88.
- **Normative modalities (obligation, permission, prohibition):** R-93.
- **Repository security posture and enforcement boundary:** R-03, R-08, R-18, R-19.
- **Canonical schemas, versioning and release identity:** R-13, R-14, R-15, R-16.
- **External governance/catalogue pattern:** R-17.
- **Candidate agent-workflow tools assessed, not adopted:** R-18, R-19.
- **Proof assistant and interface contracts:** R-20, R-21.
- **CRDTs, peer-to-peer transport and discovery:** R-45–R-50, R-66, R-87.
- **Knowledge representation and linked-data interchange:** R-51–R-61, R-83–R-86.
- **Native VCS semantics and collaboration adapters:** R-22.
- **Threat modeling, attack paths and risk management:** R-27–R-32.
- **Goal-oriented requirements modeling:** R-44, R-92.
- **Security assurance cases and metamodels:** R-33–R-34.
- **PEAK decision model:** R-74.
- **Continuous monitoring and runtime assurance:** R-70, R-72, R-75–R-76.
- **Assurance 2.0 and SACM evolution:** R-71, R-73, R-128, R-197, R-198, R-199.
- **Domain semantics, product quality and open-source compliance (candidate sources):** R-94–R-100, R-102–R-103.
- **Agent instructions and spec-driven workflows:** R-104.
- **Policy-as-code, continuous assurance and MCP governance research:** R-105.
- **AI-agent and MCP security guidance:** R-106.
- **GitHub Actions workflow placement:** R-107.
- **Open-source licensing and attribution:** R-108.
- **Repository intent and lifecycle/requirements engineering:** R-114–R-118, R-121–R-122.
- **System modeling and assurance-case metamodels:** R-119–R-120.
- **Probabilistic assurance, fuzzy logic and state-transition models:** R-193.
## Standards, government guidance and industry specifications

<a id="r-01"></a>
### R-01 — NIST SP 800-53 Rev. 5, Security and Privacy Controls
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md), [0013](architecture/0013-governance-metamodel.md), [0022](architecture/0022-governance-capability-audit.md), [0023](architecture/0023-bootstrap-governance-authority.md), [Spec 0002](specifications/0002-canonical-governance-model.md) · [Intent impact analysis](intent-impact-analysis.md)

- **Primary source:** [NIST SP 800-53 publication and control catalogue](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- **Relevant concepts:** AC-5 separation of duties; access management; auditability and control ownership.
- **Use in GovCheck:** informs the distinction between normative authorization, technical review and execution, and the need to describe limits of a single-authority regime.
- **Limit:** a control catalogue is not GovCheck's governance ontology; selecting a control does not demonstrate implementation.

<a id="r-02"></a>

### R-02 — NIST SP 800-218, Secure Software Development Framework (SSDF) 1.1
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md), [0014](architecture/0014-governed-development-workflow.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md), [0022](architecture/0022-governance-capability-audit.md) · [0027](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md)

- **Primary source:** [NIST publication](https://csrc.nist.gov/pubs/sp/800/218/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-218)
- **Relevant concepts:** documented security requirements and design decisions, secure development practices, provenance and release practices.
- **Use in GovCheck:** reference for traceable repository-development obligations and the lifecycle context in which evidence is collected.
- **Limit:** SSDF is practice guidance, not a formal acceptance predicate or proof of conformity. NIST has also published a draft SP 800-218 Rev. 1 / SSDF 1.2; use the publication status appropriate to the claim.

<a id="r-03"></a>

### R-03 — GitHub protected branches and required status checks
- **Cited by:** [0014](architecture/0014-governed-development-workflow.md), [0022](architecture/0022-governance-capability-audit.md), [0023](architecture/0023-bootstrap-governance-authority.md), [ADR 0002](decisions/0002-study-placement.md), [ADR 0007](decisions/0007-mandatory-sources.md) · [Intent impact analysis](intent-impact-analysis.md)

- **Primary source:** [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **Relevant concepts:** required reviews, required status checks, bypass lists and branch restrictions.
- **Use in GovCheck:** demonstrates a practical shared-acceptance enforcement point.
- **Limit:** forge settings are enforcement mechanisms, not normative authority. Repository administrators and permitted bypass actors remain in the threat model.

<a id="r-04"></a>

### R-04 — Goal Structuring Notation (GSN) Community Standard
- **Cited by:** [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)

- **Primary source:** [GSN Community Standard — official site](https://scsc.uk/gsn)
- **Relevant concepts:** structured assurance claims, arguments, strategies, context, assumptions and evidence.
- **Use in GovCheck:** useful vocabulary for the assurance dossier and traceability from governance requirements to properties and evidence.
- **Limit:** an assurance argument structures reasoning; it does not automatically make premises true or replace machine-checkable predicates.

<a id="r-05"></a>

### R-05 — TLA+ and TLC
- **Cited by:** [0007-technology-decision-framework](architecture/0007-technology-decision-framework.md), [0008-formalization-and-conformance](architecture/0008-formalization-and-conformance.md), [0009-govcheck-design-discussion-record](architecture/0009-govcheck-design-discussion-record.md), [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0011-lifecycle-model-assertion-audit](architecture/0011-lifecycle-model-assertion-audit.md), [0020-first-tlc-execution-record](architecture/0020-first-tlc-execution-record.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0032-canonical-publication-model-checking](architecture/0032-canonical-publication-model-checking.md), [0033-governance-evaluator-exception-revocation-model](architecture/0033-governance-evaluator-exception-revocation-model.md), [0035-canonical-journal-recovery-model](architecture/0035-canonical-journal-recovery-model.md), [0001-bootstrap-boundaries](decisions/0001-bootstrap-boundaries.md), [0002-study-placement](decisions/0002-study-placement.md), [0008-governance-applicability-arbitration-session](decisions/0008-governance-applicability-arbitration-session.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [README](formal/README.md), [lifecycle-model](formal/lifecycle-model.md), [0003-change-lifecycle](specifications/0003-change-lifecycle.md), [0005-assurance-model](specifications/0005-assurance-model.md), [0006-governance-revision-applicability](specifications/0006-governance-revision-applicability.md), [0007-canonical-governance-journal-protocol](specifications/0007-canonical-governance-journal-protocol.md), [events](work-portfolio/events.md)

- **Primary sources:** [Lamport's publications on TLA](https://www.microsoft.com/en-us/research/people/lamport/publications/) · [TLA+ project and documentation](https://lamport.azurewebsites.net/tla/tla.html)
- **Academic reference:** Leslie Lamport, “The Temporal Logic of Actions,” ACM Transactions on Programming Languages and Systems, 16(3), 1994, pp. 872–923. [DOI](https://doi.org/10.1145/177492.177726)
- **Relevant concepts:** state-transition specifications, invariants, temporal properties and model checking.
- **Use in GovCheck:** foundation for lifecycle, assurance and authority-transition models.
- **Limit:** a completed TLC run establishes properties only for the recorded model, configuration, assumptions and explored bounds; it does not prove implementation refinement or normative fidelity.

<a id="r-06"></a>

### R-06 — in-toto: software supply-chain integrity
- **Cited by:** [0006-threat-and-trust-model](architecture/0006-threat-and-trust-model.md), [0007-technology-decision-framework](architecture/0007-technology-decision-framework.md), [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0014-governed-development-workflow](architecture/0014-governed-development-workflow.md), [0015-governance-conformance-and-validation-plan](architecture/0015-governance-conformance-and-validation-plan.md), [0002-study-placement](decisions/0002-study-placement.md), [0007-mandatory-sources](decisions/0007-mandatory-sources.md), [intent-impact-analysis](intent-impact-analysis.md), [concurrent-agent-change-governance](research/concurrent-agent-change-governance.md)

- **Primary sources:** [in-toto project](https://in-toto.io/) · [USENIX Security 2019 paper](https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf)
- **Academic reference:** Santiago Torres-Arias et al., “in-toto: Providing farm-to-table guarantees for bits and bytes,” 28th USENIX Security Symposium, 2019.
- **Relevant concepts:** recording steps, materials/products and provenance in a software supply chain.
- **Use in GovCheck:** informs provenance and binding of check/evidence records to the artifacts and process steps that produced them.
- **Limit:** provenance does not define repository-specific normative rules or prove that a recorded step was semantically correct.

<a id="r-07"></a>

### R-07 — SLSA
- **Cited by:** [0006-threat-and-trust-model](architecture/0006-threat-and-trust-model.md), [0007-technology-decision-framework](architecture/0007-technology-decision-framework.md), [0014-governed-development-workflow](architecture/0014-governed-development-workflow.md), [0015-governance-conformance-and-validation-plan](architecture/0015-governance-conformance-and-validation-plan.md), [0002-study-placement](decisions/0002-study-placement.md), [concurrent-agent-change-governance](research/concurrent-agent-change-governance.md), [0005-assurance-model](specifications/0005-assurance-model.md)

- **Primary source:** [SLSA specification](https://slsa.dev/spec/)
- **Relevant concepts:** software supply-chain levels, provenance and build integrity.
- **Use in GovCheck:** complementary vocabulary for build provenance and release evidence.
- **Limit:** SLSA does not define GovCheck's canonical authority, exception policy, change lifecycle or complete assurance case.

<a id="r-08"></a>

### R-08 — OpenSSF Scorecard
- **Cited by:** [0015](architecture/0015-governance-conformance-and-validation-plan.md), [ADR 0002](decisions/0002-study-placement.md) · [Intent impact analysis](intent-impact-analysis.md)

- **Primary sources:** [OpenSSF project page](https://openssf.org/projects/scorecard/) · [Scorecard repository](https://github.com/ossf/scorecard)
- **Relevant concepts:** automated, reusable checks of selected open-source security practices.
- **Use in GovCheck:** candidate source of scoped security-posture evidence.
- **Limit:** a score is not a complete repository-specific governance evaluation, proof or authorization decision.

<a id="r-09"></a>

### R-09 — Open Policy Agent (OPA)
- **Cited by:** [0012](architecture/0012-normative-authority-and-documentation.md), [0013](architecture/0013-governance-metamodel.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md), [0021](architecture/0021-assurance-claims-and-freshness.md), [0022](architecture/0022-governance-capability-audit.md), [Spec 0002](specifications/0002-canonical-governance-model.md), [ADR 0002](decisions/0002-study-placement.md) · [Intent impact analysis](intent-impact-analysis.md)

- **Primary source:** [Official OPA documentation](https://www.openpolicyagent.org/docs)
- **Relevant concepts:** separation of policy decision-making from policy enforcement; evaluating structured input against policy.
- **Use in GovCheck:** informs a possible evaluator/enforcement-point separation and declarative-policy comparison.
- **Limit:** OPA is not GovCheck's normative authority, assurance-case engine or proof of non-bypassability. No dependency is selected.

<a id="r-10"></a>

### R-10 — Cedar authorization language
- **Cited by:** [0012](architecture/0012-normative-authority-and-documentation.md), [0013](architecture/0013-governance-metamodel.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md), [0022](architecture/0022-governance-capability-audit.md), [Spec 0002](specifications/0002-canonical-governance-model.md), [ADR 0002](decisions/0002-study-placement.md) · [Intent impact analysis](intent-impact-analysis.md)

- **Primary sources:** [Cedar language reference](https://docs.cedarpolicy.com/) · [Cedar project](https://www.cedarpolicy.com/) · [OOPSLA 2024 paper](https://doi.org/10.1145/3649835) · [FSE Companion 2024: How We Built Cedar](https://doi.org/10.1145/3663529.3663854) · [arXiv preprint](https://arxiv.org/abs/2407.01688)
- **Relevant concepts:** typed principal/action/resource/context authorization decisions and separation of authorization logic from application logic.
- **Use in GovCheck:** informs future comparison of scoped authorization and deterministic decision semantics, and the verification-guided development pattern (executable formal model, proofs, differential testing and property-based testing).
- **Limit:** Cedar is not a complete governance lifecycle, evidence-freshness model or assurance case. No dependency is selected.

<a id="r-11"></a>

### R-11 — NIST SP 800-218 SSDF project page
- **Cited by:** no current architecture, specification or decision record cites this source; retained as a candidate reference.

- **Primary source:** [NIST SSDF project and publications](https://csrc.nist.gov/projects/ssdf)
- **Relevant concepts:** secure development practices and mappings to established practices.
- **Use in GovCheck:** supplementary navigation for the status of SSDF publications and profiles.
- **Limit:** use the dated final publication when making a version-specific claim; do not confuse a draft revision with a final standard.

<a id="r-13"></a>

### R-13 — JSON Schema Draft 2020-12
- **Cited by:** [0008](architecture/0008-formalization-and-conformance.md), [0011](architecture/0011-lifecycle-model-assertion-audit.md), [0012](architecture/0012-normative-authority-and-documentation.md), [0013](architecture/0013-governance-metamodel.md), [Spec 0002](specifications/0002-canonical-governance-model.md)

- **Primary source:** [Official specification landing page](https://json-schema.org/draft/2020-12/)
- **Relevant concepts:** structural validation of machine-readable records.
- **Use in GovCheck:** candidate reference for governance records and evidence manifests if JSON Schema is adopted.
- **Limit:** schema validity does not establish authorization, semantic consistency, truth, policy adoption or evaluator correctness. Listing it does not select it as the canonical format.

<a id="r-14"></a>

### R-14 — Semantic Versioning 2.0.0
- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md), [0019](architecture/0019-catalogue-and-release-manifest-migration.md) · [ADR 0004](decisions/0004-semantic-versioning-contracts.md)

- **Primary source:** [SemVer 2.0.0](https://semver.org/)
- **Relevant concepts:** MAJOR/MINOR/PATCH relative to a declared public API and compatibility contract; published versions are immutable.
- **Use in GovCheck:** informs the distinction between artifact identity, immutable revision, contract compatibility and release identity.
- **Limit:** SemVer is not meaningful for every governance artifact. GovCheck's adopted category-specific versioning policy avoids applying it mechanically to models, evidence instances, decisions or events.

<a id="r-15"></a>

### R-15 — Git tags and releases
- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md), [0019](architecture/0019-catalogue-and-release-manifest-migration.md) · [ADR 0004](decisions/0004-semantic-versioning-contracts.md)

- **Primary sources:** [Git reference: tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging) · [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- **Relevant concepts:** identifying a source revision and publishing release-associated artifacts.
- **Use in GovCheck:** release-bound verification reports and manifests identifying the exact repository tree, commit, model/configuration and tool versions.
- **Limit:** a tag or release is an identifier/publication mechanism, not proof that verification ran or passed.

<a id="r-16"></a>

### R-16 — OpenAPI and machine-readable interface contracts
- **Cited by:** [0004](specifications/0004-vcs-collaboration-contracts.md), [0014](architecture/0014-governed-development-workflow.md)

- **Primary source:** [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- **Relevant concepts:** machine-readable interface contracts.
- **Use in GovCheck:** possible future CLI/dossier interchange and adapter-contract documentation.
- **Limit:** interface conformance does not establish authorization semantics, runtime behavior or implementation correctness.

<a id="r-17"></a>

### R-17 — Google Cloud Knowledge Catalog
- **Cited by:** [0012](architecture/0012-normative-authority-and-documentation.md), [0022](architecture/0022-governance-capability-audit.md), [Spec 0002](specifications/0002-canonical-governance-model.md), [Spec 0006](specifications/0006-governance-revision-applicability.md)

- **Primary source:** [Knowledge Catalog documentation](https://docs.cloud.google.com/knowledge-catalog/docs)
- **Relevant concepts:** typed metadata, catalogue entries, relationships/lineage, governance metadata and context discovery.
- **Use in GovCheck:** the transferable pattern is type-specific mandatory metadata and traceable relationships between governed objects.
- **Limit:** this is Google Cloud's data-catalog product, not Open Knowledge Format (OKF), which is catalogued separately as R-51. GovCheck is not a data catalog; metadata presence does not equal normative authority or enforcement.

<a id="r-18"></a>
### R-18 — Writ (infinri/Writ)
- **Cited by:** [0009](architecture/0009-govcheck-design-discussion-record.md), [0014](architecture/0014-governed-development-workflow.md), [0016](architecture/0016-writ-privateer-assessment.md), [0019](architecture/0019-catalogue-and-release-manifest-migration.md), [0021](architecture/0021-assurance-claims-and-freshness.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [repository](https://github.com/infinri/Writ) · [security policy at reviewed revision](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/SECURITY.md) · [gate/session contract](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/docs/reference/session-and-gates.md)
- **Reviewed revision:** ebdafe5450b201339f81e717ed104e6bcfd3fe3e (review recorded 2026-11-06).
- **Use in GovCheck:** optional agent-workflow test fixture and possible source of scoped execution evidence.
- **Limit:** Writ explicitly says it is not a sandbox/security boundary; its output is not GovCheck's normative authority or independent acceptance decision. See Architecture 0016.

<a id="r-19"></a>

### R-19 — Privateer (privateer-agent/privateer-agent)
- **Cited by:** [0009](architecture/0009-govcheck-design-discussion-record.md), [0014](architecture/0014-governed-development-workflow.md), [0016](architecture/0016-writ-privateer-assessment.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [repository](https://github.com/privateer-agent/privateer-agent) · [security policy at reviewed revision](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/SECURITY.md) · [README at reviewed revision](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/README.md)
- **Reviewed revision:** 181a988e443fa6b6b4138fc349d1260c96408ad4 (review recorded 2026-11-06).
- **Use in GovCheck:** candidate Pi-based agent-harness interoperability fixture.
- **Limit:** a permission gate, provenance feature or privacy warning does not replace canonical governance or independently verified acceptance. See Architecture 0016.

<a id="r-20"></a>

### R-20 — Lean
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [0008](architecture/0008-formalization-and-conformance.md), [0010](architecture/0010-assurance-proof-and-conformance.md), [ADR 0001](decisions/0001-bootstrap-boundaries.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md), [CSLib compatibility audit](research/cslib-compatibility-audit.md), [metamodel semantic-coverage audit](research/metamodel-semantic-coverage-audit.md)

- **Primary source:** [Lean language reference](https://lean-lang.org/doc/reference/latest/)
- **Related library:** [CSLib](https://github.com/leanprover/cslib), a Lean library for formalizing computer-science theories, temporal logics and transition-system semantics.
- **Relevant concepts:** proof terms checked by a small kernel; theorem proving under explicit definitions, axioms and hypotheses.
- **Use in GovCheck:** candidate for narrowly justified proof-critical predicates or certificate checking, if a later ADR supports it.
- **Limit:** a theorem about a predicate does not establish that the predicate captures approved policy or that the executable refines it. Lean is not selected as a product-wide dependency.

<a id="r-21"></a>

### R-21 — Research software release and reproducibility guidance
- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md), [ADR 0002](decisions/0002-study-placement.md) · [ADR 0004](decisions/0004-semantic-versioning-contracts.md)

- **Primary source:** [Software Sustainability Institute — guides and resources](https://www.software.ac.uk/resources) · [LUMC Research Software Guidelines — versioning and releases](https://lumc-dcc.github.io/rs-guidelines/best-practices/versioning-releases/)
- **Relevant concepts:** sustainable research software, citation, releases and reproducibility.
- **Use in GovCheck:** supports recording exact tool versions and release context needed to interpret evidence; the LUMC guide distinguishes SemVer for stable interfaces, CalVer for operational tools and meaningful tags for reproducibility.
- **Limit:** these living guides are general recommendations for research software, not a release-manifest contract or mandatory standard. The versioning scheme must remain appropriate to the artifact type and the stability of its interface.

<a id="r-22"></a>

### R-22 — Native Git and Pijul semantics
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [0009](architecture/0009-govcheck-design-discussion-record.md), [0011](architecture/0011-lifecycle-model-assertion-audit.md), [0014](architecture/0014-governed-development-workflow.md), [0021](architecture/0021-assurance-claims-and-freshness.md), [ADR 0001](decisions/0001-bootstrap-boundaries.md), [Spec 0003](specifications/0003-change-lifecycle.md), [Spec 0004](specifications/0004-vcs-collaboration-contracts.md), [ADR 0002](decisions/0002-study-placement.md), [Formal lifecycle model](formal/lifecycle-model.md), [Spec 0006](specifications/0006-governance-revision-applicability.md), [ADR 0006](decisions/0006-vcs-forge-portability.md), [ADR 0008](decisions/0008-governance-applicability-arbitration-session.md), [Formal model index](formal/README.md), [Architecture 0032](architecture/0032-canonical-publication-model-checking.md), [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md), [Architecture 0035](architecture/0035-canonical-journal-recovery-model.md), [Work portfolio events](work-portfolio/events.md)

- **Primary sources:** [Git documentation](https://git-scm.com/docs) · [Pijul manual: theory](https://pijul.org/manual/theory) · [Pijul channels](https://pijul.org/manual/workflows/channels) · [Pijul conflicts](https://pijul.org/manual/conflicts.html) · [Pijul project](https://pijul.org/) · [Nest hosting service](https://nest.pijul.com/) · [Nest source repository](https://nest.pijul.com/pijul/nest/tree)
- **Relevant concepts:** Git's snapshot/commit and tree model; Pijul's change/patch graph, channels and first-class conflicts; Nest as a Pijul repository-hosting platform.
- **Use in GovCheck:** supports the explicit VCS-adapter boundary and the requirement that candidate identity, conflict detection and application be represented using native semantics rather than forced into one shared Git-shaped abstraction.
- **Limit:** vendor documentation explains the systems' intended semantics; GovCheck still needs adapter contracts and conformance tests. This reference does not establish that either adapter is implemented.

- [0004 — VCS and Collaboration Adapter Contracts](specifications/0004-vcs-collaboration-contracts.md): R-22.

## Academic foundations and assurance

<a id="r-23"></a>

### R-23 — IMS Global / 1EdTech versioning specifications
- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md) · [ADR 0004](decisions/0004-semantic-versioning-contracts.md)

- **Primary source:** [1EdTech specifications](https://www.imsglobal.org/spec/versioning/v1) (formerly IMS Global; consult the specific versioning specification before relying on a particular rule).
- **Relevant concepts:** version identifiers and compatibility conventions for structured, published artifacts.
- **Use in GovCheck:** comparative input to the category-specific artifact-versioning analysis in Architecture 0017–0018.
- **Limit:** a domain-specific education-technology specification family, not a universal governance-artifact versioning standard.

<a id="r-24"></a>
### R-24 — W3C PROV-O
- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md) · [ADR 0004](decisions/0004-semantic-versioning-contracts.md) · [Work portfolio](work-portfolio/README.md), [ADR 0007](decisions/0007-mandatory-sources.md)

- **Primary source:** [W3C PROV-O recommendation](https://www.w3.org/TR/prov-o/).
- **Relevant concepts:** entities, activities, agents and provenance relations.
- **Use in GovCheck:** vocabulary for provenance and relationships between artifacts, activities and responsible agents.
- **Limit:** an ontology does not itself provide repository policy, identity assurance or enforcement.

<a id="r-25"></a>
### R-25 — DataCite versioning guidance
- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md) · [ADR 0004](decisions/0004-semantic-versioning-contracts.md)

- **Primary source:** [DataCite documentation on versioning](https://support.datacite.org/docs/versioning).
- **Relevant concepts:** identifying and relating versions of citable research outputs.
- **Use in GovCheck:** informs the distinction between a persistent logical artifact identity and individually identified versions.
- **Limit:** guidance for research outputs is not a general policy for all software and governance artifacts.

<a id="r-26"></a>
### R-26 — Scientific Data versioning study (2024)
- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md) · [ADR 0004](decisions/0004-semantic-versioning-contracts.md)

- **Primary source:** [Nature / Scientific Data article](https://www.nature.com/articles/s41597-024-03153-y).
- **Relevant concepts:** versioning and provenance practices for scientific data.
- **Use in GovCheck:** comparative research input to the artifact identity and versioning discussion.
- **Limit:** domain-specific research does not establish a normative versioning rule for GovCheck.

<a id="r-27"></a>
### R-27 — NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md) · [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md)

- **Primary source:** [NIST publication](https://csrc.nist.gov/pubs/sp/800/30/r1/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-30r1)
- **Relevant concepts:** threat sources and events, vulnerabilities, likelihood and impact, risk assessment, residual risk, assumptions, rationale and uncertainty.
- **Use in GovCheck:** supports scenario-based assessment that records how likelihood/plausibility is derived, the impact dimensions considered, safeguards already in place, uncertainty and the rationale for the result.
- **Limit:** NIST SP 800-30 is risk-assessment guidance, not a universal quantitative formula or a requirement to use a particular scoring scale. GovCheck must not turn illustrative scales into calibrated measurements.

<a id="r-28"></a>
### R-28 — NIST SP 800-160 Vol. 1 Rev. 1, Engineering Trustworthy Secure Systems
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md) · [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md)

- **Primary source:** [NIST publication](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-160v1r1)
- **Relevant concepts:** systems security engineering across the lifecycle; stakeholder protection needs; requirements, architecture, implementation, verification, validation and risk management.
- **Use in GovCheck:** supports connecting protection needs and security requirements to architecture, controls, verification evidence and lifecycle decisions rather than treating threat analysis as a one-off questionnaire.
- **Limit:** the publication is engineering guidance, not a repository governance schema or proof that a particular system satisfies its security requirements.

<a id="r-29"></a>
### R-29 — ISO 31000:2018, Risk management — Guidelines
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md) · [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md)

- **Primary source:** [ISO standard landing page](https://www.iso.org/standard/31000)
- **Relevant concepts:** principles and framework for identifying, analysing, evaluating, treating, monitoring, reviewing and communicating risk.
- **Use in GovCheck:** provides a general risk-management reference for keeping assessment, treatment, acceptance, monitoring and review connected to governance and decision-making.
- **Limit:** ISO 31000 is generic guidance, not a cybersecurity threat taxonomy or a prescribed risk-calculation algorithm. The full standard is not reproduced here.

<a id="r-30"></a>
### R-30 — MITRE ATT&CK
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md) · [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md)

- **Primary source:** [MITRE ATT&CK knowledge base](https://attack.mitre.org/) · [Getting started and usage guidance](https://attack.mitre.org/resources/)
- **Relevant concepts:** adversary tactics and techniques grounded in observed behavior; mappings between techniques, platforms and mitigations.
- **Use in GovCheck:** optional vocabulary and evidence source for enriching threat scenarios and attack-path analysis, and for checking whether proposed controls address known adversary behaviors.
- **Limit:** ATT&CK is not an exhaustive threat model, likelihood estimator, vulnerability database or proof of exploitability. A technique mapping does not establish that a technique is feasible in the project's context or that a mitigation is effective.

<a id="r-31"></a>
### R-31 — Microsoft Security Development Lifecycle: Threat Modeling
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md) · [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md)

- **Primary source:** [Microsoft SDL threat-modeling guidance](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- **Relevant concepts:** security requirements, system/data-flow diagrams, threat identification, mitigation and validation as an iterative engineering process.
- **Use in GovCheck:** industry example for guiding project owners through a repeatable threat-modeling workflow that links architecture and trust boundaries to mitigations and validation.
- **Limit:** Microsoft's workflow is a practical method, not a complete risk-governance or assurance-case standard. Its examples and tool are not mandatory GovCheck dependencies.

<a id="r-32"></a>
### R-32 — Bruce Schneier, “Attack Trees” (1999)
- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md) · [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md)

- **Primary source:** [Dr. Dobb's Journal article, archived by Schneier](https://www.schneier.com/academic/archives/1999/12/attack_trees.html)
- **Academic/technical reference:** Bruce Schneier, “Attack Trees,” Dr. Dobb's Journal, December 1999.
- **Relevant concepts:** hierarchical decomposition of attacker goals into alternative or conjunctive sub-goals; reasoning about attack feasibility and cost.
- **Use in GovCheck:** foundational technique for representing attack paths and alternative ways to reach a harmful objective, and for relating mitigations to specific path steps.
- **Limit:** attack trees are models whose completeness and parameter estimates require justification. Costs or probabilities assigned to nodes must not be treated as objective without calibrated evidence.

<a id="r-33"></a>
### R-33 — Mohamad, Steghöfer and Scandariato, “Security assurance cases—state of the art of an emerging approach” (2021)
- **Cited by:** [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0024-project-bootstrap-and-assurance-profiles](architecture/0024-project-bootstrap-and-assurance-profiles.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)

- **Primary source:** [Empirical Software Engineering article](https://doi.org/10.1007/s10664-021-09971-7)
- **Academic reference:** Mazen Mohamad, Jan-Philipp Steghöfer and Riccardo Scandariato, *Empirical Software Engineering* 26, article 70 (2021).
- **Relevant concepts:** systematic literature review of 51 studies on security assurance cases; structured claims, argumentation, assumptions, context and evidence; state of validation and tool support.
- **Use in GovCheck:** supports keeping claims, assumptions, context, inference and evidence explicit, while treating assurance-case construction and maintenance as an engineering activity requiring validation.
- **Limit:** the review reports an immature research/practice landscape and gaps in validation and tool support; it does not establish that adopting an assurance-case notation automatically produces a valid security argument.

<a id="r-34"></a>
### R-34 — OMG Structured Assurance Case Metamodel (SACM)
- **Cited by:** [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0024-project-bootstrap-and-assurance-profiles](architecture/0024-project-bootstrap-and-assurance-profiles.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md), [metamodel semantic-coverage audit](research/metamodel-semantic-coverage-audit.md)

- **Primary source:** [OMG SACM specification family](https://www.omg.org/spec/SACM/) · [formal version 2.3](https://www.omg.org/spec/SACM/2.3)
- **Relevant concepts:** machine-processable representation of assurance-case structures and relationships between claims, argumentation, artifacts and evidence.
- **Use in GovCheck:** candidate comparative metamodel for typed assurance artifacts and traceability, beyond free-form narrative documents.
- **Limit:** SACM is a metamodel, not a risk-assessment method, truth oracle or proof of evidence sufficiency. Version 2.4 is currently a beta; this entry points to the formal 2.3 version and does not recommend adopting SACM.

## Additional sources recovered from the assurance and integration discussions

<a id="r-35"></a>
### R-35 — Common Criteria (ISO/IEC 15408) and Common Evaluation Methodology
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [ISO/IEC 15408-1:2026 (current edition of Part 1)](https://www.iso.org/standard/15408-1) · [Common Criteria Portal](https://www.commoncriteriaportal.org/) · [CC:2022 and CEM:2022 scheme publications](https://www.commoncriteriaportal.org/cc/index.cfm)
- **Relevant concepts:** security functional requirements, security assurance requirements, evaluation methodology and Evaluation Assurance Levels (EALs).
- **Use in GovCheck:** contextualizes the assurance vocabulary explicitly contrasted with GovCheck's method classes in Specification 0005.
- **Limit:** EALs are evaluation assurance packages in the Common Criteria scheme, not generic software maturity grades or GovCheck assurance tiers. Certification scope and target-of-evaluation matter. ISO/IEC 15408-1:2026 is the current edition of Part 1; the Common Criteria Portal separately publishes the CC:2022/CEM:2022 scheme documents. Do not infer that a revision to one ISO part automatically changes every scheme or certification rule.

<a id="r-36"></a>
### R-36 — RTCA DO-178C / EUROCAE ED-12C airborne software assurance
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [FAA AC 20-115D](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D) · [RTCA DO-178C overview and supplements](https://www.rtca.org/do-178/)
- **Relevant concepts:** software life-cycle objectives, verification, independence, certification evidence and software levels (A–E); related supplements include DO-330, DO-331, DO-332 and DO-333.
- **Use in GovCheck:** provides the aviation-specific assurance/certification example named in Specification 0005 and distinguishes domain-specific assurance regimes from generic test/proof methods.
- **Limit:** DO-178C is an aviation software assurance standard used within an airworthiness certification context. FAA AC 20-115D describes an acceptable means, not the only means or a general software regulation. The full RTCA standard is not reproduced by the public overview.

<a id="r-37"></a>
### R-37 — Alloy language and Analyzer
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [0009](architecture/0009-govcheck-design-discussion-record.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Alloy project and documentation](https://alloytools.org/) · [Alloy Analyzer source repository](https://github.com/AlloyTools/org.alloytools.alloy)
- **Relevant concepts:** relational modeling, bounded analysis, SAT-based instance finding and counterexample search; Alloy 6 adds mutable state and temporal operators.
- **Use in GovCheck:** candidate formal-modeling method cited in Specifications 0005 and Architecture 0007/0009.
- **Limit:** results depend on declared scopes, bounds and model assumptions; Alloy analysis is not a proof about an implementation without a separate refinement/conformance argument.

<a id="r-38"></a>
### R-38 — SPIN and Promela
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [SPIN Basic Manual and Promela documentation](https://spinroot.com/spin/Man/Manual.html)
- **Relevant concepts:** modeling and verification of concurrent and distributed systems, asynchronous communication, invariants, deadlocks and temporal properties.
- **Use in GovCheck:** candidate model checker named in Specification 0005 as a distinct alternative to TLA+/TLC and Alloy.
- **Limit:** verification applies to the Promela abstraction and selected search mode/options; it does not establish implementation conformance or normative fidelity.

<a id="r-39"></a>
### R-39 — Kani Rust Verifier
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [Kani documentation](https://model-checking.github.io/kani/)
- **Relevant concepts:** bounded model checking of Rust programs, proof harnesses, assertions, undefined-behavior checks and counterexamples.
- **Use in GovCheck:** candidate program-verification method named in Specification 0005.
- **Limit:** supported Rust features and concurrency coverage are bounded; a successful harness proves only the modeled properties under the configured bounds and toolchain.

<a id="r-40"></a>
### R-40 — Verus Rust verification
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [Verus tutorial and reference](https://verus-lang.github.io/verus/guide/)
- **Relevant concepts:** static functional-correctness verification for Rust using specifications and computer-aided proofs.
- **Use in GovCheck:** candidate program-verification method named in Specification 0005.
- **Limit:** Verus does not support all Rust features/libraries and does not claim to verify the Rust/LLVM compilers or itself; trusted components and unsupported constructs remain relevant.

<a id="r-41"></a>
### R-41 — Dafny language and verifier
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [Dafny Reference Manual](https://dafny.org/dafny/DafnyRef/DafnyRef)
- **Relevant concepts:** specification constructs, pre/postconditions, invariants, termination metrics, verification conditions and compilation.
- **Use in GovCheck:** candidate program-verification system named in Specification 0005.
- **Limit:** verified claims are relative to Dafny specifications, verifier/toolchain and trusted backends; they do not validate whether the specification captures approved policy.

<a id="r-42"></a>
### R-42 — Coq / Rocq proof assistant
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Rocq documentation and reference manuals](https://rocq-prover.org/docs) · [versioned Coq documentation archive](https://docs.rocq-prover.org/)
- **Relevant concepts:** dependent type theory, Gallina definitions and machine-checked proof terms.
- **Use in GovCheck:** Coq is named in Specification 0005; the project is now named Rocq, so both the historical and current names are recorded.
- **Limit:** a checked derivation establishes a theorem only under its definitions, axioms, imported results and kernel/toolchain assumptions; it does not establish normative adequacy.

<a id="r-43"></a>
### R-43 — Isabelle theorem prover
- **Cited by:** [0007](architecture/0007-technology-decision-framework.md), [Spec 0005](specifications/0005-assurance-model.md), [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [Isabelle documentation, tutorials and reference manuals](https://www.isabelle.in.tum.de/documentation.html)
- **Relevant concepts:** interactive theorem proving, Isabelle/HOL, formal specification and proof checking.
- **Use in GovCheck:** candidate proof assistant named in Specification 0005.
- **Limit:** proof results depend on the selected logic, theory imports, axioms and trusted prover environment; no Isabelle integration is selected.

<a id="r-44"></a>
### R-44 — KAOS and goal-oriented requirements engineering
- **Cited by:** [0013-governance-metamodel](architecture/0013-governance-metamodel.md), [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md)

- **Primary source:** [Axel van Lamsweerde, Requirements Engineering: From System Goals to UML Models to Software Specifications (2009), UCLouvain record](https://research.dial.uclouvain.be/entities/publication/ddcd5cbc-c76d-4da2-bd29-509cbf0f9399)
- **Relevant concepts:** goal refinement, obstacles, responsibility assignment and derivation from system goals to requirements and software specifications.
- **Use in GovCheck:** grounds the KAOS/GORE goal-refinement family explicitly mentioned in Architecture 0013.
- **Limit:** this is a requirements-engineering method and scholarly source, not an adopted GovCheck ontology or executable policy language.

<a id="r-45"></a>
### R-45 — CRDT foundations
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [Shapiro, Preguiça, Baquero and Zawirski, “A comprehensive study of Convergent and Commutative Replicated Data Types” (INRIA Research Report 7506, 2011)](https://dsf.berkeley.edu/cs286/papers/crdt-tr2011.pdf)
- **Relevant concepts:** state-based and operation-based replicated data types, convergence conditions, asynchronous replication and concurrent updates.
- **Use in GovCheck:** foundational source for the CRDT/co-editing discussion recovered from the Cartocortex integration study.
- **Limit:** convergence does not by itself preserve user intent, define authorization, solve persistence/transport, or guarantee that application-level invariants survive concurrent operations.

<a id="r-46"></a>
### R-46 — Yjs and Yrs
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Yjs documentation](https://docs.yjs.dev/) · [Yjs source repository](https://github.com/yjs/yjs) · [y-webrtc provider and signaling implementation](https://github.com/yjs/y-webrtc) · [Yrs Rust port](https://github.com/y-crdt/y-crdt)
- **Supplementary article:** [Serverless Yjs signaling architecture](https://medium.com/collaborne-engineering/serverless-yjs-72d0a84326a2) (design exploration, not a protocol specification).
- **Relevant concepts:** shared CRDT data types, transport-independent updates, synchronization providers and collaborative editing.
- **Use in GovCheck:** candidate implementation family explicitly compared in the Cartocortex PR #28 transport/backlog study.
- **Limit:** library behavior does not select an application data model or transport architecture; Cartocortex-specific tree moves, undo/redo, persistence and migration require separate conformance tests. The y-webrtc provider documents a mesh topology, a default connection cap and configurable signaling servers; its room password and stated protections are not an independent security audit. Scalability and access control require separate tests.

<a id="r-47"></a>
### R-47 — Automerge
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Automerge documentation](https://automerge.org/docs/) · [Automerge source repository](https://github.com/automerge/automerge)
- **Relevant concepts:** local-first CRDT documents, concurrent change merging, history and transport-agnostic synchronization.
- **Use in GovCheck:** candidate implementation explicitly compared in the Cartocortex PR #28 study.
- **Limit:** a CRDT's merge semantics do not automatically preserve domain intent or enforce application permissions; networking and storage components must be evaluated separately.

<a id="r-48"></a>
### R-48 — Loro CRDT
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Loro documentation](https://loro.dev/docs) · [Loro CRDT concepts](https://www.loro.dev/docs/concepts/crdt) · [Loro source repository](https://github.com/loro-dev/loro)
- **Relevant concepts:** movable trees/lists, rich-text CRDTs, local-first synchronization, history and time travel.
- **Use in GovCheck:** candidate explicitly highlighted in the Cartocortex PR #28 study because movable trees may fit mind-map structures.
- **Limit:** the library's feature matrix is not an independent suitability result; benchmark and test against Cartocortex's identity, move/delete, undo/redo and persistence invariants before selection.

<a id="r-49"></a>
### R-49 — WebRTC real-time communication
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [W3C WebRTC 1.0 Recommendation](https://www.w3.org/TR/webrtc/) · [IETF RFC 8835 — Transports for WebRTC](https://www.rfc-editor.org/rfc/rfc8835.html)
- **Relevant concepts:** peer connections, data channels, transport security and interaction with ICE, STUN and TURN.
- **Use in GovCheck:** primary protocol references for the peer-to-peer transport option discussed for Cartocortex co-editing.
- **Limit:** WebRTC does not define application signaling, room authorization, CRDT semantics or persistence. Peer-to-peer does not mean infrastructure-free or metadata-free.

<a id="r-50"></a>
### R-50 — ICE, STUN, TURN and relay infrastructure
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [RFC 8445 — ICE](https://www.rfc-editor.org/rfc/rfc8445.html) · [RFC 8489 — STUN](https://www.rfc-editor.org/rfc/rfc8489.html) · [RFC 8656 — TURN](https://www.rfc-editor.org/rfc/rfc8656.html) · [coturn relay implementation](https://github.com/coturn/coturn)
- **Relevant concepts:** candidate gathering and connectivity checks, NAT traversal, relay allocation and fallback when direct paths fail.
- **Use in GovCheck:** documents the precise protocol stack behind the STUN/TURN references in the Cartocortex integration discussion.
- **Limit:** STUN alone is not a NAT-traversal solution; TURN relays traffic and introduces availability, cost, privacy and operational considerations. The PDF's approximate 10–20% relay-use estimate is not supported by the cited protocol RFCs or an independent measurement source identified in this audit; treat it as a planning heuristic to validate against deployment telemetry, not as a general WebRTC rate.

<a id="r-51"></a>
### R-51 — Open Knowledge Format (OKF) v0.2
- **Cited by:** [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md)

- **Primary sources:** [Canonical OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) · [OKF v0.2 specification in the original Knowledge Catalog repository](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- **Relevant concepts:** portable knowledge bundles built from Markdown, YAML frontmatter, links, provenance, trust and lifecycle metadata.
- **Use in GovCheck:** source of the OKF storage and mind-map projection study in Cartocortex PR #27; it is the specific meaning of “OKF” in that discussion.
- **Limit:** OKF is a lightweight knowledge-bundle convention, not a graph ontology, mind-map layout model, CRDT, transport protocol or GovCheck governance standard. The old Knowledge Catalog path is a frozen snapshot; use the dedicated repository as canonical.

<a id="r-52"></a>
### R-52 — RDF 1.1 data model
- **Cited by:** [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md)

- **Primary source:** [W3C RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/) · [W3C RDF Primer](https://www.w3.org/TR/rdf-primer/)
- **Relevant concepts:** graph and dataset data model based on subject–predicate–object triples and IRIs.
- **Use in GovCheck:** foundational data model discussed for a possible shared knowledge representation across Cartocortex, MoriNet and SaussuNet.
- **Limit:** RDF is a data model, not a domain ontology, storage engine, validation language or collaboration protocol.

<a id="r-53"></a>
### R-53 — SKOS
- **Cited by:** [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md)

- **Primary source:** [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)
- **Relevant concepts:** URI-identified concepts, labels, notations, concept schemes, mappings and lightweight semantic relations.
- **Use in GovCheck:** vocabulary considered for taxonomies and concept organization in the integration study.
- **Limit:** SKOS is not a general application object model or a substitute for OWL axioms, SHACL constraints or CRDT collaboration.

<a id="r-54"></a>
### R-54 — OWL 2 Web Ontology Language
- **Cited by:** [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md)

- **Primary source:** [W3C OWL 2 Structural Specification and Functional-Style Syntax](https://www.w3.org/TR/owl-syntax/) · [W3C OWL 2 Overview](https://www.w3.org/TR/owl-overview/)
- **Relevant concepts:** formally defined ontology semantics for classes, properties, individuals and axioms.
- **Use in GovCheck:** candidate semantic layer discussed alongside RDF and SKOS in the integration study.
- **Limit:** OWL reasoning does not validate all application data constraints, preserve arbitrary source properties or provide workflow, access-control or synchronization behavior.

<a id="r-55"></a>
### R-55 — SHACL
- **Cited by:** [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md)

- **Primary source:** [W3C Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/)
- **Relevant concepts:** validation of RDF graphs against declared shapes and constraints.
- **Use in GovCheck:** candidate for structural validation of normalized knowledge graphs in the SaussuNet integration discussion.
- **Limit:** SHACL validation is not proof of semantic truth, provenance authenticity, authorization or conformance of the transformation implementation.

<a id="r-56"></a>
### R-56 — Dublin Core Metadata Terms
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [DCMI Metadata Terms specification](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- **Relevant concepts:** general-purpose metadata properties, classes and vocabulary terms for describing resources.
- **Use in GovCheck:** candidate metadata vocabulary discussed for documentary resources in the shared knowledge profile.
- **Limit:** Dublin Core terms do not define the full domain model, identity policy, access-control semantics or validation rules.

<a id="r-57"></a>
### R-57 — Bibliographic Ontology (BIBO)
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [DCMI BIBO specification](https://www.dublincore.org/specifications/bibo/bibo/) · [BIBO vocabulary project](https://dcmi.github.io/bibo/)
- **Relevant concepts:** RDF vocabulary for bibliographic resources, citations and document types.
- **Use in GovCheck:** supplementary vocabulary considered for reports, articles and bibliographic objects in the integration study.
- **Limit:** BIBO is a DCMI Community Specification, not an ISO or W3C Recommendation; it should be combined with broader metadata vocabularies only where needed.

<a id="r-58"></a>
### R-58 — Data Catalog Vocabulary (DCAT) 3
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [W3C DCAT 3 Recommendation](https://www.w3.org/TR/vocab-dcat-3/) · [W3C DCAT specification landing page](https://www.w3.org/TR/vocab-dcat/)
- **Relevant concepts:** interoperable descriptions of datasets, data services, distributions and dataset series in catalogs.
- **Use in GovCheck:** candidate vocabulary for cataloguing knowledge bundles and collections in the integration study.
- **Limit:** DCAT describes catalogued datasets/services; it does not model all content semantics, application permissions or collaborative editing.

<a id="r-59"></a>
### R-59 — W3C Web Annotation Data Model
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/)
- **Relevant concepts:** annotations, bodies, targets, selectors and motivations for annotating resources or specific fragments.
- **Use in GovCheck:** candidate model for comments, questions and annotations attached to pages or passages in the integration study.
- **Limit:** Web Annotation does not define a full knowledge graph, real-time co-editing protocol or authorization policy.

<a id="r-60"></a>
### R-60 — ActivityStreams 2.0
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [W3C ActivityStreams 2.0 Core](https://www.w3.org/TR/activitystreams-core/) · [ActivityStreams 2.0 Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/)
- **Relevant concepts:** JSON-LD vocabulary and syntax for actors, objects, activities, collections and social interactions.
- **Use in GovCheck:** considered for representing published activities/events where the social-activity use case fits.
- **Limit:** ActivityStreams is not a provenance ledger, event-sourcing guarantee, access-control model or replacement for PROV-O.

<a id="r-61"></a>
### R-61 — P-Plan ontology
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary source:** [P-Plan ontology specification](https://www.opmw.org/model/p-plan/)
- **Relevant concepts:** representation of abstract plans and their correspondence to PROV-O records of executed processes.
- **Use in GovCheck:** candidate vocabulary for describing intended ingestion/transformation plans alongside observed provenance.
- **Limit:** P-Plan is a domain ontology extending PROV-O, not a general workflow engine or W3C Recommendation.

<a id="r-62"></a>
### R-62 — Cartocortex, MoriNet and SaussuNet integration sources
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Cartocortex repository](https://github.com/complexus-lab/cartocortex) · [MoriNet repository](https://github.com/lejeunecedric/MoriNet) · [SaussuNet repository](https://github.com/lejeunecedric/SaussuNet) · [Cartocortex PR #27 — OKF storage and graph-view study](https://github.com/complexus-lab/cartocortex/pull/27) · [Cartocortex PR #28 — CRDT, browser deployment and cloud-sync backlog](https://github.com/complexus-lab/cartocortex/pull/28)
- **Provisional namespace URI:** [Cartocortex Knowledge Ontology (CKO)](https://cartocortex.dev/ontology#) — vocabulary identifier proposed in the PDF, not a standard or an adopted ontology.
- **Relevant concepts:** source repositories and reviewed design artifacts for the integration study; PR #27 is a study of OKF v0.2 storage/projections, while PR #28 contains proposed CRDT and real-time transport work.
- **Use in GovCheck:** preserves the concrete project-level sources behind the initial PDF “Évaluer l’intégration des dépôts” (6 November 2026, 224 pages) and the discussion recorded by ADR 0002.
- **Limit:** PR #27 is a study, not an executed implementation; PR #28 is a proposal/backlog and its transport study is explicitly not executed. Repository capabilities must be rechecked at the reviewed revision before claiming current behavior. The “CKO” namespace in the PDF is a proposal, not an adopted external standard.

<a id="r-63"></a>
### R-63 — Mind-map and graph interchange formats
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Freeplane documentation](https://docs.freeplane.org/) · [FreeMind project](https://freemind.sourceforge.io/wiki/index.php/Main_Page) · [XMind](https://xmind.app/) · [OPML 2.0 specification](https://opml.org/spec2.opml) · [GraphML specification](https://graphml.graphdrawing.org/specification.html)
- **Relevant concepts:** exchange of hierarchical mind maps, outlines and general graph structures, including format-specific metadata and layout information.
- **Use in GovCheck:** records the FreeMind, Freeplane, XMind, OPML and GraphML formats explicitly considered for SaussuNet import/export and Cartocortex visualization.
- **Limit:** these formats have different expressive power and metadata conventions. A successful parse is not lossless semantic round-tripping; conversion requires per-format fixtures and explicit loss reports.

<a id="r-64"></a>
### R-64 — Cloud storage APIs and S3 interoperability
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Amazon S3 documentation and API](https://docs.aws.amazon.com/s3/) · [Google Cloud Storage interoperability](https://docs.cloud.google.com/storage/docs/interoperability) · [Google Drive API overview](https://developers.google.com/workspace/drive/api/guides/about-sdk) · [Microsoft Graph Drive resource](https://learn.microsoft.com/en-us/graph/api/drive-get?view=graph-rest-1.0) · [Azure Blob Storage introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) · [Hippius documentation](https://docs.hippius.com/) · [Hippius S3-compatible object storage](https://docs.hippius.com/storage/s3/)
- **Relevant concepts:** object-storage APIs, S3-compatible endpoints, cloud-drive APIs, OAuth/credential scopes, client-side synchronization and provider-specific semantics.
- **Use in GovCheck:** preserves the storage-provider integration candidates named in Cartocortex PR #28: Amazon S3, Google Cloud Storage interoperability, Google Drive, OneDrive/Microsoft Graph, Azure Blob Storage and Hippius.
- **Limit:** “S3-compatible” does not mean identical semantics, consistency, IAM, versioning, eventing or multipart behavior. Provider APIs have distinct authentication and permission models. These were backlog candidates, not selected providers or implemented integrations.

<a id="r-65"></a>
### R-65 — Browser file access, local persistence and WebAssembly
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [MDN File System API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API) · [MDN Origin Private File System (OPFS)](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system) · [W3C Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB-3/) · [WebAssembly specifications](https://webassembly.org/specs/) · [WebAssembly System Interface (WASI)](https://github.com/WebAssembly/WASI)
- **Relevant concepts:** user-mediated access to local files/directories, origin-private browser storage, IndexedDB persistence and WebAssembly execution interfaces.
- **Use in GovCheck:** preserves the browser-local deployment and persistence candidates named in Cartocortex PR #28, including File System Access, OPFS, IndexedDB and the conditional use of WebAssembly/WASI to reuse Rust code.
- **Limit:** browser APIs have support, permission, secure-context and quota constraints; OPFS is origin-private and not a user-visible directory. WASI is a system interface for WebAssembly runtimes, not a browser file-system permission bypass. The PR describes a proposed study/backlog, not a tested deployment.

<a id="r-66"></a>
### R-66 — Hyperswarm and HyperDHT peer discovery
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)

- **Primary sources:** [Hyperswarm project](https://github.com/holepunchto/hyperswarm) · [HyperDHT implementation](https://github.com/holepunchto/hyperdht) · [Hyperswarm peer-discovery documentation](https://docs.pears.com/p2p/reference/building-blocks/hyperswarm/)
- **Relevant concepts:** topic-based peer discovery, distributed hash-table rendezvous, UDP hole punching and encrypted peer connections.
- **Use in GovCheck:** preserves the desktop peer-discovery alternative discussed in Cartocortex PR #28 alongside browser WebRTC signaling.
- **Limit:** Hyperswarm/HyperDHT is a separate networking stack, not browser-native WebRTC signaling. DHT operation depends on bootstrap infrastructure and network reachability; peer discovery does not define application room authorization, membership policy or persistence.

<a id="r-67"></a>
### R-67 — WebDAV, Model Context Protocol and Markdown wiki conventions
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [IETF RFC 4918 — WebDAV](https://www.rfc-editor.org/rfc/rfc4918.html) · [Model Context Protocol specification, version 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic) · [MCP specification repository](https://github.com/modelcontextprotocol/modelcontextprotocol) · [CommonMark 0.31.2 specification](https://spec.commonmark.org/0.31.2/) · [Obsidian Markdown syntax documentation](https://obsidian.md/help/syntax) · [mdBook documentation](https://rust-lang.github.io/mdBook/)
- **Relevant concepts:** remote authoring and locking over HTTP (WebDAV), tools/resources/prompts over MCP, Markdown syntax, Obsidian-specific extensions and rendering Markdown knowledge bases with mdBook.
- **Use in GovCheck:** preserves the external protocols and document conventions explicitly named in the integration assessment for SaussuNet/MoriNet source ingestion and wiki exposure.
- **Limit:** WebDAV and MCP are different protocols with distinct security and authorization models. CommonMark is a baseline, not the complete Obsidian dialect. The PDF describes project interfaces and intended integration; it does not prove that each adapter or server path is implemented or secure.

<a id="r-68"></a>
### R-68 — Related GovCheck ecosystem repositories reviewed in the integration assessment
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [Pijulation](https://github.com/Martin-PB/Pijulation) · [Git–Pijul bridge](https://github.com/Martin-PB/passerelle-Git-Pijul)
- **Relevant concepts:** adjacent projects used as context for native Git/Pijul semantics, patch-graph interoperability, governance and formal assurance practices.
- **Use in GovCheck:** preserves the public repository sources named in the initial assessment.
- **Limit:** the assessment also examined private Hermes Nix and NixOS SecOps repositories; their private URLs are intentionally not reproduced in this public catalogue. “Mix”, “CCOp Agent” and a distinct standalone “Nix” repository were not uniquely identified in the assessment; no guessed links are supplied. This entry is context, not evidence that these projects are dependencies of GovCheck.

<a id="r-69"></a>
### R-69 — Cartocortex mind-map format and tool interoperability source inventory (PR #9)
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary project sources:** [Cartocortex PR #9 — mind-map format panorama](https://github.com/complexus-lab/cartocortex/pull/9) · [Cartocortex PR #1](https://github.com/complexus-lab/cartocortex/pull/1) · [PR #3](https://github.com/complexus-lab/cartocortex/pull/3) · [PR #4](https://github.com/complexus-lab/cartocortex/pull/4) · [PR #5](https://github.com/complexus-lab/cartocortex/pull/5) · [PR #6](https://github.com/complexus-lab/cartocortex/pull/6) · [PR #8](https://github.com/complexus-lab/cartocortex/pull/8)
- **Source implementations and fixtures:** [Freeplane source](https://github.com/freeplane/freeplane) · [WiseMapping frontend serializers/importer](https://github.com/wisemapping/wisemapping-frontend) · [Mindomo public backup fixture](https://github.com/aarontmaher/Lauburu-Monorepo) · [MultiMarkdown 6](https://github.com/fletcher/MultiMarkdown-6) · [SimpleMind test fixture](https://github.com/pahund/simple-mind-search) · [xmind2smmx exporter](https://github.com/BartRuSec/xmind2smmx) · [SimpleMind MCP reader/writer](https://github.com/kharabiner/simplemind-mcp-server)
- **Vendor and product documentation:** [XMind export guide](https://xmind.com/fr/user-guide/export-new) · [MindManager 2017 User Guide](https://www.mindmanager.com/static/mm/docs/MindManager_2017_User_Guide_EN.pdf) · [MindManager Microsoft integrations](https://www.mindmanager.com/en/integrations/microsoft/) · [Mindomo getting started](https://help.mindomo.com/getting-started/) · [Mindomo import](https://help.mindomo.com/basics/import-mind-maps/) · [Mindomo export](https://help.mindomo.com/basics/export-mind-maps/) · [iThoughts vendor compatibility FAQ](https://www.toketaware.com/ithoughts-faq-compatibility) · [SimpleMind export](https://simplemind.eu/faq/share-export-in-different-formats/) · [SimpleMind importable files](https://simplemind.eu/faq/what-files-can-simplemind-import/) · [SimpleMind import/export help group](https://simplemind.eu/faq_group/share-export-and-import/) · [MindMeister export](https://support.mindmeister.com/hc/en-us/articles/360017447280-Export-Your-Mind-Map) · [MindMeister iOS export/print](https://support.mindmeister.com/hc/en-us/articles/115000807204-Export-or-Print-your-Map-on-iOS) · [MindMeister import](https://support.mindmeister.com/hc/en-us/articles/360017498199-Import-Text-Files-and-Mind-Maps-into-MindMeister) · [Coggle import](https://coggle.help/article/34-import-files-into-coggle) · [Coggle blog on .mm import](https://bloggle.coggle.it/post/129486892657/import-other-files-to-coggle) · [Coggle export](https://coggle.help/article/20-export-options) · [Coggle supported export formats](https://coggle.help/article/105-supported-export-formats) · [Bubbl.us help](https://bubbl.us/help/topics.htm) · [Ayoa iMindMap import](https://support.ayoa.com/opening-imindmap-files-in-ayoa)
- **Secondary and non-normative references:** [XMind export help mirror (not verified as vendor documentation)](https://xmind-help.github.io/en/export.html) · [FileInfo .mind](https://fileinfo.com/extension/mind) · [FileInfo .imx](https://fileinfo.com/extension/imx) · [File-Extensions .nm5](https://www.file-extensions.org/nm5-file-extension) · [Mind Mapping Software import/export comparison](https://mindmappingsoftwareblog.com/wp-content/99nc2r/MMS_Import_Export_Comparison.pdf) · [Lucidchart community export request](https://community.lucid.co/ideas/exporting-mind-maps-created-in-lucidchart-to-microsoft-powerpoint-or-word-374) · [Lucidchart export overview](https://mindmap.guide/post/7-amazing-enterprise-mindmap-tools-with-powerful-export-options/) · [MindManager task export write-up](https://sociamind.com/2015/11/04/exporting-a-simple-task-table-or-to-do-list-from-mindmanager/) · [Bubbl.us feature walkthrough](https://edrawmind.wondershare.com/mind-map/bubble-us-mind-map.html)
- **Relevant concepts:** import/export capabilities, file-container formats, semantic map content, outline and graph structures, office integrations, source-level serializers and real-file fixtures.
- **Use in GovCheck:** preserves the full source trail behind the format panorama cited by the initial 224-page integration assessment, including source code/fixtures and official vendor documentation.
- **Limit:** PR #9 is an open documentation PR, not a format implementation or conformance suite. PRs #1 and #3 are closed; PRs #4, #5, #6, #8 and #9 are open at this audit date (7 November 2026). A linked PR is not proof of a merged integration or production-ready implementation. The panorama records evidence available at its review date (2026-10-18). FileInfo, blogs and community posts are secondary sources, not format specifications. A feature in a product UI does not prove lossless file interchange; the source PR and per-format fixtures must be rechecked before implementation decisions. An iThoughts reference gist attributed to B. Terpstra is named in the source PR, but its URL was not preserved; no guessed link is supplied.

<a id="r-70"></a>
### R-70 — Wei et al., “ACCESS: Assurance Case Centric Engineering of Safety-critical Systems” (2024)
- **Cited by:** [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [concurrent-agent-change-governance](research/concurrent-agent-change-governance.md)
- **Primary source:** [Journal of Systems and Software article](https://doi.org/10.1016/j.jss.2024.112034) · [open repository copy](https://eprints.whiterose.ac.uk/id/eprint/211554/)
- **Bibliographic reference:** Ran Wei, Simon Foster, Haitao Mei, Fang Yan, Ruizhe Yang, Ibrahim Habli, Colin O’Halloran, Nick Tudor, Tim Kelly and Yakoub Nemouchi, *Journal of Systems and Software* 213 (2024), article 112034.
- **Relevant concepts:** model-based assurance cases using SACM; traceability to heterogeneous engineering artifacts; automated evaluation, change-impact analysis, formal-method evidence and dynamic runtime assurance-case evaluation.
- **Use in GovCheck:** demonstrates a research-backed pattern for co-evolving assurance cases with engineering artifacts and evaluating their validity using runtime data.
- **Limit:** the paper presents a methodology, prototype and case study, not a general-purpose production-ready security-risk governance engine. Its scope and tooling maturity must not be overstated.

<a id="r-71"></a>
### R-71 — Bloomfield and Rushby, “Assurance 2.0: A Manifesto” (2021)
- **Cited by:** [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [SRI author page and paper](https://www.csl.sri.com/users/rushby/abstracts/sss21) · [arXiv manuscript](https://arxiv.org/abs/2004.10474)
- **Bibliographic reference:** Robin Bloomfield and John Rushby, *Systems and Covid-19: Proceedings of the 29th Safety-Critical Systems Symposium*, 2021, pp. 85–108.
- **Relevant concepts:** stronger scrutiny of reasoning and evidence; explicit defeaters and counterevidence; assessment of evidence weight and discrimination between a claim and its negation.
- **Use in GovCheck:** motivates explicit counterclaims, defeaters, contradictory observations and evidence-quality/strength assessments rather than a one-sided graph of supporting evidence.
- **Limit:** Assurance 2.0 is an assurance approach/manifesto, not a complete operational event schema, risk-acceptance authority model or universal numeric scoring method.

<a id="r-72"></a>
### R-72 — Ericsson, “Runtime threat modeling for attack prediction and defense” (2025)
- **Cited by:** [0006-threat-and-trust-model](architecture/0006-threat-and-trust-model.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [concurrent-agent-change-governance](research/concurrent-agent-change-governance.md)
- **Primary source:** [Ericsson engineering article](https://www.ericsson.com/en/blog/2025/12/runtime-threat-modeling-for-attack-prediction-and-defense)
- **Relevant concepts:** combining telemetry, configuration state and asset/context changes with threat knowledge; observation-driven threat hypotheses; control-effectiveness assessment and feedback loops.
- **Use in GovCheck:** industrial example of connecting production observability to evolving threat models and control assessment.
- **Limit:** this is an industry engineering article focused on radio access networks, not a neutral standard or proof that predictive scores are calibrated. GovCheck should preserve provenance, uncertainty and human-governed decisions rather than importing its scoring/automation assumptions.

<a id="r-73"></a>
### R-73 — OMG Structured Assurance Case Metamodel (SACM), Version 2.4 Beta 1 (September 2026)
- **Cited by:** [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md), [sacm24-beta1-interoperability-risk](research/sacm24-beta1-interoperability-risk.md), [sacm24-claim-inference-mapping](research/sacm24-claim-inference-mapping.md), [metamodel semantic-coverage audit](research/metamodel-semantic-coverage-audit.md)
- **Primary sources:** [OMG SACM 2.4 Beta 1 specification page](https://www.omg.org/spec/SACM/2.4/Beta1) · [PDF specification artifact (normative within the Beta 1 package)](https://www.omg.org/spec/SACM/2.4/Beta1/PDF) · [machine-readable metamodel XML (normative within the Beta 1 package), 2026-05-04](https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml). The beta package is informational/in-process; SACM 2.3 remains the formal adopted baseline.
- **Relevant issue resolutions:** [SACM24-83 explicit Claim subject](https://issues.omg.org/issues/SACM24-83) · [SACM24-75 Assessment](https://issues.omg.org/issues/SACM24-75) · [SACM24-77 advanced arguments](https://issues.omg.org/issues/SACM24-77) · [SACM24-48 inference/relationship semantics](https://issues.omg.org/issues/SACM24-48).
- **Relevant concepts:** explicit Claim subject via SACMElement; AssertionDeclarationKind (asserted, assumed, axiomatic, byRule); optional assertion truth/value/rule structures; InferenceTypeKind (probable, collective, necessary, sufficient, necessaryAndSufficient, byRule); AssertionRule and InferenceRule; assessment and advanced-argument extensions.
- **Use in GovCheck:** source-native semantic comparison and mapping target. The first formal slice preserves assertion-declaration distinctions, explicit subject/revision, and inference direction; probable inference remains outside classical implication until a probability semantics is supplied.
- **Limit:** 2.4 is a beta, not a formal adopted specification. GovCheck must not treat its draft constructs as stable contracts or claim full conformance. Preserve 2.3 as the current formal baseline pending final 2.4 review.

<a id="r-74"></a>
### R-74 — Hoover, Rosso-Llopart and Taran, *Evaluating Project Decisions: Case Studies in Software Engineering* (2009/2010)
- **Cited by:** [0013-governance-metamodel](architecture/0013-governance-metamodel.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel semantic-coverage audit](research/metamodel-semantic-coverage-audit.md)
- **Primary sources:** [PEAK section in Chapter 1 (InformIT)](https://www.informit.com/articles/article.aspx?p=1409781&seqNum=3) · [O’Reilly publisher book page](https://www.oreilly.com/library/view/evaluating-project-decisions/9780321685629/)
- **Bibliographic reference:** Carol L. Hoover, Mel Rosso-Llopart and Gil Taran, Addison-Wesley Professional, first published October 2009 (copyright 2010), ISBN 978-0-321-54456-8; Chapter 1, §1.3 introduces the PEAK decision model.
- **Relevant concepts:** Problem, Experience, Assumptions and Knowledge as decision inputs; a decision process produces a solution and an assumed risk.
- **Use in GovCheck:** supplies a decision-review lens for making the problem formulation, experiential basis, assumptions, factual knowledge, selected solution and accepted risk explicit and traceable.
- **Limit:** PEAK is a decision model, not a threat taxonomy, assurance-case metamodel, risk-calculation algorithm or normative governance standard. It does not prescribe a serialization or authorization model.

<a id="r-75"></a>
### R-75 — NIST SP 800-137, Information Security Continuous Monitoring (2011)
- **Cited by:** [0006-threat-and-trust-model](architecture/0006-threat-and-trust-model.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [concurrent-agent-change-governance](research/concurrent-agent-change-governance.md)
- **Primary source:** [NIST publication](https://csrc.nist.gov/pubs/sp/800/137/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-137)
- **Relevant concepts:** continuous visibility into assets, threats, vulnerabilities and deployed-control effectiveness; monitoring aligned with organizational risk tolerance; response when observations show controls are inadequate.
- **Use in GovCheck:** supports a production feedback loop in which observations update system posture, control assessments and risk decisions rather than leaving threat models frozen at design time.
- **Limit:** monitoring data is not automatically a validated incident, threat or assurance conclusion. Coverage, collection integrity, context, uncertainty and control-monitor health must be assessed.

<a id="r-76"></a>
### R-76 — Rushby, “Runtime Certification” (RV 2008)
- **Cited by:** [0006-threat-and-trust-model](architecture/0006-threat-and-trust-model.md), [0010-assurance-proof-and-conformance](architecture/0010-assurance-proof-and-conformance.md), [0021-assurance-claims-and-freshness](architecture/0021-assurance-claims-and-freshness.md), [0025-runtime-observations-peak-and-sacm](architecture/0025-runtime-observations-peak-and-sacm.md), [concurrent-agent-change-governance](research/concurrent-agent-change-governance.md)
- **Primary source:** [Author's paper, presented at the Eighth Workshop on Runtime Verification](https://citeseerx.ist.psu.edu/document?doi=c28045b0a573839028f6042870a3eccd8f9be748&repid=rep1&type=pdf)
- **Bibliographic reference:** John Rushby, “Runtime Certification,” invited paper at RV 2008, Budapest, April 2008.
- **Relevant concepts:** assurance cases as claims, evidence and arguments; monitoring assumptions and anomalies at runtime; using runtime verification as evidence; detecting violated environmental assumptions.
- **Use in GovCheck:** directly supports linking declared assumptions to monitorable conditions and allowing production observations to challenge assumptions and trigger reassessment of assurance claims.
- **Limit:** runtime monitors only establish properties within their formalized scope and observation boundary. An anomaly or assumption violation is not automatically a confirmed attack or proof of system failure.

<a id="r-77"></a>
### R-77 — Policy-as-code and MCP tool-governance enforcement examples
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [HashiCorp Sentinel documentation](https://developer.hashicorp.com/sentinel/docs) · [Consul MCP Gateway documentation](https://docs.hashicorp.com/consul/docs/agentic-mesh/mcp-gateway) · [GitLab agent tool governance and MCP server blocking](https://docs.gitlab.com/user/ai-governance/tool-governance/) · [Vectimus source repository](https://github.com/vectimus/vectimus) · [OPA Agent Tool Calling documentation](https://www.openpolicyagent.org/docs/agent-tool-calling)
- **Relevant concepts:** policy-as-code, policy evaluation at infrastructure and agent-tool boundaries, MCP server allow/block controls, namespace-scoped governance, approval evidence, audit events and deterministic Cedar-based hooks.
- **Use in GovCheck:** preserves the policy enforcement and MCP governance systems compared in the wider project discussions, alongside OPA (R-09) and Cedar (R-10).
- **Limit:** Sentinel is an enterprise HashiCorp feature; Consul MCP Gateway documentation marks the feature beta. GitLab's blocking scope is product/version/surface-specific. Vectimus is a project repository whose security and performance claims are not independently established by its README. These examples do not imply selection, equivalence or GovCheck integration.

<a id="r-78"></a>
### R-78 — NIST OSCAL and the Continuous Compliance Framework (CCF)
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [NIST OSCAL project](https://pages.nist.gov/OSCAL/) · [OSCAL source repository](https://github.com/usnistgov/OSCAL) · [Compliance Framework / CCF documentation](https://compliance-framework.github.io/docs/introduction) · [Compliance Framework repositories](https://github.com/compliance-framework)
- **Relevant concepts:** machine-readable security-control catalogs, profiles, system security plans, assessment plans/results and structured compliance evidence in XML, JSON and YAML; continuous evidence collection and reporting.
- **Use in GovCheck:** preserves the OSCAL and CCF options discussed for representing controls, collecting evidence and producing structured assessment outputs.
- **Limit:** OSCAL is a set of information models/formats, not a complete compliance engine or proof of control effectiveness. CCF is a separate implementation that uses policy engines and collectors; its project claims are not a normative standard or independent certification. A GovCheck mapping would require explicit control semantics, evidence provenance and scope.

<a id="r-79"></a>
### R-79 — Agent sandboxing and runtime isolation: nono, Landlock and Docker Sandboxes
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [nono project and security model](https://github.com/nolabs-ai/nono) · [nono documentation site](https://nono.sh/) · [Linux Landlock kernel documentation](https://docs.kernel.org/userspace-api/landlock.html) · [Docker Sandboxes documentation](https://docs.docker.com/ai/sandboxes/) · [Goose AI agent project](https://github.com/aaif-goose/goose)
- **Relevant concepts:** per-tool capability scoping, filesystem/network restrictions, credential brokering, kernel-enforced unprivileged sandboxing, microVM isolation and agent runtime orchestration.
- **Use in GovCheck:** preserves the runtime-isolation and agent-execution options discussed in the wider GovCheck/security architecture context. Goose is included as an agent harness example, not as a sandbox.
- **Limit:** Landlock support and available restrictions depend on kernel configuration and ABI; it is one layer, not a complete VM/container boundary. nono and Docker Sandboxes have their own trust, policy and operational assumptions; vendor/project claims require independent testing. Goose is an agent runtime, not an authorization authority.

<a id="r-80"></a>
### R-80 — Matrix protocol and Element X client
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [Matrix protocol specification](https://spec.matrix.org/latest/) · [Matrix specification source repository](https://github.com/matrix-org/matrix-spec) · [Element X on the Matrix.org ecosystem](https://matrix.org/ecosystem/clients/element-x/)
- **Relevant concepts:** federated real-time communication, homeservers, rooms, event synchronization, end-to-end encryption and mobile Matrix client behavior.
- **Use in GovCheck:** preserves the Matrix/Element X communication option discussed for agent and human collaboration.
- **Limit:** Matrix is a communication protocol and ecosystem, not a governance or authorization model for GovCheck. Room membership and encryption do not by themselves establish project-level policy, agent identity binding or durable decision provenance.

<a id="r-81"></a>
### R-81 — SearXNG metasearch
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary source:** [SearXNG documentation](https://docs.searxng.org/)
- **Relevant concepts:** self-hosted metasearch aggregation, configurable upstream search engines, privacy-oriented query handling and administration.
- **Use in GovCheck:** preserves the self-hosted search service discussed as a source-discovery component in the wider project context.
- **Limit:** SearXNG aggregates third-party search results; it does not validate source authority, freshness, accuracy or licensing. Search output must be resolved to and checked against primary sources.

<a id="r-82"></a>
### R-82 — Microsoft MarkItDown document-to-Markdown conversion
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary source:** [Microsoft MarkItDown source repository and documentation](https://github.com/microsoft/markitdown)
- **Relevant concepts:** conversion of PDF, Office and other document formats into Markdown for indexing and text analysis.
- **Use in GovCheck:** preserves the document-ingestion utility discussed for extracting and reviewing source material such as PDFs and office files.
- **Limit:** MarkItDown performs I/O with the privileges of its current process. Its own documentation warns that untrusted inputs must be sanitized and conversion should run with the narrowest needed access. Conversion output is an extraction, not proof of source completeness or semantic fidelity.


<a id="r-83"></a>
### R-83 — JSON-LD 1.1
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary source:** [W3C JSON-LD 1.1 Recommendation](https://www.w3.org/TR/json-ld/)
- **Relevant concepts:** JSON-based serialization of linked data; contexts, IRI expansion, graph and dataset representation, and integration with deployed JSON-based systems.
- **Use in GovCheck:** candidate interchange syntax for RDF-based knowledge and metadata when JSON-native tooling and web-service integration are useful.
- **Limit:** JSON-LD is a serialization and processing model, not a domain ontology, policy language or validation system. It does not decide which vocabulary or assertions are appropriate.

<a id="r-84"></a>
### R-84 — RDF 1.1 Turtle syntax
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary source:** [W3C RDF 1.1 Turtle Recommendation](https://www.w3.org/TR/turtle/)
- **Relevant concepts:** compact, text-oriented concrete syntax for expressing RDF triples and graphs.
- **Use in GovCheck:** candidate human-readable serialization for examples, fixtures and exchange of RDF graph data.
- **Limit:** Turtle is a syntax, not a vocabulary, ontology, constraint language or proof of semantic correctness. It does not replace RDF's abstract data model.

<a id="r-85"></a>
### R-85 — SIOC Core Ontology
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary source:** [SIOC Core Ontology Specification](https://rdfs.org/sioc/spec/)
- **Relevant concepts:** semantic description of online communities, discussion spaces, posts, users/accounts and relationships between community content.
- **Use in GovCheck:** candidate vocabulary if discussions, comments or community publications need interoperable semantic representation.
- **Limit:** SIOC is an evolving community ontology, not an authorization model or a complete provenance system. It should not replace PROV-O for derivation provenance or Web Annotation for targeted annotations; no adoption is implied.

<a id="r-86"></a>
### R-86 — Schema.org DigitalDocument
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary source:** [Schema.org DigitalDocument type](https://schema.org/DigitalDocument)
- **Relevant concepts:** lightweight description of digital documents as web resources, including their relation to broader CreativeWork metadata.
- **Use in GovCheck:** candidate general-purpose vocabulary for describing document resources when its properties fit the exchange context.
- **Limit:** Schema.org is broad web metadata vocabulary, not a governance ontology, access-control system, evidence-admissibility rule or replacement for domain-specific vocabularies. Use only the terms that match the intended semantics.

<a id="r-87"></a>
### R-87 — WebTorrent browser peer-to-peer transport and discovery
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [WebTorrent official repository](https://github.com/webtorrent/webtorrent) · [WebTorrent website and documentation](https://webtorrent.io/)
- **Relevant concepts:** BitTorrent client for browsers and Node.js; peer-to-peer transport over WebRTC data channels in browsers; discovery through trackers, DHT, local peer discovery and peer exchange.
- **Use in GovCheck:** preserves WebTorrent as a transport/discovery option discussed in the Cartocortex PR #28 transport study, distinct from y-webrtc and Hyperswarm/HyperDHT.
- **Limit:** WebTorrent is a content-sharing protocol and implementation, not a generic presence or CRDT synchronization service. Browser WebTorrent peers communicate only with compatible WebTorrent/WebRTC clients; discovery, room security, application authorization and persistence must be addressed separately. No adoption is implied.

<a id="r-88"></a>
### R-88 — NIST SP 800-192: Verification and Test Methods for Access Control Policies/Models
- **Cited by:** [0013-governance-metamodel](architecture/0013-governance-metamodel.md), [0015-governance-conformance-and-validation-plan](architecture/0015-governance-conformance-and-validation-plan.md), [0022-governance-capability-audit](architecture/0022-governance-capability-audit.md), [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md), [0002-canonical-governance-model](specifications/0002-canonical-governance-model.md), [0006-governance-revision-applicability](specifications/0006-governance-revision-applicability.md)
- **Primary sources:** [NIST SP 800-192 publication record](https://csrc.nist.gov/pubs/sp/800/192/final) · [NIST DOI](https://doi.org/10.6028/NIST.SP.800-192)
- **Relevant concepts:** verification and testing of access-control policies and models; inconsistency, incompleteness, safety requirements, black-box/white-box model checks and tests derived from policy models.
- **Use in GovCheck:** direct support for validating normative policy models before testing their evaluators or enforcement mechanisms. An executable policy is not necessarily a correct, complete or coherent policy.
- **Limit:** the publication focuses on access-control policies/models and their implementations. It is not a complete governance metamodel, an authorization language, or evidence that OPA/Cedar policies are verified by GovCheck.

<a id="r-89"></a>
### R-89 — B Method and Atelier B
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md), [0005](specifications/0005-assurance-model.md), [0007](architecture/0007-technology-decision-framework.md)
- **Primary sources:** [J.-R. Abrial, The B-Book (Cambridge University Press)](https://www.cambridge.org/core/books/abs/bbook/frontmatter/20E71F1E161387417D3E347D07E247A6) · [Atelier B presentation of the B method](https://www.atelierb.eu/en/presentation-of-the-b-method/) · [Atelier B online documentation](https://www.atelierb.eu/en/atelier-b-tools/online-documentation/)
- **Relevant concepts:** set-theoretic formal specification, abstract machines, invariants, generalized substitutions, proof obligations, refinement and construction of implementations from progressively refined models.
- **Use in GovCheck:** preserves B as a candidate formal-specification/refinement method in the wider assurance-method inventory, especially where state and invariant preservation are central.
- **Limit:** proving B-model obligations does not by itself establish that natural-language requirements are complete, that the model captures the intended system, or that generated/handwritten code and runtime behavior conform. No B toolchain is selected or adopted.

<a id="r-90"></a>
### R-90 — Z formal specification notation (ISO/IEC 13568:2002)
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md), [0005](specifications/0005-assurance-model.md), [0007](architecture/0007-technology-decision-framework.md)
- **Primary sources:** [ISO/IEC 13568:2002 — Z syntax, type system and semantics](https://www.iso.org/standard/21573.html) · [Technical Corrigendum 1:2007](https://www.iso.org/standard/46112.html)
- **Relevant concepts:** mathematical notation for formal specifications; syntax, type system, semantics and a toolkit of mathematical operators.
- **Use in GovCheck:** records Z as a candidate formal-specification notation for precise state/data constraints and abstract system descriptions.
- **Limit:** ISO/IEC 13568 standardizes the notation's syntax, type system and semantics; it explicitly does not prescribe a method for using Z. A notation standard is not a proof of a particular model or its refinement to implementation. The ISO record states that the 2002 edition was reviewed and confirmed in 2026.

<a id="r-91"></a>
### R-91 — Communicating Sequential Processes (CSP) and FDR
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md), [0005](specifications/0005-assurance-model.md), [0007](architecture/0007-technology-decision-framework.md)
- **Primary sources:** [C. A. R. Hoare, Communicating Sequential Processes (Oxford electronic edition)](https://www.cs.ox.ac.uk/ucs/hoarebook.pdf) · [FDR4 model checker documentation](https://cocotec.io/fdr/manual/index.html)
- **Relevant concepts:** process algebra for communicating concurrent components; traces, failures and divergences; refinement checking, deadlock/livelock and safety/liveness analysis with FDR.
- **Use in GovCheck:** candidate formalism for concurrency and interaction models where process behavior and refinement are the claim under review.
- **Limit:** CSP/FDR addresses concurrent process behavior; it is not a general-purpose governance policy language, an implementation proof for arbitrary code, or a substitute for lifecycle/authority modeling. The CSP here is Hoare's process algebra, not the unrelated CSP educational edition name used by Atelier B.

<a id="r-92"></a>
### R-92 — iStar 2.0 goal-oriented requirements modeling
- **Cited by:** [0013-governance-metamodel](architecture/0013-governance-metamodel.md), [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [Dalpiaz, Franch and Horkoff, iStar 2.0 Language Guide (arXiv:1605.07767)](https://arxiv.org/abs/1605.07767)
- **Relevant concepts:** actor-centered goal modeling, intentional and social dependencies, goals, qualities, tasks and resources; a shared core vocabulary for goal-oriented requirements engineering.
- **Use in GovCheck:** preserves iStar as a candidate complement to KAOS/GORE for relating stakeholder goals, actors, dependencies and derived requirements.
- **Limit:** the guide describes a community-defined core language and notes its intended evolution. Goal modeling does not itself prove feasibility, resolve normative authority, verify implementation or quantify accepted risk. No iStar tool or notation is selected.

<a id="r-93"></a>
### R-93 — Deontic logic and normative modalities
- **Cited by:** [0013-governance-metamodel](architecture/0013-governance-metamodel.md), [0015-governance-conformance-and-validation-plan](architecture/0015-governance-conformance-and-validation-plan.md), [0022-governance-capability-audit](architecture/0022-governance-capability-audit.md), [0002-study-placement](decisions/0002-study-placement.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md), [0002-canonical-governance-model](specifications/0002-canonical-governance-model.md)
- **Primary sources:** [G. H. von Wright, “Deontic Logic”, Mind (1951)](https://doi.org/10.1093/mind/LX.237.1) · [Stanford Encyclopedia of Philosophy, Deontic Logic](https://plato.stanford.edu/entries/logic-deontic/)
- **Relevant concepts:** formal reasoning about obligation, permission, prohibition, optionality, omission and related normative statuses.
- **Use in GovCheck:** provides a logical vocabulary for expressing obligations, permissions and prohibitions in a normative governance model, and for distinguishing these modalities from descriptive facts.
- **Limit:** deontic logic alone does not define who has authority to issue a rule, its scope, priority, delegation, exception, effective time, evidence or enforcement. Standard systems also have known paradoxes and expressive limitations; the logic must be embedded in a richer, explicitly governed model.

## Reference discipline and unresolved provenance

1. Prefer the standard body, publisher, official documentation or source repository over secondary summaries.
2. R-12 was retired when its duplicate Scorecard entry was consolidated into R-08. R-101 was retired because it duplicated the NIST SP 800-218 source already maintained in R-02. Neither identifier may be reused.
3. Pin code assessments. Writ and Privateer links identify the revisions reviewed in Architecture 0016; refresh the pins before claims about current behavior.
4. Distinguish evidence classes. A standard, research paper, product documentation, source code, test result and model-checking report are different evidence types.
5. No implied adoption. Inclusion means “relevant to assess,” not “selected,” “required,” “compatible” or “implemented.”
6. No invented bibliography. The prior discussion mentioned “Agent Package Manager” but did not preserve a unique, verified project URL. It is intentionally not cited as an identified product until its identity is established.
7. Keep links close to claims. Architecture records should link to the few sources that support their specific claim and point here for the wider bibliography.


<a id="r-94"></a>
### R-94 — OMG business decision, motivation and process standards
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary sources:** [OMG specifications catalogue](https://www.omg.org/specifications/) · [DMN 1.6](https://www.omg.org/spec/DMN/1.6/) · [DMN 1.7 Beta 1](https://www.omg.org/spec/DMN/1.7/Beta1) · [BPMN 2.0.2](https://www.omg.org/spec/BPMN/) · [CMMN 1.1](https://www.omg.org/spec/CMMN/1.1) · [Business Motivation Model 1.3](https://www.omg.org/spec/BMM/1.3/) · [SBVR 1.5](https://www.omg.org/spec/SBVR)
- **Relevant concepts:** decision requirements, decision tables and FEEL; process activities, events and gateways; adaptive case management; business goals and influencers; formal business vocabularies and rules.
- **Use in GovCheck:** primary specifications for complementary decision-logic, process, case-management, motivation and business-rule candidates discussed in the project.
- **Limit:** these specifications address different semantic layers. A decision result, process transition, case task or business rule does not itself confer repository authority, approval or risk acceptance. The OMG catalogue changes; use version-specific links for pinned baselines. Its September 2026 snapshot lists DMN 1.6 as formal and 1.7 Beta 1 as in process.

<a id="r-95"></a>
### R-95 — OMG engineering, risk, testing, requirements, metrics and provenance models
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary sources:** [RAAML 1.1](https://www.omg.org/spec/RAAML/1.1) · [RAAML 1.2 Beta 1](https://www.omg.org/spec/RAAML/1.2/Beta1) · [SysML v2](https://www.omg.org/spec/SysML/2.0) · [SysML v2 overview](https://www.omg.org/sysml/sysmlv2/) · [UTP 2.3 Beta 1](https://www.omg.org/spec/UTP2) · [ReqIF 1.2](https://www.omg.org/spec/ReqIF/1.2) · [Structured Metrics Metamodel 1.2](https://www.omg.org/spec/SMM/1.2) · [PPMN 1.0](https://www.omg.org/spec/PPMN/)
- **Relevant concepts:** risk/safety analysis; systems requirements, structure, behavior and verification; model-based test specification; requirements exchange; measurement definitions/results; provenance of entities, activities and agents.
- **Use in GovCheck:** primary sources for candidate engineering-domain models, including machine-readable model and exchange artifacts where published.
- **Limit:** these models are not interchangeable and provide no common governance authority. Versions and maturity differ: RAAML 1.1 is formal and 1.2 Beta 1 is in process; UTP 2.3 is Beta 1; SysML 2.0, ReqIF 1.2, SMM 1.2 and PPMN 1.0 are formal catalogue entries. Verify pinned versions and implementation support before adoption.

<a id="r-96"></a>
### R-96 — ISO/IEC/IEEE 42010:2022, architecture description
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html)
- **Relevant concepts:** requirements for architecture descriptions, description frameworks, viewpoints, model kinds and conformance.
- **Use in GovCheck:** candidate normative foundation for structuring architecture descriptions, stakeholder concerns, views and viewpoints.
- **Limit:** it does not prescribe the architecture process, modelling language, notation, tool or recording format; it is not a universal architecture modelling language.

<a id="r-97"></a>
### R-97 — ISO/IEC/IEEE 29148, requirements engineering
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary sources:** [ISO/IEC/IEEE DIS 29148, third edition (2026)](https://www.iso.org/standard/94091.html) · [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html)
- **Relevant concepts:** lifecycle requirements-engineering processes, required information items and their contents, and guidance for requirements work across systems/software lifecycles.
- **Use in GovCheck:** candidate process and information-item reference for requirements governance and traceability.
- **Limit:** the third edition was a Draft International Standard at enquiry stage in September 2026, not a published International Standard. The 2018 edition remains the published predecessor until formally replaced. Do not label the DIS as final.

<a id="r-98"></a>
### R-98 — ISO/IEC 25010:2023, product quality model
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)
- **Relevant concepts:** product-quality characteristics and subcharacteristics used to specify, measure and evaluate ICT/software product quality.
- **Use in GovCheck:** candidate shared quality vocabulary for quality requirements, test objectives, evaluation criteria and measurement planning.
- **Limit:** a product-quality model is not a complete quality-management process, metric catalogue, measurement implementation or evidence of product quality.

<a id="r-99"></a>
### R-99 — SPDX specification
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [SPDX specifications catalogue](https://spdx.dev/use/specifications/)
- **Relevant concepts:** standardized machine-readable representation of software components, packages, files, relationships, licensing and other supply-chain metadata. The catalogue identifies SPDX 3.0 as current at the research snapshot.
- **Use in GovCheck:** candidate native format for SBOM and license/supply-chain metadata.
- **Limit:** an SPDX document does not prove inventory completeness, component safety, trustworthy provenance or correct discharge of license obligations.

<a id="r-100"></a>
### R-100 — CycloneDX specification
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [CycloneDX specification overview](https://cyclonedx.org/specification/overview/)
- **Relevant concepts:** extensible supply-chain object model for software/hardware components, services, dependencies, cryptographic assets, operational configurations and metadata; JSON, XML and Protocol Buffers representations.
- **Use in GovCheck:** candidate SBOM and broader supply-chain exchange format, to assess alongside SPDX against actual needs.
- **Limit:** format validity does not prove inventory completeness, component integrity, vulnerability absence or trustworthy build provenance. Pin the exact version and schema.

<a id="r-102"></a>
### R-102 — W3C PROV family
- **Cited by:** [0027-domain-semantic-standards-decisions-and-bootstrap](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [metamodel-design-dossier](decisions/metamodel-design-dossier.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [W3C PROV overview](https://www.w3.org/TR/prov-overview/)
- **Relevant concepts:** interoperable provenance models for entities, activities, agents and derivation/attribution, with data model, ontology, constraints and serialization specifications.
- **Use in GovCheck:** candidate vocabulary and representation family for provenance across decisions, sources, generated artifacts, observations and evidence.
- **Limit:** PROV records provenance relationships; it does not establish truth, admissibility, integrity or sufficiency, and does not provide repository governance authority.


<a id="r-103"></a>
### R-103 — OpenChain: ISO/IEC 5230 and ISO/IEC 18974
- **Cited by:** no current record cites this candidate source. · [0027](architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md) · [Intent impact analysis](intent-impact-analysis.md)
- **Primary sources:** [ISO/IEC 5230:2020 — OpenChain Specification](https://www.iso.org/standard/81039.html) · [ISO/IEC 18974:2023 — OpenChain security assurance specification](https://www.iso.org/standard/86450.html) · [OpenChain standards and adoption guidance](https://openchainproject.org/get-started)
- **Relevant concepts:** organizational requirements for open-source license-compliance programs (5230) and open-source security-assurance programs (18974), including policy, scope, roles, processes and retained verification material.
- **Use in GovCheck:** candidate process/organizational standards for open-source compliance and open-source security-assurance capabilities.
- **Limit:** these standards specify program requirements, not SBOM serialization, vulnerability-detection algorithms or proof that a particular component is safe. Conformance concerns the scoped organizational program and its verification materials; it must not be inferred from the presence of an SBOM or a scanner.


<a id="r-104"></a>
### R-104 — Agent instruction formats and spec-driven agent workflows
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md) · [Intent impact analysis](intent-impact-analysis.md)
- **Primary sources:** [AGENTS.md open format](https://agents.md/) · [VS Code custom-instructions reference](https://code.visualstudio.com/docs/agents/reference/custom-instructions-reference) · [Secure AI-assisted development in VS Code](https://code.visualstudio.com/docs/agents/run/security) · [VS Code agent hooks](https://code.visualstudio.com/docs/agent-customization/hooks) · [VS Code approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals) · [Claude Code project instructions and AGENTS.md support](https://code.claude.com/docs/en/memory) · [Codex development-workflow guide](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex) · [GitHub Spec Kit repository](https://github.com/github/spec-kit) · [GitHub Spec Kit documentation](https://github.github.com/spec-kit/)
- **Relevant concepts:** shared repository-level agent instructions; harness-specific discovery and loading rules; project-specific and path-scoped guidance; specification-driven workflows that produce plans, tasks and reviewable outcomes.
- **Use in GovCheck:** preserves the cross-agent instruction and spec-driven workflow options discussed for repository bootstrap and agent interoperability.
- **Limit:** AGENTS.md is a plain-text convention, not an enforceable policy or proof of instruction compliance. Discovery and inclusion differ by harness and version; finding a file does not prove that an agent follows it. Spec Kit is a workflow toolkit, not a normative authority, assurance case or security boundary.


<a id="r-105"></a>
### R-105 — Policy-as-code, continuous assurance and runtime agent-governance research
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary sources:** [MSR 2026 empirical study of policy-as-code](https://2026.msrconf.org/details/msr-2026-technical-papers/22/An-Empirical-Study-of-Policy-as-Code-Adoption-Purpose-and-Maintenance) · [author preprint](https://soft.vub.ac.be/Publications/2026/vub-tr-soft-26-01.pdf) · [CUGA: Governance by Construction for Generalist Agents](https://doi.org/10.1145/3786335.3813192) · [Audit-as-Code: a policy-as-code framework for continuous AI assurance](https://doi.org/10.3389/frai.2026.1759211) · [Runtime Policy Enforcement for MCP-Based LLM Agents](https://www.mdpi.com/2079-9292/15/13/2829)
- **Relevant concepts:** empirical policy-as-code adoption and maintenance across 10,560 files and 499 repositories; runtime governance interventions at multiple agent lifecycle checkpoints; mapping governance requirements to executable controls and structured evidence; tool-call-boundary enforcement with cross-step information-flow labels and audit records.
- **Use in GovCheck:** preserves the research evidence discussed for policy-as-code adoption, governance-by-construction, continuous AI assurance and MCP tool-call enforcement.
- **Limit:** these are research publications, not standards or independent certifications. The MSR dataset is bounded to its sampled repositories and tools; CUGA is a research/demo contribution; Audit-as-Code focuses on AI/MLOps assurance; the MCP enforcement evaluation is controlled and does not establish universal production safety. None implies adoption or implementation by GovCheck.


<a id="r-106"></a>
### R-106 — OWASP guidance for AI-agent and MCP security
- **Cited by:** [ADR 0002](decisions/0002-study-placement.md)
- **Primary source:** [OWASP DevSecOps Guideline — AI Agent and MCP Security](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-2-Develop/2-2-5-AI-Agent-and-MCP-Security/) · [OWASP IDE and AI-assisted development security](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-2-Develop/2-2-2-IDE-and-AI-assisted-development/)
- **Relevant concepts:** versioned and testable policy for agent permissions; authorization at a gateway or proxy using identity, tool and arguments; deny-by-default permissions; short-lived scoped identities; sandboxing and egress allowlists; agent configuration reviewed as code; configuration validation and audit logging.
- **Use in GovCheck:** supports the distinction between natural-language agent instructions and controls enforced at tool, gateway, identity and operating-system boundaries.
- **Limit:** this is an evolving engineering guideline, not a certification or proof of implementation. Recommendations must be mapped to the actual agent harness, execution host, tool surface and threat model; the guideline does not establish that a particular deployment enforces every listed control.


<a id="r-107"></a>
### R-107 — GitHub Actions workflow location and syntax
- **Cited by:** [ADR 0003](decisions/0003-two-level-governance.md), [Work portfolio event journal](work-portfolio/events.md), [Work-item register](work-portfolio/work-items.md)
- **Primary sources:** [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) · [GitHub Actions workflow concepts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)
- **Relevant concepts:** GitHub Actions workflow definitions are YAML files stored under the repository-root `.github/workflows/` directory; GitHub discovers workflow files from that location and evaluates them against repository events.
- **Use in GovCheck:** supports the ADR 0003 constraint that reusable product-package content cannot by itself relocate a GitHub Actions workflow: the bootstrap/synchronization process must materialize the workflow at the required repository-root path.
- **Limit:** this is a GitHub Actions platform constraint, not a general CI/CD requirement. It does not establish that a workflow is enabled, trusted, protected from bypass, correctly configured or successfully executed.


<a id="r-108"></a>
### R-108 — Apache License 2.0 and GPL compatibility
- **Cited by:** [ADR 0005](decisions/0005-license-apache-2-0-with-individual-attribution.md)
- **Primary sources:** [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) · [plain-text license file](https://www.apache.org/licenses/LICENSE-2.0.txt) · [Apache Software Foundation — GPL compatibility](https://www.apache.org/licenses/GPL-compatibility.html)
- **Relevant concepts:** redistribution conditions of section 4, including retention of copyright and attribution notices and reproduction of the NOTICE file's attribution notices in distributions of the Work or Derivative Works; contribution terms of section 5; absence of trademark grant in section 6; one-way compatibility with GPLv3 and incompatibility with GPLv2 as assessed by the FSF.
- **Use in GovCheck:** supports ADR 0005's choice of Apache 2.0 with an individual NOTICE attribution, and its rule that GPL-licensed tools remain external programs rather than embedded or linked components.
- **Limit:** this is the license text and the licensor foundation's own compatibility statement, not legal advice. Attribution obligations are triggered by redistribution; the license does not require attribution for internal use or network use without redistribution.

## VCS, forge and CI platform documentation (portability evidence)

<a id="r-109"></a>
### R-109 — Pijul command reference (diff, change, log)
- **Cited by:** [ADR 0006](decisions/0006-vcs-forge-portability.md)

- **Primary sources:** [pijul diff](https://pijul.org/manual/reference/diff.html) · [pijul change](https://pijul.org/manual/reference/change.html) · [pijul log JSON output (forum discussion)](https://discourse.pijul.org/t/how-to-efficiently-query-dependencies-for-all-changes/862)
- **Relevant concepts:** change identifiers are base32 hashes addressable by unambiguous prefix; `pijul diff --channel <CHANNEL>` compares a channel or the working copy; `pijul log --output-format json` exposes machine-readable history; `pijul change <HASH>` shows the author and date of a single change.
- **Use in GovCheck:** grounds the PijulAdapter mapping of the three VCS-adapter operations (list_changed, resolve_rev, author_of) proposed in ADR 0006.
- **Limit:** vendor manual plus a community forum thread; the JSON output format is documented only in that thread, so its stability must be pinned by conformance tests if an adapter is implemented.

<a id="r-110"></a>
### R-110 — GitLab CI and SLSA level 3 provenance
- **Cited by:** [ADR 0006](decisions/0006-vcs-forge-portability.md)

- **Primary source:** [GitLab Docs — SLSA level 3](https://docs.gitlab.com/ci/pipeline_security/slsa/level_3/)
- **Relevant concepts:** merge-request pipelines as a portable enforcement point on GitLab; native SLSA provenance attestations emitted by GitLab CI jobs.
- **Use in GovCheck:** shows that the GitHub-specific anchoring of ADR 0006's CI gate (required status checks, Actions) has a GitLab counterpart (pipelines must succeed, MR approvals, verifiable SLSA attestations).
- **Limit:** platform documentation; it does not establish that any GovCheck deployment uses GitLab or that emitted attestations are verified.

<a id="r-111"></a>
### R-111 — Woodpecker CI for Forgejo/Gitea
- **Cited by:** [ADR 0006](decisions/0006-vcs-forge-portability.md)

- **Primary source:** [Woodpecker CI — Forgejo configuration](https://woodpecker-ci.org/docs/next/administration/configuration/forges/forgejo)
- **Relevant concepts:** container-based CI running against Forgejo/Gitea instances (including Codeberg); pipeline manifests under `.woodpecker/`.
- **Use in GovCheck:** supports portability of the blocking-check + report-only-check pipeline to a forge without GitHub Actions.
- **Limit:** documentation of one CI system; Woodpecker and Forgejo versions must be pinned before relying on the integration.

<a id="r-112"></a>
### R-112 — SourceHut forge
- **Cited by:** [ADR 0006](decisions/0006-vcs-forge-portability.md)

- **Primary source:** [SourceHut](https://sourcehut.org/)
- **Relevant concepts:** git and Mercurial hosting, patch-based review by email, builds.sr.ht CI, mailing lists as the coordination/tracker surface.
- **Use in GovCheck:** example of a forge whose review and tracker model is not pull-request based, informing the forge-adapter layer of ADR 0006.
- **Limit:** project page; the email-driven workflow must be evaluated against team conventions before any adoption.

<a id="r-113"></a>
### R-113 — Fossil SCM self-contained forge
- **Cited by:** [ADR 0006](decisions/0006-vcs-forge-portability.md)

- **Primary source:** [Fossil web interface](https://fossil-scm.org/home/doc/2026-06-23/www/webui.wiki)
- **Relevant concepts:** single-binary DVCS with built-in ticketing, wiki, forum and timeline served over HTTP; check-in hashes as revision identity; external CI.
- **Use in GovCheck:** shows a VCS with a native tracker (tickets) but no native required-status-check concept, informing the transposability matrix in ADR 0006.
- **Limit:** vendor documentation; Fossil's CI integration is external and must be evaluated separately.

<a id="r-114"></a>
### R-114 — Anthropic AI-native SDLC Playbook: repository/change intent records
- **Cited by:** [ADR 0009](decisions/0009-intent-record-and-authority.md), [GovCheck intent](intent.md), [intent impact analysis](intent-impact-analysis.md)
- **Primary source:** [Anthropic, The AI-native SDLC Playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook)
- **Relevant concepts:** a versioned, human-readable `intent.md` preserving the originating problem, expected outcome, users/systems, constraints and open questions; downstream specification and implementation planning; intent retained as traceable context.
- **Use in GovCheck:** closest industrial precedent for the name and conceptual role of repository-level `intent.md`.
- **Limit:** industry playbook, not a universal normative file-format standard. Anthropic also uses intent records for individual changes; GovCheck's repository-level intent has a broader persistent scope. No Anthropic schema conformance is claimed.

<a id="r-115"></a>
### R-115 — ISO/IEC/IEEE 15288:2023, Systems and software engineering — System life cycle processes
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md), [metamodel semantic-coverage audit](research/metamodel-semantic-coverage-audit.md)
- **Primary source:** [ISO/IEC/IEEE 15288:2023](https://www.iso.org/standard/81702.html)
- **Relevant concepts:** lifecycle-process framework spanning conception, development, production, utilization, support and retirement; iterative and recursive application; stakeholder involvement and information exchange.
- **Use in GovCheck:** supports modeling intent, requirements, decisions, realization and assurance as lifecycle concerns rather than a one-time bootstrap pipeline.
- **Limit:** does not prescribe a particular lifecycle model, methodology, modeling approach, technique or document naming convention.

<a id="r-116"></a>
### R-116 — ISO/IEC/IEEE 29148 requirements engineering
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md), [metamodel semantic-coverage audit](research/metamodel-semantic-coverage-audit.md)
- **Primary sources:** [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) · [ISO/IEC/IEEE DIS 29148 edition 3](https://www.iso.org/standard/94091.html)
- **Relevant concepts:** requirements-engineering processes and information items; derivation, allocation, validation, verification and bidirectional traceability of needs and requirements throughout the lifecycle.
- **Use in GovCheck:** standards reference for distinguishing intent/needs from requirements and defining derivation, allocation, validation and change-impact relations.
- **Limit:** 2018 was confirmed current in 2024; the third-edition DIS listed in 2026 is a draft under enquiry, not an adopted International Standard.

<a id="r-117"></a>
### R-117 — NASA Systems Engineering Handbook: stakeholder expectations and requirements management
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary sources:** [NASA stakeholder expectations definition](https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/) · [NASA requirements management](https://www.nasa.gov/reference/6-2-requirements-management/) · [NASA Systems Engineering Handbook](https://science.nasa.gov/wp-content/uploads/2023/04/nasa_systems_engineering_handbook_0.pdf)
- **Relevant concepts:** stakeholder expectations, ConOps, goals/objectives, iterative design decisions, requirement decomposition/allocation, bidirectional traceability, design verification, product verification and validation.
- **Use in GovCheck:** supports upward/downward traceability and consistency checks across expectations, requirements, architecture/design and verification/validation.
- **Limit:** NASA systems-engineering guidance, not a universal repository schema or mandatory process for every software project.

<a id="r-118"></a>
### R-118 — Goal-oriented Requirements Engineering systematic mapping and 2026 reflection
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [A systematic mapping of goal-oriented requirements engineering: reflections, impact, and the way forward](https://link.springer.com/article/10.1007/s00766-026-00476-7)
- **Academic background:** reflects on the extended systematic mapping study covering 246 GORE publications up to 2015 and examines subsequent influence and adoption.
- **Relevant concepts:** goals, AND/OR refinement, operationalization, actors, dependencies, quality goals/softgoals, trade-offs, KAOS, iStar, GRL and Tropos.
- **Use in GovCheck:** informs typed relationships connecting intent, goals, actors, alternatives, quality concerns and requirements.
- **Limit:** the 2026 reflection identifies persistent industrial-adoption barriers and uneven empirical evaluation. GORE is a family of approaches, not one universal standard.

<a id="r-119"></a>
### R-119 — OMG Systems Modeling Language (SysML) v2.0
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [OMG SysML specification](https://www.omg.org/spec/SysML)
- **Relevant concepts:** standardized systems modeling for requirements, behavior, structure, analysis and verification; model relationships and interoperability through standardized APIs.
- **Use in GovCheck:** candidate source for typed relationships among requirements, model elements, design and verification, and possible exchange/mapping profiles.
- **Limit:** SysML is a systems-modeling language, not GovCheck's repository-governance metamodel or a mandatory serialization.

<a id="r-120"></a>
### R-120 — OMG Structured Assurance Case Metamodel (SACM) 2.3
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-ontology-reuse-assessment](research/metamodel-ontology-reuse-assessment.md)
- **Primary source:** [OMG SACM 2.3 specification](https://www.omg.org/spec/SACM/)
- **Relevant concepts:** claims, argumentation, artifact references, asserted evidence/context, reasoning, counter-claims/counter-evidence and modular argument packages.
- **Use in GovCheck:** specialized standardized model for the assurance subgraph and argument/evidence relationships.
- **Limit:** SACM does not define the entire intent-to-goals-to-requirements-to-decisions-to-specifications lifecycle and is not GovCheck's complete metamodel.

<a id="r-121"></a>
### R-121 — UK Government Architectural Decision Record Framework (2025)
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [intent-impact-analysis](intent-impact-analysis.md), [metamodel-coherence-verification](research/metamodel-coherence-verification.md)
- **Primary source:** [UK Government ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework)
- **Relevant concepts:** context, decision, consequences, appropriate decision-making level, visibility, traceability and autonomy balanced with accountability.
- **Use in GovCheck:** supports separately authorized decision records explaining how requirements, constraints and architecture alternatives were resolved.
- **Limit:** an ADR records a decision and rationale; it does not itself establish that a choice satisfies originating intent or requirements.

<a id="r-122"></a>
### R-122 — IntentDocs open INTENT.md format
- **Cited by:** [0009-intent-record-and-authority](decisions/0009-intent-record-and-authority.md), [metamodel-coherence-verification](research/metamodel-coherence-verification.md)
- **Primary source:** [IntentDocs INTENT.md format](https://www.intentdocs.com/intent-md)
- **Relevant concepts:** published open format and convention for a repository-level `INTENT.md` that combines product overview, personas, releases, user stories and acceptance criteria.
- **Use in GovCheck:** comparison point for an existing published `INTENT.md` format and its scope.
- **Limit:** its bundled content model is not adopted by GovCheck; GovCheck does not claim conformance or compatibility.

<a id="r-123"></a>
### R-123 — Lean Computer Science Library (CSLib) for semantic proof
- **Cited by:** [metamodel-coherence-verification ](research/metamodel-coherence-verification.md)
- **Primary sources:** [CSLib repository](https://github.com/leanprover/cslib) · [organization](https://github.com/leanprover/cslib/blob/main/ORGANISATION.md) · [contributor guidance](https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md)
- **Relevant concepts:** reusable Lean formalizations for operational semantics, labeled transition systems, program equivalence and logics.
- **Use in GovCheck:** reuse suitable foundations to formalize the common semantic bridge and prove critical mapping properties.
- **Limit:** CSLib is not a ready-made GovCheck ontology; its code-translation/Boole preservation pipeline is evolving. Pin versions and disclose axioms and trusted components.

- **Compatibility snapshot (2026-11-11):** [CSLib main commit f8acdb3](https://github.com/leanprover/cslib/commit/f8acdb37c713b0124ad36b863f50c200a5f1cdba) pins Lean 4.36.0-rc2 and Mathlib commit 887bb849a9f64e1c66499fd5ff8523c864e78941; the current GovCheck prototype pins Lean 4.19.0, so direct import is not yet compatible.
- **BTL semantics limit:** CSLib's BTL module defines future/past modalities over a relation without imposing order properties; reflexivity/transitivity and any linear-time assumptions must be declared by the consuming model.

<a id="r-124"></a>
### R-124 — TLA+, TLC and TLAPS for temporal and transition-system properties
- **Cited by:** [metamodel-coherence-verification ](research/metamodel-coherence-verification.md)
- **Primary sources:** [TLA+ Proof System](https://proofs.tlapl.us/doc/web/content/Home.html) · [TLC documentation](https://github.com/tlaplus/tlaplus/blob/master/general/docs/tlcgui.txt)
- **Relevant concepts:** state-transition specifications, invariant checking, temporal properties, finite-state model checking and mechanically checked proof steps.
- **Use in GovCheck:** check authority lifecycle, revocation, expiry, invalidation and revalidation properties.
- **Limit:** finite model checking is bounded by the model and state space; TLAPS does not currently provide general temporal reasoning for all TLA+ constructs.

<a id="r-125"></a>
### R-125 — Verification of model transformations
- **Cited by:** [metamodel-coherence-verification ](research/metamodel-coherence-verification.md)
- **Primary source:** Calegari & Szasz, “Verification of Model Transformations: A Survey of the State-of-the-Art” (2013), [DOI](https://doi.org/10.1016/j.entcs.2013.02.002)
- **Relevant concepts:** verification of transformations in terms of transformation rules, properties of interest and verification techniques; heterogeneous verification.
- **Use in GovCheck:** frame mapping verification as explicit transformations plus preservation properties and declared techniques.
- **Limit:** no single method proves all transformation properties; results depend on semantics, assumptions and bounds.

<a id="r-126"></a>
### R-126 — Epsilon EVL and Alloy Analyzer
- **Cited by:** [metamodel-coherence-verification ](research/metamodel-coherence-verification.md)
- **Primary sources:** [Epsilon Validation Language](https://eclipse.dev/epsilon/doc/evl/) · [Alloy Analyzer](https://alloy.readthedocs.io/en/latest/tooling/analyzer.html)
- **Relevant concepts:** intra-/inter-model constraints, validation diagnostics and fixes; SAT-based search for finite relational counterexamples.
- **Use in GovCheck:** executable model constraints and counterexample discovery before or alongside proof development.
- **Limit:** bounded analysis and validation are not unbounded proof of arbitrary semantic preservation.

<a id="r-127"></a>
### R-127 — Ontology alignment, consistency and conservative extension
- **Cited by:** [metamodel-coherence-verification ](research/metamodel-coherence-verification.md)
- **Primary sources:** Botoeva et al., “Inseparability and conservative extensions of description logic ontologies: A survey” (2017), [repository record](https://livrepository.liverpool.ac.uk/3006616/) · “A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology” (2025), [open article](https://pmc.ncbi.nlm.nih.gov/articles/PMC11833102/)
- **Relevant concepts:** model-theoretic criteria for ontology alignment, semantic interoperability, query/concept inseparability and conservative extensions.
- **Use in GovCheck:** distinguish simple traceability from semantic mappings; state when adding GovCheck vocabulary must preserve consequences in source vocabularies.
- **Limit:** conservativity is relative to a chosen signature, semantics and application; define it per mapping/use case, not universally.

<a id="r-128"></a>
### R-128 — Assurance Forge: independent SACM 2.4 Beta 1 implementation-impact audit (2026-10-02; repository revision 2026-11-03)
- **Cited by:** [SACM 2.4 Beta 1 interoperability-risk report](research/sacm24-beta1-interoperability-risk.md), [SACM 2.4 semantic mapping slice](research/sacm24-claim-inference-mapping.md), [integrated metamodel-coherence execution record](research/metamodel-coherence-prototype-execution.md), [metamodel semantic-coverage audit](research/metamodel-semantic-coverage-audit.md), [SACM source-native metamodel ingestion](research/sacm-native-metamodel-ingestion.md), [SACM XMI structural inventory](research/sacm-xmi-structural-inventory.md), [SACM source-view alignment report](research/sacm24-source-view-alignment.md), [Work portfolio event journal](work-portfolio/events.md), [Work-item register](work-portfolio/work-items.md)
- **Primary source:** [Pinned implementation-impact audit](https://github.com/lasrod/assurance-forge/blob/0f5187099be1c28fc725cb0f381afc695a135c89/docs/sacm/sacm-2.4-beta1-impact.md) · [pinned official-artifact fetch script and SHA-256 checks](https://github.com/lasrod/assurance-forge/blob/0f5187099be1c28fc725cb0f381afc695a135c89/scripts/fetch-sacm24-beta1-references.sh).
- **Relevant concepts:** reported absence of a stable native 2.4 instance interchange contract; text/XML discrepancies reported in identity fields, assertion declaration literals, multiplicities, Claim value type and inheritance; the Claim.value value is supported by normative Figure 13.1 (MultiLangString) while informative Figure 15.1.1 and the XML show ExpressionLangString; the exact Clause 13.9 locator remains to be checked; implementation cost and versioning implications.
- **Use in GovCheck:** independent engineering cross-check that the SACM 2.4 Beta 1 text and machine-readable metamodel must be treated as separate source views, not silently normalized into one model.
- **Limit:** this is a third-party implementation audit, not an OMG statement or normative authority. Its findings must be checked against pinned OMG artifacts; it does not establish that all SACM 2.4 implementations share the same limitations.

<a id="r-142"></a>
### R-142 — ConE: Concurrent Edit Detection Tool
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary source:** [ACM/IEEE paper, DOI 10.1145/3478019](https://doi.org/10.1145/3478019)
- **Relevant concepts:** detecting concurrently edited files across pull requests; empirical relationship between overlap and bug risk.
- **Use in GovCheck:** motivates representing overlapping work scopes as a signal for impact analysis and targeted review.
- **Limit:** the study concerns six large Microsoft repositories over six months; overlap is not proof of incompatibility, and a detector is not a correctness proof.

<a id="r-143"></a>
### R-143 — Empirical investigation into merge conflicts and software quality
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary source:** [Open paper PDF](https://ics.uci.edu/~iftekha/pdf/J4.pdf)
- **Relevant concepts:** conflict prevalence, semantic conflict categories and association between conflict-affected code and bugs in a sample of open-source projects.
- **Use in GovCheck:** evidence that conflict resolution and semantic impact deserve separate treatment in assurance.
- **Limit:** results are empirical associations within a particular dataset and methodology; they do not establish universal causal rates or project-specific risk.

<a id="r-144"></a>
### R-144 — ConflictBench: A benchmark to evaluate software merge tools
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary source:** [Journal of Systems and Software, 2024](https://www.sciencedirect.com/science/article/pii/S0164121224001298)
- **Relevant concepts:** Java merge-conflict dataset and comparative evaluation of merge tools.
- **Use in GovCheck:** supports distinguishing tool applicability and merge success from semantic correctness.
- **Limit:** dataset and language coverage are bounded; benchmark outcomes do not establish correctness for arbitrary repositories or languages.

<a id="r-145"></a>
### R-145 — Lightweight Semantic Conflict Detection with Static Analysis
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary source:** [ICSE Companion 2024, DOI 10.1145/3639478.3643118](https://doi.org/10.1145/3639478.3643118)
- **Relevant concepts:** static-analysis detection of dynamic semantic conflicts that may remain after textual merge; reported F1 0.50 and accuracy 0.60 on 99 experimental units.
- **Use in GovCheck:** motivates layered detection while preserving uncertainty and detector limitations.
- **Limit:** reported evaluation is small and metrics are modest; the method is not an authoritative compatibility decision.

<a id="r-146"></a>
### R-146 — Research on search-based and synthesis-based merge conflict resolution
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary sources:** Paulino, [ACM TOSEM 2026, DOI 10.1145/3748256](https://doi.org/10.1145/3748256) · Pan et al., [Microsoft Research / ICSE 2021](https://www.microsoft.com/en-us/research/publication/can-program-synthesis-be-used-to-learn-merge-conflict-resolutions-an-empirical-analysis/)
- **Relevant concepts:** search-guided conflict-resolution candidates and learned synthesis patterns for bounded conflict classes.
- **Use in GovCheck:** supports recording resolver provenance, inputs, tool version and post-resolution assurance, without giving the resolver acceptance authority.
- **Limit:** coverage and accuracy depend on conflict class, dataset and evaluation; similarity heuristics are not semantic proof.

<a id="r-147"></a>
### R-147 — LLM-based multi-agent systems for software engineering: literature review
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary source:** [ACM TOSEM 2025, DOI 10.1145/3712003](https://doi.org/10.1145/3712003)
- **Relevant concepts:** survey of multi-agent software-engineering architectures, collaboration patterns, benefits and research gaps.
- **Use in GovCheck:** contextualizes agent collaboration as one workflow class whose coordination and assurance claims need evaluation.
- **Limit:** a literature review is not evidence that a particular framework, coordination protocol or deployment is reliable.

<a id="r-148"></a>
### R-148 — DORA 2025 State of AI-assisted Software Development
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary sources:** [DORA report](https://dora.dev/research/2025/dora-report/) · [Google Research publication](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)
- **Relevant concepts:** organizational and delivery-system factors associated with AI-assisted software development; AI as an amplifier of existing strengths and weaknesses.
- **Use in GovCheck:** cautions against equating agent count or coding speed with delivery quality; emphasizes governance, feedback and engineering-system context.
- **Limit:** survey and qualitative research inform organizational decisions but do not prove causality or predict a specific repository's outcomes.

<a id="r-149"></a>
### R-149 — GitHub merge queues
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary source:** [Official GitHub documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- **Relevant concepts:** temporary merge-group branches; required checks against the base plus queued changes; bounded build concurrency and merge grouping.
- **Use in GovCheck:** industrial example of validating an exact integration candidate rather than reusing isolated pull-request results.
- **Limit:** GitHub-specific product documentation; the feature must not become GovCheck's canonical or mandatory architecture.

<a id="r-150"></a>
### R-150 — “Your Team's Agents Are All Shipping to the Same Code at Once”
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Source:** [Video supplied for the review](https://youtu.be/fTUinMqA1XQ)
- **Relevant concepts:** industry framing of concurrent agent contributions and the coordination/integration bottleneck.
- **Use in GovCheck:** motivation for the research question and adversarial scenarios, including individually passing but collectively incompatible changes.
- **Limit:** a talk/video is a secondary industry source and problem framing, not a peer-reviewed result or sufficient evidence for adopting an architecture.

<a id="r-151"></a>
### R-151 — Predicting merge conflicts considering social and technical assets
- **Cited by:** [Concurrent agent change-governance research](research/concurrent-agent-change-governance.md)
- **Primary source:** [Empirical Software Engineering, DOI 10.1007/s10664-023-10395-8](https://link.springer.com/article/10.1007/s10664-023-10395-8)
- **Relevant concepts:** empirical prediction of merge conflicts using social and technical assets.
- **Use in GovCheck:** supports assessing work overlap and dependency/coordination context rather than treating changed-file overlap as a complete conflict predicate.
- **Limit:** predictive associations and model performance depend on the dataset, features and development context; they do not establish incompatibility or causality.

<a id="r-193"></a>
### R-193 — Probabilistic, fuzzy and state-transition modelling for software assurance
- **Cited by:** [Research discussion: semantic assurance and transition models](research/semantic-assurance-and-transition-models-2026-11.md)

- **Primary and academic sources:** [Baier & Katoen, *Principles of Model Checking*](https://is.ifmo.ru/books/_principles_of_model_checking.pdf) · [PRISM model checker manual](https://www.prismmodelchecker.org/manual/Main/Introduction) · [PRISM tutorials](https://www.prismmodelchecker.org/tutorial/) · [UPPAAL transition-system semantics](https://docs.uppaal.org/language-reference/system-description/semantics/) · [NIST Engineering Statistics Handbook: Bayesian reliability evaluation](https://www.itl.nist.gov/div898/handbook/apr/section1/apr1a.htm) · [Graydon & Holloway (2017), quantitative confidence in assurance arguments](https://doi.org/10.1016/j.ssci.2016.09.014) · [Probabilistic model of belief in safety cases (2021)](https://www.sciencedirect.com/science/article/pii/S0925753521000321) · [Johanyák & Zlatko (2025), fuzzy logic in software requirements engineering](https://doi.org/10.47833/2025.2.CSC.008) · [Yen, Tiao & Liu (1996), imprecise requirements](https://doi.org/10.1109/FUZZY.1996.551766) · [Salako & Zhao (2023), correlated software reliability tests](https://doi.org/10.1109/TSE.2022.3233802) · [Salako & Zhao (2024), conservative Bayesian software reliability](https://doi.org/10.1002/qre.3460) · [NIST, Software Assurance Using Structured Assurance Case Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC4548534/).
- **Relevant concepts:** finite-state transition systems; discrete- and continuous-time Markov chains; Markov decision processes; probabilistic timed automata; transition rates, probabilities, costs and rewards; Bayesian reliability assessment; interval-valued transition probabilities; fuzzy membership and imprecise requirements; quantitative confidence in assurance arguments.
- **Use in GovCheck:** supports the study of optional specialist profiles for probabilistic and fuzzy reasoning and of a generic transition-analysis contract linking semantics, parameters, provenance, analysis specifications/results and assurance claims.
- **Limit:** the sources describe distinct mathematical semantics and tools. A transition weight is not necessarily a probability; a fuzzy membership degree is not a probability; a model-checking result is bounded by its model and assumptions. Quantitative confidence techniques require critical evaluation and empirical validation. These sources do not establish adoption or implementation by GovCheck.

<a id="r-194"></a>
### R-194 — Linearizability: A Correctness Condition for Concurrent Objects
- **Cited by:** [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md), [Decision-session record 0008](decisions/0008-governance-applicability-arbitration-session.md), [Work portfolio event journal](work-portfolio/events.md), [Work-item register](work-portfolio/work-items.md)
- **Primary source:** Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM Transactions on Programming Languages and Systems*, 12(3), 1990, pp. 463–492. [DOI](https://doi.org/10.1145/78969.78972) · [Author-hosted paper](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf)
- **Relevant concepts:** concurrent operations appear to take effect at one point between invocation and response while respecting a legal sequential specification.
- **Use in GovCheck:** provides the formal concurrency concept behind the journal's single linearization point for compare-and-append.
- **Limit:** linearizability is a correctness condition, not a storage implementation or a proof that a particular journal satisfies it.

<a id="r-195"></a>
### R-195 — ARIES write-ahead logging and transaction recovery
- **Cited by:** [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md), [Decision-session record 0008](decisions/0008-governance-applicability-arbitration-session.md), [Work portfolio event journal](work-portfolio/events.md), [Work-item register](work-portfolio/work-items.md)
- **Primary source:** C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM Transactions on Database Systems*, 17(1), 1992. [IBM Research publication](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging)
- **Relevant concepts:** write-ahead logging, durable transaction recovery, redo/undo and restart recovery.
- **Use in GovCheck:** informs the distinction between volatile preparation, durable commit and reconstruction after interruption.
- **Limit:** ARIES is a database recovery algorithm; citing it does not select a database, imply direct adoption, or prove the GovCheck journal's durability.

<a id="r-196"></a>
### R-196 — RFC 9110, HTTP Semantics: idempotent methods
- **Cited by:** [Specification 0007](specifications/0007-canonical-governance-journal-protocol.md), [Decision-session record 0008](decisions/0008-governance-applicability-arbitration-session.md), [Work portfolio event journal](work-portfolio/events.md), [Work-item register](work-portfolio/work-items.md)
- **Primary source:** [RFC 9110 §9.2.2 — Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
- **Relevant concepts:** repeatable requests have the same intended effect as one request, enabling safe retry after a lost response when the operation semantics are idempotent.
- **Use in GovCheck:** informs the protocol distinction between retrying an exact append request and accidentally creating a second normative event.
- **Limit:** HTTP method semantics do not define GovCheck's idempotency-key namespace, journal retention or append protocol; those remain specified locally.

<a id="r-197"></a>
### R-197 — OMG SACM 2.4 Beta 1 normative machine-readable metamodel XML
- **Cited by:** [SACM source-native metamodel ingestion](research/sacm-native-metamodel-ingestion.md), [SACM XMI structural inventory](research/sacm-xmi-structural-inventory.md), [SACM source-view alignment report](research/sacm24-source-view-alignment.md), [Work portfolio event journal](work-portfolio/events.md)
- **Implementation artifacts:** [XMI inventory generator](../scripts/parse-sacm-xmi.py) · [committed inventory summary](../formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json).
- **Primary source:** [OMG SACM specification catalogue](https://www.omg.org/spec/SACM) · [normative machine-readable metamodel XML](https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml) · OMG file ID `ptc/26-05-28`.
- **Pinned identity:** SACM 2.4 Beta 1; source path dated 2026-05-04; native format XML; SHA-256 comparison value `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`, as reported by R-128 and verified by GovCheck workflow run [43444619765](https://github.com/Martin-PB/govcheck/actions/runs/43444619765) against 524,243 downloaded source bytes.
- **Relevant concepts:** normative machine-readable metamodel source, distinct from the normative PDF prose and informative UML Profile XMI.
- **Limit:** SACM 2.4 Beta 1 is in-process/informational; SACM 2.3 remains formal. This metamodel XML is not a portable assurance-case instance interchange format and its digest does not establish semantic conformance.


<a id="r-198"></a>
### R-198 — OMG SACM 2.4 Beta 1 normative specification PDF
- **Cited by:** [SACM source-view alignment report](research/sacm24-source-view-alignment.md)
- **Primary source:** [OMG SACM specification catalogue](https://www.omg.org/spec/SACM) · [SACM 2.4 Beta 1 normative PDF](https://www.omg.org/spec/SACM/2.4/Beta1/PDF) · OMG file ID `ptc/26-06-34`.
- **Pinned identity:** SACM 2.4 Beta 1; source path dated 2026-05-04; 161 pages; SHA-256 `25f32d1cd4bf32dfa9c92c7c1840e1a113b1e91c0e97252f6551878c39997ff5`, reported by the independent R-128 pinned fetch script and independently verified by GovCheck workflow run [43496689208](https://github.com/Martin-PB/govcheck/actions/runs/43496689208) against 9,019,601 downloaded bytes; source PDF is retained in artifact [14072371021](https://github.com/Martin-PB/govcheck/actions/runs/43496689208/artifacts/14072371021).
- **Relevant concepts:** normative specification prose, figures, clauses and annexes; source-fragment provenance for SACM 2.4 Beta 1 claims.
- **Limit:** the PDF itself contains conflicting fragments; PDF text extraction does not capture all diagram-only labels. No fragment should be treated as a canonical PDF-wide statement without explicit scope.

<a id="r-199"></a>
### R-199 — OMG SACM 2.4 Beta 1 informative UML Profile XMI
- **Cited by:** [SACM source-view alignment report](research/sacm24-source-view-alignment.md)
- **Primary source:** [OMG SACM specification catalogue](https://www.omg.org/spec/SACM) · [OMG SACM machine-readable files catalogue](https://www.omg.org/spec/SACM/machine-readable) · OMG file ID `ptc/26-05-21`.
- **Pinned identity:** SACM 2.4 Beta 1; source path dated 2026-05-04; SHA-256 `9149a0414628e1b70c1f7c2235f5180c64e7a144601eb2ae78d539681918838b`, reported by the independent R-128 pinned fetch script. GovCheck has not yet independently downloaded and recomputed this XMI digest.
- **Relevant concepts:** informative UML profile artifact, kept distinct from the normative metamodel XML (R-197) and normative specification PDF (R-198).
- **Limit:** informative profile XMI is not the normative SACM metamodel XML and does not establish an instance interchange contract or semantic conformance.
