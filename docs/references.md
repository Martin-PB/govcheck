# GovCheck external reference catalogue

## Thematic index

| Theme | Entries |
|---|---|
| Governance authority, separation of duties and secure development | R-01–R-03, R-11 |
| Assurance cases, safety arguments and formal methods | R-04–R-05, R-20, R-27–R-36 |
| Model checking and program-verification alternatives | R-29–R-35 |
| Evidence provenance and software supply chain | R-06–R-08 |
| Policy engines and authorization | R-09–R-10 |
| Schemas and interface contracts | R-13, R-16 |
| Artifact identity, versioning, releases and reproducibility | R-14–R-15, R-21, R-23–R-26 |
| Governance metadata and catalogues | R-17 |
| Agent workflow systems assessed as fixtures | R-18–R-19 |
| Version-control semantics and collaboration | R-22, R-37–R-42, R-54 |
| Knowledge representation and interoperability | R-43–R-53 |
| Integration project repositories and studies | R-54 |
| Mind-map and graph interchange formats | R-55 |
| Cloud storage provider APIs | R-56 |
| Browser-local persistence and WebAssembly | R-57 |
| Desktop peer discovery and DHT | R-58 |

## Full reference entries

## Detailed source register

**Purpose.** This register consolidates academic, standards-body, industrial-documentation and source-code references used to motivate GovCheck's repository-governance design. It is a navigational bibliography, not a normative policy or adoption decision.

**Selection rule.** Prefer primary publications, standards, official project documentation and pinned source revisions. A reference supports only the specific point stated here; it does not establish that GovCheck implements the capability or that a referenced tool is suitable as a dependency.

## How to use these references

- **Normative authority and separation of duties:** R-01, R-02, R-03.
- **Formal models, proofs and assurance arguments:** R-04, R-05.
- **Evidence provenance and software supply chain:** R-06, R-07, R-08.
- **Executable policy and authorization:** R-09, R-10.
- **Repository security posture and enforcement boundary:** R-03, R-08, R-18, R-19.
- **Canonical schemas, versioning and release identity:** R-13, R-14, R-15, R-16.
- **External governance/catalogue pattern:** R-17.
- **Candidate agent-workflow tools assessed, not adopted:** R-18, R-19.
- **Proof assistant and interface contracts:** R-20, R-21.
- **Native VCS semantics and collaboration adapters:** R-22.
- **Threat modeling, attack paths and risk management:** R-27–R-32.
- **Security assurance cases and metamodels:** R-33–R-34.

## Standards, government guidance and industry specifications

<a id="r-01"></a>
### R-01 — NIST SP 800-53 Rev. 5, Security and Privacy Controls
- **Primary source:** [NIST SP 800-53 publication and control catalogue](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- **Relevant concepts:** AC-5 separation of duties; access management; auditability and control ownership.
- **Use in GovCheck:** informs the distinction between normative authorization, technical review and execution, and the need to describe limits of a single-authority regime.
- **Limit:** a control catalogue is not GovCheck's governance ontology; selecting a control does not demonstrate implementation.

<a id="r-02"></a>

- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md), [0013](architecture/0013-governance-metamodel.md), [0022](architecture/0022-governance-capability-audit.md), [0023](architecture/0023-bootstrap-governance-authority.md).
### R-02 — NIST SP 800-218, Secure Software Development Framework (SSDF) 1.1
- **Primary source:** [NIST publication](https://csrc.nist.gov/pubs/sp/800/218/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-218)
- **Relevant concepts:** documented security requirements and design decisions, secure development practices, provenance and release practices.
- **Use in GovCheck:** reference for traceable repository-development obligations and the lifecycle context in which evidence is collected.
- **Limit:** SSDF is practice guidance, not a formal acceptance predicate or proof of conformity. NIST has also published a draft SP 800-218 Rev. 1 / SSDF 1.2; use the publication status appropriate to the claim.

<a id="r-03"></a>

- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md), [0022](architecture/0022-governance-capability-audit.md).
### R-03 — GitHub protected branches and required status checks
- **Primary source:** [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **Relevant concepts:** required reviews, required status checks, bypass lists and branch restrictions.
- **Use in GovCheck:** demonstrates a practical shared-acceptance enforcement point.
- **Limit:** forge settings are enforcement mechanisms, not normative authority. Repository administrators and permitted bypass actors remain in the threat model.

<a id="r-04"></a>

- **Cited by:** [0022](architecture/0022-governance-capability-audit.md), [0023](architecture/0023-bootstrap-governance-authority.md).
### R-04 — Goal Structuring Notation (GSN) Community Standard
- **Primary source:** [GSN Community Standard — official site](https://scsc.uk/gsn)
- **Relevant concepts:** structured assurance claims, arguments, strategies, context, assumptions and evidence.
- **Use in GovCheck:** useful vocabulary for the assurance dossier and traceability from governance requirements to properties and evidence.
- **Limit:** an assurance argument structures reasoning; it does not automatically make premises true or replace machine-checkable predicates.

<a id="r-05"></a>

- **Cited by:** [0010](architecture/0010-assurance-proof-and-conformance.md).
### R-05 — TLA+ and TLC
- **Primary sources:** [Lamport's publications on TLA](https://www.microsoft.com/en-us/research/people/lamport/publications/) · [TLA+ project and documentation](https://lamport.azurewebsites.net/tla/tla.html)
- **Academic reference:** Leslie Lamport, “The Temporal Logic of Actions,” ACM Transactions on Programming Languages and Systems, 16(3), 1994, pp. 872–923. [DOI](https://doi.org/10.1145/177492.177726)
- **Relevant concepts:** state-transition specifications, invariants, temporal properties and model checking.
- **Use in GovCheck:** foundation for lifecycle, assurance and authority-transition models.
- **Limit:** a completed TLC run establishes properties only for the recorded model, configuration, assumptions and explored bounds; it does not prove implementation refinement or normative fidelity.

<a id="r-06"></a>

- **Cited by:** [0008](architecture/0008-formalization-and-conformance.md), [0010](architecture/0010-assurance-proof-and-conformance.md).
### R-06 — in-toto: software supply-chain integrity
- **Primary sources:** [in-toto project](https://in-toto.io/) · [USENIX Security 2019 paper](https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf)
- **Academic reference:** Santiago Torres-Arias et al., “in-toto: Providing farm-to-table guarantees for bits and bytes,” 28th USENIX Security Symposium, 2019.
- **Relevant concepts:** recording steps, materials/products and provenance in a software supply chain.
- **Use in GovCheck:** informs provenance and binding of check/evidence records to the artifacts and process steps that produced them.
- **Limit:** provenance does not define repository-specific normative rules or prove that a recorded step was semantically correct.

<a id="r-07"></a>

- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md), [0010](architecture/0010-assurance-proof-and-conformance.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md).
### R-07 — SLSA
- **Primary source:** [SLSA specification](https://slsa.dev/spec/)
- **Relevant concepts:** software supply-chain levels, provenance and build integrity.
- **Use in GovCheck:** complementary vocabulary for build provenance and release evidence.
- **Limit:** SLSA does not define GovCheck's canonical authority, exception policy, change lifecycle or complete assurance case.

<a id="r-08"></a>

- **Cited by:** [0006](architecture/0006-threat-and-trust-model.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md).
### R-08 — OpenSSF Scorecard
- **Primary sources:** [OpenSSF project page](https://openssf.org/projects/scorecard/) · [Scorecard repository](https://github.com/ossf/scorecard)
- **Relevant concepts:** automated, reusable checks of selected open-source security practices.
- **Use in GovCheck:** candidate source of scoped security-posture evidence.
- **Limit:** a score is not a complete repository-specific governance evaluation, proof or authorization decision.

<a id="r-09"></a>

- **Cited by:** [0015](architecture/0015-governance-conformance-and-validation-plan.md).
### R-09 — Open Policy Agent (OPA)
- **Primary source:** [Official OPA documentation](https://www.openpolicyagent.org/docs)
- **Relevant concepts:** separation of policy decision-making from policy enforcement; evaluating structured input against policy.
- **Use in GovCheck:** informs a possible evaluator/enforcement-point separation and declarative-policy comparison.
- **Limit:** OPA is not GovCheck's normative authority, assurance-case engine or proof of non-bypassability. No dependency is selected.

<a id="r-10"></a>

- **Cited by:** [0013](architecture/0013-governance-metamodel.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md), [0022](architecture/0022-governance-capability-audit.md).
### R-10 — Cedar authorization language
- **Primary sources:** [Cedar language reference](https://docs.cedarpolicy.com/) · [Cedar project](https://www.cedarpolicy.com/)
- **Relevant concepts:** typed principal/action/resource/context authorization decisions and separation of authorization logic from application logic.
- **Use in GovCheck:** informs future comparison of scoped authorization and deterministic decision semantics.
- **Limit:** Cedar is not a complete governance lifecycle, evidence-freshness model or assurance case. No dependency is selected.

<a id="r-11"></a>

- **Cited by:** [0013](architecture/0013-governance-metamodel.md), [0015](architecture/0015-governance-conformance-and-validation-plan.md), [0022](architecture/0022-governance-capability-audit.md).
### R-11 — NIST SP 800-218 SSDF project page
- **Primary source:** [NIST SSDF project and publications](https://csrc.nist.gov/projects/ssdf)
- **Relevant concepts:** secure development practices and mappings to established practices.
- **Use in GovCheck:** supplementary navigation for the status of SSDF publications and profiles.
- **Limit:** use the dated final publication when making a version-specific claim; do not confuse a draft revision with a final standard.

<a id="r-13"></a>

- **Cited by:** no current architecture or specification record cites this source; retained as supplementary reference.
### R-13 — JSON Schema Draft 2020-12
- **Primary source:** [Official specification landing page](https://json-schema.org/draft/2020-12/)
- **Relevant concepts:** structural validation of machine-readable records.
- **Use in GovCheck:** candidate reference for governance records and evidence manifests if JSON Schema is adopted.
- **Limit:** schema validity does not establish authorization, semantic consistency, truth, policy adoption or evaluator correctness. Listing it does not select it as the canonical format.

<a id="r-14"></a>

- **Cited by:** [0008](architecture/0008-formalization-and-conformance.md), [0013](architecture/0013-governance-metamodel.md).
### R-14 — Semantic Versioning 2.0.0
- **Primary source:** [SemVer 2.0.0](https://semver.org/)
- **Relevant concepts:** MAJOR/MINOR/PATCH relative to a declared public API and compatibility contract; published versions are immutable.
- **Use in GovCheck:** informs the distinction between artifact identity, immutable revision, contract compatibility and release identity.
- **Limit:** SemVer is not meaningful for every governance artifact. GovCheck's category-specific versioning proposal avoids applying it mechanically to models, evidence instances, decisions or events.

<a id="r-15"></a>

- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md).
### R-15 — Git tags and releases
- **Primary sources:** [Git reference: tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging) · [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- **Relevant concepts:** identifying a source revision and publishing release-associated artifacts.
- **Use in GovCheck:** release-bound verification reports and manifests identifying the exact repository tree, commit, model/configuration and tool versions.
- **Limit:** a tag or release is an identifier/publication mechanism, not proof that verification ran or passed.

<a id="r-16"></a>

- **Cited by:** [0017](architecture/0017-artifact-identity-revision-and-versioning.md), [0018](architecture/0018-version-governance-and-compatibility-authority.md).
### R-16 — OpenAPI and machine-readable interface contracts
- **Primary source:** [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- **Relevant concepts:** machine-readable interface contracts.
- **Use in GovCheck:** possible future CLI/dossier interchange and adapter-contract documentation.
- **Limit:** interface conformance does not establish authorization semantics, runtime behavior or implementation correctness.

<a id="r-17"></a>

- **Cited by:** no current architecture or specification record cites this source; retained as supplementary reference.
### R-17 — Google Cloud Knowledge Catalog
- **Primary source:** [Knowledge Catalog documentation](https://docs.cloud.google.com/knowledge-catalog/docs)
- **Relevant concepts:** typed metadata, catalogue entries, relationships/lineage, governance metadata and context discovery.
- **Use in GovCheck:** the transferable pattern is type-specific mandatory metadata and traceable relationships between governed objects.
- **Limit:** GovCheck is not a data catalog. Do not import the product architecture or assume metadata presence equals normative authority or enforcement.

<a id="r-22"></a>

- **Cited by:** [0022](architecture/0022-governance-capability-audit.md).
### R-22 — Native Git and Pijul semantics
- **Primary sources:** [Git documentation](https://git-scm.com/docs) · [Pijul manual: theory](https://pijul.org/manual/theory) · [Pijul channels](https://pijul.org/manual/workflows/channels) · [Pijul conflicts](https://pijul.org/manual/conflicts.html)
- **Relevant concepts:** Git's snapshot/commit and tree model; Pijul's change/patch graph, channels and first-class conflicts.
- **Use in GovCheck:** supports the explicit VCS-adapter boundary and the requirement that candidate identity, conflict detection and application be represented using native semantics rather than forced into one shared Git-shaped abstraction.
- **Limit:** vendor documentation explains the systems' intended semantics; GovCheck still needs adapter contracts and conformance tests. This reference does not establish that either adapter is implemented.

- [0004 — VCS and Collaboration Adapter Contracts](specifications/0004-vcs-collaboration-contracts.md): R-22.


- **Cited by:** [0004](specifications/0004-vcs-collaboration-contracts.md).
## Academic foundations and assurance

<a id="r-18"></a>
### R-18 — Writ (infinri/Writ)
- **Primary sources:** [repository](https://github.com/infinri/Writ) · [security policy at reviewed revision](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/SECURITY.md) · [gate/session contract](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/docs/reference/session-and-gates.md)
- **Reviewed revision:** ebdafe5450b201339f81e717ed104e6bcfd3fe3e (review recorded 2026-11-06).
- **Use in GovCheck:** optional agent-workflow test fixture and possible source of scoped execution evidence.
- **Limit:** Writ explicitly says it is not a sandbox/security boundary; its output is not GovCheck's normative authority or independent acceptance decision. See Architecture 0016.

<a id="r-19"></a>

- **Cited by:** [0016](architecture/0016-writ-privateer-assessment.md).
### R-19 — Privateer (privateer-agent/privateer-agent)
- **Primary sources:** [repository](https://github.com/privateer-agent/privateer-agent) · [security policy at reviewed revision](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/SECURITY.md) · [README at reviewed revision](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/README.md)
- **Reviewed revision:** 181a988e443fa6b6b4138fc349d1260c96408ad4 (review recorded 2026-11-06).
- **Use in GovCheck:** candidate Pi-based agent-harness interoperability fixture.
- **Limit:** a permission gate, provenance feature or privacy warning does not replace canonical governance or independently verified acceptance. See Architecture 0016.

<a id="r-20"></a>

- **Cited by:** [0016](architecture/0016-writ-privateer-assessment.md).
### R-20 — Lean
- **Primary source:** [Lean language reference](https://lean-lang.org/doc/reference/latest/)
- **Relevant concepts:** proof terms checked by a small kernel; theorem proving under explicit definitions, axioms and hypotheses.
- **Use in GovCheck:** candidate for narrowly justified proof-critical predicates or certificate checking, if a later ADR supports it.
- **Limit:** a theorem about a predicate does not establish that the predicate captures approved policy or that the executable refines it. Lean is not selected as a product-wide dependency.

<a id="r-21"></a>

- **Cited by:** [0008](architecture/0008-formalization-and-conformance.md), [0010](architecture/0010-assurance-proof-and-conformance.md).
### R-21 — Research software release and reproducibility guidance
- **Primary source:** [Software Sustainability Institute — guides and resources](https://www.software.ac.uk/resources)
- **Relevant concepts:** sustainable research software, citation, releases and reproducibility.
- **Use in GovCheck:** supports recording exact software/tool versions and release context needed to interpret verification evidence.
- **Limit:** general guidance is not a concrete release-manifest contract. Link to a specific guide when relying on a particular recommendation.



<a id="r-23"></a>

- **Cited by:** no current architecture or specification record cites this source; retained as supplementary reference.
### R-23 — IMS Global / 1EdTech versioning specifications
- **Primary source:** [1EdTech specifications](https://www.imsglobal.org/spec/versioning/v1) (formerly IMS Global; consult the specific versioning specification before relying on a particular rule).
- **Relevant concepts:** version identifiers and compatibility conventions for structured, published artifacts.
- **Use in GovCheck:** comparative input to the category-specific artifact-versioning analysis in Architecture 0017–0018.
- **Limit:** a domain-specific education-technology specification family, not a universal governance-artifact versioning standard.
- **Cited by:** [Architecture 0017](architecture/0017-artifact-identity-revision-and-versioning.md), [Architecture 0018](architecture/0018-version-governance-and-compatibility-authority.md).

<a id="r-24"></a>
### R-24 — W3C PROV-O
- **Primary source:** [W3C PROV-O recommendation](https://www.w3.org/TR/prov-o/).
- **Relevant concepts:** entities, activities, agents and provenance relations.
- **Use in GovCheck:** vocabulary for provenance and relationships between artifacts, activities and responsible agents.
- **Limit:** an ontology does not itself provide repository policy, identity assurance or enforcement.
- **Cited by:** [Architecture 0017](architecture/0017-artifact-identity-revision-and-versioning.md), [Architecture 0018](architecture/0018-version-governance-and-compatibility-authority.md).

<a id="r-25"></a>
### R-25 — DataCite versioning guidance
- **Primary source:** [DataCite documentation on versioning](https://support.datacite.org/docs/versioning).
- **Relevant concepts:** identifying and relating versions of citable research outputs.
- **Use in GovCheck:** informs the distinction between a persistent logical artifact identity and individually identified versions.
- **Limit:** guidance for research outputs is not a general policy for all software and governance artifacts.
- **Cited by:** [Architecture 0017](architecture/0017-artifact-identity-revision-and-versioning.md), [Architecture 0018](architecture/0018-version-governance-and-compatibility-authority.md).

<a id="r-26"></a>
### R-26 — Scientific Data versioning study (2024)
- **Primary source:** [Nature / Scientific Data article](https://www.nature.com/articles/s41597-024-03153-y).
- **Relevant concepts:** versioning and provenance practices for scientific data.
- **Use in GovCheck:** comparative research input to the artifact identity and versioning discussion.
- **Limit:** domain-specific research does not establish a normative versioning rule for GovCheck.
- **Cited by:** [Architecture 0017](architecture/0017-artifact-identity-revision-and-versioning.md).


<a id="r-27"></a>
### R-27 — NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments
- **Primary source:** [NIST publication](https://csrc.nist.gov/pubs/sp/800/30/r1/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-30r1)
- **Relevant concepts:** threat sources and events, vulnerabilities, likelihood and impact, risk assessment, residual risk, assumptions, rationale and uncertainty.
- **Use in GovCheck:** supports scenario-based assessment that records how likelihood/plausibility is derived, the impact dimensions considered, safeguards already in place, uncertainty and the rationale for the result.
- **Limit:** NIST SP 800-30 is risk-assessment guidance, not a universal quantitative formula or a requirement to use a particular scoring scale. GovCheck must not turn illustrative scales into calibrated measurements.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (risk assessment and treatment).

<a id="r-28"></a>
### R-28 — NIST SP 800-160 Vol. 1 Rev. 1, Engineering Trustworthy Secure Systems
- **Primary source:** [NIST publication](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-160v1r1)
- **Relevant concepts:** systems security engineering across the lifecycle; stakeholder protection needs; requirements, architecture, implementation, verification, validation and risk management.
- **Use in GovCheck:** supports connecting protection needs and security requirements to architecture, controls, verification evidence and lifecycle decisions rather than treating threat analysis as a one-off questionnaire.
- **Limit:** the publication is engineering guidance, not a repository governance schema or proof that a particular system satisfies its security requirements.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (threat-led assurance, traceability and lifecycle).

<a id="r-29"></a>
### R-29 — ISO 31000:2018, Risk management — Guidelines
- **Primary source:** [ISO standard landing page](https://www.iso.org/standard/31000)
- **Relevant concepts:** principles and framework for identifying, analysing, evaluating, treating, monitoring, reviewing and communicating risk.
- **Use in GovCheck:** provides a general risk-management reference for keeping assessment, treatment, acceptance, monitoring and review connected to governance and decision-making.
- **Limit:** ISO 31000 is generic guidance, not a cybersecurity threat taxonomy or a prescribed risk-calculation algorithm. The full standard is not reproduced here.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (risk treatment and review).

<a id="r-30"></a>
### R-30 — MITRE ATT&CK
- **Primary source:** [MITRE ATT&CK knowledge base](https://attack.mitre.org/) · [Getting started and usage guidance](https://attack.mitre.org/resources/)
- **Relevant concepts:** adversary tactics and techniques grounded in observed behavior; mappings between techniques, platforms and mitigations.
- **Use in GovCheck:** optional vocabulary and evidence source for enriching threat scenarios and attack-path analysis, and for checking whether proposed controls address known adversary behaviors.
- **Limit:** ATT&CK is not an exhaustive threat model, likelihood estimator, vulnerability database or proof of exploitability. A technique mapping does not establish that a technique is feasible in the project's context or that a mitigation is effective.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (threat scenarios and attack paths).

<a id="r-31"></a>
### R-31 — Microsoft Security Development Lifecycle: Threat Modeling
- **Primary source:** [Microsoft SDL threat-modeling guidance](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- **Relevant concepts:** security requirements, system/data-flow diagrams, threat identification, mitigation and validation as an iterative engineering process.
- **Use in GovCheck:** industry example for guiding project owners through a repeatable threat-modeling workflow that links architecture and trust boundaries to mitigations and validation.
- **Limit:** Microsoft's workflow is a practical method, not a complete risk-governance or assurance-case standard. Its examples and tool are not mandatory GovCheck dependencies.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (guided threat modeling).

<a id="r-32"></a>
### R-32 — Bruce Schneier, “Attack Trees” (1999)
- **Primary source:** [Dr. Dobb's Journal article, archived by Schneier](https://www.schneier.com/academic/archives/1999/12/attack_trees.html)
- **Academic/technical reference:** Bruce Schneier, “Attack Trees,” Dr. Dobb's Journal, December 1999.
- **Relevant concepts:** hierarchical decomposition of attacker goals into alternative or conjunctive sub-goals; reasoning about attack feasibility and cost.
- **Use in GovCheck:** foundational technique for representing attack paths and alternative ways to reach a harmful objective, and for relating mitigations to specific path steps.
- **Limit:** attack trees are models whose completeness and parameter estimates require justification. Costs or probabilities assigned to nodes must not be treated as objective without calibrated evidence.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (attack paths and coverage gaps).

<a id="r-33"></a>
### R-33 — Mohamad, Steghöfer and Scandariato, “Security assurance cases—state of the art of an emerging approach” (2021)
- **Primary source:** [Empirical Software Engineering article](https://doi.org/10.1007/s10664-021-09971-7)
- **Academic reference:** Mazen Mohamad, Jan-Philipp Steghöfer and Riccardo Scandariato, *Empirical Software Engineering* 26, article 70 (2021).
- **Relevant concepts:** systematic literature review of 51 studies on security assurance cases; structured claims, argumentation, assumptions, context and evidence; state of validation and tool support.
- **Use in GovCheck:** supports keeping claims, assumptions, context, inference and evidence explicit, while treating assurance-case construction and maintenance as an engineering activity requiring validation.
- **Limit:** the review reports an immature research/practice landscape and gaps in validation and tool support; it does not establish that adopting an assurance-case notation automatically produces a valid security argument.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (assumptions, inference, evidence and assurance limits).

<a id="r-34"></a>
### R-34 — OMG Structured Assurance Case Metamodel (SACM)
- **Primary source:** [OMG SACM specification family](https://www.omg.org/spec/SACM/) · [formal version 2.3](https://www.omg.org/spec/SACM/2.3)
- **Relevant concepts:** machine-processable representation of assurance-case structures and relationships between claims, argumentation, artifacts and evidence.
- **Use in GovCheck:** candidate comparative metamodel for typed assurance artifacts and traceability, beyond free-form narrative documents.
- **Limit:** SACM is a metamodel, not a risk-assessment method, truth oracle or proof of evidence sufficiency. Version 2.4 is currently a beta; this entry points to the formal 2.3 version and does not recommend adopting SACM.
- **Cited by:** [0024](architecture/0024-project-bootstrap-and-assurance-profiles.md) (typed assurance claims and evidence).



## Additional sources recovered from the assurance and integration discussions

<a id="r-27"></a>
### R-27 — Common Criteria (ISO/IEC 15408) and Common Evaluation Methodology
- **Primary sources:** [Common Criteria Portal](https://www.commoncriteriaportal.org/) · [CC:2022 and CEM:2022 publications](https://www.commoncriteriaportal.org/cc/index.cfm)
- **Relevant concepts:** security functional requirements, security assurance requirements, evaluation methodology and Evaluation Assurance Levels (EALs).
- **Use in GovCheck:** contextualizes the assurance vocabulary explicitly contrasted with GovCheck's method classes in Specification 0005.
- **Limit:** EALs are evaluation assurance packages in the Common Criteria scheme, not generic software maturity grades or GovCheck assurance tiers. Certification scope and target-of-evaluation matter.

<a id="r-28"></a>
### R-28 — RTCA DO-178C / EUROCAE ED-12C airborne software assurance
- **Primary sources:** [FAA AC 20-115D](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D) · [RTCA DO-178C overview and supplements](https://www.rtca.org/do-178/)
- **Relevant concepts:** software life-cycle objectives, verification, independence, certification evidence and software levels (A–E); related supplements include DO-330, DO-331, DO-332 and DO-333.
- **Use in GovCheck:** provides the aviation-specific assurance/certification example named in Specification 0005 and distinguishes domain-specific assurance regimes from generic test/proof methods.
- **Limit:** DO-178C is an aviation software assurance standard used within an airworthiness certification context. FAA AC 20-115D describes an acceptable means, not the only means or a general software regulation. The full RTCA standard is not reproduced by the public overview.

<a id="r-29"></a>
### R-29 — Alloy language and Analyzer
- **Primary sources:** [Alloy project and documentation](https://alloytools.org/) · [Alloy Analyzer source repository](https://github.com/AlloyTools/org.alloytools.alloy)
- **Relevant concepts:** relational modeling, bounded analysis, SAT-based instance finding and counterexample search; Alloy 6 adds mutable state and temporal operators.
- **Use in GovCheck:** candidate formal-modeling method cited in Specifications 0005 and Architecture 0007/0009.
- **Limit:** results depend on declared scopes, bounds and model assumptions; Alloy analysis is not a proof about an implementation without a separate refinement/conformance argument.

<a id="r-30"></a>
### R-30 — SPIN and Promela
- **Primary source:** [SPIN Basic Manual and Promela documentation](https://spinroot.com/spin/Man/Manual.html)
- **Relevant concepts:** modeling and verification of concurrent and distributed systems, asynchronous communication, invariants, deadlocks and temporal properties.
- **Use in GovCheck:** candidate model checker named in Specification 0005 as a distinct alternative to TLA+/TLC and Alloy.
- **Limit:** verification applies to the Promela abstraction and selected search mode/options; it does not establish implementation conformance or normative fidelity.

<a id="r-31"></a>
### R-31 — Kani Rust Verifier
- **Primary source:** [Kani documentation](https://model-checking.github.io/kani/)
- **Relevant concepts:** bounded model checking of Rust programs, proof harnesses, assertions, undefined-behavior checks and counterexamples.
- **Use in GovCheck:** candidate program-verification method named in Specification 0005.
- **Limit:** supported Rust features and concurrency coverage are bounded; a successful harness proves only the modeled properties under the configured bounds and toolchain.

<a id="r-32"></a>
### R-32 — Verus Rust verification
- **Primary source:** [Verus tutorial and reference](https://verus-lang.github.io/verus/guide/)
- **Relevant concepts:** static functional-correctness verification for Rust using specifications and computer-aided proofs.
- **Use in GovCheck:** candidate program-verification method named in Specification 0005.
- **Limit:** Verus does not support all Rust features/libraries and does not claim to verify the Rust/LLVM compilers or itself; trusted components and unsupported constructs remain relevant.

<a id="r-33"></a>
### R-33 — Dafny language and verifier
- **Primary source:** [Dafny Reference Manual](https://dafny.org/dafny/DafnyRef/DafnyRef)
- **Relevant concepts:** specification constructs, pre/postconditions, invariants, termination metrics, verification conditions and compilation.
- **Use in GovCheck:** candidate program-verification system named in Specification 0005.
- **Limit:** verified claims are relative to Dafny specifications, verifier/toolchain and trusted backends; they do not validate whether the specification captures approved policy.

<a id="r-34"></a>
### R-34 — Coq / Rocq proof assistant
- **Primary sources:** [Rocq documentation and reference manuals](https://rocq-prover.org/docs) · [versioned Coq documentation archive](https://docs.rocq-prover.org/)
- **Relevant concepts:** dependent type theory, Gallina definitions and machine-checked proof terms.
- **Use in GovCheck:** Coq is named in Specification 0005; the project is now named Rocq, so both the historical and current names are recorded.
- **Limit:** a checked derivation establishes a theorem only under its definitions, axioms, imported results and kernel/toolchain assumptions; it does not establish normative adequacy.

<a id="r-35"></a>
### R-35 — Isabelle theorem prover
- **Primary source:** [Isabelle documentation, tutorials and reference manuals](https://www.isabelle.in.tum.de/documentation.html)
- **Relevant concepts:** interactive theorem proving, Isabelle/HOL, formal specification and proof checking.
- **Use in GovCheck:** candidate proof assistant named in Specification 0005.
- **Limit:** proof results depend on the selected logic, theory imports, axioms and trusted prover environment; no Isabelle integration is selected.

<a id="r-36"></a>
### R-36 — KAOS and goal-oriented requirements engineering
- **Primary source:** [Axel van Lamsweerde, Requirements Engineering: From System Goals to UML Models to Software Specifications (2009), UCLouvain record](https://research.dial.uclouvain.be/entities/publication/ddcd5cbc-c76d-4da2-bd29-509cbf0f9399)
- **Relevant concepts:** goal refinement, obstacles, responsibility assignment and derivation from system goals to requirements and software specifications.
- **Use in GovCheck:** grounds the KAOS/GORE goal-refinement family explicitly mentioned in Architecture 0013.
- **Limit:** this is a requirements-engineering method and scholarly source, not an adopted GovCheck ontology or executable policy language.

<a id="r-37"></a>
### R-37 — CRDT foundations
- **Primary source:** [Shapiro, Preguiça, Baquero and Zawirski, “A comprehensive study of Convergent and Commutative Replicated Data Types” (INRIA Research Report 7506, 2011)](https://dsf.berkeley.edu/cs286/papers/crdt-tr2011.pdf)
- **Relevant concepts:** state-based and operation-based replicated data types, convergence conditions, asynchronous replication and concurrent updates.
- **Use in GovCheck:** foundational source for the CRDT/co-editing discussion recovered from the Cartocortex integration study.
- **Limit:** convergence does not by itself preserve user intent, define authorization, solve persistence/transport, or guarantee that application-level invariants survive concurrent operations.

<a id="r-38"></a>
### R-38 — Yjs and Yrs
- **Primary sources:** [Yjs documentation](https://docs.yjs.dev/) · [Yjs source repository](https://github.com/yjs/yjs) · [Yrs Rust port](https://github.com/y-crdt/y-crdt)
- **Relevant concepts:** shared CRDT data types, transport-independent updates, synchronization providers and collaborative editing.
- **Use in GovCheck:** candidate implementation family explicitly compared in the Cartocortex PR #28 transport/backlog study.
- **Limit:** library behavior does not select an application data model or transport architecture; Cartocortex-specific tree moves, undo/redo, persistence and migration require separate conformance tests.

<a id="r-39"></a>
### R-39 — Automerge
- **Primary sources:** [Automerge documentation](https://automerge.org/docs/) · [Automerge source repository](https://github.com/automerge/automerge)
- **Relevant concepts:** local-first CRDT documents, concurrent change merging, history and transport-agnostic synchronization.
- **Use in GovCheck:** candidate implementation explicitly compared in the Cartocortex PR #28 study.
- **Limit:** a CRDT's merge semantics do not automatically preserve domain intent or enforce application permissions; networking and storage components must be evaluated separately.

<a id="r-40"></a>
### R-40 — Loro CRDT
- **Primary sources:** [Loro documentation](https://loro.dev/docs) · [Loro CRDT concepts](https://www.loro.dev/docs/concepts/crdt) · [Loro source repository](https://github.com/loro-dev/loro)
- **Relevant concepts:** movable trees/lists, rich-text CRDTs, local-first synchronization, history and time travel.
- **Use in GovCheck:** candidate explicitly highlighted in the Cartocortex PR #28 study because movable trees may fit mind-map structures.
- **Limit:** the library's feature matrix is not an independent suitability result; benchmark and test against Cartocortex's identity, move/delete, undo/redo and persistence invariants before selection.

<a id="r-41"></a>
### R-41 — WebRTC real-time communication
- **Primary sources:** [W3C WebRTC 1.0 Recommendation](https://www.w3.org/TR/webrtc/) · [IETF RFC 8835 — Transports for WebRTC](https://www.rfc-editor.org/rfc/rfc8835.html)
- **Relevant concepts:** peer connections, data channels, transport security and interaction with ICE, STUN and TURN.
- **Use in GovCheck:** primary protocol references for the peer-to-peer transport option discussed for Cartocortex co-editing.
- **Limit:** WebRTC does not define application signaling, room authorization, CRDT semantics or persistence. Peer-to-peer does not mean infrastructure-free or metadata-free.

<a id="r-42"></a>
### R-42 — ICE, STUN, TURN and relay infrastructure
- **Primary sources:** [RFC 8445 — ICE](https://www.rfc-editor.org/rfc/rfc8445.html) · [RFC 8489 — STUN](https://www.rfc-editor.org/rfc/rfc8489.html) · [RFC 8656 — TURN](https://www.rfc-editor.org/rfc/rfc8656.html) · [coturn relay implementation](https://github.com/coturn/coturn)
- **Relevant concepts:** candidate gathering and connectivity checks, NAT traversal, relay allocation and fallback when direct paths fail.
- **Use in GovCheck:** documents the precise protocol stack behind the STUN/TURN references in the Cartocortex integration discussion.
- **Limit:** STUN alone is not a NAT-traversal solution; TURN relays traffic and introduces availability, cost, privacy and operational considerations. The PDF's approximate relay-use estimate is a study claim, not a protocol guarantee.

<a id="r-43"></a>
### R-43 — Open Knowledge Format (OKF) v0.2
- **Primary sources:** [Canonical OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) · [OKF v0.2 specification in the original Knowledge Catalog repository](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- **Relevant concepts:** portable knowledge bundles built from Markdown, YAML frontmatter, links, provenance, trust and lifecycle metadata.
- **Use in GovCheck:** source of the OKF storage and mind-map projection study in Cartocortex PR #27; it is the specific meaning of “OKF” in that discussion.
- **Limit:** OKF is a lightweight knowledge-bundle convention, not a graph ontology, mind-map layout model, CRDT, transport protocol or GovCheck governance standard. The old Knowledge Catalog path is a frozen snapshot; use the dedicated repository as canonical.

<a id="r-44"></a>
### R-44 — RDF 1.1 data model
- **Primary source:** [W3C RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/)
- **Relevant concepts:** graph and dataset data model based on subject–predicate–object triples and IRIs.
- **Use in GovCheck:** foundational data model discussed for a possible shared knowledge representation across Cartocortex, MoriNet and SaussuNet.
- **Limit:** RDF is a data model, not a domain ontology, storage engine, validation language or collaboration protocol.

<a id="r-45"></a>
### R-45 — SKOS
- **Primary source:** [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)
- **Relevant concepts:** URI-identified concepts, labels, notations, concept schemes, mappings and lightweight semantic relations.
- **Use in GovCheck:** vocabulary considered for taxonomies and concept organization in the integration study.
- **Limit:** SKOS is not a general application object model or a substitute for OWL axioms, SHACL constraints or CRDT collaboration.

<a id="r-46"></a>
### R-46 — OWL 2 Web Ontology Language
- **Primary source:** [W3C OWL 2 Structural Specification and Functional-Style Syntax](https://www.w3.org/TR/owl-syntax/)
- **Relevant concepts:** formally defined ontology semantics for classes, properties, individuals and axioms.
- **Use in GovCheck:** candidate semantic layer discussed alongside RDF and SKOS in the integration study.
- **Limit:** OWL reasoning does not validate all application data constraints, preserve arbitrary source properties or provide workflow, access-control or synchronization behavior.

<a id="r-47"></a>
### R-47 — SHACL
- **Primary source:** [W3C Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/)
- **Relevant concepts:** validation of RDF graphs against declared shapes and constraints.
- **Use in GovCheck:** candidate for structural validation of normalized knowledge graphs in the SaussuNet integration discussion.
- **Limit:** SHACL validation is not proof of semantic truth, provenance authenticity, authorization or conformance of the transformation implementation.

<a id="r-48"></a>
### R-48 — Dublin Core Metadata Terms
- **Primary source:** [DCMI Metadata Terms specification](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- **Relevant concepts:** general-purpose metadata properties, classes and vocabulary terms for describing resources.
- **Use in GovCheck:** candidate metadata vocabulary discussed for documentary resources in the shared knowledge profile.
- **Limit:** Dublin Core terms do not define the full domain model, identity policy, access-control semantics or validation rules.

<a id="r-49"></a>
### R-49 — Bibliographic Ontology (BIBO)
- **Primary source:** [DCMI BIBO specification](https://www.dublincore.org/specifications/bibo/bibo/)
- **Relevant concepts:** RDF vocabulary for bibliographic resources, citations and document types.
- **Use in GovCheck:** supplementary vocabulary considered for reports, articles and bibliographic objects in the integration study.
- **Limit:** BIBO is a DCMI Community Specification, not an ISO or W3C Recommendation; it should be combined with broader metadata vocabularies only where needed.

<a id="r-50"></a>
### R-50 — Data Catalog Vocabulary (DCAT) 3
- **Primary source:** [W3C DCAT 3 Recommendation](https://www.w3.org/TR/vocab-dcat-3/)
- **Relevant concepts:** interoperable descriptions of datasets, data services, distributions and dataset series in catalogs.
- **Use in GovCheck:** candidate vocabulary for cataloguing knowledge bundles and collections in the integration study.
- **Limit:** DCAT describes catalogued datasets/services; it does not model all content semantics, application permissions or collaborative editing.

<a id="r-51"></a>
### R-51 — W3C Web Annotation Data Model
- **Primary source:** [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/)
- **Relevant concepts:** annotations, bodies, targets, selectors and motivations for annotating resources or specific fragments.
- **Use in GovCheck:** candidate model for comments, questions and annotations attached to pages or passages in the integration study.
- **Limit:** Web Annotation does not define a full knowledge graph, real-time co-editing protocol or authorization policy.

<a id="r-52"></a>
### R-52 — ActivityStreams 2.0
- **Primary source:** [W3C ActivityStreams 2.0 Core](https://www.w3.org/TR/activitystreams-core/)
- **Relevant concepts:** JSON-LD vocabulary and syntax for actors, objects, activities, collections and social interactions.
- **Use in GovCheck:** considered for representing published activities/events where the social-activity use case fits.
- **Limit:** ActivityStreams is not a provenance ledger, event-sourcing guarantee, access-control model or replacement for PROV-O.

<a id="r-53"></a>
### R-53 — P-Plan ontology
- **Primary source:** [P-Plan ontology specification](https://www.opmw.org/model/p-plan/)
- **Relevant concepts:** representation of abstract plans and their correspondence to PROV-O records of executed processes.
- **Use in GovCheck:** candidate vocabulary for describing intended ingestion/transformation plans alongside observed provenance.
- **Limit:** P-Plan is a domain ontology extending PROV-O, not a general workflow engine or W3C Recommendation.

<a id="r-54"></a>
### R-54 — Cartocortex, MoriNet and SaussuNet integration sources
- **Primary sources:** [Cartocortex repository](https://github.com/complexus-lab/cartocortex) · [MoriNet repository](https://github.com/lejeunecedric/MoriNet) · [SaussuNet repository](https://github.com/lejeunecedric/SaussuNet) · [Cartocortex PR #27 — OKF storage and graph-view study](https://github.com/complexus-lab/cartocortex/pull/27) · [Cartocortex PR #28 — CRDT, browser deployment and cloud-sync backlog](https://github.com/complexus-lab/cartocortex/pull/28)
- **Relevant concepts:** source repositories and reviewed design artifacts for the integration study; PR #27 is a study of OKF v0.2 storage/projections, while PR #28 contains proposed CRDT and real-time transport work.
- **Use in GovCheck:** preserves the concrete project-level sources behind the initial 224-page integration assessment and the discussion recorded by ADR 0002.
- **Limit:** PR #27 is a study, not an executed implementation; PR #28 is a proposal/backlog and its transport study is explicitly not executed. Repository capabilities must be rechecked at the reviewed revision before claiming current behavior. The “CKO” namespace in the PDF is a proposal, not an adopted external standard.

<a id="r-55"></a>
### R-55 — Mind-map and graph interchange formats
- **Primary sources:** [Freeplane documentation](https://docs.freeplane.org/) · [FreeMind project](https://freemind.sourceforge.io/wiki/index.php/Main_Page) · [XMind](https://xmind.app/) · [OPML 2.0 specification](https://opml.org/spec2.opml) · [GraphML specification](http://graphml.graphdrawing.org/specification.html)
- **Relevant concepts:** exchange of hierarchical mind maps, outlines and general graph structures, including format-specific metadata and layout information.
- **Use in GovCheck:** records the FreeMind, Freeplane, XMind, OPML and GraphML formats explicitly considered for SaussuNet import/export and Cartocortex visualization.
- **Limit:** these formats have different expressive power and metadata conventions. A successful parse is not lossless semantic round-tripping; conversion requires per-format fixtures and explicit loss reports.



<a id="r-56"></a>
### R-56 — Cloud storage APIs and S3 interoperability
- **Primary sources:** [Amazon S3 documentation and API](https://docs.aws.amazon.com/s3/) · [Google Cloud Storage interoperability](https://docs.cloud.google.com/storage/docs/interoperability) · [Google Drive API overview](https://developers.google.com/workspace/drive/api/guides/about-sdk) · [Microsoft Graph Drive resource](https://learn.microsoft.com/en-us/graph/api/drive-get?view=graph-rest-1.0) · [Azure Blob Storage introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) · [Hippius documentation](https://docs.hippius.com/) · [Hippius S3-compatible object storage](https://docs.hippius.com/storage/s3/advanced)
- **Relevant concepts:** object-storage APIs, S3-compatible endpoints, cloud-drive APIs, OAuth/credential scopes, client-side synchronization and provider-specific semantics.
- **Use in GovCheck:** preserves the storage-provider integration candidates named in Cartocortex PR #28: Amazon S3, Google Cloud Storage interoperability, Google Drive, OneDrive/Microsoft Graph, Azure Blob Storage and Hippius.
- **Limit:** “S3-compatible” does not mean identical semantics, consistency, IAM, versioning, eventing or multipart behavior. Provider APIs have distinct authentication and permission models. These were backlog candidates, not selected providers or implemented integrations.

<a id="r-57"></a>
### R-57 — Browser file access, local persistence and WebAssembly
- **Primary sources:** [MDN File System API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API) · [MDN Origin Private File System (OPFS)](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system) · [W3C Indexed Database API 3.0](https://www.w3.org/TR/IndexedDB-3/) · [WebAssembly specifications](https://webassembly.org/specs/) · [WebAssembly System Interface (WASI)](https://github.com/WebAssembly/WASI)
- **Relevant concepts:** user-mediated access to local files/directories, origin-private browser storage, IndexedDB persistence and WebAssembly execution interfaces.
- **Use in GovCheck:** preserves the browser-local deployment and persistence candidates named in Cartocortex PR #28, including File System Access, OPFS, IndexedDB and the conditional use of WebAssembly/WASI to reuse Rust code.
- **Limit:** browser APIs have support, permission, secure-context and quota constraints; OPFS is origin-private and not a user-visible directory. WASI is a system interface for WebAssembly runtimes, not a browser file-system permission bypass. The PR describes a proposed study/backlog, not a tested deployment.

<a id="r-58"></a>
### R-58 — Hyperswarm and HyperDHT peer discovery
- **Primary sources:** [Hyperswarm project](https://github.com/holepunchto/hyperswarm) · [HyperDHT implementation](https://github.com/holepunchto/hyperdht) · [Hyperswarm peer-discovery documentation](https://docs.pears.com/p2p/reference/building-blocks/hyperswarm/)
- **Relevant concepts:** topic-based peer discovery, distributed hash-table rendezvous, UDP hole punching and encrypted peer connections.
- **Use in GovCheck:** preserves the desktop peer-discovery alternative discussed in Cartocortex PR #28 alongside browser WebRTC signaling.
- **Limit:** Hyperswarm/HyperDHT is a separate networking stack, not browser-native WebRTC signaling. DHT operation depends on bootstrap infrastructure and network reachability; peer discovery does not define application room authorization, membership policy or persistence.

## Reference discipline and unresolved provenance

1. Prefer the standard body, publisher, official documentation or source repository over secondary summaries.
2. Reference identifier R-12 was retired when its duplicate Scorecard entry was consolidated into R-08; do not reuse the retired identifier.
3. Pin code assessments. Writ and Privateer links identify the revisions reviewed in Architecture 0016; refresh the pins before claims about current behavior.
4. Distinguish evidence classes. A standard, research paper, product documentation, source code, test result and model-checking report are different evidence types.
5. No implied adoption. Inclusion means “relevant to assess,” not “selected,” “required,” “compatible” or “implemented.”
6. No invented bibliography. The prior discussion mentioned “Agent Package Manager” but did not preserve a unique, verified project URL. It is intentionally not cited as an identified product until its identity is established.
7. Keep links close to claims. Architecture records should link to the few sources that support their specific claim and point here for the wider bibliography.
