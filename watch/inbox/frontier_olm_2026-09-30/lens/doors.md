# Frontier doors probe, 2026-09-30

source-fetched: 2026-09-30

Method: each door was probed exactly once with the WebFetch tool during this ask (the ask's named check). After the reddit door failed, three supplemental `curl` runs and one repo grep were run to close the reddit root-cause item the 2026-09-28 doors file left OWED; those are labeled as supplements and are not substitutes for the WebFetch probe. Evidence below is what the tools returned, recorded verbatim where it matters. The lane directory `watch/inbox/frontier_olm_2026-09-30/lens/` did not exist before this ask; it was created by this ask (`mkdir -p`, output: MADE).

Score: 3 of 4 doors answered with usable data. Door 3 (reddit json) did not answer; root cause now verified (login/rate-limit wall, see Door 3).

## Door 1: arXiv export API, ANSWERED

- Working recipe (exact URL fetched):

```
https://export.arxiv.org/api/query?search_query=all:llama&max_results=3&sortBy=submittedDate&sortOrder=descending
```

- Recipe notes: HTTPS works directly, plain GET, no auth, Atom XML out. `search_query=all:<term>` with `+` for spaces (phrase terms need percent-encoded quotes `%22...%22`, per the 09-28 probe at `watch/inbox/frontier_olm_20260928/lens/doors.md:14`). `sortBy=submittedDate&sortOrder=descending` returns freshest first; `max_results` caps the feed.
- Evidence returned: valid Atom XML. Feed reports `<opensearch:itemsPerPage>3</opensearch:itemsPerPage>` (3 entries). First entry: "XU-RS: Explaining Credal Width in Random-Set Language Models", id `http://arxiv.org/abs/2609.37594v1`, `<published>2026-09-29T13:48:33Z</published>` - one day old at probe time, so the feed is live and current.

## Door 2: hn.algolia.com, ANSWERED

- Working recipe (exact URL fetched):

```
https://hn.algolia.com/api/v1/search?query=local%20llm&tags=story&hitsPerPage=3
```

- Recipe notes: plain GET, no auth, JSON out. `search` is relevance-ranked (the 09-28 probe verified the `search_by_date` variant for freshest-first at `watch/inbox/frontier_olm_20260928/lens/doors.md:25`; both endpoints answer). `tags=story` filters to stories; `hitsPerPage` caps results; each hit carries `objectID` usable as `https://news.ycombinator.com/item?id=<objectID>`.
- Evidence returned: parsed as JSON. `"nbHits":2916` total, 3 hits in the response (`"hitsPerPage":3`), query echo `"query":"local llm"`. First hit: "Show HN: Clippy - 90s UI for local LLMs" (title's dash ASCII-normalized per the estate dash law), `"points":1122`, `"objectID":"43905942"`.

## Door 3: old.reddit.com/r/LocalLLaMA/top.json, DID NOT ANSWER

- Recipe attempted (failed, exact URL fetched):

```
https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5
```

- WebFetch evidence returned: not JSON. An HTML page containing only the text "Welcome to Reddit" and a "Skip to main content" link. No `kind` field, no `data.children`.
- Supplemental curl evidence (run this ask to close the OWED root cause, clearly beyond the one-probe cap):
  - `curl -sS -m 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Mag-lens-probe" "https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3"` → `HTTP 302 bytes 0`, curl exit 23.
  - Same URL with `-L` (follow redirects) → `HTTP 200 bytes 0 final https://old.reddit.com/login/?reason=lor2&dest=https%3A%2F%2Fold.reddit.com%2Fr%2FLocalLLaMA%2Ftop.json%3Ft%3Dday%26limit%3D3` - the redirect target is the login wall, `reason=lor2` (Reddit's anonymous rate-limit/login redirect code).
  - `curl -sSL -m 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Mag-lens-probe" "https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=1"` → `HTTP 403 bytes 189908` (a ~186 KB block page).
- Root cause (verified this ask): Reddit gates anonymous JSON and HTML from this machine's egress IP - old.reddit 302-redirects to the login wall, www.reddit serves a 403 block page. This matches the same `reason=lor2` 302 an estate lane saw on 09-28 (`watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-reddit.md:11`) and the 09-28 doors verdict (`watch/inbox/frontier_olm_20260928/lens/doors.md:31`).
- Route-around (prior-session evidence, NOT re-probed this ask): the 09-28 sweep read reddit content through mirrors - pullpush (`watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-reddit.md:60`) and redlib (`watch/inbox/frontier_olm_20260928/sweep/evals-self-improvement-reddit.md:49`, `redlib.catsarch.com`). The reddit JSON door itself stays closed; a working direct reddit recipe remains OWED.

## Door 4: api.fxtwitter.com for one known post, ANSWERED

- Working recipe (exact URL fetched), one known post:

```
https://api.fxtwitter.com/elonmusk/status/1585841080431321088
```

- Recipe notes: plain GET, no auth, JSON out. This is the `/<screen_name>/<status_id>` path form; the 09-28 probe verified the bare `/status/<tweet_id>` form (`watch/inbox/frontier_olm_20260928/lens/doors.md:47`), so both path shapes work.
- Evidence returned: parsed as JSON, `"code":200,"message":"OK"`. Author: `"screen_name":"elonmusk"`, `"name":"Elon Musk"`, tweet `"text":"the bird is freed"` (the same known 2022 post id 1585841080431321088 used by the 09-28 probe).

## Harness notes

- The fetch tool upgrades HTTP input to HTTPS, so all recipes are recorded as HTTPS directly. Cross-host redirects would be surfaced rather than followed; none of the three live doors returned one.
- Instruments used this ask: 4 WebFetch calls (one per door), 3 curl runs (reddit supplements, listed above), 1 repo grep for prior reddit recipes (hit list included `watch/inbox/burn_wave_20260926/B2_142_cerebras_dig_20260926.md:160` "Reddit served HTML walls to both .json and old.reddit"), 1 Read of the 09-28 doors file for continuity, 1 mkdir. No other commands were run.
- Continuity vs 2026-09-28: same 3-of-4 score, same failing door; the one OWED item this file closes is the reddit root cause (was "unverified" in the 09-28 doors file, now verified as login/rate-limit wall by direct curl evidence above).
