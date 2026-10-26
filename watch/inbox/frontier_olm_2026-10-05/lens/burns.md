# Lens: burns (what was already mined this week, so nobody re-banks it)

Folded 2026-10-05 morning by the frontier_olm_2026-10-05 burns lens. House laws held: ascii only,
no em or en dashes, every claim cites what was read or run this sitting. Inherited content is
marked "(via ...)" with the source file named, and that file was read in full this sitting without
re-verifying its underlying claims. This lens is the successor to frontier_olm_2026-10-04/lens/
burns.md (read in full this sitting, all 195 lines).

## How this was built (instruments, this sitting)

- The ask's named read: tail of `memory/burns/LEDGER.jsonl` via the repo venv python: row count
  693, last 8 rows read (lines 686-693, one_line fields truncated at 600 chars in the read), last
  ts 2026-09-28T13:45:00Z (line 693). `Get-Item` on the file: Length 562,938 bytes, LastWriteTime
  2026-09-28 13:15:27 local, byte-identical moment to what the 10-04 lens reported (via
  frontier_olm_2026-10-04/lens/burns.md:16-19).
- Ledger histograms run this sitting over all 693 rows: by day 09-25 = 23, 09-26 = 517,
  09-27 = 108, 09-28 = 45, zero rows after 09-28; verdict counter LANDED 310, steal 200, green 21,
  landed 19, built 8, vacuous 7, ERRATUM 7, CORRECTION 5, erratum 3, OWED-DORMANT 3, OWED 3,
  done 3, plus about 90 singleton verdict strings (several of which are full sentences pasted into
  the verdict field by the 09-26 wave); fresh_failure_mode true = 113 rows.
- Carrier walk run this sitting: python `os.scandir` over `watch/inbox`, directories by
  max(mtime, ctime) >= 2026-10-03, with per-dir file counts (section 4).
- Read in full this sitting: frontier_olm_2026-10-04/lens/burns.md (195 lines);
  frontier_olm_2026-10-04/DIGEST.md tail (last 45 lines: sections 4.5, 5, 6); the 10-04 carrier's
  register.jsonl and percolator_candidates.jsonl row counts plus the last register row's head;
  ribvault_20261005/R062_FREE_USAGE_RESOLVE_20261005.md (all 84 lines); ribvault probe_summary.json;
  the three free_lane_queue/20261005-r2gap-*.json cards; heads of
  ouroboros_20261005/r1_land_width_headers.md (16 lines) and build_wave_20261005/b9_doors_tier.md
  (18 lines).
- `git log --since="2026-10-04 10:00"` (section 5, hashes and messages mine this sitting).
- Dirs/files LISTED only (names + mtimes, bodies unread unless named above): the 10-04 carrier's
  sweep/ tree (8 areas x 4 doors, 32 sweep .md files + harvest jsonl dumps), go_wave_20261004,
  night_shift_20261004, replay_flash, replay_deepseek_thinking, replay_fable, replay_grok47,
  social_rsi, reboot_patches_20261003, buildall, local_fanout, dd_dogfood, hitler_dig, playground,
  model_garden, hermes_burn, execute_register_seed_fidelity.

## 1. The burns ledger is silent day seven

`memory/burns/LEDGER.jsonl` holds 693 rows spanning 2026-09-25T10:05:50Z (line 1, via
frontier_olm_2026-10-04/lens/burns.md:16-17) to 2026-09-28T13:45:00Z (line 693); the file is
untouched since 2026-09-28 13:15:27 local (my Get-Item read this sitting matches the 10-04 lens's
report exactly, so nothing was appended since that lens read it). My own tail read corroborates the
terminal rows: line 693 is doctrine-owed-chase CLOSED green-pending-chronogram (Sefer Raziel
year-chronogram FORMALLY OWED, the 885,009-byte plate JPEG is the resolution ceiling), line 692 is
free-resource-landscape board-consolidation GREEN (LLM7 free-class 4 to 3, GLM-5.3-Flash dropped
from the roster, first churn in five intervals), lines 686-691 are the Lightning pass k/l/m
closures (lane FULLY DEAD with Chutes/SiliconFlow/Scaleway) and the Amsterdam-imprint byte-back
plus the req-35004 Rubinstein-reprint correction. Full fold of lines 654-693 is via
frontier_olm_2026-10-04/lens/burns.md:51-78 (that lens read all 40 tail rows; its line-number map
matches my read at 686-693). Until the ledger resumes, the carrier DIGEST/RECEIPT pairs and git
log are the mining record.

## 2. The mined-set registry (the union nobody may silently re-confirm)

- **Rounds 1-2 (frontier_olm_2026-10-03 carrier):** register.jsonl 42 rows / 41 distinct finds,
  percolator 9 rows, steal 9 cards; round-2 added register rows 24-42 (list via
  frontier_olm_2026-10-04/lens/burns.md:90-99) and held 5 UNCONFIRMED items out (via
  frontier_olm_2026-10-04/lens/burns.md:100-106). Counts re-verified 2026-10-04 by the 10-04 lens
  (via frontier_olm_2026-10-04/lens/burns.md:26-29, 87).
- **Day-4 mine (frontier_olm_2026-10-04 carrier, extended overnight into 10-05):** the 10-04 lens
  was written 10-04 10:34 and covered only the morning carrier; the carrier then grew a full
  sweep/ tree (8 areas x 4 doors, mtimes 10-04 11:22 through 10-05 00:41), 10 steal cards
  (steal/*.md, 10-04 18:40 to 10-05 00:41), and its own fold outputs rewritten 10-05 01:19-02:31.
  Counted this sitting: its register.jsonl = 22 confirmed-find rows, percolator_candidates.jsonl =
  10 rows. Its DIGEST section 6 declares register confirmed-only by design; the 2 UNCONFIRMED
  items live only in DIGEST section 5: U1/U2, both Jeff fine-tune threads (1wspn24, 1wv05u1),
  U2 CONTRADICTED on the quantized-threshold claim and parked with a rewording condition. Commit
  17225e37e (10-05 02:40) is the bank row: 32/32 miners, 22/24 finds independently confirmed.
  Headline steals already banked there, do not re-mine: TV-flip pre-gate for the quant lane
  (2610.00694); strict-prefix cache-resume receipt law (2609.15030); agent-memory addressability
  law (rows-and-views, knowledge_graph.py:102-173 builder defects); Goodhart
  statistical-collapse as percolator review fields; centralized merge turn (Google 180-config,
  +80.9 pct, 17.2x vs 4.4x) onto memweave.consensus_quality; REGEXROUTE (128 regex features,
  encoder parity sub-ms); fetch-before-bank with KILLs banked first-class (daymora fabrication
  caught); AQLM method-tier rule plus the backend-tier census field.
- **The 11 ranked next actions** (via frontier_olm_2026-10-04/DIGEST.md section 4.5, read this
  sitting): KV-generation-mismatch replay; graph-builder one-line fix + regenerate; REGEXROUTE
  harvest + k=32 head; FT-never-first compile-path probe; OpenRouter key-counter logger; the
  scoped qwen2.5:7b Q4_K_M vs q8_0 A/B; TV-vs-root pre-gate; reasoning-quant ladder; consensus
  merge actor battery; ratchet cure-rate census; four fetch OWEDs (CliffCompaction 2609.26779,
  funes repo, EXL2/EXL3 primaries, Clef license page). Firing these beats re-mining their subjects.

## 3. Carrier directories, last three days (my walk this sitting, max(mtime,ctime) >= 10-03)

**Created 10-05 (6):** frontier_olm_2026-10-05 (this run; lens/ holds three _*.py helper scripts
plus this file); free_lane_queue 08:06 (3 probe cards r2gap-01 fold-de-blind, r2gap-02
stop-cert-zombie, r2gap-03 seal-hex-case, all read this sitting: free-lane SENSING probes for the
three held post-executor items named in commit 23d76bb71); ouroboros_20261005 06:44 (3 r1_land
files: parameterized, skeletons, width_headers; head read: 19/19 saved workflows now declare
max_concurrency, olm-mine 191.8M phantom struck); build_wave_20261005 03:26 (20 files, lanes
b1-b9: knowledge graph, cache receipt, merge actor, KV sweep with llama-server raw logs, strip at
use, CRLF patrol, sweep, gwap, doors+tier; b9 head read: fetch-before-bank X-door recipe ported
into .agents/skills/frontier-mine/SKILL.md); ribvault_20261005 01:49 (R062 free-usage probe
receipt, read in full, section 5 below); execute_register_seed_fidelity 02:36 (actor table +
audit_join script + fidelity_3484c5eb.md, listed).

**Created 10-04 (6):** frontier_olm_2026-10-04 (the day-4 carrier, section 2); go_wave_20261004
04:33 (19 files: WAVE_FOLD.md + 15 receipts incl prepush_instruments, gps_dedupe, fifty_wide_guard,
d4 thinking probes + CSV_VERDICT + KEY_SCRUB; LISTED only here and via
frontier_olm_2026-10-04/lens/burns.md:128-136); night_shift_20261004 04:32 (10 receipts:
estate_index_compaction_design, quantized_lattice_fold, verkle_vs_embedding, worldline_compact_tool,
leave_dispatcher_cured, night_march_cured, research_rotation_cured, skill_reform x2,
free_liveness_0430; LISTED); replay_fable 18:20 (REPRINT_INN_spec + THE_MERGE_spec);
social_rsi 06:45 (BUILD_RECEIPT + errno22-cage draft + 3 packet files, LISTED via the 10-04 lens);
replay_grok47 06:30 (0 files, empty).

**Created 10-03 (9):** frontier_olm_2026-10-03 (the rounds-1+2 fold carrier); reboot_patches_20261003
23:08 (APPLY_ORDER.md + 5 .diff patches, LISTED); replay_flash 11:56 (15 files);
replay_deepseek_thinking 14:45 (18 files; several 0-byte: KABUKI_FACES_fold, MOCAP_BUILD_spec,
REPRINT_INN_spec, SUBSTANCE_48h_synthesis); buildall 17:28 (7 files + music-cuts subdir);
local_fanout 18:20 (5 request jsons); dd_dogfood 14:59 (10 lanes, 52 mined rows, commit add33ba72,
via frontier_olm_2026-10-04/lens/burns.md:140); hitler_dig 07:39 (2 files, dead end via
frontier_olm_2026-10-04/lens/burns.md:182); playground 07:39 (119 files).

**Old carriers touched inside the window (not new mines):** secret_gate_results, ractor_engine,
endpoint_news, burn_wave_20260926, audit_20260926, hermes_burn (10-04 18:35), model_garden
(10-04 11:03), gala_20260925, 48h_synth, gap_analysis_20261001, xai_grok47. The replay_* dirs are
model-replay artifacts of already-banked session content, not new frontier finds (via
frontier_olm_2026-10-04/lens/burns.md:142-143).

## 4. Fresh instruments this week that close questions (do not re-run at these shapes)

- **R062 free-usage resolve (ribvault_20261005, read in full this sitting):** the D3
  policy-vs-evidence contradiction is RESOLVED CONDITIONS-BOUND. 52 asks, one OpenRouter key,
  2026-10-05T05:37-05:44Z: drip rate (width 1, 4s spacing) = zero 429 across 13 lanes; forced
  instantaneous width 13 = 2/39 429s, both poolside/laguna-xs-2.1:free, upstream rate-limit.
  200-EMPTY is NOT a clean throttle signal at this probe size (max_tokens 16 reasoning burn);
  only the hard 429 class adjudicates. Freshness fact: inclusionai/ling-3.0-flash-fin:free is
  retired from the free tier (404 x3, R062 line 44-47).
- **B4 measured KV sweep (build_wave_20261005/b4_kv_sweep.md + raw llama-server logs, LISTED;
  verdict via commit e80f48b8f):** q8_0 decode 100.8 vs f16 55.9 t/s, quant KV doubles decode
  costs prefill; kv_slot_pilot unblocked. This is the same animal as round-2 probe 5 (the scoped
  qwen2.5:7b Q4_K_M vs q8_0 A/B still owes its own run) but the first measured KV numbers exist.
- **24/7 free-lane fleet armed (commit e80f48b8f):** tools/free_lane_fleet.py over 7 live free
  providers, Windows task MagFreeLaneFleet every 30 min, validation cycles banked 4 -> 6 -> 11
  findings per cycle. Free-lane output is SENSING-class per the driving ladder; do not re-argue
  whether the fleet should exist.
- **Ouroboros R1 (commit 23d76bb71):** 79 findings, amendment table executed; tier-1 merge clause
  in 3 skeletons (E26 data-destruction vector); mickey17-burn.dwf.ts parameterized consolidation,
  gate PASS 423db130b866; 19/19 max_concurrency declarations; olm-mine 191.8M phantom STRUCK per
  ERRATA 001 (also struck in the day-4 fold; the struck number appears in no living claim).
- **Eleven-doors ledger (commit d1b1d6812, 10-04 14:48, then the wave):** 113 findings survived
  hostile pass; doors D3, D5, D6, D7, D8, D10, D11 landed 10-05 with receipts
  (watch/inbox/D3_CLIPPY_PROBER_20261005.md, D5 via commit 3b271d44c,
  D6_MONOCULTURE_PROXY_20261005.md, D7_PHEROMONE_METABOLISM_20261005.md,
  D8_DECAY_FAMILY_LINEAGE_20261005.md, D10_WELD_RACTIVE_20261005.md,
  D11_QUERY_BROKER_20261005.md), EG-20 resurrected and landed (EG20_PASSATK_LANDED_20261005.md,
  pass@K: all-fleet 0.586 vs best single 0.500 on arena-agreement-v1, cheap mesh 0.349 < frontier
  0.500 = ROUTE_FRONTIER); D9 half-1 agentmemory pin landed (commit de0f6a870); D12 backfill and
  D13 parked are OPERATOR-GATED; Gero-4B calibrator operator-sitting (commit f94adae8d).

## 5. Already banked TODAY (10-05) and late 10-04, from git log this sitting: do not re-mine

- Commit flood 10-05 09:01-09:56: D3 clippy-prober (6c7060a8e), D10 beat-indexed ractive
  (515e2baec), D11 three-signal query broker (6ed614399), D8 decay-family lineage (7dac8685e),
  D9 agentmemory pin (de0f6a870), COMPUTE GRIND CLOSE (f94adae8d), PRE-REBOOT HANDOFF
  (a8304c4b3), ARENA DAYS 1-3 estate state (9dbe3df40), drift-patrol 10-05 (347e7581f).
- 10-05 03:00-08:30: free-lane fleet + build wave 9/9 (e80f48b8f), night-shift close 4 doors
  (55bcac38b), D5 errno22 disposition + twin-site cure (3b271d44c), D6 (7bf3bcec8), D7
  (ae2712f89), EG-20 (f7f6b6e2b), D8 (7dac8685e), night loop armed R1 (139f5198f), ouroboros R1
  (23d76bb71), doors-ledger re-land under tracked path case (9d3b4b572; new law banked: match
  git ls-files case before adding on case-insensitive filesystems).
- 10-05 00:44-04:23 X intel, all verified-primary and banked: marfinxx GPT-6-Astra fabrication
  caught, real paper is 2608.05643 (abd480910); contrastive weight steering 2511.05408
  (ce0c67221); looped transformers shared memory 2610.02383 (bebe6a98c); OverAct 2610.01508 +
  Edwin Chen agentic-RL 2610.00890 + Harness Engineering Handbook + OpenScholar staleness
  (55b4c532c); Sigma 2610.02665, NHA 2510.07019, ReFlux 2609.32457, Uber MCP Gateway (1e4c5d0b4);
  Kelly photonic slab 2610.01473 tri-stated VERIFIED-REAL (6d044be47); imcaiden scraping craft
  (731b05b6a); GLM-5.3 substrate cost drop (d7399fb89); VISTA 2610.02200 + light-maze verdict +
  RSR 2610.02826 (9ff5c4157); convergence doctrine banked (316cc26bb).
- 10-04 afternoon/evening: READ-THE-ESTATE 100M, 12 lanes, 60 rows, ESTATE_INDEX anatomy on
  10,661,260 rows, OSError Errno 22 two-writer family 910 rows named largest uncured failure
  (eb687f76a, 21:53); STARTER KIT v0.1, .gitignore, Hermes 68 profiles steal, ARMORY +
  law_gate, 50-wide dogfood receipt, v0.2 fix list (e6d1f3975, d701e9901, f14a72e2b, 2e23f039c,
  c7b3433a0, 229f13173); ractor eleven-doors verdict (d1b1d6812).

## 6. Anti-rebank rules for the next window

1. The banked set is the union of: round-1's 23 finds + round-2's rows 24-42
   (frontier_olm_2026-10-03/register.jsonl, 42 rows) + the day-4 carrier's 22 register rows and
   10 percolator rows (frontier_olm_2026-10-04/) + section 5's git-logged drops + the ledger's
   closed topics (section 1). Overlap must be stated, never silently re-confirmed.
2. Dead ends, do not rediscover: Lightning/Chutes/SiliconFlow/Scaleway free credits; the nine
   HebrewBooks wrong-book closures; the five round-2 unconfirmed items and the two day-4
   UNCONFIRMED Jeff threads (U1/U2, DIGEST section 5 dispositions); Hitler ancestry and
   numerology; every direct reddit door and the X site: filter; the marfinxx GPT-6-Astra pairing
   (fabrication, caught); the olm-mine 191.8M figure (struck); the murmur Hub image name
   (corrected to mumblevoip/mumble-server in 229f13173); lowercase-vs-tracked-case git adds
   (law banked in 9d3b4b572).
3. Fire the owed probes before opening new seams: the 11 ranked next actions (section 2); the
   three r2gap free-lane sensing probes already queued in free_lane_queue/ (fold de-blind,
   stop-cert + fire ledger, seal hex-case); the Sefer Raziel chronogram decode (ledger line 693);
   the DeepSeek invoice-strength discount check (ledger line 680, via the 10-04 lens); the
   Featherless 28.6k-row gap (ledger line 683, via the 10-04 lens); the qwen2.5:7b Q4_K_M vs
   q8_0 A/B in its own scoped shape (B4 measured the KV axis, not this one).
4. The burns ledger is a drift flag, seven days silent. If you bank mining anywhere, either the
   ledger resumes or your DIGEST/RECEIPT pair plus a git commit is the record; do not assume a
   ledger row exists.
5. Counts law: every count above is instrument-tagged (ledger line, python Count output, DIGEST
   line, git log output, os.scandir walk). Do not difference counts taken by different
   instruments at different moments.
