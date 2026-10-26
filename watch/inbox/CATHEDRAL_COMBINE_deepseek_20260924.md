# Cathedral combine — deepseek lane (deepseek-chat)

*8ms, free/metered lane, CLARITAS-neutral system prompt*

# THE CATHEDRAL — COMBINED WORLD SPEC v1

**One world, one law: gravity is computation, audit is the terrain, and every module is a room in the same house.**

## 1. THE THROUGH-LINE

The cathedral is a **single water clock**. Everything else is a lens ground to read it.

- **water_computer** is the *engine room*. Its tanks fill by gravity; the fill sequence IS the world's tick. The **OUT tank** is the cathedral's only source of *head* (pressure). Head flows out three ways:
  - **→ fractal_maze.field**: OUT water floods the maze's bending field. Field height = tank level. At scale-1 the field is 1 unit deep (walkable); at scale-2 it is 100 units deep (the maze *is* the field). The scale-1→scale-2 crossing is a **flood event**: when OUT hits the overflow weir, the player is lifted through the bend.
  - **→ audit_dungeon.verkle_knots**: every file the player touches in the audit folds a knot; knots are *checkpoints* stamped by the TRUST BYTES clerk. Knots are paid for in OUT-water (one knot = one tick of head). The audit is the *ledger* of the water clock.
  - **→ adventure_2d6.river_ford**: the ford is the OUT tank's surface seen from outside. The "glass door into a keep of clear pipes" is the water_computer's gallery viewed through the tank wall. **Loop closes**: river_ford north exit → water_computer.gallery.

- **riddler_optics** is the *read head*. Ten lenses, one per doctrine lie. Each lens, when collected, refracts the water clock's output into a readable number (a tank level, a knot count, a test count). The **lens_gate** in doctrine_library opens at 10/10 — the library *is* the optics garage's card catalog.

- **riddler_engram** is the *ten-seat session*: the cathedral's control room. Ten seats = ten lenses = ten audit rooms = ten water tanks. Each seat holds one invariant. No map; the seats are the map.

- **dnd_classic_stub** is the *keep walk*: 14 rooms that are the audit_dungeon's 14 rooms rendered as a classic dungeon. Same rooms, different system. The keep is the audit's *skin*.

- **blob-double** is the *physics proof*: three levels demonstrating push-duplicates-not-slides. This is the cathedral's *movement law*. Every push in every module obeys it. The water_computer's tanks push water, not slide it. The fractal_maze pushes the player, not slides them.

## 2. THE PLAYER'S PATH

1. **crossroads** (2d6) — read the post riddle. Answer: *a river*.
2. **river_ford** → **gallery** (water_computer). Learn the fill sequence. Fill OUT.
3. **OUT overflow** → **fractal_maze scale-1**. Walk the field. Find the bend.
4. **scale-2 crossing** — flood event. Emerge in **audit_dungeon.atrium**.
5. **Audit walk** — 14 rooms, north/east/south/west/down. Fold knots. Collect lenses in **doctrine_library** (10/10).
6. **lens_gate** → **riddler_optics.garage_gate**. Walk the ray through all ten lenses.
7. **riddler_engram** — ten-seat session. Each seat resolves one invariant.
8. **dnd_classic_stub** — 14-room keep walk as the *final audit*: same rooms, now legible.
9. **blob-double** — three levels proving the movement law. The cathedral's exit exam.

## 3. THE ONE SHARED RESOURCE LOOP

**HEAD** (water pressure, measured in ticks).

- **Source**: water_computer OUT tank. Fills by gravity, one tick per fill step.
- **Spend**: every audit knot costs 1 head. Every lens costs 1 head. Every maze step at scale-2 costs 1 head.
- **Earn**: solving a 2d6 room (≥7) returns 1 head. Passing a blob-double level returns 3 head. Resolving an engram seat returns 5 head.
- **Cap**: head_max = 10 (one per lens). At 0 head, the player is *dry*: can only walk scale-1, cannot fold knots, cannot open gates.
- **Loop**: fill → spend → solve → refill. The cathedral is a pump.

## 4. WHAT THE WATER_COMPUTER COMPUTES

The water_computer computes **the cathedral's clock rate**. Specifically:

- **Fill sequence** = the world's tick order. Each tank fills in a fixed order (gravity decides). That order is the *canonical sequence* every other module reads.
- **OUT level** = the world's *head budget*. It is the single scalar that gates fractal_maze depth, audit knot capacity, and lens availability.
- **Overflow event** = the scale-1→scale-2 crossing trigger. The water_computer *is* the fractal_maze's field generator.
- **Verkle knots** = the water_computer's *output log*. Every knot is a checkpoint; the audit_dungeon's TRUST BYTES clerk stamps them. The water_computer computes *what the audit is allowed to trust*.

In one line: **the water_computer computes the head that every other module spends, and the knots that prove it was spent.**

---

**Invariants (RIB_CATHEDRAL_WORLD_V1):**
- `water_computer.OUT → fractal_maze.field` — AGREE
- `fractal_maze.scale2 → audit_dungeon.atrium` — AGREE
- `doctrine_library.10_lenses → riddler_optics.garage_gate` — AGREE
- `adventure_2d6.river_ford → water_computer.gallery` — AGREE
- `blob-double.movement_law` — AGREE (all modules)
- `head` is the only shared resource — AGREE