# BACKUP PRUNE LIST 2026-10-03 (operator review; nothing deleted)

Companion to watch/inbox/HYGIENE_WAVE_20261003.md task 4. Census: rg --files --no-ignore --hidden -g "*.bak-2026*" -g "*bak-orphanlane*" over the repo (excluding .git, node_modules), sizes from Get-Item, 2026-10-03 ~23:00 ET. rg exited 2 (some unreadable paths), so treat counts as a floor.

Self-steal: keep-last-N rule from scripts/backup_chain.py (KEEP=7) and the ranked order in watch/inbox/ractor_engine/2026-10-03-grokbot-estate/SYNTHESIS.md step 6 (prune the chain backups to the last 2 only AFTER step 5 lock hardening verifies). Delete is operator-gated.

## Totals

- All matched: 88 files, 317,252,331 B (317.3 MB)

- bak-orphanlane: 29 files, 316,463,036 B (316.5 MB): verkle_chain.jsonl x25 (165.8 MB), knots tar x2 (150.7 MB), verkle_tip.json x2 (988 B)

- other .bak-2026*: 59 files, 789,295 B (0.8 MB). Not worth a prune pass on size; listed for completeness.

- If the operator approves A+B+C as proposed: about 217.1 MB freed (A 149.8 MB, B 66.9 MB, C 0.4 MB across 33 candidates).
- Known vs new: 25 chain backups / 166 MB is KNOWN (SYNTHESIS item 3). NEW: 4 more orphanlane files beside them (2 knots tars 150.7 MB, 2 verkle_tip.json), so the orphanlane class is 29 files / 316.5 MB, nearly double the 166 MB figure. Newest chain backup is 10/03 18:16 ET, before state/knot_at_close.off (18:46 ET); no new one since.


## A. verkle_chain.jsonl.bak-orphanlane-* (proposed: keep newest 2, prune 23 after SYNTHESIS step 5 verify)

| Action | Path | Bytes | Mtime ET |
|---|---|---|---|
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20260906T224709Z | 5,168,308 | 2026-09-06 10:02 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20260906T224827Z | 5,168,308 | 2026-09-06 10:02 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20260906T224909Z | 5,168,308 | 2026-09-06 10:02 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20260906T225039Z | 5,168,308 | 2026-09-06 10:02 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20260906T225411Z | 5,168,308 | 2026-09-06 18:54 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20260906T225456Z | 5,169,074 | 2026-09-06 18:54 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20260906T225537Z | 5,169,074 | 2026-09-06 18:54 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T205738Z | 6,334,716 | 2026-10-03 16:55 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T205841Z | 6,338,362 | 2026-10-03 16:58 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T210317Z | 6,490,264 | 2026-10-03 17:03 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T210810Z | 6,640,736 | 2026-10-03 17:07 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T211305Z | 6,792,197 | 2026-10-03 17:12 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T212314Z | 6,795,218 | 2026-10-03 17:19 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T212408Z | 6,797,504 | 2026-10-03 17:23 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T213127Z | 6,948,861 | 2026-10-03 17:31 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T213721Z | 7,090,518 | 2026-10-03 17:35 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T214311Z | 7,243,007 | 2026-10-03 17:42 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T215144Z | 7,390,280 | 2026-10-03 17:50 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T215731Z | 7,541,286 | 2026-10-03 17:57 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T220328Z | 7,692,238 | 2026-10-03 18:02 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T220627Z | 7,774,574 | 2026-10-03 18:05 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T220823Z | 7,825,591 | 2026-10-03 18:07 |
| PRUNE | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T221322Z | 7,974,280 | 2026-10-03 18:13 |
| KEEP | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T221337Z | 7,975,804 | 2026-10-03 18:13 |
| KEEP | memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T221639Z | 7,975,804 | 2026-10-03 18:16 |

Prune A frees 149,849,320 B (149.8 MB).

## B. Other orphanlane files (proposed: keep the newest knots tar, prune the 09-06 one; keep both tip files, 988 B)

| Action | Path | Bytes | Mtime ET |
|---|---|---|---|
| PRUNE | memory/biography/knots.bak-orphanlane-20260906T224709Z.tar | 66,918,400 | 2026-09-06 18:47 |
| KEEP | memory/biography/knots.bak-orphanlane-20261003T205738Z.tar | 83,742,720 | 2026-10-03 16:57 |
| KEEP | memory/biography/verkle_tip.json.bak-orphanlane-20260906T225355Z | 494 | 2026-09-06 10:02 |
| KEEP | memory/biography/verkle_tip.json.bak-orphanlane-20260906T230013Z | 494 | 2026-09-06 18:54 |

## C. Other .bak-2026* (proposed)

Rule: files under archive snapshots (_archaeology_out/, dist_audit/, corpus/oral_history/) are part of those archives: KEEP. Backups written 2026-10-03 (this wave and the LAWLOG wave) stay until their edits are reviewed: KEEP. Everything else older than 14 days whose original is under git: PRUNE candidate (git history already holds the prior bytes; confirm with git log -- <original> before deleting).

| Action | Path | Bytes | Mtime ET |
|---|---|---|---|
| KEEP (recent) | AGENTS.md.bak-20261003b | 23,892 | 2026-10-02 08:47 |
| KEEP (archive) | _archaeology_out/mag-disk-20260905/mag/bay_organs.py.bak-20260904-pre-cas | 12,964 | 2026-09-05 18:02 |
| KEEP (archive) | _archaeology_out/mag-disk-20260905/mag/campaign.py.bak-20260904-pre-listfix | 29,914 | 2026-09-05 18:02 |
| KEEP (archive) | _archaeology_out/mag-disk-20260905/mag/lattice_logic.py.bak-20260904-pre-lattice | 11,589 | 2026-09-05 18:02 |
| KEEP (archive) | _archaeology_out/mag-disk-20260905/mag/seat_dispatch.py.bak-20260902 | 11,034 | 2026-09-05 18:02 |
| KEEP (archive) | _archaeology_out/mag-disk-20260905/mag/swarm_tools.py.bak-20260902 | 24,228 | 2026-09-05 18:02 |
| KEEP (recent) | agents/skills/operator-corrections/SKILL.md.bak-20261003b | 13,883 | 2026-09-29 11:51 |
| PRUNE candidate | configs/providers.yaml.bak-20260826-pre-deepseek-swarmcap | 22,418 | 2026-08-26 20:11 |
| KEEP (archive) | corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/mag/bay_organs.py.bak-20260904-pre-cas | 12,964 | 2026-09-05 18:02 |
| KEEP (archive) | corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/mag/lattice_logic.py.bak-20260904-pre-lattice | 11,589 | 2026-09-05 18:02 |
| KEEP (archive) | corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/mag/seat_dispatch.py.bak-20260902 | 11,034 | 2026-09-05 18:02 |
| KEEP (archive) | corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part9-mag-disk/mag-disk/mag/campaign.py.bak-20260904-pre-listfix | 29,914 | 2026-09-05 18:02 |
| KEEP (archive) | corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part9-mag-disk/mag-disk/mag/swarm_tools.py.bak-20260902 | 24,228 | 2026-09-05 18:02 |
| PRUNE candidate | deploy/openclaw/openclaw.container.json.bak-20260902 | 14,454 | 2026-09-02 08:18 |
| PRUNE candidate | deploy/openclaw/openclaw.container.json.bak-20260902-premerge | 14,536 | 2026-09-02 08:51 |
| PRUNE candidate | deploy/openclaw/openclaw.container.json.bak-20260903 | 20,174 | 2026-09-03 11:20 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/configs/providers.yaml.bak-20260826-pre-deepseek-swarmcap | 22,418 | 2026-08-26 20:11 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/mag/bay_organs.py.bak-20260904-pre-cas | 12,964 | 2026-09-04 10:30 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/mag/campaign.py.bak-20260904-pre-listfix | 29,914 | 2026-09-04 11:12 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/mag/free_tier.py.bak-20260906-pre-zai3-pin | 8,013 | 2026-09-05 21:57 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/mag/lattice_logic.py.bak-20260904-pre-lattice | 11,589 | 2026-09-04 13:34 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/mag/seat_dispatch.py.bak-20260902 | 11,034 | 2026-08-29 08:53 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/mag/swarm_tools.py.bak-20260902 | 24,228 | 2026-08-31 07:26 |
| KEEP (archive) | dist_audit/nacho_business_audit_20260912T214050Z/mag/x_interceptor.py.bak-20260906 | 8,868 | 2026-09-06 12:19 |
| KEEP (recent) | docker-compose.yml.bak-20261003 | 17,195 | 2026-09-30 15:19 |
| PRUNE candidate | docs/ZCODE_SEAT.md.bak-20260903 | 1,674 | 2026-09-03 12:23 |
| PRUNE candidate | mag/bay_organs.py.bak-20260904-pre-cas | 12,964 | 2026-09-04 10:30 |
| PRUNE candidate | mag/campaign.py.bak-20260904-pre-listfix | 29,914 | 2026-09-04 11:12 |
| PRUNE candidate | mag/free_tier.py.bak-20260906-pre-zai3-pin | 8,013 | 2026-09-05 21:57 |
| KEEP (recent) | mag/knot_at_close.py.bak-20261003 | 11,432 | 2026-09-07 08:12 |
| PRUNE candidate | mag/lattice_logic.py.bak-20260904-pre-lattice | 11,589 | 2026-09-04 13:34 |
| PRUNE candidate | mag/seat_dispatch.py.bak-20260902 | 11,034 | 2026-08-29 08:53 |
| PRUNE candidate | mag/swarm_tools.py.bak-20260902 | 24,228 | 2026-08-31 07:26 |
| PRUNE candidate | mag/x_interceptor.py.bak-20260906 | 8,868 | 2026-09-06 12:19 |
| KEEP (recent) | memory/biography/backup_20261003_prebackfill/mag_boot_lane.cmd.bak-20261003 | 1,764 | 2026-09-27 20:03 |
| PRUNE candidate | memory/percolator/invariants.json.bak-20260902 | 11,984 | 2026-09-02 09:26 |
| PRUNE candidate | queue/lanes/android_surface/manifest.md.bak-20260904-pre-lattice | 2,212 | 2026-09-04 13:32 |
| PRUNE candidate | queue/lanes/bard_ledger/manifest.md.bak-20260904-pre-lattice | 2,145 | 2026-09-04 13:32 |
| PRUNE candidate | queue/lanes/builder/manifest.md.bak-20260904-pre-lattice | 2,193 | 2026-09-04 13:32 |
| PRUNE candidate | queue/lanes/builder/surface.md.bak-20260904 | 124 | 2026-09-04 11:47 |
| PRUNE candidate | queue/lanes/day_work/manifest.md.bak-20260904-pre-lattice | 2,255 | 2026-09-04 13:32 |
| PRUNE candidate | queue/lanes/economist/manifest.md.bak-20260904-pre-lattice | 2,198 | 2026-09-04 13:32 |
| PRUNE candidate | queue/lanes/elder/manifest.md.bak-20260904-pre-lattice | 2,148 | 2026-09-04 13:32 |
| PRUNE candidate | queue/lanes/research/manifest.md.bak-20260904-pre-lattice | 2,832 | 2026-09-04 13:32 |
| KEEP (recent) | scripts/verkle_boot_view.py.bak-20261003 | 12,071 | 2026-10-03 16:50 |
| PRUNE candidate | state/vast/covenant.json.bak-20260902 | 860 | 2026-08-29 04:02 |
| PRUNE candidate | state/vast/covenant.json.bak-20260903 | 2,138 | 2026-09-03 12:25 |
| KEEP (recent) | tests/test_selffeed_integration.py.bak-20261003w | 2,995 | 2026-09-28 12:42 |
| KEEP (recent) | tools/seat_law_gate.py.bak-20261003b | 5,505 | 2026-09-29 20:00 |
| KEEP (recent) | tools/seat_law_postgate.py.bak-20261003b | 1,981 | 2026-09-29 19:36 |
| PRUNE candidate | watch/SELF_STEAL_GROK_ORPHANS_20260904.md.bak-20260904 | 17,521 | 2026-09-04 11:47 |
| PRUNE candidate | watch/TESUJI_MAP.jsonl.bak-20260906-L0 | 81,551 | 2026-09-06 00:59 |
| PRUNE candidate | watch/engine_reconciler.py.bak-20260903 | 6,069 | 2026-09-03 12:23 |
| PRUNE candidate | watch/engine_reconciler.py.bak-20260904 | 7,665 | 2026-09-03 21:04 |
| PRUNE candidate | watch/engine_spec.json.bak-20260903 | 1,755 | 2026-09-03 12:23 |
| PRUNE candidate | watch/overnight_churn.py.bak-20260903 | 8,385 | 2026-09-03 12:23 |
| PRUNE candidate | watch/overnight_churn.py.bak-20260904 | 11,368 | 2026-09-03 21:04 |
| PRUNE candidate | watch/salon_runner.py.bak-20260904 | 25,447 | 2026-09-03 19:52 |
| PRUNE candidate | watch/test_claim_race_20260904.py.bak-20260904-pre-cas | 19,375 | 2026-09-04 10:30 |

No file was deleted, moved or renamed by this wave.

