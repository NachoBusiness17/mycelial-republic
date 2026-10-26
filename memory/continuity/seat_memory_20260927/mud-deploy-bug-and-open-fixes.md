---
name: mud-deploy-bug-and-open-fixes
description: RESOLVED 2026-09-14 (commit c71a03856) — build.py games path fixed to dashboard/static/games/, games dir committed, five MUD bugs fixed; still open — netlify deploy auth, websocket relay, walkers-through-walls
metadata:
  node_type: memory
  type: project
  originSessionId: sess_cc461d2f-b0e3-4197-8520-3684da78785a
---

Found by the fifty-wide sweep (2026-09-14); **fixed same day, commit c71a03856**:

- **RESOLVED — stale deploy.** build.py now sources GAMES from `dashboard/static/games/` (canonical, committed) with top-level fallback; verified dist mud.html ships the patched build (superOrbs present, served 200).
- **RESOLVED — five MUD bugs:** boon filter now excludes taken boons (no infinite stacking); Digit1/2 boon picks consume their keys AND weapon-swap handlers gate on `!G.boonDraft`; `nextLoop()` calls `puzzleReset()` (NG+ vault/key/chest/plates respawn correctly); mine-laying is dt-based (`0.36*dt`, capped 0.05 — fair inside SUPERHOT); rogue stealth renders at alpha 0.12-0.18 shimmer.
- **RESOLVED — git hygiene:** dashboard/static/games/, vislab/, scripts, research docs all committed in c71a03856.
- **Verified live in-browser:** draft offers exclude taken boons; boon pick no longer swaps weapons; puzzle respawns on nextLoop; ascension increments.

**Still open:**
- Netlify deploy needs operator auth — until then the site serves whatever the last deploy shipped (stale to the world, fresh on LAN/localhost).
- Walkers/k8/boss still chase through the vision polygon (occlusion cosmetic for enemies, tactical only for the ranger) — design decision pending: make occlusion tactical or leave.
- `G.ng` unbounded past ascension 20 by design ("meaner forever") but cascade totals go quadratic (1,568 K3 at ng20 = full-clear wall); tuning knobs live in mud.html.
- Websocket relay for multi-user (the ramp step 1) not started.

**Round 3 (evening, post-fifty-wide):**
- roomTick rewritten per-frame (the transition-gated version froze the state machine at "spawned 0" — the body only ran on room CHANGES; now it ticks every frame while the player occupies the room).
- Darkness 0.92 → 0.985 (enemies bled through unlit areas at 8% — the "sticking images" report).
- Fuse HP gate: combines only when survivors < 55% combined HP ("if you're beating them they combine").
- Victory gate: SIGILS.count >= 4 + no boss/k8/k3 alive (the premature "dragon falls by default" fix).
- MUD handle extended: DOORS/SIGILS/ROOM_STATE/syncDoors/stepUpdate/walls/doorRects getters for rAF-independent testing.
- Full walkthrough verified: 6 rooms, sigils 0→4, nave dragon + cascade, victory.

**Round 4 (playtest simulator + fifty-wide v2):**
- **Victory skipped the boss:** the clear fired at sigil 4 before the Nave ever activated — the victory check was vacuous on an unentered Nave. Fixed: roomTick sets `G.naveEverActive = true` on Nave activation and the victory check requires it. Verified both ways: 8 rounds at sigils 4 without Nave entry → state stays play; Nave entered + dragon killed + cascade cleared → victory.
- **Deploy-path sweep re-flagged C5 (stale top-level mud) as FAIL — stale finding:** the games-source fix landed in c71a03856; the sweep witness appears to have read a pre-fix state. Live curl serves the patched file.
- **Playtest harness findings (in-page MUD handle loops + onerror hooks beat external sweeps):** (1) drip counter double-incremented (spawnRoomEnemy ++ plus drip-branch ++) → Refectory spawned 2 of 3 promised — fixed by removing the drip-branch increment; (2) infirmary center (350,220) IS the bonfire — standing there re-fires rest every frame, respawning uncleared rooms (SM-authentic; step off to fight); (3) the nave center given (1580,500) is inside the FORGE rect — room rects overlap at borders, roomOf returns the first match.
- **Node line-splice edits into mud.html are error-prone:** the roomTick rewrite left spawnChampion unclosed, nested spawnAllEnemies, and an orphan tail — four brace repairs after one "successful" splice. Prefer Edit-tool anchored edits; brace-scan helpers must init depth AFTER the opening brace.

**How to apply:** canonical MUD source = `dashboard/static/games/mud.html`; `site/dist/games/mud.html` is build output (build.py copies it) — edit the dashboard copy, run build.py, done. window.MUD exposes step/pump for rAF-independent testing (backgrounded tabs throttle rAF to zero — pump instead).
