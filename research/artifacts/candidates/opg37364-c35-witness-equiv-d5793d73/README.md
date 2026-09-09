# C35: actual admissible Witness to four index types — uncompiled successor

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Problem: problem:opg-37364-matching-cut-girth.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-root (only its Bad22 auxiliary count slice).
Base: d5793d73b99a64c1ee6452495660ab8f74efd216.

## What this successor actually adds

C34 supplied compatibility, normalizedTable/Encodes, the conventional
T/Q/L/R proof and abstract index cardinalities. It did NOT supply the actual
Lean equivalence from its graph-defined Witness subtype to those indices.
C35 now supplies candidate source for that equivalence and its inverse
laws. No Lean declaration in this capsule has been compiled here.

The chain is:

1. C33 Witness is a two-element FINSET of distinct cycles sharing a vertex.
   C34 Admissible enforces that sharing a permutation colour forces both
   endpoints to agree. Inadmissible witnesses realize no permutation tuple.
2. C35 uses a lexicographic orientation (left endpoint, right endpoint,
   binary colour-set mask). `forgetOrder` maps a genuinely ordered witness
   to the original finset. `forgetOrder_injective` handles the two possible
   orders of a two-element finset, and rules out the swapped order by
   asymmetry. `forgetOrder_surjective` uses `Finset.card_eq_two` and totality.
   This is an arbitrary-N argument, including empty endpoint types.
3. `encodeNormal` and `decodeNormal` construct explicit T/Q/L/R normal forms
   and ordered graph witnesses. Their candidate inverse proofs are
   `decode_encode` and `encode_decode`; no cardinality hypothesis is passed.
   Same endpoints split by colour disjointness. Different endpoints force
   colour disjointness by C34 compatibility.
4. Increasing endpoint pairs are explicitly equivalent to C34 `Choose N 2`.
   For colours, a two-set is identified with `Choose 24 2`; fixed finite
   source proofs propose mask injectivity and the three cardinalities
   6072, 31878, 63756 using Lean `decide`. These are unexecuted Lean
   obligations, NOT the old Python enumeration or an external certificate.
5. The colour cardinalities construct equivalences to the exact C34 rank
   index TYPES via `Fintype.equivOfCardEq`. Product and sum equivalences give

   {w : C33 Witness // C34.Admissible w}
       ≃ TIndex N ⊕ (QIndex N ⊕ (LIndex N ⊕ RIndex N)).

   `witness_index_left_inv` and `witness_index_right_inv` use that actual
   Equiv. All still require native elaboration and axiom auditing.
6. `incidenceAdmissibleEquiv` preserves full (tuple,witness) incidence,
   eliminating only zero-event inadmissible witnesses. `rank_event_count`
   invokes the constructed C34 normalized table, then the C33 exact event
   theorem, then C32 card_hit/card_hit_tuple24. It does not multiply slots
   inside one permutation or use a class-count assumption as an oracle.

## Intermediate encoding semantics

The T/Q/L/R TAG and endpoint coordinates are preserved. The final colour
reindexing is selected by proved finite cardinality, not by C34's old Python
canonical marker decoder. A marker of the final index must be interpreted
through `witnessIndexEquiv.symm`, never through that old decoder. This
difference is explicit: the index TYPE and cardinality agree, but the maps
are not asserted to agree pointwise. The intermediate choice does not
change the original Witness relation or the Bad22 event.

This layer counts graph-witness encodings, not two independent samples.
Shared-edge requirements are set-unioned by C33 and normalized by C34.
Conflicting left forks impose two outputs on one input; conflicting right
forks use a real Fin 2 input embedding and C32's b=1<k=2 zero count.
Duplicate occurrences of a shared edge do not create a second constraint.
The full coordinate event remains a product of 24 permutations, not an
independent product of input slots.

## Exact verification scope

Observed here: a bounded Python tool-discovery and source-token probe.
It found no Lean/lake/elan on PATH. No native compiler was started.
The 4 new Lean source token scans returned empty escape lists, but token
scanning does NOT prove an axiom audit or statement faithfulness.
No mathematical Python checker, Z3 query, or old 165462 atlas replay was
run in this successor. The historical atlas is not imported by any Lean file.

Actual probe command, from this capsule:
    python -S replay_c35.py --probe-only --output probe

Probe driver exit: 0, meaning discovery completed, not theorem success.
The exact process limits, timestamp, input/output hashes, and 81-byte
stdout are in probe/process.json and probe/execution.json. No compiler
exit code, axiom list, binary fingerprint, or trusted verdict is available.

The four `decide` declarations are pending native proof reductions.
The configured 8192 recursion depth and 4000000 heartbeats are intended
bounds, not consumed budgets or demonstrated performance. The finite
domain consists of 276 colour-pairs and their product, rather than the
full powerset of all colour-pairs. Reduction cost may still be too high.
A timeout is a replay gap, not a mathematical contradiction.

## Locked native replay

Input lock:
- Lean 4.33.1 commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6.
- Mathlib 0df444a360eaa60ab8c11dca51a86af692955474.
- Exact prior C31-C34 source SHA-256 listed in input-lock.json.
- No prior repository file is copied into the PR or modified.
- Exact dependency heads are read from the pinned Mathlib manifest by
  the original frozen C34 replay driver.

In an already installed environment, supply real paths:

    python -S replay_c35.py \
      --repo-root "$REPOSITORY_ROOT" \
      --mathlib-root "$PINNED_MATHLIB_ROOT" \
      --lean "$PINNED_LEAN_EXECUTABLE" \
      --output native-replay

The driver verifies hashes before importing the original C34 bounded
runner. It first replays the isolated projection and all C31-C34
dependencies, stopping at the FIRST native error with the command and
error line retained. Only after that does it stage and compile C35.
Proposed per-command limits: 120 seconds wall, 90 seconds CPU, 4 GiB
address space, one Lean worker, 262144 bytes combined output.
Those native-command limits were not exercised by this turn's probe.
The wrapper's native success path remains untested.

`R10/C35AxiomAudit.lean` names 24 declarations, including earlier count,
projection and conflict theorems. The runner requires actual output for
each name and rejects an axiom outside propext, Classical.choice, Quot.sound.
It does not sign or submit any mathematical evidence.

## Remaining formal gaps

- First requested uncompiled dependency: the isolated projection and
  R10.Parallel22.bad22_le_incidence from C33.
- First new finite declaration: C35.Colors.mask_injective, then three
  finite colour counts.
- All arbitrary-N maps, inverse scripts and coercions still need Lean
  elaboration; API plausibility is not a successful build.
- `rank_event_count` still has a constructed-table product. The final
  proof that each shape has exactly 3/4 active factors, followed by the
  probability-weighted incidence sum and rational normalization, has
  NOT been mechanically supplied or verified by this capsule.
- C34's original 165462 Python checks are NOT converted into these
  pending Lean reductions.
- No scope-matched trusted semantic/root closure has run.

The retained conventional result is only:
  Pr(Bad22) <= 69828/N - 31878/N^2, for N>=1.
Bad22 is two DISTINCT parallel two-cycles meeting a vertex, not a single
two-cycle. This class is already inside C20's coarse overlap bound and
must not be added a second time. No total probability <41/800 is derived.

Remaining catalogues are unchanged: mixed/long shared edge instances,
shared paths/multiple common components, and mixed vertex-only overlaps.
Vertex-disjoint short cycles belong to matching deletion, not new bad mass.
This successor does not research any of those catalogues.

best_verified_candidate: none
best_verified_result: none
trusted_verified_scope: []
Both admitted obligations remain open.
