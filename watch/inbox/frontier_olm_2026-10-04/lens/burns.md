# Lens: burns (what was already mined this week, so nobody re-banks it)

Folded 2026-10-04 morning by the frontier_olm_2026-10-04 burns lens. House laws held: ascii only,
no em or en dashes, every claim cites what was read or run this sitting. Inherited content is
marked "(via ...)" with the source file named, and that file was read in full this sitting without
re-verifying its underlying claims. This lens is the successor to frontier_olm_2026-10-03/lens/
burns.md (the evening version, read in full this sitting) and it discharges that fold's gap 15:
"mirroring register rows 24-42 into lens/burns.md is owed to the lens owner" (via
frontier_olm_2026-10-03/DIGEST.md:238).

## How this was built (instruments, this sitting)

- The ask's named read: `powershell Get-Content memory/burns/LEDGER.jsonl -Tail 40` = the last 40
  rows (ledger lines 654-693), all four slugs, read in full; row-level claims in section 2 cite
  their ledger line numbers.
- `(Get-Content memory/burns/LEDGER.jsonl).Count` = 693 rows; `-TotalCount 1` first ts
  2026-09-25T10:05:50Z; tail's last ts 2026-09-28T13:45:00Z (line 693); `Get-ChildItem memory/burns`
  shows LEDGER.jsonl LastWriteTime 2026-09-28 13:15 local and verdict_enum_map.json 2026-09-30
  08:30 local (section 1).
- Carrier walk: `Get-ChildItem watch/inbox -Directory | Sort-Object LastWriteTime -Descending`
  (section 4, all mtimes mine this sitting).
- Read in full this sitting: frontier_olm_2026-10-03/DIGEST.md (all 274 lines, including the
  Round 2 fold section at :140-274), frontier_olm_2026-10-03/lens/burns.md (all 219 lines),
  frontier_olm_2026-10-02/DIGEST.md (head, lines 1-40), and this carrier's sibling lenses
  lens/corpus.md and lens/graph.md.
- Counts verified by hand this sitting: frontier_olm_2026-10-03/register.jsonl = 42 rows;
  frontier_olm_2026-10-03/percolator_candidates.jsonl = 9 rows; memory/runs/hermes_burn/usage.jsonl
  = 2,497 rows (moment 2026-10-04 ~14:30Z; the round-2 fold's 1,275-row read is an earlier moment,
  via DIGEST.md:164; the growth between the two moments is not attributed here per the counts law).
- `git log -12 --format='%h %ad %s'` for today's landed commits (section 5).
- Dirs/files LISTED only (names + mtimes, bodies unread): go_wave_20261004, night_shift_20261004,
  social_rsi, replay_grok47, reboot_patches_20261003, replay_flash, replay_deepseek_thinking,
  secret_gate_results, gap_analysis_20261001, ractor_engine, playground, hermes_burn (newest file
  PRIMER_capture_spec.md 10-04 05:42 local).

## 1. The burns ledger is silent day six

`memory/burns/LEDGER.jsonl` holds 693 rows spanning 2026-09-25T10:05:50Z (line 1) to
2026-09-28T13:45:00Z (line 693); file untouched since 2026-09-28 13:15 local. The 10-03 lens
grouped all 693 rows by day: 09-26 = 517, 09-27 = 108, 09-28 = 45, zero rows 09-29 onward (via
frontier_olm_2026-10-03/lens/burns.md:15). One nuance this sitting adds: `memory/burns/
verdict_enum_map.json` was written 2026-09-30 08:30 local, two days after the ledger's last row,
so burns tooling was touched after the ledger went dark without minting a new row. The 09-26..09-28
slug census (free-resource-landscape 32, middle-path-doctrine 30, doctrine-owed-chase 26,
stego-canon-pipeline 17, world-models-multi-agent 17, third-way-game 17, adversarial-self-probes
12, b2-wave-fold 11, rsi-harness 10, steering-theory 9, queue-field 9, judge-lane-spec 7,
prompt-uplift-lane 5, atlas-fix-queue 4) is via frontier_olm_2026-10-03/lens/burns.md:41-44.
Until the ledger resumes, the carrier dirs (section 4), the per-day DIGEST/RECEIPT pairs, and
memory/runs/hermes_burn/usage.jsonl are the mining record.

## 2. The tail (ledger lines 654-693, read in full this sitting)

The last 40 rows are all 2026-09-28, four slugs: free-resource-landscape 14, doctrine-owed-chase
12, middle-path-doctrine 11, world-models-multi-agent 3 (counted this sitting from the tail read).
Verdict mix: steal 31, vacuous 5, green 3, built 1; fresh_failure_mode true on 5 rows. Line numbers
below are ledger lines (tail row N = line 653+N, mapping confirmed against the 10-03 lens's own
citations for lines 680, 687, 691, 692, 693). Terminal anti-rebank verdicts:

- **doctrine-owed-chase: topic CLOSED green-pending-chronogram (line 693).** Sefer Raziel
  Amsterdam 1701: the archive.org plate JPEG (885,009 bytes) is the resolution ceiling; the
  Amsterdam imprint is byte-backed but the copy is a modern reset reproduction; the year-chronogram
  decode is FORMALLY OWED as a named single-scope debt (lines 691, 693). The pinned HebrewBooks req
  35004 scan is a Rubinstein reprint, NOT Amsterdam 1701 (line 687). Nine wrong-book closures are
  behind it (lines 673-679, via the 10-03 lens). Do not reopen without a higher-res scan.
- **free-resource-landscape: board consolidation GREEN (line 692).** Lightning credits lane closed
  FULLY DEAD alongside Chutes/SiliconFlow/Scaleway, both pricing URLs client-rendered shells, the
  Wayback pass the same shell (pass l line 688, pass m line 690). Live state: LLM7 free-class 4 to 3,
  GLM-5.3-Flash dropped from the roster (first churn in five intervals), DeepSeek 401-alive and
  inference-proven 11:04Z in-window with the 50 percent discount check owed at invoice strength
  (line 680), OpenRouter 460 vs 458, Featherless 22,059 vs 22,054.
- **middle-path-doctrine: X6 window audit green (line 684).** 7 of 7
  scenario cards carry byte-verified fleet FAIL citations, zero die-conditions armed, 12 days to
  2026-10-10. F8 (game-class clause) re-armed but NOT fireable without a gated MUD stub build, and
  the stub has no factions, no sentiment, no VM pool, no gift channel (lines 678, 681). Four
  restatement carriers minted across the week (lines 660-675, via the 10-03 lens).
- **world-models-multi-agent: green (line 662, ts 01:20:10Z).** research seat fix landed
  (run_trail.py:61 _SEAT_MAP); falsifier is one real research-seat run post-restart minting
  seat=research in related_runs.jsonl; nothing restarted at ledger time.

## 3. The olm fold: SIX runs this week; the 10-03 carrier now holds round 1 plus round 2

Same 8 areas x 4 doors: frontier_olm_20260928, 2026-09-30, 10-01, 10-02, 10-03, and today's
2026-10-04 carrier (this run). The 10-03 DIGEST was appended 2026-10-04 by the night seat with a
Round 2 fold (DIGEST.md:140-274, read in full this sitting): 227 round-2 lane-banked items, 19
confirmed finds as register rows 24-42 (18 new; row 38 deep-reads round-1 row 23's paper), 5 held
unconfirmed, 4 more steal cards (9 total), percolator rows 6-9. Register now 42 rows / 41 distinct
finds, percolator 9 rows, steal 9 cards (counts re-verified this sitting). Do not re-confirm
round-1's 23 finds (list at frontier_olm_2026-10-03/lens/burns.md:86-106, read this sitting) nor:

- **Round-2 confirmed finds, register rows 24-42** (DIGEST.md:196-216): 2609.17848 LoRA-SFT
  tool-calling default; 2610.02206 KaliBench; 2609.39450 ActionGuard; 2609.38712 long-horizon
  context drop 62.8 pct; 2610.00890 GSPO cross-benchmark transfer; 2610.01950 MoE-CORE; reddit
  1wkorli IQ3_XXS vs ternary PQ2 (ternary 3.02x slower, 3.10x more tokens); 1wjnklv bonsai
  headline vs ~75 pct retained whitepaper; 1wgvfpr dan-Luu-style self-judge exercises; 1wefk8o
  grader-separate harness rewrite; 1wavhij OpenUI SFT-worse/self-training-fix (13 to 57.1 pct);
  1w7umnd MQL5 1 to 92.39 pct compile; HF OpenBMB/MiniCPM5-2B (behind UNPROVEN gate); 2609.39801
  RATIO W3 CoT inflation 2.94-3.77x; 2609.04098 GDN NVFP4 deep read; quesma.com transcripts-are-
  precious (91 vs 43 pct with AGENTS.md); ollama v0.35.1 release notes; Featherless paged roster
  live interval (+471); 2609.38169 STEPQuant recurrent-state pool.
- **Round-2 UNCONFIRMED, held out of the register, do not re-bank as fact** (DIGEST.md:240-265):
  the "Ollama 0.35.1 3.2x janitor regression" claim (quote not on the cited page, estate-side
  numbers, upgrade HELD pending clean re-measure); "Featherless roster halved in five days"
  (falsified by re-run, 22,122 rows stable, consistent with truncated downloads); "LLM7 churned 64
  to 68" (live roster reads 64, churn contradicted); TTPO test-time training (archive-confirmed
  substance, page standard not met); the OUI-1 Apache-to-Gemma license-flip quote (absent from the
  recovered thread).
- **Door health, two passes certified** (DIGEST.md doors bullet + :166): every direct reddit door
  dead, Arctic Shift archive API is the working reddit engine (re-certified by four lanes), new
  working variant = thread permalinks via .rss endpoints; X discovery degraded (1302/429 storms)
  with fxtwitter resolution alive; arXiv doors clean; WebSearch intermittently rate-limited.
  Do not rediscover doors.
- **Probe ledger after round 2** (DIGEST.md:267-274): probe 1 (limit-kill/salvage census) FIRED,
  its fewer-than-5 branch fired at workflow-child level, so steal cards 4 and 5 are DEFERRED as
  instrumented until a death-event writer exists (26 fatal rows, zero resumed, zero code-1005 trail
  rows, DIGEST.md:227). Probes 3 (per-dispatch tank accounting, must count requests: both hot free
  doors expose zero rate-limit headers) and 5 (qwen2.5:7b Q4_K_M vs q8_0 A/B) re-owed UNRUN. Probes
  2 (imagined-grader census) and 4 (takeover A/B) unchanged. Proposed next order: judge noise-floor
  census (percolator row 9), reasoning-quant ladder (row 7), KaliBench janitor grading (row 6),
  continuity exporter census (row 8). Firing these beats re-mining their subjects.
- **Estate telemetry split found and priced** (DIGEST.md:164, via the round-2 fold): burns LEDGER
  silent since 09-28 while the hermes usage ledger logged 1,275 rows over three days with 888 of
  the newest day carrying a doubled-key flag; verdict was telemetry break, not a spend stop. This
  sitting the same instrument reads 2,497 rows; growth since that read is real but unattributed
  here (counts law).

## 4. Carrier directories, last three days (mtime 2026-10-02 to 2026-10-04, my walk this sitting)

**Oct 4 (14 dirs):** playground 10:21; frontier_olm_2026-10-04 10:21 (this run; lens/ holds
corpus.md, graph.md, and this file); go_wave_20261004 09:13; reboot_patches_20261003 08:34
(APPLY_ORDER.md + 01_janitor_limits.diff + 05_verkle_lock_namespace.diff newest, LISTED);
ractor_engine 08:33; secret_gate_results 08:13; replay_flash 07:06; social_rsi 06:53 (BUILD_
RECEIPT.md + draft_errno22-cage-writes.md + 3 packet_* files, LISTED); replay_deepseek_thinking
06:48; replay_grok47 06:30; hermes_burn 05:42 (newest PRIMER_capture_spec.md); night_shift_20261004
05:27 (estate_index_compaction_des..., quantized_lattice_fold.md, verkle_vs_embedding.md,
worldline_compact_tool.md, LISTED); gap_analysis_20261001 05:13; frontier_olm_2026-10-03 04:05
(the round-2 append this lens folds).

**Oct 3 (7):** buildall 18:34; local_fanout 18:20; gala_20260925 18:19; 48h_synth 16:47;
dd_dogfood 15:36; xai_grok47 09:28; hitler_dig 08:03. Characterizations are via
frontier_olm_2026-10-03/lens/burns.md:129-172 (read this sitting): dd_dogfood 10/10 lanes, 52
mined rows, banked commit add33ba72; buildall 8 work items, banked af9aa05f6 (6 of 8 landed before
a quota wall); 48h_synth m1_bench + STORY/ERRATA; hermes_burn podcast/room specs; replay_* dirs are
model-replay artifacts of already banked session content, not new frontier finds; ractor_engine
SYNTHESIS.md with six card classes.

**Oct 2 (8):** frontier_olm_2026-10-02 19:58 (fold of record for 10-02: 227 items, 23 register rows
/ 20 unique finds, 9 steal cards; via its DIGEST.md:1-40, read this sitting); music 17:47;
salon_mine 12:07; handoff 11:35; ouroboros 09:36; fillball 02:16; model_garden 02:09; and
frontier_olm_2026-09-30 (mtime 00:12 10-02, name-dated 09-30, via the 10-03 lens:136). The
10-02-day dirs salon_mine through model_garden are carried via the 10-03 lens:134-136, 146-153.

## 5. Already banked TODAY (10-04), from git log this sitting: do not re-mine

- `756c78b1b` 10:12 + `9058dc238` 10:25: Schmidhuber compression-progress doctrine trio DROP, then
  FOLD AMENDED on sibling review (severity-vs-curiosity metric confound accepted; "anti-
  Schmidhuber organ" prose withdrawn; staged sqlite+skip-list GO, operator-gated; the "two 3.4GB
  copies" disproven as fsutil hardlinks to one file).
- `a4309aa7c` 10:06: THE EIGHT STONES lens-to-parable mapping + RIB_LENS_STONES_PARABLE; NVIDIA NIM
  LIVE x2 keys 81 models each (morning baseline-0 CLOSED); OneCanvas probe candidate; eFlesh
  sensor intel; WavePixel crank-signature PRESENT.
- `6d7e75aea` 09:52 + `7214ccf0d` 09:45: Beasley Zenodo drops x2 (Three-Body Operator-First, Dirac
  Time), both tri-state UNVERIFIED/OUT-OF-SCOPE, crank-check negative, filed for doctrine rhyme.
- `42452bce6` 09:35: DROP INGEST x5: VERIHARNESS (2610.00972, percolator candidate with
  kill-falsifier), OLMO 3 (not on ollama registry, 404-probed), MTP post-train (no CPU/AMD port),
  AC2 prefix-value, Distillation Dynamics.
- `50d7d45de` 09:24: FREE-SURFACE AUDIT: Cerebras/Groq/Together 403, Google x4 401 at live probe;
  Mistral LIVE 46, Cohere-free LIVE 35 unused; NVIDIA never provisioned then provisioned at 10:06.
- `7e36640c2` 09:07 + `73d16ca21` 09:16 + `acb1a0c1d` 08:36: OpenRouter CSV verdicts (exposure
  window CLEAN, root cause = CRLF .env carrying trailing carriage returns into the Bearer header;
  both keys fully accounted, combined $0.4236) and the 10-04 drift-patrol final seal.
- `993a5977b` 08:36: X intel, proper-scoring-rule decision models (Gero-4B); DIRECT HIT: gwap
  agreement_score is a raw hit-fraction (arena_gwap.py:13); System-1 router drop-in banked.

## 6. Anti-rebank rules for the next window

1. The banked set is the union of: round-1's 23 register finds + round-2's rows 24-42 (both in
   frontier_olm_2026-10-03/register.jsonl, 42 rows verified this sitting) + today's git-logged
   drops (section 5) + the ledger's closed topics (section 2). Overlap must be stated, never
   silently re-confirmed.
2. Dead ends, do not rediscover: Lightning/Chutes/SiliconFlow/Scaleway free credits; nine
   HebrewBooks wrong-book closures; the five round-2 unconfirmed items as stated (section 3); the
   round-1 struck 2610.00905 claim; Hitler ancestry and 6-7 numerology (via the 10-03 lens:175-186);
   the universal deepseek thinking-off law (superseded per-task, via the 10-03 lens:180-183);
   every direct reddit door and the X search backends.
3. Fire the owed probes before opening new seams: round-2 probe order (section 3), the Sefer Raziel
   chronogram decode (ledger line 693), the DeepSeek invoice-strength discount check (ledger line
   680), the Featherless 28.6k-row gap (ledger line 683), the post-10-02 arXiv sub-window re-query
   inside 48 hours of 10-03 (DIGEST.md:228), the OUI-1 primary (DIGEST.md:190, 265), Waggle
   full-text read (DIGEST.md:230).
4. The burns ledger is a drift flag, six days silent. If you bank mining anywhere, either the
   ledger resumes or your DIGEST/RECEIPT pair is the record; do not assume a ledger row exists.
5. Counts law: every count above is instrument-tagged (ledger line, Get-Content Count output,
   DIGEST line, git log output). Do not difference counts taken by different instruments at
   different moments.
