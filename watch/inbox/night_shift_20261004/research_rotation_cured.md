# RESEARCH LANE ROTATION CURED - night shift 2026-10-04 (free lane, $0)

Seat: night shift free-lane repair. No paid APIs touched. One live cycle fired as proof.

## Before / after (byte-backed, watch/room.jsonl rows)

| moment (UTC) | row | term resolution |
|---|---|---|
| 2026-10-04T00:33:27Z | last yield of the old window | 21 new across 6/7 terms (the last time the lane found anything) |
| 2026-10-04T05:42Z..08:37:44Z | ~20 consecutive runs | 0 new items across 0/7 terms, every run |
| 2026-10-04T08:40:36Z | cage daemon runs the new code on the seeded streaks | epoch=7, all 7 terms rotated out/in, 0 new (rotation fires post-poll) |
| 2026-10-04T08:45:03Z | host proof run `.venv\Scripts\python.exe mag/lane_runner.py --lane research --once` | 45 new items across 6/7 terms (hn=37, arxiv=8, openalex=0) |

45 items banked in watch/scout/MONITOR_LANE_2026-10-04.md under the fresh terms (run header 08:44:23Z). queue/lanes/research/trail.jsonl MONITOR row 08:45:03Z carries the same numbers; dashboard/static/trails/research.jsonl mirrored.

## Diagnosis - the actual failure mode TODAY (all three suspects present, one primary)

1. PRIMARY: dedup-saturation blindness. The same 7 terms (watch/monitor_terms.json, unchanged since 2026-09-04) polled so long that per-term seen lists held 119-217 ids (720 total). HN live-probed HTTP 200, arXiv unboxed since 04:43Z - both healthy and both returning only already-seen ids. Byte-backed streaks derived from spool + room history: 6 terms at 115 consecutive blank runs, "speculative decoding MLX" at 467.
2. SECONDARY: openalex boxed, and the box is HONEST, not stale. Live host probe at 08:31Z: HTTP 429 with body "Insufficient budget. This request has no API key, so it counts against the free daily budget shared by everyone on your network's IP address, and that budget is used up ($0 remaining; resets at midnight UTC)", retry-after ~15.5h, x-ratelimit-limit 1000. Decision: NOT unboxed - unboxing would only re-trip the 429 and feed the penalty. The 3600s breaker retries hourly and self-heals at UTC midnight. No key exists in .env (free lane would not use one anyway).
3. TERTIARY (cage-only, NOT cured tonight, out of scope): the in-cage daemon intermittently fails `EXC OSError: [Errno 22] Invalid argument: '/app/queue/lanes/research/runner_state.json'` when saving lane state (queue/ mount write flakiness in the cage). Host-side writes succeed. Flagged for a cage-seat window.

## The rotation law (one-liner)

A term with 0 new items for 3 consecutive runs rotates OUT and the least-recently-used pool term (never-used first) rotates IN; the window stays 7 wide, seen-ids survive rotation, the epoch counts swaps in watch/monitor_lane.state `_rotation` and is mirrored to the research lane state as `rotation_epoch`.

## What changed

- watch/monitor_lane.py - spec docstring first, then: DEFAULT_POOL (21 terms = the 7 standing + 14 derived from mag/arxiv_harvest.py INTEREST_MAP), POOL_FILE watch/monitor_term_pool.json (auto-seeded, on disk now), ROTATE_AFTER_BLANK=3, ACTIVE_TERMS=7, pure `rotate_terms()` (no IO, the test surface), `load_state()/save_state()` now carry `_rotation` {epoch, ledger, blank} beside `_cooldown`, run_once advances streaks from per-term yields, rotates, persists the new window, and prints the rotation fact as the last stderr line so the lane trail's tail keeps it; room rows carry `epoch=N rotated=out>in/...`.
- mag/lane_runner.py - cycle_research lifts `_rotation.epoch` from watch/monitor_lane.state into queue/lanes/research/runner_state.json as `rotation_epoch` (read-only mirror, silent-fail). Current value: 7.
- watch/monitor_lane.state - seeded `_rotation.blank` from byte history (spool per-term last yields + room.jsonl run count): 6 terms at 115, one at 467. All 720 seen-ids and cooldowns preserved. The 08:40:36Z cage run consumed the seed and stamped ledger entries 1-7.
- tests/test_monitor_lane_rotation.py - NEW, 6 tests: streak advance/reset, never-used-then-oldest ledger order, hand-added (--add) terms never rotate out, pool-exhausted keeps the window full, state roundtrip preserves `_rotation`, and a no-network run_once integration (fake source, tmp paths).

## Tests

`.venv\Scripts\python.exe -m pytest tests/test_monitor_lane_rotation.py tests/test_lane_runner_cluster.py tests/test_scripts_path_pins.py tests/test_hunger_ledger_parity.py tests/test_lite_lane_pull_20261003.py -q` -> 48 passed. Pre-existing research-named test files (test_deep_research_moonshot, test_perplexity_research, test_research_fold, test_socratic_research, test_warning_monitor) target other modules; grep tests/ for monitor_lane/cycle_research found zero prior coverage.

## Notes for the next window

- "stigmergy swarm coordination" yielded 0 on its first run (blank=1); if it stays dead 3 runs it rotates out by itself - the law is self-cleaning.
- The 7 standing terms are pool members 0-6 and return via the ledger once their stamps become the oldest; nothing is lost, only parked.
- OpenAlex unblocks itself at UTC midnight; do not unbox manually before then.
- Not committed, per night-shift instruction.
