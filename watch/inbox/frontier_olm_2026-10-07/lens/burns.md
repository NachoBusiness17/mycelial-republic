# Lens: burns (what was already mined this week, so nobody re-banks it)

Folded 2026-10-07 midday by the frontier_olm_2026-10-07 burns lens. House laws held: ascii only,
no em or en dashes, every claim cites what was read or run this sitting. Inherited content is
marked "(via ...)" with the source file named; that file was read this sitting without
re-verifying its underlying claims. This lens is the successor to frontier_olm_2026-10-06/lens/
burns.md (read in full this sitting, 217 lines).

## How this was built (instruments, this sitting)

- The ask's named read: tail of `memory/burns/LEDGER.jsonl` lines 640-705 via the Read tool,
  after a PowerShell `(Get-Content ...).Count` read 705 lines, file 571,821 bytes,
  LastWriteTime 2026-10-07 08:09:26 local.
- Max-ts verification run this sitting: PowerShell pipeline
  `Get-Content ... | ForEach-Object { ($_ | ConvertFrom-Json).ts } | Sort-Object | Select -Last 6`
  returned top ts 2026-09-28T19:30:00Z (then 18:30, 18:00, 17:30, 17:00 back).
- Carrier walk run this sitting: `Get-ChildItem watch/inbox -Directory | Sort LastWriteTime
  -Descending | Select -First 40` (section 3); filtered recursive listings of the
  frontier_olm_2026-10-05/06/07 dirs (10-07 was MISSING at the Test-Path probe, this run
  created it); newest-file listings of gauntlet, selfimp, free_lane_queue, hermes_burn,
  ractor_engine, secret_gate_results.
- Read this sitting: frontier_olm_2026-10-06/lens/burns.md in full (217 lines);
  frontier_olm_2026-10-06/DIGEST.md lines 1-75 (provenance, executive summary, steal cards,
  confirmed table).
- `git log --since="2026-10-06 11:00" --format="%h %ad %s"` run this sitting: 43 commits,
  section 2c takes its rows verbatim from that output.
- Not run this sitting: any pytest, any fresh arXiv/HN fetch, any re-verification of the
  day-5/day-6 sweep payloads. This lens folds, it does not confirm.

## 1. Ledger delta: 12 rows landed, then the ledger went quiet again at the same place

The 10-06 lens read 693 rows / 562,938 bytes / max ts 2026-09-28T13:45:00Z (via
frontier_olm_2026-10-06/lens/burns.md:11-14). This sitting the same file reads 705 rows /
571,821 bytes / max ts 2026-09-28T19:30:00Z: rows 694-705 (+8,883 bytes) are appended, all
slug doctrine-owed-chase, ts 2026-09-28T14:00Z through 19:30Z (my tail walk this sitting).
The file's LastWriteTime is 2026-10-07 08:09:26 local, so the appends landed inside the last
day even though every appended ts stays on 09-28. Still zero rows dated 2026-09-29 or later:
the ledger has not recorded any current-week mining, and DIGEST.md:19's "silent day 8, 693
rows, no writer instrument" note is hereby amended to "705 rows, no post-09-28 rows, no
writer instrument" (writer-instrument census via DIGEST.md:19, not re-run).

The appended arc closes the Sefer Raziel year-chronogram thread that lines 693 and the two
prior lenses carried as FORMALLY OWED (via frontier_olm_2026-10-06/lens/burns.md:39-40 and
:207):

- 14:00-15:30Z (lines 694-696): pagefeed route byte-proved empty; whole-book PDF yielded a
  2736x3485 JBIG2 page-1 decode; chronogram read as samekh-ayin and 5461 provisionally
  refuted (line 696).
- 15:30-16:00Z (lines 697-698): year pinned 5530 (1769/70) by paleography; provenance chain
  closed at snippet tier via van Voolen 1992 JSTOR corroboration (lines 697-698).
- 16:30-18:00Z (lines 699-702): page-tier JSTOR receipt bot-gated (line 699); Kedem auction
  lane Cloudflare-shut (line 700); 1701-vs-5530 left unresolved (line 701); NLI lane
  DNS-dead/JS-shell three attempts (line 702).
- 18:30-19:30Z (lines 703-705): the HebrewBooks catalog's own metadata year 1701 overruled
  the plate chronogram (line 703); an exhaustive subset-sum then reached 5461 (tav+samekh+
  aleph, the aleph in a line the band-break window never inventoried), refuting the 5530
  family as a heuristic artifact and re-confirming 1701 with both faces agreeing (line 704);
  topic CLOSED green-solved with the intermediate 5530 pin explicitly superseded and ONE
  formally-owed residual: the van Voolen page-tier receipt, login-gated (line 705).

ANTI-REBANK UPDATE: the prior lenses' owed item "fire the owed: Sefer Raziel chronogram
(ledger line 693)" (via frontier_olm_2026-10-06/lens/burns.md:207-208) is DONE. Do not
re-chase it; the only live debt there is the login-gated van Voolen page-tier receipt.

## 2. The mined-set registry (the union nobody may silently re-confirm)

### 2a. Inherited banked set (via frontier_olm_2026-10-06/lens/burns.md, read in full)

- Rounds 1-2 register (42 rows / 41 finds), day-4 carrier (22 register + 10 percolator rows,
  10 steal cards), the 11 ranked next actions, R062/B4/24-7-fleet/ouroboros-R1/
  eleven-doors dispositions, and the git-logged drops through 10-05 09:56 (via
  frontier_olm_2026-10-06/lens/burns.md:51-75 and :121-175).
- The day-5 mine (frontier_olm_2026-10-05, folded in commit d5f89d97b): 32 sweeps, 239 banked
  sweep items, 23 confirmed register rows, 8 steal cards, 148 files; its estate-disease
  measurements (29/31 dangling welds since cured to 0 by R4B, zknot 0.59% stable-leading
  share, 13/338 pack truncations, September deepseek write share, 36,567-row switch census)
  (via frontier_olm_2026-10-06/lens/burns.md:65-105).
- The ouroboros loop R1-R5 landing receipts, the relay audit's 6 citation defects, the
  fold_gate/stop-cert/FIRE_LEDGER machinery, and the free-lane fleet's settled SENSING status
  (via frontier_olm_2026-10-06/lens/burns.md:177-190).

### 2b. The day-6 mine (frontier_olm_2026-10-06, banked 2026-10-06 22:22 in commit 41ceea23f)

32/32 sweeps, 230 sweep-level items, 22 confirmed register rows, 2 failed-with-evidence, 10
steal cards, DIGEST + register + percolator candidates (DIGEST.md:7; commit 41ceea23f). The
fold's cards cite estate commits and line numbers; treat the whole day-6 tree as banked. Its
five load-bearing outcomes (DIGEST.md:9-19), none of which may be re-derived:

1. Decision-model wave externally contested (arXiv 2610.06625 register row 12; HN 49933476
   row 4) and landed in estate-shaped serving (llama.cpp /v1/systemone register row 3,
   Ollama 0.35 nimble register row 7), while the estate's own gate is unmet: meter n=0
   (mag/verb.py:493 returned meter_valid False; DIGEST.md:11, :31). The "rung under
   gemma:2b" idea stays a LEAD behind the beat-embeddings-baseline AND >=0.880-on-n>=40 gate
   (DIGEST.md:11, via lens/burns.md:92-95 of the 10-06 lens).
2. Quant bit-ladder is per-artifact and task-graded: 0.6B decision model bf16 0.757 / Q8_0
   0.750 / Q4_K_M 0.703 (register row 14, reddit 1wn0gga); protected-spine IQ1_M beat uniform
   IQ2_S (VeriLoop, register row 15); the owed qwen2.5:7b Q4_K_M vs q8_0 A/B remains UN-RUN
   (DIGEST.md:13).
3. Memory continuity = write-time and use-time contracts: adoption-at-use 8-9/13 vs re-read
   13/13 (arXiv 2610.03902 row 17), temporal flattening 244/381 (2609.36457 row 18), keyed
   belief retirement (cohorte row 21), 40% zero-memory-call sessions (1wlbqnl row 20), and
   the day-5 unconfirmed thread 1wl3828 UPGRADED to confirmed (row 10) (DIGEST.md:15).
4. Dispatch-shape counter-evidence: 11.7M-request production trace shows logical siblings
   rarely overlap in wall-clock (2609.34432, register row 22), gated on an estate width A/B
   with the 1.25x/1.5x band rule (DIGEST.md:17, :43); first judge2 re-look ran (12 w8 rows,
   0 flips, $0.0202, disclosed self-contamination) (DIGEST.md:17).
5. Integrity catch against the estate's own ledger: the day-5 "164.5M tokens" commit-message
   headline is PHANTOM-class; usage.jsonl summed 16,403,718 tokens / 3,012 rows over the
   window (DIGEST.md:19). Never repeat 164.5M as a mined volume.

Also day-6 banked: the placement law (zknot volatile METER line at byte 57 mechanically
causes the 0.59% prefix share; DIGEST.md:33), BreadthKV buy-count-before-fidelity (register
row, DIGEST.md:41, arXiv 2610.05685), BARQ codebook-balance (arXiv 2610.04490, DIGEST.md:39),
and the dead-instrument warnings (benchmark_bridge fallback always True; DIGEST.md:41).

### 2c. Banked by git since the 10-06 lens (my `git log --since="2026-10-06 11:00"` this
sitting; 43 commits). Headlines, do not re-mine any of these subjects:

- 10-06 15:28/15:33/18:28 link-drops: Teknium Hermes Workshop device catalog + MIRA
  meta-reasoning + token cues 2610.06851 (f503da0f5); ALoDLM 2610.04198 open-weights
  diffusion LM (095944421); QUEEN chess LM 4B silent-expert weld 1782->2697 Elo (33b596fa6).
- 10-06 20:21 CHEAP-SEAT GAUNTLET landed (52693b269): gauntlet_feed stages falsifier trials
  into the free-lane fleet queue, MagGauntletFree30 at :15/:45; first register banked $0.00
  (dice 2/2 PASS, beat 3/4 after grader self-strike, 12-count combo 3/12 on-grid, metagame
  caught qwen2.5:7b contesting the hidden roll). Register file:
  watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl (6,324 bytes, 10-06 22:57, my listing).
- 10-06 20:42 LONGRUNNERS-CAGED law (530d0158e): configs/longrunner_policy.json +
  tools/longrunner_patrol.py + MagLongrunnerPatrolDaily; first patrol caught 20, killed 4
  unambiguously hung, siblings await operator ruling.
- 10-06 20:48 canon frame (8dd34b388): roll-shape lens + Turing castle mapping banked with a
  predict-mechanical-graders falsifier.
- 10-06 21:21-21:56 and 10-07 00:22-00:26 MESH DELTA family (cb40977b4 seed, 1fe42d8d6 SSRF
  fence + tripwires 5/5, 70508dcf6 one-computer steal map: exo, cr-sqlite, rqlite/dqlite,
  Mem0/Letta/Zep, vast.ai framing; 5160003c0 overnight receipts incl GPU ladder 72.97 tok/s
  Vulkan vs 6.0 CPU = 12x, install-provenance row tier-2 unconfirmed; 9ccdfa034 memlance wire
  as MCP tools, seed_id sha256, six tools live in tools/list).
- 10-06 22:22 day-6 mine folded (41ceea23f, section 2b) + RUN CLOSEOUT REGISTER (6edc796f8:
  21 terminal-but-undispositioned runs dispositioned with evidence; rule minted: spent-token
  runs get one disposition row, zero-token deaths are admission tickets).
- 10-06 22:41 FOLD-FAST (08f0024fd): tools/fold_prose_local.py folds prose on the local
  janitor qwen2.5:7b over IP-literal http.client; live proof on real dogfood sections.
- 10-06 23:35 STOCKFISH-CODING ractor folded (3f028ec5f: 8 lenses, 86 findings, 8 moves;
  d13 bottleneck verdict re-measured as a wiring defect, not a property).
- 10-07 02:05 DA VINCI lens ractor folded (a4a34e900: 6 lenses, 73 findings, 10 ranked
  moves, tri-state DOCUMENTED/INTERPRETIVE/ELABORATED discipline; Codex Leicester row
  OPERATOR-GATED).
- 10-07 04:28-08:06 NIGHT BURN triple (ac0b4374c design; 64178cf5f night 1 move 1 bridge/test
  drift with the two-lane attribution and the port-8081 test-flake honesty note;
  389ee9c68 night 2 stockfish door moves 2-7 incl the /completion->/v1/completions route
  correction and d13 re-measured apples-to-apples; 04ee7066d DOGFOOD2 night 1/3 15/15 lanes
  incl the CONTEXT-PACK-layer propagation gap; eb7e1529c MORNING BLOCK 8/8 lanes incl
  DRAIN DEAD 20,578-rows-zero-ok re-seed and the 3 PHANTOM-NUMBER blockers now standing at
  AGENTS.md:29 which BLOCK the next push).
- 10-07 05:53 Herald OS link-drop (faeeb7ac3, 6th+ not-trapped-in-chat convergence; steal
  rows: approval-gate + token-tier repo read, crash-narration, scoped widget grants).
- 10-07 08:10/08:11 drift-patrol (2d34b747c: 70 citation debts accepted by name, lint ok, 38
  drifts healed, steady state day 15; 615528cf0 re-seal retry 1) + THE GIFT composed
  (6ab6ed4d5, send path gated on engagement).
- 10-07 08:47-09:37 morning intel wave: LINK-DROPS LiFT 2610.05538 + ES-vs-PPO thread
  (7de95df9c); TURING CASTLE SOURCED, reading upgraded INTERPRETIVE -> DOCUMENTED
  (bb976b343); FREE-RESOURCE SCOUT daily (e1b60e59a: telegraphese register-evolution
  independently confirmed, Forever Junior, AstroHelm, PS5 jailbreaks, lanes stable); THE
  NAMING banked (40a1d6047: smith chart / Turing castle / light maze one object).
- 10-07 10:09 RIB_DEEPSEEK_WINDOW warmed + daily Hermes intel cron armed 09:15
  (c34f52198).

## 3. Carrier directories, last three days (my Get-ChildItem walk this sitting; dirs with
LastWriteTime >= 2026-10-05; 20 of the 40 newest)

- 10-07: ractor_engine (8:45; newest subtree 2026-10-07-external-steal/ with accuracy,
  operations, economics and break-* attack pages written 09:35-10:03, my listing; LIVE
  sibling work, findings not yet banked, see section 4); secret_gate_results (8:13; newest
  changed_20261007T121323Z.json 2.4MB; automated secret-scan dumps on cadence, instrument
  output, not a mine, same disposition as the 10-06 lens gave it via
  frontier_olm_2026-10-06/lens/burns.md:161-162); hermes_burn (5:40; newest
  HERMES_402_WALL_20261007.md 6,735B + H247 A2/A3 drafts from 10-06 evening).
- 10-06: free_lane_queue (dir mtime 23:04 but 0 files at my count this sitting; drained
  again after the 10-06 lens found it empty at midday); frontier_olm_2026-10-06 (the day-6
  mine, section 2b; DIGEST 21:09, RECEIPT 22:14, both postdating the day's lens);
  gauntlet (22:57, section 2c); selfimp (16:41; imp002_dogfood_20261006.md, the actor-reward
  self-play orchestrator dogfood, commits 158952f4e + cb5c20edf); mates_leave_protocol
  (8:35); ouroboros_20261005 (7:37).
- 10-05: frontier_olm_2026-10-05 (the day-5 mine, section 2a); 48h_synth (10:32);
  frontier_olm_2026-10-04 (9:55); endpoint_news, burn_wave_20260926, audit_20260926 (early
  10-05 touches); build_wave_20261005, go_wave_20261004, playground,
  execute_register_seed_fidelity, ribvault_20261005 (overnight waves, dispositions inherited
  via frontier_olm_2026-10-06/lens/burns.md:160-168).

## 4. Live-this-morning: do not collide, do not pre-bank

- watch/inbox/ractor_engine/2026-10-07-external-steal/ has six+ pages written 09:35-10:03
  this morning (break-economics, break-operations, break-accuracy, operations, accuracy,
  break-dogfood, my listing). An external-steal ractor is IN FLIGHT; its verdicts are not
  register rows yet. Wait for its SYNTHESIS/landing receipt instead of re-deriving the same
  attack pages, and cite it, not this lens, once it lands.
- watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md (read as a listing only): the premium
  rung 402 wall with key2 credits aged out, matching finding F1 of commit a3d9d614d; the
  24/7 shape today is the haiku workhorse rung until top-up or cross-key failover.
- free_lane_queue is empty (0 files, my count); anything you stage there per the gauntlet
  feed is a NEW trial, not a re-bank of an old one.

## 5. Anti-rebank rules for the next window

1. The banked set is the union of: rounds 1-2 + day-4 + day-5 registers (via
   frontier_olm_2026-10-06/lens/burns.md:51-105), the day-6 register (22 rows + 10 cards,
   section 2b), section 2c's 43 git-logged commits, the R1-R5 ouroboros receipts, the 8
   mates_leave receipts, the relay audit pages, and ledger lines 640-705 (section 1).
   Overlap must be stated, never silently re-confirmed.
2. Closed or dead, do not rediscover: the Sefer Raziel chronogram (CLOSED green at 1701,
   ledger line 705; the 5530 pin superseded); the JSTOR/Kedem/NLI anonymous fetch lanes
   (bot-gated or DNS-dead, ledger lines 699-702); every Reddit JSON door, Lightning/Chutes/
   SiliconFlow/Scaleway credits, Hitler ancestry, the marfinxx fabrication, the struck
   191.8M figure, and the day-5 164.5M phantom headline (DIGEST.md:19); the day-5
   decision-model headline as a confirmable item (sweep-level by recorded verdict,
   DIGEST.md:11).
3. Fire the owed before opening new seams (all still open after this fold): manufacture
   n>=40 fleet-labeled rows so the decision-model meter is ever valid (DIGEST.md:11, :31);
   the qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B (DIGEST.md:13); the S10 width A/B with the
   1.25x/1.5x band (DIGEST.md:43); the LAPSE-mini pairing rule and R5 target 1 consult
   receipts (DIGEST.md:27, :33); the day-5 88-item confirmation pass (via
   frontier_olm_2026-10-06/lens/burns.md:96-99); DeepSeek invoice-strength discount check
   and the Featherless 28.6k-row gap (via frontier_olm_2026-10-06/lens/burns.md:203-209);
   GSTD wallet addresses (operator input); the van Voolen page-tier receipt (login-gated,
   ledger line 705); the 3 PHANTOM-NUMBER blockers at AGENTS.md:29 that block the next push
   (commit eb7e1529c).
4. Ledger drift flag, amended: rows 694-705 prove somebody can still append to
   memory/burns/LEDGER.jsonl, but nothing dated after 09-28 has landed and DIGEST.md:19
   found no writer instrument. Until a writer exists, your DIGEST/RECEIPT pair plus a git
   commit IS the mining record; do not assume a ledger row exists, and do not treat this
   file's silence on a topic as evidence nobody mined it.
5. Counts law: every count above is instrument-tagged (PowerShell ledger count, ts sort,
   Get-ChildItem walk, Read line ranges, git log output, file listings). Do not difference
   counts taken by different instruments at different moments.
