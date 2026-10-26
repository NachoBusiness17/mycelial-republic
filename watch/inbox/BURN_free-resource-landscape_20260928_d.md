# BURN free-resource-landscape 20260928_d: DeepSeek in-window retry (skipped, window closed) + LLM7 cap table completed

## Verdict

steal

## Evidence

- DeepSeek time math: `date -u` = 2026-09-28 06:02:27 UTC. Off-peak window 16:30-00:30 UTC: 06:02 sits 5h32m past close (00:30) and 10h28m before next open (16:30). Window CLOSED. Curl skipped per canon, no liveness claim this pass. Second consecutive out-of-window fire (receipt c landed 05:02 UTC, also outside): the in-window DeepSeek check is now a standing debt, first firable after 16:30 UTC today.
- LLM7 census (attempt 1): `GET https://api.llm7.io/v1/models` HTTP 200, 64 total models, `usage_based_only` false on exactly 4, all tier turbo: GLM-5.3-Flash, codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407. Third interval, zero drift, id set byte-stable (intervals 09-27 k, 09-28 c, this pass).
- codestral-latest probe (attempt 2, keyless, max_tokens 5, "reply ok"): HTTP 200, `"finish_reason":"length"`, `"content":"OK! 😊"`, usage 5 prompt / 5 completion / 10 total tokens, service_tier "standard". Cap ENFORCED, first sample on this id.
- mistral-Nemo-Instruct-2407 probe (attempt 3): HTTP 200, `"finish_reason":"length"`, `"content":"Understood. I'll"`, usage 6 prompt / 5 completion tokens, service_tier "default", estimated_cost 2.64e-07. Cap ENFORCED, second consistent sample (receipt k: 5 completion tokens).
- Board correction from byte truth: the pass brief carried "GLM-5.3-Flash enforced", but receipt c (2026-09-28 05:02 UTC) records GLM-5.3-Flash at 64 completion tokens on a 5-token ask. GLM is a violator, not an enforcer. Attempts used: 3 of 4.
- Web search "llm7 max tokens ignored" (2026): thin, stated honestly. No llm7-specific report surfaced; results were generic max_tokens issues on other providers (OpenAI community, Azure docs, SiliconFlow docs) plus an OmniRoute gateway listing llm7.io. No page opened, nothing contradicts the byte-backed probes.

## Steal or Vacuous

Steal: the LLM7 freelane cap-enforcement table is complete, four ids, byte-backed. ENFORCED (hard-stop reliable, safe for tight token budgets): codestral-latest, mistral-Nemo-Instruct-2407. VIOLATED (spill-prone, budget roughly 13x headroom on a 5-token ask): minimax-m2.7 (receipt k, 64 completion tokens) and GLM-5.3-Flash (receipt c, 64 completion tokens). Churn series holds at zero drift across three intervals; re-pull /v1/models before each wave stays the law. Window verdict: DeepSeek off-peak closed at check time and this is the second consecutive miss, so the freelane hammering target today remains LLM7 only; the DeepSeek in-window liveness probe (401 = alive) is owed after 16:30 UTC today and lands in the next fire. Receipts over board summaries: this pass also corrects the cap table canon on GLM.

## Bibliography

- https://api.llm7.io/v1/models (GET 2026-09-28 ~06:02 UTC, HTTP 200, byte-backed)
- https://api.llm7.io/v1/chat/completions (keyless POST x2 2026-09-28, HTTP 200 x2, byte-backed)
- watch/inbox/BURN_free-resource-landscape_20260928_c.md (read 2026-09-28, GLM 64-token evidence)
- watch/inbox/BURN_free-resource-landscape_20260928.md, _b.md (read 2026-09-28)
- watch/inbox/BURN_free-resource-landscape_20260927_k.md (read 2026-09-28, minimax + Nemo pass-k probes)
- watch/inbox/LINKS.jsonl (tail -30, read 2026-09-28)
- memory/facts/behavioral.jsonl (tail -30, read 2026-09-28)
- WebSearch 2026-09-28, query "llm7 max tokens ignored OR not enforced max_tokens 2026": summaries only, thin
