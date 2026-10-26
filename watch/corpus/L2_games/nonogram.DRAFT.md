# L2 — Nonogram / Picross (Nikoli) Static Pack (DRAFT)

> **Status:** DRAFT — mark verified when the line-solver passes instrumentation (primer §7:
> legal-line expansion correctness, consistency-check refutation recall, uniqueness adjudication
> on a seeded battery incl. famous clued grids). **Provenance:** derived from `00_PRIMER.md` §4
> (Nikoli galaxy, constraint-puzzle family) and `L0_universal_contract.DRAFT.md` (six-function
> contract; LLM emits pixel placements and cites the line-solver — never the solver). **Class:**
> L2 static prefix. Byte-stable static-first; only the clue lists (instance) are dynamic and
> appended at the tail.
>
> **Research status:** The puzzle is `attested` — published by Japanese publisher **Nikoli**
> in _Puzzle Communication Nikoli_ magazine in 1987 under the name **Oekaki-logic / お絵かきロジック**
> ("picture logic"); the run-length-clue mechanic ("fill runs of K pixels per row/column") is the
> defining Nikoli-era rule. Western names (Nonogram by Non Ishida; Griddlers; Picross by Nintendo's
> Mario Picross 1995) are later coinages over the same mechanic — flag as `attested` with a
> provenance note, no contested-history dispute over the core rule.

---

## GAME ID / FAMILY SLOT

- `constraint-puzzle` family engine (clause-swap over the shared Nikoli constraint grammar).
- `game id` = `NIKOLI-NONOGRAM-01` (zero-indexed enum per L0 FUNCTION 1, fixed for RNG-table
  keying and dedupe).

## RULES (run-length clues define pixels — the entire game, cached)

A Nonogram instance is a rectangular `H×W` grid (or square `N×N`) of **pixels**, each `FILLED` or
`EMPTY`. The instance supplies, for **every row** and **every column**, an ordered **run-length
clue list**: a sequence of `k` positive integers `[c₁, c₂, …, c_k]` meaning "in that line, the
filled pixels appear as exactly `k` contiguous runs, of lengths `c₁, c₂, …, c_k`, in left-to-right
(top-to-bottom) order"; between two runs there is **at least one** empty pixel. A line with an empty
clue list `[]` (the `Ø` clue) means "no filled pixels in this line".

A **solution** is a pixel assignment in which **every row's filled columns reproduce its row clue
exactly** AND **every column's filled rows reproduce its column clue exactly**. Both directions must
match simultaneously. Such an assignment is a **consistent** completion; if exactly one exists the
instance is **unique**.

---

## INSTANCE (dynamic tail)

```
rows  = [ [r₁_1, r₁_2, …], [r₂_1, …], … ]   // H clue lists, row-major
cols  = [ [c₁_1, …], [c₂_1, …], … ]         // W clue lists
H, W  = grid dimensions
```

- Clue syntax: a line with no filled pixels is `[]` (the `Ø`/empty clue). Entries are positive
  integers ≥ 1. The canonical instance string concatenates row-lists then col-lists with a fixed
  separator (see bytes below), for sample:
  `3x3|1,1|Ø|1|1|Ø|1,1` = rows `[1,1]`, `[]`, `[1]`; cols `[1]`, `[]`, `[1,1]`.
- Dimension constraint: for every line, `sum(clues) + (len(clues) - 1) <= len(line)` (the line must
  be long enough to fit the runs plus mandated gaps). Violation → an invalid instance (verifier V0).

## VERIFIER SIGNATURES (deterministic; implementable in JS)

### V0 — Instance validity (well-formedness)

```
VALID_CLUES?(rows: List, cols: List, H: int, W: int) -> Bool
```

True iff `len(rows)==H`, `len(cols)==W`, every row clue fits its width, every column clue fits its
height, all entries integers ≥ 1, and every line fits its span (`sum + gaps ≤ length`). Line-validity
is the only place G is checked; V1/V2 reuse it per-line internally.

### V1 — Line solver (expansion + consistency)

```
line_completions(clue: List<int>, length: int) -> {
  possible: List<Set<int>>, // per-index: set of positions this index can be FILLED in SOME valid line
  consistent: Bool          // false iff no valid line matches the clue
}
```

- **Expansion:** enumerate all valid binary lines of given `length` reproducing `clue` (place `k`
  runs with `≥1` gap between). Each valid line is a bitmask over indices `0..length-1`.
- **Consistency:** `consistent` is true iff at least one such line exists (equivalently
  V0's fit check holds for this single line).
- **Per-index possible-union:** for index `i`, `possible[i]` = set of indices that can be FILLED
  in at least one valid line. (A *guaranteed-filled* index is one filled in every valid line —
  the classic Nonogram deduction; expose as `guaranteed: Set<int>` for the solver to exploit.)
- JS implementation: a simple DP over runs — `dp[j][r] = set of ways to fill first `j` cells using
  first `r` clues` — yields all per-index possible/guaranteed cells in O(W·k·W) per line. Fully
  implementable.

### V2 — Grid verifier (full consistency + uniqueness)

```
solve(rows: List, cols: List, H: int, W: int) -> {
  consistent: Bool,               // does ANY pixel assignment satisfy all row AND col clues?
  count: int,                     // # distinct valid assignments (capped at `limit`)
  witness: Grid | null            // first valid assignment, or null
}
```

- Use V1's per-line expansion plus a constraint walk: start with all cells UNDECIDED; propagate
  guaranteed-filled/guaranteed-empty per line, alternate row/col passes (standard Nonogram line-
  solving loop). If a conflict/empty-possible union arises → `consistent=false`.
- If the propagation fully resolves the grid, `count=1` (unique). If it stalls with undecided
  cells, recurse/backtrack over remaining cells (branch on an undecided cell, re-propagate),
  capping enumeration at `limit` (default 2). `count >= 2` ⇒ *not unique*.
- Deterministic given clue lists; JS-implementable. The LLM reports this verdict verbatim.

### V3 — Solvency / validity gate

```
VALID?(rows, cols, H, W) -> Bool     // true iff unique_solutions(…, 2).count >= 1
unique_VALID?(rows, cols, H, W) -> Bool  // true iff count == 1
```

Canonical published Nonograms advertise a unique solution → use `unique_VALID?` for pack-generation;
`VALID?` for play-session "find any completion". As with Hitori, prefer the unique gate.

---

## CACHE BOUNDARY

- **Static (cached, byte-stable):** GAME ID, rule statement (run-length clues define pixels, both
  directions simultaneous, Ø clue), all verifier signatures V0/V1/V2/V3, output-citation rules.
- **Instance (dynamic tail, never cached):** the `rows`/`cols` clue lists, dimensions, any
  candidate completion grid, `seed-phrase` (`-` unless a future grid-sampling variant). Kept last.

## OUTPUT-CONTRACT NOTES

- Before answering, reprint the canonical clue instance with one leading `^`, then cite V0/V1/V2/V3.
- The LLM proposes pixel placements; it NEVER returns a verdict without routing to the verifier.
  Prose verdicts are reports of verifier output only.
- Nonogram is a *static* puzzle: FUNCTION 4 (transition) and FUNCTION 6 (scoring) are `null`/no-op;
  FUNCTION 5 terminal = "a claimed full completion was verifier-checked". STATE ENCODING and
  LEGALITY (via V1/V2) still bind.

## ASSET NOTES (not cached)

- **Target size:** ~300–500 tokens of prompt body below the header (excluding this notes section).
- **Research status:** `attested` (Nikoli, _Puzzle Communication Nikoli_, 1987, "Oekaki-logic").
  Name coinages (Nonogram/Ishida, Griddlers, Picross/Nintendo 1995) are provenance, not rule
  disputes — no contested-history flag required.
- Cross-refs: `L1_engines/constraint_puzzle` → `L2_games/nonogram` → (future) L3 regional/theme packs.
