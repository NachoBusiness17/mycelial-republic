# Frontier door probe - lens report

source-fetched: 2026-10-11
Instrument: WebFetch, one probe per door, this session (lens-doors).
Scope: connectivity + exact working recipe per source. No fabrication: anything not observed is marked OWED.

## Doors answered today (2026-10-11)

| Door | Verdict | Evidence quoted from the fetch |
|---|---|---|
| arXiv export API | ANSWERED | 3 entries returned out of 176 total; first entry id `http://arxiv.org/abs/2610.12458v1`, title "OmniCapBench: A Deep-Structured Evaluation Framework for Fine-Grained Audio-Visual Captioning", published `2026-10-08T17:59:21Z` |
| hn.algolia.com | ANSWERED | 5 hits on the page, `nbHits: 2957` total; newest hit created `2026-04-16T03:35:11Z`; top hit by points "Show HN: Clippy - 90s UI for local LLMs" at 1122 points (en-dash in the source title normalized to plain hyphen per seat law) |
| old.reddit.com/r/LocalLLaMA/top.json | BLOCKED | Reddit block/interstitial page, not post data: body contained only "Skip to main content" and "Welcome to Reddit"; 0 children/posts returned |
| api.fxtwitter.com | ANSWERED | HTTP 200; author `@jack`; text "just setting up my twttr"; created_at `Tue Mar 21 20:50:14 +0000 2006` |

## Exact working fetch recipes (verified by the probes above)

1. **arXiv export API** (Atom XML, no auth):
   `https://export.arxiv.org/api/query?search_query=all:%22local%20llm%22&max_results=3&sortBy=submittedDate&sortOrder=descending`
   Notes: `max_results` caps the page; `sortBy=submittedDate` + `sortOrder=descending` gives newest first; response is Atom, parse `<entry>` blocks for `id`, `title`, `published`.

2. **Hacker News (Algolia)** (JSON, no auth):
   `https://hn.algolia.com/api/v1/search?query=local%20llm&tags=story&hitsPerPage=5`
   Notes: `tags=story` filters to submissions; `hitsPerPage` caps the page; each hit carries `points`, `created_at`, `title`, `url`.

3. **Reddit old.json** (BLOCKED for this seat today):
   `https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5` was probed once and returned a block/interstitial page (see table). The fetch recipes that exist for Reddit (`?t=day&limit=5` params, JSON children) are known shape but the door did not hand data to this instrument on 2026-10-11. OWED: a retry recipe that passes (different UA/host variant, e.g. `www.reddit.com` or an authenticated token path) was NOT tested today, so none is asserted as working.

4. **fxtwitter** (JSON, no auth, per-post):
   `https://api.fxtwitter.com/<user>/status/<id>` - verified with the known post `https://api.fxtwitter.com/jack/status/20` (200 OK, tweet text and created_at returned as quoted above). Returns the tweet object directly as JSON; good as an X-surface reading door when a post id is known.

## Census

3 of 4 doors answered with real data on 2026-10-11: arXiv export API, hn.algolia.com, api.fxtwitter.com. 1 door blocked: old.reddit.com/r/LocalLLaMA/top.json.
