# Reference catalogue integrity

The catalogue is a maintained, bilingual evidence index, not an adoption list or a normative policy.

## Source of record

- [English catalogue](references.md) is the default presentation.
- [Catalogue français](references.fr.md) is its semantic counterpart.
- Every source has a stable R-XX identifier. Retired identifiers are never reused.
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
- risk and threat modeling, assurance cases, PEAK decision reasoning, continuous monitoring and runtime assurance. The approximate TURN-relay percentage repeated in the source study is explicitly unverified and must be validated with deployment telemetry;
- Git/Pijul semantics, policy engines, software-supply-chain provenance, agent workflow and isolation references.

A reference is not an endorsement. A proposal, backlog, research prototype, beta specification, product page and normative standard have different evidence status. Each entry states its own limitations. A named protocol or library in the catalogue does not imply that GovCheck, Cartocortex, MoriNet or SaussuNet implements or adopts it.

## Maintenance rule

When a document uses an external source:
1. add or update one R-XX entry, preferring the primary publisher/standards body/official repository;
2. state the specific concept and claim for which it is relevant;
3. state the limit and distinguish proposed, implemented, verified and adopted status;
4. add a direct anchor link in the citing English and French documents;
5. update **Cited by / Cité par** in both catalogues;
6. never reuse a retired identifier.

Do not add a reference merely because a technology name appears. Record it when the source materially supports a claim, comparison, interface or documented research trail. Conversely, do not let a source disappear merely because its associated option was not selected.

## Automated integrity check

Run from the repository root:

~~~sh
python3 scripts/check-reference-integrity.py
~~~

This offline check verifies bilingual entry parity, source metadata, reference anchors, all local Markdown links, and both directions of document/catalogue traceability.

To additionally probe external URLs (network required; publisher-side blocking is reported as a warning):

~~~sh
python3 scripts/check-reference-integrity.py --external
~~~

The external check is a reachability signal, not a guarantee that a source is authoritative, current, complete or semantically relevant.
