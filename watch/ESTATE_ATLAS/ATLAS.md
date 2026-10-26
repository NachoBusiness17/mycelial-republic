# ESTATE ATLAS

- **generated:** 2026-09-27T17:58:13Z
- **spine:** watch/ESTATE_INDEX/ last run 4.0h ago (fresh)
- **source rows:** 3,355,576 files, 107.59 GB under Documents/projects
- **layers up from here:** semantic = memory/runs/mickey17/MASTER_INDEX_20260920.md (what things mean) · provenance = the verkle chain (what is proven) · THIS file = what exists and where

## What is proven (the live estate)

| organ | files | bytes |
|---|---|---|
| memory/runs/ (run receipts) | 50,376 | 1.26 GB |
| memory/biography/ (the chain (biography)) | 45,010 | 0.36 GB |
| watch/ (the record (cards)) | 19,174 | 8.32 GB |
| state/ (live state) | 3,503 | 0.09 GB |
| mag/ (fleet organ (the code)) | 2,642 | 0.04 GB |
| tests/ (proof) | 726 | 0.01 GB |
| queue/ (mesh channel) | 710 | 0.01 GB |
| dashboard/ (surface) | 591 | 3.66 GB |
| docs/ (doctrine) | 532 | 0.03 GB |
| tools/ (hands) | 359 | 0.18 GB |
| scripts/ (hands) | 251 | 0.00 GB |
| **live organ total** | **123,874** | |
| HOT+WARM working set (whole projects root) | 349,754 | |

## What is dark (the sediment)

- COLD+FROZEN: **3,005,822 files** (90% of everything). Sediment, not rot — it stays until its sink rule moves it.

## Sinks (append-only writers — capped by rule, never hand-weeded)

| sink | files | bytes | law |
|---|---|---|---|
| memory/biography_backup/ — daily full-copy of memory/biography, unrotated | 103,089 | 0.14 GB | keep newest 2 stamps, tar the rest (knotnight ritual = custody, not sprawl) |
| memory/ghost/leak_reports/ — ghost leak reports, timestamped, never rotated | 18,296 | 0.01 GB | keep 7 days, tar+attic the rest |
| .mimosa/hook-state/ — Mimosa hook writes per invocation, sibling lane | 2,492,699 | 34.45 GB | propose rotation cap upstream of the hook; owner = Mimosa lane |
| memory/biography_backup_20260825/ — old-series knotnight backup | 0 | 0.00 GB | tar once -> attic + manifest |
| mine/raw/ — mined corpus, raw | 103,033 | 5.73 GB | keep (ore, cold by design) |

## Version clusters (same stem, many editions — attic candidates, dry-run only)

| stem | editions | example |
|---|---|---|
| test.* | 160 | agents/pytest-tmp-33016/test_hook_census_case_arm_repl0/stale/tests/test_new.py |
| moonshot.* | 72 | memory/runs/deep_research_moonshot/moonshot-20260927T125531.json |
| CLEAN.* | 62 | agents/pytest-tmp-46740/test_outside_dropped_register_0/inbox/CLEAN_20260926.md |
| INTAKE_B2_440_CARD.* | 60 | agents/pytest-tmp-33016/test_cage_and_canonical_write_0/cage_copy_repo/watch/INT |
| NOTE.* | 59 | agents/pytest-tmp-33016/test_cage_and_canonical_write_0/cage_copy_repo/watch/NOT |
| RECAP_7D.* | 54 | agents/pytest-tmp-46740/test_bare_absolute_host_root_r0/inbox/RECAP_7D_20260926. |
| snapshot.* | 36 | agents/pytest-tmp-33016/test_load_latest_freeze_roundt0/memory/freeze/snapshot_2 |
| test-executing-broker-contract_board_write.* | 35 | memory/runs/effect_broker/test-executing-broker-contract_board_write_20260927_09 |
| PROSE_CENSUS.* | 24 | watch/PROSE_CENSUS_20260927.md |
| whisper.* | 24 | memory/runs/whisper_images/whisper_20260831_045423.png |
| CATHEDRAL_CURVATURE_SCAN.* | 14 | watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.png |
| DRIFT_PATROL.* | 13 | watch/inbox/DRIFT_PATROL_20260927.md |
| X_REPLY_RADAR.* | 13 | watch/X_REPLY_RADAR_20260927.md |
| GAP_STEALTH_HARNESS.* | 12 | corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-dis |
| RELEASE_NOTES.* | 12 | docs/ref/releases/RELEASE_NOTES_v1.md |
| walker2d.* | 8 | fle_u1/.venv/Lib/site-packages/gymnasium/envs/mujoco/walker2d_v4.py |
| t-seat.* | 8 | memory/runs/orchestrator/tasks/t-seat-94871732.json |
| GAP_STEALTH.* | 8 | corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-dis |
| pusher.* | 7 | fle_u1/.venv/Lib/site-packages/gymnasium/envs/mujoco/pusher_v4.py |
| biography_backup.* | 7 | attic/20260923_biography_rotation/biography_backup_20260825.tar |
| os.* | 7 | _archaeology_out/mag-disk-20260905/mag/os_v2.py |
| ant.* | 6 | fle_u1/.venv/Lib/site-packages/gymnasium/envs/mujoco/ant_v4.py |
| half_cheetah.* | 6 | fle_u1/.venv/Lib/site-packages/gymnasium/envs/mujoco/half_cheetah_v4.py |
| hopper.* | 6 | fle_u1/.venv/Lib/site-packages/gymnasium/envs/mujoco/hopper_v4.py |
| humanoid.* | 6 | fle_u1/.venv/Lib/site-packages/gymnasium/envs/mujoco/humanoid_v4.py |
| swimmer.* | 6 | fle_u1/.venv/Lib/site-packages/gymnasium/envs/mujoco/swimmer_v4.py |
| ESTATE_SMITH_CHART.* | 6 | watch/inbox/ESTATE_SMITH_CHART_20260927.json |
| chord.* | 6 | dashboard-deploy/static/night/chord_v4.html |
| address.* | 6 | tortoise-wow/dep/include/asio/ip/address_v4.hpp |
| network.* | 6 | tortoise-wow/dep/include/asio/ip/network_v4.hpp |

## The protocol (how it stays clean)

1. **Spine walks, atlas reads.** Daily spine run (09:00) feeds this map. Atlas is never hand-edited; the law lives in its source.
2. **Sinks get caps.** Every append-only writer above gets a rotation rule. A cap violation shows up here as a growing number — meter, then move.
3. **Attic, not delete.** Moves land in attic/<date>_<reason>/ at original relative paths + a MANIFEST.jsonl row. Reversible by construction.
4. **GO-gated.** ATTIC_MOVE_LIST.jsonl is a plan. Execution needs the operator's word (needs-manifest law: CAP and STOP are operator inputs).

_atlas run took 42.1s, read-only, $0._