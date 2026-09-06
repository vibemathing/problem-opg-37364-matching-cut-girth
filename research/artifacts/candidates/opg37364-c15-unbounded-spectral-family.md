# C15: unbounded-girth spectral family with a 12-regular reduction

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-unbounded-spectral-c15.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: 2f583af139476c7a5d3b99e2f81c7c8246347b20.

Both admitted obligations remain open. This is a complete classical
implication from explicitly attributed LPS/prime inputs, not a verifier
receipt or an addition to the allowed axioms. It does not rely on K1,
the finite C11 witness, NP-hardness, or a claim of novelty.

## 1. All-cut spectral inequality

Let X be a finite simple r-regular graph on n>=2 vertices. Order its
adjacency eigenvalues by value, not absolute value:
r=lambda_1>=lambda_2>=...>=lambda_n.
For a nonempty proper A, put s=|A| and x=1_A-(s/n)1. The vector x is
orthogonal to 1, its squared norm is s(n-s)/n, and, for L=rI-Adj,
  x^T L x = sum_{uv in E(X)} (x_u-x_v)^2 = |delta_X(A)|.
The spectral theorem for real symmetric matrices gives
  |delta_X(A)| >= (r-lambda_2) s(n-s)/n.                 (1)
The same statement follows directly from the quadratic-form inequality
L >= mu(I-J/n), with mu=r-lambda_2, where J is the all-ones matrix.

For the smaller shore, 1<=s<=n/2, (1) is at least mu*s/2.
A matching cut has at most s crossing edges, because each vertex of
that shore is incident to at most one. Thus mu>2 excludes every
matching cut. More explicitly, every nontrivial cut then has a vertex
in its smaller shore incident to at least two crossing edges.

Bipartiteness causes no difficulty: the eigenvalue -r is not lambda_2
and must not be used as a bound on the nonconstant spectrum by absolute
value. The strict inequality mu>2 matters.

## 2. Exact attributed infinite input and parameter choices

Feghali, Lucke, Paulusma and Ries, Algorithmica 87 (2025), Section 3.1,
Lemma 5 and its proof, invoke the Lubotzky-Phillips-Sarnak construction:
for primes p<q, p=q=1 modulo 4 and Legendre symbol (p/q)=-1, there is
a finite simple bipartite (p+1)-regular graph with
  lambda_2 <= 2 sqrt(p),
  girth >= 4 log_p(q)-log_p(4).                         (2)
Here p=q=1 modulo 4 means both congruences, not equality of p and q.
The source map identifies the original LPS theorem and access limits.

Set p=13. Dirichlet's theorem applied to the coprime progression
5+52k supplies arbitrarily large primes q=5 modulo 52. These satisfy
q=1 modulo 4 and (q/13)=(5/13)=-1. The latter can be checked from
5^2=12 modulo 13 and 5^6=12 modulo 13. Quadratic reciprocity, since
both primes are 1 modulo 4, gives (13/q)=(q/13)=-1.

For any integer g>=3, choose q>13 in this progression with
  q^4 >= 4*13^g.                                      (3)
Then (2) gives girth at least g, with degree fixed at 14 before g
is chosen. Also its Laplacian gap satisfies
  mu >= 14-2 sqrt(13) > 13/2,                          (4)
because sqrt(13)<15/4, equivalently 208<225. Thus for every g there
exists a simple bipartite 14-regular X satisfying
  L_X >= (13/2)(I-J/n).                               (5)
Connectivity follows from (5): a disconnected graph would have a
nonconstant vector in the Laplacian kernel.

The source is an explicit deterministic Cayley construction. We do not
supply or claim execution of an unchecked matrix-generator recipe.
Section 5 gives a separate exact deterministic selector using only
the existence and numerical bounds of (2).

## 3. Deletion robustness

Suppose |delta_X(A)|>=c*min(|A|,|V-A|) for every nontrivial A, and
D is a spanning edge subgraph with maximum degree at most t.
At most t*s deleted edges cross a smaller shore of size s, hence
  |delta_{X-D}(A)| >= (c-t)*s.                         (6)
Deletion creates no shorter cycle. If c-t>1 then X-D has no matching
cut; if c-t>0 then it is connected.

From (5), take c=13/4. Deleting any D of maximum degree at most two
leaves
  |delta_{X-D}(A)| >= (5/4)*s > s.                    (7)
This proves the assertion for every shore at once, not just for
a list of tested cuts. Alternatively (2) gives the stronger real
coefficient 5-sqrt(13)>1 after such a deletion.

## 4. Two edge-disjoint perfect matchings

A nonempty finite k-regular bipartite graph with k>=1 has a perfect
matching. Here is a finite proof. The two parts have equal size by
counting edges. Take a matching of maximum size and suppose an
unmatched left vertex exists. Follow alternating paths starting
there: unmatched edges from left to right and matching edges back.
An unmatched reachable right vertex would give an augmenting path.
Otherwise the reachable right set T is matched bijectively to the
reachable left set S except for the starting left vertex, so
|S|=|T|+1. Every neighbour of S lies in T. Counting incidences gives
k|S|<=k|T|, a contradiction. A matching saturating the left part
also saturates the right part.

Apply this first to X and then to the 13-regular bipartite graph
obtained after deleting the first perfect matching. We obtain
edge-disjoint perfect matchings M1 and M2. Their union has degree
exactly two at every vertex. Set
  H = X-(M1 union M2).
Then H is simple, bipartite and 12-regular. By (7) it is connected
and has no matching cut, and its girth is at least that of X.

This deletion argument is not an assertion that arbitrary edge
deletion preserves the absence of matching cuts: its quantitative
expansion surplus is essential.

## 5. Deterministic, exact, finite selector

For an integer g>=3, enumerate n=2,3,... and the labeled simple graphs
on [n] in lexicographic order of their upper-triangle edge bits.
Select the first bipartite 14-regular graph of girth at least g for
which the integer symmetric matrix
  Q(X) = 2n L_X - 13(nI-J)
is positive semidefinite. Such an X exists by Sections 2 and (5).

This is an exact decidable predicate on each finite graph. For
example, test all principal minors of Q for nonnegativity using
integer determinants. This criterion for a symmetric Q is exact:
necessity follows from positive semidefiniteness of every principal
submatrix. Conversely, the coefficients of det(tI+Q), other than its
positive leading coefficient, are sums of principal minors. If all
are nonnegative, det(tI+Q)>0 for t>0. A negative eigenvalue of Q
would produce a positive root, which is impossible.

Choose the lexicographically first perfect matching M1 of this X,
then the first perfect matching M2 of X-M1, in the induced edge order.
Define H_g=X-(M1 union M2). These finite choices make the family
deterministic and computable. The existence proof ensures termination
for each g; no efficiency or actual execution is asserted. In
particular, this selector is not presented as a practical algorithm
for large graphs. Source (2) may instead be used with a fully audited
implementation of its deterministic Cayley graphs.

## 6. Root quantifiers

Fix the real parameter d0=13, independently of g. For each integer
g>=3, H_g from Section 5 is a finite simple graph with
  average_degree(H_g)=12<13=d0,
  girth(H_g)>=g,
  no matching cut.
For any nontrivial shore A, choosing its smaller side in (7) explicitly
forces a vertex with at least two crossing neighbours. Thus the
candidate has exactly the negation quantifiers
  exists d0>0, forall integer g>=3, exists qualifying H_g without MC.

The graphs are nontrivial, connected and bipartite. They contain a
cycle because their minimum degree is 12, so their orders are at
least their girths. As g tends to infinity these are not repeated
uses of one finite obstruction. They also avoid the source's
small-order/forest convention problem; none modifies the frozen
contract or removes K1 from it.

The ordinary mathematical answer already appears in the 2025 paper.
The 12-regular deletion step is a candidate deduction from its
stronger spectral input, not a claim to a new published result.
No conclusion about all 4-regular graphs is inferred.

## 7. Scope of the degree-four spectral test

The generic bound lambda_2<=2 sqrt(r-1) implies r-lambda_2>2 only
when r>4+2 sqrt(2), hence for integer r>=7. For r=4 this estimate
alone does not suffice. Failure of a sufficient inequality does not
prove existence of a matching cut.

There is also an elementary obstruction to the strict test itself:
every finite simple 4-regular graph of girth at least eight has
lambda_2>=2. Take a shortest cycle and two vertices four steps apart.
Their distance is four, since a shorter path combined with that
four-edge path would contain a cycle of length at most seven.
Their closed neighbourhoods are disjoint induced 4-stars and have
no edges between them. On each star put weight two at its centre
and weight one at each leaf. Each vector has squared norm eight,
coordinate sum six, and adjacency Rayleigh quotient two. Their
difference is orthogonal to the all-ones vector and still has
Rayleigh quotient two, proving lambda_2>=2. If the graph is
disconnected, lambda_2=4 already gives the assertion.

This rules out certifying such graphs solely by lambda_2<2. It
does not rule out no-MC graphs of degree four or a different proof.

## 8. Audit obligations, not fabricated receipts

The proof dependencies are finite spectral linear algebra; the
specific LPS existence/spectrum/girth theorem; Dirichlet and
quadratic reciprocity for the displayed progression; and the
elementary cut, deletion and matching arguments above. LPS,
Dirichlet and reciprocity are named imported theorem obligations,
not new axioms written into the contract. The reference trail
does not constitute their formal verification.

No graph generator, SAT solver, spectral computation, proof assistant
or mathematical verifier was executed. Local serialization and hashes
identify bytes only. The three GitHub checks validate transport only.
The current registry's fixture policies must not be extended by a
candidate agent. Both admitted obligations require their own valid
verification/admission chain before repository closure.

Self-review attacks: second eigenvalue is ordered by value; both
shores are nonempty; deletion loses at most two incidences per
smaller-shore vertex; perfect matchings are chosen in successive
regular graphs; girth cannot decrease under deletion; d0 is fixed
first and the density inequality is strict. PSD, source matching
and the infinite existence theorem need separate review.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: develop a finite-combinatorial probabilistic existence
argument with a deterministic selector, to remove the deep imported
LPS/number-theory dependencies from a separate root candidate.
