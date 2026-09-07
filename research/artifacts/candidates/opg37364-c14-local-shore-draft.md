# C14 draft: a local shore lemma and the closed 8/3 threshold

Verdict: candidate_only. This is a draft for the existing admitted edge-case
obligation, not a registered packet, verifier receipt, or Result.
Problem: problem:opg-37364-matching-cut-girth
Attempt: attempt:web-20260906-opg37364-a01
Route: route:degenerate-and-bridge-audit-v1
Graph: graph:opg37364-initial-v1
Target: obligation:opg37364-contract-edge-cases
Root: obligation:opg37364-root

The frozen contract is unchanged. The positive theorem below explicitly
assumes at least two vertices. The K1 obstruction and the source-domain
question remain separate. No graph enumeration, solver, Lean invocation,
or mathematical verifier was used.

## Theorem candidate

Every finite simple graph G with at least two vertices, girth at least
five, and average degree at most 8/3 has a matching cut. Both shores
must be nonempty; the crossing matching may be empty.

## 1. Preliminary local cuts

Suppose for contradiction that G has no matching cut. It is connected:
otherwise a nonempty proper union of components is an empty cut.
Its minimum degree is at least two: a vertex of degree at most one
gives a singleton shore with at most one crossing edge.

Two degree-two vertices cannot be adjacent. If they were u,v, their
other neighbours would be distinct because a triangle is forbidden.
The shore {u,v} would have two disjoint crossing edges. Its complement
is nonempty in a simple triangle-free graph of minimum degree two.

Let T be the set of degree-two vertices and H=V(G) minus T.

## 2. Strengthened local shore lemma

In fact every vertex has at least two neighbours in H.

To prove this, suppose v has at most one neighbour in H and put
A={v} union (N(v) intersect T). The neighbours of v have no mutual
edges, since a triangle is forbidden. Each w in N(v) intersect T
has one other neighbour z(w) outside A. The vertices z(w) are
pairwise distinct, since a coincidence would create a four-cycle.
If v has a neighbour u in H, none of the z(w) equals u, since that
would create the triangle v,w,u,v.

The crossing edges of A are therefore the disjoint edges w-z(w),
together with at most the one edge v-u. The shore A is nonempty.
Since deg(v)>=2 and at most one neighbour of v lies in H, there is
at least one such w and hence a vertex z(w) in the complement.
Thus both shores are nonempty and A is a matching cut, a contradiction.

Consequently the induced graph G[H] has minimum degree at least two.
The lemma is stronger than requiring just one neighbour of degree
at least three; it uses both the triangle and four-cycle exclusions.

## 3. Counting

Write h=|H|, t=|T|, and e=|E(G[H])|. The set T is independent,
each vertex of T has two neighbours in H, and hence
n=h+t and m=e+2t.

Minimum degree two in G[H] gives e>=h. Since all vertices of H have
total degree at least three, 2e+2t>=3h. Therefore
  3m-4n
    =3e+2t-4h
    =(e-h)+(2e+2t-3h)
    >=0.
It follows that average_degree(G)=2m/n>=8/3.

## 4. Equality is also impossible

If the average degree is at most 8/3, equality must hold in the
preceding display. Both nonnegative summands vanish:
e=h and 2e+2t=3h.

Because G[H] has minimum degree at least two and degree sum 2h,
every vertex of G[H] has degree exactly two. Because every vertex
of H has total degree at least three and their total degree sum
is 3h, every vertex of H has total degree exactly three.
The vertices of T have degree two. Thus G has maximum degree at most
three.

For completeness, a finite simple graph of order at least two,
maximum degree at most three and girth at least five has a matching
cut. Forests are handled by an empty cut or a bridge. Otherwise let
C be a shortest cycle, of length L>=5. Each vertex of C has at most
one neighbour outside C. No outside vertex has two neighbours on C:
the shorter arc between them would yield a cycle of length at most
floor(L/2)+2<L. If C is not spanning, its vertex set is therefore
a nonempty proper matching-cut shore. If C spans all vertices, it
has no chord by shortestness, so the graph is precisely C_L; two
consecutive vertices form a shore with two disjoint crossing edges.

This contradicts the assumed absence of a matching cut and covers
the equality endpoint as well.

## Scope and attacks

The graph order restriction is essential: K1 still meets every positive
d and finite girth cutoff under the frozen forest-girth convention,
but has no two-nonempty-shore partition.

Girth five cannot be replaced by girth four in the theorem: K(2,3)
has average degree 12/5<8/3 and has no matching cut. To check the last
claim directly, its two degree-three vertices cannot have opposite
colours: among the three other vertices, two would share a colour,
giving two opposite neighbours at one of the degree-three vertices.
If the two degree-three vertices have the same colour, each remaining
vertex must share it to avoid two opposite neighbours. Then no
nonconstant valid colouring exists.

The theorem concerns global average degree, not maximum average degree.
It does not infer that an average-degree bound is a maximum-degree
bound: the maximum-degree conclusion was obtained only in the equality
case after two separate nonnegative counting terms vanished.

No pending extremal classification or high-girth existence theorem is
used. In the notation above, a no-matching-cut graph of order at least
two and girth at least five must satisfy the strict integer inequality
3m>4n. This is a necessary condition, not an existence claim.

## Reproduction and continuation

Inspect the exact crossing edges of the strengthened local shore,
verify the two short-cycle exclusions, check the independent degree-two
set, expand the counting identity, and inspect the equality case.
These are candidate mathematical derivations, not executed test results.

Repository transport has not been completed for this draft. A next
cycle must fresh-read main, reuse Issue #3, create a unique candidate
branch, and freeze this text and its new packet against that actual base.
Do not treat a previous PR's base as this draft's base.

best_verified_result: none
best_verified_candidate: none in the mathematical-verifier sense
open_obligations:
  obligation:opg37364-contract-edge-cases
  obligation:opg37364-root
next_action: review the local shore lemma and equality case, then
             transport the frozen draft on a newly read current base.
