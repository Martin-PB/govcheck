# Repository-enforceable governance and external preconditions for AI software factories

**Status:** non-normative research and classification proposal for maintainer review. This dossier proposes a way to classify concerns; it does not adopt a new normative rule, product, cloud architecture, or mandatory workflow.
**Prepared:** 2026-11-11.

## Source and scope

This review was prompted by Zach Lloyd's AI Engineer talk, [“How to Build a Software Factory That Improves Itself”](https://youtu.be/nKjPBAw_N_0), catalogued as [R-162](../references.md#r-162). It is read alongside the official [Warp Factories overview](https://docs.warp.dev/factories/) and [workflow documentation](https://docs.warp.dev/factories/how-factories-work) ([R-163](../references.md#r-163)), a randomized controlled trial of AI-assisted work by experienced open-source developers ([R-164](../references.md#r-164)), NIST's voluntary Generative AI Risk Management Profile ([R-165](../references.md#r-165)), existing NIST SSDF guidance ([R-02](../references.md#r-02)), the existing sandboxing reference ([R-79](../references.md#r-79)), and DORA 2025 ([R-148](../references.md#r-148)).

The talk advocates treating agentic development as an infrastructure/workflow system rather than a collection of individually prompted agents: define workflows as code, sandbox execution, preserve flexibility across models and harnesses, record runs, evaluate them against local tasks, measure cost/time/quality, and use failures to propose improvements. Warp's own documentation clarifies an important boundary: factory instructions may specify human checkpoints, but repository permissions and branch protection—not an agent's prompt—enforce who can approve or merge. These are useful industrial observations, not evidence that Warp or any cloud factory is necessary or sufficient for GovCheck.

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

## 8. Traceability

New references: [R-162](../references.md#r-162), [R-163](../references.md#r-163), [R-164](../references.md#r-164), [R-165](../references.md#r-165). Related existing references: [R-02](../references.md#r-02), [R-03](../references.md#r-03), [R-79](../references.md#r-79), [R-148](../references.md#r-148). This dossier is non-normative pending review by the authorized maintainer.
