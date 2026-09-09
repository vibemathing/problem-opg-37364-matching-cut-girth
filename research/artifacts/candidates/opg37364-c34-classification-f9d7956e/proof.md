# C34: canonical four-class encoding for the C33 parallel-two-cycle incidence

Status: NONTERMINAL_CHECKPOINT; verdict=candidate_only.
This is a conventional proof refinement and executable bijection atlas, NOT a
successful native Lean replay. The requested compiled equivalence/cardinality
chain has not been completed. No root theorem or trusted closure is supplied.

Frozen repository input: f9d7956eda5ac0f30d22f0fb8e48de3d3bc1870a.
Target: obligation:opg37364-root, auxiliary C33 slice only.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.

## 1. Statement and source-faithfulness

Let Q={0,...,23}, Omega_N=Sym(Fin N)^24 and Z=(N!)^24. These are the
coloured permutation coordinates of C20; edge instances are (colour,input).
The auxiliary graph is expressly a multigraph. It is not a final simple
witness of the root statement, whose nontrivial shores remain unchanged.

A two-cycle is (x,y,A), with x,y in Fin N and A a two-element SET of colours.
It is realized by omega exactly when omega_c(x)=y for both c in A. A C33
Witness is an UNORDERED pair of distinct two-cycles sharing a left or right
endpoint. For w in Witness, E_w is its realization event, and
I22={(omega,w): omega in E_w}. Bad22={omega: there exists w with omega in E_w}.
This is exactly the C33 definition (including distinctness), not the event
that a single two-cycle exists. N=0 has no witnesses and I22=Bad22=empty.

The only proposed probability conclusion is, for N>=1,
  |Bad22|/Z <= 69828/N - 31878/N^2.
This contribution was already part of C20's coarse BadOverlap catalogue. It
must NOT be added again to that complete coarse bound. Neither total<41/800
nor the existence of a Good tuple nor the root family follows from C34 alone.
The constants are the manuscript's own counts, not quotations from a paper.

## 2. The four classes must be applied to realizable/compatible witnesses

For w={s,t}, s=(x,y,A), t=(z,v,B), call w compatible if a shared colour can
occur only with identical endpoints. That is, for c in A intersect B,
x=z AND y=v. Equivalent symmetric conditions can be imposed on all members
of the unordered witness; they do not require selecting an orientation.

Every realized witness is compatible. If x=z, equations omega_c(x)=y and
omega_c(z)=v imply y=v. If y=v, injectivity of omega_c implies x=z. C33's
shared-endpoint condition guarantees one of these two starting equalities.
Therefore an incompatible witness has E_w=empty. No event has been omitted
from I22 by restricting to compatible witnesses: its putative contribution
was zero.

A concrete counterexample to an INCORRECT unconditional classification of
all raw Witness values is N=2,
  s=(0,0,{0,1}), t=(0,1,{0,2}).
It is a genuine C33 Witness because the left endpoint is shared. It lies in
none of the FOUR NONZERO classes: the two targets differ, while colour 0 is
shared. Its event would require omega_0(0)=0 and omega_0(0)=1. This is NOT a
counterexample to C33's conventional proof, which already classified
nonzero events. It is a warning against silently strengthening its Lean
translation to all raw witnesses. No original lemma is withdrawn.

On compatible distinct witnesses, the mutually exclusive exhaustive cases
are: T same endpoints and a common colour; Q same endpoints and disjoint
colours; L only left endpoint shared; R only right endpoint shared. In L/R
compatibility forces disjoint colour sets. In T, the common colour is unique:
two distinct two-sets cannot have intersection of cardinality two. Thus T
has three union colours, while Q/L/R have four.

## 3. Explicit canonical index types and both inverse directions

Write Choose(m,r) for the r-element subsets of Fin m, presented in increasing
order. This is a finite type with cardinality binom(m,r). The implementation
uses increasing tuples; the proposed Lean index source uses powersetCard.
The order is only a canonical encoding device, not a hypothesis on graph
labels. The two components of the bipartition have separate labels.

TIndex(N) = (Fin N x Fin N) x Choose(24,3) x Fin 3.
Given (x,y,S,j), let c be the j-th colour of S, and let a,b be the other two.
Encode the unordered witness {(x,y,{c,a}),(x,y,{c,b})}. Decode a T witness by
recovering x,y, its three-colour union S, and the position of its unique
common colour c. Encode-then-decode recovers S and c by union/intersection.
Decode-then-encode recovers the two exclusive colours, hence precisely the
original unordered pair. Swapping the two input cycles changes no code.

QIndex(N) = (Fin N x Fin N) x Choose(24,4) x Fin 3.
Given (x,y,S,j), with S=(s0<s1<s2<s3), pair s0 with s_(j+1) and let the other
two colours form the second cycle. Decode by selecting the UNIQUE original
colour pair containing the least union colour s0; its other colour determines
j+1. The original two pairs are disjoint, so uniqueness is genuine. These
operations are inverse: the complement in S determines the unselected pair.
There are three, not six, Q partitions because the pair containing s0 has
been selected canonically while the witness itself remains unordered.

LIndex(N) = Fin N x Choose(N,2) x Choose(24,4) x Choose(4,2).
An index contains left centre x, right endpoints {y0<y1}, four colours S, and
two ranks U in Fin 4. Put the two selected colours at y0 and the complement
at y1. Decode an L witness by ordering its two distinct right endpoints,
recovering the union palette and the ranks of the colours at the smaller
endpoint. Encoding preserves that smaller endpoint and its selected pair;
decoding therefore returns exactly the index. Conversely the two original
cycles are recovered. There is NO further factor two: endpoint ordering
already identifies which of the six colour assignments was chosen.

RIndex(N) has the same product type. Use the right centre and the ordered
left endpoints instead. The identical two-sided inverse proof applies.

Consequently the compatible Witness subtype is in bijection with the
DISJOINT SUM TIndex + QIndex + LIndex + RIndex. A complete formal proof must
construct this equivalence between the actual C33 finset subtype and these
index types, not replace that equivalence by matching numbers. In this
package that equivalence is explicit in the mathematical argument and in
the executable encode/decode functions; its Lean Equiv proof remains open.

## 4. Why the finite colour atlas is not a small-N extrapolation

Two two-cycles use at most two distinct labels on each bipartition side.
Order each side's used labels and replace each by its rank. Equality,
distinctness, shared endpoint, and the choice of the smaller endpoint are
preserved and reflected. The colour pairs remain unchanged. Conversely an
actual choice of the used labels and their increasing placement restores
the original witness. This is a bijection on witness SUPPORT DESCRIPTIONS,
not a map from Omega_N to Omega_2 and not a probability-preserving reduction
of the ambient permutation sample space.

There are only the endpoint equality types: same both, left only, right
only, neither. For same endpoints two equal colour pairs are diagonal and
excluded. For the other two intersecting types all ordered colour-pair
assignments must be checked, including conflicts. 'Neither' is not Bad22.

The actual atlas run exhausts all 24-colour choices in these support types
and checks both encode/decode directions, not random samples of graphs.
This verifies the finite colour implementation. The preceding arbitrary-N
support-renaming proof and the factorial event counts still require their
own mathematical/formal justification. The atlas is generator-owned code,
not a native Lean or independently admitted verifier.

## 5. Index cardinalities and boundary cases

The preceding product-type equivalences give
  |TIndex|=N^2*binom(24,3)*3=6072 N^2;
  |QIndex|=N^2*binom(24,4)*3=31878 N^2;
  |LIndex|=|RIndex|=N*binom(N,2)*binom(24,4)*6
                    =31878 N^2(N-1).
The last equality uses 2*binom(N,2)=N(N-1), with natural subtraction. It is
valid at N=0,1 because Choose(N,2) is empty; no ordered pair with equal
endpoints is manufactured. The two same-endpoint classes may exist at N=1.
All binomial factors count finite sets, not independent probabilistic events.

## 6. Actual coordinate tables and the C32 connection

For a witness w, define requirements(w,c) to be the UNION of the corresponding
(x,y) pairs imposed by its two cycles at colour c. These are sets. A shared
edge in T appears in both cycle traversals but only once in this union.
Compatibility implies each requirements(w,c) has cardinality at most one.
Thus construct a table a_w(c): none when the requirement set is empty;
some(x,y) when the set is {(x,y)}. The table is unique; choosing an element
of a nonempty requirement set does not introduce an additional random choice.

This constructs the Encodes hypothesis that C33's card_encoded_event required.
No unproved per-shape table oracle is added. For a none coordinate, use C32
k=0, empty input embedding, and target all of Fin N (b=N). For a some(x,y)
coordinate, use the actual embedding Fin 1 -> Fin N with value x and the
singleton target {y}; k=b=1. C32 card_hit yields N! and (N-1)! respectively,
and card_hit_tuple24 supplies the product over coordinates. The family of
permutation coordinates is a Cartesian product. No two slots of one
permutation have been factorized.

T has three active coordinates, so |E_w|=((N-1)!)^3(N!)^21. Q/L/R have four,
so |E_w|=((N-1)!)^4(N!)^20. For N>=1, N!=N(N-1)! normalizes these probabilities
to N^-3 and N^-4. The zero-witness boundary N=0 is separate.

A same-colour left fork is not a second slot: it would give two different
outputs for one input and has no function completion. A same-colour right
fork has two DISTINCT inputs and a singleton target. The explicit Fin 2
input embedding connects it to C32 card_hit_of_target_small, b=1<k=2, so its
count is zero. When N<2 such distinct inputs do not exist in the first place.

In later catalogue classes, several compatible prescribed pairs may inhabit
one coordinate. A fixed pairing has (N-k)! completions, whereas merely
requiring hits into a k-element target allows k! different pairings. C34
does not conflate these events or claim its singleton table handles those
later classes.

## 7. Incidence sum and correct direction of the final inequality

Projection I22 -> Bad22, (omega,w) |-> omega, is surjective. A least-witness
selector would conversely give an injection Bad22 -> I22, not into the
witness index type alone. Therefore |Bad22|<=|I22|. No independence or
disjointness of the tuple events E_w is needed to SUM INCIDENCES:
  |I22|/Z =6072/N+31878/N^2+63756(N-1)/N^2
           =69828/N-31878/N^2.
For N>=1 this proves the stated candidate bound, and also a strict upper
bound 69828/N because 31878/N^2>0. The bound can exceed 1 at small N and is
not a Good-tuple existence claim. At N=1, |I22|=37950 but |Bad22|=1, a useful
exact control on the incidence/union distinction.

## 8. Native status, proof-source scope, and first open dependency

The official new target is Lean4.33.1 commit
819816b2e0a3bf405af45ae5c7af2491d8f5bee6 and Mathlib
0df444a360eaa60ab8c11dca51a86af692955474. These source refs were freshly
resolved. They do not constitute an installed binary fingerprint.

ProjectionOnly.lean is an isolated new proof of the exact C33 projection
statement, retaining its definitions but removing the irrelevant need to
import C32 just for a finite surjection. It is not imported with the full
C33 module because it intentionally uses the same names.

C34Classification.lean gives uncompiled source for realized_admissible,
inadmissible_empty, a unique four-way classifier, common/union colour
cardinalities, an actually constructed Encodes table, its C32 event count,
and the explicit right-fork b=1,k=2 zero bridge. C34IndexCardinalities.lean
contains source proofs of the abstract product-index cardinalities, not an
assumed equivalence to graph-defined Witness. All new sources remain
UNCOMPILED; the canonical witness-to-index Lean Equiv is not yet supplied.
The pending axiom-print files are queries, never observations.

The current runtime search found no lean/lake/elan. A genuinely different
acquisition route was attempted: the official exact-commit Linux CI artifact
was located, but the download action rejected its 1,456,550,059 bytes against
its 536,870,912-byte maximum. No limit bypass or fabricated compiler run
followed. Direct network acquisition supplied no usable executable. The
runtime-referenced external environment was not available as a callable tool.
Native compilation exit codes and axiom outputs therefore remain null.

Next native step: elaborate ProjectionOnly.lean at the full locked commits,
then replay the frozen C31/C32/C33 sources and these successor sources; save
the first real elaboration error, apply only a successor patch, and rerun.
Next missing formal-combinatorial dependency: port the explicit generic
encode/decode maps into actual Lean Equiv values for the four compatible
Witness subtypes, prove both inverses and join them to the index-cardinality
lemmas before asserting any Lean theorem for the numerical incidence bound.

Remaining catalogue: mixed/long shared-edge cases; shared paths (including
multiple common components); mixed/long pairs meeting only at a vertex; and
vertex-disjoint short-cycle families for matching deletion, not bad-event mass.
No total bound, root theorem, independent replay or trusted closure is claimed.
best_verified_result=none; both admitted obligations remain open.
