# SACM 2.4 Beta 1 — source-native metamodel capture and ingestion boundary

**Status:** implementation candidate; source bytes are pinned by the ingestion workflow, but this is not SACM conformance and not a SACM instance importer.  
**Date:** 2026-11-13.  
**Official source:** [OMG SACM specification page](https://www.omg.org/spec/SACM), catalogue entry [R-197](../references.md#r-197).  
**Related formal slice:** [GovCheckCoherence.SACM24](../../formal/lean/GovCheckCoherence/SACM24.lean).

## 1. Selected source artifact and version status

The first source-native ingestion target is the OMG normative machine-readable metamodel artifact:

| Field | Pinned value |
|---|---|
| Authority | Object Management Group (OMG) |
| Specification | Structured Assurance Case Metamodel (SACM) |
| Version | 2.4 Beta 1 |
| Version status | In-process / informational beta |
| Formal baseline | SACM 2.3, October 2023 |
| OMG file ID | \`ptc/26-05-28\` |
| Source revision path | \`SACM/20260504/SACM2.4_Metamodel.xml\` |
| Native format | XML |
| Source view | Normative machine-readable metamodel XML |
| SHA-256 comparison value | \`0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830\` |

The OMG catalogue identifies this XML as a **normative machine-readable document** for the 2.4 beta. The same catalogue separately identifies the specification PDF as normative prose and the UML Profile XMI as informative. SACM 2.4 Beta 1 is in process; SACM 2.3 remains the formal adopted version. These source roles must not be conflated.

The SHA-256 value above is the comparison value recorded by the independent Assurance Forge audit (R-128). GovCheck's workflow downloads the official versioned OMG URL and independently recomputes the digest. A successful run is the first GovCheck-side verification of that digest; before that run succeeds, the digest is a pinned expected value, not a locally verified fact.

## 2. Why ingest the metamodel XML first

The XML is the authoritative machine-readable description of the metamodel, not an instance of an assurance case. It is the right first ingestion target because it provides a stable, version-addressed source from which the later metaclass, property, association, multiplicity, enumeration and constraint inventory can be derived.

It does **not** establish a portable native instance interchange format. The independent R-128 audit reports that Beta 1's PDF and XML views disagree on multiple constructs and that the available UML Profile XMI is informative and vendor-specific. This work therefore does not claim to import arbitrary SACM assurance-case instances.

## 3. Ingestion contract implemented by this slice

Run:

\`\`\`bash
curl --fail --location --proto '=https' --tlsv1.2 \\
  --output /tmp/SACM2.4_Metamodel.xml \\
  https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml
python scripts/ingest-sacm-metamodel.py \\
  --input /tmp/SACM2.4_Metamodel.xml \\
  --output-dir /tmp/govcheck-sacm-import
\`\`\`

The importer:

1. reads the downloaded source as bytes and checks the expected SHA-256 before creating output;
2. writes the exact source byte sequence to \`source.xml\` without parsing and reserializing it;
3. creates a derived XML event index with qualified names as seen in the source, ordered attributes, element nesting, text, comments, processing instructions, CDATA boundaries, document offsets and line/column locations;
4. records the source authority, file ID, dated URL, source view, digest, retrieval time, byte length and parser/index format in \`manifest.json\`;
5. records no semantic correspondences by default.

The raw byte copy is authoritative for fidelity. The event index is a navigation aid, not a canonicalized replacement: XML lexical distinctions not represented in the event index remain recoverable from \`source.xml\`. External DTD/entity resolution is disabled; the importer applies a 32 MiB input limit.

The workflow runs unit tests, downloads the exact OMG artifact, verifies its digest, produces the capture manifest/index and publishes those derived files as a 90-day workflow artifact. The source payload itself remains available from the official versioned OMG URL and is not copied into Git history.

## 4. Semantic mapping boundary

This ingestion makes **no** mapping from a SACM metaclass to a GovCheck metaclass. It preserves the source-native XML and records an empty \`semanticMappings\` array.

| Source information | Current treatment | Semantic status |
|---|---|---|
| XML bytes, encoding declaration, prefixes, attributes, comments, processing instructions and text | Retained byte-for-byte in \`source.xml\`; structural events indexed separately | Source preservation, not semantic correspondence |
| Element/attribute names and containment | Indexed as source-qualified XML events | Structural observation only |
| SACM metaclass/property/association meaning | Not interpreted by this first importer | Uninterpreted source content |
| PDF/XML disagreements | Kept as distinct source views in the existing SACM research and Lean model | Explicit conflict; no normalization |
| SACM Claim/Assertion/inference to GovCheck assurance concepts | Existing Lean slice remains an authority-supplied interpretation contract | Candidate correspondence; not derived by this XML ingestion |
| GovCheck authority, lifecycle, decisions and requirements | Remain GovCheck-native concepts | No automatic SACM equivalence |

The current Lean SACM 2.4 slice is a manually authored formal model of selected Claim/Assertion/inference obligations. It is not generated from this XML and does not prove that a Python parser preserves the XML's MOF/XMI semantics. The importer and the Lean model are deliberately separate until an exact source-derived metamodel inventory and parser refinement relation exist.

Any future operative semantic correspondence must still satisfy the general GovCheck proof-carrying mapping contract: exact source/target meanings, source and target revisions, scope and assumptions, with a kernel-checked proof of the precise relation claimed. An XML digest proves byte identity relative to the hash assumption; it does not prove semantic equivalence.

## 5. Verification and acceptance status

Synthetic unit fixtures exercise:
- exact byte preservation;
- prefix-qualified element and attribute names;
- ordered attributes;
- comments, processing instructions and CDATA boundaries;
- digest mismatch rejection before output creation;
- malformed XML rejection;
- external DTD rejection;
- explicit absence of inferred semantic mappings.

These fixtures are not OMG SACM instance examples and do not establish conformance. The source-capture workflow must also pass against the actual downloaded OMG XML before the pinned source digest can be called GovCheck-verified.

## 6. Explicit non-claims and next step

This slice does not yet:
- interpret MOF/XMI classes, properties, associations, multiplicities, subsets, redefinitions or constraints;
- generate a complete SACM metamodel inventory;
- import/export a SACM assurance-case instance;
- round-trip an instance model;
- map all SACM concepts into GovCheck;
- prove a parser-to-Lean refinement theorem;
- claim SACM 2.4 conformance or normative adoption.

The next increment is to parse the pinned metamodel's actual MOF/XMI vocabulary into a lossless typed inventory while retaining the raw source, then derive a coverage matrix directly from that inventory. Only after the inventory is checked against the specification PDF and its known contradictions should individual source metaclasses be mapped to GovCheck concepts. Each mapping remains non-operative until its exact semantic obligation is proved.
