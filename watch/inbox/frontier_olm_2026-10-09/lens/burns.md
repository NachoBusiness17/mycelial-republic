# Lens: burns (what was already mined this week, so nobody re-banks it)

Folded 2026-10-09 by the frontier_olm_2026-10-09 burns lens. House laws held: ascii only, no
em or en dashes, every claim cites what was read or run this sitting. Inherited content is
marked "(via ...)" with the source file named; that file was read this sitting without
re-verifying its underlying claims. This lens is the successor to
frontier_olm_2026-10-08/lens/burns.md (read in full this sitting, 243 lines).

## How this was built (instruments, this sitting)

- The ask's named read: `Get-Content memory\burns\LEDGER.jsonl -Tail 25` (PowerShell); the
  last row of that tail is the last row of the file and begins
  `{"ts": "2026-09-28T19:30:00Z", "slug": "doctrine-owed-chase", "verdict": "green"`.
- Ledger census: `Get-Content memory\burns\LEDGER.jsonl` counted 705 lines;
  `Select-String -SimpleMatch "2026-10"` matched 13 rows, every one a deadline or week
  reference (2026-10-10 LAW-12 window, 2026-10-04 clocks, W43 2026-10-19) inside a row whose
  own ts is 2026-09-25 through 2026-09-28; zero rows carry an October ts.
- Ledger stamp: `Get-Item memory\burns\LEDGER.jsonl` returned 571,821 bytes, LastWriteTime
  2026-10-07 08:09:26 local. The 10-08 lens recorded the same three numbers
  (frontier_olm_2026-10-08/lens/burns.md:15-17), and the 10-07 lens the same before that
  (frontier_olm_2026-10-08/lens/burns.md:33-38). Three lenses in a row now read the ledger
  byte-frozen.
- Carrier walk run this sitting: `Get-ChildItem watch\inbox -Directory | Where-Object {
  $_.LastWriteTime -gt (Get-Date).AddDays(-3) } | Sort-Object LastWriteTime -Descending`
  returned 25 directories, mtime window 2026-10-06 16:41 through 2026-10-09 09:34
  (section 3). Top-file listings of the 11 dirs newer than the 10-08 lens fold were taken
  the same way (names + byte sizes, section 3).
- Git: `git log --since="2026-10-08 12:00" --pretty="%h %ad %s"` returned 21 commits
  (section 2c takes its rows from that output); `git log --all --grep="OLM"` shows the last
  olm-mine banked row is still day-7 (c7d364ab6); `git ls-files
  watch/inbox/frontier_olm_2026-10-08 | wc -l` counted 110 tracked files there;
  `git status --short` on that path is empty.
- Read this sitting in full: frontier_olm_2026-10-08/lens/burns.md (243 lines). Read this
  sitting in part: frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md (first 40 lines) and
  SUMMARY.json (whole file), the day-8 quant A/B receipt.
- Not run this sitting: any pytest, any fresh web fetch, any re-verification of inherited
  sweep or register payloads, any owed probe. This lens folds, it does not confirm.

## 1. Ledger state: byte-frozen across three lenses; no current-week mining record

This sitting the ledger reads 705 lines / 571,821 bytes / max ts 2026-09-28T19:30:00Z /
mtime 2026-10-07 08:09:26 local: identical to the 10-08 lens read and the 10-07 lens read
(via frontier_olm_2026-10-08/lens/burns.md:31-38). Nothing dated after 2026-09-28 has ever
landed in it. What the tail holds (my Tail-25 read, all rows ts 2026-09-28):

- doctrine-owed-chase: the Sefer Raziel chronogram arc, CLOSED green-solved, all 48 source
  threads terminal, the plate chronogram and the HebrewBooks catalog agreeing on 1701, ONE
  residual login-gated debt (the van Voolen page-tier receipt).
- free-resource-landscape: DeepSeek window and off-peak questions closed on official pages,
  Featherless full-dump-vs-paged gap closed at 28.6k unserved rows owed, Lightning lane
  closed FULLY DEAD alongside Chutes/SiliconFlow/Scaleway.
- middle-path-doctrine: four restatement carriers minted, F8 clause re-armed behind a gated
  stub build, X6 window audit green.

ANTI-REBANK: do not re-chase Sefer Raziel provenance, DeepSeek window/off-peak, the
Featherless roster instrument, or the Lightning credits chase; all terminal in the ledger.
Until a ledger writer instrument exists (none found, via frontier_olm_2026-10-08/lens/
burns.md:56-58 and :236-240), a DIGEST/RECEIPT pair plus a git commit IS the mining record.
The freeze is now a three-lens standing incident, re-flagged with this sitting's stamp.

## 2. The mined-set registry (the union nobody may silently re-confirm)

### 2a. Inherited banked set (via frontier_olm_2026-10-08/lens/burns.md, read this sitting)

- Day-5 mine (commit d5f89d97b): 32 sweeps, 23 confirmed rows, 8 cards; its 164.5M-token
  headline is PHANTOM-class (via :64-67). Never repeat it.
- Day-6 mine (41ceea23f): 32 sweeps, 22 confirmed, 10 cards; decision-model wave, memory
  write-time contracts, placement law, BreadthKV/BARQ (via :68-75).
- Day-7 mine (c7d364ab6): 32/32 sweeps, 21/24 confirmed, 8 cards, DIGEST rev 2; small-model
  band unmeasured (meter n=0), harness-dominates-small-models, decision-rung bar, consensus
  counter-designs, ReFold + compaction APIs, the three unconfirmed-with-evidence items stay
  out of register.jsonl (via :79-108).
- Commits banked through the 10-08 08:09 drift patrol (31edc2309, baseline 72) incl the port
  wave P1-P6 (6685db6bc), the shell-door containment, gps_embed KILL (9b72d287c), classical
  ML moonshot (19bac8201), ractor fold (1f0383d59), comics lane (714e1be01), person mine
  (e925a8d1a), residue probe (b526bc339), GSTD/MYCELIAL kickoff (7b4d86bad) (via :110-167).
- Prior rounds 1-2, day-4, ouroboros R1-R5 ride via :76-77.

### 2b. The day-8 mine (frontier_olm_2026-10-08): artifacts banked, fold debt open

State at my listing and git queries this sitting:

- 32 sweep files on disk: 8 categories (agent-memory-continuity, evals-and-self-improvement,
  finetuning-adaptation, inference-efficiency, kv-cache-context-engineering,
  open-local-models, quantization-compression, swarm-orchestration) x 4 sources
  (arxiv/hn/reddit/x) under sweep/ (my recursive listing, mimosa hook-state excluded).
- 6 steal cards under steal/: finetuning-adaptation, inference-efficiency-hn,
  kv-cache-context-engineering, open-local-models, open-local-models via reddit,
  quantization-compression via hn (my listing).
- 6 lenses under lens/ (burns, corpus, doors, graph, laws, questions) (my listing).
- quant_ab/: the four-lane-owed qwen2.5:7b Q4_K_M vs q8_0 A/B WAS RUN 2026-10-08 after the
  10-08 lens folded (RECEIPT.md:1-6 records it firing on the amended four-pinned-choices
  instrument, QUANT_AB_SPEC_AMEND.md / 6685db6bc; commands logged :17-19). Verdict TIE AT
  CEILING: both arms 50/50 full-pipeline 100.0 pct, strict 49/50 98.0 pct both, per-task
  spread 0.0 both arms (SUMMARY.json arms + per_task_spread blocks); speed separates them,
  Q4 median 6.90 tok/s vs Q8 3.00 (SUMMARY.json arms tok_s_median). This RESOLVES the
  top owed item of frontier_olm_2026-10-08/lens/burns.md:206-208. Do not re-run it; a
  re-run is only legitimate as a different-instrument replication, named as such.
- Fold debt: NO DIGEST.md, RECEIPT.md, or register.jsonl exists at the dir top (my
  recursive listing), and `git log --all --grep="OLM"` has no day-8 banked row (last is
  c7d364ab6, day-7). 110 files of the dir are tracked (my git ls-files count), landed under
  the broad disk-crisis close commit 72caa1a3a per `git log` on the path. The day-8 mine's
  findings therefore live only in its sweep/steal/lens files; the next window's job is the
  FOLD (digest + register + percolator candidates), not another sweep of the same 8
  categories.

### 2c. Banked by git since the 10-08 lens fold (my git log --since="2026-10-08 12:00" this
sitting; 21 commits, 10-08 16:43 through 10-09 09:20). Headlines; do not re-mine any of
these subjects:

- 10-08 16:43 disk-crisis relief (0b9980351): C: at 6.1GB free; docker cache +14.13GB,
  ollama rotation +19GB re-pullable with modelfile receipts; disk_free_floor_gb 15GB
  tripwire landed; DISK_INVENTORY_20261008.
- 10-08 19:45 SMITH CHART OF THE HDD (cd118ed70): tools/disk_smith.py; first live row solved
  the missing 700GB (.zcode exec-log exhaust 335.3GB); MagDiskSmithDaily 08:50.
- 10-08 20:21 disk-crisis close (72caa1a3a): churn tasks disabled for AV-fight reboot; the
  exec-log monster named (.zcode/cli/exec 310GB, no rotation).
- 10-08 21:57 DISK AUDIT WAVE 20261009 (33fabd595): 7 lanes; forest 309.12GiB autopsied,
  82.8 pct attributed to 30 named burns; 2 zombie crons found (one deleted with recipe
  banked, flash dispatcher no-opping since 09-27 needs operator kill); 8-law standing-wave
  pack + RIB_STANDING_WAVE_BUDGET_20261009.
- 10-08 22:18 CLEANUP P1-P3 (dee2db9e8): 7,377 files / 234.92GiB freed, HF dead experiments
  56.25GiB; free 167 to 459GB; P4 fleet re-enable HELD for operator AV exclusions.
- 10-08 22:26 ESTATE SMITH CHART v1 (6566cece8): estate_smith.py STORAGE/PRESSURE/COMPUTE/
  FLOW/LOSS/RESONANCE row 1.
- 10-08 22:57 MOONSHOT SELF-STEAL 20261009 FOLDED (bb0e51b0d): five-asset composition
  (mesh=body, 5h-window=metabolism, tokens=blood, WoW=work, GSTD=settlement); build order
  1-5 banked; probes 2-3 operator-gated.
- 10-08 23:03 PROBE 1 EXECUTED (4fc48b240): three-ledger join, first internal price rows:
  $94.74/12d paid, $0.45 per STEAL verdict, $4.31 per green; the free-to-paid exchange rate
  named the unmeasured column.
- 10-08 23:08 GSTD DISTRIBUTION THESIS (ce9a1053c): node-by-default installer closes supply
  AND demand; clean-vs-poisonous wallet hinge.
- 10-08 23:15 RIB_NOT_EVEN_ME + GARAGE WIZARD VISION (4adf6324a): two-tier truth (local
  verkle offline, deferred GSTD when bridged); Article 15 amended local, push GO-gated.
- 10-08 23:40 LINK DROP (7681845de): slashreboot open-dialogue article, STEAL-ADAPTED as
  Self Council opening material; author model is the one the estate composted hours earlier.
- 10-09 00:09 GSTD P1 FIRED + NIGHT BUILD (7a5d64be1): gstd-desktop LIVE as 5th network node
  on a FRESH zero-balance wallet (loaded vault retired from node duty); L2 retention
  contract as code (disk_smith --prune, 9 tests); L8 dot-dir lock (7 tests + live cure);
  estate_smith promoted (tools/, 14 tests, MagEstateSmithDaily 09:05); compost ledger
  (34 byte-verified kills, 3 pre-warmed revivals).
- 10-09 00:22 GSTD DESKTOP BUILD-OUT (4dc589b18): cloudflared quick tunnel LIVE, smoke test
  pass thru tunnel; honest findings: all tunnel traffic collapses to one docker-bridge IP,
  external scanners ate the 120/min rate bucket within 26s; heartbeat 600s erratum named.
- 10-09 00:24 REVIVALS (25367284a): REVIVAL_CATALOG 13 byte-verified rows; tools/
  shape_tripwire.py (GPS-embed cold-start crossover instrument, 8 tests, kill dormant);
  DDR3_WEEKEND_CARD frozen with eval bar + pre-registered no-heal falsifier.
- 10-09 00:59 ROUTER LEARNS THE GARDEN (700625aa0): 14 gstd-tier providers appended as
  config.gstd.json; 3 real asks routed live ALL PASS carrying _gstd tier=gstd
  sovereignty=true; mid-lane correction (live/config split) cured with 42/42 suite.
- 10-09 01:01 UPSTREAM PR SET (f91b8ca88): 3 fix branches + 1 issue draft on fork
  NachoBusiness17/gstdbot; BLOCKER BANKED NOT FAKED: PAT cannot gh pr create on
  gstdcoin/gstdbot (403); finish = 3 compare-URL clicks by the co-founder.
- 10-09 01:04 BASECAMP WAVES 1-2 + AUDIT LANE A + SELF-STEAL (708cf5bc6): three-body map,
  staleness census, queue dig (ZERO orphans), shoulder-L BANKED (~zero), platform surface
  map (28 GETs + 151 routes), codebase audit lane A (28 modules, 9 NEW findings incl
  unauth telegram webhook to /restart, unauth wallet disclosure on ~115/151 routes,
  machine-derived wallet seeds); self-steal near-miss law.
- 10-09 01:22 GSTD FULL AUDIT + DAWN REPORT (7baed4c0e): genesis seal ASPIRATIONAL (phantom
  contract methods, fabricated tx hashes at token.ts:387-396), 91 pct emissions to the
  bootstrap Pi, best steal TON ton_proof, BUILD-OURSELVES moat = replay-verified task
  settlement; DAWN_REPORT.md one-pager.
- 10-09 08:09 drift-patrol (84e29dc32): 22 citation debts accepted (baseline 88); gstd-node
  joined the fleet; 7 drifts healed; steady state day 15.
- 10-09 09:04 FREE-RESOURCE SCOUT (f80961cd9): lanes stable (openrouter 469, groq 11,
  mistral 46); four HN rows banked as intel.
- 10-09 09:20 HERMES DIGEST (f676ee787): memory runaway-recall ceiling + opt-in prefetch
  spilling, DIRECT HIT on the diagnosed L0d context-pack shedding, ACTION ported into the
  staged fix; fxtwitter timelines 404 x2 negative rows.

## 3. Carrier directories, last three days (my Get-ChildItem walk this sitting; 25 dirs,
mtime 2026-10-06 16:41 through 2026-10-09 09:34; dispositions from my same-sitting listings
and section 2c)

New since the 10-08 lens fold:

- 10-09 09:34 walkthrough_20260109 (INSTALL_TEST_RECEIPT.md, PODCAST_FACT_SHEET.md)
- 10-09 09:18 hermes_daily (HERMES_DIGEST_2026-10-09.md; f676ee787)
- 10-09 09:01 mates_leave_protocol (W3A-W3G fix receipts, grok thread jsonl, night-burn and
  oral-law mine scripts)
- 10-09 08:09 secret_gate_results (automated secret-scan dumps on cadence; disposition via
  frontier_olm_2026-10-08/lens/burns.md:172-174)
- 10-09 01:20 gstd_basecamp_20260109 (AUDIT_PLAN, DAWN_REPORT, GAPS_AND_PEOPLE,
  GSTD_CODEBASE_AUDIT, GSTD_REPUBLIC_COOKBOOK, GSTD_TOKENOMICS_AUDIT, PLATFORM_SURFACE_MAP,
  QUEUE_DIG; 708cf5bc6 + 7baed4c0e)
- 10-09 00:36 moonshot_selfsteal_20260109 (00_FOLD through 05_GSTD, PROBE1_LEDGER_JOIN,
  PROBE2_LIVE_NET_ROUTED; bb0e51b0d + 4fc48b240)
- 10-09 00:19 compost_20260109 (COMPOST_LEDGER.jsonl, COMPOST_MAP.md, REVIVAL_CATALOG.md,
  DDR3_WEEKEND_CARD.md; 7a5d64be1 + 25367284a)
- 10-08 23:57 disk_audit_20261009 (LAW_PACK.md, LESSONS.md, ORGANIZATION_SPEC.md,
  CHECKPOINT.md, CRON_FREEZE_20261009.md; 33fabd595)
- 10-08 23:38 smith_chart_estate_20260109 (estate_smith.py + jsonl + PROMOTION_LANDED.md;
  6566cece8 + 7a5d64be1)
- 10-08 23:30 analytics_pass1_20260109 (A1_VERDICT_DECAY through A5_ASK_SHAPES; 7681845de)
- 10-08 22:22 smith_chart_estate_20261009 (SPEC.md only)
- 10-08 16:37 model_modelfiles_20261008 (athena-class, frob_ling-3.0-flash, maze-keeper,
  qwen2.5_32b modelfiles; 0b9980351 re-pull receipts)
- 10-08 16:34 frontier_olm_2026-10-08 (the day-8 mine, section 2b)

Covered by the 10-08 lens (via frontier_olm_2026-10-08/lens/burns.md:169-185): port_wave_
20261007, frontier_olm_2026-10-07, gps_embed, ml_moonshot_20261007, free_lane_queue,
person_mine, ractor_engine, residue_probe_20261007, hermes_burn, frontier_olm_2026-10-06,
gauntlet, selfimp, secret_gate_results (earlier write).

## 4. Resolved since the 10-08 lens (do not re-open) and what stays owed

Resolved this window, each with its carrier:

1. qwen2.5:7b Q4_K_M vs q8_0 A/B: RUN, TIE AT CEILING (section 2b; quant_ab RECEIPT.md +
   SUMMARY.json). Was the 10-08 lens's top owed item (:206-208).
2. GSTD P1: fired, node live on a fresh zero-balance wallet (7a5d64be1); router gstd tier
   proven with 3 live routed asks (700625aa0); tunnel serves, smoke test pass (4dc589b18).
3. Disk crisis: measured, purged, fenced (0b9980351, cd118ed70, dee2db9e8, 33fabd595;
   free 167 to 459GB per dee2db9e8).
4. Moonshot self-steal fold + probe 1 (bb0e51b0d, 4fc48b240): the five-asset composition
   and the first priced verdict rows exist; do not re-derive the price rows.
5. Shell door containment, GPS-embed kill, ractor fold: already resolved at the 10-08 lens
   (via :189-198), unchanged by anything I read this sitting.

Still owed (open at this fold; no evidence any fired, except where named):

- The day-8 FOLD itself: DIGEST.md + register.jsonl + percolator candidates for
  frontier_olm_2026-10-08 (section 2b fold debt). Cheapest and highest-leverage next act.
- X surface wire (syndication/x-history) before tomorrow's Hermes fire (f676ee787 OWED line).
- Upstream PR submission on gstdbot: 3 compare-URL clicks by the co-founder or a
  rights-capable token (f91b8ca88).
- Zombie cron kill: flash dispatcher no-opping since 09-27, needs operator kill from the
  Automations page (33fabd595).
- P4 fleet re-enable after operator AV exclusions; temp ruling on recovery_pack 26.4 +
  lsarchive 18.5 GiB (dee2db9e8).
- Carried from the 10-08 lens, still no receipt found this sitting (via :204-220): the van
  Voolen page-tier receipt (login-gated, ledger line 705); manufacture of n>=40 fleet-labeled
  rows for the decision-model meter; day-7 probe queue items as printed; DeepSeek
  invoice-strength discount check; Featherless 28.6k-row gap; the day-5 88-item confirmation
  pass; kv-cache provenance re-audit and the day-5 memlance falsifier reconciliation.
- Ledger writer instrument: three consecutive lenses read the ledger frozen (section 1);
  an owner must mint a writer or take the retire decision to the operator (via
  frontier_olm_2026-10-08/lens/burns.md:236-240).

## 5. Anti-rebank rules for the next window

1. The banked set is the union of: the inherited set (section 2a), the day-8 artifacts on
   disk (32 sweeps + 6 cards + 6 lenses + quant_ab, section 2b), section 2c's 21 git-logged
   commits, and ledger lines through 705 (section 1). Overlap must be stated, never
   silently re-confirmed.
2. Closed or dead, do not rediscover: Sefer Raziel provenance (green at 1701); the JSTOR/
   Kedem/NLI anonymous lanes; DeepSeek window/off-peak; Lightning/Chutes/SiliconFlow/
   Scaleway credits; the shell-door escape as a find; GPS-embed; the quant A/B (run, tie);
   the day-5 164.5M phantom headline; the day-7 DIGEST's three unconfirmed items as
   confirmed rows; the GSTD genesis seal (audited ASPIRATIONAL at 7baed4c0e).
3. Fold before sweeping: the day-8 mine has no DIGEST/register; folding it outranks a new
   pass over the same 8 categories (section 2b, 4).
4. Ledger drift flag, re-armed with a third stamp: memory/burns/LEDGER.jsonl byte-frozen
   at 571,821 bytes / max ts 2026-09-28T19:30:00Z since 2026-10-07 08:09:26 local (my
   Get-Item this sitting).
5. Counts law: every count above is instrument-tagged (PowerShell tail, line count,
   Select-String, Get-Item stamps, Get-ChildItem walks, git log / ls-files output, Read
   line ranges). Do not difference counts taken by different instruments at different
   moments.
