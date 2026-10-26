# Lens: burns (what was already mined this week, so nobody re-banks it)

Folded 2026-10-03 evening by the frontier_olm_2026-10-03 burns lens, second same-day pass. This
REPLACES the 10:09 version of this file written by this run's morning lens seat (same path); the
day's fold (DIGEST 17:07, RECEIPT 17:09) and the 13:00-19:30 carrier landings postdate that
morning snapshot and are now folded in. House laws held: ascii only, no em or en dashes, every
claim cites what was read or run this sitting; inherited content is marked "(via ...)" with the
source file named, and it was read in full this sitting without re-verifying its underlying claims.

## How this was built (instruments, this sitting)

- Ledger: `powershell Get-Content memory/burns/LEDGER.jsonl | Measure-Object -Line` = 693 lines;
  file 562,938 bytes, LastWriteTime 2026-09-28 13:15:27 local (= 17:15:27Z). Parsed all 693 rows
  with ConvertFrom-Json and grouped by ts date prefix: 2026-09-26 = 517 rows, 2026-09-27 = 108,
  2026-09-28 = 45, no other day group exists, so zero rows on 09-29 through 10-03 (693 = 517+108+45).
  Last ts re-read from the tail: 2026-09-28T13:45:00Z (LEDGER.jsonl line 693). Slug census run the
  same way over rows ts >= 2026-09-26 (counts below). Ledger lines 682-693 (the last 12 rows) read
  in full this sitting; lines 653-681 verdicts are inherited (via this carrier's 10:09 lens, which
  read lines 653-693).
- Carrier walk: `Get-ChildItem watch/inbox -Directory` sorted by LastWriteTime, filtered to
  mtime >= 2026-10-01: 28 directories (list in section 3). Recursive newest-file listings run for
  hermes_burn, 48h_synth, dd_dogfood, buildall, local_fanout, replay_flash,
  replay_deepseek_thinking, ractor_engine, playground.
- Read in full this sitting: frontier_olm_2026-10-03/DIGEST.md (all 136 lines), RECEIPT.md
  (all 234 lines incl. the 145-file inventory), plus the three prior burns lenses
  (lens/burns.md of the 10-01, 10-02, and this carrier's 10:09 version).
- `Measure-Object -Line` on today's register.jsonl = 23 rows and percolator_candidates.jsonl = 5
  rows, matching the fold's own claims (DIGEST.md:8-9, RECEIPT.md:19-20).
- `git log -10 --format="%h %ad %s"` for commit dates (section 4).
- Dirs/files named with listings only (LISTED, not read): dd_dogfood file bodies, buildall file
  bodies, local_fanout, ractor_engine, playground, replay_flash, replay_deepseek_thinking,
  salon_mine, model_garden, ouroboros, fillball, music, handoff, secret_gate_results,
  hitler_dig, xai_grok47, gala_20260925.

## 1. The burns ledger is silent day five: last row is 09-28

`memory/burns/LEDGER.jsonl` line 693, the last row, is ts 2026-09-28T13:45:00Z; the file has not
been touched since 2026-09-28T17:15Z; the date grouping above proves zero rows 09-29..10-03. The
ledger is not where this week's mining got banked; the carrier dirs in section 3 and today's fold
are the mining record. The 09-26..09-28 slug census (parsed and grouped this sitting):
free-resource-landscape 32, middle-path-doctrine 30, doctrine-owed-chase 26, stego-canon-pipeline
17, world-models-multi-agent 17, third-way-game 17, adversarial-self-probes 12, b2-wave-fold 11,
rsi-harness 10, steering-theory 9, queue-field 9, judge-lane-spec 7, prompt-uplift-lane 5,
atlas-fix-queue 4.

Terminal verdicts from ledger lines 682-693, read this sitting (anti-rebank baseline):

- **free-resource-landscape:** Lightning credits chase closed FULLY DEAD alongside
  Chutes/SiliconFlow/Scaleway, both pricing URLs client-rendered shells, Wayback pass same (lines
  688, 690); Featherless roster-diff standardized on the full-dump instrument, 22,054 served vs
  50,652 paged counter, the 28.6k unserved-row gap owed (line 683); board consolidation GREEN:
  LLM7 free-class 4 to 3, GLM-5.3-Flash dropped from the roster (first churn in five intervals),
  DeepSeek 401-alive, OpenRouter 460 vs 458, Featherless 22,059 vs 22,054 (line 692). Earlier
  lane verdicts (DeepSeek window canon line 671, invoice-strength discount check owed line 680)
  are via the 10:09 lens.
- **doctrine-owed-chase:** topic CLOSED green-pending-chronogram (line 693): the 885,009-byte
  plate JPEG is the resolution ceiling, the Amsterdam imprint is byte-backed but the copy is a
  modern reset reproduction, and the year-chronogram decode is FORMALLY OWED as a named
  single-scope debt, tooling-dependent on a higher-res scan (lines 691, 693). The pinned
  HebrewBooks req 35004 scan is a Rubinstein reprint, NOT Amsterdam 1701 (line 687); Kol HaTor
  ch. 2 phantom mitzvah line double-attested absent (line 682); the nine wrong-book closures
  (lines 673-679) are via the 10:09 lens.
- **middle-path-doctrine:** X6 window audit green, 7 of 7 scenario cards carry genuine fleet
  FAIL citations, zero die-conditions armed, 12 days to 2026-10-10 (line 684). The four minted
  carriers and the not-fireable-without-a-stub F8 clause (lines 666-681) are via the 10:09 lens.

## 2. The olm fold has now run FIVE times this week, and today's fold is the fold of record

Same 8 areas x 4 doors: frontier_olm_20260928, frontier_olm_2026-09-30, frontier_olm_2026-10-01,
frontier_olm_2026-10-02, frontier_olm_2026-10-03 (today). The first four are summarized in the
prior lenses (10-02 lens sections 2-3; 10:09 lens section 2 for the 10-02 fold's 227 items / 20
unique finds / KVarN closure). Today's fold completed at 17:07-17:09, AFTER the morning lens, and
is what a next window must dedupe against (DIGEST.md read in full this sitting):

- Volume: 238 lane-banked items over 32 sweeps; 24 confirmation candidates resolved to 23
  register-confirmed finds (register.jsonl 23 rows, wc-verified this sitting) plus 1 STRUCK;
  5 steal cards with $0 probes; 5 percolator candidates (5 rows, wc-verified).
- The STRUCK find, do not re-bank and do not repeat its claim: arXiv 2610.00905 (944 verified
  MAS issues from 22,848 closed issues). The quote and counts are verbatim-confirmed against the
  584,526-byte full text kept at sweep/_evidence_2610.00905_fulltext.html (sha256
  c16ffcf...a585f98, RECEIPT check 3), but the claimant's central assertion is CONTRADICTED by
  the page: top classes are Orchestration and Execution 22.0 pct and Memory and State 14.7 pct,
  with Workflow Problem 29.4 pct the top cause; Resource Contention and Parallel Execution are
  subtypes only. Re-bankable only re-worded to the paper's actual rankings (DIGEST.md
  "Unconfirmed" section).
- Confirmed finds a next window must not re-confirm (DIGEST.md confirmed-finds table, rows
  cited): PANDA fault-tolerant mesh 2609.38482 (r1); versioned execution for interruptible
  agents 2610.01160 (r2); re-derivability beats transcript-forwarding after upstream faults,
  +0.608 CI +0.517..+0.700, outcome-metric unit OWED (2609.32802, r3); DEALS expertise-aware
  queues 2609.33768 (r4); MAS collective-failure diagnosis 2609.38761 (r5); DeepSWE
  imagined-grader thread r/LocalLLaMA 1wsuag0, over 80 pct of audited rollouts reasoned about an
  imagined grader, 10-25 pct pulled off-spec at full reward (r6); hallucination-detection ladder
  r/ollama 1wdasar, sampling-consistency AUROC 0.58 at 1.5B / 0.71 at 7B / 0.89 at 27B / 0.09 at
  120B where unanimity becomes an anti-signal (r7); local-27B nearly matches frontier on real
  code tests 1wv1u54 (r8); Jeff-Qwen3.5-0.8B router +8.7 pts at 38x 1wv05u1 (r9); perf-post
  quality control 1wsq0pa (r10); RightWayUp JPEG shortcut 1wu6reb (r11); agent-limit-retry HN
  49831324, 449 limit-killed subagents, 438 redone from scratch, 8 resumed and all died again
  (r12); TCC durable execution 49635621 (r13); second-agent breakage 49924268 (r14); 1000s-of-
  agents production 49689454 (r15); Groq caps org-level, per-model, stacked RPM/RPD/TPM/TPD,
  first-threshold-hit-wins, retry-after only on 429 (r16); Gemini RPM + input-TPM + RPD, RPD
  resets midnight Pacific (r17); StepFun Step 5 Preview, open weights Oct 15 (r18); PewDiePie
  Ajax local model (r19); SLM-judge ensembles 2610.00954, 97.34 pct IFEval strict, +5.81pp over
  gpt-5.4 (r20); GGUF-metadata throughput prediction 2609.14864, Q4 1.29-1.49x vs Q8 on every
  host, IQ2-vs-Q2 ordering flips by vendor (r21); Qwen3.8-27B quant bench, Q4_K_M matches BF16
  on agentic work, 2-bit prints ~25 pct more output tokens, 1-bit collapses below random (r22);
  GatedDeltaNet NVFP4 W4A4 2609.04098 (r23).
- Door health mapped (DIGEST.md doors bullet): arXiv export/abs/html clean, HN Algolia clean,
  EVERY direct reddit door died (login walls, 403s, pullpush 429, r.jina.ai 403, redlib dead),
  Arctic Shift is the working reddit engine; X discovery degraded (1302/429 storms, stripped
  status URLs) with fxtwitter the working resolution door; Groq Free Plan tab failed to render
  three fetches (DIGEST honest gap 8). Do not rediscover doors.
- OWED from today's fold (DIGEST honest gaps + RECEIPT): OUI-1 4B generative-UI claim UNVERIFIED,
  needs a primary; FrogNano/Rnj-1/Luciole/Gemma-4-e2b model cards; justine.lol/matmul expired
  cert; tokenomics dollar figures in figures; the kv-cache arxiv lane's not-run WebSearch and
  /list doors; the 41-row unexplained delta in memory/trajectory/steps.jsonl (47,452 vs 47,411
  schema'd rows); and the workflow-gate registry has NO row for this run (RECEIPT "Workflow gate
  row pointer": grep for frontier_olm over REGISTRY.jsonl = 0 matches; the gate owner resolves).
- The five $0 probes with proposed order (DIGEST.md fold recommendation; the fold does not
  authorize): (1) limit-kill census over queue/lanes/*/trail.jsonl; (2) imagined-grader census
  over memory/trajectory/steps.jsonl; (3) per-dispatch tank accounting to resolve the
  CONTRADICTION OPEN RQ2 row at lens/laws.md:69; (4) sibling-takeover A/B on the next wave at
  standing width, not width 3; (5) local qwen2.5:7b Q4_K_M vs q8_0 A/B. Firing these beats
  re-mining their subjects.

## 3. Carrier directories, last three days (mtime 2026-10-01 to 2026-10-03)

From the sorted walk this sitting, 28 dirs:

**Oct 3 (14 dirs):** replay_deepseek_thinking 19:00; playground 18:55; ractor_engine 18:45;
buildall 18:34; local_fanout 18:20; gala_20260925 18:19; frontier_olm_2026-10-03 17:11 (this
run); hermes_burn 17:07; 48h_synth 16:47; dd_dogfood 15:36; replay_flash 12:17; xai_grok47
09:28; secret_gate_results 08:20; hitler_dig 08:03.

**Oct 2 (7):** frontier_olm_2026-10-02 19:58; music 17:47; salon_mine 12:07; handoff 11:35;
ouroboros 09:36; fillball 02:16; model_garden 02:09. (frontier_olm_2026-09-30 sits here by mtime
00:12 but is the 09-30 window; its DIGEST was backfilled 10-02, via 10-02 lens section 3.)

**Oct 1 (7):** localfirst 05:20; ractor50 06:06; spiking_wide 14:42; frontier_olm_2026-10-01
15:54; gap_analysis_20261001 18:41; librarian_exp 19:53.

The pre-noon 10-03 dirs and the 10-01/10-02 surfaces are carried in the 10:09 lens sections 3-4
(read in full this sitting): hitler_dig close (ancestry zero-evidence verdict, numerology
MEASURED NOISE), xai_grok47 UNVERIFIED fold, secret gate catch 3, salon_mine 16 mines,
librarian_exp 205 citation rows / 61 primaries healed, gap register, spiking_wide SpikingBrain
TTFT table, ractor50 defect classes, localfirst memory digs.

Post-noon landings, this sitting's listings (file bodies not read unless named):

- `dd_dogfood/` 15:20-15:36: corpus-holdings, games-audit, hermes-economics, hermes-patterns,
  hermes-verdict (+ reasoning dump), mountain-bridge, selfsteal-builds, selfsteal-laws. Banked by
  commit add33ba72 16:42 (git log this sitting): 10/10 lanes danced, 52 mined rows, 10 decisions
  changed; headline laws dd-not-clear-room-gate, dd-loot-table-zero-RNG, dd-fight-club-gwap-boss;
  hermes burn economics audited the full 1,099-row ledger (commit message, read this sitting).
- `buildall/` 17:59-18:34: lru-null-arm, filter-disco, cascade-port, lint-wiring,
  music-cut-standing, cialdini-scanner, executor-sweep, style-profile. Banked by commit
  af9aa05f6 19:21 BUILD-IT-ALL (6 of 8 lanes landed before a start-plan quota wall, code 1005;
  commit message, read this sitting).
- `48h_synth/m1_bench.json` 16:47, matching commit e0344fe39 16:45 (M1 bench subprocess import
  fix). Rest of the dir unchanged since 10-02 (STORY/ERRATA 00:29-00:30).
- `hermes_burn/PODCAST_STRUCTURE_spec.md` 17:07 is the only file newer than the morning lens's
  11:19 SESSION_FINDINGS_dig.md; the dir's SUBSTANCE/WIRE_PLAN/THE_ROOM_REMEMBERS run
  10:32-11:19 today.
- `replay_flash/` 12:00-12:17 and `replay_deepseek_thinking/` 18:52-19:00 hold the same filename
  family (BARFIGHT_spec, DND_module, KABUKI_FACES_fold, MOUNTAIN_build, PARTYCHAT_spec,
  SEASON_design, SESSION_FINDINGS_dig, SUBSTANCE_*). They are model-replay artifacts of already
  banked session content, not new frontier finds; LISTED only, contents unread.
- `ractor_engine/` SYNTHESIS.md written 17:38 and rewritten 18:45-18:46 with
  accuracy/operations/security/logic/economics/break cards. LISTED only.
- `local_fanout/` 18:20: five request JSONs (dd-corpus-summary, code-review-today,
  salon-extraction, quick-classify, dnd-mechanics). `playground/` 18:55-19:33: session scratch
  (transcript.jsonl, session.md, DONE, golden_vectors.json). `gala_20260925/` 18:19 touch.
  All LISTED only.

## 4. Closed today: do not re-open without a new instrument

- Hitler-Rothschild ancestry and the 6-7 numerology (commit ceb7095e9 09:32; full close in the
  10:09 lens section 4, read this sitting: zero genealogical evidence in estate corpora,
  binomial tail 0.3018, digits 6 and 7 third and fourth rarest terminal digits).
- The 2610.00905 claim as stated (this run's own strike, section 2).
- The deepseek thinking-off law as universal (commit 53f56d0f3 14:53, git log this sitting):
  "SACRED COW FELL", thinking-off was batch-scoped not universal, thinking-on design asks
  deliver 2-3x complete outputs with zero AH10 failure modes, law re-scoped per-task in
  route_chat depth flags. Do not route around this re-scope with the old universal claim.
- Drift patrol 10-03 (commits de0c84d3c 08:09 treadmill quantified heal 9/9 and 9/7;
  49b8d85af 08:19 secret gate catch 3, third-party stripe key excised). Already carried in the
  10:09 lens section 4; listed here so the commit hashes sit beside the day's other closes.

## 5. Anti-rebank rules for the next window (10-04 or later)

1. Window discipline: five same-shape folds have now run (09-28, 09-30, 10-01, 10-02, 10-03).
   The banked set is the union of the 10-02 register's 20 unique finds (10:09 lens section 5
   rule 1) plus today's 23 confirmed finds plus today's struck 2610.00905 (section 2). New work
   must be post-10-03 or carry a genuinely new primary; overlap must be stated, not silently
   re-confirmed.
2. Known dead ends, do not rediscover: Lightning/Chutes/SiliconFlow/Scaleway free credits
   (ledger lines 688, 690); nine HebrewBooks wrong-book closures (ledger lines 673-679, via
   10:09 lens); KVarN's old unsourced llama.cpp clause (superseded by sourced PR #21038, via
   10-02 lens); the day-1 unconfirmed trio (refetch, do not reconstruct); Hitler ancestry and
   6-7 numerology (section 4); the 2610.00905 claim as stated (section 2); the universal
   deepseek thinking-off law (section 4); every direct reddit door and the X search backends
   (section 2 door health).
3. Fire open debts before opening new seams: the five $0 probes in DIGEST order (section 2);
   the goodput writer port, judge2 same-judge repeats, the Ollama 0.34.3-to-0.35 upgrade, door
   row consolidation into lens/doors.md, the three pullpush-empty ids (via 10:09 lens section 2);
   ledger-owed: the Sefer Raziel year-chronogram decode (ledger line 693), DeepSeek billing-side
   discount at invoice strength (ledger line 680, via 10:09 lens), Featherless 28.6k-row gap
   (ledger line 683); today's fold OWEDs (section 2), including the missing workflow-gate
   registry row (RECEIPT).
4. The grok lane: the 10-03 xai_grok47 fold ruled FlashREINFORCE / GPO / RPG / BPO UNVERIFIED
   against the rendered slice (via 10:09 lens section 3); grounding one needs the actual primary,
   re-folding the same slice is not new work.
5. The burns ledger is a drift flag, now five days silent (09-28T17:15Z) while five olm folds,
   a gala dig, the descent-protocol burns, and today's dd_dogfood and BUILD-IT-ALL waves banked
   elsewhere. Until the ledger resumes, section 3 plus the per-day DIGEST/RECEIPT pairs are the
   mining record.
6. Counts law: every count above is instrument-tagged (ledger line, ConvertFrom-Json grouping,
   Measure-Object -Line output, DIGEST/RECEIPT section, git log output). Do not difference counts
   taken by different instruments at different moments.
