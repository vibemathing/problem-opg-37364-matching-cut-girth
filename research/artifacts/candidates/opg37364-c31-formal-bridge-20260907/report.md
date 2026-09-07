# C31 scope and semantic audit

Verdict: candidate_only. No original C20/C21A/C21B/C22 lemma was found false.
This is not an independent verifier attestation and not a Result.

## Frozen full target

Fix d0=5. For every integer g>=3, there is a finite simple 2-connected
bipartite graph G with girth(G)>=g, 2|E(G)|+2<=5|V(G)|,
maximum degree at most 62, and no matching cut whose two shores are nonempty.
An empty crossing matching is allowed. The source of the universal existence
claim remains the persisted conventional proof. C31 proves conditional
logical/arithmetic components; it does not produce the missing seed theorem.

## E: exact statement of the general proof certificate

Interpret V as the entire vertex set, Old(x) as membership in the core,
Adj(x,y) as adjacency, Eqv as actual equality, and C as all subsets of V.
Interpret Col(c,x) as x belonging to c. In the abstract proof Eqv is simply
a binary predicate; no equality rule is used. Actual equality is a valid
specialization, not an extra premise needed by the derivation.

Define Opp(c,x,y) as
  (Col(c,x) and not Col(c,y)) or (not Col(c,x) and Col(c,y)).
Valid(c) says that for all x,u,v, Adj(x,u), Adj(x,v), Opp(c,x,u), and
Opp(c,x,v) imply u=v. In a simple undirected graph this means at most one
opposite neighbour at every vertex, exactly the crossing-matching condition.
ValidOld adds Old(x), Old(u), Old(v) to these hypotheses.

TwoSidedOld(c) has two existential witnesses: an old member of c and an old
nonmember. TwoSided(c) has the same two witnesses without the old restriction.
The certificate proves the implication from the following three premises:

1. There is an old vertex.
2. Every vertex is old, or has two distinct adjacent old vertices.
3. For every c, ValidOld(c) implies not TwoSidedOld(c).

The conclusion is: for every c, Valid(c) implies not TwoSided(c).
All three premises are discharged inside the closed proof term. They are
not added as axioms. The claim is conditional: C31 does not prove that a
high-girth core satisfying premise 3 exists.

The first part of the derivation pulls global validity back to the core.
No-cut core validity implies every two old vertices have the same colour;
the nontrivial-shore witnesses in this implication are explicit. Fix an old
anchor. For an attached vertex, opposite colour to that anchor would put
two distinct old neighbours across its cut, contradicting Valid. The
certificate uses classical double-negation elimination four times and no
finite graph enumeration. It then explicitly contradicts the two global
shore witnesses. Eigenvariables introduced by existential elimination cannot
escape; universal variables cannot be free in an open hypothesis.

For the subdivision construction, each new vertex is adjacent to the two
distinct endpoints of its own artificial edge, and all old edges remain.
These observations instantiate the attachment and restricted-validity
premises. Simple/bipartite/girth/2-connectivity of the construction remain
separate graph lemmas: they are NOT smuggled into the logical certificate.

## Quantifier bridge and polarity

The second closed proof derives not(root) from
  exists d, Positive(d) and
    forall g, Threshold(g) -> exists G, Admissible(d,g,G) and not Cut(G).
Here Positive(d) means d>0; Threshold(g) means integer g>=3; Admissible
contains the finite simple graph, average-degree and girth requirements.
The root is forall d, Positive(d) -> exists g, Threshold(g) and
forall G, Admissible(d,g,G) -> Cut(G).
The density is chosen once outside forall g. The bridge has no classical
rule and no graph-existence premise hidden in its proof. A proof of this
conditional must never be registered as proof of the positive root.

## A-D/F and strict inequalities

The new coefficient checker computes a weighted permanent by matching-mask
DP, then compares C22's coefficient formula and ordered-tuple convolution.
The fixed-shore event remains different from its union over shores.
At N=2,q=24, exact binomial type aggregation yields incidences 1204 and
bad-tuple union 602; the correct inequality is union <= incidences.
The general count needs the complement-bijection and induction, still open
for native formalization. The small checks are not substitutes for it.

The edge-instance DFS canonicalizes only complete unoriented cycle edge sets.
Parallel two-cycles survive this canonicalization. Overlapping pairs are
checked by e>=v+1, including shared paths. A figure-eight control additionally
covers shared-vertex-only overlap. The newly enumerated domain includes
cycles through length six, hence its 3588 adjacent-shared-path count is not
the earlier shorter-cycle domain's 1200. Original statistics/corrections
in PR29 remain untouched.

Thirteen exact polynomial certificates add general arithmetic checks, not
bounded substitution experiments. Named slack variables range over all
nonnegative integers. Coefficient expansion verifies these identities or
nonnegative differences; positive constant term licenses a strict inequality.
The graph-to-slack substitutions are explicit in each certificate and remain
part of the semantic audit.

In particular, b=i+u and N=b+t give
  b(N-i)-N(b-i)=i*t>=0.
This is the without-replacement slot comparison after verifying positive
denominators; it is NOT slot independence. The C20 exact rational constants
and finite-tail inequalities are checked with integers. Its conventional
induction and finite sum arguments remain the general justification.

For a smaller shore, write deltaY=2s+2+2z. Deleting at most s-a matching
edges and one additional edge leaves boundary-s >= a+1+2z>0.
This separates matching deletion from the extra single deletion. The
2-connectivity argument still uses the bipartite 43-versus-24 component
bound rather than an unsupported claim of deletion invariance.

For D, write k=1+j and N=5B+1+u. Then
  k(N-B)-4kB=(1+j)(1+u)>0.
This verifies the far-edge arithmetic, not existence of the maximum object
or the entire graph-exchange lemma. Current J distances, both cycle pairings,
u=v, and one-new-edge cycles remain explicit. Their path-length comparisons
are also certified for every g=3+h with nonnegative slack lengths.

For F, write 2m=24n-2-r and t=19n, with r>=0. Then
  5(n+t)-(2m+4t)=2+r>0.
Thus the strict-five endpoint genuinely needs the seed deficit. The
polynomial part of the order formula also checks exactly; substituting
T=(384g^2)^(2g) additionally requires the usual natural-power identity.
The first choice of d0=5 and k=38 is never made dependent on g.

## Sixteen mutations

All M01-M16 are executed by the new implementation: replacement slots;
incidence/union equality; omitted parallel two-cycles; omitted shared paths;
nonmatching deletion; stale H rather than current J distances; parity;
omitted u=v; one-new-edge cycles; opposite new point on a monochromatic
core; weak-five versus strict-five endpoint; edge-instance collapse;
twice subdividing a core edge; empty shore; disjoint common edges mislabeled
as a path; new leaf. These reject altered hypotheses, not the actual theorem.

The natural-deduction replay separately rejects eleven malformed proof
controls, including variable capture, existential escape, wrong sorts,
forged conclusions and unauthorized inference/axiom fields. One positive
control exercises disjunction elimination. The checker is not thereby
self-certified: its soundness and export correspondence need external review.

## Actual evidence ceiling and first open dependency

Native Lean is absent. The complete proof-term exports use Init only and
are pinned to 4.19.0; they have not been elaborated. No native axiom-print
output, admitted toolchain fingerprint, provider attestation, mathematical
run ID or trusted gate verdict exists. The replay results are local checks
of the frozen proof certificates, not trusted Lean results.

Current verifier registry, candidate ledger and adapter/closure code retain
the missing scoped chain described by the existing admission-request.
No new request is substituted for progress, no fixture is run out of scope,
and no truth ledger is changed. Trusted verified scope remains empty.
First native replay action: lake build on the three pinned exports, followed
by the three printed-axiom commands and semantic mapping review.
First genuinely unformalized combinatorial lemma remains compatible
permutation completions = (N-k)!; next is the finite cycle-pattern cover.

## Transport limitation recorded before the C31 commit

Two attempts at the unchanged tree write containing the two E Lean exports
were blocked by the platform's undetermined-safety state. The logical ND
certificates, exact replay inputs and actual outputs are preserved, but
`CoreExtension.lean`, `NoCutExtension.lean` and their three constructor
scripts remain local pending files enumerated in `pending-files.json`.
The only Lean build target included in this partial commit is the
quantifier-order bridge, which is also uncompiled. Do not confuse the
locally generated full exports discussed above with transported source.
This interruption is a transport/compilation gap, not a counterexample
to the conventional graph argument and not an admission verdict.

## Output-label scope clarification

The generic ND replay wrapper uses the same short `scope` string for each
certificate, including the quantifier bridge. That string is a coarse
disclaimer, not the formal statement. The frozen `goal`, its checksum and
the per-certificate explanations above distinguish the E implication from
the family-to-negative-root implication. Raw measured output is retained
unchanged; no graph-existence assertion follows from that wrapper label.
