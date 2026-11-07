# 0020 — First recorded TLC execution on the lifecycle model

**Status:** recorded execution of a mechanical check (`MODEL_CHECKED` in the vocabulary of [0015](0015-governance-conformance-and-validation-plan.md)) against the recorded model and configuration only. This is not a proof about the implementation, not a conformance claim, and not evidence about any governed target repository. **French:** [0020 (français)](0020-first-tlc-execution-record.fr.md).

## Subject and scope

- Model: `formal/tla/GovCheckLifecycle.tla` with `formal/tla/GovCheckLifecycle.cfg`, repository `Martin-PB/govcheck`.
- Tool: `tla2tools.jar` v1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`, downloaded from the SourceForge mirror of the tlaplus project and checksum-verified before use.
- Invocation: SANY parse check, then `tlc2.TLC -config formal/tla/GovCheckLifecycle.cfg formal/tla/GovCheckLifecycle.tla`, executed by the `.github/workflows/tla-check.yml` workflow.

## Evidence

- Workflow run on pull request [#15](https://github.com/Martin-PB/govcheck/pull/15) (head commit `49d9c2d43d10459e2878a1e36e188a38d57d50f0`, 6 November 2026): job `tlc` concluded `success`; job `diagram-drift` concluded `success`. Check runs: <https://github.com/Martin-PB/govcheck/pull/15/checks>.
- The run uploads the raw output as the `tlc-report` artifact (`tlc-report.txt` and `tla2tools.sha256`).

## Limits

- `MODEL_CHECKED` covers only the recorded TLA+ model and TLC configuration. It does not establish implementation conformance, and the model itself documents its abstraction limits in `docs/formal/lifecycle-model.md`.
- The result is bound to the exact tool version, configuration and model revision above; it is not transferable to other revisions.
- Earlier runs of the same workflow on PR #10 failed at tool download (mutable v1.8.0 release asset); those failures are recorded here for honesty and are not model-check results.

## Bibliographic references

- [R-05 — TLA+ and TLC state-transition modeling](../references.md#r-05)
