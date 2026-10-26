# doors.md: frontier door probe, 2026-10-03

source-fetched: 2026-10-03
Instrument: WebFetch, one probe per door, run in a single parallel batch during this lens. Every result below is what the fetch returned this session; nothing is carried from prior runs.

## Scoreboard

| Door | URL host | Status |
|---|---|---|
| arXiv export API | export.arxiv.org | OPEN |
| Hacker News | hn.algolia.com | OPEN |
| Reddit r/LocalLLaMA | old.reddit.com | SHUT (HTML landing page, no JSON) |
| fxtwitter proxy | api.fxtwitter.com | OPEN |

## Per-door recipes and evidence

### 1. arXiv export API: OPEN

Recipe (exact URL that worked):

```
https://export.arxiv.org/api/query?search_query=all:%22large+language+model%22&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
```

Response: Atom/XML feed, root element `<feed>`, 3 entries, `opensearch:totalResults` 78,518.
Freshness proof it serves current-day submissions: first two entries are 2610.02199v1 ("TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning") and 2610.02196v1 ("InterEvolve: Test-Time Evolution of Reward Programs for Humanoid Loco-Manipulation"), i.e. October 2026 arXiv IDs at the head of a submittedDate-descending sort.

Working recipe notes: HTTPS root; `search_query=all:"..."` with `+` as the space encoding inside the quoted phrase; `sortBy=submittedDate&sortOrder=descending` puts the newest papers first; parse as Atom, not JSON.

### 2. Hacker News (hn.algolia.com): OPEN

Recipe (exact URL that worked):

```
https://hn.algolia.com/api/v1/search?query=local%20LLM&tags=story&hitsPerPage=3
```

Response: valid JSON, `hits` array with 3 hits out of 2,930 total for the query. Top hit: objectID 43905942, "Show HN: Clippy - 90s UI for local LLMs", 1122 points, created 2025-05-06T15:02:22Z.

Working recipe notes: plain HTTPS GET, JSON directly, no key, no headers needed. `tags=story` filters to stories; `numericFilters=points>100` style filters are available (not exercised this session, so unverified here).

### 3. Reddit r/LocalLLaMA (old.reddit.com): SHUT to WebFetch

Recipe probed (did NOT work through this instrument):

```
https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3
```

Response: no JSON. The fetch returned a Reddit HTML landing page containing only "Welcome to Reddit" and a "Skip to main content" link; no `data.children` array. This is Reddit serving an HTML shell instead of the .json payload, not a fetch-tool error.

Working fetch recipe: NOT ESTABLISHED through WebFetch on 2026-10-03. OWED: a working recipe (candidate untested paths: an authenticated or browser-like User-Agent via curl, or the www.reddit.com host) must be probed and receipted before any lane claims reddit mining. Do not assert either candidate works; this file records zero successful reddit fetches today.

### 4. fxtwitter proxy (api.fxtwitter.com): OPEN

Recipe (exact URL that worked), using a known post as the fixture (Jack Dorsey's first tweet):

```
https://api.fxtwitter.com/jack/status/20
```

Response: valid JSON, code 200 "OK", with a tweet object: text "just setting up my twttr", author @jack, created Tue Mar 21 20:50:14 +0000 2006.

Working recipe notes: shape is `https://api.fxtwitter.com/<handle>/status/<id>`; returns JSON without any key. Swap handle and status id for any target tweet.

## Probe protocol for the next lens

One WebFetch per door, all four in one parallel batch, each with a pointed extraction prompt. Record OPEN/SHUT per door the same hour; a SHUT door gets its failure mode quoted verbatim (as done above for reddit) so the next lens knows what changed.

## Probe run 2 (this seat, 2026-10-03)

Attribution note: the run-1 content above was found already banked in this file when this seat went to write; the author is not this seat's session. Left intact as a sibling/prior receipt; not verified by this seat. This seat then re-probed all four doors once each, in one parallel WebFetch batch, with different query params. Every verdict agrees with run 1.

Exact run-2 fetches and what they returned this session:

1. arXiv: `https://export.arxiv.org/api/query?search_query=all:%22local+llm%22&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending` - Atom XML, totalResults 169, newest first: arXiv:2610.01768v1 "The Innocent Courier: Covert Exfiltration Through Legitimate LLM Web Fetching" (2026-10-01T14:25:55Z), arXiv:2609.38630v1 "Strong Multilingual Privacy Tagging at Encoder Speed" (2026-09-29T22:41:39Z), arXiv:2609.33878v1 "Curating Merchant-Matching Training Data with Two Confidence-Gated Local LLM Judges" (2026-09-27T19:55:34Z). OPEN.
2. HN: `https://hn.algolia.com/api/v1/search?query=%22local%20llm%22&tags=story&hitsPerPage=3` - JSON hits: "Building a fully local LLM voice assistant to control my smart home" (699 pts, 186 comments, objectID 38985152, 2024-01-13T22:12:10Z), "The local LLM ecosystem doesn't need Ollama" (648 pts, 207 comments, objectID 47788385, 2026-04-16T03:35:11Z), "Lemonade by AMD: a fast and open source local LLM server using GPU and NPU" (572 pts, 111 comments, objectID 47612724, 2026-04-02T11:04:51Z). OPEN.
3. Reddit: `https://old.reddit.com/r/LocalLLaMA/top.json?t=week&limit=3` - same SHUT mode as run 1 but on t=week: HTML shell, "Welcome to Reddit" / "Skip to main content", no JSON, no data.children. HTTP status not visible to the instrument: OWED. No retry made (one probe per door); run 1's OWED candidate recipes (browser-like UA via curl, www.reddit.com host) remain untested by this seat.
4. fxtwitter: `https://api.fxtwitter.com/jack/status/20` - HTTP 200, JSON: "just setting up my twttr", @jack, created Tue Mar 21 20:50:14 +0000 2006, 308,784 likes, 124,695 retweets. OPEN.

Run-2 verdict: 3 of 4 doors answered (arXiv export API, hn.algolia.com, api.fxtwitter.com); old.reddit.com top.json SHUT to WebFetch in both runs (t=day and t=week), identical HTML-shell failure mode. Run-1 and run-2 recipe notes are consistent: Atom-not-JSON for arXiv, plain keyless JSON for HN and fxtwitter.
