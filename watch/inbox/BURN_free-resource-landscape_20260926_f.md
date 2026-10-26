# BURN receipt: free-resource-landscape (2026-09-26, pass f)

## Verdict
steal

## Evidence
1. console.groq.com/docs/prompt-caching (read 2026-09-25, pass c; snippet refetched 2026-09-26 unchanged): "Cached tokens do not count towards your rate limits" and the caveat "cached tokens are subtracted from your limits after processing, so it's still possible to hit your limits." Window: "128 to 1024 tokens" minimum by model, "Exact Prefix Matching", 2 hour idle expiry, auto-on. Quantified on paper, never measured live.
2. console.groq.com/docs/rate-limits (passes a/b 2026-09-25; headers via fresh search 2026-09-26): x-ratelimit-* response headers, 429 retry-after, org-level limits.
3. Repo call path: mag/lane_probe.py groq lane = GROQ_API_KEY, POST https://api.groq.com/openai/v1/chat/completions, model openai/gpt-oss-20b; mag/free_tier.py groq surface "~1.9s/call at 91% ok"; models/providers.py:415 browser-like UA because Cloudflare (groq) returns 403/1010 to a bare UA; mag/_cache_ab_probe.py is the working precedent for reading usage.prompt_tokens_details.cached_tokens across a frozen-prefix pair.
4. memory/facts/behavioral.jsonl: 472 rows, grep -ci groq = 0. No groq lane config lives there; it lives in code. Filed as a miss, not synthesized.

## Steal or Vacuous
Steal: the live bypass measurement protocol (spec only; zero API calls executed this pass).
(a) Arms. Model openai/gpt-oss-120b (the 1K RPD / 8K TPM row). FROZEN arm: one fixed prefix over 1024 tokens (clears the worst-case minimum), repeated verbatim, tiny numbered tail. FRESH arm: same total length, unique body every call. Transport: the lane URL above, Bearer $GROQ_API_KEY read from .env at runtime (value never logged or copied), browser-like UA, max_tokens 16.
(b) Observables. Body: usage.prompt_tokens, usage.prompt_tokens_details.cached_tokens, usage.total_tokens. Headers captured verbatim: x-ratelimit-limit-requests, x-ratelimit-remaining-requests, x-ratelimit-limit-tokens, x-ratelimit-remaining-tokens, retry-after. Per honest_cache_meter law: raw blobs stored, tokens never estimated.
(c) Measurement. Five interleaved pairs (F, Z, F, Z...) inside the 2 hour TTL; frozen call 1 primes, calls 2 to 5 are hits. Per call record the remaining-requests decrement (request-axis cost) and the remaining-tokens decrement against prompt_tokens minus cached_tokens (token-axis refund). First call also reads x-ratelimit-limit-requests to confirm the 1K/day denominator before attribution (plan-toggle drift guard).
(d) Open dependency. A free-plan GROQ_API_KEY in repo .env. Only key names were inspected (the lane_probe loader reads names, never values). If the key resolves Developer-plan, rerun and restate the denominator from response headers, not the docs table.

## Falsifier
Pre-registered, two kill conditions. (1) Token axis dies if frozen-arm calls 2 to 5 read cached_tokens = 0, or remaining-tokens drops by the full prompt_tokens on hits. (2) Scope guard against a narrower-than-finding closure: the doctrine claims a token refund, never a request refund; remaining-requests decrementing identically in both arms with nonzero cached_tokens is expected, not a kill; the doctrine then files as measured, bounded to the TPM/TPD axis, 1K RPD wall untouched. A 429 inside the frozen arm despite nonzero cached_tokens kills the scaled hammer use.

## Bibliography
- watch/inbox/LINKS.jsonl (SCOUT rows, 2026-09-20 to 09-22)
- watch/inbox/BURN_free-resource-landscape_20260925.md, _c.md, _e.md (prior passes; quantified bypass and the open row)
- memory/facts/behavioral.jsonl (472 rows, zero groq mentions)
- mag/lane_probe.py, mag/free_tier.py, mag/_cache_ab_probe.py, mag/honest_cache_meter.py, models/providers.py
- https://console.groq.com/docs/prompt-caching (page read pass c 2026-09-25; snippet refetched 2026-09-26)
- https://console.groq.com/docs/rate-limits (page read passes a/b 2026-09-25; headers via search 2026-09-26)
- One fresh web search 2026-09-26 (one backend 429 code 1302, then results returned)
