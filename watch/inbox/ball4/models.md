# RECEIPT — ball4 luncheon follow, lane `follow-models` (division B)

Date: 2026-09-29 · Writer: gala-ball4-follow-models · Register: `watch/inbox/luncheon_watchlist_20260929_signals.jsonl` (appended 9 rows at 2026-09-29T21:57:37Z; register now 17 lines: 8 sibling-lane rows + 9 mine) · Check: `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow-models.check.txt` (exit 0, PASS)

## Targets (watchlist rows with lane containing `models`)

| Row | Target | Primary in-window signal | Date | Grade |
|---|---|---|---|---|
| 5 | Greg Brockman (OpenAI) | OpenAI paused frontier training + delayed a "too capable" release over security concerns | ~2026-09-26 (+/-1d, recency marker) | search |
| 17 | Tom Brown (Anthropic) | Super Intelligence Luncheon seat (no dated personal press found in-window) | 2026-09-29 | fetch |
| 20 | Dario Amodei (Anthropic) | Luncheon attendance + Politico Sept 28 WH AI-risk meeting; slowdown essay is **edge** (Sept 12-14, outside window, reported as edge) | 2026-09-29 / 2026-09-28 | fetch + search |
| 24 | Mark Zuckerberg (Meta) | Privacy reorientation of Meta AI ("all about privacy") | 2026-09-28 (URL-dated) | fetch |
| 28 | Sundar Pichai (Google) | Project Suncatcher TPU-satellite launch imminent; Gemini 4 "nearly ready" (DeepMind chief) | ~2026-09-24 (recency markers) | search |
| org | OpenAI | Training pause + agent-rogue reports; GPT-6.1 Astra cancellation (single low-grade source, flagged) | ~2026-09-26 | search |
| org | Anthropic | Claude Sonnet 5.5 released 2026-09-28 + Opus 5.5 2026-09-22 (Wikipedia byte-grep verified); $11.6B/7yr Akamai deal 2026-09-24 | 2026-09-28 / 09-22 / 09-24 | fetch (models) + search (Akamai) |
| org | Meta | Enterprise AI business + MongoDB CEO CJ Desai hire | ~2026-09-28 | search (+ fetch for privacy pivot) |
| org | Google | Gemini 4 imminent (no API as of felloai page currency 2026-09-17); Suncatcher launch | 2026-09-24 / 09-19 | search + fetch |

## Handle resolution (the fxtwitter door)

- **9/9 handles live-resolved via `api.fxtwitter.com`** (raw JSON saved as `fxtw_*.json` in the lane dir): @gdb (Greg Brockman, bio "President & Co-Founder @OpenAI"), **@DarioAmodei (real, bio "Anthropic CEO. darioamodei.com", 829,245 followers)**, @finkd (Mark Zuckerberg), @sundarpichai (CEO, Google and Alphabet), orgs @OpenAI / @AnthropicAI / @Meta / @Google.
- **The ask said "resolve the 2 search-grade handles"; the models-lane rows carry exactly ONE** (`search:TomBrown-Anthropic`, watchlist line 17). The other watchlist search-grade rows (Kratsios, Walters, Clayton, McDermott, Cairncross) belong to other lanes.
- **NEGATIVE RESULT, FIRST-CLASS: Tom Brown's X handle is UNRESOLVED.** Search-engine suggestions @NLPerson and @nocompute were both live-probed and REJECTED on identity (@NLPerson = "Tyler", 5 followers; @nocompute = "Stuart Peot", 1 follower); 6 candidates probed total (incl. @TomBrownAnthro = nonexistent), zero identity matches. Handle stays search-grade-unresolved; documented in the register row, watchlist left unedited.
- **Door limitation:** the fxtwitter user endpoint exposes identity only — no timeline/tweet payload on any of the 15 fetches (`tweet: null`). Person-level signals therefore came from web search, not tweet bodies.

## Fetch-grade pins (fetched and grepped this session)

- `https://www.nbcnews.com/politics/donald-trump/trump-host-summit-top-ai-leaders-washington-rcna599853` — datePublished 2026-09-29; Brockman/Amodei/Zuckerberg/Pichai all named; "Super Intelligence" x12.
- `https://en.wikipedia.org/wiki/Claude_(AI)` — byte-grep: Opus 5.5 `start date and age|2026|09|22`, **Sonnet 5.5 `|2026|09|28`** (the freshest Anthropic drop, in-window).
- `https://felloai.com/all-we-know-about-google-gemini-4/` — "pre-training started July 21, 2026... no model or API yet" (page currency Sept 17).
- `https://www.btpm.org/2026-09-28/can-you-trust-mark-zuckerbergs-meta-with-your-ai-data` — loads, URL-dated 2026-09-28.

**Fetch-attempted and BLOCKED (recorded):** Akamai PR (Access Denied, 544-byte shell) and its Reuters twin (771-byte stub) — the $11.6B Akamai claim therefore stays search-grade, resting on two concordant search-surfaced outlets incl. the issuer's own PR URL.

## Estate angles (one per register row; the through-line)

Frontier parity window is measurably OPEN: OpenAI paused training (~Sept 26), Gemini 4 is unshipped, Anthropic ships biweekly. The lane arms one operator decision — run the next distill/quantize cycle against the current frontier (Sonnet 5.5 / GPT-5.6-class) **before** Gemini 4 lands — and banks one posture: "slow down" rhetoric (Amodei essay, edge-of-window) coexists with $11.6B capex, so policy shock is a live scenario and owned weights + owned compute is the hedge. Meta's flagship succession (Llama herd → Muse Spark, secondary-sourced) is open-weights continuity risk: archive weights/licenses you depend on.

## Read-only compliance

No engagement, no posts, no writes to any external surface. Only local files written: register append, receipt, lane dir artifacts.

## Files

- Register rows: `watch/inbox/luncheon_watchlist_20260929_signals.jsonl` (lines 10-18 of the post-append file, writer `gala-ball4-follow-models`)
- Lane JSON: `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow-models.json`
- Check output: `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow-models.check.txt` (exit 0)
- Raw evidence: `fxtw_*.json` (15 handle fetches incl. 6 Tom Brown probes), `fetch_{akamai,reuters,wiki_claude,felloai,btpm,nbc}.html`, `append_models_rows.py`, `finish_check.py` — all in `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/`
