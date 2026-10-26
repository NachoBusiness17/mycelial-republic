# L1 — Sowing/Capture Engine (DRAFT) — `L1_engines/sowing_capture.DRAFT.md`

> **Status:** DRAFT. **Class:** L1 family engine — one mechanical spec shared by every
> **sowing/capture** (mancala-family) game: Oware → Bao. It is a **sibling, not a child**, of the
> race/dice engine: same L0 six-function contract, a different core operator (**sowing**, not
> movement-to-a-finish) and a different resolution order (**end-of-sow capture**, not per-landing
> capture). **Boundary origin:** flagged as an open item by `L3_packs/oware.DRAFT.md` §BOUNDARY
> TEST (the race engine could not express the sowing kernel). **Provenance:** primer §7 build-order
> (mancala family), Fact 7 taxonomy. **Research status:** Oware mechanics `attested` (Akan
> recensions); Bao `reconstructed`/speculative in finer rules; family genealogy contested — flags
> per pack, never silently upgraded. **Consumption order:** L0 contract → this engine (family
> mechanics) → one mancala pack (deltas) → L2 statics → L3 cultural pack.
>
> ---

[PROMPT-BODY-START — byte-stable from here]

## SOWING/CAPTURE ENGINE — FAMILY MECHANICS

A **sowing/capture game** is a closed ring of pits holding seed-counts, two off-ring stores, and a
**sow** operator: a player lifts the full count from a chosen own-side pit and re-deposits one seed
into each successive pit counterclockwise; a **capture** resolves when the final seed of the sow
meets the pack's landing rule (canonically: lands in an empty pit on the sower's own side whose
opposite holds `2`/`3` seeds). Win is by **store count**, not track completion. There is **no RNG
move amount**: move length is the chosen pit's stored count. You apply these mechanics exactly as
written, plus pack deltas, never anything else.

### RNG-NEGATIVE (deterministic — resolves L0 negatively)

There is **no seeded RNG draw in this engine**. The L0 Universal RNG protocol applies here in the
**negative**: because no roll, cast, or draw exists, the L0 rule "the LLM never improvises a roll"
is satisfied by construction — there is nothing to report and nothing to invent. Move amount is the
chosen pit's count (`board[pit]`), not a table value; the canonical `seed-phrase` stays `-`; a roll
is never emitted, narrated, or fabricated.

### STATE (board of pits, seed counts, stores)

- **Board:** a ring of `N` pits (canonical `N = 12`, `N/2` per player), each holding a non-negative
  seed count, encoded `[c_0 .. c_{N-1}]`, ascending counterclockwise, wrap `/N`; a pit's
  **opposite** = `(i + N/2) mod N`. Pits `0..(N/2-1)` = one side, `(N/2)..(N-1)` = the other (pack
  keys roles).
- **Stores:** one **store** per player, off the ring, only ever receiving captures; a sow never
  lands in a store (canonically).
- **Canonical string** (L0 F1): `<id>:<hash>:<turn-index>:<active-role>:<board+2stores>:<order>:
  <seed-phrase `-`>:<reserved `-`>`. The `board` field is the sole authority on pit/store counts.

### INITIAL (seeded n-seed distribution)

- **INIT:** fixed distribution — **`s` seeds per pit** over `N` pits (Oware `s = 4`, total `48`);
  stores empty; starting `active-role` and `turn-index = 0` per pack.
- **Determinism:** fully determined by pack `INIT` + game id; reproduces identically each run. The
  canonical layout is symmetric, so `seed-phrase` does not perturb INIT (L0 reproducibility holds
  trivially). The initial move is legal by construction.

### LEGALITY (legal sowing moves from pit with n>1 seeds)

`LEGAL?(state, T) -> Bool { legal, reason }` (L0 F3). A candidate `T = (role, pit)` is **legal**
iff all hold:

1. **Own-side:** `pit` is on the `active-role`'s own side.
2. **Has seeds:** `board[pit] >= 1` (engine floor; a pack may raise to `≥2`).
3. **Feeding / supply rule (pack-dependent, Oware:`on`):** choosing `pit` must not leave the
   opponent with **zero legal moves** next. If every candidate breaks this, `LEGAL?` is hard-
   `false` and play passes to TERMINAL/`LOOP`. A pack may disable it (free-move/grand-slam vars).
4. Nothing is "blocked": pits are concurrent; no piece collision exists.

A `false` on role/order or a `0`-count pit is a hard `false`; ambiguity → hard `false`. The LLM
reports the chosen pit as a predicate (`LEGAL?(s, pit p)`) and **never** emits a roll.

### TRANSITION (sow one-by-one counterclockwise; last-seed landing rules; capture via
landing-in-empty-across with backward chaining)

`APPLY(state, T) -> state'` (L0 F4). A move is a **sow cascade + optional capture**, in fixed order:

1. **Lift:** remove all `s = board[pit]` seeds (pit becomes `0`).
2. **Sow, one-by-one, counterclockwise:** deposit one seed into indices `pit+1, pit+2, …, pit+s
   (mod N)`; the chosen pit is left empty and not re-seeded. The cascade is a single atomic
   resolution, not recomputed per step; pits may be re-seeded during it.
3. **Last-seed capture test** — end-of-sow position `pit_s = (pit + s) mod N`; tested once only:
   if the final seed landed in an own-side pit that was **empty before the last deposit** (now =
   `1`) **and** its opposite `(pit_s + N/2) mod N` holds the pack's capture count (canonical
   `2`/`3`), capture that opposite count **plus** the just-sown seed into the sower's store; else
   `effect: none` (seed stays as a new count).
4. **Backward chaining:** after a capture at `pit_s`, chain to `pit_s - 1, pit_s - 2, …`: capture
   each pit that is on the sower's own side, ended this sow at exactly `1` (empty-before-sow), and
   whose opposite holds the capture count. Resolve each pit exactly once; stop at the first
   non-trigger. A pit is never captured more than once per sow.
5. **Advance:** `turn-index += 1`, recompute `state-hash`, swap `active-role` (or keep it on a
   `LAPE: on` bonus turn — see GRAND-SLAM/LAPE FLAG), reprint canonical string, then narrate.

### TERMINAL (store majority 25/48 or no-legal-moves)

`TERMINAL?(state) -> Bool { terminal, winner, score }` (L0 F5):

- **Store-majority win:** a player wins when their store reaches a **strict majority** of total
  seeds — canonically **25 of 48** (`24`=tie, `25` clinches). Ends immediately on that landing.
- **No-legal-moves / board-empty:** when the player to move has no legal move, end the game: the
  **remaining board stones go to the player on whose side they sit**, then stores are compared; the
  higher store wins, a `24–24` split is a pack tie-break or `draw`.
- **LOOP guard (L0 F5):** a repeated state does **not** auto-terminate unless the pack WIN says so;
  report `LOOP` with the prior `state-hash`. No piece ever "bears off"; there is no finish line.

### SCORING (store counts)

`SCORE(state) -> Score` (L0 F6): **score = each player's store count**, derived from the
`board`/store fields alone. Higher store wins; tie per pack; else `SCORE` returns the raw
`(storeA, storeB)` tuple.

### GRAND-SLAM / LAPE (lape/winning-again) VARIANT FLAG

`LAPE: on | off` (pack flag). When **on** (a common mancala-family variant — *lape*/"win again",
also *grand-slam*), a capture that meets the pack's bonus condition (e.g. empties the opponent's
side) grants the sower an immediate **bonus turn** before the role swaps. When **off**, the standard
`active-role` swap occurs (TRANSITION §5). The exact trigger is pack-defined; the engine supplies
the flag and the swap behavior it toggles, defaulting to `off`.

### OUTPUT (inherited from L0)

Apply the L0 OUTPUT CONTRACT before/after any move: restate canonical state on the `^` line, cite
the governing L0 function + engine clause, emit the new canonical string, then narrate. **No roll is
ever reported** (RNG-negative); the move is a chosen predicate, instance data, not narrative
flourish. Pack delta **wins** over this engine clause-wise, except structural clauses (ring/sow
order, end-of-sow capture, chain direction, store-majority machinery), which a pack may not
override — it may only set the exposed flags and constants.

[PROMPT-BODY-END]

---

## Asset notes (NOT cached prompt body)

- **Target size:** 800–1.5k tokens of prompt body (the body above is byte-stable engine; each pack
  adds a 1–3-line delta — constants, capture count, feeding/lape flag, majority number — and
  expands into its own `L3_packs/*`).
- **RNG-negative is structural:** unlike race_dice, this engine defines an *empty* roll table; L0's
  "never improvise a roll" is satisfied negatively (no roll exists). Same framing the Oware pack
  uses.
- **Static-first template order** fixes the six functions STATE → INITIAL → LEGALITY → TRANSITION →
  TERMINAL → SCORING, matching L0's numbering so a reply cites both function number and clause.
- **Capture is end-of-sow, backward-chained** — not per-landing: the genuine engine divergence
  from race_dice, and what the race engine's BOUNDARY TEST flagged as unexpressible.
- **Kalah slot rationale:** Kalah is the classic **commercial (American) mancala** — a **1940s
  invention** credited to **William Champion Jr.** (marketed/patented around the 1940s, later
  resold widely), a deliberate abstraction of the African family, **not** a traditional regional
  game. The history note belongs in the pack, not the engine; the slot exists because Kalah shares
  the sow/capture kernel and store-majority scoring with Oware/Bao.

## FAMILY PACK SLOTS (cultural packs that dock on this engine)

- **Oware** (`L3_packs/oware.DRAFT.md`, **attested**) — `N=12`, `s=4` (48 seeds), capture on
  `2`/`3`-opposite, feeding hard-`on`, win `25/48`, `LAPE: off`. The reference build: a near-thin
  delta (only constants, the feeding constraint, and the capture count differ).
- **Bao** (`L3_packs/bao.DRAFT.md` TBD, **reconstructed**/speculative in finer rules) — the East
  African (Swahili coast) **4-row** high-strategy mancala; docks here for the shared sow/capture
  core, but its multi-row layout and home/mark concepts need pack-level extensions — not flattened
  into Oware's 2×6 shape.
- **Kalah** (`L3_packs/kalah.DRAFT.md` TBD, **attested** as a commercial game) — the **1940s
  Champion invention**, `N` variable (often 6+6), `s=3–4`, capture on empty-opposite-nonzero,
  store-majority win, `LAPE` store-majority variants. Slotted to signal the family's modern
  **commercial** branch; its history pack documents the 1940s invention/patent framing, so the
  engine itself carries no commercial claim.

---

*Corpus cross-refs: contract `L0_universal_contract.DRAFT.md`; sibling engine
`L1_engines/race_dice.DRAFT.md` (sow/capture is a distinct L1, boundary-origin per
`L3_packs/oware.DRAFT.md`); downstream `L2_games/*`, `L3_packs/oware.DRAFT.md`,
`L3_packs/bao.DRAFT.md`, `L3_packs/kalah.DRAFT.md` (TBD); honor `00_PRIMER.md` §8 open questions.*
