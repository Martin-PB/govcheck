# GovCheck external reference catalogue

## Thematic index

| Theme | Entries |
|---|---|
| Governance authority, separation of duties and secure development | R-01–R-03, R-11 |
| Assurance cases, safety arguments and formal methods | R-04–R-05, R-20 |
| Evidence provenance and software supply chain | R-06–R-08 |
| Policy engines and authorization | R-09–R-10 |
| Schemas and interface contracts | R-13, R-16 |
| Artifact identity, versioning, releases and reproducibility | R-14–R-15, R-21, R-23–R-26 |
| Governance metadata and catalogues | R-17 |
| Agent workflow systems assessed as fixtures | R-18–R-19 |
| Version-control semantics and collaboration | R-22 |

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

## Reference discipline and unresolved provenance

1. Prefer the standard body, publisher, official documentation or source repository over secondary summaries.
2. Reference identifier R-12 was retired when its duplicate Scorecard entry was consolidated into R-08; do not reuse the retired identifier.
3. Pin code assessments. Writ and Privateer links identify the revisions reviewed in Architecture 0016; refresh the pins before claims about current behavior.
4. Distinguish evidence classes. A standard, research paper, product documentation, source code, test result and model-checking report are different evidence types.
5. No implied adoption. Inclusion means “relevant to assess,” not “selected,” “required,” “compatible” or “implemented.”
6. No invented bibliography. The prior discussion mentioned “Agent Package Manager” but did not preserve a unique, verified project URL. It is intentionally not cited as an identified product until its identity is established.
7. Keep links close to claims. Architecture records should link to the few sources that support their specific claim and point here for the wider bibliography.
