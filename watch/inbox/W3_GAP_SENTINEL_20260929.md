# W3 GAP SENTINEL (Mickey17 wave 3, telemetry lane, 2026-09-29)

Return 24 improvement landed: "gap-sentinel patrol - one cheap cron diffing consecutive
rollups + detecting sensor silence; every sensor inherits gap-detection free."

## Files

- `tools/gap_sentinel.py` (new, 358 lines): (1) diffs consecutive rollup snapshots;
  rollup.json + last_run.json in, per-project bytes/day out, bar default 1.0 GiB/day
  (sized to the 1.1GB kpi.jsonl class), windows under 0.25d are evidence only;
  history self-kept in `logs/gap_sentinel/history.jsonl`, one row per rollup run keyed
  on the last_run ts (deduped). (2) sensor silence over `SENSORS` (today:
  dashboard/static/x_radar.json): embedded top-level date field when the writer stamps
  one, else mtime (x_radar stamps none; verdict names the source); bar default 2.0d;
  missing sensor file flags as SENSOR-MISSING. (3) alerts to memory/attention.md in
  the estate patrol shape (### Gap sentinel fired (stamp) + verdict/record/response
  bullets; matched to the live census-patrol and FTS-daily blocks read before writing).
  Idempotent by key: alert lands FIRST in `logs/gap_sentinel/alerted.jsonl` (single
  writer, the B2-465 fts law: attention.md is a hot multi-writer file, best-effort
  only), key also grepped in attention.md so either survivor heals the other; a
  persistent gap stays exit 1 but never re-files (key carries the gap origin).
  Exit codes: 0 ok, 1 gaps, 2 cannot verify (missing/unparsable inputs).
- `tests/test_gap_sentinel.py` (new, 10 tests): fixture rollups -> growth computed
  (2 GiB/day flagged over a 1 GiB bar, 0.1 GiB/day not), short-window evidence-only
  law, stale sensor by mtime, embedded-date-beats-mtime, missing sensor, idempotent
  alerting across reruns + re-darkening at a new stamp, attention-survivor heals the
  lost jsonl, dry-run writes nothing, exit 2 on missing inputs, CLI exit codes.

## Real test line

`.venv/Scripts/python.exe -m pytest tests/test_gap_sentinel.py -q` -> **10 passed in
0.67s** (2026-09-29, repo venv).

## Real pass (live estate, 2026-09-29 ~20:24 local)

```
GAP-SENTINEL: ok - baseline: no prior rollup snapshot to diff, run 2026-09-29T14:23:05+00:00 recorded
GAP-SENTINEL: ok - sensor dashboard/static/x_radar.json fresh (mtime age 0.51d of 2.0d bar)
EXIT=0
```

Rerun minutes later: exit 0, history still 1 row (ts dedupe held), no writes duped.

## Real findings

1. **No rollup history ever existed on disk** (the disease, confirmed): index_data
   holds exactly one rollup.json, overwritten each run; first sentinel run is
   baseline-only. History starts now.
2. **First real metabolism reading** (tool core compute_growth over real bytes:
   git-committed snapshot 383fed94f @ 2026-09-27T13:57:14Z vs live 2026-09-29T14:23:05Z,
   window 2.02d): total +25.41 GiB = **12.59 GiB/day**; local_sovereign_agent +24.76 GiB
   = **12.27 GiB/day, 12x over the 1 GiB/day bar**. This was computed through the
   sentinel's own core but NOT filed by the tool (its ledger diffs only its own
   history); it becomes a sentinel-filed alert on the next index run. 12 GiB/day into
   the live lane is the kpi.jsonl class: logs/kpi.jsonl measures **1,085,592,447 bytes
   (1.01 GiB)** right now.
3. **Sep 22-25 x_radar hole byte-witnessed**: memory/runs/x_reply_radar/ err_*.log
   jumps 2026-09-21 straight to 2026-09-26 (4 days dark, exactly the unalerted hole
   return 24 named). Today's radar is fresh (0.51d), so no silence alert fired live.
4. **Rollup itself ran 10h before the pass** (mtime 10:23 local vs 20:24 pass) with
   last_run seconds=4992 (83-min runs): the index cadence is slower than its runtime
   suggests; noted as evidence, the silence bar does not yet cover the rollup sensor.

## Not done / next window

- No scheduled task registered (lane scope was build + one real pass). Register
  MagGapSentinelDaily mirroring scripts/census_patrol_daily.ps1 when adopting.
- Git holds prior rollup snapshots (rollup.json is tracked); a `--seed-from-git`
  history bootstrap is available if wanted, not built (scope).

## Gates

- Ratchet `check --changed`: my files add zero NEW debt (the FAIL rows name
  mag/physical_compute_acquire.py and tools/regen_front_door.py, other lanes' files).
- Em-dash count in both new files: 0.
- No git commit (lane order).
