# FRONTIER DOORS PROBE - 2026-10-01

source-fetched: 2026-10-01
method: one WebFetch probe per door, same day, no retries (ask scale: once per door)
probed by: lens-doors (subagent), repo C:/Users/foste/Documents/projects/local_sovereign_agent

## Verdict table

| Door | Answered today | Evidence seen |
|---|---|---|
| arXiv export API | YES | valid Atom XML, 3 entries, totalResults 6685 |
| hn.algolia.com API | YES | valid JSON, nbHits 1090 |
| old.reddit.com/r/LocalLLaMA/top.json | NO | HTML block page, zero JSON |
| api.fxtwitter.com | YES | JSON code 200, first tweet returned |

Score: 3 of 4 doors answered 2026-10-01.

## Working fetch recipes (exactly as run today)

### 1. arXiv export API - WORKING
URL (the exact one fetched):
`https://export.arxiv.org/api/query?search_query=all:llama&max_results=3&sortBy=submittedDate&sortOrder=descending`

Recipe notes:
- Returns Atom XML (not JSON); parse `<entry>` elements, take `opensearch:totalResults` for corpus size.
- Returned this run: feed title `arXiv Query: search_query=all:llama&id_list=&start=0&max_results=3`; 3 `<entry>` elements; first entry "QuLoC: Photonic Quantum-Assisted Low-Rank LLM Compression", published 2026-09-30T16:53:11Z; totalResults 6685.
- `sortBy=submittedDate&sortOrder=descending` works for recency-first mining.
- Plain `all:llama` works as the query term; HTTPS (not HTTP) is what was fetched.

### 2. HN Algolia - WORKING
URL (the exact one fetched):
`https://hn.algolia.com/api/v1/search?query=local%20llama&tags=story&hitsPerPage=5`

Recipe notes:
- Returns JSON; key fields `nbHits` and `hits[].title / .points / .objectID`.
- Returned this run: nbHits 1090; hit 1 "GPTScript working with function calling on local Llama3.3:70B" (3 pts, objectID 42463686); hit 2 "XTTS v2 and Local LLaMa" (3 pts, objectID 38337642).
- `tags=story` filters to stories; no auth, no key, no UA games needed.
- For date-sorted mining, the same host's `search_by_date` path is the documented sibling endpoint, but it was NOT probed today (once-per-door rule), so its behavior today is unverified here.

### 3. old.reddit.com/r/LocalLLaMA/top.json - BLOCKED
URL (the exact one fetched):
`https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5`

What came back:
- NOT JSON. An HTML page reading "Welcome to Reddit" with a "Skip to main content" link; no subreddit name, no `children` array, no posts. Reddit served a block/redirect page to the fetcher.
- Consequence: this door is closed to plain WebFetch as of 2026-10-01.
- OWED / not verified today: whether a real browser User-Agent, `www.reddit.com` instead of `old.reddit.com`, or a curl with `-A` gets through. The ask capped this door at one probe, so no workaround was attempted and none is claimed working. Next probe of this door should try `www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5` and a curl UA variant, and only then report a recipe.

### 4. api.fxtwitter.com - WORKING
URL (the exact one fetched), using a known stable post (Jack Dorsey's first tweet):
`https://api.fxtwitter.com/jack/status/20`

Recipe notes:
- Pattern: `https://api.fxtwitter.com/<handle>/status/<id>` returns JSON, no auth.
- Returned this run: `code: 200`; author `jack`; text "just setting up my twttr"; created_at "Tue Mar 21 20:50:14 +0000 2006".
- Known-post probe confirmed the endpoint shape; door is open for tweet text pulls.

## Honesty ledger

- All four probes were run live during this ask, 2026-10-01, via WebFetch; no cached or hand-copied results.
- The Reddit door failure is reported as it happened; the two headline doors (arXiv, HN) returned data consistent with live queries (arXiv first entry published 2026-09-30T16:53:11Z, the day before the fetch).
- Nothing in this file is asserted beyond what the four fetches returned.
