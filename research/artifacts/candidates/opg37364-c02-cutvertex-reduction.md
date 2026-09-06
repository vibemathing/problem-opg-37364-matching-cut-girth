# C02: density-preserving cut-vertex reduction

Verdict: candidate_only. Candidate: candidate:opg37364-cutvertex-c02.
Owner: math-proof. Kind: proof, within the contract-faithfulness audit.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: fb078f6f3aa0c7cbaae06dd7bed5de1129004b59.
Contract SHA-256: cb72346bada4d4c41ce287a6d04f4b756717cc0a12cdb85ace863b379873d0eb.
Both admitted obligations remain open; no verifier receipt is supplied.

## Scope and prior inputs

MC(G) retains the frozen definition: both shores nonempty, crossing matching
possibly empty. All graphs are finite and simple. Order zero has undefined
average degree and is not assigned one. The n>=2 assertions below are
explicitly subsidiary; they do not remove K1 from the original quantifiers.

C01, already on this base, supplies the elementary disconnected, bridge and
degree-at-most-one arguments. Its source-faithfulness flag is retained.
The failed-route ledger is unchanged from the preceding candidate-only PR;
no ledger entry is written here. A bounded search for cut-vertex/block
reuse did not supply a theorem used as a black box below. In particular,
results about proper disconnection numbers are not substituted for MC.
No novelty is claimed for the elementary block reduction.

## C02.1 / claim:opg37364-c02-local-global

Let G be connected and x a cut vertex. Let C_1,...,C_k, k>=2, be the vertex
sets of the components of G-x, and H_i=G[C_i union {x}].
Then MC(G) holds if and only if MC(H_i) holds for at least one i.

Proof. Each H_i is connected: every C_i has a neighbour of x, since G is
connected. If H_i has an MC two-colouring, assign every vertex outside H_i
the colour of x. No edge connects distinct C_j, and all other edges to x
are monochromatic. The crossing edges in G are exactly the crossing edges
in H_i. Both colours still occur, so the colouring extends an MC of G.

Conversely, a nontrivial colouring of connected G has a crossing edge.
That edge lies in one H_i. Restrict the colouring to H_i. Both colours
occur at its endpoints; the restricted crossing edges form a subset of
the matching in G. Thus this H_i has MC. This proves both directions.
In particular, if G has no MC, every H_i has no MC.

## C02.2 / claim:opg37364-c02-density

Write n=|V(G)|, m=|E(G)| and n_i=|V(H_i)|, m_i=|E(H_i)|.
Each n_i>=2, the edge sets partition E(G), and x is counted k times, so
sum_i m_i=m and sum_i n_i=n+k-1. Consequently
  (sum_i n_i * (2m_i/n_i)) / (sum_i n_i) = 2m/(n+k-1) < 2m/n.
The last inequality is strict because m>0 and k>=2.
Some H_i therefore has average degree strictly smaller than G.
It is not necessary, and is generally false, that every H_i does.

Every cycle of H_i is a cycle of G; hence girth(H_i)>=girth(G), with the
given +infinity convention. Since k>=2, each H_i is a proper induced
subgraph with 2<=n_i<n. Thus selecting a minimum-average-degree H_i
preserves average degree <d and girth >=g and strictly decreases order.

## C02.3 / claim:opg37364-c02-two-connected

Fix d>0 and integer g>=3. If there is a graph G of order at least two,
average degree <d and girth >=g without MC, there is such a graph H that
is 2-connected. Here 2-connected means order at least three, connected,
and with no cut vertex.

Proof. G cannot be disconnected, by C01's component-shore argument.
While the current graph has a cut vertex, select an H_i from C02.2.
C02.1 preserves absence of MC; C02.2 preserves the numerical hypotheses
and lowers the positive integer order. There are at most |V(G)|-2 such
steps. The final graph is connected and has no cut vertex, and has order
at least two. A connected simple graph of order two is K2 and has an MC,
so the final graph has order at least three. It is the required H.

Conversely any such 2-connected H is already an order-at-least-two
counterexample candidate. Therefore, for each fixed d,g, the assertion
that all qualifying n>=2 graphs have MC is equivalent to the assertion
restricted to qualifying 2-connected graphs, with exactly the same d,g.

For the literal nonempty-graph assertion the faithful logical reduction is
  MC(K1) AND [all qualifying 2-connected graphs have MC].
K1 satisfies the numerical hypotheses for every d,g in scope, and C01
shows MC(K1) fails. The K1 conjunct cannot be erased. The displayed
reduction is not a repaired ProblemContract or a Result admission.

## C02.4 / claim:opg37364-c02-degree-two-pair

If G has girth at least four and adjacent degree-two vertices u,v,
it has MC. Let a be u's neighbour other than v, and b be v's neighbour
other than u. Simplicity gives a,b outside {u,v}. If a=b then a,u,v form
a triangle, which is excluded. Thus a,b,u,v are distinct. The shore
{u,v} is nonempty and proper, and its crossing edges are exactly ua,vb,
which are disjoint. They give the claimed matching cut.

Combining with C02.3 and C01, at girth at least four the residual n>=2
search can be restricted to 2-connected graphs of minimum degree at
least two with no adjacent degree-two vertices. This is a precisely
proved restriction, not an assertion of an absolute strongest possible
reduction among all conceivable graph properties.

## C02.5 / claim:opg37364-c02-attack-witnesses

A. An arbitrary block need not preserve the average-degree upper bound.
Take K3 and K5 sharing exactly one vertex x and no other vertices or edges.
The resulting connected graph has n=7, m=13 and average degree 26/7.
At d=39/10 it qualifies, since 260<273. The K5 piece has average degree 4,
which is not <39/10. The K3 piece does have smaller average degree.
Each clique of order at least three has no MC: if a partition of a clique
has both shores nonempty, its crossing graph is complete bipartite; it
can be a matching only when both shores have size one. By C02.1 the
wedge has no MC. Its girth is three. This is an exact attack on choosing
an arbitrary block, not on the minimum-average selection.

B. Minimum degree three is not implied by the proved triangle-free
residual conditions. K(2,3) is simple, 2-connected, of girth four, with
three pairwise nonadjacent degree-two vertices and no MC. Let its two
degree-three vertices be the hubs. If the hubs receive the same colour,
any leaf of the opposite colour has two crossing edges, so all vertices
would have to be monochromatic. If the hubs receive different colours,
each of the three leaves has exactly one crossing edge. A matching can
use at most two edges incident with the two hubs, a contradiction.
Removing any vertex leaves K(1,3) or K(2,2), both connected; a 4-cycle
exists and bipartiteness excludes odd cycles. These verify all premises.

This does not rule out a separate, newly proved reduction for girth >=5;
it only rejects the unsupported implication from the stated girth-four
conditions to minimum degree >=3. Do not repeat that implication.

## Dependency map, verification and checkpoint

C02.1 and C02.2 use only the component definitions and finite counting.
C02.3 uses C02.1, C02.2 and the explicit C01 cuts; termination uses
strict decrease of order. C02.4 is the explicit four-endpoint cut.
C02.5 checks the two tempting stronger reductions by exact small graphs.
No graph enumerator, CAS, solver, proof assistant or repository command
was run. Text hashes identify artifacts and are not mathematical checks.

Reproduction: draw the vertex/edge sets of each H_i, verify both cut
directions, sum n_i and m_i, and check each strict inequality. Reproduce
the two witness arguments and ensure the K1 conjunct is retained.
A trusted statement-faithfulness review and the declared kernel/axiom
audits are still required before any obligation can be closed.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
route_status: active, with nonterminal source-domain ambiguity.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: audit the nontrivial 14-regular high-girth source family,
             its quantifiers and the strict choice d>14, without using
             it as unreviewed mathematical Evidence.
