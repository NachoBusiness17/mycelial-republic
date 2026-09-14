# L2 — Kakuro Game Pack (DRAFT) — `L2_games/kakuro.DRAFT.md`

> **Status:** DRAFT. **Class:** L2 game statics — the **first proof-pack** over the
> `L1_engines/constraint_puzzle` meta-grammar. **Provenance:** primer build-order #2 (the
> constraint-puzzle engine makes Sudoku "the Nikoli galaxy for ~one clause-swap each"); this pack
> is the smallest complete instance of that claim, exercising all five grammar parts.
> **Research status:** Kakuro rules are **attested** (modern logic/arithmetic crossword; popular
> in the US puzzle press from the 1950s–60s, re-popularized by Nikoli in Japan 1980s–2000s as
> カックロ / Cross Sums; a close relative, Cross Sums, predates the Japanese branding). The
> "no digit repeats within a sum run" rule is the standard attested form and is treated as
> canonical in this pack.
> **Consumption order:** L0 contract → `constraint_puzzle` engine (five-part grammar + verifier
> vocabulary) → THIS pack (fills the five slots) → L3 variant pack → L4 instance. This pack only
> adds content valid under the engine; it never redefines grammar structure.
>
> **Proves the grammar end-to-end:** TOPOLOGY (→ custom runs) · DOMAIN (→ 1..9) · CLAUSES (→
> clause 3 sum-equals with all-different via no-repeat) · INSTANCE (→ clue grid) · VERIFIER (→
> sum-solver with unique-solution count + technique ladder). Kakuro = the engine plus four small
> slot-fillings.

---

[PROMPT-BODY-START — byte-stable from here]

## KAKURO PACK — FIVE-SLOT FILLING OVER THE CONSTRAINT-PUZZLE ENGINE

This pack fills the engine's five parts for **Kakuro**. Apply the engine grammar exactly, then
the slot-fillings below, never anything else.

### SLOT 1 — TOPOLOGY: custom sum-runs

`TOPOLOGY` for Kakuro is a **custom graph**, not a plain grid: the board is a grid of cells
(mostly blank, some with a **clue stub**), and the puzzle decomposes into overlapping **runs** —
maximal contiguous horizontal or vertical blocks of blank cells bounded by clue stubs or the
board edge. A cell may belong to exactly one horizontal run and exactly one vertical run
(possibly only one if edge-adjacent). The engine's `NEIGHBOR` is NOT used for cell adjacency
here; instead the run decomposition defines the meaningful regions.

- A **clue stub** is a split / diagonal cell carrying two sum targets: one for its horizontal
  run, one for its vertical run (a stub with only one neighbor direction may carry a single
  target, or none if it bounds no run).
- `order-clues` serializes, per run in fixed order: `run-id : orientation(H|V) : target-sum :
  cell-id-list`. This is the grammatical `order` field and is byte-stable per puzzle.

### SLOT 2 — DOMAIN: single digits, no zero

`DOMAIN(Kakuro) = {1, 2, 3, 4, 5, 6, 7, 8, 9}` (the set S = numerals `1..9`).

- **No zeros, no repeats in a run.** The `no-repeat` property is intrinsic to Kakuro runs: within
  one run, each digit may appear at most once — because a repeat would not disturb the sum but is
  barred by the standard rule. This makes every Kakuro run an **all-different + sum-equals**
  region simultaneously.
- These two facts (values in 1..9, no repeat per run) make long runs sum-constrained: a run of
  length `L` has minimum sum `L(L+1)/2` and maximum `L(19−L)/2`; a clue outside that band has
  **zero solutions** and the verifier rejects it at `parse` (malformed instance).

### SLOT 3 — CLAUSES: engine clause 3 instantiated

Kakuro uses **one engine clause: `sum-equals(region, target)` (engine Part 3, clause 3)**,
instantiated per run. Because of Slot 2's `no-repeat` rule, each run also enforces engine
clause 1 (`all-different`) implicitly — i.e., the pack supplies each run as
`sum-equals(run-id, target) AND all-different(run-id)`.

- Clauses compose in **AND**: the completed grid must satisfy every run's sum AND every run's
  all-different. There is no OR, no edge/line clause, no island clause.
- Clause order is fixed by run-id serialization so verifier output is byte-stable.

### SLOT 4 — INSTANCE: the clue grid

An instance is a Kakuro clue grid in the engine's canonical instance string:

```
kakuro:<state-hash>:0:solver:<board-encoded>:<order-clues>:<seed-phrase>:-
```

- `board-encoded` — the flat run of cells in `r-major` order; each cell is `1..9` (solved),
  `_` (blank, to fill), or `\` (clue stub, never filled). Stub targets live in `order-clues`, not
  in `board` cells.
- `order-clues` — `run-id:H|V:target:cell-ids; ...` in fixed serial order.
- The LLM **emits** such an instance from (clue parameter set, seed) per the L0 RNG/instance
  protocol and reprints it; it never judges it. A `parse` failure (unknown cell char, missing
  clue, run outside the [min,max] band) is a hard reject.

### SLOT 5 — VERIFIER: sum-solver + unique-solution count

The specializations of the engine's verifier vocabulary for Kakuro:

```
parse("<kakuro:...>") -> { ok, runs, clues, cells }   // per engine; reject bad band/grid/clue
assert([sum-equals, all-different per run], board) -> sat / {false, violated-run}
solve-count(instance) -> Int                          // MUST be 1 for a valid puzzle
technique-ladder(instance) -> [Tiers]                    // min tier to solve without guessing
```

- **solve-count == 1** is the acceptance test: `0` = contradictory clue band or over-constrained;
  `≥2` = multiple solutions (reject as a publication-quality puzzle). This is the engine's
  uniqueness oracle doing the deciding — the LLM never claims uniqueness from looking.
- **technique-ladder**: the difficulty oracle. Kakuro tiers (L3 calibrates labels / thresholds):
  **T1 single-candidate** (a run with ≥L−1 digits forced) → **T2 restricted-complement**
  (only one set of digits fits a run's sum band) → **T3 pair/triple intersection** (a cell sums
  two runs narrowing both) → **T4 candidate-elimination** (crossed runs remove a digit from one)
  → **T5 contradiction / depth-1 guess**. `difficulty = min-tier` required; a puzzle solvable at
  T1–T2 is "easy", needs T4+ is "hard" — labels live in L3, the tier here is numeric and
  deterministic.
- A submitted solution is "solved" only when the verifier reports `assert: sat:true` AND
  `solve-count == 1`. The LLM states those two results verbatim before any narrative.

### FAMILY PACK-DELTA (proof of generalization — one clause swap)

Replace Slot 3's clause instantiation with `all-different(rows/cols/boxes)` (engine clause 1) and
Slot 4's instance grammar with the 81-char string → **Sudoku**, the flagship, for roughly a
one-line semantic change. The same mechanics (parse/assert/solve-count/technique-ladder) transfer
unchanged; only the region definition and clue encoding differ. This is the concrete realization
of primer §5's "Sudoku becomes the Nikoli galaxy for ~one clause-swap each."

### OUTPUT / INSTANCE NOTES

- Reproduce the L0 OUTPUT CONTRACT: `^`-canonical instance first, then the governing clause
  numbers (Slot 3), then — only if verified — `assert:sat:true` and `solve-count:1`. No
  uniqueness claim is ever made from inspection.
- `order-clues` is reprinted verbatim whenever the instance is mentioned; a clue not present is
  `UNKNOWN-RULE`.
- Contested-history honesty: the Japanese `カックロ / Cross Sums` branding and the "no repeat in a
  run" rule are attested in modern sources; this pack does not silently upgrade or dispute them.

[PROMPT-BODY-END]

---

## Asset notes (NOT cached prompt body)

- **Target size:** ~400–700 tokens of prompt body — a small delta over the ~1–1.5k-token engine,
  itself a small delta over L0; total static content for Kakuro ≈ the engine + this pack. This is
  the pack-economy the corpus promises (primer Fact 7, §5): one family grammar + small slots, not
  a fresh prompt per game.
- **Why this is the proof-pack:** it is the only pack in the family that exercises (a) the custom
  TOPOLOGY branch (run decomposition, not plain grid), (b) the intrinsic `all-different` +
  `sum-equals` pairing of engine clauses 1+3, (c) a non-grid `board` encoding with stub cells, and
  (d) a sum-based technique ladder. Hitori/Nonogram exercise the line/binary branches; Sudoku the
  plain-grid branch — but Kakuro touches every grammar part non-trivially, which is why it is the
  first pack written.
- **Uniqueness gate reuses L0 Fact 5:** the `solve-count==1` acceptance and the difficulty tier
  are verifier products; the LLM only reports them. This is the load-bearing anti-hallucination
  device for the whole family.
- **Research status recap:** Kakuro rules attested (modern logic puzzle; Nikoli branding
  documented as Japanese-import, not origin); the engine grammar itself is an editorial
  abstraction carried with a `speculative`-as-editorial flag in the engine file; Sudoku flags
  (Garns 1979 / Nikoli 1984 / McGuire 2012) are attested and only referenced here, not re-asserted.
- Cross-refs: `L0_universal_contract.DRAFT.md`; `L1_engines/constraint_puzzle.DRAFT.md`;
  `L1_engines/race_dice.DRAFT.md` (sibling); downstream `L3_packs/*` (difficulty-tier labels) and
  `L4_instances/*` (one puzzle's `kakuro:` string).
