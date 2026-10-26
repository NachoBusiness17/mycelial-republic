---
name: dd-layer-cross-game-transfer-20260917
description: D&D layer v1 SHIPPED + traits MECHANICAL (vision pathfind, berserk
  double-move wired into step()); seeded stat blocks, mud-boon traits, 8 tiny tales,
  classes (Squire/Rogue/Monk/Bard); oracle_dice.js shared module; gate 51/51, pack
  30+ ALL PASS; transfer matrix + RPG tool queue with falsifier
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Operator orders 2026-09-17 night: "introduce stat blocks randomness of DND spells monsters
and physics and tiny storys as well as rpg tools — do a self steal on our gaming theory and
pad out our games to all learn from one another mechanics" + earlier "I also want to
incorporate more puzzle levels... same with the mud/games. I also want the dnd tools to be
used like the ones in our stuff. keep this shit working warmed."

**SHIPPED (commit f10546570):**
- **D&D layer v1 in ruins_go_engine.js**: `rollStatBlock(defId, seed)` + `rollTale` —
  mulberry32 PRNG hashed from level id (DETERMINISTIC — replay law holds; D&D randomness
  without breaking byte-exact replays), MONSTER_TABLE (8 monsters, Crypt Snake → Queen's
  Whelp) with traits PORTED FROM THE MUD'S BOON SYSTEM (thorns/chain/berserk/arc/vision —
  first cross-game transfer executed), TRAIT_TEXT one-liners, 8 TALES in the parable
  register ("The charcoal is free. Nothing else is."). UI renders stat block + tale at
  level start. Gate 51/51 held through the change.
- **Class system (UI-side, player chooses; determinism holds)**: Squire (pure), Rogue
  (BFS-derived first-move sight — compact solver in the UI), Monk (sealed bits survive
  death), Bard (tick parity always visible — spears readable). Built into ruins_go.html
  with class buttons; engine laws untouched.
- **briefs.json grown to 15**: 4 combo puzzles (climb+crank, parity-door, twin-light,
  push-descent) + 4 D&D encounter packs (Gelatinous Cube = block-in-corridor push-down;
  Mimic plate = real plate beside a collapse lure; Riddle Door = parity corridor with
  odd-arrival gem; Dragon Hoard = crank ring + greed-order collapse), plus decoration +
  boss tiers. First combo fire hit stealth-window 404s — retry law carries it.
- **Transfer matrix + falsifier** filed at watch/inbox/GAMING_THEORY_SELF_STEAL_20260917.md:
  mud→ruins boon traits [SHIPPED]; ruins step-clock rooms→mud; frontier grudges→ruins HUD
  names your killer; swarm habit-window→snake directional preference; parable tales→all.
  RPG tool queue: shared oracle-dice module, pack-schema encounter generator, spell scrolls
  as THE_WEAVE mechanics, physics tags (boulder momentum, rope) — each behind its own gate
  test, each citing its donor game in the ledger.
- **Falsifier:** if after 20 new levels the cross-game traits never appear in gate-relevant
  behavior (flavor only), the transfer matrix collapses to flavor tables honestly.

**Related lessons same window:** hand-probe writes can wipe canonical packs (restore =
git HEAD + promotion receipts, commit b197eb7a6); AMENDMENT 001 filed
(transport-deaths-never-count-as-attempts); briefs.json must stay one valid JSON array —
appending a bare object after the array silently breaks the driver's parse into QUEUE_EMPTY
(repair = split at array-close bracket, parse both parts, dedupe by id).

Related: [[ruins-go-shipped-20260917]], [[gaming-weave-20260916]], [[mud-superhot-adam-access]],
[[frontier-souls-adam-intake]], [[wing-chun-operating-lenses]], [[dd-layer-cross-game-transfer-20260917]].
