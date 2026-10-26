# L2 — Bao (East African mancala) Static Pack (DRAFT)

> **Status:** DRAFT. **Engine:** `L1_engines/sowing_capture.DRAFT.md` — docks on the SOWING/
> CAPTURE family kernel as its Bao slot. **Class:** L2 static prefix — a **thin delta** over the
> engine: only exposed flags and constants change (board geometry, seed count, opening/lape rules);
> the engine's structural clauses (ring sow order, end-of-sow capture, chain direction,
> store-majority machinery) are inherited verbatim and *not* overridden. Byte-stable static-first:
> everything at and after `[PROMPT-BODY-START]` is identical every request; only the canonical
> board string and the player's chosen pit land in the dynamic tail. **Provenance:** primer §7
> build-order (mancala family), L1 engine FAMILY PACK SLOTS §Bao. **Research status:**
> `reconstructed` — Bao la Kiswahili standard tournament rules (Zanzibar recension) are used as
> the encoded ruleset; the finer moves (the namuamba opening obligate-move rule and the
> grand-slam/lape trigger) are `reconstructed`/speculative and flagged, never silently upgraded.

---

## GAME ID / FAMILY SLOT

- `sowing-capture` family engine — this is the **Bao (4-row, high-strategy) slot**, a pack-level
  delta docked on the shared sow/capture kernel.
- `game id` = `BAO-ZANZIBAR-01` (zero-indexed enum per L0 FUNCTION 1; fixed for dedupe and
  RNG-table keying).
- **Boundary stance (inherited from engine §BOUNDARY):** Bao is NOT a race/dice game. No RNG, no
  track-to-a-finish; move length is the chosen pit's stored count. The L0 "never improvise a roll"
  mandate is satisfied **negatively** — there is no roll to invent.

## BOARD DELTA (the 4-row extension — the pack's only geometry change)

The engine canonical ring of `N` pits is **flattened into a 2×4-row board** without changing the
ring-sow mechanics. Bao la Kiswahili plays on a **4-row board: 2 rows (8 pits each = 16 pits) per
player**, the two inner rows forming the playing arena and the two outer rows forming the **nyumba**
(home) and store-linked sides.

- **Row roles (Zanzibar recension):**
  - The **inner rows** (the two rows nearest the center, one belonging to each player) are the
    **namumba stage** — the live playing rows where sowing and capture happen for most of the game.
  - The **outer rows** (each player's far row) are the **keta rows** (also named the player's
    "back/home" row), which hold the opening stones and anchor the **nyumba** (home pit) capture-
    doubling house.
- Ring encoding for the engine: index the board counterclockwise as a single ring of **`N = 32`**
  (16 per player); a pit's ring-opposite = `(i + 16) mod 32`. Pack maps ring indices to the 4-row
  grid; the engine's per-pit count array is the single authority. **Capture counts** follow the
  engine's chain rule: the final seed landing in an own-side pit that was empty-before-sow captures
  the opposite pit's count **plus** the sown seed; the chain continues backward while the trigger
  holds.
- **The nyumba (home) exception:** in standard tournament Bao the **nyumba** (leftmost pit of the
  front/inner row) has special home status: once captured into, the holder keeps capture rights to
  it and may not be forced out except per the grand-slam rule. This is a pack flag —
  `NYUMBA: on` default — and is the one clause the engine's generic capture does not supply
  (the engine has no per-pit "home" concept); it is encoded at pack level as a home-pit capture
  priority and flagged `reconstructed`.

## OPENING DELTA — the namuamba stage (seed-count 22+s)

The engine's fixed INIT (`s` per pit) is replaced by Bao's **namuamba (opening) stage**:

- **Seed count:** **`s = 22+`** — the opening is set by the deal, not a uniform per-pit count.
  Canonical tournament deal: **32 seeds** are dealt around the player's seed-holes (the two rows),
  distributed per the standard opening layout (2 seeds in most of the 16 pits, with the fixed
  five named pits — the two *kichwa* (heads) and the *nyumba* row anchors — holding the defined
  higher opening counts, so the total is 32; the open/`+` clause notes the deal is the tournament
  constant). Total **64 seeds on the board** (32 per side).
- **Obligate-move rule (`reconstructed`):** during the opening the very first draw is **obligated**:
  a player must lift and sow the pit matching the opponent's opening pit choice (the "waiting" rule
  of the namuamba), before the game opens into free sowing. This is the single most contested fine
  point and is flagged `reconstructed` (standard tournament Bao enforces a waiting-pit obligate
  move; club-house variants relax it).
- **End of opening:** when all namuamba stones are sown into the inner rows the game leaves the
  opening and enters ordinary sowing with free pit choice on the namumba stage. This transition is
  engine TERMINAL-free (it is not a win condition; it only changes which pits are legal targets).

## RULE DELTA (only what differs from the engine — everything else inherited)

- **MOVEMENT SOURCE:** none — no RNG; a turn lifts a chosen own-side pit's full count and sows one
  per successive pit ringwise (engine §TRANSITION). **Inherited unchanged.**
- **FEEDING / SUPPLY:** engine default `on` is **disabled at the arena opening but the waiting
  obligate-move overrides free choice** during namuamba. After the opening, standard Bao has **no
  forcing-feeding `LEGAL?` constraint** (unlike Akan Oware) — a pit choice is legal if it is
  own-side and holds ≥1 seed, subject to the home-pit rules. **Pack sets `FEEDING: off`** after
  the opening, `FEEDING: waiting-obligate on` during it.
- **LAPE / GRAND-SLAM (`reconstructed`):** `LAPE: on` for the **grand-slam** trigger — if a sow
  captures so as to **empty the opponent's entire side**, the sower takes an immediate **bonus
  turn** (engine §GRAND-SLAM/LAPE §5 role-swap override) and additionally gains a **lape** (the
  right to resume a capture run from the home pit at their next turn). The exact lape grant is
  variant and flagged `reconstructed`. **Home-honor:** the `nyumba` home is refilled/loss rules are
  part of this same flag block.
- **WIN / TERMINAL:** engine store-majority machinery **inherited** but with the official
  **25-capture model**: record the number of captures (the first player to capture **a majority of
  the 64 stones — 33 of 64**) wins; because captures land in the store, this is engine
  `SCORE(storeA,storeB)` with the threshold **`33/64`** (vs Oware's 25/48). Store-majority
  supersedes; board-empty sweeps remaining on-side stones to the owning stores before comparison,
  engine §TERMINAL. **No-legal-moves** ends and sweeps likewise.

## SQEFFECT (mapped to the engine; only the delta triggers differ)

- Each pit doubles as a possible final landing; the engine's §SQEFFECT chain resolves captures.
  **Pack delta:** the capture count is **any nonzero own-opposite** (Bao captures the opposite
  pit's whole stock, not only `2`/`3` as Oware) — engine's own-side-empty-before-sow precondition
  holds, then transfer the **entire** opposite count plus the sown seed. The `nyumba` home pit
  confers a **home capture** (opposite stock taken in full on any legal landing; `NYUMBA: on`).
- Stores are off-ring, receive captures only; never a sow target (engine-inherited).

## CACHE BOUNDARY / OUTPUT-CONTRACT

- **Static (cached):** game id, board-row roles, namuamba deal (32/side), obligate-waiting rule
  flag, grand-slam/lape flag, win `33/64`, `^`-canonical restatement rule, and the rule-clause
  citations. Identical every request.
- **Dynamic (tail, never cached):** the canonical board string (`<64 seed counts + 2 stores>`),
  the player's chosen pit predicate, `seed-phrase` `-` (deterministic), reserved. Kept last, small.
- Before any move: restate the canonical state on the `^` line (game id `bao`, turn-index, active
  role, board as 32 pit-counts + 2 stores, order, `seed-phrase -`, reserved), cite the governing L0
  function + engine clause, apply the sow cascade, resolve the capture chain, reprint, narrate. **No
  dice, no cast, no improvised roll — ever.**

## RESEARCH / ORIGIN NOTE (Bao la Kiswahili, Zanzibar)

- Bao (Bao la Kiswahili, "the game of the Swahili", named for the seed-hole rows) is the flagship
  of the East African mancala family, played especially on the **Zanzibar archipelago and the
  Swahili coast**. Its **4-row** layout is the family's most elaborate; the **namumba + keta row**
  split and the **nyumba home** concept are characteristic Zanzibar recension features.
- **Ruleset:** `reconstructed` from the **standard tournament Bao (Bao la Kiswahili)** recension
  as formalized by mid-20th-c. collectors / the Zanzibar competitive scene. Playable, deterministic
  core is stable; the **waiting-obligate opening and the grand-slam/lape grants** are the finer
  points that remain variant and carry the `reconstructed` flag here — never upgraded to rule fact.
- **Sensitivity:** Bao is living contested practice (championship culture at Zanzibar). The pack
  names the Swahili-coast heritage, encodes the tournament recension, and refuses to frame it as a
  chance game. No invented archaeology; contested priority stays flagged.

## BUILD PROMPT

> Build **Bao (Bao la Kiswahili, Zanzibar recension)** on the SOWING/CAPTURE engine as a
> deterministic sowing game — NO RNG, NO dice, NO track-to-a-finish; state this first. Layout is a
> **4-row board**: 2 inner rows (the **namumba stage**, your live playing rows) × 2 outer rows (the
> **keta rows**), 8 pits per row, 16 pits per side, encoded as a 32-pit ring (opposite =
> `(i+16)%32`). Open with the **namuamba**: 32 seeds per side dealt (total 64; `s=22+` deal), with a
> **waiting-pit obligate first draw** before free sowing; the leftmost inner-row pit is the
> **nyumba** home (`NYUMBA: on`). On a turn choose an own-side pit on the namumba stage, lift its
> full count, and **sow one per pit counterclockwise**; if the last seed lands in a pit empty-before-
> sow on your side, **capture the ENTIRE opposite pit's count plus the sown seed** into your store
> and chain backward while the trigger holds (capture count is any nonzero, not just 2/3). After the
> opening there is **no feeding constraint** (`FEEDING: off`), but a **grand-slam** capture that
> empties the opponent's side grants an immediate bonus turn plus a **lape** (`LAPE: on`,
> grand-slam; flagged `reconstructed`). WIN when your store captures **33 of 64** (store-majority),
> or board-empty sweeps to owners then highest store. For every reply: `^`-canonical restate (game
> id `bao`, turn-index, active-role, 32 pit-counts + 2 stores, order, seed-phrase `-`, reserved),
> cite the L0 function + engine clause, the sow cascade, the capture chain, the new canonical, then
> narrate. Flag that the ruleset is **`reconstructed`** — the finer opening (waiting-obligate) and
> grand-slam/lape rules remain variant; the Zanzibar Swahili-coast heritage is honored as living
> practice. No dice, no cast, no improvised roll — ever.

---

*Corpus cross-refs: engine `L1_engines/sowing_capture.DRAFT.md` (§Bao slot); contract
`L0_universal_contract.DRAFT.md`; sibling L2 `kalah.DRAFT.md`; sibling cultural pack
`L3_packs/oware.DRAFT.md` (2×6 Oware — this pack is the 4-row sibling); family open items per
`00_PRIMER.md` §8; honor SPORE_SEED boundary test (sowing vs race engine).*
