# W3V — x_radar hole census + HOLES stanza (2026-09-29)

Mickey17 wave 3 telemetry lane. Mission: enumerate `memory/runs/x_reply_radar/` honestly,
render the gaps instead of silently skipping them, file one idempotent attention alert.
Tool: `tools/x_radar_backfill.py` (new, idempotent, data pass only). No git commit.

## Real hole table (census 2026-09-08..2026-09-29: 22d expected, 15 ok, 7 missing, 2 holes)

| dates | status | cause (byte witness) | first_seen |
|---|---|---|---|
| 2026-09-08 | empty-raw (0-byte `out_2026-09-08.json`) | no err log survives; era-matched to the 402 window, NOT byte-proven for that day | 2026-09-09 |
| 2026-09-09 | empty-raw | `err_2026-09-09.log`: 402 Payment Required "Grok Build usage balance exhausted" | 2026-09-09 (same-day err log) |
| 2026-09-10 | empty-raw | `err_2026-09-10.log`: same 402 | 2026-09-10 (same-day err log) |
| 2026-09-22..25 | missing | writer never ran: ZERO artifacts (no out_*, no err_*, no card); no in-repo scheduler owns `mag.x_reply_radar run()` (grep: no caller in mag/, scripts/, configs/); telemetry finding named it "x_radar silent hole Sep 22-25 unalerted" | 2026-09-29 (`watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md` return 24; no same-day witness existed — the disease itself) |

Corroboration: cards exist for 09-12..21 and 09-26..29 only. Runs dir is untracked by git
(`git ls-files` empty), so disk bytes are the only witness.

## Census caveats filed honestly

- `watch/X_REPLY_RADAR_20260906.md` is a daemon-import artifact: `mag/x_reply_radar.py`
  freezes the card path at module import (2026-09-06) while header dates run daily; its
  surviving content is the 2026-09-11 run (mtime 09-11 08:05). The census matches cards by
  HEADER date, never filename. No raws survive for 09-06/07 → window opens at first raw
  attempt 09-08; earlier days are witness-only prehistory, not counted holes.
- Census end defaults to LOCAL today: just-past-midnight-UTC would frame the not-yet-run
  fresh local day as a hole (fabrication, not silence).

## Artifacts landed

- `tools/x_radar_backfill.py` — census + gaps writer + HOLES injector + idempotent alert
  (exit 0/1/2; `--dry-run`). Rerun any time; new holes get a new key and re-alert.
- `dashboard/static/x_radar_gaps.json` — durable 22-day per-day table + holes + prehistory note.
- `dashboard/static/x_radar.json` — one-time safe edit: top-level `HOLES` added
  (2 stanzas, `{missing_dates, cause, first_seen, days}`), original
  threads/leaderboard/patterns preserved byte-for-byte in meaning. Schema-safe: only
  consumer is `estate_walk.html` (path listed as graph node) and `tools/gap_sentinel.py`
  (reads top-level date fields only; none added). Post-edit: `gap_sentinel --dry-run` still
  green, `tests/test_gap_sentinel.py` 10 passed.
- `memory/attention.md` — one estate-patrol block, key
  `x-radar-holes 2026-09-08..2026-09-10+2026-09-22..2026-09-25`;
  single-writer truth `logs/x_radar_backfill/alerted.jsonl` (B2-465 dual-survivor heal,
  pattern stolen from gap_sentinel). Re-run verified: "already on file, not duplicated".

## Known limit (ownership respected)

`mag/x_reply_radar.py` `emit()` rewrites `x_radar.json` wholesale every daily run, wiping
HOLES; that file is NOT this lane's to fix. `x_radar_gaps.json` is the durable record;
re-running the backfill re-injects HOLES. Both JSONs validated to parse off disk bytes.
