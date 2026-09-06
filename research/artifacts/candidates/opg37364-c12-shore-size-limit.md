# C12: a girth-dependent shore bound and its exact route limitation

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-shore-size-limit-c12.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: 2f583af139476c7a5d3b99e2f81c7c8246347b20.

The frozen contract, its K1 obstruction and both open obligations are
retained. This note supplies a sufficient no-MC criterion and falsifies
one proposed extrapolation of that criterion. Failure of a sufficient
criterion is not a theorem that the relevant graphs have MC.

## C12.1 / claim:opg37364-c12-girth-size-bound

For integers k>=2 and g>=3 define the finite sums
  M(k,2t+1) = 1 + k*sum_{i=0}^{t-1}(k-1)^i,
  M(k,2t)   = 2*sum_{i=0}^{t-1}(k-1)^i.
In the odd case t>=1, and in the even case t>=2.

Every nonempty finite simple graph F of minimum degree at least k and
girth at least g has at least M(k,g) vertices. For odd g, expose
breadth-first layers from a vertex through distance t. The root has at
least k neighbours and each subsequent nonterminal vertex has at least
k-1 new children. A repeated child or a premature return would give a
cycle of length at most 2t. Thus the displayed odd sum counts distinct
vertices.

For even g, start with an edge and expose two rooted trees through
depth t-1 on its two sides, excluding the central edge from the child
choices. Each branching factor is at least k-1. A collision within a
tree or between the trees would give a cycle of length at most 2t-1.
The displayed even sum therefore also counts distinct vertices.
Edges among the terminal layers need not be absent; the argument
excludes collisions that invalidate the count, not every boundary edge.

Connectedness is unnecessary: apply the same argument within a
component, whose vertices are also vertices of F.

If an r-regular finite simple graph G, r>=3, of girth at least g has
an MC, each of its nonempty induced shores has minimum degree at
least r-1 and girth at least g. Consequently
  |V(G)| >= 2*M(r-1,g).                                  (1)
Therefore |V(G)|<2*M(r-1,g) is a sufficient no-MC criterion.

## C12.2 / claim:opg37364-c12-degree-four-cutoff

Consider the subdirection: construct 4-regular graphs of arbitrarily
large girth whose order is less than 2*M(3,g), and use (1) alone to
exclude MC. A graph in that subdirection would necessarily satisfy
  M(4,g) <= |V(G)| < 2*M(3,g).                            (2)

For odd g=2t+1, the difference between the two bounds is
  D_t := M(4,2t+1)-2*M(3,2t+1)
       = 2*3^t - 6*2^t + 3.
At t=3, D_3=9. The exact recurrence
  D_{t+1}=3*D_t+6*2^t-6
shows D_t>0 for every t>=3.

For even g=2t, the difference is
  E_t := M(4,2t)-2*M(3,2t)
       = 3^t - 4*2^t + 3.
At t=4, E_4=20. The recurrence
  E_{t+1}=3*E_t+4*2^t-6
shows E_t>0 for every t>=4.

These two parity cases cover every integer g>=7. Hence interval (2)
is empty for all g>=7. This is an exact contradiction to the proposed
size-only subdirection, not a claim that no 4-regular high-girth no-MC
graphs exist.

The earlier finite witness sits exactly in the remaining gap:
  M(4,6)=26 < 28=2*M(3,6).
C11 constructs a graph of order 26, so its use of (1) is valid.
For girth five the numerical interval is 17<=n<20; this numerical
interval alone makes no existence claim about a graph of any such order.

## C12.3 / claim:opg37364-c12-fixed-degree-limitation

The limitation is not peculiar to degree four. For fixed integer
r>=4 put a=r-1 and b=r-2. The finite geometric sums give, for both
g=2t and g=2t+1,
  M(r,g)/M(r-1,g) >= ((r-3)/(r-1))*(a/b)^t.               (3)

For odd g, use M(r,g)>=a^t and
M(r-1,g)<=(r-1)*b^t/(r-3).
For even g, use M(r,g)>=2*a^(t-1) and
M(r-1,g)<=2*b^t/(r-3).
These are inequalities between explicit positive finite sums.

Bernoulli's elementary inequality
  (1+1/b)^t >= 1+t/b
follows by induction on t. Therefore if
  t >= ceil((r-2)*(r+1)/(r-3)),
the right side of (3) is at least two. For such t,
  M(r,g)>=2*M(r-1,g),
and the interval analogous to (2) is empty. The bound is sufficient
and deliberately not claimed sharp; the degree-four calculation
above is much sharper.

Degree three also has an explicit limitation. For odd g=2t+1,
M(3,g)-2*M(2,g)=3*2^t-4t-4, which is zero at t=2 and increases
strictly thereafter. For even g=2t, the difference is
2^(t+1)-2-4t, positive at t=3 and increasing thereafter.
Thus the size-only interval is empty for r=3 and every g>=5.
This agrees with, but does not prove, C07's stronger positive
shortest-cycle theorem for the subcubic class.

## C12.4 / claim:opg37364-c12-quantifier-and-route-audit

This paragraph concerns an explicitly subsidiary construction problem
on n>=2; it does not remove K1 from the frozen root.

Increasing regular degree together with girth cannot repair this
particular root-counterexample proposal at a fixed d: an r-regular
graph has average degree exactly r and requires r<d. Only finitely
many integer r>=3 lie below any fixed real d. Each has a finite
cutoff supplied above, so their size-only construction windows all
eventually close. Degree two gives cycles, handled directly by C01;
it does not supply an unbounded-girth no-MC family.

This does not exclude other fixed-degree arguments or irregular
constructions. In particular, the pending source family in C03 and
the density-changing construction in C04 use different information.
No contrary conclusion about those candidates follows from (2).

The failed-route proposal attached to this packet concerns only the
explicit sufficient-size extrapolation, not the whole admitted
degenerate-and-bridge-audit route. It is a proposal for a trusted
importer; this agent does not append the failed-routes truth ledger.

## Attacks, reproduction and checkpoint

The sufficient criterion uses a strict order inequality. Equality of
the two bounds already makes its feasible interval empty; no strict
positive difference is needed. The r=3 odd g=5 equality is an
explicit check of this distinction. The argument requires actual
regularity; replacing r by global average degree would not give
minimum degree r-1 within either shore.

To reproduce, expose the vertex-rooted and edge-rooted trees, derive
the finite sums, verify the two degree-four recurrences and their
initial values, and check (3) separately in both parity cases.
Keep the finite-field witness of C11 separate from a proposed
arbitrary-girth family. No graph generator, solver or mathematical
checker ran; these are finite symbolic derivations, not recorded
computer outputs. Serialization and SHA-256 computation concern
artifact bytes only.

Internal dependencies: C11's two-nonempty-shore observation and its
finite witness; C06 contains the earlier special degree-three
breadth-first count. The displayed counting proof is self-contained
and does not import T3, TABC, T14 or an unproved existence theorem.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
current_blocker: nonterminal small-order source ambiguity and pending
                 mathematical / statement-faithfulness verification.
discarded_subdirection: arbitrary-girth fixed-degree no-MC families
                        obtained solely from n<2*M(r-1,g).
next_action: retain the explicit finite witness and use the distinct
             source/spectral route or semantic verification handoff;
             do not repeat the contradicted size-only extrapolation.
