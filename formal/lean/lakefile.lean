import Lake
open Lake DSL

package govcheckCoherence where
  version := v!"0.0.0"

lean_lib GovCheckCoherence where
  srcDir := "."
  roots := #[`GovCheckCoherence]

