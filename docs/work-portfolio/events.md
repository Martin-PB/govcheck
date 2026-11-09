# Portfolio event journal

**Policy:** append-only. This is a logical journal, not a tamper-proof storage mechanism. Never edit or delete an earlier event; corrections are new events.

## WP-EVT-000001 — Initial issue-to-registry import

- **Subject:** govcheck.work-portfolio
- **Event type:** initial-import
- **Recorded:** 2026-11-09
- **Actor/provenance:** maintainer-directed repository migration, prepared by an automated assistant through the GitHub repository integration.
- **Base:** main at 93024d4d0e61a9dcac93510cd607098094e12238.
- **Candidate:** branch work/governed-work-portfolio-registry; exact resulting commit is preserved by the PR and repository history.
- **Scope:** create the repository-backed portfolio; map issues #33, #41–#77 and #86 where relevant; preserve issue numbers as adapter provenance; retain open issues during transition; delete no source discussions.
- **Disposition:** candidate import for maintainer review. This event does not authorize execution of imported work and does not adopt Architecture 0028 before the required governance decision.
- **Rationale:** GitHub issues are forge-specific mutable coordination records. The repository needs a forge-independent, revision-addressable portfolio and must not rely on issue-editor discipline to preserve prior accepted states.
- **Related records:** README.md, work-items.md, Architecture 0028 and Specification 0003.
- **Known limitations:** no machine-enforced append-only storage, independent backup, signature policy, automatic adapter synchronization or local edit interception is implemented by this migration.

 
## WP-EVT-000002 — Adapter pointers and migration cross-references updated

- **Subject:** govcheck.work-portfolio
- **Event type:** adapter-mapping-updated
- **Recorded:** 2026-11-09
- **Actor/provenance:** maintainer-directed migration, prepared by an automated assistant through the GitHub repository integration.
- **Base:** main at 90f155489e2ff0138e0270e181f509d72124429b (the branch was synchronized with this mainline before final review).
- **Candidate:** current head of work/governed-work-portfolio-registry; see PR #89 for the exact candidate revision.
- **Scope:** prepend canonical registry pointers to GitHub issues #40 and #78–#85 without deleting their existing bodies; map atomic issue #33 to its stable work ID; record #46 as completed pending closure after registry acceptance; link #75 to the pending adoption proposal.
- **Disposition:** adapter updates only. All referenced issues remain open. No issue closure, work authorization or Architecture 0028 adoption is implied.
- **Rationale:** make the transition discoverable while preserving the existing GitHub coordination dossiers and their histories.
- **Related records:** PR #89; work-items.md; README.md; Architecture 0030.
- **Known limitations:** issue edits are still performed through GitHub's native mutable API; no automatic synchronization, tamper-proof issue history or registry enforcement is claimed.


## WP-EVT-000003 — Governance revision applicability specification and model prepared

- **Subject:** govcheck.work.governance-revision-temporal-applicability
- **Event type:** specification-and-model-prepared
- **Recorded:** 2026-11-09
- **Actor/provenance:** maintainer instruction to proceed with the #86 work item; technical artifacts prepared by an automated assistant through the GitHub repository integration.
- **Base:** main after merge of PR #89; exact branch base is recorded in the pull request comparison.
- **Candidate:** branch work/governance-revision-applicability; exact commits are preserved by branch and PR history.
- **Scope:** add Specification 0006 in English/French; refine Specification 0003; add a separate bounded governance-applicability TLA+ module/configuration; add the reusable package counterpart; integrate catalogue backlinks, indexes and scoped TLC workflow.
- **Disposition:** proposed technical contract and model for review. This event does not adopt the specification, amend Architecture 0023, or authorize a governance regime change. Decision #41 remains reserved to the designated authority.
- **Rationale:** the existing authority and lifecycle models did not bind a decision position to the unique governance revision effective at that position. The new model isolates this missing temporal applicability contract without claiming that either existing model already provides it.
- **Related records:** Issues #41 and #86; Specification 0006; formal/tla/GovCheckGovernanceApplicability.tla; Architecture 0023; PR for work/governance-revision-applicability.
- **Known limitations:** TLC has not yet been executed for this candidate; the model is finite and does not establish cryptographic identity, distributed consensus, implementation refinement, complete multi-writer concurrency, delegation or forge enforcement.
