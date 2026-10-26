# B2-454 receipt: cache-rate byte audit (2026-09-26)

## Verdict

BLOCKED AT SOURCE, filed as the audit's real finding: the zcode logs CANNOT reproduce a cache hit rate for any day, because every token field on every logged network event is redacted at source. On zcode-2026-09-26.jsonl (233,193,509 bytes, 264,059 lines) there are 15,724 "cacheReadTokens" fields and every single one carries the string "[Redacted]"; the numeric-form grep (digits) returns zero hits, and 2026-09-25 is the same. The brief's premise ("cached vs fresh input token fields on completed network events") fails on bytes: the fields exist, the values do not. Consequences, stated exactly: (1) no divergence between log-derived rate and the operator panel's 97.3 pct can be computed, so the correction arm against DOGFLOOD_METERS_20260926.md is not triggered; (2) the falsifier's blocking arm is CONFIRMED - no full day of logged traffic reproduces a rate in the 90s pct band, and none ever will from these logs; (3) the 97.3 pct reading stands exactly as DOGFLOOD_METERS already frames it: operator-reported, witness-corroborated by pin lines (BURN_WAVE_PIN_20260926.md, ASTRA_PROMPT_WORLDLINE_WITNESS3_20260907.md), never byte-measured. One sharpening this audit adds: DOGFLOOD's "corroborated on repo bytes" phrase overstates - the corroboration is textual (a pin sentence repeated across two files), not computational.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md:5: "average cache hit rate 97.3 pct" (operator reading 1) and :5: "The panel percentages themselves have no in-repo measurement surface and are recorded here as operator-reported readings, marked as such, never as byte measurements."
- DOGFLOOD_METERS_20260926.md:11: "97.3 pct cache rate corroboration on bytes: watch/inbox/BURN_WAVE_PIN_20260926.md line 'width 10 clean, 109M tok/h measured, 97.3pct cache hit rate'" (the corroboration this audit shows is a witness LINE, not a computation).
- Log probe (this lane, C:\Users\foste\.zcode\cli\log\zcode-2026-09-26.jsonl): usage rows carry context.usage {inputTokens, cacheReadTokens, cacheWriteTokens, outputTokens, reasoningTokens, totalTokens} on completed network events (event/module/level/durationMs/status context shape, providerId/modelId present); value census: '"cacheReadTokens":"[Redacted"]' x 15,724 via uniq -c; numeric grep '"cacheReadTokens": ?"?[0-9]{2,}"?' -> 0 hits; 2026-09-25 same result.
- Sample row shape (this lane): top keys timestamp/event/module/level/turnId/sessionId/traceId/durationMs/status/context; context keys attempt/baseURL/modelId/providerId/finishReason/usage/... (the meter surface exists; its values are stripped).

## Work done

1. Located the meter surface the brief believed in: .zcode/cli/log/zcode-YYYY-MM-DD.jsonl, one file per day, completed network events with the full usage block - structurally exactly what the audit needs.
2. Ran the value census across the full 2026-09-26 log (233MB) and spot-verified 2026-09-25: 100 percent of token values are the literal "[Redacted]" string; zero numeric values on either day; therefore no daily cache rate is computable from in-repo bytes (the harness strips token counts before they hit disk).
3. Reconciled with DOGFLOOD_METERS_20260926.md: that receipt already refuses to claim byte-measurement for the panel percentages, so no correction is filed against its cost-engine paragraph; the one wording sharpening (its "corroborated on repo bytes" is a textual-witness corroboration) is recorded here rather than edited into the sealed receipt.
4. Named what a real byte surface requires, for the lane that wants this meter standing: an unredacted usage-event export (harness-side meter or a debug flag that writes numeric usage), one full UTC day, rate = cacheReadTokens / (cacheReadTokens + fresh inputTokens) per completed event, aggregated by model. Until that exists, the audit is structurally impossible in-repo.

## Falsifier

The brief's falsifier ("no full day of logged traffic reproduces a rate in the 90s pct band") is CONFIRMED in its blocking arm: no logged day reproduces any rate at all, 90s or otherwise. This audit dies if: (a) any zcode log day appears with numeric token fields (rerun the value census: a single numeric hit reopens the audit and that day becomes computable); (b) a redaction bypass surface lands (a meter flag or export path writing numeric usage) - then the one-full-UTC-day computation proceeds per Work done item 4; (c) someone cites DOGFLOOD's 97.3 as byte-measured after this receipt (the wording sharpening above is the standing correction).

## Bibliography closed

All read this lane: watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md (readings, corroboration line, cost-engine paragraph), watch/inbox/BURN_WAVE_PIN_20260926.md (pin line, via DOGFLOOD quote), C:\Users\foste\.zcode\cli\log\zcode-2026-09-26.jsonl and zcode-2026-09-25.jsonl (structure + value census), watch/inbox/ASTRA_PROMPT_WORLDLINE_WITNESS3_20260907.md (second 97.3 witness, via DOGFLOOD), QUEUE.md B2-454 row.
