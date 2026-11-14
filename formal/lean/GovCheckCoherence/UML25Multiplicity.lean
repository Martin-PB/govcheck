/-
  Version-pinned subset of OMG UML 2.5 multiplicity semantics.

  This module interprets only the literal/default cases used by the pinned SACM
  2.4 Beta 1 XMI. It does not parse XML, evaluate arbitrary ValueSpecifications,
  execute OCL, or establish that a parser extracted a source fragment correctly.
-/
namespace GovCheck.Coherence.UML25Multiplicity

inductive LowerValueSpecification where
  | literalInteger (explicitValue : Option Nat)
  | literalNull
  | unsupported
  deriving DecidableEq, Repr

inductive UpperBound where
  | finite (value : Nat)
  | unlimited
  deriving DecidableEq, Repr

inductive UpperValueSpecification where
  | literalUnlimitedNatural (explicitValue : Option UpperBound)
  | literalNull
  | unsupported
  deriving DecidableEq, Repr

structure Multiplicity where
  lower : Nat
  upper : UpperBound
  deriving DecidableEq, Repr

/-- UML 2.5 §7.8.8.7: lowerBound() returns 1 when lowerValue is absent
    or its integerValue() is null. A LiteralInteger with no serialized value
    uses the metamodel default 0 (§8.6.9.4). -/
def lowerBound : Option LowerValueSpecification → Option Nat
  | none => some 1
  | some (.literalInteger none) => some 0
  | some (.literalInteger (some value)) => some value
  | some .literalNull => some 1
  | some .unsupported => none

/-- UML 2.5 §7.8.8.7: upperBound() returns 1 when upperValue is absent
    or its unlimitedValue() is null. A LiteralUnlimitedNatural with no
    serialized value uses the metamodel default 0 (§8.6.14.4). -/
def upperBound : Option UpperValueSpecification → Option UpperBound
  | none => some (.finite 1)
  | some (.literalUnlimitedNatural none) => some (.finite 0)
  | some (.literalUnlimitedNatural (some value)) => some value
  | some .literalNull => some (.finite 1)
  | some .unsupported => none

/-- Interpret a multiplicity only when both bounds belong to the supported
    literal/default subset. Unsupported ValueSpecifications remain unresolved. -/
def interpretMultiplicity
    (lower : Option LowerValueSpecification)
    (upper : Option UpperValueSpecification) : Option Multiplicity :=
  match lowerBound lower, upperBound upper with
  | some lowerValue, some upperValue => some ⟨lowerValue, upperValue⟩
  | _, _ => none

theorem absent_lower_value_specification_defaults_to_one :
    lowerBound none = some 1 := rfl

theorem omitted_literal_integer_value_defaults_to_zero :
    lowerBound (some (.literalInteger none)) = some 0 := rfl

theorem explicit_literal_integer_value_is_preserved (value : Nat) :
    lowerBound (some (.literalInteger (some value))) = some value := rfl

theorem literal_null_lower_value_uses_lower_bound_fallback :
    lowerBound (some .literalNull) = some 1 := rfl

theorem absent_upper_value_specification_defaults_to_one :
    upperBound none = some (.finite 1) := rfl

theorem omitted_literal_unlimited_natural_value_defaults_to_zero :
    upperBound (some (.literalUnlimitedNatural none)) = some (.finite 0) := rfl

theorem explicit_unlimited_natural_is_preserved :
    upperBound (some (.literalUnlimitedNatural (some .unlimited))) = some .unlimited := rfl

theorem literal_null_upper_value_uses_upper_bound_fallback :
    upperBound (some .literalNull) = some (.finite 1) := rfl

theorem unsupported_lower_value_specification_remains_unresolved :
    lowerBound (some .unsupported) = none := rfl

theorem unsupported_upper_value_specification_remains_unresolved :
    upperBound (some .unsupported) = none := rfl

end GovCheck.Coherence.UML25Multiplicity
