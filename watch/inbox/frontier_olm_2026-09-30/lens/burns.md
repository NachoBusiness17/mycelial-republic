# burns lens 2026-09-30: what was already mined this week, so nobody re-banks it

Lens seat: lens-burns, carrier `watch/inbox/frontier_olm_2026-09-30/`. This continues
`watch/inbox/frontier_olm_20260928/lens/burns.md` (2026-09-28 21:56). Everything below was read
or run in this ask (2026-09-30, repo root). All times on carrier listings are local.

## 0. Commands actually run (the evidence base)

- `wc -l` + `tail -c 8000 memory/burns/LEDGER.jsonl` (693 lines).
- Day-count greps: `grep -c '"ts": "2026-09-30' ...` = 0, `2026-09-29` = 0, `2026-09-28` = 45,
  `2026-09-2[4-7]` = 648 (sums to 693, so the file holds nothing but 09-25..09-28).
- Full parse via a temp parser `watch/inbox/frontier_olm_2026-09-30/lens/tmp_lens_burns_20260930.py`
  run as `./.venv/Scripts/python.exe <script>` (venv per AGENTS.md; script spawns no subprocess),
  then deleted: 693 rows, 0 parse fails, per-day/per-slug/verdict aggregation, latest row per
  standing lane, and an `os.scandir` census of `watch/inbox` dirs with mtime >= 2026-09-28 00:00
  local plus per-dir `os.listdir` peeks. Raw output: the transcript of this ask.
- Byte-backs: line counts of the prior olm registers (`register.jsonl` = 21 rows,
  `percolator_candidates.jsonl` = 5 rows, confirming `frontier_olm_20260928/DIGEST.md` claims).

## 1. Ledger state: NOTHING new banked since the 09-28 lens. Do not re-mine it, do not re-lens it.

- `memory/burns/LEDGER.jsonl`: mtime 2026-09-28 13:15:27 local, 562,938 bytes, 693 rows, 0 parse
  fails, max ts 2026-09-28T13:45:00Z (line 693). Zero rows dated 09-29 or 09-30.
- Therefore the 2026-09-28 burns lens is still the current, complete picture of burn-mined work.
  Its standing-lane table and the 09-26 mega-wave section remain authoritative. A fresh sweep
  that re-derives those lanes is re-banking.
- Day shape (rows / distinct slugs): 09-25 = 23/10 (ledger lines 1-23), 09-26 = 517/455
  (lines 24-540, the B2-NNN mega-wave), 09-27 = 108/28 (lines 541-648), 09-28 = 45/5
  (lines 649-693). Verdict histogram highlights: 310 `LANDED` + 19 `landed` + landing variants,
  200 `steal`, 21 `green`, 7 `vacuous`, 8 `built`, plus per-row custom verdicts.
- 449 of the slugs are one-row one-shot items; 14 lanes carry >= 4 rows each (section 2).

## 2. Standing burn lanes (>= 4 rows in this ledger), latest state per lane

Counts and latest rows re-derived by this seat's parse (exact-slug census; the 09-28 lens grouped
some alias slugs, e.g. its judge-lane-spec "12" included +deep-dive/+correction slugs, mine
counts the bare slug at 10):

| lane | rows | span | last burned | latest verdict | latest landing |
|---|---|---|---|---|---|
| free-resource-landscape | 35 | 09-25..09-28 | 09-28 13:20Z | green | `watch/inbox/BURN_free-resource-landscape_20260928_n.md` |
| middle-path-doctrine | 30 | 09-26..09-28 | 09-28 11:55Z | green | `watch/inbox/BURN_middle-path-doctrine_20260928_k.md` |
| doctrine-owed-chase | 26 | 09-26..09-28 | 09-28 13:45Z | green | `watch/inbox/BURN_doctrine-owed-chase_20260928_m.md` |
| world-models-multi-agent | 19 | 09-25..09-28 | 09-28 01:20Z | green | `watch/inbox/BURN_world-models-multi-agent_20260928_d.md` |
| stego-canon-pipeline | 19 | 09-25..09-28 | 09-28 00:00Z | green | `watch/inbox/BURN_stego-canon-pipeline_20260927_j.md` |
| third-way-game | 17 | 09-26..09-27 | 09-27 14:20Z | green | `watch/inbox/BURN_third-way-game_20260927_d.md` |
| adversarial-self-probes | 15 | 09-25..09-27 | 09-27 21:45Z | green | `watch/inbox/BURN_adversarial-self-probes_20260927_h.md` |
| rsi-harness | 12 | 09-25..09-27 | 09-27 12:30Z | green | `watch/inbox/BURN_rsi-harness_20260927_g.md` |
| queue-field | 11 | 09-25..09-27 | 09-27 10:30Z | green | `watch/inbox/BURN_queue-field_20260927_d.md` |
| steering-theory | 11 | 09-25..09-27 | 09-27 08:40Z | green | `watch/inbox/BURN_steering-theory_20260927_b.md` |
| b2-wave-fold | 11 | 09-26..09-27 | 09-27 12:00Z | green | `watch/inbox/WINDOW_CLOSE_20260927_MORNING.md` |
| judge-lane-spec | 10 | 09-25..09-27 | 09-27 08:40Z | green | `watch/inbox/BURN_judge-lane-spec_20260927_c.md` |
| prompt-uplift-lane | 8 | 09-25..09-27 | 09-27 04:15Z | green | `watch/inbox/BURN_prompt-uplift-lane_20260927.md` |
| atlas-fix-queue | 4 | 09-27 | 09-27 03:40Z | retired | `watch/inbox/LIBRARIAN_RETIRED_20260927.md` |

Lane-state one-liners (do not re-derive, read the landings):
- free-resource-landscape: board consolidation green-solved pending next churn (LLM7 free-class
  4 to 3, GLM-5.3-Flash dropped, DeepSeek 401-alive, Featherless 22,059 served rows vs 28.6k
  counter gap, Lightning lane closed FULLY DEAD, credits still-owed dashboard-gated).
- doctrine-owed-chase: Amsterdam-imprint/chronogram topic CLOSED green-pending-chronogram; the
  year-chronogram is a formally OWED single-scope debt needing a higher-res scan.
- middle-path-doctrine: X6 window audit green, 7/7 scenario cards fleet-cited, 12 days to
  2026-10-10, zero die-conditions armed.
- stego-canon-pipeline: end-to-end routing drill green on the live 4-entry dictionary; the
  drop-#874/#1104 misidentification erratum already propagated 09-26.
- world-models-multi-agent: research seat fix landed (`mag/run_trail.py:61`), driver restart
  still NOT done as of last row.

## 3. Frontier mining already banked this week: the whole prior olm carrier

`watch/inbox/frontier_olm_20260928/` (created 09-28 21:50, mtime 09-29 21:09) is the week's
frontier mine and this ask's own predecessor. Per its `DIGEST.md` (41,801 B) with this seat's
byte-backs on the registers:

- Window mined: 2026-08-29 to 2026-09-28.
- Sweep: 8 areas x 4 doors (arxiv, hn, reddit, x), 32 return files in `sweep/`, all ok:true.
  Areas: open-and-local-language-models, quantization-compression, agent-memory-continuity,
  swarm-orchestration, finetuning-and-adaptation, kv-cache-context-engineering,
  evals-self-improvement, inference-efficiency. Raw fetch receipts in `sweep/_raw/`, plus
  pullpush JSON dumps (`pp_*.json`) for reddit.
- Findings: `register.jsonl` = 21 rows = 21 confirmed finds (count re-run this ask); 3
  unconfirmed items with evidence noted in DIGEST.md; one carried-forward refutation
  (PolAgentBench CC0 attribution FALSE, repo is MIT code + CC BY 4.0 data).
- Steals: `percolator_candidates.jsonl` = 5 rows; 13 steal cards in `steal/` (the 5 folded plus
  prior-cycle and via-door variants), topics mirroring the 8 areas.
- Headline already folded (DIGEST.md executive summary): the percolator promote gate is a bare
  counter (`mag/percolator.py:264-272`) while the estate's own paired-blind gate exists
  unwired (`mag/seed_percolator.py:6-16`); certified-decision acceptance (REUSE, arXiv
  2609.33180) is the named upgrade path.
- A today-sweep over the same 8 areas x 4 doors with the same date window would be a re-bank.
  Overlap against `register.jsonl` row ids/titles is the cheap dedupe.

## 4. watch/inbox carrier directories, last three days (mtime >= 2026-09-28 00:00 local)

New carriers (created inside the window), from the scandir census:

| dir | created | mtime | entries | shape (peeked filenames only, contents NOT read) |
|---|---|---|---|---|
| `frontier_olm_2026-09-30/` | 09-30 12:35 | 09-30 12:35 | 1 | this carrier; sibling lens files `corpus.md`, `doors.md` already present |
| `last_mile_20260930/` | 09-30 05:38 | 09-30 09:32 | 127 | AA1..AC12+ last-mile wave receipts (Opus refire, cleanup, worldgen, doctor, HUD, merge fix, RL reward, oral law) |
| `hydrology/` | 09-29 23:13 | 09-30 06:31 | 40 | X1-X12 + Y-series items (airflow, gps feed, duel series, propagator, motion) |
| `water_engineering_20260930/` | 09-29 22:32 | 09-29 22:41 | 5 | WA-WF briefs (HVAC archaeology, water organ census, k8s-as-water, synthesis) |
| `mates_leave_protocol/` | 09-29 21:04 | 09-29 23:25 | 17 | W3A-W3T wave receipts + NIGHT_BURN output 20260930 |
| `operator_model/` | 09-29 21:07 | 09-30 08:10 | 8 | DECISIONS, INTERRUPTS, OCEAN, OPERATOR_CARD_V2, ORAL_LAW dedupe/index, STEER |
| `mountain_climb_ractor_20260929/` | 09-29 14:41 | 09-29 23:49 | 10 | ractor essay set (FRAME, 4 LENS_*, GRADED, SYNTHESIS, FINAL_PIECE) |
| `gps_baseline_ractor_20260929/` | 09-29 14:03 | 09-30 08:06 | 7 | baseline spec/quality, SEAT_A/B/C, JUDGED, RECEIPT |
| `ball4/` | 09-29 17:46 | 09-29 18:05 | 4 | frontier-lab intel: capital-policy, compute, defense-enterprise, models (receipts in `gala_20260925/`) |
| `ball3/` | 09-29 14:38 | 09-29 15:16 | 3 | driver-meter, live-state, quantizer-fallout |
| `game_platform_essay_20260929/` | 09-29 12:18 | 09-29 12:31 | 9 | essay set (LENS_ARCHITECT/ECONOMIST/MECHANIC, GRADED, SYNTHESIS) |
| `PHONE_RECOVERY_20260929/` | 09-29 12:32 | 09-29 12:34 | 1 | METHODS.md |
| `ball2/` | 09-29 10:34 | 09-29 11:49 | 11 | abliterate p1 (+runs banks), attention-ledger, bare-spawn-descent, driver-v2, fold-gate, mcp-bridge, quantizer-hygiene |
| `selfimp/` | 09-29 11:39 | 09-29 11:40 | 1 | imp001.md |
| `GSTD_RESEARCH_20260929/` | 09-29 10:10 | 09-29 10:25 | 3 | comparables audit, public footprint, verdict |
| `RAINBOW_ROAD_RACTOR_20260929/` | 09-29 09:46 | 09-29 10:58 | 9 | ractor essay set |
| `Q_OPERATION_RACTOR_20260929/` | 09-29 08:46 | 09-30 11:52 | 12 | ractor essay set + RAINBOW_CLAIMS_AUDIT + REPLY_TRUMP_SI |
| `game_platform_basecamp_20260929/` | 09-29 08:28 | 09-30 05:26 | 51 | basecamp: botsport ledger, cost model, delegation research, lanes, gopher burn outputs |
| `wave5_repair/` | 09-29 05:53 | 09-29 08:58 | 13 | repair wave: patrol-fix, suite-burn, queue-closes, dna-repair, stealth-tools, mcp-pin-wire, etc. |
| `seed_rib_20260929/` | 09-29 06:26 | 09-29 06:26 | 1 | seed-rib/ subdir |

Older carriers still touched inside the window (created earlier; recent mtime):

- `secret_gate_results/` (created 09-26 23:44, mtime 09-30 12:30, 197 `changed_*.json` watch
  snapshots, still being written).
- `burn_wave_20260926/` (created 09-26 07:23, mtime 09-30 11:52, 771 entries): the B2-NNN
  mega-wave index. Primary do-not-re-mine surface for the week (455 one-shot slugs).
- `gala_20260925/` (mtime 09-29 18:39, 21 entries incl. ball/ball3/ball4 subdirs + receipts).
- `union_fullsend_20260917/` and `transcripts/` (mtime 09-30 11:52), `fifty_wide_20260917/`
  (mtime 09-28 15:09), `burn_reset_20260927/` (mtime 09-28 12:36).

Top-level 09-29/09-30 receipt files worth knowing exist before filing anything similar
(filenames/sizes from the dir listing, contents not read): `DAY_SYNTHESIS_20260929.md` (14,676B),
`MICKEY17_WAVE_LEDGER_20260929.md` (99,306B), `W1_REPRINT_HARNESS_20260929.md` through the
W3* series (lane-gap briefs, 09-29 20:24..22:41), `TIE_IT_ALL_20260930.md`,
`COVERAGE_GAPS_20260930.md`, `MORNING_REPORT_20260930.md`,
`MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md` (37,415B), `AI_WELFARE_DOSSIER_20260930.md` (61,200B),
`DRIFT_PATROL_20260930.md`, `STEALTH_SWEEP_LATEST.md` (09-30 09:50), `DATED_METERS.jsonl`,
`STEALTH_MINED_FINDINGS.jsonl` (157,803B, 09-30 12:19), `PACK_OFFLOAD.jsonl` (09-30 11:58).

## 5. OWED / not done by this seat (stated, not guessed)

- Pre-rotation burn ledger (weeks before 09-25): still not located; the file is entirely
  09-25..09-28 (grep counts in section 0). Week claims are scoped to these 693 rows.
- Contents of the section-4 carriers were NOT read; shapes above are filename/size peeks only.
- INDEX.json registration of this lens file: not performed (not asked; the workflow publishes).
- Temp parser `tmp_lens_burns_20260930.py` was created in this lens dir, run once, and deleted
  in the same ask (byte-back counts came from a separate inline venv python -c).
