# NIGHT SHIFT 001 — the long dark (2026-09-01 05:45Z → 10:45Z)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the night ran under operator authority with a ≤$2 paid-API burn gate and stage-gated receipts ending in a $200 deployment recommendation — SUPPORTED (sibling receipts from the same window: NIGHT_CACHE_RECEIPTS / CACHE_YIELD_MATH / lineage_genC files) · falsifier: water_ledger rows for the window exceeding the $2 gate, or a stage missing its named receipt file

**Authority:** operator 05:44Z — full operational budget ($200 crypto.com refund = dawn deployment capital), z.ai Lite seat/API authorized for the night (amends conservation law until 09-02 12:52Z; z.ai coding-plan 5.3 full still untouched). Tonight's own burn gate: **≤$2 total paid API** (DS off-peak ≤$1, Together ≤$1); everything else = plan-$0 + free lanes.

**End state by 10:45Z:** receipts pack that answers — which lesser model holds which lane at what quality; what cache mining actually yields on Lite + DS off-peak; does the switchboard pass its Five Tests; and a $200 deployment recommendation grounded in all of it.

## Stages (ticker advances; two-strike bail per stage; every stage = board receipt)

- **S0 05:45-06:00 SETUP** — brief filed (this file), ticker armed, workboard card, battery wave-1 launched (groq via swarm seat).
- **S1 06:00-07:00 BATTERY GEN C WAVE 1** — frozen 20-probe battery (`/board/lineage_battery_v1.json`, VALID, gen B = glm-5.3-flash exists for comparison) run across lesser lanes: groq gpt-oss-120b, cerebras gpt-oss-120b, nvidia v4-flash (free credits, no spend), together V4-flash (≤$0.5 gate), openrouter free fleet (llama-3.3-70b, gemma-2-9b), z.ai Lite glm-4.7-flash. Raw verbatim outputs per lane → `/board/lineage_genC_<lane>_20260901.md`. Keys from /mag/.env read-only, never printed. Scoring rubric = gen B sheet.
- **S2 06:00-08:00 CACHE MINING CAMPAIGN (parallel)** — z.ai Lite: frozen FROZEN_SELF prefix, glm-4.7-flash + glm-5.3-flash, measure hit-rate/tokens/latency (extend `zai_probe.mjs` pattern, /board/zai_probe2.mjs); DeepSeek off-peak window 06:00-10:00Z: repeat prefix measurement, cached $0.03/1M math; output `/board/NIGHT_CACHE_RECEIPTS_20260901.md` + append water_ledger rows per reservoir (finally measuring the 11 unmeasured reservoirs).
- **S3 07:00-09:00 FIVE TESTS RUNNER v0** — staged switchboard (staging/switchboard_v2.py, effect_broker.py, policy_engine.py, harness.py) vs the Five Hypervisor Tests: bypass / capability-attenuation / noisy-neighbor / replay / confused-deputy. Each test scripted, verdict + receipt → `/board/FIVE_TESTS_RUN_20260901.md`. Codex convergence gate: no 32×32 until green.
- **S4 08:00-09:30 STEERING NIGHT PASSES** — 2-3 live steering experiments per RND brief agenda on bonded cache lanes (steer organ + steers.jsonl precedent); findings append to RND receipt chain.
- **S5 09:30-10:30 SCORE + SYNTHESIZE** — wavelength matrix gen C vs gen B (which model replaces which seat at what confidence); cache yield math; Five Tests verdict; ponytail ladder stats (fires/hits overnight).
- **S6 10:30-10:45 WRAP** — `/board/NIGHT_SHIFT_SYNTHESIS_20260901.md` + INDEX registration + memory write + $200 recommendation (ladder: A = OpenRouter $10 top-up unlocks 1000 RPD free fleet; B = Together batch credits for bulk; C = hold for hardware rung after FreeToken host check) + remove ticker job + wake main with morning brief.

## Rules
- Conservation amendment is NIGHT-SCOPED: at 10:45Z the old law resumes (DS + free).
- No z.ai coding-plan 5.3 full burn. No zcode (hands-off till 09-02 12:52Z). No AutoClaw autostart.
- Every $ spent lands in water_ledger with reservoir label. Every claim in receipts = measured or UNVERIFIED.
- Restart discipline: no gateway restarts during the window unless something is on fire (in-flight runs die).
- One supervisor: Mag docker stack; ticker is OpenClaw cron (sanctioned mill), not a second gateway.
