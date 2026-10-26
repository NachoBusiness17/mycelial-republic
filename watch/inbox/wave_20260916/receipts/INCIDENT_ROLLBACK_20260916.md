# INCIDENT_ROLLBACK_20260916 — receipt (append-as-you-go)

**Lane:** rollback incident response (second rollback tonight, escalated)
**Window:** damage window ~17:14–22:53 local, 2026-09-16
**Law:** no git restore (worktree uncommitted-by-design). Write/Edit only for source. dashboard/static/games/ = CANONICAL; site/dist = DERIVED. Any dist→games push is wrong-direction.

## Status: OPEN — assessment in progress

- [ ] 1. Damage assessment (mud/toy/frontier/swarm markers, WAVE_STATE, test scripts)
- [ ] 2. Mechanism hunt (what syncs dist→games)
- [ ] 3. Re-land: FX4 mud replay port / W5 StS consumer / W1A mud fleet-seed / verify W1A toy / restore WAVE_STATE
- [ ] 4. Verify: node test harness runs, node --check on edited files
- [ ] 5. Prevention: ROLLBACK_WATCH.md

## Damage table (file / was / now)

Assessment at lane start (marker census, 2026-09-16 ~23:1x):

| file | was (pre-incident) | now (bytes on disk) | verdict |
|---|---|---|---|
| dashboard/static/games/mud.html | FX4 port (105,849 B / 2,369 ln) + W5 hunks + W1A startGame seed law | 101,844 B @ 23:04:47 — pristine 17:14 vintage + W1A additive fleet block (FLEET_DATE/fleetSeedOf/FLEET_SEED, title line, MUD fleet exports, staging note L66-70). LCG `1664525`: **0** · evlog: **0** · runSeed: 1 (staging comment) | **REVERTED** — FX4 + W5 game-side + W1A startGame wiring gone |
| dashboard/static/games/toy.html | W1A fleet patch | 13,952 B @ 23:02:54 — `1664525`: 1 · fleetDate: 1 | **INTACT** — W1A's own re-application held (verified in bytes) |
| dashboard/static/games/frontier_souls.html | W1A fleet + W3 law | 94,903 B @ 22:50:47 — `1664525`: 1 · runSeed: 8 · SOULS_LEX: 6 | **INTACT** (survived because dist copy was refreshed 22:50 per W3's law) |
| dashboard/static/games/swarm.html | FX1 house pattern | 80,408 B @ 17:14:03 — SAFE_STORE: 9 · AUDIO_BASES: 6 · LCG: 1 | **INTACT** (dist copy identical → backward sync was a no-op) |
| watch/inbox/WAVE_STATE_20260916.md | F1 fold master index (present 22:33) | **MISSING** | vanished, same incident family |
| scripts/test_mud_replay.js | FX4 11 lanes + W5 ASC → 24 lanes | present @ 22:53, 43,197 B | **LANDED** (scripts/ not hit by sync) |
| scripts/test_mud_fifty.js | FX4 robustness + V/N12/L lanes → 63 | present @ 22:48 | **LANDED** |
| scripts/test_toy.js | W1A 15 lanes | present @ 22:50 | **LANDED** |
| site/dist/games/mud.html | stale | 100,832 B @ 17:14:03.590 — byte-identical to the reverted pristine | **SMOKING GUN** — the backward-sync source |

## Mechanism-hunt findings

**MECHANISM NAMED: `scripts/build_vislab_catalog.py` → `sync_games()` (lines 81–94).**

- It copies `site/dist/games/*.html → dashboard/static/games/` via `shutil.copy2` — **mtime-preserving**, exactly the incident signature ("17:14 mtimes PRESERVED on a revert").
- Direction is WRONG per front law: `site/dist` is derived; `dashboard/static/games/` is CANONICAL. dist→games is backward.
- Byte-evidenced firings tonight:
  1. **17:14:03** — FX2_SURFACE_RECONCILE.md: "build_vislab_catalog.py executed (×3 over the lane; final at 21:13Z)" = 17:13 local. This stamped the 17:14:03.58x–.60x mtimes on every canonical game (all seven still carry it).
  2. **22:50:47 → 22:51:22** — W3's surface law ran (canonical frontier → byte-copy to dist → catalog re-run). `dashboard/static/vislab/catalog.json` mtime **22:51:22.703** pins it. `sync_games()` then copied the STALE 17:14 dist mud/toy/swarm/arena/arrakis/maze back over canonical — **this is the second rollback**. frontier_souls survived only because its dist copy had just been refreshed from canonical (22:50:47, byte-identical — copy2 overwrote it with itself).
- **Re-fire risk: YES, unconditional.** No scheduler, no watcher, no daemon — the danger is any lane/human following the receipts' own doctrine: FX2_SURFACE_RECONCILE.md documents dist→games as "by-design", G2_STATIC_INFRA_AUDIT.md notes the builder "copies site/dist/games/*.html over dashboard/static/games/ (mutation)" but only warns; W3's law (canonical→dist→catalog) is safe ONLY if ALL games' dist copies are refreshed first. site/dist/games/mud.html is STILL the stale 17:14 pristine right now — one more catalog run before re-land eats the field again.
- Ruled out: Windows Task Scheduler (full verbose query, zero non-Microsoft/repo tasks), OneDrive/KFM (repo path is local `C:\Users\foste\Documents\projects…`, not under `C:\Users\foste\OneDrive`; Documents is the legacy local folder), docker containers (mag-sovereign/worker/redis bind-mount dashboard/ but no repo code calls build_vislab_catalog — grep found zero Python callers), no file-watcher configs, no recent .log files near site/ builders. The runner is manual/agent-invoked under documented-but-wrong doctrine.

## Repair summary

(pending)

## Harness outputs (verbatim)

(pending)

## Guard recommendation

(pending)

- [CLOSED] Runner sweep finished: zero callers of `sync_games()`/builder in dashboard/*.py + mag/**; `mag-docker-watchdog` task (every 5 min) runs `watch/docker_watchdog.ps1` = docker engine check ONLY, no file writes; `vast-bargain-loop` Disabled; MagImproveDaily/MagLabKit8765/MagPrivateOffice8765 Disabled. Verdict above stands: build_vislab_catalog.py sync_games() under wrong doctrine, invoked by lanes/humans. Re-fire risk live until dist refreshed + guard lands.

## Repair summary (updating as the lane proceeds)

- [23:2x] DISCOVERED: a CONCURRENT restore lane is actively re-landing mud.html (vintages 101,844 → 115,920 → 123,368 → 123,563 → 123,730 B between 23:04 and 23:29) and extending scripts/test_mud_replay.js (24 → 35 lanes). All mandated patches verified PRESENT in their landed bytes at 23:2x: FX4 LCG/evlog/seedRun + getters, W5 boot-load/victory-gate/forcedAsc-pin/run-receipt-asc/persistAsc/ascendForNextRun, W1A FLEET_SEED auto-seed + title line + fleet exports, W2 bones with the tomb-purity law (deterministic class cause; cosmetic killer name excluded — coordinator note #3 honored in their bytes at L1885-1892). This lane therefore STANDS DOWN from editing mud.html (collision hazard) and switches to verify-their-gate + the non-conflicting deliverables.
- [23:21/23:25] DEFUSED the standing re-fire vector: site/dist/games/mud.html + toy.html re-copied canonical→dist (right direction) after their vintages landed; cmp byte-identical. NOTE: dist must be re-synced again after the restore lane's final vintage (their loop is still active at 23:29).
- [23:24] Rebuilt watch/inbox/WAVE_STATE_20260916.md (REBUILT-POST-INCIDENT) from F1_FOLD_STATE.md close counts + CV1/CV2 census + fresh enumeration (104 wave + 57 phys-comp receipts). F1's original 11-line memory block was lost; the rebuilt block is reconstructed to spec and marked as such.
- [23:2x] Verification run #1 against the 23:22:51 mid-restore vintage: scripts/test_mud_replay.js → 29/35 lanes green, 6 RED (F1 non-vacuous, BD max law, ASC spawnBoss export, ASC no-double-bump, BN ghost chill — mid-restore edit seam; harness itself grew to 35 lanes with BN bones lanes). Honest intermediate numbers; the concurrent lane is iterating (game + harness edited again at 23:29:22, seconds after this lane's run). Final gate run(s) to follow when their loop settles.
- [23:3x] Filed watch/inbox/ROLLBACK_WATCH.md (timeline + mechanism + 5 ranked guards + interim operational law).

## FINAL — gate results (verbatim)

Settled vintage: `dashboard/static/games/mud.html` 123,856 B / 2,620 lines @ 23:30:49 (concurrent restore lane's final; this lane verified, did not edit). dist lockstep: byte-identical (`cmp` clean, canonical→dist copies 23:36:56). mud sha16 `c2d400c32e8a6da4`, toy sha16 `881d2fca8e72f792`.

`node scripts/test_mud_replay.js` — **41/41 lanes green × 3 consecutive runs** (R/F1/F2/G 1-11, BD 12-16, LOOT 17, ASC 18-24, FLT 25-28, BN 29-35, GP 36-41). First post-edit run was 40/41 (lane 40 RED: "the champion kept no grudge") — a transient racing the restore lane's 23:38:08 harness write; a standalone instrumented probe of the same duel law PASSED (champion filed `took` @ frame 121, state=dead, `champGhosts.crypt.grudges = [slain, took]`), and the three clean re-runs confirm. Intermediate honest numbers: the mid-restore 23:22:51 vintage measured 29/35 (six RED edit-seams: F1 non-vacuous, BD max law, ASC spawnBoss export, ASC no-double-bump, BN ghost chill).

```
PASS 40 GP: the ledger is capped (5, newest kept); a champion victory files "took" through the real kill path
PASS 41 GP: replay law with lived ghosts — same seed + tape + ledger twice -> byte-identical trace + evlog

41/41 lanes green
mud: 2620 lines, seed 20260916, 1800 steps @ 60fps, tape A 14 events, runSeed 20260916
```

`node scripts/test_toy.js`:
```
PASS 13 FLT: default load (no seed) = the fleet seed of the reported UTC day
PASS 14 FLT: two fresh same-day loads share the seed — the fleet ritual
PASS 15 FLT: explicit seeds always win — start(4242) overrides the fleet seed

15/15 lanes green
toy: 243 lines, seed 20260916, tape A sha 678ddd9d2e189555…, verdict win, duration 1.717s
```

`node scripts/test_mud_fifty.js`:
```
PASS 63 L: kill-drops draw the same stream — same seed, same kills, same drop outcome

63/63 lanes green
```

Syntax: `vm.Script` compile of the extracted game script — `mud.html syntax OK`, `toy.html syntax OK` (node --check equivalent; no bare `node --check` exists for html).

## Repair summary (final)

| Item | Disposition |
|---|---|
| FX4 mud replay port | Re-landed by the CONCURRENT restore lane (23:17–23:30); this lane verified in bytes + 41/41 gate |
| W5 StS ascension consumer | Re-landed by the same lane (boot-load, victory gate, title/start UI, `startGame(seed, asc)` pin, persist/nextLoop, exports incl. spawnBoss); ASC lanes 18-24 green |
| W1A mud fleet-seed | Landed: `FLEET_SEED` auto-seed L2496, title line, fleet exports; FLT lanes 25-28 green |
| W1A toy patch | VERIFIED intact (W1A's own re-application held): 15/15, `1664525`+`fleetDate` present, sha16 `881d8fca`-family (881d2fca8e72f792) |
| W2 determinism note | Honored in the landed bytes: tomb evlog carries deterministic class cause (`player.lastHitEnemy.type`), cosmetic grudge name confined to SAFE_STORE record + whisper (game L1885-1892) |
| watch/inbox/WAVE_STATE_20260916.md | REBUILT-POST-INCIDENT by this lane (F1 close receipt + CV1/CV2 census + fresh enumeration; F1's exact 11-line memory block lost, reconstructed to spec and marked) |
| dist rollback vector | DEFUSED: canonical→dist byte-copies for mud + toy (cmp clean); next catalog run is a no-op for these files |
| Guard | `watch/inbox/ROLLBACK_WATCH.md` filed: timeline, named mechanism, 5 ranked guards, interim operational law |

## Guard recommendation (short form — full detail in ROLLBACK_WATCH.md)

Fix `scripts/build_vislab_catalog.py sync_games()` direction (refresh dist FROM canonical, or refuse dst-newer-than-src copies without `--force`); until code lands, the standing operational law is: after ANY canonical games edit, byte-copy canonical→dist BEFORE anyone runs the catalog builder. The builder is invoked by lanes under documented-but-wrong doctrine (FX2 calls dist→games "by-design") — the doctrine line in FX2_SURFACE_RECONCILE.md and G2_STATIC_INFRA_AUDIT.md needs the same one-line correction.

## Status: CLOSED (with attribution)

Damage assessed · mechanism NAMED (`build_vislab_catalog.py sync_games()` dist→games, `shutil.copy2` mtime-preserving; catalog.json 22:51:22.703 pins the 22:50:47 firing; 17:14:03 firing pinned to FX2's 21:13Z catalog run) · lost work re-landed (concurrent lane; this lane verified + defused the vector + rebuilt WAVE_STATE + filed the guard) · all gates green (41/41 ×3, 15/15, 63/63). No git commands used. No paid APIs. Probe file deleted; only inbox artifacts + this receipt written by this lane.
