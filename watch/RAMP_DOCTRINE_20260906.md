# RAMP DOCTRINE — arming the BATCH5 concurrency ramp (2026-09-06, r1)

**Self-steal of every swarm/concurrency measurement the fleet owns.** Operator order:
ramp +5 per wave toward 30-50, ceiling 50 concurrent NEVER exceeded, see what breaks.
Every number below is receipted; tri-state tags where the record is thin.

---

## 1. THE RECEIPTS (what we have measured)

### Lane table (BURST_DOCTRINE_20260903, live-measured + corrections)
| Lane | Width | p50 latency | Law |
|---|---|---|---|
| glm-5.3-flash (API credits) | **50/50 in-flight measured**, p50 1.7s @50 vs 1.1s solo | 1.7s | THE burst lane |
| glm-4-32b-0414-128k | 15 | 0.8s (fastest) | many small decisions |
| glm-5.3 (API) | **15** (record corrected 5→15, transcription error) | 1.1s | judgment |
| glm-4.5-flash (free) | 2 | 0.9s short / **11.8s @9Ktok** | 8K tax law — long context dies here |
| glm-4.7-flash (free) | **1** (2nd call = 1302, measured) | 0.8s | single-flight cache mining only |
| Plan door / ZCode (5.3-flash OAuth) | **Unproven past 5** — this ramp's job | ~1s class | night window = zero credits |

### CONC_PROBE_PAST50 (2026-09-04, 260 requests ~$0.02, scripts/conc_probe_past50.mjs)
- Waves c=50→60→70→80: successes hard-cap at **exactly 50 every wave**; excess fails
  INSTANTLY with business code **1302** (not 429 — key-side policy, not provider load).
- Latency of successes flat (1.4–1.7s) at every width → provider serving fine.
- c=70 wall_s 17.3 (one straggler) = soft queuing at the row edge, not a capacity cliff.
- **LAW 13: the 50-row is enforced PER KEY.** Parallelism past 50 = MORE KEYS (horizontal),
  never concurrency tricks.

### Sep-5 five-wide probe (watch/GROUNDING_WAVE.md + CONVO row 09-05 ~23:2xZ)
- 5/5 workers CLEAN on the Max coding-plan seat: 0 rejections, 0 429s, 0 deaths.
- Wall 9.8min vs 36.8min serial = **3.75x throughput**; ~3.78M tokens / 78 tool calls.
- T1 proof of true concurrency: five START rows 23:10:16Z–23:10:57Z, zero DONE at T1
  23:11:47Z; gate lane `max-flash-5x:5` held all 5 slots simultaneously; fleet 7/7,
  verkle chain untouched throughout.
- **Ceiling NOT hit — width 5 was our choice, not the wall.** This is the ramp's mandate.

### Failure modes catalog (all seen on our lanes)
| Class | Signature | Meaning | Seen |
|---|---|---|---|
| 1302 | instant, per-model | "you hit your model's row" — key-side cap. Information, not insult | 09-04 probe, 4.7-flash ×2 |
| 1305 | thousands queued, 1 in-flight | service overloaded — in-flight cap exceeded cross-process | gate module's founding case |
| 429 | quota-side | key/budget exhausted | free ox lane ("429 upstream", 60% ok) |
| worker death | returncode≠0, straggler | harness bug (probe run 1 = 0/0 rows "not measured") or timeout | 08-25 8-fail swarm bug; c=70 straggler |
| latency wall | p50 >2x baseline | saturation/queuing | 8K tax: 11.8s vs 1.2s |
| volume starvation | throughput OK, seat starves | context-debt: 274 calls = 201.3M computed, 98% cache_read (Lite dogfood) | LITE_DOGFOOD_20260904 |

### Model params that matter
- **Thinking cannot be disabled on 5.x** (provider law). 4.7-flash `thinking{type:disabled}`
  DOES return 200 (forced-thinking claim DISPUTED by live test 09-03; §4 row lives).
- 5.3 needs **thinking=low + ≥1536 max_tokens** (epoch-1 infra finding).
- **Terse outputs are money:** output tokens cost 3.3x input (API) to 3.5x (plan credits).
  max_tokens discipline is a budget line (salon organ fixed 900→2200 after truncation).
- **Cache law:** frozen prefix + append-only turns = 99.5% hit (receipted 08-29, reconfirmed
  09-04). B1 refeed_guard: 94% of input is re-fed cache reads — width multiplies re-fed
  cache, so ramping raises burn sublinearly IF prefixes stay frozen.

### Recorded corrections riding with this card (apply at execution time)
1. glm-5.3 row is 15-wide, not 5 (transcription fix, BURST_DOCTRINE).
2. 4.7-flash forced-thinking DISPUTED — thinking-off works; cache-miner lives.
3. Cite the NUMBERS not the plan name (probe key attribution was ambiguous — economist audit).
4. Lite pool pin = **glm-5.3-flash** (not 4.5); live clamp **1400/day** (not 1228);
   tracks live at configs/auth_tracks.yaml; mag/free_tier.py:52 stale-list flagged for audit.
5. swarm_worker DEFAULT_PROVIDER = **cerebras** (Lite unhooked from default, 2026-09-05).
6. 21,264 knots DISPUTED → 13,678 real (99.995% indexed); "215 replies" DISPUTED (17 found).

---

## 2. THE MACHINERY (knob → file → current value)

| Knob | File | Current value |
|---|---|---|
| Per-model in-flight caps (lease-file slots, cross-process) | mag/concurrency_gate.py `MODEL_CONCURRENCY` | 4.7-flash:1, 4.7:2, 5.3:1, 4.5-flash:2, 4.5:10, 5.1:10, 5.2:10, 4-32b:15, 4-plus:20, search-prime:5, web-reader:5, deepseek-v4-flash:3 (local guess, not vendor) |
| Ramp probe lane | mag/concurrency_gate.py:56 | `"max-flash-5x": 5` — measured test width, NOT a vendor cap. **Ramp raises this per rung.** |
| Stale lease steal | concurrency_gate.py `LEASE_SECS` / `POLL_SECS` | 120s / 0.5s (crashed holder can't deadlock a lane) |
| Gate hold timeout per seat task | mag/seat_dispatch.py:234 | `hold(gate_model, timeout=240)` — EVERY seat dispatch passes the gate |
| Swarm default lane | mag/swarm_worker.py:54 | DEFAULT_PROVIDER="cerebras" (Lite unhooked) |
| Per-pass queue drain | mag/swarm_worker.py `MAX_PER_PASS`; scan cap 4x | gated tasks don't consume pass budget (head-of-line fix, ~594 starved) |
| Task timeout | mag/swarm_worker.py:348 | 360s free lanes / 720s paid brake (deepseek) |
| Free reroute lanes | mag/swarm_worker.py:258 | `_FREE_REROUTE_LANES = (nvidia, groq, openrouter)`; brake = deepseek |
| Free bodies registry | mag/free_tier.py `FREE_SURFACES` | z_ai3(Lite), groq, cerebras, nvidia, openrouter a1+a2, ox (dying, 429), together (key missing) |
| Width observability | mag/overseer.py `_in_flight()` | reads gate leases → dashboard/static/overseer.json, live.html 5s poll |
| Lite pool clamp | fuel_feed FREE_LANES + LITE_REARM receipt | 1400/day, pinned glm-5.3-flash; re-arm 2026-09-08T02:19Z gated by B1 (configs/auth_tracks.yaml `lite-rearm-sep8`) |
| Per-seat pools | multiple coding-plan seats | each seat = separate quota pool; fan bulk across seats |

---

## 3. THE LADDER (+5 per wave, ceiling 50 NEVER exceeded)

Rungs: **4 → 9 → 14 → 19 → 24 → 29 → 34 → 39 → 44 → 49 → 50** on the Max coding-plan seat,
driven through `concurrency_gate.hold("max-flash-5x", ...)` with `MODEL_CONCURRENCY["max-flash-5x"]`
raised to the rung width. One rung per wave; soak ≥1h before climbing. Baselines: p50 1.7s,
wall 9.8min at width 5 (the 09-05 probe).

Per rung, watch (in escalation order):
- **Rungs 4–24 (expected-safe zone):** 1302 singles (instant row bumps), straggler wall_s
  outliers, worker deaths from harness bugs (distinguish code failures from width failures —
  re-run a dead worker solo before blaming width).
- **Rungs 29–39 (probe zone):** 1302 rate climbing, p50 drift >2.5s, 1305 first appearances
  (cross-process queueing), overseer.json in-flight vs leased slots mismatch (stale leases).
- **Rungs 44–50 (wall zone):** 1302/1305 STORMS (>10% of workers), p50 >2x baseline (>3.4s),
  latency wall. Expected shape per LAW 13 precedent: hard cap, flat latency, instant refusals —
  on the plan door the shape may differ (429s, slow degradation) because it is Unproven past 5.

BREAKAGE (any one = rung failed):
1. 1302 or 1305 storm: >10% of in-flight slots erroring in a 10-min window.
2. Worker death >20% per wave (exit≠0 not attributable to task content).
3. Latency wall: p50 success latency >2x the width-5 baseline sustained across the wave.
4. Fleet harm: docker fleet <7/7, verkle chain stall, or gate slot leak (leased, never released).

BACKOFF RULE (operator law, two-strike bail): **a rung failing twice = step down one rung
and file.** First failure: halt climb, hold current rung, diagnose (stale leases? key-side?
provider-side?), one retry. Second failure at the same rung: drop one rung, write the finding
with receipts, the ladder stops there for the day. NEVER hand-patch the ceiling past 50 —
past 50 is MORE KEYS / MORE SEATS (LAW 13), which is a separate operator gate.

GOPHER DELEGATION PROFILE (stolen shape, blackboard DELEG-POLICY pins seq 22/28 —
delegation is a policy layer, not a routing table; parent_edit_allow is model-agnostic):
- **Workers spawn gophers ONLY for read-only fan-out**: search, read, list, grep, fetch,
  score. Gophers get NO write/edit authority, ever.
- **Parent (the worker) keeps ALL write/edit authority**: every file mutation, blackboard
  post, and pheromone drop happens in the parent, serially. A gopher's output is DATA the
  parent files, not an edit the gopher makes.
- Skip rules (when NOT to delegate): judgment/folds/arbitration, anything touching
  credentials, anything with a GO-gate. Risk-gated reviewer shape: high-impact effects
  (fs_write, lane_spawn, model_call) refuse self-grant — same invariant as the Five Tests'
  capability-attenuation.
- Width accounting: a worker's gophers count against ITS rung slot budget — gopher fan-out
  inside a rung must not multiply past the gate (`hold()` covers parent + its gophers).

---

## 4. THE FALSIFIER (24h observable — real burn vs waste)

The ramp is REAL when, over any rolling 24h at a held rung:
1. **Billed tokens/day RISE** while **billed-per-useful-receipt FALLS** (more width → more
   receipts per token spent; receipts = chain-verified posts, filed cards, done tasks).
2. **Cache-hit share HOLDS ≥90%** (frozen-prefix law; B1 measured 94% re-fed at width 5).
   Width must multiply cache reads, not cold contexts.
3. **Steps/day in the trajectory stream RISES** (trajectory lens envelope; goal curve toward
   100 sealed steps/day) with error-class steps flat.

KILL CRITERIA (any one = the ramp is WASTE at this rung — step down, file):
- Tokens/day up but receipts/day flat or down for a full 24h → burn without product.
- Cache-hit share falls below **85%** → width is buying cold context, the exact B1 refeed
  failure shape at scale.
- Error steps (1302+1305+429+deaths) >20% of steps sustained at a rung → wall found; that
  number IS the result — file it, don't fight it.
- Breakage rule 4 (fleet harm) at ANY rung → immediate full stop, operator notification.

**Measurement source:** overseer.json (in-flight, fleet), fuel_feed/billing rows (billed
tokens), trajectory_stream.ndjson (steps/day), gate lease files (slot accounting).

---

*Filed by r1-ramp-doctrine, wave 2 BATCH5. Sources: watch/INTAKE_GLM53_HIGH_CONCURRENCY_20260904.md,
docs/ref/BURST_DOCTRINE_20260903.md, watch/GROUNDING_WAVE.md, watch/LITE_DOGFOOD_20260904.md,
mag/concurrency_gate.py, mag/swarm_worker.py, mag/seat_dispatch.py, mag/overseer.py,
mag/free_tier.py, configs/auth_tracks.yaml, queue/handoff/zcode/CONVO.md 09-05 rows.*
