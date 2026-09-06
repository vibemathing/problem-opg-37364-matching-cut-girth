# C06: source-faithful extremal bound and strict girth translations

Verdict: candidate_only. Kind: proof / conditional source audit.
Candidate: candidate:opg37364-extremal-audit-c06. Owner: math-proof.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: cebd7c559a90416d64b03bbe955673947514005f.

The contract is unchanged. MC requires two nonempty shores; its crossing
matching may be empty. All positive assertions explicitly concern n>=2.
The literal K1 obstruction from C01 remains. Both admitted obligations
are open; source-domain ambiguity is nonterminal.

## External dependency T3: statement, not an added axiom

T3 is the attributed Farley-Proskurowski edge bound: a finite simple
graph without MC has m>=ceil(3(n-1)/2). Bonsma's 2005 primary conference
paper, Theorem 1, prints this bound and allows multigraphs, thus covering
simple graphs. The source map gives version, locators and limitations.
T3 is pending faithful reuse and mathematical verification. Statements
below using T3 are conditional, not extra axioms admitted to the contract.

The remaining arguments use only integer arithmetic, finite graph
counting and the explicit C01/C02/C05 candidate arguments.

## C06.1 / claim:opg37364-c06-parity-threshold

For integer n>=1 write f(n)=2*ceil(3(n-1)/2)/n. Direct integer arithmetic
gives
  f(n)=3-3/n if n is odd;
  f(n)=3-2/n if n is even.
For g>=3 let q(g) be the smallest odd integer at least g. Then
  min_{integer n>=g} f(n) = beta(g):=3-3/q(g).

Within each parity f increases with n. If g is odd, compare the first
even candidate g+1: 2/(g+1)<3/g, so f(g)<f(g+1). If g is even,
g>=4 and 2/g<=3/(g+1), so f(g+1)<=f(g). This proves the formula.

A no-MC graph of order n>=2 is connected and has minimum degree at
least two by C01. It contains a cycle: otherwise it is a nontrivial
tree, which has a bridge and hence MC. At girth at least g this gives
n>=g. Conditional on T3, its average degree is at least f(n)>=beta(g).
Consequently n>=2, girth>=g, and average degree <beta(g) suffice for MC.

The density inequality is strict. Any d<=beta(g), including equality,
is sufficient under average degree <d. It is not legitimate to replace
that hypothesis by <=d. At g=3 equality is witnessed by C3; at g=4,
beta(4)=12/5, and K(2,3) audits equality.

In particular, for every 0<d<3 the n>=2 subsidiary question has a
finite sufficient girth. A simple, not necessarily best, choice is
  g=max(3,ceil(3/(3-d))).
Indeed 3-3/g>=d and beta(g)>=3-3/g. For d<=2, C01 already gives g=3
without using T3. No limiting argument here covers d=3.

## C06.2 / claim:opg37364-c06-size-growth

A simple graph H with minimum degree at least three and girth at least
2r+1, where r>=1 is an integer, has at least N(r)=3*2^r-2 vertices.

Start from any vertex and expose breadth-first layers through distance r.
The root has at least three neighbours. Each vertex at depth i<r
has at least two neighbours besides its parent, and these must be new
distinct vertices at depth i+1. An additional edge to an earlier layer
or a collision between two proposed children would produce a cycle of
length at most 2r. Thus the layer sizes are at least 3*2^(i-1) for
1<=i<=r. Summing gives 1+3*(2^r-1)=N(r). Edges entirely within the
last layer need not be absent and do not invalidate this vertex count.

Now fix a hypothetical no-MC graph with n>=2, average degree <d, and
girth at least 4r+1. C02 selects a 2-connected no-MC piece with the same
strict d bound and girth bound; rename this piece G. Apply only the
structural part of C05.2: suppress its degree-two vertices to a simple
graph H of minimum degree at least three and girth at least 2r+1.
The simplicity proof requires original girth at least five, which
4r+1 supplies. No density formula or condition 2<d<4 is needed for
these structural assertions. Each vertex of H is a vertex of G, so
  |V(G)|>=|V(H)|>=N(r).

Conditional on T3 applied to this G,
  average_degree(G)>=3-3/|V(G)|>=3-3/N(r).
Hence, on n>=2, girth>=4r+1 and average degree <3-3/N(r) suffice for MC.

## C06.3 / claim:opg37364-c06-logarithmic-girth

For 2<d<3 choose any integer r>=1 with
  2^r >= 1/(3-d)+2/3.
Then N(r)>=3/(3-d), so C06.2 yields a sufficient girth g=4r+1.
This is a separate changed-parameter consequence, not a claim that
C05 suppression preserves the original average degree or girth.

Exact examples: d=29/10 allows r=4, N=46 and g=17 because 30<=46.
For d=299/100, r=7 gives N=382 and g=29 because 300<=382.
The elementary linear choices from C06.1 are respectively g=30 and
g=300. These examples compare sufficient bounds, not optimal girths.
C05's elementary d=5/2, g=5 result remains useful without T3.

## C06.4 / claim:opg37364-c06-order-one-source-check

The 2005 text lists ABC graphs as immune and explicitly allows order
one. Therefore its terminology does not treat an empty shore as an MC:
that interpretation would make every graph, including K1, have MC.
This supports the nonempty-shore convention in the frozen contract.
It does not establish that the separate OPG universal question intended
to omit K1. The two issues must not be conflated.

The frozen definition of average degree does not define the empty
graph's average. No value is assigned to 0/0 here. Replacing n>=1 by
n>=2 in the root, changing <d to <=d, or replacing average degree by
maximum average degree would each change the problem.

## Attacks and dependency map

C06.1 depends on T3 and the C01 cycle argument. C06.2's vertex bound is
elementary; its MC consequence additionally uses C02, the structural
part of C05.2 and T3. C06.3 depends on C06.2 and positive 3-d.
C06.4 is a bounded statement comparison, not a mathematical receipt.

K1 does not satisfy n>=g and is not used in the cycle argument.
K2 cannot be a no-MC example. The ceiling must be retained before
splitting parity. A minimum-degree assertion for a suppressed multigraph
would not justify the breadth-first count used for simple H. Source
extremal examples at every order need not have large girth. No endpoint
claim at d=3 follows from sufficient bounds diverging as d approaches 3.

No equality characterization of immune graphs is used in these proofs.
A further source audit may study that distinct theorem to narrow the
endpoint; it must remain separate from the present dependency T3.

## Reproduction and nonterminal checkpoint

Verify the two parity formulae, compare consecutive parity minima,
check that a no-MC n>=2 graph has a cycle, and trace the breadth-first
collision bound and the suppression hypotheses. Recompute the exact
integer examples without rounding. Audit T3's source, graph class,
matching-cut convention and proof separately.

Source map: research/artifacts/source-notes/opg37364-c06-extremal-source-map.md.
No graph enumerator, solver, proof assistant or repository command was
run for this candidate. Serialization and hashes are not math verification.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: audit the separate extremal equality characterization and
             its small-cycle/parity consequences, without asserting d=3.
