# Architecture 0033 — Governance evaluator, exception and revocation control model

**Status:** recorded finite model-checking evidence for a bounded TLA+ control abstraction. This record is not normative adoption, implementation evidence, or proof of production enforcement.

## 1. Subject and purpose

This record documents the bounded control model [GovCheckGovernanceControls](../../formal/tla/GovCheckGovernanceControls.tla), introduced to formalize selected outcomes from the owner-authorized arbitration session 0008. It complements the canonical publication model in Architecture 0032; it does not replace it.

The model covers five control concerns:

1. the evaluator recognized under the prior governance revision remains the sole authoritative evaluator; a proposed replacement can only produce comparative shadow results;
2. evaluation outcomes remain distinct: `Pass`, `Fail`, `Unknown`, and `Conflict`; unknown and conflict block authorization;
3. explicit exceptions are justified, time-bounded, revocable, restricted to waivable requirements, and revalidated at publication; non-derogable requirements cannot be excepted;
4. authority revocation takes effect prospectively and blocks subsequent publication without deleting prior decisions;
5. historical requalification is represented as a separate append-only record referring to the original decision.

Evaluation, authorization and publication remain distinct logical acts in the underlying canonical-publication model. This model does not collapse them into one normative act.

## 2. Exact model and configuration

- **TLA+ module:** `formal/tla/GovCheckGovernanceControls.tla`
- **TLC configuration:** `formal/tla/GovCheckGovernanceControls.cfg`
- **Git blob — module:** `b237fa3bc939c711f0510c4aeca1346c8e50264f`
- **Git blob — configuration:** `9e8f48d409eeb31adaf22890bbb8ff90674aa96a`
- **Checked PR head:** `01d9f0e4147d50a1daaa3ca03487c0be22770c7b`
- **CI merge checkout:** `41d61b314e81c433e7d5337408d67bd7af703d50`
- **TLC workflow run:** [42826055617](https://github.com/Martin-PB/govcheck/actions/runs/42826055617)
- **TLC job:** `129863528869`
- **TLA tools:** tla2tools v1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`
- **SANY:** 2.1
- **TLC:** 2.19
- **Java:** Temurin 17.0.21+9

## 3. Checked properties

The exact module/configuration passed SANY and TLC. TLC reported:

- **2,826,117** generated states;
- **1,026,484** distinct states;
- **0** states remaining;
- complete state-graph depth **12**;
- no invariant or temporal-property violation.

The nine configured invariants passed:

1. `TypeOK` — state variables remain within the configured finite types;
2. `UniquePublishedRevisions` — publication records do not reuse a published revision identity;
3. `PublicationUsesPriorAuthority` — the authorization basis and resulting revision are distinct;
4. `ShadowCannotAuthorize` — authoritative evaluations identify the prior evaluator;
5. `UnknownAndConflictBlock` — neither unknown nor conflict can support an authorization;
6. `NonDerogableNeverExcepted` — an active exception cannot target a non-derogable requirement;
7. `RevocationIsProspective` — a revocation is associated with a later logical position;
8. `HistoricalDecisionsPreserved` — requalification records continue to refer to the original governance decision;
9. `NoStaleAuthorization` — authorization retains the evaluation's captured base identity and position.

The temporal property `AppendOnly` also passed. It checks that the journal, comparative shadow-evaluation history, decision history and requalification history only grow by appending and never rewrite their existing prefixes.

## 4. Deliberate bounds and abstraction limits

This is a finite design model, not a general unbounded protocol proof. Its TLC instance deliberately uses:

- two candidate content values and two governance-revision values;
- one authoritative evaluation identifier and one authorization identifier;
- one exception identifier;
- at most one comparative shadow result and one historical requalification;
- a bounded logical-time progression.

Consequently, this run does **not** establish multi-publication concurrency, a complete rollback sequence, arbitrary evaluator succession, cryptographic identity, delegation, a complete structured risk-acceptance record, real-time expiry, durable journal storage, crash recovery, distributed replica reconciliation, Git/Pijul adapter correctness, or implementation refinement. These remain engineering/formalization obligations tracked by issue #86.

The model's finite state-space result is model-checking evidence for these exact source/configuration identities only. It is not a theorem proof, not evidence that production code refines the model, and not an act of normative adoption. The eleven owner-selected choices remain selected inputs; formal adoption remains exclusively the project owner's authority.

## 5. References

- [R-05 — TLA+ and TLC state-transition modeling](../references.md#r-05)
- [Specification 0006 — governance revision applicability](../specifications/0006-governance-revision-applicability.md)
- [Architecture 0032 — canonical publication model-checking report](0032-canonical-publication-model-checking.md)
- [Decision-session record 0008](../decisions/0008-governance-applicability-arbitration-session.md)
- [Issue #86 — governance applicability engineering obligations](https://github.com/Martin-PB/govcheck/issues/86)
