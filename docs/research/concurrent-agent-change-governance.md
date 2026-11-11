# Concurrent agent changes and repository governance: research review

**Status:** non-normative research dossier for maintainer review. No architecture, policy, workflow, or tool is adopted here.
**Prepared:** 2026-11-11.
**Trigger:** Patrick Debois and Tessl, “Your Team's Agents Are All Shipping to the Same Code at Once”: https://youtu.be/fTUinMqA1XQ
**Related work:** [multi-agent collaboration and attribution #84](https://github.com/Martin-PB/govcheck/issues/84), [semantic contracts and metamodel #73](https://github.com/Martin-PB/govcheck/issues/73), [reference provenance #74](https://github.com/Martin-PB/govcheck/issues/74), [evaluation and assurance #79](https://github.com/Martin-PB/govcheck/issues/79), [formal lifecycle #81](https://github.com/Martin-PB/govcheck/issues/81).

## 1. Executive assessment

The video is a useful research trigger, not sufficient evidence by itself to change GovCheck. Its central problem—multiple agents making concurrent changes—intersects with established research on concurrent edits, merge conflicts, semantic interference, merge queues, provenance, and AI-assisted software delivery.

**Provisional conclusion:** GovCheck should be able to represent and assess concurrent work, interactions between changes, the scope and freshness of verification results, and the authority to integrate changes. Before changing the metamodel, audit whether the existing lifecycle, revision-applicability, assurance, provenance and VCS contracts already express these concerns. The report identifies candidate gaps, not confirmed implementation defects.

This is not exclusively an agent problem. The same issues occur with human teams, automated refactoring, release branches, dependency updates, generated code, and independent systems. The canonical model should not assume a particular agent harness, forge, VCS, merge queue, or CI provider.

## 2. Research method and limits

This is a targeted source-led survey, not a registered systematic literature review. It prioritizes peer-reviewed papers and official primary documentation, records each source's relevance and limits, and avoids treating product features or empirical associations as universal guarantees.

Search themes: concurrent edits and merge-conflict quality; semantic conflicts not exposed textually; detection and resolution; merge queues and combined-change validation; provenance and authority in AI-assisted development; organizational effects of AI assistance.

Coverage is not exhaustive. Some studies concern particular languages, repositories, organizations or datasets; their numbers must not be generalized without qualification. Vendor documentation describes intended product behavior, not independent proof of correct configuration or sufficiency.

## 3. Academic evidence

### 3.1 Concurrent edits are a governance signal, not just a textual conflict

- **ConE — Concurrent Edit Detection Tool** studies six large Microsoft repositories over six months and reports that files edited concurrently across pull requests are more likely to introduce bugs. It proposes proactive overlap detection. This supports recording overlapping work and triggering targeted review; it does not imply every overlap is a conflict or that detection proves correctness. [ACM/IEEE DOI 10.1145/3478019](https://doi.org/10.1145/3478019).
- **An empirical investigation into merge conflicts and software quality** analyzes 143 open-source projects, 556,911 commits and 36,122 merge commits; 19.32% of merges in its sample produced conflicts. It reports a higher bug association for code involved in semantic conflicts. These are dataset-specific observations, not a universal risk multiplier. [Paper PDF](https://ics.uci.edu/~iftekha/pdf/J4.pdf).
- **ConflictBench** creates a Java merge-conflict dataset and evaluates five tools, finding limitations in current tools and differences in applicability. Tool success must remain distinct from semantic correctness. [Journal of Systems and Software, 2024](https://www.sciencedirect.com/science/article/pii/S0164121224001298).
- **Lightweight Semantic Conflict Detection with Static Analysis** studies dynamic semantic conflicts that can remain after textual merge succeeds. Its evaluation reports F1 0.50 and accuracy 0.60 on 99 experimental units. These modest metrics mean a detector is fallible evidence, not an authoritative arbiter. [ICSE Companion 2024, DOI 10.1145/3639478.3643118](https://doi.org/10.1145/3639478.3643118).
- **Predicting merge conflicts considering social and technical assets** studies conflict prediction using social and technical factors, reinforcing that coordination and dependency context can matter beyond changed lines. [Empirical Software Engineering ([R-151](../references.md#r-151))](https://link.springer.com/article/10.1007/s10664-023-10395-8).

### 3.2 Automatic resolution is a proposal, not acceptance

Research on search-based and synthesis-based resolution shows that some patterns can be assisted automatically, but coverage is partial and results depend on conflict classes and evaluation datasets.
- Paulino, “Towards a Feasible Evaluation Function for Search-Based Merge Conflict Resolution” (2026), analyzes 9,998 conflict chunks from 1,062 open-source projects and evaluates an approach on a subset. Similarity to prior versions is a heuristic, not a semantic correctness criterion. [ACM TOSEM DOI 10.1145/3748256](https://doi.org/10.1145/3748256).
- Pan et al., “Can Program Synthesis be Used to Learn Merge Conflict Resolutions? An Empirical Analysis” (ICSE 2021), reports useful results for a bounded class of Microsoft Edge C++ conflicts. This does not justify trusting arbitrary agent-generated resolutions. [Microsoft Research](https://www.microsoft.com/en-us/research/publication/can-program-synthesis-be-used-to-learn-merge-conflict-resolutions-an-empirical-analysis/).

GovCheck implication: retain resolution provenance, inputs, tool/version, resulting revision, checks, assumptions and residual uncertainty. The resolution algorithm must not grant itself acceptance authority.

### 3.3 AI amplifies the surrounding engineering system

Google's DORA 2025 research draws on more than 100 hours of qualitative work and nearly 5,000 technology-professional survey responses. It characterizes AI as an amplifier of existing organizational strengths and weaknesses, cautioning against assuming that agent count or code-generation speed directly translates into reliable delivery. [DORA 2025 report](https://dora.dev/research/2025/dora-report/) · [Google Research](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/).

A 2025 literature review of LLM-based multi-agent systems for software engineering surveys collaboration architectures, benefits, limitations and research gaps. It maps the field; it does not prove any particular workflow reliable. [ACM TOSEM DOI 10.1145/3712003](https://doi.org/10.1145/3712003).

## 4. Industrial practice

### 4.1 Merge queues validate a particular combined revision

GitHub's merge queue creates temporary merge-group branches combining a pull request with the current base and earlier queued changes, then requires checks on that combined state. A check on an individual pull request and a check on a merge group are distinct executions over different revisions. The queue is GitHub-specific and must not become GovCheck's canonical abstraction. [GitHub: managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

Generalizable concept: an **integration candidate** identifies the exact base state, ordered change set, resolution and configuration against which integration checks ran. Assurance applies only to that candidate and its declared assumptions.

### 4.2 Concurrency controls are operational policy

A queue may bound concurrent builds, group changes, prioritize throughput or wait for checks. These are useful controls, but GovCheck should represent intended constraints and outcomes without requiring a queue or particular scheduling strategy. Low-volume repositories may integrate directly; high-volume repositories may use staged or speculative validation.

### 4.3 Provenance is complementary, not sufficient

GovCheck already catalogues in-toto and SLSA ([R-06](../references.md#r-06)/[R-07](../references.md#r-07)), and separately addresses artifact identity, revision and evidence freshness. These systems can identify how an artifact was produced; they do not by themselves prove that it satisfies repository intent or that an actor had authority to accept it.

## 5. Candidate implications for GovCheck

These are research-derived candidates for audit, not adopted requirements.

| Concern | Candidate representation or invariant | Existing concepts to audit first |
|---|---|---|
| Work coordination | Work item, scope, expected artifacts, dependencies, producer provenance and lifecycle state | Governed work portfolio; attribution #59; lifecycle model |
| Concurrent work | Overlap relation between work scopes or changed artifacts at a declared revision/time | VCS collaboration contracts; change lifecycle |
| Conflict taxonomy | Textual, structural, dependency/build, behavioral/semantic, requirement/decision and policy conflicts; detector limits | Existing conflict/contradiction relations; architecture 0013 |
| Integration candidate | Exact base revision, ordered changes, resolution, configuration and toolchain identity | Artifact identity/versioning; VCS adapter contract |
| Assurance applicability | Exact subject revision, inputs, assumptions, method, tool version, scope and status | Specification 0005; revision applicability; assurance freshness |
| Invalidation | Changes to dependency, assumption, policy, base, resolution or tool invalidate affected results by explicit rules | GovCheckAssurance.tla; GovCheckLifecycle.tla; architectures 0021/0033 |
| Acceptance authority | Integration authorization and risk acceptance distinct from authorship, merge mechanics, green CI and automatic resolution | Architecture 0023; authority/exception models |
| Feedback | Production observations may trigger an incident, claim, requirement change, reassessment or remediation decision | Monitoring references [R-70](../references.md#r-70), [R-72](../references.md#r-72), [R-75](../references.md#r-75) and [R-76](../references.md#r-76) |

### 5.1 Individually valid does not imply jointly valid

For changes c1 and c2, passing local checks does not establish that their composition satisfies a shared invariant. GovCheck must not infer:
- textually mergeable ⇒ semantically compatible;
- build succeeds ⇒ requirements satisfied;
- tests pass ⇒ theorem proven;
- individually conforming changes ⇒ a conforming combination;
- merge queue completes ⇒ normative acceptance was authorized;
- agent/tool produced a change ⇒ that producer has decision authority.

The video's financial-unit example is a useful adversarial fixture: one change alters the interpretation or representation of a monetary amount while another changes a consumer or report. Each may pass isolated tests while the combination violates a shared semantic requirement.

### 5.2 Evidence freshness must be revision-sensitive

An assurance record should identify its subject and relevant dependencies. If the base revision, dependency, policy, assumption, mapping, resolution or verification tool changes, GovCheck must determine which results remain applicable and which become stale. Test this against existing temporal models rather than creating a parallel freshness model without a demonstrated gap.

### 5.3 Layered detection must preserve uncertainty

A practical sequence can combine textual/VCS conflict detection; structural, dependency and build checks; tests and static analysis; contract/invariant and model checks; formal proof where a suitable specification exists; and human review with explicit acceptance of residual ambiguity/risk.

This is not a universal maturity ladder and does not imply every repository must use every method. The required method follows the claim, risk and declared assurance policy. Detector results must preserve false-positive/false-negative limitations.

## 6. Proposed adversarial scenarios

These could later become fixtures under existing verification work. They are not implemented or run yet.

- **CC-01 — Semantic unit mismatch:** two independently passing changes use different monetary units or scales; their combination violates an invariant.
- **CC-02 — Stale verification:** change A is tested against base B; change C modifies a relevant dependency or policy; A's old result is reused incorrectly.
- **CC-03 — Shared-interface drift:** producer and consumer contracts are changed independently, with no textual conflict but incompatible meanings.
- **CC-04 — Competing policy decisions:** parallel work changes the same governance rule incompatibly; mergeability cannot decide normative authority.
- **CC-05 — Automatic-resolution provenance:** an automated resolver edits conflict chunks, but the resulting revision lacks resolver identity, inputs or post-resolution evidence.
- **CC-06 — Overlap false positive:** changes touch the same file but independent regions; the system blocks solely due to file overlap.
- **CC-07 — Detector miss:** no textual conflict or overlap warning appears, but the composed change violates behavior.
- **CC-08 — Unauthorized green merge:** all checks pass, but required approval or delegated authority is absent/revoked.
- **CC-09 — Non-Git workflow:** changes are coordinated through Pijul or a patch/email forge; semantics must not depend on GitHub PR identifiers.
- **CC-10 — Production feedback:** an operational observation invalidates an assumption/claim and triggers impact analysis and reassessment.

Expected behavior: distinguish pass/fail/inconclusive/unsupported/stale, preserve provenance and scope, and never convert detection into authority or evidence into proof.

## 7. Candidate invariants for formalization

These require precise definitions before model checking or proof.

- **INV-CC-01 Scope:** every integration candidate identifies base state, constituent changes, resolution and relevant configuration.
- **INV-CC-02 No stale assurance:** acceptance cannot rely on a result known to be stale under declared dependency/invalidation rules.
- **INV-CC-03 Composition:** acceptance requires applicable assurance for the combined candidate, not merely its components.
- **INV-CC-04 Authority:** merge mechanics or automatic resolution cannot substitute for required, currently valid authorization.
- **INV-CC-05 Epistemic non-promotion:** textual merge, build or test success cannot silently become a proof claim.
- **INV-CC-06 Provenance:** automatic resolutions and checks identify relevant inputs, producer/tool and exact output revision.
- **INV-CC-07 Portability:** canonical semantics do not depend on GitHub-only identifiers or queue behavior.
- **INV-CC-08 No universal lock:** overlap is a signal to analyze, not proof of incompatibility or a universal reason to block work.

TLA+/TLC may suit lifecycle, concurrency, revocation and freshness properties over explicit state spaces. Lean or another proof assistant may suit static semantic-preservation claims with precise definitions. Tests and static analysis provide scoped evidence. No method proves every invariant; model-checking results are bounded by the modeled system and explored configuration.

## 8. Recommended next steps, subject to review

1. Audit Architectures 0013, 0014, 0021, 0022, 0023, 0028, 0032 and 0033; Specifications 0002, 0003, 0005 and 0006; and existing formal lifecycle/assurance models.
2. Map each candidate invariant to existing concepts, rules, models and tests; classify as covered, partial, absent, contradictory or not implemented, with exact locations.
3. Reuse issue #84 and child issues #58/#59 for collaboration and attribution; connect semantic contracts to #73, freshness to #69/#79/#81, and reference provenance to #74/#83. Do not create a duplicate epic.
4. Only if the audit demonstrates a gap, propose a small explicit change to the canonical model or a VCS-neutral collaboration contract. Keep queues, locks, agent protocols and CI providers as adapters/policies.
5. Add confirmed sources to the central bilingual catalogue with stable IDs and accurate reverse links. Validate links and backlinks on the eventual PR head.
6. Keep this report non-normative. Adoption of requirements, architecture or tools remains a separate decision for the authorized maintainer.

## 9. Recommendation

Treat concurrent agent work as a first-class use case for testing the adequacy of GovCheck's generic governance model, not as GovCheck's exclusive purpose. The strongest candidate improvement is composition- and revision-aware assurance: which exact combined change was checked, against which assumptions and dependencies, and whether the current authority accepted it.

This report recommends no mandatory lock, merge queue, agent framework, forge, CI service, ontology or proof tool.

## 10. References and traceability

Proposed catalogue entries are the catalogue entries [R-142](../references.md#r-142), [R-143](../references.md#r-143), [R-144](../references.md#r-144), [R-145](../references.md#r-145), [R-146](../references.md#r-146), [R-147](../references.md#r-147), [R-148](../references.md#r-148), [R-149](../references.md#r-149), [R-150](../references.md#r-150) and [R-151](../references.md#r-151) in the central catalogue. Related records: [Architecture 0013](../architecture/0013-governance-metamodel.md), [Architecture 0021](../architecture/0021-assurance-claims-and-freshness.md), [Architecture 0022](../architecture/0022-governance-capability-audit.md), [Architecture 0023](../architecture/0023-bootstrap-governance-authority.md), [Architecture 0028](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.md), [Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.md), [Specification 0005](../specifications/0005-assurance-model.md), and work items [#84](https://github.com/Martin-PB/govcheck/issues/84), [#73](https://github.com/Martin-PB/govcheck/issues/73), [#74](https://github.com/Martin-PB/govcheck/issues/74), [#79](https://github.com/Martin-PB/govcheck/issues/79), [#81](https://github.com/Martin-PB/govcheck/issues/81).
