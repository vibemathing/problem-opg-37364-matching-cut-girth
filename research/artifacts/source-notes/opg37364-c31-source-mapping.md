# C31 primary-source and formal-statement mapping

Verdict: candidate_only. Fresh HTML retrieval: 2026-09-07.
OPG: https://www.openproblemgarden.org/op/matching_cut_and_girth
Locator: displayed Question and next paragraph, posted November 30, 2011.
The displayed S-subset cut definition does not explicitly forbid empty S.
That omission is not silently repaired or represented as settled author intent.

Version of record: Feghali, Lucke, Paulusma, Ries, Algorithmica 87,
1199-1221 (2025), published May 8, 2025.
https://link.springer.com/article/10.1007/s00453-025-01318-8
Locators: section 1 Our Focus; section 2 valid-colouring clauses 1-3,
Observation 1(i). Only HTML was used, not a PDF.
Bounded exact excerpts:
- "both colours red and blue are used at least once"
- "a forest has infinite girth"
The source SHA-256 in the manifest identifies THIS saved UTF-8 note,
not a whole-page download or unverifiable raw HTTP payload.

Mapping to the new certificate:
- V is the finite vertex set; Adj is symmetric, irreflexive adjacency.
- C is the powerset of V; Col(c,x) means membership, Eqv actual equality.
- The two existential shore witnesses implement clause 3 exactly.
- Valid(c) implements clauses 1-2 by uniqueness of an opposite neighbour.
- The final witnesses are 2-connected, so the source's connected-graph
  colouring equivalence applies. The core is cyclic, so its large girth
  does not depend on the forest convention.
- d0=5 is fixed before forall g; 2m+2<=5n and n>0 imply 2m/n<5.
- The formal certificate proves propagation conditional on core immunity;
  it is not the source's existence theorem and not the root itself.

Section 1.2's prior-art attribution is not used as a proof premise.
The existing C21B construction and source-faithfulness obligation remain
separate from trusted acceptance of this new formal slice.
