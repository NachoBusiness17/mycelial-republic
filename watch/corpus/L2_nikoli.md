# L2 Nikoli Grammar — Sudoku (SELF-BUILT-CORPUS)

STATUS: SELF-BUILT-CORPUS (fallback draft; not builder-original)
SCHEMA: l2_nikoli_sudoku.v1
EXTENDS: L0 Universal Game Contract (six functions, verdict vocab).
ROLE: W1 insurance — static grammar for Nikoli-style constraint puzzle.

## 1. Grid

- 9×9 board, cells indexed (row, col), both 0..8.
- Cell value domain: 1..9, or empty (placeholder for puzzle givens/blanks).

## 2. Constraints (deterministic, verifiable)

1. Rows: each row 0..8 contains each digit 1..9 exactly once.
2. Columns: each column 0..8 contains each digit 1..9 exactly once.
3. Boxes: each 3×3 block (rows 3a..3a+2, cols 3b..3b+2 for a,b in 0..2)
   contains each digit 1..9 exactly once.

## 3. Uniqueness Constraint

- A valid puzzle (given set) MUST have exactly ONE solution.
- Verification:
  - A candidate solution passes if it satisfies constraints 1-3 (PASS).
  - A candidate grid that violates any constraint => FAIL with reason code
    `ROW_DUP | COL_DUP | BOX_DUP | OUT_OF_RANGE`.
  - A grid matching the givens and satisfying 1-3 with >1 completion => TIE
    (non-unique), reason `NON_UNIQUE`.
- givens are immutable; a solution must equal {given || blank-inferred} where
  blanks are filled but givens never change.

## 4. L0 Instantiation

- `setup(seed, puzzle)` initializes from the given grid.
- `move(state, actor, cell, value)` sets a blank cell; rejects changes to givens.
- `legal` returns empty (constraint solvers don't enumerate game moves) or the set
  of {cell, value} consistent with current partial fill.
- `evaluate` => PASS if complete and satisfies 1-3 with unique completion;
  FAIL on any violation; TIE on non-unique or incomplete.
- RNG: unused; all state derives from givens (deterministic by construction).
