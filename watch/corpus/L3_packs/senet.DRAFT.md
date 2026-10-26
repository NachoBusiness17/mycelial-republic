# L3 — Senet Cultural Pack (DRAFT) — `L3_packs/senet.DRAFT.md`

> **Status:** DRAFT. **Engine:** race_dice. **Class:** L3 cultural pack — a delta over the
> race/dice engine, not a full rules rewrite. **Consumption order:** L0 contract → L1 race/dice
> engine → this pack (deltas) → L2 statics → this pack's cultural/historical notes.
> **Research status:** `reconstructed` throughout — no period rulebook survives; rules are
> reconstructed from boards, the religious text (Ch.17 of the Book of the Dead), tomb vignettes,
> and modern analysts. Contested points ship as named competing schools and are never silently
> upgraded.
>
> ---

## CULTURAL PACK: Senet

**Variant family:** race/dice (linear track, seeded-external casting sticks).
**Path in family:** the oldest named variant in the race/dice family (lowest strata of the family
sketch order — predates Ur, Patolli, Pachisi).

## RULE DELTA (only what differs from the race/dice engine)

- **TRACK:** `linear`, **30 squares**, indices `0..29`. Square 0 = start ("House of Rebirth"),
  square 29 = the final square before bear-off.
- **MOVEMENT:** destination = `min(current + roll, 29)` with **`roll-exact`** entry, **`land-exact`**
  overshoot clamp is NOT used — per the attuned schools, an over-roll passes through/beyond the
  final ritual squares and must resolve against them (see SQEFFECT). **Delta vs engine:** the
  engine default linear `land-exact` is overridden here.
- **MOVEMENT SOURCE:** **casting sticks**, historical mode (L0 RNG #3). Standard build: **2 sticks**,
  one marked side each; result `0,1,2` with the double (both-marked) counting highest. Move amount
  comes ONLY from the seeded RNG — LLM never improvises a throw.
- **CAPTURE: off.** **Delta vs engine:** the race/dice default capture flag is explicitly OFF. No
  piece is ever removed from the board by landing on it.
- **BLOCKING:** no piece interaction by capture; pieces co-locate on a square unless a `safe` flag
  applies. Two pieces of the same player on a square may block *opponents* from passing *only as a
  house option* (see House options), never by engine default.
- **ENTRY:** **`roll-exact`** entry — a piece leaves the off-board stock only on a qualifying roll
  (per school; commonly any roll, with the high stick-throw counting as the entry throw). Delta
  vs engine: entry is pack-defined, not engine.
- **WIN / BEAR-OFF:** all pieces (default 5) must traverse squares `0..29` and bear off. The bear-off
  crosses the ritual exit at squares 26–30 (see School of Piccione below). **WIN** when all pieces
  have left the track.
- **SQEFFECT[30-square table]** — grouped, resolved on landing in fixed order per engine:
  - squares `0..` start-region: `none` (start area).
  - **squares 26–30 (ritual/afterlife region):** `{ effect: ritual-safe }` at the passage squares, plus
    a **`jump` to the afterlife-exit** at the final passage square(s). These squares are `safe`
    (capture is already off; the `safe` flag means pieces there are part of the ritual passage,
    not capturable — retained for family consistency and for the House option that turns capture
    on elsewhere).
  - **House of water / "House of Beauty" hazard square** (traditionally near squares 26–27 under
    Piccione; per the Kendall reading the hazard is among squares 26–30): `{ effect: retreat }` back
    to the "House of Netting"/rebirth region (commonly square 15), a **miss-a-turn**, or a **reroll**
    — chosen per school and per house, resolved once per landing.
  - All other squares: `none`.
  - **School-dependent detail** — Deltas between the two named schools are expressed ONLY here and
    in the Historical Module, never silently merged (see Research Status).

## HISTORICAL MODULE

**Era / culture:** Predynastic through New Kingdom Egypt (earliest artifacts ~3100 BCE; peak
popularity Middle–New Kingdom). Grave goods, tomb wall-paintings, and the religious text
(*Book of the Dead*, Ch. 17 the "House of Netting" passage) place it as both a leisure game and a
vehicle for the afterlife/judgement symbolism — the passage across squares 26–30 allegorizes the
Netherworld journey.

**Archaeological corpus:** 30-square boards in three rows of 10 (occasionally the earlier 3×10
grid with differing hazard markings), e.g. the board from the tomb of Queen Nefertari; vignettes of
Senet in tombs of the Old and New Kingdom; the 20-square Ur boards are a *different* game (see
engine family) and are not conflated with Senet here.

**Sources / uncertainty:** no contemporary rulebook survives. All reconstructions are heuristic.
Contested points ship as named schools:

- **School of Kendall (Timothy Kendall, 1978):** reads the 30-square path as a pure race with
  capture ("House of Water"/hazard) squares at the start- and water-regions; pieces are knocked off
  by opponents, emphasizing the social/competitive gameplay. Bear-off is a literal race to exit.
- **School of Piccione (Peter Piccione, 1990):** reads the board through the religious text as an
  allegory of the Netherworld journey; the last five-plus squares (the "Netherworld" group, 26–30)
  are a **luck-dominated** judgement passage where capture is ineffective and outcomes are decided
  by the throws, not by duel. The two schools agree on the 30-square grid, casting-stick movement,
  and that capture is disallowed/irrelevant on the ritual squares — the conservative shared
  reading — but differ on where the hazard sits and on the weight given to removal-vs-passage.

**`research_status`:** `reconstructed` for all reconstructed mechanics (movement source, capture,
ritual squares, win handle). No element is `attested` from a period rules text; the existence of
the game, board geometry, and stick-throw culture are attested archaeologically. This file never
upgrades `reconstructed` to `attested`.

## MATERIALS MODULE

**Original pieces:** (1) the board — 30 squares (3×10), with hazard/ritual squares often marked
with hieroglyphs or painted glyphs (water, the "House of Beauty," the Netherworld); (2) **casting
sticks** — flat sticks/rods, one side marked (later/regional skins: 4 sticks counted per Patolli,
or the knucklebones/astragali); a modern equivalent is the 2-stick marked/non-marked throw; (3)
**pawns** — 5 (occasionally 7) tall conical pawns, matched by color; (4) a cup/board-rest to cast
the sticks (optional).

**Modern-skin equivalents:**
- board → any 30-cell `linear` track marked on a table/paper, cells 26–30 highlighted as the
  ritual region;
- casting sticks → 2 marked coins/flat tokens tossed together (each marks 1 when marked-face up),
  or a `2d2-?` mapped through the L0 casting-sticks table — always seeded-external, never rolled by
  the LLM;
- pawns → 5 identical counters per player, distinct by color.

## REGIONAL VARIANTS (named deltas)

- **Standard (2-stick) Senet** — the conservative shared build above. Most portable.
- **4-stick Senet** — casting-sticks with 4 sticks (count `0..4`, double highest); increases dice
  spread, same track. Noted regional/collection variance.
- **"House of Water on 26–27" (Kendall-leaning)** — places the retreat hazard at the water squares
  near the exit, emphasizing the removal/duel reading (see School of Kendall).
- **"Netherworld passage" (Piccione-leaning)** — squares 26–30 as ritual/luck-only region with the
  hazard inside it, capture meaningless (see School of Piccione).
- **7-pawn Senet** — some boards attest 7 pawns per player; a house variant with more pieces and
  denser occupancy, same track/win.

## ETHICS / ATTRIBUTION

**Origin culture:** Ancient Egypt (Predynastic–New Kingdom). Senet is one of the oldest known
board-game families and the base strata of the race/dice engine's historical lineage.
**Sources honored:** Kendall (1978), Piccione (1990), and the archaeological corpus; the *Book of
the Dead* Ch.17 reading is attributed and flagged `reconstructed`, not presented as rule fact.
**Sensitivity:** the game's afterlife/judgement symbolism belongs to a living heritage tradition;
this pack treats it with attribution and flagging and does not flatten it into mere mechanics.
The ritual squares are `safe`/ritual by design per the conservative shared reading, not as an
editorial choice to strip competition.
**Attribution note:** any disputed claim is shipped as a named competing school with
`research_status`, per the corpus rule — never a single invented consensus.

## PLAYABLE BUILD PROMPT (BUILD PROMPT)

> Build the Ancient Egyptian game **Senet** as a deterministic race game: a **linear track of 30
> squares** (indices 0–29), 5 identical pawns per player entering **roll-exact** from an off-board
> stock and bearing off after crossing square 29. Movement comes ONLY from the seeded external RNG
> using the **L0 casting-sticks** mode (2 marked sticks: 0 / 1 / 2, the doubled throw counting
> highest) — you never invent a roll. Apply the race/dice engine with these deltas: **capture is
> OFF** (no pieces are ever removed by landing), no default blocking, and **squares 26–30 are the
> ritual/afterlife region** — mark them `safe`, route the passage as a `jump` to the afterlife exit,
> and put the retreat hazard (back to square 15) in this region per the Piccione passage reading;
> flag in your output that these ritual squares are `reconstructed` and that **historians disagree
> (Kendall 1978 vs Piccione 1990)** on where the water/hazard sits and on whether play is a removal
> duel or a luck-dominated Netherworld passage — this build uses the conservative shared reading
> (ritual squares 26–30, no capture). WIN when all pieces bear off. For every reply: restate the
> canonical state on the `^` line (game id `senet`, turn-index, active-role, board, order,
> seed-phrase), cite the governing clause (L0 function number + casting-sticks RNG mode), emit the
> seeded roll, apply the SQEFFECT for the landing square in engine order, then the new canonical
> state, and only then narrate.

---

*Corpus cross-refs: parent `L1_engines/race_dice.DRAFT.md`; contract `L0_universal_contract.DRAFT.md`;
family siblings `ur.DRAFT.md`, `patolli.DRAFT.md`, `pachisi.DRAFT.md`, `ludo.DRAFT.md`,
`snakes_ladders.DRAFT.md`.*
