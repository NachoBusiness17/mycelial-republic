# X INTEL: Adam's Link-to-the-Past build - the open-source steal map (2026-10-04)

Operator drop: the r/godot LttP open-world-design thread + "adam wants a link
to the past built can you help him find and open source project to steal like
this one for https://github.com/sourceofmana/sourceofmana"

## The four-pillar steal map (all license-verified at fetch)

| project | what it is | license | engine/lang | state | steal role |
|---|---|---|---|---|---|
| sourceofmana | open 2D MMORPG by The Mana World veterans; NOT a Square remake - original IP | MIT code + CC BY-SA-4.0 assets | Godot 4 (client + server), GDScript, Tiled | active TODAY (tip c6c5445 2026-10-04; 2,272 commits; playable solo + multiplayer, server-authoritative) | THE BASE - Adam's pick is right: cleanest full steal, original IP, multiplayer included |
| solarus-games/solarus | the Zelda-like 2D engine: C++ runtime, Lua quests, quest editor | GPL-3.0 (GitHub mirror archived 2018; dev on GitLab; 8,980 commits) | C++/Lua | mature | THE DESIGN GRAMMAR - dungeon/room/door/entity semantics are the LttP language; steal patterns, not the famous quests (those ship Nintendo-ripped assets) |
| snesrev/zelda3 | reverse-engineered LttP itself, playable start to end | MIT code; distributes NO assets (user extracts from own ROM) | C (70-80k LOC), SDL2 | 4.8K stars, active | THE PHYSICS REFERENCE - authentic movement, collision, corner-slide, enemy contact, room transitions; study, verify against its frame-sync test rig; do not ship Nintendo's design wholesale |
| flare-engine | single-player 2D ARPG (Diablo-class), original assets | GPL-3.0 + CC-BY-SA 3.0 default mod | C++/SDL2 | mature, low activity (2010-2013 core) | the fallback if single-player-only and GPL is fine; mod system + Tiled plugin |

## The IP line (what actually matters for "a Link to the Past built")

- The thing NOT to steal: Nintendo's assets, names, and overworld layout. A
  LttP-FEELING game with original assets is the lawful shape; a "Zelda"
  fangame ships takedowns.
- Source of Mana is the only pillar with zero inherited-IP baggage: original
  world riding The Mana World's CC BY-SA lineage. Share-alike applies to the
  ASSETS (Adam's derivative assets must also be CC BY-SA if mixed in).
- zelda3's posture: MIT code, no assets distributed, ROM extraction is the
  user's job. Study the code freely; the game DESIGN is still Nintendo's.
- Solarus engine: clean GPL. Solarus's flagship quests (Zelda Mystery of
  Solarus etc.) use LttP-ripped sprites - engine yes, those quests no.

## Recommended build path for Adam

1. Base on Source of Mana (Godot 4, MIT): clone in hand, playable today,
   server-authoritative multiplayer means the operator/Adam can co-op from
   two seats (the estate's phone+laptop pattern; a vast box later).
2. Steal the LttP grammar from Solarus quest docs: room-and-door topology,
   dungeon item progression (the "one item gates one region" rule), enemy
   key-and-lock design.
3. Study zelda3 for FEEL: the 8-directional walk, subpixel movement,
   corner-slide on collisions, screen-transition scroll, enemy contact
   knockback. Godot reimplementation of those constants beats guessing.
4. The estate cross-pollen (already banked, Godot-readable):
   tools/beat_map.py's damage-map contract {t, zone, hp, imp} JSON is a
   combat-feel feed a Godot game can consume directly (hit-stop, knockback
   impulses per body part); tools/dungeon.py's sha256 dice carrier
   (chain-tip preimage, actors never see rolls) is the fair-loot/fair-combat
   organ for any game Adam builds; the gwap independent-cop pattern
   (commit-bound verification, landed bb0f34586) governs any
   server-authoritative anti-cheat he grows.

## Honest limits

- The Reddit thread itself was unreachable through both doors (old.reddit
  serves a JS placeholder; the .json API 403s). Its design insights are
  embodied in the repos above; if Adam pastes the thread text it can be
  mined directly.
- sourceofmana cloned to corpus/library/sourceofmana @ c6c5445 (293MB,
  gitignored library pattern). Nothing executed; inventory only.
- Solarus activity lives on GitLab (GitHub mirror archived 2018) - cite
  gitlab.com/solarus-games/solarus for current state.

Writer: zcode-53-strategy-window
fetched: 2026-10-04
