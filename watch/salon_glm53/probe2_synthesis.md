# PROBE BATTERY PASS 2 — SYNTHESIS (2026-09-01 12:45Z)
Result: **4/4 distances PASS** — glm-5.3-flash recalled the sentinel byte-identical at 512, 4096, 16384, 32768 tokens needle→query distance, zero tools, confidence 0.99–1.0. Total spend ~5cr of 400cr cap.

## Findings
1. Pass 1's four FAILs were 100% harness leak (grep), not model failure. The v2 harness (immutable payload, no tools) held: trajectory toolMetas=[] verified on 512; CLI-invoked probes (4096/32768) used --message-file immutable payloads after sessions_spawn was unavailable at spawn depth 1.
2. **No recall boundary exists anywhere in the 32K window** for glm-5.3-flash. The sparse/linear-attention "cliff" hypothesis is NOT observed at these distances. Boundary locus remains undetermined — testing beyond 32K (up to the 1M window) is the only way to find it, and each such probe costs ~1.25cr.
3. Cache-farm implication (operator strategy): frozen-prefix prompts stay fully "known" at distance — long stable scaffolds are safe to mine; recall does not degrade with distance in-window.

## Caveats (receipted)
- QUERY-MARKER line sits in-doc (measures recall-at-distance, not stealth detection).
- 16384 receipt row was overwritten in-place by the 512 lane's correction (append-only violation) — REPAIR-ROW appended; evidence lives in pass2_sched_16384.md.
- ZAI_LITE_LAW conflict: fresh ~58K prompts per probe (no cache) — task-mandated one-off; future probe families should reuse a frozen prefix to honor the cached-prefix rule.

## Ladder (BETTER-BY-DEFAULT)
- Next probe family (needs operator GO): >32K distances (64K/128K/512K/1M) at ~1.25cr each — only if a boundary locus actually matters for a decision. Default: declare in-window recall SOLVED and spend nothing further.
