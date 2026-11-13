# SACM 2.4 Beta 1 — source-view alignment and conflict inventory

**Status:** source-view comparison and fragment-level conflict model; no precedence rule or SACM 2.4 conformance claim is adopted.  
**Independent implementation audit:** [R-128](../references.md#r-128).  
**Normative metamodel XML:** [R-197](../references.md#r-197).  
**Normative PDF:** [R-198](../references.md#r-198).  
**Informative UML Profile XMI:** [R-199](../references.md#r-199).  
**Structural inventory:** [XMI inventory report](sacm-xmi-structural-inventory.md) and [committed summary](../../formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json).  
**Formal source-fragment model:** [`GovCheckCoherence.SACM24`](../../formal/lean/GovCheckCoherence/SACM24.lean).

## 1. Keep the artifacts separate

The OMG catalogue exposes distinct SACM 2.4 Beta 1 artifacts. They are not interchangeable representations of one already-resolved schema:

| Source view | OMG file ID | Exact source path | Authority/status | SHA-256 provenance |
|---|---|---|---|---|
| Normative specification PDF | `ptc/26-06-34` | `SACM/20260504/SACM2.4.pdf` | Normative specification text/figures | `25f32d1cd4bf32dfa9c92c7c1840e1a113b1e91c0e97252f6551878c39997ff5`, reported by independent R-128 audit; not yet independently recomputed by GovCheck |
| Normative machine-readable metamodel XML | `ptc/26-05-28` | `SACM/20260504/SACM2.4_Metamodel.xml` | Normative machine-readable metamodel | `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`, verified by GovCheck against 524,243 downloaded bytes |
| Informative UML Profile XMI | `ptc/26-05-21` | `SACM/20260504/SACM2.4_Profile.xmi` | Informative profile artifact, not the normative metamodel XML | `9149a0414628e1b70c1f7c2235f5180c64e7a144601eb2ae78d539681918838b`, reported by R-128 |
| Informative changebar PDF | `ptc/26-06-35` | `SACM/20260504/SACM2.4_Changes.pdf` | Informative change summary | `6840a0f67104d07997168d07079c0e168f5ac65ef5fa1779eccb9ebef1fe5f96`, reported by R-128 |

The three latter hashes are provenance values from the independent audit's pinned fetch script. GovCheck has independently verified the XML digest only. The PDF is 161 pages; R-128 reports approximately 98% text extraction coverage and warns that the remaining diagram-only labels require visual review. A missing PDF text statement must therefore be recorded as an omission in the extracted text view, not automatically as proof that no diagram states it.

## 2. Conflict and omission matrix

The table preserves source-fragment scope. “PDF” never means a single internally coherent set of claims where the PDF itself disagrees.

| Concept / feature | Normative PDF source statement | Normative XML metamodel statement | Classification | Impact on the current Lean slice |
|---|---|---|---|---|
| `SACMElement` identity | Clause 9.2: `gid : String[0..1]`; Figure 9.1 shows `elementId : UID[1]` | `elementId : UID[1]` | **PDF-internal conflict**; XML agrees with the figure, not the clause text | Identity evidence must cite a clause/figure fragment. A PDF-wide “gid” rule is invalid. |
| `Claim.value` | Clause 13.9: `MultiLangString[0..1]` | `ExpressionLangString[0..1]` | **Direct type conflict** | Keep the source type label and raw payload; do not coerce either type to a GovCheck proposition or plain string. |
| `Claim.subject` | Not stated in the extracted PDF prose view | `SACMElement[0..*]` | **XML addition / PDF-text omission**; not a direct contradiction | `Option (List ...)` distinguishes an absent feature from a present empty or multi-valued feature. No PDF mapping is inferred. |
| `Claim.whole` | Not stated in the extracted PDF prose view | `SACMModel[0..*]` | **XML addition / PDF-text omission** | Preserve the XML feature separately; no PDF value is fabricated. |
| `AssertionDeclarationKind` | Clause 13.6 / Figure 13.1 includes `needsSupport`; Annex G.6 item 6 lists only `axiomatic`, `assumed`, `asserted`; Clause 15.2.1 adds `byRule` | `axiomatic`, `assumed`, `asserted`, `byRule` | **PDF-internal conflict across fragments**; XML agrees with the Clause 15 extension, not the Clause 13 list | Declaration evidence is now bound to a specific clause/annex/XML fragment. Neither `needsSupport` nor `byRule` is rejected for the PDF document as a whole. |
| `AssertedEvidence.evidence` multiplicity | Clause 13.13: `ArtifactReference[0..*]` | `ArtifactReference[1..*]` | **Direct multiplicity conflict** | Not yet represented in the current Claim slice; requires a separate relationship mapping. |
| `SACMElement.abstraction` multiplicity | Clause 9.2: `SACMElement[0..1]` | `SACMElement[0..*]` | **Direct multiplicity conflict** | Not yet mapped. Do not reduce a multi-valued XML relation to an optional single reference. |
| `AssertedRelationship.isCounter` multiplicity | Clause 13.11: `Boolean[1]` | `Boolean[0..1]` | **Direct multiplicity conflict** | Not yet mapped; absence and explicit false must not be conflated. |
| `BindingPackage` inheritance | Clause 10.5: `ScopedPackage` and `SACMPackageWithBinding`; clause 11.3: `ModelElement` | `ScopedPackage` and `SACMPackageWithBinding` | **PDF-internal conflict**; XML agrees with clause 10.5 | Do not pick one PDF clause silently. |
| `SACMModel` inheritance | Clause 9.10: `ModelElement`; Annex G.6 item 5 additionally lists `Assertion` and `Assessment` | `ModelElement`, `Assertion`, `Assessment` | **PDF-fragment difference / annex expansion**; XML agrees with Annex G.6 | Preserve clause and annex as distinct claims; no single flattened superclass set yet. |
| `SACMDependency` inheritance | Clause 9.11: `DirectedRelationship` | `DirectedRelationship` and `BaseElement` | **XML addition relative to PDF clause text** | Not yet mapped. |
| `Rule` inheritance | Clause 15.2.3: `BaseElement` | `ModelElement` and `BaseElement` | **XML addition relative to PDF clause text** | Not yet mapped. |
| Assertion rule feature name | PDF text/diagram uses `assertionRule` | XML property is `assertionDeclarationRule` | **Feature-name divergence**; semantic identity not yet established | Keep source names and provenance separate until a mapping is proved. |
| `InferenceTypeKind` | The six literals are described across the PDF fragments | XML has `probable`, `collective`, `necessary`, `sufficient`, `necessaryAndSufficient`, `byRule` | No literal-set conflict identified in the current audit | The literal set alone does not prove the Lean entailment semantics. |

**Multiplicity caveat:** the XMI inventory preserves the literal nodes and their explicit XML attributes; it does not currently apply UML default-value semantics to normalize omitted `LiteralInteger.value` or absent upper/lower value nodes. The cardinalities above are the normalized readings recorded by the independent R-128 audit. They are not claimed to have been mechanically proved by the Python inventory parser.

## 3. Correction to the first Lean slice

The earlier Claim/Assertion formalization treated `specificationText` as one coherent PDF view and consequently rejected `byRule` for the PDF view. That was too coarse: the same PDF adds `byRule` in Clause 15.2.1 while another fragment includes `needsSupport`. The PDF also gives conflicting identity fields between Clause 9.2 and Figure 9.1.

The Lean model now uses fragment-level evidence:

- `DeclarationSourceFragment` distinguishes PDF Clause 13.6, Annex G.6 item 6, Clause 15.2.1 and the normative XML model.
- `IdentitySourceFragment` distinguishes PDF Clause 9.2, PDF Figure 9.1 and the XML model.
- A mapped Claim must carry the exact declaration and identity fragments used; a document-level label alone is insufficient.
- The formal `SACMClaim.subject` is `Option (List SACMElementRef)`: `none` means the selected source view does not state the feature; `some []` means the feature is present with no values; a non-empty list preserves multiple subjects.
- Declaration presence is optional and its effective default is modelled separately as `asserted`.
- A raw Claim value retains a source type label and payload; assertion values, rule references and strengths are retained as lists of opaque references.
- The source-to-GovCheck mapping remains partial: it requires a non-empty identity and explicit mapping evidence. It is not a full SACM object encoding.

The Lean theorems prove injectivity of the declaration-to-disposition mapping and differences between the **transcribed fragment facts** (declaration sets, identity fields, multiplicities, inheritance lists and feature names). They do not prove that the PDF/XML transcription is correct, that the Python parser refines XMI semantics, or that an abstract inference bridge is the semantics intended by SACM.

## 4. Authority and normalization boundary

No precedence rule is adopted between the normative PDF and normative metamodel XML. Both source artifacts remain available as separately versioned claims. A conflict may be:
- internal to one document (PDF clause versus annex/figure);
- between the PDF and XML;
- an addition or omission rather than a direct contradiction;
- a naming difference whose semantic identity is not yet established;
- unresolved because a diagram or external reference has not been interpreted.

GovCheck must preserve these distinctions, exact source locations, source revisions and the relation asserted. A normalized view, if later required, must be a separately identified, versioned transformation with declared loss and an explicit authorized decision. It must not overwrite the source claims.

## 5. Remaining proof and implementation obligations

1. Verify the normative PDF digest by a GovCheck-controlled download, not only by the independent R-128 record.
2. Parse and inventory the informative UML Profile XMI as a distinct source artifact; do not merge it into the normative metamodel XML.
3. Add source-derived UML default/multiplicity interpretation with explicit provenance to the UML semantics used.
4. Prove parser refinement or independently verify the generated structural facts before treating them as formal premises.
5. Build a typed source-view-specific Claim/Assertion mapping that preserves source type, multiplicity, defaulting and provenance; prove each claimed relation.
6. Add separate typed mappings for AssertedEvidence, AssertedRelationship, SACMElement, packages, model inheritance and Rule; preserve unresolved/contradictory facts as non-operative proposals.
7. Keep SACM 2.3 as the formal conformance baseline. SACM 2.4 Beta 1 remains research input; no 2.4 conformance or normative adoption is claimed.

Issue #73 remains open. This report and its Lean fragment model are an engineering/research increment, not an authority decision.
