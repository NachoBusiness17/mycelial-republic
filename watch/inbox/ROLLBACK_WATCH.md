# ROLLBACK_WATCH — temporary guard doc (until the mechanism is fixed at the source)

> **RESOLVED 2026-09-16 ~23:5x (FX5):** the mechanism is fixed at the source. `sync_games()` in `scripts/build_vislab_catalog.py` is INVERTED (canonical `dashboard/static/games/` → derived `site/dist/games/`, plain copy) with a drift guard (newer+different dist copy = refused + warning naming both files). Demonstrated: deliberately-edited dist/toy.html refused; canonical untouched across all runs; mud 123,856 B sha c2d400c3 in catalog. The interim operational law in §3 is no longer needed. Receipt: `wave_20260916/receipts/FX5_SYNC_DIRECTION_FIX.md`. Treat `site/dist/**` as WRITE-ONLY-BY-BUILD still stands.

Filed: 2026-09-16 ~23:3x · incident lane · companion receipt: `wave_20260916/receipts/INCIDENT_ROLLBACK_20260916.md`

## 1. Incident timeline (byte-evidenced)

| Time (local) | Event | Evidence |
|---|---|---|
| 17:03–17:14 | `site/build.py` builds dist; FX2 lane runs `build_vislab_catalog.py` ×3 (final 21:13Z = 17:13 local). `sync_games()` copies 17:14-vintage dist→games, stamping every canonical game with mtime 17:14:03.5x | FX2 receipt; all games' mtimes; `site/__pycache__/build.cpython-311.pyc` 17:03 |
| evening | FX4 (replay LCG), W5 (ascension), W1A (fleet seed), W2 (bones) land on `games/mud.html`; W1A lands toy; W3 lands frontier via canonical→dist→catalog law | lane receipts |
| ~22:47–22:51 | **Rollback #1/#2 (second rollback of the night, this incident):** catalog run at 22:50:47→22:51:22 syncs STALE 17:14 dist over mud/toy/swarm/arena/arrakis/maze canonical files. FX4+W5+W1A+W2 mud work destroyed; mtimes preserved at 17:14 by `shutil.copy2`. frontier survives (its dist copy was refreshed 22:50 by W3's law) | `dashboard/static/vislab/catalog.json` mtime **22:51:22.703**; W5/W1A incident entries |
| 23:02 / 23:04 | W1A re-applies toy (held) and mud additive fleet block | toy 23:02:54; mud 23:04:47 vintage |
| 23:17–23:29 | Concurrent restore lane re-lands FX4+W5+W1A+W2 mud work and extends harness to 35 lanes; iterating game+harness against the gate | mud.html 115,920→123,730 B; test_mud_replay.js 43,197→43,271 B |

Also destroyed in the family: `watch/inbox/WAVE_STATE_20260916.md` (rebuilt REBUILT-POST-INCIDENT tonight).

## 2. Mechanism (NAMED)

`scripts/build_vislab_catalog.py` → `sync_games()` (L81–94): `shutil.copy2(site/dist/games/*.html → dashboard/static/games/)` — **derived→canonical, mtime-preserving**. Fired by hand/lane invocation under documented-but-wrong doctrine (FX2 calls it "by-design"; G2 notes the mutation but only warns). No scheduler (full schtasks sweep clean), no watcher, no daemon (`mag-docker-watchdog` = docker engine check only), no OneDrive/KFM in path, docker containers mount but never call the builder.

**Re-fire condition:** ANY catalog run while `site/dist/games/*` is older than canonical. That condition was true all evening and is THE standing hazard.

## 3. Guard recommendation (in order of preference — recommend, not executed)

1. **Fix the direction at the source (the real fix):** invert `sync_games()` to refresh dist FROM canonical (`dashboard/static/games/*.html → site/dist/games/`) before cataloging, or gate the dist→games copy behind an explicit `--from-dist` flag that refuses when canonical is newer. One-line law: **canonical wins; dist is a build target, never a source.**
2. **Newer-mtime sentinel inside sync_games():** refuse (or warn-and-skip per file) any copy where `dst.mtime > src.mtime` unless `--force`. Catches every future stale-dist accident regardless of who holds the doctrine wrong.
3. **Checksum sentinel script (interim tripwire):** a tiny `scripts/canonical_games_watch.js` that sha256s `dashboard/static/games/*.html` + `watch/inbox/WAVE_STATE_*.md` into `watch/inbox/GAMES_SENTINEL.json` after every green gate run; any lane can diff before/after an edit session. Cheap, no OS deps.
4. **Read-only attribute dance (heavier):** after a green gate, `attrib +R` the canonical games; builders that try copy2 will fail loudly instead of silently destroying. Downside: every legitimate lane must toggle it — friction breeds workarounds.
5. **Move canonical games out of the synced path (structural, largest blast radius):** e.g. `dashboard/games_canonical/` served + synced one-way. Only worth it if (1)+(2) keep getting bypassed.

**Interim operational law (in effect until code lands):** after ANY edit to `dashboard/static/games/*.html`, byte-copy canonical→dist (`cp dashboard/static/games/X.html site/dist/games/X.html`) BEFORE any lane runs the catalog builder. Done tonight for mud.html + toy.html at 23:21:59/23:25; frontier already lockstep; other five games byte-identical both sides.

## 4. Who should do what

- Whoever owns `scripts/build_vislab_catalog.py` (CV5 touched it last): land guard #1+#2; rerun catalog; verify DEPLOYED GAMES entries show the new mud sha (123,730 B vintage, not 100,832).
- Wave coordinator: keep the concurrent restore lane exclusive on mud.html until its gate is green (verified 23:2x run: 29/35, six RED mid-restore — lane actively iterating).
- All lanes: treat `site/dist/**` as WRITE-ONLY-BY-BUILD; never a recovery source for canonical work.
