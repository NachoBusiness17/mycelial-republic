# FRONTIER DOORS PROBE - 2026-10-04

source-fetched: 2026-10-04

Instrument: WebFetch tool only, one probe per door per the ask. The four doors
are the estate's standing research intake surfaces, named at
`.agents/skills/frontier-mine/SKILL.md:9-10` (arXiv, HN, Reddit, X).

## Scoreboard

| Door | Verdict | Attempts |
|---|---|---|
| arXiv export API | ANSWERED (valid Atom XML) | 2 (first timed out at 60s, retry answered) |
| hn.algolia.com | ANSWERED (valid JSON) | 2 (first timed out at 60s, retry answered) |
| old.reddit.com/r/LocalLLaMA/top.json | NOT ANSWERED (HTML shell, not JSON) | 2 (first timed out at 60s, retry returned block shell) |
| api.fxtwitter.com | ANSWERED (valid JSON) | 1 (first try) |

## Working recipes (exact, as they answered today)

### arXiv export API - WORKS

```
https://export.arxiv.org/api/query?search_query=all:transformer&max_results=2
```

Answered: valid Atom XML, feed title `arXiv Query:
search_query=all:transformer&id_list=&start=0&max_results=2` (180,644 total
results), entries carry id/title/published (e.g. `2201.00978v1`,
"PyramidTNT: Improved Transformer-in-Transformer Baselines with Pyramid
Architecture", published 2022-01-04T04:56:57Z). Note the echo in the feed
title shows no `sortBy` param: the recipe that ANSWERED is the minimal one
above. A richer first attempt carrying
`sortBy=submittedDate&sortOrder=descending` timed out at 60s, so a
date-sorted recipe is UNPROVEN today, not proven broken. OWED: re-probe the
sortBy variant before relying on recency ordering.

### hn.algolia.com - WORKS

```
https://hn.algolia.com/api/v1/search?query=local%20llama&tags=story&hitsPerPage=2
```

Answered: valid JSON, `"query": "local llama"`, `nbHits: 1094`, hits carry
`objectID`/`title`/`points`/`created_at` (e.g. objectID `42463686`, "GPTScript
working with function calling on local Llama3.3:70B", 3 points,
2024-12-19T17:27:08Z). No auth, no UA games. This is the turnkey HN door.

### old.reddit.com/r/LocalLLaMA/top.json - DOES NOT ANSWER via WebFetch today

```
https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=2
```

Answered with a web page shell ("Welcome to Reddit", "Skip to main content"
accessibility link), zero JSON fields. Consistent with Reddit serving an HTML
shell to the WebFetch client, but the cause (UA block vs other) is NOT
verified: no recipe was established by this probe. OWED: a working Reddit
fetch recipe (candidate levers: different UA via curl, or a mirror) before
the Reddit leg of the mine can run from this seat.

### api.fxtwitter.com - WORKS

```
https://api.fxtwitter.com/elonmusk/status/1585841080431321088
```

Answered first try: valid JSON, HTTP 200 in the payload, `screen_name:
"elonmusk"`, id `1585841080431321088`, text `"the bird is freed"`,
`created_at: "Fri Oct 28 03:49:11 +0000 2022"`. Recipe shape:
`https://api.fxtwitter.com/<screen_name>/status/<id>`. The chosen post is a
canonical public post; its reality was verified by the fetch response itself,
not assumed. (An estate-held post id was preferred but not available in time:
two `grep -rEoh` sweeps over `watch/inbox memory corpus` and
`watch/inbox memory catalog` for `/(twitter\.com|x\.com)/<user>/status/<id>`
patterns were cut for runtime before returning any rows, so no estate-held id
is claimed here.)

## Notes for the sweep

- WebFetch tool timeout is 60s: arXiv and HN each burned one attempt on a
  timeout and answered on retry. Budget two attempts per door before calling
  a door dead.
- Doors answered today: arXiv, HN Algolia, fxtwitter. Door dark today:
  old.reddit.com top.json via WebFetch.
