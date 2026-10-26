# HYGIENE WAVE 2026-10-03 (overnight, operator-approved)

Grok Bot, Sat 10/3 22:53 to ~23:25 ET, on DESKTOP-7C70KSC. Nothing committed. No daemon, no scheduled task. No .env, key or token file read. Nothing deleted, nothing rotated for real.
Not touched, by rule: mag/ghost.py, mag/health.py, mag/orchestrator.py, verkle writers, janitor code, Startup scripts, AGENTS.md.
Wave protocol: the repo defines the fifty-wide wave protocol for "N >= 30 independent byte-checks" (queue/STANDING_RAILS.md:30). These 5 tasks are serial chores, not 30 independent checks, so it did not apply. One seat, one receipt.
Self-steal sources are cited per task. New vs known is marked on every finding.

## Files written
| File | Kind | Backup |
|---|---|---|
| state/CURRENT.md | refreshed | state/CURRENT.md.bak-20261003w |
| state/_astra_triangulation.md | 8 link targets | state/_astra_triangulation.md.bak-20261003w |
| .agents/skills/image-blast/SKILL.md | 1 link target | .agents/skills/image-blast/SKILL.md.bak-20261003w |
| tools/rotate_kpi.py | new | - |
| watch/inbox/BACKUP_PRUNE_LIST_20261003.md | new | - |
| watch/inbox/ARMC_DECISION_MEMO_20261003.md | new | - |
| this receipt | new | - |

## 1. state/CURRENT.md refresh
- KNOWN premise correction: the file was not stale since 10/2. It had been rewritten 10/3 20:39 ET (stamp 23:55Z) after the SYNTHESIS "CURRENT.md stale" finding. It still lacked the audit, janitor, dive, lawlog, redboard and zknot facts.
- Kept the header and the Goal / Plan / Last result / Critique / Recent tools structure and voice. Added, inside Plan, "Post-reboot sequence" (SYNTHESIS ranked 0-8) and "Owed" (operator-gated, seat, SYNTHESIS OWED).
- NEW: post-reboot step 0 is already done. state/knot_at_close.off exists (18:46 ET), and the boot line now passes --skip-knot-backup. The newest orphanlane backup (18:16 ET) predates the stop file.
- NEW: CURRENT.md is mirrored by mag/agent_cli.py:2251, so a seat run can overwrite the hand edit.
- Sources: SYNTHESIS.md, JANITOR_FIX_PLAN_20261003.md, OPERATOR_WORKFLOW_DIVE_20261003.md, LAWLOG_20261003.md, IMAGE_BLASTER_GO_20261003.md, LITE_LANE_PULL_20261003.md, state/REDBOARD.md, memory/zknot/LATEST.md. SYNTHESIS lives at watch/inbox/ractor_engine/2026-10-03-grokbot-estate/, not at a top-level ractor_engine/.

## 2. Dead links (scripts/doc_link_check.py, self-steals mag/cite_gate.py)
- Run at 22:57 ET: 110 missing in 40 docs (brief said 105). After fixes: 101 in 40 docs.
- FIXED (target moved, verified with Test-Path):
  - state/_astra_triangulation.md: docs/ref/DECISION_LAYERS.md -> docs/DECISION_LAYERS.md
  - the same file's quoted release table: releases/RELEASE_NOTES_v1/v2/v3.md, releases/VERSION_REGISTRY.md, MAG_V4_CONDUCTOR_LOOP_DRAFT.md, MAG_v5_PIPE.md, MAG_MYCELIAL_REPUBLIC_COMPASS.md -> ../docs/ref/...
  - .agents/skills/image-blast/SKILL.md:36 -> corpus/library/image-blaster/.claude/skills/image-blast-3d/SKILL.md
- Left on purpose: docs/ZEITGEIST.md -> docs/archive/ZEITGEIST.md (state/_astra_triangulation.md:134). The string occurs twice in the file and the second hit is not flagged, so it is not a safe one-shot replace. Operator hand.
- Remaining 101, not fixed (no moved target found by rg --files --no-ignore; prose untouched):
  - 45 in state/_astra_triangulation.md:1904-2066 point at memory/biography_backup_20260825/**. That backup was pruned by the keep-7 rotation in scripts/backup_chain.py, not moved. Candidate for a PHANTOM heading so the checker files them as ledger.
  - The rest of _astra_triangulation.md: data/raw (:612).
  - docs/SKILLS_LINT.md:44-59 (7): docs/email.md, scripts/auth-probe.sh, image_gen.py, update_plugin_cachebuster.py, read_marketplace_name.py, rotate_pdf.py, list-skills.py. Likely paths inside the linted skills' own dirs (not verified).
  - UsersfosteAppDataLocalTempjevals_readme.md (3): examples/quickstart.py, examples/support_agent_gates.py, logs/traces.jsonl. Stray root file with a mangled %TEMP% name. Candidate to move to attic/ (operator).
  - Stop files that are absent by design (not dead): state/redboard.off, state/worker.off (x2), state/mag_power.off.
  - tests/test_selffeed_integration.py (AGENTS.md:29, state/REDBOARD.md:12). NEW: the file is absent on disk, which explains the census patrol's "collect zero items" red. AGENTS.md was not touched.
  - corpus/library/image-blaster/.env (image-blast SKILL.md:19). It names where the keys go. Not read, not touched.
  - Single misses: configs/organs/egress_proxy.yaml, mag/egress_proxy.py; docs/ref/SEALIS_DOSSIER.md (x2), memory/runs/harness/first_47_report.md; docs/register/, docs/audit_prep/REGISTER_CLARIFICATION_20260912.md; memory/research_packs/mag_virtual_desk/REPORT.txt, RUN.txt; memory/research_packs/mesh_forest (+ INTEGRATION_BRIEF.md, x3 across two .cmd); data/json/posts.json; watch/foo.md; mag/work_register.record; mag/headless_render_fidelity.py; audit/witness_sampling_mathematics.v1.md; memory/behavioral_tracking_schema.md; watch/grounding_wave_witnesses.jsonl; artifacts/lens_artifact_20260912.md; local_sovereign_agent/audit_schemas/; research/aiTruthCode/; memory/verkle_tip.json; state/max_distill.json; models/fanout_router.py; memory/runs/rib_bus/frontier_synthesis.md; salon/SKILL.md; memory/working/first_user_model.md, agent_desk_trust_log.jsonl; memory/cursor_preamble_latest.md; state/MAZE_DOOR_PREP.md; build/drain; memory/mag_journal.md; mag/lite_guard.check; watch/CITE_GATE_MISSING_EVIDENCE_PROBE_20260906.md; watch/VAST_EXPERIMENT_VERDICT_20260905.md.
- Full JSON: %TEMP%\doclink_20261003w.out (before) and %TEMP%\doclink_after_20261003w.json (after) on the PC.

## 3. logs/kpi.jsonl
- Writer (KNOWN): mag/records.py:138 write_kpi, append at :166. Callers per watch/inbox/burn_reset_20260927/flash50/large-file-census.md section 7: biography summarize, lanes board, operator-os, main.py pack-status / migrate-lean, backfill.
- Readers (rg over all code, 10/3): only synthesis_agent.py:181 `_last_jsonl(KPI_JSONL)`, which wants the last row. memory/biography/kpi.json already holds the latest row. tools/gap_sentinel.py names the file only in prose.
- NEW: that reader loads the whole ~790 MB file into memory (read_text().splitlines() at synthesis_agent.py:48) to get 1 row.
- Self-steal: no rotation helper existed (rg rotat|gzip over tools/ and scripts/). The shape is borrowed from scripts/backup_chain.py (dated archive, no-write mode). tools/rotate_kpi.py has a dry-run default and needs --apply for a real run. It keeps the newest N rows (default 1000), gzips the older ones to attic/kpi/, verifies row count + sha256 before truncating, and preserves rows appended during the run. Synthetic self-test passed (50 rows + partial tail; archive 40, live 10 + tail).
- Dry run at 23:01 ET (only run made): 791,534,748 B, 24,556 rows. A real run would archive 23,556 rows (773.9 MB raw, est ~7 MB gzip from a 32 MB sample, ratio 0.009) to attic/kpi/kpi_2026-09-07_2026-10-03_<stamp>.jsonl.gz and leave 1,000 rows (17.6 MB) live. At ~940 rows/day, 1,000 rows is about one day.
- NEW: the first row is dated 2026-09-07. The 9/27 census saw 81,945 rows from 7/21 at 1.06 GB. Rows before 9/07 are gone, and no archive was found in attic/ or logs/. An earlier unreceipted cut is likely. Not chased further.
- Rows now average ~32 KB (each embeds the full incomplete_ids list). Fixing the schema at the writer (census recommendation) is the real cure. Not done: it is writer code.

## 4. Backups
- Full list and proposals: watch/inbox/BACKUP_PRUNE_LIST_20261003.md. Delete is operator-gated.
- 88 files matched, 317.3 MB in total.
- KNOWN: 25 verkle_chain.jsonl.bak-orphanlane-* (165.8 MB, 9/06 to 10/03 18:16 ET).
- NEW: 4 more orphanlane files sit beside them: knots tars 66.9 MB (9/06) and 83.7 MB (10/03 16:57 ET), plus 2 tip jsons. That makes the class 29 files / 316.5 MB.
- Other .bak-2026* sprawl: 59 files, 0.8 MB.
- Proposal: keep the newest 2 chain backups and the newest knots tar, after SYNTHESIS step 5 verifies. That frees about 217.1 MB.

## 5. Arm C
- One-page memo: watch/inbox/ARMC_DECISION_MEMO_20261003.md. Options only, no decision.
- NEW evidence:
  - The boot-lane line cannot finish the leg: the script opens its output with mode "w" and has no resume.
  - Projected leg is about 17h or more of uninterrupted box time.
  - No reboot since 9/25 23:47 ET.
  - With knot_at_close.off in place, the next logon doubles as a free test of the Ctrl-C hypothesis (break.md X1).
- KNOWN: the adversarial review rated the 200-state inference unsound without a null arm.

## Notes for the operator
- NEW: Startup\mag_boot_lane.cmd mtime is 10/3 22:53 ET (not written by this wave; another seat or the boot lane). Read-only here.
- Closed items not re-raised: the 9/30 key purge, the 191.8M figure, gap-register rows, the instance guard.
- No em-dash bytes in this receipt.
