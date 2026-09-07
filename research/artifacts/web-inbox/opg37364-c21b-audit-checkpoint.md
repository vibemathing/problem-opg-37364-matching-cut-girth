# C21B A-G proof audit checkpoint

Verdict: candidate_only.
Research status: RESULT_CANDIDATE_READY / full-refutation-proof-drafted.
Frozen main: 1735793e9f60d9d003e8948b350cfc09efd8a7ea.
Issue: #3; initial audit comment 5565212102.
Branch: web/attempt-opg37364-a01-c21b-audit-20260907.
Packet: research/artifacts/web-inbox/opg37364-a01-c21b-audit-20260907.json.

A-G have complete conventional proof-draft arguments in the main audit
file. No fatal gap in the frozen theorem was identified. The draft
expands the finite seed argument; it does not turn earlier candidates
into axioms. G distinguishes raw source shorthand from the explicitly
frozen nonempty-shore convention. All trusted obligations remain open.

| Block | Proof-draft status | Bounded checks |
|---|---|---|
| A | Complete: finite shore counts, recurrence induction, strict tails | N<=6 coefficients; q<=24 recurrence; N=2 weighted full count |
| B | Complete: catalogue coverage includes edge instances and shared paths | 988 extension counts; 3036 overlapping-cycle union checks |
| C | Complete: matching deletion, parity margin, spare edge, two-connectivity | 360 deletion collections and a positive 16-vertex control |
| D | Complete: maximum-cardinality switch, parity, current distance, u=v | 8913 local exchanges; both pairings; full N=52 numeric control |
| E | Complete: retained core and two colour cases | 1024 subdivision controls, 16 no-cut core cases |
| F | Complete: fixed d0=5 and k=38, integer deficit, explicit order | Strict endpoint mutation; 48 parameter controls |
| G | Complete explicit map for the frozen theorem, not trusted acceptance | K1/empty crossing controls; primary-source comparison |

Final local execution: CPython3.13.5, standard library, exit0,
127643 assertions, no timeout, empty stderr. Limits: wall45seconds,
CPU40seconds, address space536870912bytes, each output65536bytes.
This is finite generator checking, not a trusted verifier or proof kernel.
The first run's coverage defect is explicitly retained with a reverse
patch to reconstruct its exact source; it is not a C21B lemma failure.

best_verified_result: none.
best_verified_candidate: none in the trusted mathematical-verifier sense.
best_proof_draft: candidate:opg37364-c21b-ag-audit-20260907.
first_open_mathematical_gap_in_frozen_draft: none identified by this audit.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
failed_routes: no new candidate-theorem failure; existing ledger unchanged.
next_obligation: trusted formal check of the finite A/B catalogue and
edge-instance/simple-graph bridge, then D-F composition and G semantic
acceptance. No additional axiom or fixture-policy extension is licensed.

The file records prepared candidate state before PR creation. The live
packet receives the actual PR binding, and the final Issue comment records
actual checks/head/merge. Neither this file nor any CI success closes
repository mathematics.

## Frozen companion file hashes

`research/artifacts/candidates/opg37364-c21b-ag-audit-proof.md`

    fb654e9b15064842648e59a80da48a334515e9ff1677096072a39d078dbe307a

`research/artifacts/candidates/opg37364-c21b-audit-checker.py`

    f203a11c2a1734bd4fde50c8d34c5fb4170c85056281aae0c13c5b29d010d3f5

`research/artifacts/candidates/opg37364-c21b-audit-execution.json`

    d1ccf78bfa0f059f33b3bdadfc08aec579a2584ae164423395e15a3080a308b6

`research/artifacts/candidates/opg37364-c21b-audit-input.json`

    71debf99a59e57823f959c9eb71313073fa90fdad564c8fec902e211b8abd1bf

`research/artifacts/candidates/opg37364-c21b-audit-output.json`

    e51abd80ce6dd1d4100b8a4f4d41f68f8576d4870b11da10f429d81812f539d7

`research/artifacts/candidates/opg37364-c21b-audit-runner.py`

    9a26a947909dce518683ea9baf457d3031c41f15fac946b03836387babcf10c7

`research/artifacts/candidates/opg37364-c21b-audit-stderr.txt`

    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

`research/artifacts/candidates/opg37364-c21b-audit-v1-execution.json`

    662daca24a353204eb7021e73f4a707237d17df68f76d5fc2b0b65c38ce7ff57

`research/artifacts/candidates/opg37364-c21b-audit-v1-output.json`

    4252488a55ebeef1fd18f91073437d842bda308e5eede3a31b5db5a42c37ce14

`research/artifacts/source-notes/opg37364-c21b-audit-source-scope.md`

    92a5371e827efcaebaf39ea62950fb497e0ed569398688b350f198218795f13c

`research/artifacts/source-notes/opg37364-c21b-audit-v1-from-v2.patch`

    e63430252558af6c8c0aabdf6a40a3235e0c0887e979aa6a058b82b1018f529c

