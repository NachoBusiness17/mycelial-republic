# R2 LANDING: CACHE-RECEIPT PRODUCER (ouroboros night loop, cache lane)

Seat: R2-landing cache lane. Moment: 2026-10-05T16:43:49Z (12:43 EDT). Producer executed: row 6 of `watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/SYNTHESIS.md` (cache-receipt law has zero producers). Landing file: `mag/flight_recorder.py` (this lane's only code file) plus the pinning test `tests/test_flight_recorder_receipt.py`. No git commit, per lane law.

## WHAT WAS WIRED

The reuse/decision point in the recorder is the row build inside `record_call` after the cache-field parse: the vendor's `cached_tok` is a nominal claim, and the receipt law (`mag/context_checkpoint.py`, prefix_receipt.v1 from the B2 lane) says a hit claimed by token identity but unproven by state identity costs the same as a miss. Changes, all additive:

1. `mag/flight_recorder.py:97` ROW_FIELDS gains `cache_receipt`; every future row carries the key (null when unstamped), old rows simply lack it.
2. `mag/flight_recorder.py:192` new `_stamp_cache_receipt()`, called from `record_call` (`mag/flight_recorder.py:264`) between the credits estimate and the emit. Two verdict sources, gate first: (a) caller-supplied `cached_prefix` + `prefix_receipt` + `config_generation` run through `gate_skip_recompute()` from `mag/context_checkpoint.py`, stamping `{ok, verified_tokens, reason}` with `verified_bytes // 4` (the estate chars-per-token convention); (b) pass-through of an upstream producer's `usage.cache_receipt` dict when it carries `ok`. No inputs or no cache telemetry leaves the row nominal (pre-law behavior byte-preserved). Fail-open per the recorder law: a stamping error prints loudly to stderr and never breaks the wrapped call.
3. `mag/flight_recorder.py:156` `_extract_tokens()` now also accepts the generic `cache_hit_tokens` / `cache_miss_tokens` split, candidate added at `mag/flight_recorder.py:182`; that is the shape `tools/cache_kpi.py` already accepted from the estate usage log. Found by the new tests: the recorder rejected the KPI reader's own accepted shape, so a response shaped like the estate log landed no telemetry at all. Vendor-specific keys keep precedence.

Producer contract for callers: pass the receipt trio to `record_call` (they are recorder-owned kwargs, never forwarded to the wrapped fn), or stamp `usage.cache_receipt` upstream; either way the row carries the verdict.

## KPI READING AFTER

Baseline, a same-session run of the KPI tool before wiring: TOTAL 77715 rows, nominal tok_hit 96.4 percent, recv_tok 0, recv_hit 0.0 percent on the primary estate usage log; the flight-recorder side read 1456 rows with 105 cache rows, nominal tok_hit 28.06 percent, receipted 0.0 percent.

After wiring, both real logs read unchanged: receipt_tok 0, recv_hit 0.0 percent. This is the executed-with-deviation branch the producer ask pre-authorized: no live reuse row exists yet because no live caller passes the receipt trio and no upstream producer stamps `usage.cache_receipt` yet. The producer is wired and proven; adoption is the next lane's move.

Synthetic-row KPI proof from the test fixtures, run through the exact producer path (a `record_call` emit read back by the KPI compute; fixture source is the producer test's feed-the-KPI case at `tests/test_flight_recorder_receipt.py:138`): two deepseek-shaped rows, row 1 gated verified with verified_tokens 63 and reason ok, row 2 nominal unstamped. The KPI read: cached_tok 200, receipt_rows 1, receipt_ok_rows 1, receipt_tok 63, unreceipted_tok 137, nominal tok_hit_rate 0.5, tok_hit_receipted_rate 0.1575. The receipted split is nonzero for the first time: the KPI now measures usable cache, not claimed cache.

## GATE

- The two receipt test files (`tests/test_cache_receipt_law.py`, `tests/test_flight_recorder_receipt.py`) together read 12 passed, zero failures, rerun clean under `-W error`.
- Ratchet `check --changed`: zero NEW rows on this lane's diff (a grep of the ratchet output names neither landing file). The changed-scope run printed one NEW row, `tools/free_lane_fleet.py` in the file-too-long class, a sibling lane's working-tree edit; the unscoped run adds `mag/mycelium.py`, likewise not this lane's diff. Not accepted, not baselined, not touched by this lane.
- No em/en dashes introduced; no git commit made.

## RESIDUE

- Real-log receipted split stays 0.0 until a caller adopts the receipt trio or an upstream producer stamps `usage.cache_receipt`. Richest candidate: the deepseek_overmind lane, 96.4 percent nominal over 2549888 cached tokens. Second candidate: any lane already checkpointing through `mag/context_checkpoint.py`.
- The ratchet NEW debt on the two sibling files is filed here as observed, owned by nobody in this lane.
