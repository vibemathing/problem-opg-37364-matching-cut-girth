import R10.Parallel22
import R10.C34IndexCardinalities

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-!
UNCOMPILED successor source. Each `decide` below is a proposed Lean logical
reduction on a FIXED finite 24-colour domain. No Python certificate is
imported. Performance and elaboration have not been measured.
The finite type uses powersetCard 2 (276 entries), not the full powerset of
ColorPair. The arbitrary endpoint parameter N does not occur in these checks.
-/
namespace R10.Parallel22.C35.Colors
open R10.Parallel22
open R10.Parallel22.C34.Indices
open scoped BigOperators

abbrev Choice := Choose 24 2

/-- Identity on the underlying two-element colour sets. -/
def choiceEquiv : ColorPair ≃ Choice where
  toFun a := ⟨a.val, Finset.mem_powersetCard.mpr ⟨Finset.subset_univ _,a.property⟩⟩
  invFun a := ⟨a.val, (Finset.mem_powersetCard.mp a.property).2⟩
  left_inv _ := rfl
  right_inv _ := rfl

def mask (a : Choice) : Nat := ∑ c ∈ a.val, 2^c.val

/-- Finite proof obligation, not an observed successful reduction. -/
theorem mask_injective : Function.Injective mask := by decide

abbrev TCode := {p : Choice × Choice //
  mask p.1 < mask p.2 ∧ ¬Disjoint p.1.val p.2.val}
abbrev QCode := {p : Choice × Choice //
  mask p.1 < mask p.2 ∧ Disjoint p.1.val p.2.val}
abbrev ForkCode := {p : Choice × Choice // Disjoint p.1.val p.2.val}

/-- These reductions must actually elaborate before their counts are certified. -/
theorem card_TCode : Fintype.card TCode = 6072 := by decide
theorem card_QCode : Fintype.card QCode = 31878 := by decide
theorem card_ForkCode : Fintype.card ForkCode = 63756 := by decide

/-- Cardinality-selected colour reindexing, NOT the old Python rank encoder. -/
noncomputable def tRankEquiv : TCode ≃ (Choose 24 3 × Fin 3) :=
  Fintype.equivOfCardEq (by
    rw [card_TCode, Fintype.card_prod, card_choose, Fintype.card_fin]
    norm_num)

noncomputable def qRankEquiv : QCode ≃ (Choose 24 4 × Fin 3) :=
  Fintype.equivOfCardEq (by
    rw [card_QCode, Fintype.card_prod, card_choose, Fintype.card_fin]
    norm_num)

noncomputable def forkRankEquiv : ForkCode ≃ (Choose 24 4 × Choose 4 2) :=
  Fintype.equivOfCardEq (by
    rw [card_ForkCode, Fintype.card_prod, card_choose, card_choose]
    norm_num)

end R10.Parallel22.C35.Colors
