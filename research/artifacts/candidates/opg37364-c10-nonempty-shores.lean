/- C10 formalization slice. Verdict: candidate_only.
   This file has not been compiled or checked by a proof assistant.
   It encodes only the nonempty-shore obstruction and an empty-cut witness,
   not graph cardinality, average degree, girth, or the full frozen root.
   No explicit imports are requested. Toolchain authorization is separate.
-/

namespace Opg37364.C10

universe u

def UsesBoth {V : Type u} (c : V → Bool) : Prop :=
  (∃ a : V, c a = false) ∧ (∃ b : V, c b = true)

def HasTwoShoreColouring (V : Type u) : Prop :=
  ∃ c : V → Bool, UsesBoth c

def LocalMatching {V : Type u} (Adj : V → V → Prop)
    (c : V → Bool) : Prop :=
  ∀ v a b : V, Adj v a → Adj v b →
    c a ≠ c v → c b ≠ c v → a = b

def HasMatchingCut (V : Type u) (Adj : V → V → Prop) : Prop :=
  ∃ c : V → Bool, UsesBoth c ∧ LocalMatching Adj c

theorem matching_cut_implies_two_shores {V : Type u}
    {Adj : V → V → Prop} :
    HasMatchingCut V Adj → HasTwoShoreColouring V := by
  intro h
  cases h with
  | intro c hc =>
    exact ⟨c, hc.left⟩

theorem no_two_shores_of_at_most_one {V : Type u}
    (hcard : ∀ a b : V, a = b) :
    ¬ HasTwoShoreColouring V := by
  intro h
  cases h with
  | intro c hc =>
    cases hc.left with
    | intro a ha =>
      cases hc.right with
      | intro b hb =>
        have hab : c a = c b := congrArg c (hcard a b)
        have hbad : (false : Bool) = true :=
          Eq.trans (Eq.symm ha) (Eq.trans hab hb)
        cases hbad

theorem no_matching_cut_of_at_most_one {V : Type u}
    (hcard : ∀ a b : V, a = b) (Adj : V → V → Prop) :
    ¬ HasMatchingCut V Adj := by
  intro h
  exact no_two_shores_of_at_most_one hcard
    (matching_cut_implies_two_shores h)

theorem unit_at_most_one : ∀ a b : Unit, a = b := by
  intro a b
  cases a
  cases b
  rfl

def K1Adj (_ _ : Unit) : Prop := False

theorem no_k1_matching_cut : ¬ HasMatchingCut Unit K1Adj :=
  no_matching_cut_of_at_most_one unit_at_most_one K1Adj

theorem edgeless_bool_has_matching_cut :
    HasMatchingCut Bool (fun _ _ => False) := by
  exact ⟨(fun b : Bool => b),
    ⟨⟨false, rfl⟩, ⟨true, rfl⟩⟩,
    (fun _ _ _ h _ _ _ => False.elim h)⟩

end Opg37364.C10

#print axioms Opg37364.C10.no_two_shores_of_at_most_one
#print axioms Opg37364.C10.no_k1_matching_cut
#print axioms Opg37364.C10.edgeless_bool_has_matching_cut
