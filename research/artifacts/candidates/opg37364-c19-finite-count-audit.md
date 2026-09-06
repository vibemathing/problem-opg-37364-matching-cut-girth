# C19: finite-counting and representation audit of the root family

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-finite-count-audit-c19.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: 7526b1f8ad30911ca9e18e00dfad5e675b609450.

This is an audit of the complete C16+C18 family proof, not a new
finite-girth witness. No mathematical verifier or sampler was run.
The two admitted obligations remain open. This text and the companion
mutation data are proof candidates, not receipts.

## C19.1. Exact finite sample space and dependence within a permutation

For C16's input g>=3 use its integers
  K=2g, C=K^2*(160*K^2)^K,
  M=max(1000,4C,2g), N=M^2.
The finite sample space is Omega=(Sym(N))^40, of size Z=(N!)^40>0.
For a subset A of Omega, "probability" means the rational |A|/Z only.

For one uniform permutation, prescribe k distinct input-output pairs.
If an input has two outputs or an output two inputs, the count is zero.
Otherwise exactly (N-k)! permutations realize them: freely permute
the remaining N-k inputs onto the remaining N-k outputs.
Thus a compatible coloured pattern having e_i prescribed pairs of
colour i has exactly
  product_{i=1}^{40} (N-e_i)!
realizing tuples, and probability product_i 1/(N)_(e_i).
Here (a)_(j)=a(a-1)...(a-j+1), with empty product one.

For k distinct input slots required merely to land in a fixed b-set,
there are (b)_(k)*(N-k)! permutations if k<=b, and zero otherwise.
Consequently the probability is (b)_(k)/(N)_(k).
For b<=N and j<b,
  (b-j)/(N-j)<=b/N,
because N(b-j)<=b(N-j) is equivalent to bj<=Nj.
It follows that this probability is at most (b/N)^k.
This is a proved without-replacement bound, not an assumption that
slots of one permutation are independent. Products across the forty
coordinates are justified by direct multiplication of finite counts.

## C19.2. Replace the geometric tails by finite identities

Let BadCut be C16's event that some shore S with 1<=|S|<=N has at
most 2|S| crossing COLOURED EDGE INSTANCES in the auxiliary multigraph.
C16.2-C16.3 give the finite union estimate
  |BadCut|/Z <= 4*sum_{a=1}^{floor(N/2)} a*Q_a^a,
where
  Q_a=194400*min(2a/N,3/5)^35.                       (A)
The orientation factor and at most 2a possible opposite part sizes
are already accounted for by 4a. An empty part of S cannot be bad:
its crossing count is 40|S|>2|S|. No positive small-shore size is omitted.

Put L=floor(N/2) and theta=194400*(2/M)^35.
Since M>=1000, theta<=194400/500^35<1/100.
For example 500^3=125000000>19440000 suffices to check the strict
last comparison. For a<=M, Q_a<=theta.

For every integer T>=1 and real 0<=x<1, direct cancellation of the
finite sums gives
  (1-x)^2*sum_{a=1}^T a*x^a
    = x-(T+1)*x^(T+1)+T*x^(T+2) <= x.              (B)
One way to verify the identity is to subtract x times the sum from
the sum, and then do this once more; only the first and last terms
remain. The last inequality uses T*x<=T<T+1.
Thus the part of (A) with a<=M is at most
  4*theta/(1-theta)^2 < 400/9801 < 1/20.
The last comparison is 8000<9801. This uses only a finite identity.

For a>M, C16's exact constant bound Q_a<1/4 follows from
  (3/5)^5<1/10,
  (3/5)^10<1/100,
  (3/5)^35<1/10000000,
  4*194400=777600<10000000.
The first two inequalities are respectively 10*243<3125 and
100*59049<9765625; combine three powers of the second and one
of the first for exponent35. Hence
  4*sum_{a=M+1}^L a*Q_a^a
    <=4*sum_{a=M+1}^L 2^(-a)
     =4*(2^(-M)-2^(-L)) < 4/2^M < 1/1000.          (C)
Here a<=2^a follows by induction; L>=M since N=M^2 and M>=1000.
The final inequality follows already from 2^12=4096>4000.
Every sum in (B) and (C) is finite. No convergence theorem or limit
in N, g or the degree is required.

## C19.3. Overlapping cycles and an integer count of good tuples

Let BadOverlap be the event that two distinct short cycles share a
vertex. The cycles have length from two through g-1 and are identified
by their unoriented COLOURED EDGE SETS. Reversing or rotating the same
cycle does not create a second cycle. Parallel edges may form a
two-cycle; loops are absent from the bipartite model.

The union F of two such genuinely distinct cycles is connected and
has e>=v+1. It has v,e<=K. For completeness, a connected graph with
e=v has just one edge outside a spanning tree, and therefore only
one cycle, including the possible parallel-edge two-cycle.
This proves the necessary excess when the cycles are distinct.

C16.5's deliberately overcounting catalogue has at most
  K^2*2^K*(40*K^2)^K
abstract typed and edge-coloured patterns. At most N^v injective
vertex labelings are possible. For any compatible labeled pattern,
C19.1 and N>=2K imply probability at most (2/N)^e: each of the e_i
factors N-j is at least N-K>=N/2.
Multiplying by labelings gives at most 2^K/N because e>=v+1.
An incompatible pattern has probability zero and cannot spoil the bound.
Hence, by a union bound on finite sets,
  |BadOverlap|/Z <= K^2*(160*K^2)^K/N = C/N
                 <=1/(4M)<=1/4000.                 (D)

Let Good=Omega minus (BadCut union BadOverlap). From (A)-(D),
  (|BadCut|+|BadOverlap|)/Z
    < 1/20+1/1000+1/4000 = 41/800.
Equivalently, the relevant exact integer inequality is
  800*(|BadCut|+|BadOverlap|) < 41*Z.                (E)
The finite union-cardinality inequality now gives
  800*|Good| > 759*Z > 0.
Thus Good is nonempty for every input g. This is a finite-counting
existence certificate, not a count obtained by enumerating Omega.
Selecting the least member of the finite lexicographic order is
well defined. The value of Z need not be evaluated by a runtime.

This audit retains C16's slot/event catalogue as a candidate input.
A trusted verifier must check that catalogue as well as the finite
algebra above; the displayed fraction does not self-admit that input.

## C19.4. The multigraph-to-simple-graph bridge cannot be omitted

In the auxiliary object, the edge identity is the pair (colour,input).
Two different colours may connect the same old endpoints, and their
crossing contributions count separately. The graph is not asserted
to be a finite SIMPLE graph at this stage.

For a Good tuple, the short cycles are pairwise vertex-disjoint.
Choose one coloured edge from each short cycle and delete it.
Those deleted edges form a matching of EDGE INSTANCES. A vertex loses
at most one incident edge, so its final degree is 39 or 40.
All two-cycles have been hit. If two surviving parallel edges existed,
their two-cycle would not have been hit, a contradiction.
Hence forgetting colours now gives a simple graph and preserves the
number of surviving edges and every vertex's degree.

Deleting edges cannot create a new cycle. A purported final cycle
shorter than g would already have been one of the hit coloured cycles.
For every smaller shore, deletion removes at most one crossing edge
per shore vertex. Therefore the auxiliary strict bound >2|S| becomes
the final strict bound >|S|. This proves the no-MC seed conclusion
using distinct neighbours only AFTER simplicity has been proved.

Mutation fixture: two vertices L,R joined by two differently coloured
parallel edges. Colour L false and R true. There is only one distinct
opposite neighbour at each vertex, so a simple-neighbour predicate
accepts. But the two crossing edge instances share both endpoints
and do not form a matching. Thus applying C08's simple-graph CNF
directly to the auxiliary multigraph is an invalid semantic bridge.
The fixture is not an input graph to the frozen simple-graph root.

## C19.5. Source-domain robustness of the final negative quantifiers

C18's final family, with fixed k=72, consists of simple, bipartite,
2-connected cyclic graphs of order at least three. It satisfies
  average_degree<364/73<5, girth>=g, no matching cut
for every integer g>=3.

The same witnesses are therefore available whether the original
source domain is all nonempty simple graphs, only graphs of order
at least two, only connected graphs, or only 2-connected graphs.
Their girth is finite, so no convention for acyclic girth is invoked.
No value of the empty graph's average is needed.
On a connected final graph a nontrivial cut is automatically nonempty,
so allowing or forbidding an empty crossing matching also makes no
difference to these particular witnesses.

The fixed two-NONEMPTY-shore interpretation remains essential.
The published 2025 Algorithmica article explicitly requires both
colours in Section2 and identifies the negative OPG answer in
Section1.2. These are source comparisons, not new premises of C16.
Source: https://doi.org/10.1007/s00453-025-01318-8 .

Thus C01's historical small-order ambiguity is not used to generate
or justify the infinite family. This does not erase its audit record
or claim that a trusted statement-faithfulness receipt already exists.

## Verification boundary and exact handoff

Proof-input locators on the frozen base:
- research/artifacts/candidates/opg37364-c16-elementary-unbounded-family.md
- research/artifacts/candidates/opg37364-c18-elementary-density.md
- research/artifacts/candidates/opg37364-c08-boolean-faithfulness.md
The first two provide the complete elementary family chain. The third
is used only to audit the graph predicate after simplicity.

The next trusted proof obligations are: finite permutation extension
counts and the slot union bound; the coloured-pattern catalogue and
e>=v+1 lemma; finite identities (B)-(E); matching deletion and the
injective final edge representation; the C18 greedy augmentation;
and the fixed-d0=5 quantifier map with nonempty shores.
No missing statement should be replaced by an extra axiom.

The current generator has not run a mathematical toolchain and cannot
sign or extend the registry's fixture verifier policies. Requested
capabilities remain kernel_check, axiom_escape_audit and
statement_faithfulness. Their successful receipts and trusted admission
are still absent; PR checks and this audit cannot substitute for them.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
best_candidate_chain: C16 + C18, with the C19 counting/semantics audit.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: replay the six precisely separated proof blocks through an
authorized verifier and audit the original/final graph representation;
do not run the discarded finite-size extrapolation or infer a receipt
from this proof package.
