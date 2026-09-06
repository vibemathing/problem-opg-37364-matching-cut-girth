# C01: contract-faithfulness and degenerate cases

Verdict: candidate_only. Kind: proof (source-faithfulness audit, not root admission).
Candidate: candidate:opg37364-edge-audit-c01.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: f0df824cb29a0a68ea860d76a2b0668d3900fac2.
Owner: math-proof. Both the target and obligation:opg37364-root remain open.

## Frozen semantics

Use the canonical contract at the base above, unchanged. Graphs are finite and
simple. For n=|V|>0 and m=|E|, average degree is 2m/n. Forests have girth
+infinity. MC(G) means that there is A with empty != A != V such that
delta(A), the complete set of crossing edges, is a matching; that matching
may be empty. The root order of quantifiers is forall real d>0, exists integer
g>=3, forall qualifying G, exists such A.

The empty graph has undefined average degree under the supplied definition.
Do not assign 0/0 a value. Statements below use n>=1; excluding n=0 does not
exclude n=1. Any decision about the original source's omitted conventions
requires semantic review, not editing this contract.

## Atomic deductions

### C01.1 / claim:opg37364-c01-singleton
For every d>0 and every integer g>=3, K1 meets the numerical hypotheses but
does not satisfy MC. Indeed n=1, m=0, so 2m/n=0<d; its girth is +infinity.
The two subsets of its vertex set are empty and V, so there is no permissible
A. Thus K1 is a uniform obstruction candidate to the literal quantifiers.
Even fixing d=1 leaves the same witness for every g. K1 is connected, so
adding connectedness alone does not remove this obstruction.

### C01.2 / claim:opg37364-c01-disconnected
Every disconnected graph of order at least two has an empty matching cut.
Take A to be one component's vertex set. It and its complement are nonempty;
there are no crossing edges. The empty set satisfies the matching condition.
In particular this includes edgeless graphs of order at least two.

### C01.3 / claim:opg37364-c01-bridge
For a connected graph, an edge e is a bridge if and only if some nontrivial
vertex partition has precisely {e} as its crossing edge set.
If e is a bridge, deleting it leaves exactly two components: connectedness
before deletion and a path ending at an endpoint of e give this assertion.
Their vertex sets have no other crossing edge. Conversely, deleting the only
crossing edge of a nontrivial partition disconnects the graph. A singleton
edge set is a matching. Consequently every connected graph with a bridge
has a matching cut, without any density or girth hypothesis.

### C01.4 / claim:opg37364-c01-forest
A nonempty forest has a matching cut exactly when n>=2.
For n=1 use C01.1. For n>=2, a disconnected forest uses C01.2; otherwise it is
a tree with an edge, and every tree edge is a bridge (an alternate endpoint
path would form a cycle). Use C01.3.
If the forest has c components, adding the identities m_i=n_i-1 for its
trees gives m=n-c and average degree 2-2c/n. Its girth is +infinity whether
or not it has any edges. For 0<d<2 the strict degree hypothesis is exactly
(2-d)n<2c; for d=2 every nonempty forest meets it.

### C01.5 / claim:opg37364-c01-small-d
For n>=2 and average degree <2 there is a matching cut with a one-vertex
shore. Otherwise every vertex would have degree at least two and the degree
sum would be at least 2n. Choose a vertex v of degree at most one and set
A={v}. Its crossing edges are empty or a singleton. The complement is
nonempty. No girth assumption was used.
Thus for 0<d<=2 the restricted statement on n>=2 holds with g=3.
This is not a repair or a positive assertion about the unrestricted root:
K1 still satisfies its hypotheses and still has no permissible partition.

For completeness, the connected n>=2 instances with average degree <d<=2
are exactly the following:
- 0<d<=1: none. Connectedness gives m>=n-1 and 2m/n>=2-2/n>=1.
- 1<d<2: trees of orders 2<=n<2/(2-d).
- d=2: every tree of order at least two.
To prove the last two statements, m>=n-1 and m<n imply the integer m=n-1.
For a tree, rearranging 2-2/n<d for d<2 gives the displayed strict upper
bound. At equality n=2/(2-d), the hypothesis fails.
Values d<=0 are outside the root's parameter domain.

### C01.6 / claim:opg37364-c01-equality-audit
For n>=1 and average degree <=2, the only graphs lacking MC are K1 and C3.
Disconnected graphs use C01.2. In a connected graph n-1<=m<=n. If m=n-1,
use the tree case. If m=n, a spanning tree has one extra edge, hence exactly
one cycle. All edges off that cycle are bridges. With no such edges the
graph is a cycle. C3 has no matching cut: a singleton shore has two incident
crossing edges, and every nontrivial partition has a singleton shore.
For a cycle of length at least four, two consecutive vertices form a shore;
its two crossing edges have four different endpoints and form a matching.
This explains why substituting <= for < at d=2 and g=3 is not harmless.
On n>=2, girth>=4 would suffice for the <=2 variant.

## C01.7 / claim:opg37364-c01-safe-residual

For each fixed d>0 and g>=3, every qualifying graph with n>=1 is either K1,
already handled by C01.1, or has n>=2. A qualifying n>=2 graph lacking MC
must be connected, bridgeless and have minimum degree at least two.
For 0<d<=2 that residual class is empty. None of these deductions permits
deleting K1 from the literal quantified problem. A further cut-vertex
reduction, if submitted, must preserve density and extend the cut explicitly.

## Adversarial audit and limitations

1. Nonempty shores and nonempty crossing edges are different requirements.
   Requiring the latter would invalidate C01.2 and is not this contract.
2. Allowing an empty shore makes every graph pass via A=empty; that is not MC.
3. K2 has average degree 1, so it is excluded at d=1 and included only for d>1.
4. Average degree <2 does not imply forest without connectedness:
   C_l plus one isolated vertex has average 2l/(l+1)<2 and girth l for any
   l>=3. Its empty matching cut still exists.
5. Connectedness alone does not exclude K1; excluding only n=0 is insufficient.
6. C3 has average degree exactly 2, so it is not a counterexample to C01.5.
7. No finite enumeration, solver, proof assistant or mathematical verifier
   was executed. The arguments above are candidate deductions from
   finite-graph basics, finite combinatorics and real arithmetic.

Source comparison: research/artifacts/source-notes/opg37364-c01-source-faithfulness.md.
The original page does not settle all small-order/nonempty-shore conventions;
the primary literature also contains a directly relevant nontrivial family.
Flag: ambiguous_problem_contract (nonterminal). Continue only the declared
faithfulness audit and explicitly conditional reductions; do not upgrade the
root, introduce replacement axioms, or silently repair the graph domain.

## Reproduction and next verification

Read the frozen definitions; verify the degree sums, tree edge count, all
nontrivial partitions of K1 and C3, and the explicit shores above. Audit each
use of n>=2 and each strict inequality. Have a trusted semantic reviewer
resolve source/domain faithfulness; then request the declared kernel and
axiom-audit capabilities on a separately frozen encoding. No receipt is
created here. Best verified result: none.
