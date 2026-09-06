# C15 source and statement-faithfulness audit

Verdict: candidate_only. Target: obligation:opg37364-root.
Retrieval date: 2026-09-06. No full source is mirrored.

## Primary source actually read

Carl Feghali, Felicia Lucke, Daniel Paulusma and Bernard Ries,
Matching Cuts in Graphs of High Girth and H-Free Graphs,
Algorithmica 87, 1199-1221 (2025), published 8 May 2025.
DOI: https://doi.org/10.1007/s00453-025-01318-8
Official HTML: https://link.springer.com/article/10.1007/s00453-025-01318-8

The official HTML's Section 1.2 explicitly identifies the OPG question
and a negative answer. Section 2 specifies finite simple undirected
graphs and valid two-colourings using both colours. Section 3 defines
edge expansion; Observation 2 relates expansion to forbidden cuts.
Theorem 3 and Lemma 4 give the prime progression. The proof of Lemma 5
states the exact LPS degree, adjacency-eigenvalue and girth bounds
used in C15. No NP-hardness assumption is needed for witness existence.
The journal version is open access under CC BY 4.0.

## Underlying theorem and access boundary

A. Lubotzky, R. Phillips and P. Sarnak, Ramanujan graphs,
Combinatorica 8, 261-277 (1988).
DOI: https://doi.org/10.1007/BF02126799

The publisher abstract corroborates an explicit regular Cayley
construction, Ramanujan eigenvalue bounds and large girth.
The attempted original PDF route redirected to the article/abstract;
the full original proof was not inspected in this continuation.
The exact p,q specialization is taken from the 2025 authors' proof,
not asserted to have been checked against an unread original PDF.

Dirichlet's progression theorem and quadratic reciprocity remain
separately named mathematical dependencies. In particular, the
Legendre-symbol orientation is explicitly bridged in C15 rather
than silently swapping (q/13) and (13/q).

## Relation to the frozen contract

Original OPG locator:
https://www.openproblemgarden.org/op/matching_cut_and_girth
Frozen mirror locator:
https://www.unsolvedmath.com/problems/OPG-37364

C01 and C07 retain the separate ambiguity about omitted small-order
conventions. The C15 witnesses have minimum degree 12 and are connected,
so excluding K1, requiring connectedness, or restricting to nonforests
does not avoid these witnesses. No missing source convention is guessed.

The source provides the 14-regular spectral input. The all-cut proof,
deletion robustness, second perfect matching, 12-regular reduction and
integer-PSD deterministic selector are explicit candidate deductions.
They are not quotations, and no originality or optimality is claimed.
The selector is computable but not claimed efficient or executed.

Required review separates source identity, theorem correctness, finite
linear algebra, graph/cut semantics and fixed-d/forall-g quantifiers.
Publication and a correct-looking citation are not a repository
EvidenceLink or trusted Result. Both admitted obligations stay open.
