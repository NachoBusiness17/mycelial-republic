# INTAKE: GLM 5.3 Flash high-concurrency serving evidence — 2026-09-04

**Source:** @net_termina status 2095880004097790297 (2026-09-04 14:21Z), bio "Hard Work and Guts". Video demo, no repo/paper attached.

**Claim (as posted):** GLM 5.3 Flash TP=4 serving: 5718 tok/s at 512 concurrent users; 6610 tok/s engine decode at c=768; c=1024 didn't fit. Video shows a wall of c=256 sessions each generating unique code. "Warning: do not stare too long."

## Rubric (5 axes, 0-5)
| FIT | PULL | COST | WINDOW | NOVELTY | TOTAL |
|-----|------|------|--------|---------|-------|
| 3 | 3 | 5 | 3 | 3 | **17/25** |

- **FIT 3** — intel, not an organ. Bolts onto docs/ref/ZAI_API_EXPERT_REFERENCE.md (lane catalog/economics) as a provider-capacity datapoint. No new vendor/substrate needed to file it.
- **PULL 3** — feeds the saturation grind arc: promo lane 5.3-flash (wall = Sep 20), key saturation is the named throttle, batch planning needs concurrency ceilings. Doesn't unblock a Stage on its own.
- **COST 5** — zero. One doc line + a measured follow-up if ever acted on.
- **WINDOW 3** — timely during the Sep 3-20 promo grind (informs how hard we can lean on the 5.3-flash lane), but the action is a doc update, not tonight's build.
- **NOVELTY 3** — new surface (first third-party concurrency ceiling datapoint for 5.3-flash we've filed); anecdotal, single source.

**Band: 17/25 BUILD, WINDOWED** — lane named: lane-economics / provider intel. Gate named: none (free); fold into ZAI_API_EXPERT_REFERENCE.md next time it's touched, or before the next batch-grind scheduling call.

**Verdict verb:** REMEMBER (file the datapoint) + CALIBRATE hook (our own lanes are the falsifier: if 5.3-flash really holds c=512, our saturation complaints are client-side/key-side, not provider capacity — one concurrency probe on our lanes would settle it).

**Tri-state: Unproven.** Single self-reported benchmark, video not frame-verified (media is video; not read), no repro artifacts or repo attached. Would upgrade to Supported if a fleet-side concurrency probe reproduces the ballpark.

## Fleet relevance (one line each)
- MAX_DISTILL / batch fires: provider can absorb much higher concurrency than our lanes use — supports "quiet-window" dogma being about key quota, not provider load.
- Claim-organ CAS fix: this is exactly the class of claim the workbench should falsify cheaply (probe our lane at rising c, compare tok/s).
- Shadow-fields/matrix-style "wall of agents" visuals: the video itself is a salon-grade visual motif (wall of c=256 code sessions).

## Dogfood note
INVARIANT PASS not run (time-box). Worth one blind-post if this ever graduates to a law ("5.3-flash serves 5k+ tok/s at c=512").

## ADDENDUM — CONC_PROBE_PAST50 (measured 2026-09-04, card-worker, single run)
Falsification probe: `scripts/conc_probe_past50.mjs`, z_ai3/Lite key (the key our 50/50 receipt came from), glm-5.3-flash, max_tokens 8, "say ok", 10s pauses. 260 requests total, ~$0.00 on Lite package (pennies). Prior receipt `docs/ref/BURST_DOCTRINE_20260903.md` never tested past 50 because 50 was the vendor-documented row.

| wave | launched | HTTP 200 | err 1302 | err 429 | p50 latency (successes) |
|------|----------|----------|----------|---------|--------------------------|
| c=50 | 50 | 50 | 0 | 0 | 1.68s |
| c=60 | 60 | 50 | 10 | 0 | 1.41s |
| c=70 | 70 | 50 | 20 | 0 | 1.44s |
| c=80 | 80 | 50 | 30 | 0 | 1.57s |

**Verdict (tri-state → Supported): the 50-in-flight row is ENFORCED PER KEY.** Successes hard-cap at exactly 50 in every wave including c=80; the excess fails instantly with business code 1302 (not 429 — not quota-side, not provider load). Latency of successes stays flat (~1.4-1.7s, matches the burst-receipt p50 1.7s), so the provider is serving fine — the wall is key-side policy. Third-party c=512 claim: NOT contradicted (that run was TP=4 self-hosted serving, engine-level, not the vendor API), but for OUR lanes the claim is moot — ceiling is 50 per key, full stop. Fleet consequence: saturation grind is bounded by keys, not provider — parallelism past 50 needs MORE KEYS (pool them), not schedule cleverness. Wave c=70 wall_s 17.3 (one slow straggler) — soft evidence of queuing at the row edge, not a capacity cliff.

Probe: 260 requests fired once, no loops. Keys never echoed.
