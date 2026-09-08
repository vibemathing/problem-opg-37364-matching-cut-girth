import R10.ProductCounts
import Mathlib.Data.Fintype.CardEmbedding
import Mathlib.Tactic

/-
C32 source candidate. Compilation status is exclusively in the replay record.
This module does not assume independent slots of a single permutation.
It imports the frozen C31 factorial-completion theorem, not a replacement axiom.
-/

namespace R10.Hits
open scoped BigOperators
open R10.Cardinality

variable {N k : Nat}

/-- The image of an embedding, with the actual embedding as an equivalence. -/
noncomputable def imageEquiv {I A : Type*} (u : I ↪ A) :
    I ≃ {x : A // ∃ i, u i = x} :=
  Equiv.ofBijective (fun i => (⟨u i, ⟨i, rfl⟩⟩ : {x : A // ∃ i, u i = x})) (by
    constructor
    · intro i j h
      exact u.injective (congrArg Subtype.val h)
    · rintro ⟨x, i, rfl⟩
      exact ⟨i, rfl⟩)

@[simp] theorem imageEquiv_apply {I A : Type*} (u : I ↪ A) (i : I) :
    (imageEquiv u i).val = u i := rfl

noncomputable def prescription (u w : Fin k ↪ Fin N) :
    {x // ∃ i, u i = x} ≃ {y // ∃ i, w i = y} :=
  (imageEquiv u).symm.trans (imageEquiv w)

@[simp] theorem prescription_apply (u w : Fin k ↪ Fin N) (i : Fin k) :
    (prescription u w (imageEquiv u i)).val = w i := by
  change (imageEquiv w ((imageEquiv u).symm (imageEquiv u i))).val = w i
  rw [(imageEquiv u).symm_apply_apply]
  rfl

/-- A permutation realizing an ordered compatible list of input/output pairs. -/
def Assigned (u w : Fin k ↪ Fin N) :=
  {f : Equiv.Perm (Fin N) // ∀ i, f (u i) = w i}

noncomputable instance assignedFintype (u w : Fin k ↪ Fin N) :
    Fintype (Assigned u w) := by
  classical
  unfold Assigned
  infer_instance

/-- The ordered-pair description is exactly C31's region description. -/
noncomputable def assignedEquivCompletion (u w : Fin k ↪ Fin N) :
    Assigned u w ≃
      Completion (fun x => ∃ i, u i = x) (fun y => ∃ i, w i = y)
        (prescription u w) where
  toFun f := ⟨f.val, by
    intro x
    obtain ⟨i, hi⟩ := x.property
    have hx : x = imageEquiv u i := Subtype.ext hi.symm
    rw [hx]
    exact (f.property i).trans (prescription_apply u w i).symm⟩
  invFun f := ⟨f.val, by
    intro i
    exact (f.property (imageEquiv u i)).trans (prescription_apply u w i)⟩
  left_inv _ := Subtype.ext rfl
  right_inv _ := Subtype.ext rfl

/-- This is a direct use of the existing card_fin_completion. -/
theorem card_assigned (u w : Fin k ↪ Fin N) :
    Fintype.card (Assigned u w) = (N - k).factorial := by
  classical
  rw [Fintype.card_congr (assignedEquivCompletion u w)]
  apply card_fin_completion N k _ _ (prescription u w)
  simpa using (Fintype.card_congr (imageEquiv u)).symm

/-- All the distinct specified inputs land in the fixed target subset. -/
def Hit (u : Fin k ↪ Fin N) (B : Finset (Fin N)) :=
  {f : Equiv.Perm (Fin N) // ∀ i, f (u i) ∈ B}

noncomputable instance hitFintype (u : Fin k ↪ Fin N) (B : Finset (Fin N)) :
    Fintype (Hit u B) := by
  classical
  unfold Hit
  infer_instance

/-- Keep the injective choice of outputs, rather than treating them as slots. -/
def restriction (u : Fin k ↪ Fin N) (B : Finset (Fin N)) (f : Hit u B) :
    Fin k ↪ B where
  toFun i := ⟨f.val (u i), f.property i⟩
  inj' _ _ h := u.injective (f.val.injective (congrArg Subtype.val h))

def forgetTarget (B : Finset (Fin N)) (v : Fin k ↪ B) : Fin k ↪ Fin N where
  toFun i := (v i).val
  inj' _ _ h := v.injective (Subtype.ext h)

def restoreHit (u : Fin k ↪ Fin N) (B : Finset (Fin N))
    (v : Fin k ↪ B) (f : Assigned u (forgetTarget B v)) : Hit u B :=
  ⟨f.val, by
    intro i
    rw [f.property i]
    exact (v i).property⟩

/-- A hit permutation determines one image injection and one of its completions. -/
noncomputable def hitEquivSigma (u : Fin k ↪ Fin N) (B : Finset (Fin N)) :
    Hit u B ≃ (Σ v : Fin k ↪ B, Assigned u (forgetTarget B v)) where
  toFun f := ⟨restriction u B f, ⟨f.val, fun _ => rfl⟩⟩
  invFun t := restoreHit u B t.1 t.2
  left_inv _ := Subtype.ext rfl
  right_inv t := by
    rcases t with ⟨v, f⟩
    have hv : restriction u B (restoreHit u B v f) = v := by
      apply Function.Embedding.ext
      intro i
      apply Subtype.ext
      exact f.property i
    apply Sigma.ext hv
    apply (Subtype.heq_iff_coe_eq ?_).mpr
    · intro pi
      change (∀ i, pi (u i) = forgetTarget B (restriction u B (restoreHit u B v f)) i) ↔
        (∀ i, pi (u i) = forgetTarget B v i)
      rw [hv]
    · rfl

/-- Exact without-replacement hit count; valid also when B.card < k. -/
theorem card_hit (u : Fin k ↪ Fin N) (B : Finset (Fin N)) :
    Fintype.card (Hit u B) = B.card.descFactorial k * (N - k).factorial := by
  classical
  calc
    Fintype.card (Hit u B) =
        Fintype.card (Σ v : Fin k ↪ B, Assigned u (forgetTarget B v)) :=
      Fintype.card_congr (hitEquivSigma u B)
    _ = ∑ v : Fin k ↪ B, Fintype.card (Assigned u (forgetTarget B v)) :=
      Fintype.card_sigma
    _ = ∑ _v : Fin k ↪ B, (N - k).factorial := by
      apply Finset.sum_congr rfl
      intro v _
      exact card_assigned u (forgetTarget B v)
    _ = B.card.descFactorial k * (N - k).factorial := by
      simp [Fintype.card_embedding_eq]

/-- The empty family of image injections makes the count zero. -/
theorem card_hit_of_target_small (u : Fin k ↪ Fin N) (B : Finset (Fin N))
    (h : B.card < k) : Fintype.card (Hit u B) = 0 := by
  rw [card_hit, Nat.descFactorial_of_lt h, zero_mul]

@[simp] theorem card_hit_zero (u : Fin 0 ↪ Fin N) (B : Finset (Fin N)) :
    Fintype.card (Hit u B) = N.factorial := by
  simp [card_hit]

/-- The k=N endpoint has no hidden nonempty-complement assumption. -/
theorem card_hit_all_inputs (u : Fin N ↪ Fin N) (B : Finset (Fin N)) :
    Fintype.card (Hit u B) = if B.card = N then N.factorial else 0 := by
  by_cases h : B.card = N
  · simp [card_hit, h, Nat.descFactorial_self]
  · rw [if_neg h]
    apply card_hit_of_target_small
    have hle : B.card ≤ N := by simpa using (Finset.card_le_univ B)
    omega

/-- Includes the unique permutation on the empty set. -/
example (u : Fin 0 ↪ Fin 0) (B : Finset (Fin 0)) :
    Fintype.card (Hit u B) = 1 := by simp

/-- A dependent family of hit permutations is exactly a constrained full tuple. -/
noncomputable def tupleEquiv (N r : Nat) (ks : Fin r → Nat)
    (us : ∀ j, Fin (ks j) ↪ Fin N) (Bs : Fin r → Finset (Fin N)) :
    {f : Fin r → Equiv.Perm (Fin N) // ∀ j i, f j (us j i) ∈ Bs j} ≃
      (∀ j, Hit (us j) (Bs j)) where
  toFun f j := ⟨f.val j, f.property j⟩
  invFun f := ⟨fun j => (f j).val, fun j => (f j).property⟩
  left_inv _ := Subtype.ext rfl
  right_inv f := by funext j; exact Subtype.ext rfl

/-- Only Cartesian coordinates factorize; there is no within-permutation independence. -/
theorem card_hit_tuple (N r : Nat) (ks : Fin r → Nat)
    (us : ∀ j, Fin (ks j) ↪ Fin N) (Bs : Fin r → Finset (Fin N)) :
    Fintype.card {f : Fin r → Equiv.Perm (Fin N) // ∀ j i, f j (us j i) ∈ Bs j} =
      ∏ j, (Bs j).card.descFactorial (ks j) * (N - ks j).factorial := by
  classical
  rw [Fintype.card_congr (tupleEquiv N r ks us Bs), Fintype.card_pi]
  apply Finset.prod_congr rfl
  intro j _
  exact card_hit (us j) (Bs j)

/-- The twenty-four-coordinate sample space used by C20. -/
theorem card_hit_tuple24 (N : Nat) (ks : Fin 24 → Nat)
    (us : ∀ j, Fin (ks j) ↪ Fin N) (Bs : Fin 24 → Finset (Fin N)) :
    Fintype.card {f : Fin 24 → Equiv.Perm (Fin N) // ∀ j i, f j (us j i) ∈ Bs j} =
      ∏ j, (Bs j).card.descFactorial (ks j) * (N - ks j).factorial :=
  card_hit_tuple N 24 ks us Bs

/-- Directly reuses C31's surjective incidence projection with the correct direction. -/
theorem badCut_le_incidence {S : Type*} [Fintype S] (N : Nat)
    (R : (Fin 24 → Equiv.Perm (Fin N)) → S → Prop) :
    Nat.card {w : Fin 24 → Equiv.Perm (Fin N) // ∃ s, R w s} ≤
      Nat.card {t : (Fin 24 → Equiv.Perm (Fin N)) × S // R t.1 t.2} := by
  classical
  simpa [Nat.card_eq_fintype_card] using
    (R10.Cardinality.bad_objects_le_incidences R)

end R10.Hits
