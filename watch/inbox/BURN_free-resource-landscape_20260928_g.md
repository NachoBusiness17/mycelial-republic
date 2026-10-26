## Verdict

steal

## Evidence

- LLM7 churn interval 4 (attempt 1, GET https://api.llm7.io/v1/models, HTTP 200, read 2026-09-28 09:11 UTC): 65 total rows, pricing_mode token 51 / second 10 / image 4, tier pro 60 / turbo 5, usage_based_only true on 61. Free class (usage_based_only false) exactly 4, all tier turbo: "GLM-5.3-Flash", "codestral-latest", "minimax-m2.7", "mistral-Nemo-Instruct-2407". Interval 3 (receipt d): "64 total models, usage_based_only false on exactly 4", same ids. Series 4/4/4/4, zero id drift; total moved 64 to 65 (one paid-class addition). Newest census row "DeepSeek-V4-Flash-0731" carries created 1790579103 = 2026-09-28T07:05:03Z, consistent with being the +1 (attribution probable, not asserted).

- Featherless roster-diff interval 2 (attempt 2, GET https://api.featherless.ai/v1/models?sort=-created_at&per_page=100, HTTP 200, keyless): total 50641, pagination total_items 50641, total_pages 507. First (newest) row "Makanemeka/Qwen2.5-Coder-0.5B-Instruct-Gensyn-Swarm-raging_downy_wallaby" created 1790559007 = 2026-09-28T01:30:07Z: same-day signature holds. 17 rows on the page newer than 2026-09-27T00:00:00Z; page created range 2026-09-15T17:56:24Z to 2026-09-28T01:30:07Z.

- Denominator catch from receipt h (2026-09-27): "paged mode reports total_items 50586 vs 22044 in the default dump". The board's 22,044 baseline is the full-dump instrument; tonight's 50,641 is the paged instrument. Same-instrument diff: 50,586 to 50,641 = +55 rows over roughly one day. Differencing 22,044 against 50,641 would have reported a false roster doubling.

- Web search "Featherless new models this week" (2026): thin, stated honestly. No Featherless-specific this-week list surfaced, only generic trackers (llm-stats.com, evertune.ai, featherless.ai landing page). No page opened, nothing contradicts the byte readings.

## Steal or Vacuous

Steal. Churn series interval 4: zero drift, byte-identical free id set across four intervals (09-27 k, 09-28 c, 09-28 d, this pass); re-pull /v1/models before each wave stays the law. Roster-diff interval 2: the h-pre-registered falsifier is not triggered (17 new rows since 09-27T00:00, newest same-day 09-28T01:30Z, keyless 200 held), so the diff premise survives its first two-night test and Featherless stays on the churn-telemetry freelane path toward the EPNEWS roster-diff ledger lane. Steal within the steal: per census-denominator law (name instrument, moment, and delta before comparing counts), the ledger now records paged total_items as the roster-diff denominator (50,586 to 50,641, +55), with the full-dump 22,044 kept as a separate weekly backstop instrument. Owed: one pass reading the no-params full dump beside the paged call to reconcile the 28,542-row instrument gap (h's gated-or-archived superset hypothesis, still unverified). The DeepSeek in-window authenticated hammer (owed after 16:30 UTC today per receipt d) was out of scope this pass and stays owed.

## Bibliography

- https://api.llm7.io/v1/models (GET 2026-09-28 09:11 UTC, HTTP 200, byte-backed)
- https://api.featherless.ai/v1/models?sort=-created_at&per_page=100 (GET 2026-09-28, HTTP 200 keyless, byte-backed)
- watch/inbox/BURN_free-resource-landscape_20260928_d.md (read 2026-09-28, interval 3 baseline and owed hammer)
- watch/inbox/BURN_free-resource-landscape_20260927_h.md (read 2026-09-28, paged 50586 vs dump 22044, pre-registered falsifier)
- watch/inbox/LINKS.jsonl (tail -30, read 2026-09-28)
- memory/facts/behavioral.jsonl (tail -30, read 2026-09-28)
- WebSearch 2026-09-28, query "Featherless new models this week" (2026): thin, summaries only
