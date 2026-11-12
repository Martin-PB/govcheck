# ADR 0009 — Repository intent record and canonical naming

- **Status:** Adopted by the repository owner on 2026-11-10.
- **Decision scope:** GovCheck's own repository intent record and the canonical intent artifact expected by a GovCheck-governed repository.
- **Supersedes:** none.
- **References:** [R-114](../references.md#r-114), [R-115](../references.md#r-115), [R-116](../references.md#r-116), [R-117](../references.md#r-117), [R-118](../references.md#r-118), [R-119](../references.md#r-119), [R-120](../references.md#r-120), [R-121](../references.md#r-121), [R-122](../references.md#r-122).

## Context

GovCheck needs a durable, human- and agent-readable record of the repository's purpose, intended outcomes, operating context, boundaries, constraints and unresolved questions. This record must remain distinct from requirements, architecture decisions, specifications, implementation plans and assurance evidence.

The name `product-intent.md` was initially used in a working branch. The repository owner requested investigation of existing academic and industrial conventions before adopting a canonical name. The comparison identified Anthropic's documented `intent.md` practice as the closest conceptual and naming precedent. The owner explicitly approved `intent.md` for GovCheck on 2026-11-10.

## Decision

1. The canonical artifact name is **`intent.md`**, in lowercase.
2. In GovCheck's documentation tree, the English canonical file is **`docs/intent.md`** and its maintained French counterpart is **`docs/intent.fr.md`**.
3. A GovCheck-governed repository must represent its repository-level intent as a first-class governance artifact. Its canonical filename is `intent.md`; the repository's governed layout places it at `docs/intent.md` unless a separately recorded structural constraint requires a different location.
4. The intent record states why the repository exists, the context and boundaries in which it operates, the stakeholders/users or beneficiaries, the problems or needs it addresses, intended outcomes, constraints, assumptions and open questions. Its level of detail is proportionate to the repository, but its existence and identity are not optional.
5. GovCheck adopts the **naming and broad conceptual practice** documented by Anthropic's AI-native SDLC Playbook as an inspiration. This is not a claim that Anthropic publishes a universal normative file standard, nor that GovCheck conforms to an Anthropic schema.
6. GovCheck does **not** adopt the IntentDocs `INTENT.md` format or claim compatibility with it. That published format combines product overview, personas, releases, stories and acceptance criteria in ways that would collapse distinctions GovCheck deliberately preserves.
7. The intent is an upstream design-direction artifact, not itself a complete normative policy, adopted requirement set, executable governance model, architecture decision, implementation contract or assurance case. Derived objectives, requirements, constraints, properties, decisions, specifications and assurance obligations retain their own identities, statuses, authority and traceability.
8. The intent-to-derived-artifact relationships are not fully specified by this ADR. Their metamodel, relation types, cardinalities, temporal semantics, completeness rules and validation properties require separate research and design. This ADR does not adopt a linear lifecycle chain.

## Consequences

- The current working files are renamed to `docs/intent.md`, `docs/intent.fr.md`, `docs/intent-impact-analysis.md` and `docs/intent-impact-analysis.fr.md`.
- References, README indexes and architecture indexes use the canonical names.
- The reference catalogue records the external academic, standards and industry sources informing this decision, including their status and limitations.
- Bootstrap, migration and conformance mechanisms must eventually create, preserve and validate the intent artifact; this ADR does not claim those mechanisms are implemented.
- A concise intent is valid for a small repository; absence is not equivalent to a concise record.
- The impact analysis remains a working audit and does not itself adopt the candidate relationship model.

## Rejected alternatives

- **`product-intent.md`:** unnecessarily narrows the concept to a product and introduces a new compound convention without need.
- **`INTENT.md` as defined by IntentDocs:** a published open format, but its bundled structure is not GovCheck's intended semantic separation. GovCheck makes no compatibility claim.
- **A freely chosen filename per repository:** weakens discoverability, consistent tooling and interoperability.
- **A root-only location:** the current GovCheck documentation organization uses `docs/`; the canonical location is therefore `docs/intent.md`, with any future repository-layout profile requiring an explicit rule rather than ad hoc naming.

## Review and change

Changes to the canonical name or semantic role require an explicit decision by the competent GovCheck authority. Changes to an individual repository's intent are governed changes to that record; they do not silently amend existing decisions or requirements.

The relationship metamodel is intentionally deferred to a separate, research-backed architecture/specification effort.
