# C10: minimal formalization slice and constrained ToolPlan

Verdict: candidate_only. Primary owner: math-proof for the statement audit.
Supporting Skills: math-formalization (uncompiled slice) and
math-toolchain (ToolPlan only).
Candidate: candidate:opg37364-formal-slice-plan-c10.
Attempt: attempt:web-20260906-opg37364-a01.
Route: route:degenerate-and-bridge-audit-v1.
Graph: graph:opg37364-initial-v1.
Target: obligation:opg37364-contract-edge-cases.
Base: c1771a3b1830639a51d5b2cd8d626d79498317c5.

## C10.1 / claim:opg37364-c10-subsingleton-slice

For any vertex type V on which all two elements are equal, a function
c:V->Bool cannot take both Boolean values. Witnesses a,b for false
and true would give a=b, hence false=c(a)=c(b)=true. Thus no colouring
whose definition requires both values can exist. This argument also
applies to the empty type, but does not assign an average degree to
the empty graph.

The proposed Lean file
research/artifacts/candidates/opg37364-c10-nonempty-shores.lean
expresses this argument with an explicit at-most-one hypothesis.
It then specializes to Unit and the constantly false adjacency
relation. It separately supplies a positive colouring of Bool with
constantly false adjacency. This positive witness audits that an empty
crossing matching has not been inadvertently forbidden.

The file is an uncompiled formalization slice. Its displayed proof
terms and axiom-inspection commands are source, not execution output.
No compatibility, compilation success, axiom report or kernel receipt
is claimed.

## C10.2 / claim:opg37364-c10-semantic-boundary

The declared `UsesBoth` predicate records the two nonempty shores.
`LocalMatching` says that two neighbours opposite in colour to the
same centre must be the same vertex. On a simple undirected graph,
this is precisely the at-most-one-crossing-edge condition used in C08.
`HasMatchingCut` combines those two predicates; it does not require
a crossing edge.

Unit with false adjacency is intended to model K1; Bool with false
adjacency models the edgeless order-two graph. This intended graph
interpretation still needs semantic review. The Lean file does not
define or prove vertex cardinality, edge count, average degree, girth,
or the real/integer quantifiers of the frozen root. It therefore cannot
be submitted as a complete formalization of the root.

A future full mapping must show cardinality one, no edges, strict
0<d, forest girth +infinity, and the equivalence of the actual graph
library's cut predicate to both nonempty shores. A library that uses
a different acyclic-girth value or admits an empty shore must not be
silently substituted. The natural-language uniform admissibility
argument remains in C01/C08.

## Current capability check, without running a mathematical tool

At this base, the channel profile declares command_execution=false.
The maturity registry labels the T18 Lean 4/Mathlib family
verifier_admitted for a tested adapter. The separate knowledge-source
entry lean-mathlib-local is installed but quarantined, and describes
the v4.33.0 environment as blocked pending review. Neither is a current
runtime receipt or an authorization for this channel.
The fixture's lean-toolchain contains leanprover/lean4:v4.33.0.
This is a declared fixture version, not an observed or approved
execution version for this candidate.

Accordingly the authorization precheck stops before binary execution.
No Lean installation, version command, compilation, package download,
network request from a checker, or proof-object validation was run.
The slice asks for no explicit imports and does not need a mathlib
search hit, but that does not bypass runtime or verifier admission.

## ToolPlan (not executed)

- tool_id: T18 (Lean 4/Mathlib family).
- requested_verifier_principal: lean-kernel.
- knowledge_source_id: lean-mathlib-local.
- family_registry_maturity: verifier_admitted (metadata for a tested adapter).
- source_registry_status: installed and quarantined (metadata, not execution).
- acting_channel_execution_status: not_authorized_by_current_profile.
- selected_execution_version: unresolved; a trusted verifier must
  approve and pin an actual compatible Lean 4 runtime. The quarantined
  fixture declaration is not automatically selected for execution.
- candidate_input: the exact digest-bound Lean file listed above.
- package_requirement: no explicit source imports; record the actual
  implicitly loaded core and toolchain identity if a run is authorized.
- proposed_command_after_authorization:
  lean research/artifacts/candidates/opg37364-c10-nonempty-shores.lean
- requested_limits: one thread, 30-second external timeout, 512 MiB
  memory, 128 KiB output, no network, no package installation, no GPU.
- expected_artifact_type: compilation and axiom-inspection output, plus
  a separately produced semantic comparison. No output is supplied here.
- failure_policy: stop on a syntax/type error, timeout, unexpected
  axiom/escape route, version mismatch or semantic mismatch. Preserve
  actual diagnostics and revise only a new allowed-path candidate.
- evidence_ceiling_now: ToolPlan/uncompiled Candidate only.
- requested_verifier_roles: kernel check, axiom-escape audit and
  statement-faithfulness review. Registry entries lean-kernel,
  lean-axiom-auditor and lean-faithfulness-reviewer exist, but their
  fixture policies must be checked for authorization on this actual
  obligation; this plan does not extend their scope.

An eventual receipt must bind the frozen inputs, actual verifier trust
domain and authority, exact version/provenance, command, limits, exit
status, output digest and limitations. The generator does not issue
such a receipt. An eventual successful compile of this slice would
still leave graph cardinality, arithmetic/girth and source-faithfulness
mapping obligations open.

## Reproduction and adversarial review

Read the proof term before attempting a build: the only contradiction
is the equality of the two distinct Boolean constructors. Confirm that
both-colour witnesses are required and that the positive edgeless Bool
case is retained. Compare the literal source text against the packet
digest. Never replace the unproved graph/arithmetic/girth mapping by
an additional axiom merely to complete the file.

The official Lean language-reference search was consulted for the
core inductive-type/elimination setting:
https://lean-lang.org/doc/reference/latest/Basic-Types/Other-Types/
and the theorem-proving text:
https://lean-lang.org/theorem_proving_in_lean4/inductive_types.html
These are documentation locators, not a pinned executable environment
or a receipt. No source theorem is imported from the pending
extremal/expander arguments.

## Nonterminal checkpoint

best_verified_result: none.
best_verified_candidate: none in the mathematical-verifier sense.
open_obligations: obligation:opg37364-contract-edge-cases;
                  obligation:opg37364-root.
current_blockers: source small-order scope remains ambiguous; mathematical
                  execution and verifier scope are not authorized here.
retained_branch: web/attempt-opg37364-a01-c10-formal-slice.
transport_binding: research/artifacts/web-inbox/opg37364-a01-c10.json.
next_action: trusted semantic review of the literal small-order contract
             and authorization of an exact scope-limited slice check.
No root or subsidiary obligation is closed by this checkpoint.
