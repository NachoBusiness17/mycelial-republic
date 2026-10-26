# L2 — Kalah (American commercial mancala) Static Pack (DRAFT)

> **Status:** DRAFT. **Engine:** `L1_engines/sowing_capture.DRAFT.md` — docks on the SOWING/
> CAPTURE family kernel as its **Kalah slot** (the modern **commercial** branch). **Class:** L2
> static prefix — a **thin delta** over the engine: only exposed flags and constants change (board
> size `6+1`, seed count `s=3–4`, `FEEDING: off`, capture-own-store rule, instant-win majority);
> the engine's structural clauses (ring sow order, end-of-sow capture, chain direction,
> store-majority machinery) are inherited verbatim. Byte-stable static-first: everything at/after
> `[PROMPT-BODY-START]` is identical every request; only the canonical board string and the chosen
> pit land in the dynamic tail. **Provenance:** primer §7 build-order (mancala family),
> `L1_engines/sowing_capture.DRAFT.md` §FAMILY PACK SLOTS §Kalah. **Research status:** rules
> `attested` (commercial publication/patent lineage); origin-culture note below: the **Akan (West
> African) mancala ancestry** is honored even as Kalah is a modern commercial abstraction — never
> flattened into "traditional."

---

## GAME ID / FAMILY SLOT

- `sowing-capture` family engine — this is the **Kalah (6+1 store layout, commercial) slot**, a
  pack-level delta docked on the shared sow/capture kernel.
- `game id` = `KALAH-CHAMPION-01` (zero-indexed enum per L0 FUNCTION 1; fixed for dedupe and
  RNG-table keying).
- **Boundary stance (inherited from engine):** Kalah is NOT a race/dice game. No RNG, no track-to-a-
  finish; move length is the chosen pit's stored count; L0's "never improvise a roll" is satisfied
  **negatively** — there is no roll to invent. This pack keeps that core honest.

## BOARD DELTA (the 6+1 store layout)

The engine canonical ring of `N` pits is used with **`N = 12` (6 per player)**, plus **one store**
per player **of the board** — the classic "6+1" Kalah layout:

- **Pits:** `0..5` = Player A, `6..11` = Player B; ring-opposite = `(i+6) mod 12` (engine standard).
- **Stores:** each player's **store sits at their own side's end, off the ring**, i.e. adjacent to
  their low-indexed pit. Kalah is the mancala whose store is **captured into on your own sow AND
  receives the "sweep" on a pit passing over it** (see TRANSITION delta) — the store is still
  outside the ring (never a legal sow pit), but a sow's extra stones that wrap past the store
  **land in it** on the owner's own pass. This is the one store-contact the engine's "canonical
  store off-ring" clause must be extended for — the pack states it as the board's defining feature:
  **a player deposits into their own store when the sow passes over it**, giving the "6+1" its
  name and its distinct play.

## SEED COUNT / INIT DELTA

- **`s = 3–4` seeds per pit** — a pack constant. Canonical **`s = 4`** (48 stones, standard
  tournament Kalah); a **`s = 3`** (36-stone) house variant is accepted but 4 is the reference
  constant encoded here. Total stones = `s × 12` on the board, **stores empty at deal**.
- INIT is deterministic: the engine's INIT with this `s`; starting `active-role` and `turn-index =
  0`; layout symmetric so `seed-phrase` does not perturb it.

## RULE DELTA (only what differs from the engine)

- **MOVEMENT SOURCE:** none — no RNG; lift a chosen own-side pit holding ≥1 seed and sow one per
  pit counterclockwise. **Inherited unchanged.**
- **STORE DEPOSIT (the pack's structural-ish rule):** during the sow, when the counter passes the
  player's **own store**, one seed is deposited into it, then the sow continues onto the opponent's
  side. The **opponent's store is skipped** (never landed in). The chosen empty pit is never
  reseeded. This is the full "6+1" store interaction; the engine's "sow never lands in a store"
  clause is **overridden to "lands in the sower's own store, never the opponent's"** — a pack flag
  (`STORE_DEPOSIT: own-pass`).
- **FEEDING / SUPPLY:** **`FEEDING: off`** — Kalah has **no forced-feeding constraint** (unlike
  Akan Oware). A pit is legal iff it is own-side and holds ≥1 seed; there is no rule against
  leaving the opponent with zero legal moves (the opponent then simply skips per TERMINAL and all
  stones sweep). **Pack sets `FEEDING: off`.**
- **CAPTURE (to own store):** engine capture rule **retained** (last-sown-seed lands in an empty
  pit on the sower's own side) with the opponent's opposite pit containing **≥1 seed** (`2/3-or-
  nonzero` per the engine Kalah slot: **any nonzero count**); the sower captures the **entire
  opposite count plus the sown seed into their own store**. Backward chaining is retained
  (engine §TRANSITION §4) but in the common single-store recension chaining is often off; this pack
  sets **`CHAIN: off`** (single-capture — only the paired opposite is taken, matching the majority
  of published Kalah) with a `CHAIN: on` variant noted.
- **LAPE / GRAND-SLAM:** **`LAPE: off`** by default (ordinary role swap after a move/capture).
  Kalah's "go again" variant — landing the last seed in one's **own store** grants an **immediate
  extra turn** (engine §GRAND-SLAM/LAPE) — is the classic and here defaults **`LAPE: store-landing
  on`**: a sow whose final seed falls in the player's own store awards a **bonus turn**. Task
  frame: mark this as the Kalah bonus-turn variant, `on` per standard recension.
- **WIN / TERMINAL — INSTANT store-majority:** engine store-majority machinery **retained** but
  Kalah's signature is **instant win on store majority during play**: as soon as a player's store
  exceeds **half of the total stones** (for `s=4`: **`>24` i.e. 25 of 48**; for `s=3`: `>18` i.e.
  19 of 36), the game **ends immediately on that landing** — no waiting for board empty. Additionally
  (standard recension): when **one side's pits are all empty**, the opponent **sweeps all remaining
  stones on their own side into their store**, then the higher store wins (engine §TERMINAL,
  board-sweep), tie per pack (a `24–24` split is a `draw`).

## SQEFFECT (mapped to engine; delta triggers)

- Each pit doubles as a possible final landing; engine §SQEFFECT chain resolves. **Pack delta:**
  capture count is **any nonzero opposite** (whole stock), `CHAIN: off` default; the final landing
  in the **own store** awards the `LAPE: store-landing` bonus turn. The **opponent's store is never
  a target** (skipped on sow).
- Stores off-ring receive captures and own-pass deposits only; never a sow target (with the
  own-store deposit being the pack's store-contact exception stated above).

## CACHE BOUNDARY / OUTPUT-CONTRACT

- **Static (cached):** game id, `N=12` + 6+1 stores, `s=4`, `FEEDING: off`, `CHAIN: off`,
  `LAPE: store-landing on`, instant-win `25/48`, `^`-canonical restatement rule, rule-clause
  citations. Identical every request.
- **Dynamic (tail, never cached):** canonical board string (`12 pit counts + 2 stores`), the chosen
  pit predicate, `seed-phrase -` (deterministic), reserved. Kept last, small.
- Before any move: restate canonical state on `^` (game id `kalah`, turn-index, active-role, 12
  pit-counts + 2 stores, order, `seed-phrase -`, reserved), cite the governing L0 function + engine
  clause, apply the sow cascade (including the own-store deposit), resolve capture, reprint, narrate.
  **No dice, no cast, no improvised roll — ever.**

## RESEARCH / ORIGIN NOTE (commercial invention + honored Akan ancestry)

- **Invention (`attested` commercial):** Kalah was invented by **William Champion Jr.** in the
  **United States in the 1940s**, marketed/patented under his name (the patent's specific claims and
  the exact commercialization dates are the finite historical record; the invention is a deliberate
  **commercial abstraction of the African mancala family**, not a traditional regional game). It was
  later resold widely under several brand names and became the standard American "mancala." Ruleset
  is `attested` from commercial publication/patent lineage — the encoded rules are the modern
  tournament-standard Kalah.
- **Origin-culture attribution (honored, not erased):** Kalah descends mechanically from the
  **Akan (West African, esp. Ghana/Ashanti) mancala heritage** (the `oware.DRAFT.md` family).
  Even though Kalah is a 20th-c. commercial invention, this pack **honors and names that Akan
  ancestry** explicitly, presenting Kalah as the modern commercial branch *of* the family rather
  than a root tradition. The engine carries no commercial/patent claim; this history note is the
  pack's own `attested` record.
- **Sensitivity:** Kalah is a modern game and carries no contested-priority claim itself; the
  one-careful point is not to let the commercial label displace the acknowledged Akan ancestry.
  This pack states the invention honestly AND foregrounds the West-African root. No invented
  archaeology; the patent/commercial record is the `attested` source, the Akan debt is the honored
  attribution.
- **Research status legend:** rules `attested` (commercial publication); ancestry `honored` /
  genealogy documented via the family; nothing marked `reconstructed` beyond the standard-variant
  flags above (instant-win exact threshold is the published constant).

## BUILD PROMPT

> Build **Kalah (the modern American commercial mancala, William Champion Jr., 1940s invention)**
> on the SOWING/CAPTURE engine as a deterministic sowing game — NO RNG, NO dice, NO track-to-a-
> finish; state this first. Layout is the **6+1**: 12 pits (`0..5` A, `6..11` B, opposite
> `(i+6)%12`), **`s = 4` seeds per pit (48 total)**, and **one store per player off the ring**. On
> your turn choose an own-side pit holding ≥1 seed, **lift and sow one per pit counterclockwise**;
> when the sow passes your **own store, deposit one seed into it** and continue (the **opponent's
> store is skipped**). If the **last seed lands in a pit empty-before-sow on your side**, capture
> the **entire opposite pit's count plus the sown seed into your own store** (single capture —
> `CHAIN: off`); there is **no feeding constraint** (`FEEDING: off`). If the last seed lands in
> your **own store, take an immediate bonus turn** (`LAPE: store-landing on`, the Kalah go-again
> variant). WIN **instantly when your store holds more than half the stones — 25 of 48** — or, when
> one side is empty, sweep the opponent's remaining on-side stones into their store and compare
> (higher wins; a `24–24` split is a draw). For every reply: `^`-canonical restate (game id `kalah`,
> turn-index, active-role, 12 pit-counts + 2 stores, order, `seed-phrase -`, reserved), cite the L0
> function + engine clause, the sow cascade (own-store deposit), the capture, the new canonical, then
> narrate. Flag in your output that the ruleset is **`attested` (commercial publication)** and that
> Kalah is a **1940s Champion commercial invention whose Akan (West African) mancala ancestry is
> honored** — present it as the modern commercial branch of the family, never as a root tradition.
> No dice, no cast, no improvised roll — ever.

---

*Corpus cross-refs: engine `L1_engines/sowing_capture.DRAFT.md` (§Kalah slot: "attested as a
commercial game, 1940s Champion invention;" engine carries no commercial claim); contract
`L0_universal_contract.DRAFT.md`; sibling L2 `bao.DRAFT.md`; cultural pack `L3_packs/oware.DRAFT.md`
(Akan heritage named and honored); family open items per `00_PRIMER.md` §8; honor SPORE_SEED
boundary test (sowing vs race engine).*
