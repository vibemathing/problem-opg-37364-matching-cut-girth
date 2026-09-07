# C31 native-build continuation

Verdict: candidate_only. State: NONTERMINAL_CHECKPOINT.
Problem: problem:opg-37364-matching-cut-girth.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1. Target: obligation:opg37364-root.
Read main: 7754aecc74e74f35f535880693282be3bc26d0d0.

## Exact objective, not accomplished by a source file

The first native obligation is that k compatible distinct prescribed pairs
between N-element sets admit exactly (N-k)! bijection completions. The
source expresses a partial bijection e between two subtypes. Its completion
is a total equivalence agreeing with e. No nonempty-complement assumption
is added. A later source theorem specializes the subtype cardinality to k.
The full d0=5 graph-family statement is unchanged and is not proved here.

This continuation did NOT obtain a Lean executable and did NOT compile any
module. It resolved the actual source revisions, checked the exact-version
API signatures, preserved the recovered Lean sources, and ran a native
build driver that failed before starting the compiler. No additional Z3,
finite checker, custom logical kernel, admission request, or substitute for
native compilation was added.

## Resolved immutable dependencies

Official refs/tags/v4.19.0 resolve directly to commits:
- Lean: 6caaee842e9495688c1567e78c0e68dbb96942aa.
- Mathlib: c44e0c8ee63ca166450922a373c7409c5d26b00b.

The Mathlib manifest at that commit supplies eight exact downstream commits,
all saved in resolved-source-lock.json. lakefile.toml now uses the full
Mathlib commit rather than a mutable tag. This is a resolved SOURCE lock,
not an acquired dependency tree or a measured native toolchain fingerprint.
The original lean-toolchain bytes remain leanprover/lean4:v4.19.0; the
build driver checks the actual version/commit prefix before accepting it.

Official immutable files checked:
Mathlib/Data/Fintype/Perm.lean: card_equiv takes an equivalence and gives the
factorial of the domain cardinality, with the requisite Fintype/DecidableEq
instances. It is not the cardinality-equality argument of equivOfCardEq.
Mathlib/Data/Fintype/BigOperators.lean: card_pi counts dependent functions;
card_pi_const takes a codomain type and n and specializes the domain to Fin n.
Mathlib/Data/Fintype/Card.lean: card_subtype_compl applies to subtype and
complement Fintype instances, with no nonempty assumption. The surjective
projection inequality has codomain cardinality <= domain cardinality.

These checks support the intended API uses; they are not elaborator results.
No false original mathematical lemma or actual Lean type error was found.

## Actual runtime result

compile_pinned.py attempted [lake, env, lean, --version]. Process creation
failed with errno=2. The driver exited 2; the nonexistent compiler has no
exit code. Current lookup found no lean, lake or elan. compiled_modules is
empty. actual_toolchain_fingerprint, actual_axioms and trusted_gate_verdict
remain null. native-build-attempt.json binds this observation to the actual
source, source lock and driver SHA-256 values.

Per-command enforced budgets in the driver: wall120s, CPU90s, address space
2GiB, combined stdout/stderr128KiB; thread environment1. No compiler consumed
those budgets because its process did not start. The Python driver itself
was run under a ten-second outer tool timeout and used CPython3.13.5.
The literal escape-token scan returned empty; this is not an axiom audit.

Current native network access failed name resolution. Separate download
attempts for the official Linux tar.zst, Linux zip and source tarball
returned download failure and produced no usable runtime. The plugin search
found no applicable Lean compiler service. These are acquisition failures,
not failures of the combinatorial theorem. No workflow was edited and no
transport job was repurposed as a compiler.

## Recovery scope

All 46 members of the supplied recovery ZIP were read and hashed. Five Lean
files and lean-toolchain are copied byte-for-byte to this capsule. The Lake
configuration differs only in the Mathlib rev. recovery-inventory.json
lists every original path/hash and distinguishes the six byte-identical
copies from the remaining original members; it does not claim those other
historical programs/outputs are transported or freshly rerun here.

This native capsule is separate from the existing C31 ND-certificate packet
already present on the branch. The packet is extended in the same PR; no
second packet is added. PR29/30 and their artifacts remain untouched. The
five previously held files in the existing branch's pending-files.json are
not included, reconstructed, or resubmitted by this capsule.

## First unresolved native declaration and next action

First uncompiled lemma: R10.Cardinality.preservesRegion.
First unclosed native combinatorial result: R10.Cardinality.card_fin_completion.
R10.CompletionEquiv, then R10.CompletionCardinality, then R10.ProductCounts
must be built in the resolved environment. Run the existing AxiomAudit.lean
only after these succeed; it prints nine relevant theorem axiom reports.
The driver can be run as python -S compile_pinned.py --resolve in a Linux
environment with Lean4.19.0/Lake and authorized dependency access. It stops
on any dependency mismatch, compiler error or incomplete axiom output.

A/B's hit-set count, without-replacement bound, 24-coordinate product,
parallel-edge/shared-path pattern catalogue, and the <41/800 bound are NOT
claimed mechanically derived. They remain subsequent native obligations,
not finite-test conclusions. Trusted statement-faithfulness and root closure
remain absent; no truth ledger or verifier authorization is altered.

best_verified_candidate: none.
best_verified_result: none.
trusted_verified_scope: [].
open_obligations: obligation:opg37364-contract-edge-cases; obligation:opg37364-root.
