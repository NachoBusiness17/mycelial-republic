# B2-261 mimo watch arm-or-decline with delete-at-close (SW-07, 2026-09-26)

## Verdict

LANDED (ARMED, with the end-of-life half bound in the same decision). The filed-but-uninstalled scheduler line from B2-235 is now installed as MagMimoWatchHourly, and the append-forever tail (tools/mimo_watch.py writing "probe": "window-closed" rows once hours_left <= 0, lines 158-166) is bounded by a paired one-shot task MagMimoWatchClose that deletes BOTH tasks at 2026-09-28T21:25Z, 6 minutes after window close 2026-09-28T21:19Z. The task buys state history, not lane access: the live fire this lane ran recorded serve down (opencode not armed on 127.0.0.1:4096), consistent with the 403 FreeTierError client-lock story in B2-236; B2-253 still owns the transport decision.

## Evidence file:line quotes

- QUEUE.md row: "install `schtasks /create /tn \"MagMimoWatchHourly\" ...` or consciously decline before window close 2026-09-28T21:19Z, and in the same decision bind the end-of-life half (`schtasks /delete /tn \"MagMimoWatchHourly\" /f`) because tools/mimo_watch.py:118-121 keeps appending window-closed rows forever once hours_left hits 0".
- tools/mimo_watch.py:158-166 (current numbering): `if hours_left > 0: row.update(_serve_probe()) else: row["probe"] = "window-closed"` then unconditional `with LEDGER.open("a"...)` append -- the forever-append the delete binding kills.
- Install output: `SUCCESS: The scheduled task "MagMimoWatchHourly" has successfully been created.` and `SUCCESS: The scheduled task "MagMimoWatchClose" has successfully been created.`; query shows `\MagMimoWatchHourly` Next Run Time 9/26/2026 4:58:00 PM Status Ready and `\MagMimoWatchClose` Next Run Time 9/28/2026 5:25:00 PM Status Ready (local = EDT; 9/28 17:25 EDT = 21:25Z).
- Close task /tr bytes: `cmd /c schtasks /delete /tn MagMimoWatchHourly /f & schtasks /delete /tn MagMimoWatchClose /f` -- deletes the watch AND itself, leaving zero surviving tasks after close.
- Live fire this lane: `[mimo-watch] 2026-09-26T19:58:13+00:00 hours_left=49.3 skipped lane idle: opencode serve not reachable on 127.0.0.1:4096 (operator arms it)`; ledger row appended `"probe": "skipped", "serve": "down"` -- state history accruing as designed.

## Work done

- Armed MagMimoWatchHourly: hourly single-shot python run of tools/mimo_watch.py, exact command shape from the B2-235 filed line.
- Bound the end-of-life half: MagMimoWatchClose one-shot at 2026-09-28 17:25 local (21:25Z, 6 min past close) running the double delete (watch + self).
- Fired one watch run by hand to prove the wiring end-to-end; the row landed in the mimo watch ledger with an honest serve-down result.
- Decision recorded: ARM over decline because the probe is a zero-cost local command with the key already on disk (root .env OPENCODE per B2-235), state history feeds the B2-253 transport decision, and the close task removes the forever-append exposure the brief named.

## Falsifier

From the brief: "a row with ts after 2026-09-28T21:19Z lands with neither a decline receipt nor the task deleted" -- falsified here by construction if the close task fires: after 2026-09-28T21:25Z both `schtasks /query /tn MagMimoWatchHourly` and `/tn MagMimoWatchClose` must error "does not exist". Reopen if: a window-closed probe row (probe == "window-closed") ever lands in the mimo watch ledger (means the close task failed or was disabled), or the close time is found later than 21:19Z close plus a tolerance the next auditor accepts.

## Bibliography closed

Read: tools/mimo_watch.py (probe + main append block), watch/inbox/burn_wave_20260926/B2_235_mimo_revival_20260926.md (filed schtasks line, key source), watch/inbox/burn_wave_20260926/B2_236_mimo_retest_20260926.md (cited via QUEUE row), QUEUE.md B2-261 row, live schtasks query/create outputs, one live watch run. No external sources.
