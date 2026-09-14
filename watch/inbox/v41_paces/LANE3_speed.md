# LANE3 — V4.1 Flash real streaming speed + cache behavior (2026-09-11, zcode seat)

**THE POINT:** measured `deepseek-flash` (the live API id for V4.1 Flash — confirmed
via `GET /v1/models`, which now serves only `deepseek-flash` + `deepseek-v4-pro`; the
old `deepseek-v4-flash` id is gone) through our own key, streaming SSE, thinking
disabled, temp 0.2. 5 calls, ~$0.003. Raw data: `LANE3_speed_data.json`.

## Measurement table

| call type                          | tok/s (stream) | tok/s (e2e) | cache status            | TTFT ms | total latency ms |
|------------------------------------|---------------:|------------:|-------------------------|--------:|-----------------:|
| A cold — fresh ~1k-token prompt    | 138.8          | 95.2        | 0% hit (981 miss)       | 1008.7  | 3214.0           |
| A warm — same prompt again         | 176.6          | 119.9       | 78.3% hit (768/981)     | 798.1   | 2527.9           |
| B partial — shared prefix, new Q   | 158.8          | 112.6       | 78.4% hit (768/980)     | 721.5   | 2478.6           |
| C1 — fresh 2477-token prompt       | 171.7          | 121.5       | 0% hit (2477 miss)      | 701.8   | 2403.3           |
| C2 — same 2477-token prompt again  | 158.3          | 106.6       | 93.0% hit (2304/2477)   | 866.0   | 2655.2           |

tok/s (stream) = completion_tokens / (last-delta − first-delta) — the true decode rate.
tok/s (e2e) = completion_tokens / total wall time, TTFT included.

## 2000-token cache pair (C1 vs C2)

- Prompt: 2477 tokens both calls, byte-identical.
- C2 hit 2304/2477 = **93.0%** (2304 = exactly 36×64 — DeepSeek's 64-token block granularity; the ~173-token tail never hits).
- Latency delta: C2 was **+252 ms SLOWER** end-to-end (2655 vs 2403 ms) and TTFT was not better (866 vs 702 ms). At this prompt size, a 93% cache hit bought zero latency.
- Warm pair A (1k prompt): cache saved ~210 ms TTFT and ~35 ms stream, +31% tok/s (139→177).

## Verdict (tri-state)

- **295/390 tok/s claim: DISPUTED.** Measured decode rate 139–177 tok/s across 5 calls
  (best single call 176.6). That is 45–60% of the 295 claim and under half the 390 claim.
  No call, cold or warm, approached either number. DSpark speculative drafting is not
  showing up as 2x decode on our surface.
- **97% cache claim: PARTIAL.** Directionally real, number not reproduced: 93.0% on the
  2477-token repeat, 78.3% at ~1k tokens. Hit ratio scales with prompt length because the
  trailing partial block (plus suffix) never caches. Expect ~90%+ only on long, identical,
  repeated prefixes.
- **Cache = cost play, not speed play** (at our sizes): cached tokens bill ~10x cheaper,
  but latency was flat-to-worse on the hit call. TTFT gain only showed on the smaller pair.

**Fleet read:** as a routing lane, deepseek-flash behaves like a ~150-175 tok/s decoder
with aggressive prefix caching — still the cheap read-heavy lane; the marketing speed
numbers are not on our surface.

Method: raw SSE via urllib, same pattern as `models/providers.py chat_messages` +
`_iter_sse_events`; usage from final streamed chunk (`stream_options.include_usage`),
cache split from `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens`. 5 chat calls
spent (bound was 6), model id probe was the free `/models` endpoint.
