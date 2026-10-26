---
name: mud-fifty-wide-playtest-20260914
description: MUD monastery was unwinnable until this round — d6/d7 door rework,
  Ossuary 8th room, 51-lane harness in scripts/test_mud_fifty.js is the
  regression gate for mud.html
metadata:
  node_type: memory
  type: project
  originSessionId: sess_cc461d2f-b0e3-4197-8520-3684da78785a
---

The 2026-09-14 fifty-wide playtest round found the Crimson Monastery **unwinnable**: d6 (the only door to the forge) required the forge cleared + 4 sigils, d4 was solid wall behind a painted door, the dragon spawned in the forge, and void strips let players walk around the whole map. All fixed; the sealed dead pocket became The Ossuary (8th room). The AFK soul farm (+60 souls/frame in cleared rooms) had silently returned — the `st.cleared` roomTick guard gets lost in edits; check for it.

**Why:** reading the file never caught these — teleports and eyeballing hid them. The 51-lane headless harness (`node scripts/test_mud_fifty.js`, DOM-shim + window.MUD) caught a real crash (fuse splice vs stale loop index → killEnemy must stay identity-based), the dead scent scan (oldest-first array + break = mechanic dies after 4s), and the map bugs. 6 consecutive green runs = stable.

**How to apply:** any mud.html change runs the harness before claiming done. Harness lessons: lane actors must clean up (a wounded walker dying to spikes mid-later-lane mints phantom orbs/ghosts); clear ROOM_STATE mocks or they leak through spawnAllEnemies' skip-cleared; startGame resets SIGILS/naveEverActive since this round. Flaky lane = design smell, not retry fodder. Related: [[mud-deploy-bug]], [[audit-our-way-game-medium]].
