# C09: a local cut and exclusion of orders nine and eleven

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-small-order-audit-c09.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: 1da1f526db05b232c45911206a9fd73059ecfaf1.

All graphs in this note are finite and simple; MC has two nonempty
shores and allows an empty crossing matching. The frozen root is not
changed. The principal theorem below assumes an explicit edge-count
equation, rather than treating it as a consequence of average degree.

## C09.1 / claim:opg37364-c09-closed-neighbourhood-cut

Suppose minimum degree is at least two and girth at least five.
If a vertex v has only degree-two neighbours, then A={v} union N(v)
and its complement form an MC.

There are no edges among N(v), since a triangle is forbidden.
Each u in N(v) has exactly one other neighbour w(u), outside A.
These w(u) are distinct: a coincidence for u!=u' would give the
four-cycle v,u,w(u),u',v. Hence the crossing edges are exactly the
pairwise disjoint edges u-w(u). Both shores are nonempty, since
N(v) is nonempty and w(u) exists outside A.

Consequently, in a no-MC graph of order n>=2 and girth at least five,
every vertex has at least one neighbour of degree at least three.
Here minimum degree two follows first from the singleton-shore cut.

For any vertex v of degree D, absence of triangles and four-cycles
makes all second-layer neighbours distinct and outside the first
layer and root. Thus
  n >= 1+sum_{u in N(v)} deg(u)
    = 1+2D+sum_{u in N(v)}(deg(u)-2) >= 2D+2.       (A)
In particular D<=floor((n-2)/2). This improves the earlier radius-two
bound by using the explicit closed-neighbourhood cut, not a density
assumption.

## C09.2 / claim:opg37364-c09-equation-order-bound

Theorem candidate. If n>=2, girth>=5, 2m=3n-1, and G has no MC,
then n>=13.

The proof is elementary; the equation 2m=3n-1 is a hypothesis.
It does not invoke the pending extremal theorems T3 or TABC.

A no-MC graph of order at least two is connected, has minimum degree
at least two, and has no adjacent degree-two vertices. The last
assertion follows by taking such an adjacent pair as a shore:
their other neighbours are distinct, since a triangle is forbidden.
These are the explicit C01/C02 elementary cut arguments.

The shortest-cycle lemma C07.2 implies some vertex has degree at least
four. To recall its proof, a shortest cycle of length L>=5 with all
its vertices of degree at most three is an MC shore unless spanning.
An outside vertex cannot meet it twice, since this would create a
cycle of length at most floor(L/2)+2<L. The spanning case is an
unchorded cycle and has an MC using two consecutive vertices.
A forest is handled by a bridge. No extremal theorem is used here.

The equation makes n odd. Bound (A) and a vertex of degree at least
four give n>=10, hence n>=11. It remains to exclude n=11.

Assume n=11. Bound (A) forces maximum degree four. Let H, P, T be
the vertices of degrees four, three, two, respectively, with sizes
h,p,t. Summing 3-deg(v) and using 3n-2m=1 gives
  t-h=1,   t=h+1,   p=10-2h,   1<=h<=5.           (B)
The set T is independent. At any vertex of H, the stronger part of
(A) gives
  sum over its neighbours of (degree-2) <= 2.      (C)

Two adjacent vertices of H would each have three other neighbours
in T by (C). Those two triples are disjoint, since a shared neighbour
would make a triangle. Thus H is independent whenever t<=5, which
covers h<=4.

### Case h=1: t=2, p=8

The unique degree-four vertex v has exactly two T neighbours and two
P neighbours a,b, by (C) and the total number of T vertices.
The radius-two count is then equality: 1+2+2+3+3=11.
All six second-layer vertices lie in P. Each has exactly one neighbour
in the first layer and none at the root; otherwise there is a triangle
or four-cycle. Its other two neighbours must therefore be within the
six-vertex second layer.

The induced second layer is a simple 2-regular graph with girth at
least five, hence is C6. The two children of a must be opposite on
that C6: distance one or two would give a triangle or four-cycle
through a. Joining a to the length-three arc between its children
produces a five-cycle all of whose vertices are in P. It is a shortest
cycle because the ambient girth is at least five. C07.2 gives an MC,
contrary to the hypothesis.

### Case h=2: t=3, p=6

The two H vertices v,w are nonadjacent. Each has at least two T
neighbours by (C). They cannot share two neighbours because of a
four-cycle. With only three T vertices, each therefore has exactly
two T neighbours, sharing exactly one, z. Write the others as t_a
at v and t_b at w. Each H vertex also has two P neighbours; the
two P pairs are disjoint, since v and w already share z.

The radius-two count at v and at w is equality. In particular t_b
lies at distance two from v, so its endpoint other than w is one
of v's two P neighbours (T is independent). Similarly, the endpoint
of t_a other than v lies in w's P pair.

It follows that the induced graph on the six P vertices has degrees
1,2,1,2,3,3: one vertex in each pair has an additional T neighbour,
and the two remaining P vertices have no neighbour outside P.
Its degree sum is twelve, so it has six edges and contains a cycle.
The two degree-one vertices cannot belong to a cycle, leaving at
most four possible cycle vertices. This contradicts girth at least
five.

### Case h=3: t=4, p=4

H is independent. Each H vertex has at least two T neighbours by (C),
so there are at least six H-T incidences. Let q be the number of T
vertices with two endpoints in H, and r the number with exactly one
endpoint in H. Then q+r<=4 and 2q+r>=6, so q>=2.
Also q<=3, since there is at most one shared T vertex per pair of H
vertices.

If q=3, every pair of H vertices shares a T neighbour. A P vertex
cannot then have two H neighbours, because a four-cycle would result.
But r<=1, so the number of H-P incidences is 12-(6+r)>=5, exceeding
the four available P vertices.

If q=2, the inequalities force r=2 and exactly six H-T incidences.
Every H vertex has two T and two P neighbours. The two shared-T
pairs form a path on the three H vertices. The middle vertex's two
P neighbours are disjoint from the P neighbours of either endpoint.
Only four P vertices exist, so both endpoints must share the other
two P vertices. This again gives a four-cycle.

### Case h=4: t=5, p=2

H is independent. By C09.1 every H vertex has at least one P
neighbour. Let k be the number of H-P edges. At most one H vertex
can meet both P vertices, since otherwise a four-cycle results.
Thus 4<=k<=5.

The induced graph on H union P has
  (4h+3p-2t)/2=(16+6-10)/2=6
edges, since T is independent and has total degree 2t.
It has no H-H edges and at most one P-P edge. Therefore k=5 and the
P-P edge exists. The H vertex adjacent to both P vertices then
forms a triangle with that edge, a contradiction.

### Case h=5: t=6, p=0

Every H vertex has an H neighbour by C09.1, and at most one by (C).
Thus the induced graph on H is 1-regular on five vertices, impossible
because the sum of its degrees would be odd.

These five cases exhaust (B), exclude n=11, and complete C09.2.

## C09.3 / claim:opg37364-c09-conditional-residual-refinement

C07 derived, conditional on the separate pending source theorems
T3 and TABC, that a no-MC graph with n>=2, girth>=5 and average degree
<3 must satisfy 2m=3n-1. Combining only that attributed implication
with C09.2 raises the necessary order from nine to thirteen.

The local theorem C09.2 has no external theorem dependency; the
translation from average degree <3 to its edge-count hypothesis does.
No graph with n>=13 is constructed or excluded by this note.
No positive endpoint statement for every order is asserted.

## Attacks, finite scope and reproduction

At n=11 the degree partition is exhaustive only after the improved
radius-two bound excludes degree five. The claim that every H vertex
has a P neighbour is used only in cases with H independent. In h=5
the required neighbour is in H instead. The two shared-neighbour
restrictions always use a genuine four-cycle with distinct vertices.

Equality of a radius-two count is used only in h=1 and h=2. In h=2,
the contradiction is in the induced six-vertex P graph, not a claim
that all six-vertex six-edge graphs have short cycles. Its two leaves
are essential. In h=1, the five-cycle is shortest in the original
graph and excludes the unique degree-four vertex.

Reproduce the local shore, the radius-two injectivity count, the
handshaking equation, and the five displayed cases. These are concise
finite derivations, not outputs of graph generation or an exhaustive
computer run. No solver, enumerator, proof assistant or repository
command was executed; local serialization and hashes are not receipts.

Sources are the frozen contract and the explicit elementary candidate
arguments in C01, C02 and C07. T3/TABC source locators remain in C06/C07.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
current_blocker: nonterminal source-domain ambiguity and pending
                 mathematical/statement-faithfulness verification.
next_action: formalize the nonempty-shore obstruction without importing
             unproved extremal claims; use the n>=13 residual only as
             a necessary condition in any later bounded search.
