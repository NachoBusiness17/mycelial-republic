## Verdict

vacuous

## Evidence

Bond-source census (memory/runs/related_runs.jsonl, 13 rows, grep 2026-09-28): seats are 12 `"local"` + 1 `"grok_tui"`, zero `"research"`. Repo grep for `"seat": "research"` across memory/runs/: zero hits. No artifact on the bond path carries seat=research.

The seat-stamping writer the g receipt left owed is now byte-read. mag/run_trail.py:814-831 `related_run_card` passes `"seat": run.get("seat")` verbatim; `close_run` calls `append_related_run(card)` at 868 into `RELATED = RUNS / "related_runs.jsonl"` (line 31); mag/bonds.py:290-296 ingests via `list_related_runs`. The writer exists, but the value is capped upstream: start_run line 387 `seat = normalize_seat(seat)`, and normalize_seat (73-77) ends `return "local" if not key else key if key in _SEAT_MAP.values() else "local"` with `_SEAT_MAP` values exactly local/remote/grok_tui/hermes/human/cursor (46-60). "research" is not canonical; it collapses to "local".

Runner half: mag/lane_runner.py:110 `st.setdefault("seat", lane)` is committed (a23928aca, 2026-09-27 22:53:18 -0400 = 02:53:18Z). run_lane saves state every cycle (1067-1069). Yet queue/lanes/research/runner_state.json (last_run 2026-09-28T04:01:49.933746+00:00) holds only inbox_offset/last_run/last_day/last_result. Trail and state mtimes (00:01:49.841 / 00:01:49.941 -0400) prove one run_lane pass wrote both 68 minutes after the commit, so the ticking process ran pre-commit code: a long-lived driver holding a stale import. Owed, unverified (read-only pass, no processes inspected).

Nearest live trail: queue/lanes/research/trail.jsonl, 2131 lines, mirror dashboard/static/trails/research.jsonl (2131), last tick 2026-09-28T04:01:49Z, actor `research-cage`, event MONITOR. Lane trail events never touch append_related_run; the lane trail cannot seed a bond row by itself.

## Steal or Vacuous

Vacuous: no existing trail close can seed a seat=research bond row, and replay through the current pipeline is structurally impossible, not merely absent. A replayed close re-stamps the run's stored seat (all 13 rows are local/grok_tui); a fresh honest run with seat="research" is normalized to "local" before the record exists; hand-appending a card would be fabrication. The runner_state half is replay-legit: the next research tick after the driving process restarts mints seat=research via the landed setdefault. The bond-row precondition is new-code-required: one line, `"research": "research"` in `_SEAT_MAP`, then one real research-purposed goal through start_run(seat="research") plus close_run seeds the card, which flows into bonds on next refresh and surfaces in bonds_meta.related_by_seat. Until that lands, the b-receipt falsifier stays pending on a precondition no existing artifact can satisfy.

WebSearch "bond row seeding replay pipeline multi-agent shared state 2026": thin, one snippet-level hit, nothing read in full.

## Bibliography

- watch/inbox/BURN_world-models-multi-agent_20260928_b.md (read 2026-09-28)
- watch/inbox/BURN_world-models-multi-agent_20260927_e.md (read 2026-09-28)
- mag/run_trail.py lines 40-77, 810-870, 975-1000, seat grep trace (read 2026-09-28)
- mag/lane_runner.py lines 95-134, 1048-1070, research grep, git log -S setdefault (read 2026-09-28)
- mag/bonds.py related_runs ingestion grep, lines 290-296, 449 (read 2026-09-28)
- memory/runs/related_runs.jsonl full seat census (read 2026-09-28)
- queue/lanes/research/trail.jsonl tail, runner_state.json, mtimes (read 2026-09-28)
- dashboard/static/trails/ listing, research.jsonl line count (read 2026-09-28)
- WebSearch "bond row seeding replay pipeline multi-agent shared state 2026", 2026-09-28, thin: snippet-level only, [Dicklesworthstone/franken_node](https://github.com/Dicklesworthstone/franken_node), nothing read in full
