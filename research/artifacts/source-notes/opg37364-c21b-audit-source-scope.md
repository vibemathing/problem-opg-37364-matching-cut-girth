# C21B audit: G statement-faithfulness and source scope

Verdict: candidate_only. Retrieval: 2026-09-07, HTML only.
Target: obligation:opg37364-root. This is a source comparison, not a
trusted semantic receipt, and it adds no external existence premise.

Primary sources:

1. Open Problem Garden, "Matching cut and girth", posted 2011-11-30.
   https://www.openproblemgarden.org/op/matching_cut_and_girth
   Relevant locations: Question and the following defining paragraph.
2. Carl Feghali, Felicia Lucke, Daniel Paulusma and Bernard Ries,
   Matching Cuts in Graphs of High Girth and H-Free Graphs,
   Algorithmica 87 (2025), 1199-1221; version of record 2025-05-08.
   https://link.springer.com/article/10.1007/s00453-025-01318-8
   Relevant locations: introduction, Section 1.2, Section 2 and Observation 1.

Source observations (bounded paraphrase): the OPG question uses average
degree smaller than the parameter, and a lower bound on girth. Its cut
uses every crossing edge, but the displayed subset notation does not
explicitly exclude the empty set. The journal paper restricts its graph
objects to finite simple undirected graphs, works with connected graphs
for the colouring formulation, requires both colours to occur, and
equates that formulation to matching cuts. It assigns infinite girth
to forests and reports a negative answer to the OPG question.

Map to the frozen theorem: two nonempty shores are EXPLICIT in the
ProblemContract and the audited theorem. An empty-shore reading of the
raw OPG notation would instead make every graph trivially decomposable;
that different reading is not silently equated to this theorem. The
constructed witnesses are connected, 2-connected and cyclic, of positive
order. Their nontrivial boundaries are nonempty. Thus their validity is
unaffected by excluding order one, restricting to connected graphs,
requiring nonempty crossing sets, or conventions for forests. No average
is assigned to an empty graph.

The proof's fixed d0=5 and every integer g>=3 map directly to the frozen
negation. Neither an NP-hardness assumption nor a published expander
existence theorem is used in the elementary proof. No novelty is claimed.
A trusted statement-faithfulness review is still required for admission.

## Execution-scope note

The user explicitly requested actual bounded local checks. They were run
in the available local Python runtime, not by a GitHub command capability
and not under a registered verifier identity. The GitHub profile's
command_execution=false was not edited. No fixture verifier's scope was
extended. Two run records retain exact input/code/output hashes and limits.
The first checker used an insufficient finite infinity sentinel in some
small forest controls; the final version repairs that test-coverage issue.
A reverse patch reconstructs the first executed source exactly. No
candidate theorem was altered to conceal a failed test.
