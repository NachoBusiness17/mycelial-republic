# BURN receipt: free-resource-landscape (2026-09-25, pass c)

## Verdict
steal

## Evidence
1. Groq rate-limits page (fetched 2026-09-25) carries exactly one caching sentence: "Cached tokens do not count towards your rate limits." No per-limit spec (RPM/RPD/TPM/TPD/ITPM/OTPM), no tier gate, no cap. All detail defers to /docs/prompt-caching.
2. Groq prompt-caching page (fetched 2026-09-25) quantifies the window: "Prompt caching works automatically on all your API requests with no code changes required"; "automatically enabled and cannot be manually disabled"; "Minimum cacheable prompt length varies by model, ranging from 128 to 1024 tokens"; "Exact Prefix Matching"; "All cached data automatically expires after 2 hours without use"; volatile memory. Billing: "50% discount for cached input tokens", discount "only on successful cache hits", does not stack with batch discount.
3. The caveat prior passes missed, same page: "However, cached tokens are subtracted from your limits after processing, so it's still possible to hit your limits." The bypass is an after-the-fact accounting refund, not an upfront exemption. One oversized request can breach the wall before the refund lands.
4. No tier gate and no bypass cap are documented anywhere on either page. Free vs Developer tables exist only on the rate-limits page; caching text is plan-agnostic.
5. Fresh search for other free-tier vendors documenting a cache-bypass: none found. NVIDIA developer-forums snippet (Aug 2026) lists cached tokens only as pricing line items alongside rate limits; no bypass claim. Cerebras: nothing. Aggregator hits (evalics.com, fastrouter.ai, dev.to, medium) discuss caching purely as cost/latency optimization, snippets only, not fetched.

## Steal or Vacuous
Steal, three adoptions:
1. Upgrade pass-b doctrine from headline to bounded mechanism. The stealth window is real and free-plan-agnostic as documented: auto-on, exact frozen prefix, 128 to 1024 token minimum (fleet frozen-prefix signatures clear it), 2 hour idle TTL, so a lane must re-hit the prefix within 2 hours or re-prime it. Register these parameters in chat_provider lane notes.
2. Bound the hammer pattern: the bypass sustains bursts of many prefix-shared small asks (the deliberate-ask signature), not single mega-prompts, because tokens are subtracted after processing. Cap any window run at prompt sizes under the TPM floor and keep asks tight.
3. Keep the bypass Groq-specific: no other free-tier vendor documents it. Do not generalize cache-evasion assumptions to NVIDIA or Cerebras lanes.

## Falsifier
Pre-registered live-lane probe: send 10 identical frozen-prefix requests (prefix above 1024 tokens, small ask) to free-plan gpt-oss-120b inside one minute. Prediction: prompt_tokens_details.cached_tokens nonzero from request 2 onward and no 429. Control: 10 unique-prefix requests of the same size will 429 once fresh tokens cross 8K TPM. If cached_tokens reads zero or 429s fire in the prefix arm, the bypass doctrine dies.

## Bibliography
- watch/inbox/LINKS.jsonl (SCOUT rows 276-305)
- memory/facts/behavioral.jsonl (skimmed, 404 rows; frozen-prefix deliberate-ask invariants only, no vendor facts)
- watch/inbox/BURN_free-resource-landscape_20260925.md and _b.md (prior passes, read in full)
- https://console.groq.com/docs/rate-limits (fetched 2026-09-25)
- https://console.groq.com/docs/prompt-caching (fetched 2026-09-25)
- Web search snippets citing evalics.com, fastrouter.ai, dev.to, forums.developer.nvidia.com, llmrumors.com (snippet-level only, none fetched, not adopted as evidence)
