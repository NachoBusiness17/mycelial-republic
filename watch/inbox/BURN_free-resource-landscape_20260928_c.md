# BURN free-resource-landscape 2026-09-28 c

## Verdict

steal

## Evidence

- Churn series interval 2 (2026-09-28 05:02 UTC): `GET https://api.llm7.io/v1/models` returned `HTTP 200`, `{"object":"list","data":[...]}` with 64 total models. Free-class filter (usage_based_only false or absent) yields exactly 4: GLM-5.3-Flash, codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407. usage_based_only=true count: 60. Interval 1 was 4 to 4 over the same id set, so the series now reads 4 to 4 to 4: zero drift across two intervals, id set byte-stable.
- Keyless usability probe (one shot, no key material): `POST https://api.llm7.io/v1/chat/completions` with model GLM-5.3-Flash, max_tokens 5 returned `HTTP 200` with content present: `"finish_reason":"length"` and `"content":"alive\n\n**<br>**\n\n*Note: The format"`. Probe observed the 5-token cap was not enforced on this response (usage shows 64 completion tokens, 19 prompt); API usable keyless regardless.
- DeepSeek time math: `date -u` = Mon Sep 28 05:02:25 UTC 2026. Off-peak canon window 16:30-00:30 UTC: 05:02 sits 4h32m past close (00:30) and 11h28m before next open (16:30). Window CLOSED at check time. Liveness probe `GET https://api.deepseek.com/models` unauthenticated returned `HTTP 401` with body "Authentication Fails (governor)": alive per canon (401 = alive).
- Web search "LLM7 free model changes api.llm7.io 2026": thin. No announcements of a specific model deprecation event on api.llm7.io in 2026 surfaced; secondary guides (aismartcore.com, 2026-09-14; freecodingmodels.vercel.app) document only an anonymous-access restriction plus token.llm7.io tier system and free-tier rate limits near 40 RPM / 2,400 RPD. Secondary, unverified here: owed if relied on.

## Steal or Vacuous

Steal, hammerable now. The LLM7 freelane is the live target: churn series holds zero drift two intervals and the keyless probe returned 200 with content, so the 4-id free set (GLM-5.3-Flash, codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407) is confirmed grindable at this hour. DeepSeek is alive but its off-peak window is closed; the re-check fires in-window (after 16:30 UTC today) before any hammering there. Board state unchanged otherwise: OpenRouter funded, Groq cached-token RPDs, Featherless recon, Chutes/SiliconFlow/Scaleway dead, Lightning half-closed. Receipt this file; ledger row to follow.

## Bibliography

- https://api.llm7.io/v1/models (fetched 2026-09-28 ~05:02 UTC, HTTP 200)
- https://api.llm7.io/v1/chat/completions (keyless probe, HTTP 200)
- https://api.deepseek.com/models (unauthenticated probe, HTTP 401)
- watch/inbox/LINKS.jsonl (tail -30, read 2026-09-28)
- memory/facts/behavioral.jsonl (tail -30, read 2026-09-28)
- WebSearch summaries: aismartcore.com free-API guide (2026-09-14); freecodingmodels.vercel.app LLM7 setup docs (secondary, unverified)
