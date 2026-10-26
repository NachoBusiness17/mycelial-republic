---
name: dogfood-canonical-machinery-20260917
description: operator self-steal correction 2026-09-17 — "we had mechanisms for all of
  this... we even have a switchboard you redesigned yesterday. you need to be dogfooding
  everything" — models/providers.py chat_provider (65,536 ceiling, quota, peak-defer,
  tiers, multi-key) + configs/providers.yaml (26 ids incl. nvidia, z_ai3) already solved
  what I re-built bespoke; LOOK before writing transport
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Operator correction 2026-09-17, after I hand-rolled urllib lanes all night: "self steal — we
had mechanisms for all of this. No sacred cows — have it inform what you are building. We
even have a switchboard you redesigned yesterday. You need to be dogfooding everything."

**What already existed (found by walking the machinery instead of writing new):**
- `models/providers.py::chat_provider(provider_id, system, user, *, model, temperature,
  max_tokens=65536, tier, session_id, thinking, timeout, allow_peak)` — the canonical door:
  **65,536 default max_tokens** (codified 08-29 under operator order: "mine the ceiling by
  default... callers opt DOWN; never up from crumbs"), quota tracking via
  models.quota (pick_provider/provider_budget/record_usage), PEAK GATE (paid providers defer
  during DeepSeek peak 2x windows; MAG_ALLOW_PEAK=1 overrides), tier security (T0/T1
  fail-closed on remote), multi-key rotation with key_idx in meta, opencode_only refusal for
  coding-plan keys, empty-content honesty (finish=length = budget failure, reported not
  faked). Returns {ok, text, provider, model, usage, budget_after, key_idx}.
- `configs/providers.yaml` — 26 provider ids: groq, cerebras, mistral, cohere, gemini,
  together, deepseek(+_overmind), xai, openrouter, openai, anthropic, vast, github_models,
  moonshot, fireworks, hf_router, dashscope, saelis, ollama, z_ai…z_ai4, **nvidia**
  (NVIDIABuild key, live 70 chars; 102 models incl. qwen, deepseek-v4-flash verified 3.4s,
  moonshot kimi, gpt-oss; 100 calls/month quota), **z_ai3** = the Lite seat.
- Switchboard/effect broker (mag/auth_switchboard.py, mag/effect_broker.py) — effects
  authorize there, not in driver code.

**Fixed en route:** z_ai3's base_url was stale /api/paas/v4 (endpoint law: coding keys
fake-1113 there) → corrected to /api/coding/paas/v4 in the yaml so every canonical caller
inherits the fix.

**How to apply:** before writing ANY transport/lane code, walk the canonical surfaces first
(chat_provider signature, providers.yaml ids, switchboard, salon_phone's gate pattern) —
bespoke HTTP is only justified for capabilities the registry lacks (e.g. dual-key rotation
across OPENROUTER_API_KEY + _2). The Librarian ([[the-librarian-fleet-imprint-20260917]])
is the standing structural fix: ask it before building.

Related: [[no-token-caps-100k-windows]], [[lite-key-seat-glm53flash]],
[[union-fullsend-day-20260917]].
