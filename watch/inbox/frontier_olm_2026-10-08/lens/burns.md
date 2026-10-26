# Lens: burns (what was already mined this week, so nobody re-banks it)

Folded 2026-10-08 by the frontier_olm_2026-10-08 burns lens. House laws held: ascii only, no
em or en dashes, every claim cites what was read or run this sitting. Inherited content is
marked "(via ...)" with the source file named; that file was read this sitting without
re-verifying its underlying claims. This lens is the successor to
frontier_olm_2026-10-07/lens/burns.md (read in full this sitting, 234 lines).

## How this was built (instruments, this sitting)

- The ask's named read: `Get-Content memory\burns\LEDGER.jsonl -Tail 40` (lines 666-705 of
  the file) via PowerShell; then `[System.IO.File]::ReadAllLines(...LEDGER.jsonl).Count`
  returned 705, first line ts 2026-09-25T10:05:50Z, last line begins
  `{"ts": "2026-09-28T19:30:00Z", "slug": "doctrine-owed-chase", "verdict": "green"`.
- Ledger stamp: `Get-Item memory\burns\LEDGER.jsonl` returned 571,821 bytes, LastWriteTime
  2026-10-07 08:09:26 local. The 10-07 lens recorded the same three numbers
  (frontier_olm_2026-10-07/lens/burns.md:11-13), so the ledger is unchanged since that fold.
- Carrier walk run this sitting: `Get-ChildItem watch\inbox -Directory | Sort-Object
  LastWriteTime -Descending | Select-Object -First 60` (section 3); newest-file listings of
  port_wave_20261007, gps_embed, person_mine, residue_probe_20261007, ml_moonshot_20261007,
  free_lane_queue.
- Read this sitting: frontier_olm_2026-10-07/DIGEST.md in full (111 lines, the day-7 mine
  rev 2); frontier_olm_2026-10-06/DIGEST.md in full (114 lines, the day-6 mine);
  frontier_olm_2026-10-07/lens/burns.md in full (234 lines).
- `git log --since="2026-10-07 10:00" --format="%h %ad %s"` run this sitting: 30 commits
  (section 2c takes its rows from that output).
- Not run this sitting: any pytest, any fresh web fetch, any re-verification of sweep or
  register payloads, any probe from the 10-07 DIGEST probe queue. This lens folds, it does
  not confirm.

## 1. Ledger state: byte-unchanged since the 10-07 lens; still no current-week mining record

The 10-07 lens read 705 rows / 571,821 bytes / max ts 2026-09-28T19:30:00Z (via
frontier_olm_2026-10-07/lens/burns.md:30-40). This sitting the same file reads the same
705 rows / 571,821 bytes / max ts 2026-09-28T19:30:00Z, LastWriteTime still 2026-10-07
08:09:26 local (my Get-Item this sitting). Zero rows have landed in over 24 hours; nothing
dated after 2026-09-28 has ever landed (max-ts verification this sitting and via
frontier_olm_2026-10-07/lens/burns.md:14-16).

What the tail holds (lines 666-705, my tail read): three slugs, all closing on 09-28.

- doctrine-owed-chase (lines 675-705): the Sefer Raziel chronogram arc, CLOSED green-solved
  at line 705 with all 48 source threads terminal; the plate chronogram and the HebrewBooks
  catalog both agree on 1701 via exhaustive subset-sum (line 704); ONE residual formally
  owed: the van Voolen page-tier receipt, login-gated (lines 703-705).
- free-resource-landscape (lines 675-702 even slots): DeepSeek window contest CLOSED on the
  official pricing page (line 681), off-peak inference PROVEN (line 692), Featherless
  full-dump vs paged gap closed at 28.6k unserved rows owed (line 694), Lightning lane
  closed FULLY DEAD with Chutes/SiliconFlow/Scaleway (line 701).
- middle-path-doctrine (lines 675-693 odd slots): four independent restatement carriers
  minted, F8 game-class clause re-armed behind a gated stub build (line 688), X6 window
  audit green (line 693).

ANTI-REBANK: do not re-chase the Sefer Raziel provenance, the DeepSeek window/off-peak
question, the Featherless roster instrument, or the Lightning credits chase; all terminal
in the ledger tail this sitting. Until a writer instrument exists (none found, via
frontier_olm_2026-10-06/DIGEST.md:19 and :83), a DIGEST/RECEIPT pair plus a git commit IS
the mining record; do not assume a ledger row exists.

## 2. The mined-set registry (the union nobody may silently re-confirm)

### 2a. Inherited banked set (via the two prior lenses, read this sitting)

- Day-5 mine (frontier_olm_2026-10-05, commit d5f89d97b): 32 sweeps, 23 confirmed register
  rows, 8 steal cards; its "164.5M tokens" headline is PHANTOM-class, usage.jsonl summed
  16,403,718 tokens / 3,012 rows (via frontier_olm_2026-10-06/DIGEST.md:19, :84). Never
  repeat 164.5M as a mined volume.
- Day-6 mine (frontier_olm_2026-10-06, commit 41ceea23f): 32 sweeps, 230 sweep items, 22
  confirmed, 2 failed-with-evidence, 10 steal cards; load-bearing: decision-model wave
  contested with the estate meter at n=0 (DIGEST.md:11), quant bit-ladder per-artifact
  task-graded with the qwen2.5:7b Q4-vs-Q8 A/B still un-run (DIGEST.md:13), memory
  continuity write-time/use-time contracts (DIGEST.md:15), 11.7M-request dispatch-shape
  counter-evidence gated on a width A/B (DIGEST.md:17, :43), the placement law and
  BreadthKV/BARQ steals (DIGEST.md:33, :39, :41) (via frontier_olm_2026-10-07/lens/burns.md
  :82-114, which cites these; both DIGESTs re-read this sitting).
- Prior banked set older than day-5 (rounds 1-2, day-4, ouroboros R1-R5, the 11 ranked next
  actions) rides via frontier_olm_2026-10-07/lens/burns.md:65-81.

### 2b. The day-7 mine (frontier_olm_2026-10-07, banked in commit c7d364ab6, 10-07 23:27)

32/32 sweeps, 21/24 confirmed (3 failed with evidence, DIGEST.md:89-91), 8 steal cards,
DIGEST rev 2 with 18 cold-reader repairs applied in place (DIGEST.md:5). Headlines, all
banked, do not re-derive (DIGEST.md:15-23, section 2 named finding :25-33, cards :38-45):

- 0.5B-8B band UNMEASURED on public evidence and on the estate's own battery (meter n=0,
  mag/verb.py:493 meter_valid False, DIGEST.md:15).
- Harness/serving stack dominates small-model outcomes: Mingbird 0.405 to 0.886 LRAB,
  tool-call fidelity is a serving-layer property, 7B quant A/B flips on prompt/scoring/
  parsing choices (arXiv 2610.07781 CONFIRMED, DIGEST.md:16).
- Decision-rung bar (>=0.880 on n>=40 vs beat-embeddings) cleared by nothing read;
  semantic-entropy tops at 0.871 AUROC, nimble 86.9 percent CI 82.9-90.0 straddles the gate
  (DIGEST.md:17).
- llama.cpp b11465-b11475 runtime deltas are Metal-specific; Windows/Vulkan estate box not
  forced; b11475 body primary-verified this fold (DIGEST.md:18).
- Consensus-illusion counter-designs: ArcticSwarm 82.6 vs 63.5, probe monitors 97-99
  percent recall vs judge 9, judge kappa 0.15 (DIGEST.md:19).
- Context-engineering cure class: ReFold reversible folding (2610.07863) + xAI/Anthropic
  compaction APIs with zero continuity measurements (DIGEST.md:20).
- Named finding: the estate shell door (tools/code_execution.run_python) measured
  UNCONTAINED twice, live-verified (DIGEST.md:25-33). SUPERSEDED BY THE PORT WAVE, see
  section 4.
- Tag-digest aliasing verified live: qwen3 4b and 4b-thinking manifests byte-identical
  sha256 (DIGEST.md:18, :43).
- Judge-agreement-is-the-wrong-target, three independent ways (DIGEST.md:22).
- The 3 unconfirmed items with evidence (35B MoE thread second-hand only; the OpenAI
  caching-doc claim CONTRADICTED by the fetched page; TokenProbe partially supported with
  three factual errors) stay out of register.jsonl (DIGEST.md:89-91). Do not re-bank any of
  the three as confirmed.

### 2c. Banked by git since the 10-07 lens fold (my git log --since="2026-10-07 10:00" this
sitting; 30 commits). Headlines, do not re-mine any of these subjects:

- 10-08 08:09 drift-patrol (31edc2309): 3 citation debts accepted, baseline now 72, 9
  drifts healed, port wave landed, steady state day 13.
- 10-08 02:11 PORT WAVE 20261007 LANDED (6685db6bc): P1 cite-allowlist gate (13 tests), P2
  contamination tripwire duty_fuzz (22 tests, first pair gemma:2b 0.9167/0.8333), P3
  tag-digest pinning + boot verify + thinking-default reader (97 passed), P4 CONTAINED
  SHELL DOOR (AST static gate + win32 Job Object + canary walk failing loud exit 125), P5
  ReFold reversible sheds (restore door proved 4290 chars; the 84 stale full-mode rows
  traced to a LIVE pre-commit container renderer), P6 trio (quant A/B four-pinned-choices
  spec, marker-penalty logit_bias OFF by default, G2 blind-sweep placement law WARN).
  Receipts: watch/inbox/port_wave_20261007/ (p2_contamination.md, p4_shell_door.md,
  p5_refold.md, QUANT_AB_SPEC_AMEND.md, p6_small_ports.md, my listing this sitting).
- 10-07 23:27 day-7 mine banked (c7d364ab6, section 2b) + LINKS row (a6d55bd0e) + handoff
  append (64ce56318).
- 10-07 22:41 NO-SLOP steal landed (ee3756f0d): .agents/skills/no-slop +
  tools/prepush_slop_patrol.py, WARN-only, 13 tests; self-audit: the estate's dominant tic
  is the colon reveal (25/28).
- 10-07 20:51/21:00 GPS-EMBED TRIAL KILLED BY ITS OWN FALSIFIER (9b72d287c): string keys
  100.0 percent vs embedding-kNN 99.05, McNemar p=0.5, 60x over latency budget; cold-start
  leg banked not built. Receipt: watch/inbox/gps_embed/GPS_EMBED_TRIAL.md.
- 10-07 20:13/20:18 EmbeddingGemma 2 banked under models/ (56b836d5a, fd09a9fce).
- 10-07 19:34 CLASSICAL ML MOONSHOT (19bac820a1, dwfrun-926ad13e, 8/8 lanes, 38 rows, ACCEPT,
  zero unconfirmed): ml1 labeled corpus, ml2 NASA lineage + defect frame (1443 modules),
  ml3 GPS ROUTER (GB AUC 0.9434 vs percolator lexicon 0.5012 CHANCE), ml4 regression
  forecaster, ml5 anomaly head, ml6 ES mesh skeleton, ml7 quantizer bridge, ml8 roll-shape
  classifier. Receipts: watch/inbox/ml_moonshot_20261007/ (ML3_GPS_ROUTER_RECEIPT.md et al.,
  my listing).
- 10-07 17:39 TRACK 5 GAUNTLET folded (794bdd56d: 7 lenses, 77 findings, 8 moves; the
  lyrics-never-banked-verbatim repeat offense named).
- 10-07 17:17 COMICS LANE landed (714e1be01: schema door measured per-seat; mistral 2/2 +
  qwen2.5:7b 2/2 PASS; nvidia llama-3.2-11b ACCEPTS-but-IGNORES response_format; gemma:2b
  full PASS uninstructed; GEMMA-4 seat PATH-DARK 429, console re-provision owed; Discord
  posting refused as theater).
- 10-07 14:20/16:50 PHEROMONE BUS + SWARM (d475824df tools/pheromone.py D7 decay;
  633b884ad Merkle cure shipped: MAG_POSITION_BOUND_LEAVES flag flips the [a,b,c] vs
  [a,b,c,c] falsifier; twin-python verdict; ONE unconfirmed p1a L0d).
- 10-07 14:59 EXTERNAL-STEAL RACTOR FOLDED (1f0383d59: 7 lenses, 76 findings, 6 moves; the
  meta-cure: the 48h law-pack day-lag is blocked at MINTING, cure is mint-at-closeout; the
  402/429 confusion has LiteLLM vendor precedent). This RESOLVES the prior lens section 4
  live-collision item on ractor_engine.
- 10-07 13:14 PERSON MINE LIVE (e925a8d1a): Lilith 9 concepts + 12 new tweet IDs,
  VaultMother 12 concepts, the syndication-CDN no-auth door; dossiers at
  watch/inbox/person_mine/ (my listing).
- 10-07 12:35-12:56 Cognitopolis v0 spec (e02fef752), City Generator link-drop BUY-GATED
  (d7ab3e227), REACH + push decision staged awaiting operator GO (ac3cfb4cc).
- 10-07 12:14 RESIDUE PROBE, doctrine survived its substantive test (b526bc339: recovery
  stage at chance AUROC 0.49-0.55 vs coupling-keeping 0.47-0.983; 157 rows, $0;
  watch/inbox/residue_probe_20261007/, my listing).
- 10-07 11:29-11:49 NACHO VEIN canon archaeology (02c513767: 12 posts fetched first-hand;
  doctrines appear in operator public writing 1-2 years before the instruments; "coldest
  shared vertex" NOT byte-found, tagged INTERPRETIVE) + two lens readings (3ecde4243,
  75c3b7369) + VEIN rows 13-14 (a93ff5cb2).
- 10-07 10:55 MERKLE PADDING COLLISION proven triple-armed (29c8c87e9).
- 10-07 10:32 GSTD/MYCELIAL KICKOFF (7b4d86bad: gstd door connected, 13 tests, exit 3
  WALLET GATE BLOCKED proven on-box; wallets still owed from the operator).
- 10-07 10:09 RIB_DEEPSEEK_WINDOW warmed + daily Hermes intel cron armed 09:15 (c34f52198).

## 3. Carrier directories, last three days (my Get-ChildItem walk this sitting; dirs with
LastWriteTime >= 2026-10-06; 15 of the 60 newest)

- 10-08: secret_gate_results (08:10; automated secret-scan dumps on cadence, instrument
  output not a mine, disposition via frontier_olm_2026-10-07/lens/burns.md:171-174);
  port_wave_20261007 (01:53; the landed port receipts, section 2c).
- 10-07: frontier_olm_2026-10-07 (23:22; the day-7 mine, section 2b); gps_embed (20:51;
  trial receipt, verdict KILL, section 2c); ml_moonshot_20261007 (17:49; classical ML
  moonshot receipts, section 2c); free_lane_queue (17:24; 0 files at my count, drained);
  person_mine (13:08; two dossiers, section 2c); ractor_engine (12:44; external-steal ractor
  FOLDED at 1f0383d59, section 2c, collision resolved); residue_probe_20261007 (12:10;
  PREREG + results + RECEIPT + paste-ready reply, section 2c); hermes_burn (05:40; the 402
  wall + A2/A3 drafts, via frontier_olm_2026-10-07/lens/burns.md:196-198).
- 10-06: frontier_olm_2026-10-06 (22:14; the day-6 mine, section 2a); gauntlet (20:13;
  via frontier_olm_2026-10-07/lens/burns.md:122-126); selfimp (16:41; imp002 dogfood, via
  frontier_olm_2026-10-07/lens/burns.md:181); mates_leave_protocol (08:35) and
  ouroboros_20261005 (07:37) (dispositions via frontier_olm_2026-10-07/lens/burns.md:181-187).

## 4. Resolved since the 10-07 lens (do not re-open) and what stays owed

Resolved this window, each with its carrier:

1. Shell door containment: the day-7 named finding (UNCONTAINED, frontier_olm_2026-10-07/
   DIGEST.md:25-33) is contained by port wave P4 (6685db6bc; watch/inbox/port_wave_20261007/
   p4_shell_door.md, my listing; AST gate + win32 Job Object + loud-exit-125 canary).
   Re-running the escape probe to "discover" the hole is re-banking; dogfood the canary
   instead.
2. External-steal ractor: was in flight at the prior lens (via frontier_olm_2026-10-07/lens/
   burns.md:191-195), now FOLDED at 1f0383d59. Cite it, do not re-derive its attack pages.
3. GPS-embed: pulled, wired, measured, KILLED by its pre-registered falsifier (9b72d287c).
4. Citation-drift wave: 3 more debts accepted by name at the 10-08 patrol (31edc2309,
   baseline 72). Whether that discharges the 3 PHANTOM-NUMBER blockers at AGENTS.md:29 (via
   frontier_olm_2026-10-07/lens/burns.md:224-225) is NOT verified by me this sitting; check
   the gate output before a push, do not assume either way.

Still owed (all still open at this fold; no evidence any fired):

- The qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B: the spec was AMENDED by P6
  (QUANT_AB_SPEC_AMEND.md, my listing; 6685db6bc "quant A/B four-pinned-choices spec"), the
  A/B itself has no run receipt I found. Owed.
- Manufacture n>=40 fleet-labeled rows so the decision-model meter is ever valid
  (frontier_olm_2026-10-07/DIGEST.md:15, probe queue :97-108).
- Probes 1-9 of the day-7 probe queue as printed (frontier_olm_2026-10-07/DIGEST.md:97-108):
  all PROPOSED as of that fold; I re-ran none.
- The van Voolen page-tier receipt (login-gated, ledger line 705).
- DeepSeek invoice-strength discount check and the Featherless 28.6k-row gap (via
  frontier_olm_2026-10-07/lens/burns.md:221-223).
- The day-5 88-item confirmation pass (via frontier_olm_2026-10-07/lens/burns.md:220-221).
- GSTD wallet addresses (operator input; 7b4d86bad).
- The provenance re-audit of the five unre-audited kv-cache lane items and the day-5
  memlance falsifier reconciliation (frontier_olm_2026-10-07/DIGEST.md:90; frontier_olm_2026-
  10-06/DIGEST.md:82).

## 5. Anti-rebank rules for the next window

1. The banked set is the union of: the inherited set (section 2a), the day-7 register
   (21 rows + 8 cards + DIGEST rev 2, section 2b), section 2c's 30 git-logged commits, and
   ledger lines 666-705 (section 1). Overlap must be stated, never silently re-confirmed.
2. Closed or dead, do not rediscover: Sefer Raziel provenance (green at 1701, ledger line
   705); JSTOR/Kedem/NLI anonymous lanes (ledger lines 699-702); DeepSeek window/off-peak
   (ledger lines 681, 692); Lightning/Chutes/SiliconFlow/Scaleway credits (ledger line 701);
   the shell-door escape as a find (contained, section 4.1); GPS-embed (killed, section 2c);
   the day-7 DIGEST's three unconfirmed items as confirmed rows (section 2b); the day-5
   164.5M phantom headline; the struck Weave Router zero-overlap claim (c7d364ab6, DIGEST
   rev 2 fold annotations).
3. Fire the owed before opening new seams (section 4 list). Cheapest-deterministic first is
   the day-7 queue's own ordering rule (frontier_olm_2026-10-07/DIGEST.md:95).
4. Ledger drift flag, re-armed: memory/burns/LEDGER.jsonl has been byte-frozen since
   2026-10-07 08:09:26 local with max ts 2026-09-28T19:30:00Z (my Get-Item this sitting).
   Two windows in a row now find it frozen; the no-writer-instrument question is a standing
   incident per frontier_olm_2026-10-06/DIGEST.md:83 until an owner mints a writer or takes
   the retire decision to the operator.
5. Counts law: every count above is instrument-tagged (PowerShell tail, ReadAllLines count,
   Get-Item stamps, Get-ChildItem walks, git log output, Read line ranges). Do not
   difference counts taken by different instruments at different moments.
