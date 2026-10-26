# arch-03: stealth_driver v2 design

Item: arch-03 | 2026-09-28 | seat: mirror-arch-03 (flash50, z.ai)
Source read fully: `tools/stealth_driver.py` (880 lines, HEAD f48e5aaa6 lineage, working tree clean at ask start).
Method: full file read + live-state instruments (commands and outputs in section 7). Read-only session: no driver code or live state was modified, no process killed.

## 0. What the driver is today (as-built)

A 12-topic loop, every topic run every cycle, cycle nominally 300s (`CYCLE_SECONDS`, tools/stealth_driver.py:68), stagger 2s per topic (tools/stealth_driver.py:849), one heartbeat JSONL row per cycle (tools/stealth_driver.py:850-852). Control is the `.off` flag (tools/stealth_driver.py:516-517, 864-868). Topics (tools/stealth_driver.py:826-839): prompt_lance, selfimp, selffeed, work, probe20, rumor, fossil, chain, roster, stealth_driver, fkb, backlog. Network boundary: exact URL allowlist + public-IP resolution + no redirects for GETs (tools/stealth_driver.py:96-111) and a POST allowlist for work dispatch (tools/stealth_driver.py:495-513). Work rides the free-first ladder with per-lane 30-min spacing (tools/stealth_driver.py:334-344), LESSIG rails (budget retry 4x on length, reasoning-tail banking, stable cache prefix, ponytail path audit; tools/stealth_driver.py:143-148, 415-427, 442-446), Q-036 effort dial (tools/stealth_driver.py:161-172).

## 1. Measured baseline (live, 2026-09-28T22:44:13Z to 23:30:43Z)

Instrument: `watch/inbox/burn_reset_20260927/flash50/_arch03_instrument.py` run with `.venv/Scripts/python.exe` (output in section 7). Heartbeat `state/fuel/stealth_driver.jsonl`: 9 rows, cycles 56-64.

Cadence: consecutive deltas min 332s / median 348s / max 612s. Nominal 300s sleep plus cycle work; the 612s outlier is a hermes dispatch (600s timeout, tools/stealth_driver.py:274) landing inside a cycle. Real cadence is 332-612s, never 300s.

Topic outcomes over 9 cycles:

| topic | ok | err | skip | live note |
|---|---|---|---|---|
| prompt_lance | 9 | 0 | 0 | info-grade findings, cheap |
| selfimp | 0 | 0 | 9 | queue drained (16/16 done), zero feeders exist |
| selffeed | 0 | 9 | 0 | every cycle: `ERR rc=1 The system cannot find the file specified.` |
| work | 7 | 2 | 0 | 7 of 9 cycles sensed the SAME item (lib-belady-1966) |
| probe20/rumor/fossil/chain | 9 | 0 | 0 | healthy, each one bounded subprocess |
| roster | 9 | 0 | 0 | groq 403 all 9 cycles; llm7=64, openrouter=460 |
| stealth_driver | 9 | 0 | 0 | output duplicates roster's same-cycle diff |
| fkb | 9 | 0 | 0 | top-sig line, cheap file read |
| backlog | 9 | 0 | 0 | half its output self-describes as history |

Six live defects, each code-cited:

- D1 SENSED-never-DONE re-dispatch loop. `_next_work` selects rows lacking `done_ts` (tools/stealth_driver.py:295-298); `t_work` marks rows `status: sensed` and never writes `done_ts` (tools/stealth_driver.py:483-488); the only `done_ts` writer in the file is the SELFIMP queue marker (tools/stealth_driver.py:740). Measured: work queue has 13 rows, 13 without done_ts, and lib-belady-1966 was re-sensed in 7 of 9 cycles across rotating lanes; 37 files sit in `watch/inbox/burn_reset_20260927/work/`, most copies of that one item. The queue cannot shrink by consumption, only grow by selffeed: the docstring line "The queue never drains - it grows" (tools/stealth_driver.py:786-787) is the bug stated as a feature.
- D2 selffeed is dead in situ: 9/9 ERR. `t_selffeed` runs every cycle regardless (tools/stealth_driver.py:829) and burns a hermes dispatch (up to 600s) to fail. Two selffed rows (m1, m002) prove it worked at least twice earlier under a different invocation context; id formats already drifted (m1 vs m002), so even its success path had no id discipline. `tests/test_selffeed_integration.py:39-51` pins only "appends a line when hermes is up" and cannot catch this failure mode.
- D3 `t_stealth_driver` (tools/stealth_driver.py:749-779) is a duplicate: it re-reads `configs/mirrors.json`, which `t_roster` rewrote seconds earlier in the same cycle (tools/stealth_driver.py:603-638, including the `diff_line` field at :632). Live proof: roster says "groq=ERR(403) llm7=64 openrouter=460"; stealth_driver same cycle says "groq: unreachable stable | llm7: 64 stable | openrouter: 460 stable". Zero added bits, 9 runs per 45 min. Only reader of mirrors.json in live code is the driver itself (grep, section 7).
- D4 groq roster host 403s every cycle (9/9) with its key header attached (tools/stealth_driver.py:583-589). Dead weight plus one 15s timeout per cycle.
- D5 Two concurrent driver instances + heartbeat retention anomaly. `wmic process where "name='pythonw.exe'"` shows TWO PIDs running `scripts/run_stealth_driver.py`: 55528 (.venv pythonw) and 55068 (uv cpython-3.11 pythonw). The shared stdout log has 8 untimestamped "loop start" lines. The heartbeat holds only cycles 56-64 although the cycle counter reached 64, and the only code write to it is an append (tools/stealth_driver.py:850-852); the loss mechanism for cycles 1-55 is UNVERIFIED from here. Concurrent instances make every read-modify-write surface unsafe: lane spacing `stealth_work_state.json` (whole-file writes at tools/stealth_driver.py:363, 433, 448-457) and `_mark_work` tmp-replace (tools/stealth_driver.py:301-309) are last-writer-wins, the exact hazard class already documented for context_pack_latest.md (s2-08 receipt). The same doubling pattern hits sibling boot-lane launchers: two PIDs also run `memory/runs/interference_replication_20260925/run_armC.py` (40980, 42364).
- D6 Hollow claims. The mined row note "percolator/quantizer may ingest" (tools/stealth_driver.py:477) names no real module: `mag/quantizer.py` does not exist (mag has auto_quantize.py, state_quantizer.py, tool_quant.py), and grep of mag/percolator.py for mined ingestion returns nothing. The ponytail audit regex (tools/stealth_driver.py:444-446) matched 0 repo paths across the 102 direct-API rows of the 151-row mined register: the audit runs as designed but is a measured no-op on research-shaped asks. Nothing consumes `state/fuel/stealth_driver.jsonl` (zero live-code readers, grep).

Queue economics at measurement: 13 open rows (11 manual + 2 selffed), consumption capacity ~7-9 dispatches/hour when lanes are healthy (7 free lanes x 30-min spacing, tools/stealth_driver.py:340), but 100% of live consumption re-burned one row (D1). Lane error ledger: nous 402 Payment Required, nous read timeout, llm7 400, openrouter 403, openrouter empty-content (state/fuel/stealth_work_state.json, instrument output).

## 2. v2 topic table

Verdicts: KEEP, KEEP-CHANGED, REMOVE, ADD. Cadence is per-topic (section 5).

| topic | v2 | cadence | grounding |
|---|---|---|---|
| prompt_lance | KEEP | every tick | 9/9 ok, deterministic $0 (tools/stealth_driver.py:665-683) |
| work | KEEP-CHANGED | every tick | add the DONE gate, per-lane dedupe, and a 3-copy divergence cap (section 4) |
| verify | ADD | hourly | closes D1; the missing funded-tier rung (section 3.1) |
| selfimp | KEEP | every tick, cheap skip | build arm; stays drained-safe (tools/stealth_driver.py:705-746) |
| impfeed | ADD | weekly inside daily slot | feeds selfimp from mined STEALABLE ideas (section 3.3) |
| selffeed | KEEP-CHANGED | hourly, bounded | 7 rails in section 4; today 9/9 ERR and unbounded by design |
| probe20 | KEEP | every tick | measurement stream; skip-fast when llama down is healthy (tools/stealth_driver.py:540-545) |
| rumor | KEEP | 15 min | deadline watch with hour granularity (tools/stealth_driver.py:548-553) |
| fossil | KEEP | 15 min | staleness eyes, 9/9 ok |
| chain | KEEP | hourly | verify-only dry run; hourly is plenty (tools/stealth_driver.py:564-569) |
| roster | KEEP-CHANGED | hourly | drop groq (D4); keep its own diff_line write; hosts llm7 + openrouter |
| stealth_driver | REMOVE | - | duplicate of roster (D3) |
| fkb | KEEP | 15 min | remedy-bridge pressure line, cheap |
| backlog | KEEP-CHANGED | daily | drop the dead B2 board half, keep queue_index census |
| selfwatch | ADD | every tick + external probe | dead-man for the loop itself (section 3.2) |

## 3. New topics spec

### 3.1 verify (the missing tier-2 rung)

Law it implements: RIB_DRIVING_LADDER_20260928 (memory/rib/, cited in AGENTS.md): a free-lane dispatch is SENSED, never DONE; verification climbs to the funded tier. The code agrees in its own comment (tools/stealth_driver.py:486-489) and then implements nothing: no path flips `done_ts`. v2 shape: hourly, take the oldest row with `status: sensed` and no verdict, read its banked answer file from `watch/inbox/burn_reset_20260927/work/`, dispatch ONE funded-lane ask (hermes or nous scarce5) that checks the answer's claims against the repo (the ponytail path check generalized) and returns verdict DONE / OWED / diverged; write `done_ts`, `verdict`, `verifier_lane` into the row. This is the only mechanism that actually drains the work queue, and it converts the existing 37-copy pile into a reviewable census instead of waste.

### 3.2 selfwatch (the loop watching its own pulse)

The loop can die silently: 8 restarts in the log, heartbeat history truncated (D5), and zero consumers of the heartbeat file. In-loop part (cheap, honest): each cycle refresh `state/fuel/stealth_driver_alive.json` with ts + pid + cycle; also enforce single-instance via `state/fuel/stealth_driver.lock` (pid + boot time; a second starter exits if the lock is fresh, takes over if stale), which kills the D5 double-instance class at the root. Out-of-loop part (stated plainly): a loop cannot detect its own death, and the boot-trigger law says timed schedules never work here (tools/stealth_driver.py:4-5), so the external probe must ride a surface that already runs: the cheapest honest option is one heartbeat-age check folded into the existing daily scheduled tasks (MagCensusPatrolDaily-style, per AGENTS.md B2-246 line) or into `python -m mag.hermes_warm_boot` at session start; the probe alerts when alive-file age exceeds 3 nominal ticks. I did not implement or schedule anything in this session; this is the design.

### 3.3 impfeed (feed the build arm from the mine)

The selfimp queue has zero feeders (grep, section 7) and sits drained 16/16, while the mined register accumulates 151 rows each carrying a mandated "STEALABLE idea" field (MINING_PREAMBLE, tools/stealth_driver.py:143-146). v2: weekly, batch the week's mined rows, one funded dispatch ranks the stealable ideas, and the top candidate is appended to `state/fuel/stealth_selfimp_queue.jsonl` as a build item. This closes mine -> investigate -> build without the operator, which is the Mickey17 closure the selffeed docstring reaches for (tools/stealth_driver.py:783-787). Also fix the D6 note: either name the real ingester or drop the "percolator/quantizer may ingest" claim.

### 3.4 Considered and rejected

- Repo census / drift-patrol topics: violates the header law "Nothing here invents work; it rotates work that already exists" (tools/stealth_driver.py:7-8) and duplicates fossil_check plus tools/census_drift_patrol.py.
- Removing rumor/fossil/chain to save time: each is one bounded subprocess, 9/9 ok; the cost problem is cadence (section 5), not existence.
- A second driver process dedicated to the verify tier: rejected; the single-instance lock (3.2) is the law, verify rides the same loop.
- Token-budget-only bounding of selffeed: does not bound queue growth; row caps and depth caps do (section 4).

## 4. Selffeed v2: the bounded loop

Today's selffeed (tools/stealth_driver.py:782-823) runs every cycle, asks hermes to propose one item, and appends unconditionally on success: no cap, no dedupe, no depth limit, no ttl. At the nominal 300s cadence that is up to +12 items/hour against ~7-9/hour consumption: designed-to-grow. v2 rails:

1. Trigger gate: selffeed fires only if the work topic sensed a NEW item this tick (selffeed today runs even when work skipped or errored; TOPICS order at tools/stealth_driver.py:826-839 is unconditional), and at most once per hour (spacing stamp in stealth_work_state.json).
2. Open-queue cap: skip when open rows >= 20. Measured consumption capacity is 7-9/hour, so 20 open is over 2 hours of buffered work; beyond that, proposing more is inventory, not work.
3. Depth cap: every row carries `depth` (manual seeds = 0; selffed = parent depth + 1); max depth 2. The ask text must state the current depth and demand a TESTABLE-hypothesis-only reply at depth 2, so an investigation of an investigation can spawn at most one more level.
4. Dedupe gate: before append, cheap similarity check of the proposed ask against open asks (difflib ratio > 0.6 drops it) plus id discipline: selffed ids are `m%03d` unique against existing ids (live ids already drifted m1 vs m002).
5. TTL: rows carry `queued_ts`; a row not sensed within 24h is reaped to `status: expired` by the verify topic's sweep, so the bounded queue cannot silt up.
6. Circuit breaker: 3 consecutive selffeed failures auto-suspend the topic for 12h (stamped in stealth_work_state.json). Today a dead selffeed costs a 600s-timeout hermes dispatch every single tick (D2: 9/9 ERR) for nothing.
7. Contract unchanged where it works: malformed or missing-field JSON is already dropped (tools/stealth_driver.py:808-818); keep that, add depth/parent_id/ttl to the schema and to tests/test_selffeed_integration.py, which currently pins only append-shape (tests/test_selffeed_integration.py:62-79).

## 5. Optimal cycle time

Measured facts: nominal 300s tick; real per-cycle wall 332-612s (median 348s); the stagger alone is a fixed 22s (12 topics x 2s, tools/stealth_driver.py:849); heavy topics (hermes dispatches up to 600s, work POST up to 300s plus one 4x retry, tools/stealth_driver.py:274, 513, 415-416) can overrun the sleep. A uniform 300s run-everything cadence is the wrong shape because topic natural rates span three orders of magnitude: prompt_lance is seconds, roster churn is hours, backlog census is days (its own output says the board it reads drained 09-27, tools/stealth_driver.py:702).

v2: keep the 300s base tick (it matches the operator's flash-job pattern, cited at tools/stealth_driver.py:68) but make it a scheduler tick with per-topic intervals, not a full run:

- every tick (5 min): prompt_lance, work, probe20 (skip-fast), fkb, selfwatch stamp
- 15 min: fossil, rumor, fkb if not already run is fine at 15
- hourly: roster (groq removed; 2 hosts), chain, verify, selffeed (bounded, section 4)
- daily: backlog census (queue_index only); weekly inside that slot: impfeed

Arithmetic (stated as estimates derived from the measured cadence): heavy hermes-family dispatches drop from up to 288/day (selffeed alone at 5-min cadence, each up to 600s) to at most ~26/day (24 selffeed-or-verify hourly + bounded retries); roster GETs drop from 288 to 24 per host. Tick wall time stays under the sleep because the 600s-class dispatches leave the every-tick set, and the observed 612s overrun class disappears from the common path. The cycle counter and heartbeat row gain a `ran` field listing the topics that fired that tick, so heartbeat consumers can audit the schedule.

## 6. Landing order (all behind the .off law; none executed in this session)

1. Single-instance lock + kill the duplicate instance (operator word; D5 is corrupting shared state today).
2. DONE gate: verify topic + divergence cap + per-lane dedupe in t_work (D1; this is where the estate stops paying 7x for one item).
3. Selffeed rails 1-7 (section 4), then repair the hermes dispatch root cause that produces the 9/9 rc=1.
4. Remove t_stealth_driver, drop groq from roster, repoint backlog (D3, D4, backlog half).
5. Per-topic cadence scheduler + heartbeat `ran` field (section 5).
6. selfwatch lockfile + external age probe on an existing always-on surface (section 3.2).
7. impfeed + fix the hollow ingester note (D6).

## 7. Evidence appendix (commands run this session)

- Read: `tools/stealth_driver.py` in full (880 lines); `scripts/run_stealth_driver.py` (21 lines); `tests/test_selffeed_integration.py` (92 lines).
- `ls -la` on the 7 driver state surfaces: all present; heartbeat 8076 B and mirrors.json both mtime Sep 28 19:25 (driver live at ask time).
- Instrument: `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_arch03_instrument.py` (banked beside this file). Output: heartbeat rows 8 at run time (9 by the second read, cycle 64 landing mid-session), deltas min 332 / med 348 / max 612s, topic outcome table in section 1, work queue 13 rows / 0 done_ts / 2 selffed, selfimp 16 rows / 0 open, lane_errors 5, cache_stats finishes 49 stop / 1 length, cached_tokens n=21 max=194, mined register 151 rows (hermes 36, openrouter 80, nous 22, manual waves 13), ponytail audit total=0, reasoning-tail banked=0.
- `grep -rln` for the driver's data surfaces across mag/ tools/ scripts/ tests/ main.py: only tools/stealth_driver.py, its pycache, and tests/test_selffeed_integration.py; heartbeat and mined register have zero live-code consumers; mirrors.json readers: driver only; selfimp queue writers: none.
- `grep -n "done_ts" tools/stealth_driver.py`: lines 296, 717 (reads), 740 (selfimp queue only).
- `grep -n "loop start" logs/stealth_driver_stdout.log`: 8 lines, 3 at "cycle every 900s", 5 at "cycle every 300s", untimestamped.
- `wmic process where "name='pythonw.exe'" get processid,commandline`: PIDs 55528 (.venv) and 55068 (uv cpython-3.11) both on scripts/run_stealth_driver.py; PIDs 40980 and 42364 both on run_armC.py.
- `ls mag/ | grep -i quant`: auto_quantize.py, state_quantizer.py, tool_quant.py (no mag/quantizer.py).
- `git log --oneline -3 -- tools/stealth_driver.py`: f48e5aaa6 (selffeed landed), ac47c2180 (Q-036 effort dial), 390814497.
- Not run: any pytest suite, any driver code change, any process kill, any state write. This item is design-only by ask; all fixes are proposals with cited landing order.

Em/en dash scan: run post-write (see receipt line in commit message).
