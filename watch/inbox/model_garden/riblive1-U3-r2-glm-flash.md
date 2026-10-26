# riblive1-U3-r2-glm-flash (glm-5.3-flash @ zai, turn 1, channel: content)

L1: The probe verdict needs the patrol's cannot-verify arm, not just UNMEASURABLE
CLAIM: My compare() collapses an empty shared set to rel_pct 0.0 and DECORATIVE (my L1), while (U2 L3) routes every unverifiable gather to a distinct exit code rather than a verdict. The probe has exactly this gap: shared_positions == 0 is a gather failure (token misalignment) wearing a verdict.
STEAL: Adopt (U2 L3)'s two-code rule: exit 0 for a verdict, exit 1 for a measured verdict against the selector, exit 2 for cannot-verify. In cmd_probe, when shared_positions == 0, print the row with verdict "UNMEASURABLE" and exit 2; never let compare() emit DECORATIVE from empty dlp. Same for observer_effect_same_text False (my L4): relabel MEASURED-PERTURBED but keep the verdict gated on exit 0 arms only.
FALSIFIER: A probe invocation returning 0 and a DECORATIVE verdict with shared_positions: 0 in the row.
SOURCE: mag/preload_selector.py compare, "rel_pct = (100.0 * mean_dlp / mean_lp) if mean_lp > 1e-12 else 0.0" + (U2 L3)
LEVERAGE: high

L2: Snapshot probe inputs with a byte contract before scoring, per the census frozen-vector rule
CLAIM: My selftest never pins load_blocks inputs to fixed bytes (my L5), and (U2 L2) shows frozen fixtures must never auto-sync to live data without a named receipt. The probe currently trusts whatever TESUJI_MAP.jsonl holds at run time, so a silent corpus edit between probe and selftest invalidates comparisons with no witness.
STEAL: Write catalog_bytes and catalog_sha256 of TESUJI_MAP.jsonl and steps.jsonl into each probe row at load time, mirroring (U3 L1)'s meta byte contract; in cmd_selftest, re-hash and flag input drift distinctly from orderer failure. Freeze selftest fixture vectors with a receipt requirement like (U2 L2) so a growing live file cannot silently move the expected booleans.
FALSIFIER: A probe row with no input hash field whose verdict later cannot be distinguished from one run against edited bytes.
SOURCE: mag/preload_selector.py "ok1 = ids_a == [b[\"id\"] for b in again]" + (U2 L2) + (U3 L1)
LEVERAGE: medium

L3: Zero-span recency and malformed-ts counting are one fix, not two
CLAIM: (My L1) proves the zero-span branch can never reach 1.0, and (my L3) shows unparseable ts collapses to recency 0.0 undetected. After patching the branch per my L1, the two populations become distinguishable: known-same-ts blocks get 1.0, malformed-ts blocks stay 0.0, and the (U3 L5) pattern of counting-and-continuing with an operator-visible counter covers the rest.
STEAL: Patch the branch to "(1.0 if ts and ts_span == 0 else 0.0)", then add the cmd_order counter from my L3 printing malformed-ts recency-0.0 count vs genuine-oldest count, and fail the run above a threshold, copying (U3 L5)'s malformed_lines handling made loud.
FALSIFIER: Two blocks with identical valid timestamps scoring recency 0.0 after the patch, or an order run on a file with every ts malformed exiting 0.
SOURCE: mag/preload_selector.py score_blocks, "1.0 if ts and ts_span == 0 and ts == ts_min and not known else 0.0" + (U3 L5)
LEVERAGE: high

L4: Cross-source heat scores are an index built over incommensurable rows, so apply the malformed-line rule
CLAIM: My L2 shows tape (duration_ms) and tesuji (token count) heat share one 0.2 weight with different denominators; (U3 L5) shows silently skipped malformed lines shrink a corpus invisibly. A block with ts or token count unparseable currently drops out of normalization silently, so each source's max heat may be computed over a shrunk set.
STEAL: In cmd_order, print per-source block counts vs raw line counts alongside the top-10 heat table from my L2's steal; a gap means dropped rows, and any tape block with 0 tokens outranking a token-rich tesuji block opens the cross-source normalization card.
FALSIFIER: An order run where heat maxima match across sources despite a nonzero malformed/unparseable count, proving dropped blocks do not move normalization.
SOURCE: mag/preload_selector.py "for src in (\"tesuji\", \"tape\")" + (U3 L5)
LEVERAGE: medium

L5: The verdict core in compare() should be pure over parsed bytes
CLAIM: (U2 L3) extracts verdict logic into pure cores taking only parsed dicts so every failure is a declared exit. compare() already takes computed metrics, which is why it can silently emit DECORATIVE on empty input; the fix is to widen the core's contract, not add guards downstream.
STEAL: Refactor so compare() returns {verdict, rel_pct, shared_positions, guard_ok, unmeasurable_reason} and cmd_probe maps unmeasurable_reason to exit 2; assert in selftest that every fault shape (empty shared set, perturbed observer, zero scale) yields unmeasurable_reason, table-driven like (U2 L3)'s five-fault vector test.
FALSIFIER: A compare() call returning verdict DECORATIVE with unmeasurable_reason unset and empty shared positions.
SOURCE: mag/preload_selector.py compare + (U2 L3)
LEVERAGE: medium
