# C11: an explicit 26-vertex finite obstruction

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-incidence-witness-c11.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: 68232aa54f5a84f99685e461d3b19000feee6908.

The frozen definition uses two nonempty shores and a possibly empty
crossing matching. This is a finite graph witness and a proof candidate,
not a counterexample family of unbounded girth. Both admitted obligations
remain open. No novelty or mathematical-verifier execution is claimed.

## C11.1 / claim:opg37364-c11-bipartite-shore-bound

Let F be a nonempty finite simple bipartite graph with minimum degree
at least k>=2 and no four-cycle. Write its bipartition sizes p<=l.
Both sizes are positive. Each of the l vertices has at least k
neighbours in the p-part, contributing at least binom(k,2) unordered
pairs of neighbours. A pair can be contributed by at most one vertex,
since two common neighbours would give a four-cycle. Consequently
  l*k*(k-1)/2 <= p*(p-1)/2.
Using l>=p and p>0 gives p>=k*(k-1)+1, and hence
  |V(F)| >= 2*(k*(k-1)+1).                         (A)

If a finite simple r-regular bipartite graph G with r>=3 and no
four-cycle has an MC, each nonempty induced shore has minimum degree
at least r-1: at most one incident edge can cross the cut. Each shore
also inherits bipartiteness and absence of four-cycles. Applying (A)
with k=r-1 to the two disjoint shores gives
  |V(G)| >= 4*((r-1)*(r-2)+1).                     (B)
The requirement that both shores are nonempty is used explicitly.

For r=4 the right side of (B) is 28. Thus any 4-regular simple
bipartite graph with no four-cycle and fewer than 28 vertices has no MC.

## C11.2 / claim:opg37364-c11-explicit-incidence-graph

Work over the three-element field, with all arithmetic modulo 3.
Let R consist of the 13 nonzero triples whose first nonzero coordinate
is 1:
  (1,a,b) for a,b in {0,1,2};
  (0,1,b) for b in {0,1,2};
  (0,0,1).
Every nonzero triple is uniquely a nonzero scalar multiple of an
element of R. Make disjoint point and line copies P_v,L_w of R.
There is one edge P_v--L_w exactly when v dot w = 0 modulo 3.

There are 26 vertices, and the graph is simple and bipartite by its
definition. For a fixed nonzero v, the equation v dot w=0 has nine
solutions w: one coordinate is determined by the other two. Excluding
zero leaves eight, grouped into four pairs {w,2w}, giving degree four.
The same argument applies to every line vertex. Thus m=13*4=52.

Two distinct point representatives are not proportional. Their two
homogeneous equations on a line vector have a one-dimensional common
solution space: a nonzero 2-by-2 minor lets two coordinates be solved
in terms of the third. There are exactly two nonzero solutions, one
projective line representative. Hence two distinct points share
exactly one line, excluding every four-cycle.

The graph is connected: any two points share a line, and each line
has four point neighbours. Its girth is exactly six, since it has no
odd cycle or four-cycle and contains
  P_(1,0,0), L_(0,0,1), P_(0,1,0),
  L_(1,0,0), P_(0,0,1), L_(0,1,0), P_(1,0,0).
All consecutive dot products vanish, and the six typed vertices are
distinct. All uses of the finite field here reduce to arithmetic
modulo 3; no existence theorem for arbitrary finite planes is needed.

By (B), an MC would require at least 28 vertices, contrary to 26.
This proves the candidate's no-MC assertion without T3, TABC, T14,
an eigenvalue bound, or any computation output.

## C11.3 / claim:opg37364-c11-parameter-scope

The average degree is exactly 4, not less than 4. The witness satisfies
the frozen admissibility inequalities for every real d>4 and every
integer 3<=g<=6; for instance d=5 and g=6. It is not admissible at
d=4 under the strict inequality and is not admissible at g>=7.

Accordingly this fixed graph does NOT establish the negation of
the full forall-d / exists-g root. It does show that the elementary
C07 assertion for maximum degree at most three cannot be replaced by
maximum degree at most four, even on nontrivial connected bipartite
graphs of girth six. The unbounded-girth source family in C03/C04 is
a separate argument with its own pending dependencies.

## Finite data, attacks and reproducibility

The companion JSON is an exact declarative construction: it lists
all 13 representatives, uses disjoint typed copies, gives the modular
dot-product adjacency rule and a six-cycle. It does not purport to
contain an executed enumeration or a verifier receipt.

To audit, check normalization of nonzero triples, count the solutions
to one and two independent equations, verify the displayed cycle,
and apply the pair-count shore bound. A future authorized checker
may expand the 13-by-13 incidence rule, reconstruct the graph, and
compare its degrees, girth and C08 cut formula. Such a run has not
occurred. An alternative algebraic audit identity is B*B^T=3I+J for
the incidence matrix; it follows from the same degree/common-line
counts and is not needed as an extra premise of the cut proof.

The typed point/line copies must not be identified merely because
their coordinate triples coincide. Counting degree two rather than
degree three within a proposed shore would give an insufficient
bound. The empty-shore convention would invalidate (B); the frozen
nonempty-shore convention is essential. The finite parameter scope
cannot be extrapolated to arbitrary g.

Internal source comparison: C07's shortest-cycle argument establishes
the contrasting subcubic positive case; C08 fixes the exact matching
cut predicate and separates graph admissibility from cut existence.
This proof is self-contained and asserts no originality. No external
classification of cages or projective planes is used.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
current_blocker: nonterminal small-order source ambiguity and pending
                 mathematical / statement-faithfulness verification.
next_action: audit the general girth-dependent shore-size criterion;
             determine exactly where it cannot generate an
             unbounded-girth counterexample family.
