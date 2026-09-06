# C22: exact integer interface for the all-shore count

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-integer-count-c22.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: 81e69c6f3aeddb2c40103378f54ff57ef2d0e0ed.

## Scope

This note replaces one proof interface by an exact integer recurrence:
the number of permutation tuples incident with a given bad shore.
It does not execute that recurrence and does not identify incidence
counts with the number of tuples having at least one bad shore.
The short-cycle overlap test remains a separate obligation.
C20 and C21 are candidate inputs, not mathematical receipts.

All root graphs remain finite and simple; the counted auxiliary graph
has distinct coloured edge instances and may have parallel edges.
No choice of an empty shore or nonempty crossing matching is introduced.
Both admitted obligations remain open.

## C22.1. Count one permutation by its preimage

Fix N>=1 and subsets A,B of the left and right N-element label sets,
with |A|=a and |B|=b. For j in the integer interval
  max(0,a+b-N)<=j<=min(a,b),
define
  c_j=binom(a,j)*binom(N-a,b-j)*b!*(N-b)!;             (1)
outside this interval put c_j=0. Assume 0<=a,b<=N.

There are exactly c_j permutations pi with |pi(A) intersect B|=j.
Indeed pi^{-1}(B) is a b-element set consisting of j elements of A
and b-j elements outside A. Once this preimage is chosen, there are
b! bijections to B and (N-b)! bijections on the complementary sets.
The choices are unique in both directions. They count all permutations,
so
  sum_j c_j=N!.                                       (2)

For valid j, expansion of the binomial coefficients gives
  c_j=a!*(N-a)!*b!*(N-b)! /
      [j!*(a-j)!*(b-j)!*(N-a-b+j)!].                  (3)
This proves symmetry in a,b without evaluating factorials of negative
integers. It also follows from the bijection pi -> pi^{-1}.
The expression in (3) is a derived identity for the integer in (1);
an implementation should use (1) or exact factorial arithmetic.

## C22.2. Tuple recurrence and its invariant

Let P(z)=sum_j c_j*z^j. Define nonnegative integers A_r(t) by
  A_0(0)=1; A_0(t)=0 for t!=0;
  A_{r+1}(t)=sum_j c_j*A_r(t-j),                       (4)
where values at negative t are zero.
Only 0<=t<=r*min(a,b) need be stored at stage r.

The exact invariant is:
A_r(t) is the number of ordered r-tuples of permutations whose total
number of edge instances internal to A union B equals t.
For r=0 there is just the empty tuple and its total is zero.
For the next coordinate, separate tuples according to the internal
count j of that coordinate. Equation (1) counts its possibilities,
and (4) counts each ordered extension exactly once.
This proves the invariant by induction.

In particular
  sum_t A_r(t)=(N!)^r,                                (5)
and A_r(t) is the coefficient of z^t in P(z)^r.
The recurrence is a finite integer convolution, not a model of
independent edge slots within the same permutation. No such slot
independence was assumed in C20 either.

## C22.3. Count fixed bad shores, then their incidences

Set q=24. For a+b=s with 1<=s<=N, the auxiliary crossing count is
  24s-2t.
Thus a fixed shore is bad for C20 exactly when
  t>=11s.
Put
  B_{N,a,b}=sum_{t>=11(a+b)} A_24(t).                  (6)
This number is zero when its lower summation bound exceeds the support.
If a=0 or b=0 and s>=1, the crossing count is24s>2s, so these shores
are not bad.

Let Z=(N!)^24. Define the integer
  alpha_N =
    sum_{1<=a<=b, a+b<=N}
      w(a,b)*binom(N,a)*binom(N,b)*B_{N,a,b},          (7)
where w(a,b)=1 for a=b and w(a,b)=2 for a<b.
Equation (3) or inversion of each permutation justifies combining
the two orientations in (7). For each fixed ordered pair of sizes,
the number (6) is independent of the particular labelled sets A,B.

Let I be the finite set of pairs (omega,S), where omega is a tuple,
S is a bad shore of omega, and 1<=|S|<=N.
Then (7) proves |I|=alpha_N. Projection onto omega therefore gives
  |BadCut|<=alpha_N.                                  (8)
Equality need not hold: one tuple can have several bad shores.
At |S|=N a shore and its complement can both occur, which is harmless
because the objects being counted are shores, not unoriented cuts.

The equality case a=b uses w=1, not2. C20's simpler factor2 bound
may overcount equal-size orientations; it is still an upper bound.
Its termwise slot estimates bound (7)/Z as well as |BadCut|/Z.

## C22.4. Combine with the distinct overlap condition

Fix g>=3, K=2g and C_g=K^2*(96*K^2)^K.
For N>=2K, C20.5 proves
  N*|BadOverlap| <= C_g*Z.                             (9)
Here BadOverlap means that two distinct short cycles share a vertex,
including the coloured length-two cycles formed by parallel edges.

The following exact integer test is sufficient for a good tuple:
  N*alpha_N + C_g*Z < N*Z.                            (10)
Indeed (8)-(9) and the union bound imply
  N*|BadCut union BadOverlap| <= N*alpha_N+C_g*Z < N*Z.
As N>0, at least one tuple lies outside the union.
No independence of the two bad events is used.

For the C20 values N=M^2, M>=max(1000,4C_g,2g), its pointwise estimates
in C20.3-C20.4 bound alpha_N/Z by less than1/20+1/1000.
Also C_g/N<=1/4000. Thus (10) follows from the same finite rational
proof; it is not necessary to run (4) at the enormous selector size.

A trusted verification can separately check the combinatorial invariant
(4), the numerical upper bounds used in C20, and the overlap cover (9).
An arithmetic trace for (4) alone would not verify (9), matching deletion,
or the mapping to the original simple-graph statement.

## C22.5. Small reference cases, derived rather than run

For N=2, a=b=1, formula (1) gives c_0=c_1=1, so P(z)=1+z.
At q=24 and s=2 the threshold is22. The fixed-shore count is
  B_{2,1,1}=binom(24,22)+binom(24,23)+binom(24,24)
           =276+24+1=301.
The only positive sizes with a<=b and a+b<=2 are a=b=1.
Consequently alpha_2=4*301=1204. These are hand-derived reference
values; no recurrence program or exhaustive tuple enumeration ran.

For N=3, a=1,b=2 gives P(z)=2+4z.
Swapping a,b gives the same polynomial, and P(1)=6=3!.
These cases test the preimage orientation and its symmetry.

The N=2 case is NOT a simple high-girth graph certificate.
For g>=3 it fails N>=2K, a hypothesis of (9).
Moreover a 24-coordinate tuple has48 edge instances on only four
possible endpoint pairs. Some pair has at least three parallel
instances, producing distinct overlapping length-two cycles.
Thus every such tuple is in BadOverlap, despite the small value
of alpha_2/Z. This is an explicit attack on omitting the overlap test.

## Candidate data and verification limits

The companion declarative JSON records formulas, domains, invariants
and the reference cases. It is not a command output, executable
verifier, registered schema or receipt. No code is added to scripts
or to the trusted Harness. No selected mathematical runtime is implied.

A future consumer must reconstruct (1)-(7) from the actual N,a,b and
q, use exact integers and finite support, check every recurrence entry
rather than trust a claimed final number, and keep (9) and the graph
semantics separate. A finite computation would verify its supplied
parameters only unless the universal invariants were separately proved.

Inputs: the frozen contract, C20's finite count and C21's requirement
for a uniform-size seed. No external theorem or library API is used.
Both old-colour and new-vertex cases in C21 remain required after
the seed is constructed. Source-domain ambiguity is not silently
repaired by this arithmetic interface.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: test a degree-preserving replacement for C20's deletion
step, with explicit bounds ensuring distant buffer edges exist.
