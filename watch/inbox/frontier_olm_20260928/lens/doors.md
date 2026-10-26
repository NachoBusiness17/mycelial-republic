# Frontier doors probe, 2026-09-28

source-fetched: 2026-09-28

Method: each door was probed exactly once with the WebFetch tool during this ask. No retries, no substitutes. Evidence below is what WebFetch returned, recorded verbatim where it matters. The lane directory `watch/inbox/frontier_olm_20260928/lens/` did not exist before this ask; it was created by this ask (mkdir -p, then this file).

Score: 3 of 4 doors answered with usable data. Door 3 (reddit json) did not answer; cause not verified.

## Door 1: arXiv export API, ANSWERED

- Working recipe (exact URL fetched):

```
https://export.arxiv.org/api/query?search_query=all:%22local+llm%22&max_results=2&sortBy=submittedDate&sortOrder=descending
```

- Recipe notes: HTTPS works directly. The phrase term needs percent-encoded quotes (`%22local+llm%22`); spaces become `+`. `sortBy=submittedDate&sortOrder=descending` returns the freshest entries first; `max_results` caps the feed size.
- Evidence returned: valid Atom XML, feed element in the `http://www.w3.org/2005/Atom` namespace, `opensearch:totalResults` 164. Entries seen: arXiv 2609.32288v1, "A Solvable Theory of Pre-training Data Poisoning: Regime-Dependent Scaling Exponents", published 2026-09-26T06:21:46Z; arXiv 2609.31540v1, "Can You Check That? The Checkability Boundary for Local LLM Network Automation", published 2026-09-25T17:11:55Z. Freshest entry is 2 days old at probe time, so the feed is live and current.

## Door 2: hn.algolia.com, ANSWERED

- Working recipe (exact URL fetched):

```
https://hn.algolia.com/api/v1/search_by_date?query=LocalLLaMA&tags=story&hitsPerPage=3
```

- Recipe notes: plain GET, no auth, JSON out. `search_by_date` for the freshest (use `search` for relevance-ranked); `tags=story` filters to stories; `hitsPerPage` caps results. Every hit carries `objectID`, which is the HN item id usable for `https://news.ycombinator.com/item?id=<objectID>`.
- Evidence returned: parsed as JSON, `nbHits` 285, `page` 0. Hits: "Redditor Connects an AMD GPU to a MacBook Pro" (2 points, 0 comments, objectID 49837324, created_at 2026-09-24T22:04:54Z); "Open AI in the Wild: Adoption and Adaptation of Open Models on R/LocalLLaMA" (1 point, 0 comments, objectID 49833786, created_at 2026-09-24T17:16:14Z); "UkisAI Swift Series / 27B, Flash Next and Bonsai 2 /-63.4% thinking, x1.95 speed" (1 point, 1 comment, objectID 49833102, created_at 2026-09-24T16:33:21Z).

## Door 3: old.reddit.com/r/LocalLLaMA/top.json, DID NOT ANSWER

- Recipe attempted (failed, exact URL fetched):

```
https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3
```

- Evidence returned: not JSON. The content was an HTML shell containing only the text "Welcome to Reddit" and a "Skip to main content" link. No `kind` field, no `data.children`, no JSON error object, and no status code or rate-limit text was visible to the fetch tool.
- Verdict: this door is closed to this fetch recipe today. OWED: root cause (bot interstitial, redirect, or rate-limit block) is unverified. The ask capped probing at one fetch per door, so no retry or variant (different UA, different path, www vs old) was run and none is claimed.

## Door 4: api.fxtwitter.com for one known post, ANSWERED

- Working recipe (exact URL fetched), one known post:

```
https://api.fxtwitter.com/status/1585841080431321088
```

- Recipe notes: plain GET, no auth, JSON out. Path form `/status/<tweet_id>` resolves any tweet id without knowing the author handle; a `/screen_name/status/id` form also exists but was not probed this ask.
- Evidence returned: parsed as JSON, `code` 200 with message "OK". Author Elon Musk, screen_name elonmusk, tweet text "the bird is freed", created_at "Fri Oct 28 03:49:11 +0000 2022". The known-post id 1585841080431321088 was supplied by this ask's probe selection (a widely known 2022 tweet, chosen as the stable known post).

## Harness notes

- The fetch tool upgrades HTTP input to HTTPS, so all recipes are recorded as HTTPS directly.
- Cross-host redirects would have been surfaced by the tool rather than followed; none of the three live doors returned one.
- Instruments used this ask: 4 WebFetch calls (one per door, listed above), one `dir` check that showed the lane dir absent (output: NO_DIR_YET), one `mkdir -p` that created it (output: MADE). No other commands were run. The reddit-door root cause was not probed further and is not claimed.
