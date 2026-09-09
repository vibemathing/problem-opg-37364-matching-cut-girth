import R10.Parallel22

set_option autoImplicit false

/- C34 successor source. NOT elaborated in the current runtime.
No conditional cardinality of a class is imported as an assumption. This
file addresses compatibility, a mutually exclusive four-way classifier,
and constructs the formerly conditional Encodes witness used by C33.
The canonical index equivalence is still a separate open Lean dependency.
-/
namespace R10.Parallel22.C34
open R10.Parallel22
open scoped BigOperators

variable {N : Nat}

def Compatible (s t : Cycle2 N) : Prop :=
  ∀ c ∈ s.2.2.val, c ∈ t.2.2.val → s.1 = t.1 ∧ s.2.1 = t.2.1

def Admissible (w : Witness N) : Prop :=
  ∀ s ∈ w.val, ∀ t ∈ w.val, Compatible s t

/-- Sharing a permutation colour at a common endpoint fixes both endpoints. -/
theorem realized_admissible (omega : Omega N) (w : Witness N)
    (hw : Rel omega w) : Admissible w := by
  intro s hs t ht c hcs hct
  have heq : omega c s.1 = s.2.1 := hw s hs c hcs
  have heq' : omega c t.1 = t.2.1 := hw t ht c hct
  rcases w.property.2 s hs t ht with hx | hy
  · exact ⟨hx, heq.symm.trans ((congrArg (omega c) hx).trans heq')⟩
  · exact ⟨(omega c).injective (heq.trans (hy.trans heq'.symm)), hy⟩

/-- It is unsound to classify every raw witness into four NONZERO classes. -/
theorem inadmissible_empty (w : Witness N) (hw : ¬Admissible w) :
    Nat.card {omega : Omega N // Rel omega w} = 0 := by
  classical
  letI : IsEmpty {omega : Omega N // Rel omega w} :=
    ⟨fun omega => hw (realized_admissible omega.val w omega.property)⟩
  simp

inductive Shape where
  | T | Q | L | R
  deriving DecidableEq, Repr

def InClass (s t : Cycle2 N) : Shape → Prop
  | .T => s.1 = t.1 ∧ s.2.1 = t.2.1 ∧ ¬Disjoint s.2.2.val t.2.2.val
  | .Q => s.1 = t.1 ∧ s.2.1 = t.2.1 ∧ Disjoint s.2.2.val t.2.2.val
  | .L => s.1 = t.1 ∧ s.2.1 ≠ t.2.1 ∧ Disjoint s.2.2.val t.2.2.val
  | .R => s.1 ≠ t.1 ∧ s.2.1 = t.2.1 ∧ Disjoint s.2.2.val t.2.2.val

/-- Endpoint separation forces colour disjointness; no slot independence. -/
theorem compatible_disjoint_of_endpoint_ne (s t : Cycle2 N)
    (h : Compatible s t) (hne : s.1 ≠ t.1 ∨ s.2.1 ≠ t.2.1) :
    Disjoint s.2.2.val t.2.2.val := by
  apply Finset.disjoint_left.mpr
  intro c hcs hct
  have heq := h c hcs hct
  rcases hne with hx | hy
  · exact hx heq.1
  · exact hy heq.2

noncomputable def classify (s t : Cycle2 N) : Shape := by
  classical
  exact if s.1 = t.1 then
    if s.2.1 = t.2.1 then
      if Disjoint s.2.2.val t.2.2.val then .Q else .T
    else .L
  else .R

theorem classify_spec (s t : Cycle2 N) (hs : shares s t)
    (hc : Compatible s t) : InClass s t (classify s t) := by
  classical
  by_cases hx : s.1 = t.1
  · by_cases hy : s.2.1 = t.2.1
    · by_cases hd : Disjoint s.2.2.val t.2.2.val
      · simpa [classify, InClass, hx, hy, hd]
      · simpa [classify, InClass, hx, hy, hd]
    · have hd := compatible_disjoint_of_endpoint_ne s t hc (Or.inr hy)
      simpa [classify, InClass, hx, hy] using hd
  · have hy : s.2.1 = t.2.1 := hs.resolve_left hx
    have hd := compatible_disjoint_of_endpoint_ne s t hc (Or.inl hx)
    simpa [classify, InClass, hx, hy] using hd

theorem class_unique {s t : Cycle2 N} {a b : Shape}
    (ha : InClass s t a) (hb : InClass s t b) : a = b := by
  cases a <;> cases b <;> simp_all [InClass]

/-- Mutual exclusion and exhaustive coverage are restricted to compatible pairs. -/
theorem compatible_fourway (s t : Cycle2 N) (hs : shares s t)
    (hc : Compatible s t) : ∃! a : Shape, InClass s t a := by
  refine ⟨classify s t, classify_spec s t hs hc, ?_⟩
  intro a ha
  exact class_unique ha (classify_spec s t hs hc)

/-- Instantiation on two actual, distinct members of a realized C33 witness. -/
theorem realized_members_fourway (omega : Omega N) (w : Witness N)
    (hw : Rel omega w) (s t : Cycle2 N) (hs : s ∈ w.val) (ht : t ∈ w.val)
    (_hne : s ≠ t) : ∃! a : Shape, InClass s t a :=
  compatible_fourway s t (w.property.2 s hs t ht)
    (realized_admissible omega w hw s hs t ht)

/-- For distinct two-sets the nonempty intersection in T has exactly one colour. -/
theorem common_card_one (s t : Cycle2 N) (hne : s ≠ t)
    (ht : InClass s t .T) : (s.2.2.val ∩ t.2.2.val).card = 1 := by
  rcases ht with ⟨hx, hy, hd⟩
  have hab : s.2.2.val ≠ t.2.2.val := by
    intro h
    exact hne (Prod.ext hx (Prod.ext hy (Subtype.ext h)))
  have hle : (s.2.2.val ∩ t.2.2.val).card ≤ 2 := by
    simpa only [s.2.2.property] using
      (Finset.card_le_card (Finset.inter_subset_left :
        s.2.2.val ∩ t.2.2.val ⊆ s.2.2.val))
  have hzero : (s.2.2.val ∩ t.2.2.val).card ≠ 0 := by
    intro h
    exact hd (Finset.disjoint_iff_inter_eq_empty.mpr (Finset.card_eq_zero.mp h))
  have htwo : (s.2.2.val ∩ t.2.2.val).card ≠ 2 := by
    intro h
    have hleft : s.2.2.val ∩ t.2.2.val = s.2.2.val :=
      Finset.eq_of_subset_of_card_le Finset.inter_subset_left (by
        simp only [s.2.2.property, h, le_refl])
    have hright : s.2.2.val ∩ t.2.2.val = t.2.2.val :=
      Finset.eq_of_subset_of_card_le Finset.inter_subset_right (by
        simp only [t.2.2.property, h, le_refl])
    exact hab (hleft.symm.trans hright)
  omega

theorem t_union_card (s t : Cycle2 N) (hne : s ≠ t)
    (ht : InClass s t .T) : (s.2.2.val ∪ t.2.2.val).card = 3 := by
  have h := Finset.card_union_add_card_inter s.2.2.val t.2.2.val
  rw [s.2.2.property, t.2.2.property, common_card_one s t hne ht] at h
  omega

theorem disjoint_union_card (s t : Cycle2 N)
    (hd : Disjoint s.2.2.val t.2.2.val) :
    (s.2.2.val ∪ t.2.2.val).card = 4 := by
  rw [Finset.card_union_of_disjoint hd, s.2.2.property, t.2.2.property]

/-- Normalized requirements are sets, not occurrences in two cycle traversals. -/
theorem mem_requirements (w : Witness N) (c : Fin 24) (e : Fin N × Fin N) :
    e ∈ requirements w c ↔
      ∃ s ∈ w.val, c ∈ s.2.2.val ∧ e = (s.1, s.2.1) := by
  constructor
  · intro he
    rcases Finset.mem_biUnion.mp he with ⟨s, hs, he⟩
    by_cases hc : c ∈ s.2.2.val
    · refine ⟨s, hs, hc, ?_⟩
      simpa only [if_pos hc, Finset.mem_singleton] using he
    · simp only [if_neg hc, Finset.not_mem_empty] at he
  · rintro ⟨s, hs, hc, rfl⟩
    exact Finset.mem_biUnion.mpr ⟨s, hs, by simp only [if_pos hc, Finset.mem_singleton]⟩

theorem requirements_unique (w : Witness N) (hw : Admissible w)
    (c : Fin 24) (e f : Fin N × Fin N)
    (he : e ∈ requirements w c) (hf : f ∈ requirements w c) : e = f := by
  obtain ⟨s, hs, hcs, rfl⟩ := (mem_requirements w c e).mp he
  obtain ⟨t, ht, hct, rfl⟩ := (mem_requirements w c f).mp hf
  have h := hw s hs t ht c hcs hct
  exact Prod.ext h.1 h.2

noncomputable def normalizedTable (w : Witness N) : Table N := fun c =>
  if h : (requirements w c).Nonempty then some (Classical.choose h) else none

/-- Constructs Encodes from compatibility instead of requiring it as an oracle. -/
theorem normalizedTable_encodes (w : Witness N) (hw : Admissible w) :
    Encodes (normalizedTable w) w := by
  classical
  intro c
  by_cases h : (requirements w c).Nonempty
  · change requirements w c = match (if h : (requirements w c).Nonempty then
        some (Classical.choose h) else none) with | none => ∅ | some p => {p}
    rw [dif_pos h]
    apply Finset.ext
    intro e
    constructor
    · intro he
      exact Finset.mem_singleton.mpr
        (requirements_unique w hw c e (Classical.choose h) he (Classical.choose_spec h))
    · intro he
      have heq := Finset.mem_singleton.mp he
      simpa only [heq] using Classical.choose_spec h
  · change requirements w c = match (if h : (requirements w c).Nonempty then
        some (Classical.choose h) else none) with | none => ∅ | some p => {p}
    rw [dif_neg h]
    exact Finset.not_nonempty_iff_eq_empty.mp h

/-- The actual C32 card_hit/card_hit_tuple24 chain is invoked by card_encoded_event. -/
theorem admissible_event_count (w : Witness N) (hw : Admissible w) :
    Nat.card {omega : Omega N // Rel omega w} =
      ∏ c, factor N (normalizedTable w c) :=
  card_encoded_event (normalizedTable w) w (normalizedTable_encodes w hw)

/-- Every witness occurring in incidence has the constructed, not assumed, table. -/
theorem realized_event_count (omega : Omega N) (w : Witness N) (hw : Rel omega w) :
    Nat.card {omega' : Omega N // Rel omega' w} =
      ∏ c, factor N (normalizedTable w c) :=
  admissible_event_count w (realized_admissible omega w hw)

/-- The two distinct inputs of an output conflict form a real embedding. -/
def twoInput (x z : Fin N) (hxz : x ≠ z) : Fin 2 ↪ Fin N where
  toFun i := if i.val = 0 then x else z
  inj' := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all

noncomputable def rightForkEquiv (x z y : Fin N) (hxz : x ≠ z) :
    {pi : Equiv.Perm (Fin N) // pi x = y ∧ pi z = y} ≃
      R10.Hits.Hit (twoInput x z hxz) {y} where
  toFun f := ⟨f.val, by
    intro i
    fin_cases i
    · simpa [twoInput] using f.property.1
    · simpa [twoInput] using f.property.2⟩
  invFun f := ⟨f.val, by
    constructor
    · simpa [twoInput] using f.property (0 : Fin 2)
    · simpa [twoInput] using f.property (1 : Fin 2)⟩
  left_inv _ := Subtype.ext rfl
  right_inv _ := Subtype.ext rfl

/-- This zero is the exact C32 b=1,k=2 count, not multiplication of two slot probabilities. -/
theorem right_fork_count_zero (x z y : Fin N) (hxz : x ≠ z) :
    Nat.card {pi : Equiv.Perm (Fin N) // pi x = y ∧ pi z = y} = 0 := by
  classical
  rw [Nat.card_congr (rightForkEquiv x z y hxz), Nat.card_eq_fintype_card]
  exact R10.Hits.card_hit_of_target_small (twoInput x z hxz) {y} (by simp)

end R10.Parallel22.C34
