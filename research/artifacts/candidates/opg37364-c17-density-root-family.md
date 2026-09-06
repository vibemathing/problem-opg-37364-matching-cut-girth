# C17: elementary no-matching-cut families below every fixed d>4

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-density-root-c17.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: dce0f17a89e751cac6795812f27d5541298be030.

## Statement and dependency boundary

For every real d>4 and every integer g>=3, there is a finite simple
2-connected bipartite graph G with
  4 < average_degree(G) < d,
  girth(G)>=g,  minimum_degree(G)=2,
  maximum_degree(G)<=40+ceil(144/(d-4)),
and no matching cut. In particular, fixing d0=5 gives a deterministic
family for all integer girth thresholds, with maximum degree at most
184 and average degree strictly below 184/37<5.

The existence input is C16's fully written finite-counting argument,
not a new axiom and not the former imported T14 theorem. The present
proof adapts the finite augmentation mechanism of C04 with its constants
recomputed for the C16 seed. The two notes together are a self-contained
classical root-negation candidate using finite combinatorics and real
arithmetic. Both admitted obligations remain open in the trusted ledger.
No originality, optimal threshold, computation run or verifier receipt
is asserted.

MC always means two nonempty shores whose entire crossing set is a
matching, possibly empty. No change to the frozen contract is made.

## C17.1. The C16 seeds are 2-connected

Write H_h for C16's deterministic graph at integer parameter h>=3.
It is simple, connected and bipartite, has all degrees 39 or 40,
girth at least h, and
  |delta_H(S)| > |S|  for 1<=|S|<=|V(H)|/2.            (1)

Suppose x is a cut vertex, and choose a smallest component C of H-x.
Then |C|<= (|V(H)|-1)/2 and its only possible external neighbour is x.
Assume x is in the left bipartition class. Every vertex retains at
least 38 neighbours after x is removed, so C contains both classes.
A left vertex in C has all of its at least 39 neighbours in the right
class of C. A right vertex in C has at least 38 neighbours in the left
class of C. Therefore |C|>=39+38=77. But
  |delta_H(C)|<=degree_H(x)<=40,
contradicting (1). The other bipartition class is symmetric. The graph
has more than two vertices, so it is 2-connected.

This uses actual minimum and maximum degrees of H, not an unsupported
replacement of global average degree by minimum degree.

## C17.2. Parameter order and a sufficiently large seed

Fix d>4, put epsilon=d-4>0, and choose the integer
  k=ceil(144/epsilon),  D=40+k.
For fixed g>=3 define
  B=1+D*sum_{j=0}^{g-3}(D-1)^j,
  h=max(g,4B+1).                                      (2)
All parameters are finite, and D depends on d but not g.
The ball of radius g-2 in any simple graph of maximum degree at most
D has at most B vertices: count at most D(D-1)^(l-1) non-returning
walks of each positive length l<=g-2, plus its centre.

Take H=H_h from C16, with its inherited vertex labels and bipartition
X,Y; write n=|V(H)| and m=|E(H)|. The seed has minimum degree 39,
so it contains a cycle. Consequently
  n>=girth(H)>=h>4B,  39n<=2m<=40n.                   (3)
The dependency order is not circular: choose d,k,D,g,B,h first;
then use C16 at the integer h. The seed's actual order need not be
known in advance of that choice.

## C17.3. Finite maximal augmentation

Start with F empty and J=H. Repeatedly add the lexicographically first
pair uv for which:
- u and v are distinct vertices of the same original part X or Y;
- uv is not already an edge of J;
- both endpoints have F-degree below k;
- their distance in the CURRENT graph J is at least g-1.
Stop when there is no such pair. This is a deterministic finite
process, with at most floor(kn/2) additions.

At every step J=H+F is simple, has maximum degree at most D and girth
at least g. Indeed any newly created cycle uses uv and a previous
u-v path of length at least g-1. All seed edges are retained.
The current distance, rather than a distance measured only in H,
is essential for this invariant.

In either original part, at most B vertices have F-degree below k.
Otherwise take one such u and another such v outside the radius-(g-2)
ball of u in the final J. They have available F-degree, are nonadjacent,
and adding uv is legal by the preceding cycle argument, contrary to
termination. Apply this separately to X and Y.

Writing t=|F|, at least n-2B vertices have F-degree k. By (3),
  2t=sum_v degree_F(v)>=k(n-2B)>kn/2,
hence
  t>kn/4>0.                                          (4)

## C17.4. Subdivide only the added edges

For each artificial edge e=uv of F, replace it by u-w_e-v with a
distinct new vertex w_e. Do not remove or subdivide any edge of H.
Let G be the resulting graph. The old vertex set induces exactly H;
the new vertices are pairwise nonadjacent and each has two distinct
old neighbours.

The graph is finite and simple. It is bipartite: if u,v are in X,
put w_e in the other part, and conversely for Y. Every cycle in G
projects to a cycle of the simple J when its new degree-two vertices
are suppressed. The projected cycle has no greater length. Distinct old vertices
remain distinct; a projected two-edge cycle would require parallel
edges in J, which its simplicity excludes. Thus
  girth(G)>=girth(J)>=g.
The old degrees are at most 40+k, and each new degree is two.
By (4) new vertices exist, so the minimum degree is exactly two.

The graph is 2-connected. Deleting an old x leaves H-x connected by
C17.1, and every new vertex retains at least one old neighbour.
Deleting one new vertex leaves H connected and every other new vertex
attached. These vertex-deletion tests, with order at least three,
prove the assertion.

## C17.5. Every nontrivial cut fails to be a matching

Consider any partition of V(G) into two nonempty shores.
If both shores meet H, restrict the partition to H. By C16 there is
an old vertex with at least two old crossing neighbours. Its two
crossing edges are still present in G.

Otherwise all old vertices lie on one shore. The other nonempty shore
contains a new vertex w_e; its two distinct old neighbours both lie
opposite it, giving two incident crossing edges. These cases cover
every nontrivial partition. Therefore G has no matching cut.

The proof uses the unchanged induced core. It does NOT infer that
edge expansion (1) survives after increasing the vertex set, or that
arbitrary subdivision preserves absence of MC. It also does not confuse
a matching in G with a matching that is an edge cut.

## C17.6. Strict density and the root witness d0=5

We have |V(G)|=n+t and |E(G)|=m+2t. By (3) and (4),
  average_degree(G)
    =4+(2m-4n)/(n+t)
    <=4+36n/(n+t)
    <4+144/(k+4)
    <4+epsilon=d.                                    (5)
The final strict inequality holds because k>=144/epsilon and
epsilon>0, so epsilon(k+4)>144. Also 2m>=39n implies
  average_degree(G)>=4+35n/(n+t)>4.                  (6)
No assertion at d=4 is obtained or silently included.

For the root, fix the rational d0=5 once and for all. Then epsilon=1,
k=144 and D=184, independently of g. For each integer g>=3 use
(2) and the two deterministic finite selectors. Equations (5)-(6) give
  4<average_degree(G)<4+144/148=184/37<5,
  girth(G)>=g,  no MC(G).
The density comparison 184/37<5 is the integer inequality 184<185.
This supplies exactly
  exists real d0>0, forall integer g>=3,
  exists finite simple G with average<d0 and girth>=g and no MC.

The family is finite at every g and has unbounded girth. It is not
the finite C11 witness and does not depend on forest girth or K1.
For the real-parameter variant k is a mathematical integer choice.
Computability is asserted for the fixed rational d0=5 (and rational
inputs d>4), not for arbitrary noncomputable real input.

## C17.7. Why the naive core reduction cannot prove the root

The old core H is induced in G and has average degree at least 39.
Thus these graphs can have global average below five but maximum
average degree and degeneracy at least 39. The new degree-two vertices
form an edgeless set. Deleting them recovers H; this deletion does not
preserve the original average-degree upper bound. In fact the 3-core
is exactly H: the new vertices cannot survive a minimum-degree-three
subgraph, while every old vertex has at least 39 old neighbours.

These are unbounded-girth witnesses to the distinction, not merely
isolated-vertex padding or bridge attachments. The 2-connectedness
above excludes those easy cuts. The argument does not deny valid
reductions with explicitly changed parameters.

## Audit and verification handoff

Root proof dependencies: C16.1-C16.8 and C17.1-C17.6. C17.7 is an
additional audit consequence, not needed for the root. C04 supplies
an attributed internal construction idea; all changed constants and
premises are proved here. C15's spectral/prime input and T3/TABC/T14
are not mathematical dependencies of this proof chain.

A trusted check should first formalize C16's permutation-slot count
and coloured overlapping-cycle count, then its simplification and
strict cut bound. It can then check this finite greedy augmentation,
the unchanged-core cut argument and the fixed rational d0=5 mapping.
There is no need to execute the enormous brute-force family selector
to verify its existence proof.

The source small-order question is retained historically. These
nontrivial 2-connected cyclic witnesses qualify under both the
literal contract and the discussed n>=2/connected source readings;
no contract repair or undefined empty-graph average is used.

No graph generator, sampler, SAT solver, spectral calculation, proof
assistant or mathematical verifier was executed. File hashing and
GitHub checks are not mathematical evidence. The companion handoff
is a request, not a receipt; the generator cannot extend fixture
verifier policies or create an EvidenceLink/Result.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
best_candidate: candidate:opg37364-density-root-c17,
                with candidate:opg37364-elementary-unbounded-c16.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: trusted verification of the finite-counting root chain,
followed by statement-faithfulness and admission gates; do not restart
a search for a finite witness or the contradicted size-only route.
