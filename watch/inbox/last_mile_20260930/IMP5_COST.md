# IMP5_COST — cost_rollup.py landed (2026-09-30)

**Fence owner:** seat (ZCode, last-mile IMP5). **Files owned:** `tools/cost_rollup.py`, `tests/test_cost_rollup.py`, this receipt.

## Problem

Cost truth scattered across four schemas, no aggregate: `logs/duel/duels.jsonl` (per-row `a_cost`/`b_cost`/`judge_cost`, day from row `ts`), `logs/mates/*.jsonl` (`cost_usd` + `model`, no row ts -> day from filename `YYYYMMDD`), `logs/hermes_gopher_burn_*/*.jsonl` (`cost_usd`, fallback `cost`, day from dir/file `YYYYMMDD`), `training/cost_ledger.jsonl` (`cost_ledger.v1`: `actual.usd_est`+`usd_fixed`, `actual.calls`, model = `platform.model` -> `estimate.model` -> `platform.seat`; route-only rows with 0 calls/0 usd carry no cost and make no bucket). Note: mission brief said duels.jsonl carries `cost_usd`; schema read shows the a/b/judge triple instead, tool handles both.

## Landed

- `tools/cost_rollup.py`: read-only scan of all four surfaces; rollup per (day, model) -> calls, total_usd, contributing surfaces; grand total + calls; trailing 7-day trend (zero-filled, `--days N`); `--json` dashboard payload; `--root` for hermetic tests. Unparseable surfaces NAMED (path + line + error) and never dropped; missing required surfaces (duels, ledger) also named. Zero-cost buckets suppressed; zero-cost calls still count inside existing buckets.
- `tests/test_cost_rollup.py`: 7 tests — four-surface aggregation arithmetic, model fallback chain, no-op-row suppression, grand-total consistency, trailing zero-filled trend window, named-unparseable (bad JSON line survives with neighbors counted), missing-surface naming, `--json` and text CLI smoke (subprocess, `--root` fixture).

## Evidence

- Tests: `pytest tests/test_cost_rollup.py -q` -> 7 passed (2026-09-30).
- Live run (2026-09-30T17:41Z): surfaces scanned duels 63/63, mates 2 files 7/7, gopher 3 files 18/18, ledger 2439 rows / 1801 cost rows; UNPARSEABLE: none.
- **Live grand total $135.7095 over 25,376 calls.** Trend 09-24..09-30: 0 / 0 / 0.8777 / 0.3448 / 0 / 1.9245 / 6.0712.
- Independent cross-check (raw sums per surface, no rollup code): duels 5.565 + mates 0.2916 + gopher 1.7910 + ledger 128.0618 = 135.7094 vs rollup 135.7095; 1e-4 delta is the per-cell 4dp rounding policy (grand sums rounded cells), not a scan gap.
- Day attribution caveat: mates/gopher files carry no row timestamps; day comes from filename/dir date, mtime fallback. A file copied under a renamed path would re-date its rows.

## Full-suite status (honest, per census law: name instrument + moment)

- Full `pytest -q` NOT completed this lane. Instrument: `.venv\Scripts\python.exe -m pytest -q --ignore=tests/test_mountain_reveal.py`, 2026-09-30 ~14:20-15:10 EDT.
- Blocker 1 (collection): sibling lane's in-flight `tools/mountain_reveal.py:384` SyntaxError makes untracked `tests/test_mountain_reveal.py` uncollectable; `-x` run stops there. Not this lane's ownership; excluded, named.
- Blocker 2 (environment): two subsequent full runs died silently at 22% and ~27% with no Python traceback and no pytest summary (external kill; host was also running other lanes' concurrent full suites). A first attempt's output was lost to a stale background wrapper. These are host kills, not test failures; no FAIL/ERROR summary was ever produced by my change.
- Blast radius: this landing is purely additive (`tools/cost_rollup.py`, `tests/test_cost_rollup.py`, this receipt); zero existing modules imported or modified, so the suite exposure of this change is the 7 targeted tests above, all green.

## Dashboard seam

`python tools/cost_rollup.py --json` -> keys `generated_utc, root, trend_days, surfaces, rollup, grand_total_usd, grand_total_calls, trend, unparseable`.
