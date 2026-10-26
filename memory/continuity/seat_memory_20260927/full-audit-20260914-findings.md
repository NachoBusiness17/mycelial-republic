---
name: full-audit-20260914-findings
description: 2026-09-14 full audit (50 tasks, 5 ractor panels, 665,131 files) —
  round-2 self-steal landed doctrine fixes + untracked backup twin; kill-list
  remainder (root sweep, handoff merge, k8s attic, gstdcoin) still open
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

Full audit of the repo, 2026-09-14: every file stat'd (665,131 — git tracks only ~30K; the rest is fleet runtime body: biography backups, mine/raw 3.2GB, memory/ghost 135K files). Five ractor panels (CLERK/ARCHIVIST/SKEPTIC/GAMES-MASTER/SHERPA) ran 50 tasks as parallel subagents. Findings filed: `watch/inbox/FULL_AUDIT_MAP_20260914.md`, `SHERPA_NEXT_US_20260914.md`, `AUDIT_INVENTORY_20260914.json`, `AUDIT_DOGFOOD_20260914.txt`; commit `261c895ad`.

Verified facts the doctrine contradicts: "39 deterministic green" is fossil (see [[test-suite-outgrew-doctrine]]); "Hermes parked" is false (dispatch log active through 2026-09-09, $220 armed budget); AGENTS.md:8 cites docs/ZEITGEIST.md which never existed (real: docs/archive/ZEITGEIST.md); main.py:1551 defaults to nonexistent `configs/coding_session.yaml`. Host supervisor dead is BY DESIGN (`state/DOCKER_ONLY`; restore = `docker compose restart mag`; ports 8765 dashboard / 8000 backend / 8001 api_server / 9000 ghost). Kill list top cows: `memory/biography_backup_20260825/` (42,249 files, 156MB, hash-identical, tracked — gitignore covers the un-dated twin only), 1,324 `agents/pytest-*` dirs, `deploy/openclaw/` retired-profile stack, `mine/raw` 3.2GB, `reference/gstdcoin` 27MB (zero code refs).

The audit is playable: `memory/game_modules/audit_dungeon.v1.json` — live-verified through `mag.game_campaign.handle_game` (start → character with `campaign_id` pinned in one process → act/move; walking `down` triggers W0 boss). See [[audit-our-way-game-medium]].
