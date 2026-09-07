import Mathlib.Data.Fintype.Perm

/-
Candidate source. This file has not been elaborated in the current runtime.
It is not the unavailable source mentioned in the earlier Issue checkpoint.
No nonempty-complement or chosen-default-point hypothesis is used.
-/

namespace R10.Cardinality

universe u v
variable {A : Type u} {B : Type v}
variable (p : A → Prop) (q : B → Prop)

/-- A completion of a specified bijection between the prescribed regions. -/
def Completion (e : {x // p x} ≃ {y // q y}) :=
  { f : A ≃ B // ∀ x : {x // p x}, f x.val = (e x).val }

/-- Every total completion maps precisely the prescribed region to its image. -/
theorem preservesRegion (e : {x // p x} ≃ {y // q y})
    (f : Completion p q e) (x : A) : q (f.val x) ↔ p x := by
  constructor
  · intro hq
    let y : {y // q y} := ⟨f.val x, hq⟩
    have hfx : f.val (e.symm y).val = f.val x := by
      calc
        f.val (e.symm y).val = (e (e.symm y)).val := f.property (e.symm y)
        _ = y.val := congrArg Subtype.val (e.apply_symm_apply y)
        _ = f.val x := rfl
    have heq : (e.symm y).val = x := f.val.injective hfx
    simpa only [heq] using (e.symm y).property
  · intro hp
    have hfx := f.property ⟨x, hp⟩
    rw [hfx]
    exact (e ⟨x, hp⟩).property

/-- Restriction of a completion to the exact complementary regions. -/
def restrictComplement (e : {x // p x} ≃ {y // q y})
    (f : Completion p q e) : {x // ¬p x} ≃ {y // ¬q y} where
  toFun x := ⟨f.val x.val, fun hq => x.property ((preservesRegion p q e f x.val).mp hq)⟩
  invFun y := ⟨f.val.symm y.val, by
    intro hp
    apply y.property
    have hq := (preservesRegion p q e f (f.val.symm y.val)).mpr hp
    simpa only [f.val.apply_symm_apply] using hq⟩
  left_inv x := Subtype.ext (f.val.symm_apply_apply x.val)
  right_inv y := Subtype.ext (f.val.apply_symm_apply y.val)

/-- Glue the prescribed bijection and an arbitrary complement bijection. -/
noncomputable def assemble (e : {x // p x} ≃ {y // q y})
    (h : {x // ¬p x} ≃ {y // ¬q y}) : A ≃ B := by
  classical
  exact {
    toFun := fun x => if hx : p x then (e ⟨x, hx⟩).val else (h ⟨x, hx⟩).val
    invFun := fun y => if hy : q y then (e.symm ⟨y, hy⟩).val else (h.symm ⟨y, hy⟩).val
    left_inv := by
      intro x
      by_cases hx : p x
      · simp only [dif_pos hx, dif_pos (e ⟨x, hx⟩).property]
        exact congrArg Subtype.val (e.symm_apply_apply ⟨x, hx⟩)
      · simp only [dif_neg hx, dif_neg (h ⟨x, hx⟩).property]
        exact congrArg Subtype.val (h.symm_apply_apply ⟨x, hx⟩)
    right_inv := by
      intro y
      by_cases hy : q y
      · simp only [dif_pos hy, dif_pos (e.symm ⟨y, hy⟩).property]
        exact congrArg Subtype.val (e.apply_symm_apply ⟨y, hy⟩)
      · simp only [dif_neg hy, dif_neg (h.symm ⟨y, hy⟩).property]
        exact congrArg Subtype.val (h.apply_symm_apply ⟨y, hy⟩)
  }

noncomputable def assembleCompletion (e : {x // p x} ≃ {y // q y})
    (h : {x // ¬p x} ≃ {y // ¬q y}) : Completion p q e := by
  classical
  refine ⟨assemble p q e h, ?_⟩
  intro x
  change (if hx : p x.val then (e ⟨x.val, hx⟩).val else (h ⟨x.val, hx⟩).val) = (e x).val
  simp only [dif_pos x.property]

/-- No enumeration or finite testing is used for either inverse law. -/
theorem restrict_assemble (e : {x // p x} ≃ {y // q y})
    (h : {x // ¬p x} ≃ {y // ¬q y}) :
    restrictComplement p q e (assembleCompletion p q e h) = h := by
  classical
  apply Equiv.ext
  intro x
  apply Subtype.ext
  change (if hx : p x.val then (e ⟨x.val, hx⟩).val else (h ⟨x.val, hx⟩).val) = (h x).val
  simp only [dif_neg x.property]

theorem assemble_restrict (e : {x // p x} ≃ {y // q y})
    (f : Completion p q e) :
    assembleCompletion p q e (restrictComplement p q e f) = f := by
  classical
  apply Subtype.ext
  apply Equiv.ext
  intro x
  change (if hx : p x then (e ⟨x, hx⟩).val
      else ((restrictComplement p q e f) ⟨x, hx⟩).val) = f.val x
  by_cases hx : p x
  · rw [dif_pos hx]
    exact (f.property ⟨x, hx⟩).symm
  · rw [dif_neg hx]
    rfl

/-- The source-level bridge required before counting completions. -/
noncomputable def completionEquiv (e : {x // p x} ≃ {y // q y}) :
    Completion p q e ≃ ({x // ¬p x} ≃ {y // ¬q y}) where
  toFun := restrictComplement p q e
  invFun := assembleCompletion p q e
  left_inv := assemble_restrict p q e
  right_inv := restrict_assemble p q e

end R10.Cardinality
