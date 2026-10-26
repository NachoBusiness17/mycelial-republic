# BURN free-resource-landscape 20260927 j

## Verdict

steal

## Evidence

Time math: `date -u` at probe time returned 2026-09-27T23:02:20Z (UTC hour 23); weekday check returned 2026-09-27 Sunday (day=7). 2026-09-27 23:0x UTC is inside the classic off-peak canon (16:30-00:30 UTC) and is a weekend hour, fully off-peak under the newer shape below. In-window under BOTH candidate definitions.

DeepSeek liveness: `curl -s https://api.deepseek.com/models` unauthenticated at 2026-09-27T23:02Z returned HTTP 401, body "Authentication Fails (governor)". Alive (endpoint answers, rejects keyless as designed; connection refused would mean dead).

LLM7 roster: `curl -s https://api.llm7.io/v1/models` keyless returned HTTP 200, `{"object":"list","data":[...]}`; turbo tier includes `"id":"DeepSeek-V4-Flash-0731"` with `"tier":"turbo","usage_based_only":true` and `"id":"GLM-5.3-Flash"` with `"tier":"turbo","usage_based_only":false` (keyless-viable), availability_last_hour_percent 100.0.

LLM7 turbo chat probe: attempt 1 to `POST https://api.llm7.io/v1/chat/completions` (model GLM-5.3-Flash, max_tokens 5, prompt "reply ok", keyless) returned HTTP_CODE:000, a transport-level failure with no HTTP answer, cause unknown (owed). Attempt 2 returned HTTP 200 EXIT:0, body coarse shape: `{"choices":[{"finish_reason":"length","message":{"content":"","reasoning_content":"..."}],"model":"GLM-5.3-Flash","usage":{"completion_tokens":64,"prompt_tokens":14}}`. No 429.

Window definition (WebSearch "DeepSeek off peak pricing hours UTC", thin): only source found was a third-party aggregator, getaiperks.com, dated Sep 16, 2026: "Peak hours are 01:00 to 04:00 and 06:00 to 10:00 UTC on weekdays. Everything else, including weekends, is off-peak at half price." This conflicts with the classic 16:30-00:30 UTC daily canon and is NOT an official source; DeepSeek's official pricing page was not fetched this pass (owed). The search itself conceded: "Some sources reference different or updated windows for newer model versions."

## Steal or Vacuous

DeepSeek off-peak: STEAL. API alive (401 governor, not refused) and UTC 23h Sunday is in-window under both the 16:30-00:30 canon and the weekday-peak-blocks shape, so half-price off-peak inference is hammerable right now. Churn flag: the window definition itself may have moved shape; byte-verify the official pricing page before scheduling heavy lanes.

LLM7 turbo: USABLE-AGAIN. Keyless chat cleared with 200 on the turbo tier, no 429 wall at n=1, and the roster confirms turbo ids live. One probe cleared is not wall breadth measured, and one 000 transport failure sits in the record; single-probe status.

Groq cached-token RPDs, OpenRouter 1000 rpd, Featherless roster diff: not probed this pass, board status unchanged, owed.

## Bibliography

- `date -u` probe-time and weekday reads, 2026-09-27T23:02-23:05Z
- curl GET https://api.deepseek.com/models (unauth, 2026-09-27T23:02Z)
- curl GET https://api.llm7.io/v1/models (keyless, 2026-09-27T23:03Z)
- curl POST https://api.llm7.io/v1/chat/completions x2 (keyless, turbo tier, 2026-09-27T23:03Z)
- WebSearch "DeepSeek off peak pricing hours UTC" returning getaiperks.com snippet, Sep 16 2026
- watch/inbox/LINKS.jsonl (tail -30)
- memory/facts/behavioral.jsonl (tail -30)
