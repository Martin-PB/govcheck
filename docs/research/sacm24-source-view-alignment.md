# SACM 2.4 Beta 1 — source-view alignment and conflict register

**Status:** revision-pinned comparison of two distinct normative source views; no precedence decision, canonicalized model, SACM conformance claim or GovCheck semantic mapping is established.  
**Work item:** [#73 — inter-model contract conformance](https://github.com/Martin-PB/govcheck/issues/73).  
**Metamodel source:** [R-197](../references.md#r-197), [source-derived XMI inventory](sacm-xmi-structural-inventory.md).  
**Specification text source:** [R-198](../references.md#r-198).  
**Independent discrepancy audit:** [R-128](../references.md#r-128).  
**Formal transcription:** `formal/lean/GovCheckCoherence/SACM24.lean`, namespace `GovCheck.Coherence.SACM24.SourceFacts`.

## 1. Scope and source identity

The OMG catalogue lists the SACM 2.4 Beta 1 specification PDF as a **normative document** (file ID `ptc/26-06-34`) and the machine-readable metamodel XML as a **normative machine-readable document** (file ID `ptc/26-05-28`). They are separate artifacts and separate source views, not two serializations that may be silently merged. The catalogue also lists an **informative UML Profile XMI** ([R-199](../references.md#r-199)); it is intentionally excluded from this normative PDF/XML comparison and remains a third, separately scoped source view.

| Source view | OMG file ID | Official URL | SHA-256 | Current GovCheck status |
|---|---|---|---|---|
| Specification text, figures and annexes (PDF) | `ptc/26-06-34` | <https://www.omg.org/spec/SACM/2.4/Beta1/PDF> | `25f32d1cd4bf32dfa9c92c7c1840e1a113b1e91c0e97252f6551878c39997ff5` | GovCheck-verified by workflow run [43495625975](https://github.com/Martin-PB/govcheck/actions/runs/43495625975); 9,019,601 bytes; retained in artifact [14071287095](https://github.com/Martin-PB/govcheck/actions/runs/43495625975/artifacts/14071287095) |
| Machine-readable metamodel (XML) | `ptc/26-05-28` | <https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml> | `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830` | Independently downloaded, digest-verified by GovCheck; 524,243 bytes |

The PDF digest reported by R-128 was independently recomputed by GovCheck against the official PDF download in workflow run [43495625975](https://github.com/Martin-PB/govcheck/actions/runs/43495625975): 9,019,601 bytes and the exact SHA-256 above. The 90-day artifact [14071287095](https://github.com/Martin-PB/govcheck/actions/runs/43495625975/artifacts/14071287095) contains the PDF, exact XML, source-view manifest and generated XMI inventory. The workflow does not extract or interpret PDF text automatically.

SACM 2.4 Beta 1 remains an in-process/informational version; SACM 2.3 remains the formal version. The fact that both PDF and XML are catalogued as normative artifacts does not settle contradictions between them.

## 2. Conflict register

The 12 comparison entries comprise 11 currently modelled source-fragment differences/additions and one unresolved R-128 audit discrepancy (`Claim.value`). The informative PDF Figure 15.1.1 is not a substitute for verifying the exact normative Clause 13.9 passage. The table records claims at their actual source-fragment granularity. “Not stated in PDF text” is deliberately not treated as “forbidden by the PDF”: diagrams, annexes or other fragments may add information.

| Topic | PDF source fragment | Metamodel XML source view | Classification | Lean source-fact theorem(s) |
|---|---|---|---|---|
| Element identity | Clause 9.2 uses `gid : String[0..1]`; Figure 9.1 labels `elementId` | `elementId : UID[1]`; no `gid` | **Conflict inside the PDF and between PDF fragments and XML.** A document-wide PDF identity rule is unsound. | `pdf_identity_fragments_disagree`; `pdf_clause9_2_uses_gid`; `pdf_figure9_1_uses_elementId`; `xml_model_uses_elementId` |
| Assertion declaration literals | Clause 13.6 lists `axiomatic`, `assumed`, `asserted`, `needsSupport`; Annex G.6 item 6 lists three literals; Clause 15.2.1 includes `byRule` | `axiomatic`, `assumed`, `asserted`, `byRule` | **Conflict inside the PDF**; the XML agrees with Clause 15.2.1 on `byRule`, but not with Clause 13.6. | `pdf_assertion_declaration_fragments_disagree`; fragment literal theorems |
| `Claim.value` | R-128 reports Clause 13.9 as `MultiLangString`; informative Figure 15.1.1 (printed p.59) shows `ExpressionLangString` | `ExpressionLangString` | **Unresolved audit discrepancy, not an established conflict.** The inspected informative figure agrees with the XML, but does not settle the cited normative Clause 13.9 passage. Keep the R-128 report as an unverified claim until that exact passage is located and checked. | `claim_value_type_agrees_in_informative_pdf_figure15_1_1_and_xml`; `r128_reported_claim_value_type_differs_from_informative_pdf_figure` |
| `AssertedEvidence.evidence` | Clause 13.13: `[0..*]` | `[1..*]` | **Multiplicity conflict.** Empty evidence collections differ in admissibility. | `asserted_evidence_multiplicity_conflict` |
| `BindingPackage` inheritance | Clauses 10.5 and 11.3 give different superclass statements | `ScopedPackage` and `SACMPackageWithBinding` | **Conflict inside the PDF**; XML matches Clause 10.5, not Clause 11.3. | `binding_package_pdf_fragments_conflict`; `xml_binding_package_matches_pdf_clause10_5` |
| `SACMElement.abstraction` | Clause 9.2: `[0..1]` | `[0..*]` | **Multiplicity conflict.** | `sacm_element_abstraction_multiplicity_conflict` |
| `AssertedRelationship.isCounter` | Clause 13.11: `Boolean[1]` | `Boolean[0..1]` | **Multiplicity/requiredness conflict.** | `asserted_relationship_isCounter_multiplicity_conflict` |
| `SACMModel` inheritance | Clause 9.10: `ModelElement`; Annex G.6 item 5 adds `Assertion` and `Assessment` | `ModelElement`, `Assertion`, `Assessment` | **Conflict inside the PDF**; XML matches the annex fragment. | `sacm_model_pdf_fragments_differ`; `xml_sacm_model_matches_pdf_annex_g6` |
| `SACMDependency` inheritance | Clause 9.11: `DirectedRelationship` | XML also declares `BaseElement` | **XML addition relative to the cited PDF clause**, not proof that the PDF globally forbids it. | `sacm_dependency_xml_adds_base_element` |
| `Rule` inheritance | Clause 15.2.3: `BaseElement` | XML declares `ModelElement` and `BaseElement` | **XML addition relative to the cited PDF clause.** | `rule_xml_adds_model_element` |
| Assertion-rule feature name | PDF uses `assertionRule` | XML uses `assertionDeclarationRule` | **Feature-name divergence.** A rename mapping needs an explicit contract. | `assertion_rule_feature_name_differs` |
| `Claim.subject` and `Claim.whole` | Not stated in the inspected PDF text view | XML declares multi-valued properties | **Unstated-versus-present**, not an established contradiction. The PDF text omission does not prove absence from all figures/annexes. | `claim_subject_is_xml_addition_over_pdf_text`; `claim_whole_is_xml_addition_over_pdf_text` |

The register preserves the R-128 audit's findings while adding fragment-level distinctions already represented in Lean. The table is a comparison record, not an OMG errata determination. Exact PDF fragment transcription remains a reviewable evidence task; the digest authenticates bytes, not the correctness of a human transcription.

## 3. Formalization boundary

The Lean module separates:
- document-level `SourceView` values (specification text/PDF versus normative metamodel XML);
- `DeclarationSourceFragment` values for PDF Clause 13.6, Annex G.6 item 6, Clause 15.2.1 and the XML;
- `IdentitySourceFragment` values for PDF Clause 9.2, Figure 9.1 and the XML.

A `SACMClaimInterpretation` must bind its declaration and identity fragments to the selected document view, preserve the exact source fields, and retain the source model revision. This prevents a PDF-wide identity field or declaration set from being assumed where the PDF itself contains incompatible fragments.

The `SourceFacts` theorems prove that the **transcribed constants** differ or agree as stated. They do not prove that the transcription faithfully represents the PDF/XML. The proof kernel verifies the Lean derivations from those constants; it does not authenticate the source citations. The updated axiom report explicitly audits the source-fact theorems, but that audit is still pending the PR workflow.

## 4. Handling rules for the current integration

1. Preserve PDF and XML as distinct, independently identified source artifacts.
2. Attach every claim to a specific clause, figure, annex item or XML metaclass/property, not only to a document label.
3. Represent disagreement as a first-class conflict with both source values, locators, revisions and provenance.
4. Do not select a winning source, repair an OMG artifact, or normalize the values without an explicit authorized decision.
5. Do not treat absence from a text passage as proof of absence from the complete PDF.
6. Keep mappings partial and source-view-qualified. A mapping that depends on a disputed fact cannot become an established premise until its exact semantic relation is proved.
7. Keep SACM 2.3 as the formal conformance baseline. Do not advertise SACM 2.4 Beta 1 instance import/export or conformance.

## 5. Verification and remaining limits

The XML capture and structural inventory are independently workflow-verified (12 Python tests; official XML digest; generated inventory compared with the committed summary; raw source and full inventory published). The PDF download and SHA-256 check also passed against R-128's pinned value; the manifest records both source identities, hashes and byte lengths, and the combined source artifact was published. Lean 4.19.0 compiled the fragment-qualified source model in [run 43495626076](https://github.com/Martin-PB/govcheck/actions/runs/43495626076) on merge candidate `c6029f9`; the axiom audit covered 43 declarations under GovCheckCoherence.Proofs, all within the configured allowlist (four source-fragment wrapper theorems use propext; no unapproved axiom was reported). The directly printed SourceFacts theorems do not depend on axioms.

Still not demonstrated:
- correctness/completeness of the PDF-to-Lean and XML-to-Lean transcriptions;
- full UML/MOF semantics or parser refinement from XML infoset to a formal source model;
- source-derived semantic correspondence to the GovCheck metamodel;
- resolution/precedence of the source conflicts;
- instance interchange, round-trip behavior or SACM 2.4 conformance.

No normative adoption is proposed by this research increment. Issue #73 remains open.
