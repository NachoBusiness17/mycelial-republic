PROMPT-BODY-START
# CONSTRAINT VERIFIER INTERFACE — L1 ENGINE
# Mechanical law only. Flags travel with packs.
# No scholarship. External solver stub only for V3.

## VERIFIER SIGNATURE (V1–V5)

V1 LEGAL-PARTIAL
- Input: pack (clauses + instance string)
- Output: bool (satisfies all clauses under partial assignment)
- No solver call. Pure clause check.

V2 COMPLETE?
- Input: pack
- Output: bool? (may be UNKNOWN if solver timeout)
- Calls external solver stub; labels result as COMPLETE / INCOMPLETE / TIMEOUT
- LLM never decides completeness.

V3 UNIQUE?
- Input: pack (V3 mandatory for Sudoku packs)
- Output: bool? labeled by solver stub only
- Calls external solver stub; returns UNIQUE / NOT-UNIQUE / TIMEOUT
- LLM NEVER judges uniqueness.
- Sudoku binding: instances under 17 givens can never be emitted as unique.

V4 DIFFICULTY
- Input: pack
- Output: scalar or band label from solver metrics (clues, backtracks, etc.)
- Solver stub supplies the metric.

V5 INVENTORY
- Input: pack
- Output: list of clause coverage / variable domains / fixed cells
- Pure mechanical count, no interpretation.

## SUDOKU PACK BINDING

- Grid: 9x9
- Domain: 1..9
- Clauses: all-different (row, col, box) — 27 all-different constraints
- Instance string: exactly 81 characters (0-9, 0 = empty)
- V3 UNIQUE? is mandatory for any Sudoku pack emission.
- Rule: any instance string with fewer than 17 non-zero givens MUST NOT be emitted as UNIQUE (solver stub will label such cases NOT-UNIQUE or TIMEOUT; interface passes the label verbatim).

## PACK FLAGS (travel with every pack)

- legal_partial: V1 result
- complete: V2 result (with solver label)
- unique: V3 result (solver label only)
- difficulty: V4 metric
- inventory: V5 list

## SOLVER STUB CONTRACT

interface calls:
  solver_stub(pack, mode="unique" | "complete" | "difficulty")
returns:
  {label: "UNIQUE" | "NOT-UNIQUE" | "COMPLETE" | "INCOMPLETE" | "TIMEOUT", metric?: number, inventory?: [...]}

LLM supplies no judgments on V2/V3/V4. Stub is authoritative.

PROMPT-BODY-END