import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Tactic

set_option autoImplicit false

/- Uncompiled C34 index-cardinality source.
These are the sizes of explicit index types. They do not silently assert
an equivalence with C33 Witness. The actual witness-index equivalences are
provided by the written/executable maps and remain pending Lean translation.
-/
namespace R10.Parallel22.C34.Indices

abbrev Choose (n k : Nat) :=
  ↥((Finset.univ : Finset (Fin n)).powersetCard k)

theorem card_choose (n k : Nat) : Fintype.card (Choose n k) = n.choose k := by
  simp [Choose]

/-- Increasing three-colour set and the rank of its common colour. -/
abbrev TIndex (N : Nat) := (Fin N × Fin N) × (Choose 24 3 × Fin 3)

/-- Increasing four-colour set; marker j in Fin 3 means partner rank j+1 of rank 0. -/
abbrev QIndex (N : Nat) := (Fin N × Fin N) × (Choose 24 4 × Fin 3)

/-- Centre, unordered endpoint pair, four colours, and two ranks assigned to the lesser endpoint. -/
abbrev LIndex (N : Nat) := Fin N × Choose N 2 × Choose 24 4 × Choose 4 2
abbrev RIndex (N : Nat) := Fin N × Choose N 2 × Choose 24 4 × Choose 4 2

theorem card_T_index (N : Nat) : Fintype.card (TIndex N) = 6072 * N^2 := by
  simp only [TIndex, Fintype.card_prod, Fintype.card_fin, card_choose]
  norm_num
  <;> ring

theorem card_Q_index (N : Nat) : Fintype.card (QIndex N) = 31878 * N^2 := by
  simp only [QIndex, Fintype.card_prod, Fintype.card_fin, card_choose]
  norm_num
  <;> ring

private theorem twice_choose_succ (n : Nat) : 2 * (n+1).choose 2 = n*(n+1) := by
  induction n with
  | zero => norm_num
  | succ n ih =>
    have step : (n+2).choose 2 = (n+1).choose 2 + (n+1) := by
      rw [Nat.choose_succ_succ]
      simp [Nat.add_comm]
    rw [show n+1+1 = n+2 by omega, step]
    nlinarith [ih]

theorem twice_choose_two (N : Nat) : 2 * N.choose 2 = N*(N-1) := by
  cases N with
  | zero => norm_num
  | succ n => simpa using twice_choose_succ n

theorem card_L_index (N : Nat) :
    Fintype.card (LIndex N) = 31878 * N^2 * (N-1) := by
  calc
    _ = 63756 * N * N.choose 2 := by
      simp only [LIndex, Fintype.card_prod, Fintype.card_fin, card_choose]
      norm_num
      <;> ring
    _ = 31878 * N * (2 * N.choose 2) := by ring
    _ = 31878 * N * (N*(N-1)) := by rw [twice_choose_two]
    _ = _ := by ring

theorem card_R_index (N : Nat) :
    Fintype.card (RIndex N) = 31878 * N^2 * (N-1) := card_L_index N

end R10.Parallel22.C34.Indices
