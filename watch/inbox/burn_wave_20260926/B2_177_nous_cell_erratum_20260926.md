# B2-177 receipt: PROVIDER_HEALTH nous cell erratum (2026-09-26)

## Verdict

LANDED. The one-cell erratum is in: the nous scoreboard row no longer claims "no rate headers exposed"; it now cites the measured x-ratelimit set (50 req/min, 2100 req/h, 500k tok/min, 6M tok/h) with the probe file as its anchor, and keeps the 0 x 429 across 7 calls sub-claim untouched. The verdict cell (YES 3/3) and the token cell (822) are unchanged; no other cell in the row moved.

## Evidence file:line quotes

- watch/inbox/PROVIDER_HEALTH_20260926.md:17 (pre-edit): "| nous (Hermes k1) | inference-api.nousresearch.com/v1 | stealth/space-bunny-alpha | YES 3/3 | no rate headers exposed; 0 x 429 across 7 calls | 822 |".
- watch/inbox/burn_wave_20260926/B2_04_probe_results.json rl block (the lines the brief cites, 608-623): "\"x-ratelimit-limit-requests\": \"50\"", "\"x-ratelimit-limit-requests-1h\": \"2100\"", "\"x-ratelimit-limit-tokens\": \"500000\"", "\"x-ratelimit-limit-tokens-1h\": \"6000000\"", plus remaining/reset siblings and the fairshare ratelimit-policy headers (re-read this lane before the edit).
- watch/inbox/PROVIDER_HEALTH_20260926.md:17 (post-edit): "| nous (Hermes k1) | inference-api.nousresearch.com/v1 | stealth/space-bunny-alpha | YES 3/3 | full x-ratelimit set exposed (50 req/min, 2100 req/h, 500k tok/min, 6M tok/h; B2_04_probe_results.json rl block); 0 x 429 across 7 calls | 822 |".

## Work done

1. Re-read the probe rl block from B2_04_probe_results.json and confirmed every header value quoted in the new cell (limits only; no remaining/reset values moved into the scoreboard, the cell names the probe file for the full set).
2. Applied the one-cell fix on freshly-read bytes; the 0 x 429 sub-claim, verdict, model, base URL and token total are byte-identical to the pre-edit row.

## Falsifier

The erratum dies if: (a) a fresh nous probe shows the 0 x 429 sub-claim false (a 429 within the window the row covers), or (b) the cited rl block disappears from B2_04_probe_results.json (the anchor must resolve), or (c) the header set changes materially on a future probe (new limits) without a dated refresh of this cell, re-creating the stale-cell disease in the opposite direction.

## Bibliography closed

All read this lane: watch/inbox/PROVIDER_HEALTH_20260926.md (line 17 row, pre + post), watch/inbox/burn_wave_20260926/B2_04_probe_results.json (nous rl block 605-625), QUEUE.md B2-177 row.
