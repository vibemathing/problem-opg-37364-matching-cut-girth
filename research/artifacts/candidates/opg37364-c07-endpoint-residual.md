# C07: extremal equality, shortest cycles, and an endpoint residual

Verdict: candidate_only. Candidate: candidate:opg37364-endpoint-residual-c07.
Primary owner: math-proof. Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: 48aa1f09a24aab8bbd597a4e573499ffe4b74273.

The frozen contract and K1 obstruction are retained. Positive
subsidiary assertions require n>=2. This is not an endpoint solution
or an upgrade of either admitted obligation.

## Pending source input TABC

Besides T3 from C06, let TABC denote the attributed characterization:
every no-MC graph with m=ceil(3(n-1)/2) is an ABC graph.

Source: Bonsma, Farley and Proskurowski, Extremal graphs having no
matching cuts, Journal of Graph Theory 69(2), 206-222 (2012),
https://doi.org/10.1002/jgt.20576, publisher abstract. The construction
is specified in Bonsma's 2005 conference text, Definition 1, printed
page 136, https://dmtcs.episciences.org/3398/pdf (hal-01184354v1).
TABC and T3 are separate pending dependencies; neither is an added
allowed axiom or a verifier receipt. Full Wiley proof access was not
obtained. The following conditional deductions do not assume any
unstated stability theorem for near-extremal graphs.

## C07.1 / claim:opg37364-c07-small-cycle-gap

The ABC construction starts from K1. Operation A adjoins a triangle
on an old vertex and two new vertices. B replaces one old edge uv
by two internally disjoint length-two u-v paths. C adds one vertex
joined to two old vertices, which may coincide; C is used at most once.

Every nontrivial ABC graph has a cycle of length at most four, with
parallel edges regarded as a length-two cycle. To prove this, consider
the last operation of type A or B, if one exists. It creates a triangle
or a four-cycle. Only C can follow it, and C deletes no edges, so that
cycle survives. If there is no A or B, a nontrivial output is the single
C operation on K1 and has two parallel edges. In particular, a
nontrivial simple ABC graph cannot have girth at least five.

For a simple no-MC graph of order n>=2 and girth at least five, T3
gives m>=ceil(3(n-1)/2). Equality would contradict TABC and the
previous paragraph. Since m is integral,
  m>=ceil(3(n-1)/2)+1.                         (1)
This is conditional on T3 and TABC, not on an extrapolation of T3.

If n is even, (1) says 2m>=3n. If n is odd, it says 2m>=3n-1.
Therefore a hypothetical such graph with average degree <3 must have
  n odd, m=(3n-1)/2.                          (2)
Conversely, the integer equation (2) alone does not construct a graph
or establish no-MC; it is a necessary condition only.

For fixed g>=5 and q(g) the least odd integer >=g, these statements
also yield a sufficient subsidiary threshold
  average degree < 3-1/q(g).
Indeed any no-MC graph contains a cycle and has n>=g; even n gives
average at least 3, while odd n gives at least 3-1/n>=3-1/q(g).
This conditional sufficient bound does not include d=3.

## C07.2 / claim:opg37364-c07-shortest-cycle-cut

This claim is elementary and does not use T3 or TABC.

Let C be a shortest cycle of length L>=5 in a finite simple graph.
Suppose every vertex of C has graph degree at most three. If C does
not span all vertices, the bipartition (V(C), V(G) minus V(C)) is MC.

Each vertex on C has two cycle neighbours and hence at most one
neighbour outside C. An outside vertex with two distinct neighbours
on C, joined by the shorter C-arc, would make a cycle of length at
most floor(L/2)+2<L. This contradicts shortestness. Thus every
outside vertex has at most one neighbour on C as well. Both shores
are nonempty, and each vertex is incident to at most one crossing
edge, as required.

If C spans all vertices, shortestness rules out every chord, so G is
the cycle C_L. Taking two consecutive vertices as one shore gives two
vertex-disjoint crossing edges for L>=5. Forests of order at least two
are already covered by C01. It follows that every finite simple graph
of order at least two, maximum degree at most three, and girth at least
five has MC. Girth four cannot replace five: K(2,3) from C02 is a
subcubic counterexample to that strengthened assertion.

The same proof shows that in a no-MC graph of girth at least five,
every shortest cycle contains a vertex of degree at least four.
This does not say that every cycle has such a vertex, nor does an
average-degree hypothesis imply a maximum-degree hypothesis.

## C07.3 / claim:opg37364-c07-endpoint-degree-balance

Consider the hypothetical residual (2). By C01 its minimum degree is
at least two; by C02 its degree-two vertices form an independent set.
Let t count its degree-two vertices and let
  X=sum over vertices of degree at least four of (degree-3).
The handshaking identity gives
  3n-2m=t-X=1, hence t=1+X.                   (3)
C07.2 forces some degree at least four, so X>=1 and t>=2.

Also n>=9: root a two-layer breadth-first exploration at a vertex of
degree D>=4. The D neighbours are distinct and each has another
neighbour, since minimum degree is at least two. Absence of triangles
and four-cycles forces these next neighbours to be distinct and
outside the first layer and root. Thus n>=1+2D>=9, and in fact
D<=floor((n-1)/2) for every vertex.

Necessary conditions collected for the unresolved n>=2, girth>=5,
average-degree-<3 no-MC residual, conditional on T3 and TABC:
n is odd and at least nine; 2m=3n-1; minimum degree is two;
degree-two vertices are pairwise nonadjacent; t=1+X>=2; maximum
degree is at least four and at most floor((n-1)/2); each shortest
cycle meets a degree-at-least-four vertex. By C02 one may search
a 2-connected counterexample. Selecting that piece preserves the
strict <3 bound, so the same conditional arithmetic applies to it.

None of these necessary conditions is asserted sufficient. Neither
a graph witness nor the absence of all such graphs has been obtained.

## C07.4 / claim:opg37364-c07-definition-cross-check

The University of Twente's primary thesis abstract explicitly defines
an edge cut by a nonempty proper vertex subset and then a matching-cut
as an edge cut that is a matching:
https://research.utwente.nl/en/publications/sparse-cuts-matching-cuts-and-leafy-trees-in-graphs/
Bonsma, 2006, DOI https://doi.org/10.3990/1.9789036523707.

This directly supports the frozen two-nonempty-shores convention.
It still does not supply a missing n>=2 restriction on the OPG
universal quantifier. The thesis PDF link returned HTTP 403; only
the primary abstract and metadata are used for this cross-check.
UnsolvedMath search-index text matched the original statement, but
a direct open returned a cache-miss error; no fresh full-page retrieval
or hidden small-order convention is claimed.

## Attacks, reproduction and checkpoint

The last-operation argument concerns exact ABC graphs, not graphs
one edge above their edge-count bound. In particular, deleting an
edge from a near-extremal immune graph need not preserve immunity;
it cannot turn (2) into an automatic application of TABC.

The shortest-cycle argument requires L>=5 and the degree condition
on the cycle. It is not licensed on every shortest cycle merely
because global average degree is below three. An all-vertex cycle
needs a different shore, as handled explicitly. The size-nine bound
uses minimum degree two and no cycles of lengths three or four.

Reproduce (1) by the integer gap, split parity to obtain (2), inspect
both sides of the proposed cycle cut, and sum degree excesses in (3).
Review TABC and T3 separately from these local arguments.

No solver, enumerator, proof assistant or repository command ran.
Serialization and content hashes do not verify these mathematical claims.
best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
current_blocker: nonterminal ambiguous_problem_contract and pending
                 source-faithfulness / mathematical verification.
next_action: give a nonempty-shore Boolean encoding and exact boundary
             certificates; keep the residual search bounded and unexecuted
             unless an authorized mathematical runtime is available.
