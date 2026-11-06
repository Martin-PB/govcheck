# 0016 — Source-based assessment of Writ and Privateer

**Status:** bounded source review of the public repositories identified below, using their default-branch state as of 6 November 2026. This is not a security audit, independent reproduction, or adoption decision. **French:** [0016 (français)](0016-writ-privateer-assessment.fr.md).

## 1. Scope and disambiguation

“Writ” is an ambiguous product name. This assessment concerns [`infinri/Writ`](https://github.com/infinri/Writ), described by its repository as a governance runtime for Claude Code. It does not assess the separate products at writ.now, withwrit.com, or usewrit.app.

Privateer here means [`privateer-agent/privateer-agent`](https://github.com/privateer-agent/privateer-agent), a MIT-licensed, provider-agnostic distribution of the Pi coding agent. It does not mean unrelated products sharing the name.

Source snapshots reviewed:
- Writ `main`: `ebdafe5450b201339f81e717ed104e6bcfd3fe3e` (3 November 2026).
- Privateer `main`: `181a988e443fa6b6b4138fc349d1260c96408ad4` (3 November 2026).

This review reads public repository descriptions and selected architecture/security documents. It does not claim to have built, installed, run, fuzzed or independently audited either project.

## 2. Writ: what the source describes

Writ is a local Claude Code-specific workflow-governance runtime. The repository describes Claude Code hooks around tool events, a local daemon, and a Neo4j database storing rules and decision records. It combines rule/context retrieval with code-based workflow gates and decision continuity.

Documented capabilities include:
- workflow modes and phases;
- a plan gate and test-skeleton gate before source writes in work mode;
- human approval represented by a token bound to the pending gate and plan fingerprint;
- write-time checks, credential-path refusals and role/project write scopes;
- rule retrieval, decision recall and session records;
- structured logs/auditing of selected gate events.

These are useful **agent-workflow and action-gating** capabilities. They are not the same as GovCheck's canonical repository governance model, change dossier, native Git/Pijul semantics, assurance case or exact-candidate acceptance predicate.

### Security boundaries documented by Writ itself

Writ's own `SECURITY.md` explicitly says it is not a sandbox or security boundary, that hooks run as the user's shell privileges, and that the daemon API is unauthenticated and relies on its default localhost binding. It documents bypass gaps in shell-write inspection. If the daemon cannot answer and the local fallback cannot obtain any verdict, a write proceeds by default; `WRIT_STRICT=1` changes that behavior for the write path.

These are explicit limitations, not a basis for assuming malicious-agent containment. A localhost-only unauthenticated API also requires care on shared hosts and with local processes that can access it.

### Potential role alongside GovCheck

Writ could be evaluated as an **optional agent-specific workflow adapter** or as a source of narrowly scoped execution evidence. It must not become GovCheck's normative authority, acceptance authority or mandatory runtime dependency. Any reported gate event must be treated as a claim from the Writ installation and bound to the agent/session, repository candidate, configuration and Writ revision. It is not independent evidence merely because Writ emitted it.

Before integration, test:
- what exact event is emitted for allow/deny/approval and how it binds to candidate and rule revisions;
- fail-open/fail-closed behavior for every hook and daemon-outage path;
- bypasses through shell forms, alternate write paths and direct filesystem/VCS operations;
- session identity, approval-token scope, concurrency and state-file protection;
- daemon API access control, local multi-user exposure, logs/privacy and upgrades;
- which gates are blocking versus advisory/report-only.

Do not describe Writ as an adversarial sandbox. Its own security policy rejects that interpretation.

## 3. Privateer: what the source describes

Privateer is a distribution of the Pi coding agent, not a repository governance engine. Its repository advertises interchangeable model providers, a permission gate for shell commands, file edits and network actions, MCP connectors, sub-agents, workflows and a privacy-related personal-data warning before sending data to an unverified model. It also offers local CLI/desktop surfaces and optional unattended/hosted modes.

The repository's `SECURITY.md` provides useful supply-chain details: no install scripts in the published package, recommended installation with npm scripts disabled, provenance/signature checks, bundle checksum verification, and a `privateer verify` command that distinguishes verified from inconclusive checks. These are project claims documented in the source; this assessment has not independently reproduced them.

### Security and assurance boundaries

Privateer's permission gate is a valuable **agent/harness control**, but it is not GovCheck's governance authority. The repository documents `--no-quarter` as a switch that disables the gate entirely and warns against using it with untrusted content or valuable machine state. That is incompatible with treating the agent's local permission prompt as an unbypassable acceptance boundary.

Its privacy features are also distinct from repository conformance:
- a local PII warning is not proof that every secret or private datum is detected;
- a provider's attested confidential-computing mode applies only when that provider/mode is selected and its attestation assumptions hold;
- provenance or checksum evidence helps assess artifact origin/integrity but does not prove policy correctness or code safety;
- optional cloud/Harbor operation has a different trust and data-location posture from local CLI execution.

### Potential role alongside GovCheck

Privateer is a **candidate agent harness for interoperability testing**, not a GovCheck dependency or policy engine. Use it to test whether the CLI contract can be discovered and followed by a Pi-based agent; assess whether evidence can be captured without granting the agent authority to approve its own work. Treat its gate output as agent-generated evidence unless a separate verifier validates it.

Before any production integration, test permission-gate defaults and bypasses, local/network boundaries, provider routing and data egress, MCP/sub-agent propagation, session/evidence identity, dependency/provenance checks, and the exact local versus hosted execution mode.

## 4. Comparative fit

| Dimension | GovCheck target | Writ (`infinri/Writ`) | Privateer (`privateer-agent/privateer-agent`) |
|---|---|---|---|
| Primary object | Repository and exact proposed change | Claude Code session/workflow and tool events | Agent session and delegated coding work |
| Normative authority | Canonical repository governance source (planned) | Local rule corpus/graph for Writ gates | Agent configuration, permissions and loaded project instructions |
| Workflow gates | Acceptance/application predicate at a declared boundary | Tool-time gates and human approvals in supported Claude Code hooks | Per-action permission gate in the agent harness |
| Repository change identity | Exact base/candidate/governance/spec tuple (planned) | Must be independently checked before use as GovCheck evidence | Must be independently checked before use as GovCheck evidence |
| VCS semantics | Git and Pijul as distinct first-class adapters (planned) | Not a replacement for native VCS contracts | Built on Pi; not a replacement for GovCheck's VCS contract |
| Independent acceptance authority | Required for shared enforcement | Not established by its agent hooks | Not established by its permission gate |
| Adversarial containment | Must disclose real boundary and bypass limits | Explicitly not a sandbox; documented bypass/fail-open cases | Permission gate can be disabled; not an independent acceptance boundary |
| Best integration hypothesis | Core governance evaluator/dossier | Optional Claude Code workflow adapter / evidence source | Optional Pi-based agent test fixture / evidence source |
| Decision | Core product | Do not adopt as core or claim sandbox guarantees | Do not adopt as core governance engine |

## 5. Recommendation

1. **Keep GovCheck's product boundary unchanged.** Neither project replaces the canonical governance model, assurance dossier or exact-candidate acceptance logic.
2. **Use both as test fixtures, not dependencies.** Writ probes tool-time workflow enforcement; Privateer probes Pi-based agent interoperability and permission-gate behavior.
3. **Define a neutral CLI/dossier contract first.** Integrations must consume the same normative semantics and must not embed competing policy decisions.
4. **Treat their output as evidence with provenance and limits.** Bind to tool revision, configuration, session, candidate and exact invocation; independently validate where required.
5. **Run adversarial tests before relying on gates.** Specifically include fail-open paths, disabled controls, direct filesystem/VCS changes, stale approvals, session confusion, local API exposure and data-egress cases.
6. **Do not select either as a mandatory dependency at this stage.** The current evidence supports complementary evaluation, not a conclusion that either satisfies GovCheck's full requirements.

## Sources

- Writ repository and architecture: https://github.com/infinri/Writ
- Writ security policy: https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/SECURITY.md
- Writ session/gate contract: https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/docs/reference/session-and-gates.md
- Privateer repository: https://github.com/privateer-agent/privateer-agent
- Privateer security policy: https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/SECURITY.md
- Privateer README and install verification instructions: https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/README.md
