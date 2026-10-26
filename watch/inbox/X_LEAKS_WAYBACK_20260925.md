# X LEAKS VIA WAYBACK CDX - x-frontier-today lane retry (2026-09-25)

Lane: x-leak-retry, MICKEY-17 wave (OWED knockdown). The `x-frontier-today` lane was walled live
(X search 404/login, `MICKEY17_V2_ENGINE_SPEC_20260924.md:4`). This seat re-ran it through the
estate's receipted Wayback CDX door: `memory/runs/gapwave/hn_x_fanout/corpus_sources.md:61-72`
(section 2a, verified end-to-end 2026-09-20). json-mimetype captures only; window 2026-09-18..2026-09-25.

Raw evidence (every claim below is byte-checkable against these files):
`memory/runs/x_leaks_wayback_20260925/` - cdx_phase1.py, cdx_phase2.py, cdx_run_log.jsonl,
rows_midas_twitter.json, rows_simonw_*.json, phase1_summary.json, resp_*.txt

## Request ledger (7 Wayback requests, 6s sleep between calls)

| label | status | bytes | secs |
|---|---|---|---|
| midas_twitter | 200 | 5128 | 2.9 |
| simonw_twitter | ERROR <HTTPError 504: 'Gateway Time-out'> | 0 | 60.3 |
| simonw_x | 200 | 3 | 32.3 |
| id_2102150076076265726 | 200 | 20954 | 0.8 |
| id_2100991010855641520 | 200 | 7587 | 0.5 |
| id_2102569889881813328 | 200 | 6433 | 0.6 |
| simonw_twitter_retry | ERROR <HTTPError 504: 'Gateway Time-out'> | 0 | 60.3 |

Commands (venv python per repo law):

```
.venv/Scripts/python.exe memory/runs/x_leaks_wayback_20260925/cdx_phase1.py
.venv/Scripts/python.exe memory/runs/x_leaks_wayback_20260925/cdx_phase2.py
```

CDX query shape (recipe line 67, plus server-side json filter):

```
https://web.archive.org/cdx/search/cdx?url=twitter.com%2Fthemidasproj%2A&from=20260918&to=20260925&output=json&filter=mimetype%3Aapplication%2Fjson&limit=500
```

## HEADLINE: 25 json-mimetype X captures of @TheMidasProj escaped into Wayback this week

All 25 rows are captures of `twitter.com/TheMidasProj/status/<id>` URLs with mimetype
`application/json` (raw X API JSON, not the JS login shell). Full row list with capture ts,
digest and byte length: `rows_midas_twitter.json` (25 distinct URLs, zero duplicate digests).

Capture clusters (all capture timestamps 09-18 to 09-23, inside the window):

- 2026-09-18: 1 single (status/2100763690718908875) + 6-tweet thread 2100991010855641520..2100991019042906121
- 2026-09-21: 5-tweet thread 2102150076076265726..2102150084079005879 + 2 singles (2102182311903015256, 2102182611002990870) + 7-tweet thread 2102183742823436476..2102183753300799489
- 2026-09-23: 3 tweets (2102569889881813328, 2102572406669709554, 2102572407076630783) + 1 single (2102777664373457119)

## Recovered thread leads (3 of 25 fetched raw via the id_ door, recipe lines 68-69)

Fetch shape: `https://web.archive.org/web/<ts>id_/https://twitter.com/TheMidasProj/status/<id>`
returned `data` + `includes` X API JSON; author resolved as The Midas Project (@TheMidasProj).
Note: public_metrics are all zero in these captures (syndication-class client sees no engagement
counts); treat engagement as unknown, not zero.

### Thread 1 - 2026-09-18T16:51:06Z - the METR-bias thread (6 tweets, lead recovered)

- capture: ts 20260918165106, status/2100991010855641520, 7587 bytes raw (`resp_id_2100991010855641520.txt`)
- quotes tweet: x.com/nypost/status/2099992081624096899 (New York Post)
- verbatim `data.text`:

```
If you want to claim METR is biased, or that it acts in Anthropic's interests, you need to make an argument.

So, what does the evidence say? 🧵 

https://t.co/8d7TscguqX
```

### Thread 2 - 2026-09-21T21:36:48Z - the Kratsios "you can just stop it" thread (5 tweets, lead recovered; capture row 3845B, raw fetch 20954B)

- capture: ts 20260921213648, status/2102150076076265726 (`resp_id_2102150076076265726.txt`)
- quotes tweet: x.com/FoxNewsSunday/status/2101677761869816042 (Fox News Sunday)
- verbatim `data.text`:

```
“If you do believe that you’re developing a technology that is unsafe or you don’t want it out in the world, you can just stop it”.

This comment, from White House science and technology adviser Michael Kratsios, is the latest in a series of remarks from people close to the Trump https://t.co/k34UnMgZqS
```

### Thread 3 - 2026-09-23T01:25:00Z - the 20-country human-control statement thread (lead recovered)

- capture: ts 20260923012500, status/2102569889881813328 (`resp_id_2102569889881813328.txt`)
- quotes tweet: x.com/MTSlive/status/2102387840579711026
- verbatim `data.text`:

```
“AI must remain under human direction, oversight and control. It must be developed and used in line with international law.”

This is important: representatives of 20 countries and the European Commission signed this statement, calling for AI to remain under human control. https://t.co/KFLayX1faW
```

## Honest negatives and gaps

1. @simonw lane: CDX query `twitter.com/simonw*` (json filter, same window) returned HTTP 504
   Gateway Time-out twice (60.3s each: phase1 attempt and the phase2 retry). Transport death,
   not a verdict: INCONCLUSIVE, zero knowledge either way. `x.com/simonw*` in-window returned
   200 with an empty array: 0 json rows on the x.com domain (resp_simonw_x.txt is literally `[]`).
2. 22 of the 25 Midas rows were discovered but NOT id_-fetched (request budget ~6, ledger at 7).
   Their text is unknown. In particular the DSEWiki agent-to-agent wiki thread that led this
   week's agent discourse (per `memory/runs/mickey17_v2/lanes/x-frontier-today.json` row 1 and
   the lane's captaincompliance source) was NOT located among the recovered leads; the 09-21
   cluster 2102183742823436476..2102183753300799489 (7 tweets) and the 09-23 rows are the
   unexamined candidates. Rows + digests are on disk for the next seat: no Wayback re-query
   needed, only id_ fetches of already-known (ts, url) pairs.
3. Midas-on-x.com is UNTESTED, not zero: the twitter.com query hit rows first, so the phase1
   fallback never ran. Only simonw has a verified-empty x.com row set in-window.

## Estate binding (greps run this ask)

- `grep -ril kratsios watch/inbox corpus` -> 0 hits: Kratsios remark is NEW to the estate.
- `grep -rli "human direction, oversight and control|remain under human control" watch/inbox corpus` -> 0 hits: the 20-country statement is NEW to the estate.
- `grep -ril METR watch/inbox` -> many hits (topic present; the bias-defense angle is the new sliver).

## Steals (one seat, one sitting each)

1. Kratsios row -> the US science-and-tech adviser publicly told frontier labs that unsafe tech
   can "just stop" voluntarily; binds to the estate line that voluntary disclosure is the
   failure mode (x-frontier-today lane row 1). Landing spot: mickey17 v2 fold negatives
   section, next revision.
2. METR-bias thread -> the estate already treats METR as an external oracle; the leak shows the
   counter-discourse (bias accusation) is now organized. Steal: add a one-line "who benefits"
   field to external-oracle citations. Landing spot: watch triage rubric, next edit.
3. Next seat: id_-fetch the 22 unexamined rows starting with the 7-tweet 09-21 thread
   (ts/digest pairs already in rows_midas_twitter.json); look there for the DSEWiki thread.

*Append-only receipt. Written by x-leak-retry 2026-09-25. No em-dashes used.*
