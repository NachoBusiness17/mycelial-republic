# ECONOMIST AUDIT — the Sep-20 proof, priced (2026-09-04)

Mandate: prove by Sep 20 the fleet burns two Max plans usefully. Five sections, each:
verdict + evidence + one call. All figures quoted from disk; estimates labeled [est].

## 1. THE MARCH — what $0.09 buys
Evidence: watch/march/MARCH_RECEIPT_20260904.md
- 657/657 signals, 0 errors, 12 consecutive 50-wide tranches clean. Cost ~$0.09
  OUT-of-window on flash promo rates; $0.00 in the 23:00-09:00 window. Wall time: minutes.
- Honest unit rates (this regime only — simple triage prompts, mean 85 tok/req):
  **$0.09/657 = ~$0.00014 per signal = per verdict. Per ACTION-grade signal (142):
  ~$0.00063.** In-window: $0 across the board.
- CITATION-CASCADE WARNING (my own law): these rates do NOT transfer to burns 2-5.
  The march was short-prompt triage at promo cash rates. The KG pass and canon mine are
  100-1000x more tokens per item (burn plan: 30-50M and 10-20M tok/night). Any slide that
  multiplies march $/signal by a bigger corpus is inventing money.
- What it teaches for Sep 20: (a) 50-flight is operationally solved at the width we have;
  (b) the whole 228-signal explore backlog = one coffee — **food, not compute, is the
  binding constraint** (SWARM_SCALE_PLAN_20260904.md predicted "one evening"; it was less).
VERDICT: Supported. CALL: the proof metric is receipts/day at rising width, not $ —
the $ collapses in-window; condition 1 of the burn test must carry the argument.

## 2. THE BURN PLAN — unlocked vs starved
Evidence: watch/BURN_PLAN_20260904.md, watch/SWARM_SCALE_PLAN_20260904.md
- Burn 1 (march): DONE, receipt above.
- Burn 2 (backlog dies): **UNLOCKED NOW** — food on shelf, night window free, width proven.
  Duration-limited: at march metabolism the hermes backlog dies in nights, not weeks.
- Burn 4 (verifier denominator): **UNLOCKED NOW** — adversarial 50-way wings run on the
  FRESH-claim path, which the race test proved sound (60 claimants, 10/10 single winner).
- Burn 5 (canon mine): **UNLOCKED** (chain v0 in hand, same lane).
- Burn 3 (shadertoy KG): **PARTIALLY STARVED on data, not tokens** — source wall receipted
  (Shadertoy 403; only door = real browser, INTAKE_SFGSWG Identity Fold 09-04). Lattice
  build can start on already-stolen material; 52k-shader scale waits on the wall.
- Burn 6 (gamebuild farm): HOLD — horse-gated, correct to keep last.
- Max key #2: **STARVED by the ledger's own law** — sequencing law #2 requires demonstrated
  starvation (restock cannot fill 50-flight for N windows). Measured opposite: capacity
  outran food in one pass. Buying #2 before the hunger meter moves fails our own test.
VERDICT per burn above. CALL: run burns 2+4 tonight in-window at current width; that IS
the Sep-20 evidence. Scale-up wider than 50 waits on the CAS fix (section 3).

## 3. THE THROTTLE — CAS fix vs 50-lane unlock
Evidence: watch/CLAIM_ORGAN_RACE_TEST_20260904.md
- Fresh-claim CAS: proven (10/10 rounds single winner). Takeover path: SPLIT-BRAIN —
  4/4 contended rounds gave 2-3 simultaneous winners; deterministic TOCTOU at
  bay_organs.py ~L247 (unconditional tomb-move). Corrupt-file wedge = minor finding 2.
- Economics: **cost of fix ≈ one seat-afternoon, $0 cash, fix shape already written in the
  finding** (token-match re-read or overwrite-CAS embedding the stale token). Cost of NOT
  fixing: every grace-expiry under hungry engines double-mines — duplicate token burn,
  corrupted receipts, and a direct violation of burn-test condition 3 (100% receipt
  coverage), i.e. the exact "stupid burn" the plan outlaws. At 50 sustained lanes with
  engine churn, stale takeovers are routine, not edge.
VERDICT: Disputed-takeover, Supported-fresh. CALL: **CAS fix is priority #1 before any
tranche scale-up — GO, this week.** It is the cheapest lever on the board: hours of labor
buy the entire scale-up path. (Scale-up beyond current width, not burns 2/4/5 at current
width, is what it gates.)

## 4. THE LEDGER — utilization and what breaks first at 10x
Evidence: docs/ref/ZAI_API_EXPERT_REFERENCE.md (pricing/concurrency/campaign sections)
- Max = 28K credits/5h + 140K/wk. Measured credit rates: flash input ~12,312 tok/cr,
  cache ~50,381, output ~3,591 → weekly ceilings ~1.72B input / ~7.05B cached / ~503M
  output tok. Observed bay 09-03: ~600M tok ≈ 17K credits.
- **Honest utilization: ~12% of weekly credits (17K/140K) [est — one day's rows].**
  Theoretical ~480K wing-requests/day vs actual order-of-magnitude ~1K/day class [est].
  The night window (zero-quota, receipted: 32.26M tok / $0 / 0 cr) makes in-window burn
  effectively unmetered on top.
- What breaks first at 10x, in order: (1) **FOOD** — proven tonight; backlog consumption
  outruns restock 100:1 [est]; (2) **the claim organ** — double-mining at takeover rates
  (section 3); (3) **host orchestration** — one Windows box herding 50 lanes, unmeasured
  above 63s duty (duty-cycle receipt: 27.85 req/s, 99.89%, 63s only — sustained-hours
  unproven); (4) 5h/weekly credit windows only if work goes output-shaped or out-window.
  Vendor concurrency (50 in-flight) does NOT break — receipted.
VERDICT: Supported (utilization, ceilings); Unproven (sustained-hours host duty).
CALL: the hunger ledger is the real fuel gauge — instrument restock-vs-consumption per
window now; it is also the legal basis for Max #2.

## 5. DEADLINE — Sep 20 vs Sep 23
Evidence: reference §10.6 vendor notice, verbatim scope: **"Sep 3–20, 2026, DAILY
23:00–09:00 UTC+8."** No promo-page receipt showing Sep 23 exists on disk.
- Sep 20: **Supported** (filed vendor notice). Sep 23 (operator's figure): **Unproven.**
- Note: a SECOND promo ends Sep 9 — the 5.3-flash 50% CASH price (reference §1). Two
  different clocks; do not conflate.
CALL: 30-second operator read of the promo page settles it. Until then PLAN TO Sep 20 —
the conservative date loses nothing if the window extends; the optimistic date risks an
unreceipted cliff.

## THE ECONOMY IN ONE BREATH
Capacity is rented abundance (12% used, night window free, 50 lanes receipted); the
binding scarcities are FOOD, the CAS fix (one afternoon), and 16 days of calendar.
Burn 2+4 tonight, fix the organ this week, let the hunger ledger — not ambition — sign
the purchase order for Max #2.
— E out.

## CORRECTION APPENDIX (13:3xZ, same day — the audit's denominator was wrong)

The utilization figure (~12% of weekly credits) read the BAY's books only. The zcode seat's own meter (~/.zcode/cli/db/db.sqlite, never previously queried by any fleet surface) shows **2.84B tokens lifetime / 10 days through this seat alone** — the biggest single burner in the fleet, ~0.4-0.5B/day, majority = one zombie heartbeat automation on the paid 5.3-full model (740M no-op tokens, 11 useful posts ever). The Economist's "Max #2 STARVED" verdict SURVIVES (food still binds — burn ≠ useful output; useful-output ratio of the zombie was 7e-7), but the breaks-first order changes: **the seat's own sessions break the budget before the bay does.** Full forensics + salon laws: watch/USAGE_METER_SELF_STEAL_20260904.md. The usage tab is now a standing receipt source: read it before ANY capacity claim.
