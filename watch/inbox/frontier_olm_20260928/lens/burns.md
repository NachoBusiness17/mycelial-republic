# burns lens 2026-09-28: what was already mined this week, so nobody re-banks it

Lens seat: lens-burns. Sources read this ask (all commands run 2026-09-28, repo root):

- `memory/burns/LEDGER.jsonl` parsed whole via `./.venv/Scripts/python.exe watch/inbox/tmp_lens_burns_20260928.py` (temp parser, deleted after run): 693 rows, parse-fail count 0.
- Per-day counts via `./.venv/Scripts/python.exe -c` census (output in transcript): 09-25 = 23 rows / 10 slugs, 09-26 = 517 rows / 455 slugs, 09-27 = 108 rows / 28 slugs, 09-28 = 45 rows / 5 slugs. Total 693.
- Every row's ts falls between 2026-09-25 and 2026-09-28T13:45:00Z, so the entire ledger file IS this week. Earlier burn history is not in this file (inference: rotated; the `watch/inbox/burn_reset_20260927/` carrier exists, created 09-27 19:10 per dir listing). I did not locate the pre-rotation ledger; treat prior weeks as unverified from this seat.
- Carrier dir census via the same script's `os.scandir` pass (created + mtime for every `watch/inbox` dir with mtime >= 2026-09-25) plus per-dir `os.listdir` content peeks (second temp script `tmp_lens_burns_20260928_b.py`, deleted after run).
- Latest-state one_line extracts per standing lane, same second script.

## 1. Standing lanes: burned to green or near-green already. Do not re-bank.

Fourteen slugs are standing burn lanes re-fired daily. 221 of the 693 rows belong to them; the rest are one-shot wave items (section 2). Per-lane row counts summed from the per-day parse (exact command cited above). Latest verdict and landing:

| lane | rows | last day burned | latest verdict | latest landing |
|---|---|---|---|---|
| free-resource-landscape | 35 | 09-28 | green | `watch/inbox/BURN_free-resource-landscape_20260928_n.md` |
| middle-path-doctrine | 30 | 09-28 | green | `watch/inbox/BURN_middle-path-doctrine_20260928_k.md` |
| doctrine-owed-chase | 26 | 09-28 | green | `watch/inbox/BURN_doctrine-owed-chase_20260928_m.md` |
| stego-canon-pipeline | 19 | 09-28 | green | `watch/inbox/BURN_stego-canon-pipeline_20260927_j.md` |
| world-models-multi-agent | 19 | 09-28 | green | `watch/inbox/BURN_world-models-multi-agent_20260928_d.md` |
| third-way-game | 17 | 09-27 | green | `watch/inbox/BURN_third-way-game_20260927_d.md` |
| adversarial-self-probes | 15 | 09-27 | green | `watch/inbox/BURN_adversarial-self-probes_20260927_h.md` |
| rsi-harness | 12 | 09-27 | green | `watch/inbox/BURN_rsi-harness_20260927_g.md` |
| judge-lane-spec (+deep-dive, +correction) | 12 | 09-27 | green | `watch/inbox/BURN_judge-lane-spec_20260927_c.md` |
| b2-wave-fold (+correction) | 12 | 09-27 | green | `watch/inbox/WINDOW_CLOSE_20260927_MORNING.md` |
| steering-theory | 11 | 09-27 | green | `watch/inbox/BURN_steering-theory_20260927_b.md` |
| queue-field | 11 | 09-27 | green | `watch/inbox/BURN_queue-field_20260927_d.md` |
| prompt-uplift-lane | 8 | 09-27 | green | `watch/inbox/BURN_prompt-uplift-lane_20260927.md` |
| build-fold-verify (+b) | 4 | 09-27 | green | `watch/inbox/BURN_build-fold-verify_20260927.md` |

Current state per lane, from the 09-27/09-28 one_line rows (ledger ts as cited):

- **free-resource-landscape** (09-28 13:20:10Z, green): board consolidation solved pending next churn. LLM7 free-class 4 to 3 with GLM-5.3-Flash dropped (first churn in five intervals), DeepSeek 401-alive, OpenRouter 460 vs 458, Featherless 22,059 vs 22,054. Standing debts named: DeepSeek in-window hammer, Featherless 28,542-row gap, Groq row carried. Re-banking any free-tier roster census without re-probing is a duplicate.
- **doctrine-owed-chase** (09-28 13:45:00Z, green): the Amsterdam-imprint / chronogram topic is CLOSED green-pending-chronogram. Imprint byte-backed from the archive.org 885,009-byte plate JPEG (resolution ceiling); year-chronogram is a FORMALLY OWED single-scope debt (needs a higher-res scan), falsifier receipt carried in landing `_l.md`/`_m.md`. Sefer Raziel archive candidates were already byte-closed as identity mismatches (09-27 row). Do not reopen the same archive.org hunt.
- **middle-path-doctrine** (09-28, green): X6 window audit, 7 of 7 scenario cards cite byte-verified fleet FAIL rows per AMD-1, suite exit 0 read-only, 12 days to 2026-10-10, zero die-conditions armed. Death-arm twin-key patch already confirmed then closed (09-27 row).
- **stego-canon-pipeline** (09-28, green): first end-to-end routing drill green against the live 4-entry dictionary; sole open item is the sense-blind exact-name leg pending the pass-h sense-field build. The drop-#874/#1104 misidentification erratum already propagated 09-26 (row `B2-93-stego-erratum-20260926`).
- **world-models-multi-agent** (09-28, green): research seat fix landed (`mag/run_trail.py:61`, `_SEAT_MAP += research`), stale-import CONFIRMED by timestamps, driver restart required and NOT yet done. The diffs were sized byte-exact 09-27 (`mag/lane_runner.py:109` setdefault, `context_pack.py:601` filter).
- **rsi-harness** (09-27, green): LAW-12-AMD-1 application verified complete; disclosed gap: no applier receipt field exists. Scenario-gate card suite runs exit 0 read-only.
- **judge-lane-spec** (09-27, green): B2-111's V2 emitter is real at `mag/lane_runner.py:301-326` but has zero production callers, so "dormant-until-V2" is the corrected wording.
- **queue-field** (09-27, green): drain holds byte-stable, 3 closed / 39 open / 8 superseded of 50, Q-029/Q-044/Q-045 queue-owner closes verified.
- **steering-theory** (09-27, green): drift.py + probe20 verified live (gps_50 corr 0.1807, noise-floor override on demo2, VACUOUS kill on demo3); canon pair A/B series still empty, live cycle collection owed.
- **adversarial-self-probes** (09-27, green): 40-row catch hunt drew clean (20 checks, 0 warns); B2-303 twelve pollution rows and B2-427 25-vs-30 REGISTRY growth both ruled designed, 0 true mismatches.
- **third-way-game** (09-27, green): spec READY for the one build pass; 4/4 patch items verified pure additions against stub bytes.
- **prompt-uplift-lane** (09-27, green): roblox/prompts V2 amendment laws hold under fresh 2026 search; DeepEval and PEEM leads filed owed at snippet level.
- **b2-wave-fold** (09-27, green): window closed clean; owed list ledgered for the fresh window (State XI fire 2, Featherless recon tool, generic close mode, LLM7 unlisted ids and more).
- **build-fold-verify** (09-27, green): all four claimed builds byte-verified on disk, zero NOT FOUND.

## 2. The 09-26 mega-wave: 455 one-shot items, banked. Do not re-bank.

09-26 alone carries 517 rows / 455 distinct slugs. The overwhelming shape is `B2-NNN-<topic>` items landed under `watch/inbox/burn_wave_20260926/` (verdict strings "LANDED" throughout the parse). Anything with a `B2-NNN` id from 09-26 is already filed there; a fresh frontier sweep should treat that directory as the primary index, not re-mine it. Notable non-LANDED outcomes worth knowing so they are not "rediscovered" as open: B2-125 bridge GO BLOCKED, B2-113 cascade falsifier UNDECIDABLE-OWED, B2-326 qlora smoke OWED, B2-175 shadowledger datastore leg scheduled Sep-29, B2-470 links dedupe OWED, B2-349 rotation OWED-OPERATOR-GATED, B2-264 links seal OWED-PARTIAL, B2-195 and B2-449 OWED-DORMANT, B2-443 dwf error census LANDED-CENSUS-AS-RECORD, B2-484 law12 clause PASS (filed 14 days early).

## 3. watch/inbox carrier directories created in the last three days (2026-09-26 through 09-28)

From the scandir census (creation timestamps listed verbatim):

| dir | created | contents (peeked via os.listdir) |
|---|---|---|
| `burn_wave_20260926/` | 09-26 07:23 | the B2-NNN mega-wave receipts (section 2) |
| `play_as_work_20260926/` | 09-26 11:41 | 5 files: BRIEF_v4_full, BRIEF_v6_master (62,831B), MASTER_BUILD_NOTES_v6, STEAL_RECEIPT, VERIFICATION_v6 |
| `noir_gwap_steal_20260926/` | 09-26 12:20 | 8 files: STEAL_PACK, REPORT_noir_shaders (10,720B), REPORT_gta_lineage, REPORT_design_precedents, REPORT_destruction_tech, HOPPER_RENDER_HARDWARE_VERDICT, SUBSTRATE_DECISION, drop_evidence_gta_video_thumb.jpg |
| `asekin113/` | 09-26 14:56 | 3 files: GRADING_LEDGER.jsonl, GRADING_VERDICT.json, WINDOW_CONVENTION_20260926.json (this is the asekin grading ledger B2-24 named as owed) |
| `full_blast_20260926/` | 09-26 19:00 | 17 files: FULL_BLAST md, L00-L11 lane briefs (omniroute, cliproxyapi, 9router, fle_u1, fivem_noir, ue5_destruction, gwap_literature, memos_dreamscapes, provider_terms), PROVIDER_KEY_ASKS |
| `digs/` | 09-26 19:26 | 1 subdir: palworld_breeding |
| `ractor_panel_20260926/` | 09-26 20:19 | 27 entries: burnaudit.final.md (29,198B), credrot.final.md, dfdials.final.md + verdict.jsons, checks/ and cands/ subdirs (the test-census receipt carrier cited in AGENTS.md) |
| `audit_20260926/` | 09-26 20:59 | 28 files: LANE0..LANE10 audit briefs (prior-map-delta 35,263B, dogfood-tools, gate-enforcement, unversioned-risk, history-secrets, stale-receipts, adversarial, plus GATE_DEFECT_ASSIGNMENT_BYPASS_20260927) |
| `tmp_digger_holocure/` | 09-26 21:21 | 0 entries (empty scratch) |
| `digger_ls_18/` | 09-26 22:56 | 35 entries: blr_* wikitext/json dumps (AFK_World, Advent_Calendar, Cash, Codes, Flow, Gamepasses...) |
| `seed_rib_20260926/` | 09-26 23:29 | 18 entries: SEED_RIB_LANDED_RECEIPT.md, build/check scripts, coldseat gemma_2b + qwen2.5_3b run outputs |
| `secret_gate_results/` | 09-26 23:44 | 94 entries: changed_*.json watch snapshots (about 3MB each), still being written (mtime 09-28 21:32) |
| `lens_20260927/` | 09-27 09:39 | 8 files: THE_LENS_20260927.md, ATTIC_ORPHAN_CENSUS.md, DIRAC_GAPS_READ.md, did_census.jsonl + .md, are_inventory.md (141,719B), doctrine_revisit.md, external_links.md (yesterday's lens material; today's frontier_olm lens should not repeat it) |
| `burn_reset_20260927/` | 09-27 19:10 | 13 entries: all_seat.md, desk_baseline.md, dirac_loop6.md, dirac_loops45.md, flash50/ dir, healthz.md, mirror_intro.md, no_win.md, pack_modes.md, probe20_live.md, queue/ dir, substrate.md; mtime 09-28 12:36 |
| `seed_rib_20260928/` | 09-27 23:57 | 1 entry: seed-rib/ subdir |

Older dirs still touched inside the three-day window (created earlier): `gala_20260925/` (created 09-25 22:32, mtime 09-26 14:28), `fifty_wide_20260917/` (created 09-17, mtime 09-28 15:09), `method_card_exp/` (mtime 09-26 01:21), `qdrop_export/` (09-26 16:47), `mrpool_export/` (09-26 15:22), `union_fullsend_20260917/` (09-26 09:53), `four_condition_battery/` (09-25 23:18), `bearableguy_export/` (09-25 15:44), `.mimosa/` (mtime 09-27 01:21).

## 4. OWED / not done by this seat

- Pre-rotation burn ledger for weeks before 2026-09-25: not located, not read. All week claims above are scoped to the current file's 693 rows.
- INDEX.json registration of this lens file: not performed (not asked; the workflow script publishes the path).
- I did not open the 94 secret_gate_results snapshots or the 28 audit_20260926 briefs beyond the directory listing; content descriptions above come from filenames and sizes only.
- Temp parser scripts `watch/inbox/tmp_lens_burns_20260928.py` and `tmp_lens_burns_20260928_b.py` were created, run, and then deleted this ask (watch/inbox root is a shared surface; receipts live here and in the transcript).
