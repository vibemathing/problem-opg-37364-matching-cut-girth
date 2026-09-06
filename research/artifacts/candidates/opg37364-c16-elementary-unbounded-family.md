# C16: finite-counting construction at unbounded girth

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-elementary-unbounded-c16.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: b36909d3bf9a4ead143ea074f6eae08b916af1b7.

## Theorem candidate and scope

For every integer g>=3 there is a deterministically specified finite
simple connected bipartite graph G_g of girth at least g, with every
vertex of degree 39 or 40, such that every nontrivial cut has more
edges than its smaller shore has vertices. In particular G_g has no
matching cut, and the fixed real parameter d0=41 gives
  average_degree(G_g)<=40<41,  girth(G_g)>=g.

This proof uses only finite counting, finite graph arguments and
rational inequalities. No LPS graph, prime-distribution theorem,
spectral theorem, random-regular-graph theorem, limiting probability
theorem, local lemma, or external existence theorem is an assumption.
Probabilities below are ratios in a finite uniform sample space.

The final witnesses are simple graphs, as required by the frozen
contract. Auxiliary edge-coloured bipartite multigraphs are explicitly
allowed only inside this construction. Parallel pairs are counted as
length-two cycles there. Both shores of a matching cut remain nonempty;
an empty crossing matching is allowed by the contract. K1 is not used.
All assertions remain candidates; no mathematical verifier has run.

## C16.1. An elementary binomial estimate

For integers 1<=k<=n,
  binom(n,k) <= (3n/k)^k.                              (1)
For completeness, (1+1/j)^j <= sum_{i=0}^j 1/i! < 3
for j>=1: use binom(j,i)<=j^i/i! and i!>=2^(i-1) for
i>=1, followed by the finite geometric sum. Induction then gives
k!>=(k/3)^k. Indeed the induction step reduces to
3>=(1+1/k)^k. The estimate binom(n,k)<=n^k/k! proves (1).
No asymptotic factorial formula is needed.

## C16.2. Finite random model

Let N be a positive integer, to be chosen explicitly in C16.6.
Make disjoint parts L={L_1,...,L_N} and R={R_1,...,R_N}.
Choose 40 permutations pi_1,...,pi_40 of [N], independently and
uniformly. For each i in [40] and u in [N], put one coloured edge
(i,u) from L_u to R_{pi_i(u)}. Distinct colours may make parallel
edges. Call the auxiliary multigraph Y.

The sample space has exactly (N!)^40 equally likely elements.
Every vertex has degree 40 counting multiplicity. There are no loops.
For a set S of size s<=N, write a=|S intersect L|, b=|S intersect R|
and I for its internal edge count, with multiplicity. Then
  |delta_Y(S)| = 40(a+b)-2I.                           (2)
Call S bad when 1<=s<=N and |delta_Y(S)|<=2s.
If either a or b is zero, it is not bad.

We may assume 1<=a<=b by interchanging the part names; the opposite
orientation is counted by a factor of two in the union bound.
Permutations become inverse permutations under this interchange,
which preserves the independent uniform distribution.

A bad S satisfies
  I>=19(a+b),   I<=40a,
so
  b<=21a/19<2a,  b<=21N/40<3N/5,  I>=38a.             (3)
The second bound follows from a>=19b/21 and a+b<=N.

## C16.3. A fixed-shore probability bound

There are 40a source slots (i,u) with L_u in S. If I>=38a,
some 38a of these slots all have their images in S intersect R.
If a chosen set uses k_i slots of permutation i, its probability is
  product_i (b)_{k_i}/(N)_{k_i} <= (b/N)^(38a),         (4)
where (x)_j=x(x-1)...(x-j+1). If k_i>b the corresponding probability
is zero; otherwise each ratio factor (b-j)/(N-j)<=b/N.
Independence is used between permutations, not between their slots.

A union bound over chosen slots therefore gives
  P(S bad) <= binom(40a,2a) (b/N)^(38a).              (5)
For fixed a,b, sum this over the binom(N,a)binom(N,b) possible shores.
Apply (1) and (3):
  binom(N,a) <= (6N/b)^a,
  binom(N,b) <= (3N/b)^b <= (3N/b)^(2a),
  binom(40a,2a) <= 60^(2a).
Their product with (b/N)^(38a) is at most
  [194400 (b/N)^35]^a.                                (6)

Let K0=194400. The bounds on b in (3) show that (6) is at most both
  [K0 (2a/N)^35]^a  and  [K0 (3/5)^35]^a.
Moreover
  K0 (3/5)^35 < 1/4.                                 (7)
Indeed 100*3^10<5^10, so (3/5)^30<1/1000000, and
194400/1000000<1/4. The additional fifth power only decreases it.

For a fixed a there are at most 2a relevant positive integers b.
Including the factor two for the two orientations proves
  P(some bad S)
    <= 4 sum_{a=1}^{floor(N/2)}
          a [K0 min(2a/N,3/5)^35]^a.                  (8)

## C16.4. Explicit separation of small and large shores

Take N=M^2 with integer M>=1000 and put
  theta = K0 (2/M)^35.
For a<=M the bracket in (8) is at most theta. For a>M it is
less than 1/4 by (7). Hence
  P(some bad S)
    <= 4 theta/(1-theta)^2 + 4 sum_{a>M} a/4^a
    < 1/20 + 1/1000.                                 (9)

Here theta<1/100: since 2/M<=1/500, use
500^3=125000000>100*K0=19440000 and 35>=3.
Thus 4 theta/(1-theta)^2<400/9801<1/20.
For the tail, a<=2^a gives
  4 sum_{a>M} a/4^a <= 4 sum_{a>M} 1/2^a = 4/2^M
  < 1/1000,
because M>=1000>=12 and 2^12=4096>4000.

Infinite geometric sums in these displayed upper bounds can equivalently
be replaced by their finite partial-sum inequalities. They only bound
a finite union in a finite probability space; no limiting random-graph
result is used.

## C16.5. Overlapping short cycles have a finite-counting bound

Fix g>=3 and put
  K=2g,   C_g=K^2 (160 K^2)^K.                         (10)
Assume N>=2K. A short cycle in the auxiliary multigraph means a cycle
of length between 2 and g-1, inclusive. Cycles are identified by their
coloured edge sets, not by choices of starting vertex or direction.
A length-two cycle uses two distinct parallel edges.

If two distinct short cycles share a vertex, their union F is connected
and has v<=K vertices and e<=K edges, with
  e>=v+1.                                            (11)
To justify (11), a connected multigraph with e=v-1 is a tree; with
e=v it consists of a spanning tree plus one extra edge and has just
one cycle. Two distinct cycles cannot occur in either case.

An occurrence of F is covered by one of finitely many patterns:
choose v,e in [K], choose the two parts of each of the v abstract
vertices, and list e coloured edges on those vertices. The number
of such patterns is at most
  K^2 * 2^K * (40 K^2)^K.                             (12)
We use only patterns with distinct coloured edges and (11). Patterns
whose same-colour edges conflict at an endpoint have probability zero.
The larger count (12), allowing all lists, is still an upper bound.

For a consistent pattern with e_i edges of colour i, each injective
labeling of its vertices into the prescribed parts has probability
  product_i 1/(N)_{e_i} <= (2/N)^e.                    (13)
Indeed each colour specifies e_i distinct input-output pairs of its
permutation, and N>=2K ensures every falling-factorial factor is
at least N/2. There are at most N^v labelings. By (11), the expected
number of labeled occurrences of this pattern is at most 2^K/N.

A union bound using (12) therefore gives
  P(two distinct short cycles share a vertex) <= C_g/N. (14)
Every actual pair has such a coloured union pattern, so none is lost
by not assuming that the two cycles are edge-disjoint. Shared paths,
shared edges, and three parallel edges are all covered. Inconsistent
patterns contribute zero; a cycle counted twice by orientation is
not considered a distinct second cycle.

## C16.6. One explicit finite choice of size

For the given g, use C_g from (10) and set
  M_g=max(1000,4*C_g,2g),  N_g=M_g^2.                 (15)
Then N_g>=2K, theta<1/100, and
  C_g/N_g <= 1/(4M_g) <= 1/4000.
Combining (9) and (14),
  P(some bad shore OR overlapping short cycles)
       < 1/20 + 1/1000 + 1/4000 = 41/800 < 1.         (16)

Thus at least one tuple of 40 permutations has BOTH properties:
(E) every 1<=|S|<=N_g has |delta_Y(S)|>2|S|;
(C) all short cycles are pairwise vertex-disjoint.
This is a strict finite count. There is no independence assumption
between (E) and (C), and no conditioning on the multigraph being simple.

## C16.7. Delete short cycles without losing the cut obstruction

For a tuple with (E) and (C), select one coloured edge from each
short cycle and let D be the set of selected edges. Since those
cycles are vertex-disjoint, D is a matching in the multigraph sense:
each vertex loses at most one incident edge. Define G=Y-D, forgetting
colours after deletion.

There are no short cycles left. Deletion cannot create a cycle, and
every original short cycle was hit. In particular there is no parallel
pair, since g>=3 and a parallel pair is a short length-two cycle.
There were no loops. Thus G is simple and bipartite, with girth>=g.
Every degree is 39 or 40.

For any nonempty proper shore, take its smaller side S, so |S|<=N_g.
At most |S| deleted edges crossed S. Property (E) yields
  |delta_G(S)| >= |delta_Y(S)|-|S| > |S|.              (17)
Since G is now simple, its smaller shore contains a vertex with at
least two distinct crossing neighbours. Thus no nontrivial cut is
a matching, and the graph is connected. Its minimum degree at least
39 implies that it contains a cycle; the forest convention is not
being used to fake large girth.

The role of disjoint short cycles is essential: deleting arbitrary
many edges at a vertex would invalidate (17). The two bad-event
estimates were proved precisely to prevent that defect.

## C16.8. A deterministic family, not a proposed random experiment

For g>=3, compute the integers in (10) and (15). Order permutations
of [N_g] lexicographically by their value lists, and order their
40-tuples lexicographically. Select the first tuple satisfying (E)
and (C). Such a tuple exists by (16), within the finite universe
of size (N_g!)^40. All tests are finite exact graph predicates.

Order coloured edges by (colour,left index,right index), and delete
the least edge of each short cycle. This specifies D uniquely.
Let G_g be the resulting uncoloured graph. Its vertex set has
exactly 2N_g elements; (17) is the all-cut proof for every G_g.

This is a deterministic, computable family with an explicit finite
search bound, not an efficient graph generator or a claimed run.
The selector tests expansion and cycle intersection, not the desired
no-MC conclusion; its nonemptiness was proved before it was defined.
No finite experimental sequence is extrapolated to all g.

Fix d0=41. For every g>=3, G_g is a finite simple connected graph and
  average_degree(G_g)<=40<41=d0,  girth(G_g)>=g,
and every nontrivial cut fails the matching condition by (17).
This is the complete negative-root quantifier pattern with fixed d0.
The family also lies in the bipartite class. It has no vertex of
degree zero or one and is not a small-order artefact. Increasing g
forces unbounded girth, regardless of the enormous chosen orders.

## Dependency map, source comparison, and audit boundary

C16.1 supplies the elementary arithmetic estimate. C16.2-C16.4 give
the all-shore counting bound. C16.5 is a separate overlapping-cycle
count. C16.6 uses only their union bound and explicit integers.
C16.7 proves simplification, girth, degree and the all-cut obstruction.
C16.8 freezes deterministic selection and the exact root quantifiers.
All steps are finite combinatorics, finite graph reasoning or rational
inequalities; no unproved external existence theorem is inserted.

The root's negative answer is already stated in Feghali, Lucke,
Paulusma and Ries, Algorithmica 87 (2025), Section 1.2; its proof
uses a different spectral construction, mapped in C03/C15.
This candidate is an alternate counting-and-deletion argument, with
no originality or optimal degree claim. The source theorem is not
a mathematical premise of C16. Source locator:
https://doi.org/10.1007/s00453-025-01318-8

Attacks addressed: slots within one permutation are not independent;
the factor two for exchanging parts is retained; the bad-cut threshold
is 2s before deletion and s afterward; parallel pairs are explicitly
removed; overlapping cycles are controlled including shared paths;
auxiliary multigraphs are not passed off as final simple witnesses;
d0 is fixed before g; no n=1 or infinite graph is used.

No permutation sampler, graph generator, SAT solver, spectral code,
proof assistant or mathematical verifier was executed. Serialization
and file hashes identify candidate bytes only. The declared verifier
capabilities and source-faithfulness review are still required for
trusted repository closure. Both admitted obligations remain open.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
next_action: audit the finite counting argument in a trusted formal
environment; separately adapt the density-lowering construction of
C04 to this bounded-degree seed to cover every fixed d>4 without LPS.
