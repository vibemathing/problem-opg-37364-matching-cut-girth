# C34 — parallel-two-cycle classification continuation

`NONTERMINAL_CHECKPOINT`; `candidate_only`; `best_verified_result=none`.

**The requested native Lean compilation and the full Lean Witness/index
Equiv chain are NOT complete.** This package is neither a replacement for
C33 nor a root-closure artifact. It must not be described as mechanically
proved merely because the Python atlas succeeds or source files exist.

## New work

- The four-class statement is explicitly restricted to compatible witnesses;
  a general zero-event proof handles incompatible raw Witness values.
- Canonical T/Q/L/R encode/decode maps are fully implemented. An actual run
  exhausts the fixed 24-colour palette and endpoint equality types, checking
  165462 compatible code/witness pairs in both directions. This is a local
  colour atlas, not an enumeration of Omega_N or a probability experiment.
- A direct isolated projection proof retains C33 definitions and avoids
  requiring C32 merely to show a finite surjection. Its declaration has the
  requested name R10.Parallel22.bad22_le_incidence.
- Additional uncompiled Lean source constructs Encodes from compatibility,
  connects it to the original C32 count chain, and gives the actual
  two-input/singleton-target zero-count equivalence. Abstract index-cardinality
  sources are separate from the still-missing Lean canonical Equiv proofs.
- The source lock is Lean4.33.1 commit819816b2e0a3bf405af45ae5c7af2491d8f5bee6
  and Mathlib0df444a360eaa60ab8c11dca51a86af692955474, not the older4.19 lock.

## Files and exact status

`proof.md`: self-contained conventional classification and both inverse maps.
`bijections.py`, `input.json`, `run_atlas.py`, `run-01/`: actual finite atlas,
inputs, outputs and resource/command records. The output's assertion counter
is a program-level comparison counter, not a count of Lean theorems.
`ProjectionOnly.lean`: uncompiled isolated native target, same C33 definitions.
`R10/C34Classification.lean`: uncompiled compatibility/table bridge.
`R10/C34IndexCardinalities.lean`: uncompiled cardinalities of index product types.
`R10/C34AxiomAudit.lean`: fourteen queries, no observed printed axioms.
`source-lock.json`: exact upstream source identities, NOT binary attestation.
`runtime-observation.json`: actual absence/acquisition observations, not a
compiler rejection. No repeated ENOENT child run was manufactured.
`replay_locked.py`: portable bounded native replay, syntax-checked as Python
only; successful native path untested in the preparing runtime.

`ProjectionOnly.lean` intentionally has the same R10.Parallel22 names as the
frozen C33 module. Compile it in its own Lean process. Do NOT import it with
R10.Parallel22. The other new files import the frozen C33 module normally.

## Native replay in a reachable installed environment

Run, using actual local paths as arguments (do not commit them):

```sh
python -S replay_locked.py --repo-root REPOSITORY \
  --mathlib-root PINNED_MATHLIB --lean NATIVE_LEAN --output REPLAY_OUTPUT
```

The driver verifies full native githash, pinned Mathlib/dependency HEADs,
source hashes, and limits. It compiles the isolated projection first, then
frozen C31/C32/C33 dependencies and the new modules, and checks named axiom
outputs. It does not install tools, dispatch Actions, alter registry policy,
or write Evidence/Result. Only the native observed transcript can populate
`compiled_modules`, `actual_axioms` and binary fingerprints.

First uncompiled declaration: R10.Parallel22.bad22_le_incidence.
First still-untranslated formal dependency: the actual canonical Lean Equiv
between compatible C33 Witness values and the disjoint sum of four index
types. The Python bijections and conventional proof do not supply that Lean
proof term. Do not add an axiom or a cardinal-equality hypothesis to conceal it.

Shared-edge, shared-path, mixed vertex-only cases and disjoint-cycle deletion
families remain later catalogue work. Do not add the two-cycle bound to the
whole coarse catalogue bound or assert total<41/800.
