# B2-04 receipt: free-lane live probe + burn (2026-09-26)

## Verdict

STEAL. Eight lane-keys answered live today (groq, openrouter x2, nous, together,
cohere, z_ai Pro, z_ai Lite); 6,890 usage-reported tokens burned on synthetic
estate prompts. Four configured lanes are dead with named causes measured from
live responses, not assumed: cerebras 402 (no credit), nvidia 410/404 (roster
purged for this account), gemini 401 (AQ.* credential cannot generate), mistral
429 with x-ratelimit-limit-req-minute: 0. The two old openrouter :free ids in
providers.yaml are gone from the catalog (458 models, 17 :free, neither old id
present); the free lane today is stealth/space-bunny-alpha on both keys.

## Evidence

- groq denominator from live headers: x-ratelimit-limit-requests 1000,
  x-ratelimit-limit-tokens 8000. Burn 489 tok. One hallucination caught:
  gpt-oss-120b dated the Gettysburg paragraph 1776 while summarizing it.
- openrouter /key endpoint (200): key1 usage $4.608 limit null; key2 usage
  $0.7377 limit null. Stealth burn 801 + 808 tok, both answered all 3 prompts.
- z_ai 1305 lore re-measured: 429 code 1305 "temporarily overloaded" on ~1 in 3
  calls at 6s spacing on Pro, 2 of 5 on Lite; recovered after 15s waits.
  glm-4.7-flash reasoning ate the whole 600-token budget on 2 of 7 burns
  (usage shows completion 600, content empty). Burn Pro 1801, Lite 1449.
- nvidia 404 body names the cause: "Function '23bd454d-...': Not found for
  account 'WHfuoDu5...'". The /models list (82 ids) is a fossil; nothing calls.
- gemini: GET /models 200 (61 models) but generateContent 401 as API key
  ("API keys are not supported by this API") and 401 as Bearer OAuth. Catalog
  readable, inference impossible with what is on file.
- cohere word-count answer was 13; ground truth 14; every other lane said 14.
- All quotes trimmed in watch/inbox/PROVIDER_HEALTH_20260926.md.

## Work done

1. Read configs/providers.yaml; enumerated 20 lanes; resolved keys from .env
   (prefixes only, never printed full secrets).
2. B2_04_probe.py: GET /models + 3 alive calls + 3 synthetic burns per lane,
   latency and rate-limit headers captured. Round 1 verdicts: 4 alive.
3. B2_04_probe2.py + inline round 3: diagnosed every dead status against live
   bodies (nvidia listed-model test, gemini native + Bearer-only retry,
   openrouter catalog-present model, z_ai bigger budget + spacing), then burned
   the same 3 synthetic prompts on lanes that came alive (openrouter x2, z_ai
   x2). Ground-truthable prompts: public-domain paragraph, Go phase classify,
   14-word count. Zero repo contents, zero private material sent.
4. Filed watch/inbox/PROVIDER_HEALTH_20260926.md (per-lane table + verdict
   lines + real quotes) and raw JSON (B2_04_probe_results*.json).
5. Ledger row appended to memory/burns/LEDGER.jsonl via .venv python
   json.dumps. Self-fed 3 briefs to QUEUE.md (B2-26..B2-28).

## Falsifier

This verdict dies if: (a) any quoted response body cannot be reproduced by
rerunning B2_04_probe.py / B2_04_probe2.py against the same .env keys today;
(b) any "dead" verdict shows a 200 with content on one retry with the exact
same model id and auth (cerebras 402, nvidia 410, gemini 401, mistral limit-0
are all single-cause claims); (c) token totals disagree with usage blocks in
B2_04_probe_results*.json; (d) any prompt string in the harness files contains
repo or private material (they are Gettysburg, Go coordinates, and a word count
only, checkable by reading the two .py files).

## Bibliography closed

- configs/providers.yaml (lane roster, endpoint laws, dormant flags)
- watch/inbox/PROBE files: B2_04_probe.py, B2_04_probe2.py,
  B2_04_probe_results.json, B2_04_probe_results2.json (this wave)
- watch/inbox/PROVIDER_HEALTH_20260926.md (deliverable)
- watch/inbox/burn_wave_20260926/QUEUE.md (B2-03 endpoint-news lane, the
  prior pass this probe verifies live)
- memory/burns/LEDGER.jsonl (row appended)
- AGENTS.md fan-out law (z_ai raw-call caution, 1302/1305 notes)
