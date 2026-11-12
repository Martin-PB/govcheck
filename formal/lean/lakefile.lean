import Lake
open Lake DSL

require cslib from git "https://github.com/leanprover/cslib" @ "f8acdb37c713b0124ad36b863f50c200a5f1cdba"

package govcheckCoherence where
  version := v!"0.0.0"

lean_lib GovCheckCoherence where
  srcDir := "."
  roots := #[`GovCheckCoherence]
