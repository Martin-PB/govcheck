# SACM 2.4 Beta 1 — interoperability and source-consistency risk

**Status:** independent implementation audit recorded; GovCheck source-view guards added; no SACM 2.4 conformance claim.  
**Date:** 2026-11-12.  
**Primary catalogue source:** [R-73 — OMG SACM 2.4 Beta 1](../references.md#r-73).  
**Independent implementation audit:** [R-128 — Assurance Forge SACM 2.4 Beta 1 impact audit](../references.md#r-128).

## 1. Decision-relevant finding

SACM 2.4 Beta 1 must not be treated as one stable, implementable interchange model. The official OMG page labels the beta as in-process/informational and SACM 2.3 remains the formal specification. An independent implementation audit in Assurance Forge reports that Beta 1 currently lacks a usable native interchange contract (no stable namespace/XSD/Ecore/reference implementation or external native files) and that the specification PDF text contradicts the machine-readable metamodel XML on multiple structural points.

The Assurance Forge report is not an OMG authority and its conclusions must be checked against the pinned OMG artifacts. It is, however, a concrete engineering audit with a reproducible download script, artifact hashes, a model-diff tool and an implementation impact analysis. It is sufficient evidence to **block any claim that GovCheck currently supports or conforms to SACM 2.4 Beta 1 as a single coherent format**.

## 2. Text/model contradictions reported by the independent audit

| Subject | Specification PDF text | Machine-readable metamodel XML | Consequence |
|---|---|---|---|
| Element identity | `gid : String[0..1]` | `elementId : UID[1]`; no `gid` | Identity cannot be normalized without selecting a source view and recording the transformation |
| Assertion declaration literals | `axiomatic`, `assumed`, `asserted`, `needsSupport` | `axiomatic`, `assumed`, `asserted`, plus `byRule`; no `needsSupport` | The same enum name has incompatible value sets |
| `AssertedEvidence.evidence` multiplicity | `[0..*]` | `[1..*]` | Empty evidence collections are valid in one view and invalid in the other |
| `Claim.value` | `MultiLangString` | `ExpressionLangString` | Text and typed expression values are not interchangeable |
| `BindingPackage` inheritance | Text clauses disagree on the superclass set | XML declares `ScopedPackage` and `SACMPackageWithBinding` | A parser/validator may build a different type hierarchy |
| `SACMElement.abstraction` multiplicity | `[0..1]` | `[0..*]` | One view permits at most one abstraction, the other multiple |
| `AssertedRelationship.isCounter` multiplicity | `Boolean[1]` | `Boolean[0..1]` | Requiredness differs |

The audit also reports stale 2.3 names in the beta text/annexes, removed literals still referenced by Annex C, ambiguity around compliance points and a vendor-specific UML Profile XMI example. See the complete pinned audit and its linked defect inventory before implementing any additional construct.

## 3. What the audit says about interchange

The audit distinguishes the official machine-readable metamodel XML from an interoperable instance format:

- The OMG Beta 1 page publishes a normative metamodel XML artifact, but the audit reports no stable 2.4 XMI namespace or XSD/Ecore contract for native instance interchange.
- The available UML Profile XMI example uses a vendor-specific MagicDraw namespace and is not a portable SACM 2.4 instance format.
- No independent native 2.4 files or reference implementation were available to build an interoperability corpus at the audit date.
- The beta fetch script pins four official OMG artifacts and SHA-256 hashes; the audit says the beta may be republished in place, so unpinned references are unsafe.

This is not a claim that the OMG XML file is invalid. It is a distinction between a machine-readable metamodel artifact and a stable, portable serialization contract for governed assurance cases.

## 4. Pinned artifact hashes reported by the audit

The Assurance Forge fetch script records comparison SHA-256 values for four official OMG Beta 1 artifacts as downloaded on 2026-10-02. GovCheck independently downloaded and verified the normative specification PDF (9,019,601 bytes) and normative metamodel XML (524,243 bytes) in workflow run [43494908580](https://github.com/Martin-PB/govcheck/actions/runs/43494908580); both exact source payloads are retained in artifact [14071002816](https://github.com/Martin-PB/govcheck/actions/runs/43494908580/artifacts/14071002816). The changebar PDF and informative UML Profile XMI remain unverified by GovCheck.

| OMG artifact | File ID | SHA-256 reported by Assurance Forge |
|---|---|---|
| Specification PDF | ptc/26-06-34 | `25f32d1cd4bf32dfa9c92c7c1840e1a113b1e91c0e97252f6551878c39997ff5` |
| Specification changebar PDF | ptc/26-06-35 | `6840a0f67104d07997168d07079c0e168f5ac65ef5fa1779eccb9ebef1fe5f96` |
| Metamodel XML | ptc/26-05-28 | `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830` |
| UML Profile XMI | ptc/26-05-21 | `9149a0414628e1b70c1f7c2235f5180c64e7a144601eb2ae78d539681918838b` |

## 5. GovCheck response: source-view-qualified mapping

The Lean module `GovCheckCoherence.SACM24` now distinguishes document-level views from the individual clauses, annexes and figures that make claims within those views. The earlier PDF-wide predicate was too coarse: it incorrectly rejected `byRule` for the PDF even though Clause 15.2.1 adds it, while Clause 13.6 includes `needsSupport`.

- `SourceView` identifies the document format; `DeclarationSourceFragment` separately identifies PDF Clause 13.6, Annex G.6 item 6, Clause 15.2.1 and the normative XML model.
- `IdentitySourceFragment` distinguishes PDF Clause 9.2 (`gid`), PDF Figure 9.1 (`elementId`) and the XML model (`elementId`).
- A Claim interpretation must carry the exact declaration and identity fragments used. It no longer asserts one canonical declaration set or identity field for the entire PDF.
- The Claim slice preserves `subject` as `Option (List SACMElementRef)`, declaration presence separately from its default `asserted`, raw value type labels, optional `whole`, and multi-valued opaque assertion/rule/strength references.
- A mapped identity must be non-empty; this makes the current mapping contract explicitly partial for source records without a usable identity.
- Lean theorems prove differences between the transcribed fragment facts: declaration literal sets, identity fields, selected multiplicities, inheritance lists and assertion-rule feature names.

The detailed [source-view alignment report](sacm24-source-view-alignment.md) records the evidence and classification for each item. These theorems do not prove that the source transcription is correct, that the Python XMI parser refines UML/MOF semantics, or that the manually encoded inference bridge is SACM's intended semantics. The `SACMClaimInterpretation` and `SACMClaimMapping` types define proof obligations; no concrete source-derived GovCheck mapping instance or full-source conformance claim is established.

## 6. Required handling policy

Until OMG publishes a stable formal SACM 2.4 version or a beta with a coherent serialization contract:

1. **Keep SACM 2.3 as the formal conformance baseline.** Do not change 2.3 schemas, fixtures, validators or conformance claims to fit the beta.
2. Treat SACM 2.4 Beta 1 as research input only. Do not advertise native 2.4 import/export.
3. Pin each source artifact by URL, publication/file identifier, retrieval date and cryptographic hash. Record whether a mapping reads the PDF text, normative metamodel XML or informative UML Profile XMI.
4. Preserve conflicting fields and values in their source view. Any normalization must be an explicit, versioned transformation with declared loss and an authorized decision.
5. Do not invent an XMI namespace, XSD, Ecore or interchange profile. Wait for an official or independently interoperable contract and real external instance files.
6. Keep the 2.4 model and any future conformance matrix separate from 2.3. A later implementation should be additive and version-dispatched, not a silent replacement.

## 7. Next verification work

The current [source-view alignment report](sacm24-source-view-alignment.md) is a revision-bound comparison record, not a precedence decision.

- Obtain and pin the four OMG Beta 1 artifacts using the official URLs and compare their hashes with the independent audit's recorded hashes.
- Validate the human transcription of each PDF/XML fragment against the pinned source bytes; the current Lean theorems prove differences among transcribed constants, not transcription correctness. Build an explicit extraction/reconciliation pipeline before claiming automated PDF/XML diff coverage.
- Build negative fixtures where the source view and declaration/identity/multiplicity disagree; each must be rejected or explicitly represented as a conflict.
- Only after a portable instance format and sample files exist, build a native import/export round-trip corpus.
- Revisit the mapping when OMG publishes Beta 2 or the formal SACM 2.4 specification.

**Conclusion:** the first SACM Claim/Assertion mapping is useful precisely because it exposes the beta's contradictions instead of hiding them. It is a formalized source-view boundary, not a declaration of SACM 2.4 support.
