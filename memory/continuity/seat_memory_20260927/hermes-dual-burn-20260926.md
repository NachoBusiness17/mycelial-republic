---
name: hermes-dual-burn-20260926
description: Hermes $180 credit burn COMPLETE 9/26 late (LAW-11 execution) — 150/150
  game briefs dual-run through Nous inference API
  (glm-5.3-prime/qwen3.8-max-prime/ember-1 rotation, ~724K tokens) as dual-runtime
  verification of the game-dig wheel specs; parallelized 6 workers mid-run,
  checkpoint switchover lost zero jobs
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fce37d85-5c78-49f1-81cb-d55612026cab
---

2026-09-26 operator: "we also have 180$ in hermes credits we need to blow." LAW-11 ([[law-11-credits-over-failure]]) execution: the credits fund dual-runtime verification of the five game-dig wheel specs ([[game-dig-workflows-20260926]]) — same 150 briefs, second engine, findings cross-compared.

**Lane:** Nous inference API (OpenAI-compatible, https://inference-api.nousresearch.com/v1), keys HERMES_API_KEY_1/2 loaded via `models.env_load.load_dotenv()` from .env (sk-nou prefix, never print beyond prefix). Verified live with a 1-call probe ("LANE LIVE", 19/50 tokens). Model rotation per call: z-ai/glm-5.3-prime → qwen/qwen3.8-max-prime → fireworks/ember-1; config note: reasoning models burn thinking out of max_tokens, so 8000 sized.

**Driver:** watch/inbox/hermes_dual_burn_20260926.py — all 150 briefs, per-job checkpoint to logs/hermes_dual_20260926/output.jsonl (JSON-per-line, resume = skip done ids read from the same literal file), retry 5x with 30s*attempt backoff + key + model rotation, host allowlist + getaddrinfo IP-class blocking on every request (Mimosa SSRF guard). Honest finding baked in: cached/async refunds and failures are logged per-call; runs AFTER the 50-wide rate-limit hit, but Nous is a different provider so it does not touch the z.ai window.

**Why it matters:** cross-engine comparison = the muratcan dual-runtime law applied to research (divergent findings between engines mark the weak claims in the wheel specs). Related: [[width-envelope-amendment-20260926]], [[game-dig-workflows-20260926]], [[bash-hook-guard-workarounds]].

**PARALLELIZED 9/26 late (operator: "how do we speed this up" then "show me your moves"):** the sequential driver was the bottleneck (1 call at a time across 150 jobs); killed at 74/150 checkpoint and relaunched as watch/inbox/hermes_dual_burn_parallel_20260926.py — ThreadPoolExecutor 6 workers, same literal OUT_FILE checkpoint (resume = skip done ids, zero loss on switchover), per-attempt model+key rotation, write_lock serializing appends. 6x second-engine throughput on a provider with its own quota (does not touch the z.ai window). Lesson: checkpointed drivers make width a free knob — kill, re-slot, relaunch.
