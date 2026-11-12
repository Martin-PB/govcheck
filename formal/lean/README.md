# GovCheck Lean epistemic core

This directory contains the first proposed kernel-checked semantic slice for
metamodel coherence. It is intentionally independent of CSLib initially:
the first obligation is small enough to establish the semantics and trusted
base directly, then assess whether CSLib provides reusable definitions that
match them.

## Build

With Lean 4.19.0 and Lake installed:

```sh
cd formal/lean
lake build
```

## Current scope

- Distinguishes evidence method (`EvidenceKind`) from result (`EvidenceStatus`).
- Pure transport preserves method class.
- A theorem-proof result can only be introduced through a separate
  `KernelCheckedDerivation` constructor.
- Mapping coverage, source/target identities, assumptions and declared losses
  are represented explicitly.

## Important limitation

This is a small formal core, not a proof that SACM, SEON/ReqON, OWL or the
whole GovCheck metamodel are mutually coherent. The theorems establish only
the definitions in this module. They do not establish that a real importer,
serializer or mapping implementation conforms to those definitions.

The source has not yet been built in this environment. Do not report this
prototype as passing until `lake build` has actually run against the pinned
toolchain and the output has been recorded. No CSLib import is present yet;
that is deliberate pending a definition-by-definition compatibility and
trusted-base review.
