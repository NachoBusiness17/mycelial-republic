# BURN-DOWN PLAN — touching the limit we aren't touching (2026-09-06, w4 of batch5)

Operator order: "plan how we can burn down our usage because right now we aren't even
touching our limit." Promo window Sep 3-20 gives LIMITED DAILY PER-SEAT quota that expires
unused; Sep 20 is the proof deadline. Supersedes **watch/BURN_PLAN_20260904.md** on the
quota-sizing question only — that card asked "which burns are useful," this one sizes the
burn against the promo pool. Its sequencing law (prove on ONE package; Max #2 earned by the
hunger ledger) and its six useful burns carry forward UNCHANGED; nothing in it is
contradicted, it is extended from night-window economics to per-seat daily-quota economics.

---

## (a) CURRENT STATE — measured (all numbers tri-state with source)

Primary instrument: `C:/Users/foste/.zcode/cli/db/db.sqlite` (314MB, opened mode=ro),
table `model_usage`, epoch-ms timestamps, `status='completed'`. Window carve: by
`provider_id` lane.

| Metric | Value | Source | Verdict |
|---|---|---|---|
| Last-24h burn (all lanes) | 2,008 calls, 457.5M raw in / 1.73M out (264:1), 96% of input = cache reads | db model_usage, completed, since 2026-09-05T01:35Z | Supported (deterministic query) |
| Last-24h by lane | coding-plan GLM-5.3-Flash: 1,052 calls, 270.5M in; coding-plan GLM-5.3: 16 calls, 3.9M in; start-plan: 940 calls, 183.1M in | db, same query | Supported as history; start-plan lane is DEAD since 16:16Z 401 (configs/auth_tracks.yaml) — its 940 calls predate the expiry |
| BILLED last-24h (uncached_in + out) | coding-plan ~11.0M; start-plan ~8.1M; total ~19.1M | db: SUM(input-cache_read)+output | Supported arithmetic; billing model UNPROVEN (see next row) |
| Vendor weekly meter | 87.04M tok / 220 calls, window Sep 1→Sep 6; weekly credits 6,420/10,000 used (64%) | state/fuel/lite_quota_log.jsonl (04:35Z detail; 19:15Z quota reading identical → stale or rolling window) | Supported as a pasted meter row; RECONCILIATION: db 7d coding-plan billed = 87.5M ≈ 87.04M vendor (0.5% delta). Working model: **the pool bills uncached input + output; cache reads are quota-free.** Mechanism Unproven; magnitude agreement is why we keep the model |
| Clamp | Lite fuel-lane pacing 1,228/day live (designed ~1,400/wk of the 10,000/wk pool) | watch/COUNSEL_QUOTA_BURN_20260905.md:91, salon_source_self_steal_20260905.md | Supported — and it guards the LITE key, a SEPARATE pool from the coding-plan promo seat |
| "300M weekend pool burned to zero" | Weekly meter shows 64% used, 87M tokens billed, reset ≈ Sep 8-15 | lite_quota_log vs WEEKEND_BURN_BOARD header | **Disputed as current state** — true as the morning's alarm, superseded by the meter rows above; the pool did NOT stay at zero |
| Rollout jsonl proxy | 3 files × ~190KB only (current batch); dir reset Sep 5 13:08 | C:/Users/foste/.zcode/cli/rollout/ | Supported: NOT a usable 24h proxy — db used instead |

## (b) STANDING BATCH SHAPE + CADENCE PROPOSAL

The shape: **batch5 = 5-wide in-seat** — 4 workers × 4 sub-items + 1 salon, each worker
iterating ~10-step salon-loop calls, one orchestrator window. Proven CLEAN 5/5, 3.75x
throughput, 0 losses (GROUNDING_WAVE.jsonl T2 receipt 09-05; this batch is live evidence).

**Churn-law reconciliation (why 5-wide does not violate ≤3 free windows):** the ≤3 law
(WEEKEND_BURN_BOARD header) counts concurrent WINDOWS chewing a SHARED pool — the 4th+
auto-launches on Max. A batch5 wave is ONE window on ONE seat making parallel CALLS; the
pool sees one consumer. Both laws hold: ≤3 windows per pool, ≤5 workers per window.

**Failover law (unchanged):** waves ride the promo coding-plan seat (builtin:zai-coding-plan).
What still routes to Max: operator-gated spends (KEYS/ONE STOP), blocked→unblocking work,
anything needing GLM-5.3-full. Lite stays dead until Sep 8 02:19Z re-arm THROUGH B1's guard
(auth_tracks.yaml `lite-rearm-sep8`).

### ITEM 3 — BATCH ECONOMICS (measured, verbatim section)

Measured per-call sizes (db model_usage, 2026-09-05):
- Subagent call: avg input 54-65K raw, avg output ~900, cache-read share ~90% →
  **billed ≈ 7K per call** (uncached_in + out).
- Main-turn (orchestrator) call: avg input 93K-330K raw, cache ~95% → billed ≈ 11K.
- Live batch5 wave (this one): 37 subagent calls = 2.0M raw in / 26.5K out in first ~15 min.
- Prior 5-wide probe receipt: 3.78M raw across 78 tool calls, 9.8 min wall, 3.75x.

ASSUMPTIONS (inline): a heavy research wave = ~200-260 subagent calls + ~8 orchestrator
turns (4 workers × ~45 calls + salon); raw ≈ 4-8M per wave; billed ≈ 500K-1.2M per wave
(cache discipline holding at ~90%). Wall time 10-15 min light / 40-60 min heavy.

| Shape | Waves/day | Raw tokens/day | Billed/day | Notes |
|---|---|---|---|---|
| Today's default (1-2 ad-hoc) | 2 | ~8-16M | ~1-2.4M | the "aren't touching it" baseline |
| Proposed standing cadence | 6 | ~24-48M | ~3-7M | 2 waves/hour light blocks, heavy waves get an hour |
| Proof-sprint ceiling (Sep 15-20) | 12 | ~48-96M | ~6-14M | hunger-ledger gated, not ambition-gated |

Waves/hour sustainable: **2-3 light or 1 heavy** — wall time, not quota, is the short-term
binding constraint while Max is drained; the seat is interactive (operator-gated GOs), so
cadence is "waves while the operator is in the window, 8AM-6PM PT."

Headroom: at 6 waves/day for the 14 days to Sep 20 → ~40-100M billed, inside a pool the
operator describes as barely touched (meter shows 64% of 10K credits AFTER the heaviest
weekend so far; billed-token read: 87M/wk actual vs 300M-class pool claim). Even the 12/day
sprint ceiling stays under ~140M. **The limit is receipts-per-day, not tokens** — which is
exactly BURN_PLAN_20260904's four-condition test, carried forward: burn only scales if
receipts scale and cost-per-receipt falls.

## (c) REFEED-TAX MITIGATION (pointer)

- Refeed tax today: meter in:out = **264:1 last-24h / 247:1 7d coding-plan-flash** — the
  "~240:1 meter reading" is SUPPORTED as current (source: db aggregates above).
- B1 `mag/refeed_guard.py` is BUILT (exists in mag/, char-proxy measurement over the db,
  $0, mode=ro, writes state/refeed_guard_latest.json; first run shows char-ratio 9-15:1 on
  work-shaped chars vs 264:1 on the full meter — most input is mechanical context re-feed).
- The "~50% waste" figure was the 09-05 restart-attribution AUDIT on the dead Lite pool —
  it is an audit-era estimate, not a standing number; B1's per-lane per-day refeed_ratio
  (>15% for 2 days → clamp) is the instrument that replaces guesswork. Lite re-arms Sep 8
  THROUGH that guard, not before (configs/auth_tracks.yaml). Mitigation for waves: keep
  workers long-lived (fewer restarts = fewer full-context re-feeds = the 90% cache share
  stays cache), which batch5 already does.

## (d) FALSIFIER — 48h observable, kill criterion

Instrument: one $0 db query per day at 18:00 local (`SELECT SUM(input_tokens-cache_read_input_tokens)+SUM(output_tokens) FROM model_usage WHERE started_at >= day_start AND status='completed' AND provider_id='builtin:zai-coding-plan'`) + the weekly credits reading at 6PM.

- **BURNING REAL (kill = back to 4 waves/day):** billed > 3M/day sustained AND weekly
  credits remaining < 50% at 6PM.
- **CADENCE DOUBLES:** weekly credits remaining > 50% at day-end for 2 consecutive days
  WITH receipts/day not flat → go 6→12 waves/day (BURN_PLAN four conditions still must hold).
- **PLAN IS VAPOR:** 48h with zero new waves launched AND quota untouched → the plan changed
  nothing; delete it rather than let it decorate the watch/.

---
Sources: db model_usage (mode=ro) · state/fuel/lite_quota_log.jsonl · configs/auth_tracks.yaml ·
watch/BURN_PLAN_20260904.md · watch/WEEKEND_BURN_BOARD_20260905.md · watch/COUNSEL_QUOTA_BURN_20260905.md ·
watch/GROUNDING_WAVE.jsonl T2 · mag/refeed_guard.py + state/refeed_guard_latest.json · HUNGER_LEDGER.md
