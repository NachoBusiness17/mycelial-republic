# L2 — Hitori (Nikoli) Static Pack (DRAFT)

> **Status:** DRAFT — mark verified when the verifier passes instrumentation (primer §7
> continuous: legal-instance acceptance, uniqueness-count sanity, refutation recall on a
> seeded test battery). **Provenance:** derived from `00_PRIMER.md` §4 (Nikoli galaxy,
> constraint-puzzle family, family table clause-swap per build-order #2) and `L0_universal_contract.DRAFT.md`
> (six-function contract; LLM emits decodes/moves and applies the three-constraint checker —
> never the solver). **Class:** L2 static prefix. Byte-stable static-first: everything before
> `[PROMPT-BODY-START]` is fixed across requests; only the instance (the digit grid) and seed
> are dynamic and appended at the tail.
>
> **Research status:** Hitori rules are `attested` (Nikoli Magazine, published late 1980s–present;
> Nikoli's own English rule page). The principle of a grid puzzle with duplicates-plus-fewer-
> constraints is Nikoli-stable. No contested-history flag needed for the core rule set; see
> `§Cache boundary` and accept a loose `Hitori`-name provenance note (a few unrelated Western
> practices share the name; the Nikoli genre is the one encoded here).

---

## GAME ID / FAMILY SLOT

- `constraint-puzzle` family engine (per primer §7 build-order #2 — this is a clause-swap over the
  shared Sudoku/Mahjong/Nikoli constraint grammar).
- `game id` = `NIKOLI-HITORI-01` (zero-indexed enum per L0 FUNCTION 1; kept fixed for RNG-table
  keying and dedupe).

## RULES (the three constraints — the entire game, cached)

A Hitori instance is a square grid of digits. The player shades cells. A **solution** is an
assignment of every cell to `SHADE` or `UNSHADE` satisfying **all three** rules:

1. **Shade duplicates.** No row and no column may contain an unshaded duplicate — i.e., for every
   row and every column, the unshaded digits present are **pairwise distinct**. (Two identical
   digits in the same row/column force one or both to be shaded; identical digits in different
   rows/columns are unconstrained.)
2. **No orthogonal shade adjacency.** No two shaded cells may share an edge (orthogonal neighbor);
   diagonal adjacency is allowed.
3. **Unshaded connected.** The set of unshaded cells must be **fully connected** under orthogonal
   adjacency (every unshaded cell reachable from every other by orthogonal unshaded steps).

All three are simultaneously necessary and sufficient. A grid with at least one assignment
satisfying all three is **solvent**; if exactly one assignment satisfies all three, the instance
is **unique**.

---

## INSTANCE (dynamic tail)

```
grid = <digits, row-major, W x W, 1..9>
width = <W>
```

- `grid` is a single flat string of `W*W` single digits, row-major, no separators (e.g. `123456789`
  for W=3). Whitespace and separators are FORBIDDEN in the canonical string — byte-shape matters
  for the static prefix.
- `width` is implicit from `length(grid)` (must be a perfect square `W*W`); it is not separately
  encoded, but should be restated in prose as `W=N`.

## VERIFIER SIGNATURES (deterministic; implementable in JS)

The LLM never solves. It emits candidate shade-sets / completion claims; the verifier decides.
Provide the following pure functions. All are deterministic given the canonical `grid`.

### V1 — Constraint check (the three-rule checker)

```
solve(grid: String, shade: Set<int>) -> {
  legal: Bool,
  reasons: String[]          // set of violated rule names; empty when legal
}
```

Where `shade` is an index set into the `W*W` row-major cells (`0..W*W-1`). For each of the three
rules, compute and append a violation string if it fails:
- `"row/col unshaded duplicate at <pos>"` if an unshaded duplicate digit shares a row or column.
- `"shade adjacency at <pos>"` if two shaded cells share an orthogonal edge.
- `"unshaded disconnected (component <k>)"` if the unshaded graph is disconnected (report the
  count of orthogonal connected components `k` ≥ 2).

`legal == true` iff all three are satisfied. All checks are linear / O(W²) union-find or BFS —
trivially JS-implementable.

### V2 — Uniqueness count

```
unique_solutions(grid: String, limit: int = 2) -> {
  count: int,                // number of distinct valid shade-sets found (capped at `limit`)
  witness: Set<int> | null   // first valid shade-set found; null if none
}
```

Enumerate distinct shade-sets satisfying all three constraints up to `limit`. Return the count
(≥ the number actually enumerated when `count >= limit`) plus the first witness. For adjudication
of "unique" vs. "multi", the caller uses `count >= 2` to mean *not unique*. Implementation note for
JS: a backtracking search over cells with the three constraints as pruning + a visited-set keyed on
the canonical shade signature (sorted index string) is enough for the W≤9 magazine scale; exact
counting beyond `limit` is not required.

### V3 — Solvency / instance validity

```
VALID?(grid: String) -> Bool       // true iff unique_solutions(grid, 2).count >= 1
```

A claim that "this instance is a valid Hitori" passes only if `count >= 1`. A publisher-facing
`VALID?` gate (for pack-generation) requires `count == 1` (unique); a play-facing gate for a
"find any one valid shade-set" variant requires only `count >= 1`. Prefer the unique gate for
canonical published Hitori, which always advertises a single solution.

---

## CACHE BOUNDARY

- **Static (cached, byte-stable):** GAME ID, the three-rule statement, all three verifier
  signatures (V1/V2/V3), OUTPUT-contract citation rules (restate `^`-canonical grid, cite a
  rule number before answering, never invent cells). These are identical every request.
- **Instance (dynamic tail, never cached):** the `grid` string, any candidate `shade` set, `seed-phrase`
  (unused here — Hitori is non-random/zero-move; seed field is `-` unless a future variant needs
  grid-sampling). Kept last and small.

## OUTPUT-CONTRACT NOTES

- Before answering, reprint the canonical grid with one leading `^`, then cite V1/V2/V3 clause as
  the governing rule.
- The LLM may reason and propose; it must NOT return a final verdict (`legal`, `unique`) without
  first routing to the verifier. Verdicts in prose are only ever a report of verifier output.
- Hitori is a *static* puzzle (no turn transitions, no scoring): FUNCTION 4 (transition) and
  FUNCTION 6 (scoring) are `null`/no-op; FUNCTION 5 terminal = "a claimed complete shade-set was
  verifier-checked". The six-function contract still binds `state encoding` and `legality`.

## ASSET NOTES (not cached)

- **Target size:** ~300–500 tokens of prompt body below the header (excluding this notes section).
- **Research status:** `attested` for rules (Nikoli Magazine, late 1980s–present; Nikoli English
  rules). Flag only if a variant adds contested mechanics (e.g., rectangle/region variants are
  post-hoc house rules — mark those L3 if ever added).
- Cross-refs: `L1_engines/constraint_puzzle` → `L2_games/hitori` → (future) L3 regional variants.
