# Frontier door probe - lens record

source-fetched: 2026-10-02
instrument: WebFetch (one probe per door, plus one retry on each timeout) + curl cross-check on the doors WebFetch could not read
seat: lens-doors (Mag Resource Harness)

## Verdict table

| Door | Answered today (WebFetch) | Answered (curl) | Working recipe established |
|---|---|---|---|
| arXiv export API | YES | not re-run (no need) | yes |
| hn.algolia.com | YES | not re-run (no need) | yes |
| old.reddit.com/r/LocalLLaMA/top.json | NO (timeout x2) | reached, but auth-walled | NO, none today |
| api.fxtwitter.com | NO (timeout x2) | YES, full JSON | yes, curl only |

## Door 1: arXiv export API - ANSWERED

Probe (WebFetch, https):

```
https://export.arxiv.org/api/query?search_query=all:quantization&sortBy=submittedDate&sortOrder=descending&max_results=3
```

Evidence of life: well-formed Atom feed (namespace `http://www.w3.org/2005/Atom`), `totalResults` "40387", `itemsPerPage` "3", `startIndex` "0". First entry: "ZTA-Q: an Open-source RISC-V Platform for Accurate Quantized CNN Inference", `http://arxiv.org/abs/2610.01867v1`, published `2026-10-01T15:27:14Z`.

Working recipe: `https://export.arxiv.org/api/query?search_query=<terms>&sortBy=submittedDate&sortOrder=descending&max_results=<N>` returns Atom; entry id = `<feed>.entry.id`, date = `<feed>.entry.published`, title = `<feed>.entry.title`. Caveat learned this probe: bare `all:quantization` pulls quantum-physics strays (entries 2 and 3 of the probe were ILW/BO quantum hierarchies and hexatriene DMRG), so real sweeps should constrain with a category clause (e.g. `cat:cs.CL` / `cat:cs.LG` AND-joined) instead of trusting relevance ordering.

## Door 2: hn.algolia.com - ANSWERED

Probe (WebFetch, https):

```
https://hn.algolia.com/api/v1/search?query=ollama&tags=story&hitsPerPage=3
```

Evidence of life: valid JSON, `processingTimeMS: 4`, `nbHits: 4484`, `nbPages: 334` for query=ollama tags=story. Top hit: "Ollama is now powered by MLX on Apple Silicon in preview", objectID `"47582482"`, points 648, created_at `2026-03-31T03:40:45Z`; second hit "The local LLM ecosystem doesn't need Ollama" objectID `"47788385"` 648 points `2026-04-16T03:35:11Z`.

Working recipe: `https://hn.algolia.com/api/v1/search?query=<terms>&tags=story&hitsPerPage=<N>`; response shape is `{exhaustive, exhaustiveNbHits, hits[], hitsPerPage, nbHits, nbPages, page, params, processingTimeMS, query, serverTimeMS}`; per-hit fields used here: `title`, `objectID`, `points`, `created_at`. For freshness frontiers add `&numericFilters=created_at_i><unix_ts>` (standard Algolia param; not exercised this probe).

## Door 3: old.reddit.com/r/LocalLLaMA/top.json - DID NOT ANSWER (auth-walled)

Probe (WebFetch): `https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3` timed out at 60s. Retried once: timed out at 60s again. No body, no status ever surfaced through that instrument.

Cross-check (curl, exact commands run):

```
curl -sS -m 30 -A "mag-frontier-probe/1.0" -o NUL -w "status:%{http_code} redirect:%{redirect_url} size:%{size_download}\n" "https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3"
-> status:302 redirect:https://old.reddit.com/login/?reason=lor2&dest=https%3A%2F%2Fold.reddit.com%2Fr%2FLocalLLaMA%2Ftop.json%3Ft%3Dday%26limit%3D3 size:0
```

```
curl -sS -m 30 -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" -o NUL -w "final_status:%{http_code} final_url:%{url_effective} size:%{size_download}\n" "https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3"
-> final_status:200 final_url:https://old.reddit.com/login/?reason=lor2&dest=... size:323243
```

Verdict: the host is reachable (302 answered well under the 30s curl budget) but the `.json` endpoint redirects to a login page (`reason=lor2`), and even a Chrome user agent following redirects lands on 323KB of login HTML, not JSON. This is an auth wall from this network today, not a hard outage. OWED: a working unauthenticated-or-authenticated recipe for r/LocalLLaMA JSON (cookie jar with a logged-in session, or an alternate read path). Nothing asserted beyond what the two curl runs above showed.

## Door 4: api.fxtwitter.com - UP (curl only; WebFetch instrument timed out)

Probe (WebFetch): `https://api.fxtwitter.com/jack/status/20` timed out at 60s; retried once, timed out again.

Cross-check (curl, exact command run):

```
curl -sS -m 30 "https://api.fxtwitter.com/jack/status/20"
```

Evidence of life: JSON `{"code":200,"message":"OK",...}` with full tweet object for jack/status/20: `tweet.id` "20", `tweet.text` "just setting up my twttr", `tweet.author.name` "jack", `tweet.author.screen_name` "jack", `tweet.created_at` "Tue Mar 21 20:50:14 +0000 2006" (the known first tweet ever, used as the fixture post).

Working recipe: `https://api.fxtwitter.com/<user>/status/<id>` returns `{code, message, tweet:{id, text, raw_text, author:{name, screen_name, followers, ...}, replies, retweets, likes, created_at, ...}}`. Door is healthy; the failure was in the WebFetch instrument (60s timeout twice), not the door. Until WebFetch reads this host, fetch it with curl and parse the JSON locally.

## Instrument note for the next sweep

WebFetch succeeded on arXiv and HN but timed out at 60s on both reddit and fxtwitter while curl answered each in under a second to a few seconds. So: a WebFetch timeout here is NOT proof a door is down; pair it with a curl status check before declaring a door dead. Both timeout doors got exactly one WebFetch retry per the probe protocol (each door probed once, plus one retry on failure).

## Receipt

- arXiv probe: WebFetch, 2026-10-02, URL above, Atom feed quoted in Door 1.
- HN probe: WebFetch, 2026-10-02, URL above, JSON shape and hits quoted in Door 2.
- Reddit probes: WebFetch x2 timeouts; curl 302-to-login and curl -L browser-UA login-HTML, commands and outputs verbatim in Door 3.
- fxtwitter probes: WebFetch x2 timeouts; curl 200 full JSON, verbatim fields in Door 4.
