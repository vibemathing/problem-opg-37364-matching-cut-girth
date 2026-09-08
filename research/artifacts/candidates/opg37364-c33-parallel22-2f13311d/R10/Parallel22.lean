import R10.HitProbability

/- C33 portable source candidate. No elaboration is claimed.
The T/Q/L/R classification and its index cardinalities are proved in proof.md,
not silently imported as assumptions into this finite interface. -/
namespace R10.Parallel22
open scoped BigOperators

abbrev Omega (N : Nat) := Fin 24 → Equiv.Perm (Fin N)
abbrev ColorPair := {s : Finset (Fin 24) // s.card = 2}
abbrev Cycle2 (N : Nat) := Fin N × Fin N × ColorPair

def shares {N : Nat} (s t : Cycle2 N) : Prop :=
  s.1 = t.1 ∨ s.2.1 = t.2.1

/-- Unordered DISTINCT cycle pairs; diagonal pairs are excluded by card=2. -/
def Witness (N : Nat) :=
  {p : Finset (Cycle2 N) // p.card = 2 ∧ ∀ s ∈ p, ∀ t ∈ p, shares s t}

noncomputable instance witnessFintype (N : Nat) : Fintype (Witness N) := by
  classical
  unfold Witness
  infer_instance

def Rel {N : Nat} (omega : Omega N) (w : Witness N) : Prop :=
  ∀ s ∈ w.val, ∀ c ∈ s.2.2.val, omega c s.1 = s.2.1

/-- Incidence projects ONTO bad objects, not the reverse cardinal inequality. -/
theorem bad22_le_incidence (N : Nat) :
    Nat.card {omega : Omega N // ∃ w : Witness N, Rel omega w} ≤
      Nat.card {t : Omega N × Witness N // Rel t.1 t.2} := by
  classical
  exact R10.Hits.badCut_le_incidence N Rel

/-- Set union removes the duplicated common edge before counting constraints. -/
def requirements {N : Nat} (w : Witness N) (c : Fin 24) : Finset (Fin N × Fin N) :=
  w.val.biUnion fun s => if c ∈ s.2.2.val then {(s.1, s.2.1)} else ∅

theorem rel_iff_requirements {N : Nat} (omega : Omega N) (w : Witness N) :
    Rel omega w ↔ ∀ c e, e ∈ requirements w c → omega c e.1 = e.2 := by
  constructor
  · intro hw c e he
    rcases Finset.mem_biUnion.mp he with ⟨s, hs, he⟩
    by_cases hc : c ∈ s.2.2.val
    · have heq : e = (s.1, s.2.1) := by simpa only [if_pos hc, Finset.mem_singleton] using he
      subst e
      exact hw s hs c hc
    · simp only [if_neg hc, Finset.not_mem_empty] at he
  · intro h s hs c hc
    apply h c (s.1, s.2.1)
    exact Finset.mem_biUnion.mpr ⟨s, hs, by simp only [if_pos hc, Finset.mem_singleton]⟩

variable {N : Nat}

def emptyInput : Fin 0 ↪ Fin N where
  toFun := Fin.elim0
  inj' := by intro i; exact Fin.elim0 i

def oneInput (x : Fin N) : Fin 1 ↪ Fin N where
  toFun := fun _ => x
  inj' := by intro i j _; exact Subsingleton.elim i j

abbrev Table (N : Nat) := Fin 24 → Option (Fin N × Fin N)

def K : Option (Fin N × Fin N) → Nat
  | none => 0
  | some _ => 1

def U : (a : Option (Fin N × Fin N)) → Fin (K a) ↪ Fin N
  | none => emptyInput
  | some p => oneInput p.1

def B : Option (Fin N × Fin N) → Finset (Fin N)
  | none => Finset.univ
  | some p => {p.2}

def HasValue (pi : Equiv.Perm (Fin N)) : Option (Fin N × Fin N) → Prop
  | none => True
  | some p => pi p.1 = p.2

def factor (N : Nat) : Option (Fin N × Fin N) → Nat
  | none => N.factorial
  | some _ => (N-1).factorial

theorem local_iff (pi : Equiv.Perm (Fin N)) (a : Option (Fin N × Fin N)) :
    HasValue pi a ↔ ∀ i, pi (U a i) ∈ B a := by
  cases a with
  | none =>
    constructor
    · intro _ i; exact Fin.elim0 i
    · intro _; trivial
  | some p =>
    rcases p with ⟨x,y⟩
    constructor
    · intro h i
      change pi x ∈ ({y} : Finset (Fin N))
      exact Finset.mem_singleton.mpr h
    · intro h
      exact Finset.mem_singleton.mp (h (0 : Fin 1))

/-- An explicit full-tuple equivalence supplies C32's coordinate interface. -/
noncomputable def tableEquiv (a : Table N) :
    {omega : Omega N // ∀ c, HasValue (omega c) (a c)} ≃
      {omega : Omega N // ∀ c i, omega c (U (a c) i) ∈ B (a c)} where
  toFun f := ⟨f.val, fun c => (local_iff (f.val c) (a c)).mp (f.property c)⟩
  invFun f := ⟨f.val, fun c => (local_iff (f.val c) (a c)).mpr (f.property c)⟩
  left_inv _ := Subtype.ext rfl
  right_inv _ := Subtype.ext rfl

/-- One active coordinate uses card_hit with k=b=1, not an independent slot. -/
theorem card_singleton (x y : Fin N) :
    Fintype.card (R10.Hits.Hit (oneInput x) {y}) = (N-1).factorial := by
  rw [R10.Hits.card_hit]
  simp

/-- Exact product over all 24 coordinates, using the frozen C32 theorem. -/
theorem card_table (a : Table N) :
    Nat.card {omega : Omega N // ∀ c, HasValue (omega c) (a c)} =
      ∏ c, factor N (a c) := by
  classical
  rw [Nat.card_eq_fintype_card]
  calc
    _ = Fintype.card {omega : Omega N // ∀ c i, omega c (U (a c) i) ∈ B (a c)} :=
      Fintype.card_congr (tableEquiv a)
    _ = ∏ c, (B (a c)).card.descFactorial (K (a c)) * (N-K (a c)).factorial :=
      R10.Hits.card_hit_tuple24 N (fun c => K (a c)) (fun c => U (a c)) (fun c => B (a c))
    _ = ∏ c, factor N (a c) := by
      apply Finset.prod_congr rfl
      intro c _
      cases a c <;> simp [B, K, factor]

/-- Exact equality of normalized sets, not just an upper-cover relation. -/
def Encodes (a : Table N) (w : Witness N) : Prop :=
  ∀ c, requirements w c = match a c with | none => ∅ | some p => {p}

theorem encoded_event_iff (a : Table N) (w : Witness N) (ha : Encodes a w)
    (omega : Omega N) : Rel omega w ↔ ∀ c, HasValue (omega c) (a c) := by
  rw [rel_iff_requirements]
  constructor
  · intro h c
    cases hc : a c with
    | none => trivial
    | some p =>
      apply h c p
      rw [ha c, hc]
      exact Finset.mem_singleton_self p
  · intro h c e he
    rw [ha c] at he
    cases hc : a c with
    | none => simp only [hc, Finset.not_mem_empty] at he
    | some p =>
      have hp : e = p := by simpa only [hc, Finset.mem_singleton] using he
      subst e
      simpa only [hc, HasValue] using h c

/-- Applying this to T/Q/L/R requires their actual normalization, not an oracle. -/
theorem card_encoded_event (a : Table N) (w : Witness N) (ha : Encodes a w) :
    Nat.card {omega : Omega N // Rel omega w} = ∏ c, factor N (a c) := by
  classical
  calc
    _ = Nat.card {omega : Omega N // ∀ c, HasValue (omega c) (a c)} := by
      exact Nat.card_congr (Equiv.subtypeEquivRight (encoded_event_iff a w ha))
    _ = _ := card_table a

/-- Duplicate occurrences do not introduce a second random choice. -/
theorem duplicate_pair (pi : Equiv.Perm (Fin N)) (x y : Fin N) :
    (pi x = y ∧ pi x = y) ↔ pi x = y := by simp

theorem conflicting_input (pi : Equiv.Perm (Fin N)) (x y z : Fin N)
    (h : y ≠ z) : ¬ (pi x = y ∧ pi x = z) := by
  rintro ⟨h1,h2⟩
  exact h (h1.symm.trans h2)

theorem conflicting_output (pi : Equiv.Perm (Fin N)) (x z y : Fin N)
    (h : x ≠ z) : ¬ (pi x = y ∧ pi z = y) := by
  rintro ⟨h1,h2⟩
  exact h (pi.injective (h1.trans h2.symm))

/-- In particular a repeated right-fork coordinate has k=2,b=1 and zero count. -/
theorem target_too_small {k : Nat} (u : Fin k ↪ Fin N) (b : Finset (Fin N))
    (h : b.card < k) : Fintype.card (R10.Hits.Hit u b) = 0 :=
  R10.Hits.card_hit_of_target_small u b h

/-- Arithmetic only; the combinatorial index count is not assumed proved here. -/
theorem constant_identity (n : ℚ) (hn : n ≠ 0) :
    6072/n + 31878/n^2 + 63756*(n-1)/n^2 = 69828/n - 31878/n^2 := by
  field_simp [hn]
  <;> ring

end R10.Parallel22
