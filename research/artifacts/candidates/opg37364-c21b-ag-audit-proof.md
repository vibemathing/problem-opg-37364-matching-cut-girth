# C21B audit: a conventional proof of the fixed-five theorem

Verdict: candidate_only.
Candidate: candidate:opg37364-c21b-ag-audit-20260907.
Primary owner: math-proof.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Frozen read revision: 1735793e9f60d9d003e8948b350cfc09efd8a7ea.
ProblemContract SHA-256: cb72346bada4d4c41ce287a6d04f4b756717cc0a12cdb85ace863b379873d0eb.

## Conclusion and status boundary

RESULT_CANDIDATE_READY / full-refutation-proof-drafted.

The proof below expands all existence inputs; it does not assume the
conclusions of C16, C20 or C21B as additional axioms. The A-G audit found
no fatal mathematical gap in the frozen theorem. This is a checked
natural-language proof draft, not a trusted mathematical-verifier result.
The computational controls are finite, generator-owned checks only.
The two admitted repository obligations remain open. Their closure still
requires scoped kernel, axiom/escape and statement-faithfulness validation
and trusted admission. No truth record is changed by this document.

## Frozen theorem and notation

For every integer g >= 3 there exists a finite, undirected, simple,
2-connected bipartite graph G such that

    girth(G) >= g,
    2|E(G)| + 2 <= 5|V(G)|,
    maximum degree(G) <= 62,
    G has no matching cut.

Here 2-connected means order at least three, connected, and connected
after deleting any one vertex. A matching cut is the complete crossing
edge set of a partition into TWO NONEMPTY vertex sets, with at most one
crossing edge incident to each vertex. An empty crossing set is allowed.
Average degree is 2|E|/|V| for positive order; forests have infinite girth.
No empty-graph average is used. The final graphs contain cycles.

A temporary coloured multigraph is not a root witness. Its edges are
instances, parallel pairs are cycles of length two, and degrees and
boundaries count instances. Colours are discarded only after simplicity
is proved. For a vertex set S, delta(S) denotes its complete boundary.
For integers z >= 0 write (z)_j = z(z-1)...(z-j+1), with (z)_0 = 1.
All probabilities below are ratios of cardinalities of finite sets.

## A. Uniform finite counting of bad shores

Fix g >= 3 and temporarily let N = M^2, where M is an integer to be
chosen. Take two disjoint labelled parts X,Y of size N. A point of the
finite sample space Omega = Sym(N)^24 is an ordered tuple of permutations
(pi_1,...,pi_24). Its size is Z = (N!)^24 > 0. The coloured edge instance
(i,u) joins X_u to Y_{pi_i(u)}. Call this 24-regular multigraph Y0.

We first justify the counting inequalities used below. For 1 <= j <= n,

    binom(n,j) <= (3n/j)^j.                              (A1)

Indeed i! >= 2^(i-1) for i >= 1. Hence the finite sum of 1/i! from i=0
to j is less than 3. Expanding (1+1/j)^j and using binom(j,i) <= j^i/i!
gives (1+1/j)^j < 3. Induction, starting at j=1, gives j! >= (j/3)^j:
the induction step is exactly 3 >= (1+1/j)^j. Finally
binom(n,j) <= n^j/j!, proving (A1).

For one permutation, k compatible distinct prescribed input-output pairs
have (N-k)! extensions. Conflicting input or output prescriptions have
zero extensions. Requiring k distinct inputs merely to land in a fixed
b-set has (b)_k (N-k)! extensions if k <= b, and zero otherwise. Its
probability is therefore (b)_k/(N)_k <= (b/N)^k; each factor satisfies
(b-j)/(N-j) <= b/N because b <= N. Different permutation coordinates
multiply by a Cartesian-product count. SLOTS WITHIN ONE PERMUTATION ARE
NOT ASSUMED INDEPENDENT.

For a shore S let a=|S intersect X|, b=|S intersect Y|, s=a+b, and let I
be its internal edge-instance count. Its boundary is

    |delta_Y0(S)| = 24s - 2I.

Call S bad when 1 <= s <= N and this boundary is at most 2s. If a=0 or
b=0 it is not bad. Exchanging X,Y inverts each permutation and preserves
the uniform sample space; count both orientations and assume 1 <= a <= b.
For a bad shore,

    I >= 11(a+b),  I <= 24a,
    b <= 13a/11 < 2a,  b <= 13N/24,  I >= 22a.           (A2)

The N-bound follows from a >= 11b/13 and a+b <= N. If I >= 22a, some
22a of the 24a slots starting in the a-set all land in the b-set. The
without-replacement count and a union bound over these choices give

    P(S bad) <= binom(24a,2a) (b/N)^(22a).

For fixed sizes a,b, multiply by binom(N,a)binom(N,b). By (A1)-(A2),
these three binomial factors are at most (6N/b)^a, (3N/b)^(2a), and
36^(2a), respectively. The contribution is consequently at most

    [69984 (b/N)^19]^a.                                 (A3)

There are at most 2a relevant b for each a and at most two orientations.
Also a <= floor(N/2). Thus the expected NUMBER OF BAD SHORES, and hence
the probability of at least one, is at most

    4 sum_{a=1}^{floor(N/2)} a Q_a^a,
    Q_a = 69984 min(2a/N,13/24)^19.                      (A4)

Double-counting the diagonal orientation is harmless in this upper bound;
it is not used as an equality. A shore and its complement at size N are
also allowed as separate incidences.

The uniform large-shore bracket has the exact bound

    69984 (13/24)^19 < 2/3.                             (A5)

To check the constant, 25*13^3 = 54925 < 55296 = 4*24^3. Raising this
comparison to the sixth power and multiplying by 69984*13/24 gives

    69984 (13/24)^19
       < 3726508032/5859375000
       < 3906250000/5859375000 = 2/3.

Suppose M >= 1000. For a <= M, Q_a <= theta := 69984 (2/M)^19 < 1/100;
it suffices that 500^3 = 125000000 > 100*69984. For any T >= 1 and
0 <= x < 1, twice subtracting x times the finite sum proves

    (1-x)^2 sum_{a=1}^T a x^a
       = x-(T+1)x^(T+1)+T x^(T+2) <= x.

Hence the a <= M contribution to (A4) is less than 400/9801 < 1/20.
For every integer a >= 12, a <= (5/4)^a: the base case is
12*4^12 = 201326592 < 244140625 = 5^12, and a+1 <= 5a/4 for a >= 4
proves the induction step. By (A5), a Q_a^a <= (5/6)^a for a > M.
The finite geometric tail in (A4) is therefore less than
24 (5/6)^M < 1/1000. The last comparison follows already at M=64 from
(5/6)^4 < 1/2 and 24000 < 65536. We have proved

    P(BadCut) <= expected bad-shore count < 1/20+1/1000. (A6)

No infinite series, independence of edges in a permutation, or asymptotic
random-graph theorem has been used.

### Exact C22 interface and its invariant

For arbitrary 0 <= a,b <= N define

    c_j = binom(a,j) binom(N-a,b-j) b! (N-b)!

for max(0,a+b-N) <= j <= min(a,b), and zero elsewhere. The b-set
pi^{-1}(B) chooses j elements from A and b-j from its complement;
there are b! (N-b)! bijections once this preimage is chosen. Thus c_j
counts permutations with j internal slots and sum c_j = N!.
Inversion of a permutation proves symmetry in a,b.

Set A_0(0)=1 and all other A_0(t)=0, and set

    A_{r+1}(t) = sum_j c_j A_r(t-j),

with negative indices zero. Induction on r, by appending one permutation,
proves that A_r(t) counts tuples with exactly t internal instances. Its
support is within 0 <= t <= r min(a,b), and its sum is (N!)^r. For q=24,
a fixed bad shore has count B_{N,a,b}=sum_{t >= 11(a+b)} A_24(t).
The number of PAIRS (tuple,bad shore) is exactly

    alpha_N = sum_{1<=a<=b, a+b<=N}
        w(a,b) binom(N,a)binom(N,b) B_{N,a,b},

where w=1 on the diagonal and w=2 otherwise. Projection onto the tuple
coordinate only proves |BadCut| <= alpha_N, not equality. The pointwise
bound above also proves alpha_N/Z < 1/20+1/1000 at the specified sizes.

## B. All overlapping short-cycle patterns are covered

Put K=2g and C=K^2 (96 K^2)^K. A short cycle has length between 2 and g-1
and is identified by its unoriented coloured EDGE SET. If two distinct
short cycles share a vertex, their union F is connected, has v,e <= K,
and satisfies e >= v+1. To justify the last assertion, a connected
loopless multigraph has a spanning tree with v-1 edges. With only one
extra edge its only cycle is that edge plus the unique tree path between
its endpoints, including a possible parallel-edge two-cycle. Two distinct
cycles need at least two extra edges. Shared edges and paths do not
invalidate this argument.

Such a union is covered by a finite catalogue: choose v,e in [K], assign
one of two part types to each abstract vertex, and list e coloured
endpoint pairs. At most

    K^2 2^K (24 K^2)^K

patterns suffice. This is a deliberately overcounting catalogue. Retain
only distinct coloured edges and e >= v+1. Patterns that prescribe two
outputs at one same-colour input, or two inputs at one output, contribute
zero; all other patterns are counted by permutation extensions above.

There are at most N^v injective labellings into the prescribed parts.
If colour i supplies e_i distinct constraints, the occurrence probability
at a fixed labelling is product_i 1/(N)_{e_i}. For N >= 2K it is at most
(2/N)^e. After multiplying by labellings, this is at most 2^K/N because
e >= v+1 and e <= K. The finite union bound therefore gives

    P(BadOverlap) <= C/N.                               (B1)

This explicitly includes parallel pairs, triples of parallel edges,
cycles sharing one vertex, and cycles sharing an edge or a longer path.
Reversing a cycle is not a second cycle.

Take any M >= max(1000,4C,K) and N=M^2. Then N >= 2K and
C/N <= 1/(4M) <= 1/4000. From (A6) and (B1), the number of tuples in
neither bad event satisfies the strict INTEGER inequality

    800 |Good| > 759 Z > 0.                             (B2)

In particular Good is nonempty. The two bad events need not be independent.
Equivalently, the C22 sufficient condition
N alpha_N + C Z < N Z follows from the same bounds. We do not evaluate
that recurrence at the enormous existence size.

## C. Simplification, strict spare edge, and two-connectivity

Select a Good tuple. Its short cycles are pairwise vertex-disjoint.
Delete one edge instance of each short cycle, forming a matching D0:
each vertex lies on at most one such cycle and loses at most one edge.
Deletion creates no cycle, and every original short cycle is hit. Any
surviving parallel pair would be an unhit original two-cycle. Hence
forgetting colours now gives a SIMPLE bipartite H, with girth >= g and
every degree 23 or 24.

For 1 <= s=|S| <= N, the even integer |delta_Y0(S)|=24s-2I is greater
than 2s and therefore at least 2s+2. At most s deleted matching edges
cross S. Thus |delta_H(S)| >= s+2. H has an edge because its minimum
degree is at least 23. Remove one additional edge, obtaining H'. Then

    |delta_H'(S)| >= s+1 > s,                           (C1)
    22 <= minimum degree(H') <= maximum degree(H') <= 24,
    2m <= 24n-2, where n=|V(H')|=2N, m=|E(H')|.        (C2)

The displayed middle inequality means all degrees lie between 22 and 24.
The graph is still simple and bipartite and has girth at least g.
For any nontrivial partition, its smaller shore has size at most N;
(C1) excludes a crossing matching by counting incidences at that shore.
It also implies connectedness: a smallest component of a disconnected
graph would have boundary zero and positive size at most N.

Recheck two-connectivity rather than assuming it survives deletion.
Suppose x is a cut vertex of H', and let W be a smallest component of
H'-x. Then 1 <= |W| < n/2 and all edges leaving W go to x. Thus
|W| < |delta_H'(W)| <= 24. Put x in X. Every vertex of H'[W] has at
least 21 neighbours in W, so W meets both parts. A vertex in X intersect W
loses no neighbour to x and has at least 22 neighbours in Y intersect W.
A vertex in Y intersect W has at least 21 neighbours in X intersect W.
Consequently |W| >= 22+21=43, a contradiction. The degree bounds imply
order at least three. This proves 2-connectivity. The identical argument
with 23 and 22 also checks the original H if needed.

The minimum degree at least two ensures a cycle: a longest simple path
has at its last vertex a second neighbour on the path, closing a cycle.
There is no dependence on the forest convention. All estimates above
hold for EVERY M satisfying the displayed lower bounds, not just the
smallest one; hence increasing the square part size at fixed g is valid.

## D. Exact artificial regularization, not greedy saturation

We prove the switching lemma at the parameters used in this theorem.
Let a simple bipartite graph H' on equal parts of size N have maximum
degree at most r, girth at least g, and let k >= 1, D=r+k >= 2. Put

    B = 1+D sum_{j=0}^{g-3} (D-1)^j.

Assume kN is even and N > 5B. Then there is an edge set F, entirely within
the two old parts, with degree exactly k at EVERY old vertex, such that
J=H'+F is simple and has girth at least g. No edge of H' is altered.

Choose F of MAXIMUM CARDINALITY among the feasible edge sets of degree
at most k. The universe has N(N-1) possible artificial pairs and is
finite; the empty set is feasible. Thus a maximum exists. Every J has
maximum degree at most D. Counting walks without immediate reversal
through length g-2 bounds each radius-(g-2) ball by B, including its
centre. Distances in this argument always refer to the CURRENT J.

In either part P, at most B vertices are unsaturated. Otherwise a pair
of unsaturated vertices at distance at least g-1 (possibly infinity)
could be joined, preserving caps and girth, contradicting maximality.
If any deficit remains in P, its sum is kN-2|F[P]|, a positive even
integer, hence at least two. Choose vertices u,v carrying these two
units, allowing u=v when a vertex has deficit at least two.

At least N-B vertices of P are saturated, so

    2|F[P]| >= k(N-B) > 4kB.

At most 2kB artificial edges of F[P] touch the union of the radius-(g-2)
balls about u,v. There is therefore an edge xy of F[P] with both endpoints
outside both balls. Remove xy and add ux,vy; when u=v add ux,uy. These
are distinct absent edges and x,y differ from the deficit centres.
Degrees at x,y are unchanged and the selected deficits are filled;
|F| increases by one.

Here is the complete cycle audit. In J0=J-xy, each path from either
centre to either x or y has length at least g-1. Every x-y path in J0
also has length at least g-1, since the former edge xy would otherwise
close a cycle shorter than g in J. A cycle using just one new edge has
length at least g. If u != v, a cycle using both new edges leaves exactly
one of the following TWO pairings when they are removed:

* a u-v path and an x-y path: length at least 1+(g-1)+2 = g+2;
* a u-y path and a v-x path: length at least 2(g-1)+2 = 2g.

The pairing of each new edge with a separate path between its own
endpoints would give two cycles, not the single cycle being considered.
If u=v, both new edges lie on the cycle through u, leaving an x-y path;
its length is at least g-1 and the cycle length is at least g+1.
Missing paths create no exception. Cycles using neither new edge were
already in J0. Thus the switch is feasible and contradicts maximal
cardinality. Both parts must be fully saturated, proving the lemma.

This is a finite extremal proof. It neither equates inclusion-maximality
with maximum size nor asserts that an unmodified greedy algorithm finds
F. Any implementation allowing these augmentations has the strictly
increasing quantity |F| bounded by kN; the proof itself only needs a
maximum chosen from a finite set.

## E. Subdivide only artificial edges

Apply D with r=24, k=38 once a sufficient N is chosen below. Then

    t=|F|=kn/2=19n.

Replace each artificial edge uv by the path u-w_uv-v, using one distinct
new vertex per edge, and retain every edge of H'. Denote the final graph
by G. Its new vertex is placed in the opposite bipartition part from
u,v, which belonged to the same old part. Thus G is bipartite. It is
simple because all new vertices are distinct, endpoints differ, and
H' is simple.

Suppressing the degree-two new vertices of any simple cycle of G yields
a cycle of J of no greater length. Old vertices remain distinct; a
projected loop would require an artificial loop, and a projected two-cycle
would require parallel edges in J. Both are excluded. Hence girth(G)>=g.
Deleting an old vertex leaves connected H'-x, and every new vertex still
has a surviving old endpoint. Deleting a new vertex leaves the connected
core and all other new vertices attached. Order is at least three, so G
is 2-connected.

Suppose G had a matching-cut colouring. If both colours appear on H',
its restriction is a nontrivial matching-cut colouring of H', contrary
to C. If all old vertices have one colour, nonempty shores force a new
vertex of the other colour; its TWO DISTINCT old neighbours give it two
crossing edges. This is also impossible. These cases exhaust the
possibilities. Arbitrary subdivision of core edges is not being used.
New degrees are two and old degrees are at most 24+38=62. There is at
least one new vertex since t=19n>0.

## F. Fixed-five arithmetic, sufficient parameters, and finite order

Fix d0=5 and k=38 BEFORE the input g. Let

    K=2g, C=K^2(96K^2)^K, M=4C, N=M^2,
    D=62, B=1+62 sum_{j=0}^{g-3}61^j.

The ball bound gives B <= sum_{ell=0}^{g-2}62^ell <= 62^(g-1).
Furthermore

    M = 16g^2 (384g^2)^(2g) > 6*62^(g-1) >= 5B+1.

For this strict comparison use g>=3, 16g^2>=144>6, 384g^2>62, and
2g>=g-1. Also M>1000 and M>=K. It is even. Thus M satisfies every
A-C size requirement, N>5B, and kN is even. No larger girth input or
unstated extension to arbitrary part sizes is required.

G has n_G=n+t=20n vertices and m_G=m+2t edges. Equation (C2) proves

    2m_G = 2m+4t <= 24n-2+76n = 5n_G-2.

Since n_G>0, this is the required STRICT average bound
2m_G/n_G <= 5-2/n_G < 5. Without the spare seed edge the same worst-case
calculation would give only <=5, so that deletion cannot be dropped.
Finally its prescribed order is

    n_G = 40 M^2 = 10240 g^4 (384g^2)^(4g).

All sets are finite. A deterministic mathematical specification chooses
the lexicographically first Good permutation tuple, the least edge on
each short cycle, one least remaining seed edge, and the lexicographically
first maximum feasible artificial edge set. The finite search universes
have (N!)^24 and 2^(N(N-1)) members, respectively. Their nonemptiness was
proved before selection. This is a finite specification, not an efficient
implemented graph generator or an executed search at these sizes.

We have proved, as a conventional proof draft,

    exists fixed d0=5>0, for every integer g>=3,
    exists a finite simple G with average degree<d0 and girth>=g
    for which no two-nonempty-shore crossing matching exists.

Indeed our G is also bipartite and 2-connected and satisfies the stronger
integer inequality and degree bound in the frozen theorem. This is the
exact negation pattern of the frozen root. It says nothing about the
endpoint d=4, optimum maximum degree, or novelty.

## G. Source and statement faithfulness

The source note identifies two primary HTML sources, freshly read in this
audit. The Open Problem Garden page states the average-degree/girth
question and defines the full crossing-edge set, but does not explicitly
write that S is nonempty. The published Algorithmica paper's Section 2
explicitly requires both colours, works with finite simple undirected
graphs, and equates valid colourings with matching cuts of connected
graphs. Its introduction gives infinite girth for forests and Section 1.2
attributes a negative answer to this precise OPG question.

The working theorem explicitly fixes nonempty shores; the raw omitted
empty-shore condition is not silently repaired. Allowing an empty shore
would give every graph a vacuous cut and is a DIFFERENT statement. For
our connected cyclic witnesses, excluding order one, requiring
connectedness or two-connectivity, and requiring nonempty crossing edges
all leave the witnesses valid. Forest and empty-graph conventions are
never invoked. No source theorem, hardness assumption, spectral result
or novelty claim is a premise of A-F.

## Fixed-input map and audit matrix

Every repository input below was read at the frozen revision above:

| Input (under research/artifacts/) | Git blob | Role |
|---|---|---|
| candidates/opg37364-c16-elementary-unbounded-family.md | 1357c2b8aff9d92c0dc609dc25b914ea4651a92c | Earlier 40-coordinate mechanism; not an existence axiom |
| candidates/opg37364-c20-degree24-seed.md | ed9a46326c3a994e26d0236a5b87eda7c2004c6c | A-C expanded above |
| source-notes/opg37364-c20-source-map.md | fd32b584415c519f7bf465028c7ef610ab2c4368 | Attribution and conventions, freshly rechecked |
| web-inbox/opg37364-a01-c20.json | 0612966d64cb5362d673f20af50f1f84fd74d098 | Frozen C20 identity, not mathematical evidence |
| candidates/opg37364-c21-degree63-density.md | 1e332bb52016b1f43094aa61fa9de12094c8cd04 | Distinct earlier near-saturation proof, not substituted for D |
| candidates/opg37364-c21-seed-margin-9491f4b1.md | bbd02fbae16c186c1c7fd6bb92de01a65fdf31d8 | Uniform size and additive cut margin |
| candidates/opg37364-c21-density62-9491f4b1.md | 75fb6ca72e8d69dd4e45934bb15e5b41ef2ddec1 | Frozen audit subject |
| candidates/opg37364-c22-integer-count.md | f1628e285b4d80ef8f1362242d9930cd0a15acdb | Exact recurrence and incidence distinction |
| candidates/opg37364-c22-integer-interface.json | 95ad2064894a7e213b25a9b0a9cab1c7c3cc58ac | Declarative interface; not executed output |

The C21A/B local bytes were also SHA-256 hashed and their Git-blob hashes
matched the current remote blobs. Their SHA-256 values are respectively
4297bdb0cc3f1b484936f74c719f1701c10ccf08414d638a1a0b8b6566d0a43a and
e1f10b41a6233e4ad8325f302cf8fc23ece3b954d1a41cd3019fa19f2cdd0857.

| Block | Natural-language audit | Bounded control | Remaining trusted work |
|---|---|---|---|
| A | Closed at proof-draft level by (A1)-(A6) and recurrence induction | Exact permutation/tuple counts, mass, symmetry, finite tails | Formal finite-set counts and inequalities |
| B | Closed at proof-draft level by full union-pattern catalogue | Parallel, shared-edge/path/vertex controls and extension counts | Verify catalogue coverage and multigraph cycle semantics |
| C | Closed at proof-draft level by (C1)-(C2) and 43-versus-24 cut-vertex contradiction | Matching deletion and extra-edge control | Formal simple-graph bridge, parity and deletion |
| D | Closed at proof-draft level by maximum-cardinality switch | 8,913 local switch instances; both pairings; full-hypothesis u=v control | Formal extremal argument and cycle decomposition |
| E | Closed at proof-draft level by cycle projection and two colour cases | 1,024 subdivision controls, including 16 no-cut core cases | Faithful graph construction and colour restriction |
| F | Closed at proof-draft level by exact integer counts | Endpoint mutation and 48 parameter/order controls | Full quantified theorem over all integer g>=3 |
| G | Explicit convention map completed for frozen theorem; raw empty-shore variant distinguished | K1 and edgeless-two-vertex controls | Trusted statement-faithfulness acceptance |

## Executed checks and limitations

The final v2 checker uses CPython 3.13.5 and only its standard library.
It passed 127,643 assertions with exit code 0, no stderr, and no timeout.
The launcher enforced a 45-second wall limit, 40 CPU seconds, 512 MiB
address-space limit, and 64 KiB each for stdout/stderr. Exact code,
launcher, input, stdout and execution metadata are companion files.

Finite coverage includes coefficient counts for N<=6; recurrence mass
and support through q=24; complete tuple enumeration for the input's
small pairs (N,q); exact weighted compression of all 2^24 tuples at N=2;
988 partial coloured-pattern counts; short cycles in small permutation
multigraphs; every oriented local switch meeting the tested hypotheses
on labelled simple graphs of orders 3 through 5; and explicit larger
synthetic controls. The N=2,q=24 count is incidence=1204, bad union=602,
and BadOverlap=(2^24). It is not a high-girth existence certificate.

Eleven explicit bad modifications are detected, including slot
independence, incidence=union, omission of overlap, cycle-orientation
duplication, neighbour collapse before simplicity, maximal=maximum,
stale distances, absent parity, arbitrary core subdivision, empty shores,
and omission of the spare seed edge. The earlier 1/4 large-shore constant
is separately rejected for q=24. None is a counterexample to the stated
C21B proof, which retains the necessary conditions.

The first v1 run passed its tests but used n+1 as an infinity sentinel;
that omitted some forest switches when the cutoff exceeded the order.
The final v2 corrects this coverage defect with an exact sufficiently
large integer sentinel and checks both ordered switch orientations.
The v1 output and execution metadata are retained; a reverse patch from
v2 reconstructs its exact executed source. This is a CHECKER coverage
correction, not a failed mathematical lemma or a hidden runtime failure.

No general Good tuple, high-order witness, Lean theorem, SMT proof, or
registered mathematical-verifier receipt was produced by these finite
checks. A-G are checked here only as proof-draft argument blocks,
not as admitted repository EvidenceLinks. The proof is not justified by
127,643 tests; its universal content is the finite combinatorial argument
above. The tests are falsifiers and implementation controls.

## Reasoning discipline and continuation

Definitions and quantifier order are frozen above. Dependencies form the
acyclic chain A,B -> C -> D,E -> F with G as the separate semantic map.
The explicit finite selectors are given in F. Recurrence invariants use
an actual induction with base and step; finite examples do not replace it.
The edge-count extremum in D exists in a finite nonempty set. The switch
preserves degree caps, simplicity and girth and strictly increases |F|.
Symmetry keeps diagonal weights distinct, and no independence between
bad events or within a permutation is inserted. Scale checks retain the
same-girth uniform square-size hypotheses. No limiting, compactness or
spectral argument is applicable or needed. Computation is exact and
bounded, but no runtime feasibility at the selector's size is claimed.

best_verified_result: none.
best_verified_candidate: none in the trusted mathematical-verifier sense.
best_proof_draft: candidate:opg37364-c21b-ag-audit-20260907.
first_open_mathematical_gap_in_frozen_draft: none identified by this audit.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_obligation: trusted verification of A/B's finite-set catalogue and
its exact edge-instance/simple-graph bridge, then composition with D-F
and a separate G statement-faithfulness review. Fixture registry labels
must not be taken as authorization for a broader theorem without scoped
approval. The generator does not perform Result admission.
