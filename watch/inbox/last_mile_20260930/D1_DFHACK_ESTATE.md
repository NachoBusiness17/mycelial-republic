# D1 — The Estate Through Its Own Admin Console (DFHack dogfood)

Owner of record: D1 (file ownership per dispatch). Session 2026-09-30 ~19:00.
Mission (operator): "df hack dogfood" — run the DFHack tools we built ON the estate
itself. The estate IS the world; this receipt IS the chronicle.

Commands actually run (all byte-backed, exits noted):

```text
.venv/Scripts/python.exe tools/mountain_legends.py replay logs/world_server.jsonl          # exit 0
.venv/Scripts/python.exe tools/mountain_reveal.py prospect --from-replay logs/world_server.jsonl   # exit 0 (PARTIAL degrade)
.venv/Scripts/python.exe tools/mountain_reveal.py events 6 --from-replay logs/world_server.jsonl   # exit 0 (PARTIAL degrade)
.venv/Scripts/python.exe tools/mountain_units.py units --ticks 600 --player hunt           # exit 0
```

Estate numbers below were measured this session (psutil + Win32_Process +
`stat` over `logs/`). Nothing is estimated.

---

## 1. LEGENDS — the chronicle of the estate's own mountain

`mountain_legends.py replay logs/world_server.jsonl` — the estate's REAL chained
log (103 tick rows, written 2026-09-30 05:32 by the estate's own server):

> **CHAIN VERIFIED** over 103 rows (seq 1..103, tip sha `dc0fb70a8389`). Every
> row seals its parent; this history is byte-true.
>
> | X | 1 | The First Verdict | Junction gate1 passes (p_spring sole inlet) | 1 / `49b4a6a2e74d` |
> | D | 6 | The Spring Fails | spring volume hits 0 at tick 6 |
> | Q | 9 | The Still World | from tick 9 no pipe moves, no gate speaks |
>
> water ledger: first-row sum 7, final 0 — a falling sum with `to waste` events
> names the pre-V5 deletion law

### The sagas of the day (estate epochs, in the legends' names)

**THE LEAK — the mountain that bled to waste.** Two leaks, both measured.
(1) The water: the log's own ledger falls 7 → 0 with `to waste` rows — the
pre-V5 engine DELETED water; drift vs endowment −8 (see prospect). The current
engine refuses to fake compatibility with that fossil (PHYSICS DRIFT → honest
PARTIAL). Trust bytes, not reports — the tool caught the estate's own old bug.
(2) The ink: `logs/` is **1,710,773,863 bytes (1.71 GB)** of leaked history —
`kpi.jsonl` 718 MB alone. The chronicle writes itself faster than it is read.

**THE WALLS.** (1) The 402 wall: the funded Nous lane returns 402 on both prime
models post-rotation — old keys in Hermes `.env` match NEITHER of the repo's
rotated pair (AJ9_NOUS_402.md, all 4 cross-pairs compared, values never printed).
(2) The account wall: `1310, reset 10-05` blocks agent spawns on the z.ai quota
(FULL_BURN_STATE.md). (3) The held walls: the pre-push ratchet + scenario gates
held all day — debt stayed registered, no loosening.

**THE WAVES.** The mates wave: 8 personas (cartographer, locksmith,
archaeologist, innkeeper, jester, lamplighter, mariner, gambiter) dispatched
08:00:02 width 8 — **all 8 caught@~66s, exit=1 by 08:01:09** (runner_20260930.log).
Re-armed with the auth fix: the full burn runs FOUR quotas concurrently, 8/8
CLAIMED and RUNNING fired ~01:50 ET, Nous volley 1 COMPLETE at 8 asks × $0.89
(FULL_BURN_STATE.md). The 09-26 burn/freelane waves are the ancestors.

**THE STILL WORLD.** Dispatcher 15:09:57 rewrote missions `dry=True`; runner
logged "honest no-op, exit 0" at 06:12. Between waves the mountain rests —
but the queue still breathes (see unit 0 below: a verifier spawned 0.1h ago).

---

## 2. PROSPECT — what is the water? (fuel / quota / RAM)

`mountain_reveal.py prospect --from-replay` verdict, verbatim:

> **PHYSICS DRIFT**: seq 1 replay diverges from the logged row — log predates
> current engine — PARTIAL fallback.
> water: 0 total · endowment 8 · **drift −8**
> fracture risk: all pipes 0 stress (a dry board cannot burst)

The estate's own prospect, same grammar (measured 2026-09-30 ~19:00):

| the water question | the estate's answer |
|---|---|
| total water (RAM) | 64 GiB; **83.0% used, 10.8 GiB avail**; swap 23.4% |
| the deep rock (disk) | C: 67.0% used, 614 GiB free of 1,862 GiB |
| the age of the world | uptime **115.2 h** (never rebooted through the waves) |
| the fuel | Nous volley COMPLETE (8 × $0.89 ≈ $7.12); Anthropic keys UNFUNDED; Hermes is the only funded rail |
| the quota walls | Nous 402 on prime models (key rotation mismatch); z.ai 1310 until 10-05 |

**Fracture risks (the loaded pipes), ranked by bytes:**

| pipe | stress | the risk |
|---|---|---|
| `kpi.jsonl` | 718,062,964 B | 42% of the whole logs/ basin on one append-only file |
| `dashboard_sv.err.log` | 179,871,108 B | a 180 MB ERROR stream nobody drained |
| `backend_sv.log` | 84,804,695 B | plus 672 KB of .err beside it |
| `usage.jsonl` + `behavioral_events.jsonl` | 70.6 + 67.4 MB | the usage organs double as flood plains |
| RAM @ 83% + llama runner 6,433 MB | — | one more big model load has 10.8 GiB to stand on |
| fossil world logs | drift −8 | old physics bytes that replay only PARTIAL — compaction debt |

---

## 3. UNITS — the fleet as fish

Tool truth first (`mountain_units.py units --ticks 600 --player hunt`): under a
hunting cursor every fish fled, fatigued, was carried, and **all 12 caught by
tick ~325; population: dead 12, headroom 45**. That is the 08:00 mates story in
miniature — the cursor was the auth wall.

The live fleet, in the tool's own column grammar (INT = RAM MB, the honest
intensity this rig can measure; AGE from Win32_Process CreationDate; TRN not
measurable cross-process, marked "-"; mapping is labeled, never invented):

```text
ESTATE UNITS - tick 2026-09-30 19:00 - player hunt (the quota cursor)
 ID  STATE    INT   TARGET                              AGE      NOTE
  0  pursue     25  w-nelson-shuffle VERDICT            0.1h     hermes -z "funded-tier VERIFIER... free-lane dispatches are SENSED, never DONE" (pid 43356)
  1  carry       5  governor_autorun loop (5.0s)        0.6h     mag.governor_autorun autorun_loop (pid 53952)
  2  dance     399  Hermes renderer                     69.3h    cpu 2241s; desktop 49776 + gpu 41672 (the throne's face)
  3  carry     205  hermes serve 127.0.0.1              69.3h    gateway 45392 + serve 46844 (cpu 4785s) — dormant no longer
  4  dance    1994  ZCode app-server (this seat)        37.6h    pid 37112, cpu 3942s — the observer fish
  5  idle       37  ollama serve (janitor tier)        115.2h    pid 11112, up since boot
  6  idle       61  llama-server :8080 (estate organ)   68.3h    tools/llamacpp on a .ollama blob
  7  carry      21  stealth driver (sensing lane) x2    31.6h    run_stealth_driver.py x2 (49400/54484)
  8  carry       0  interference armC replication       85.3h    run_armC.py x2, spawned 2026-09-25, still coasting
  9  idle       41  Docker Desktop + wsl                -        the /board surface, open but quiet
 caught@08:01  -   8 mates, exit=1, ~66s after launch    -        cartographer..gambiter; re-armed by FULL_BURN
 population: pursue 1 · carry 4 · dance 2 · idle 3 · dead(morning) 8 · headroom: unbounded (spawns walled until 10-05)
```

Foreign fish in the water (named, not counted as fleet): `fle_u1` inspect eval
on `ollama/qwen2.5-coder:7b` (pids 556/43824) — a sibling project drinking from
the same ollama spring.

---

## 4. The estate as DF sees it (the honest close)

A 103-row hash-verified mountain whose spring died at tick 6 under a deletion
bug, went Still at tick 9, and left a fossil the current engine honestly refuses
to fake. Above ground: 1.71 GB of leaked ink, walls on two quotas, and a fleet
that got caught once at 08:00 and re-fired by night — one funded verifier fish
actively pursuing a verdict while janitors idle and a 1994 MB observer watches.
The console held: chain verified, drift named, every intensity measured.

**Mapping law:** blocks quoted from tool stdout are literal (exits in the
header); saga names, the prospect table, and the units table are the labeled
metaphor layer — every value in them measured this session, sources cited inline.
