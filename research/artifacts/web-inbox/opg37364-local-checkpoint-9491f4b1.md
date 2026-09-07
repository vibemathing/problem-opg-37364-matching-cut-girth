# Local continuation checkpoint: exact artificial regularization

Verdict: candidate_only.
Checkpoint state: nonterminal; locally saved, not written to GitHub.
Repository: vibemathing/problem-opg-37364-matching-cut-girth
Issue to reuse: https://github.com/vibemathing/problem-opg-37364-matching-cut-girth/issues/3
Latest main read: 9491f4b15e504fc415362ba55591483a941443a6
Candidate transport intended branch: web/attempt-opg37364-a01-c21-exact-regularization-9491f4b1
The intended branch name is not a claim that it has been created.

## Frozen identities

Problem: problem:opg-37364-matching-cut-girth
ProblemContract SHA-256:
cb72346bada4d4c41ce287a6d04f4b756717cc0a12cdb85ace863b379873d0eb
Harness: 1.1.2
Harness snapshot SHA-256:
ae8996d3666d0964bf02dadfc701c16dd10cb4f82d9b096f7619fb49973af861
Attempt: attempt:web-20260906-opg37364-a01
Route: route:degenerate-and-bridge-audit-v1
Graph: graph:opg37364-initial-v1
Current target: obligation:opg37364-root

## Mathematical state

best_verified_candidate: none
best_verified_result: none
best_available_local_candidate:
  C21A uniform-square-size reuse of C20, additive cut margin and strict
  one-edge deletion; C21B exact artificial regularization and the
  degree-62, average-degree-below-five, all-prescribed-girth family.
This candidate has a written derivation and byte-bound files only.
No graph sampler, enumerator, mathematical solver, proof assistant or
trusted mathematical verifier was executed.

open_obligations:
  obligation:opg37364-contract-edge-cases
  obligation:opg37364-root

The source root is already attributed a negative answer by the cited
2025 paper. C21 claims no originality or best-known constant. The new
family uses a cyclic nontrivial core and does not erase K1 from the
frozen quantifier. Required source-faithfulness and mathematical checks
remain separate and unsupplied.

## Research delta retained without duplicating current main

The early local 24-colour rederivation was not published. A later read
found C20 and confirmed its actual merge at main 9491f4b15e504fc415362ba55591483a941443a6.
The active package therefore does not re-submit that counting result.
It instead supplies the uniform-size bridge, parity margin, additional
edge deletion and exact regularization. The old locally staged C20
packet is not included in this continuation bundle.

The exact new regularization hypotheses are kN even and N>5B. Its
exchange proof considers two deficit units at one vertex as well as
two distinct vertices, and both pairings of a cycle using the new
edges. At fixed k=38 it yields the integer inequality 2m+2<=5n and
maximum degree at most 62. Removing the parity, current-distance or
strict-seed-deficit hypotheses is not licensed.

## Failed directions already checked

The authoritative failed-routes ledger was freshly read empty at
the main above. This does not erase candidate-level failed-route
proposals. In particular the C12 size-only fixed-degree extrapolation
is not repeated; no-MC existence is not inferred from an empty
size-only interval. No new failed-route record was written.

Also retain the earlier distinctions: global average is not maximum
average; arbitrary subdivision does not preserve no-MC; an empty
crossing matching differs from an empty shore; the old 1/4 numerical
tail bound is not valid for the 24-colour bracket. C20 already handles
the latter issue, so no duplicate failed-route proposal is added here.

## Remote transport chronology: do not apply obsolete patches

The initial read found main a045cb08b9b9d3251431b7c4caf648857289a1b2,
PR15 at head 2eb8ae5e42d3a112cde83f6259d0a1984dc6c548,
and PR18 at head 6d5f17fe855889128c67eef62c74fefc6c45c40c.

Their real failed job logs were read:
- PR15 run 34026084916: packet and diff failed on the C12 proof digest.
  Unchanged proof blob c335249546611f7c7f4346ad2561150bd28a1134
  was reconstructed with the same Git blob identity. Its actual SHA-256:
  4606eff0245b4d3a407253a6826f40eb79edccddceaa707d29e58f00bcd1ed4b.
- PR18 run 34033732599: snapshot and packet passed, while the diff
  rejected an output-status key in its candidate handoff.
  A local minimal field-removal/hash patch was prepared, not applied.

SUBSEQUENT REAL READS SUPERSEDE THAT RECOVERY PLAN:
- PR15 is merged as 3976e5c58bfcfc0b193a922e8dc15968191ae3a1.
  Final observed head: 9a447499c81770a83599b660240522e3877cbff8.
- PR18 is merged as b21a752dfce02c244cf67630e8b20e8d55d22d00.
  Final observed head: 7af984a8a5b407dcae12d774f1304c62757323e4.
- C20 / PR21 is merged as 9491f4b15e504fc415362ba55591483a941443a6.
  Final head: 78406f993d8540af871820879f5b86483395fe10.
  Run 34043559510 was read directly; jobs 101514502468,
  101514502607 and 101514502623 completed successfully for the
  three required checks.
- The latest open-PR listing returned an empty list.

These are observed remote facts, not write calls made through the
read-only tool surface of this continuation. The earlier patches
must NOT be applied to the now-repaired files or treated as pending
work. They are deliberately excluded from the active bundle.

Relevant live locators:
https://github.com/vibemathing/problem-opg-37364-matching-cut-girth/pull/15
https://github.com/vibemathing/problem-opg-37364-matching-cut-girth/pull/18
https://github.com/vibemathing/problem-opg-37364-matching-cut-girth/pull/21
https://github.com/vibemathing/problem-opg-37364-matching-cut-girth/issues/3#issuecomment-5560397553

## Current capability and persistence limit

The exposed GitHub tool catalog was inspected, including a later retry:
it supplies read/search actions but no create/update/comment/merge action.
The installed-plugin search found the already installed GitHub connector;
it did not provide an alternate write action. No gh executable was found.
No credentials were inspected and no unrecognized write tool was invoked.
This is a tool-surface limitation, not an observed permission denial,
not a missing admitted Attempt, and not a missing branch protection.
Historical pending-smoke metadata was not used as a research stop condition.

GitHub checkpoint written for this local C21 package: no.
Remote C21 branch/commit/PR/checks: none claimed.
The local checkpoint preserves the work but is not equivalent to Issue
persistence or accepted transport. No platform-quota termination label
is asserted merely because writing is unavailable.

## Local structural validation, not remote or mathematical verification

The fetched packet schema was reconstructed in memory and its Git blob
identity matched 920bddf2ec1ef1d655cea76d3dbd84232f6e328a.
Python jsonschema 4.26.0, Draft202012Validator with FormatChecker, accepted
the C21 draft packet. Its candidate byte digests were recalculated and
matched the files. This was local JSON/serialization checking, not the
repository's required CI, a mathematical computation, or a trusted receipt.

## Active artifacts and SHA-256

research/artifacts/candidates/opg37364-c21-seed-margin-9491f4b1.md
  4297bdb0cc3f1b484936f74c719f1701c10ccf08414d638a1a0b8b6566d0a43a
research/artifacts/candidates/opg37364-c21-density62-9491f4b1.md
  e1f10b41a6233e4ad8325f302cf8fc23ece3b954d1a41cd3019fa19f2cdd0857
research/artifacts/source-notes/opg37364-c21-source-scope-9491f4b1.md
  b917a094a3e9d2b3ed8ff5ca811ec23a469bea009dad4859582d661be9dd6dfa
research/artifacts/web-inbox/opg37364-a01-c21-exact-regularization-9491f4b1.json
  5ec65fda2d084ee2a94af4c9f1d0c9a3e6566bd66021499d5b8da911339bdd48

The package contains exactly one JSON file under web-inbox: that draft
attempt packet. This Markdown checkpoint is not another packet.

## Unique next action

Fresh-read main, Issue3, all open candidate PRs and candidate branches.
Reuse the current research Issue. Do not repair PR15/18 again.
Check whether the exact-regularization candidate has since been
transported or superseded by another live candidate; compare statements,
not just sequence labels.

If write actions are actually exposed, start from the newly read main,
use a unique candidate branch, preserve source revision bindings, and
transport this same admitted-route/root candidate through the three
required gates. Rebind the packet base after any intervening merge,
then populate the actual PR number/URL and update hashes after edits.
Do not reuse a planned branch name as proof of existence and do not
force-push or change protected files.

The mathematical next verification focuses on the C20 finite-count
dependency, C21A parity/deletion bridge, C21B regularization exchange
and strict integer root mapping. The existing registry names do not
by themselves extend fixture-verifier policy or authorize a runtime.
Both open obligations remain nonterminal.
