# REPORT: destruction-tech stacks (inline bank, seat-authored fetches)

Provenance: the dispatched destruction-tech agent died in the z.ai 1302 storm (receipt in session log), so this vertical was banked inline by zcode-seat-20260926 via direct WebFetch on 2026-09-26. Three load-bearing sources fetched; the Finals inner-tech detail is named as a gap rather than guessed.

---

## Teardown (Steam app 1167630, fetched live)

- Multiplayer: yes, "Multiplayer chaos - up to 12 people", private or public lobbies across campaign, sandbox, and mods.
- Modding: built-in mod support with Lua scripting and Steam Workshop, using the same editor as the developers.
- Price: $29.99 (50% off $14.99 at fetch time, offer ends Oct 1); Ultimate bundle with 4 DLC $32.11.
- Destruction: "Fully destructible voxel environments" with physics, fire, water, vehicles. Released 2022-04-21, 95% Overwhelmingly Positive (76,276 reviews), 40-mission campaign plus sandbox and free "Art Vandals" mini campaign.

## The Finals (Wikipedia, fetched live)

- Runs Unreal Engine 5. Fully destructible environment is a core design pillar; destruction is physics-driven at the gameplay level: whole buildings collapse if support structures are targeted, large debris damages other buildings.
- Players can also build: deployable cover and Goo tools (Goo Gun, Goo Grenade, Goo Barrels) that solidify into destructible foam-like structures.
- Environmental effects interact (smoke extinguishes fire, fire ignites gas and burns goo).
- Embark producer quote: "Why open a door when you can use a rocket launcher to blow a hole in the wall, right?"
- A Eurogamer/Digital Foundry piece covers "next-gen physics destruction on PS5 and Series X/S at 120fps" (not summarized here; the custom-destruction-layer detail is a named gap, Embark tech talks unread this session).

## Shadows of Doubt (Wikipedia, fetched live)

- Voxel-based (models adapted from Concrete Jungle into pixel art and voxels), Unity engine, single-player only.
- Procedurally generated city: layout, citizens, routines, and murder cases generated per save; player sets city name, size, seed.
- Citizen simulation with daily routines; reviews note limits (repetitive dialogue, "slightly wonky" NPC behavior, generated inhabitants lacking depth).
- No mod tools discussed. September 2025 update added official modifiers including a Film Noir filter, permadeath, Ironman, rat detective, Snail Nemesis.
- ColePowered Games (Cole Jeffries), EA April 2023, full release 2024-09-26, published by Fireshine Games.

## Seat analysis (authored 2026-09-26)

- Teardown is the only ship-today product with The Finals-adjacent destruction AND official scripting AND multiplayer. Its gaps for this project: 12-player ceiling, and a voxel look that needs the noir print-shader layer to read as 1950s illustration (see REPORT_noir_shaders.md).
- The Finals' destruction layer is custom tech on UE5, not stock Chaos; the practical steal for us is UE5 Chaos (open) plus the Digital Foundry teardown as a design reference, owed as a debt.
- Shadows of Doubt is steal-the-design, not steal-the-engine: single-player Unity, closed, but it proves fully simulated citizens + procedural cases + noir filter as a product shape, and its modifier system (Film Noir, permadeath) is the GWAP knob panel we want.
