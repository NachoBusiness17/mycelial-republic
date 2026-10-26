# THE MOUNTAIN — the estate on Roblox

One experience. **Basecamp is the MUD** (the Roshomon engine, `mag/game_mud.py` as a place).
The climbs are the ported games. The summit is THE ANSWER. The Head Museum holds the
fleet's minds as AI NPC heads riding the free stealth lanes (`stealth/space-bunny-alpha`,
free on OpenRouter x2 keys + Nous mirror).

```
Basecamp (the mud: rooms, Vellum's hall, survey/claim)
  ├─ Head Museum (7 AI heads: elder, bard, economist, builder, research, ghost, janitor)
  ├─ SWARM       (122bpm disco bullet-hell + Fire pellets + streak announcer)
  ├─ RUINS GO    (grid capture)
  ├─ ARRAKIS     (speed is score; the Maker telegraphs before it breaches)
  ├─ SKI         (downhill, the yeti chase)
  ├─ LIGHT MAZE  → FLICKER TOWER (Tower-of-Hell law: no checkpoints, 8:00 rounds)
  ├─ THE ANSWER  (5 phases, the 15-degree tell, Wing Chun redirect)
  ├─ THE OSSUARY (Halloween: skeleton maze, weeping-angel sentinels, Bone Key, the King)
  └─ THE WAVE (zones_extra fan-out, 11 zones / 12 games):
     GALLERY · FRONTIER SOULS · TOY BOX · HARDWARE PRIMER · INCIDENT DUNGEON ·
     MAZE ARENA · SPECTRAL MAZE · RIDDLE MAZE (quantum eraser) · LIGHTMAP ROOMS ·
     EROSION FIELD · STEER FIELD
  └─ THE CATHEDRAL (the eigen-map plate, far south past the Wave): five doctrine
     regions placed BY their CATHEDRAL_CURVATURE_SCAN eigen_centroids - the world
     map generated from data, not hand-placed. The walker overlay (client) shows
     live eigen position + distance + bearing to every region; edges obey the
     referee's saddle law (none touch the DARK anchor).
```

Build gate: `bash tools/mountain_check` (structural lint → sourcemap →
luau-lsp semantic analyze with Roblox defs → place build). The built artifact
is `roblox/the_mountain.rbxlx` — open it directly in Studio, no Rojo needed.

## Play it (10 minutes)

1. **Install Rojo** (VS Code extension or `cargo install rojo` / `aftman add rojo-rbx/rojo`).
2. **Serve the tree**: in this folder run `rojo serve`. Default port 34872.
3. **Roblox Studio**: new Baseplate place → Rojo plugin → Connect. The tree syncs in.
4. **Fill the SKU ids**: publish once (File → Publish), create the Game Passes and Dev
   Products in the Creator Hub, paste their ids into `src/shared/Config.luau`
   (`id = 0` means disabled until filled; everything still runs).
5. **Enable Studio access**: Game Settings → Security → *Allow HTTP Requests* ON,
   *Enable Studio Access to API Services* ON (DataStores).
6. **Start the brain** (the NPC heads): on the host machine run
   `python tools/roblox_npc_gateway.py` — it serves `127.0.0.1:8771/npc` over the
   free stealth lanes with failover. Studio test clients can reach localhost;
   for a live published server, host the gateway on the fleet's public box and
   set `Config.Gateway.url`.
7. Play: talk to Vellum (sign or count the chairs), Survey a room (the heads
   witness the same scene; two agree = ROSHOMON CORE = Invariants), take a
   portal, climb.

## What is faithful (source → port)

| Source | Kept |
|---|---|
| game_mud.py (game_mud.v2) | rooms = systems, frontier questions, Roshomon core ≥2, claim = invariants, Hall prose, Vellum, "speak the count and they come" |
| swarm.html | 122 BPM, SPB = 60/122/2, spawn curve `max(0.07, 0.55 − 0.07·diff)/spawnMul`, horde count `(1+⌊diff·0.8⌋)·spawnMul`, depthMods, cursed upgrades incl. THE MOUNTAIN, the taunts; the flock (`shared/Flock.luau`, CLONED_MECHANICS §3.7): flee/tire/rest crop physics, boids school (cohesion + separation + wiggle), pheromone-trail horde steering (score floor 1.2), kill-drop toss, "the fish stir..." warn at 30 |
| arrakis.html | speed is score, spice chain = LINE ×N, crest launches, thumper ×3 redirects the Maker, gates bank, "the slow are safe and the safe are poor" |
| skifree.html | speed ramp, score/frame, trees, crash → yeti (faster than you), Extra Life rescue |
| ROBLOX_MONETIZATION_PLAN | SKUs: Double Score 99, Watchful Eye 199, Skip the Waiting 99, Salt-Cellar Key 299, Virtue Doubler 149, Answer's Weakness 499, Extra Life 49 |
| NPC = SEAT architecture | one ractor (the gateway), many faces (the heads); offline = honest recordings, never fabricated |

## The mesh layer (operator: "interactive layer for our mesh and our smart gps")

- **KSpace** (`src/shared/KSpace.luau`): every zone is an address (knowledge ×
  practice × depth). Items and choices index by it. `nearest(pos)` is the
  receiver read; `drift()` is the angular error between a claimed heading and
  the beacon — the smart-GPS drift pair, in-world.
- **CathedralMap plate + HUD** (`src/shared/CathedralMap.luau` +
  `src/server/CathedralPlate.luau` + `src/client/CathedralMapHud.client.luau`,
  ractor eigenmap-two 2026-09-26; the estate's ONE cathedral map since the
  2026-09-27 judge fold): the south plate where the world map IS the data,
  under ONE compass held in data, minimap and world at once - bearing 0° =
  north = eigen -y (the `tools/cathedral_eigen_map.py` formula, so every
  number matches a JSON recompute), the minimap draws -y up, and `toWorld`
  maps eigen -y to world -Z so the compass you walk is the compass you read.
  No edge - drawn or built - anchors on the DARK riddler_engram (referee
  ruling; it stands isolated). `pairwise()` freezes the 10-pair
  distance/bearing table. Falsifiers, repo-owned and rerunnable:
  `.venv/Scripts/python.exe tools/eigenmap_two_check.py` runs the module's
  real math under `tools/bin/luau/luau.exe` and diffs it against the scan
  JSON (receipt `watch/inbox/ractor_panel_20260926/eigenmap-two-check.txt`);
  `.venv/Scripts/python.exe tools/eigenmap_two_smoke.py` EXECUTES the plate
  and HUD scripts headless under Roblox-API stubs (build, derived portal
  landing, chain breathing, beacon Touched filing ShadowLedger rows, the
  live HUD readout; receipt `eigenmap-two-smoke.txt` beside it). A live
  Studio smoke stays owed (real GUI/physics/DataStore; debt filed in
  queue/todo.md P0 THE MOUNTAIN). The killed sibling build eigenmap-one
  (mirrored minimap, judge 2026-09-27) is byte-preserved in
  `watch/inbox/ractor_panel_20260926/cands/killed/`.
- **ShadowLedger** (`src/server/ShadowLedger.luau`): the room that remembers.
  Every observed choice lands in a DataStore keyed by player+day, and The
  Watchful Eye pass reads dispositions, not chat. Durable write law (t74):
  every append goes through one UpdateAsync on the player+day key, so
  concurrent records from multiple servers serialize and no row is lost;
  the stored value stays a plain array of entry rows, so saves written
  before this law read back unchanged.
  Disposition read law (B2-176, decided 2026-09-26): `disposition()` is
  SESSION-SCOPED by design. It reads the in-memory `sessionLedger` (what this
  server has observed), never the DataStore, so a Watchful Eye verdict on a
  fresh server is the blank string ("THE LEDGER IS BLANK. THAT IS ITS OWN
  VERDICT.") even when durable day rows exist. Rationale: disposition() is a
  synchronous call on the Watchful Eye hot path and a per-call GetAsync would
  add DataStore latency plus throttle exposure to a 199R SKU interaction for
  no record loss (the t74 write law already guarantees the durable rows);
  the durable day rows are the estate's record, not a verdict cache. The
  upgrade path if cross-server continuity is ever product-demanded: one async
  hydrate into `sessionLedger` at join or at Watchful Eye purchase, never a
  per-call store read.
- **NpcGateway** (`src/server/NpcGateway.luau` + `tools/roblox_npc_gateway.py`):
  the world's one HTTP nerve to the fleet. Receipts both sides: Roblox side in
  the ledger, Python side in `memory/runs/roblox_npc/gateway.jsonl`.
- **Leaderstats page** (`src/client/LeaderstatsHud.client.luau`, Q-041
  2026-09-28): the always-on-screen scorecard, top-right - VM, Rebirths,
  Invariants, Summits. A read-only mirror of the server's `leaderstats`
  folder (init.server.luau): the same four IntValues, Changed-signal bound,
  no second truth; the M-key player list stays the Roblox-standard view.

## Known gaps (honest)

- Basecamp speech now rides the `Chat` remote (Q-037, 2026-09-28): `say()`
  FireClients the speaking player, whose HUD stacks the last lines as a fading
  log (client/init.client.luau). The Studio-output print stays. Head answers
  still replace nameplate text, not chat.
- The swarm shoots (Z: `Abil_Fire` -> pellets -> horde deaths, SwarmZone) and
  the boss redirect is the full Wing Chun input (C: `Abil_Redirect` 1.5s window
  turns the wave, the only way to hurt THE ANSWER). Still open: the depth
  upgrade pool (SwarmZone `upgrades`, incl. the fire-rate row) is never offered
  mid-run, so depthMods stay at their defaults.
- Input is now dual-path (Q-040, 2026-09-28): the keyboard path is unchanged,
  and touch devices get ContextActionService buttons (sprint hold, dash, the
  four ability slots) with the cooldown chips re-parented over the ability
  buttons; the mobile jump button feeds the double jump via JumpRequest. The
  dash FOV kick was verified per-player, not rewritten (server stamps `DashAt`
  on the Player, client/init.client.luau listens on the LocalPlayer only).
  Button placement is a thumb-reach constant, not a verified visual: a live
  touch playtest stays owed.
- Rojo syncs scripts; terrain/textures stay hand-placed in Studio for now.
- SKU ids ship as 0 (disabled) until first publish creates the products.

*Ports are ports, not inventions: the Python engines are the source of truth.
Built 2026-09-24 in one burn on the free stealth lanes.*
