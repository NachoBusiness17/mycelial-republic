# GAMING THEORY SELF-STEAL — cross-game mechanic transfer + the D&D layer (2026-09-17)

*Operator order: "introduce stat blocks, randomness of DnD spells monsters and physics,
tiny stories, rpg tools; self steal on our gaming theory; pad out our games to all learn
from one another's mechanics."*

## SHIPPED THIS PASS (bytes on disk)

- **D&D layer v1 in RUINS GO engine**: seeded stat blocks (mulberry32 by level id —
  deterministic, replay law holds), MONSTER_TABLE with traits ported from the mud's boon
  system (thorns / chain / berserk / arc / vision), 8 tiny tales in the parable register
  ("the charcoal is free. nothing else is."), UI renders stat block + tale at level start.
- Gate 51/51 still green. Classes (Squire/Rogue/Monk/Bard) already shipped player-side.

## THE TRANSFER MATRIX (what learns from whom)

| From \ To | RUINS GO | MUD | FRONTIER SOULS | SWARM |
|---|---|---|---|---|
| MUD | **boon traits** (SHIPPED: thorns/chain/berserk/arc/vision as stat-block traits) | — | boons already there; add **boonDraft on boss kill** | boon-like powerup drops on wave milestones |
| RUINS GO | — | **step-clock rooms**: puzzle chambers where mud monsters only move on player command (superhot already proves the mud can host it) | **grid puzzles as duels**: mirror-toll structure as a rival gunslinger | **parity gates**: spear-timing as swarm door mechanics |
| FRONTIER SOULS | **grudges**: a level that killed you names its snake in the HUD on retry (the tomb remembers) | grudge → mud NPC dialogue (the innkeeper mentions the thing that killed you) | — | grudge → swarm elite spawns hunt the killer pattern |
| SWARM | **horde-learns lite**: snakes prefer the direction you moved most (5-move history window) | mud patrols adapt route frequency to player traffic | swarm's habit-window drives ambush placement | — |
| Parable register | inscriptions (live) | innkeeper tales (mud has lore hooks) | wanted-poster micro-stories | wave-name stories |

## THE RPG TOOL LAYER (queued, in build order)

1. **Oracle dice** (d20 yes/no + how-table) as a shared JS module — used by the mud DM,
   RUINS GO tale rolls, and frontier encounters; one implementation, all games.
2. **Encounter generator**: pack-schema field `"encounter"` → stat-block roll + tale roll
   + terrain twist, validated by the gate (solvability still exact).
3. **Spell scrolls as pack items**: one-shot level modifiers (frost = snakes skip a tick
   once; knock = one denied move becomes legal). Each scroll is a mechanic from THE_WEAVE.
4. **Physics tags**: boulder momentum (pushed blocks keep sliding until blocked), rope
   (tether return on collapse cells) — engine v1.2, each behind its own gate test.

## LAWS HELD

- Randomness is SEEDED and recorded (mulberry32 + level id): replay stays byte-exact.
- No mechanic enters without a gate test; no tale enters without the parable register's
  voice (nameless, no em-dashes, nothing prosecutable).
- Transfer goes THROUGH THE LEDGER: each borrowed mechanic cites its donor game.

## falsifier

If after 20 new levels the cross-game traits (boon traits, grudges, habit-window) never
appear in gate-relevant behavior (only flavor), the transfer matrix is decoration —
collapse it to flavor tables and stop calling it mechanics.
