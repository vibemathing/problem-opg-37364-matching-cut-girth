# C04: global average degree is not maximum average degree

Verdict: candidate_only. Kind: proof / conditional assumption audit.
Candidate: candidate:opg37364-average-audit-c04. Owner: math-proof.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: 0de3e02657c0ab47b8ccc4b031382db2adbf1310.

The contract is unchanged. MC means two nonempty shores with a possibly
empty crossing matching. Both admitted obligations remain open. T14 is
the attributed, pending external dependency documented in C03, not an
extra allowed axiom. All conclusions using T14 are conditional on its
faithful reuse. No novelty claim is made.

## Objective and definitions

Test whether one may replace the contract's global average degree by
maximum average degree, or simply delete degree-two vertices while
preserving the same density bound. Define mad(G) as the maximum of
2|E(Q)|/|V(Q)| over nonempty subgraphs Q of G, and degeneracy as the
maximum of the minimum degrees of those Q. These are distinct from
the global average degree. The following construction keeps an induced
14-regular core but lowers the global average below any prescribed d>4.

## C04.1 / claim:opg37364-c04-core-inheritance

Let H be a graph without MC. Retain every edge of H, and add vertices
each adjacent to exactly two distinct vertices of H, with no edges
between added vertices. The resulting G has no MC.

If an MC colouring of G uses both colours on H, restricting it to H
gives an MC of H: the crossing edges are a subset of the crossing
matching of G. Otherwise all vertices of H have one colour. Any added
vertex of the other colour has two incident crossing edges, impossible.
Thus both colours cannot occur on G. This proves the claim.

This is not the assertion that arbitrary subdivision preserves absence
of MC: subdividing one edge of C3 produces C4, which has MC.

## C04.2 / claim:opg37364-c04-finite-augmentation

Fix real d>4 and integer g>=3. Put epsilon=d-4,
k=ceil(40/epsilon), D=14+k, and
  B=1+D*sum_{j=0}^{g-3}(D-1)^j.
These are finite; k>=1. A graph of maximum degree at most D has at most
B vertices at distance at most g-2 from any given vertex: count the
initial vertex and at most D(D-1)^{l-1} walks without immediate reversal
at each positive length l<=g-2.

Apply T14 at h=max(g,4B+1) to obtain a connected simple 14-regular
bipartite H of girth at least h and without MC. Let n=|V(H)|, with
bipartition X,Y. Such H has a cycle: a nonempty finite forest cannot
be 14-regular. Hence n>=girth(H)>=h>4B. Also |E(H)|=7n.
C03's elementary bipartite degree count shows H is 2-connected.

Choose an inclusion-maximal set F of additional edges on V(H) satisfying:
each edge joins two distinct vertices of the same original part X or Y;
deg_F(v)<=k for every v; J=H+F is simple and has girth at least g.
The empty set is admissible, and the universe of possible edges is finite,
so a maximal F exists. Let t=|F|. The maximum degree of J is at most D.

At most B vertices in X can have F-degree less than k. Otherwise choose
one such u and another such v outside its distance-(g-2) ball in J.
The pair uv is absent and may be added: its endpoints are unsaturated,
it stays inside X, and every new cycle has length at least g, because
the previous distance is at least g-1. This contradicts maximality.
The same argument holds in Y. At least n-2B vertices therefore have
F-degree k, and
  2t=sum_v deg_F(v)>=k(n-2B)>kn/2,
so t>kn/4.

This is a finite existence construction, not a claimed execution. A
greedy implementation may add only currently legal pairs and stops
after at most floor(kn/2) additions. Distances must be evaluated in
the current J, not only in the original H.

## C04.3 / claim:opg37364-c04-geometry

Replace each artificial edge e=uv of F by u-w_e-v, using a distinct
new vertex w_e. Do not subdivide, remove or alter any edge of H.
Call the resulting graph G.

It is finite and simple. Added vertices form an edgeless set, have
degree two, and have distinct old neighbours. Old degrees are
14+deg_F(v), so the maximum degree is at most D and, since t>0,
the minimum degree is exactly two.

The graph is bipartite: when u,v belong to X, put w_e in the Y part,
and conversely. Every cycle projects, by suppressing the distinct
new degree-two vertices, to a cycle of the simple graph J of no
greater length. Thus girth(G)>=girth(J)>=g.

It is 2-connected. Deleting an old vertex x leaves H-x connected;
each new vertex still has at least one old neighbour. Deleting a
new vertex leaves H connected and every other new vertex attached.
G has at least three vertices. These deletion tests prove the claim.

C04.1 applies to the unchanged H core, so G has no MC.

## C04.4 / claim:opg37364-c04-strict-density

The counts are |V(G)|=n+t and |E(G)|=7n+2t. In particular,
  average_degree(G)=4+10n/(n+t)
                  <4+40/(k+4)
                  <4+epsilon=d.
The first strict inequality uses t>kn/4. The second uses
k>=40/epsilon, so k+4>40/epsilon. The value is also strictly greater
than four; this construction gives no conclusion for d<=4.

H is induced on the old vertices of G. Consequently mad(G)>=14 and
degeneracy(G)>=14 even though the global average degree is <d.
Deleting all added degree-two vertices recovers H of average degree 14.

Conditional conclusion: for every d>4 and every integer g>=3, the
construction gives a 2-connected bipartite graph of girth at least g,
without MC, of average degree <d, and of maximum degree at most
14+ceil(40/(d-4)), containing an induced 14-regular core.

In particular d=5 yields global average degree <5 and mad/degeneracy
at least 14 at arbitrary girth. It is an exact conditional obstruction
to replacing average degree by maximum average degree, or to naive
degree-two deletion preserving the same bound. The new degree-two
vertices are pairwise nonadjacent. This does not deny the possibility
of other, explicitly proved transformations with changed parameters.

## Attacks, scope and review gaps

- Isolated vertices and bridge attachments are not used.
- One old neighbour per added vertex would create a singleton cut;
  the two distinct old neighbours are essential.
- Arbitrary subdivision is not used: all original H edges remain.
- Initially distant pairs alone would not suffice; maximality uses
  the current J and its girth after previous additions.
- Repeated artificial pairs are prohibited by simplicity; creating
  several length-two paths on one pair would create a short cycle.
- The count is 7n+2t, not 7n+t.
- No perfect matching in the augmented graph is asserted.
- The bound four is not asserted to be optimal, and no statement at
  the endpoint d=4 or below is obtained.
- The n>=2 witnesses do not erase K1 from the literal contract; C01's
  nonterminal ambiguous_problem_contract flag is retained.

## Reuse, reproduction and nonterminal checkpoint

Sources: C03 and its primary-source map at the base above; T14 is
Feghali, Lucke, Paulusma and Ries, arXiv:2212.12317v5, Lemma 5,
https://arxiv.org/html/2212.12317v5 .
The 2025 version of record is identified in the C03 source note.
Bounded searches for matching-cut/girth/density and degree-two reuse
were checked; no claim of exhaustive search or novelty is made.

A reviewer can verify C04.1 without external input, check the finite
ball bound and maximality proof, then audit every graph operation
and strict inequality. A separate review must validate the T14
dependency and its exact meaning under this contract. No graph
generator, solver, proof assistant or repository command was run.
Artifact hashes are not mathematical verification.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: seek a justified degree-two suppression reduction with
             explicitly changed density and girth parameters, rather
             than the same-parameter deletion rejected here.
