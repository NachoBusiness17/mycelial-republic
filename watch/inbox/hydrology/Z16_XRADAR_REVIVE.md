# Z16 - X RADAR REVIVE (the scheduler ownership fix landed)

2026-09-29/30 window. Filed per the shared surface contract; receipt before
promotion. No commit made (per order); registration WAS run (per order).

## Root cause (byte-proven, not guessed)

`dashboard/static/x_radar_gaps.json` holes[1]: 2026-09-22..25 are
"writer never ran: zero artifacts (no out_*, no err_*, no card) on those days;
**no in-repo scheduler owns mag.x_reply_radar run**". Confirmed by sweep:
`Get-ScheduledTask` across ALL tasks (not just Mag\*) found zero actions
matching "radar" (2026-09-30). The 09-11..09-29 cards were hand/seat runs
(raw mtimes ~08:05-08:08 daily, with the 4-day hole). The instrument existed;
nothing owned its firing.

## How the radar runs (mag/x_reply_radar.py, read)

Entry: `.venv\Scripts\python.exe -m mag.x_reply_radar run` from repo root
(stdlib-only module; no venv deps). It shells out to the grok CLI
(`~/.grok/bin/grok -p <survey> --no-plan --max-turns 12`, timeout 420 s),
files `memory/runs/x_reply_radar/out_<UTCdate>.json` + `err_<UTCdate>.log`,
then emits `watch/X_REPLY_RADAR_<UTCdate>.md` +
`dashboard/static/x_radar.json`. `parse <raw.json>` re-emits from an old raw.

## What landed (the census -File pattern, mirrored)

1. `scripts/x_radar_daily.ps1` — daily runner: venv + grok-CLI preflight
   (missing = exit 2 cannot-verify), UTF-8 line-streamed `logs/x_radar.log`
   (no Tee-Object, the B2-246 mojibake law), nonzero exit alerts
   `memory/attention.md` with the 402-balance / parse / env response cards.
2. `scripts/register_x_radar_task.ps1` — registers **MagXRadarDaily** at
   **08:00**, the documented original time (`watch/BUILD_REPORT_20260907_NIGHT.md`
   "X radar 08:00"; empirical 08:05-08:08 mtimes = 08:00 starts; mission
   default 08:05 yielded to the documented original). Slot already holds
   MagImproveDaily + MagLeaveProtocolDaily — proven 2-task shape, now 3.

## Registered + verified (2026-09-30 ~05:2x local)

- `schtasks /Create` SUCCESS via `scripts/register_x_radar_task.ps1`.
- `Get-ScheduledTask MagXRadarDaily`: **State=Ready**,
  Action=`powershell.exe -NoProfile -ExecutionPolicy Bypass -File
  <abs>\scripts\x_radar_daily.ps1`, Trigger daily 08:00,
  NextRun 2026-09-30 08:00, LastResult 267011 (never ran — fresh, expected).
- Falls under the census patrol fleet task doctor's morning Mag\* sweep as a
  second net; its own no-START-stamp-today response law is in the script head.

## Hand-run state: SKIPPED, balance-gated (per the order's own cost rule)

The order: "run the radar ONCE by hand if cheap — if it needs a Grok balance,
note it and skip." It needs one: the grok CLI rides a Grok Build usage balance
— `x_radar_gaps.json` holes[0] byte-proves the 402 Payment Required class
(2026-09-09/10, err-log witness). $0 in money, but balance-gated, so the
hand-run is noted-and-skipped. Cheap no-spend proof ran instead:

- `x_radar_daily.ps1` parse-check: OK.
- `import mag.x_reply_radar` under `.venv\Scripts\python.exe`: OK (entry
  confirmed `python -m mag.x_reply_radar run`; `run()` fires only via CLI arg,
  so the import spent nothing).

End-to-end proof rides the first scheduled firing (today 08:00 local, ~2.6 h
after filing). A 402 there is the known balance class: top-up/wait, never
backfill (cost law in the script head). Do NOT hand-run it before 08:00 — it
would double-spend today's balance and steal the firing's proof.

## Files

- `scripts/x_radar_daily.ps1` (new, owned)
- `scripts/register_x_radar_task.ps1` (new, owned)
- `watch/inbox/hydrology/Z16_XRADAR_REVIVE.md` (this receipt)
- `logs/x_radar.log` (will appear at first firing)
