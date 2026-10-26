## Verdict

green

## Evidence

- LLM7 (GET https://api.llm7.io/v1/models, keyless, 2026-09-28, HTTP 200, 63,729 bytes): 64 total models, usage_based_only false on exactly 3: "codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407", all tier "turbo". Board said 4 free ids; GLM-5.3-Flash is ABSENT from today's roster (only glm-5.2 and glm-5.3 remain, both usage_based_only true, tier "pro"). First churn after four zero-drift intervals: free set 4 to 3.
- DeepSeek (GET https://api.deepseek.com/models, unauthenticated, 2026-09-28): HTTP 401, body "Authentication Fails (governor)". Board 401-alive: MATCH.
- OpenRouter (GET https://openrouter.ai/api/v1/models, keyless, 2026-09-28, valid JSON envelope parsed, 754,557 bytes): 460 models. Board 458: +2 drift, row holds.
- Featherless (GET https://api.featherless.ai/v1/models, no params, keyless, 2026-09-28, HTTP 200, 7,075,320 bytes, envelope key "data"): 22,059 rows. Receipt j baseline 22,054 same instrument: +5, alive, full-dump instrument intact.
- Web search "free LLM API tier closing" 2026, snippets only, pages not opened: ianlpaterson.com notes "on May 31, 2026, one LLM provider quietly deleted most of its free tier"; wotai.co claims "~110 free models across 16 providers, but only ~57 truly free". Not corroborated against any opened page, filed as tripwire scent, not fact.

## Steal or Vacuous

Board verdict: green, solved until the next churn event, and this pass caught one. The churn the board exists to catch arrived mid-consolidation: GLM-5.3-Flash dropped off the LLM7 roster, breaking the four-interval zero-drift series, and the standing law (re-pull /v1/models before each wave) absorbed it without loss. Freelanes board final state: hot = OpenRouter funded (460 today), Groq cached-token RPDs (not probed this pass, board status unchanged, carried), LLM7 free keyless now 3 turbo ids (codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407; cap table on those ids unchanged: codestral and Nemo ENFORCED, minimax VIOLATED), DeepSeek off-peak armed and inference-proven, 401-alive today. Recon = Featherless roster-diff standardized on the full-dump instrument, 22,059 rows alive. Dead = Chutes/SiliconFlow/Scaleway/Lightning (closed pass m). Standing debts named: DeepSeek in-window authenticated hammer still owed (firable in the 16:30 to 00:30 UTC window); Featherless paged versus full-dump instrument gap (28,542 rows) unreconciled; Groq row rides on prior receipts, no fresh probe today. Topic ruled green: every row either verified today or carried with a named debt; no key material touched; receipts over reports.

## Bibliography

- https://api.llm7.io/v1/models (GET 2026-09-28, HTTP 200, 63,729 bytes, byte-backed)
- https://api.deepseek.com/models (GET 2026-09-28, HTTP 401, byte-backed)
- https://openrouter.ai/api/v1/models (GET 2026-09-28, 754,557 bytes parsed, byte-backed)
- https://api.featherless.ai/v1/models (GET 2026-09-28, HTTP 200, 7,075,320 bytes, byte-backed)
- watch/inbox/BURN_free-resource-landscape_20260928_m.md, _j.md, _g.md, _d.md (read 2026-09-28)
- watch/inbox/BURN_free-resource-landscape_20260927_c.md (read 2026-09-28, Featherless baseline context)
- watch/inbox/LINKS.jsonl (tail -60, read 2026-09-28)
- memory/facts/behavioral.jsonl (tail -60, read 2026-09-28)
- WebSearch 2026-09-28, query "free LLM API tier closing 2026": snippets only, ianlpaterson.com and wotai.co named, pages not opened
