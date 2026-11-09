# Reference provenance audit

**Status:** working audit record for the initial 224-page discussion PDF and subsequent GovCheck source reviews. This is a documentary provenance audit, not a claim that every external URL has been reached or every publication has been independently re-evaluated.

## 1. Source artifacts and scope

The primary historical source is **“Évaluer l’intégration des dépôts.pdf”**, dated 6 November 2026, 224 pages. It is retained in the project Library rather than copied into the repository. It was created to carry a long ChatGPT design discussion into a new conversation; it is therefore a record of discussion, decisions, rejected proposals, hypotheses and cited external material—not an external standard or normative authority by itself.

The PDF covers several project streams before and alongside the GovCheck-specific design: Cartocortex, MoriNet and SaussuNet; a NixOS SecOps agent stack; and then the GovCheck governance/bootstrap discussion. GovCheck becomes explicit at approximately page 133. The earlier project contexts remain relevant where they supply repositories, formats, protocols and interoperability sources behind the initial assessment.

The audit also considers external critical reviews in GitHub issues #23 and #26 the consolidated tracker in issue #30, and the multilingual governance review in issue #33. These reviews are comparative inputs, not decisions adopted automatically by GovCheck.

## 2. Provenance and catalogue changes

- The catalogue had 105 active entries at the start of this audit.
- The current bilingual catalogue has **143 active entries**.
- Thirty-nine new source entries were added ([R-108](references.md#r-108)–[R-146](references.md#r-146)), while duplicate identifier 102 was retired and consolidated into [R-24](references.md#r-24). Identifiers 12 and 101 were already retired. No retired identifier is reused.
- Nine entries had contradictory “no current record cites” wording despite linking to Architecture 0027. The wording was removed from [R-94](references.md#r-94)–[R-100](references.md#r-100), retired identifier 102 and [R-103](references.md#r-103); retired identifier 102 was subsequently consolidated into [R-24](references.md#r-24).
- [R-24](references.md#r-24) now covers the W3C PROV family and retains both the PROV-O Recommendation and the family overview. retired identifier 102 is retired.
- The name **Privateer** was ambiguous. [R-19](references.md#r-19) now identifies the privateer-agent/privateer-agent Pi coding-agent distribution. [R-120](references.md#r-120) separately identifies the OpenSSF security/compliance evaluator. Architecture 0016 distinguishes and assesses both.
- The checker now detects a contradiction where an entry says no record cites it while also declaring backlinks. The integrity guide documents this check.

## 3. Source coverage map

| Discussion area | Catalogue coverage |
|---|---|
| Cartocortex, MoriNet, SaussuNet, reviewed PRs and adjacent GovCheck repositories | [R-62](references.md#r-62), [R-68](references.md#r-68), [R-69](references.md#r-69) |
| Git/Pijul/Darcs semantics and patch theory | [R-68](references.md#r-68), [R-133](references.md#r-133) |
| Forge-specific approval controls and merge-gating systems | [R-127](references.md#r-127), [R-131](references.md#r-131)–[R-132](references.md#r-132) |
| Mind-map interchange, serializers, import/export fixtures and vendor documentation | [R-63](references.md#r-63), [R-69](references.md#r-69) |
| CRDTs, Yjs/Yrs, Automerge, Loro, WebRTC, ICE/STUN/TURN, WebTorrent, Hyperswarm/HyperDHT | [R-45](references.md#r-45)–[R-50](references.md#r-50), [R-66](references.md#r-66), [R-87](references.md#r-87) |
| OKF, RDF, SKOS, OWL, SHACL, JSON-LD, PROV, Dublin Core, BIBO, DCAT, Web Annotation, ActivityStreams, SIOC, P-Plan and Schema.org | [R-24](references.md#r-24), [R-51](references.md#r-51)–[R-61](references.md#r-61), [R-83](references.md#r-83)–[R-86](references.md#r-86) |
| Assurance cases, SACM 2.3 and 2.4 Beta 1, Assurance 2.0, PEAK and runtime assurance | [R-33](references.md#r-33)–[R-34](references.md#r-34), [R-70](references.md#r-70)–[R-76](references.md#r-76), [R-129](references.md#r-129), [R-134](references.md#r-134) |
| Model checking, proof assistants and alternative formal methods (TLA+, Lean, Alloy, B, Z, CSP/FDR, iStar, deontic logic) | [R-05](references.md#r-05), [R-20](references.md#r-20), [R-37](references.md#r-37)–[R-43](references.md#r-43), [R-89](references.md#r-89)–[R-93](references.md#r-93) |
| Threat/risk methods, access-control policy verification and structured compliance | [R-27](references.md#r-27)–[R-36](references.md#r-36), [R-78](references.md#r-78), [R-88](references.md#r-88) |
| Policy engines, agent/MCP enforcement, sandboxing and agent instructions | [R-09](references.md#r-09)–[R-10](references.md#r-10), [R-77](references.md#r-77), [R-79](references.md#r-79), [R-104](references.md#r-104)–[R-106](references.md#r-106), [R-128](references.md#r-128), [R-130](references.md#r-130) |
| Software-supply-chain provenance, artifact identity, attestations, signing and source/build assurance | [R-06](references.md#r-06)–[R-08](references.md#r-08), [R-14](references.md#r-14)–[R-15](references.md#r-15), [R-21](references.md#r-21), [R-23](references.md#r-23)–[R-26](references.md#r-26), [R-108](references.md#r-108), [R-112](references.md#r-112)–[R-113](references.md#r-113), [R-121](references.md#r-121)–[R-122](references.md#r-122) |
| Project security declarations, baselines, repository checks and assessment tools | [R-08](references.md#r-08), [R-109](references.md#r-109)–[R-120](references.md#r-120), [R-127](references.md#r-127) |
| Decision/process/requirements/quality and engineering-domain candidates | [R-74](references.md#r-74), [R-94](references.md#r-94)–[R-100](references.md#r-100), [R-103](references.md#r-103), [R-114](references.md#r-114), [R-123](references.md#r-123)–[R-126](references.md#r-126), [R-128](references.md#r-128) |
| Multilingual documentation synchronization and language identifiers | [R-136](references.md#r-136)–[R-144](references.md#r-144) |
| Translation platforms mentioned but not evaluated | [R-145](references.md#r-145)–[R-146](references.md#r-146) |
| Agent-instruction formats, workflow tools and GitHub Actions placement | [R-18](references.md#r-18)–[R-19](references.md#r-19), [R-104](references.md#r-104), [R-107](references.md#r-107) |

The catalogue also preserves the additional sources recovered from the critical reviews: gittuf, SLSA Source Track, Gemara, Gerrit submit requirements, Minder, Allstar, Conftest, CUE, OpenSSF Privateer, SLSA Verification Summary Attestation (VSA), Sigstore, Symboleo, Catala, Event Calculus, runtime verification and GitHub CODEOWNERS, CEL, eliminative argumentation, Kyverno, GitLab approval rules, Zuul/Bors, formal patch theory, GSN and NIST SP 800-192 ([R-112](references.md#r-112)–[R-135](references.md#r-135)).


## 4. PDF page landmarks

The following page landmarks connect notable discussion passages to the catalogue. They are navigation aids, not a substitute for checking the exact source edition/version.

- **Pages 31–49:** RDF, ontology composition, mind-map ingestion, graph validation and semantic-web vocabularies — [R-51](references.md#r-51)–[R-61](references.md#r-61), [R-63](references.md#r-63), [R-83](references.md#r-83)–[R-86](references.md#r-86).
- **Pages 33–34:** distinction between RDF's graph model and CRDT-based real-time co-editing — [R-45](references.md#r-45)–[R-50](references.md#r-50), [R-66](references.md#r-66), [R-87](references.md#r-87).
- **NixOS SecOps project section:** local agent isolation and sandbox/tool comparisons, including nono, Landlock, Goose, mcp-nixos, SmolVM and Nixi — [R-79](references.md#r-79) covers the cross-project sandbox and agent mechanisms; other project-specific dependencies remain a scope question below.
- **Page 117:** NIST SP 800-192 and the requirement to verify policy models, not merely execute policies — [R-135](references.md#r-135), alongside OPA/Rego [R-09](references.md#r-09), Cedar [R-10](references.md#r-10) and Sentinel [R-77](references.md#r-77).
- **Pages 154–156:** SLSA, in-toto, GUAC, OpenSSF Scorecard, Best Practices Badge, Security Insights and OSPS Baseline — [R-06](references.md#r-06)–[R-08](references.md#r-08), [R-108](references.md#r-108)–[R-111](references.md#r-111).
- **Page 178:** Writ and Privateer are discussed as complementary workflow and compliance-evaluation tools; Agent Package Manager is named without a resolvable identity — [R-18](references.md#r-18), [R-120](references.md#r-120); see the unresolved identity notes below.
- **Pages 188–200:** GovCheck bootstrap, repository-local authority, acceptance boundary, Git/Pijul adapters and local/team forges — [R-05](references.md#r-05), [R-20](references.md#r-20), [R-68](references.md#r-68), [R-133](references.md#r-133).
- **Pages 219–220:** artifact identity, stable paths, releases, tags and versioning policy — [R-14](references.md#r-14), [R-15](references.md#r-15), [R-21](references.md#r-21), [R-23](references.md#r-23)–[R-26](references.md#r-26).

## 5. Semantic boundaries retained

- SACM 2.3 is the formal specification baseline recorded in [R-34](references.md#r-34); SACM 2.4 Beta 1 is a draft candidate recorded separately in [R-73](references.md#r-73). Neither is automatically adopted as GovCheck’s repository-wide governance metamodel.
- PEAK ([R-74](references.md#r-74)) is a decision-reasoning model for problem, experience, assumptions and knowledge; it is not SACM and does not replace the assurance-case model.
- Tests, runtime observations, model checking, program verification, theorem proof, conformance claims and acceptance decisions remain distinct evidence/assurance categories.
- A VSA or signed attestation delegates trust to a verifier; it does not prove that the verifier is trustworthy or that a claim is true.
- Security baselines and repository-assessment tools are candidates for selectable controls, not universal GovCheck tiers or mandatory dependencies.
- GitHub CODEOWNERS, Allstar and GitHub branch protection are platform-specific mechanisms; they do not define a forge-neutral authority model.
- A source mentioned in the discussion can be retained as historical context without becoming an adopted dependency, normative requirement or implementation claim.

## 6. Unresolved source identity and provenance

The following items cannot be assigned a reliable, unique source record without further information:

1. **Tarski** appears as a possible verification/kernel reference in the discussion, but the exact project, paper or tool is not uniquely identifiable from the preserved context. No guessed URL or dependency is recorded.
2. **Agent Package Manager** is mentioned in the prior discussion without a uniquely verified product identity or URL. It remains intentionally unlinked.
3. **EPIC** appears in later project context as a possible decision-modelling reference, but the exact framework/publication is not identified in the initial PDF or current catalogue. It should not be guessed.
4. The PDF also records implementation-specific NixOS SecOps inputs such as **AgntOS, Nixi, mcp-nixos, nix-agent, SmolVM, matchlock, AerolVM, agent-sandbox, Goose, Lemonade, FastFlowLM, nixpkgs, Lanzaboote, microvm.nix, QEMU, Firecracker, libkrun and cloud-hypervisor**. [R-79](references.md#r-79) already captures the cross-project sandbox/agent references nono, Landlock and Goose. The remaining inputs are not yet assigned GovCheck reference IDs because they may be dependencies of that separate project rather than sources materially used by GovCheck.

These are provenance gaps, not blockers to the current catalogue corrections. They should be resolved only if the corresponding concepts remain relevant to GovCheck.

## 7. Verification status and remaining work

The repository changes are committed on the audit branch, but the following checks have **not** been executed in this environment:

- python3 scripts/check-reference-integrity.py
- python3 scripts/check-reference-integrity.py --external

No GitHub Actions workflow was triggered. The first command must be run locally to verify bilingual parity, identifier/index coverage, anchors, local Markdown links and bidirectional traceability. The external mode must then be run separately to probe URL reachability. Even a successful URL probe cannot establish source authority, semantic relevance, completeness or correctness.

The PDF source inventory is now substantially reconciled with the catalogue and the critical reviews, but a final page-by-page provenance pass over all pre-GovCheck context remains necessary before claiming exhaustive coverage of every source mentioned anywhere in the 224-page PDF.

## 8. Maintenance rule

For every source materially used by a GovCheck record:
1. maintain one canonical R-XX entry, with primary source identity and version/status;
2. describe the precise claim or comparison it supports and its limitations;
3. distinguish a historical mention, candidate, adopted method, implementation and verified result;
4. link the source from every relevant English and French document;
5. maintain the reverse **Cited by / Cité par** links in both catalogues;
6. do not reuse retired identifiers or guess missing source identities.