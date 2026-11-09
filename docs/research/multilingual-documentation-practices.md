# Multilingual documentation practices and synchronization models

**Status:** comparative research derived from issue #33 and the source catalogue. This document records options and constraints; it does not decide which language is normatively authoritative.

## 1. Why this is a governance question

For GovCheck, a translation can be linguistically correct yet stale relative to its source. Conversely, a synchronized translation can still be semantically wrong. These are separate properties and must not be collapsed into a single “translated” or “valid” flag.

The problem is more consequential for documents consumed by agents or tools. If two operational instruction files express different obligations, an agent may follow the wrong rule. A repository therefore needs an explicit distinction between normative authority and informative localized views.

## 2. Comparative source patterns

| Source / practice | Synchronization unit | Useful mechanism | Limitation for GovCheck |
|---|---|---|---|
| MDN translated-content ([R-136](../references.md#r-136)) | File | Source-commit marker such as l10n.sourceCommit; freshness relative to source revision | Commit identity is Git-specific; adoption is incomplete; source alignment does not establish translation quality. |
| Kubernetes localization ([R-137](../references.md#r-137)) | File/language | Source-first correction, human triage, per-language status and explainable automation | Some practices are prototypes; does not settle language primacy or normative authenticity. |
| Vue translation guidelines ([R-138](../references.md#r-138)) | Repository / translation PR | Upstream synchronization, glossary and reviewable diffs | Community-specific workflow, not a general governance model. |
| React translation workflow ([R-139](../references.md#r-139)) | Separate translation repository/fork | Explicit upstream delta and synchronization PRs | Fork maintenance and source alignment require independent validation. |
| Comprehensive Rust / mdbook-i18n-helpers ([R-140](../references.md#r-140)) | Segment | PO files, msgmerge, fuzzy and obsolete markers | Extraction/generation constraints; segment identity may not match GovCheck's stable document/record identifiers. |
| po4a ([R-141](../references.md#r-141)) | Paragraph/segment | Fuzzy state for changed source segments; generated translations; configurable completeness threshold | Structured Markdown, anchors, code blocks and normative identifiers need careful handling. |
| Docusaurus i18n ([R-142](../references.md#r-142)) | File/locale | Locale-specific directories and source-language fallback | No native semantic freshness tracking; external tooling or project-specific checks are needed. |
| Microsoft translation-as-artifact proposal ([R-143](../references.md#r-143)) | Versioned artifact | Separate synchronization state from linguistic quality; report status and leave quality judgments to humans | Article/design guidance, not proof of a complete deployed implementation. |
| BCP 47 ([R-144](../references.md#r-144)) | Language identifier | Standardized language/script/region tags | Identifies language only; it does not define source primacy, translation quality or freshness. |

## 3. GovCheck-specific constraints

- **VCS neutrality:** Git commit hashes are not portable to Pijul. A translation source marker may need a content digest or a stable source-record identity, with the VCS revision retained as additional provenance.
- **Canonical governance model:** the structured governance authority is intended to be normative; Markdown documents are readable projections checked against it. A translated Markdown view must not silently become a second authority.
- **Operational versus documentary artifacts:** agent instructions, conventional platform files and CI configuration can affect tool behavior; explanatory documents, ADRs and catalogues primarily inform humans. They may need different primacy and fallback rules.
- **Language default:** English is the repository's current default and French documentation exists in parallel. This does not, by itself, decide whether English is the only authentic normative version or whether EN/FR are co-authoritative.
- **Language-neutral outputs:** executable results, identifiers, status codes and attestations should remain language-neutral; human-readable messages can be localized.
- **No hosted dependency:** translation platforms may be optional adapters, never a required hosted service or the governance core.

## 4. Decisions that remain open

| Decision | Viable options | Consequence to specify |
|---|---|---|
| Normative primacy | English authoritative with French informative; EN/FR co-authoritative with enforced parity; per-document authority | Which text controls when translations diverge, especially for agent instructions and normative specifications |
| Operational filenames | One canonical operational instruction file; separate informative translations under non-conventional names | Avoid two files that agents or platforms may load as competing instructions |
| Translation scope | Only user-facing documentation; also ADRs/specifications/catalogue; operational instructions; CLI/refusal messages | Which artifacts require translation metadata and blocking checks |
| Synchronization unit | Whole file; stable section/record; paragraph/segment | How source changes invalidate translations and how to preserve identity across Git/Pijul |
| Source marker | Git commit; blob/content digest; stable source-record ID plus digest | Reproducible freshness comparison across squash, rename and VCS migration |
| Staleness semantics | Any source edit; normative-only changes; classified source changes (normative/informative/editorial) | Avoid marking a translation stale for harmless editorial changes while missing normative changes |
| Stale/missing behavior | Warning; explicit fallback to authoritative language; block normative changes until translation is updated | Fail-open/fail-closed policy by artifact class |
| Translation review | Human-reviewed; machine-assisted with explicit reviewer; unreviewed draft | Who can attest that a translation has been reviewed and what that attestation means |
| Terminology | Machine-readable glossary and prohibited alternatives; normative keyword mapping | Stable translations of MUST/SHOULD/MAY and domain-specific vocabulary |
| Additional languages | BCP 47 tags and per-language status | Add a third language without redesigning the model |

## 5. Candidate model (not adopted)

A useful design to evaluate is to model each localized artifact as a derived record with:

1. a stable identity for the source artifact or source section;
2. a language tag (BCP 47);
3. a source content digest and optional VCS revision;
4. translation revision/content digest;
5. status such as unknown, synchronized, stale, missing or review-required;
6. method (human, machine-assisted, machine draft), reviewer and review timestamp;
7. change classification (normative, informative, editorial);
8. a link to the authoritative version and an explicit statement of normative/informative status.

This model allows deterministic checks of structure, identifiers, anchors, links, code blocks, numbers and source digests. It does not pretend that semantic equivalence or linguistic quality is decidable; those remain human-attested or unknown.

## 6. Open naming issue

The existing project discussion uses both AGENTS.md and the preferred agent.md naming convention. The canonical operational filename must be confirmed before a translation rule is adopted. Do not create parallel operational files under names that agents may automatically load.

## 7. Sources

- [MDN translated-content](../references.md#r-136)
- [Kubernetes localization](../references.md#r-137)
- [Vue](../references.md#r-138) and [React](../references.md#r-139)
- [Comprehensive Rust](../references.md#r-140), [po4a](../references.md#r-141) and [Docusaurus](../references.md#r-142)
- [Microsoft translation-as-artifact guidance](../references.md#r-143)
- [BCP 47](../references.md#r-144)