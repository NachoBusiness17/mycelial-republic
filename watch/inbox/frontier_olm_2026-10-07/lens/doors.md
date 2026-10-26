# Frontier doors probe - 2026-10-07

source-fetched: 2026-10-07

Method: each door probed exactly once with WebFetch, per the ask. Two doors answered via WebFetch (hn.algolia.com, api.fxtwitter.com). Two did not (arXiv export API timed out on the WebFetch path; old.reddit.com .json served no JSON). After the once-only probes, plain `curl` diagnostics were run against the two failed doors to separate "door down" from "our fetcher blocked"; those diagnostics are labeled as such below and are NOT the ask's probe.

## Verdicts

| Door | Answered today? | Evidence |
|---|---|---|
| arXiv export API | No via WebFetch (timeout at 60s); YES via plain curl diagnostic (HTTP 200 in 0.35s, 7,812 bytes) | see recipes |
| hn.algolia.com | YES, via WebFetch, valid JSON | recipe below |
| old.reddit.com/r/LocalLLaMA/top.json | NO, no JSON; 302 to login (`reason=lor2`) for unauthenticated fetch, custom UA did not help | see recipes |
| api.fxtwitter.com | YES, via WebFetch, valid JSON, HTTP 200 | recipe below |

## Exact working fetch recipes (verified today, this seat)

### hn.algolia.com - WORKING via WebFetch
- URL: `https://hn.algolia.com/api/v1/search?query=llm&tags=story&hitsPerPage=3`
- One WebFetch call, no headers needed. Returned valid JSON: `hits` array + `nbHits: 53859`, `nbPages: 334`.
- Sample hit (parse check): objectID `44567857`, "LLM Inevitabilism", 1773 points, created 2025-07-15.
- Variants not probed today (not run): `search_by_date` for recency sort, `tags=front_page` for the front page. Unverified here.

### api.fxtwitter.com - WORKING via WebFetch
- Known-post URL: `https://api.fxtwitter.com/jack/status/20` (jack's first tweet).
- One WebFetch call, no headers needed. HTTP 200, valid JSON.
- Parse check: author `@jack`, text "just setting up my twttr", created_at "Tue Mar 21 20:50:14 +0000 2006".
- Recipe generalizes: `https://api.fxtwitter.com/<handle>/status/<id>`.

### arXiv export API - NOT verified via WebFetch; WORKING via plain curl
- WebFetch probe: `https://export.arxiv.org/api/query?search_query=all:llm&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending` -> tool execution timed out after 60000ms. Honoring the once-only ask, no WebFetch retry was run. The WebFetch recipe is therefore UNVERIFIED today (OWED).
- Diagnostic (curl, not the ask's probe): `curl -sS --max-time 30 -o NUL -w "HTTP %{http_code} in %{time_total}s, %{size_download} bytes" "<same URL>"` -> `HTTP 200 in 0.345390s, 7812 bytes`. The door itself is up and fast; the failure is on the WebFetch fetch path (timeout), not arXiv.
- Working recipe until a WebFetch retry proves otherwise: the same URL via curl/requests with a short timeout; response is Atom XML.

### old.reddit.com/r/LocalLLaMA/top.json - CLOSED to unauthenticated fetch today
- WebFetch probe: `https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5` -> returned HTML titled "Welcome to Reddit" (skip-to-content nav only), no JSON, no posts.
- Diagnostic (curl with descriptive User-Agent `MagResourceHarness-frontier-olm/1.0 (local; contact: operator)`): first response `HTTP 302`, `Location: https://old.reddit.com/login/?reason=lor2&dest=...` (the `lor2` reason is Reddit's login-required gate for this surface); following the chain lands `HTTP 200` but `content-type: text/html` on the login page, not JSON.
- Conclusion: custom User-Agent alone does not open this door today. No verified unauthenticated recipe exists from this probe (OWED: verify a cookie/OAuth-bearing recipe or an alternate reddit surface before the sweep relies on this door).

## Receipts (commands run this session)

1. WebFetch `https://export.arxiv.org/api/query?search_query=all:llm&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending` -> TIMEOUT 60000ms
2. WebFetch `https://hn.algolia.com/api/v1/search?query=llm&tags=story&hitsPerPage=3` -> JSON, nbHits 53859, 3 hits parsed
3. WebFetch `https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5` -> HTML "Welcome to Reddit", no JSON
4. WebFetch `https://api.fxtwitter.com/jack/status/20` -> HTTP 200 JSON, @jack, tweet text + date parsed
5. curl arXiv same URL -> HTTP 200, 0.345390s, 7812 bytes
6. curl reddit with custom UA -> HTTP 302, 0 bytes, Location to `/login/?reason=lor2`
7. curl reddit with custom UA, follow redirects (-L) -> final 200 at old.reddit.com login page, content-type text/html
