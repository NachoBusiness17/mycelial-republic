---
name: glm-flashx-not-on-plan-20260927
description: GLM-5.3-FlashX 9/27 — not on the coding plan (paid API tier, 2.5x Flash); probe BUILT+FIRED on operator "build it" order: DECLINED per frozen rule (default thinking tax makes first-content token SLOWER than flash despite 2.36x faster decode); flip = reasoning-disabled refire
metadata:
  type: project
---

Operator asked 2026-09-27 "why arent we using glm x" → clarified GLM-5.3-FlashX. Answer given on facts:

- glm-5.3-flashx announced 2026-09-18: same 5.3-Flash capability base at ~200 tok/s (5x Flash); 320B MoE 18B activated, 1M context.
- NOT on the coding plan: fresh ListModels shows only GLM-5.3 + GLM-5.3-Flash across all three plan families (individual/start/offpeak). FlashX is a separate paid API tier (zai-api) at 2.5x Flash price. No fleet lane can fire it without a paid key.
- Lane math (extends [[ractor-panel-ladder-20260927]] and [[width24-experiment-verdict-20260926]]): the burn wall is rolling ADMISSION (~7 streams), not decode speed; thinking-dominated judgment lanes gain almost nothing from 5x faster decoding behind the same limiter. FlashX earns its 2.5x price only on latency-facing consumers: operator's interactive seat, mag companion cycle, Roblox NPC gateway, phone relay.
- Scout miss named: announced 09-18, zero canon rows until the question; LINKS row filed 9/27 (writer zcode-flashx-scout) with the lane math attached.

**Probe receipt (tools/flashx_probe.py, watch/inbox/FLASHX_PROBE_20260927.md, INDEX-registered + LEDGER row, spend ~$0.02):** flashx TTFT first-content 5,246ms vs flash 3,521ms (0.67x); total 5.37s vs 12.65s (2.36x faster decode); diagnostic: 133 of 138 completion tokens on a trivial prompt were reasoning_tokens. Fresh failure mode named in LEDGER: "speed tier with default thinking ON loses the first-content-token race it is sold for". Measurement lesson: first pass returned null TTFT (parser counted only content deltas while thinking ate the 220-token budget); the null verdict was DISCARDED as measurement failure, never filed, then fixed (count reasoning deltas separately, budget 600, stream_options include_usage). Probe passed the violation ratchet clean.

**Why:** prevents re-deriving the model-availability question every window; the plan model list is the seat-level source of truth regardless of pricing journalism.

**How to apply:** when a new model tier appears, check ListModels first (admission decides), then ask whether the fleet bottleneck it targets (speed vs admission vs thinking depth) matches the lane shape; file the scout row same day.
