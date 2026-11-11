# AI-assisted software quality, maintainability and engineering governance: research review

**Status:** non-normative research dossier for maintainer review. No architecture, requirement, metric, workflow or tool is adopted.
**Prepared:** 2026-11-11.

## Sources supplied for review

- [AI-Friendly Code: The Missing Link for Speed with Quality — Adam Tornhill, GOTO Copenhagen 2026](https://youtu.be/ciRTdOIhNCc) — [R-157](../references.md#r-157).
- [Video ID hP2vfBcQhfk](https://youtu.be/hP2vfBcQhfk) — metadata/content not independently resolved; retained as [R-160](../references.md#r-160).
- [How to Use Test-Driven Development with AI Agents — Emily Bache / Modern Software Engineering](https://youtu.be/a6HYpocKwXU) — [R-158](../references.md#r-158).
- [Video ID cZ_PqBpZygY](https://youtu.be/cZ_PqBpZygY) — metadata/content not independently resolved; retained as [R-161](../references.md#r-161).
- [What the Top Companies Do Differently With AI Coding — Martin Harrysson and Prakhar Dixit, McKinsey / AI Engineer](https://youtu.be/21tuT-e4NVo) — [R-159](../references.md#r-159).

**Related GovCheck work:** [#73](https://github.com/Martin-PB/govcheck/issues/73) formal contracts; [#74](https://github.com/Martin-PB/govcheck/issues/74) reference provenance; [#79](https://github.com/Martin-PB/govcheck/issues/79) evaluation and assurance; [#81](https://github.com/Martin-PB/govcheck/issues/81) formal lifecycle; [#83](https://github.com/Martin-PB/govcheck/issues/83) state of the art; [#84](https://github.com/Martin-PB/govcheck/issues/84) multi-agent collaboration and attribution; [#86](https://github.com/Martin-PB/govcheck/issues/86) revision-applicable evaluation.

## 1. Executive assessment

The shared governance question is how to increase AI-assisted change throughput without conflating generated code, correctness, maintainability, requirement satisfaction and justified acceptance.

The principal candidate for GovCheck is an auditable chain: **intent and stakeholder examples → requirements/specification → implementation change → verification evidence → assurance argument → authorized decision → post-release observation and reassessment**. This chain must preserve distinctions among tests, static analysis, model checking, theorem proof, human review and accepted residual risk.

**Provisional recommendation:** audit the existing metamodel, assurance model, lifecycle, revision applicability and attribution before proposing changes. Candidate areas include context-sensitive quality claims, explicit test/acceptance oracles and their independence, evidence freshness, longitudinal maintainability, and organizational accountability. This dossier does not establish that these capabilities are absent. No CodeHealth threshold, TDD workflow, EXACT method, subagent pattern, vendor product or organizational model is proposed as mandatory.

## 2. Method and limitations

This is a targeted source-led review, not a systematic literature review. Peer-reviewed studies support bounded claims about their methods and datasets; practitioner experiments provide useful hypotheses but require scrutiny of baselines, test oracles and repeatability; industry interviews describe practice but do not independently establish causality. Vendor metrics are signals, not universal definitions of quality.

The two unresolved links, R-160 and R-161, are retained without content claims. The dossier is not exhaustive with respect to those videos until their titles and contents are checked directly.

## 3. Academic evidence

### 3.1 Code health and AI refactoring

Borg, Hagatulah, Tornhill and Söderberg's FORGE 2026 paper studies AI refactoring on 5,000 Python competitive-programming solutions. It reports an association between CodeHealth and semantic preservation as measured through test-suite outcomes, with lower break rates for several medium-sized models on healthier code. Effects depend on model/task, and some comparisons are not statistically significant. See [R-152](../references.md#r-152).

This motivates investigating maintainability and comprehensibility as risk/context factors. It does not validate a metric as a universal acceptance threshold. The corpus, task, code-smell selection and test oracle are bounded; passing tests does not establish semantic equivalence beyond tested properties.

### 3.2 Balanced evidence on downstream maintainability

The preregistered two-phase study *Echoes of AI* involved 151 participants, 95% professional developers. Its randomized downstream task found no clear systematic difference in manual evolution time or code quality between AI-assisted and unaided code in the studied setting. See [R-153](../references.md#r-153). This does not prove there is no risk; it cautions against assuming that AI assistance necessarily degrades maintainability.

### 3.3 Context and provenance at scale

A preliminary ESEM 2026 study analyzes over 10,000 developers and 400,000 diffs at Meta. It traces AI-suggested code through editing, review and landing, and identifies contextual confounds including code centrality, change size, tests and author tenure. See [R-154](../references.md#r-154). This supports explicit context and provenance for metric-based claims, not copying organization-specific thresholds into other repositories.

### 3.4 Agent-generated pull requests and review

A study of 567 Claude Code-generated PRs across 157 open-source projects reports that 83.8% were eventually merged, while 45.1% of merged PRs required further changes. See [R-155](../references.md#r-155). GovCheck should distinguish producer, submitted revision, reviewer modifications, exact integrated revision and authorized acceptance. Merge rate is not a correctness measure; agent authorship confers no decision authority.

## 4. Practitioner evidence: examples, TDD and feedback

Emily Bache's account of the EXACT workflow describes collaborative example mapping, a natural-language test list, a red/green/refactor loop, predictive TDD and experiments with a dedicated refactoring subagent. Its test lab uses code katas and acceptance suites not shown to the model. The authors report benefits in their experiments, but outcomes and costs vary by model and workflow. See [R-156](../references.md#r-156) and [video R-158](../references.md#r-158).

Potentially useful separation of concerns:
1. Stakeholders clarify intent through examples.
2. Requirements and acceptance examples are made explicit.
3. An implementation agent works through a controlled feedback loop.
4. Predicted test outcomes are compared with actual outcomes.
5. An acceptance oracle hidden from the generator can improve evaluation if its independence and coverage are understood.
6. A refactoring agent proposes changes but cannot self-authorize acceptance.

These practitioner results do not prove that TDD, example mapping or multiple agents always improve quality. Hidden tests only check encoded properties; they do not replace requirements analysis, risk assessment, proof, model checking or authorized review. The industry talk [AI-Friendly Code](https://youtu.be/ciRTdOIhNCc) is recorded in [R-157](../references.md#r-157) and should be assessed alongside, not instead of, the empirical paper.

## 5. Organizational practice

The McKinsey interview “What the Top Companies Do Differently With AI Coding” is catalogued as [R-159](../references.md#r-159). It prompts review of engineering standards, training, task selection, feedback loops, review capacity, responsibility and outcome measurement. As an industry interview, its claims should be traced to underlying data and methods before being used normatively.

DORA 2025, already catalogued as [R-148](../references.md#r-148), provides a useful counterweight: AI tends to amplify existing strengths and weaknesses in the delivery system. Assessment may need to consider task, repository, team, workflow, integration pipeline and post-release outcomes, while naming the entity each claim concerns. Do not equate maturity with agent count, lines generated, PR throughput, merge rate or one quality score.

## 6. Candidate implications to audit in GovCheck

| Concern | Candidate capability to look for | Existing work to audit |
|---|---|---|
| Intent-to-evidence chain | Trace intent, objectives, requirements, examples, specifications, implementation, verification, argument and decision without collapsing their types | #73; Architecture 0013; Specification 0005 |
| Test oracle | Record oracle provenance, scope, coverage, independence from generator and blind spots | #79; Specification 0005 |
| Quality dimensions | Keep correctness, maintainability, security, reliability, complexity, performance and changeability distinct | #73; #79 |
| Context and provenance | Record task, repo/revision, dependencies, model/tool version, agent/human contributions and configuration | #74; #84; #86 |
| Evidence applicability | Bind evidence to exact revisions/dependencies; define when stale or partly applicable | #69; #79; #81; #86 |
| Longitudinal quality | Connect short-term checks to later defects, incidents, rework, maintenance and reassessment | #79; #81; #83 |
| Agent workflow | Treat producer attribution and collaboration as provenance, never authorization | #58; #59; #84 |
| Organizational claims | State population, context, baseline, measures, uncertainty and decision owner | #79; #83 |
| Acceptance authority | Separate green checks, agent self-assessment, merge mechanics, human review and authorized acceptance/risk decision | Architecture 0023; #73; #84 |

Map each candidate to exact existing definitions, rules, models and tests. Classify it as **covered, partially covered, absent, contradictory or not implemented**. A missing mention in one document is not itself proof of a metamodel gap.

## 7. Assurance distinctions to preserve

- **Test result:** observed behavior on a specified test set/environment; evidence within that scope, not proof of all behavior.
- **Static analysis:** a tool result under its model/configuration; scope and false-positive/false-negative behavior matter.
- **Model checking:** exploration of a declared transition system/configuration, bounded by the model and explored state space.
- **Theorem proof:** a derivation checked against definitions and a trusted kernel/verifier; it establishes only the formal statement proved.
- **Human review/attestation:** an attributable claim under a stated process, not automatically independent or infallible.
- **Assurance argument:** reasoning linking claims, evidence, assumptions and defeaters; quality depends on the adequacy of the argument.
- **Accepted risk/decision:** an authorized governance act, not technical evidence merely because it was approved.

Example mapping, TDD and hidden acceptance tests can improve specification clarity and evaluation without erasing these epistemic distinctions.

## 8. Adversarial scenarios for future verification

Not implemented or executed by this research PR; reconcile with existing verification work before adding fixtures.

- **AQ-01 — Green but wrong oracle:** visible tests pass but omit a requirement or encode wrong behavior.
- **AQ-02 — Generator/oracle coupling:** the same agent generates implementation and tests from one mistaken interpretation.
- **AQ-03 — Hidden-test overclaim:** an independent suite catches defects, then is incorrectly claimed to prove total correctness.
- **AQ-04 — Metric substitution:** a CodeHealth/complexity threshold is treated as proof of correctness or security.
- **AQ-05 — Context confounding:** outcomes are attributed to AI without accounting for task difficulty, code centrality, author experience, review selection or change size.
- **AQ-06 — Stale evidence:** prior test/proof/model-check/review results are reused after relevant dependency, assumption, policy or implementation changes.
- **AQ-07 — Self-refactoring acceptance:** an agent accepts its own output without required independent checks or authority.
- **AQ-08 — Reviewer-modified PR:** provenance and evidence still point to the original agent commit rather than the integrated revision.
- **AQ-09 — Short-term speed, long-term regression:** implementation time improves but maintenance, rework or operational outcomes are not measured.
- **AQ-10 — Organizational overclaim:** an industry case becomes a universal rule without population, baseline, uncertainty and applicability limits.

Expected behavior: preserve claim type, scope, provenance, uncertainty and decision authority. A positive test must not silently become a proof claim; valid approval must not be misrepresented as technical evidence.

## 9. Next steps proposed for review

1. Audit the intent/requirements/assurance chain, lifecycle, revision applicability and attribution before adding concepts.
2. Trace examples and test specifications to requirements and claims; check whether oracle and evidence producer are separately represented.
3. Check whether quality dimensions/context can be expressed without adopting one proprietary metric or organizational framework.
4. Check whether invalidation rules cover relevant revision, tool, dependency, assumption and environment changes.
5. Reuse #73, #74, #79, #81, #83, #84 and #86; do not create a duplicate epic.
6. Review R-160 and R-161 directly and update them if their metadata/content becomes available.
7. Only if the audit demonstrates a real gap, propose a small explicit change and adversarial fixtures. Keep this dossier non-normative until the authorized maintainer adopts any decision.

## 10. Recommendation

**The research supports an audit, not an immediate metamodel redesign.** The key question is whether GovCheck can express a complete, epistemically precise, revision-aware assurance chain from intent/examples through implementation and verification to authorized acceptance and later feedback.

Code-health metrics, TDD, example mapping, agentic refactoring, hidden acceptance suites and organizational practices are techniques whose claims should be evaluated in context. None should become mandatory because it appears in a video or one study. GovCheck should be able to represent such techniques when chosen by a repository and record their assumptions, evidence and limitations.

## 11. Traceability

New catalogue entries: [R-152](../references.md#r-152), [R-153](../references.md#r-153), [R-154](../references.md#r-154), [R-155](../references.md#r-155), [R-156](../references.md#r-156), [R-157](../references.md#r-157), [R-158](../references.md#r-158), [R-159](../references.md#r-159), [R-160](../references.md#r-160), [R-161](../references.md#r-161). Existing source: [R-148 — DORA 2025](../references.md#r-148). Related issues: #73, #74, #79, #81, #83, #84, #86.