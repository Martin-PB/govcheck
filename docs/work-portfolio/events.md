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
