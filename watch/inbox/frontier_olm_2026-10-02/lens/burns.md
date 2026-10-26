# Lens: burns (what was already mined this week, so nobody re-banks it)

Folded 2026-10-02 by the frontier_olm_2026-10-02 burns lens. House laws held: ascii only,
no em or en dashes, every claim cites the file it was read from this sitting, nothing
asserted from memory.

## How this was built (instruments, this sitting)

- `./.venv/Scripts/python.exe` read of `memory/burns/LEDGER.jsonl`: 693 lines, 562,938 bytes,
  mtime 2026-09-28T17:15:27Z; last 30 rows read in full (lines 664-693).
- Directory walk of `watch/inbox/` with cutoff mtime >= 2026-09-29 (45 dirs returned, 44 in
  window); the three-day window (2026-09-30 to 2026-10-02) carrier list below comes from that walk.
- Full or head reads this sitting of every file cited below with line numbers. Dirs named
  without line numbers were LISTED only, not read: `secret_gate_results` (probe JSON dumps),
  `frontier_asks`, `ds_batches`, `music`, `transcripts`, `handoff` (ZCode session zip).

## 1. The burns ledger is stale: this week's burns are NOT in it

`memory/burns/LEDGER.jsonl` last row is ts 2026-09-28T13:45:00Z (line 693) and the file has not
been touched since 2026-09-28T17:15Z. Anything burned 09-29 onward lives as carrier directories,
not ledger rows. Three lanes ran the ledger through 09-28; their terminal verdicts are the
anti-rebank baseline:

- **Free-resource-landscape:** Lightning credits chase closed FULLY DEAD alongside
  Chutes/SiliconFlow/Scaleway after docs, search, and Wayback doors all returned
  client-rendered shells with zero quotable tier language (line 690, receipts
  `watch/inbox/BURN_free-resource-landscape_20260928_k.md` through `_m.md`). DeepSeek window
  canon corrected: peak = 01:00-04:00 plus 06:00-10:00 UTC Mon-Fri, everything else off-peak at
  50 pct (line 671); lane live-and-armed, authenticated models GET 200 (line 677), first real
  chat call 200 at 11:04Z (line 680); the billing-side 50 pct discount check is owed at
  invoice strength, not re-derivable from responses (no price field). Featherless roster-diff
  standardized on the full-dump instrument (22,054 served rows); the paged 50,652 counter is
  reported-superset telemetry; the 28.6k unserved-row gap stays owed (line 683). LLM7 cap
  table: GLM-5.3-Flash dropped from the free roster, 4 free ids stable across intervals
  (lines 665, 674, 692). Do NOT re-chase any of these lanes without a new instrument.
- **Doctrine-owed-chase:** Sefer Raziel topic closed green-pending-chronogram (line 693). The
  pinned scan (HebrewBooks req 35004) is a Rubinstein press reprint, Nagyvarad 1953/54, NOT
  Amsterdam 1701 (line 687); the Amsterdam imprint is byte-backed off the archive.org plate
  JPEG but the copy is a modern reset reproduction carrying a 1701-style frontispiece
  (line 691); the year-chronogram decode is the single formally OWED debt (tooling-dependent
  on a higher-res scan). Nine wrong-book closures already spent. Kol HaTor ch. 2 phantom
  mitzvah line double-attested absent, English-stream vs Hebrew-print-stream provenance noted
  (line 682).
- **Middle-path-doctrine:** carrier-supply work, all minted: founding-sentence restatement
  (line 666), X6 withdrawal clause (line 669), Abulafia/Vital third carrier (line 672),
  Kook/Inquisitor fourth carrier (line 676). The game-class clause F8 re-armed with a
  pre-registered ractor-class falsifier (line 678) and an instrumentation spec against
  `mud.html` bytes proving the stub has NO factions, sentiment, VM pool, or gift channel, so
  F8 is not fireable without a gated stub build (line 681). X6 window audit green, 12 days to
  2026-10-10 (line 684).

## 2. The olm fold was already run THREE times this week: same areas, same doors

This sweep's direct predecessors. Re-banking any of these is the failure mode this lens exists
to stop.

### frontier_olm_20260928 (fold written 09-29, second pass, superseded its same-day predecessor)

32 sweep returns (8 areas x 4 doors, all ok:true), 21 confirmed finds, 3 unconfirmed, 5 steal
cards; the overwrite that produced it destroyed the first-pass text irrecoverably
(`frontier_olm_20260928/DIGEST.md:1-39`).

### frontier_olm_2026-09-30 (day-1 run; DIGEST backfilled 2026-10-02 by fillball, banner at :3)

23 confirmed finds, 6 steal cards, selection rule stated at :12 (`frontier_olm_2026-09-30/DIGEST.md`).
Headline confirmed finds with probes already specced: admission control with measured
false-accept rates (Touchstone, arXiv 2609.31540, row 12); provider choice as a second decision
axis, 8.8x price and 68x latency spread (arXiv 2609.37902, row 13); KV cache byte-identity with
the 17.5/33.1/~49.4 pct recompute decomposition and the ~60 pct fill cliff (doug.sh + HN rows
7-11); Qwen small-model supply drying up (r/LocalLLaMA 1wrez7j, row 16); quant laws: never
below 3 bits for agentic work, Q2_K never, perplexity alone never gates (:18, rows 20-23).
One probe was RUN, not just specced: the tokenizer probe (`tools/olm_tokenizer_probe.py`)
falsified the 2.6x context-cost claim and surfaced a truncation-cap defect at
`mag/lattice_loop.py:280` (:16, :34). GLM-5.3-Flash free on ZCode extended through Oct 7
(row 15); the olm-x probe window closes Oct 7 (:85). Known unrecoverables: the day-1
unconfirmed trio (r/LocalLLaMA 1sy7srk KV tables, arXiv 2609.21341 serving confound) is
NOT on disk and NOT registered (:72); refetching them is a named rank-10 fill (:82).

### frontier_olm_2026-10-01 (the-gala run, the most recent completed fold)

244 items banked, 23 confirmed (22 unique), 1 unconfirmed (KVarN), 5 steal cards
(`frontier_olm_2026-10-01/DIGEST.md`). Confirmed finds that are now estate baseline, with
register rows at :57-85: transformers runs llama.cpp GGUF quants natively (rows 1, 3);
Ollama 0.35 typed decision models Nimble/Tev1 at a claimed 91 ms/decision (row 2); Ling-3.1-flash
~560B/25B-active release radar (row 6); dynamic abliteration engram steering (row 4); refusal
falls 98.0 to 80.5 pct under KV compression while classifier refusal holds (arXiv 2609.31678,
row 19); fold conduct tracks model date not vendor (2609.25447, row 20); llama.cpp cross-tenant
state-restore flaw, 200/200, plaintext prompts in allocator memory (2609.18526, row 21); the
61-day context-reach instrumentation, 96.6 pct compaction removal, ~11 pct worst-event reach
(r/LLMDevs 1wu24sc, rows 13); vLLM tool-schema key-order cache invalidation, 78 to 95 pct
cached share; prompt-caching economics (1wug1mo, row 16); judge-panel laws (Ising aggregation
9-14 pct, 2609.12002 three-family panel, DeepSWE imagined-grader reward hacking naming GLM 5.3,
HoneyBench); HiveMind AIMD backpressure 72-100 pct vs 0-18 pct failure (2604.17111); small-model
debate loses to self-consistency (2609.35875); MemCodex pointer-beats-inline 60.8 vs 55.4
(2609.39765); TAGGRAPH loses to BM25; mem0 flattens progressive phrasing (2609.36457); EMIR2
SUPERSEDES/CONTRADICTS/SUPPORTED_BY edges (2609.32584).
Five steal cards with $0 probes are specced and ordered at :122-128: reach-ratio meter,
abliterate-probe judge channel, E3b runtime parity, Ollama 0.35 systemone port, KV degradation
ladder. KVarN (arXiv 2606.03458) stays UNCONFIRMED and its llama.cpp kv-rotation clause is
UNSOURCED, do not repeat it (:109-115). Queued from that fold: append 2606.03458 to
`memory/runs/corpus_gap_research/ARXIV_REGISTER.json`; fetch the theneurondaily GLM tok/s
article before acting on 380/790 numbers (confidence 0.55) (:117-121).

**Janitor verdict already ruled twice:** KEEP gemma:2b/gemma4, in both the 09-30 window
(`frontier_olm_2026-09-30/DIGEST.md:18`) and the 10-01 window
(`frontier_olm_2026-10-01/DIGEST.md:9`). Do not re-litigate without new measured evidence.

**Door degradation already mapped:** reddit primary doors walled in all prior reddit lanes
(Welcome shell / 403 / 302 to login `reason=lor2`), working fallbacks PullPush,
arctic-shift.photon-reddit.com, redlib mirrors, serial WebSearch site:reddit.com; X long-form
article path 404s (`frontier_olm_2026-10-01/DIGEST.md:21,89-96`). Rediscovering this costs a
lane for nothing.

## 3. Other carrier dirs active in the 09-30 to 10-02 window (what each already banked)

- `48h_synth/` (09-30, ERRATA 10-02): `STORY.md` is the receipt-backed 48h narrative
  (drain, 2,568-passing green suite, mine died twice and went daily); `steals.md` is the
  ranked EV-per-cost steal menu folding the olm cards plus ABLITERATUS and the grok-4.7
  luncheon run (`48h_synth/steals.md:1-25`); chapters lattice/laws/measure/next.
- `salon_mine/` (10-02): 16 m-file mines of the operator's salon transcripts (SALON-Salon,
  cognition-salon, astra-moonshot, traj); method = line-cited extraction of research questions
  and briefs (`salon_mine/m01.md:1-19`). Per `ouroboros/holdings-of-fleet.md:21` its 105
  citations are 0 pct held: the sources are desktop transcripts, the mines are the only copy.
- `model_garden/` (10-01/10-02 night): `DUMB_AGENT_FRONTIER_DIG.md` (tools+scaffold beats
  scale strongly; small-model-with-tools wins only in narrow regimes; MCP-Bench S7 verdict
  table); `MATING_LIT_SWEEP.md`, `MCP_LATTICE_5W.md`, `DEEPSEEK_API_DOSSIER.md`,
  `ARCHEOLOGY_WAVE1.md` (core vocabulary minted in one 48h window 2026-03-02/03), GRID run
  receipts, `NIGHT_CLOSE.md` running fold (`model_garden/NIGHT_CLOSE.md:1-50`).
- `spiking_wide/` (10-01): SpikingBrain-7B primary dig with the exact TTFT table (7.3x at 256k
  to 26.5x at 1M seq on H100s, `spiking_wide/spikingbrain-deep.md:9-20`), plus neuromorphic
  hardware, non-NVIDIA stacks, upcycle economics, energy frontier, linear-family cards.
- `ractor50/` (10-01): eight retro chapters mining the gala's own wrong verdicts for instrument
  shape; the defect-class table (ok:true-equals-landed, hand-copied count, memory-written
  citations, nine more) at `ractor50/accuracy.md:8-20`; `MCP_PARITY_R20_20261001.md` verdict.
- `localfirst/` (10-01): seven digs of local-memory projects (RAG-OS cloned and probe-run,
  AIDA, Atlas, LBrain, OwnMem, PAM, ragos), e.g. `localfirst/ragos.md:1-15`.
- `librarian_exp/` (10-01): the librarian expedition; cited-but-missing sweep extracted 205
  citation rows from the last-48h receipts and tested holdings against the 691,789-row catalog
  (`librarian_exp/cited-missing.md:1-18`); 61 primaries healed; foundational-gaps and
  instrument-audit cards; 197KB inventory.
- `gap_analysis_20261001/` (10-01): `GAP_REGISTER.md`, the first estate gap register, ranked
  severity x fill-ease for the next 100M-token job, merged from 8 sibling audits
  (`gap_analysis_20261001/GAP_REGISTER.md:1-30`).
- `hermes_burn/` (10-01/10-02): the paid-judgment burn surface; duel volumes DUEL1/DUEL2 with
  r2 adjudications, A1 antiforgery, A2 duel provenance, C1 censorship cross-family, D1-D3
  doctrine roasts, T1W1/T1W2 windows, and `DAY1_CROSS_RACTOR.md` (cross-file laws over the
  whole 10-01 burn; usage ledger snapshot 179 rows / $29.91 at 2026-10-01T20:12:58Z,
  `hermes_burn/DAY1_CROSS_RACTOR.md:8-12`).
- `ouroboros/` (10-02, newest): `holdings-of-fleet.md` verdict: of 396 unique primaries cited
  by standing workflows in the last 48h, 74 pct do NOT survive offline (293 leak), olm-mine is
  the best large workflow at 75 pct held, salon-mine 0 pct, drop-dig worst at 24 pct
  (`ouroboros/holdings-of-fleet.md:9-24`); plus cadence, cross-gap, cross-ractor,
  description-tri-state cards.
- `gala_20260925/ouroboros/` (10-02): `PRIME_JUDGMENT_20261002.STUB1.md` is a TRUNCATED paid
  glm-5.3-prime run (finish_reason=length, 59,476 prompt / 16,000 completion tokens, $0.3073,
  banked GALA_OUROBOROS_PRIME_JUDGMENT_20261002); it is an OWED re-ask, not a landing
  (`gala_20260925/ouroboros/PRIME_JUDGMENT_20261002.STUB1.md:1-11`). Do not cite it as verdict.
- `monitor_lane_selfsteal_20261002.md` (root, 10-02): folded the sibling monitor lane's 10-02
  spool; 3 live needles already claimed with steal plans and falsifiers: CRJudgeBench+Sentinel
  (arXiv 2609.37216, GLM-5.3 judge weakness measured at 76.60 pct minus 6.13), the Socratic
  pressure test (Zenodo 10.5281/zenodo.23049784, execution-verified leak instrument), SPLASH
  (arXiv 2609.37626, mid-run attention-parallelism switching, sglang code public)
  (`monitor_lane_selfsteal_20261002.md:26-75`); the monitor lane itself diagnosed ALIVE-BLIND
  (13h of 0-new polling, dedup fossil, `:79-93`).
- `hermes_burn` neighbor `watch/inbox/STEALTH_SWEEP_LATEST.md` (10-02 13:50Z): free-wall probe
  fired 2, both fails, anchor chore 0 correct (`STEALTH_SWEEP_LATEST.md:1-11`).
- `fillball/` (10-02): the fill-ball receipts (day1-digest backfill, citation-lint, seed-seal,
  percolator candidates, elder salvage, corpus fold).
- `ractor_engine/` (10-02, listed not read), `frontier_olm_2026-09-30` DIGEST backfill
  (10-02 04:12Z, covered in section 2), `handoff/` (ZCode session zip, 10-02).

## 4. Anti-rebank rules for the 2026-10-02 sweep

1. Window discipline: the 10-01 fold preferred 2026-09-01 to 2026-10-01. New confirmed finds
   must be post-10-01 or carry a genuinely new primary (new arXiv id, new thread id). Anything
   in section 2's tables is banked; overlap must be stated, not silently re-confirmed.
2. Same 8 areas x 4 doors ran three times (09-28, 09-30, 10-01 windows). Differentiation lives
   in: new doors (none were added), deeper reads of the 10-01 unread leads (six X article
   bodies 404'd; the OWED list at `frontier_olm_2026-10-01/DIGEST.md:105-106` names full texts
   never pulled), or new areas entirely.
3. Known dead ends, do not rediscover: Lightning/Chutes/SiliconFlow/Scaleway free credits
   (fully dead); KVarN's llama.cpp clause (unsourced); the day-1 unconfirmed trio evidence
   (unrecoverable, refetch instead); Ollama 0.35's unpublished 13-dataset benchmark; nine
   HebrewBooks wrong-book closures.
4. Queued actions still open from 10-01: KVarN register append (one line, zero spend); the
   theneurondaily tok/s fetch; the olm-x free-rung probe before its Oct 7 close
   (`frontier_olm_2026-10-01/DIGEST.md:117-121`, `frontier_olm_2026-09-30/DIGEST.md:83`).
   Firing these beats re-mining their subjects.
5. The burns ledger (`memory/burns/LEDGER.jsonl`) is silent since 09-28T17:15Z. If this week's
   lanes were supposed to bank there, that is a drift to flag, not a fact to paper over; until
   then the carrier dirs in section 3 are the only mining record.
6. Counts law: every count above is instrument-tagged (ledger line, digest section, register
   row). Do not difference counts taken by different instruments at different moments.
