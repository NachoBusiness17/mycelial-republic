# AB1 — merge-conflict fix: tests/test_behavioral_awareness.py

- Date: 2026-09-30 · Owner lane: AA4 triage #1 (last mile) · No commit (file ownership only).
- Defect: unresolved conflict markers at line 70 (`<<<<<<< Updated upstream` / `=======` / `>>>>>>> Stashed changes`) → `SyntaxError` blocking full-suite collection (3,211 collected, 1 error).

## What the conflict was between

Inside `test_behavioral_candidates_mines_crash_log`, two versions of the crash-row claim assertion:

- **Updated upstream (kept):** B2-374 repair — asserts `"crash entries" in claim` and `"real=" in claim`, with the receipt comment explaining B2-357 rewrote the crash row claim to name its census.
- **Stashed changes (dropped):** stale pre-B2-357 token — asserted `"real crash blocks" in claim`.

## How resolved

Kept the upstream side. Byte-verified against the producer: `mag/improve.py:999` emits `f"Seat crash log: real={real} crash entries"`, so only the upstream assertions match current code; the stashed token was documented as having sat red since the B2-357 landing. Single conflict block — grep for `<<<<<<<`/`=======`/`>>>>>>>` returns nothing after the edit.

## Verification (trust bytes)

```
$ .venv/Scripts/python.exe -c "import ast; ast.parse(open('tests/test_behavioral_awareness.py',encoding='utf-8').read()); print('parses')"
parses

$ .venv/Scripts/python.exe -m pytest tests/test_behavioral_awareness.py --collect-only -q | tail -2
4 tests collected in 0.67s
```
