pass e, supplement to BURN_free-resource-landscape_20260927_d.md

# Free-resource landscape: LLM7 + Scaleway redo probe (2026-09-27)

## Verdict

steal

## Evidence

- LLM7 `GET https://api.llm7.io/v1/models`, unauthenticated, attempt 1: HTTP 200, 63,722 bytes. 64 unique model ids (grep count of `"id"` fields, sort -u). Payload is an OpenAI-shaped `{"object":"list","data":[...]}` with per-model tier and pricing fields (example entry: tier "turbo", pricing_mode "token", USD per 1M tokens). Model list includes DeepSeek-V4-Flash-0731.
- Scaleway `GET https://api.scaleway.ai/v1/models`, unauthenticated, attempt 1: HTTP 401, 80 bytes, body `{"status":401,"error":"UNAUTHORIZED","message":"missing 'Authorization' header"}`. Key-gated as expected; that is the finding, not a failure.
- Scaleway docs `https://www.scaleway.com/en/docs/ai-products/generative-apis/`: HTTP 404. No free-tier documentation observed at that URL; filed as-is.
- WebSearch "LLM7 free API 2026" (one search, per rules): LLM7 described as a free OpenAI-compatible gateway; as of Aug 2026 anonymous access is limited to select models and a free token from token.llm7.io unlocks the rest. Corroborates the live unauthenticated list.

Probe discipline: 1 of 2 curl attempts used per endpoint, 20s timeout each, no key material involved.

## Steal or Vacuous

- LLM7: GOES HOT. Unauthenticated 200 with 64 models is the known shape of a usable free lane; anonymous tier exists today with select models, free token widens it. Worth a follow-up probe of actual completion round-trips (chat/completions) and rate-limit behavior before any harness wiring.
- Scaleway Generative APIs: STAYS DEAD for unauthenticated fleet use. 401 without a key, and the docs path probed returns 404, so no documented free tier was observed in this pass. Not chased further under the no-fabrication rule.

## Bibliography

- https://api.llm7.io/v1/models (probed, HTTP 200)
- https://api.scaleway.ai/v1/models (probed, HTTP 401)
- https://www.scaleway.com/en/docs/ai-products/generative-apis/ (probed, HTTP 404)
- WebSearch "LLM7 free API 2026" result snippets only, pages not opened: tokengratis-m9jj.vercel.app (Aug 20, 2026 note on anonymous limits and token.llm7.io), freecodingmodels.vercel.app, api-battle.pages.dev, dev.to 35+ free providers list.
