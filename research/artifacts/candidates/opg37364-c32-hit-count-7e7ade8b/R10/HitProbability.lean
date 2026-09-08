import R10.HitCounts

/-
C32 source candidate, not a claimed compilation.
Natural subtraction in counts is distinguished from rational subtraction
in the displayed probability. When k>b the product is zero, not a product
of factors that are all nonnegative. The proof splits this case explicitly.
-/

namespace R10.Hits
open scoped BigOperators

/-- Falling factorial as a product of natural-number differences. -/
theorem descFactorial_natCast_prod (n k : Nat) :
    (n.descFactorial k : ℚ) = ∏ i ∈ Finset.range k, ((n - i : Nat) : ℚ) := by
  induction k with
  | zero => simp
  | succ k ih =>
    simp only [Nat.descFactorial_succ, Nat.cast_mul, Finset.prod_range_succ, ih]
    ring

/-- Rational subtraction agrees after taking the whole product, even for k>n. -/
theorem descFactorial_rat_prod (n k : Nat) :
    (n.descFactorial k : ℚ) = ∏ i ∈ Finset.range k, ((n : ℚ) - (i : ℚ)) := by
  by_cases hk : k ≤ n
  · rw [descFactorial_natCast_prod]
    apply Finset.prod_congr rfl
    intro i hi
    have hin : i ≤ n := le_trans (Nat.le_of_lt (Finset.mem_range.mp hi)) hk
    exact Nat.cast_sub hin
  · have hnk : n < k := Nat.lt_of_not_ge hk
    rw [Nat.descFactorial_of_lt hnk, Nat.cast_zero]
    symm
    apply Finset.prod_eq_zero (Finset.mem_range.mpr hnk)
    simp

/-- An embedding of k distinct inputs supplies the necessary k<=N premise. -/
theorem input_count_le {N k : Nat} (u : Fin k ↪ Fin N) : k ≤ N := by
  simpa using Fintype.card_le_of_injective u u.injective

/-- Cancellation uses positive factorials, never division by a zero factorial. -/
theorem factorial_ratio_eq_product (N b k : Nat) (hk : k ≤ N) :
    ((b.descFactorial k : ℚ) * ((N - k).factorial : ℚ)) / (N.factorial : ℚ) =
      ∏ i ∈ Finset.range k, ((b : ℚ) - (i : ℚ)) / ((N : ℚ) - (i : ℚ)) := by
  have hf : (((N - k).factorial : Nat) : ℚ) ≠ 0 := by
    exact_mod_cast Nat.factorial_ne_zero (N - k)
  have hdNat : N.descFactorial k ≠ 0 := by
    intro hz
    exact (Nat.not_lt.mpr hk) (Nat.descFactorial_eq_zero_iff_lt.mp hz)
  have hd : (N.descFactorial k : ℚ) ≠ 0 := by exact_mod_cast hdNat
  have hfac : (((N - k).factorial : Nat) : ℚ) * (N.descFactorial k : ℚ) =
      (N.factorial : ℚ) := by
    exact_mod_cast Nat.factorial_mul_descFactorial hk
  rw [Finset.prod_div_distrib, ← descFactorial_rat_prod b k,
    ← descFactorial_rat_prod N k, ← hfac]
  field_simp [hf, hd]
  <;> ring

/-- The probability is a ratio in the finite permutation sample space. -/
theorem hit_probability_eq_product {N k : Nat}
    (u : Fin k ↪ Fin N) (B : Finset (Fin N)) :
    (Fintype.card (Hit u B) : ℚ) / (N.factorial : ℚ) =
      ∏ i ∈ Finset.range k,
        ((B.card : ℚ) - (i : ℚ)) / ((N : ℚ) - (i : ℚ)) := by
  rw [card_hit, Nat.cast_mul]
  exact factorial_ratio_eq_product N B.card k (input_count_le u)

/-- A single nonnegative without-replacement factor is at most b/N. -/
theorem slot_ratio_le (N b i : Nat) (hi : i < b) (hb : b ≤ N) :
    ((b : ℚ) - (i : ℚ)) / ((N : ℚ) - (i : ℚ)) ≤ (b : ℚ) / N := by
  have hNi : (i : ℚ) < N := by exact_mod_cast lt_of_lt_of_le hi hb
  have hN : (0 : ℚ) < N := lt_of_le_of_lt (Nat.cast_nonneg i) hNi
  have hden : (0 : ℚ) < (N : ℚ) - i := sub_pos.mpr hNi
  have hBN : (b : ℚ) ≤ N := by exact_mod_cast hb
  have hi0 : (0 : ℚ) ≤ i := Nat.cast_nonneg i
  apply (div_le_div_iff₀ hden hN).mpr
  nlinarith [mul_nonneg hi0 (sub_nonneg.mpr hBN)]

/-- Includes k=0 and N=0. The k>b case is proved by a zero factor. -/
theorem without_replacement_le (N b k : Nat) (hb : b ≤ N) (hk : k ≤ N) :
    (∏ i ∈ Finset.range k, ((b : ℚ) - (i : ℚ)) / ((N : ℚ) - (i : ℚ))) ≤
      ((b : ℚ) / N) ^ k := by
  by_cases hkb : k ≤ b
  · calc
      _ ≤ ∏ _i ∈ Finset.range k, (b : ℚ) / N := by
        apply Finset.prod_le_prod
        · intro i hi
          have hib : i < b := lt_of_lt_of_le (Finset.mem_range.mp hi) hkb
          have hiN : i < N := lt_of_lt_of_le hib hb
          apply div_nonneg
          · exact sub_nonneg.mpr (by exact_mod_cast Nat.le_of_lt hib)
          · exact sub_nonneg.mpr (by exact_mod_cast Nat.le_of_lt hiN)
        · intro i hi
          exact slot_ratio_le N b i
            (lt_of_lt_of_le (Finset.mem_range.mp hi) hkb) hb
      _ = _ := by simp
  · have hbk : b < k := Nat.lt_of_not_ge hkb
    have hz : (∏ i ∈ Finset.range k,
        ((b : ℚ) - (i : ℚ)) / ((N : ℚ) - (i : ℚ))) = 0 := by
      apply Finset.prod_eq_zero (Finset.mem_range.mpr hbk)
      simp
    rw [hz]
    positivity

/-- Count and probability are connected, not separate asserted interfaces. -/
theorem hit_probability_le {N k : Nat} (u : Fin k ↪ Fin N)
    (B : Finset (Fin N)) :
    (Fintype.card (Hit u B) : ℚ) / (N.factorial : ℚ) ≤
      ((B.card : ℚ) / N) ^ k := by
  rw [hit_probability_eq_product]
  apply without_replacement_le
  · simpa using Finset.card_le_univ B
  · exact input_count_le u

/-- Exactly twenty-four coordinate factors; no factorization of slots. -/
theorem tuple24_probability_le (N : Nat) (ks : Fin 24 → Nat)
    (us : ∀ j, Fin (ks j) ↪ Fin N) (Bs : Fin 24 → Finset (Fin N)) :
    (Fintype.card {f : Fin 24 → Equiv.Perm (Fin N) //
        ∀ j i, f j (us j i) ∈ Bs j} : ℚ) / (N.factorial : ℚ)^24 ≤
      ∏ j, (((Bs j).card : ℚ) / N)^(ks j) := by
  classical
  calc
    _ = ∏ j, (Fintype.card (Hit (us j) (Bs j)) : ℚ) / (N.factorial : ℚ) := by
      rw [Fintype.card_congr (tupleEquiv N 24 ks us Bs), Fintype.card_pi]
      simp only [Nat.cast_prod, Finset.prod_div_distrib, Finset.prod_const,
        Finset.card_univ, Fintype.card_fin]
    _ ≤ _ := by
      apply Finset.prod_le_prod
      · intro j _
        positivity
      · intro j _
        exact hit_probability_le (us j) (Bs j)

end R10.Hits
