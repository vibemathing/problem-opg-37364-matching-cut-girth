# C03: nontrivial prior-art family and faithful quantifiers

Verdict: candidate_only. Kind: proof / statement-faithfulness candidate.
Candidate: candidate:opg37364-nontrivial-source-c03.
Owner: math-proof.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: 0e34fb407a9778818f4d9b509b7ead03d6762e6e.
The frozen contract is not changed. Both admitted obligations remain open.

## External input, attributed and not admitted as an axiom

T14 denotes Lemma 5 of Feghali, Lucke, Paulusma and Ries, Matching Cuts in
Graphs of High Girth and H-Free Graphs, in the pinned arXiv v5 and the
2025 version of record. It supplies, for each integer h>=3, a nonempty
finite connected simple 14-regular bipartite graph H with girth>=h and
no matching cut. A perfect matching is also supplied but is not needed
here. The source's term immune means connected and without a matching cut.

This is a literature theorem used as a named, pending reuse dependency.
The paper is not mirrored. No external theorem is silently added to the
allowed-axiom list. See the source note for exact locators and review gaps.

## C03.1 / claim:opg37364-c03-strict-quantifier

Assuming the faithful reuse of T14, fix d=15 before choosing any h.
For each integer h>=3 choose the graph H from T14. Its average degree
is exactly 14: summing its degrees gives 2|E(H)|=14|V(H)|.
Thus its average degree is strictly less than 15, its girth is at least
h, and it has no MC in the frozen nonempty-shore sense.

This has the required obstruction quantifiers
  exists d>0, forall integer h>=3, exists qualifying H without MC.
Indeed the same argument works for every fixed d>14.
Using d=14 with a 14-regular graph would be an error: 14<14 is false.
No conclusion about smaller d is obtained from regularity alone.

## C03.2 / claim:opg37364-c03-two-connected-family

Every nonempty connected simple r-regular bipartite graph with r>=2 is
2-connected. This is an elementary deduction, not an additional source
theorem required from T14.

Proof. Write the bipartition as X,Y. Suppose x in X is a cut vertex.
For a component C of H-x write a=|C intersect X|, b=|C intersect Y|,
and let t be the number of edges from x to C. Connectedness gives t>0.
Every vertex of C intersect X has all r neighbours in C; hence the
number of internal edges is ra. Counting degrees on C intersect Y
gives rb=ra+t. Thus t=r(b-a) is a positive multiple of r.
The components partition the r edges incident with x. There cannot be
two positive multiples of r summing to r, contradicting that x is a
cut vertex. The case x in Y is symmetric. A simple bipartite r-regular
graph with r>=2 has at least four vertices, so the order requirement
for 2-connectivity also holds.

For r=14 each bipartition class has at least 14 vertices, since neighbours
are distinct, so |V(H)|>=28. Therefore the T14 witnesses also lie in the
2-connected residual class of C02 and are not small-order artefacts.

## C03.3 / claim:opg37364-c03-domain-comparison

The witnesses in C03.1 work both in the literal nonempty-graph domain and
in the explicitly stronger domains n>=2, connected, or 2-connected.
They are not forests, so ambiguity about the girth of an empty graph or
a forest is irrelevant to these particular witnesses. The source's
valid colouring requires both colours, exactly the contract's two
nonempty shores. A perfect matching in H is not asserted to be a cut.

C01's K1/source-convention ambiguity remains separately recorded; this
candidate does not decide the author's unstated small-order convention
or rewrite the canonical contract. It supplies a robust comparison
that does not rely on exploiting that convention.

## Dependency and attack audit

C03.1 depends on T14, the degree-sum identity and 14<15.
C03.2 is finite bipartite degree counting.
C03.3 uses C03.1, C03.2 and the frozen/source definitions.

The NP-hardness theorem is not used as the witness-existence argument,
and no assumption about P versus NP is introduced. The existence of
a perfect matching is not confused with existence of a matching cut.
The graph is allowed to depend on h; d is fixed first. No finite set of
tested girths is substituted for all h. A search result alone is not
treated as verification.

The source proof relies on number-theoretic and expander results. These
dependencies, the construction's simple/connected status, and the exact
statement match still need trusted review or a separately checked encoding.
No mathematical verification command, graph generator or kernel was run.

## Nonterminal checkpoint

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
source_status: attributed prior art; source-faithfulness candidate only.
blockers: pending trusted reuse/semantic review and required verifier
          capabilities; the canonical small-order flag is not erased.
next_action: audit whether replacing global average degree by maximum
             average degree or deleting degree-two vertices is safe,
             using an explicit conditional graph transformation.
