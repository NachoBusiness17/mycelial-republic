ROW
pointer: https://api.z.ai/api/paas/v4 + glm-4.7-flash (env ZAI_API_KEY)
claim: reachable / 541ms
type: probe
confidence: H
status: BLOCKED
evidence: HTTP 429 @541ms; error 1305 "service may be temporarily overloaded, please try again later"; no x-ratelimit/retry-after headers returned
ROW
pointer: https://api.z.ai/api/paas/v4 + glm-4.7-flash (env ZAI_API_KEY_PRO)
claim: reachable / 8833ms
type: probe
confidence: H
status: VERIFIED
evidence: HTTP 200 @8833ms; body choices[finish_reason=length] content="" (max_tokens 1); no rate-limit headers returned
ROW
pointer: https://api.z.ai/api/paas/v4 + glm-4.7-flash (env ZAI_API_KEY_LITE)
claim: reachable / 45006ms
type: probe
confidence: H
status: BLOCKED
evidence: connection ERR (socket hang up) @45006ms at 45s timeout; no HTTP status, no headers
ROW
pointer: https://api.z.ai/api/coding/paas/v4 + glm-4.7-flash (env ZAI_API_KEY_2)
claim: reachable / 15451ms
type: probe
confidence: H
status: VERIFIED
evidence: HTTP 200 @15451ms; body choices[finish_reason=length] content="" (max_tokens 1); no rate-limit headers returned

QUOTA LAW
zai: RATE-HOE — 429/overloaded on light call; NOT safe for prime-hour work (retry, back off)
zai-pro: SLOW-WORKING — 200 in 8.8s on max_tokens 1; tolerable for light work, avoid prime-hour bursts
zai-lite: DEAD-LINK — socket hang up/timeout; not safe for any work right now
zai-2: SLOW-WORKING — 200 in 15.5s on max_tokens 1; heavy latency, light work only, not prime-hour
