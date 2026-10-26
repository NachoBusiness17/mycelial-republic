# PROVIDER KEY ASKS: what only the operator can do (gate 2 outcome)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 · **Class:** RECEIPT / documented asks

Probed live this pass: none of the three signups can be completed by this seat (accounts need your email/browser; no free token path exists keyless). What I verified so you do not sign up blind:

1. **llm7.io** — key REQUIRED for inference (verified live: missing_api_key on a catalog model). Catalog has 64 models and ZERO zero-price ones: the free tier is gone; it is now a cheap paid marketplace. Signup: dash.llm7.io. Worth it ONLY as a cheap lane: DeepSeek-V4-Flash-0731, 400K context, tools/reasoning/JSON, $0.02/M input and $0.04/M output. Paste the key back as LLM7_API_KEY.
2. **SiliconFlow** — console signup (email), key from Create API Key, no card mentioned in quickstart. Base: api.siliconflow.com/v1. Verify their Sep 2026 ToS automation clause when you are in the console. Paste back as SILICONFLOW_API_KEY.
3. **Chutes.ai** — signup (chutes.ai), Bearer key from dashboard. Endpoint llm.chutes.ai/v1. Per-token from ~$0.0245/M; failed requests not billed; optional $10-20/mo bundles. Paste back as CHUTES_API_KEY.

Standing note: keys go into .env under those names and get a 1-token liveness test + providers.yaml entry through the normal operator-gated promote path. No lane decisions happen before your keys exist.
