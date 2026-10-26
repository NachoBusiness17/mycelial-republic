# Frontier doors probe - 2026-10-11 (adhoc)

source-fetched: adhoc
instrument: WebFetch, exactly one probe per door, run 2026-10-11 by lens seat "lens-doors" (this session; every quoted value below is verbatim tool output from these four probes)
ask: "Probe each frontier door once with WebFetch: the arXiv export API, hn.algolia.com, old.reddit.com/r/LocalLLaMA/top.json, and api.fxtwitter.com for one known post."
recipe lineage: URL shapes carried from the 10-10 predecessor at this same path (read in full this session before overwrite: minimal arXiv shape, HN search shape, reddit top.json shape, fxtwitter known-post shape) and before that from `watch/inbox/frontier_olm_2026-10-08/lens/doors.md` (arXiv minimal shape at line 23, HN shape at line 44, reddit shape at line 59, fxtwitter known post at line 68). The known post is the same one the 10-08 and 10-10 seats used (`watch/inbox/frontier_olm_2026-10-08/lens/doors.md:68`).

## Verdict table

| Door | Probed URL | Answered with data? | Note |
|---|---|---|---|
| arXiv export API | `export.arxiv.org api/query` minimal shape | YES, 1st probe | `search_query=all:electron&max_results=1` returned immediately; the sorted/phrase variant remains the known timeout landmine (10-08: `watch/inbox/frontier_olm_2026-10-08/lens/doors.md` sorted-variant URL), not re-probed today per the once-per-door rule |
| hn.algolia.com | `hn.algolia.com/api/v1/search` | YES, 1st probe | clean JSON, no auth, no redirect games |
| old.reddit.com `.json` | `old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=2` | NO | HTML "Welcome to Reddit" stub, zero JSON payload; THIRD consecutive recorded failure of this exact shape (10-08: `watch/inbox/frontier_olm_2026-10-08/lens/doors.md:62`; 10-10: prior file at this path, same verdict) |
| api.fxtwitter.com | `api.fxtwitter.com/elonmusk/status/1585841080431321088` | YES, 1st probe | known post resolved to full tweet JSON |

Score: 3 of 4 doors open to WebFetch today. Third consecutive identical verdict pattern (10-08: `watch/inbox/frontier_olm_2026-10-08/lens/doors.md:16`; 10-10: prior file at this path, same score).

## Recipes (what actually worked, verbatim probe evidence)

### 1. arXiv export API - WORKING with the minimal shape

```
GET https://export.arxiv.org/api/query?search_query=all:electron&max_results=1
```

Verbatim result of today's probe (WebFetch output, all fields present):

- Feed contains 1 `<entry>` element.
- First entry title: "The electronic structure of cuprates from high energy spectroscopy"
- First entry id: `http://arxiv.org/abs/cond-mat/0011267v1`
- `<opensearch:totalResults>`: "187346"

Liveness cross-check, neutral today: totalResults reads "187346", UNCHANGED from the 10-10 predecessor at this path (which recorded 187346; 10-08 had read 187279 at `watch/inbox/frontier_olm_2026-10-08/lens/doors.md:31`). The door answered with a well-formed feed today, so it is open; but the counter did not move day-over-day this time, so the counter is a weak freshness signal, not proof of staleness (WebFetch caches per URL for 15 minutes only; day-old carryover is not the explanation).

Known landmine, NOT re-probed today (once-per-door rule): the phrase+sortBy variant `search_query=all:%22local%20llm%22&max_results=2&sortBy=submittedDate&sortOrder=descending` timed out at the 60s WebFetch limit on 10-08 (per the 10-08 file and its 10-10 successor). Keep per-fetch shapes minimal until someone re-times the sorted variant.

### 2. hn.algolia.com (HN Search API) - WORKING, first choice for discovery

```
GET https://hn.algolia.com/api/v1/search?query=local%20llama&tags=story&hitsPerPage=2
```

Verbatim result of the probe (WebFetch output, all fields present in both hits):

- nbHits: 1,099 (unchanged from the 10-10 predecessor at this path; 10-08 had read 1,097 at `watch/inbox/frontier_olm_2026-10-08/lens/doors.md:49`). Same neutral-flat note as arXiv above.
- Hit 1: title "GPTScript working with function calling on local Llama3.3:70B", points 3, num_comments 0, objectID 42463686, created_at 2024-12-19T17:27:08Z.
- Hit 2: title "XTTS v2 and Local LLaMa", points 3, num_comments 0, objectID 38337642, created_at 2023-11-19T20:40:43Z.

No auth, no redirect games. Time-window sibling `search_by_date` remains OWED (that exact URL not fetched this session, same as 10-08 and 10-10).

### 3. old.reddit.com/r/LocalLLaMA/top.json - WALLED for WebFetch, day 3

```
GET https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=2
```

Verbatim probe outcome (WebFetch output): "This is an HTML page, not a JSON listing. The visible text content is: 'Welcome to Reddit' and 'Skip to main content'". Zero posts extractable.

Three consecutive sessions (10-08, 10-10, today) now show the same stub for the same URL shape under WebFetch, so treat this as the standing verdict, not a flake. OWED (not run in this ask, do not assume): whether curl with a browser `User-Agent` header, or the `www.reddit.com/...json` variant, gets through. Until re-probed with that instrument, reddit JSON is a curl-side door at best, never a WebFetch door.

### 4. api.fxtwitter.com - WORKING

Known post used (same as 10-08 `watch/inbox/frontier_olm_2026-10-08/lens/doors.md:68` and the 10-10 predecessor): `https://twitter.com/elonmusk/status/1585841080431321088`

```
GET https://api.fxtwitter.com/elonmusk/status/1585841080431321088
```

Verbatim probe result (WebFetch output):

- A `tweet` object exists in the JSON.
- id: 1585841080431321088
- text: "the bird is freed"
- author.screen_name: elonmusk
- created_at: "Fri Oct 28 03:49:11 +0000 2022"
- Media field: absent from the tweet object (no media key present).

Recipe for the sweep: `https://api.fxtwitter.com/<screen_name>/status/<id>` returns the tweet JSON the web UI hides. OWED, unchanged from 10-08 and 10-10: the media-bearing JSON shape (photos/videos arrays) is unverified because the probe post carries no media.

## Handoff

- Three doors stand open: hn.algolia.com (discovery lead), api.fxtwitter.com (X posts), arXiv export (minimal shape only, hang-tolerant timeout).
- Reddit stays a non-WebFetch door on three sessions of evidence; any sweep wanting r/LocalLLaMA must budget a separate curl+UA probe first.
- Both open counters (arXiv totalResults, HN nbHits) read flat vs 10-10; if the next probe also reads flat, stop citing counter movement as the liveness cross-check and switch to entry-content recency.
