# BURN: free-resource-landscape 2026-09-28

## Verdict

steal

## Evidence

- Owed one-liner landed (from the world-models trace): the Agora-2 technical report URL is https://agora-2.odyssey.systems/agora-2.pdf, shown three times on https://odyssey.systems/introducing-agora-2 (fetched 2026-09-28), which states the report "describes the architecture, training, and serving system in more detail." HEAD verify 2026-09-28 03:04 GMT: HTTP/1.1 200 OK, Content-Type: application/pdf, Content-Length: 7408464. The trace's owed row ("link not extractable, guessed path 404'd") closes.
- OpenRouter denominators, byte-backed: GET https://openrouter.ai/api/v1/models returned 458 data rows; all 458 carry per-model pricing.prompt and pricing.completion (sample pricing keys exactly ["completion","prompt"]); 21 rows sit at prompt=0 and completion=0. 458 matches the SCOUT-QUIET-2 baseline "openrouter 458 ... stable" (watch/inbox/LINKS.jsonl, 2026-09-22).
- LLM7 churn re-check, byte-backed: GET https://api.llm7.io/v1/models returned 64 total; usage_based_only false on exactly 4: GLM-5.3-Flash, codestral-latest, minimax-m2.7, mistral-Nemo-Instruct-2407; turbo tier 5. Identical to pass k (2026-09-27).
- Web search thin, stated honestly: no 2026 page on OpenRouter free-list restructuring surfaced; a search summary cited docs/limits as "traditionally 20 requests/min and 50 requests/day free, or 1,000/day with $10+ in credit purchases" but the page was not fetched.

## Steal or Vacuous

Steal on three fronts. (1) Ledger debt paid: the world-models trace owed one line and it now has a live, sized, typed target (7.4 MB PDF); canon gains a resolvable source instead of a guessed 404. (2) OpenRouter funded-lane denominators are current-shaped: the recon surface (models endpoint) carries per-model prompt/completion pricing on 100 pct of rows, and the 458 total is byte-identical to the 09-22 baseline, so the lane's denominator claim holds at endpoint-shape strength; the rpd number itself remains un-fetched docs text, filed owed, not fabricated. (3) The LLM7 churn series now has its first interval: 5 (2026-09-26 pre-drift) then 4 (2026-09-27) then 4 (2026-09-28), one measured interval at 0 ids/day drift with sample size 2; the freelane roster is unchanged and the same 4 keyless ids stay hammerable, re-pull before each wave remains the law. Staleness note: this pass refreshed the hot rows (OpenRouter, LLM7) by byte census; the dead rows (Chutes, SiliconFlow, Scaleway) and the Featherless recon were not re-checked today, so their staleness clocks are untouched by this receipt.

## Bibliography

- https://api.llm7.io/v1/models (fetched 2026-09-28, HTTP 200, byte-backed)
- https://openrouter.ai/api/v1/models (fetched 2026-09-28, byte-backed)
- https://odyssey.systems/introducing-agora-2 (fetched 2026-09-28)
- https://agora-2.odyssey.systems/agora-2.pdf (HEAD 2026-09-28, HTTP 200, application/pdf)
- watch/inbox/BURN_world-models-multi-agent_20260925.md (read 2026-09-28)
- watch/inbox/BURN_free-resource-landscape_20260927_k.md (read 2026-09-28)
- watch/inbox/LINKS.jsonl (tail -30, read 2026-09-28)
- memory/facts/behavioral.jsonl (tail -30, read 2026-09-28)
- WebSearch 2026-09-28, summaries only, no page fetched
