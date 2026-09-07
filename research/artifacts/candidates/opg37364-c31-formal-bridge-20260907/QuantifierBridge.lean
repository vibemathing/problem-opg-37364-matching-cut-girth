import Init
/- Candidate quantifier bridge only. The fixed-density family is a premise,
   not a theorem supplied by this file. Native Lean compilation pending. -/
universe u v w
namespace R10
variable {D : Type u} {G : Type v} {X : Type w}
variable (Positive : D → Prop) (Threshold : G → Prop)
variable (Admissible : D → G → X → Prop) (Cut : X → Prop)
theorem family_negates_positive_root :
((∃ (d : D), ((Positive d) ∧ (∀ (g : G), ((Threshold g) → (∃ (x : X), ((Admissible d g x) ∧ ((Cut x) → False))))))) → ((∀ (d : D), ((Positive d) → (∃ (g : G), ((Threshold g) ∧ (∀ (x : X), ((Admissible d g x) → (Cut x))))))) → False)) :=
(fun (family : (∃ (d : D), ((Positive d) ∧ (∀ (g : G), ((Threshold g) → (∃ (x : X), ((Admissible d g x) ∧ ((Cut x) → False)))))))) => (fun (positive_root : (∀ (d : D), ((Positive d) → (∃ (g : G), ((Threshold g) ∧ (∀ (x : X), ((Admissible d g x) → (Cut x)))))))) => (Exists.elim family (fun densityw family_data => (Exists.elim ((positive_root densityw) (And.left family_data)) (fun girthw threshold_data => (Exists.elim (((And.right family_data) girthw) (And.left threshold_data)) (fun graphw witness => ((And.right witness) (((And.right threshold_data) graphw) (And.left witness)))))))))))

#print axioms R10.family_negates_positive_root
end R10
