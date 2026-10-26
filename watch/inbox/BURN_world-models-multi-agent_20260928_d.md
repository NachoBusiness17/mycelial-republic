## Verdict

green

## Evidence

Code fix landed (Edit tool, 2026-09-28 01:02:25 -0400 mtime). The map entry as applied, mag/run_trail.py `_SEAT_MAP` (after the cursor block): `"research": "research",`. normalize_seat (73-80) is unchanged; the map values check `key in _SEAT_MAP.values()` now passes "research" through instead of collapsing it to "local".

Parse result: `ast.parse` on mag/run_trail.py returned PARSE_OK via the repo venv interpreter. Live import smoke: `normalize_seat("research") -> research`, `normalize_seat("local") -> local` (no regression on the existing seat).

Stale-import confirmed, byte-read. mag/lane_runner.py:110 holds `st.setdefault("seat", lane)` on disk. queue/lanes/research/runner_state.json: last_run "2026-09-28T04:48:50.025613+00:00" (mtime 2026-09-28 00:48:50 -0400), keys exactly inbox_offset, last_run, last_day, last_result, no seat key. That save postdates the lane_runner setdefault commit (2026-09-27 22:53:18 -0400, per the c receipt) by about two hours, yet minted no seat key: the writer process is executing pre-commit code. The last related_runs.jsonl write is 2026-08-02 19:39:03 -0400, dormant for near two months, so the ledger adds nothing recent; runner_state is the live heartbeat. My run_trail.py edit (01:02:25 -0400) postdates the last runner save (00:48:50 -0400) by 14 minutes, so the running process has also never loaded the new map. Finding, stated plainly: the driver process must restart to pick up the lane_runner setdefault and the new _SEAT_MAP entry. Nothing was restarted (read-only pass on processes, per order).

WebSearch "seat map normalization trail" (2026-09-28): thin. Results drifted to airline seat maps, StandardScaler notebooks, database normalization lectures. Nothing on agent-seat normalization or shared human+agent sims read in full.

## Steal or Vacuous

Steal, small. The fleet adopts the landed invariant: seat canon lives in one map, `_SEAT_MAP` in mag/run_trail.py; a new seat is one map line, never a normalize_seat branch. The runner-side setdefault (lane_runner.py:110, seat from lane name) is now trusted but inert until a driver restart reloads it. NPC=SEAT canon: a research-seat trail can only mint a seat=research bond row through the normal path, start_run -> trail -> close_run -> related_run_card -> related_runs.jsonl -> bonds. Hand-appended cards stay fabrication; replay of the 13 dormant rows (local/grok_tui) re-stamps their stored seats and cannot seed research. Owed from the prior pass is now paid: the stale-import hypothesis is confirmed by timestamp math, not guessed.

## Falsifier

One real research-seat run after a driver restart. Restart the research lane driver so it loads both landings, then drive one research-purposed goal through start_run(seat="research") and close_run. Falsified if the resulting row in memory/runs/related_runs.jsonl reads seat "local" or "grok_tui" instead of "research", or if a post-restart runner_state.json save still lacks a seat key. Verified if the row reads "seat": "research" and surfaces in bonds_meta.related_by_seat on next refresh. Until that byte-read row exists, the bond-row precondition stays pending on the restart.

## Bibliography

- watch/inbox/BURN_world-models-multi-agent_20260928_c.md (read 2026-09-28)
- mag/run_trail.py lines 40-89, _SEAT_MAP and normalize_seat as edited (read 2026-09-28)
- mag/lane_runner.py lines 95-129, the line-110 setdefault (read 2026-09-28)
- memory/runs/related_runs.jsonl last row tail (read 2026-09-28)
- queue/lanes/research/runner_state.json full content (read 2026-09-28)
- stat mtimes: mag/run_trail.py, runner_state.json, related_runs.jsonl (read 2026-09-28)
- WebSearch "seat map normalization trail", 2026-09-28, thin: airline-domain noise, nothing read in full
