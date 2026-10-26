# B8 — VERKLE V2 PRECONDITIONS (compaction guard + reader rows!=sessions resolution)

**Class:** BUILD RECEIPT · **Date:** 2026-09-30 · **Seat:** B8 (AJ6 memo preconditions)
**Mission:** land VERKLE_V2_DECISION.md §4 preconditions 1+2 so the operator flip is ready at the quiet window. **No chain writes; `configs/mag.yaml` `chain_mode` untouched (still v1, verified by test_live_config_defaults_to_v1 in the same run).**

## 1. Compaction v2 refusal guard (precondition 1)

`mag/verkle_compaction.py` — both entry points now READ `vk.chain_mode()` and refuse under v2 BEFORE any read/write:

- `plan()` and `apply(execute=...)` return `{ok: False, refused: True, exit: 2, reason, error, chain_mode: "v2", changed: False}` — exit 2 is the estate's hard-block grammar (ratchet/census-patrol: cannot run, never a soft skip), so a future `--compact --execute` CLI wrapper can pass it straight through.
- Reason names the cause: under v2 the fold candidates are canonical append-only history ((session_id, session_seq) leaves that never unlink); the fold is a history destroyer until compaction learns v2 semantics. Mirror of `verkle_knot.consolidate`'s guard.
- Test `test_plan_and_apply_refuse_v2` proves it non-vacuously: the fixture chain HAS 3 real fold candidates; the refusal is the only thing stopping the fold (zero writes, no archive dir, 7 rows unchanged).

## 2. Reader rows!=sessions resolution (precondition 2, "session-dedupe" branch)

Decision per reader (the memo allowed dedupe or tag; all three got the minimal latest-per-session resolution, last-matching-row-in-chain-order — the same rule as `verkle_knot.latest_leaf_for_session`'s fallback, exact for v1 and for mixed chains):

| reader | what breaks under v2 | minimal resolution |
|---|---|---|
| `mag/cache_map.py` | every chain row becomes a time window: one session double-counts as N windows/N sessions; a STALE earlier row's window shadows the live one | `latest_rows_per_session()` dedupe before the sweep-line join; `verkle.n_sessions` = sessions, new `verkle.n_chain_rows` = raw rows (different denominators, census law) |
| `mag/knot_untangle.py` | one session's own seq history is near-identical content → false "tangled" near-duplicate clusters; n_knots counts rows | dedupe in `scan_chain()` before clustering; scan surfaces `n_knots == n_sessions` plus `n_chain_rows` |
| `mag/gene_pool_feeder.py` | consumes aud_verkles AGGREGATES (never raw rows): `rows`/theme counts would count re-saves; `dup_rate` would read as anomaly while canonical | `resolve_verkle_basis()` seam: session basis = `distinct_session_ids`, `append_mode` flag when rows != distinct, gene TEXT names both denominators; emphasis stays row-count (operator law: duplication IS emphasis); per-theme session counts are unrecoverable from aggregates — the regenerator (tombstone revive condition) must dedupe before counting; the seam refuses to guess |

**v1 identity law:** every resolution short-circuits to the input when no session_id repeats (one row per session = v1 amend semantics) — pinned by identity tests, and by the live read-only smoke below.

## 3. Tests (all green, 2026-09-30, `.venv/Scripts/python.exe -m pytest`)

- NEW `tests/test_b8_v2_preconds.py` (7 tests): multi-row→latest for cache_map (stale window never shadows, n_sessions vs n_chain_rows), basis identity + v2 append_mode for gene_pool, latest-row-represents-session for knot_untangle (stale seq row never appears in a tangled cluster), plus identity-on-v1 for both dedupe helpers.
- `tests/test_verkle_compaction.py` +1 (`test_plan_and_apply_refuse_v2`), whole family green.
- Families run: test_b8_v2_preconds + test_verkle_compaction + test_ah19_append_leaves + test_verkle_lock + test_verkle_audit + test_verkle_artifact + test_verkle_dangling + test_verkle_restore_prep + test_abundance_rogue (the knot_untangle consumer) = **57 passed**, includes AH19 family (decision precondition 3 rerun).
- Live v1 chain smoke (read-only, this moment): chain now 8,670 rows (memo read 8,669 — census denominator law, snapshots; post-memo fold). `cache_map`: n_sessions 8670 == n_chain_rows 8670 (identity), 11 themes. `knot_untangle`: ok, n_knots 8670 == n_chain_rows (identity), 1,478 tangled clusters (unchanged meaning on v1).

## 4. Ratchet / debt (named, single claim)

`mag/verkle_compaction.py` crossed the 400-line cap (397 → 446; the guard is ~50 lines). Fixing meant restructuring tested pre-existing code; instead the claim is REGISTERED BY NAME: fingerprint `4daad8149e0cc9a7`, `by: B8-v2-guard`, accepted_lines 446 (B2-273 growth law stamps the size). Registered by hand because blanket `baseline-update` registers the WHOLE tree and would have swallowed other lanes' NEW debt (water_graph, pain_replication, mountain_reveal, cost_rollup, child_development_acquire — all still unregistered, none mine). Ratchet `check --changed` after registration: no NEW hits in B8 files.

## 5. Files touched

- `mag/verkle_compaction.py` (guard + docstring)
- `mag/cache_map.py`, `mag/knot_untangle.py`, `mag/gene_pool_feeder.py` (latest-per-session / basis resolution)
- `tests/test_verkle_compaction.py` (+1 test), `tests/test_b8_v2_preconds.py` (new)
- `configs/violation_baseline.json` (single named claim, §4)
- CRLF note: the editor churned four files to CRLF mid-edit; normalized back to LF (HEAD is LF; diffs are now line-exact: +210/−11 across the five code/test files).

**Status: both flip preconditions (1) and (2) LANDED and green; precondition 3 (AH19 family) rerun green. The flag itself remains the operator's quiet-window call — nothing here flips it.**
