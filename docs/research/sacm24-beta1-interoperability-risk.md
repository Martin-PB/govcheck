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

## 4. GovCheck response: source-view-qualified mapping

The Lean module `GovCheckCoherence.SACM24` has been tightened so it cannot silently merge the two conflicting views:

- `SourceView` distinguishes `specificationText` from `normativeMetamodelXML`.
- `AssertionDeclarationKind` retains the union of both value sets, including both `needsSupport` and `byRule`.
- `declarationSupportedBySourceView` rejects `byRule` when the PDF text view is selected and rejects `needsSupport` when the metamodel XML view is selected.
- `ElementIdentityField` preserves `gid` versus `elementId`; the source view determines the expected field.
- `SACMClaimInterpretation` requires proofs that the declaration literal and identity field are consistent with the selected source view, and pins any explicit subject to the exact source-model revision.
- `SACMClaimMapping` composes that source interpretation with the general GovCheck `EvidenceMapping` semantic bridge.

These guards formalize the two conflicts relevant to the current Claim/Assertion slice. They do not resolve the remaining multiplicity, value-type or inheritance conflicts, and they do not establish conformance to either full source view.

## 5. Required handling policy

Until OMG publishes a stable formal SACM 2.4 version or a beta with a coherent serialization contract:

1. **Keep SACM 2.3 as the formal conformance baseline.** Do not change 2.3 schemas, fixtures, validators or conformance claims to fit the beta.
2. Treat SACM 2.4 Beta 1 as research input only. Do not advertise native 2.4 import/export.
3. Pin each source artifact by URL, publication/file identifier, retrieval date and cryptographic hash. Record whether a mapping reads the PDF text, normative metamodel XML or informative UML Profile XMI.
4. Preserve conflicting fields and values in their source view. Any normalization must be an explicit, versioned transformation with declared loss and an authorized decision.
5. Do not invent an XMI namespace, XSD, Ecore or interchange profile. Wait for an official or independently interoperable contract and real external instance files.
6. Keep the 2.4 model and any future conformance matrix separate from 2.3. A later implementation should be additive and version-dispatched, not a silent replacement.

## 6. Next verification work

- Obtain and pin the four OMG Beta 1 artifacts using the official URLs and compare their hashes with the independent audit's recorded hashes.
- Run GovCheck's own text/XML structural diff and extend the Lean source-view model to the remaining conflicts: AssertedEvidence multiplicity, Claim.value type, BindingPackage inheritance, abstraction multiplicity and isCounter multiplicity.
- Build negative fixtures where the source view and declaration/identity/multiplicity disagree; each must be rejected or explicitly represented as a conflict.
- Only after a portable instance format and sample files exist, build a native import/export round-trip corpus.
- Revisit the mapping when OMG publishes Beta 2 or the formal SACM 2.4 specification.

**Conclusion:** the first SACM Claim/Assertion mapping is useful precisely because it exposes the beta's contradictions instead of hiding them. It is a formalized source-view boundary, not a declaration of SACM 2.4 support.
