# C08: nonempty-shore Boolean encoding and boundary proof objects

Verdict: candidate_only. Owner: math-proof.
Candidate: candidate:opg37364-boolean-faithfulness-c08.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: ed1b090020fef321742e6bb538807793b8f995ce.

This package is a candidate proof of encoding faithfulness, together
with manually composed finite proof objects. No solver, enumerator,
proof assistant or proof-object checker was executed. The certificate
file is not a verifier receipt. Both admitted obligations remain open.

## C08.1 / claim:opg37364-c08-boolean-equivalence

Let G be a finite simple graph on vertices 1,...,n with n>=1.
For each vertex v introduce a Boolean variable x_v. Use the clauses
  OR_{v=1}^n x_v,           OR_{v=1}^n NOT x_v.             (N)
For each v and each unordered pair of distinct neighbours u,w use
  (NOT x_v OR x_u OR x_w),
  (x_v OR NOT x_u OR NOT x_w).                             (L)

The conjunction F(G) is satisfiable if and only if G has an MC under
the frozen convention: two nonempty shores, with crossing edges a
possibly empty matching.

Proof. Clauses (N) say both Boolean values occur. For any neighbour
pair, (L) excludes exactly the two assignments in which the centre
v differs from both neighbours. Therefore (L), for all pairs, says
each vertex has at most one neighbour of the other colour. An edge
set in a simple graph is a matching exactly when each vertex is
incident with at most one of its edges. Set A={v:x_v=false} and
B={v:x_v=true}; these observations prove both directions. No additional
crossing-edge existence condition is imposed or needed.

The number of clauses is 2+2*sum_v binom(deg(v),2), including clauses
that might coincide. Every clause has at most three literals except
the two nonempty-shore clauses.

Adding the unit clause NOT x_1 preserves satisfiability: complement
all variables of any satisfying assignment with x_1=true. The
nonempty-shore clauses are interchanged and the local clause pairs
are interchanged. This justification uses n>=1. It is a symmetry
reduction, not an assumption that a specific shore was nonempty
before (N) was imposed.

## C08.2 / claim:opg37364-c08-boundary-proof-objects

The accompanying JSON uses integers as literals: i means x_i and
-i means NOT x_i. Clauses are sets, displayed as lists. Each resolution
step names two earlier clauses and a positive pivot p occurring
positively in one and negatively in the other; remove those pivot
literals and take the union of the remaining literals. The displayed
child is exactly that resolvent. The terminal empty clause represents
a contradiction. This format is a proposed proof object, not a
registered checker format or an admission record.

For K1, the two clauses are [1] and [-1]. Their resolvent on pivot 1
is empty. This is a complete two-clause propositional argument.

For K(2,3), vertices 1,2 are the size-two part and 3,4,5 the other
part. The JSON lists both nonempty-shore clauses, all 18 local clauses,
and the symmetry unit [-1]. Lines 22-24 give the three pairwise
negative clauses on the leaves. Lines 25-30 derive [-2]. Lines 31-36
then derive [-3], [-4], [-5]. Lines 37-41 resolve those units and
[-1],[-2] against the positive nonempty-shore clause to obtain the
empty clause. The proof of symmetry preservation in C08.1 is essential
to transfer this contradiction to F(G) without its symmetry unit.

The same JSON supplies explicit two-colour assignments and crossing
edge sets for the edgeless order-two graph, K2, a three-vertex path,
and C4. In each, both colours occur and the listed crossing edges have
no common endpoint. These are proposed positive witnesses, not
reported results from a witness checker.

These finite proof objects do not enumerate the residual class from
C07 and make no assertion about unlisted graphs.

## C08.3 / claim:opg37364-c08-admissibility-separation

The cut formula does not encode average degree or girth. Those are
separate witness-admissibility obligations. For n>=1 and rational
d=p/q with p,q positive integers, the frozen strict inequality is
  2*m*q < p*n,
not <=. No division or floating-point rounding is required.

Thus K2 does not satisfy average degree <1, C3 does not satisfy
average degree <2, and K(2,3) does not satisfy average degree <12/5.
K(2,3) does satisfy average degree <5/2: 2*6*2=24<25=5*5.

For a forest, a verifier must confirm acyclicity and then apply the
contract's girth=+infinity convention. The empty graph is not assigned
an average degree: the frozen expression is undefined at n=0.

For K1 the admissibility argument is symbolic and uniform:
m=0,n=1 imply average degree 0<d for every real d>0; acyclicity gives
girth +infinity>=g for every integer g>=3. C08.2 rules out a cut.
This is a literal counterexample candidate under the frozen small-order
domain, not a claim that finite testing covers real parameters.
The source-domain question from C01/C06/C07 is still nonterminal;
this package does not silently replace n>=1 by n>=2 in the root.

## C08.4 / claim:opg37364-c08-failed-encodings

If (N) is omitted, the all-false assignment satisfies every local
clause for every graph. In particular, the resulting formula is
satisfiable for K1 even though K1 has no MC. This is an exact
faithfulness failure, not a solver-performance issue.

Conversely, requiring a nonempty crossing set rejects the edgeless
order-two graph, whose two singleton shores are a valid MC under
this contract. The symmetry unit alone cannot replace (N).
Admissibility conditions must not be inferred from cut satisfiability.

## Verification request and finite scope

Inputs are this proof, the frozen contract, and
research/artifacts/candidates/opg37364-c08-boundary-certificates.json.
A future authorized checker should independently reconstruct the local
clauses from each edge list, compare them with the supplied inputs,
check each signed-literal resolution step, and validate the four
positive assignments and claimed crossing sets. Reconstruction and
checking the proof must remain separate to catch encoding errors.

Suggested bounded check: the six supplied cases only, at most five
vertices, one thread, five-second timeout, 128 MiB memory, 64 KiB
output. Record the actual checker identity/version, frozen input
digests, limits, exit status, output digest and limitations if run.
No such runtime observation is present in this package.

The proof uses finite-graph basics, Boolean case analysis, finite
combinatorics and real/integer arithmetic. It does not depend on T3,
TABC, T14 or any newly admitted axiom. Repository CI and hashes only
validate transport and byte identity.

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
current_blocker: nonterminal source-domain ambiguity and pending
                 encoding-faithfulness / mathematical verification.
next_action: audit the finite proof objects with an authorized checker;
             continue elementary attacks on the odd-order residual
             without mistaking necessary conditions for a witness.
