# Reference provenance audit

**Status:** working audit record for the initial 224-page discussion PDF and subsequent GovCheck source reviews. This is a documentary provenance audit, not a claim that every external URL has been reached or every publication has been independently re-evaluated.

## 1. Source artifacts and scope

The primary historical source is **“Évaluer l’intégration des dépôts.pdf”**, dated 6 November 2026, 224 pages. It is retained in the project Library rather than copied into the repository. It was created to carry a long ChatGPT design discussion into a new conversation; it is therefore a record of discussion, decisions, rejected proposals, hypotheses and cited external material—not an external standard or normative authority by itself.

The PDF covers adjacent integration work (including Cartocortex, MoriNet and SaussuNet) before the GovCheck-specific design and bootstrap discussion. GovCheck becomes explicit at approximately page 133. The earlier context remains relevant where it supplies repositories, formats, protocols and interoperability sources behind the initial assessment.

The audit also considers external critical reviews in GitHub issues #23 and #26 and the consolidated tracker in issue #30. These reviews are comparative inputs, not decisions adopted automatically by GovCheck.

## 2. Provenance and catalogue changes

- The catalogue had 105 active entries at the start of this audit.
- The current bilingual catalogue has **125 active entries**.
- Twenty new source entries were added (R-108–R-127), while duplicate R-102 was retired and consolidated into R-24. Previously retired R-12 and R-101 remain retired. No retired identifier is reused.
- Nine entries had contradictory “no current record cites” wording despite linking to Architecture 0027. The wording was removed from R-94–R-100, R-102 and R-103; R-102 was subsequently consolidated into R-24.
- R-24 now covers the W3C PROV family and retains both the PROV-O Recommendation and the family overview. R-102 is retired.
- The name **Privateer** was ambiguous. R-19 now identifies the privateer-agent/privateer-agent Pi coding-agent distribution. R-120 separately identifies the OpenSSF security/compliance evaluator. Architecture 0016 distinguishes and assesses both.
- The checker now detects a contradiction where an entry says no record cites it while also declaring backlinks. The integrity guide documents this check.

## 3. Source coverage map

| Discussion area | Catalogue coverage |
|---|---|
| Cartocortex, MoriNet, SaussuNet, reviewed PRs and adjacent GovCheck repositories | R-62, R-68, R-69 |
| Mind-map interchange, serializers, import/export fixtures and vendor documentation | R-63, R-69 |
| CRDTs, Yjs/Yrs, Automerge, Loro, WebRTC, ICE/STUN/TURN, WebTorrent, Hyperswarm/HyperDHT | R-45–R-50, R-66, R-87 |
| OKF, RDF, SKOS, OWL, SHACL, JSON-LD, PROV, Dublin Core, BIBO, DCAT, Web Annotation, ActivityStreams, SIOC, P-Plan and Schema.org | R-24, R-51–R-61, R-83–R-86 |
| Assurance cases, SACM 2.3 and 2.4 Beta 1, Assurance 2.0, PEAK and runtime assurance | R-33–R-34, R-70–R-76 |
| Model checking, proof assistants and alternative formal methods (TLA+, Lean, Alloy, B, Z, CSP/FDR, iStar, deontic logic) | R-05, R-20, R-37–R-43, R-89–R-93 |
| Threat/risk methods, access-control policy verification and structured compliance | R-27–R-36, R-78, R-88 |
| Policy engines, agent/MCP enforcement, sandboxing and agent instructions | R-09–R-10, R-77, R-79, R-104–R-106 |
| Software-supply-chain provenance, artifact identity, attestations, signing and source/build assurance | R-06–R-08, R-14–R-15, R-21, R-23–R-26, R-108, R-112–R-113, R-121–R-122 |
| Project security declarations, baselines, repository checks and assessment tools | R-08, R-109–R-120, R-127 |
| Decision/process/requirements/quality and engineering-domain candidates | R-74, R-94–R-100, R-103, R-114, R-123–R-126 |
| Agent-instruction formats, workflow tools and GitHub Actions placement | R-18–R-19, R-104, R-107 |

The catalogue also preserves the additional sources recovered from the critical reviews: gittuf, SLSA Source Track, Gemara, Gerrit submit requirements, Minder, Allstar, Conftest, CUE, OpenSSF Privateer, SLSA Verification Summary Attestation (VSA), Sigstore, Symboleo, Catala, Event Calculus, runtime verification and GitHub CODEOWNERS and CEL (R-112–R-128).

## 4. Semantic boundaries retained

- SACM 2.3 is the formal specification baseline recorded in R-34; SACM 2.4 Beta 1 is a draft candidate recorded separately in R-73. Neither is automatically adopted as GovCheck’s repository-wide governance metamodel.
- PEAK (R-74) is a decision-reasoning model for problem, experience, assumptions and knowledge; it is not SACM and does not replace the assurance-case model.
- Tests, runtime observations, model checking, program verification, theorem proof, conformance claims and acceptance decisions remain distinct evidence/assurance categories.
- A VSA or signed attestation delegates trust to a verifier; it does not prove that the verifier is trustworthy or that a claim is true.
- Security baselines and repository-assessment tools are candidates for selectable controls, not universal GovCheck tiers or mandatory dependencies.
- GitHub CODEOWNERS, Allstar and GitHub branch protection are platform-specific mechanisms; they do not define a forge-neutral authority model.
- A source mentioned in the discussion can be retained as historical context without becoming an adopted dependency, normative requirement or implementation claim.

## 5. Unresolved source identity and provenance

The following items cannot be assigned a reliable, unique source record without further information:

1. **Tarski** appears as a possible verification/kernel reference in the discussion, but the exact project, paper or tool is not uniquely identifiable from the preserved context. No guessed URL or dependency is recorded.
2. **Agent Package Manager** is mentioned in the prior discussion without a uniquely verified product identity or URL. It remains intentionally unlinked.
3. **EPIC** appears in later project context as a possible decision-modelling reference, but the exact framework/publication is not identified in the initial PDF or current catalogue. It should not be guessed.

These are provenance gaps, not blockers to the current catalogue corrections. They should be resolved only if the corresponding concepts remain relevant to GovCheck.

## 6. Verification status and remaining work

The repository changes are committed on the audit branch, but the following checks have **not** been executed in this environment:

- python3 scripts/check-reference-integrity.py
- python3 scripts/check-reference-integrity.py --external

No GitHub Actions workflow was triggered. The first command must be run locally to verify bilingual parity, identifier/index coverage, anchors, local Markdown links and bidirectional traceability. The external mode must then be run separately to probe URL reachability. Even a successful URL probe cannot establish source authority, semantic relevance, completeness or correctness.

The PDF source inventory is now substantially reconciled with the catalogue and the critical reviews, but a final page-by-page provenance pass over all pre-GovCheck context remains necessary before claiming exhaustive coverage of every source mentioned anywhere in the 224-page PDF.

## 7. Maintenance rule

For every source materially used by a GovCheck record:
1. maintain one canonical R-XX entry, with primary source identity and version/status;
2. describe the precise claim or comparison it supports and its limitations;
3. distinguish a historical mention, candidate, adopted method, implementation and verified result;
4. link the source from every relevant English and French document;
5. maintain the reverse **Cited by / Cité par** links in both catalogues;
6. do not reuse retired identifiers or guess missing source identities.