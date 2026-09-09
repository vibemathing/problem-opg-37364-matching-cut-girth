import R10.C34Classification
import R10.C34IndexCardinalities
import R10.C35FiniteColors

set_option autoImplicit false

/-!
C35 successor SOURCE, not an elaboration receipt.
The equivalence below starts with C33's actual Witness type. Arbitrary-N
endpoint data and fixed-colour data are separated. C35RankBridge connects
the latter to C34's index types. No finite test or class-cardinality premise
is accepted as input to this module.
-/
namespace R10.Parallel22.C35
open R10.Parallel22
open R10.Parallel22.C34
open scoped BigOperators

variable {N : Nat}

/-- Binary-mask tie break; not the historical Python order. -/
def colorRank (a : ColorPair) : Nat := Colors.mask (Colors.choiceEquiv a)

theorem colorRank_injective : Function.Injective colorRank := by
  intro a b h
  exact Colors.choiceEquiv.injective (Colors.mask_injective h)

/-- Lexicographic orientation: left endpoint, right endpoint, colour pair. -/
def Before (s t : Cycle2 N) : Prop :=
  s.1 < t.1 ∨ (s.1 = t.1 ∧
    (s.2.1 < t.2.1 ∨ (s.2.1 = t.2.1 ∧ colorRank s.2.2 < colorRank t.2.2)))

theorem before_irrefl (s : Cycle2 N) : ¬Before s s := by
  simp [Before]

theorem before_ne {s t : Cycle2 N} (h : Before s t) : s ≠ t := by
  intro e
  subst t
  exact before_irrefl s h

theorem before_asymm {s t : Cycle2 N} (h : Before s t) : ¬Before t s := by
  rcases s with ⟨x, y, a⟩
  rcases t with ⟨z, v, b⟩
  simp only [Before] at *
  intro h'
  rcases h with h | ⟨hx, h | ⟨hy, h⟩⟩ <;>
    rcases h' with h' | ⟨hx', h' | ⟨hy', h'⟩⟩ <;> omega

theorem before_total {s t : Cycle2 N} (hne : s ≠ t) : Before s t ∨ Before t s := by
  rcases lt_trichotomy s.1 t.1 with hx | hx | hx
  · exact Or.inl (Or.inl hx)
  · rcases lt_trichotomy s.2.1 t.2.1 with hy | hy | hy
    · exact Or.inl (Or.inr ⟨hx, Or.inl hy⟩)
    · rcases lt_trichotomy (colorRank s.2.2) (colorRank t.2.2) with hc | hc | hc
      · exact Or.inl (Or.inr ⟨hx, Or.inr ⟨hy, hc⟩⟩)
      · exact False.elim (hne (Prod.ext hx (Prod.ext hy (colorRank_injective hc))))
      · exact Or.inr (Or.inr ⟨hx.symm, Or.inr ⟨hy.symm, hc⟩⟩)
    · exact Or.inr (Or.inr ⟨hx.symm, Or.inl hy⟩)
  · exact Or.inr (Or.inl hx)

theorem compatible_refl (s : Cycle2 N) : Compatible s s := by
  intro c _ _
  exact ⟨rfl, rfl⟩

theorem compatible_symm {s t : Cycle2 N} (h : Compatible s t) : Compatible t s := by
  intro c hc hs
  obtain ⟨hx, hy⟩ := h c hs hc
  exact ⟨hx.symm, hy.symm⟩

theorem compatible_same (x y : Fin N) (a b : ColorPair) :
    Compatible (x, y, a) (x, y, b) := by
  intro c _ _
  exact ⟨rfl, rfl⟩

theorem compatible_of_disjoint (s t : Cycle2 N)
    (h : Disjoint s.2.2.val t.2.2.val) : Compatible s t := by
  intro c hc ht
  exact False.elim (Finset.disjoint_left.mp h hc ht)

abbrev OrderedWitness (N : Nat) :=
  {p : Cycle2 N × Cycle2 N //
    Before p.1 p.2 ∧ shares p.1 p.2 ∧ Compatible p.1 p.2}

abbrev AdmissibleWitness (N : Nat) := {w : Witness N // Admissible w}

noncomputable def forgetOrder (p : OrderedWitness N) : AdmissibleWitness N := by
  classical
  rcases p with ⟨⟨s, t⟩, hbefore, hshare, hcompat⟩
  refine ⟨⟨{s, t}, ?_, ?_⟩, ?_⟩
  · simp [before_ne hbefore]
  · intro a ha b hb
    simp only [Finset.mem_insert, Finset.mem_singleton] at ha hb
    rcases ha with rfl | rfl <;> rcases hb with rfl | rfl
    · exact Or.inl rfl
    · exact hshare
    · rcases hshare with h | h
      · exact Or.inl h.symm
      · exact Or.inr h.symm
    · exact Or.inl rfl
  · intro a ha b hb
    simp only [Finset.mem_insert, Finset.mem_singleton] at ha hb
    rcases ha with rfl | rfl <;> rcases hb with rfl | rfl
    · exact compatible_refl s
    · exact hcompat
    · exact compatible_symm hcompat
    · exact compatible_refl t

@[simp] theorem forgetOrder_val (p : OrderedWitness N) :
    (forgetOrder p).val.val = {p.val.1, p.val.2} := by
  rcases p with ⟨⟨s, t⟩, hb, hs, hc⟩
  rfl

/-- Both listings of an unordered pair are retained until orientation is used. -/
theorem pair_equal_cases {A : Type*} [DecidableEq A] {a b c d : A}
    (hab : a ≠ b) (_hcd : c ≠ d) (h : ({a,b} : Finset A) = {c,d}) :
    (a = c ∧ b = d) ∨ (a = d ∧ b = c) := by
  have ha : a = c ∨ a = d := by
    have : a ∈ ({c,d} : Finset A) := h ▸ (by simp)
    simpa using this
  have hb : b = c ∨ b = d := by
    have : b ∈ ({c,d} : Finset A) := h ▸ (by simp)
    simpa using this
  rcases ha with ha | ha <;> rcases hb with hb | hb
  · exact False.elim (hab (ha.trans hb.symm))
  · exact Or.inl ⟨ha, hb⟩
  · exact Or.inr ⟨ha, hb⟩
  · exact False.elim (hab (ha.trans hb.symm))

theorem forgetOrder_injective : Function.Injective (@forgetOrder N) := by
  classical
  intro p q h
  have he : ({p.val.1,p.val.2} : Finset (Cycle2 N)) = {q.val.1,q.val.2} := by
    simpa only [forgetOrder_val] using congrArg (fun w : AdmissibleWitness N => w.val.val) h
  rcases pair_equal_cases (before_ne p.property.1) (before_ne q.property.1) he with hh | hh
  · exact Subtype.ext (Prod.ext hh.1 hh.2)
  · have hrev : Before p.val.2 p.val.1 := by
      simpa only [hh.1, hh.2] using q.property.1
    exact False.elim (before_asymm p.property.1 hrev)

theorem forgetOrder_surjective : Function.Surjective (@forgetOrder N) := by
  classical
  intro w
  obtain ⟨s, t, hst, hpair⟩ := Finset.card_eq_two.mp w.val.property.1
  have hs : s ∈ w.val.val := by rw [hpair]; simp
  have ht : t ∈ w.val.val := by rw [hpair]; simp
  rcases before_total hst with hbefore | hbefore
  · refine ⟨⟨(s,t), hbefore, w.val.property.2 s hs t ht, w.property s hs t ht⟩, ?_⟩
    apply Subtype.ext
    apply Subtype.ext
    simpa only [forgetOrder_val] using hpair.symm
  · refine ⟨⟨(t,s), hbefore, w.val.property.2 t ht s hs, w.property t ht s hs⟩, ?_⟩
    apply Subtype.ext
    apply Subtype.ext
    simpa only [forgetOrder_val, Finset.pair_comm] using hpair.symm

noncomputable def orderedWitnessEquiv : OrderedWitness N ≃ AdmissibleWitness N :=
  Equiv.ofBijective forgetOrder ⟨forgetOrder_injective, forgetOrder_surjective⟩

abbrev TColor := {p : ColorPair × ColorPair //
  colorRank p.1 < colorRank p.2 ∧ ¬Disjoint p.1.val p.2.val}
abbrev QColor := {p : ColorPair × ColorPair //
  colorRank p.1 < colorRank p.2 ∧ Disjoint p.1.val p.2.val}
abbrev ForkColor := {p : ColorPair × ColorPair // Disjoint p.1.val p.2.val}
abbrev IncreasingEndpoints (N : Nat) := {p : Fin N × Fin N // p.1 < p.2}

/-- Explicit normal forms, not aliases of the actual graph Witness. -/
abbrev TNormal (N : Nat) := (Fin N × Fin N) × TColor
abbrev QNormal (N : Nat) := (Fin N × Fin N) × QColor
abbrev LNormal (N : Nat) := Fin N × IncreasingEndpoints N × ForkColor
abbrev RNormal (N : Nat) := Fin N × IncreasingEndpoints N × ForkColor
abbrev Normal (N : Nat) := TNormal N ⊕ (QNormal N ⊕ (LNormal N ⊕ RNormal N))

noncomputable def decodeNormal : Normal N → OrderedWitness N
  | .inl a => ⟨((a.1.1,a.1.2,a.2.val.1), (a.1.1,a.1.2,a.2.val.2)),
      Or.inr ⟨rfl, Or.inr ⟨rfl, a.2.property.1⟩⟩,
      Or.inl rfl, compatible_same _ _ _ _⟩
  | .inr (.inl a) => ⟨((a.1.1,a.1.2,a.2.val.1), (a.1.1,a.1.2,a.2.val.2)),
      Or.inr ⟨rfl, Or.inr ⟨rfl, a.2.property.1⟩⟩,
      Or.inl rfl, compatible_same _ _ _ _⟩
  | .inr (.inr (.inl a)) =>
      ⟨((a.1,a.2.1.val.1,a.2.2.val.1), (a.1,a.2.1.val.2,a.2.2.val.2)),
       Or.inr ⟨rfl, Or.inl a.2.1.property⟩, Or.inl rfl,
       compatible_of_disjoint _ _ a.2.2.property⟩
  | .inr (.inr (.inr a)) =>
      ⟨((a.2.1.val.1,a.1,a.2.2.val.1), (a.2.1.val.2,a.1,a.2.2.val.2)),
       Or.inl a.2.1.property, Or.inr rfl,
       compatible_of_disjoint _ _ a.2.2.property⟩

noncomputable def encodeNormal (p : OrderedWitness N) : Normal N := by
  classical
  let s := p.val.1
  let t := p.val.2
  by_cases hx : s.1 = t.1
  · by_cases hy : s.2.1 = t.2.1
    · have hc : colorRank s.2.2 < colorRank t.2.2 := by
        have h := p.property.1
        change Before s t at h
        rcases h with h | ⟨_, h | ⟨_, h⟩⟩
        · exact False.elim ((ne_of_lt h) hx)
        · exact False.elim ((ne_of_lt h) hy)
        · exact h
      by_cases hd : Disjoint s.2.2.val t.2.2.val
      · exact .inr (.inl ((s.1,s.2.1), ⟨(s.2.2,t.2.2),hc,hd⟩))
      · exact .inl ((s.1,s.2.1), ⟨(s.2.2,t.2.2),hc,hd⟩)
    · have hylt : s.2.1 < t.2.1 := by
        have h := p.property.1
        change Before s t at h
        rcases h with h | ⟨_, h | ⟨h, _⟩⟩
        · exact False.elim ((ne_of_lt h) hx)
        · exact h
        · exact False.elim (hy h)
      have hd := compatible_disjoint_of_endpoint_ne s t p.property.2.2 (Or.inr hy)
      exact .inr (.inr (.inl (s.1, ⟨(s.2.1,t.2.1),hylt⟩,
        ⟨(s.2.2,t.2.2),hd⟩)))
  · have hy : s.2.1 = t.2.1 := p.property.2.1.resolve_left hx
    have hxlt : s.1 < t.1 := by
      have h := p.property.1
      change Before s t at h
      exact h.resolve_right (fun h' => hx h'.1)
    have hd := compatible_disjoint_of_endpoint_ne s t p.property.2.2 (Or.inl hx)
    exact .inr (.inr (.inr (s.2.1, ⟨(s.1,t.1),hxlt⟩,
      ⟨(s.2.2,t.2.2),hd⟩)))

theorem decode_encode (p : OrderedWitness N) : decodeNormal (encodeNormal p) = p := by
  classical
  rcases p with ⟨⟨⟨x,y,a⟩,⟨z,v,b⟩⟩, hb, hs, hc⟩
  apply Subtype.ext
  by_cases hx : x = z
  · subst z
    by_cases hy : y = v
    · subst v
      by_cases hd : Disjoint a.val b.val <;> simp [encodeNormal, decodeNormal, hd]
    · simp [encodeNormal, decodeNormal, hy]
  · have hy : y = v := hs.resolve_left hx
    subst v
    simp [encodeNormal, decodeNormal, hx]

theorem encode_decode (a : Normal N) : encodeNormal (decodeNormal a) = a := by
  classical
  rcases a with a | a | a | a
  · rcases a with ⟨⟨x,y⟩,⟨⟨c,d⟩,hcd,hd⟩⟩
    simp [decodeNormal, encodeNormal, hd]
  · rcases a with ⟨⟨x,y⟩,⟨⟨c,d⟩,hcd,hd⟩⟩
    simp [decodeNormal, encodeNormal, hd]
  · rcases a with ⟨x,⟨⟨y,z⟩,hyz⟩,⟨⟨c,d⟩,hd⟩⟩
    simp [decodeNormal, encodeNormal, ne_of_lt hyz]
  · rcases a with ⟨y,⟨⟨x,z⟩,hxz⟩,⟨⟨c,d⟩,hd⟩⟩
    simp [decodeNormal, encodeNormal, ne_of_lt hxz]

noncomputable def orderedNormalEquiv : OrderedWitness N ≃ Normal N where
  toFun := encodeNormal
  invFun := decodeNormal
  left_inv := decode_encode
  right_inv := encode_decode

noncomputable def witnessNormalEquiv : AdmissibleWitness N ≃ Normal N :=
  orderedWitnessEquiv.symm.trans orderedNormalEquiv

/-- Every realized witness is admissible; no mass is lost by this reindexing. -/
noncomputable def incidenceAdmissibleEquiv :
    {t : Omega N × Witness N // Rel t.1 t.2} ≃
      (Σ w : AdmissibleWitness N, {omega : Omega N // Rel omega w.val}) where
  toFun t := ⟨⟨t.val.2, realized_admissible t.val.1 t.val.2 t.property⟩,
    ⟨t.val.1,t.property⟩⟩
  invFun t := ⟨(t.2.val,t.1.val),t.2.property⟩
  left_inv _ := Subtype.ext rfl
  right_inv t := by rcases t with ⟨⟨w,hw⟩,⟨omega,h⟩⟩; rfl

/-- Constructed table -> C33 -> C32 exact event count, not a class-count oracle. -/
theorem normal_event_count (a : Normal N) :
    Nat.card {omega : Omega N // Rel omega (witnessNormalEquiv.symm a).val} =
      ∏ c, factor N (normalizedTable (witnessNormalEquiv.symm a).val c) :=
  admissible_event_count (witnessNormalEquiv.symm a).val
    (witnessNormalEquiv.symm a).property

noncomputable def endpointChoose (p : IncreasingEndpoints N) :
    R10.Parallel22.C34.Indices.Choose N 2 := by
  classical
  refine ⟨{p.val.1,p.val.2}, ?_⟩
  apply Finset.mem_powersetCard.mpr
  exact ⟨Finset.subset_univ _, by simp [ne_of_lt p.property]⟩

noncomputable def endpointChooseEquiv : IncreasingEndpoints N ≃
    R10.Parallel22.C34.Indices.Choose N 2 := by
  classical
  apply Equiv.ofBijective endpointChoose
  constructor
  · intro p q h
    have hp : ({p.val.1,p.val.2} : Finset (Fin N)) = {q.val.1,q.val.2} :=
      congrArg Subtype.val h
    rcases pair_equal_cases (ne_of_lt p.property) (ne_of_lt q.property) hp with hh | hh
    · exact Subtype.ext (Prod.ext hh.1 hh.2)
    · have hrev : p.val.2 < p.val.1 := by
        simpa only [hh.1,hh.2] using q.property
      exact False.elim (lt_asymm p.property hrev)
  · intro s
    have hcard : s.val.card = 2 := (Finset.mem_powersetCard.mp s.property).2
    obtain ⟨x,y,hxy,hpair⟩ := Finset.card_eq_two.mp hcard
    rcases lt_or_gt_of_ne hxy with hlt | hlt
    · refine ⟨⟨(x,y),hlt⟩, ?_⟩
      exact Subtype.ext hpair.symm
    · refine ⟨⟨(y,x),hlt⟩, ?_⟩
      apply Subtype.ext
      simpa only [Finset.pair_comm] using hpair.symm

theorem increasingEndpoints_card : Nat.card (IncreasingEndpoints N) = N.choose 2 := by
  classical
  rw [Nat.card_congr endpointChooseEquiv, Nat.card_eq_fintype_card]
  exact R10.Parallel22.C34.Indices.card_choose N 2

end R10.Parallel22.C35
