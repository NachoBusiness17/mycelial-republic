# DEEP RESEARCH — z.ai, all its offerings, and what we wired in (2026-08-24)

**Commitment:** `deep-research-zai-offerings-001`
**Operator:** "what the fuck is autoclaw wow do a deep research dive on zai and all its offerings
and what i just did and wire everything in including autoclaw or anything else we can pick up steal"
**Method:** docs.z.ai (llms.txt index, pricing, GLM-4.7 model doc, devpack, cache doc, FAQ),
autoclaw.z.ai (home + changelog), OUR telemetry (z_ai lane 81% ok / 1305 overload; cache fires on
12-token prompt). Everything below is grounded in those fetched pages.

## The full z.ai surface (what exists)

### Text models (pricing, per 1M tokens)
- **Frontier paid:** GLM-5.3/5.2/5.1 ($1.4 / cached $0.26 / out $4.4), GLM-5 ($1/$0.2/$3.2),
  GLM-5-Turbo ($1.2/$0.24/$4.0).
- **Workhorse paid:** GLM-4.7 ($0.6/$0.11/$2.2), GLM-4.6, GLM-4.5, GLM-4.5-X, GLM-4.5-Air/AirX.
- **FlashX (near-free fast):** GLM-4.7-FlashX $0.07 / cached $0.01 / out $0.4 — 200K ctx, 128K out,
  lightweight high-speed, strong at coding. NOT free but pennies with cache mining.
- **FREE (all tiers, incl. cached + storage):** GLM-4.7-Flash, GLM-4.5-Flash — both 200K ctx /
  128K out. These are the cache-mining free lanes.
- GLM-4-32B-0414-128K ($0.1).

### The GLM-4.7 series — the coder (model doc, grounded)
- 200K context, 128K max output. Agentic coding SOTA among open models: SWE-bench Verified 73.8%,
  LiveCodeBench V6 84.9 (surpasses Claude Sonnet 4.5), Terminal Bench 2.0 41%, τ²-Bench 84.7.
- **RETENTION-BASED REASONING: "automatically preserves reasoning blocks across multi-turn
  dialogues, improving cache hit rates and reducing computational costs."** The vendor shipped OUR
  pattern: the model keeps its own cache warm. Also round-level reasoning (disable for simple
  tasks, enable for complex). Interleaved reasoning before each tool call.
- Function calling, structured output, streaming, context caching, web search tool.

### API surface (all OpenAI-compatible)
- Base: https://api.z.ai/api/paas/v4 (chat completions, streaming, thinking modes, function
  calling, structured output). OpenAI SDK compatible; official zai-sdk (pip install zai-sdk).
- Tools: Web Search ($0.01/use), Web Reader, tokenizer, layout parsing (GLM-OCR), GLM-Image
  ($0.015/img), CogView-4 ($0.01/img), CogVideoX, Vidu video, GLM-ASR audio, translation agent,
  slide/poster agent.
- Vision: GLM-5V-Turbo, GLM-4.6V, GLM-4.6V-Flash (FREE), GLM-4.5V, GLM-OCR.

### GLM Coding plans (devpack) — what the operator got
- Lite (2,000 credits/5h, 10,000/wk) / Pro (12,000/60,000) / Max (28,000/140,000).
- Models: GLM-5.3, GLM-5-Turbo, GLM-4.7. Credit multipliers: GLM-5.3 input 6.9 / cached 1.7 /
  out 24 (cached ~4x cheaper). Off-peak = 50%. Allowance is CACHE-HIT-SCALED: Lite 43-105M
  tok/wk by hit rate.
- Supported tools (STRICT): Claude Code, Cline, Roo, Kilo, OpenCode, OpenClaw, Crush, Goose,
  Cursor. Endpoints: api.z.ai/api/anthropic (Claude Code/Goose), api.z.ai/api/coding/paas/v4
  (others), api.z.ai/api/v1 (Responses). MCP servers: Vision, Web Search, Web Reader, Zread.
- PRICE CAVEAT (honest): devpack overview says "from $18/mo"; the GLM-4.7 page says "from
  $10/month". Pages disagree — confirm on the subscribe page before buying.

### AutoClaw (autoclaw.z.ai, by AutoGLM) — what the operator just signed up for
- Desktop AI agent for work (Windows 10+/macOS/iOS/Android), IM-integrated (WhatsApp, Telegram,
  Discord, Lark). GLM + DeepSeek models. 50+ skills: office (Word/Excel/PPT), content ops,
  investment research, web product building, browser automation, IM workflows.
- **Built on the OpenClaw kernel v6.8** (from the changelog). Features: connectors to external
  apps (Cloudflare, Vercel), Agent cluster mode, scheduled tasks, "Hermes evolution", check-in
  points/events, image recognition, design expert, cost-per-model hover stats.
- New users: 26,000 free credits (~$20, 30 days). GLM Coding plan connect: 150% quota boost +
  monthly login bonus (Lite 5,000 / Pro 10,000 / Max 26,000).
- No public API/local endpoint documented → it's a desktop/IM surface, not directly drivable
  from our code today. BUT its kernel (OpenClaw) IS a supported GLM Coding tool → programmatic
  path exists via OpenClaw CLI + the coding plan key (tomorrow).

## What the operator just did (mapped)
1. Got **GLM Coding Lite** (starts 2026-08-25) — frontier coder on dedicated quota.
2. **Signed up for AutoClaw** — desktop agent + 26k free credits + plan boost.
Together with the free flash lanes, that's the three-surface arsenal from the deep steal.

## What we wired in (2026-08-24, real bytes)
- **providers.yaml z_ai block**: added `glm-4.5-flash` (FREE at all tiers) as a second free
  cache-mining lane. `glm-4.7-flashx` (paid) and `glm-4.7` (paid) NOT wired into free lanes —
  noted in the config; paid deep-coding routes through the GLM Coding plan instead.
- **harness/glm_coder.py** — built + waiting (fail-closed) for tomorrow's GLM_CODING_API_KEY +
  a supported tool (claude CLI or OpenClaw CLI).
- Probe scripts: memory/runs/_probe_zai_cache.py (cached_tokens at scale),
  memory/runs/_probe_zai_ratelimit.py (headers: no x-ratelimit; cache fires on tiny prompts).

## The steals worth keeping (from this dive)
1. **Retention-based reasoning** (GLM-4.7) = the vendor making cache mining native. Our frozen-
   prefix discipline aligns with the model's own design — use round-level reasoning off for cheap
   scut, on for deep tasks.
2. **FlashX as the near-free fast tier**: $0.01 cached input at 200K ctx. For paid-escalation
   work that needs speed + quality beyond flash, FlashX is the cheapest fast step up.
3. **OpenClaw = programmatic path into the AutoClaw/agent machinery**: install OpenClaw CLI
   (supported GLM Coding tool) + coding plan key → a headless agentic coding lane, same family as
   AutoClaw, drivable from the machine. Add to tomorrow's list.
4. **The free lanes double**: GLM-4.5-Flash is a second free cache-mining lane on the same key.
5. **z.ai tools as cheap surfaces**: Web Search $0.01/use, GLM-OCR layout parsing, tokenizer —
   cheap deterministic tools to consider as fetch/parse helpers.

## Ordered next moves
1. THIS deep research (memory) — DONE.
2. providers.yaml z_ai free lane update — DONE (glm-4.5-flash added).
3. TOMORROW (plan live): GLM_CODING_API_KEY → .env; install a supported tool (claude CLI, or
   OpenClaw CLI for the agentic path); readiness green; route coding-intent through glm_coder.
4. Scale-probe the flash self-lane (measure cached_tokens per call, ~92% hit target).
5. AutoClaw in-app: claim 26k credits + connect GLM Coding plan (150% boost + monthly bonus).
6. Evaluate FlashX as a paid-escalation step (pennies, 200K ctx) when free lanes can't deliver.

## Refuse
- Wiring paid models (flashx/4.7) into the FREE lane rotation.
- Claiming AutoClaw is programmatically drivable without an API (it isn't, yet — OpenClaw path
  only).
- Trusting the $10 vs $18 price without a checkout-page check.

## Fold with
deep-steal-free-cache-self-20260824, glm-coding-lite-evaluated-20260824, cache-extract-joint,
tokenomics-cache-deep-dive, fuel_feed z_ai lane, free-usage-policy-iterate, clawbot thread.
