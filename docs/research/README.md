# GovCheck research register

**Purpose:** durable index of non-normative research records that may inform future decisions. This register is not an implementation backlog, not a set of accepted requirements and not a record of adopted decisions.

## How to use this register

Every research record receives a stable **STUDY-ID** independent of PR number, branch, file name or current product status. A study preserves:
- the user-supplied source(s) and source identity;
- the research questions and scope;
- source analyses and complementary academic/industry/standards research;
- applicability to GovCheck, including non-applicability and external prerequisites;
- limitations, counterarguments, uncertainty and unresolved research gaps;
- links to related studies, reference-catalogue entries, architecture/specifications/issues and later decisions.

**Research is not authorization.** A study may suggest a question, expose a gap or provide evidence; it does not create an implementation obligation. Only an explicitly authorized decision can adopt a recommendation. Do not turn every study into an issue. Create a decision record only when an actual arbitration is requested or made.

### Retrieval workflow

When the user asks to revisit a study:
1. Resolve the stable STUDY-ID or search by source title, speaker, URL, topic or reference ID.
2. Open the complete study record and its linked applicability assessment.
3. Reopen the primary source and relevant research references if the question depends on details not preserved in the summary.
4. Retrieve any decision records that cite the study and report whether each source was considered, accepted, rejected or left unresolved.
5. Keep later interpretations separate from the original source analysis; append a dated revision or decision link rather than silently rewriting the historical reasoning.

When a new study is added, update this register and both central reference catalogues. Link the study from each relevant R-entry, and link the R-entries from the study. Preserve source uncertainty explicitly.

## Study catalogue

| Stable ID | Research topic | Main record (FR) | Main record (EN) | Decision status |
|---|---|---|---|---|
| STUDY-001 | AI-assisted code quality, maintainability, agentic TDD and organizational adoption | [Revue de recherche](ai-assisted-quality-governance.fr.md) | [Research review](ai-assisted-quality-governance.md) | Research only; no recommendation adopted |
| STUDY-002 | Software factories, AI engineering governance and GovCheck applicability | [Applicabilité de GovCheck](govcheck-applicability-and-boundaries.fr.md) · [Analyse de la conférence](software-factory-self-improvement.fr.md) | [GovCheck applicability](govcheck-applicability-and-boundaries.md) · [Conference analysis](software-factory-self-improvement.md) | Research only; no factory architecture or audit taxonomy adopted |
| STUDY-003 | Constructivist epistemology, irreducible complexity and systemic modelling (three-session Le Moigne colloquium) | [Dossier du colloque](le-moigne-colloquium.fr.md) · [Applicabilité à GovCheck](govcheck-applicability-constructivism-and-systems.fr.md) | [Colloquium dossier](le-moigne-colloquium.md) · [GovCheck applicability](govcheck-applicability-constructivism-and-systems.md) | Research only; no constructivist/systemic ontology adopted |
| STUDY-004 | Multi-disciplinary specifications, plural viewpoints, semantic alignment and formal deliberation | [Dossier de recherche](multi-viewpoint-specification-governance.fr.md) | [Research dossier](multi-viewpoint-specification-governance.md) | Research only; no metamodel or implementation decision adopted |

## Cross-study themes

These are navigation aids, not adopted concepts or product taxonomy.

- **Knowledge, epistemology and model validity:** STUDY-003; compare with the metamodel/ontology research record and assurance specifications.
- **Intention, specification, verification and assurance:** STUDY-001 and STUDY-003.
- **AI-assisted engineering and organizational fit:** STUDY-001 and STUDY-002.
- **Repository boundaries and external preconditions:** STUDY-002.
- **Complexity, uncertainty, model scope and residual risk:** STUDY-003 and STUDY-002.
- **Plural specifications, semantic alignment and cross-domain deliberation:** STUDY-004; compare with existing ontology/interoperability and assurance-case studies.
- **Evidence, provenance and decision authority:** all studies.

## Decision traceability

Future decision records should link:
- the stable STUDY-ID;
- exact R-entry IDs used as evidence;
- exact claims or passages relied on (with page/section/timestamp where available);
- counterarguments and sources not accepted;
- context and applicability limits;
- the decision authority and date;
- adopted/rejected/deferred outcome and rationale;
- follow-up questions that remain research rather than implementation work.

Current related PRs are provenance only, not decisions:
- [PR #111 — AI-assisted quality and engineering governance research](https://github.com/Martin-PB/govcheck/pull/111) (STUDY-001).
- [PR #112 — software-factory analysis and GovCheck applicability](https://github.com/Martin-PB/govcheck/pull/112) (STUDY-002).
- [PR #113 — Le Moigne colloquium and durable research register](https://github.com/Martin-PB/govcheck/pull/113) (STUDY-003).

No decision should be inferred from the fact that a research PR was merged.
