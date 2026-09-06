# C21: a degree-63 fixed-five family without the nested girth parameter

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-degree63-density-c21.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: 9491f4b15e504fc415362ba55591483a941443a6.

## Statement

For each real d>4, put
  k=max(1,ceil(40/(d-4))-1).
For every integer g>=3, there is a finite simple 2-connected bipartite
graph G with no matching cut, girth at least g, minimum degree two,
maximum degree at most24+k, and
  4<average_degree(G)<4+80/(2k+3)<d.                    (1)

At the fixed rational d0=5, k=39, so
  maximum_degree(G)<=63,
  average_degree(G)<404/81<5.                          (2)
An explicit order bound at this fixed d0 is
  |V(G)|<=656*(2g)^4*(384*g^2)^(4g).                   (3)

This reduces C18's degree112 bound and removes the need for its
exponentially large auxiliary girth input. The number404/81 is NOT
claimed to be a smaller numerical average-degree bound than364/73:
both are below5, and the improvement here concerns maximum degree
and the explicit order estimate. No optimality or novelty is asserted.

All graph definitions and root quantifiers are unchanged. Both shores
of a matching cut are nonempty; its crossing matching may be empty.
The proof uses C20's expanded elementary counting argument, not an
imported existence theorem or a newly added axiom. Both admitted
obligations remain open. No mathematical runtime was executed.

## C21.1. Uniform-size reading of C20

C20's proof in fact applies at every integer M satisfying
  M>=max(1000,4C_g,2g),
  C_g=(2g)^2*(96*(2g)^2)^(2g), N=M^2.                 (4)
This is checked from its hypotheses, rather than assumed from a
single selector: the small/large-shore split uses M>=1000; the overlap
estimate uses M>=4C_g and N>=2(2g); and all graph operations retain
the same bounds. Thus its positive finite count and degree23-or24
conclusion hold at every such M.

For each (g,M), choose the lexicographically first tuple satisfying
the two C20 good predicates and apply its matching deletion. Denote
the resulting seed by H(g,M). It has n=2M^2 vertices, degrees23 or24,
girth at least g, strict all-shore boundary, and no matching cut.
C20's bipartite45-versus24 argument proves 2-connectivity at every
g>=3; no additional girth condition is required.

This uniform-size restatement changes no probability estimate and
does not assert that the same permutation tuple works at different M.

## C21.2. Parameters, ball bound and saturation

First choose integers k>=1 and g>=3. Define
  D=24+k,
  B=1+D*sum_{j=0}^{g-3}(D-1)^j,
  M=max(1000,4C_g,2g,2kB+1).                          (5)
All quantities in (5) are explicit positive integers. Take H=H(g,M)
with its inherited bipartition X,Y and n=2M^2 vertices. Then
  n>4kB,   23n<=2m<=24n,                             (6)
where m=|E(H)|. Indeed M>=2kB+1 implies2M^2>=2M>4kB.

Add artificial pairs F on the old vertex set, only within X or within Y.
Repeatedly take the least currently legal pair uv: its endpoints are
distinct, have F-degree below k, and have distance at least g-1 in
the current J=H+F. The distance condition excludes an existing edge.
Every new cycle uses uv and an earlier path of length at least g-1,
so J remains simple with girth at least g and maximum degree at most D.

Each addition raises the F-degree sum by two, while that sum is at
most kn. Hence the procedure terminates after at most floor(kn/2)
additions and is maximal for these conditions.

In a graph of maximum degree at most D a ball of radius g-2 has at
most B vertices. At positive length ell, count at most
D(D-1)^(ell-1) walks without immediate reversal; the sum bounds the
number of distinct vertices even when paths collide.

At most B old vertices in X can remain unsaturated. Otherwise choose
one unsaturated u and another outside its radius-(g-2) ball. They would
form a legal pair, contradicting termination. Repeat in Y. Consequently,
with t=|F|,
  2t>=k(n-2B)>kn-n/2,
or equivalently
  4t>(2k-1)n.                                        (7)
The strict improvement over C18's (k-1)n bound uses n>4kB in (6).
It also ensures t>0 when k=1.

## C21.3. Transform only the new edges and audit every cut

Replace each artificial edge uv by u-w_uv-v with its own new vertex.
Keep all edges of H. Call the new graph G.

The graph is simple. Colour each w_uv by the opposite bipartition
part from its two old endpoints. This makes G bipartite. A cycle of G
projects under suppression of the new degree-two vertices to a cycle
of the simple J, of no greater length. The old vertices on the cycle
are distinct; a projected two-edge cycle would require parallel
edges in J. Thus girth(G)>=girth(J)>=g.

Deletion of an old x leaves H-x connected; each new vertex still
has at least one old neighbour. Deletion of a new vertex leaves all
of H connected and all other new vertices attached. Since the order
is at least three, this proves 2-connectivity.

The old degrees are at most24+k, and every new degree is two.
By (7) a new vertex exists. The induced subgraph on old vertices is
exactly H and has minimum degree at least23.

In a two-nonempty-shore colouring, either both colours occur on H or
only one does. In the first case a crossing matching would restrict
to a crossing matching in H, contrary to C20. In the second case any
new vertex on the other nonempty shore has its two distinct old
neighbours opposite it. Its two crossing edges prevent a matching.
Hence G has no matching cut.

The argument does not assert that edge expansion itself survives
addition of new vertices, or that arbitrary edge subdivision preserves
absence of matching cuts.

## C21.4. Exact density and fixed-real quantifiers

There are n+t vertices and m+2t edges. Equations (6)-(7) give
  average_degree(G)=4+(2m-4n)/(n+t),
  4+19n/(n+t)<=average_degree(G)
                 <=4+20n/(n+t)<4+80/(2k+3).           (8)
In particular the average is strictly greater than4.

For real d>4 let r=40/(d-4), s=ceil(r), k=max(1,s-1).
Then k+1>=s>=r, whence2k+3>2r and
  80/(2k+3)<80/(2r)=d-4.
This proves (1). For d0=5, the integer choices are s=40 and k=39.
Then2k+3=81 and24+k=63, proving (2), with404<405.

Fix d0=5 and k=39 before the integer input g. The two lexicographic
finite procedures specify a graph for each g>=3. The universe for
the seed is finite and nonempty by C20; augmentation is bounded by
floor(kn/2). No computation of a noncomputable real input is claimed.
The graph contains a cycle because H has minimum degree at least23.
Thus the girths are unbounded finite girths, not a convention for forests.

This gives exactly a fixed positive real d0 followed by a graph
witness for every integer girth threshold, while retaining the
frozen simple-graph and nonempty-shore definitions.

## C21.5. Direct seed at the input girth and the order bound

For every D>=2 and g>=3, the finite ball sum satisfies
  B<=sum_{ell=0}^{g-2} D^ell<=D^(g-1).                 (9)
For k=39, D=63, so2kB+1<=78*63^(g-1)+1.
Put K=2g>=6. Then
  4C_g=4K^2*(96K^2)^K
       >=144*63^K
        >78*63^(g-1).
The last strict inequality follows from144>78 and K>=g-1.
Since both sides are integers, 4C_g>=78*63^(g-1)+1>=2kB+1.
Also4C_g>1000 and4C_g>=K. Thus the maximum in (5) is exactly
  M=4C_g,
the same explicit size used by C20 at input g itself. In particular
no seed at a larger, nested girth parameter is needed for d0=5.

Since t<=kn/2 and n=2M^2,
  |V(G)|<= (k+2)M^2=41*(4C_g)^2
          =656*K^4*(96K^2)^(2K)
          =656*(2g)^4*(384*g^2)^(4g).
This is (3). It is only an upper bound for this elementary selector.
It is not asserted to be the best known order at prescribed girth.

For other d>4 the extra term2kB+1 in (5) is retained. Omitting it
uniformly when k can be arbitrarily large would need a new argument.

## Attacks, dependence and next verification task

C21.1 checks every occurrence of M in C20 before increasing its value.
C21.2 uses current distances and actual degree caps, not global
average degree. C21.3 retains the whole seed as an induced core.
C21.4 keeps strict comparisons, handles k=1 and fixes d0 before g.
C21.5 proves rather than assumes that the size term is redundant at
k=39. The proof does not discard the historical K1/source audit.

The assertion at d=4 does not follow: (8) stays above4 for every finite
constructed graph. The published degree14 spectral seed recorded in
C20's source note is not improved by the degree24 elementary seed.
The claim here is the checked derivation of the new internal bounds,
not a priority claim or a Result.

No graph selector, greedy implementation, sampler, solver or proof
assistant was executed. Arithmetic displays are proof derivations;
artifact hashing and CI do not verify those derivations.
The next useful verification slice is an exact integer recurrence
for the all-shore incidence count, separate from overlapping cycles
and from the graph-to-contract semantic map.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
best_candidate: candidate:opg37364-degree63-density-c21,
                conditional only on expanding the C20 candidate proof.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: freeze an exact finite-count interface for C20 rather
than asking a verifier to run the astronomically large selector.
