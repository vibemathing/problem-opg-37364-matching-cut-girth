# C31: general no-cut propagation and quantifier proof certificates

Verdict: candidate_only. This is a NONTERMINAL_CHECKPOINT.
Repository: vibemathing/problem-opg-37364-matching-cut-girth.
Base: 7754aecc74e74f35f535880693282be3bc26d0d0.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root.

This package supplies new general proof terms, not another admission request
and not a retransmission of PR29/PR30. It reuses the previously initialized
C31 branch. The earlier C31 checkpoint reported staged Lean/SMT work, but a
fresh ref read showed that branch still at the base with no new commit.
The reported earlier SMT source/output bytes were not available among the
mounted attachments or that branch. Their hashes are not treated as actual
inputs or execution records here. The present files and measured runs are new.

## New general slice

`no-cut-extension.nd.json` is a closed 252-node classical first-order proof.
It derives immunity of the whole graph from a nonempty immune old core and
the condition that every vertex is old or has two distinct old neighbours.
Both shores are explicitly required to be nonempty. It quantifies over
arbitrary vertex and colouring sorts, not graphs up to a tested order.

`quantifier-bridge.nd.json` is a separate 26-node proof that a fixed-density
family of admissible graphs without matching cuts contradicts the positive
root quantifiers. Existence of that family remains an explicit premise.
`core-extension.nd.json` is the 178-node monochromatic-core intermediate proof.

The small replay checker has only logical introduction/elimination rules,
eigenvariable/sort/capture checks, and classical double-negation elimination.
It contains no graph-existence rule, theorem-specific oracle, solver answer,
or caller-supplied axiom mechanism. It is nevertheless new, generator-owned,
unregistered code, not a trusted repository verifier. Its implementation and
the semantic instantiation require external review.

## Native Lean boundary

Three complete proof-term exports were generated locally with target
leanprover/lean4:v4.19.0; only QuantifierBridge.lean is included in this
partial commit, in a dependency-free Lake project. No native Lean/elan/lake was found, and
bounded retrieval attempts did not supply the runtime. Native compilation
and printed-axiom results are absent. The files are candidates, not a claim
that Lean compiled them. `Classical.byContradiction` is explicit in the
exports; the actual Lean axiom list must be obtained from native replay.

## Reproduction

From this directory, use CPython 3.13.5:

    python -S run_bounded.py replay
    python -S run_bounded.py separate
    python -S run_bounded.py algebra

The runner enforces 40s wall, 35s CPU, 256 MiB address space, 64 KiB per
stream, 128 KiB combined output and thread environment 1. Execution records
bind the interpreter binary, inputs, runner and bounded raw outputs.
Exploratory outputs are explicitly separated because their full input
fingerprints were not captured at execution and their memory was not
separately limited. Do not treat them as frozen bounded receipts.

The builders regenerate the certificates/Lean text; replay imports neither
builder nor an earlier checker. The separate finite audit imports no earlier
checker. Its permanent/closed-walk implementation is different source code,
not a new verifier trust domain.

First uncompiled declaration: R10.core_extension (then the complete
R10.no_matching_cut_extension and the quantifier bridge).
First unformalized combinatorial dependency: the complement-bijection proof
that k compatible prescribed permutation pairs have exactly (N-k)! extensions.
Next: actual pinned Lean elaboration/axiom audit, then that cardinality lemma
and the general overlapping-cycle catalogue. No full root closure is claimed.

## Platform transport interruption

The write call containing `CoreExtension.lean` and `NoCutExtension.lean`
was blocked because the platform could not determine its safety state;
an unchanged retry was also blocked. Those two local exports and their
three constructor scripts are NOT included in this commit.
`pending-files.json` records their actual byte hashes and precise disposition.
The ND certificates are self-contained inputs and can be replayed without
these constructors. The included `lakefile.toml` targets only the separately
persisted `QuantifierBridge.lean`; it does not claim a native E build.
The three Python replay commands above remain available in this partial
commit. Regenerating the certificates/exports from the held constructor
scripts is not available here. Native Lean was never executed.
The full original local sources are retained, not silently deleted or
represented as already transported.
