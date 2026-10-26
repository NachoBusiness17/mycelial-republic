# SOUL FRONTIER COLLAB: the charter + Source of Mana combat bones map (2026-10-04)

From the operator's Discord paste (Sofan x ItsCommodore, 2026-10-04 12:01-13:02):
the plan crystallized - a co-built TOP-DOWN ZELDA/ALUNDRA CLONE with their own
story/lore. Roles: Sofan (operator) builds the ENGINE ("might take a crack at
one top down... after a platformer/mud; i have the mud i dont have a
platformer"); ItsCommodore (Adam) owns the COMBAT ("that will be the combat
system. I have such a stick up my ass for it being solid as fuck. It is a must
or the game will be trash") and his solo mission is "soul frontier". Compute
offer standing ("i'll even throw compute your way"). Adam's method: start from
an open project to conserve tokens, tear it apart, mash it with other shit,
"build it 3 times and then discover this exists".

## The combat bones inside sourceofmana (Adam's named love, mapped in bytes)

Clone: ../library_parked/sourceofmana @ c6c5445 (293MB, Godot 4, 278 .gd +
138 .tscn). The magic and summoning that felt "intuitive and challenging":

- sources/skill/Skill.gd - THE CORE: static Cast -> Process -> Handle flow.
  TargetMode SINGLE/ZONE/SELF; mana consumption gates the cast
  (TryConsume Mana); castTime + castAttackDelay timers; delayed-hit handles;
  ThrowProjectile for skill projectiles; per-map NO_SPELL flags.
  THE CHALLENGE MECHANIC IN ONE LINE: SkillCommons.GetRNG(hasStamina) -
  STAMINA BUYS A BETTER ROLL. Skill.Process consumes Stamina, and the hit
  handle binds the RNG WITH that consumption: spend resources to swing the
  odds. That is the intuitive-but-challenging feel Adam described, as code.
- sources/skill/abilities/ - ability components: Buff / Jump / Morph / Run
  (Morph = the shapeshift/summon-adjacent class; instant abilities short-
  circuit the cast flow via IsInstantAbility).
- addons/game_data_manager/ - COMBAT IS TABLES, NOT CODE: SkillTableView,
  SkillModifierTableView, EntitySkillsView, and a CombatSimulatorView (a
  combat simulator INSIDE the editor). Tune the game without touching GDScript.
- sources/: actor/entity/components (Visual/Interactive/Sfx), ai/, network/
  (server-authoritative), world/, map/, effects/, shaders/ - full engine
  anatomy to steal from.
- designs/: Backstory.md, Concepts.md, Design.md, Enemies.md, Lore.md,
  Prologue.md, Chapter-Tonori.md - the lore-doc template for their own story.
  The magic system lore: Zielite amulets (Brass -> Silver -> Gold -> Platinum
  rarity ladder) gate magic; Soul Menhirs are the respawn anchors; amulet =
  the key to avoiding death.
- entities.json is EMPTY (6 bytes) - entity data lives server-side (sources/
  sql/ + db migrations); the client ships the systems, the server owns the
  data. Clone the server tables for a full-game start.

## The estate differentiator only this collab can ship

PROVABLY FAIR COMBAT: sourceofmana's RNG is server-side (authoritative but a
black box). The estate's tools/dungeon.py sha256 dice carrier (chain-tip in
the preimage, actors never see rolls, golden vectors 19/13/8, session-tested)
drops into that RNG seat: every hit roll, drop, and crit becomes
cryptographically verifiable - the thing no ARPG has ever shipped. Pairs with
the gwap independent-cop pattern (bb0f34586) for anti-cheat verification and
tools/beat_map.py's {zone, hp, imp} damage contract for hit feel (hit-stop
and knockback impulses per body part, deterministic per track).

## Adam's Zelda-versions question, answered

- Link to the Past: snesrev/zelda3 - MIT C reimplementation, playable start
  to end, ships no assets (own-ROM extraction).
- Link's Awakening DX: the zladx community disassembly
  (github.com/zladx/ladx-disassembly; progress blog zladx.github.io; builds
  verified retail ROMs from your own supply) plus the Link's Awakening DX HD
  PC port built on it (map/world editor, Win/Linux/Mac/Android, on GitLab).
  Same legal posture as zelda3: no assets distributed.
- Catalog context: retroreversing.com tracks the decompiled-retail list.

## Engine build path (the operator's lane)

1. Start from the sourceofmana systems above (not a fresh project) - the
   token-budget law Adam named applies to compute too.
2. Gut the Mana lore, keep the systems; own story per designs/ template.
3. Swap server RNG -> dungeon.py carrier (provably fair).
4. Combat feel loop with Adam: SkillTable tuning (no code) + beat_map
   impulses; his solid-as-fuck bar is a tunable, not a rewrite.
5. Alundra note: Alundra = zelda-like with platformer sections - the
   operator's platformer itch and this project may be the SAME build.

fetched: 2026-10-04
Writer: zcode-53-strategy-window
