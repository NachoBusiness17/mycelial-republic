# Frontier doors probe - 2026-10-09

source-fetched: 2026-10-09

Instrument: each door probed exactly once with WebFetch on 2026-10-09 (the ask's named instrument). Reddit got one extra curl diagnostic afterward because its WebFetch probe failed and the ask wants a working recipe; that diagnostic is labeled curl, never presented as the WebFetch probe result.

Score: 3 of 4 doors answered. arXiv, HN Algolia, fxtwitter per-status = green. Reddit logged-out JSON = closed from this host.

## 1. arXiv export API - ANSWERED

- Probe URL: `https://export.arxiv.org/api/query?search_query=all:%22local+llm%22&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending`
- Working recipe: plain GET, no auth, no UA tricks. Response is an Atom XML feed; iterate `<entry>` for `id` / `title` / `published`. WebFetch upgrades http to https, so write the `https://` form directly.
- Evidence of life: feed returned 3 of 176 total entries, newest `2610.12458v1` "OmniCapBench" published 2026-10-08T17:59:21Z, plus `2610.11651v1` and `2610.11482v1` (all 2026-10-08). Fresh same-week material confirms the sort params rode through.

## 2. hn.algolia.com - ANSWERED

- Probe URL: `https://hn.algolia.com/api/v1/search?query=local%20llm&tags=story&hitsPerPage=3`
- Working recipe: plain GET JSON, no auth. Fields: `nbHits`, `hits[].objectID` / `title` / `points` / `num_comments` / `created_at`. Relevance-ranked; for fresh-first sweeps the standard variant swaps `search` for `search_by_date` (that variant was NOT run today, unverified this session).
- Evidence of life: `nbHits: 2947`, 3 hits returned, e.g. objectID `47788385` "The local LLM ecosystem doesn't need Ollama" 648 pts / 207 comments (2026-04-16).

## 3. old.reddit.com/r/LocalLLaMA/top.json - DID NOT ANSWER

- WebFetch probe URL: `https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5`
- Result: HTML page shell ("Welcome to Reddit" + skip-to-content link), zero Listing JSON, zero children. No titles/scores extractable.
- Curl diagnostic (browser UA `Chrome/126`, `Accept: application/json`): HTTP 302, and following it lands on `https://old.reddit.com/login/?reason=lor2&dest=...` which renders 404. `reason=lor2` is Reddit's logged-out block on `.json` surfaces.
- Working recipe: NONE from this host today, via either instrument. OWED: authenticated session cookie, or an alternate Reddit surface, before the next fire counts this door.

## 4. api.fxtwitter.com - ANSWERED (per-status endpoint)

- Probe URL: `https://api.fxtwitter.com/jack/status/20` (known post: Jack Dorsey's first tweet)
- Working recipe: plain GET, no auth. Path shape `/:screen_name/status/:id`. JSON carries `text`, `author.screen_name`, `created_at`, tweet ID, engagement counts.
- Evidence of life: 200 OK; text "just setting up my twttr", author `jack`, created `Tue Mar 21 20:50:14 +0000 2006`, ID `20`.
- Corroboration: today's digest commit f676ee787 recorded fxtwitter TIMELINE endpoints 404ing twice ("fxtwitter timelines 404 x2 = negative rows"); this probe shows the per-status path is alive, so the negative rows were timeline-shaped, not a dead host.

## Recipe card (copy-paste forms)

| Door | Green | URL form |
|---|---|---|
| arXiv | yes | `https://export.arxiv.org/api/query?search_query=all:QUERY&start=0&max_results=N&sortBy=submittedDate&sortOrder=descending` |
| HN Algolia | yes | `https://hn.algolia.com/api/v1/search?query=QUERY&tags=story&hitsPerPage=N` |
| Reddit JSON | no | blocked logged-out (lor2); OWED auth path |
| fxtwitter | yes | `https://api.fxtwitter.com/:screen_name/status/:id` (per-status only) |
