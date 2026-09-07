# Original A-G audit attachment: provenance and live-status separation

Verdict: candidate_only. Target: obligation:opg37364-root. Issue: #3.

The attached ZIP has SHA-256 6d5d8ec8d139a7ddedc0ea811b9a77a397ef9f63946747ae606702e0d23f4b92. All 28 text members are preserved byte-for-byte under research/artifacts/candidates/opg37364-c21b-audit-1735793e/. The ZIP is a packaging container, not another mathematical artifact. Before commit, all remote member Git blob identities and sizes were compared with values recomputed from the actual attachment bytes; all matched. The original manifest lists all members other than itself; its own SHA-256 is ffcb68b9e900249f9b50ab44312b35d3394b874ef751652e5bd19b19ad88ebf5.

The proof SHA-256 is 82a1adb1043c9a60b3c9d43696d68c24ca14bf7addd3189dd09b9cfcbd13cbb8. It is different from the previously merged PR28 proof (fb654e9b15064842648e59a80da48a334515e9ff1677096072a39d078dbe307a). The original checker also differs; neither existing audit is overwritten or passed off as the other.

The original execution records, timestamps, runtime version, raw bounded outputs and empty stderr files are historical observations supplied with the attachment. This archive transaction does not claim to have rerun them. It preserves the correction in overlap-path-audit/: shared_path_pairs=1560 originally meant at least two common edges; the separately executed adjacency test reports1200 actual shared-path pairs and360 nonadjacent-only pairs. Both original output and correction are retained.

Original README/checkpoint statements that the package was local-only and writes were unavailable remain unchanged as historical text. They are superseded for transport only by the live packet research/artifacts/web-inbox/opg37364-a01-c21b-original-1735793e.json and the current Issue3 checkpoint. They confer no authority on any later execution.

No protected original, truth record, schema, Harness, workflow, registry, Evidence or Result is edited. Both admitted obligations remain open. Next: run a separate second implementation, perform primary-source comparison and submit a scoped admission request. Mathematical correctness is not inferred from this preservation or from the three transport checks.
