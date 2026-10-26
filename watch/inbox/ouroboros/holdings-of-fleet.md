# HOLDINGS OF THE FLEET (cross-dogfood 3, the librarian rides the fleet)

Class: RECEIPT · Lane: cross-librarian (division B, gala_20260925/ouroboros ball) · Moment: 2026-10-02T13:27:41Z · Window: last 48h (since 2026-09-30T13:27Z)

Ask: check the holdings status of every primary source the standing workflows cited in the last 48h; the librarian expedition landed 61, so how many of the fleet's OTHER citations are held vs evaporated-with-session. Judge the fleet by the librarian-expedition holdings doctrine (HOLD-BOTH-DIRECTIONS, LIVENESS-IS-NOT-TRUTH, one-line law: no verdict=LANDED without the primary in holdings; source: watch/inbox/gala_20260925/librarian-expedition_RECEIPT.md + watch/inbox/gala_20260925/librarian-expedition/lanes/holdings-doctrine.json).

## Verdict first

The fleet's memory leaks: of 396 unique primaries cited by standing-workflow receipts in the window (after the line-context verification pass retracted 3 score-table false positives, see Method), 103 are held durably (26 pct), 291 are cited-only (a live URL promise, no bytes) and 2 are missing (locator dead). Leak count: 293 of 396 (74 pct) of the fleet's citation evidence does NOT survive offline. The estate held its own record-class primaries (the holdings audit is CLEAN at 262 claims / 842,965,168 B, both directions, 0 orphans) while the workflows that ran this week cite almost everything from unheld sources. The expedition's 61 healed the librarian's own sweep window; the rest of the fleet was not healed.

Per-workflow held columns do not sum to the fleet total: a citation held for one workflow is usually held for the others that cite it; fleet totals dedupe across workflows, rows do not.

## The holdings-of-the-fleet table

| workflow | cited uniques | held | cited-only | missing | LEAK count | survives offline |
|---|---|---|---|---|---|---|
| olm-mine | 36 | 27 | 9 | 0 | 9 | 75 pct (best large workflow) |
| wide-dig | 61 | 35 | 26 | 0 | 26 | 57 pct |
| drop-dig | 86 | 21 | 65 | 0 | 65 | 24 pct (worst large workflow) |
| music program | 0 | 0 | 0 | 0 | 0 | 0 pct (worse than the numbers show: see finding M) |
| salon-mine | 105 | 0 | 105 | 0 | 105 | 0 pct (total leak) |
| gap-analysis | 28 | 23 | 5 | 0 | 5 | 82 pct |
| fill-ball | 23 | 13 | 10 | 0 | 10 | 57 pct |
| ractor-engine | 3 | 3 | 0 | 0 | 0 | 100 pct (cites almost nothing external) |
| librarian-expedition | 92 | 58 | 34 | 0 | 34 | 63 pct |
| 48h-synth | 7 | 3 | 4 | 0 | 4 | 43 pct |
| the-gala | 0 | 0 | 0 | 0 | 0 | no id/repo-class citations (its sub-ball surfaces are the per-workflow rows above) |
| mickey17-v2 | 0 | 0 | 0 | 0 | 0 | no id/repo-class citations (its addendum cites estate paths only) |
| the-50 | n/a | n/a | n/a | n/a | n/a | no active surface found in the window |
| game-dig-* | n/a | n/a | n/a | n/a | n/a | no active surface found in the window |
| ADJACENT: model_garden (not a standing card workflow) | 85 | 7 | 78 | 0 | 78 | 8 pct |
| FLEET TOTAL (deduped) | 396 | 103 | 291 | 2 | 293 | 26 pct |

held = the cited primary's bytes survive in the estate at the snapshot moment: for papers, an id-matching file under a durable root (corpus/, memory/, state/arxiv/, docs/, mag/, tools/, watch/inbox) or a LANDED row in any memory/runs/**/*LANDING*.json ledger (262 claims, the audit re-hashed them today); for repos, a .git clone in the walk or an archive file named after the repo. cited-only = locator resolves (HTTP 200 probe this run) and no bytes held. missing = locator does not resolve (HTTP 404 this run). Instrument and raw per-citation detail: watch/inbox/gala_20260925/ouroboros/lanes/fleet_citations.json (535 workflow-citation pairs); full instrument output: watch/inbox/gala_20260925/ouroboros/lanes/cross-librarian.check.txt (audit block + extraction block, 31,984 B).

## Per-workflow doctrine verdicts (which evidence survives offline, which leaks)

- ractor-engine (3/3 held, 0 leak): the dogfood runs cite estate internals, and the 3 external primaries they do cite (the UF-124 fabricated-citation artifact set around arXiv 2407.12345) are held from the earlier gathering pass. Small cited set, fully held.
- olm-mine (27/36, leak 9): the mines are the best large surface because the state/arxiv ingest (4,010 dated files) and the 20260928 sweep _raw catches happen to land under its most-cited ids. The 9 leaks include headline ids from the 10-01 DIGEST: 2601.07054, 2604.17111, 2609.29757, 2609.32584, 2609.35875, 2609.36457, 2609.33180, huawei-csl/KVarN, 2609.12002.
- gap-analysis (23/28, leak 5) and fill-ball (13/23, leak 10): mid-table because they mostly cite the OTHER workflows' surfaces; their leaks are inherited leaks, concentrated on the same olm DIGEST ids above plus the two repo candidates gauravapiscean/agentic-kv-cache and Abrar051/sml_mcp_benchmark.
- wide-dig (35/63, leak 26): spiking_wide's heavy tail of linear-attention citations (the linear-family card alone names ~15 primaries) is held only where older holding passes caught it; 26 cited-only including the BICLab/SpikingBrain repos (cited 6 times, never cloned: the clone the sweep's atlas finding named is absent here too) and ggml-org/llama.cpp (190 cite locations, zero bytes held).
- librarian-expedition (58/92, leak 34): its own receipt set still leaks 34, and the sharpest one is self-inflicted: foundational-gaps.md's decision named arXiv 2406.11717 as today's zero-spend pinnable fetch (8 cite locations) and the expedition's fetch order led with it, but no byte of 2406.11717 is held at snapshot (the 61 landed other things). The decision was banked, not executed.
- drop-dig (21/86, leak 65): the landscape dig named ~65 repos and papers it never retained. Two honest heals inside the leak: the localfirst-steal ball's own lanes hold .git clones of its two central repos (watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain and .../lbrain-coding-agents), which is exactly the point-of-claim holding the doctrine asks for; the other ~63 repos in the scraped landscape (lbrain kit/website/test-n-learn forks, cognee community repos, anything-llm family) have zero estate bytes.
- salon-mine (0/105, total leak): the transcript vault's mined cards cite 105 unique papers and repos; not one byte is held. The vault's own pasted GitHub locators include two that do not resolve at all (see missing below). The salon's evidence survives only as prose about the transcripts.
- music program (0 id/repo-class citations, but the worst doctrine case in the fleet): its receipts carry NO locators at all. The evidence register in watch/inbox/music/lyric-archaeology.md section 3 is prose-only ("all fetched live this session via WebFetch, genius.com", 24 tracks titled but never URL'd), the fetched lyric bytes were retained nowhere, and the underlying corpus (C:/Users/foste/Desktop/music-ai, 110 files / 938,915,380 B, 51 artists) sits OUTSIDE every estate root, scratch-class. LIVENESS-IS-NOT-TRUTH is violated by construction: the program's primaries were live fetches, and what banked is prose about them.
- 48h-synth (3/7, leak 4) and the-gala / mickey17-v2 (0 external-primary citations each): the synthesis chapters inherit the fleet's leaks (agentic-kv-cache, sml_mcp_benchmark, 2609.33180); the gala card and the mickey17 addendum cite estate paths only.
- ADJACENT model_garden (7/85, leak 78; NOT a standing card workflow, labeled and separated): the 24-wide garden night is the same disease at larger scale. CORRECTION during this lane's verification pass: the earlier draft of this receipt called arXiv 2708.1190 a fabricated future-dated id cited by the garden; the line-context pass shows it is a BENCHMARK SCORE (watch/inbox/model_garden/MATE_MOE_V0_RESULT.md:72, "B MATE_MOE_v0 E=2 top-1 | 2602.9582 | 2708.1190") that my own bare-id regex misread as a citation. The fabrication smell was the instrument's, not the garden's; both score artifacts (2602.9582, 2708.1190) are retracted from the set.

## The 2 missing (unresolvable locators; named debt, never silently dropped)

| citation | cited by | locs | probe | note |
|---|---|---|---|---|
| bioankh84/echo-root-ve | salon-mine | 6 | 404 | transcript-pasted GitHub locator that does not resolve |
| docshotgun/a02a4c0c0a57e43ff4f... | salon-mine | 4 | 404 | same class |

## Top 10 for the next gathering expedition (not held, ranked by claim weight; all probe 200 today)

1. arXiv 2609.12002 (7 locs: fill-ball, gap-analysis, librarian-expedition, olm-mine)
2. arXiv 2609.35875 (6 locs: fill-ball, gap-analysis, librarian-expedition, olm-mine)
3. arXiv 2604.17111 (5 locs: fill-ball, librarian-expedition, olm-mine)
4. arXiv 2609.32584 (5 locs: fill-ball, librarian-expedition, olm-mine)
5. arXiv 2609.36457 (5 locs: fill-ball, librarian-expedition, olm-mine)
6. github gauravapiscean/agentic-kv-cache (4 locs: 48h-synth, fill-ball, gap-analysis)
7. github Abrar051/sml_mcp_benchmark (5 locs: 48h-synth, fill-ball)
8. arXiv 2601.07054 (4 locs: librarian-expedition, olm-mine)
9. arXiv 2609.29757 (4 locs: librarian-expedition, olm-mine)
10. arXiv 2609.33180 (3 locs: 48h-synth, fill-ball)

Weight = cite locations (capped 20) + 25 for a wide-read surface (drop receipt, DIGEST, LANDSCAPE, SYNTHESIS, synth chapter, receipt) + 5 per additional workflow citing it + 3 if missing. Ranked 11+ the same way, the queue continues with ggml-org/llama.cpp (190 locs, wide-dig), santhoshravindran7/portable-agent-memory, 2310.08560, 2505.11427, SakanaAI/natural_niches (still uncloned since the prior sweep named it), Mintplex-Labs/anything-llm, and the salon's 105-paper backlog. The full not-held list is in fleet_citations.json and in the check.txt EVERY NOT-HELD block.

## Method (and what this sweep adds to the prior one)

- Surfaces: every standing-workflow receipt surface with mtime in the window, including five surface groups the prior cited-missing sweep did not see: watch/inbox/music + the three music gala balls, salon_mine (+ gala ball), ractor_engine (3 dogfood runs, 51 cards), fillball (+ gala ball), the gap register plus its 15 mickey17_v2 run lanes, 48h_synth gala ball, model_garden top level (labeled adjacent, not standing). ABLITERATUS_DROP_20260929.md (2026-09-29T09:51Z) is outside this window strictly; kept for continuity with the prior sweep's window, flagged boundary.
- Extraction: arxiv.org URLs, month-validated bare arXiv ids, github owner/repo, and (new, for the music class) genius.com page slugs, per line, byte-regexed as in the prior sweep's extract_citations.py. github captures normalized: URL-path segments (users/, repos/, sponsors/, licenses/, rest/, user-attachments/ ...) blacklisted, .git suffixes and trailing punctuation stripped, case-folded.
- Held test: single 530,165-file walk over corpus/, memory/, state/, docs/, mag/, tools/, watch/inbox (scratch markers appdata/%temp%/tmpdir/.mimosa/.git internals excluded) plus all 14 LANDING ledgers (382 rows, 262 LANDED claims, of which gathering_expedition 61 verified directly from GATHERING_LANDING.json 23/23 + PAPERS_LANDING.json 38/38). Repos count as held ONLY via a .git clone or a named archive: the v3 spot-check caught and removed two false holds (state-spaces/mamba via an unrelated test filename inside the lmcache clone; vllm-project/vllm via lmcache's integration subdirectory) - a false held violates the doctrine exactly like a false zero.
- Fetchability: live HTTP HEAD probes this run, 12-wide, 12s cap: 295 not-held citations probed in the raw instrument run, 292 resolved 200 (cited-only), 3 returned 404, 0 unprobed. Liveness numbers are this run's promise-check only; per the doctrine they are not truth and not holdings.
- Line-context verification pass (verify_score_table_fps.py, this lane): every one of the 374 arXiv unique-match locs classified by its source line: 327 genuine (arxiv.org URL or explicit arXiv mention on the line), 43 bare-id-prose (id cited in prose or JSON without a URL on the line; kept, flagged as the softer class), 4 score-table hits. Of the 4, exactly 2 change the set: 2602.9582 and 2708.1190 are benchmark scores in one table row (MATE_MOE_V0_RESULT.md:72) and are retracted (fleet 398 -> 396 uniques, missing 3 -> 2). The other 2 (2503.01155, 2609.16338) keep their held status on genuine locs plus LANDED ledger rows; no other count moves.
- Delta vs the prior sweep (2026-10-01 ~19:37Z snapshot): 280 of this sweep's workflow-citation pairs, 269 unique citations, ride on surfaces that sweep did not read. The prior sweep's one WEAK holding (2609.27612, catalog pointer to a %TEMP% file) reads not-held here by construction: this instrument does not walk %TEMP% (outside the estate) and catalog-only temp pointers are not holdings (the instrument-audit decision already ruled the catalog unfit as the matching organ).
- Not run / limits: content-level checks (does the held text contain the quoted claim) NOT run - held means bytes exist, not that a quote re-verifies, same limit the prior sweep stated; book-class and non-id primaries (founding texts, Wilkes/Wheeler class, the music mp3 corpus as a byte set) are out of the id/repo instrument's scope and are handled as named findings; music genius-page holding would only register if a slug-named file existed in the walk (none does).

## Checks run for this receipt (this lane, this ask)

1. .venv/Scripts/python.exe -m mag.holdings_audit -> exit 0, verdict CLEAN, 262 claims / 842,965,168 B ledger-to-disk re-hashed, 263 files / 861,732,447 B disk-to-ledger, 0 unreceipted, 0 dup groups, 0 unreadable. Raw: watch/inbox/gala_20260925/ouroboros/lanes/cross-librarian.check.txt lines 1-5.
2. watch/inbox/gala_20260925/ouroboros/lanes/holdings_of_fleet.py -> exit 0, full fleet extraction + held-check + 295 probes + top-10 + JSON bank (fleet_citations.json, 535 pairs, ts 2026-10-02T13:27:41Z). Raw: the same check.txt, HOLDINGS INDEX line through the EVERY NOT-HELD block.
3. watch/inbox/gala_20260925/ouroboros/lanes/verify_score_table_fps.py -> exit 0, line-context classification of all 374 arXiv uniques: 327 genuine-url / 43 bare-id-prose / 4 score-table; retractions applied as stated in Method. Raw: the same check.txt, ARXIV MATCH VERIFICATION block.
4. Gathering ledger count: python json.load over memory/runs/gathering_expedition/GATHERING_LANDING.json + PAPERS_LANDING.json -> 23/23 + 38/38 LANDED = 61.
5. Music corpus location: os.walk(C:/Users/foste/Desktop/music-ai) -> exists, 110 files / 938,915,380 B; audio-suffix scan of estate corpus/memory/state -> 128 hits, all unrelated library samples.
6. Negative check: genius.com URL grep over all 17 music surfaces -> 0 hits; the register is prose-only (lyric-archaeology.md section 3).
7. Em/en-dash scan (record law): watch/inbox/ouroboros/holdings-of-fleet.md, lanes/cross-librarian.json, lanes/cross-librarian.check.txt -> em 0, en 0 in all three.
8. Not run: no test suite, no ratchet (this lane wrote no code under mag/ or tools/; its instrument lives in watch/inbox/gala_20260925/ouroboros/lanes/), no quote re-verification against held bytes (stated limit above).
