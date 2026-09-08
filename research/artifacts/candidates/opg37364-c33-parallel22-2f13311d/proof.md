# C33: the overlapping parallel-two-cycle incidence slice

Verdict: candidate_only. Status: NONTERMINAL_CHECKPOINT.
Primary owner: math-proof. Target: obligation:opg37364-root.
Problem: problem:opg-37364-matching-cut-girth.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Frozen repository revision: 2f13311db729316187f5b3fc073bf8b831ae1166.

## 1. Statement-faithfulness before counting

The frozen root concerns finite SIMPLE graphs, both matching-cut shores nonempty,
and all crossing edges forming a matching (possibly empty). The target family
in C21B fixes d0=5 before the arbitrary integer g>=3; it additionally asks for
2-connectivity, bipartiteness, 2|E|+2<=5|V|, and maximum degree<=62.
Nothing in this slice changes those quantifiers or claims that family exists.

C20.2-C20.6 explicitly use a different, auxiliary object: a coloured bipartite
MULTIGRAPH from 24 permutations. Its parallel edge instances are intentional.
C20's Good condition forbids two DISTINCT short cycles sharing a vertex. It does
not forbid an isolated two-cycle: one edge of each vertex-disjoint short cycle
is deleted later. A two-cycle is short at every g>=3. We freeze only

  Bad22 = {tuples having two distinct parallel two-cycles with a common vertex}.

This is a subclass of BadOverlap, not all of BadOverlap and not the event
"there is a parallel edge pair". The latter distinction is indispensable.
A longer cycle meeting a two-cycle is outside this slice.

The original OPG page, Question and the following definition, does not explicitly
exclude the empty set S. The canonical contract does. The 2025 publisher's
Section 2, valid-colouring condition 3, says "both colours red and blue are used
at least once". Its graph domain is simple; Section 1, Our Focus, assigns infinite
girth to forests. These definitions agree with the explicitly frozen root
interpretation, not with treating auxiliary two-cycles as cycles in a root witness.
Source locators are in source-map.json. No published existence theorem is used.
The numerical constants below are derived here for the candidate manuscript;
they are NOT attributed to the 2025 publication.

## 2. Finite objects and the correct projection

Let N>=1 and q=24. Define U={0,...,N-1}, C={0,...,23},
Omega=Sym(U)^C and Z=|Omega|=(N!)^24. Left and right vertices are tagged disjoint
copies L(U), R(U). Edge instance (c,x) joins L(x) to R(pi_c(x)). Its identity
includes c even when another edge has the same two endpoints.

A two-cycle code is (x,y,A), where x,y in U and A is a TWO-element subset of C.
It is present in omega iff pi_c(x)=y for every c in A. The two orientations of
this two-cycle are the SAME code; two different two-element colour sets give
different cycles. A witness w is an UNORDERED pair {s,t} of distinct two-cycle
codes, with s.x=t.x or s.y=t.y. Define R(omega,w) to mean that both codes are
present. All types are finite. Put

  I22 = {(omega,w) : R(omega,w)},
  Bad22 = {omega : exists w, R(omega,w)},
  X22(omega) = number of witnesses w satisfying R(omega,w).

The projection I22 -> Bad22, (omega,w) |-> omega, is surjective, because every
bad tuple has a witness. Consequently |Bad22|<=|I22|. It is generally not
injective. Alternatively choose the lexicographically first witness of each
bad tuple: omega |-> (omega,first(omega)) is an INJECTION Bad22 -> I22.
There is no asserted injection from bad tuples to the witness index alone.
Also |I22|=sum_omega X22(omega), exactly. Thus

  Pr(Bad22) <= |I22|/Z = E[X22].                         (1)

This is precisely the relation accepted by C32 R10.Hits.badCut_le_incidence,
whose name does not restrict its generic relation argument to graph cuts.
The relation instantiated here is R, not C20's shore relation.

## 3. Normalizing prescriptions; connection to C31/C32

For each witness list the four edge occurrences of its two cycles, then for
coordinate c take the SET D_c of required pairs (x,y). Identical repeated pairs
are one constraint. If D_c contains (x,y),(x,z) with y!=z, it has no realizing
function. If it contains (x,y),(z,y) with x!=z, it has no realizing permutation.
Otherwise it specifies a partial injection with k_c distinct inputs and exactly
k_c distinct prescribed outputs. It has (N-k_c)! extensions: restrict a completion
to the two complements, and conversely glue a complement bijection to the
prescription. Complement sets have size N-k_c, so choosing their images in turn
counts (N-k_c)!, including the empty complement. This is C31 card_fin_completion,
and C32 card_assigned explicitly identifies the ordered pairs with that type.

A related but DIFFERENT event says that k_c distinct inputs all land somewhere
in a target B_c of size b_c. Its count is (b_c)_(k_c)*(N-k_c)!, by first choosing
an injection of these inputs into B_c and then a completion. This is C32 card_hit.
It is zero when b_c<k_c. A fixed prescribed bijection into k_c allowed targets is
NOT that Hit event when k_c>1: Hit also permits all k_c! assignments of those
outputs. This distinction must be retained for subsequent longer-cycle patterns.

For every FEASIBLE witness in the present slice, each active coordinate has
exactly one distinct pair, hence k_c=b_c=1 with input list [x] and B_c={y}.
Every other coordinate has k_c=0 and may take B_c=U, b_c=N. Thus the fixed-pair
condition is EXACTLY C32's Hit condition, not a relaxation. Its per-coordinate
counts are (N-1)! for active coordinates and N! for inactive ones.

The full event is the Cartesian product of these 24 coordinate Hit types;
C32 tupleEquiv/card_hit_tuple24 give its count. If d coordinates are active,

  |E_w| = ((N-1)!)^d * (N!)^(24-d),
  Pr(E_w) = 1/N^d.                                     (2)

Only the Cartesian coordinates factor. Repeated slots within one permutation
never factor. The rational identity N!=N*(N-1)! is used only for N>=1.
The case N=0 has no cycle codes, hence I22=Bad22=empty, and is handled separately.

## 4. Exhaustive classification and event multiplicities

Write s=(x,y,A), t=(z,v,B), |A|=|B|=2. Their pair is unordered and s!=t.
A witness with nonzero event count belongs to exactly one of the following.

### T: same endpoints, one shared EDGE INSTANCE

Here x=z, y=v and |A intersect B|=1. The union of colours has size 3.
Select x,y, a three-element colour set T, then its common colour c (three
choices). The other two colours determine the two unordered cycles uniquely.
The shared pair (c,x,y) occurs twice in the raw list but is one prescription.
Exactly three coordinates have k=b=1. There are

  W_T = 3*binom(24,3)*N^2 = 6072*N^2                 (3)

witnesses, each of probability N^(-3). Equivalently any fixed triple of parallel
edges supports three unordered pairs of two-cycles. Dividing out this factor
without changing the witness type would corrupt the exact incidence count.

### Q: same endpoints, NO shared edge instance

Here x=z, y=v and A intersect B is empty. Choose four colours, then split them
into an unordered pair of two-element sets. There are exactly three splits
(fix the smallest colour and choose one of the three others as its partner).
Exactly four coordinates have k=b=1. There are

  W_Q = 3*binom(24,4)*N^2 = 31878*N^2                 (4)

witnesses of probability N^(-4). These cycles share BOTH endpoints. Four
parallel edges also contain T witnesses, but those are DIFFERENT cycle pairs.
The T and Q witness classes are disjoint even though their tuple events overlap.

### L: one shared LEFT vertex, two distinct right endpoints

Here x=z and y!=v. Order the right endpoints y<v to canonically order the cycles.
The colour sets must be disjoint: if c belongs to both, pi_c(x)=y and pi_c(x)=v
would conflict. Such colour choices have event count zero, not N^(-4).
For a feasible choice, four separate coordinates each have k=b=1.
Choose the left centre (N choices), the two right endpoints (binom(N,2)),
the two colours at the smaller endpoint (binom(24,2)), and the two colours at
the other endpoint (binom(22,2)). These choices are uniquely recovered from w.
Since binom(24,2)*binom(22,2)=6*binom(24,4),

  W_L = 3*binom(24,4)*N^2*(N-1).                       (5)

Each event has probability N^(-4). No extra factor two for ordering the two
cycles is permitted: ordering the endpoints already fixed that order.

### R: one shared RIGHT vertex, two distinct left endpoints

Here y=v and x!=z. Order x<z. Again the colour sets must be disjoint: a common
coordinate would prescribe two distinct inputs to the same output. This is
also the C32 b=1,k=2 zero case, not an independent-slot event. The feasible
count equals W_L and its probability is N^(-4). Direct prescription counting
or the bijection (pi_c)_c |-> (pi_c^(-1))_c proves the same value; symmetry is
not an independence assumption.

These four cases exhaust all witnesses of nonzero count. If both endpoints
agree and the colour intersection has size two, the cycles are identical and
were excluded. If neither endpoint agrees, the cycles are vertex-disjoint and
were excluded. No connectedness assumption about the entire auxiliary graph
enters this classification.

## 5. Exact symbolic incidence and manuscript constant

Summing event sizes (not claiming disjointness of the tuple events) gives

  |I22|/Z = 3*binom(24,3)/N
          +3*binom(24,4)/N^2
          +6*binom(24,4)*(N-1)/N^2
          =69828/N - 31878/N^2.                        (6)

Combining (1) and (6), for every integer N>=1,

  N^2*|Bad22| <= N^2*|I22|
                 =(69828*N-31878)*(N!)^24,             (7)

and equivalently

  Pr(Bad22) <= 69828/N - 31878/N^2 < 69828/N.           (8)

The strict last inequality uses N>0 and 31878>0. A bound greater than one at
small N is still an upper bound and supplies no existence conclusion there.
For q permutation coordinates the same classification replaces 69828 by
3*binom(q,3)+6*binom(q,4), and 31878 by 3*binom(q,4). This q-parameter variant
is proved by the identical four counts; finite tests below do not prove it.

Manuscript-ready lemma: If X22 counts unordered pairs of distinct parallel
two-cycles meeting a vertex in the 24-permutation model on equal N-element
parts, then E[X22]=69828/N-31878/N^2, and P(X22>0)<=E[X22].

In contrast, the SINGLE-two-cycle incidence has N^2*binom(24,2) indices, each
of probability N^(-2), so its expected count is 276, not an O(1/N) incidence
term. This shows why the two event definitions cannot be interchanged in
C20's deletion argument. It does not identify an expectation with a union.

## 6. How this interfaces with the other pattern counts

C20's generic C_g=(2g)^2*(96*(2g)^2)^(2g) already covers the present class.
The 69828 contribution is an explicitly classified portion, NOT an extra
penalty to add on top of the old all-pattern C_g bound. A sharper total would
require partitioning the remaining witnesses and recomputing that remainder.

Still pending after this slice:
1. A two-cycle/longer-cycle or two longer cycles sharing edge instances; raw
   common edges must be normalized, and a coordinate can have k>1.
2. Shared paths (especially length>=2), including multiple common components;
   avoid counting the same unoriented cycle twice or equating disjoint common
   edges with one path. A path of length one belongs to the previous category.
3. Vertex-disjoint short-cycle families: these are not BadOverlap events.
   Their catalogue supports simultaneous matching deletion, not an additional
   bad-event union-bound term.

Mixed/long pairs sharing only vertices but no edges must also be covered in the
remaining overlap catalogue. The three headings are not by themselves a claimed
exhaustive disjoint partition of every remaining longer-cycle intersection.
No total probability <41/800, Good-tuple theorem, root theorem, or closure is
asserted by C33.

## 7. Portable source and exact controls

parallel22.py specifies the labelled cycles, unordered witness identity,
prescription normalization, incompatible-pair zeros, and exact event counts.
It enumerates tuples only for the explicitly supplied small controls, never
for the enormous C20 selector. The independent input/output-pair formula used
by the controls is stated and proved in section 3; code success is supplemental.

The actual bounded run is run-01/execution.json; it completed with exit code 0.
It compares every realized witness frequency against its factorial event count,
the four index counts, the full incidence sum and its bad-object projection.
The N=1,q=24 control has 37950 incidences but only one bad tuple. The N=2,q=2
control in the mutations has disjoint two-cycles with no Bad22 witness. The
four-coordinate two-identity/two-swap control has only one-endpoint forks.
Fourteen negative controls detect wrong multiplicities, missing Q/forks,
within-coordinate independence, b<k, collapsed colours, and identical cycles.
All finite sizes and exact outputs are recorded; no finite extrapolation is used.

Parallel22.lean is portable uncompiled source. It defines the finite witness
relation and correct incidence projection and connects a normalized 24-coordinate
prescription table to C32's exact Hit counts. It does not pretend the general
four-shape bijective classification/count has already been elaborated in Lean.
Its names are listed in AxiomAudit.lean. The mathematical completion above is a
self-contained conventional proof; the Lean completion state remains separate.
The local tool probe found no locked Lean environment. No compiler output or
axiom list has been fabricated; no repeated ENOENT transaction was opened.

## 8. Candidate boundary and next atomic action

All generated objects stay in candidate paths. Existing C20/C21B/C31/C32 are
unchanged. Their recorded source and proof status is not upgraded by imports.
No fatal error in the original C21B is shown; incorrect event/multiplicity
variants are rejected without withdrawing the actual original lemma.

best_verified_candidate: none.
best_verified_result: none.
trusted_verified_scope: [].
open_obligations: obligation:opg37364-contract-edge-cases; obligation:opg37364-root.
Next action: elaborate the finite two-cycle witness/table bridge and the
T/Q/L/R counting bijections at the locked Lean/Mathlib version, then take the
first remaining mixed two-cycle/long-cycle shared-edge pattern. Do not rerun
transport, resubmit admission_request, or claim the full union bound from (8).
