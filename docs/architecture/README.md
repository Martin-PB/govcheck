# Architecture records

English is the default language. Each record has a French counterpart.

- [0006 — Threat and trust model](0006-threat-and-trust-model.md) · [Français](0006-threat-and-trust-model.fr.md)
- [0007 — Technology decision framework](0007-technology-decision-framework.md) · [Français](0007-technology-decision-framework.fr.md)
- [0008 — Formalization and conformance plan](0008-formalization-and-conformance.md) · [Français](0008-formalization-and-conformance.fr.md)
- [0009 — GovCheck design discussion record](0009-govcheck-design-discussion-record.md) · [Français](0009-govcheck-design-discussion-record.fr.md)
- [0010 — Assurance, testimony, proof and conformance](0010-assurance-proof-and-conformance.md) · [Français](0010-assurance-proof-and-conformance.fr.md)
- [0011 — Lifecycle model: assertion-by-assertion audit](0011-lifecycle-model-assertion-audit.md) · [Français](0011-lifecycle-model-assertion-audit.fr.md)
- [0012 — Canonical normative authority and documentation conformity](0012-normative-authority-and-documentation.md) · [Français](0012-normative-authority-and-documentation.fr.md)
- [0013 — Governance metamodel](0013-governance-metamodel.md) · [Français](0013-governance-metamodel.fr.md)
- [0014 — Governed development workflow and actor responsibilities](0014-governed-development-workflow.md) · [Français](0014-governed-development-workflow.fr.md)
- [0015 — Governance conformance tool and validation plan](0015-governance-conformance-and-validation-plan.md) · [Français](0015-governance-conformance-and-validation-plan.fr.md)
- [0016 — Source-based assessment of Writ and Privateer](0016-writ-privateer-assessment.md) · [Français](0016-writ-privateer-assessment.fr.md)
- [0017 — Artifact identity, revision and versioning policy](0017-artifact-identity-revision-and-versioning.md) · [Français](0017-artifact-identity-revision-and-versioning.fr.md)
- [0018 — Version governance, compatibility and approval authority](0018-version-governance-and-compatibility-authority.md) · [Français](0018-version-governance-and-compatibility-authority.fr.md)
- [0019 — Artifact catalogue and release-manifest evolution](0019-catalogue-and-release-manifest-migration.md) · [Français](0019-catalogue-and-release-manifest-migration.fr.md)
- [0020 — First recorded TLC execution on the lifecycle model](0020-first-tlc-execution-record.md) · [Français](0020-first-tlc-execution-record.fr.md)
- [0021 — Assurance claims, arguments and evidence freshness](0021-assurance-claims-and-freshness.md) · [Français](0021-assurance-claims-and-freshness.fr.md)
- [0022 — Governance capability audit](0022-governance-capability-audit.md) · [Français](0022-governance-capability-audit.fr.md)
- [0023 — Bootstrap governance authority decision](0023-bootstrap-governance-authority.md) · [Français](0023-bootstrap-governance-authority.fr.md)
- [0024 — Project bootstrap, governance choices and domain capability profiles](0024-project-bootstrap-and-assurance-profiles.md) · [Français](0024-project-bootstrap-and-assurance-profiles.fr.md)
- [0025 — Cross-domain lifecycle observations, PEAK decision traceability and SACM integration](0025-runtime-observations-peak-and-sacm.md) · [Français](0025-runtime-observations-peak-and-sacm.fr.md)
- [0026 — SACM 2.4-conformant assurance capability and GovCheck integration](0026-sacm-24-conformance-and-govcheck-integration.md) · [Français](0026-sacm-24-conformance-and-govcheck-integration.fr.md)
- [0027 — Domain semantic standards, decision models and bootstrap commitments](0027-domain-semantic-standards-decisions-and-bootstrap.md) · [Français](0027-domain-semantic-standards-decisions-and-bootstrap.fr.md)
- [0028 — Governed work portfolio and issue-tracker boundary](0028-governed-work-portfolio-and-issue-tracker-boundary.md) · [Français](0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md)
- [0029 — Concern-scoped CI and formal verification boundaries](0029-concern-scoped-ci-and-formal-verification-boundaries.md) · [Français](0029-concern-scoped-ci-and-formal-verification-boundaries.fr.md)
- [0030 — Repository-backed governed work portfolio and recoverable revision history](0030-repository-backed-work-portfolio-and-recoverable-history.md) · [Français](0030-repository-backed-work-portfolio-and-recoverable-history.fr.md)
- [0031 — First TLC execution of the governance-applicability model](0031-first-tlc-governance-applicability.md) · [Français](0031-first-tlc-governance-applicability.fr.md)

Architecture 0028 defines the portfolio lifecycle and the issue-tracker boundary. Architecture 0030 adds the repository-backed registry, stable work-item identity, append-preserving logical events, native VCS revision binding, migration rules and explicit limitations of the initial history/recovery mechanism. Neither record claims that a registry engine, tamper-proof journal, automatic adapter synchronization or enforcement service is implemented.

Records 0009–0027 preserve design rationale, assurance distinctions, governance capability findings, the initial governance-authority decision and the proposed guided project-bootstrap experience. Record 0022 audits the gap between governance designs and an adopted, executable canonical authority; its recommendations are proposals, not approved policy. Record 0023 records the initial governance-authority decision; its integration into the registry and executable formalization remain separate work. Record 0024 proposes a guided, non-destructive bootstrap with selectable domain capabilities and assurance methods while preserving invariant governance foundations; it is not an implemented capability. Record 0025 situates observations across the repository lifecycle and multiple engineering domains, and distinguishes PEAK decision traceability from SACM assurance semantics. Record 0026 proposes complete SACM 2.4 Beta 1 semantic coverage as a dedicated GovCheck assurance capability, with explicit cross-model mappings and conformance tests. Record 0027 generalizes the bootstrap into explicit, versioned commitments to domain models and standards; it distinguishes PEAK decision rationale, DMN decision logic, BPMN process flow, CMMN adaptive case work, SACM assurance and GovCheck's authority/lifecycle governance. Its candidate standards inventory is a research baseline, not a set of adopted dependencies. None of these records makes SACM the repository-wide governance metamodel. Record 0021 proposes claims, argument, dependency and invalidation semantics; it remains to be model-checked and connected to the lifecycle. Record 0019 proposes a staged catalogue and release-manifest migration; it remains a proposal, not an implemented control or approved normative rule. Record 0017 defines the adopted category-specific policy separating logical identity, immutable revisions, contract compatibility versions, release identities and evidence/event instances. ADR 0004 adopts this policy and the version-governance process in 0018. SemVer is not universal; automated enforcement remains unimplemented.

## Reference index

Use the [single thematic and detailed reference catalogue](../references.md) ([Français](../references.fr.md)) for external sources, their uses and limits, and backlinks to citing records. Follow the [reference-integrity maintenance guide](../reference-integrity.md) and run the offline checker before submitting catalogue changes. Inclusion does not imply adoption or implementation.

PR #21 has been merged and records the bootstrap authority baseline. ADR 0004 is merged and adopts Architecture Records 0017 and 0018 as the category-specific versioning and version-governance policies. This does not mean that the version-decision schemas, authority resolver, compatibility evaluator or release automation are implemented. Other records remain proposals/design records unless their individual status says otherwise.

## Status

Architecture records are proposals/design records unless stated otherwise. They are not evidence of implemented controls, verified security properties or technology adoption. Read each record's status, scope and limits.
