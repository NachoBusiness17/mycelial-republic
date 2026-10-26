# MUSE_SPARK_ACCESS_20260928 — Access Recon Bank

**Date**: 2026-09-28
**Scope**: meta/muse-spark-1.3 on OpenRouter — whether a 403 is a free-tier gate or a key-tier gate
**Verdict**: 403 is a KEY-TIER gate (permission_denied), not a free-tier gate.

## Evidence

### Model pricing (paid, not free)
- Source: https://openrouter.ai/meta/muse-spark-1.3
- Muse Spark 1.3: $1.25/M input tokens, $4.25/M output tokens, $0.15/M cache read
- Context window: 1,048,576 tokens; released Sep 2, 2026 by Meta
- "Muse Spark 1.3 Contributor" (the free/cheap tier): $0.10/M input, $0.20/M output — but that's a *different model slug*, not the same as "free access to muse-spark-1.3"

### OpenRouter 403 meaning (from official docs)
- Source: https://openrouter.ai/docs/api/reference/errors-and-debugging
- OpenRouter's typed error vocabulary:
  - `authentication` → 401 (bad/missing key)
  - `payment_required` → 402 (insufficient credits)
  - `permission_denied` → 403 (insufficient permissions, guardrail block, moderation flag)
  - `rate_limit_exceeded` → 429
- The docs explicitly say: "403: Forbidden (insufficient permissions, guardrail block, or moderation flag)"
- Guardrail example: `{"error": {"code": 403, "message": "Request blocked: prompt injection patterns detected"}}`

### Free-tier rate limits (not 403)
- Free models: 50 req/day without credits, 1000 req/day with ≥$10 account credits
- Exceeding free-tier caps → 429 (rate limit), never 403
- Credit exhaustion → 402 (payment required)

## Diagnosis

| Symptom | Likely cause | Error code |
|---|---|---|
| 403 on muse-spark-1.3 | Key lacks permission, guardrail block, or moderation flag | permission_denied |
| 403 on muse-spark-1.3 Contributor | Same — Contributor is a separate paid tier ($0.10/$0.20) | permission_denied |
| 429 | Free-tier cap hit | rate_limit_exceeded |
| 402 | Account out of credits | payment_required |

## Conclusion

**The 403 is a key-tier gate.** It means the API key used does not have permission to access meta/muse-spark-1.3 — possible causes:
1. The key belongs to an account that hasn't agreed to Meta's model terms (Meta models sometimes require explicit opt-in).
2. A guardrail/moderation block on the request content.
3. The key is a free-tier key that was never provisioned for paid-model access.

It is NOT a free-tier rate limit — those produce 429. And muse-spark-1.3 itself is a paid model, so "free tier" doesn't apply to it at all (the Contributor variant at $0.10/$0.20 is a separate slug).

## Action
- Check the key: `GET https://openrouter.ai/api/v1/key` → look at `is_free_tier`, `limit_remaining`, `free_model_daily_requests`
- If `is_free_tier: true`, the key needs credits or an upgrade to access paid models
- If the key has credits but still 403, check the error `metadata` for guardrail/pattern details
