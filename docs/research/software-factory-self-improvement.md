# How to Build a Software Factory That Improves Itself — conference analysis

**Status:** non-normative source analysis. This document analyses the supplied conference and supporting sources; it does not adopt a product, architecture, workflow, metamodel concept or requirement.
**Prepared:** 2026-11-11.

## Source and method

Zach Lloyd (Warp), [“How to Build a Software Factory That Improves Itself”](https://youtu.be/nKjPBAw_N_0), presented at AI Engineer; catalogued as [R-162](../references.md#r-162).

The analysis uses the presentation and its timestamped transcript, then checks its claims against the official [Warp Factories documentation](https://docs.warp.dev/factories/) ([R-163]), the METR randomized study of experienced open-source developers ([R-164]), and NIST's Generative AI Risk Management Profile ([R-165]). Existing references to SSDF, GitHub branch protection, agent sandboxing and DORA are cited where they provide relevant context ([R-02](../references.md#r-02), [R-03](../references.md#r-03), [R-79](../references.md#r-79), [R-148](../references.md#r-148)).

This is a targeted critical analysis, not an independent evaluation of Warp or a systematic literature review. The speaker is the founder of a vendor demonstrating its own product. Product documentation is evidence of the vendor's design and claims, not independent proof of operational properties.

## 1. Detailed analysis of the talk

### 1.1 The argument, reconstructed from the presentation

The talk is not merely a product demonstration for remote agents. It advances a coherent operating-model proposal:

1. **Move from interactive prompting to automated development (01:12–03:08).** In the current pattern described by Lloyd, engineers individually run agents on their laptops. This makes the engineer a throughput bottleneck, fragments configuration, makes spend difficult to control, and gives a compromised agent access comparable to the signed-in user's local privileges.
2. **Treat the factory as a company-level workflow loop (03:08–04:03).** Humans submit work; agents may perform triage, collaborate on specifications, implement changes and carry out computer-use verification. The organization defines how human and agent responsibilities fit together, then measures and improves that operating model.
3. **Treat it as infrastructure, not as a single AI teammate (04:03–05:15).** The factory should be open to different models and harnesses, adaptable to existing infrastructure, and precisely defined in version-controlled code. Its definition includes workflows, skills, MCPs, execution locations and related configuration.
4. **Preserve control over data, compute and inference (05:15–06:55).** Lloyd presents AI sovereignty as an enterprise concern: own or control inputs and outputs, consider own infrastructure and compute, and preserve the option to choose inference providers. He also distinguishes product engineers, who deliver customer value through the factory, from factory engineers, who improve skills, context, model selection and the factory itself.
5. **Make runs observable (07:51–11:57).** The demonstration shows views of automation, cycle time and spending, and access to individual runs and their artifacts. The factory definition is backed by a repository containing agent definitions, automations, benchmarks, execution locations, skills and webhooks. The intended effect is that the operating process becomes inspectable and changeable as code.
6. **Score runs and feed failures back into the system (12:01–14:42).** LLM-based evaluators inspect runs against criteria, including a demonstration criterion for redundant tests. Aggregated failure patterns can lead to proposed changes to factory configuration or skills, delivered as a pull request. The example mentions a failure pattern observed 37 times and a proposed change to make agents read more positive skills before implementation.
7. **Benchmark on the organization's own tasks (14:42–17:15).** Rather than relying only on public benchmarks, teams should curate representative historical tasks and replay them across model/configuration choices. Cost and quality results can inform model routing for the team's own codebase and stack.
8. **Keep a verification and economics discipline (17:15–end).** In the Q&A, Lloyd recommends spec-driven development and computer-use verification to cope with PR volume and review burden. For budgeting, he suggests measuring cost per PR and the share spent on scoring and benchmarking, then extrapolating. He suggests this becomes particularly valuable for teams of roughly ten or more engineers; this is a practical heuristic, not a universal threshold.

### 1.2 What is genuinely useful in the proposal

- **The factory is a governed system in its own right.** Prompts, agent roles, tool grants, skills, workflows, evaluators, benchmark tasks and deployment locations are not incidental setup; they influence the properties of the produced software and deserve identity, revision history, review and evidence.
- **The operational loop is explicit.** Run → trace/artifacts → evaluation → failure analysis → proposed workflow change → review/test → new run. This is a useful lifecycle to model, including the possibility that the loop itself is defective.
- **Local task evidence matters.** Public benchmark rankings do not establish expected performance on a particular repository, language, architecture, risk profile or review process. A curated, versioned local task set can answer a narrower and more useful question, provided its limits are visible.
- **Cost must be tied to outcomes.** Cost per PR is more informative than token spend alone, but only if its denominator and scope are defined: accepted/rejected PRs, retries, human specification and review time, failed runs, rework, verification, incidents and maintenance may all change the interpretation.
- **Human and agent responsibilities should be designed, not improvised.** The distinction between product engineering and factory engineering makes the maintenance of the production system visible as work with owners, competence requirements and assurance obligations.
- **Sovereignty is a set of concrete choices.** Data control, compute location, inference provider, retention, subprocessors and exit options can be specified and assessed separately instead of collapsed into a vague “self-hosted” label.

### 1.3 Assumptions and limitations that the talk does not establish

The presentation is an industry proposal by the founder of a vendor demonstrating that vendor's product. It is useful primary evidence for the design philosophy and a concrete implementation example, but it is not an independent evaluation of the product or the general approach.

In particular, the talk does not establish:

- that moving execution to a cloud factory necessarily makes it safer than a carefully isolated local or self-hosted worker;
- that a provider's sandbox, secrets handling, tenant isolation, logging or deletion guarantees are effective merely because the factory configuration declares them;
- that complete run recording is compatible with privacy, least privilege, data minimization, legal retention obligations or protection of credentials and customer data;
- that an LLM judge can reliably distinguish good from bad engineering, or that evaluator errors are independent of generator errors;
- that the chosen score captures the property that matters. The example of redundant tests is a heuristic; removing tests can improve that score while reducing assurance;
- that a historical benchmark is representative, uncontaminated, resistant to overfitting or stable as the repository and task distribution evolve;
- that replaying recorded model/tool interactions measures the behavior of a live, changing provider in all relevant respects;
- that a proposed factory change actually causes improvement in production, rather than merely improving the benchmark or evaluator score;
- that cycle time, automation rate, cost per PR and correctness can be optimized independently without shifting work or risk to reviewers, operators or users.

A self-improvement loop is therefore not automatically a quality-improvement loop. It can amplify a defective metric, evaluator bias, benchmark leakage or a mistaken diagnosis. Each transition in the loop needs provenance and an appropriate independent check.

### 1.4 Implications for GovCheck — adopt the questions, not the product architecture

The talk should prompt GovCheck to govern the **production system as an object of assurance**, but it does not imply that GovCheck should become a cloud factory or operate agents itself.

This distinction is especially important because GovCheck is intended to be a forge-agnostic, repository-oriented bootstrap with a small local executable. A repository can describe and validate its own governance contract and the artifacts that a factory must provide. It cannot, without an integration and trusted authority, guarantee the runtime behavior of an external factory. Nor should a Warp-specific schema, MCP arrangement, cloud execution model or vendor-specific score become a generic GovCheck requirement.

The useful questions to carry into the repository audit are:

- **Factory identity:** can a run be tied to an immutable revision of workflow definitions, agent roles, skills, tool permissions, evaluator definitions and benchmark suite?
- **Execution identity:** can evidence identify the actual harness, model/provider/version, runner image, isolation profile, tool grants, relevant configuration and execution location? Which of these are asserted by the runner and which independently attested?
- **Lifecycle traceability:** can the run link the originating intention/request, triage, specification, implementation revision, tests, review, verification and release decision without confusing agent activity with authorization?
- **Evaluation validity:** are scoring criteria explicit, versioned and linked to claims or requirements? Are judges calibrated, sampled, challenged by independent evidence and prevented from silently becoming the sole oracle?
- **Benchmark governance:** who selects tasks, expected results and difficulty; how are sensitive tasks protected; how are additions/removals and benchmark versions reviewed; how are leakage, representativeness and overfitting assessed?
- **Improvement governance:** does a self-improvement proposal enter the same change-control, review, test and assurance path as any other governance-sensitive change? Can the system change its own evaluator or benchmark without independent authorization?
- **Economic and quality claims:** are denominators, exclusions, uncertainty, cost attribution, review effort, rework and downstream outcomes recorded so that a dashboard cannot turn partial telemetry into an unjustified productivity claim?
- **Human authority:** are the people who specify, review, approve, accept risk and operate the factory distinguishable in the evidence? Does a recorded human checkpoint correspond to a permission-enforced control?
- **Exit and portability:** can the organization export its definitions, run evidence and benchmark data, replace a model/harness/provider, and continue to interpret old evidence after a migration?

These are candidate audit questions, not a new mandatory factory schema. They should first be mapped to the existing GovCheck concepts and open issues.

### 1.5 A crucial distinction: governing a factory versus enforcing its guarantees

A repository can enforce that a factory definition is versioned, schema-valid, reviewed and associated with a run. It may verify a signed attestation or query a forge/provider API. It can reject a release claim when required evidence is missing or stale, if an adopted policy says so.

It cannot infer from the presence of a YAML file that the remote service executed it faithfully. It cannot make a human reviewer competent, ensure a provider's isolation is effective, or prove that a benchmark is representative merely by checking that benchmark files exist. Those are external evidence, organizational preconditions or residual risks.

The factory itself may also be a separate governed repository. In that case, GovCheck can bootstrap and govern that repository using the same general model; it should not silently assume that the product repository has authority over the factory's infrastructure repository, cloud account or organization.

### 1.6 Suggested evidence chain for a factory improvement

A candidate traceability chain, to be compared with the existing metamodel rather than immediately added as a new schema, is:

`FactoryRevision → Run → TraceAndArtifacts → EvaluationResult → FailureFinding → ImprovementProposal → ReviewedChange → VerifiedFactoryRevision`

Each link needs stable identity and provenance. The evaluation result must state its criterion and evaluator; the improvement proposal must state which findings support it; the reviewed change must identify the human/authority decision; and the subsequent verification must use an identified task set and environment. A passing benchmark is evidence about the tested cases, not proof of general improvement.

### 1.7 Overall assessment

The strongest contribution of the talk is its shift in unit of analysis: from the individual coding agent to the governed system that configures, executes, observes, evaluates and improves agent work. GovCheck should take that shift seriously when auditing repository lifecycle and assurance completeness.

The weakest part is the implied confidence that centralized cloud execution, LLM scoring and self-improvement will produce safer or more productive development. Those are hypotheses to test, not guarantees. GovCheck's contribution should be to make the claims, evidence, authority, boundaries and residual risks explicit—without mandating a cloud factory, a vendor, a model, a harness or an organizational structure.

## Research disposition

This conference is one input to the broader research programme on AI-assisted software engineering and GovCheck applicability. Its observations must be compared with the other supplied talks, academic studies and standards before any cross-cutting product recommendation is made. The applicability assessment is maintained separately in [GovCheck applicability and external boundaries](govcheck-applicability-and-boundaries.md).

## Traceability

New references: [R-162](../references.md#r-162), [R-163](../references.md#r-163), [R-164](../references.md#r-164), [R-165](../references.md#r-165). Supporting references: [R-02](../references.md#r-02), [R-03](../references.md#r-03), [R-79](../references.md#r-79), [R-148](../references.md#r-148). No source in this document is adopted as a GovCheck requirement.
