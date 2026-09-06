# Source note C01: graph domain and cut conventions

Status: candidate_only; target obligation:opg37364-contract-edge-cases.
Retrieval date: 2026-09-06. Contract unchanged at
f0df824cb29a0a68ea860d76a2b0668d3900fac2.

## Locators and bounded comparison

S0. The contract's upstream locator is
https://www.unsolvedmath.com/problems/OPG-37364 .
The Web open returned an internal error, not usable page contents. No claim
about that page's exact wording or implicit domain is made.

S1. Open Problem Garden, Matching cut and girth, posted 2011-11-30:
https://www.openproblemgarden.org/op/matching_cut_and_girth .
The question uses the same density/girth quantifier pattern. Its definition
displays S subset V and M=E(S:V\S), without an explicit nonempty-S condition
or order bound in the displayed paragraph. This does not demonstrate that
the author intended to allow an empty shore or intended to exclude K1.
The contract explicitly requires a nontrivial partition; the missing source
conventions must not be guessed. Relation: unknown at these boundary cases.

S2. C. Feghali, F. Lucke, D. Paulusma, B. Ries,
Matching Cuts in Graphs of High Girth and H-Free Graphs,
arXiv:2212.12317v5 (2023-11-07):
https://arxiv.org/html/2212.12317v5 .
Section 2 uses finite simple graphs, connected inputs for matching-cut
colourings, and both colours at least once. This supports the nonempty-shore
interpretation on connected graphs. Connectedness does not itself remove K1.
Section 1.2 explicitly discusses the OPG question. Relation: exact cut
semantics on connected graphs; not a justification for editing the domain.

S3. Version of record:
https://doi.org/10.1007/s00453-025-01318-8 ,
Algorithmica 87, 1199-1221 (2025), published 2025-05-08, CC BY 4.0:
https://creativecommons.org/licenses/by/4.0/ .
The same authors' Lemma 5 states existence of 14-regular bipartite graphs
without matching cuts at every requested girth. This is a prior-art lead
requiring an explicit scope/dependency audit, not new work by this agent.
The pinned arXiv PDF pages 4, 6 and 7 were visually checked against the HTML:
https://arxiv.org/pdf/2212.12317v5 .
No paper is mirrored.

## Semantic decision requiring trusted review

The literal n>=1/nonempty-shores contract has the K1 obstruction shown in
C01. Adding n>=2 is a different statement; merely adding connectedness is
insufficient. Allowing empty shores gives a different, trivial property.
The n=0 average-degree domain is undefined, not zero.
Flag ambiguous_problem_contract. Preserve all three distinctions and retain
both admitted obligations as open. Subsequent candidates may compare
existing theorems or prove conditional reductions, but cannot admit a Result.
