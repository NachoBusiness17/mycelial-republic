# LANE_SLOT_MAP — operator doctrine, 2026-09-01 01:27Z (operator-confirmed, VERBATIM)

Consumed by: the five-lane wiring (lane scaffold). Do not paraphrase — this file IS the spec.
Cross-ref: /board/riddler_common.jsonl 01:27Z law entry · spend audit /board/ECONOMIST_SPEND_AUDIT_20260901.md

---

**Direct answer: flash. DeepSeek-Pro is not a lane's model — it's a verdict-step upgrade. And even that slot belongs to 5.3-flash.**

The confusion dies with one rule: **lanes hold memory and org — calls pick models.** Every lane gets three slots, assigned per call, not per lane:

| Slot | Share of calls | Research lane gets | Price (off-peak) |
|---|---|---|---|
| **Tail** (mechanical) | ~70% | glm-4.7-flash — dedupe, link stacking, formatting, digest scrub | $0 |
| **Hands** (workhorse) | ~20% | **deepseek-v4-flash** — fetch, extract quotes, verify bytes, receipts, triage | $0.22/M in, $0.66/M out, cache-hit $0.007 |
| **Brain** (synthesis + verdicts) | ~10% | glm-5.3-flash, reasoning high (zai standard) — VALID/INFLATED/FALSE calls, BANGER digests | $0.075 in / $0.25 out promo |

**Why not DS-Pro as the brain:** it's $1.98/M output — **8× the 5.3-flash brain** and not obviously smarter. DS-Pro's job in research is narrow: HOT-gate tiebreaks, two-strike escalations when flash failed twice, or backup when z.ai quota dies. That's it.

Live receipts that sharpen this:
- **DeepSeek peak pricing is active right now** (01:00–04:00 + 06:00–10:00 UTC Mon–Fri = double: $0.44/$1.32). Off-peak 04:00–06:00 and 10:00–01:00 + weekends. Schedule heavy fan-outs there — your harvest cron already lands off-peak.
- **Flash concurrency 2500 vs Pro 500** — flash is built for GOPHER fan-out, pro is built for single hard calls.
- **Both DS tiers support 1M context** — my earlier "no lane has 1M" was true of config, not the provider. OpenClaw caps flash at 128k; one config line raises it if you want long research sessions. Cheap too: a cached 1M head re-sends at $0.007/call. Still recommend warm-pack discipline — cache hits only exist if the prefix stays frozen.
- **HOT gate jury (3/4):** DS-flash + nvidia's DS-flash-0731 (same model, second host, spreads limits) + 4.7-flash + 5.3-flash. Diverse juries catch hallucination better than one smart model.

So the research lane reads: **default DS-flash, tail 4.7-flash free, brain 5.3-flash high-reasoning, DS-Pro shelved for tiebreaks.** This slot-map goes into the lane scaffold verbatim when I wire the five lanes.
