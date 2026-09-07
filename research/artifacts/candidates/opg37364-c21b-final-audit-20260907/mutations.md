# Sixteen executed negative controls

Verdict: candidate_only. These are incorrect variants, not counterexamples
to the original C21B hypotheses. Exact witnesses and checks are in
checker.py; raw bounded results are in output.json.

01. Within-coordinate replacement rather than without-replacement probability.
02. Tuple-shore incidences equated with bad-tuple union.
03. Parallel two-cycles omitted.
04. Shared paths or edges omitted from overlap cover.
05. Deletion not a matching.
06. Initial-H distances substituted for current-J distances.
07. Odd kN admitted for exact regularity.
08. Coincident deficit centres forbidden.
09. Cycles using only one new edge ignored.
10. Opposite-coloured new vertex on monochromatic core accepted.
11. Strict average <5 replaced by <=5.
12. Parallel edge instances collapsed to one neighbour.
13. Original core edge subdivided twice.
14. Empty shore admitted.
15. Two disjoint common edges counted as a path.
16. New vertex given only one old neighbour.

All sixteen conditions were detected in the recorded successful run.
The weak-five example is an arithmetic boundary, not a claimed high-girth
graph. K2,3 and K3,3 are synthetic graph controls. M15 explicitly prevents
repeating the previous shared-edge/shared-path label error.
