# WATER NETWORK SPEC — the API network as one water computer (v0, 2026-09-01 13:34Z)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: the API network routes as one water computer — measured reservoir levels, seven standing gates, and the free-first dumb-window pipeline keep smart-lane tokens a premium used only at synthesis — SUPPORTED (levels and exploits measured in-card: E5 99.7%, E6 100%, Lite 1.39K/3.3h) · falsifier: per-reservoir burn rows showing a gate firing wrongly twice (two-strike amendment) or a reservoir holding zero productive flow for 2 weeks without demotion
Operator directive: entire API network modeled after water computer, correctly working together,
exploiting our discoveries and skills, all surfaces/structures efficient, through self-improving
dogfood babystep processes. This spec is the mapping; babysteps implement it.

## THE MAPPING (computer → water)
| water concept | network reality | meter/source |
|---|---|---|
| Reservoir | one API lane (key×endpoint family) | water_ledger + meter_readings |
| Water level | measured quota/credit state per lane | 5h/weekly credits, TPD left, water cash pool |
| Inflow | resets, unlocks, deposits | 12:52Z wall reset, weekly refreshes, operator top-ups |
| Evaporation | use-it-or-lose-it buckets (5h expiry) | Lite/Pro/Max rolling pools |
| Channel | a route: seat×workload×lane binding | LANE SLOT-MAP + prefer_order |
| Gate | a law that opens/closes flow | Lite isolation, off-peak multiplier, wall-aware demotion, AUTO-SPLIT |
| Pressure | demand (queued work) | workboard backlog, cron lanes, operator drops |
| Flow rate | observed tok/s + hit-rate per channel | invariant probes, gopher receipts |
| Silt | dead queries / INFLATED patterns | archivist verdicts, two-strike records |
| Rain dance | discoveries that open new channels | E5 cache-mining, endpoint-scoping, key-family matching |

## THE GATES (laws already passed — v1 enforces them in routing order)
1. OFF-PEAK GATE: peak Mon-Fri 06:00-10:00Z = flow throttled to emergencies only (3.5-4.3× cost).
2. ISOLATION GATE: Lite = 1-slot sequential, no fan-out; heavy work never touches it.
3. FAMILY GATE: key-family must match endpoint-family (today's saga) — routing table carries the pair.
4. WALL GATE: 1310/429 quota walls demote a reservoir to bottom until measured reset (no thrash).
5. AUTO-SPLIT GATE: splittable work fans out across live reservoirs; fatter pipes bond.
6. CASH GATE: billed lanes require operator word OR standing law (Lite law, conservation window).
7. GOSSIP GATE: discoveries auto-promote — E5 proved cache-mining → cache-mining becomes a standing channel.

## RESERVOIR CENSUS (v0 state, 13:34Z)
| reservoir | family/endpoint | level | state |
|---|---|---|---|
| PRO (e18faf) | coding-plan @ anthropic-compat | 12K/5h, 60K/wk pool | LIVE (zcode primary) |
| MAG (bafc5c) | coding-plan @ anthropic-compat | shared weekly pool | WALL until 09-02 12:52Z |
| Cache (e3c505) | coding-plan @ anthropic-compat | same shared pool | WALL until 09-02 12:52Z |
| LITE (4f8ac5) | Lite @ anthropic-compat | 2K/5h, 10K/wk own bucket | LIVE (1-slot, ISOLATION GATE) |
| slot1 (3254ac) | intl PAYG @ paas | DELETED | empty — needs new intl key for E5 channel |
| deepseek | direct API, 98% cache | cash pool $24.13 | LIVE, off-peak half-price |
| together | serverless DS-V4-Flash | per-token cash | LIVE, E6 100% cache proven |
| cerebras/groq | free tiers | 1M TPD / 200K TPD | LIVE scut lanes |
| ollama | local | electricity | T0 janitor |

## BABYSTEP LADDER (self-improving, better-by-default)
- **v0 (done at birth):** this spec + M0 daily meter + water_ledger reservoir rows = levels measured.
- **v1 (this week):** gate enforcement in OUR routing decisions — every spawn/lane choice cites its gate
  (off-peak, isolation, family, wall). Cost ledger gets per-reservoir burn rows (close the 11/12 unmeasured gap).
- **v2 (post-reset 09-02):** ask_router integration (host organ, $0 control plane) reads water levels →
  live routing; E5 cache-mining channel reopens on new intl key; MAG/Cache reservoirs refill (rain).
- **v3 (babystep autos):** weekly lane hit-rate review — prune silt (dead queries/lanes), promote
  discoveries to standing channels, re-level reservoirs from measured burn.
- LADDER LAW: a reservoir with 2 weeks of zero productive flow gets demoted to rain-only.
  A gate that fires wrongly twice gets amended (two-strike applies to laws too).

## EXPLOIT LIST (discoveries the network must route to exploit)
E5 cache-mining (99.7% PAYG) · E6 Together (100%) · off-peak 0.5× credits · steering transfer (5/5)
· key-family × endpoint-family matching · Lite 1-slot economics · DeepSeek 98% cache · UD quant custody.

## v1.5 — THE DUMB WINDOW PIPELINE (operator directive 13:41Z: salon on every prompt)
Flow: operator prompt → FREE massage → TIE → SMART answer. The point of salons, applied at the front door.
1. **STAGE 1 FREE (parallel, $0):** 2-3 interpreters on cerebras/groq/DS-offpeak: (a) intent trajectory,
   (b) self-steal (memory_search + board grep — what do we already hold?), (c) gap-check. Salons on the
   prompt as input — dozens of salon examples are the prior art.
2. **STAGE 2 TIE (cage-local, $0):** system attaches what the prompt needs automatically — RIB pointers,
   receipts, laws, WARM_PACK spine. The prompt never hits the smart lane naked.
3. **STAGE 3 SMART (1 call):** main session / glm-5.3-high answers from the massaged brief.
   Plan bucket dry → **API BUFFER**: PAYG at cached economics (E5 99.7%) absorbs overflow — the buffer
   reservoir the operator named. Water: pressure (prompt) hits the free aquifer first; the smart reservoir
   only releases judgment-water.
4. **RANKING (measured 13:41Z):** Lite (zcode) = 1.39K credits/3.3h — the giant. Fleet DeepSeek ≈ $0.09/day.
   zai-API residue $0.74 one-time. This pipeline pushes fleet traffic further into free aquifers and makes
   smart-lane tokens a premium used only at synthesis. The API buffer converts wall-days (like tomorrow's
   12:52Z MAG/Cache drought) from stall → flow at cached cost.
LADDER: measure per-prompt (free-tok share, smart-tok share, brief size, latency); prune interpreters
that yield INFLATED twice; promote interpreters that measurably improve smart-lane answers.
