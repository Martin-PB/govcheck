# GovCheck applicability: repository responsibilities, external dependencies and user fit

**Status:** non-normative cross-source synthesis and audit framework. The applicability labels and mappings below are working analysis aids, not adopted GovCheck vocabulary or product behavior.
**Prepared:** 2026-11-11.

## Research basis and scope

This synthesis is not the analysis of one conference. It consolidates the earlier research review of AI-assisted quality, maintainability, agentic TDD and organizational practice ([research review](ai-assisted-quality-governance.md)), the separate [software-factory conference analysis](software-factory-self-improvement.md), and the supporting academic, standards and industry sources described in the earlier [AI-assisted quality and governance research review](ai-assisted-quality-governance.md), including empirical work on code health, downstream maintainability, large-scale change context, agent-generated pull requests and practitioner workflows.

The purpose is to determine what GovCheck can reasonably govern or assess at repository level, what requires external evidence or organizational action, and what should be communicated as a limitation or applicability condition. It also develops a provisional user-facing answer to the question “When is GovCheck an appropriate fit?” without claiming that the planned product is already implemented.

The existing [Architecture 0024](../architecture/0024-project-bootstrap-and-assurance-profiles.md) already proposes a context-sensitive bootstrap and recommendation process. This document is an input to its review, not an amendment or adoption.

## 1. The design question

GovCheck is a general-purpose governance bootstrap for repositories and must not pretend that a repository-local executable can control every system around it. The practical question is:

**For each governance concern, what can be deterministically checked or enforced at the repository boundary; what can only be recorded or evaluated as evidence; what depends on external actors/infrastructure; and what must remain an explicit warning, assumption, or acceptance decision?**

This classification should be applied to each proposed control individually, not used to label an entire concern “enforceable” or “unenforceable”. A repository can, for example, require a declared sandbox profile and validate its configuration while still being unable to prove that a remote provider actually isolates workloads as claimed.

## 2. Candidate applicability classes

These are proposed audit labels, not adopted GovCheck vocabulary. Their semantics should be tested against the current metamodel before adding new concepts.

| Class | Meaning | Appropriate repository response |
|---|---|---|
| **E — Enforceable locally** | The repository has the relevant inputs and can decide compliance deterministically within a defined trust boundary. | Validate schema, policy, signatures, required artifacts, test results, permitted state transitions, or release predicates; fail closed where the repository's adopted policy requires it. |
| **V — Verifiable only with external evidence** | A meaningful claim is checkable only if a trusted actor/provider supplies evidence or a queryable attestation. | Bind evidence to issuer, scope, time, configuration and revision; check its format, provenance and validity; state what the evidence does not establish. |
| **O — Observable/recordable, not enforceable by GovCheck alone** | The concern can be measured or declared, but GovCheck cannot make the underlying system behave as claimed. | Record measurements, source, method, uncertainty and owner; compare to an explicitly adopted criterion if one exists; avoid presenting a score as a guarantee. |
| **P — External precondition** | Success depends on infrastructure, people, organization, service terms, credentials or decisions outside the repository's authority. | State the assumption/precondition, owner, verification method and failure consequence; require explicit acceptance or block a claim that depends on it. |
| **W — Warning / heads-up** | The repository can explain a material risk or limitation but cannot resolve it unilaterally, or no adopted policy makes it a rejection condition. | Emit a contextual warning with rationale and suggested evidence/action; distinguish warning from failure and permit an authorized risk decision where governance allows. |
| **X — Out of scope for repository enforcement** | The concern cannot reasonably be controlled or reliably observed at this boundary. | Declare the boundary and residual risk; do not claim coverage. Revisit only if the system boundary or available authority changes. |

Classes may compose. For example, local validation of a declared runner configuration is E; proof that a cloud provider's underlying isolation works may be V or P; the residual risk of provider compromise may remain W/P/X. The classification should identify the *claim* and *boundary*, not merely the topic.

## 3. Initial concern map

This is a hypothesis map for the next GovCheck audit, not a claim that every listed control already exists or is missing.

| Concern | Likely class at repository boundary | What GovCheck can reasonably do | What remains outside its direct control |
|---|---|---|---|
| Governance files, schemas, required fields and internal links | E | Parse and validate repository-owned declarations; reject malformed or inconsistent artifacts. | Whether the declarations describe reality. |
| Required checks and evidence bound to a commit/revision | E/V | Require evidence records, verify artifact identity and freshness metadata, reject stale or absent evidence when policy says so. | Truthfulness of external evidence and completeness of the checked properties. |
| CI workflow definitions and test execution results | E/V | Inspect versioned workflow definitions; consume signed/identified results; verify expected jobs and result-to-revision binding. | Runner integrity, platform availability, secret exposure, or whether tests encode the right requirements. |
| Forge branch protection, reviews and merge permissions | V/P | Document desired settings and, where APIs/permissions permit, inspect them; verify status before making a claim. | Administrator/bypass privileges, forge outages, policy drift and actions by authorized humans. |
| Agent workflow definitions stored in the repository | E | Review configuration changes, validate schemas, version prompts/roles/tool grants, and test deterministic workflow predicates. | A provider's actual execution semantics, hidden platform defaults and model nondeterminism. |
| Agent sandbox profile declared as code | E/V | Check that a declared profile meets local policy and that runs identify the profile. | Whether host/kernel/cloud controls are effective, escape resistance, side channels and provider operations. |
| Secrets and credentials | E/V/P | Detect forbidden secret material in tracked files; declare required secret classes and least-privilege expectations; inspect permission evidence where available. | Secret manager configuration, runtime leakage, provider access, rotation and human handling unless integrated evidence is available. |
| Model/harness selection and reproducibility | E/O | Record model identifiers, versions, prompts, tool configuration, sampling settings and task context where available. | Hidden model updates, unavailable weights, provider-side changes and exact reproducibility of stochastic services. |
| Cost, latency, throughput and quality metrics | O/V | Define metric semantics, units, denominators, scope, provenance, uncertainty and comparison rules; calculate from available records. | Whether metrics capture business value, missing events, provider billing accuracy or generalize to future work. |
| LLM-as-judge / agent-generated scoring | V/O | Require scorer identity/version, rubric, calibration set, sampling, disagreement/error analysis and human escalation criteria. | Judge reliability, shared model blind spots, correlated evaluator/generator errors and subjective rubric choices. |
| Local benchmark suite and replayed tasks | E/O | Version task sets, expected outcomes, environment, scoring logic and benchmark revisions; compare configurations on the same cases. | Representativeness, selection bias, hidden leakage, changes in real-world task mix and external validity. |
| Self-improvement of the factory | E/V | Require proposed changes to be versioned, reviewed and checked like other repository changes; record the run and evidence motivating each proposal. | Whether an improvement transfers beyond the benchmark, and the external platform's actual deployment path. |
| Human review, expertise, training and staffing | P/O | Specify required roles, attestations, review scope, conflicts and evidence of completion where policy allows. | Actual competence, attention, organizational incentives, capacity and whether the reviewer independently challenged the claim. |
| Data ownership, privacy, residency and retention | V/P | Record data-flow assumptions, approved destinations, policy declarations and provider attestations; flag missing terms/evidence. | Actual provider handling, subprocessors, legal interpretation, deletion from backups, jurisdiction and contract enforcement. |
| Operational outcomes after release | O/V | Record incidents, defects, rollback, maintenance, rework and later observations linked to released revisions. | Complete telemetry, user context, external causes and causal attribution. |
| Human authority to approve risk or merge | E/V/P | Encode required approval records and repository-enforced protections where available; distinguish approval from technical evidence. | Identity assurance, collusion, admin bypass, out-of-band changes and the legitimacy of the authority model itself. |

## 4. What the evidence says—and does not say

The talk's “measure on your own tasks” recommendation is a reasonable experimental principle, not a guarantee. The METR randomized trial studied 16 experienced developers, 246 tasks and mature repositories familiar to the developers; it found early-2025 AI tools increased completion time by 19% in that setting, despite participants expecting a speed-up. This result should not be generalized to all developers or current tools; it does demonstrate why self-reported productivity, benchmark performance, and measured outcomes should be kept distinct. See [R-164](../references.md#r-164).

Warp's docs describe a specific commercial implementation: versioned factory definitions, agent stages, scorers, benchmarks, self-improvement proposals and human approval checkpoints. This is a concrete industrial example, not a neutral standard. In particular, an LLM judge's score is itself evidence from a fallible evaluator, not ground truth. A factory configuration in Git does not, by itself, prove that the cloud runtime executed exactly that configuration or that external permissions were correctly applied.

NIST AI RMF's Generative AI Profile offers risk-management guidance for organizations; it is not a repository-local enforcement engine. SSDF and existing supply-chain/provenance sources similarly inform practices but do not prove a particular implementation conforms merely because the references are cited.



The earlier research review also supplies important counterweights to the software-factory narrative: studies report context-dependent relationships between code health and AI refactoring, no clear universal downstream maintainability penalty in one preregistered setting, substantial contextual confounds in large-scale data, and a non-trivial share of agent-authored PRs needing further changes after merge. Practitioner TDD/example-mapping workflows offer useful ways to clarify intent and test oracles, but remain methods to select per project rather than universal requirements. Industry interviews and DORA-style organizational evidence are prompts for local assessment, not causal proof that a particular operating model will work. Two supplied video identifiers (R-160 and R-161) remain unresolved in the earlier review; no content claims should be inferred from them.

### 4.1 What the earlier multi-source review contributes

The preceding review of supplied talks, practitioner material and academic studies adds several counterweights to any simple “more agents means more productivity” narrative:

- **Code health and AI refactoring:** the FORGE 2026 study reports context- and model-dependent associations between code-health measures and semantic preservation as measured by tests. This supports examining maintainability and comprehensibility as context; it does not establish a universal metric threshold or prove semantic equivalence beyond the test oracle.
- **Downstream maintainability:** the preregistered *Echoes of AI* study did not find a clear systematic downstream maintainability or evolution-time penalty in its studied setting. GovCheck should not encode the blanket assumption that AI-assisted code is necessarily less maintainable.
- **Large-scale engineering data:** the ESEM study highlights contextual confounds such as code centrality, change size, testing and author experience. Any comparison needs an identified population, task mix, baseline and denominator.
- **Agent-authored pull requests:** the Claude Code PR study reports both eventual merges and substantial follow-up changes among merged PRs. Merge status is a workflow outcome, not a correctness or assurance result; provenance must identify the exact revision reviewed and integrated.
- **Practitioner workflows:** Emily Bache's EXACT/TDD account shows how example mapping, explicit acceptance examples and a feedback loop can help clarify intent and test oracles. These are selectable practices, not universal requirements; hidden tests still establish only their encoded properties.
- **Organizational adoption:** the McKinsey interview and DORA material motivate attention to engineering standards, training, task selection, review capacity and feedback loops. They do not establish one universal organizational model or causal effect for every team.
- **AI-friendly code:** Adam Tornhill's talk is a useful practitioner hypothesis about code health and AI-assisted change, but a proposed metric or heuristic must be assessed against independent evidence and the project's own goals.

The two other supplied video identifiers retained as R-160 and R-161 were not independently resolved in the earlier review. They remain explicit research gaps; no title, speaker, claim or applicability conclusion should be inferred from the URLs alone.

Taken together, the evidence supports **context-sensitive evaluation and honest uncertainty**, not a universal AI workflow, maturity score, productivity promise or mandatory quality metric. The earlier [research review](ai-assisted-quality-governance.md) contains the detailed source descriptions and limitations.

## 5. Proposed boundary record for each requirement or claim

Before implementing a control, the audit should be able to answer:

1. **Claim/control:** what exact property or obligation is being asserted?
2. **Boundary and subject:** which repository, revision, runner, service, team, agent or organization does it concern?
3. **Applicability class:** E, V, O, P, W or X (or a documented composition).
4. **Authority:** who can enforce it, who can attest to it, and who can accept residual risk?
5. **Mechanism:** local deterministic check, external attestation, observation, warning, or explicit assumption?
6. **Evidence contract:** source/issuer, method and version, scope, timestamp, revision/configuration binding, freshness/invalidation rule and known limitations.
7. **Failure semantics:** reject, block a claim, request evidence, warn, or allow an authorized exception?
8. **Residual risk:** what remains unverified, who owns it, and what decision is required?
9. **Bypass and threat model:** who can change the rule, suppress the signal, alter the runner, forge evidence or bypass the enforcement point?
10. **Review trigger:** what change or observation requires reassessment?

Do not add this as a new metamodel object solely because it is a useful checklist. First map each field to existing claims, requirements, policies, decisions, evidence, assumptions, exceptions and authority concepts; record any genuine expressiveness gap before proposing a schema change.

## 6. Adversarial cases for future tests

Not implemented or executed by this research change. Reconcile them with existing lifecycle, enforcement-boundary and evidence-freshness fixtures before creating duplicates.

- **SF-01 — Prompt-only guardrail:** a prompt says “never merge without approval,” but the token has merge permission and branch protection is absent.
- **SF-02 — Declared sandbox, unverified runtime:** the repo declares an approved sandbox profile, but the run record does not identify the effective runtime/configuration.
- **SF-03 — Green benchmark, wrong target:** the benchmark passes while its tasks do not represent the repository's high-risk changes.
- **SF-04 — Judge correlated with generator:** the same model family produces code and judges its quality, with no calibration or independent sample.
- **SF-05 — Cost/quality denominator drift:** a new configuration appears cheaper because retries, review time, failed runs or downstream rework were excluded.
- **SF-06 — Self-improvement bypass:** an agent's proposed factory-definition change is deployed outside the required review and CI path.
- **SF-07 — Stale provider attestation:** sandbox/security evidence applies to a previous runner image, account, region or configuration.
- **SF-08 — Missing external prerequisite:** a repository says data residency is assured but no provider/contract/runtime evidence is available.
- **SF-09 — Warning misrepresented as enforcement:** documentation claims GovCheck prevents a risk although it only emits a warning.
- **SF-10 — Authorized bypass:** a privileged administrator bypasses required checks; the evidence report still claims the integration boundary was enforced without qualification.

Expected behavior: state exactly which predicate was checked, against which revision/configuration, by which authority, with which evidence and limitations. A missing external guarantee must not silently become a passed local check.

## 7. Proposed next step

Use the existing governance and assurance audit to classify current requirements and controls, beginning with the repository enforcement boundary, evidence provenance/freshness, authorization, and revision applicability. Keep a gap register with one row per *claim/control*, not one row per broad topic. For each row record: current coverage, class, local mechanism, external dependency, evidence needed, failure behavior, bypass path, residual-risk owner and linked issue/decision.

Do not assume GovCheck must operate a cloud software factory. Its purpose is to govern repositories and make assurance boundaries explicit across different workflows and forges. A repository can describe and validate its local contract, request or verify external evidence when integrations exist, and refuse unjustified claims; it cannot turn an untrusted provider, insufficient organizational capacity, unreliable measurement or privileged bypass into a guarantee by documenting it.

## 8. User-facing applicability: when GovCheck is and is not a fit

The eventual product should not present GovCheck as universally sufficient, nor reduce applicability to project size or a single maturity score. Suitability depends on the governance boundary, the claims the project needs to support, the authority available to enforce decisions, and the evidence that can be obtained.

### 8.1 Strong fit

GovCheck is conceptually a strong fit when a project needs to:

- make repository governance, decision authority and change-acceptance rules explicit and traceable;
- connect intentions, objectives, requirements, specifications, changes, verification evidence, assurance arguments and authorized decisions;
- govern both human and agent contributions without treating agent output or a green check as authorization;
- preserve evidence provenance, revision applicability, uncertainty, assumptions, exceptions and accepted residual risk;
- bootstrap or evolve governance in a non-destructive, profile-driven way;
- operate across Git or Pijul and different local, team-hosted, self-hosted or public collaboration arrangements, subject to the adapters and integrations actually available.

This is a statement of intended product fit, not a claim that these capabilities are currently implemented.

### 8.2 Fit with explicit external prerequisites

GovCheck may still be useful where important properties depend on systems beyond the repository, provided the project can identify the responsible authority and obtain evidence proportionate to the claim. Examples include:

- forge-enforced reviews, branch protection and merge permissions;
- CI runner integrity, build provenance and artifact signing;
- agent sandboxing, secret management and cloud-provider isolation;
- identity assurance, access administration and separation of duties;
- data residency, retention, deletion, privacy and contractual obligations;
- organizational review capacity, competence, training and incident response;
- production telemetry, operational outcomes and long-term maintainability observations.

In such cases, GovCheck should distinguish a repository declaration from an external attestation or observation. It may validate evidence and bind it to a scope/revision when suitable integrations exist; it cannot manufacture the external guarantee.

### 8.3 Warning, limitation or poor fit when used alone

GovCheck must not be presented as a sufficient solution when the user's actual need is to:

- guarantee that an agent, runner, host, cloud provider or administrator cannot bypass controls;
- establish legal or regulatory compliance merely by generating governance files or recording a checklist;
- prove that software is correct because tests pass, a benchmark score is high, a model checker completed, or an assurance argument exists;
- replace a competent security team, independent reviewer, risk owner, service operator or legal adviser;
- provide complete production observability or causal attribution where the necessary telemetry and organizational process do not exist;
- enforce controls in an external forge or service for which no trusted adapter, permission or evidence path is available.

The correct response is not necessarily “GovCheck is unusable”. It is to state which part of the desired outcome it can support, which part remains an external responsibility, what evidence is missing, and whether the remaining gap is acceptable to the authorized owner.

### 8.4 No binary applicability score

Do not assign one universal “GovCheck-compatible” score. A project may be a strong fit for governance traceability while lacking the external prerequisites for runtime enforcement. Another may be able to validate local policy but lack independent acceptance authority. Applicability should be described per claim, capability, boundary and intended assurance outcome.

The guided bootstrap in Architecture 0024 is the natural place to elicit the context and explain recommendations, costs, assumptions and limitations. A concise user-facing “Is GovCheck right for this project?” section may later summarize the same rules, but must be derived from the accepted product scope and implemented capabilities—not imply that planned features already exist.

## 9. Disposition and next audit

The current research does not justify adopting the six proposed audit labels as a metamodel taxonomy, changing the canonical governance model, or mandating a software-factory architecture. Their only present purpose is to keep repository-local controls distinct from external evidence, observation, prerequisites, warnings and out-of-scope guarantees during the audit.

Next, compare these findings against Architecture 0024, Architecture 0029, Specifications 0002/0003/0005/0006 and the relevant issue portfolio. Record coverage as implemented, specified, proposed, partial, absent or outside GovCheck's authority. Only propose changes where a concrete contradiction or expressiveness gap is demonstrated.
