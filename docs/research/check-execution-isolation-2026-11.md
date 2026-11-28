# Repository-controlled check execution: isolation and resource-boundary research

**Status:** source-grounded design research and candidate contract; not an adopted execution policy, sandbox implementation or security certification.  
**Date:** 2026-11-28. **Parent:** [Issue #218](https://github.com/Martin-PB/govcheck/issues/218).  
**French:** [Isolation de l'exécution des contrôles fournis par un dépôt](check-execution-isolation-2026-11.fr.md).

## 1. Executive conclusion

GovCheck should treat repository-controlled build, test, scanner and generator commands as **untrusted workloads**, even when their source is part of the candidate repository. The trusted evaluator, trust policy, signing keys, runner supervisor and acceptance adapter must not share the candidate workload's authority or writable environment.

No single mechanism provides all required properties:

- **Landlock** adds unprivileged, additive restrictions on filesystem access. It is not a general syscall or resource-control mechanism.
- **seccomp** restricts system calls and selected arguments. It is not a filesystem policy, network-egress policy or CPU/memory quota.
- **cgroups v2** control CPU, memory, process count and I/O consumption. They are not a filesystem or trust boundary.
- **OCI containers** configure namespaces, cgroups, capabilities, seccomp, LSM and filesystem controls. A container is not a security guarantee unless its effective configuration and host integration are constrained.
- **Nix build sandboxing** is useful for dependency/build isolation but has platform and execution-mode qualifications; it is not a universal hostile-code sandbox.
- **Ephemeral hosted VMs and microVMs** offer stronger isolation for hostile public-repository workloads, at higher cost and with additional deployment dependencies. A microVM still needs host-level egress controls and a hardened supervisor.

**Recommendation:** specify a platform-neutral execution contract and profiles, not a mandatory sandbox product. The default should be **no execution** of candidate-controlled commands by GovCheck. If a deployment elects to run them, it must select a declared execution profile and backend, minimize credentials, enforce resource/network/filesystem boundaries, and produce evidence bound to the exact candidate and policy. If the required boundary cannot be established, the result is UNKNOWN or NOT-RUN, never PASS.

## 2. Trust boundary and adversary

The candidate workload may be malicious or compromised through a pull-request change to a test/build/scanner script, a package-manager lifecycle hook, a compromised dependency, a compiler/plugin/test runner, a malicious archive/symlink/submodule, a vulnerable tool/runtime, or a workflow change that broadens permissions.

Assume it attempts to:
1. read host files, credentials, environment variables, sockets, metadata services or other jobs;
2. exfiltrate data through DNS, HTTPS, raw sockets, proxy variables or dependency endpoints;
3. alter the trusted evaluator, policy, keys, runner configuration or Git refs;
4. persist through background processes, caches, writable mounts, shared workspaces or runner reuse;
5. exhaust CPU, memory, PIDs, file descriptors, disk, inodes, network, logs or artifact storage;
6. forge or replace output evidence, or make untrusted output appear to be trusted metadata.

The trusted computing base (TCB) must be declared per profile. It may include the host kernel, hypervisor, runner supervisor, container runtime, filesystem, network filter, image builder, toolchain, policy store and artifact collector. A sandbox claim without a declared TCB and adversarial tests is not a meaningful assurance claim.

## 3. Mechanism comparison

| Mechanism | Useful properties | What it does not establish alone | Constraint |
|---|---|---|---|
| Linux Landlock | Unprivileged, per-process, additive filesystem restrictions; composes with existing access controls. | Does not replace syscall filtering, quotas, process isolation, network policy or a VM boundary. | Linux kernel/ABI dependent; supported ABI and rules must be checked. |
| Linux seccomp-BPF | Restricts syscall entry and can inspect syscall numbers/arguments; reduces kernel attack surface. | Does not express general path semantics, set resource quotas or filter all network egress. | Linux-specific; syscall/architecture differences and filter correctness matter. |
| Linux namespaces | Separate selected PID, mount, network, IPC, UTS, user and cgroup views. | An omitted namespace may be inherited; namespaces do not impose CPU/memory budgets. | Linux-specific; privilege, mount and device setup must be correct. |
| cgroups v2 | CPU quota/weight, memory ceilings, PID limits and I/O accounting/throttling. | Does not prevent host-file reads, credential use, network access or kernel attacks. | Linux-specific; controller availability and parent hierarchy matter. |
| OCI runtime | Standardized configuration for namespaces, cgroups, capabilities, seccomp, LSM, root filesystem and resources. | “Container” alone proves nothing. Privileged mode, host mounts/sockets, host network, broad capabilities or inherited namespaces can defeat isolation. | Host kernel and runtime configuration remain trusted. |
| Nix build sandbox | Restricts build visibility to declared store inputs, temporary directories and selected paths; Linux namespaces isolate several views. | Does not cover every arbitrary command outside Nix builds; fixed-output derivations may need network; does not define GovCheck evidence semantics. | Manual documents Linux/macOS, a root requirement and platform-dependent defaults. |
| Ephemeral hosted VM | Fresh worker boundary and disposable state; separates candidate code from persistent control plane. | Does not prevent exfiltration of data intentionally provided or compensate for unsafe workflow permissions. | Provider-specific image, lifecycle, credential, network and artifact policies. |
| MicroVM (e.g. Firecracker) | Hardware virtualization boundary with a small guest; can be layered with jailer, seccomp, namespaces and cgroups. | Does not remove host/hypervisor/supervisor trust; guest egress must be filtered on the host. | Linux/KVM and privileged host integration; greater operational complexity. |

### 3.1 Containers are a configuration, not a policy

The OCI runtime specification makes the relevant controls explicit: namespace selection, cgroup placement, memory/PID/CPU resources, process capabilities, seccomp, LSM profiles, filesystem mounts and devices. An omitted namespace may inherit the runtime namespace. A future GovCheck profile must therefore record the effective configuration, not merely say that a container is used.

A container-runtime socket, privileged container, writable host bind mount, host PID/network namespace, broad device access or shared writable runner directory can collapse the intended boundary.

### 3.2 Layering is defense in depth, not proof by accumulation

A Linux process profile may combine a dedicated unprivileged identity, private namespaces, read-only candidate input, bounded writable scratch, Landlock path restrictions, a default-deny seccomp filter, cgroup v2 limits, no ambient capabilities/host sockets/credentials, and host-enforced egress denial.

The composition still depends on the kernel, namespace/mount setup, file descriptors passed into the workload, supervisor correctness and the exact toolchain. Each layer needs negative tests. A layered configuration is not automatically a verified sandbox.

## 4. Candidate execution profiles

These profiles are proposals for discussion, not adopted requirements.

### P0 — No candidate execution (default)

- GovCheck does not invoke candidate-controlled commands.
- It may validate static metadata and verify detached evidence produced by an independently configured system.
- Missing execution evidence remains UNKNOWN or NOT-RUN; the evaluator must not infer that tests passed.
- Evidence identifies the external producer, exact candidate, policy, verifier and report digest.

This profile has the smallest GovCheck execution TCB and should be the universal fallback.

### P1 — Local restricted execution (best-effort, explicit operator consent)

- Run only after an operator explicitly selects the profile.
- No repository, forge, signing or cloud secrets are inherited.
- Use an unprivileged account, isolated temporary workspace, read-only candidate input, bounded writable scratch, timeouts and process-tree cleanup.
- On Linux, Landlock + namespaces + seccomp + cgroups may provide defense in depth; other platforms need an explicitly named backend and documented limits.
- Make no strong hostile-code containment claim unless the exact platform/backend profile passes its adversarial test suite.

Useful for local development; not silently promotable to a production acceptance boundary.

### P2 — Ephemeral isolated worker (recommended baseline when public candidate code must run)

- Create a fresh disposable VM/worker per candidate or trust-equivalent batch.
- Keep the trusted controller, policy, signing keys and artifact verifier outside the worker.
- Provide no secrets to the candidate process; use a read-only least-privilege token only if the platform requires one, and keep it inaccessible to untrusted steps where possible.
- Deny network egress by default; dependency access requires a constrained proxy/cache, explicit allowlists and a recorded exception.
- Destroy the worker and writable state after evidence collection; do not reuse candidate-controlled caches across trust boundaries.
- Bind the result to worker-image digest, runner identity, exact candidate/base, policy revision, command, effective isolation profile and artifact digests.

GitHub's documentation distinguishes its own ephemeral clean hosted VMs from self-hosted runners, for which persistent compromise by untrusted workflows is possible. This is a provider statement about its service, not a generic guarantee for all hosted CI.

### P3 — High-risk isolated execution (optional deployment profile)

- Use a microVM or equivalently strong disposable VM boundary.
- Keep the host supervisor minimal and patched; run it under a jailer/least-privilege profile.
- Apply host-level network egress filtering; do not assume the guest filters outbound traffic.
- Apply per-VM CPU, memory, process and I/O quotas.
- Treat guest output as untrusted bytes until independently validated and hashed by the host-side collector.

This profile is justified only where the threat model warrants its complexity; it is not mandatory for every repository.

## 5. Execution contract: minimum fields

A future execution request/attestation should bind:

| Field group | Required information |
|---|---|
| Identity | Execution ID, repository identity, candidate revision/tree/content digest, base revision, target ref and governance/policy revision/digest. |
| Command | Executable identity/digest, argv, working directory, declared input files, toolchain and dependency identities. |
| Environment | Explicit environment allowlist or digest; secret policy; inherited variables denied by default. Never include secret values in the attestation. |
| Filesystem | Candidate snapshot, read-only/writable mounts, mount flags, allowed paths, symlink policy, scratch quota and cleanup result. |
| Network | Disabled/allowlist/proxy mode, DNS policy, egress-filter identity, allowed destinations and exception rationale. |
| Isolation | Backend/profile ID and version; OS/kernel/hypervisor/runtime versions; namespaces, Landlock ABI/rules, seccomp-profile digest, capabilities and cgroup limits. |
| Budgets | Wall-clock timeout, CPU quota, memory/swap ceilings, PID/thread count, file descriptors, disk/inodes, network bytes, stdout/stderr and artifact-size limits. |
| Result | Started/completed/failed/denied/not-run/timed-out/resource-exhausted/cleanup-failed; exit status, termination reason, bounded logs and output/evidence digests. |
| Provenance | Runner/supervisor identity, image digest, policy revision, timestamps and signature/trust-policy binding. |

Infrastructure failure must not be collapsed into a successful test result. Timed-out, resource-exhausted, cleanup-failed, runner-untrusted and incomplete should map to blocking UNKNOWN or explicit failure under the applicable profile, never PASS.

## 6. Secrets and network

- **No secrets by default.** Candidate-controlled processes must not receive signing keys, forge write tokens, deployment credentials, cloud metadata credentials or persistent runner credentials.
- **Separate privileged stages.** If a post-check action needs a credential, run it after the untrusted workload in a separate trusted job with minimal permissions. Never expose it to the same process tree.
- **Avoid credential-bearing caches.** Do not reuse writable caches, home directories, package-manager credentials or workspaces across trust boundaries.
- **Network deny-by-default.** A network namespace is not an egress policy. Enforce egress at the host/provider boundary; consider DNS, proxy bypass, raw sockets and IPv6.
- **Explicit dependency exceptions.** Private dependency fetches need a narrow broker/proxy or a credential mechanism that does not expose the raw secret to the candidate command. Record destination, scope and expiry.
- **Untrusted outputs.** Bound log/artifact size; sanitize secrets; hash exact bytes; parse structured output with strict schemas; never interpret arbitrary stdout as an authenticated acceptance decision.

## 7. Adversarial validation required before a sandbox claim

A backend/profile needs positive and negative tests for:
1. reading host /etc, /proc, home, SSH/GPG directories and runner credentials;
2. symlink traversal, bind mounts, hard links and archive paths outside the workspace;
3. access to container-runtime sockets, devices, host PID/network namespaces and metadata endpoints;
4. exfiltration through DNS, HTTPS, raw sockets, IPv6 and proxy bypass;
5. fork/thread bombs, CPU spin, memory exhaustion, disk/inode exhaustion, descriptor exhaustion and output flood;
6. background processes, shared-cache modification and persistence after the job;
7. modification of evaluator, policy, keys, refs or evidence after execution;
8. malformed archives, path normalization, Unicode paths and parser differentials;
9. cleanup failure or worker reuse after abnormal termination;
10. evidence forgery, swapping or replay from another candidate, base, policy, runner image or verifier.

Each result records the exact backend/profile, OS/kernel/runtime version, candidate, base, policy and fixture revision. Passing on one backend or kernel version does not prove another profile.

## 8. Proposed architecture boundary

Separate four roles:

1. **Governance/evaluator controller:** interprets the repository's declared execution profile and decides whether execution is permitted.
2. **Execution supervisor:** provisions the isolated worker, applies the profile and enforces budgets. It is trusted infrastructure, not candidate code.
3. **Candidate workload:** untrusted commands and dependencies; receives only declared inputs and capabilities.
4. **Evidence collector/verifier:** obtains bounded output from the supervisor, hashes it, verifies provenance and produces a detached record bound to the exact candidate/policy.

The controller must not trust a candidate-produced file that claims its own isolation properties. The supervisor reports effective configuration from outside the workload; the collector independently binds that report to candidate and policy. If the supervisor cannot attest a required control, the result is UNKNOWN.

## 9. Decisions still open

- Does GovCheck orchestrate candidate execution, or only verify/record execution evidence from external systems?
- What is the minimum profile for a repository that opts into execution?
- Is network always denied by default, and how are dependency exceptions authorized?
- Are secrets ever allowed into a candidate workload, or only exposed through a narrow external broker?
- What cross-platform profile is meaningful without overstating Linux-only controls?
- Which supervisor identity and attestation format are trusted, and how are runner-image/toolchain updates handled?
- If the platform cannot enforce a requested control, is execution rejected, marked degraded, or subject to operator risk acceptance?

No answer is adopted by this report. Issue #218 remains a design candidate.

## 10. References

- [R-236 — Linux Landlock](../references.md#r-236)
- [R-237 — Linux seccomp filter](../references.md#r-237)
- [R-238 — Linux cgroup v2](../references.md#r-238)
- [R-239 — Open Container Initiative runtime configuration](../references.md#r-239)
- [R-240 — Firecracker design and sandboxing](../references.md#r-240)
- [R-241 — GitHub Actions secure use](../references.md#r-241)
- [R-242 — Nix build sandbox](../references.md#r-242)
- [Architecture 0006 — Threat and Trust Model](../architecture/0006-threat-and-trust-model.md)
- [Threat-model coverage audit](threat-model-coverage-audit-2026-11-28.md)
- [Issue #218 — execution isolation candidate](https://github.com/Martin-PB/govcheck/issues/218)
