# Roblox Dev Craft Tutorials — Research Receipt (2026-09-24)

Scope: non-beginner craft material from respected Roblox devs. All URLs verified via live fetch/search on 2026-09-24. Knit and Red are confirmed ARCHIVED — do not start new work on them.

## 1. Educators (verified current status)

**GnomeCode** — youtube.com/@GnomeCode (144K subs, 268 videos, active 2025). Solo dev whose Roblox games claim hundreds of millions of plays; free tutorials at gnomecode.com. Flagship: **"How to Make a Doors Game" series** (ep. 1 "Generating Rooms") — DOORS-style room-by-room procedural generation, interactable doors/keys, Rush-style entity spawn windows, jumpscare UI + heartbeat audio. Also a full Tower Defense series. Steal: generate the next maze section only when the player advances (streamed rooms, not one giant map); entity spawn-then-despawn windows; door/key gating as pacing control.

**BrawlDev** — youtube.com/@BrawlDev, active 2025 ("Roblox Studio Tutorials" playlist incl. Viewport Frame GUI #16 2025; "How to Make Roblox Games in ONE Week"). DataStore tutorial covers `pcall()` wrapping, scopes, server interaction; Gamepasses video covers receipt-info purchase handling. Steal: ProfileService-style pcall/retry patterns for saving maze progress; viewport-frame item previews.

**TheDevKing** — youtube.com/@TheDevKing. "Beginner to Pro" scripting series (OrderedDataStores, leaderboards). Channel largely inactive since ~2023, but still the best-structured fundamentals reference. Pair with BrawlDev for current APIs.

**okeanskiy** — youtube.com/@okeanskiy (16.4K subs). Advanced "Beginner to Pro 2019" playlist (playlist: https://www.youtube.com/playlist?list=PLUUm0OvGDjJ-XgB2O02mN_deIeHS3-AHd) — ModuleScripts/services (#11.5), DataStores (#13). Dormant; and correction: his series is general advanced scripting, not a Rojo pipeline series. Treat 2019 API details as dated.

**sleitnick** — github.com/Sleitnick/RbxUtil (active, 464 stars; docs: sleitnick.github.io/RbxUtil). Modules: **Shake** (procedural camera shake), Spring (critically damped), Signal, Trove (cleanup), Component, Comm/TypedRemote (networking), Streamable. Credibility: authored AeroGameFramework; ex-industry. His **Knit framework was archived 2024-07-31** (github.com/Sleitnick/Knit) — use RbxUtil Component+Comm instead. Steal: Shake for skeleton-hit and entity-proximity feedback; Trove for killing AI loops on death; Streamable for streaming-enabled dungeon rooms.

**Quenty** — github.com/Quenty/NevermoreEngine (very active, 278 npm packages; docs: quenty.github.io/NevermoreEngine). Powers all Studio Koi Koi games, 1B+ play sessions. Maid/Promise/Signal/Rx, Binder, DataStore, layered camera stack, Octree. Steal: Octree for skeleton awareness queries in dense mazes; Binder pattern for tagging skeleton parts.

## 2. Procedural dungeon generation (Roblox-specific)

- GnomeCode Doors ep. 1 "Generating Rooms" — the reference implementation of streamed room gen.
- **EgoMoose** (top-tier community dev) — github.com/EgoMooseOldProjects/Dungeon-generator (2016, unmaintained but clean grid-cell Luau worth reading).
- Bryan0-0AG/Procedural-Dungeon-Generator_Roblox-Studio (2025) — weighted room templates, branching maps.
- Standard Luau pattern: 2D grid table → carve rectangular rooms → L-shaped corridors → `Model:PivotTo()` prefabs. BSP/cellular-automata threads live on devforum.roblox.com (search "procedural dungeon generation"). For a spooky maze: recursive backtracker on the grid + room-carving for encounter chambers.

## 3. NPC AI patterns

- DevForum: **"How To Use Roblox Pathfinding Service 2.0"** — https://devforum.roblox.com/t/how-to-use-roblox-pathfinding-service-20/1857779 (agent params, waypoints, PathModifiers).
- Guide w/ code: https://simplified.media/guides/roblox-npc-pathfinding (patrol/chase state machines + LOS).
- Guide w/ Luau: https://enderdevelopment.com/blog/en/roblox-npc-ai-pathfinding-smart-enemies (chase nearest player, patrol, attack).
- Video: "Pathfinding (AI, Dynamic Paths, Modifiers)" — https://www.youtube.com/watch?v=ckA4fVkAjIA
- **Weeping-angel freeze**: no dedicated open repo exists; the community pattern is camera `LookVector:Dot(toEntity) > cos(FOV/2)` + `workspace:Raycast` LOS (exclude the entity) → `Humanoid:MoveTo()` when unseen, anchor/pause when seen. Skeleton variant: slow patrol when unobserved, lunge when LOS first acquired (audio sting via Shake + Sound).

## 4. Game feel / horror presentation

- RbxUtil **Shake** + **Spring** for camera impact/proximity rumble; Signal/Trove for clean trigger wiring.
- Official Atmosphere docs (create.roblox.com/docs → Atmosphere): Density 0.4–0.7, dark Color/Decay, low Glare + ColorCorrectionEffect (Brightness −0.1..−0.3, Saturation toward −0.5, sickly Tint), `Lighting.ClockTime` night, near FogEnd, Bloom/DepthOfField. GnomeCode's Doors series demonstrates the jumpscare UI + layered heartbeat/stinger audio sync.

## 5. Professional pipeline

- **Rojo**: docs https://rojo.space/docs/v7; setup thread https://devforum.roblox.com/t/how-to-setup-and-use-rojo-may-2023/2322815; "Rojo for Roblox Actually Explained" https://www.youtube.com/watch?v=Zhl_NAPMztY; "Rojo + VSCode + Git setup" https://www.youtube.com/watch?v=ulBM7UdHk_4
- Framework reality check: **Knit (archived)**, **Red networking (github.com/red-blox/Red, archived Feb 2024)** — current pros use RbxUtil Comm/TypedRemote, Nevermore packages (npm/Wally + Moonwave docs), and selene/StyLua linting (RbxUtil's CI). Testing via Nevermore's test-runner packages.
- Steal: Rojo + git from day 1; Nevermore Binder for skeletons; Comm for client-predicted flashlight/door state.
