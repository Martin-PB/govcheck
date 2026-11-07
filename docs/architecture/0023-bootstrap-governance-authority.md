# 0023 — Bootstrap governance authority decision

**Status:** decision recorded from the project owner's explicit instruction on 2026-11-07; proposed for adoption through this pull request. It does not claim that an authority registry or enforcement engine is implemented.  
**Scope:** GovCheck's canonical governance authority.

## 1. Decision

For the current governance regime, exactly one principal holds the authority to adopt, amend, suspend and supersede the canonical governance model and its normative policies.

The principal is the project owner, identified in this repository's governance records by the stable principal identifier `Martin-PB`. This is an explicit project decision, not an inference from GitHub repository ownership, administrator privileges, commit authorship, CI status or pull-request merge rights.

No committee, maintainer group, reviewer or delegated actor shares this root authority under the current regime.

## 2. Self-amendment

The sole authority may itself amend the authority model, including:

- changing the identity of the sole authority holder;
- introducing or removing delegated authorities;
- changing the permitted scope or powers of delegates;
- introducing collective or multi-party approval;
- changing succession, suspension or revocation rules.

Such a change must be an explicit, attributable, versioned governance decision. It takes effect prospectively from its recorded effective point. It must not silently rewrite the authority basis of earlier decisions or retroactively validate decisions that were unauthorized when made.

A change to the authority model is not valid merely because it appears in a merged pull request. The decision record must identify the approving principal and the exact prior governance revision under which that principal acted.

## 3. Operational consequences

Until a later explicit decision changes this regime:

1. Only principal `Martin-PB` may adopt or amend canonical governance policy.
2. Repository collaborators may propose changes and provide technical review, but cannot authorize normative adoption.
3. Pull-request approval, merge permission, repository administration, green CI and code ownership are not substitutes for the governance decision.
4. Delegation is absent by default. A delegate has no authority unless a versioned decision explicitly grants a bounded scope and action set.
5. Where the authority record is missing, inconsistent, revoked or cannot be resolved, authorization evaluates to `unknown`/blocked, never implicitly approved.
6. Technical review may be requested as an assurance measure, but it does not transfer or share the final normative authority.

## 4. Separation of duties

The current single-authority regime cannot provide two-person authorization for adoption: the same principal may propose and authorize a governance change.

This is an explicit governance choice, not a property to disguise as independent approval. Controls should therefore distinguish:

- **normative authorization:** the decision of the sole authority;
- **technical assessment:** automated validation and optional independent review;
- **execution:** publication or application of the already authorized revision.

For changes where the sole authority is also the proposer, the system must record that self-authorization occurred under this regime. It must not report that a distinct-person approval or independent authorization invariant was satisfied.

## 5. Integrity and temporal rules

The future authority registry and evaluator must enforce:

- stable principal identifiers, not display names;
- immutable decision and policy revisions;
- explicit effective times/sequence positions and supersession links;
- no retroactive authority grants;
- no implicit delegation or privilege escalation;
- fail-closed handling of ambiguous, missing or conflicting authority records;
- a complete audit trail for authority changes.

A future delegation may grant only the explicitly listed actions and scopes, must have a validity interval, and must be revocable. Delegation cannot exceed the grantor's own authority or outlive its validity.

## 6. Recovery and compromise limitation

A single root authority creates a single point of compromise and availability failure. The current decision accepts that trade-off for the initial regime; it does not solve account compromise, key loss, incapacity or succession.

Those concerns must be addressed by a separately approved, explicit amendment (for example, a recovery mechanism or a transition to multi-party authority). No recovery principal is silently implied by repository administration or hosting-provider controls.

## 7. Formalization work

The initial bounded authority-transition model is provided in `formal/tla/GovCheckAuthority.tla` with `formal/tla/GovCheckAuthority.cfg`. It checks that each amendment is authorized by the immediately preceding authority, that the authority/revision chain remains continuous, and that the current authority/revision match the last recorded decision. It deliberately does not yet model delegated authorities, exception lifecycles, cryptographic identity, wall-clock validity or integration with the version-decision validator. The governance lifecycle model and conformance tests should additionally represent:

- one configured root principal;
- adoption/amendment by that principal only;
- an explicit self-amendment transition for changing the authority regime;
- prospective effect and preservation of prior decision validity;
- absence of delegates unless explicitly granted;
- fail-closed behavior for unknown or revoked authority;
- explicit recording that proposer and authorizer may be the same principal under this regime.

This decision establishes the governance rule to model. It does not claim those checks are already implemented or verified.

## 8. Source

Explicit instruction from the project owner in the GovCheck governance discussion, 2026-11-07: “Pour l'instant, moi seul et je pourrai donc moi-même faire évoluer cette autorité.”

