# ADR 0007 — Mandatory sources for decisions and attestations

**Status:** adopted by the repository owner on 2026-11-10. **French:** [0007 (français)](0007-mandatory-sources.fr.md).

## Context

Agents can state decisions, reviews or claims without evidence. The reference catalogue (docs/references.md / docs/references.fr.md) already indexes external sources as R-xx anchors with backlinks, and scripts/check-reference-integrity.py enforces catalogue integrity, but nothing forced a decision document to cite any source: an ADR could satisfy bilingual-decisions and reference-integrity while containing zero references. Issue #33 sets the research rule (blogs and wikis are leads only; academic sources and standards are evidence); issues #72, #74 and #77 track the adversarial corpus, the reference status semantics and the justification requirement. Together they motivate making sources mandatory rather than advisory.

## Decision

Add a decidable `sources-present` rule to `govcheck/check.py` (slice 0.3.0):

1. Every non-guide `docs/decisions/*.md` must contain a `## References` / `## Bibliographic references` / `## Références` / `## Références bibliographiques` heading followed, before the next `##` heading, by at least one source link: a reference-catalogue anchor (`references(.fr)?.md#r-xx`) or an external `http(s)://` URL. Guide files (`README*`, `TEMPLATE*`) are exempt.
2. Every attestation record in `docs/attestations/*.json` must carry a non-empty `sources` list of strings: the evidence the reviewer relied on.
3. The rule is decidable and fail-closed: missing or empty sources are `fail`. When no decision documents and no attestation records exist, the rule is not applicable.

The `govcheck/decisions/TEMPLATE*` files gain a References placeholder so target repositories start compliant. ADR 0006 (branch docs/adr-0006-vcs-forge-portability, PR #93) had its sources catalogued as R-109–R-113 when it was written, which is exactly the behaviour this rule now enforces.

## Consequences

- `govcheck check` now rejects unsourced decisions offline, in CI and in any target repository bootstrapped with the package.
- Agents must cite catalogue anchors (preferred: keeps the single external-URL index) or explicit URLs; raw URLs left in decision documents are warned about by the reference-integrity tooling and should be catalogued.
- Existing decisions ADR 0001–0005 already carry references and remain compliant.

## Out of scope

- Checking that a cited source actually supports the claim (semantic adequacy is human review, recorded through attestations).
- Cryptographic signing of attestations or sources.
- Retroactive re-audit of architecture records.

## References

- [R-03 — GitHub protected branches and required status checks](../references.md#r-03)
- [R-06 — in-toto: software supply-chain integrity](../references.md#r-06)
- [R-24 — W3C PROV-O](../references.md#r-24)
- [Reference catalogue integrity](reference-integrity.md)
- [ADR 0002 — study placement](0002-study-placement.md)
- Issues #33 (research rule), #72 (adversarial corpus), #74 (reference status), #77 (justification)
