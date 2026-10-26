# PHOTON ROT RE-ADJUDICATION — 2026-09-25 (photon-aftermath#1 follow-up)

Filed by the photon-rot-check seat, MICKEY-17 v2.1 wave (OWED knockdown). The fold ruled the Perplexity Photon post "mutated post-publication, stranding 4 quotes in persistent-coding-agents.json rows 2-5 with no Sep 24 Wayback capture to adjudicate" (`C:/Users/foste/Documents/projects/local_sovereign_agent/corpus/steal/MASTER_MICKEY17_V2.md:171`, Reason 7, id photon-aftermath#1; restated at `C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md:27`). This seat pulled Wayback captures (4 of the ~6-request throttle used) and re-adjudicated each stranded quote. Every fetched byte cited below is saved in this directory so the next seat can re-run every check.

## 0. RULING (one paragraph)

Verbatim-at-publish remains **byte-unadjudicable**: Wayback's entire capture history for the post is one contentless 204 record (CDX-verified this session; replay returns 403), archive.today has no snapshot (404), and a web search found no public mirror of the original wording. The mutation finding itself is **upgraded, with one correction**: today's live bytes carry a systematic rewording of all four stranded sentences (same facts, new sentences), and the launch-day AlphaSignal piece (datePublished 2026-09-24T18:07:51Z, fetched and saved this session) carries the stranded phrase "20% fewer machines" that today's post no longer uses verbatim, which is the first phrasing-level witness supporting mutation over burn-side fabrication. Correction: photon-aftermath#1's sub-claim that the 20% figure is "absent from today's live Photon post bytes" is false as of this session's fetch; the figure is present, reworded as "approximately 20% fewer equivalent serving machines than the old system's content nodes". One stranded fragment ("five months") is corroborated nowhere and stays fully stranded.

## 1. THE FOUR STRANDED QUOTES (read from the archive of record)

Lane file `C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/mickey17_v2/lanes/persistent-coding-agents.json`, rows 2-5 (1-indexed; list items 1-4), quotes at lines 15, 24, 33, 42. The same file in the workspace copy `C:/Users/foste/.zcode/workspace/default/mickey17_v2/lanes/persistent-coding-agents.json` is byte-identical (checked this session with `diff`: IDENTICAL). Rows are labeled by 1-indexed row number because photon-aftermath#1 and the fold use that convention.

- Row 2 (line 15): "Photon went from early design to full production serving 100% of live traffic in five months, while reducing p99 search latency from 800ms to 65ms and operating with 20% fewer machines than the system it replaced."
- Row 3 (line 24): "Prior to each full rollout, we also validated the new index by mirroring live traffic into it" + two U+2014 characters wrapping "known as shadow traffic validation" + "and compared retrieval and ranking outputs statistically against the incumbent." (em-dash glyph rendered as prose here per the no-em-dash law; exact bytes are in the lane file line 24 and in the saved scripts' inputs.)
- Row 4 (line 33): "The controller also logs its progress in resumable state, so if interrupted, it can continue from where it left off."
- Row 5 (line 42): "Note that because the two index formats differ, the percentiles are not directly comparable."

Row 1 (the swarm sentence, line 6) is NOT stranded: it is byte-exact in today's live bytes (my check, section 4), confirming the fold's duplicate ruling persistent-coding-agents#0 = photon-aftermath#2 (`MASTER_MICKEY17_V2.md:173`).

## 2. WAYBACK RECEIPTS (4 requests used of the ~6 cap; honest failures listed)

All requests curl with a Chrome UA, run this session.

- R1 (FAILED): `curl "https://web.archive.org/cdx/search/cdx?url=www.perplexity.ai/hub/blog/photon&output=json&from=20260923&to=20260926"` returned HTTP 200 with the Internet Archive-wide "Temporarily Offline" outage HTML page ("Internet Archive services are temporarily offline."). Consistent with the brief's "Wayback 429s since 09-15". Retried once per the transport-death rule.
- R2 (OK): same CDX query without the date filter, saved to `/tmp/wayback_cdx.json`. HTTP 200. Full response, verbatim, is the complete capture history for this URL:
  ```
  [["urlkey","timestamp","original","mimetype","statuscode","digest","length"],
  ["ai,perplexity)/hub/blog/photon","20260925181612","https://www.perplexity.ai/hub/blog/photon","application/http","204","FWVIMTF2FRUP4PFKWSNHMINRVOQOBMLO","4681"]]
  ```
  Exactly one capture ever: 2026-09-25 18:16:12 UTC, statuscode 204. This matches photon-aftermath#1's own record ("only a 204-status 09-25 18:16 record", `memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/photon-aftermath.json:16`). A 204 response has no body by RFC, so this capture holds zero page text: **Wayback still cannot adjudicate the stranded quotes.**
- R3 (OK, belt-and-suspenders): host-wide CDX query `matchType=host&limit=40` returned HTTP 200 with only 2021-2022 captures of the bare domain. No new /hub/blog/photon record. Note: CDX canonicalization collapses www and non-www of the same path onto one urlkey, so R2's exact query already covered both host forms of the lane's cited URL.
- R4 (FAILED replay, informative): `curl "https://web.archive.org/web/20260925181612id_/https://www.perplexity.ai/hub/blog/photon"` returned HTTP 403 with a 6,007-byte Wayback error body (saved `/tmp/wayback_204.bin`). No content retrievable from the only capture.

Not run (budget honesty): further Wayback replay variants; the CDX index fields above are authoritative for the no-content finding.

## 3. NON-WAYBACK FETCHES (each saved to disk in this directory)

- Live post: `curl -L "https://www.perplexity.ai/hub/blog/photon"` -> HTTP 200, 136,746 bytes, saved as `PHOTON_ROT_20260925.live.html`. (photon-aftermath#0/#1 measured 136,385 bytes earlier on 09-25; the +361-byte drift is unexplained, see section 7.)
- AlphaSignal piece: `curl -L "https://alphasignal.ai/news/perplexity-s-photon-slashes-search-latency-by-12x-for-ai-agents"` -> HTTP 200, 107,585 bytes, saved as `PHOTON_ROT_20260925.alphasignal.html`. Page metadata: `"datePublished":"2026-09-24T18:07:51.000Z"` (three occurrences: rendered JSON-LD and embedded payload), making it a launch-day witness.
- archive.today probe (supplementary, outside the named Wayback check): `archive.ph/newest/<url>` -> HTTP 404, no snapshot exists. Reported as attempted and empty, not substituted for the Wayback check.
- One web search for the most distinctive stranded phrase ("shadow traffic validation" + Perplexity Photon): no public mirror of the original wording surfaced. Reported as not found, not as absence-proof.

## 4. BYTE-COMPARE RECEIPTS (ran this session; re-runnable)

Script: `PHOTON_ROT_20260925.compare.py` (this directory; run with `.venv/Scripts/python.exe`). Receipt: `PHOTON_ROT_20260925.compare.json`. Method: HTML-unescape plus \uXXXX-escape decode, tag strip, NFC, dash/quote canonicalization, whitespace collapse ("exact" test), plus an alphanumeric-slug test that ignores all punctuation and spacing ("slug" test). Context extractor: `PHOTON_ROT_20260925.contexts.py`.

Results, verbatim from the script's stdout:

```
[row2] live.exact=False live.slug=False asig.exact=False asig.slug=False
[row3] live.exact=False live.slug=False asig.exact=False asig.slug=False
[row4] live.exact=False live.slug=False asig.exact=False asig.slug=False
[row5] live.exact=False live.slug=False asig.exact=False asig.slug=False
[row1-swarm] live.exact=True live.slug=True
[key] '20% fewer machines': live=False alphasignal=True
[key] 'five months': live=False alphasignal=False
[key] '100% of live traffic': live=False alphasignal=False
[key] 'shadow traffic': live=True ...
[key] 'percentile': live=True alphasignal=True
```

Reading: all four stranded quotes are full-sentence MISS against live bytes (replicating photon-aftermath#1's central finding) and against AlphaSignal. The swarm sentence (row 1) is byte-exact in live bytes. The key scan plus context extraction then found that the live post is not missing these FACTS, only these SENTENCES:

## 5. THE REWORDING MAP (stranded sentence -> current live sentence, both readable from saved bytes)

Current-wording carriers below are extracted by `PHOTON_ROT_20260925.contexts.py` from `PHOTON_ROT_20260925.live.html` (the post's Sanity CMS payload, so these are article body text, not site chrome).

- Row 2. Live carriers: "we continued the rollout until Photon served all production traffic." (no "100% of live traffic", no "five months": zero hits for "month" and "five" anywhere in live text); "In our production workflow, p99 response time fell from roughly 800 ms in the old system to roughly 65 ms in Photon."; "Photon uses approximately 20% fewer equivalent serving machines than the old system's content nodes while storing approximately 2.5 times as much data per document." Note the comparator changed: stranded text says "than the system it replaced", live text says "than the old system's content nodes".
- Row 3. Live carrier: "After these checks, we sent live queries to both engines simultaneously using shadow traffic. This allowed us to compare their performance and results on production workloads before changing which engine served users." The words "mirroring", "statistically", "incumbent" (all in the stranded sentence) have zero hits in live text.
- Row 4. Live carriers: "Because operation state is persisted, a restart doesn't force a build to start over; the controller can reattach to preparation already in progress, reuse a ready result, or continue an interrupted rotation from the saved step." and a figure caption "persisted controller state allows an interrupted rotation to resume." The word "resumable" has zero hits in live text.
- Row 5. Live carrier (FIG. 01 caption): "The reported percentiles and measurement setups are not a controlled like-for-like comparison." The phrase "index formats" has zero hits in live text.

## 6. PER-QUOTE ADJUDICATION

"Verbatim-at-publish" needs publication-era bytes; none exist (section 2). So the verdict per quote is: NOT ADJUDICABLE AS VERBATIM-AT-PUBLISH (no witness bytes), plus the strongest honest status each quote's content can claim from live witnesses.

1. Row 2: NOT ADJUDICABLE verbatim; content corroborated publication-era in part. Launch-day AlphaSignal carries "Internal p99 latency dropped from 800 ms to 65 ms, using 20% fewer machines" (verified at two locations in the saved bytes: rendered list and embedded JSON, sources array cites the same Photon URL), and the estate's 09-24 steal doc independently banks "Production p99 retrieval+ranking: 800ms -> 65ms" (`C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/PHOTON_FAST_SEARCH_STEAL_20260924.md:13`). AlphaSignal's "20% fewer machines" phrasing matches the stranded quote, not today's "20% fewer equivalent serving machines": first phrasing-level witness for mutation. Weakest fragments in the whole incident: "five months" and "100% of live traffic" appear in no witness (live post, AlphaSignal, or the 09-24 steal doc). "Five months" is wholly uncorroborated anywhere in the estate or the live web; treat it as unverified even for content.
2. Row 3: NOT ADJUDICABLE verbatim; no publication-era witness for the sentence; live post carries a reworded shadow-traffic passage covering the same fact. Mutation plausible via the post-wide rewording pattern, unproven for this sentence.
3. Row 4: NOT ADJUDICABLE verbatim; no publication-era witness; live post carries a reworded persisted-state/resume passage covering the same fact. Same status as row 3.
4. Row 5: NOT ADJUDICABLE verbatim; no publication-era witness; live post carries a reworded percentile caveat covering the same function. Same status as row 3.

Overall: photon-aftermath#1's mutation ruling STANDS, now with a launch-day phrasing witness and a verified rewording map; its "no Wayback capture to adjudicate" clause is re-verified this session (still true: the only Wayback record is contentless).

## 7. CORRECTION TO THE PRIOR RECORD, RESIDUAL UNKNOWNS

- CORRECTION: photon-aftermath#1 states the "20% fewer machines" figure is "absent from today's live Photon post bytes (re-fetch 136,385 B; 'fewer machines' MISS)" (`.../photon-aftermath.json:16`). True for the exact phrase "fewer machines"; false for the figure. This session's 136,746-byte fetch contains "approximately 20% fewer equivalent serving machines". The earlier MISS was an exact-phrase artifact of the revision, not a deletion of the claim. The row's core (four stranded sentences, no pub capture) is unaffected.
- What mutated is phrasing, not (mostly) facts: 3 of 4 stranded sentences have same-fact reworded carriers live today; only "five months" lost both its sentence and any carrier.
- Byte drift: photon-aftermath fetched 136,385 B earlier on 09-25; this seat fetched 136,746 B later the same day. Cannot distinguish a further small edit from dynamic payload (nonces, build hashes) at this seat's reach. Both fetches agree on the reworded text, so the adjudication is unaffected.
- Alternative to mutation not fully excluded: per-request A/B or geo-variant serving of the post. Argued unlikely because the reads split cleanly in time (v2-burn-era reads got the stranded text; all photon-aftermath-era and this seat's reads got the current text, including two same-session Sanity-plus-HTML reads), but no archival bytes exist to close it.
- Unrecoverable from this seat: Perplexity's Sanity document history (needs a token with history read), and the @perplexity_ai launch post (X is walled for the estate).

## 8. FILES THIS SEAT CREATED (all in `C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/`)

- `PHOTON_ROT_20260925.md` (this file)
- `PHOTON_ROT_20260925.compare.py` (byte-compare script; re-runnable)
- `PHOTON_ROT_20260925.compare.json` (machine receipt of every test result)
- `PHOTON_ROT_20260925.contexts.py` (live-text context extractor; re-runnable)
- `PHOTON_ROT_20260925.live.html` (live post bytes, HTTP 200, 136,746 B, fetched this session)
- `PHOTON_ROT_20260925.alphasignal.html` (AlphaSignal bytes, HTTP 200, 107,585 B, datePublished 2026-09-24T18:07:51Z)

No lane file, fold file, or other seat's artifact was modified.

Provenance: everything above was read or run this session; cited estate records are `MASTER_MICKEY17_V2.md:171,173`, `MICKEY17_V2_RUN_SPEC_ADDENDUM.md:27`, `memory/runs/mickey17_v2/lanes/persistent-coding-agents.json` (lines 6,15,24,33,42), `memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/photon-aftermath.json:16`, and `watch/inbox/PHOTON_FAST_SEARCH_STEAL_20260924.md:13`. Not done, stated as such: no publication-era byte capture exists anywhere this seat could reach, so no quote is certified verbatim-at-publish; "five months" remains uncorroborated for content as well.
