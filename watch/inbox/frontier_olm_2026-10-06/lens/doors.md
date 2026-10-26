# Frontier doors probe - lens-doors - 2026-10-06

source-fetched: 2026-10-06

One probe per door, all via WebFetch on 2026-10-06. Verdict per door, then the exact recipe that worked.

## Scoreboard

| Door | URL | Verdict |
|---|---|---|
| arXiv export API | `https://export.arxiv.org/api/query` | ANSWERED (Atom XML, full data) |
| Hacker News Algolia | `https://hn.algolia.com/api/v1/search` | ANSWERED (JSON, full data) |
| Reddit (old.reddit top.json) | `https://old.reddit.com/r/LocalLLaMA/top.json` | FAILED (HTML interstitial, no JSON) |
| FixTweet | `https://api.fxtwitter.com` | ANSWERED (JSON, code 200) |

## Door 1: arXiv export API - ANSWERED

Recipe (worked first try):

```text
https://export.arxiv.org/api/query?search_query=all:quantization&start=0&max_results=3
```

Returns Atom XML. Probe evidence: `opensearch:totalResults` read 40448; first entry was
`arxiv.org/abs/2407.15508v3` ("Compensate Quantization Errors+: Quantized Models Are
Inquisitive Learners", published 2024-07-22T09:45:16Z). The plain-text `search_query=all:quantization`
form parses with no URL-encoding beyond none; sort defaults to relevance. For recency-sorted
frontier sweeps, add `&sortBy=submittedDate&sortOrder=descending` (documented param, NOT
probed today: mark any such run OWED until executed).

## Door 2: Hacker News (Algolia API) - ANSWERED

Recipe (worked first try):

```text
https://hn.algolia.com/api/v1/search?query=quantization&tags=story&hitsPerPage=3
```

Returns JSON. Probe evidence: `nbHits` read 503; top hit was "Quantization from the Ground
Up" (351 points, objectID 47519295, created_at 2026-03-25T16:06:34Z); third hit was
"Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses" (286 points,
objectID 49611128, created_at 2026-09-08). For date-bounded sweeps use the sibling endpoint
`https://hn.algolia.com/api/v1/search_by_date?query=...&numericFilters=created_at_i>...`
(documented endpoint, NOT probed today: OWED).

## Door 3: Reddit r/LocalLLaMA - FAILED for JSON

Probed once:

```text
https://old.reddit.com/r/LocalLLaMA/top.json?t=week&limit=5
```

Result: did NOT parse as Reddit JSON. The fetched body was an HTML page containing only
"Welcome to Reddit" and a skip link, no `"kind": "Listing"` structure, so no post titles or
scores were obtainable. This is Reddit serving an HTML interstitial to the fetcher's
non-browser client (interpretation of the observed body; the fetch tool does not send a
browser User-Agent and offers no UA override). Status: this door is CLOSED to WebFetch as
probed today. A curl with a spoofed browser UA might work but was NOT run (the ask limited
probes to one WebFetch per door): OWED if the lane needs Reddit. Fallbacks inside the estate:
use the hn.algolia door (LocalLLaMA-adjacent stories surface there) or WebSearch for
reddit-sourced links.

## Door 4: FixTweet (api.fxtwitter.com) - ANSWERED

Recipe (worked first try, but the post ID was NOT guessed: it was verified first via
WebSearch, which returned the canonical permalink
`https://twitter.com/elonmusk/status/1585841080431321088`):

```text
https://api.fxtwitter.com/elonmusk/status/<status_id>
```

Probe evidence: code 200; text exactly "the bird is freed"; author "elonmusk"; created_at
"Fri Oct 28 03:49:11 +0000 2022". The API accepts the legacy `twitter.com` permalink ID and
returns full JSON (text, author, timestamps) with no auth. Frontier-lane use: resolve a post
permalink via search first, then hit this door for the machine-readable body.

## Laws honored this probe

- Never fabricate: the fxtwitter post ID came from a WebSearch result (URL above), not from
  memory. The arXiv `sortBy` and hn `search_by_date` recipes are labeled OWED because they
  were not executed today.
- One probe per door, per the ask; no retry loops on the Reddit failure.
- Probe instrument: the WebFetch tool (HTTP upgraded to HTTPS, HTML-to-markdown on the
  response), 2026-10-06.
