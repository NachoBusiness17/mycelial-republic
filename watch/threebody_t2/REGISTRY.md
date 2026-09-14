# T2 REGISTRY — pointer verification (SCRIBE)

- **OK** — ask_router.py:20 — `LEDGER = LEDGER_DIR / "ledger.jsonl"` (exact; ledger file absent from disk).
- **OK** — ask_router.py:84 — `else 0.5 # unseen lane = neutral prior`.
- **OK** — ask_router.py:110 — `mem = {"ok": False, "err": "dry: skipped"}` (Sancho-confirmed).
- **OK** — ask_router.py:108-146 — span nests both dry-skip blocks (memlance ~109-114, verkle ~144-150).
- **OK** — ask_router.py:210 — `add_argument("--record", action="store_true")` (Sancho-confirmed).
- **OK** — ask_router.py:181-182 — `--record` reads stdin via `sys.stdin.read()`; `cmd_record` writes ledger.jsonl.
- **OK** — "zero callers" — grep /mag/mag: `--record`/`cmd_record` only inside ask_router.py; no external invoker.
- **OK** — harness.py:282-305 — AUTHORIZED handling: dry→`_record_receipt("execute_stub"...STUB)` + `_mark_processed`; stub consistent with "no advancement".
- **OK** — /mag/memory/runs/ask_router/receipts.jsonl — 4 rows, ts 04:42:34–04:54:29Z, all `dry:true`, `ledger_rows:0`.
- **OK(nuance)** — receipts "memlance.ok:false" — actual fields `optional_memlance_ok`/`optional_verkle_ok` false; semantics match dry-skip, field name off.

**VERDICT: 9 OK, 0 WRONG-SPAN, 0 MISSING.** All pointers verify; only naming nuance in receipts fields.
