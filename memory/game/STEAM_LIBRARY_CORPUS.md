# STEAM LIBRARY CORPUS — the installed games, mined like our own corpus (2026-09-14)

Source: `C:/Program Files (x86)/Steam/steamapps/common` — 16 games fingerprinted by marker files,
engines corrected against public tech records. Machine-readable twin: `steam_corpus.json`.
Purpose: game-type candidates + mechanics to steal for MUD / the ramp (tabletop → mud → roguelite).

## THE HEADLINE

**6 of 16 games run engines their authors wrote themselves.** Exanima (Rayform), Destiny 2 (Tiger),
Dwarf Fortress (custom C++), PoE2 (Grinding Gear custom), BG3/DOS2 (Divinity 4.0, Larian).
The operator's instinct — hand-rolled, beacon public, provenance private — has the best company
in the library.

## THE EXANIMA STEAL (shipped today)

Exanima runs **Rayform**, a fully in-house engine: custom physics (rebuilt from scratch mid-development),
custom renderer, dynamic motion synthesis for enemy animation, `.rpk` resource packs, OpenAL audio.
Madoc Evans wrote graphics, physics, audio, UI and tooling himself — a 3.9MB exe for a whole engine.
Binary analysis found Borland register conventions, suggesting a Delphi-adjacent origin.

**Shipped in MUD (mud.html, 2026-09-14):** torch-light vision with wall occlusion —
raycast visibility polygon against wall segments, soft radial falloff, torch flicker,
enemies hidden when occluded or out of the 270px attention radius. Verified by canvas dump:
hard shadow edges behind walls, lit-area dropped 40% → 21%.

Steal-list still open from Exanima: physics-driven melee (momentum over animation),
per-limb damage, motion synthesis, and Exanima's own structure lesson — *it is the prelude
that funded and field-tested the big game* (Sui Generis), exactly our parables → game ramp.

## THE SHELF

| game | appid | engine | confidence | steal for our builds |
|---|---|---|---|---|
| Exanima | 362490 | Rayform (in-house) | researched | torch vision (SHIPPED), physics melee, motion synthesis |
| Gunfire Reborn | 1217060 | Unity | fingerprinted | powerup synergy (SUPERHOT drop owes it), elemental procs |
| Megabonk | 3405340 | Unity | fingerprinted | 3D survivors horde budgeting |
| Slay the Spire 2 | 2868840 | Godot | fingerprinted | card-intent state machines; Unity→Godot migration story |
| Slay the Spire | 646570 | Java/libGDX | fingerprinted | deterministic seeded runs |
| Baldur's Gate 3 | 1086940 | Divinity 4.0 (Larian) | known | reactivity; the world remembers |
| DOS2 | 435150 | Divinity (Larian) | known | elemental surface combos |
| BG1/BG2 Enhanced | 228280/257350 | Infinity EE (Beamdog) | known | D&D 2e rules as data |
| Satisfactory | 526870 | Unreal Engine 5 | fingerprinted | factory logistics as idle loops |
| DOOM Eternal | 782330 | id Tech 7 | known | arena encounters; refuel-by-violence pacing |
| Destiny 2 | — | Tiger (Bungie) | known | live-ops cadence |
| Marathon | — | Unreal 5 | known | extraction loops |
| Dwarf Fortress | 975370 | custom C++ Premium | known | simulation-as-content; legends-mode history |
| Stardew Valley | 413150 | MonoGame/FNA | fingerprinted | one-dev scale; SMAPI mod API as adoption lever |
| Path of Exile 2 | 2694490 | custom (GGG) | known | endgame orbit; skill-link systems |

## CANONICAL TECH LINKS

- Exanima Modding Toolkit — Engine Details (Rayform): https://exanimamodding.codeberg.page/Book/contributing/game_engine/engine_details.html
- Bare Mettle forums — all tech original, no middleware: https://www.baremettle.com/forums/index.php?threads/can-the-physics-engine-of-exanima-be-applied-to-other-types-of-games.7384/
- Exanima: A Complete Development History (6 parts): https://steamcommunity.com/app/362490/discussions/0/801218545819173932/
- Sui Generis Kickstarter (origin): https://www.kickstarter.com/projects/1473965863/sui-generis
- Store pages: https://store.steampowered.com/app/<appid> per table
- PCGamingWiki per game: https://www.pcgamingwiki.com/wiki/<Game_Name>
- Engine docs: https://unity.com · https://www.unrealengine.com · https://godotengine.org · https://libgdx.com · https://monogame.net
- id Software open-source releases (id Tech lineage): https://github.com/id-Software

## NEXT MINING WAVES (declared, not done)

- save-file forensics per game (StS profile JSON, DF legends, Exanima .rpk unpack)
- PCGamingWiki API sweep per appid → engine/monetization/modding columns
- link filing into watch/inbox/LINKS.jsonl (canonical registry, dedupe first)
- lane tasks: "launch 16 wide" — one witness per installed game, mechanics report each
