# Temporary bootstrap governance

**Status: accepted as a temporary, human-reviewed policy for the initial bootstrap only.** This is not the final canonical governance model and is not mechanically enforced.

Until a canonical machine-readable model and evaluator exist, substantive changes require maintainer review. Contributors must inspect the repository and relevant decisions, state intended outcomes and risks, preserve existing content, keep changes focused, run relevant local checks where available, and report the exact revision assessed. Never claim checks that were not run. Do not trigger GitHub Actions or other hosted CI without explicit authorization. Architecture decisions require paired English/French ADRs, English first/default.

Explicit maintainer review is required for changes to product scope, normative authority, assurance semantics, VCS/hosting/collaboration/acceptance boundaries, security boundaries, mandatory dependencies, implementation language, formal kernel, data format, or license.

## Limitations

There is no executable, machine-enforced canonical policy, formal proof, model-checking result, forge enforcement, or local VCS enforcement yet. This temporary process relies on human review and repository history. Do not present it as stronger than it is.

## Exit criteria

Replace this policy only when a reviewed implementation provides a versioned canonical model; defined semantics for obligations, permissions, prohibitions, exceptions, and lifecycle transitions; a deterministic local evaluator; assurance records bound to exact repository and governance states; documented verification and trust boundaries; and a history-preserving migration.

French: [BOOTSTRAP_GOVERNANCE.fr.md](BOOTSTRAP_GOVERNANCE.fr.md).