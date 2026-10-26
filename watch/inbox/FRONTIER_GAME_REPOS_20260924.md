# FRONTIER GAME REPOS — pattern-steal census (2026-09-24)

All URLs verified live against the GitHub API today. Status = last push.

## 1. Roblox architecture (lead steals)

**Knit is dead — don't adopt it.** https://github.com/Sleitnick/Knit — archived Jul 2024. Steal only its service/controller shape. sleitnick's live descendants are micro-packages: https://github.com/Sleitnick/RbxUtil (pushed 2026-08; Trove, Signal, Streamable, Component) and https://github.com/Sleitnick/RbxObservers (2026-08).
Steals: (a) **Trove**-scoped cleanup per portal ring / skeleton agent — despawn can't leak connections; (b) **Component** pattern for NPC agents (patrol state machine as a mounted component); (c) **Streamable** for zone load/unload lifecycles around portals.

**Networking: Red is dormant; Zap is the heir.** https://github.com/red-blox/Red — typed RemoteEvent wrapper, last push 2024-02. Successor in same org: https://github.com/red-blox/zap — pushed 2026-06, Rust codegen producing typed Luau bindings. Alternative: https://github.com/ffrostfall/ByteNet (pushed 2025-08), buffer-based serialization for high-frequency data.
Steals: declare the whole protocol in one typed file (protocol-as-code, compile-time checked); unreliable events for portal FX/NPC cosmetics, reliable events only for ledger mutations.

**Data: ProfileStore is the ledger spine.** https://github.com/MadStudioRoblox/ProfileStore (pushed 2025-07) — session-locked, periodically-saved DataStore profiles; ProfileService's official successor.
Steals: ledger = one session-locked profile per player; `Reconcile()` for schema migrations; append-only log field for filed workdays (matches our DNA).

**UI:** https://github.com/jsdotlua/react-lua (pushed 2025-05) — React 17 in Luau; or https://github.com/dphfox/Fusion (pushed 2026-02) — reactive Value/binding state. ("roach" does not exist — verified.) Steal: one reactive state tree feeding Basecamp HUD.

**Zones/portals:** https://github.com/1ForeverHD/ZonePlus — region+raycast enter/exit detection, far more robust than Touched. Steal: portal rings as Zone volumes (`entered` → FX + teleport); patrol anchors as invisible zones.

**Framework discipline:** https://github.com/Quenty/NevermoreEngine (pushed 2026-09-24, ~600 modules) — steal its module-per-package, shared server/client module structure.
**Probe / Ray:** no notable repos exist (verified) — dead ends.

## 2. Luau procedural generation

- https://github.com/greenviper126/Simple-Maze-Gen (MIT, 2024) — grid maze generator in Luau.
- https://github.com/EgoMooseOldProjects/Dungeon-generator (MIT) — classic room-and-corridor dungeon module from EgoMoose.
- https://github.com/CaidenSteele05/Procedural-Maze-Generator (2026-04) — tile-based 3D maze, configurable dimensions.

Steals: pure layout pass on an integer grid seeded with `Random.new(seed)` — no Instances until layout validates; then a separate build pass maps grid → parts. Store the seed per zone in the DataStore ledger so mazes are reproducible and shareable ("seed 4471" as content).

## 3. Single-file juicy games (structure steals)

- https://github.com/phoboslab/q1k3 — js13k 2021 overall winner (MIT). Raycast FPS in 13 kB; everything procedural, struct-of-arrays entities, zero garbage in the loop.
- https://github.com/KilledByAPixel/BounceBack — js13k 2020 overall winner (GPL-2.0). Zelda-like; pooled particles + oscillator-envelope sfx, no audio assets.
- https://github.com/jackrugile/radius-raid-js13k (MIT) — the textbook "juice" reference: every event fires particles + screenshake + sound.

Steals: (a) every gameplay event pairs **particle + sfx + shake** as one emitted bundle; (b) fixed-dt update, interpolated render, pooled particles; (c) procedural audio (oscillators) — zero asset weight, instant iteration.

## 4. AI-built games with prompts committed

- https://github.com/Kevin-Liu-01/Claude-of-Tanks (437 stars) — Three.js tank sim built end-to-end by a multi-agent Claude/Codex pipeline; pipeline and source in-repo.
- https://github.com/bridge-mind/turbo-kart-rush — kart racer built by five sub-agents from one prompt.
- https://github.com/tettethu/VibeGame (250 stars) — framework turning natural language into playable web games on Claude Code/Codex.
- https://github.com/lappemic/awesome-ai-built-games — index of vibe-coded games.
- https://github.com/jflam/sdd-space-invaders-claude — spec-driven + test-driven game build.

Steals: commit `PROMPTS.md` + per-agent transcripts beside the source (our biographer/residual habit, externalized); spec-first then tests, exactly the frozen-RIB/deliberate-ask posture.

## 30-second plan for our Rojo world

1. Wally: RbxUtil (Trove/Component/Streamable) + Zap + ProfileStore + ZonePlus.
2. Ledger: session-locked profile + append-only log; maze seeds stored per zone.
3. Skeletons: Components with Trove-scoped patrol FSMs; portal rings as Zones.
4. Juice rule from js13k: event → particle+sfx+shake, pooled, fixed-dt.
