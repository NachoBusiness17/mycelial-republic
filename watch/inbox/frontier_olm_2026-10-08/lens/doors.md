# Frontier doors probe - 2026-10-08

source-fetched: 2026-10-08
instrument: WebFetch, one probe per door, run 2026-10-08 by lens seat "lens-doors" (this session; every quoted value below is verbatim tool output from these probes)
ask: "Probe each frontier door once with WebFetch: the arXiv export API, hn.algolia.com, old.reddit.com/r/LocalLLaMA/top.json, and api.fxtwitter.com for one known post."

## Verdict table

| Door | Probed URL | Answered with data? | Note |
|---|---|---|---|
| arXiv export API | `export.arxiv.org/api/query` | YES, on 2nd probe | 1st probe (phrase + sortBy variant) timed out at the 60s WebFetch limit; minimal canonical query returned fine |
| hn.algolia.com | `hn.algolia.com/api/v1/search` | YES, 1st probe | clean JSON, no auth, no UA games |
| old.reddit.com `.json` | `old.reddit.com/r/LocalLLaMA/top.json` | NO | served an HTML "Welcome to Reddit" stub, zero JSON payload |
| api.fxtwitter.com | `api.fxtwitter.com/elonmusk/status/1585841080431321088` | YES, 1st probe | known post resolved to full tweet JSON |

Score: 3 of 4 doors open to WebFetch today.

## Recipes (what actually worked)

### 1. arXiv export API - WORKING (with a timeout landmine)

```
GET https://export.arxiv.org/api/query?search_query=all:electron&max_results=1
```

Verbatim result of the working probe:

- Feed contains 1 `<entry>` element.
- First entry title: "The electronic structure of cuprates from high energy spectroscopy"
- First entry id: `http://arxiv.org/abs/cond-mat/0011267v1`
- `<opensearch:totalResults>`: "187279"

Gotcha, measured today: the richer variant

```
https://export.arxiv.org/api/query?search_query=all:%22local%20llm%22&max_results=2&sortBy=submittedDate&sortOrder=descending
```

timed out after 60000 ms ("Tool execution timed out after 60000ms"). The export endpoint can hang on phrase queries with sort params. Working shape: plain `search_query=all:<term>` + `max_results`, no phrase quoting, no sortBy, until someone re-times the sorted variant. Keep per-fetch expectations small.

### 2. hn.algolia.com (HN Search API) - WORKING, first choice

```
GET https://hn.algolia.com/api/v1/search?query=local%20llama&tags=story&hitsPerPage=2
```

Verbatim result of the probe:

- Total hits: 1,097 (2 returned on this page).
- First hit title: "GPTScript working with function calling on local Llama3.3:70B"
- points: 3, num_comments: 0, objectID: "42463686", created_at: "2024-12-19T17:27:08Z"
- url: `https://blog.helix.ml/p/gptscript-helix-apps-for-fun-and`

No auth, no redirect, sub-second. Recipe for the sweep: `search_by_date` (`/api/v1/search_by_date?tags=story&numericFilters=created_at_i>...`) is the time-window sibling of this endpoint, not re-verified today (that exact URL was not fetched this session).

### 3. old.reddit.com/r/LocalLLaMA/top.json - WALLED for WebFetch

```
GET https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=2
```

Verbatim probe outcome: "This is an error/stub page, not actual Reddit content. The only text available is 'Welcome to Reddit' and a skip link." No `data` object, no `data.children` in what came back; zero posts extractable. Reddit served the fetcher an HTML shell instead of the JSON listing.

OWED (not run in this ask, do not assume): whether a browser `User-Agent` header via curl or a `www.reddit.com/...json` variant gets through. Only the WebFetch instrument above was used today. Until re-probed, treat reddit JSON as a curl-side door, not a WebFetch door.

### 4. api.fxtwitter.com - WORKING

Known post used: `https://twitter.com/elonmusk/status/1585841080431321088`

```
GET https://api.fxtwitter.com/elonmusk/status/1585841080431321088
```

Verbatim probe result:

- A `tweet` object exists in the JSON.
- id: 1585841080431321088
- text: "the bird is freed"
- author.screen_name: elonmusk
- created_at: "Fri Oct 28 03:49:11 +0000 2022"
- No media field present on this post (probe reported no "media" or photo entities; `is_note_tweet` is false). HTTP code 200, "OK".

Recipe for the sweep: `https://api.fxtwitter.com/<screen_name>/status/<id>` returns the tweet JSON the web UI hides. OWED: the media-bearing JSON shape (photos/videos arrays) is unverified because the probe post carries no media; pick a media post before relying on that field.

## Handoff to the sweep

- Lead with hn.algolia.com for discovery and fxtwitter for X posts; arXiv works but only with the minimal query shape and a hang-tolerant timeout.
- Reddit needs a different instrument (curl + UA candidate) before it counts as an open door; today's verdict is walled-for-WebFetch, based only on the single probe above.
