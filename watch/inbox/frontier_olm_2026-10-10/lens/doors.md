# Frontier doors probe - 2026-10-10

source-fetched: 2026-10-10

Instrument: WebFetch, one probe per door, run in this session (lens-doors seat, Mag Resource Harness estate, repo `local_sovereign_agent`). Every claim below is exactly what a fetch returned today; nothing is enriched or extrapolated. Probe-only pass: no content mining, no follow-on requests except the one fxtwitter ID correction documented in section 4.

## Verdict table

| Door | Status today | Evidence (this session's fetch) |
|---|---|---|
| arXiv export API | OPEN | Valid Atom XML, `opensearch:totalResults` = 79192 |
| hn.algolia.com | OPEN | Valid JSON, `nbHits` = 2957 |
| old.reddit.com `.json` | BLOCKED | HTML shell page ("Welcome to Reddit"), not JSON |
| api.fxtwitter.com | OPEN | JSON `code: 200` on a canonical known post |

## Recipes (the exact URLs that answered today)

### 1. arXiv export API - OPEN

```
GET https://export.arxiv.org/api/query?search_query=all:%22large+language+model%22&max_results=3&sortBy=submittedDate&sortOrder=descending
```

- Answered with a well-formed Atom feed for the probe query.
- `opensearch:totalResults` read 79192 for `all:"large language model"`.
- First 3 entries (sorted newest first): "OmniCapBench: A Deep-Structured Evaluation Framework for Fine-Grained Audio-Visual Captioning" submitted 2026-10-08T17:59:21Z; "FastBench: Can Streaming VLMs Perceive High-Dynamic Real-World Streams?" submitted 2026-10-08T17:55:20Z; "WOVEN: Weaving Visual World Modeling into Multimodal LLMs" submitted 2026-10-08T17:52:03Z. Freshness is within roughly 2 days of this probe, so the pipe carries current submissions.
- Recipe notes: use the `https` form of `export.arxiv.org` (the fetch layer upgrades `http` to `https` anyway); quote multi-word queries with `%22`; `sortBy=submittedDate&sortOrder=descending` is what makes the door a freshness lane. `max_results` bounds the response.

### 2. hn.algolia.com - OPEN

```
GET https://hn.algolia.com/api/v1/search_by_date?query=local%20llm&tags=story&hitsPerPage=3
```

- Answered with parseable JSON, no auth, no headers.
- `nbHits` = 2957 for query "local llm", tags=story.
- First 3 hits by date: objectID 50032575 "Local LLM Inference at Scale with vLLM" (1 point); objectID 50032037 "If LLMs Can Decide Without Fine-Tuning, Do We Still Need Models Like Jev?" (1 point); objectID 50029518 "Show HN: SRA-RiskGate-4B - Local LLM for stablecoin risk gating and disputes" (2 points).
- Recipe notes: `search_by_date` is the recency lane; the sibling endpoint `/api/v1/search` is the relevance-ranked form (documented shape, not re-probed today). `tags=story` filters out jobs/asks. `hitsPerPage` bounds the response.

### 3. old.reddit.com .json - BLOCKED today

```
GET https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3
```

- Did NOT return JSON. The response was an HTML page containing only "Welcome to Reddit" plus a "Skip to main content" link. The request was redirected or blocked at the door; there was no `data.children` structure to read. This is the session's observed outcome, not a diagnosis of the cause.
- OWED: a working Reddit JSON recipe. Candidates the estate should try next from a lane that can set headers (custom User-Agent per Reddit's API etiquette) or the `oauth.reddit.com` route with a token. Neither was verified today, so neither is asserted to work.
- Standing rule until the OWED closes: treat r/LocalLLaMA as an unverified door. Do not cite any Reddit-sourced rank or score through this path.

### 4. api.fxtwitter.com - OPEN (one corrective fetch documented)

Attempt 1, ID guess `1522979712296849280`, returned HTTP 404 with no body retrieved. That ID could not be verified as a real post by this seat, so it is recorded as a bad known-post guess by the lens, not as a door failure or a door outage.

Working recipe (attempt 2, canonical known post):

```
GET https://api.fxtwitter.com/BarackObama/status/266031293945503744
```

- Answered with parseable JSON: top-level `code: 200`, `message: "OK"` (there is no top-level `success` field in the response).
- Author: handle `@BarackObama`, name "Barack Obama".
- Text: "Four more years. http://t.co/bAJE6Vom", `created_timestamp` 1352261778 (2012-11-07).
- Recipe notes: the path shape is `api.fxtwitter.com/:screen_name/status/:id`. The bare `/status/:id` form was not tested today and stays OWED. Lesson for the sweep: verify a post ID exists before probing with it; a 404 here is ambiguous between dead post and dead door.

## Door-law notes for the frontier sweep

- Two doors (arXiv export, HN Algolia) answer through the plain fetch layer with zero headers and zero auth: they are the safe bulk lanes for tonight's run.
- Reddit needs a header-setting or authenticated lane before it counts as a source; its probe returned an HTML block page, so it is CLOSED for this pass.
- fxtwitter answers cleanly but demands a genuinely known post ID; a single 404 must not be read as door death.
- All fetches today were against the exact URLs printed above; the only retry in the whole pass was fxtwitter attempt 2 after the documented 404.
