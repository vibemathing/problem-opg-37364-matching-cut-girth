{
  "schema_version": "1.1.0",
  "channel": "chatgpt-web-github-issue-pr-writer",
  "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
  "repository_identity": {
    "binding_state": "verified",
    "database_id": 1358762848,
    "node_id": "R_kgDOUP0TYA",
    "default_branch": "main"
  },
  "problem_id": "problem:opg-37364-matching-cut-girth",
  "problem_contract_sha256": "cb72346bada4d4c41ce287a6d04f4b756717cc0a12cdb85ace863b379873d0eb",
  "harness_snapshot_sha256": "ae8996d3666d0964bf02dadfc701c16dd10cb4f82d9b096f7619fb49973af861",
  "base_revision": "9491f4b15e504fc415362ba55591483a941443a6",
  "importer_policy_sha256": "a7650a8ba5be3fef370914b24a49b1118f57dc12f41980f21b11ef2b0a8267c1",
  "attempt_id": "attempt:web-20260906-opg37364-a01",
  "route_id": "route:degenerate-and-bridge-audit-v1",
  "graph_id": "graph:opg37364-initial-v1",
  "obligation_id": "obligation:opg37364-root",
  "generator": {
    "principal": "chatgpt-web-github",
    "model_label": "ChatGPT",
    "model_fingerprint_status": "unverified"
  },
  "transport": {
    "branch": "web/attempt-opg37364-a01-c21-exact-regularization-9491f4b1",
    "issue_number": 3,
    "issue_url": "https://github.com/vibemathing/problem-opg-37364-matching-cut-girth/issues/3",
    "pull_request_number": null,
    "pull_request_url": null
  },
  "objective": "Continue the now-merged C20 seed by proving uniform-size reuse, a strict one-edge deletion margin and exact artificial regularization; derive a fixed-d0=5, all-girth no-matching-cut candidate family with maximum degree at most 62 and an explicit non-nested order bound.",
  "candidate_artifacts": [
    {
      "candidate_id": "candidate:opg37364-c21-seed-margin-9491f4b1",
      "kind": "proof",
      "locator": "research/artifacts/candidates/opg37364-c21-seed-margin-9491f4b1.md",
      "sha256": "4297bdb0cc3f1b484936f74c719f1701c10ccf08414d638a1a0b8b6566d0a43a"
    },
    {
      "candidate_id": "candidate:opg37364-c21-density62-9491f4b1",
      "kind": "counterexample",
      "locator": "research/artifacts/candidates/opg37364-c21-density62-9491f4b1.md",
      "sha256": "e1f10b41a6233e4ad8325f302cf8fc23ece3b954d1a41cd3019fa19f2cdd0857"
    }
  ],
  "atomic_claims": [
    {
      "claim_id": "claim:opg37364-c21-uniform-size-reuse",
      "text": "Every size-dependent inequality in C20 remains valid for all M>=max(1000,4C,2g), N=M^2 at fixed g, giving a uniform-square-size seed rather than requiring a raised girth input.",
      "status": "candidate"
    },
    {
      "claim_id": "claim:opg37364-c21-strict-seed-margin",
      "text": "The even auxiliary degree gives at least |S|+2 final crossing edges at each smaller shore; one more edge deletion retains strict cut expansion, two-connectivity and 2m<=24n-2.",
      "status": "candidate"
    },
    {
      "claim_id": "claim:opg37364-c21-exact-regularization",
      "text": "If kN is even and N>5B, a maximum-cardinality artificial augmentation is exactly k-regular, by a far-edge switch that includes coincident deficit centres and both cycle pairings.",
      "status": "candidate"
    },
    {
      "claim_id": "claim:opg37364-c21-fixed-five-degree62",
      "text": "For every integer g>=3, fixed k=38 gives a finite simple 2-connected bipartite graph with no MC, girth>=g, minimum degree two, maximum degree<=62, and 2m+2<=5n.",
      "status": "candidate"
    },
    {
      "claim_id": "claim:opg37364-c21-explicit-order",
      "text": "At d0=5 one admissible prescribed order is 10240*g^4*(384*g^2)^(4*g), using an enlarged square part size at the same girth rather than nested girth inflation.",
      "status": "candidate"
    }
  ],
  "assumptions": [
    "The frozen finite-simple-graph, two-nonempty-shore and possibly-empty-crossing-matching definitions are unchanged.",
    "C20's finite counting is a fully specified candidate dependency, not an admitted theorem or a new axiom.",
    "The uniform-size argument uses square part sizes N=M^2 with every C20 lower-size bound retained.",
    "Exact artificial regularization requires kN even, N>5B and current-graph distances. One additional seed edge is deleted before artificial regularization."
  ],
  "risks": [
    "LOCAL STAGING ONLY: transport.branch is a proposed name, not a created branch. No C21 commit, PR, remote check or importer action has been performed through the current exposed tools.",
    "The GitHub tool surface rechecked in this turn exposes reads but no create/update/comment/merge actions; this is not repository admission drift.",
    "PR15 and PR18 were subsequently observed merged, and C20 was observed on main 9491f4b15e504fc415362ba55591483a941443a6. The earlier local repair patches are obsolete and must not be applied.",
    "Refresh actual main, open PRs and the unique Issue3 before a real cycle; rebind this packet after any further intervening merge.",
    "The degree-24 counting result already belongs to C20 and is not claimed as new here.",
    "The full C20 permutation counts and coloured-to-simple bridge, C21 reuse proof, exact-regularization switch and root semantics require the requested trusted verification.",
    "The strict deficit in the seed is needed to obtain average degree <5 at k=38; without it the displayed count gives only <=5.",
    "No graph enumerator, sampler, mathematical solver or proof assistant was executed; local JSON schema checks and hashes are transport preparation only.",
    "Both admitted obligations remain open. No endpoint at d=4, optimality or originality is claimed."
  ],
  "open_obligations": [
    "obligation:opg37364-contract-edge-cases",
    "obligation:opg37364-root"
  ],
  "failed_route_proposal": null,
  "source_refs": [
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "problem-library/records/canonical-problems.jsonl",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "exact"
    },
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "research/records/obligation-graphs.jsonl",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "exact"
    },
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "research/records/failed-routes.jsonl",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "prior_art"
    },
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "research/artifacts/candidates/opg37364-c20-degree24-seed.md",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "prior_art"
    },
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "research/artifacts/web-inbox/opg37364-a01-c20.json",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "prior_art"
    },
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "research/artifacts/candidates/opg37364-c18-elementary-density.md",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "prior_art"
    },
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "research/artifacts/candidates/opg37364-c19-finite-count-audit.md",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "prior_art"
    },
    {
      "repository": "vibemathing/problem-opg-37364-matching-cut-girth",
      "path": "research/verifiers.json",
      "revision": "9491f4b15e504fc415362ba55591483a941443a6",
      "relation": "exact"
    }
  ],
  "requested_verification": [
    "kernel_check",
    "axiom_escape_audit",
    "statement_faithfulness"
  ],
  "verdict": "candidate_only",
  "created_at": "2026-09-06T15:57:28Z"
}
