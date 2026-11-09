# Reference catalogue integrity

The catalogue is a maintained, bilingual evidence index, not an adoption list or a normative policy.

## Source of record

- [English catalogue](references.md) is the default presentation.
- [Catalogue français](references.fr.md) is its semantic counterpart.
- The bilingual catalogues contain 118 active entries. Two identifiers are retired and must never be reused; the later retired identifier was consolidated into the canonical NIST SP 800-218 entry because it duplicated the same source.
- Each entry records primary sources, relevant concepts, the specific GovCheck use and explicit limitations.
- Each architecture record, decision or specification links to the exact catalogue anchor it uses.
- Each catalogue entry's **Cited by / Cité par** field links back to every document that cites it.

## Status and provenance

The initial integration study, **“Évaluer l’intégration des dépôts.pdf”** (6 November 2026, 224 pages), is retained in the project Library and is not duplicated in this repository. Its placement and evidence boundary are recorded in [ADR 0002](decisions/0002-study-placement.md) and [ADR 0002 (français)](decisions/0002-study-placement.fr.md).

The catalogue preserves sources discussed in that study and in subsequent GovCheck design discussions, including:
- the Cartocortex, MoriNet and SaussuNet repositories and their PRs #9, #27 and #28;
- CRDT foundations and implementations (Yjs/Yrs, Automerge, Loro), y-webrtc, WebTorrent, WebRTC, ICE, STUN, TURN, Hyperswarm/HyperDHT and peer discovery;
- OKF, RDF, OWL, SKOS, SHACL, JSON-LD, Turtle, PROV-O, Dublin Core, BIBO, DCAT, Web Annotation, ActivityStreams, SIOC, P-Plan and Schema.org;
- mind-map interchange formats and import/export tools;
- cross-agent instruction formats and spec-driven workflows (AGENTS.md, VS Code, Codex, Claude Code and GitHub Spec Kit);
- risk and threat modeling, NIST SP 800-192 access-control policy/model verification, B and Z formal specification, CSP/FDR process modeling, iStar goal modeling, deontic logic, assurance cases, PEAK decision reasoning, continuous monitoring and runtime assurance. The approximate TURN-relay percentage repeated in the source study is explicitly unverified and must be validated with deployment telemetry;
- Git/Pijul/Nest semantics, policy engines and OPA tool calling, software-supply-chain provenance, agent workflow and isolation references;
- research on CUGA, Audit-as-Code, empirical policy-as-code adoption and runtime enforcement for MCP-based agents;
- OWASP guidance for agent/MCP security, LUMC research-software versioning/release guidance and GitHub Actions workflow placement.

A reference is not an endorsement. A proposal, backlog, research prototype, beta specification, product page and normative standard have different evidence status. Each entry states its own limitations. A named protocol or library in the catalogue does not imply that GovCheck, Cartocortex, MoriNet or SaussuNet implements or adopts it.

## Maintenance rule

When a document uses an external source:
1. add or update one R-XX entry, preferring the primary publisher/standards body/official repository;
2. state the specific concept and claim for which it is relevant;
3. state the limit and distinguish proposed, implemented, verified and adopted status;
4. add a direct anchor link in the citing English and French documents;
5. update **Cited by / Cité par** in both catalogues;
6. never reuse a retired identifier.

Candidate sources that have not yet been used by a record may remain in the catalogue with an explicit “no current record cites” field. Never link a **Cited by / Cité par** field to a record absent from the same branch. The domain-semantic/bootstrap sources R-94–R-103 are cited by Architecture 0027 as candidate inputs; they remain research candidates, not adoption decisions. Their catalogue backlinks identify the architecture record that discusses them.

Do not add a reference merely because a technology name appears. Record it when the source materially supports a claim, comparison, interface or documented research trail. Conversely, do not let a source disappear merely because its associated option was not selected.

## Automated integrity check

Run from the repository root:

~~~sh
python3 scripts/check-reference-integrity.py
~~~

This offline check verifies bilingual entry parity, two- and three-digit reference identifiers, thematic-index coverage, EN/FR citation symmetry for paired records, source metadata, reference anchors, local Markdown links under docs/, both directions of document/catalogue traceability, and consistency between an entry's no-citation marker and its declared backlinks. It also warns when a source document contains an external URL that is not represented in the central catalogue.

To additionally probe external URLs (network required; publisher-side blocking is reported as a warning):

~~~sh
python3 scripts/check-reference-integrity.py --external
~~~

The external check is a reachability signal, not a guarantee that a source is authoritative, current, complete or semantically relevant.
