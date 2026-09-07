import R10.CompletionEquiv
import Mathlib.Data.Fintype.Card

/-
Candidate source, requested Lean 4.19.0 / Mathlib v4.19.0.
The requested dependencies have not been resolved or compiled here.
This file supplies the cardinality step left open in the earlier checkpoint.
-/

namespace R10.Cardinality

universe u v
variable {A : Type u} {B : Type v}
variable (p : A → Prop) (q : B → Prop)
variable [Fintype A] [Fintype B] [DecidablePred p] [DecidablePred q]

noncomputable instance completionFintype (e : {x // p x} ≃ {y // q y}) :
    Fintype (Completion p q e) := by
  classical
  unfold Completion
  infer_instance

/-- Compatible prescribed pairs have exactly a complementary factorial of completions. -/
theorem card_completion (e : {x // p x} ≃ {y // q y})
    (hAB : Fintype.card A = Fintype.card B) :
    Fintype.card (Completion p q e) =
      (Fintype.card A - Fintype.card {x // p x}).factorial := by
  classical
  have hPQ : Fintype.card {x // p x} = Fintype.card {y // q y} :=
    Fintype.card_congr e
  have hCompl : Fintype.card {x // ¬p x} = Fintype.card {y // ¬q y} := by
    calc
      Fintype.card {x // ¬p x} = Fintype.card A - Fintype.card {x // p x} :=
        Fintype.card_subtype_compl p
      _ = Fintype.card B - Fintype.card {y // q y} := by rw [hAB, hPQ]
      _ = Fintype.card {y // ¬q y} := (Fintype.card_subtype_compl q).symm
  let h : {x // ¬p x} ≃ {y // ¬q y} := Fintype.equivOfCardEq hCompl
  calc
    Fintype.card (Completion p q e) =
        Fintype.card ({x // ¬p x} ≃ {y // ¬q y}) :=
      Fintype.card_congr (completionEquiv p q e)
    _ = (Fintype.card {x // ¬p x}).factorial := Fintype.card_equiv h
    _ = (Fintype.card A - Fintype.card {x // p x}).factorial := by
      rw [Fintype.card_subtype_compl]

/-- The precise (N-k)! statement used by C20's partial-permutation probability. -/
theorem card_fin_completion (N k : Nat) (p q : Fin N → Prop)
    [DecidablePred p] [DecidablePred q]
    (e : {x // p x} ≃ {y // q y})
    (hk : Fintype.card {x // p x} = k) :
    Fintype.card (Completion p q e) = (N - k).factorial := by
  classical
  simpa only [Fintype.card_fin, hk] using card_completion p q e rfl

/-- A full prescription has one completion, including the N=0 case. -/
theorem card_full_completion (N : Nat) (p q : Fin N → Prop)
    [DecidablePred p] [DecidablePred q]
    (e : {x // p x} ≃ {y // q y})
    (hk : Fintype.card {x // p x} = N) :
    Fintype.card (Completion p q e) = 1 := by
  simpa using card_fin_completion N N p q e hk

/-- Conflicting prescribed outputs at the same input cannot be satisfied. -/
theorem input_conflict (f : A → B) (x : A) (y z : B)
    (hy : f x = y) (hz : f x = z) (hne : y ≠ z) : False := by
  exact hne (hy.symm.trans hz)

/-- Distinct prescribed inputs cannot share an output under a bijection. -/
theorem output_conflict (f : A ≃ B) (x y : A)
    (heq : f x = f y) (hne : x ≠ y) : False := by
  exact hne (f.injective heq)

end R10.Cardinality
