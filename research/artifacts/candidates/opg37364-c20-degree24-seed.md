# C20: a degree-24 finite-counting seed at every girth

Verdict: candidate_only. Primary owner: math-proof.
Candidate: candidate:opg37364-degree24-seed-c20.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Base: b21a752dfce02c244cf67630e8b20e8d55d22d00.

## Statement and change from the existing candidate

For every integer g>=3, there is a deterministically specified finite
simple 2-connected bipartite graph H_g such that every degree is 23 or24,
its girth is at least g, and every nonempty proper shore S satisfies
  |delta_H(S)| > min(|S|,|V(H) minus S|).                  (A)
It has no matching cut. In particular fixed d0=25 gives the negative-root
quantifier pattern with average degree <=24<25, without using K1.

This replaces C16's forty-permutation seed by twenty-four permutations.
All changed constants, the tail bound and the overlap catalogue are
proved below. The previous 1/4 bound for large shores is NOT reused:
the new large-shore bracket is bounded instead by 2/3.
The construction uses finite graph reasoning, finite counting and
rational inequalities only. No external existence theorem is a premise.
No mathematical runtime, sampler, solver or verifier was run.
Both admitted obligations remain open.

The frozen graph domain is finite and simple. The auxiliary object below
is expressly an edge-coloured bipartite multigraph, not a root witness.
Both shores of a matching cut are nonempty, and an empty crossing matching
is allowed. Colours are forgotten only after simplicity is proved.

## C20.1. Elementary counting estimates

For integers 1<=j<=n,
  binom(n,j) <= (3n/j)^j.                               (1)
Indeed, for i>=1, i!>=2^(i-1). A finite geometric sum gives
sum_{i=0}^j 1/i!<3. Expanding (1+1/j)^j and using
binom(j,i)<=j^i/i! shows (1+1/j)^j<3.
Induction now proves j!>=(j/3)^j: the induction step reduces to
3>=(1+1/j)^j. Finally binom(n,j)<=n^j/j! proves (1).

A uniform permutation on [N] realizing k compatible prescribed pairs
has (N-k)! extensions. Incompatible input/output prescriptions have
zero extensions. If k distinct inputs are required to land in a fixed
b-set, the number of permutations is (b)_k*(N-k)! when k<=b, otherwise
zero. Here (b)_k is a falling factorial. Since
  (b-i)/(N-i) <= b/N  for 0<=i<b<=N,
the probability is at most (b/N)^k.
For several permutation coordinates, multiply their finite counts.
No independence is assumed between different slots of one permutation.

## C20.2. Auxiliary model and the exact bad-shore constraints

Take 24 uniformly chosen permutation coordinates pi_1,...,pi_24 of [N].
The sample space Omega has Z=(N!)^24 elements, all equally weighted.
Probability here means a finite cardinality divided by Z.

Make disjoint parts L and R, each with N labelled vertices. Edge instance
(i,u) joins L_u to R_{pi_i(u)}. Distinct instances may be parallel.
Every auxiliary degree is24, counting instances; there are no loops.

For a shore S of size s=a+b<=N, put a=|S intersect L|, b=|S intersect R|,
and let I count internal edge instances. Then
  |delta_Y(S)|=24(a+b)-2I.
Call S bad when 1<=s<=N and |delta_Y(S)|<=2s.
If either a or b is zero, it is not bad.

By exchanging L and R, and hence inverting every permutation, it suffices
to treat 1<=a<=b and count two orientations. A bad shore satisfies
  I>=11(a+b),  I<=24a,
and therefore
  b<=13a/11<2a,  b<=13N/24,  I>=22a.                  (2)
For the second inequality use a>=11b/13 and a+b<=N.
These are necessary conditions, not assertions of independent events.

## C20.3. All-shore bound with the new constant

If I>=22a, some 22a of the 24a slots starting in the a-set hit the b-set.
C20.1 bounds the probability of each chosen slot set by (b/N)^(22a).
A union bound thus gives, for fixed sets A,B,
  P(S bad)<=binom(24a,2a)*(b/N)^(22a).

Multiply by binom(N,a)binom(N,b) to sum over shores of sizes a,b.
From (1) and (2),
  binom(N,a)<=(6N/b)^a,
  binom(N,b)<=(3N/b)^b<=(3N/b)^(2a),
  binom(24a,2a)<=36^(2a).
Consequently the contribution for these sizes is at most
  [69984*(b/N)^19]^a,                                  (3)
because 6*9*36^2=69984 and 22-1-2=19.

For fixed a there are at most2a possible positive b. Also a<=floor(N/2).
Accounting for both orientations yields the finite union estimate
  P(BadCut)<=4*sum_{a=1}^{floor(N/2)} a*Q_a^a,
  Q_a=69984*min(2a/N,13/24)^19.                         (4)

The following exact rational comparison is the required replacement
for C16's forty-colour constant:
  69984*(13/24)^19 < 2/3.                              (5)
To verify it without decimals, (13/24)^3<4/25 follows from
25*2197=54925 < 55296=4*13824. Hence the left side of (5) is less than
  69984*(4/25)^6*(13/24)
    =3726508032/5859375000
    <3906250000/5859375000=2/3.
All denominators are positive.

## C20.4. Finite small/large-shore split

Let N=M^2 with integer M>=1000, and put
  theta=69984*(2/M)^19.
Then theta<1/100: use 2/M<=1/500 and
500^3=125000000>6998400=100*69984.
For a<=M, Q_a<=theta. For any positive integer T and 0<=x<1,
  (1-x)^2*sum_{a=1}^T a*x^a
    =x-(T+1)*x^(T+1)+T*x^(T+2)<=x.                    (6)
The identity follows by twice subtracting the sum multiplied by x;
the remaining end term is nonpositive. Therefore the part of (4)
with a<=M is at most
  4*theta/(1-theta)^2 <400/9801<1/20.

For every integer a>=12, a<=(5/4)^a. At a=12 this is
201326592=12*4^12<5^12=244140625.
The induction step follows from (5/4)*a>=a+1 for a>=4.
By (5), a*Q_a^a<=(5/6)^a whenever a>M.
Writing T=floor(N/2), the finite tail is bounded by
  4*sum_{a=M+1}^T (5/6)^a <24*(5/6)^M<1/1000.         (7)
For the final inequality M>=64 and
(5/6)^4=625/1296<1/2 imply (5/6)^M<1/65536; then
24000<65536. No infinite sum or convergence theorem is used.
Combining (6)-(7),
  P(BadCut)<1/20+1/1000.                              (8)

## C20.5. Short-cycle overlap and a single explicit size

Fix g>=3 and define integers
  K=2g, C=K^2*(96*K^2)^K,
  M=max(1000,4C,2g), N=M^2.                           (9)
A short auxiliary cycle has length from2 through g-1.
Cycles are identified by their unoriented sets of coloured edge
instances. A parallel pair is a length-two cycle.

If two genuinely distinct short cycles share a vertex, their union is
a connected pattern with v,e<=K and e>=v+1. To justify the last bound,
a spanning tree in a connected multigraph has v-1 edges, and adding
just one edge gives only one cycle, including a possible parallel pair.
Thus two distinct cycles require at least two additional edges.
Shared paths and shared edges between the cycles are not excluded.

At most K^2*2^K*(24*K^2)^K typed edge-coloured patterns need be considered:
choose v,e, the bipartition types of the abstract vertices, and an
ordered list of coloured endpoint pairs. This deliberately overcounts.
Restrict to distinct edge instances and e>=v+1; inconsistent same-colour
prescriptions have probability zero.

There are at most N^v injective labelings into the prescribed parts.
For a consistent labelled pattern, C20.1 gives probability
product_i 1/(N)_{e_i}<=(2/N)^e, since each e_i<=K and N>=2K.
Thus each abstract pattern contributes at most2^K/N.
The finite union bound gives
  P(BadOverlap)<=K^2*(96*K^2)^K/N=C/N
                <=1/(4M)<=1/4000.                    (10)
In (9), M>=K>=6 ensures N>=2K, and M>=4C proves the first ratio bound.

From (8)-(10), the number of tuples that fail either condition is less
than (41/800)Z. Consequently Good satisfies
  800*|Good|>759*Z>0.                                 (11)
It consists of tuples having no bad shore and pairwise vertex-disjoint
short cycles. No independence between those two properties is assumed.
This is a finite existence count, not a count obtained by enumeration.

## C20.6. Matching deletion and the final graph

Choose a Good tuple. From every short cycle delete one edge instance.
Because the short cycles are vertex-disjoint, the deleted set is a
matching of edge instances and each vertex loses at most one edge.

Deletion creates no cycle, and every original short cycle is hit.
In particular every parallel pair is hit, since g>=3 includes the
length-two cycles among the short ones. There are no surviving parallel
edges or loops. Forgetting colours now gives a simple bipartite H,
with every degree23 or24 and girth at least g.

For a nonempty proper shore take its smaller side S, with |S|<=N.
At most|S| deleted edge instances crossed it. Therefore
  |delta_H(S)|>=|delta_Y(S)|-|S|>|S|.                  (12)
This proves (A). It implies connectedness, and it excludes a matching
cut, since a matching has at most one incident crossing edge at each
vertex of its smaller shore. Distinct-neighbour language is used only
after the final graph has been proved simple.

The graph is also 2-connected. Suppose x is a cut vertex and C0 is a
smallest component of H-x. Then |C0|<|V(H)|/2 and its boundary has at
most24 edges, all ending at x. If x is in the left part, every left
vertex in C0 has at least23 right neighbours in C0, and every right
vertex has at least22 left neighbours there. Both classes occur since
minimum degree after deletion of x is at least22. Thus |C0|>=45.
This contradicts (12). The other part is symmetric, and the original
minimum degree23 guarantees the required order at least three.

## C20.7. Deterministic selector and root quantifiers

Order permutation tuples lexicographically by their value lists.
For each input g use exactly (9), choose the first Good tuple, and
delete the least edge of each short cycle under order (colour,left
label,right label). The selector exists by (11), and its universe
has exactly (N!)^24 elements. The expansion and short-cycle tests are
finite predicates defined before this selector.

This is a deterministic finite specification, not an efficient
algorithm or a claimed sample. Let H_g be the resulting graph.
Fix the rational d0=25 before g. For every integer g>=3, H_g has
  average_degree(H_g)<=24<25=d0,
  girth(H_g)>=g, and no matching cut.
It has cycles because its minimum degree is23. Thus the witnesses
also work in the nontrivial connected or 2-connected interpretations
of the source domain, without a forest-girth or empty-graph convention.
No real-number oracle is needed for this fixed-d0 family.

## Adversarial audit, sources and handoff

The changes are not the substitution of24 for40 in a conclusion.
They require the simultaneous replacements I>=22a, b<=13N/24,
slot loss2a, exponent19, constant69984, tail ratio5/6 and overlap
constant96. An unjustified reuse of the old1/4 tail would be a gap.
The necessary strict bound is proved in (5), not inferred numerically.

The two short-cycle orientations are the same cycle; two distinct
cycles sharing a path are covered. The slot estimates are without
replacement. Empty intersections with a bipartition part are excluded
by their actual crossing count24s, not overlooked. Expansion is counted
with edge instances before deletion and ordinary edges afterward.
A deletion set with unbounded degree would not justify (12).

C16 and C19 supply the earlier mechanism and its finite-count audit;
this note expands and rederives the changed proof. It does not import
their conclusion as a new axiom. The source map records the published
negative answer and stronger spectral seed for attribution only.
No originality or best possible degree is claimed.

Reproduction: check (1)-(5), the two finite tail estimates, the abstract
pattern cover and compatible permutation counts, then the matching
deletion and the nonempty-shore quantifier map. Verification concerns
these lemmas, not execution of the enormous selector.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: transfer the sharper C18 saturation count to the new
degree23-or24 seed, keeping d0 fixed and proving the changed constants.
No mathematical receipt or trusted admission is supplied by this file.
