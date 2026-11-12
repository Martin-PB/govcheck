import Lake
open Lake DSL

package govcheckCslibCompat where
  version := v!"0.0.0"
  defaultTargets := #[`CslibCompat]

require cslib from git
  "https://github.com/leanprover/cslib" @ "70e25828d89a3916e41c9d84cfffd7e6093bb1a0"

lean_lib CslibCompat where
  srcDir := "."

