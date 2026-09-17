# CV2_SHADOW_INVENTORY — wave 2026-09-16

Lane: CV2 · Operator: "unowned shadow work" · Mode: READ-ONLY sweep (only this receipt mutates)
Scope: (1) shadow artifacts outside tracked estate, (2) inbox shadow pile (G2: 388 unindexed), (3) unclaimed output dirs.
Verdicts: FOLD (register+file properly) · ARCHIVE (park+hash) · VOID (flag for procedure) · KEEP (already owned).

## Status: COMPLETE — read-only sweep, 2026-09-16 evening

Method notes: INDEX.json is derived from `index_events.jsonl` (156 events, 140 active items, derived 2026-09-16T12:04Z). Top-level inbox holds 440 files (excluding INDEX*/ledger/contract) → **~300 top-level files unindexed**; G2's 388 figure includes subdir piles. Membership test was name-match against INDEX.json; items indexed by hash-only would be miscounted as shadow (caveat).

---

# §1 — Shadow artifacts OUTSIDE the tracked estate

## 1a. Sibling project dirs (`C:\Users\foste\Documents\projects\*`)

| Path | What | Verdict | One command next step |
|---|---|---|---|
| `projects/mag-current-rebuild/` | Full Mag clone (docs-first: AGENTS/CONSTITUTION/THE_MACHINE/TOOLS), last touch Aug 26. Superseded rebuild attempt | ARCHIVE | `git -C ../mag-current-rebuild log -1 --format=%H > ../local_sovereign_agent/.trash/mag-current-rebuild.tip && mv ../mag-current-rebuild ../.trash/` (after hash) |
| `projects/mag-sovereign-kit/` | Earlier Mag distribution (OPEN_MAG.cmd, audit.py, agents/) Aug 2 | ARCHIVE | `sha256sum` manifest → park under `.trash/` or `projects/.trash/` |
| `projects/sovereign-mirror/` | README-only stub, Jul 10 | VOID | `rm -rf` after logging hash of README |
| `projects/embassy-aos/` + `embassy-sandbox/` | Mag-adjacent sandboxes (mag/, conftest, ghost_seat.py), Aug 22 | ARCHIVE | hash + park; check `mag/` for unique modules first |
| `projects/codex_pytest_desk/factory/factory2/factory3/factory4/tier_gate2/3/4/tmp/` (9 dirs) | Codex pytest factory desks, all Aug 6, one day of life | VOID | `rm -rf` batch after `du -sh` log |
| `projects/memory/` (sibling!) | **Shadow twin of repo `memory/`**: `corpus/kungfu/` 3 mp4s (~71 MB) + `runs/astra_world/` (empty) — misplaced video-lane corpus OUTSIDE the durable root | FOLD | `mv projects/memory/corpus/kungfu local_sovereign_agent/memory/corpus/kungfu` + INDEX append |
| `projects/ractor-salon/` | **OWNED, not shadow**: git repo v0.1.0, actively modified tonight (U9 lane builds its MCP server) | KEEP | none — leave alone |
| `projects/mycelial-republic/` | Companion repo, cited in constitution | KEEP | none |
| `projects/field-strike-the-chord/` | Agent-seat dirs (ANTHROPIC/BOLT/BRAVE/CLINE/…), Jul 31 | ARCHIVE | hash + park |
| `projects/audit_prep/`, `audit_prep_verkle/`, `docs_register/` | Tonight-adjacent (Sep 12) audit cells: verkle evidence tables, verified findings, STACK_V1 | FOLD | register in inbox INDEX + move under `watch/inbox/` or `docs/` |
| `projects/teach/f_01..f_08/` | Frame PNGs (frm_*.png) — `scripts/teach_recorder.sh` output (that script is itself orphaned) | ARCHIVE | hash + park, or claim via teach lane |
| `projects/research/` (hermes, cl4r1t4s, system_prompts_leaks_20260912) | Leak/prompt research clones | ARCHIVE | hash manifest → `watch/inbox/steal_research_pipeline/` |
| stray PNGs: `phonesalon_01..07*.png`, `farm_receipt_5554/5556.png`, `headless_receipt_01.png`, `pocketfleet_receipt_01.png`, `runner_debug_01.png` | Sep 4–5 phone-salon + runner debug screenshots loose at projects root | ARCHIVE | `mv` into `watch/inbox/media/` + INDEX |
| debris: `nul` (115 B), `path_to_output_contract_file` (775 B), `msys_proof.txt`, `AGENTS.md.bak-bootapply-20260911` | Shell-debris / bak files, Sep 5–12 | VOID | delete after hash log |

## 1b. %TEMP% clones from tonight (listed, not read deep)

- **`/tmp/dtm-replication/`** (Sep 16 14:07) — shallow git clone: thrml-denoising / Active-Inference replication (pyproject, training_script.py, denoisingTests). Research-lane scratch. Verdict: **ARCHIVE** (capture README hash + remote URL into inbox, then let TEMP clean) — one step: `git -C /tmp/dtm-replication remote -v | tee >> inbox note`.
- **Fungal-research grab-bag** (Sep 16 17:26–17:39): `adamatzky_*.xml`, `buffi_*.xml`, `towards_fungal_computer.xml`, `crossref_fems.json`, `blatt2024.json`, `draguhn.json`, `gb_species/`, `lang_fungi.xml`, `pdjamor.xml` — mycelial-science lane PDF/XML/JSON harvests (ties to `docs/ref/MYCELIAL_SCIENCE_MAP.md`). Verdict: **FOLD** → `mag.cmd research-pack` output belongs in `watch/inbox/` (one step: re-run the pack with output into inbox).
- **Wave test debris**: `wave_driver_selftest_*` (2), `wave_worker_test_*` (7), 20+ `tmp*` pytest dirs, `pytest-of-foste/`, `g1_games_audit/` (G1 lane JS blocks), `u3_worker/` (`dispatch_union_alpha.py`, `draft_hydro_xor_sim.py`, `raw_response.json` — E-union lane scratch). Verdict: **VOID** (TEMP is cache; u3_worker scripts worth a 30-second diff against `watch/inbox/wave_20260916/e_union_alpha_20260916.py` before voiding).
- ~222 items modified today in TEMP overall; tonight's big `.tmp` blobs (26 MB, 11.8 MB, 5 MB, 1.6 MB) are session-ephemeral. Verdict: VOID.

## 1c. Orphaned harness scripts (`scripts/` — no reference in docs/, AGENTS.md, README, main.py, queue, memory/briefs)

**98 of 142 scripts are orphaned.** Buckets:
- **Chess-line one-offs (17)**: `_bfs_qxd1.py`, `_find_exd5.py`, `_find_from_qxd1.py`, `_find_full_line.py`, `_find_qxd1_prefix.py`, `_replay_chess_line.py`, `_bump11/12.py`, `_bump_tesuji10.py`, `_search_opening.py`, `_pick_line.py`, `edg_compiler.py`, `_survival_bag.py`, `_scrub_story(2).py`, `_test_suffix.py`, `_gen_game_verkle.py`, `_route_tool_quant.py`, `k17_pilot.py` — the "edg" chess-opening lane debris. Verdict: **ARCHIVE** batch → `scripts/archive/chess_20260916/`.
- **Underscore one-off patches/probes (12)**: `_fix_appjs_load.py`, `_patch_diary_js.py`, `_patch_journey.py`, `_patch_load_verkle.py`, `_gen_memory_map.py`, `_gen_module_map.py`, `_audit_*.py` (4), `_desk_step_cycle.py`, `_mesh_integration_brief.py`. Verdict: **ARCHIVE**.
- **Named but unreferenced (44 py)**: incl. `secrets_hygiene_check.py`, `verify_verkle_continuity.py`, `salon_phone.py`, `harness_eval.py`, `corpus_packer.py`, `tg_harvest.py`, `x_auth_loop.py`, `vision_bench.py`, `vast_paces*.py`, `meld_claims.py`, `light_replay_falsifier.py`, `lesson_gate.py`… Some are likely load-bearing-by-convention (call out `secrets_hygiene_check.py` and `verify_verkle_continuity.py` for a keep/rename decision rather than blind archive). Verdict: **FOLD-or-ARCHIVE per script** (30-second triage each; default ARCHIVE).
- **PS1/CMD/MJS/SH/JS (25)**: `fix-wifi.*`, `mag_exec.cmd` (duplicate of `mag.cmd`?), `install_mag_startup.ps1`, `improve_daily/deep.ps1` (note: AGENTS.md cites `register_improve_task.ps1`, which IS referenced — these two are not), `art_forge.mjs`, `decks_nightly.mjs`, `rocinante_r1_bench.mjs`, `teach_recorder.sh`, `hofw_001_seed.sh`… Verdict: **ARCHIVE** after confirming no scheduled task references (`schtasks /query | findstr Mag`).

---

# §2 — The inbox shadow pile (top unindexed items)

Coverage: 140 active INDEX items vs 440 top-level files. The named big items are ALL unindexed (verified by name-grep against INDEX.json).

| Item (size, date) | What it is | Lane / maker | Verdict | One command next step |
|---|---|---|---|---|
| `SPORE_LEDGER_CHAIN_20260901.txt` (99,662 B, Sep 1) | Operator↔AI doctrine chain: "bubbles are tokens / spores / ouroboros" — compute-accounting metaphors formalized (Zai + Google passes). Canon-adjacent to Mag DNA | Operator hand-feed (chat export), Sep 1 | **FOLD** | `python -c "import hashlib;print(hashlib.sha256(open('watch/inbox/SPORE_LEDGER_CHAIN_20260901.txt','rb').read()).hexdigest())"` → append INDEX event, file under `docs/ref/` or `memory/` |
| `SPORE_LEDGER_CHAIN_DUP_20260901.txt` | **Byte-identical twin** — sha256 `cf11795916b973d9…` matches original exactly, same mtime | Same, duplicated save | **VOID** | `rm watch/inbox/SPORE_LEDGER_CHAIN_DUP_20260901.txt` after logging the shared hash (dedupe procedure) |
| `dogfood-trajectory save.txt` (313,735 B, Sep 9 09:18) | Main-session trajectory export ("IN 279,765 · OUT 1,529 · 38.7s"), desk-dogfood audit session log | Desk-dogfood lane, bulk save Sep 9 (same minute as both ractor transcripts → one paste-save burst) | **ARCHIVE** | `sha256sum` + `mv "watch/inbox/dogfood-trajectory save.txt" watch/inbox/desktop_bundle_20260901/` (or park dir) + INDEX event |
| `ractor-salon.txt` (121,424 B) + `ractor-salon-001.txt` (189,753 B), Sep 9 09:18 | Ractor multi-model salon transcripts ("THE FLAW: shared grounding only ships a human-authored prior…") — source corpus for the now-owned `projects/ractor-salon` repo | ractor lane (sancho writers, per INDEX nonce warnings) | **FOLD** | Register + move under `watch/inbox/ractor_transcripts/` and cross-link from `projects/ractor-salon/docs` |
| `kirk_2096316053630415211.jpg` (239 KB, Sep 6) | Educational infographic: "Local Attention vs Global Attention — CNN vs ViT" (viewed: standard teaching chart, bluejay classifier) | X/Twitter image steal — `<name>_<snowflake-id>.jpg` pattern | **ARCHIVE** | `mv` into `watch/inbox/media/` + INDEX (keep snowflake id in the event for provenance) |
| `exm_2096343368121164050.jpg` (171 KB), `tezmak_…jpg`→`techmak_2096509074800345136.jpg` (131 KB) | Same snowflake-steal family, unviewed | same | **ARCHIVE** | same one-liner, batch |
| `BCHAIN2_DISSECTOR_20260907.jsonl` (62 KB) + `.md` twin | Chain dissector intake, Sep 7 — has an .md companion, still unindexed | bchain lane | **FOLD** | append INDEX event for the pair |
| `BUBBLES_PHYSICS_BRIEF_20260901.txt` (55 KB), `RESEARCH_DEEP_DIVE_20260901.txt` (48 KB), `CORPUS_EXTENSION_20260901.txt` (30 KB), `PERSONA_CONDITIONING_SHARE_RAW_20260907.md` (37 KB) | Sep 1 research wave strays — named work products that never got events | research/salon lanes | **FOLD** | batch INDEX append (one loop command over the 20260901 strays) |
| `dai_multi_agent_system_competitive_analysis.docx` (44 KB) | Competitive-analysis docx | unknown (docx is the only one in inbox) | **ARCHIVE** | hash + park in `media/` or convert to md |
| top-level unindexed counts | **~300 files**: 389 md / 23 json / 13 txt / 4 jpg / 2 mp3 / 1 mp4 / 1 gz / 1 docx / 2 jsonl / 2 mjs / 1 cjs / 1 log (some of the 389 md may be hash-indexed — caveat above) | many lanes | bulk **FOLD** | run `mag.shared_surface validate` then a batch event-append script per date bucket |

---

# §3 — Unclaimed output dirs

| Path | What | Verdict | One command next step |
|---|---|---|---|
| `memory/runs/` — 567 entries | Run estate. Only **6** `receipt.json` files; `RECEIPTS_INDEX_20260912.json` covers just the 3 waves of Sep 12 (clarke/loom/loom3) | mixed — see below | extend RECEIPTS_INDEX generator over all `*_2026091*` dirs |
| `memory/runs/*_empty_recovery/` — 55 dirs (Aug 3 → Sep 15) | Crash-recovery debris (each holds `pre_turn_messages.json` + `traces.txt`, ~20 KB) | **VOID** | `find memory/runs -maxdepth 1 -name "*_empty_recovery" -type d` → hash-manifest then delete |
| `memory/runs/archetype_art, concurrency, space_ear/` | 3 truly empty dirs | **VOID** | `rmdir` |
| `memory/runs/orphans_53, orphan_sweep, orphan_sense, orphans_ds, orphans_ling/` | **Prior orphan sweeps already exist** (orphans_53 has stdout/stderr logs; orphan_sweep has lanes.json + pack.md) — reuse their format | FOLD (precedent) | diff tonight's inventory against `memory/runs/orphan_sweep/pack.md` |
| `memory/runs/governor_autorun_trail.jsonl` — **51 MB** (Sep 16 18:07, live) | Governor autorun trail — currently growing | KEEP (live) but needs rotation | add size-based rotation to the governor writer |
| `watch/salon_responses/astra_smoke_12/` (12 model responses + verdict_matrix) | Claimed by tonight's `A4_ASTRA_SMOKE_12.md` receipt | KEEP | none |
| `watch/salon_responses/astra_union_alpha/` | Claimed by `U2_UNION_ASTRA13.md` | KEEP | none |
| `watch/salon_responses/u6_union_creative/` | Claimed by `U6_UNION_CREATIVE.md` | KEEP | none |
| `watch/salon_responses/gap_probe_response_source.txt` (Sep 8) | No references anywhere in inbox/docs | **ARCHIVE** | hash + fold into nearest gap_probe run dir |
| `artifacts/salon_ess_*(5 files, Sep 16 13:19–13:56)` | Salon-ESS generator + shuffled corpus + replicate script | Claimed: referenced in `WAVE_STATE_20260916.md` + `A1_BLIND_CHALLENGE_SET.md` | KEEP (confirm A1 lane registers paths in INDEX) |
| `artifacts/rashomon_dedupe_20260916.py`, `backfill_links_20260916.py` | Tonight's B12/B6 lane scripts parked outside scripts/ | FOLD | move into `scripts/` with lane prefix or add INDEX pointers |
| `artifacts/mud_script_0.js` (33 KB, Sep 14), `depthscan.js`, `spectator_view.md`, `verdict.md`, `vertigo_boat_20260908/`, `quiet_forge/`, `training/`, `magatama_edition_strike_the_chord.txt` | Older strays, no receipts in dir | **ARCHIVE** (hash + park) per item | batch: `sha256sum artifacts/* > watch/inbox/wave_20260916/artifacts_manifest.json` |
| `projects/memory/corpus/kungfu/` (71 MB mp4s) | (duplicate entry from §1a — the biggest unclaimed output dir of all) | **FOLD** | `mv` into repo `memory/corpus/` |

---

# §4 — Shadow inventory summary

Counts by verdict (items/dirs inventoried across §1–§3, counting buckets not individual files):

| Verdict | Count | Notes |
|---|---|---|
| **FOLD** (register + file properly) | 14 | SPORE original, ractor transcripts ×2, fungal TEMP research pack, audit_prep trio, projects/memory corpus, BCHAIN2 pair, Sep-1 research strays, ~300-file bulk inbox backlog, run-receipts extension, prior-orphan-sweep formats |
| **ARCHIVE** (park + hash) | 19 | dtm-replication, mag-current-rebuild, mag-sovereign-kit, embassy ×2, field-strike-the-chord, teach frames, research clones, 12 stray PNGs, kirk/exm/techmak jpgs, dogfood trajectory, 96-orphan scripts (default), gap_probe txt, artifacts strays, dai docx |
| **VOID** (flag for procedure) | 9 | SPORE_DUP twin, codex_pytest ×9 (1 bucket), sovereign-mirror, debris files ×4, TEMP tmp*/wave-test debris, 55 empty_recovery dirs, 3 empty run dirs, nul/bak files |
| **KEEP** (already owned) | 12 | ractor-salon repo, mycelial-republic, salon_responses ×3, artifacts salon_ess family, governor trail (live), RECEIPTS_INDEX precedent |

**Total distinct shadow items inventoried: ~54 buckets covering 450+ physical artifacts.**

## The 5 that most deserve revival-or-closure this week

1. **`projects/memory/corpus/kungfu/` (71 MB mp4s outside the durable root)** — violates the shared-artifact boundary outright; sole-copy risk on a video-lane corpus. One `mv` + INDEX event closes it. (FOLD)
2. **`SPORE_LEDGER_CHAIN` twin (Sep 1)** — 100 KB of canon-adjacent doctrine (bubbles-are-tokens) sitting unindexed since day one, with a byte-identical _DUP insulting it. Fold the original into docs/ref, void the twin. (FOLD+VOID)
3. **The ~300-file unindexed inbox backlog (389 md / 23 json / 13 txt / …)** — the pile G2 quantified; every future INDEX derivation will keep flagging it. One batch event-append per date bucket (Sep 01 / Sep 06 / Sep 07 / Sep 09 / Sep 11+) clears 80% in an afternoon. (FOLD, bulk)
4. **`watch/inbox/ractor-salon.txt` + `-001.txt` + `dogfood-trajectory save.txt` (625 KB, one paste-burst, Sep 9)** — the founding corpus of the now-versioned ractor-salon repo is still unowned scratch in inbox root. Fold into the repo or a registered subdir; the salon lane is active *tonight* (U9) so provenance is fresh. (FOLD)
5. **98 orphaned scripts (69% of `scripts/`)** — including safety-relevant ones (`secrets_hygiene_check.py`, `verify_verkle_continuity.py`) that may be load-bearing-by-convention. One 30-minute triage: keep/rename the ~5 load-bearing, batch-park the chess+patch debris (29 scripts) to `scripts/archive/chess_20260916/`. (ARCHIVE, with 5 FOLD calls)

**Boundary note for the fold procedure:** ractor-salon (repo) is owned; `projects/ractor-salon` has uncommitted modifications from tonight's U9 lane — do not sweep it.

*CV2 signing off — read-only honored; only this receipt was written.*
