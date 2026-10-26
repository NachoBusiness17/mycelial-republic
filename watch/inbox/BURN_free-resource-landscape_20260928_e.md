# BURN free-resource-landscape 2026-09-28 e (DeepSeek in-window debt fire)

## Verdict

vacuous

## Evidence

- Time math: `date -u` at fire returned `2026-09-28T07:03:52Z`. Canon window 16:30-00:30 UTC (wrap-around): 07:03Z sits 9h26m before the 16:30Z open and 6h34m past the 00:30Z close. Out of window. The board line "in-window now: current UTC is past 16:30" was stale at execution time.
- Liveness probe (out-of-window, attempt 1 of 2, 20s cap): unauthenticated `GET https://api.deepseek.com/models` returned `HTTP=401` in 0.749s, body `Authentication Fails (governor)`. Legend: 401 = alive and gated. No retry needed.
- Key gap check: `grep -i DEEPSEEK .env | cut -d= -f1` names `DEEPSEEK_API_KEY` (plus the comment line and `AOS_AGENT_MODEL` matching the shape). Values never read or printed. Lane is key-armed; the authenticated probe was not run because it needs a driver file (owed, not built in this fire).
- Window-definition search "DeepSeek off peak discount window UTC 2026": thin, third-party only. usagepricing.com summary: "peak hours include 01:00-04:00 and 06:00-10:00 UTC, with off-peak at 50% discount outside those windows", which contradicts the canon 16:30-00:30 shape and would place 07:03Z inside peak. studioglobal.ai summary: peak/off-peak billing began "August 17, 2026 at 00:00 Beijing time (16:00 UTC on Aug 16)". getnadir.com summary: V4.1-Flash "$0.15/$0.60 per million tokens off-peak vs $0.30/$1.20 weekday peak". No official platform.deepseek.com page fetched.

## Steal or Vacuous

Vacuous. The standing in-window debt was NOT discharged: the fire landed outside every candidate window, so no off-peak hammer was fired and none may be claimed. Worse, the window definition moved from canon-asserted to contested: the memory canon says 16:30-00:30 UTC, the only fresh signal (aggregator summaries, unofficial) says off-peak is everything outside 01:00-04:00 and 06:00-10:00 UTC. The two shapes are materially different hammer plans and neither is verified against an official source. What the pass did bank: the DeepSeek freelane is alive and gated (401, not open, not down) and the lane is key-armed (`DEEPSEEK_API_KEY` present by name). Ledger row: liveness receipt stands, in-window probe stays owed, window definition stays owed against platform.deepseek.com before the next hammer.

## Bibliography

- `watch/inbox/LINKS.jsonl` (tail -30, read 2026-09-28; no DeepSeek window rows)
- `memory/facts/behavioral.jsonl` (tail -30, read 2026-09-28; percolator invariants only)
- repo `.env`, key names only via `cut -d= -f1`
- `date -u` (2026-09-28T07:03:52Z)
- https://api.deepseek.com/models (HTTP 401 observed, unauthenticated, 2026-09-28T07:04Z)
- WebSearch "DeepSeek off peak discount window UTC 2026", summaries of [usagepricing.com](https://usagepricing.com), [studioglobal.ai](https://studioglobal.ai), [aicreditsapi.com](https://aicreditsapi.com), [getnadir.com](https://getnadir.com) (search summaries only, pages not fetched, unofficial)
