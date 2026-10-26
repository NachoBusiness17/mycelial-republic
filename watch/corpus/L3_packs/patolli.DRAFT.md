# L3 — CULTURAL PACK: Patolli (DRAFT) — `L3_packs/patolli.DRAFT.md`

> **Status:** DRAFT. **Class:** L3 pack — a delta over the race/dice family engine.
> **Research status:** `reconstructed` (Durán; Murray; contested schools flagged below —
> never silently upgraded). **Consumption order:** L0 contract → L1 race/dice engine →
> this pack (deltas) → L2 statics. **Provenance:** primer §7 build-order #1; SPORE seed
> 2026-09-01 fan-out. Game id (L2 statics): `patolli` — state draws resolve under
> `game-id="patolli"` in every L0 RNG mode.
>
> This file is byte-stable static prefix + per-variant content appended atomically. The
> L0 contract and L1 engine mechanics apply verbatim and are NOT restated here; this pack
> only declares the deltas. Where a pack clause conflicts with the engine, this pack wins
> for that clause except structural engine clauses (track shape, capture order,
> bear-off machinery), which the pack may not override.

---

## CULTURAL PACK: PATOLLI

**Game:** Patolli (Nahuatl *patolli*, from *patolli* "runner bean"). The classic Mesoamerican
race-and-dice game of the Aztec/Mexica world, with deep Teotihuacan roots and attested spread
through central Mexico into the post-contact colonial era.

**Culture/era:** Nahua (Mexica/Aztec) — Late Postclassic central Mexico (c. 1300–1521 CE),
with archaeological substrate extending to **Teotihuacan** (c. 200–650 CE) and earlier
Gulf-coast / western-Mexico pebble-board traditions. Played on woven mats and (by the colonial
period) on cut-stone or adobe boards; gambling was a core social function.

**ENGINE:** `race_dice`

**RULE DELTA** (only what differs from the L1 engine):

- **TRACK SHAPE — cross, mapped to a ring with a junction:**
  The board is a large **X / cross-shaped track** — historically rendered (Durán) as a
  cross/maltese form of **52 squares in total**, four arms radiating from a central junction.
  Encode as a **ring** of 52 indices `0..51` with a **cross-track turn**: the four arms meet at a
  per-scheme central junction, and at the junction a piece may turn down the arm of its owner's
  route. The default scheme (conservative reading) treats the cross as one continuous
  clockwise circuit of 52 squares through the junction — a pure ring with no branch choice.
  The branching reading is a **named regional variant** (see REGIONAL VARIANTS) and ships
  behind its own `research_status: speculative` flag.
- **ENTRY:** all players start their pieces **off-board / in home stock** and enter onto the board
  on a qualifying roll (`1` or `5` in the default marked-bean scheme). Entry is part of this pack,
  not the L1 engine. (Note: the historical number and start of pieces is contested — see
  HISTORICAL MODULE.)
- **MOVEMENT:** move amount comes ONLY from the marked-bean RNG draw (L0 historical mode #5).
  Direction is a single fixed clockwise circuit around the ring (default scheme).
- **CAPTURE: on.** Landing on a square occupied by an opponent piece removes that opponent piece
  and returns it to its owner's **start/stock** (re-entry per ENTRY rule above). Capture is
  disabled on `safe` squares (see SQEFFECT).
- **SAFE (ritual) squares:** the central **junction** is a `safe` square — pieces there may not
  be captured. The four **arm bases/homes** per player are marked safe. Additional per-scheme
  safe squares may be named in a variant.
- **SQEFFECT table:** `safe` at the junction and arm-bases; `miss-a-turn` on a configured set of
  penalty squares (counts to the engine's per-square table); `reroll` optional behind a
  variant flag; all other squares `none`. Effects resolve in the L1 fixed order after landing,
  before capture resolution, exactly once.
- **WIN:** **track completion** — a piece that completes the full circuit (ring finish) and lands
  exactly on the final square (`roll-exact`) bears off; **WIN when one player has brought ALL their
  pieces around and borne off** (the default "all pieces" engine default). Gambling stakes do not
  alter the mechanical win condition (see ETHICS/ATTRIBUTION).

**HISTORICAL MODULE:**

- **Era/culture:** Mexica (Aztec) Late Postclassic central Mexico; ancestor/parallel traditions
  visible at **Teotihuacan** and in earlier western-Mexico and Gulf-coast patolli-like pebble
  boards. The 52-square cross-form is the canonical Mexica board (Durán; Sahagún mentions; see
  uncertain origin below).
- **Archaeology/sources:** The authoritative period account is **Fray Diego Durán's** *Historia de
  las Indias de Nueva España* (c. 1581), who describes the board, the marked-bean dice, and the
  heavy gambling. **Bernardino de Sahagún's** Florentine Codex (c. 1577) corroborates the game's
  place in Mexica life and its association with ritual/gambling. **Stewart Culin** and **H. J. R.
  Murray** collate the historical ethnography in the modern literature. Archaeological
  substrate: pre-Columbian pebble/bean boards from **Teotihuacan** and western Mexico are put
  forward by some scholars as proto-Patolli; direct, unambiguous Mexica-period Patolli boards are
  comparatively few and mostly colonial-period stone examples.
- **Uncertainties / contested history (named schools — ships intact, not invented away):**
  1. **Origin-depth school A ("Teotihuacan proto-Patolli"):** the cross pebble-board motif found
     at Teotihuacan and in West Mexico is a direct ancestor; Patolli is therefore old and broadly
     Mesoamerican. **research_status: speculative.**
  2. **Origin-depth school B ("colonial/attested-horizon only"):** the *reconstructed* rules rest
     securely only on the post-contact colonial accounts (Durán/Sahagún); any deeper antiquity is
     plausible but not securely attested for the specific 52-square rule form.
     **research_status: speculative** for the proto-forms, `reconstructed` for the colonial-rule
     reconstruction itself.
  3. **Board geometry school C ("branching arms"):** the four arms carry directional/branch
     choices beyond a simple ring. **research_status: speculative** (this pack's default uses the
     conservative continuous-ring scheme).
- **research_status (aggregate):** `reconstructed` — rules built from Durán + modern collation
  (Murray; Culin); archaeology of the specific rule form is `speculative`; the 1569 ban is
  **attested** documentary history.
- **THE 1569 SPANISH INQUISITION BAN (mandatory historical item):** Patolli is the Mesoamerican
  game whose documented suppression example is the **1569 decree of the Spanish Inquisition** in
  New Spain, which proscribed *patolli* (along with associated gambling and certain indigenous
  ritual practices) as idolatrous/associated with gambling and Indigenous religious practice.
  In this corpus this ban is recorded as a **cultural-pack history note, NOT a rules change**:
  it did not alter the mechanics on the page, and the game's rules did not "become" different
  because of the ban. It is attested colonial suppression of indigenous play. Per the L0
  contested-history rule, the pack states this with its `attested` flag and the honesty note that
  the ban is a legal/religious document, not a rulebook.

**MATERIALS MODULE** (original → modern-skin equivalents):

- **Original pieces:**
  - **Board:** a woven fiber mat (petate) painted/worked with the cross of 52 squares, or a
    carved stone / adobe / wooden board in the same layout. Modern skin: an illustrated board /
    printed cloth with the 52-square cross ring.
  - **Dice (the load-bearing RNG device):** **5 marked beans** (*patolli* derives from the bean
    itself) — each bean has one marked side; the seeded draw counts the marked beans, per L0
    historical mode #5. Modern skin: 5 two-tone tokens / 5 flippable disks with one marked face.
  - **Pieces:** small stone/corn-kernel markers per player; modern skin: colored pawns/halved
    counters.
- **L0 RNG binding:** the roll is the **marked-beans** mode (`mode #5`) resolved from the seeded
  table under `game-id="patolli"` with a **seeded finite pool** — beans are not reused until the
  pool refills (exhaustive reshuffle), so the stream is a fair finite sample. The LLM reports the
  draw; it never chooses or improvises it.

**REGIONAL VARIANTS** (named deltas, each with its own flag):

- **Mexica/Aztec (default), `reconstructed`:** 52-square continuous-ring cross, marked-bean dice,
  capture-on, junction + arm-bases safe. Basis: Durán et al.
- **Branching-arms reading, `speculative`:** four arms carry a branch choice at the junction
  (down the owner's arm); encoded as a per-scheme ring-route patch. Requires its own
  `research_status: speculative` flag on every output per L0 rule 5.
- **Peasant / low-stakes variant, `speculative`:** same mechanics with reduced/no stakes (see
  ETHICS — stakes reduced to counters when not gambling).
- **Modern-skin / teaching variant, `speculative`:** replaces beans with two-tone disks and stones
  with pawns (materials-only delta; no mechanical change).

**ETHICS/ATTRIBUTION:**

- **Origin culture:** Nahua (Mexica/Aztec), central Mesoamerica; Mesoamerican pebble-board
  heritage at Teotihuacan and West Mexico. The cultural attribution is the Mexica/Nahua people and
  their broader Mesoamerican inheritance.
- **Sources:** Durán, *Historia de las Indias de Nueva España*; Sahagún, *Florentine Codex*;
  collated in Culin and Murray. The 1569 Inquisition ban documents colonial suppression.
- **Sensitivity / attribution notes:**
  1. **Gambling is load-bearing:** Patolli was played for high stakes — Durán records that even
     commoners wagered as much as they owned, sometimes their person/shirts. A respectful modern
     build should default to **playing for counters/tokens only** unless the operator explicitly
     opts into a stakes fiction; this is an ethical choice in the pack, not a rule.
  2. **Colonial suppression is real:** the 1569 ban (and later prohibitions) targeted the game in
     part for its Indigenous religious/gambling associations. Do not present the suppression as a
     matter of pure "house rules"; it is a recorded act of colonial prohibition and belongs in the
     historical record, which this pack carries verbatim rather than laundering into mechanics.
  3. **Reconstructed not "authentic gospel":** the rule form is a scholarly reconstruction
     (Durán/Murray). Present it as *a* faithful build, never as a monolithic "the one true
     ancient ruleset." Contested points ship as named schools with their flags.
  4. No cultural stereotype; the game's gambling history is honored, not exoticized.

**BUILD PROMPT** (one paragraph — the one-shot instruction):

> BUILD PATOLLI as a race/dice game. Apply the L0 Universal Game Contract (six-function state
> encoding, canonical `^` restatement first, cite the governing clause, never invent objects,
> contested history ships with its flag) and the L1 race/dice engine mechanics, with ONLY these
> pack deltas: a cross/ring track of 52 square-indices `0..51` in one fixed clockwise circuit
> through a central junction; 5 marked-bean dice resolved EXCLUSIVELY via the L0 seeded
> marked-beans mode (`game-id="patolli"`, seeded finite pool, draw reported never chosen);
> pieces enter from home stock on a roll of 1 or 5, move the drawn bean-count around the ring,
> CAPTURE on (return captured pieces to their owner's stock for re-entry), safe squares at the
> junction and each arm-base, and WIN by bringing ALL your pieces around the full circuit and
> bearing off on an exact/higher roll. Restate the canonical state before every move, report
> each bean draw from the seeded table, and flag each historically-contested rule
> (board-origin and geometry schools) with its `research_status: reconstructed|speculative`
> plus a one-line honesty note; record the 1569 Spanish Inquisition ban as an attested
> historical suppression note in your output, not as a rules change. Default stakes to counters,
> not real wagers.
