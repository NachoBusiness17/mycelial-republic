# Provenance — 8kun board snapshots, 2026-09-20

Harvest run: 2026-09-20T02:39:46Z .. 2026-09-20T02:44Z UTC (by gapwave board-harvest agent).
Host: https://8kun.top (door served plain `application/json; charset=utf-8`, no Cloudflare
challenge, no auth). Requests used: 4 of 40 cap; >=2s between requests.

| file | URL | fetched (UTC) | HTTP | bytes | rows |
|---|---|---|---|---|---|
| 8kun_qresearch_20260920.json | https://8kun.top/qresearch/catalog.json | 2026-09-20T02:39:46Z | 200 | 1,888,361 | 25 pages / 375 threads |
| 8kun_projectdcomms_20260920.json | https://8kun.top/projectdcomms/catalog.json | 2026-09-20T02:42Z | 200 | 9,609 | 1 page / 4 threads |
| 8kun_boards_20260920.json | https://8kun.top/boards.json | 2026-09-20T02:42Z | 200 | 87,982 | 350 boards |
| 8kun_qresearch_20260920_thread25055950.json | https://8kun.top/qresearch/res/25055950.json | 2026-09-20T02:44Z | 200 | 137,172 | 164 posts |

User-Agent: `gapwave-harvest/1.0 (research snapshot)`. Files are byte-exact server responses
(renamed from raw captures; JSON re-validated after rename). Content is public board metadata
as served; `com`/`sub` fields contain raw user HTML from the source community, retained
unedited for corpus fidelity.

Key freshness facts at capture:
- Freshest catalog OP: general #30593 "Castle Lock Edition", no 25055950, time 2026-09-20T01:20:16Z (116 replies already).
- Freshest individual post (thread witness): no 25056231, time 2026-09-20T02:43:41Z — board live to the minute.
- Board-level (boards.json): qresearch posts_total 25,055,342; ppd 3,172; pph 268 (next-most-active board on the site: 1 pph).
- Caveat: catalog `last_modified` is sparsely populated on this deployment (345/375 threads lack it); use OP `time` for ordering.
