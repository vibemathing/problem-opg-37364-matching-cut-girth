# C21A: uniform-size reuse of C20 and a strict one-edge deletion margin

Verdict: candidate_only.
Candidate: candidate:opg37364-c21-seed-margin-9491f4b1.
Primary owner: math-proof.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.
Read base: 9491f4b15e504fc415362ba55591483a941443a6.
Transport: locally staged only; no C21 branch, commit or PR is claimed.

## Frozen dependency and the precise new assertions

C20 is now on the read main:
  research/artifacts/candidates/opg37364-c20-degree24-seed.md
  SHA-256 declared by its packet:
  2633106848426c561eb173591321516ab85340826db0d0e405bb3aaf08e674db.
Its Git blob was read as ed9a46326c3a994e26d0236a5b87eda7c2004c6c.
Its transport packet is research/artifacts/web-inbox/opg37364-a01-c20.json.
C20's mathematical arguments remain candidate dependencies, not Evidence.

Do not re-register the reduction from forty to twenty-four permutation
coordinates as new work here. The present advance is:
(1) make explicit that C20's finite existence count works at EVERY
    sufficiently large square part size, with the girth input fixed;
(2) use parity of the auxiliary cut count to obtain an additive
    two-edge margin, then safely delete one more edge;
(3) preserve two-connectivity and enforce a strict seed edge deficit.

The construction continues to use the frozen two-nonempty-shore convention,
and permits an empty crossing matching. Final graphs are finite and simple.
Both admitted obligations remain open. No mathematical runtime was run.

## A1. Uniform-size extension, checked against every size-dependent step

Fix g>=3 and set
  K=2g, C=K^2*(96*K^2)^K, M0=max(1000,4C,K).
For any integer M>=M0 put N=M^2.

Use the same 24-permutation finite space and coloured edge representation
as C20. The C20.1-C20.3 counting bounds concern an arbitrary positive N.
In particular they give
  P(BadCut) <=4*sum_{a=1}^{floor(N/2)} a*Q_a^a,
  Q_a=69984*min(2a/N,13/24)^19,
with the exact rational bound
  69984*(13/24)^19<2/3.
No special equality M=M0 is used in these bounds.

C20.4 only uses N=M^2 and M>=1000. For a<=M its small-shore
bracket is at most theta=69984*(2/M)^19<1/100. The displayed finite
sum identity gives the contribution below 1/20.
For a>M, the same proof uses a<=(5/4)^a for a>=12 and Q_a<2/3,
bounding a*Q_a^a by (5/6)^a. Its finite geometric tail is below
24*(5/6)^M<1/1000. Each inequality remains true as M is increased.
Thus
  P(BadCut)<1/20+1/1000.                                   (1)

The union-of-two-cycles catalogue in C20.5 has at most
K^2*2^K*(24*K^2)^K patterns. Its v,e bounds and excess e>=v+1
depend only on g. Its permutation-extension probability bound needs
N>=2K, which follows from M>=K>=6. Summing the labelled-pattern
bounds gives
  P(BadOverlap)<=C/N.
The only other size step is
  C/N=C/M^2<=1/(4M)<=1/4000,                               (2)
using M>=4C and M>=1000. Again an equality M=M0 is not required.

Equations (1)-(2) and a finite union bound yield
  800*|Good|>759*(N!)^24>0                                (3)
for EVERY such M. All counts use finite sets; no limit, independence
of the two bad events, or unproved larger-order existence theorem
is inserted.

Consequently C20's selector can be extended to input (g,M): choose
the first Good tuple in the finite lexicographic ordering. The
existence of that tuple is supplied by (3) in the written candidate
before the selector is defined. This is not a claim that graphs of
an arbitrary, non-square part size are supplied.

## A2. The parity margin is a property of this construction

Let Y be the selected 24-regular coloured auxiliary multigraph.
For any nonempty smaller shore S, write s=|S| and I for its number
of internal edge instances. Then
  |delta_Y(S)|=24s-2I.
It is an EVEN integer. Good excludes |delta_Y(S)|<=2s, so in fact
  |delta_Y(S)|>=2s+2.                                    (4)

As in C20.6, delete one edge instance of each short cycle.
The short cycles are pairwise vertex-disjoint, so this deleted
set is a matching and removes at most s crossing instances at S.
Every parallel pair is hit, and no cycle is created by deletion.
For the final simple bipartite graph H,
  |delta_H(S)|>=s+2,                                     (5)
with degrees 23 or 24 and girth>=g.

Equation (5) is stronger than the inequality quoted in C20's main
statement. It is not inferred from the abstract property h(H)>1
alone. It uses the even auxiliary degree, its edge-instance cut
formula and the matching deletion bound.

There is an edge e of H since its minimum degree is at least 23.
Remove one such edge, selecting the least one if a deterministic
family is wanted, and call the result H'. Then
  |delta_H'(S)|>=s+1>s.                                  (6)
This holds for every smaller nonempty shore, because one global
edge deletion removes at most one crossing edge from any cut.
Thus H' stays connected and has no matching cut.

It is simple and bipartite with girth>=g, minimum degree at least
22 and maximum degree at most 24. For n=2N and m=|E(H')|,
  2m<=24n-2.                                             (7)
This exact deficit is what permits a strict density endpoint in C21B.
The argument licenses ONE additional edge deletion, not arbitrary
deletion of a larger edge set.

## A3. Recheck two-connectivity after the additional deletion

More generally, let a simple bipartite graph have minimum degree l>=2,
maximum degree R, and |delta(S)|>|S| for every smaller nonempty shore.
If 2l-1>R, it is 2-connected.

The cut inequality gives connectedness. Suppose x is a cut vertex
and C0 a smallest component of the graph minus x. Then
  |C0|<|V|/2,  |C0|<|delta(C0)|<=R.                       (8)
Put x in the left part. Both parts of C0 are nonempty since its
internal minimum degree is at least l-1>=1. A left vertex of C0
has all its at least l neighbours in C0, so the right part has at
least l vertices. A right vertex loses at most x, so the left part
has at least l-1 vertices. Thus |C0|>=2l-1>R, contrary to (8).
The degree assumptions ensure order at least three. The other part
is symmetric.

For H', use l=22 and R=24. Thus H' is 2-connected, not just
connected and bridgeless. Its minimum degree also ensures a cycle,
so the girth convention for forests is not being used.

## A4. Scope, finite counting dependency and next use

For every g>=3 and any M>=M0 this gives a simple 2-connected bipartite
H' on equal parts of size M^2, with degrees in [22,24], no matching
cut, girth at least g, and the strict edge deficit (7).
Taking M=M0 and fixed d0=24 already gives the negative-root quantifier
pattern with average degree <24. The n>=2, connected and cyclic
witnesses do not exploit small-order or acyclic conventions.

C21B instead chooses a larger even M at the SAME g to meet an
artificial regularization lemma. This use is justified by A1; it
does not silently strengthen C20's stated selector.

The core existence proof still requires the full C20 finite proof:
its without-replacement counts, orientation factor, finite tails,
overlap-pattern catalogue, and edge-instance simplification.
This audit does not replace those proof blocks by new axioms.
No trusted proof or semantic receipt has been supplied.

Review priorities: every occurrence of M in C20.3-C20.5; square
part size rather than arbitrary size; parity in (4); the bound on
deleted crossing instances; the single extra deletion; the renewed
cut-vertex proof rather than preservation assumed automatically.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
next_action: audit this reuse bridge and C21B's exact artificial
regularization, then request the registered verification capabilities.
