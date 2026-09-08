# C33: parallel two-cycle incidence

Verdict: candidate_only. NONTERMINAL_CHECKPOINT.

Read proof.md first. It gives the complete conventional classification and
finite count; no Lean compilation or root closure is claimed.

Run the portable finite controls from this directory with:

    python -I -S run_bounded.py run-02

The runner creates a NEW directory, imposes wall40s/CPU35s/256MiB/128KiB limits,
and records input/output hashes and actual exit status. run-01 is immutable.
These finite controls do not replace the general proof.

## Optional pinned Lean replay

Use Lean commit 6caaee842e9495688c1567e78c0e68dbb96942aa (4.19.0),
Mathlib commit c44e0c8ee63ca166450922a373c7409c5d26b00b and its pinned
transitive manifest. In a NEW workspace, copy the existing C31 native-lock
CompletionEquiv, CompletionCardinality and ProductCounts modules, the existing
C32 HitCounts and HitProbability modules, then these two R10 modules. Reuse
the C31 pinned lakefile.toml and lean-toolchain there. No frozen repository
source should be edited. Under wall120s/CPU90s/4GiB/256KiB bounds per command,
check lean --githash, all dependency commit heads, compile the dependency
modules in order, build R10.Parallel22 and run R10/AxiomAudit.lean. Save source,
compiler/shared-library digests and each named audit output.

These are replay instructions, not a receipt. The current native-tool probe
found no locked environment; the eleven print-axioms commands were not run.
The T/Q/L/R counting bijections remain a Lean obligation even after the
interface compiles. Do not replace that obligation by the arithmetic identity.

The final Issue checkpoint contains branch/head/PR/check/merge state. The
JSON checkpoint here is a pre-PR snapshot. Source-map digests are not raw
webpage hashes, and the displayed constants are not attributed to a paper.
