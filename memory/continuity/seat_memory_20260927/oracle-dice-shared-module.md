---
name: oracle-dice-shared-module
description: oracle_dice.js shared RPG dice module — seeded mulberry32
  (deterministic, replay-safe), d4-d100, check/advantage/disadvantage, yes/no
  oracle, table picker, roll log; foundation of the RPG tool layer shared across
  all games
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---
Shipped 2026-09-18 at dashboard/static/games/oracle_dice.js. Seeded mulberry32 (same PRNG as the D&D layer engine); deterministic — seed 42 → same rolls every time. API: dN/d4/d6/d8/d10/d12/d20/d100, check(mod), advantage(mod), disadvantage(mod), yesNo(mod) returning yes_and/yes/no/no_and, pick(table), log() for receipts, reseed(seed) for deterministic replay.

This is the RPG tool layer's foundation — shared across mud, ruins_go, frontier_souls, swarm. The mud's boon gods and the D&D layer's stat blocks both route through this instead of bare Math.random.

Related: [[dd-layer-cross-game-transfer-20260917]], [[npc-seat-architecture-20260917]].
