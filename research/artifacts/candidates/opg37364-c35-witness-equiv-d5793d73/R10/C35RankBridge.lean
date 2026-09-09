import R10.C35WitnessEquiv

set_option autoImplicit false

/-!
UNCOMPILED source. Equiv components provide the requested target type and
inverse laws without accepting a cardinality/equivalence hypothesis.
C35FiniteColors contains proposed, not executed, Lean reductions.
The colour reindexing is cardinality-selected: tags and endpoints are
preserved, but marker fields must NOT be decoded with the old Python map.
-/
namespace R10.Parallel22.C35
open R10.Parallel22
open R10.Parallel22.C34
open R10.Parallel22.C34.Indices
open scoped BigOperators

variable {N : Nat}

def tColorCodeEquiv : TColor ≃ Colors.TCode where
  toFun p := ⟨(Colors.choiceEquiv p.val.1,Colors.choiceEquiv p.val.2),p.property⟩
  invFun p := ⟨(Colors.choiceEquiv.symm p.val.1,Colors.choiceEquiv.symm p.val.2),p.property⟩
  left_inv _ := rfl
  right_inv _ := rfl

def qColorCodeEquiv : QColor ≃ Colors.QCode where
  toFun p := ⟨(Colors.choiceEquiv p.val.1,Colors.choiceEquiv p.val.2),p.property⟩
  invFun p := ⟨(Colors.choiceEquiv.symm p.val.1,Colors.choiceEquiv.symm p.val.2),p.property⟩
  left_inv _ := rfl
  right_inv _ := rfl

def forkColorCodeEquiv : ForkColor ≃ Colors.ForkCode where
  toFun p := ⟨(Colors.choiceEquiv p.val.1,Colors.choiceEquiv p.val.2),p.property⟩
  invFun p := ⟨(Colors.choiceEquiv.symm p.val.1,Colors.choiceEquiv.symm p.val.2),p.property⟩
  left_inv _ := rfl
  right_inv _ := rfl

noncomputable def tNormalRankEquiv : TNormal N ≃ TIndex N :=
  Equiv.prodCongr (Equiv.refl _) (tColorCodeEquiv.trans Colors.tRankEquiv)

noncomputable def qNormalRankEquiv : QNormal N ≃ QIndex N :=
  Equiv.prodCongr (Equiv.refl _) (qColorCodeEquiv.trans Colors.qRankEquiv)

noncomputable def lNormalRankEquiv : LNormal N ≃ LIndex N :=
  Equiv.prodCongr (Equiv.refl _) (Equiv.prodCongr endpointChooseEquiv
    (forkColorCodeEquiv.trans Colors.forkRankEquiv))

noncomputable def rNormalRankEquiv : RNormal N ≃ RIndex N :=
  Equiv.prodCongr (Equiv.refl _) (Equiv.prodCongr endpointChooseEquiv
    (forkColorCodeEquiv.trans Colors.forkRankEquiv))

abbrev RankIndex (N : Nat) := TIndex N ⊕ (QIndex N ⊕ (LIndex N ⊕ RIndex N))

noncomputable def normalRankEquiv : Normal N ≃ RankIndex N :=
  Equiv.sumCongr tNormalRankEquiv
    (Equiv.sumCongr qNormalRankEquiv (Equiv.sumCongr lNormalRankEquiv rNormalRankEquiv))

/-- Actual C33 Witness subtype, not a local-code surrogate. -/
noncomputable def witnessIndexEquiv : {w : Witness N // Admissible w} ≃
    (TIndex N ⊕ (QIndex N ⊕ (LIndex N ⊕ RIndex N))) :=
  witnessNormalEquiv.trans normalRankEquiv

theorem witness_index_left_inv (w : {w : Witness N // Admissible w}) :
    witnessIndexEquiv.symm (witnessIndexEquiv w) = w :=
  witnessIndexEquiv.symm_apply_apply w

theorem witness_index_right_inv (i : RankIndex N) :
    witnessIndexEquiv (witnessIndexEquiv.symm i) = i :=
  witnessIndexEquiv.apply_symm_apply i

theorem t_normal_card : Nat.card (TNormal N) = 6072*N^2 := by
  classical
  rw [Nat.card_congr tNormalRankEquiv, Nat.card_eq_fintype_card]
  exact card_T_index N

theorem q_normal_card : Nat.card (QNormal N) = 31878*N^2 := by
  classical
  rw [Nat.card_congr qNormalRankEquiv, Nat.card_eq_fintype_card]
  exact card_Q_index N

theorem l_normal_card : Nat.card (LNormal N) = 31878*N^2*(N-1) := by
  classical
  rw [Nat.card_congr lNormalRankEquiv, Nat.card_eq_fintype_card]
  exact card_L_index N

theorem r_normal_card : Nat.card (RNormal N) = 31878*N^2*(N-1) := by
  classical
  rw [Nat.card_congr rNormalRankEquiv, Nat.card_eq_fintype_card]
  exact card_R_index N

/-- Witness count only; not the probability-weighted incidence sum. -/
theorem admissible_witness_card : Nat.card (AdmissibleWitness N) =
    6072*N^2 + 31878*N^2 + 2*(31878*N^2*(N-1)) := by
  classical
  rw [Nat.card_congr witnessIndexEquiv, Nat.card_eq_fintype_card]
  simp only [Fintype.card_sum, card_T_index, card_Q_index, card_L_index, card_R_index]
  ring

/-- Constructed C34 table -> C33 -> C32 card_hit_tuple24/card_hit. -/
theorem rank_event_count (i : RankIndex N) :
    Nat.card {omega : Omega N // Rel omega (witnessIndexEquiv.symm i).val} =
      ∏ c, factor N (normalizedTable (witnessIndexEquiv.symm i).val c) :=
  admissible_event_count (witnessIndexEquiv.symm i).val
    (witnessIndexEquiv.symm i).property

end R10.Parallel22.C35
