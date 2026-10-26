# B2-37 close receipt: provider health receipt verify (2026-09-26)

## Verdict

CLOSED, NO REBUILD. watch/inbox/PROVIDER_HEALTH_20260926.md exists (6,140 bytes,
Sep 26 07:38, landed by B2-04) and its scoreboard matches the raw probe bytes
claim by claim: every status code, model id, rate-limit header, per-lane token
count, and quoted response in the table reproduces from B2_04_probe_results.json
and B2_04_probe_results2.json. Three carve-outs found and named in Evidence: one
wrong scoreboard cell (nous headers), two figures that trace to the probe
session console instead of persisted JSON. Receipt stands; errata filed to the
queue as B2-127..B2-129.

## Evidence

- Totals re-added by hand from usage blocks: groq 489 (165+154+170), nous 822,
  together 540, cohere 180, openrouter k1 801 + k2 808, zai-pro 1801 incl alive
  137, zai-lite 1449 incl alive 167; grand total 6,890 = the md's "6,586 tokens
  on the estate prompts, plus 304 on alive pings (z_ai lanes)"
  (PROVIDER_HEALTH_20260926.md:35-36). Match.
- Dead lanes byte-verified: cerebras 402 x3 after a 2-model 200 catalog
  (B2_04_probe_results.json:160-204); nvidia 410 x3 plus the 404 body
  "Function '23bd454d-b225-49a3-8118-582a62fc51b8': Not found for account"
  (results.json:230-265; B2_04_probe_results2.json:52-63); gemini 61-model 200
  then 401 "API keys are not supported by this API" (results.json:278-313;
  results2.json:64-74); mistral 429 x3 with "x-ratelimit-limit-req-minute": "0"
  (results.json:949-993). All match the md table.
- Quotes verified: groq 1776 hallucination (results.json:96), cohere count "13"
  (results.json:916), zai-pro go classify 600 completion tokens reasoning-only
  (results2.json:200-208), zai-lite count 429 code 1305 body
  (results2.json:266-274), ollama 16 models / saelis refused / no-key rows /
  zai-main skip (results.json:1-10, 1000-1028). All match.
- ERRATUM 1: md:17 says nous "no rate headers exposed" but results.json:608-623
  records the full nous x-ratelimit set (limit-requests 50, limit-tokens 500000,
  1h 2100/6000000). The cell is wrong; headers were exposed and are the actual
  measured denominator. "0 x 429 across 7 calls" in the same cell does check
  out (1 models + 3 alive + 3 burn, zero 429).
- ERRATUM 2: the openrouter /key dollars $4.608 and $0.7377 (md:15-16) exist in
  no JSON. probe2.py:186-187 fetches /key but report() (probe2.py:96-99)
  persists only choices content, which is empty for /key. Console-only figures.
- ERRATUM 3: gemini "401 as Bearer (invalid authentication credentials)"
  (md:24) is in no JSON; probe2.py scripts only the API-key-mode native diag.
  Console-only quote.

## Work done

1. Read PROVIDER_HEALTH_20260926.md whole (59 lines) and both probe JSONs whole
   (17 lane records).
2. Read B2_04_probe.py whole (348 lines) and the probe2.py capture paths;
   confirmed all prompts are synthetic public-domain (probe.py:21-35), groq
   ran reasoning_effort low (probe.py:220), and the dead :free chain ids
   (probe.py:261), matching md:56.
3. Hand-recomputed all 8 lane token sums and the 6,890 total from usage blocks.
4. Filed this receipt, LEDGER row 85 via .venv python json.dumps, and 3
   self-feed briefs (B2-127..129). No rebuild: the receipt exists and every
   load-bearing claim holds.

## Falsifier

This close dies if: (a) the /key dollar figures or the gemini Bearer 401 turn
up in a persisted artifact I did not check (I read both JSONs whole and both
probe scripts' capture paths); (b) any hand sum above mismatches its JSON usage
blocks; (c) a later edit moves the md:17 nous cell so the erratum target no
longer exists without a pointer update in B2-127.

## Bibliography closed

- watch/inbox/PROVIDER_HEALTH_20260926.md (the receipt under verify)
- watch/inbox/burn_wave_20260926/B2_04_probe_results.json
- watch/inbox/burn_wave_20260926/B2_04_probe_results2.json
- watch/inbox/burn_wave_20260926/B2_04_probe.py
- watch/inbox/burn_wave_20260926/B2_04_probe2.py
- watch/inbox/burn_wave_20260926/B2_04_provider_health_20260926.md (B2-04 lane receipt)
- watch/inbox/burn_wave_20260926/QUEUE.md (B2-127..129 appended)
- memory/burns/LEDGER.jsonl (row 85 appended)
