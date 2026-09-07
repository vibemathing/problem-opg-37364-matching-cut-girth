# C21B second exact audit and admission request

Verdict: candidate_only. All original archive bytes remain on main; this
is a separate checker/report, not a replacement or a mathematical receipt.
The primary proof is the fixed original proof referenced by report.md.

Run only in a fresh copy to preserve the recorded observations:

    python3 -S runner.py
    cd pairings && python3 -S runner.py

CPython3.13.5 standard library was used. The runner applies resource limits
before process creation; the checker inherits them. The initial non--S
runner failed to create a process under the memory limit; startup-failure.json
records the sanitized failure. The same runner/checker then succeeded with
-S, without raising limits. Do not overwrite the archived execution records
when replaying. The supplemental checker binds its parent checker digest.

output.json contains the sixteen explicit mutation results; checker.py
contains their finite witnesses and predicates. pairings covers all four
cycle classes nonvacuously. The quoted source extracts and source comparison
are persisted separately under research/artifacts/source-notes/.

No Lean/SMT or registered verifier was run. admission-request.json is a
request, not an executable Lean request or accepted gate verdict. It freezes
the exact missing prerequisites found in the current gate source. All
claims remain candidates and both admitted obligations remain open.
