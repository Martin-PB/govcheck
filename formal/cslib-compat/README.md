# Isolated CSLib compatibility probe

This Lake package is deliberately separate from `formal/lean`.

- GovCheck epistemic core: Lean 4.19.0.
- CSLib probe: Lean 4.36.0-rc2, matching inspected CSLib HEAD
  `70e25828d89a3916e41c9d84cfffd7e6093bb1a0`.
- CSLib's Mathlib revision is resolved from its own pinned `lakefile.toml`.

The probe imports only CSLib's Basic Temporal Logic and infinite-sequence
temporal definitions. It checks API availability and compilation. It does
not yet prove that a GovCheck lifecycle model refines CSLib's semantics, nor
that CSLib is suitable as a mandatory dependency.

Run:

```sh
cd formal/cslib-compat
lake update
lake build
```

Do not merge this toolchain into the core package. A compatibility pass is
evidence for a possible isolated backend only.
