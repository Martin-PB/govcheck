# SACM 2.4 Beta 1 — source-derived XMI structural inventory

**Status:** generated structural inventory for one digest-pinned OMG metamodel XML revision; no GovCheck semantic mapping is inferred.  
**Source:** [R-197 — OMG SACM 2.4 Beta 1 normative machine-readable metamodel XML](../references.md#r-197).  
**Independent source-view risk:** [R-128](../references.md#r-128).  
**Generator:** [`scripts/parse-sacm-xmi.py`](../../scripts/parse-sacm-xmi.py).  
**Reviewable summary:** [`formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json`](../../formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json).  
**Full generated inventory:** published with the source capture workflow artifact; not duplicated as a large generated file in the repository.

## 1. Exact input and reproducibility

The parser consumes only the captured source payload whose SHA-256 matches the pinned R-197 value:

- OMG file ID: `ptc/26-05-28`;
- dated source revision: `2026-05-04`;
- URL: `https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml`;
- byte length: `524243`;
- SHA-256: `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`.

The source is XML whose document root and metamodel vocabulary use OMG XMI 20131001 and UML 20131001 namespaces. The exporter metadata identifies MagicDraw Clean XMI Exporter 2024x v6. This describes the actual source representation; it does **not** imply that SACM 2.4 defines a portable XMI instance interchange contract.

The original `source.xml` remains authoritative and is preserved byte-for-byte by the capture workflow. The generated inventory is a derived view and can always be regenerated from those exact bytes and the parser revision.

## 2. Structural findings

The digest-pinned document contains:

| XMI/UML construct | Count |
|---|---:|
| Identified XMI elements (`xmi:id`) | 1,616 |
| UML Profile | 1 |
| UML Packages | 19 |
| UML Classes | 121 |
| UML Associations | 121 |
| UML Properties (owned attributes and association ends) | 355 |
| UML Generalizations | 167 |
| UML Enumerations | 8 |
| UML Enumeration literals | 37 |
| UML Constraints | 40 |
| UML Comments | 157 |
| UML DataTypes | 2 |
| UML OpaqueExpressions | 40 |
| UML OpaqueBehaviors | 3 |

The package tree includes the core packages `Base`, `Foundation`, `Terminology`, `Packaging`, `Artifact` and `Argument`; `Mapping` contains `CAE` and `GSN` packages. A `NonNormative` branch contains additional material such as `SACMView`, `DI`, `NamedValueTypes`, `DateTimeDuration`, assessment-related constructs and joins. The inventory preserves source spellings, including names that may look unusual; it does not silently normalize them.

The eight enumerations and their source literals are recorded explicitly. They include `AssertionDeclarationKind` (`axiomatic`, `assumed`, `asserted`, `byRule`) and `InferenceTypeKind` (`probable`, `collective`, `necessary`, `sufficient`, `necessaryAndSufficient`, `byRule`). These are XML-source facts only; R-128 documents conflicting PDF-text declarations, including `needsSupport` in place of `byRule`.

## 3. Reference and containment accounting

The inventory records 1,434 explicit reference edges:

- 1,371 references resolve to an `xmi:id` within this exact document;
- 63 references are external `href` references and remain unresolved by design;
- zero unresolved internal references were observed in the recognized reference attributes.

The output preserves each identified element's stable `xmi:id`, XML tag, `xmi:type`, name, full attributes, nearest identified owner, containment path, direct text and ordered child structure. It separately indexes package/classifier ownership, association member ends, property types and multiplicities, generalization targets, constraint targets/specifications and reference edges. ID-less nodes (including exporter documentation, constraint expression children, comments' nested data and other non-identified XML nodes) are retained inline; namespace declarations are recorded.

This accounting is a parser result for the pinned file, not proof that the XML is a semantically complete or well-formed UML model.

## 4. Parser boundary and defensive behavior

The parser uses only Python's standard-library `xml.etree.ElementTree`. It:

- verifies the exact source SHA-256 before parsing;
- rejects empty/oversized payloads, malformed XML, duplicate `xmi:id` values and DTD/entity declarations;
- distinguishes `xmi:type` metaclass declarations from unqualified UML `type` references;
- resolves recognized internal ID references against the complete document ID set;
- preserves external `href` values without fetching or interpreting their targets;
- preserves unknown identified constructs generically rather than dropping or coercing them.

It does not execute OCL or other constraint languages, resolve the external UML metamodel, validate UML/MOF well-formedness, interpret vendor extensions, infer inheritance semantics beyond recording `general` references, or assert any SACM-to-GovCheck equivalence. The raw XML remains the source of truth whenever the derived representation is incomplete or ambiguous.

## 5. Verification status

The test suite contains seven synthetic tests covering construct indexing, property multiplicities, association/generalization/constraint references, ID-less exporter documentation, duplicate IDs, unresolved references, digest mismatch, DTD/entity rejection, malformed XML and summary derivation. The workflow passed on source-code revision `8c0288d5992929089e96596c3f31a8f20ea535f4` in [run 43451737489](https://github.com/Martin-PB/govcheck/actions/runs/43451737489): all 12 tests (five ingestion tests and seven inventory tests), official download/digest verification, full inventory generation, structural JSON comparison with the committed summary and artifact publication succeeded. The current PR branch retains identical parser, test, summary and workflow blobs. The full inventory is published in [artifact 14051746241](https://github.com/Martin-PB/govcheck/actions/runs/43451737489/artifacts/14051746241) alongside the raw source and capture manifest.

These tests establish the behavior of this Python implementation over the tested fixtures and pinned source run. They are **not** a formal proof that the parser is a correct implementation of the complete XMI/UML standards or that its output is a semantics-preserving UML model. No Lean theorem currently links the Python parser output to the source XML infoset.

## 6. Explicit non-claims and next work

This increment does not:

- resolve the known PDF/XML contradictions in SACM 2.4 Beta 1;
- establish a complete SACM metamodel interpretation or SACM 2.4 conformance;
- import/export SACM assurance-case instances;
- prove parser refinement to Lean or GovCheck's metamodel;
- generate an operative GovCheck semantic mapping;
- adopt SACM 2.4 Beta 1 or make it the formal baseline.

Next, compare the source-derived structural inventory with the exact PDF source view and the R-128 conflict list, classify each discrepancy by affected construct and scope, and only then define typed source-view-specific mapping obligations. Existing Lean Claim/Assertion/inference declarations remain manually authored; this inventory does not validate them. Any semantic correspondence used as an established GovCheck premise must carry a proof of the exact relation claimed.
