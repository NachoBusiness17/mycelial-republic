# BURN free-resource-landscape 20260928_b: LLM7 pro-tier keyless self-ID probe

## Verdict

steal

## Evidence

- Probe 1, gpt-6-astra, keyless POST https://api.llm7.io/v1/chat/completions (2026-09-28): HTTP 401, body verbatim: {"error":{"message":"Missing API key.","type":"authentication_error","param":null,"code":"missing_api_key"}}
- Probe 2, claude-opus-5-5, same keyless POST: HTTP 401, identical body, code "missing_api_key". Probes 3 and 4, grok-4.6 and kimi-k3: HTTP 401, identical body. 4 attempts, 4 auth walls, zero model output; the self-ID prompt ("State your exact model id and version... If you are a proxy or alias, say so.") never reached a model.
- Catalog https://api.llm7.io/v1/models (HTTP 200, 64 ids): all four frontier ids tier "pro", usage_based_only true, availability {"old":100.0,"mid":100.0,"recent":100.0}, availability_last_hour_percent 100.0. gpt-6-astra priced 2.5/9.0, claude-opus-5-5 3.2 output visible, grok-4.6 0.4/0.5, kimi-k3 2.0/10.0. The ids are advertised fully available yet anonymous requests are rejected at auth: the wall is paywall, not capacity.
- Churn note: /v1/models returned data as an object on two GETs and as a list on a third GET minutes later; response shape itself flaps within the hour.
- Web search "gpt-6-astra llm7" (2026-09-28): thin. One third-party aggregator, aile.sh (search snippet, not opened), lists claude-opus-5-5 and gpt-6-astra on llm7, marking gpt-6-astra "Offline" at 10.00/50.00 per M, which contradicts the live catalog (2.5/9.0, availability 100). No public documentation of alias vs real for any pro id.

## Steal or Vacuous

Per-id grades, rubric CONSISTENT / ALIAS-SUSPECT / UNKNOWN (error/empty): gpt-6-astra UNKNOWN, claude-opus-5-5 UNKNOWN, grok-4.6 UNKNOWN, kimi-k3 UNKNOWN. Self-ID is weak evidence even when it fires; here it never fired. The pass still banks a real ledger fact: the cheap keyless authenticity test proposed for pro ids does not exist on llm7 as of 2026-09-28. The 401 is deterministic (code missing_api_key, not 429 or timeout), so retrying keyless is waste. Fleet adoption: (1) per-id authenticity law stands unchanged, pro ids (gpt-6-astra, claude-opus-5-5, grok-4.6, kimi-k3) stay owed until keyed A/B; no keyless proxy, self-ID or otherwise, is admissible for the pro tier; (2) freelane burn rotation stays on the keyless-verified set (GLM-5.3-Flash, codestral-latest) per 20260927_g; (3) the anonymous lane remains burst-only under the concurrency wall; (4) catalog availability 100 plus keyless 401 means availability fields describe the paid path only, so freelane scans must filter on usage_based_only, never on availability. The aile.sh price and status mismatch is logged as churn evidence, not truth.

## Bibliography

- watch/inbox/BURN_free-resource-landscape_20260927_g.md (read 2026-09-28, the per-id authenticity law)
- watch/inbox/LINKS.jsonl (tail -30, read 2026-09-28)
- https://api.llm7.io/v1/models (GET x3, 2026-09-28, HTTP 200)
- https://api.llm7.io/v1/chat/completions (keyless POST x4, 2026-09-28, HTTP 401 x4, bodies quoted)
- WebSearch 2026-09-28, query "gpt-6-astra" llm7: aile.sh snippet (not opened)
