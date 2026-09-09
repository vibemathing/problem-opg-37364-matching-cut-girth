import Mathlib.Data.Fintype.Perm
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Prod
import Mathlib.SetTheory.Cardinal.Finite

set_option autoImplicit false

/- C34 isolated successor draft. Not compiled in this runtime.
The definitions below are byte-for-byte the C33 definitions from Omega
through Rel. The independent projection proof avoids importing C32 merely
to establish a finite surjection. Do not import this isolation view together
with R10.Parallel22: they intentionally carry the same namespace/definition.
-/
namespace R10.Parallel22
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

theorem bad22_le_incidence (N : Nat) :
    Nat.card {omega : Omega N // ∃ w : Witness N, Rel omega w} ≤
      Nat.card {t : Omega N × Witness N // Rel t.1 t.2} := by
  classical
  let projection : {t : Omega N × Witness N // Rel t.1 t.2} →
      {omega : Omega N // ∃ w : Witness N, Rel omega w} :=
    fun t => ⟨t.val.1, ⟨t.val.2, t.property⟩⟩
  have hsurj : Function.Surjective projection := by
    intro omega
    obtain ⟨w, hw⟩ := omega.property
    refine ⟨⟨(omega.val, w), hw⟩, ?_⟩
    exact Subtype.ext rfl
  simpa only [Nat.card_eq_fintype_card] using
    Fintype.card_le_of_surjective projection hsurj

#print axioms R10.Parallel22.bad22_le_incidence
end R10.Parallel22
