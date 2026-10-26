# W2-L06: Teardown depth + licensing (wave 2 retry, verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore W2-L06) · **Class:** RECEIPT / feasibility
**Closes:** wave-1 lane L06 (1302 death) and noir-pack debt #9 (Teardown commercial/server licensing).

## Lua API reach (v2.1.0, teardowngame.com/modding/api.html)

- **NPC cops: spawnable, but NO documented NPC AI API.** Spawn()/SpawnLayer() for prefabs; player-character hooks only (SetPlayerCharacter etc.). Community cop NPCs exist (Swedish Police AI, a reskin of Modern Soldier NPCs) but are single-player-only as written, and the proven one was already community-removed for Steam guideline violations. AI must be hand-rolled from QueryPath/PathPlannerQuery (pathfinding), DriveVehicle (scripted driving), QueryAabbBodies/QueryRaycast/QueryRejectPlayer (perception), ConstrainPosition/ConstrainVelocity (physical pinning: workable for arrest/cuff mechanics).
- **Missions/win conditions: assemble from primitives.** Ui* family (client.draw only), PauseMenuButton, PostEvent/GetEvent, timers, StartLevel/Restart; arrest geometry via trigger entities (IsBodyInTrigger family). No dedicated win/lose function.
- **Persistence: registry save keys under savegame.mod ("used for persistent mod data") BUT per-machine local save only.** No server-side store. Cross-session persistence is only as durable as the host's savefile.
- **Multiplayer scripting (teardowngame.com/modding-mp): scripts split server/client/shared; server authoritative at 60Hz fixed timestep; docs MANDATE server-side game logic (scoring, rules, spawning, validation); shared state auto-synced read-only on clients.** Game modes are first-class; `#version 2` required or scripts are silently disabled in multiplayer.
- **Official game-mode library: mplib, MIT-licensed, github.com/tuxedolabsorg/mplib**: spawn/teamspawn tags, teams, hud (scoreboard, results, timers, world markers), countdown, stats, tools (loot crates), spectate, eventlog. The sanctioned skeleton for a cops-vs-robbers round mode; used by the built-in Multiplayer Classics.

## Multiplayer facts (official FAQ + store)

PC multiplayer launched (out of experimental); console MP planned 2026-09-15. Max 12 players, public/private, co-op and PvP. **Dedicated servers: NO, exact quote: "The host functions as the server and there are currently no plans to support dedicated servers."** Server-authoritative scripting yes (within the listen host). Mod sync automatic, published-unmodified mods only. No crossplay, none planned.

## Licensing (Teardown Terms of Use, 2026-03-06, store EULA page)

- Long-lived public servers: EULA SILENT, no clause addressing game servers; only built-in lobby hosting contemplated. Prohibited #3 bans emulators/places-to-play without written permission; #9 bans interfering with game servers. An ordinary 12-player lobby is plainly intended; an always-up service is not contemplated and has no supporting mechanism.
- Selling access: no explicit server-monetization clause, but Prohibited #2 bans buying/selling/sharing access to the Game; paywalled slots sit grey-to-risky. Everyone must own the game regardless. 12.2: published mods grant Tuxedo an irrevocable royalty-free license; 12.1 + Prohibited #6: their materials may only be used inside Teardown.

## Workshop inventory

Police: Raccoon City PD + station, riot police playermodels, Löckelle police vehicles (~180 "police" results). City maps incl. MP-ready: HL2 City 17 MP, Volia City districts, Tselona, Traffic City, City Center. Heists: Neverside/Underside/Turret Heist 2/Cullington + the Heist Example family as the de facto mission template. **Noir/1950s: the thin pillar** (retro vehicles, props, period radios; no era-city maps). The base game's late-70s Swedish-industrial palette gets you moody for free; the 1950s look is build-it, not download-it.

## Verdict (updates the noir pack ranking)

**Viable as a round-based 6v6 heist mode; NOT viable as a persistent world.** The 12-player cap is fine for cops-vs-robbers rounds, and mplib + the server-authoritative script split delivers ~80% of a round mode out of the box with one shared destruction battlefield. But "persistent" fails structurally: no dedicated servers (explicitly no plans), the host is a player whose exit ends the world, persistence is host-local registry, and monetized uptime is grey-to-risky. Plus the cop-fantasy tax: zero NPC AI API means AI patrol/chase/arrest is hand-rolled. Build "PAYDAY-meets-noir, destructible, 12 slots, session-based" on Teardown, or if the concept hard-requires a permanent world or monetized uptime, the substrate says no: that pushes the persistent-world requirement to FiveM (de-risked in L07) or UE5-native (L08).

## Agent debts

EULA quoted from the store page (full text parsed); console MP date from official pages (verify on arrival); workshop counts as of fetch time.
