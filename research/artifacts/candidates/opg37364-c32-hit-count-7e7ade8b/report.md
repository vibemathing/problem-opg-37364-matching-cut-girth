# C32: fixed-input hit counts, without replacement

Verdict: candidate_only. Status: NONTERMINAL_CHECKPOINT.
Primary owner: math-formalization.
Problem: problem:opg-37364-matching-cut-girth.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Read base: 7e7ade8bde918c2c9eac9925bb068254de2f0bc0.

## Observations and assurance boundary

PR31 is merged. Its native-lock directory and the four original Lean modules
were freshly read and matched to the available attachment bytes. They are
inputs, not edited or retransmitted by C32. PR29/30 are not retransmitted.
No admission_request is added.

The user reports an external successful C31 replay with nine axiom outputs
and a 4 GiB address-space limit. This is recorded as a user report, not as an
observed compiler receipt: no external run artifact or callable runtime was
provided in the current accessible repository state. The current local
runtime probe found no lean/lake/elan executable. A new bounded replay
actually attempted `lean --version` and failed before process creation with
errno 2. Driver exit was 2; compiler exit is null. Actual compiled_modules=[],
actual_axioms=null, actual_toolchain_fingerprint=null. No new Lean theorem
in this package is claimed compiled, and no assertion about the external
replay is inferred from these local failures.

The exact hit-count and probability arguments below are conventional
candidate proofs, with accompanying Lean source to replay next. Writing
that source does not complete the prerequisite native replay. Z3 and finite
enumeration were not used as substitutes in this continuation.

## Frozen atomic statement

Let N,k be natural numbers, let u:Fin k -> Fin N be injective, and let
B be a subset of Fin N with cardinality b. Thus k<=N and b<=N are structural
facts, not omitted assumptions. Write Hit(u,B) for the permutations pi of
Fin N for which pi(u(i)) belongs to B for every i in Fin k.

The candidate statement is

    |Hit(u,B)| = b.descFactorial(k) * (N-k)!,

where b.descFactorial(k)=(b)_k is the falling factorial, equal to zero when
k>b. In particular this does not use b^k as the number of image choices.
For the uniform finite permutation space, probability means |Hit(u,B)|/N!.
The additional candidate identity and inequality are

    |Hit(u,B)|/N! = product_(0<=i<k) (b-i)/(N-i) <= (b/N)^k.

The displayed product uses rational subtraction. If k>b, the term i=b is
zero; later negative numerators are not individually replaced by truncated
natural differences in the proof. At N=0 the only possible k and b are zero;
the cardinality is 1 and the empty probability product is 1. Lean's rational
b/N is total, and exponent zero is 1. The probabilistic definition itself
still divides by N!=1, never by N=0.

## 1. Injection choices and C31 factorial fibers

For each hit permutation pi, restrict pi o u to an injection v:Fin k -> B.
The remaining information is a permutation satisfying all fixed pairs
u(i)->v(i). Conversely, any injection v and such a completion determine
exactly one hit permutation. These are inverse maps, so

    Hit(u,B) equiv Sigma(v:Fin k embeds B), Assigned(u,v).

For fixed v, identify the ranges of u and v with Fin k. The prescribed
region bijection is imageEquiv(u).inverse followed by imageEquiv(v).
The subtype Assigned(u,v) is then equivalent to the exact Completion type
used by C31. This is the explicit connection to
R10.Cardinality.card_fin_completion, not an assumed replacement for it.
Every fiber therefore has cardinality (N-k)!.

At the pinned Mathlib commit, Fintype.card_embedding_eq gives
|Fin k embeds B| = b.descFactorial(k). Summing the equal fiber cardinalities
proves the exact hit-count formula. If b<k there are no image injections,
and descFactorial is zero. For k=0 there is one empty image injection and
N! completions. For k=N the complement is empty; if B contains all N points
there are N! permutations, and if b<N there are none. These endpoints appear
as explicit source lemmas, not tests used to assert the general theorem.

## 2. Rational normalization and the zero-factor split

The integer identity (N-k)! * N.descFactorial(k) = N! holds because k<=N.
All factorials are positive, and N.descFactorial(k) is nonzero. Cancellation
therefore turns the count ratio into (b)_k/(N)_k. Expanding falling factorials
as finite products yields the displayed rational product.

For k<=b and i<k, both denominators N and N-i are positive. Cross multiplying

    (b-i)/(N-i) <= b/N

is equivalent to i*(N-b)>=0. Every left factor is nonnegative, so finite
product monotonicity gives the k-th power bound. For k>b, first use the zero
factor at i=b to prove the entire product is zero, then compare zero with
the nonnegative right hand side. Applying nonnegative-product monotonicity
to all rational factors when k>b would be unjustified; C32 does not do so.

## 3. Twenty-four coordinates and incidence projection

A tuple with coordinate j constrained by u_j and B_j is exactly a dependent
family of Hit(u_j,B_j). Cardinality of the Cartesian product is

    product_j (b_j)_(k_j) * (N-k_j)!.

The unconstrained denominator is (N!)^24, by the existing C31 sample-space
lemma. Dividing and applying the single-coordinate bound gives the product
of (b_j/N)^(k_j). The source proves the correspondence with a subtype of
full permutation tuples, so no extra tags or independent slot model are
silently counted.

The generic map from (tuple,bad-shore) incidences to tuples with a bad shore
is surjective, not generally injective. C32 reuses C31's theorem with
|BadCut|<=|Incidence|. Correctly instantiating the relation with the graph
predicate, the all-shore sums, and the short-cycle catalogue remains later
work; this generic alias is not a claim that those graph obligations are
already formalized.

## 4. Fixed APIs and content locators

Lean source commit: 6caaee842e9495688c1567e78c0e68dbb96942aa.
Mathlib source commit: c44e0c8ee63ca166450922a373c7409c5d26b00b.
The eight transitive commits and four immutable C31 source hashes are in
input-lock.json. Read-only API checks used the exact source commit:

- Mathlib/Data/Fintype/CardEmbedding.lean, Git blob
  59eaaa17ce8e80a1fa85aa0ca61f362de7ad5556: Fintype.card_embedding_eq.
- Mathlib/Data/Nat/Factorial/Basic.lean, Git blob
  b9a296334cc6cd39bf037fe7f94c9a6d90017ae8: descFactorial recursion,
  descFactorial_of_lt, factorial_mul_descFactorial.
- Mathlib/Data/Subtype.lean, Git blob
  e5526d7f153715ea47976adf6b0b836f100da3eb: heq_iff_coe_eq requires an
  explicit equivalence between the two predicates. C32 supplies it.
- Lean src/util/shell.cpp, Git blob
  ba106b5349e17f088c70394170a03d230685b459: --githash and -j/-o flags.

These are source/signature checks, not elaborator output or mathematical
receipts. No source full text is copied into the package.

## 5. Native replay procedure and current result

Use the actual native Lean executable (not an elan shim) and an installed
Mathlib checkout, with its exact transitive dependency checkouts and compiled
imports. From this C32 directory run:

    python -S replay.py --lean <native-lean> --mathlib-dir <mathlib-checkout>

The default C31 directory is the existing sibling native-lock directory.
No C31 source is changed: verified sources are copied to a temporary build
capsule. The driver enforces 4 GiB address space, 90 CPU seconds, 120 wall
seconds, one Lean worker, and 256 KiB combined output per command. It checks
full --githash, dependency HEADs, tracked source cleanliness, and records the
actual lean and libleanshared SHA-256 if those stages are reached. It then
compiles three C31 modules, audits exactly their nine named declarations,
and only then compiles HitCounts/HitProbability and audits their twelve
named declarations. Source escape scanning is lexical, distinct from actual
printed axioms. Imported binary caches are not externally attested by this
driver; even success is local candidate replay, not trusted admission.

The actual current replay reached only lean --version. Its real command
record, empty stdout/stderr, input hashes and code hash are in replay-local/.
The later successful-runtime path is not yet exercised in this environment.
Official binary acquisition did not supply an executable; no download or
source resolution is misreported as installation. No finite graph, enormous
permutation selector, solver proof or trusted gate ran in this continuation.

## Remaining dependencies

First C31 lemma not locally replayed: R10.Cardinality.preservesRegion.
First old native counting target: R10.Cardinality.card_fin_completion.
First new module to elaborate after the old audit: R10.HitCounts.
New atomic count: R10.Hits.card_hit, via card_assigned/card_fin_completion.
Next arithmetic target: R10.Hits.hit_probability_le.

The general short-cycle catalogue (parallel two-cycles and cycles sharing
edges or paths), graph-to-count incidence map, small/large shore sums, and
mechanical total bound <41/800<1 are still not formalized by this package.
The root remains the fixed d0=5 counterexample-family statement with two
nonempty shores. C32 changes neither that statement nor the source comparison
already frozen in PR30. No fatal counterexample to an original C31/C21B
lemma was found, and none is withdrawn on the basis of a runtime failure.

trusted_verified_scope: [].
best_verified_candidate: none.
best_verified_result: none.
open_obligations: obligation:opg37364-contract-edge-cases; obligation:opg37364-root.
