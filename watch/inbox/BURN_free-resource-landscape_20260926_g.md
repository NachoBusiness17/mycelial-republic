# BURN receipt: free-resource-landscape (2026-09-26, pass g)

## Verdict
steal

## Evidence
Executed per pass f protocol. GROQ_API_KEY read from repo .env at runtime (name inspected only, never printed). Model openai/gpt-oss-120b, POST api.groq.com/openai/v1/chat/completions, browser-like UA (models/providers.py:443), max_tokens 16, temperature 0. Raw blobs: logs/groq_cache_bypass_20260926.jsonl (28 rows). Pre-reg said 10 calls; executed 3 cycles: 21 HTTP 200 + 7 429. Header denominator: x-ratelimit-limit-requests = 1000 (free plan confirmed), x-ratelimit-limit-tokens = 8000 (the 8K TPM row, not 30K). rem_req 589 at open, 572 at close.
Run 1 (prefixes 2339 to 2802 tokens, 1s pacing): calls 1-2 returned 200, then 429 type "tokens", retry-after 4 to 13s. Fresh control: 7,529 reported tokens through the window before the wall.
Run 2 (prefixes 1298 to 1304 tokens, 15s pacing): 10/10 200. Bucket refills to cap between calls, so each snapshot reads exactly that call's charge: fresh 6680 = 8000 - 1320 (total_tokens), frozen 6685 = 8000 - 1315, including pair 4 frozen (cached_tokens = 1280 reported) which still snapshotted the full 1315 charge.
Hammer (8 back-to-back frozen calls, zero pacing): 8/8 200, reported totals 2594 + 7x1314 = 11,792 tokens in ~8s against lim_tok 8000, zero 429. h1 exact refund signature: charge 8000 - 6686 = 1314 = 2594 - 1280 cached. h6 and h8 rem_tok ticked UP (1642 to 1660, 407 to 446): refunds posting asynchronously. cached_tokens reported on only 4/18 frozen-arm calls (field absent otherwise, flaky).

## Steal or Vacuous
Steal, scored per axis. Request axis: NO refund. rem_req decremented exactly 1 per 200 in both arms (run 2: 588 down to 579; hammer: 579 down to 572). The 7 run-1 429s did not decrement it (588 read at run 2 open, above the 587 pre-429 sequence). Expected per pre-registration, not a kill. Token axis: bypass CONFIRMED, ASYNC shape. Snapshots always read full charge (paced run 2), yet operationally the frozen arm carried 11,792 reported tokens through the same 8K window that 429'd fresh traffic at 7,529 (1.57x), zero 429, with an exact arithmetic refund on h1 and upward rem_tok ticks on h6/h8. Matches the docs caveat "cached tokens are subtracted from your limits after processing". Bounded to the TPM axis; TPD exposes no response header, unmeasured.

## Falsifier
Pre-registered pass f, updated with results. (1) Token-axis kill: the literal snapshot condition fired (cached_tokens absent on 14/18 frozen calls; full-charge snapshot on the confirmed cached_tokens=1280 call), but the hammer clause resolves it: zero 429 across 8 back-to-back frozen calls past the wall that killed fresh control, so the scaled hammer use SURVIVES. Doctrine files as measured, async-refund shape, bounded to TPM. (2) Scope guard held: 1:1 request decrement in both arms, expected and observed. Run 1's frozen-arm 429 preceded any nonzero cached_tokens reading, so the "429 despite nonzero cached" kill was not met.

## Bibliography
- watch/inbox/BURN_free-resource-landscape_20260926_f.md (pre-registration; executed with 3 cycles instead of 10 calls, disclosed above)
- logs/groq_cache_bypass_20260926.jsonl (raw per-call bodies + headers, 28 rows, this pass)
- mag/lane_probe.py, mag/free_tier.py, mag/_cache_ab_probe.py, models/providers.py:443
- https://console.groq.com/docs/prompt-caching and https://console.groq.com/docs/rate-limits (carried from pass f, unchanged)
