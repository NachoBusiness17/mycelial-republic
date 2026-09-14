# CHAIN_INDEX_AUDIT_20260905 — worker chainidx (concurrency probe)

Verdict up front: the builder is REAL and its run COMPLETED today (2026-09-05T02:13:17Z). The sidecar holds **13,677 rows**, not 21,264. **The 21,264 figure is DISPUTED** — measured off-chain knot count is 13,678; index coverage of present knots is 99.995% with exactly ONE file uncovered.

## Builder + sidecar (both exist, read directly)
- Builder: `scripts/chain_index_completion.py` (stdlib-only, idempotent, additive-only; docstring confirms sidecar path + schema)
- Sidecar: `memory/biography/chain_index_completion.jsonl` — row schema: `{knot_file, session_id, ts, dominant_theme, leaf_hash, indexed_by: chain_index_completion_v0, indexed_ts}`
- Builder stats: `memory/audit/chain_completion_stats.json` (run_ts 2026-09-05T02:13:17Z, parse_error_count 0)

## Measured counts (independent stream-count, not copied from stats)
| what | number |
|---|---|
| sidecar rows | 13,677 (all unique, 0 unparseable) |
| knot files present (`memory/biography/knots/*.knot.json`) | 20,951 |
| verkle_chain.jsonl rows (all carry `filename`) | 7,291 |
| off-chain knots (present, not in chain) | 13,678 |
| off-chain covered by sidecar | 13,677 |
| union coverage (chain ∪ sidecar ∩ present knots) | 20,950 / 20,951 = **99.995%** |
| GAP (present in neither index) | **1 file**: `2026-08-11_0330_biography_mag-agen_276a6070.knot.json` |

Note: since the builder's 02:13Z run, chain grew 7,199→7,291 rows and knots grew 20,859→20,951 (+92 both). 91 of those 92 new knots got chain rows; the 1 gap file is the fallout. Also: 18 chain rows reference filenames no longer present in knots/ (historical drift, not sidecar's problem — sidecar has 0 dangling refs).

## Tri-state on the 21,264 claim
- **DISPUTED.** Measured: 13,678 off-chain knots present; sidecar 13,677. Total knots is 20,951 — still not 21,264. The builder's own docstring claims "~7,200 of ~28,400 knot files" — also stale vs measured 7,291 / 20,951. Nothing measured reaches 21,264. Real number of record: **13,678 off-chain, 13,677 indexed, 1 gap**.

## Builder process state
`tasklist | grep -i python` → 1 python.exe, pid 13976. No args dumped (law). Can't attribute it to the builder; the builder is a batch script (runs to exit, not a daemon), and the stats file shows its run finished at 02:13:17Z. No evidence of a live builder loop. The sidecar is DONE except one file.

## THE one next row that completes the index
Re-run the idempotent builder — it diffs, appends only the missing row(s), never touches verkle_chain.jsonl:

```
cd C:\Users\foste\Documents\projects\local_sovereign_agent && python scripts/chain_index_completion.py
```

Expected delta: +1 row (`2026-08-11_0330_biography_mag-agen_276a6070.knot.json`), sidecar → 13,678, coverage → 100% of present knots.

— chainidx, 2026-09-05. All counts streamed line-by-line; chain file untouched.
