# AG4 — party_subchain hash coverage + byte-exact append (audit finding #12)

Date: 2026-09-29 · Owner: AG4 seat · Files: `mag/party_subchain.py`, `tests/test_party_subchain.py`

## Finding (fixed)

1. `_hash_entry` hashed only `ts, seat, ok, move, prev_hash, parent_leaf_hash, kind` — the
   `extra` payload (48 rows in the live chain carry one), `parent_root`, and `schema` were
   unauthenticated: anyone appending could mutate `extra` without detection.
2. Appends (`_genesis_unlocked`, `append`) opened the chain text-mode without
   `newline=""`, writing CRLF on Windows — contradicting the byte-exact law.

## Fix (versioned, chain-compatible)

- Schema bumped: `SCHEMA_V1 = "party_subchain.v1"` (legacy), `SCHEMA_V2 = "party_subchain.v2"`,
  module `SCHEMA` now points at v2 so all new rows (genesis + append) are v2.
- `_hash_entry` dispatches per-row on the row's own `schema` field: v1 rows hash under the
  old seven-field rule (unchanged bytes → old hashes still verify); v2 rows additionally
  authenticate `extra`, `parent_root`, and `schema`. Schema-downgrade attacks (v2 row
  rewritten as v1) fail because the stored v2 hash covers the wider blob.
- Both JSONL appends opened with `newline=""` so `chr(10)` stays bare LF on Windows.

## Proofs

- `pytest tests/test_party_subchain.py -q` → **6 passed in 1.00s** (3 existing + 3 new:
  v1-rows-verify + mixed v1/v2 upgrade, v2 extra-tampering FAILS with content hash
  mismatch, appended file carries no CRLF bytes via rb read).
- Live chain verify: `python -m mag.party_subchain verify` →
  `{"ok": true, "schema": "party_subchain.v2", "n": 834, "errors": []}` — PASS.
  Row count by bytes is **834** (the mission brief said 831; trust bytes: 834 parsed
  non-blank rows, all `party_subchain.v1`). Head `0d09563f…4347` unchanged.
- Live file already contains **280 historical CRLF** line endings from pre-fix text-mode
  appends; verification parses per line so they are read-compatible. NOT rewritten —
  the chain is the record; only new appends are guaranteed bare-LF.
- No external literal dependency on the schema string (grep across `mag/ tools/ tests/`:
  only the module itself defines/uses `party_subchain.v1/.v2`; callers import only
  `append`/`mount`/`want_full`).

## Notes for future appends

First live append after this landing writes the first v2 row with `prev_hash` = current
v1 head — mixed-chain verify is proven by test. v1 rows keep their historical
unauthenticated-`extra` weakness (accepted, chain-compatible); v2 closes it.
