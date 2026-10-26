# B2-25 ENVELOPE RE-MEASURE 20260926

## Verdict

The width-10 rung is now measured clean from this burn's own lane data. Wave 1 ran 10 Task agents concurrently, 10/10 completed, zero 1302 in any of the session's 25 agent output files, banking 37,386,533 witnessed tokens in 1229.9 s (20.50 min): 109.4M tok/h at width 10. Wave 2, also width 10, fired 176.9 s after wave 1's last completion: 8/10 completed at measure time (22,795,253 tokens, partial 85.6M tok/h, window open-ended), 2 still running, zero 1302. Three back-to-back waves in 37 min never tripped the post-burst penalty the afterparty saw at 12. The recorded envelope law holds; the clean ladder now reads 3-6-10-12; the 15-16 ceiling rung is untested today and stands unchanged; one blind spot (silent retry absorption) is named and fed.

## Evidence

Wave 1, all lanes created 11:24:57Z, all completed. Source: per-agent metadata.json totalDurationMs/totalTokens/totalToolUseCount, e.g. agent_ac61e087.../metadata.json:29-31.

| lane | dur s | tokens | tools |
|---|---|---|---|
| B2-01 | 1229.9 | 8767163 | 108 |
| B2-02 | 987.4 | 3748742 | 43 |
| B2-03 | 842.4 | 3444078 | 49 |
| B2-04 | 1004.8 | 2106734 | 25 |
| B2-05 | 1052.5 | 4166730 | 63 |
| B2-06 | 610.1 | 1950043 | 35 |
| B2-07 | 997.4 | 4426642 | 64 |
| B2-08 | 692.3 | 2124709 | 38 |
| B2-09 | 1001.0 | 3849129 | 72 |
| B2-10 | 641.3 | 2802563 | 43 |
| mean | 905.9 | 3738653 | 54.0 |

Token max 8,767,163 (B2-01), min 1,950,043 (B2-06). Duration max 1229.9 s, min 610.1 s. Window 11:24:57.106Z to 11:45:27.043Z = 0.34165 h. Throughput 37,386,533 / 0.34165 = 109.4M tok/h. Wave 2 (B2-11..B2-20, 8/10 done): token mean 2,849,407, max 4,560,367 (B2-11); dur mean 606 s, max 958 s.

1302/429 scan: `grep -c 1302 agent_*/output.txt agent_*/task.output` returns 0 files with hits. The only 429s are provider probes inside lanes: B2_04_provider_health_20260926.md:10 "429 with x-ratelimit-limit-req-minute: 0" (mistral), :21 "429 code 1305 ... on ~1 in 3" (z_ai); B2_15_xintel_dig_20260926.md:27 "one search fell back to model text on a 429".

Recorded envelope: AFTERPARTY_CLOSE_20260926.md:8-9 "Envelope law measured, not guessed: Task agents clean at 3/6/12; ceiling between 12 and 16; after a burst even 12 gets 1302s until the window decays." LEDGER.jsonl:46 (afterparty-94-lane-churn): "1302 ceiling found at width 15-16 then 12-post-burst: limit is rolling throughput, not width-only". Today's width-10 data sits inside that law and strengthens the clean rungs.

## Work done

Pulled 25 metadata.json from sess_fd5ec147-a47d-41ee-91f4-afd899b524ca; classified three waves by createdAt clusters (11:24:57Z width 10, 11:48:23Z width 10, 12:01:06Z width 5); computed sums, means, maxima per wave with .venv/Scripts/python.exe; grepped 1302/429 across all outputs; read today's rows of the 64-row LEDGER and both gala receipts; appended a dated amendment block to watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md (append only, originals untouched); appended LEDGER row; fed B2-97..99 to QUEUE.md.

## Falsifier

1. "Zero 1302 recorded" means zero surfaced: the main-session retry path absorbs errors silently (TETHERED_LINK_STEAL_20260925.md:17 "main-session requests get `maxAttempts 11`"), so a 1302 retried to success leaves no lane-visible trace. A per-agent provider-error counter in metadata.json would close this; until then lane bytes cannot prove zero occurred.
2. The 15-16 ceiling is untouched by today's data; a clean width-15 Task wave would amend the ladder, a 1302 there would confirm it.
3. Wave-2 numbers are partial (B2-12, B2-13 running); final totals may shift means, not the 1302 count.

## Bibliography closed

Read: watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md (whole); watch/inbox/GALA_20260925.md (whole); corpus/steal/TETHERED_LINK_STEAL_20260925.md; memory/burns/LEDGER.jsonl (today's rows); watch/inbox/burn_wave_20260926/QUEUE.md; 25 agent metadata.json under C:\Users\foste\.zcode\cli\agents\sess_fd5ec147-a47d-41ee-91f4-afd899b524ca\; B2_04 and B2_15 receipts for 429 provenance. No web sources. Every figure recomputed from metadata bytes this session; nothing synthesized.
