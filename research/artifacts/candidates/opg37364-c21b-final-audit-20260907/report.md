# C21B final candidate audit: fixed d0=5

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-c21b-final-audit-20260907.
Read base: 87efc30c69b94224519dd7affbe4770fc65a5bff.
Problem: problem:opg-37364-matching-cut-girth.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.

## Frozen statement and proof identity

Fix d0=5. For each integer g>=3 there is a finite simple undirected,
2-connected bipartite graph G with girth>=g, maximum degree<=62,
2|E(G)|+2<=5|V(G)|, and no matching cut. A matching cut has two
nonempty shores and includes every crossing edge; the crossing matching
is allowed to be empty. This is a negative-root witness family, not a
proof of the positive root sentence.

The self-contained conventional proof being audited is
research/artifacts/candidates/opg37364-c21b-audit-1735793e/proof.md,
SHA-256 82a1adb1043c9a60b3c9d43696d68c24ca14bf7addd3189dd09b9cfcbd13cbb8,
Git blob c4914d9d9d81ff1c95fb8b7a927ecdd25ef7bcf0.
The original 28-file attachment tree was recomputed from its actual bytes
and equals the current remote subtree cc386d6831e5d9d3c7922e4ed59865b12d652897.
PR29 persisted that archive; PR28 contains a different audit, not a byte
replacement. The original shared-edge label and its separate executed
1200-path/360-nonadjacent correction are both preserved. No original
candidate, source, output, or historical execution record was changed.

## A. Without-replacement counts and all-shore incidences

A tuple consists of 24 permutations on N labels. Its sample space has
Z=(N!)^24 elements. For fixed left/right subsets of sizes a,b, the second
checker uses image sets:
c_j=binom(b,j) binom(N-b,a-j) a! (N-a)!.
The archived C22 uses preimages:
c_j=binom(a,j) binom(N-a,b-j) b! (N-b)!.
Expanding factorials on their common valid support gives the same integer.
Direct permutation enumeration, not the recurrence itself, is the second
finite oracle. Convolution counts ordered tuple extensions by induction:
the empty tuple has total zero, and adjoining one coordinate with j
internal edges counts each extension exactly once. Its total is (N!)^q.

For k prescribed distinct slots in one coordinate the hit probability is
(b)_k/(N)_k, or zero when k>b. Each factor is at most b/N. Products across
coordinates follow from the Cartesian sample space; no slot independence
within one coordinate is used. For a<=b, a+b<=N, a bad shore satisfies
I>=11(a+b), b<=13a/11<2a, b<=13N/24 and I>=22a. The contribution from all
shores of fixed sizes is bounded by [69984(b/N)^19]^a. At most 2a choices
of b and two orientations give 4 sum a Q_a^a, with
Q_a=69984 min(2a/N,13/24)^19.

The direction is |BadCut|<=alpha_N, where alpha_N counts (tuple,shore)
pairs. It is not alpha_N<=|BadCut|, nor equality. Diagonal orientations
have exact weight one in C22; the factor two in C20 is a safe overcount.
For N=M^2, M>=1000, theta=69984(2/M)^19<1/100. The finite identity
(1-x)^2 sum_(a=1)^T a x^a=x-(T+1)x^(T+1)+T x^(T+2)
gives the small-shore bound <400/9801<1/20. The exact comparison
69984(13/24)^19<2/3 and a<=(5/4)^a for a>=12 give the finite large-shore
bound <24(5/6)^M<1/1000. These are uniform proofs, not extrapolated tests.

## B. Overlapping cycles and a nonempty good set

A cycle is an unoriented edge-instance set, connected and 2-regular.
Parallel instances yield length-two cycles. The union of two distinct
cycles sharing a vertex is connected, has e>=v+1, and v,e<=K=2g. A
connected multigraph with at most one edge beyond a spanning tree cannot
contain two different cycles. Shared paths and edges do not change this.

There are at most K^2 2^K (24K^2)^K typed, coloured list patterns. Restrict
to distinct coloured edges; conflicting prescriptions of a permutation
have count zero. A compatible pattern has at most N^v injective labelings
and probability product_i 1/(N)_(e_i)<=(2/N)^e when N>=2K. Its contribution
is at most 2^K/N. Thus BadOverlap has probability at most
C/N, C=K^2(96K^2)^K. For M>=max(1000,4C,K), C/N<=1/4000.
The two bad events need not be independent. Their union has probability
strictly below 41/800, so 800|Good|>759Z>0. Every size-dependent inequality
holds for any larger such M at the same g.

## C. Matching deletion, spare edge, and renewed two-connectivity

Good makes all short cycles vertex-disjoint. One edge from each is a
matching deletion, losing at most s crossing instances at a shore of
size s. No new cycle is created; every original short cycle and parallel
pair is hit. Only then are colours forgotten and the graph called simple.
The auxiliary boundary 24s-2I is even and >2s, hence >=2s+2. The simple
seed H has boundary >=s+2. Deleting one further existing edge gives H'
with boundary >=s+1>s, degree between 22 and24, and 2m<=24n-2.

For any cut vertex x of H', take a smallest component T of H'-x. Then
|T|<|V|/2 and its boundary is at most24. Put x in the left part. Both
parts of T occur since internal minimum degree is at least21; a left
vertex has at least22 right neighbours in T and a right vertex at least21
left neighbours there. Thus |T|>=43, contradicting its boundary>|T|.
This proves two-connectivity anew after the spare deletion, not automatic
preservation by deletion. Positive minimum degree also gives a cycle.

## D. Maximum-cardinality exact artificial regularization

Put D=24+k and B=1+D sum_(j=0)^(g-3)(D-1)^j. Choose even N=M^2>5B.
All artificial edges remain within original parts. A maximum-cardinality
feasible F exists in a finite universe, with degree at most k and J=H'+F
simple of girth>=g. Each current-J radius-(g-2) ball has at most B points.
At most B vertices per part are unsaturated, since a far unsaturated pair
would admit an extra edge. A positive deficit kN-2|F[P]| is even. Take two
deficit units at u,v, allowing u=v. At least k(N-B)/2>2kB artificial edges
lie in P; at most2kB touch the two balls. Choose an artificial xy outside.

Remove xy and add ux,vy (ux,uy for u=v). Degree caps hold, edge count
increases by one, and simplicity follows from the current distances.
In J-xy, every centre-to-endpoint path and every x-y path has length>=g-1.
A new cycle using one new edge therefore has length>=g. A cycle using
both new edges has either u-v and x-y paths (length>=g+2), or u-y and
v-x paths (length>=2g). With u=v its length is >=g+1. These cases exhaust
simple cycles. Thus the switch contradicts maximum cardinality. All
vertices have artificial degree exactly k. Inclusion-maximality alone,
stale H distances, or omitting the coincident-centre case would not prove it.

## E. Subdivision semantics

Replace only artificial uv by u-w-v with a distinct new vertex. Its two
old endpoints are different and in the same old part; putting w opposite
them proves bipartiteness. Old edges are unchanged, so the graph is simple.
Suppressing new vertices of a simple cycle gives a cycle of simple J;
old vertices do not repeat, and a projected two-cycle would require
parallel J edges. Its length cannot increase, so girth remains >=g.
Deleting an old x leaves H'-x connected and every new vertex attached to
its other old endpoint. Deleting a new vertex leaves H' connected. Hence
the final graph is two-connected. An MC colouring using both colours on
H' would restrict to an MC there. If H' is monochromatic, a new vertex of
the opposite colour has two crossing neighbours. If none does, one shore
is empty. This exhausts the no-MC proof.

## F. Integer endpoint, prescribed order, and quantifiers

For exact k-regular F, t=kn/2. The final counts are n_G=n+t and m_G=m+2t.
Fix k=38 and d0=5 BEFORE choosing g. Then t=19n, n_G=20n and
2m_G=2m+4t<=24n-2+76n=5n_G-2. Thus the required average is strictly <5,
not merely <=5, and the maximum degree is <=24+38=62. New vertices have
degree2. Without the spare seed edge the same calculation permits =5.

For g>=3, B<=62^(g-1). The even integer M=4C=16g^2(384g^2)^(2g)
exceeds 1000,K,5B+1, so its square meets parity and size conditions.
The final order is 40M^2=10240g^4(384g^2)^(4g). All selectors are finite
(maximum or lexicographic choices after existence), not claimed efficient
or actually executed. A different G may depend on each g; d0 stays fixed.
No K1, empty graph, acyclic infinite-girth convention or finite-girth
extrapolation supplies these witnesses.

## G. Source mapping and admission boundary

See the separately frozen source comparison. The explicit two-nonempty-
shore theorem matches the checked publisher convention; the raw OPG
omission is not silently repaired. The witnesses are cyclic and
2-connected, so connectedness, small-order and acyclic conventions cannot
create this family. Existing publication is attribution, not a premise.

No fatal original lemma was identified. A-F and the explicit G mapping
are complete at conventional candidate-audit level, not trusted acceptance.
The required root and edge-case obligations remain open in repository truth.
The existing Lean CLI and closure functions are real, but current candidate
registration is empty; registry toolchain allowlists are absent; a full
Lean negative-root source is not supplied; the CLI accepts proof/formalization
kinds and emits statement_identity, while this negative-root family needs
correct counterexample classification and separate statement_faithfulness.
No execution of an unrelated fixture can fix these prerequisites. See the
admission request: it asks the trusted coordinator for the exact next steps,
without changing policy or pretending that natural-language negation is a
formal proof of the positive root statement.

## Executed checks and limitations

The second checker uses image enumeration and connected 2-regular subset
cycles, not imports of the previous checker. One actual run passed75725
assertions:90 coefficient cases,275 enumerated small tuples,988 compatible/
incompatible pattern controls,241 cycle tuples,4539 overlapping-cycle pairs,
4311 shared-edge pairs and1200 adjacent-shared-edge-path pairs;7248 local
switches (5592 coincident),2 full-size saturation controls,64 artificial
subdivision graphs and46528 nonconstant colourings. The separate pairing
run checks20 nonvacuous cases at g=4..8 covering both pairings, coincident
centres, and cycles with only one new edge.

All16 mutations M01-M16 are detected; the exact witnesses and outcomes are
in output.json and their definitions in checker.py. They drop hypotheses
or change predicates and are NOT counterexamples to the original theorem.
N=2,q=24 gives fixed301, incidence1204, union602; this is exact aggregation
of25 types and not an enumerated high-girth witness. K6,6 is used only as
an even-degree synthetic deletion control, not as a24-degree/generic-g seed.

Both successful runs are local user-authorized generator checks, CPython
3.13.5 standard library, CPU35s/wall40s/256MiB/128KiB combined output limits.
The initial runner startup hit OSError errno12 BEFORE the checker started;
its sanitized record is preserved. The same bytes succeeded with python -S
and no raised budget. No raw private traceback is published. See the real
execution records for code/input/output hashes and observations. No Lean,
SMT, trusted gate, general good tuple or enormous selector was executed.
Finite passing tests are supplemental; the general theorem rests on the
written finite arguments above and the fixed complete proof, not on counts
of assertions, CI, PR, model review or merge.

best_verified_candidate: none.
best_verified_result: none.
open_obligations: obligation:opg37364-contract-edge-cases; obligation:opg37364-root.
next_action: trusted import/classification and formal/semantic validation
of the frozen negative-root theorem as specified in admission-request.json.
