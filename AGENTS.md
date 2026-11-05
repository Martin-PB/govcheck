# Coding-agent instructions

These bootstrap instructions guide contributors; they do not claim that enforcement is already implemented.

1. Govern the repository and its change lifecycle. Do not turn GovCheck into an agent sandbox or tool-call gateway.
2. Do not introduce a mandatory hosted service, daemon, or MCP server. The intended primary interface is a small local executable.
3. Formal governance and assurance foundations apply to every repository size; do not create assurance tiers.
4. Treat Git and Pijul as first-class, semantically distinct VCSs. Preserve Pijul patches, dependencies, channels, and conflicts natively.
5. Separate VCS, hosting, collaboration, and acceptance. Local-only and team-hosted use are in scope.
6. Do not assume a language, CI provider, build system, or package manager. Do not trigger hosted CI without explicit maintainer authorization.
7. Prefer a small core, declarative profiles, and narrow adapters over a dynamic plugin framework or large mandatory dependency stack.
8. Never claim a check, model check, proof, or conformance result ran without evidence of execution and scope.
9. The future machine-readable canonical governance model is the normative authority. Markdown must not silently become a competing authority.
10. Follow the temporary policy in docs/BOOTSTRAP_GOVERNANCE.md until the canonical engine replaces it.

## Bootstrap discipline

Inspect before planning; plan before applying. Preserve existing content. Record architecture decisions as ADRs with English as default and a French counterpart. Do not select implementation language, formal kernel, data format, license, or mandatory dependencies without an explicit reviewed decision. Report files changed, rationale, checks actually run, checks not run, and remaining decisions.

French: [AGENTS.fr.md](AGENTS.fr.md).