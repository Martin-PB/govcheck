# 0014 — Governed development workflow and actor responsibilities

**Status:** workflow contract proposed for review; no agent orchestration, task templates or approval enforcement is claimed to exist. **French:** [0014](0014-governed-development-workflow.fr.md).

## Scope and dossier

GovCheck governs the repository and proposed-change lifecycle. It does not supervise every agent tool call, provide a sandbox or own agent memory. Humans and agents are contributors. The workflow guides work from request interpretation through implementation, verification, review, acceptance and application. It applies to every repository; obligations vary by scope/profile, not repository-size tiers.

Before substantive work, resolve a dossier bound to repository/base/candidate identities (including relevant uncommitted state), governance and specification revisions, change type, affected goals/components, impact and initiating actor/authority. A dossier is not a branch, commit, patch, PR or chat thread; these are linked native objects.

The task statement records intent, acceptance criteria, non-goals, scope, constraints, risks, assumptions, dependencies, required decisions and expected evidence. Missing or contradictory input is recorded, not silently invented.

## Governed sequence

1. **Discover governance:** locate/validate canonical source, applicable profiles, project instructions and tool capabilities; report missing, conflicting, unsupported or stale governance.
2. **Interpret request:** restate intent/acceptance criteria; distinguish facts, assumptions, constraints and open decisions.
3. **Impact analysis:** trace affected goals, requirements, norms, properties, components, interfaces, data and trust boundaries.
4. **Plan:** identify obligations, prohibitions, permissions, reviews, verification methods, evidence and authority; plan before destructive/irreversible operations.
5. **Design:** update architecture/contracts/models where required; assess consistency and feasibility; record decisions.
6. **Implement:** make the smallest coherent change while preserving native repository/VCS semantics.
7. **Verify:** run applicable checks under declared constraints; capture exact invocation, inputs, tools, environment, subject identity, outputs and limits.
8. **Review assurance:** map mandatory claims to admissible evidence; preserve failures, unknowns, contradictions and deviations; no self-approval.
9. **Request decision:** submit exact candidate and dossier to authorized reviewers/authority.
10. **Accept/apply:** derive acceptance from governance predicate; revalidate exact identities immediately before application; record native adapter receipt.
11. **Close dossier:** preserve decisions, evidence references, deviations, invalidations and lessons.

A different sequence may be justified, but reason and assurance impact are recorded. A task cannot skip a mandatory gate merely by calling itself documentation or refactoring.

## Task classes

| Class | Impact questions | Typical assurance |
|---|---|---|
| Feature | Which goals, requirements and interfaces change? | Acceptance vectors, tests, docs, architecture review |
| Bug fix | Which expected behavior failed and what is regression scope? | Reproduction, regression test, root-cause evidence |
| Security | Which assets, threats, trust boundaries and abuse cases change? | Threat analysis, adversarial tests, review, provenance |
| Architecture | Which contracts/components/quality attributes change? | ADR, consistency/feasibility analysis, model updates |
| Dependency/toolchain | Which trust, build, license and reproducibility assumptions change? | Version/digest, SBOM or equivalent, compatibility/security evidence |
| Formal model/specification | Which approved clauses are formalized and what is abstracted away? | Parser/model checks, counterexample review, traceability |
| Docs/governance | Is content normative, operational or explanatory? | Rule mapping, translation/projection drift, authority approval |
| Release/application | Which exact candidate/artifacts are published/applied? | Manifest, attestations, freshness, exact identity receipt |

These are workflow templates, not assurance tiers.

## Roles and separation of duties

Roles are logical responsibilities; one person may hold several in a small project, but incompatible actions remain distinguishable.

- **Contributor (human/agent):** proposes changes, reports work and supplies evidence; their assertion is not authoritative by itself.
- **Implementer/agent:** works within delegated scope; cannot approve its own exception, certify its own authority or be sole verifier of evidence it produced when independent verification is required.
- **Validator:** checks claims/evidence using an identified method and trust context; independence is claim-relative and disclosed.
- **Reviewer:** examines design, impact, reasoning and limits; a review comment is not acceptance unless governance explicitly grants that authority and binds it to the candidate.
- **Governance authority:** approves normative rules, exceptions and acceptance within explicit scope.
- **Operator/administrator:** operates local/shared enforcement; privileges and bypass capabilities are disclosed.
- **Adapter/service:** reports native repository/forge operations and capabilities; it does not invent governance approval.

An agent cannot be the sole source of truth for command execution or test results when independent verification is required. Role overlap and compensating review are recorded; higher-risk policy may require separation.

## Agent interoperability and qualification

The mandatory baseline is a documented deterministic CLI with machine-readable output. Agent-specific adapters may improve ergonomics but contain no normative logic. MCP was discussed as optional in an earlier iteration; it is not a mandatory dependency. Future interfaces call the same semantics as the CLI and do not create a second evaluator.

Agent qualification is a scoped claim about agent/harness version, configuration, permissions and task class: can it discover governance, preserve identities, report uncertainty, avoid prohibited actions, gather admissible evidence, respect human authority and produce a reviewable dossier? It is neither a universal badge nor a sandbox guarantee. Refresh it when harness, tools, permissions, governance or environment changes.

## Institutional record

The dossier/history preserves decisions, rationale, accepted/rejected alternatives, ADRs, rule changes, exceptions, verification results, invalidations and lessons. Git history records file changes but not necessarily authority, rationale, supporting evidence or exception expiry. This is an auditable project record, not semantic agent memory. Protect access and privacy; do not copy secrets/private data into governance records.

## Limits and sequencing

A local CLI cannot stop a privileged contributor bypassing local hooks or editing files. Shared enforcement requires a trusted integration boundary able to prevent application and recheck the exact candidate. Reporting failure is not blocking application. Mandatory unknowns remain unknown; request clarification or a governed exception, never invent one.

Start with a small CLI contract and dossier, task templates and language-neutral conformance vectors. Validate against representative repositories and different agent harnesses before optional adapters/remote integration. Do not wait for every formal proof, but preserve stable identities and traceability.

## Bibliographic references

- [R-02 — NIST SP 800-218 secure software development practices](../references.md#r-02)
- [R-03 — GitHub protected-branch enforcement and bypass limitations](../references.md#r-03)
- [R-06 — in-toto software supply-chain provenance](../references.md#r-06)
- [R-07 — SLSA software supply-chain assurance](../references.md#r-07)
- [R-18 — Writ source-based agent-workflow assessment](../references.md#r-18)
- [R-19 — Privateer source-based agent-workflow assessment](../references.md#r-19)
- [R-16 — OpenAPI machine-readable interface contracts](../references.md#r-16)
- [R-22 — native Git and Pijul semantics](../references.md#r-22)
