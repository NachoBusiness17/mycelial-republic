# WAVE_STATE_20260916 — master index

> **REBUILT-POST-INCIDENT** (2026-09-16 ~23:3x, incident lane). The original 22:33 file by the F1
> fold lane was destroyed in tonight's rollback family (see
> `wave_20260916/receipts/INCIDENT_ROLLBACK_20260916.md` — `build_vislab_catalog.py sync_games()`
> dist→games backward sync; mechanism named there). This rebuild is composed from:
> F1's surviving close receipt (`wave_20260916/receipts/F1_FOLD_STATE.md`) + CV1/CV2 census
> receipts + a fresh on-disk enumeration taken at rebuild time. F1's exact §3 memory lines are
> LOST — the block below is RECONSTRUCTED to the same spec (11 lines, ≤200 chars, salon_50 fossil
> correction explicit). **Trust bytes, not reports** — re-verify any count before citing.

## §1 Receipt census

- At F1's 22:33 snapshot: **60 receipts** indexed (35 wave_20260916 + 25 physical_computing).
- Fresh enumeration at rebuild: `wave_20260916/receipts/` = **104** · `physical_computing/receipts/` = **57** (the wave kept landing after the fold — growth, not loss).
- Incident damage inside the receipts tree: **none lost** (the sync hit `dashboard/static/games/` + this file only).

## §2 Artifacts by program (F1 §2, verified-then vs now)

- Verified on disk at F1 time: `mag/wow_world.py`, `mag/wow_player.py`, `mag/hydro_xor_sim.py`, `scripts/test_toy.js`, `dashboard/static/games/toy.html`, `estate_walk.lod.html`, 3 test files, ractor-salon standalone repo — all present.
- Rollback family destroyed and (re)landed tonight: `dashboard/static/games/mud.html` (FX4 replay port + W5 ascension consumer + W1A fleet-seed + W2 bones — re-landed 23:17–23:22 by the concurrent restore lane, harness-gated), `dashboard/static/games/toy.html` (W1A re-applied, held), `watch/inbox/WAVE_STATE_20260916.md` (this file).
- Survivor: `dashboard/static/games/frontier_souls.html` (dist copy was fresh per W3's law).

## §3 Memory block (RECONSTRUCTED — paste-ready, each line ≤200 chars)

```text
- wave_20260916: 161 receipts on disk (104 wave + 57 physical_computing) at 23:3x rebuild; F1's 22:33 fold indexed 60.
- FOSSIL KILL: salon_50 is 39/50 (answered 39, failed 11) per memory/runs/salon_50_20260916/receipt.json — never "50/50".
- INCIDENT: dist→games backward sync (build_vislab_catalog.py sync_games, shutil.copy2 = mtime-preserving) rolled games back twice tonight.
- Incident mechanism NAMED: catalog builder at 17:14:03 and again 22:50:47→22:51:22 (catalog.json mtime pins it); no scheduler/watcher/daemon.
- mud.html lost FX4 replay LCG + W5 ascension + W1A startGame seed law; re-landed 23:17–23:22; gates = test_mud_replay/test_mud_fifty.
- toy.html (W1A fleet) and frontier_souls.html (W1A+W3) verified intact in bytes; swarm.html untouched.
- W5 consumer law: win → mud_asc=ng+1 persisted → fresh boot starts ascended; startGame(seed, asc) pins replay identity.
- W2 purity law: evlog events carry deterministic cause kinds only; cosmetic grudge names live in chronicle/bonesWrite, never the log.
- CV1: 35 local branches — 14 ATARI carry unique work; top revives = push Mag-backup.git, sovereign-mirror-scaffold dirty beta/v2, breadcrumbs+governor salvage.
- CV2: ~300-file unindexed inbox backlog; projects/memory/corpus/kungfu 71MB outside durable root; 98 orphaned scripts (69%) need triage.
- Requeue gen-2: G2+G3 stubs, G1 partial, X_MINE_FIGURES verdict pending, drafts/W1_union_alpha_draft.py (0-byte 429 orphan) + soft: B13 post ID, D20 gates, stale headers, D23 fossil line.
```

## §4 Gen-2 requeue (F1 §4 — carried verbatim from the fold close)

- **Hard:** G2 (stub) · G3 (stub) · G1 (partial) · X_MINE_FIGURES (verdict pending) · `drafts/W1_union_alpha_draft.py` (0-byte 429 orphan) · misfiled nested HERMES_REDTEAM_USAGE json.
- **Soft:** B13 bad post ID · D20 operator gates · stale headers · D23 fossil line (killed in §3 above).
- **Added post-incident:** `scripts/build_vislab_catalog.py sync_games()` direction guard (see `wave_20260916/receipts/INCIDENT_ROLLBACK_20260916.md` + `ROLLBACK_WATCH.md`) — until landed, every catalog run over a stale dist re-eats canonical games.

## §5 Counts

- Receipts: 60 at fold · 161 at rebuild. Artifacts: ~75 at fold. Requeues: 6 hard + 4 soft (+1 post-incident guard task).
- F1's original §5 closed: receipts indexed 60 · artifacts ~75 · stubs/orphans requeued 6 hard + 4 soft.

*Rebuilt 2026-09-16 by the rollback incident lane. No git commands. No paid APIs. $0.*
