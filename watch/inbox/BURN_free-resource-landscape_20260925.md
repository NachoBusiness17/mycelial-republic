# BURN receipt: free-resource-landscape (2026-09-25)

## Verdict
steal

## Evidence
1. Groq rate-limits docs (console.groq.com/docs/rate-limits, fetched 2026-09-25), free-plan table: "openai/gpt-oss-120b | 30 | 1K | 8K | 200K", identical quota rows for "openai/gpt-oss-20b" and "qwen/qwen3.8-27b". Llama survives on the free plan only as classifiers: "meta-llama/llama-prompt-guard-2-22m | 30 | 14.4K | 15K | 500K". Doc notes: "Cached tokens do not count towards your rate limits" and limits "apply at the organization level, not individual users."
2. LINKS.jsonl scout row 2026-09-18: "Groq free tier stable this week (30 req/min, up to 14,400 req/day, Llama 3.x/4 + Whisper)". That 14.4K RPD figure is now wrong for every text model: the live docs show 1K RPD. The 09-21 and 09-22 churn rows tracked model counts ("13 -> 11 models") but never filed the RPD cut.
3. LINKS.jsonl standing items confirmed still open: "cerebras+nvidia baselines still 0 = key gap + purge persist"; "Cerebras free tier now REQUIRES A CARD (klymentiev.com Sep 11 roundup)"; "NVIDIA build API purged 82 models"; "Qwen3.6-27B VERIFIED INSTALLABLE".
4. Two fresh search hits rendered empty: apishare.cc (leaderboard "marked 'Loading...' and never appear"; title promises "Best Free LLM APIs 2026: Groq, Gemini, Mistral, Cloudflare & More" with no body) and autonix-lab.online (marketing homepage, no tier data). Filed as owed, not synthesized.

## Steal or Vacuous
Steal, three adoptions:
1. Correct the ledger's Groq free-budget denominator: text-model free plan is 1K requests/day and 200K tokens/day, not 14.4K requests/day. Wave math built on the old figure overdraws the lane by roughly 14x. Fleet groq lanes (gpt-oss-120b, gpt-oss-20b, qwen3.8-27b) are all still live at 30 RPM / 1K RPD / 8K TPM / 200K TPD; zero lane action needed.
2. Stealth window: Groq prompt caching. "Cached tokens do not count towards your rate limits" plus org-level limits means the deliberate-ask frozen-prefix signature rides free: hammer the same frozen system prefix and the TPM wall largely stops mattering. Register the caching behavior in chat_provider lane notes as the cheap way to stretch the 8K TPM floor.
3. Standing gaps unchanged and restated: Cerebras key needs a card (operator decision still unmade), NVIDIA post-purge re-probe still owed, Qwen3.6-27B remains the verified local judgment upgrade. No new free lane appeared this week; OpenRouter expanding while Groq contracts remains the landscape shape.

## Falsifier
none proposed

## Bibliography
- watch/inbox/LINKS.jsonl (repo scout rows, 2026-09-16 through 2026-09-22, incl. ALERT-NVIDIA-PURGE, ALERT-GROQ-FREE-CHANGES, ALERT-CEREBRAS-CARD, SCOUT-GROQ-CONTRACT)
- https://console.groq.com/docs/rate-limits (fetched 2026-09-25)
- https://apishare.cc (rendered empty, owed)
- https://autonix-lab.online (rendered empty, owed)
