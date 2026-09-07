import R10.CompletionCardinality
import Mathlib.Data.Fintype.BigOperators

/-
Candidate source only; not elaborated in this runtime.
Cartesian-product counting concerns coordinates, never edge slots within one coordinate.
-/

namespace R10.Cardinality

open scoped BigOperators

/-- The exact finite sample-space denominator, including zero coordinates. -/
theorem sample_space_card (N r : Nat) :
    Fintype.card (Fin r → Equiv.Perm (Fin N)) = (N.factorial) ^ r := by
  rw [Fintype.card_pi_const, Fintype.card_perm, Fintype.card_fin]

/-- Different coordinates may have different compatible prescriptions. -/
theorem completion_tuple_card (N r : Nat)
    (p q : Fin r → Fin N → Prop)
    [∀ i, DecidablePred (p i)] [∀ i, DecidablePred (q i)]
    (e : ∀ i, {x // p i x} ≃ {y // q i y})
    (k : Fin r → Nat) (hk : ∀ i, Fintype.card {x // p i x} = k i) :
    Fintype.card (∀ i, Completion (p i) (q i) (e i)) =
      ∏ i, (N - k i).factorial := by
  classical
  rw [Fintype.card_pi]
  apply Finset.prod_congr rfl
  intro i _
  exact card_fin_completion N (k i) (p i) (q i) (e i) (hk i)

/-- Projection from object-witness pairs need not be injective. -/
theorem bad_objects_le_incidences {Ω : Type*} {S : Type*}
    [Fintype Ω] [Fintype S] (R : Ω → S → Prop)
    [∀ w s, Decidable (R w s)] [DecidablePred (fun w => ∃ s, R w s)] :
    Fintype.card {w // ∃ s, R w s} ≤
      Fintype.card {t : Ω × S // R t.1 t.2} := by
  classical
  let projection : {t : Ω × S // R t.1 t.2} → {w // ∃ s, R w s} :=
    fun t => ⟨t.val.1, ⟨t.val.2, t.property⟩⟩
  have hsurj : Function.Surjective projection := by
    intro w
    rcases w.property with ⟨s, hs⟩
    refine ⟨⟨(w.val, s), hs⟩, ?_⟩
    apply Subtype.ext
    rfl
  exact Fintype.card_le_of_surjective projection hsurj

end R10.Cardinality
