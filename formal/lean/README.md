# Lean coherence prototype

**Status:** experimental first slice; not an adopted GovCheck metamodel.

## Scope

This package formalizes the first evidence-coherence invariants and a proof-carrying cross-model mapping contract. It keeps `EvidenceMethodClass`, `EvidenceKind` and `EvidenceStatus` as separate dimensions. The
Lean vocabulary mirrors the existing GovCheck evidence schema's
`methodClass` values and result-status values, while keeping the epistemic
kind explicit and separate.

This distinction matters: a record labelled with method class
`theorem-proving` and status `passed` is not, by those labels alone, an
authenticated kernel-checked derivation. A test execution with status
`passed` remains testimony; a model-checking result remains model-checking
evidence. Freshness/staleness is computed separately and is not conflated
with the source schema's result status. The source schema's method-class
vocabulary is represented directly by `EvidenceMethodClass`; the epistemic
kind is an additional assurance interpretation, not a replacement enum.

The first module deliberately imports no CSLib modules. This isolates the
proposition and gives us a baseline against which candidate CSLib definitions
can later be compared. It does **not** imply that CSLib is unsuitable or that
the assurance obligation for critical mappings is optional.

The Lean `EvidenceKind` is an additional semantic interpretation: the current
production `evidence-record.schema.json` has `method.methodClass` and
`result.status`, but no explicit epistemic-kind field or typed kernel-checked
derivation object. Therefore the Lean record is not a lossless projection of
the current JSON schema. The fixtures under `fixtures/` are intentionally
minimal semantic fixtures, **not** full production records valid against the
JSON Schema. The theorem `schema_method_and_status_do_not_determine_epistemic_kind`
constructs two semantic interpretations with identical method class and
status but different epistemic kinds; this is a formal counterexample to
inferring epistemic kind from the current schema dimensions. See the bilingual
prototype contract for this identified #73/#79 decision gap.

## Toolchain and commands

Pinned toolchain: Lean 4.19.0.

From this directory:

```sh
lake env lean GovCheckCoherence.lean
lake build
```

## SACM 2.4 Beta 1 semantic slice

`GovCheckCoherence.SACM24` preserves SACM assertion-declaration distinctions, binds explicit Claim subjects to exact model revisions, and types inference direction. The `probable` inference kind has no classical implication bridge; `byRule` requires a concrete proof term. The source-view guards for PDF text versus metamodel XML, including `needsSupport`/`byRule` and `gid`/`elementId`, passed the same axiom audit. See the [SACM Beta 1 interoperability-risk report](../../docs/research/sacm24-beta1-interoperability-risk.md). The thirteen public SACM mapping theorems passed the pinned Lean 4.19.0 build and axiom audit in [run 43216879988](https://github.com/Martin-PB/govcheck/actions/runs/43216879988) with no axioms. See the bilingual [SACM 2.4 mapping study](../../docs/research/sacm24-claim-inference-mapping.md) / [étude française](../../docs/research/sacm24-claim-inference-mapping.fr.md).


## UML 2.5 multiplicity semantics

`GovCheckCoherence.UML25Multiplicity` formalizes a deliberately narrow subset of the UML 2.5 rules used by the SACM 2.4 Beta 1 XMI source. It proves the fallback to 1 for absent/null lower/upper value specifications, the default 0 for an omitted `LiteralInteger.value` or `LiteralUnlimitedNatural.value`, preservation of an explicit unlimited upper bound, and non-interpretation of unsupported value specifications. The exact source clauses are catalogued in [R-200](../../docs/references.md#r-200).

`GovCheckCoherence.SACM24.SourceFacts` then records seven manually transcribed XML value-specification shapes and proves that this UML 2.5 interpreter yields the corresponding SACM property intervals. This does not prove that the Python XMI parser extracted those shapes correctly; that parser/source refinement obligation remains open. The implementation and generated inventory summary are versioned as inventory v2.

## Mapping contract

The status model also proves `unknown_status_is_distinct_from_inconclusive`; both statuses are represented in the JSON Schema, while staleness remains a separate freshness property.

`GovCheckCoherence.Mapping` binds a source and target claim identifier to Lean propositions. Its operative coverage is restricted to `equivalent`, `soundDirectional` and `partialMapping`; each `SemanticBridge` constructor carries the corresponding proof obligation. Approximate, traceability-only and unsupported candidates use the separate `MappingProposal` type. A proposal has no semantic bridge and cannot inhabit `EvidenceMapping`, so it cannot be consumed by the current typed mapping interface as an established semantic premise.

An operative mapping also binds exact source/target model revisions and requires preservation of the evidence source identity/revision, exact scope, all source assumptions, and method class. A target theorem-proof kind can only be introduced through `KindMappingRule.deriveTheoremProof`, which contains an actual Lean proof term of the exact target proposition. The generic transport constructor explicitly excludes `theoremProof`; even an existing source theorem-proof label is not enough to carry that status to a target. Target result status remains independent: a new theorem derivation has its own result, not an automatic copy of a source test status.

The first profile requires exact scope equality; it does not yet define a scope partial order or safe scope narrowing. The `premises`, `assumptions`, `kernelIdentity` and `kernelVersion` fields on `KernelCheckedDerivation` remain provenance metadata and are not yet mechanically linked to the proof term's complete dependency closure. The contract is a typed obligation, not proof that any production importer/exporter satisfies it.

## Explicit limits

This is not yet a complete metamodel coherence proof. In particular, it does
not prove that a production importer/exporter constructs valid mapping values,
that a source-native SACM/OWL/SEON interpretation is correctly bound to the
Lean propositions, that mappings compose conservatively, or that an external
implementation refines the formal contract. Freshness and temporal authority
remain governed by the repository's TLA+ models and require a separate
conformance argument.

The proof term is checked by the pinned Lean kernel, but the `premises`,
`assumptions`, `kernelIdentity` and `kernelVersion` fields are provenance
metadata and are not yet mechanically linked to the proof term's complete
dependency closure. Claim identifiers are paired with Lean propositions in
the mapping subject, but no production parser has yet been proven to preserve
that binding. Approximate, traceability-only and unsupported candidates are
non-operative `MappingProposal` values; they do not carry a semantic proof.

## Verification status

The tightened mapping API was built and axiom-audited successfully with the
pinned Lean 4.19.0 toolchain in [workflow run 43437994055](https://github.com/Martin-PB/govcheck/actions/runs/43437994055),
on formal source revision `6580daaeef6c506b0a2da30c790cac43481a15f3`.
The workflow built `GovCheckCoherence`, audited 36 declarations under
`GovCheckCoherence.Proofs` (all within the configured allowlist
`propext`, `Classical.choice`, `Quot.sound`), and the explicit
`#print axioms` report found no axioms for the listed theorem declarations.
The artifact catalogue records this exact checked revision and workflow run.

The result applies to the exact formal source revision above. Subsequent
documentation/portfolio commits do not change the checked Lean source blobs.
This is a result about the small formal slice only: it is not a semantic
mapping proof against SACM/OWL/SEON, proof of imported-source fidelity,
mapping-composition proof, or implementation conformance. A successful Git
commit or a historical green run is not a Lean verification result for a
different formal source revision.
