# SALON ROUND 1 — LENS: ELLUL (technique and its self-augmentation)
Topic: "The Game at the Right Time" temporal-authority moonshot. Chair: ractor lens, cage-side.
Charter: `/board/inbox/MOONSHOT_RIGHT_TIME_20260901.md` (Q1–Q5). Verified R0:
`/board/SALON_RIGHT_TIME_R0_20260901.md`. Every number quoted or marked **UNVERIFIED**.
MONEY_MAP.md / LANE_MAP.md **do not exist on /board** — all figures taken directly from
`/board/water_windows.mjs` (read, full) and `/board/ECONOMIST_SPEND_AUDIT_20260901.md` (read),
quoted with source tags.

---

## 1 — THE EFFICIENCY LEDGER: what enforcing WHEN buys, and its price

Technique's promise per window, then its invoice. ($ quoted from economist audit; window defs from water_windows.mjs.)

**a) groq_oss — 30 RPM / 1K RPD / 200K TPD, $0 free tier**
(econ `groq` row: MEASURED rate card; fuel 90/103=87.4%)
- BUYS: no $ (free tier). Capacity headroom only — the binding cap is the **1K RPD**, not the 30 RPM. Enforcing "spread across the day" buys day-long runway off one free ladder.
- COSTS: maxed. Window id is `POLLED — cage cannot read usage; poll from host or trust deferrals`. Enforcing WHEN needs host-side read + a new meter = **one more organ to feed** to get a fraction of a free tier.

**b) cerebras — 5 RPM / 30K TPM / 1M TPD, $0 free tier** (econ MEASURED, activated 08-31 21:15Z)
- BUYS: $0, capacity only. 5 RPM is tight; 1M TPD near-unlimited. Enforcing WHEN is pure throttle friction on a lane that is free and rarely binding.
- COSTS: same as groq — `POLLED` host-side, new meter, growth of the clock itself.

**c) or_free — 50 RPD (<$10 bal) / 1000 RPD (≥$10), $0** (econ CORPUS, operator receipt not probed)
- BUYS: $0. The WHEN that matters is the **LOW-cliff** — stay ≥$10 to hold 1000 RPD vs collapsing to 50. That is a *balance* gate, not a clock gate: it is about DOLLARS IN the openrouter account, which the temporal layer does not read. Cheap WHEN-enforcement buys very little until a balance signal exists.
- COSTS: balance state is **UNVERIFIED-OPERATOR-PULL** — enforcing a window you cannot see is architecture over a phantom.

**d) zai paid key / zai_half_price / zai_credits — the one real-money pool**
(econ: billed key `$0.075/$0.25/$0.015` in/out/cache; ledger zai_credits burn = `$3.40` → `$16.60` left, **internally consistent but rate-receipt math, NOT a provider invoice = CREED GAP**; `$20` pool; zai_half_price `50% off till 2026-09-09` from water_windows.mjs)
- BUYS: real $. 50% off till 09-09 halves billed token spend; staying offpeak nets like deepseek. This is the only window where "right time" has a hard dollar floor under it.
- COSTS: **the $16.60 is self-derived.** Enforcing WHEN against a balance no provider has confirmed = scheduling against a guessed bank. The temporal authority would be gating on a **fan fiction ledger** until the 08-31 session burn (`$0.743`, 4.29M in/11.3M cache/374k out over 236 calls — MEASURED zai_billing_telemetry) is reconciled to a provider invoice.

**e) deepseek offpeak — weekday BJ peak 09-12/14-18, 2x price; half price offpeak + all weekend** (water_windows.mjs; econ: avg `$1.33/day`, run-rate `~$40/30d`, month `$93.34 / 69,335 req / 98.01% cache`)
- BUYS: real $ — the half-price window halves the marginal out/~`$0.66/1M` blended. This is the **only window already enforced as architecture** (R0: `offpeak.defer_if_peak` → `deferred_peak` gate consumed by cheap_swarm + lane_salon). It is the one gate that already *refuses work*, not merely meters it.
- COSTS: already institutionalized. The enforcing organ exists; the invoice is the `MAG_ALLOW_PEAK` override knob — operator deliberation routed through an env variable every time someone wants peak.

**Ledger bottom line:** four of five windows are $0 free tiers where "when" buys capacity headroom against a POLLED/meter blind-spot; two are real-money (zai, deepseek) of which exactly **one** is already architecture-enforced. Extending the scheduler to five windows multiplies the clock's organs faster than it multiplies savings.

---

## 2 — THE OVERREACH WARNING: where temporal authority starts running the fleet

Ellul's cut: every efficiency creates its own demand. The scheduler that "saves" money becomes a **second supervisor we did not elect** — R0's own law: *"No second supervisor."* Two failure modes, mapped to K_T1–K_T5 (supporting/sharpen them).

**Failure Mode 1 — REDUNDANCY FOG SHAPED AS ONE AUTHORITY.**
More windows gated = more overlapping clocks (offpeak.py, water_windows.mjs, desk_timing meters, water_computer season, verified_clock readout). "Unify into one scheduler" is the Ellulian seduction: it fixes drift (K_T2) by **fusing controllers**, not removing them — a master clock whose failure now kills every lane at once. **Trigger:** unifying all 5 windows under one gate organ while the underlying meters stay `POLLED`/UNVERIFIED → you inherit their blindness as your authority's own. Map: **hardens K_T2** (clock drift) into the sharper risk that the "one authority" is only as honest as its least-verified meter. **Kill sharpening:** K_T2 should also fire if ANY window gates on a non-invoice balance (zai $16.60) — drift by *garbage-in*, not just wall-clock disagreement.

**Failure Mode 2 — THE ENFORCER BECOMES THE PRODUCT (organ that must justify its own existence).**
A scheduler-authority that gates 5 windows, reads N meters, holds override knobs, and logs deferral receipts is a **job** — one that consumes cadence to stay live (fleet audit: 27 organs, 17 LIVE, gap_count 0; every organ keeps a heartbeat to avoid becoming a corpse). The authority starts *generating demand for its own dispatch* (cheap_swarm runs to be seen running; deferral logs to prove the gate matters) instead of serving the operator's "game." **Triggers:** (a) scheduler heartbeat/cadence on the MORNING_RUNBOOK as a standing line item; (b) a new receipt row type `deferred_peak` accumulating as a *success metric* (people chase gate-firings) rather than a waste signal. **Map: hardens K_T3** — K_T3 says 0 deferred_peak rows in a week = gate is decoration. Add the invert: gates firing *constantly* and being *celebrated* = the enforcement machine has become the workload. K_T3 should also measure **why** rows exist, not just that they do.

---

## 3 — Q5 VERDICT: does the stew compose?

**Verdict: PARTIAL — composes only on the two capped-$ axes, then it must stop.**

The recipe (rules-before-play freeze packs + ractive loop + temporal authority) only "got a stew" if the clock gates what it can actually see and pay. It can see deepseek (architecture, half-price, real) and zai (real dollar pool, but unverified balance). It **cannot see** groq/cerebras/or_free (all `POLLED`, all $0) — enforcing those is teaching the computer to play chess against an invisible board. Ellul's refusal stands: the scheduler that buys $ on two lanes but spends organs on five is not efficiency, it is institutionalization of waste.

**Smallest playable experiment (≤3 lines):**
1. Consolidate to the two see-able windows: gate deepseek offpeak (exists) + add a zai credits offpeak gate.
2. One probe: run the same dispatch during zai peak vs zai_half_price window; record billed $ from the provider export (not the $16.60 self-balance) → proves WHEN pays on a receipted lane.
3. If the zai probe shows no billable difference (or the pool is a phantom), kill the multi-window claim and keep only deepseek — the temporal moonshot **descopes to one enforced window** (matches R0 K_T4 descope).
