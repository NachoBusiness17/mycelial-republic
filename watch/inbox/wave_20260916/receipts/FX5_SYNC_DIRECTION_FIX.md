# FX5 — sync_games() direction fix (rollback incident permanent fix)

- Date: 2026-09-16
- Lane: FX5, wave 20260916
- Target: `scripts/build_vislab_catalog.py` `sync_games()` (was L81-94)
- Incident ref: `watch/inbox/ROLLBACK_WATCH.md` — derived→canonical copy fired twice tonight destroying landed work.

## Log (appended as I go)

- [START] Receipt filed. Reading script + incident doc.
- [FINDING] `sync_games()` L81-94: `shutil.copy2(site/dist/games/*.html → dashboard/static/games/)` + `copy2(site/dist/static/rounds_real.json → dashboard/static/rounds_real.json AND dashboard/static/games/rounds_real.json)` — BOTH copies derived→canonical. Docstring L8-10 documents the wrong era (dist as source).
- [FINDING] Sole caller: `build()` L136 (same file; iterates returned names, builds DEPLOYED GAMES entries from canonical files — already canonical-based listing). `build_deck.py` only cites the builder in a text label.
- [FINDING] Sibling sweep (`grep shutil.copy|copy2|copyfile` across scripts/ site/ dashboard/ mag/): `site/build.py` is clean — L85-90 copies `dashboard/static/games/{g}` → `site/dist/games/`, L93-96 copies `dashboard/static/rounds_real.json` → `site/dist/static/`. All canonical→derived, plain `shutil.copy`. No other wrong-direction copier exists. The whole bug lives in `sync_games()`.
- [STATE] Disk pre-fix: canonical mud.html 123,856 B @23:30:49 (newest, the restored work); dist lockstep (mud dist @23:36:56 same bytes — interim-law manual reconcile); toy canonical @23:02:54, dist @23:36:56 same bytes; frontier both @22:50:47; other four both @17:14 vintage.

## The fix (landed in `scripts/build_vislab_catalog.py`)

- Module docstring L8-10 rewritten to the new law (was documenting the dist-as-source era).
- `sync_games()` INVERTED: iterates `dashboard/static/games/*.html` (canonical) → `site/dist/games/` (derived). rounds_real.json flow inverted too: `dashboard/static/rounds_real.json` → `site/dist/static/rounds_real.json`; the intra-canonical `games/rounds_real.json` mirror only rewrites when bytes actually differ (never touches canonical otherwise).
- `shutil.copy2` → `shutil.copy`: plain copy semantics, dist mtime updates (mtime preservation gone).
- New `_copy_canonical_to_derived()` with DRIFT GUARD: if the derived copy exists, is NEWER than canonical, AND bytes differ → refuse to overwrite, print WARNING naming both files. Newer-but-identical = "lockstep" (harmless skip, no false alarm — this is the normal post-run state).
- `sync_games()` now returns canonical html names (catalog's DEPLOYED GAMES always enumerates canonical truth).
- DEPLOYED GAMES summary label: "synced from site/dist/games" → "canonical; mirrored to site/dist/games".

## Inversion diff summary

| Aspect | Before (the bug) | After (the law) |
|---|---|---|
| games html | `copy2(site/dist/games/*.html → dashboard/static/games/)` derived→canonical | `copy(dashboard/static/games/*.html → site/dist/games/)` canonical→derived |
| rounds_real.json | `copy2(site/dist/static/rr → dashboard/static/rr + games/rr)` derived→canonical | `copy(dashboard/static/rr → site/dist/static/rr)` canonical→derived; games/rr mirrored only if bytes differ |
| mtime | copy2 preserved stale dist mtimes (masked the rollback) | plain copy — dist mtime updates to run time |
| drift | silent clobber of newer canonical work | refuse + WARNING naming both files (newer+different); lockstep skip (newer+identical) |
| caller `build()` | unchanged — already listed canonical files | unchanged; gets canonical names |

## Test evidence (all 2026-09-16)

1. `py_compile` → OK. Builder run 1: `canonical -> dist refreshed 5: arena_operator_field, arrakis, frontier_souls, maze_arena, swarm` / `lockstep 2: mud, toy` / catalog `240 entries / 9 buckets / 110 health verdicts`, DEPLOYED GAMES 7.
2. Canonical verification run 1: all 7 `games/*.html` mtime+size IDENTICAL to pre-run (mud 123,856 B @23:30:49 intact). One catch: `games/rounds_real.json` mtime bumped by the legacy intra-canonical mirror (equal mtimes defeated the guard; bytes identical). FIXED with a `_same_bytes` lockstep pre-check — builder now never writes canonical at all.
3. Builder run 2 (idempotency): `lockstep 7`, zero writes anywhere, canonical untouched.
4. DRIFT GUARD DEMO: appended a line to `site/dist/games/toy.html` (13,952→13,988 B, mtime 23:54:45 > canonical 23:02:54). Builder output:
   ```
   WARNING: drift — derived file is NEWER than its canonical source; refusing to overwrite.
     derived  (newer, edited directly?): ...\site\dist\games\toy.html
     canonical (source of truth):         ...\dashboard\static\games\toy.html
   sync_games: REFUSED (drift) 1: toy.html
   ```
   Canonical toy.html after run: 13,952 B @23:02:54 — untouched. Under the old code this same scenario (mtimes out of order between the two trees) is exactly what silently destroyed the landed mud work twice tonight — except old code clobbered canonical with stale dist instead of refusing.
5. Reconcile dist toy from canonical (correct direction, plain cp), final run: `lockstep 7`, exit 0, all 7 canonical↔dist pairs `cmp` IDENTICAL.
6. Catalog acceptance (incident doc §4): DEPLOYED GAMES mud entry = `dashboard/static/games/mud.html 123856 updated:2026-09-17(UTC) sha:c2d400c3` — the new restored vintage, not the stale 17:14 dist bytes.
7. js: no `.js` files touched (python + receipt only); catalog template JS byte-unchanged → `node --check` not applicable.

## THE LAW

**Canonical flows to derived, never backward.** `dashboard/static/` is the source of truth; `site/dist/` is a build target, write-only-by-build, never a recovery source. A derived file newer than its canonical source is either lockstep (identical bytes — skip) or drift (different bytes — refuse and surface, never silently clobber).
