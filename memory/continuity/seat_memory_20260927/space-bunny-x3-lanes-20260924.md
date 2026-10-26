---
name: space-bunny-x3-lanes-20260924
description: Space Bunny Alpha stealth drop 9/24 — free 1M-ctx text+image+video
  reasoning model LIVE on three keys (OpenRouter nacho + fostertron/ox + Nous
  sk-nous); Nous = OpenRouter-compatible mirror (417 models); wired as nous_api
  provider; token starvation over for whole-corpus reads
metadata:
  node_type: memory
  type: project
  originSessionId: sess_d7f6f4b6-0b61-484e-8bea-0408db77ca4f
---

Tommy (Nous Research) drop 9/25 01:54Z quoting OpenRouter 9/23: `stealth/space-bunny-alpha`, anonymous, $0/$0, ctx 1,000,000, max completion 524,288, text+image+video→text, reasoning mandatory (default max, adjustable low..max), tools+response_format. Fleet verified all three lanes LIVE via `mag.probe_route probe --json` (self-steal, not raw curl): openrouter × 2 keys + Nous inference-api.nousresearch.com (HERMES_API_KEY_1/2, the sk-nous Hermes accounts). Nous serves a 417-model OpenRouter-compatible catalog — it is a mirror-relay.

Durable wiring: `nous_api` provider in configs/providers.yaml (gitignored file, edit persists locally), bunny added to openrouter models; probe organ allowlist fixed (+openrouter.ai — was blind to our biggest free host); LINKS-322; brief watch/inbox/SPACE_BUNNY_BURN_20260924.md.

**Why:** 1M-context free reasoning × 3 keys ends token starvation for whole-ledger reads; mandatory reasoning eats small max_tokens (30-token probe = empty content false-kill, budget 512+).

**How to apply:** route wide jobs through the normal lane ladder (no bespoke transport); comparative audit = same prompt × 3 keys, drift = signal; effort low for scut, max for judgment; video input is the unburned surface (Mr Pool/DOA mp4s); stealth windows expire — spend, don't hoard. Mirror drift is real: longcat-2.0:free dead on Nous, live on OR (selftest 4/5). Related: [[lite-free-window-schedule]], [[dogfood-canonical-machinery]], [[zcode-mobile-run-cards-20260920]].
