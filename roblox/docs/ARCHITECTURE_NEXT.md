# ARCHITECTURE NEXT — verified steals from the open-source Roblox world

**2026-09-24 · Sources: watch/inbox/FRONTIER_GAME_REPOS_20260924.md and
ROBLOX_DEV_TUTORIALS_20260924.md (all URLs live-verified by the wave).**

## ADOPT (when the mountain leaves Studio-toy scale)

| Need | Steal | Why |
|---|---|---|
| scoped cleanup | [RbxUtil](https://github.com/Sleitnick/RbxUtil) Trove/Signal/Component/Comm (sleitnick, active 2026-08) | every portal ring, NPC loop and sentinel gets Trove-scoped teardown; Component for skeleton agents |
| networking | [Zap](https://github.com/red-blox/zap) (typed codegen, active) or [ByteNet](https://github.com/ffrostfall/ByteNet) | protocol as one typed file; unreliable for FX, reliable for ledger mutations. Knit and Red are ARCHIVED (2024) — steal their shape, adopt nothing |
| the ledger spine | [ProfileStore](https://github.com/MadStudioRoblox/ProfileStore) | session locking + Reconcile() schema migration; the ShadowLedger grows up without wipe incidents |
| zone triggers | [ZonePlus](https://github.com/1ForeverHD/ZonePlus) | region/raycast enter/exit; Touched is a toy at scale |
| UI | [Fusion](https://github.com/dphfox/Fusion) (active 2026-02) or react-lua | for the ability cooldown chips and leaderstats pass |
| discipline reference | [NevermoreEngine](https://github.com/Quenty/NevermoreEngine) (Quenty, pushed daily, 1B+ play sessions) | the package architecture to imitate, plus test-runner + selene/StyLua linting |
| procgen | Simple-Maze-Gen (greenviper126), EgoMoose Dungeon-generator, CaidenSteele05 tile maze | pure seeded integer-grid layout pass, headless-testable, then a separate build pass; store seeds in the ledger — seed-as-content |

## ALREADY COMPLIANT (verified against the craft)

- Sentinel freeze = dot-product FOV + Raycast + anchor/freeze toggle — the
  community-standard weeping-angel pattern (no open repo exists; ours is homegrown).
- Atmosphere Density 0.55 + near FogEnd + desaturation sits inside the
  official horror recipe (0.4–0.7) from the GnomeCode Doors-series lineage.
- Client courier → RemoteEvents → server authority = the Comm pattern's shape.

## THE NEXT THREE CODE MOVES (from the tutorials wave)

1. ~~Streamed maze sections (GnomeCode ep.1 pattern) — the Ossuary builds its
   floors lazily around the player instead of 3 full grids at boot.~~
   **LANDED 2026-09-28 (Q-043):** `src/shared/SectionStream.luau` holds the
   pattern (one-shot section closures + center + radius, ordered mode keeps a
   shared SeedRng's draw order so a streamed build is byte-identical to the
   eager one). OssuaryZone builds floor 1 eagerly and streams floors 2-3 with
   one floor of lookahead; RiddleMazeZone streams its ~1,400-part wall grid in
   8x8-cell chunks (radius 120, budget 4/poll) — everything gameplay-bearing
   still builds eagerly. SpectralMaze (7 doors) and MazeArena (10 walls)
   judged too small to stream.
2. Rush-style spawn windows with audio pre-cue — entities telegraph by sound
   before sight (Doors pacing law). **STILL OPEN.**
3. ~~Trove cleanup on every task.spawn loop we hand-rolled — six loops in
   zones currently die by `task.delay` age, not ownership.~~
   **LANDED 2026-09-28 (Q-043):** `src/shared/Trove.luau` implements the
   RbxUtil Trove shape (Add/Connect/AttachToInstance/Clean/Destroy) plus a
   local `Loop(interval, fn)` extension (repeating thread the trove owns;
   body returns false to end itself). All six hand-rolled loops converted:
   HeadMuseum flush, LedgerExchange conveyor, LightMaze wisp, MudBasecamp
   night-terror, Swarm enemy, TheAnswerBoss fight (raw tracked thread there —
   a phase paces with two different waits Loop cannot express). Age caps stay
   as game behavior but now enforce themselves by destroying the subject; an
   early destroy cancels the thread immediately.

The cooldown-chips UI pass from the ADOPT table (UI row) also landed in the
same item, as plain Instances rather than Fusion — no vendor step exists in
this repo yet, so Fusion adoption stays an open move: `init.client.luau`
chips now carry a draining cooldown fill bar, an active-window stroke glow,
and a cluster dim while `Carrying` (the server's abilities-disabled penalty).

## THE PROMPTS-IN-REPO LAW

AI-built repos worth studying commit their PROMPTS.md beside the source
(Kevin-Liu-01/Claude-of-Tanks, jflam/sdd-space-invaders-claude, turbo-kart-rush).
We already do this (roblox/prompts/) — keep it law: every world feature that
was model-generated carries the prompt that generated it. Trajectory is
content; the repo is the record.
