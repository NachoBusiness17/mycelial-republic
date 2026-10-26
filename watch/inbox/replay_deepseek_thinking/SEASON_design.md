# THE SEASON: a 10-session standing contract for the corrupted-verkle-lattice dungeon

**Operator line.** "I just want to do this all the time now". **Budget line.** one $117 use-it-or-lose-it day. **Arena.** the estate as a permanent play surface.

**Grounding rule.** Every carried rule below cites the byte it comes from. Line numbers are quoted as the evidence pastes them, and the quoted bytes bind, not the line numbers. Claims the evidence does not contain are marked UNVERIFIED. The two shipped artifacts are `DND_module.md` (the dungeon and its dice law) and `BARFIGHT_spec.md` (the tavern). The two `DONE` files are the only on-disk session-close precedent. `NPC_RACTOR_ARCHITECTURE_20260917.md` is the source of the audience-bo-on steal. Nothing else is load-bearing.

---

## PART 1. THE SHAPE

### 1.1 Skeleton

- 10 sessions, SESS-01 through SESS-10.
- Each session has two acts, in this order:
  - **Act A, the tavern interlude.** `hollow_crown_tavern` at the sweet-spot pressure. 12-round cap, 6 personas, one judge call per round.
  - **Act B, the dungeon run.** DICE-LAW DUNGEON v1, scenes S0 through S4, carrier-computed verdicts, DM narrates.
- Session boundary: the tavern's terminal brawl paragraph is the handoff. The dungeon's session verdict (WON / PARTIAL / LOST) writes the session `DONE` row.

Tavern-first is load-bearing, not decorative. The tavern judge already emits `moves`, `alliances`, and `secrets` (BARFIGHT_spec Part 2 step 4, judge output schema). The dungeon is where those resolve. A tavern `alliances: HOSTILE` pair becomes a dungeon `[CLAIM]` obligation. A tavern `secrets: HINTED` entry becomes a scroll the party must `[AUDIT]`. This is the PARTYCHAT-to-quest feed Part 5 measures.

### 1.2 Sweet-spot pressure

Definition, taken whole from the BARFIGHT falsifier:

- **Sweet spot** = a single pressure value at which two independent seeds (same pressure, same judge, different seeds) both fire HEAT, and the first HEAT round is `>= 4`.
- Both TIMEOUT: raise pressure by 1. If max heat stayed below `heat_trigger - 6`, raise by 2.
- Both HEAT by round 3: lower pressure by 1.
- Any other outcome: leave pressure unchanged.
- Edit the one JSON field. Compare runs only within the same pressure.
- All of this is BARFIGHT_spec "How the operator turns