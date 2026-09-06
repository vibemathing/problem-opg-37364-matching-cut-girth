# C17: elementary unbounded-girth families below every d>4

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-elementary-density-c17.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: dce0f17a89e751cac6795812f27d5541298be030.

## Statement and exact dependency

For every real d>4 and integer g>=3, there is a finite simple
2-connected bipartite graph G with no matching cut, girth at least g,
and
  4 < average_degree(G) < d,
  minimum_degree(G)=2,
  maximum_degree(G)<=40+ceil(72/(d-4)).
It contains an induced subgraph of minimum degree at least 39.

In particular, set d0=5 once and for all. The deterministic family
below gives, for every g>=3, a graph of average degree <364/73<5,
maximum degree at most 112, and girth at least g, with no matching cut.
This supplies the negative-root quantifiers without K1 or a finite-girth
extrapolation. No assertion at d=4 is obtained.

The only existence input is the explicit elementary candidate C16:
for every h>=3 it constructs a finite simple bipartite H of girth
at least h, degrees 39 or 40, and
  |delta_H(S)| > min(|S|, |V(H) minus S|)
for every nonempty proper S.
C16 proves this by finite counting and matching deletion, not by LPS,
Dirichlet, a spectral theorem, or an external random-graph theorem.
C17 uses that proof as a candidate dependency, not as admitted Evidence.
Both admitted obligations remain open.

## C17.1. A cut-vertex test for an expanding high-girth seed

Let H have minimum degree at least three, maximum degree at most D,
girth at least D, and the strict cut inequality just displayed.
Then H is 2-connected.

The cut inequality first implies connectedness. Suppose x is a cut
vertex and C is a smallest component of H-x. There are at least two
components, so 1<=|C|<|V(H)|/2. All edges leaving C end at x.
Consequently
  |C| < |delta_H(C)| <= deg_H(x) <= D.
Every vertex in H[C] loses at most the one neighbour x, and hence
H[C] has minimum degree at least two. A finite graph of minimum degree
at least two has a cycle: take a longest simple path and use the second
neighbour of its final vertex on that path. This cycle has length at
most |C|<D, contrary to girth(H)>=D.
The minimum-degree hypothesis also ensures at least four vertices,
so the order condition in 2-connectivity is satisfied.

For the C16 seed, D=40. Every seed used below has girth at least 40,
so it is 2-connected without deleting vertices or losing its dense core.

## C17.2. Explicit integer parameters and seed size

First define the family for integers k>=1 and g>=3, not for an oracle
giving an arbitrary real number. Set
  D=40+k,
  B=1+D*sum_{j=0}^{g-3}(D-1)^j,
  h=max(g,2*k*B+1).
All these are positive integers. In particular B>=D+1>=42, so h>=85.

Choose the deterministic C16 graph H at input h. Write n=|V(H)|,
m=|E(H)|, and let X,Y be its two parts. Its minimum degree 39 implies
it has a cycle, so
  n>=girth(H)>=h>2*k*B.
Also 39n<=2m<=40n, and C17.1 makes H 2-connected.

For reference, C16 fixes
  K_h=2h, C_h=K_h^2*(160*K_h^2)^K_h,
  M_h=max(1000,4*C_h,2h), N_h=M_h^2,
and H has n=2N_h vertices. These integers are enormous but finite.
No seed is claimed to have been generated or checked by a runtime.

## C17.3. Greedy augmentation with current-distance tests

On V(H), consider additional unordered pairs whose endpoints are in
the same original part X or Y. Starting with F empty, repeatedly add
the lexicographically least currently legal pair, where legality means:
its endpoints are distinct, each has F-degree less than k, and their
distance in the current simple graph J=H+F is at least g-1.

The distance condition implies that the pair is absent, since g>=3.
Adding it cannot create a cycle shorter than g: any new cycle consists
of the new edge and an old path between its endpoints. Thus J always
has girth at least g and maximum degree at most D.
This procedure stops after at most floor(kn/2) additions. Its terminal
F is maximal for these conditions. The distances are tested in the
current J, not merely in the initial H.

A graph of maximum degree at most D has at most B vertices within
distance g-2 from any fixed vertex. Indeed the numbers of walks without
immediate reversal at positive lengths ell are at most D(D-1)^(ell-1);
summing through ell=g-2 gives B. Counting walks overcounts vertices
and is therefore a valid upper bound even in a graph with cycles.

Call an old vertex unsaturated when its F-degree is less than k.
There are at most B unsaturated vertices in X. Otherwise, fix one
of them u and choose another v outside its distance-(g-2) ball in J.
The pair uv is legal, contradicting maximality. The same reasoning
applies to Y. Hence at least n-2B old vertices have F-degree k.
Putting t=|F| gives
  2t=sum_v deg_F(v)>=k(n-2B)>(k-1)n.                 (1)
The strict inequality uses n>2kB. In particular t>0, including k=1.

## C17.4. Subdivide only the artificial edges

For each uv in F, replace that artificial edge by u-w_uv-v, with one
distinct new vertex w_uv. Keep every original H edge unchanged.
Call the resulting graph G.

It is simple. Put w_uv in the opposite bipartition part from u and v;
the old vertices keep their parts. Then G is bipartite.
A cycle of G projects, by suppressing its distinct new degree-two
vertices, to a cycle of the simple graph J of no larger length.
Thus girth(G)>=girth(J)>=g.

Deleting an old vertex x leaves H-x connected and every new vertex
still attached to at least one old endpoint. Deleting a new vertex
leaves all of H connected and every other new vertex attached to it.
These tests, together with |V(G)|>=3, prove 2-connectivity.
Old degrees are at most 40+k; new degrees are exactly two and t>0.
Therefore minimum_degree(G)=2 and maximum_degree(G)<=40+k.

Suppose a two-shore colouring of G gave a matching cut. If both colours
occur on H, its restriction gives a matching cut of H: crossing edges
of H are a subset of the crossing matching of G. This contradicts
C16's strict cut inequality. If H has just one colour, a new vertex
of the other colour has two distinct old neighbours, both opposite
in colour to it, again contradicting the matching condition.
Thus every nontrivial cut of G has a vertex with at least two distinct
crossing neighbours. No arbitrary subdivision principle is being used.

The original H is induced in G. Thus the maximum average degree
(maximum of the average degrees of nonempty subgraphs) is at least 39,
and the degeneracy (maximum subgraph minimum degree) is at least 39.
These facts do not impose the same lower bound on global average degree.

## C17.5. Strict density and the full quantifier map

There are n+t vertices and m+2t edges. Consequently
  average_degree(G)=4+(2m-4n)/(n+t).
Since 39n<=2m<=40n and t is finite,
  4 < average_degree(G)
    <= 4+36n/(n+t)
     < 4+72/(k+1).                                   (2)
The last inequality uses (1), namely n+t>(k+1)n/2.

For an arbitrary real d>4, choose the positive integer
  k=ceil(72/(d-4)).
Then 72/k<=d-4 and 72/(k+1)<72/k, so (2) implies average_degree(G)<d.
This is an existence argument for each real d, not a claim to compute
the ceiling of an arbitrary unencoded real number.

For the root, no real-number oracle is needed. Fix k=72 and d0=5:
  average_degree(G)<4+72/73=364/73<5,
and maximum_degree(G)<=112. For every integer g>=3 the construction
above is deterministic using only finite searches and integer arithmetic.
It gives precisely
  exists d0>0, for every g>=3, exists a finite simple G
  with average_degree(G)<d0, girth(G)>=g, and no matching cut.
The same integer k is used for every g. The graph order is finite and
at most (k+2)N_h because t<=kn/2 and n=2N_h.

The parameter g may increase without bound. Each constructed graph has
a cycle (it contains H), and its girth is at least its input g. Therefore
these are genuinely unbounded finite girths, not forests with infinite
girth or a repeated bounded-girth witness.

## Audit, dependency boundary and next exact task

C17.1 is elementary and shows why the full dense seed can be retained.
C17.2 uses C16 at one explicitly larger girth. C17.3 is finite greedy
maximality and a walk count. C17.4 verifies every graph transformation
and both possibilities for the old colours. C17.5 checks the strict
density and the order of quantifiers. No external existence theorem
is a premise once C16's finite proof is expanded.

The construction resembles the conditional C04 augmentation, but
replaces its T14 input by C16, retains an induced minimum-degree-39
core, proves 2-connectivity by C17.1, and improves the saturation count
using n>2kB. It is not a repetition of C11's finite incidence witness.

Attacks covered: maximum degree and global average are not conflated;
original edges are never removed; new vertices have two distinct old
neighbours; distances are recomputed after additions; final simplicity
and girth are proved; k=1 is valid; strict <d is not replaced by <=d;
g can vary while d0 and k remain fixed. Nothing is asserted at d=4.

The original problem's negative answer is attributed in the 2025
Algorithmica paper by Feghali, Lucke, Paulusma and Ries, Section 1.2:
https://doi.org/10.1007/s00453-025-01318-8
That attribution is not a premise of the finite construction. No
originality or optimal parameter claim is made.

No mathematical runtime, sampler, enumerator, SAT solver or proof
assistant was executed for this candidate. A full review must first
check C16's all-cut and overlapping-cycle counts, then the deductions
above. Byte hashes, PR checks, model review and merge are not Evidence.
The frozen contract and all truth records are unchanged.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: produce an exact finite-counting audit for C16 with finite
sum identities and a separately specified graph/colour semantics map;
request the registered capabilities without fabricating their receipts.
