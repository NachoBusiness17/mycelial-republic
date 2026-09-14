# FULL AUDIT MAP — 2026-09-14, 50 tasks, 5 ractors, no sacred cows

- **class:** RECEIPT (findings are FACT with paths) + INFERENCE (verdicts)
- **writer:** zcode-audit-20260914
- **coverage:** every file stat'd — **665,131 files** walked (`AUDIT_INVENTORY_20260914.json`); 50 audit tasks executed by 5 ractor panels (CLERK · ARCHIVIST · SKEPTIC · GAMES-MASTER · SHERPA); fleet tools dogfooded on the repo (`AUDIT_DOGFOOD_20260914.txt`).
- **medium:** findings are playable — `memory/game_modules/audit_dungeon.v1.json`, live-verified through `mag/game_campaign.handle_game` (start → atrium → vault → W0 boss trigger).

## The one-paragraph audit

The fleet is alive and the map is not: 3 Docker containers carry everything while the host supervisor lies dead by design; 665K files on disk vs ~30K in git; 5 weeks of work unfiled against an Aug-06 version arc; doctrine lies in three places (39 tests, Hermes parked, ZEITGEIST path); the shared-surface INDEX is 12 days stale because its fold tool only runs in Docker; 23 commits exist on one disk; and ~2GB of ore (mine/raw, gstdcoin, biography twins) sits inside the repo walls violating the contract's own bounded-pointer law.

## Coverage matrix (50 tasks → verdicts)

| Ractor | Tasks | Territory | Verdict summary |
|---|---|---|---|
| CLERK | 1–10 | mag/ 5Ws, main.py 179 cmds, configs parity, tests, servers, scripts ratio, root files | 980+ ownerless mag files; 5 zero-importer giants; 1 missing default config; 4 listeners not 3; every AGENTS.md command works |
| ARCHIVIST | 11–20 | memory/, docs/, canon reading order, inbox fold, handoff channels | AGENTS.md cites a ghost ZEITGEIST; INDEX fold Docker-only; two corpus_index.json name collision; load canon frozen in August; backup outgrew live 5:1 |
| SKEPTIC | 21–30 | static/ data diet, server redundancy, root debris, graves, doctrine dupes, sacred cows | 42K-file tracked backup twin; 1,324 pytest tmp dirs; retired-openclaw stack in tree; "39 tests" fossil; Hermes parked is false; 10 orphan HTML pages |
| GAMES-MASTER | 31–40 | world_state schema, campaign ingestion, quests, kifu tradition, dungeon path | `mag_game_module.v1` is the only zero-code ingestion path; dungeon built + live-verified; swarm_quests output exists but has no consumer |
| SHERPA | 41–50 | version arc, handoff freshness, deployment truth, host/container split, git state | 23 commits unpushed since Aug 9 (git 1.6GB, backup on same disk); DOCKER_ONLY is law; port map 8765/8000/8001/9000; W0.3 archive drop is the operator-side boss |

## Relational map — repo ↔ organs ↔ lanes ↔ canon (the edges that matter)

- **Runtime spine:** docker-compose `mag` service → `scripts/container/entrypoint.sh` → `mag_launch.py` → dashboard/server.py (:8765) + backend/server.py (:8000) + mag/api_server (:8001) + mag/ghost daemon (:9000) + mag/lane_runner + mag/ghost autorun drainer. Redis :6379. **K8s = standby bones; openclaw = retired profile.**
- **Memory writes:** mag/janitor.py + session_state_brief → memory/briefs/latest.md (fresh, same-day) · mag/biography.py → memory/biography (38K live) · scripts/backup_chain.py → biography_backup (206K, unbounded) · mag/pigeonhole.py → memory/mail (absent from boundary doc) · mag/agent_state.py / agent_cli.py → gitignored-but-test-pinned state dirs.
- **Canon chain (as written vs as lived):** AGENTS.md load order → 5 docs frozen Aug 4–6 → only `mag.cmd context-pack` is live. AGENTS.md:8 → docs/ZEITGEIST.md (**ghost**; real: docs/archive/ZEITGEIST.md). AGENTS.md:27 → "39 deterministic green" (**fossil**; real: 1305/34/9).
- **Inbox flow:** writers append index_events.jsonl (142+) → INDEX.json fold (Sep 2, Docker-only tool) → readers told to read INDEX first get a 12-day-old map. mag/link_library.py now canonicalizes URLs at the door.
- **Game medium:** memory/game_modules/*.json → mag/game_campaign.handle_game → mag/game_world.set_state (verkle knots) → game_world_render ASCII + dashboard/rest /api/v1/game. **The audit dungeon rides this whole chain with zero code changes.**

## Kill list — the 10 cows, boldest first (SKEPTIC, ratified by panel)

1. `memory/biography_backup_20260825/` — untrack 42,249 files / 156MB (hash-identical twin; gitignore line 53 misses the dated form). Pack is 1.50GiB.
2. 1,324 `agents/pytest-*` basetemp dirs + `.pytest-collect.txt` — delete; point basetemp at system temp.
3. `deploy/openclaw/` stack + `retired-openclaw`/`retired-eye` compose profiles — delete with receipt; k8s dir to attic (standby bones).
4. "39 deterministic green" — strike from AGENTS.md:27 + memory_tier_design.md:48; emit real count from boot_check; merge test_wave_driver/wave_driver_test twins; quarantine water_computer/wave_driver failures.
5. dashboard/static diet — untrack ractor_board.full-40k (9.8MB self-violating), topic_index.json, orphan_ledger.json; kill 53 .bak*; shelve 10 orphan HTML pages.
6. `mine/raw` 3.2GB — never git; move out of repo to a pointered corpus store (bounded pointers + hashes).
7. `reference/gstdcoin/` 27MB — delete; keep docs/ref/GSTDCOIN_REPOS_INDEX.md as receipt.
8. Root sweep — ~100 loose debris files (`_alpha_*`, `_g42/_g33`, wildmind media, `%SystemDrive%/`, 20MB tarball, correspondence mds) → inbox then delete.
9. Handoff unification — root `handoff/` (1,018 dead files, Aug 26) merged into `queue/handoff/`; evict .py from memory/working; pre-contract watch/ root artifacts → inbox.
10. Doctrine consolidation — AGENTS.md wins; de-duplicate boundary paragraph from ZCODE_SEAT.md + cursor .mdc; fix "Hermes parked" (dispatch log active Sep 9, $220 armed).

## Fix list — what the map was lying about (ARCHIVIST/CLERK)

1. AGENTS.md:8 ghost link → point at docs/archive/ZEITGEIST.md.
2. `configs/coding_session.yaml` missing while main.py:1551 defaults to it — create or repoint.
3. Fold the INDEX: `docker compose exec mag node /board/inbox/REVIEW_index_fold.mjs rebuild` (or host-patch `/board/inbox` → `watch/inbox`).
4. Two `corpus_index.json` (research_lens vs ractor_corpus) — rename one.
5. Missing file-level ownership: extend configs/modules.yaml beyond its handful; 980+ mag files ownerless.
6. Create the missing default config; add owner + test for the ~150 undocumented main.py subcommands, 10 at a time by lane.
7. tests pinning gitignored state — either move those contracts to tracked fixtures or track the dirs.
8. swarm_quests builds shadow_quests.json that nothing renders — give it a page or retire it.

## Wake-priority (SHERPA, verbatim from verdicts)

1. Fleet alive, host dead **by design** — `docker compose restart mag` is the restore; never a second host supervisor.
2. **Push the 23 unpushed commits** to Mag-backup.git before anything else — one disk holds the only copies.
3. Window-death runbook: 5 steps, proven (docker ps → rollout jsonl → inbox inventory → SESSION_RECOVERY receipt → resume).
4. Trust bytes over doctrine: test counts, heartbeat, git reflog, briefs — the Sep-14 bytes beat the Aug-06 prose.
5. W0.3 X archive drop is the operator-side boss; the republic chain queues behind it.
