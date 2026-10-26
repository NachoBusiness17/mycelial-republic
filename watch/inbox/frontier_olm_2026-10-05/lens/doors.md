# Frontier doors probe - 2026-10-05

source-fetched: 2026-10-05
instrument: WebFetch (one probe per door, this session)
seat: lens-doors (workflow subagent)

## Scoreboard

| Door | URL shape | Status today |
|---|---|---|
| arXiv export API | export.arxiv.org/api/query | ANSWERED |
| HN Algolia | hn.algolia.com/api/v1/search | ANSWERED |
| r/LocalLLaMA top.json | old.reddit.com/r/LocalLLaMA/top.json | BLOCKED (HTML interstitial, not JSON) |
| fxtwitter | api.fxtwitter.com/:user/status/:id | ANSWERED |

3 of 4 doors answered. Every claim below is from the actual fetch run in this session; each fetch was made exactly once.

## Door 1: arXiv export API - ANSWERED

Working recipe:

```
https://export.arxiv.org/api/query?search_query=all:%22local+llm%22&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending
```

- Response format: Atom XML feed, parses clean, no auth, no key.
- Evidence: feed title echoed the query ("arXiv Query: search_query=all:"local llm"&id_list=&start=0&max_results=3"); `opensearch:totalResults` = 170; exactly 3 `<entry>` elements returned as asked; first entry "SoftGene: Protein Language Model-Enhanced Soft Prompting for Interpretable Gene Set Annotation", published 2026-10-02T09:07:55Z.
- Notes: space is encoded as `+` inside the quoted phrase; `sortBy=submittedDate&sortOrder=descending` gives freshest-first, which is what a frontier sweep wants.

## Door 2: HN Algolia - ANSWERED

Working recipe:

```
https://hn.algolia.com/api/v1/search?query=local+llm&hitsPerPage=3
```

- Response format: JSON, no auth, no key.
- Evidence: `nbHits` = 35091 for query "local llm" (echoed back in the `query` field). First three hits: "Show HN: Clippy - 90s UI for local LLMs" (1122 points, 275 comments, created 2025-05-06T15:02:22Z); "Building a fully local LLM voice assistant to control my smart home" (699 points, 186 comments, 2024-01-13T22:12:10Z); "The local LLM ecosystem doesn't need Ollama" (648 points, 207 comments, 2026-04-16T03:35:11Z).
- Notes: default endpoint is relevance-sorted; swap to `/api/v1/search_by_date` with `numericFilters=created_at_i>...` for a freshest-first window. Unverified here; only the recipe above was run.

## Door 3: r/LocalLLaMA top.json - BLOCKED

Recipe attempted:

```
https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3
```

- Result: Reddit served its standard HTML welcome/interstitial page ("Welcome to Reddit" / "Skip to main content") instead of JSON. No `data`, no `children`, no kind/message fields. This is the well-known unauthenticated-UA block shape.
- OWED: a working recipe for this door. Candidates not tried today (single-probe limit): oauth.reddit.com with credentials, `www.reddit.com` variant, alternative mirrors, or the free-tier Reddit API. None of these are verified; do not cite any of them as working until probed.

## Door 4: fxtwitter - ANSWERED

Working recipe (one known post, banked in the estate's own receipts):

```
https://api.fxtwitter.com/NachoQuixotic/status/2028342347361141030
```

- Post provenance: the v1 genesis napkin post, banked at `docs/ref/releases/RELEASE_NOTES_v1.md:51` and cross-listed in the witness spine at `docs/ref/releases/WITNESS_SPINE.md:27`.
- Response format: JSON, no auth, no key. HTTP code 200, status text "OK".
- Evidence: author @NachoQuixotic ("Nacho Business"); text `"Test chord: 44 28 K13 e4 Fool #NachoOvermindSeed"`; created "Mon Mar 02 05:31:15 +0000 2026"; engagement 1 like, 2 replies, 0 retweets, 1 bookmark, 1 quote, 12353 views.
- Notes: pattern is `https://api.fxtwitter.com/<user>/status/<id>` for any banked x.com URL; returns full text, media, and metrics without login.

## Harness caveats (observed behavior of the probe instrument)

- WebFetch upgrades http:// to https:// automatically.
- WebFetch responses are cached 15 minutes per URL, so a re-probe of the same URL inside 15 minutes is not a fresh fetch.

## OWED (explicit)

1. r/LocalLLaMA door: a verified working fetch recipe. Today's single probe of `old.reddit.com/r/LocalLLaMA/top.json` was blocked; no substitute was probed, so none is claimed.
