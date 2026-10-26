# L1 — Race/Dice Engine (DRAFT) — `L1_engines/race_dice.DRAFT.md`

> **Status:** DRAFT. **Class:** L1 family engine — one mechanical spec shared by every race game
> (Senet → Ludo). **Provenance:** primer §7 build-order #1 (ships with L0), Fact 7 taxonomy.
> **Research status:** family-level rules (`attested` for Ludo/Pachisi/S&L; `reconstructed` for
> Senet/Ur/Patolli). Appended per-game deltas carry their own flags; never silently upgrade.
> Consumption order: L0 contract (above) → this engine (family mechanics) → one game pack (deltas)
> → L2 statics → L3 cultural pack.
>
> ---
>
> [PROMPT-BODY-START — byte-stable from here]

## RACE/DICE ENGINE — FAMILY MECHANICS

A **race game** is a track of ordered squares; each player's pieces advance along the track in a
fixed direction, the move amount decided by the seeded RNG, with the win condition defined by the
game's pack. You apply these mechanics exactly as written, plus the pack deltas, never anything
else.

### TRACK (two shapes)

- **linear** — `ranked [0..N-1]` squares, index 0 is the start, index N-1 the last square before
  the bear-off. Play proceeds monotonically toward N.
- **ring** — a closed loop; pieces may lap. Encode as linear indices `0..N-1` where index N wraps
  back to 0; a pass over the "far edge" may trigger a pack rule (e.g., Patolli's turn).

### MOVEMENT

- Move amount comes ONLY from the seeded RNG (L0 Universal RNG). If the roll exceeds the remaining
  distance to the final square in a **linear** track where a game forbids overshoot, clamp the
  move to land on the final square (`land-exact`) or ignore it (`roll-exact`), per the pack.
- **Seeded movement:** the destination square is `(current + roll) mod N` for ring, and
  `min(current + roll, N-1)` with `land-exact` for linear unless the pack says otherwise.
- A piece may be **blocked** by an occupied square of an opponent-specific kind only if the pack
  defines blocking; otherwise squares are concurrent.

### PER-SQUARE EFFECTS TABLE

Each pack supplies `SQEFFECT[square-id] -> { effect, target, param }`. On landing (after movement,
before any capture resolution), resolve the effect in this fixed order:
1. **advance/retreat** by `param` (`+k` moves forward, `-k` back);
2. **jump** to a specified square-id;
3. **reroll** (draw again from seeded RNG for this same turn);
4. **miss-a-turn** (skip next active-role turn);
5. **safe/ritual** (mark square so pieces there may not be captured);
6. `none` — no effect.

Each effect is applied exactly once per landing; a pack may chain effects (e.g., landing on an
effector that then itself has an effect) by listing them in sequence in the pack.

### CAPTURE-ON-LANDING FLAG

`CAPTURE: on | off`. When **on**, a piece landing on a square occupied by an opponent piece (and
not a `safe` square per effect table, and not `blocked`) removes that opponent piece from the
board and returns it to that opponent's `start`/`stock` (per pack). When **off**, landing on an
occupied square either co-locates (no effect) or follows the pack's `block` rule.

### BEAR-OFF / WIN

- **linear:** once a piece reaches N-1 (final square), it is eligible to **bear off**: on a
  subsequent exact-or-higher roll it leaves the track to the finish line. **WIN** when the required
  number of pieces (per pack, default all) have borne off. If a `roll-exact` pack, only an exact
  roll bears off.
- **ring:** **WIN** when the first piece completes the required number of laps (per pack) and
  crosses the finish line exactly, unless the pack defines otherwise.
- In either shape, if pieces must start off-board / in a home stock and enter on a qualifying roll
  (e.g., 1 or a 6/invariant; per pack), apply the pack's `ENTRY` rule, which is part of the pack
  and not of this engine.

### FAMILY PACK-DELTAS (sketched — each becomes its own pack)

1. **Senet** — `linear 30`, `CAPTURE: off`, no blocking. **(reconstructed: Kendall 1978 /
   Piccione 1990 two-school.)** Ritual squares **26–30** have special effects (often 27–30 as
   passing/judgement squares); SQEFFECT groups squares 26–30 to the afterlife exit; pieces may be
   "blocked" only by the ritual-safe flags at squares 26+, not captured. Move dice: **casting
   sticks** (4-stick 0/1 count per L0 historical mode). Roll-exact entry.
2. **Royal Game of Ur** — `ring` 20-square path (two routes, per pack: long / short as attested),
   `CAPTURE: on` at rosette squares. **Dice: Ur binary tetrahedral** (4 marked-face dice, count
   0..4, reconstructed from BM 33333, Finkel). Rosettes are `safe` squares (no capture). Roll-exact
   movement.
3. **Patolli** — cross-shaped board mapped to a ring with a **cross-track turn** (pieces cross a
   per-scheme junction), `CAPTURE: on`. **Dice/beans: marked beans** (5 beans, count of marked
   drawn, seeded finite pool). **1569 ban history** is a cultural-pack note, not a rules change.
   **(reconstructed: Durán; Murray.)** Win = track completion.
4. **Pachisi** — cross/lap ring, `CAPTURE: on`, `safe` at home/central squares. **Dice: cowries**
   (count of open, with the all-open double-count per school). Pieces enter from a home-stock on a
   qualifying roll. **attested** (period accounts; modern cross-cultural variants differ only in
   pack swappables).
5. **Ludo** — commercial reskin of Pachisi (**attested**: patented, rules effectively fixed).
   `linear` per-arm 4×? uses the same four-arm cross; rolling **single `1d6`** (modern mode) with
   entry-on-6 and a 6→bonus-turn; `CAPTURE: on` at non-safe squares, `safe` at start-square each
   arm; block-2-for-a-blockbuster + exact-entry `roll-exact`; WIN = all 4 pieces borne off.
6. **Snakes & Ladders** — `linear` N (classic 100), `CAPTURE: off`, no blocking, single `1d6`
   (modern), `roll-exact` land on final square → WIN; landing with `SQEFFECT` on ladder = `jump`
   up, on snake = `jump` down. **(attested; virtue/vice theme and chutes/ladders is cultural, not
   mechanical; capture stripped by design.)** No piece interaction by construction.

### OUTPUT / INSTANCE NOTES

- Apply L0 OUTPUT CONTRACT before and after any move: restate the canonical state with the
  `^` line, cite the movement clause and RNG mode, emit the new canonical state.
- Roll results are reported (never chosen) from the seeded table; a roll is an instance datum, not
  a narrative flourish.
- Any collision between this engine and a pack delta resolves **delta wins** for the specific
  clause, except engine clauses that are structural (track shape, capture order, bear-off
  machinery), which the pack may not override.

[PROMPT-BODY-END]

---

## Asset notes (NOT cached prompt body)

- **Target size:** 800–1.5k tokens of prompt body. The six pack-delta sketches here are 1–3 lines
  each (roughly on the 100–800-token pack budget); each expands into its own `L3_packs/*` file.
- **Historical-mode coverage:** casting sticks (Senet), Ur binary tetrahedral, Patolli beans,
  Pachisi cowries — completed by modern `1d6` for Ludo & Snakes—Ladders. All 5 historical modes
  from L0 are exercised across this family.
- **Senet (26–30) and Ur rosettes:** both `reconstructed`; the "ritual squares on which capture is
  disallowed" behavior is the conservative reading shared by both schools and is flagged as such.
- **Ludo "commercial reskin"** and **Snakes & Ladders "capture stripped"** are editorial framing
  within the corpus taxonomy; the underlying mechanics are attested.
- **1569 Patolli ban:** history documented in the cultural pack; does not alter rules.
- Cross-refs: parent `L0_universal_contract.DRAFT.md`; downstream `L2_games/*`, `L3_packs/*` per
  game; honor `00_PRIMER.md` §8 open questions where applicable.
