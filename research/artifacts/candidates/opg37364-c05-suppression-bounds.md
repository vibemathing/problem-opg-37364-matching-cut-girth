# C05: degree-two suppression with explicit parameter changes

Verdict: candidate_only. Candidate: candidate:opg37364-suppression-c05.
Kind: proof. Owner: math-proof.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: 3623ee2060b87e1a45320fa184fe438c79d1c7c5.

All graphs are finite and simple. MC retains nonempty shores and permits
empty crossing matchings. The n>=2 statements here are subsidiary; they
do not modify the root or erase K1. No external seed theorem is used.
Both admitted obligations remain open.

## C05.1 / claim:opg37364-c05-triangle-free-density

A triangle-free graph G of order at least two without MC has average
degree at least 12/5.

By C01 it is connected and has minimum degree at least two. By C02 its
degree-two vertices form an edgeless set. Let S be the vertices of degree
at least three and T those of degree two; write s=|S| and t=|T|.
All edges from T end in S, so the degree sum on S is at least 2t and
also at least 3s. Hence
  2m>=3s+2t,   2m>=4t.
Taking four fifths of the first bound and one fifth of the second gives
  2m>=12(s+t)/5.
S cannot be empty, since then every vertex has degree two while T has
no edges. The inequality proves the claim. Thus n>=2, girth>=4 and
average degree <12/5 suffice for MC. Equality is not included:
K(2,3) has average degree 12/5 and no MC, as audited in C02.

## C05.2 / claim:opg37364-c05-suppression

Suppose now g>=5, 2<d<4, and a graph of order at least two has average
degree <d, girth>=g, and no MC. By C02 choose a 2-connected such G,
preserving the same d,g. Its degree-two vertices T form an edgeless
set and S=V(G) minus T is nonempty with all degrees at least three.

Suppress every vertex w in T: replace its two incident edges uw,wv
by one marked edge uv. Let H be the resulting graph on S. Let H0=G[S]
be the unmarked-edge subgraph. Write s=|S|, t=|T|, a=|E(H0)| and
M=|E(H)|=a+t.

H is simple. Its marked edges have distinct endpoints. A marked edge
parallel to an unmarked edge would yield a triangle in G. Two marked
edges with the same endpoints would yield a 4-cycle. These possibilities
are excluded by g>=5. Each old degree is preserved, so minimum degree
of H is at least three; in particular s>=4.

H is 2-connected: paths between old vertices in G project to paths in H.
After deleting an old x, a path in connected G-x between two other old
vertices cannot use a degree-one remnant of a subdivided edge internally.
It therefore projects to a path in H-x. This verifies connectedness
after every vertex deletion.

Every cycle of H lifts to a cycle in G by replacing each marked edge
with its distinct length-two path. A cycle of length l lifts to length
at most 2l. Thus girth(H)>=ceil(g/2).

MC(H) would extend to MC(G). Keep the old colours. For a marked edge
whose endpoints have the same colour, give w that colour. For a marked
crossing edge, give w either endpoint's colour, so exactly one of its
two edges crosses. Distinct crossing edges of H have disjoint endpoints;
the lifted crossing edges therefore also form a matching. Both old
colours remain present. Consequently H has no MC.

This is a one-way implication under suppression, not an unsupported
equivalence for arbitrary subdivisions.

## C05.3 / claim:opg37364-c05-core-components

Every component C of H0 has at least g-3 vertices.

Suppose q=|C|<=g-4. No marked edge can have both endpoints in C:
a path in H0 between those endpoints has length at most q-1, so its
union with the length-two path through T would form a cycle in G of
length at most q+1<g.

Moreover C is not all of S. Otherwise there are no marked edges at
all, so G=H0 has minimum degree at least three on q<g vertices. A
finite graph of minimum degree at least two contains a cycle, here
of length at most q, which contradicts its girth.

Let A consist of C and every vertex of T with a neighbour in C.
A is nonempty, and a vertex of S outside C shows it is proper.
Each vertex of T in A has exactly one neighbour outside C. No old
vertex z outside C can be the other neighbour of two such vertices:
their neighbours u,v in C must be distinct, since H is simple, and
a u-v path in H0 of length at most q-1 together with the two
length-two paths through z gives a cycle of length at most q+3<g.

There are no unmarked edges from C to S outside C. It follows that
the crossing edges of A are exactly the edges from its added T
vertices to distinct old vertices outside C. They form a matching,
contradicting that G has no MC. This proves the component bound.

Put h=g-3>=2. If H0 has c components, c<=s/h, so
  a>=s-c>=s(1-1/h).

## C05.4 / claim:opg37364-c05-parameter-map

Since |V(G)|=s+t, |E(G)|=M+t and t=M-a, its strict density bound gives
  2(M+t)<d(s+t),
  (4-d)M<ds-(d-2)a
         <=[2+(d-2)/h]s.
Using d<4, d>2 and C05.3, we obtain the explicit map
  average_degree(H)<rho(d,g)
    :=[4+2(d-2)/(g-3)]/(4-d).

Thus a no-MC instance with parameters (d,g), n>=2, 2<d<4, g>=5
yields a simple 2-connected no-MC instance of minimum degree at least
three, average degree <rho(d,g), and girth>=ceil(g/2).
This is a safe changed-parameter reduction. It does not claim that
the original average bound or original girth survives unchanged.

## C05.5 / claim:opg37364-c05-positive-range

The minimum degree of H forces its average degree to be at least
three. Hence such G cannot exist whenever rho(d,g)<=3. Rearranging,
this sufficient condition is
  d<=theta(g):=(8(g-3)+4)/(3(g-3)+2)=(8g-20)/(3g-7).
The original density hypothesis remains strict.

Therefore every finite simple graph of order at least two, girth>=g>=5,
and average degree <theta(g) has MC. These are elementary candidate
deductions; no optimal density threshold or novelty is claimed.

At g=5, theta(5)=5/2. For d=5/2 the least integer girth requirement
for this n>=2 universal assertion is exactly five: the sufficient
argument above handles g=5, while C3 (average 2) and K(2,3) (average
12/5, girth 4) show that g=3 and g=4 do not suffice.

More generally, for 2<d<8/3, take
  h=max(2,ceil(2(d-2)/(8-3d))),  g=h+3.
Then the sufficient condition holds. The cases 0<d<=2 are already
covered by C01 with g=3. No endpoint claim at d=8/3 follows by taking
a limit in this formula.

## Attacks and source comparison boundary

Girth five is needed to keep the suppressed graph simple: K(2,3)
would suppress to two vertices with three parallel edges at girth
four. The degree-three lower bound is then a multigraph statement
and cannot be used as though the suppressed graph were simple.
The direct-edge count a, not the total count M, is bounded using
components of H0. The signs d-2>0 and 4-d>0 are essential.
Neither deletion nor suppression is claimed to preserve both
parameters unchanged. C04's conditional dense-core example is not
a counterexample to this changed-parameter theorem.

The OPG source and the Bonsma-Farley-Proskurowski extremal paper
report a stronger general edge-count theorem:
https://www.openproblemgarden.org/op/matching_cut_and_girth
and https://doi.org/10.1002/jgt.20576 .
Its reuse is kept
separate from this elementary proof; do not present the range 8/3
as the best known range. Primary-source verification of that theorem
and its strict endpoint translation is the next source audit.

## Reproduction and nonterminal checkpoint

Recheck the two degree-sum inequalities, the absence of loops and
parallel edges after suppression, the lifted colouring, the short
cycles in C05.3, and the signs in C05.4. Verify the strict comparison
at d=5/2 and the two smaller-girth witnesses without floating point.

No enumerator, solver, proof assistant or repository command was run.
The proof depends only on finite-graph basics, finite combinatorics,
real arithmetic, and the explicit C01/C02 arguments. Hashes and CI
are not mathematical verification. C01's ambiguous_problem_contract
flag remains; all positive statements here explicitly require n>=2.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: compare the primary extremal edge-count theorem with
             these bounds, preserving strict inequalities and the
             separate source-faithfulness review requirement.
