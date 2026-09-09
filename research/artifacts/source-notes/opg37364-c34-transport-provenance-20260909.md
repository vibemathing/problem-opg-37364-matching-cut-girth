# C34 transport provenance and minimal gate repair

verdict: candidate_only. No mathematical closure.

All 26 supplied ZIP members were preserved byte-for-byte in the existing
branch's first commit `b13039c710c63d05a60a5097112eee205f20fa0a`.
ZIP SHA-256: `929347a1a49400238549e7310ca61c14c28ffd17a6d8efcea73e38c2faaae2b3`.
Original 24-file candidate subtree: `7fcf5d513ad1413ccf1b7eda659c521831fdfd96`.
The original provisional packet has blob `b4661ce1f07e33f8dce808e94a525bdc94cd2110`
and SHA-256 `b0fe0fa457a44f7c988af520876b17cff0dfb8194101559d39f104282dfb278b`.
It is retained in that first commit; the live packet binds the actual branch
`web/attempt-opg37364-a01-c34-tqlr-20260909` and PR #34.

## Actual gate diagnosis

At head `29ca70dd1a3732867c02cb8dced4ba27aabe2452`, Actions run
`34302270551` passed web-attempt-packet and web-harness-snapshot. The
web-pr-diff-boundary job `102311512200` rejected the following JSON key:
`runtime-observation.json`: `$.acquisition_attempt.outcome`.
This is a reserved-key transport error, not a mathematical or Lean failure.
No raw runner log, private host path, credential or environment inventory is
copied into this note. The job is the locator for the exact diagnosis.

## Minimal data repair

In `research/artifacts/candidates/opg37364-c34-classification-f9d7956e/runtime-observation.json`,
only the key `outcome` is renamed to `acquisition_status`. The string value
and every other byte are unchanged. Historical absence/acquisition
observations remain historical, not a new execution record.
Original file SHA-256: `e78b79550fbf4157921597de2a8b84c1307f11f0812a4b26426e787498db3576`.
Repaired file SHA-256: `66aa38c9a56d96b251096f75ff6449868251db814af5eb083c1d525e00893784`.
The original is available under the same path in the first commit above.
The candidate manifest and the single live packet update these digests.
No Lean source, Python checker, old output, conventional proof, C31-C33
artifact, truth record, schema, Harness, workflow or verifier is modified.

## Native and mathematical boundary

All C34 Lean declarations remain uncompiled at this transport repair.
The historical 165462 compatible code checks are Python comparisons, not
Lean proofs or new executions. The actual Lean equivalence from compatible
C33 Witness values to TIndex + QIndex + LIndex + RIndex remains missing.
Abstract index cardinalities are not a substitute. Scope stays the Bad22
candidate constant only; no addition to the coarse catalogue, total bound,
root theorem, independent replay or trusted closure is claimed.
