# DOOR VERIFIER INTAKE — 2026-09-06 (worker: verifier, group 2 width 8)

Commission: watch/SELF_STEAL_ASTRA_SEAT_20260905.md — door_verifier.py, the world
capsule's small verifier with the three founding receipts as built-in tests.

## Present/absent
PRESENT — the codex seat had returned `state/world/door_verifier.py` (Sep 5 17:07).
Path: `C:\Users\foste\Documents\projects\local_sovereign_agent\state\world\door_verifier.py`
Status: REVIEWED + TESTED + MINIMALLY FIXED (interface failures only, listed below).

## PoW rule (verified against the record BEFORE coding)
FOUNDING_RECORD.md line 3: `work: SHA256(M|n), d=16, UTF-8, no trailing newline`,
with `M = door/add/v1|door_id|author|world|content_hash`.
The record's own receipts each have exactly 4 leading zero hex chars = 16 leading
zero BITS, and nonces (58,947–100,898) sit at the 2^16 expected-trials budget.
VERDICT (tri-state): **d=16 means 16 leading zero BITS** — SUPPORTED by the record
itself. The commission brief's phrasing "16 leading zero NIBBLES" is DISPUTED by
the record's own bytes; under the nibble reading all three founding receipts would
fail, which contradicts the record's "VERIFIED (both sides)".

## Receipt results (`python state/world/door_verifier.py selftest`, exit 0)
| Receipt | Record line | n | Recorded hash | Verdict |
|---|---|---|---|---|
| R1 (Law 1, first-voice) | 9 | 86761 | 00004d9c...cc8d78 | PASS |
| R2 (Law 2b full id, second-voice) | 15 | 100898 | 00007716...66e3e4 | PASS |
| R3 (Law 3, second-voice) | 20 | 69666 | 0000577b...9a805 | PASS |
| R1 full-M vs AUDIT TRAIL (record line 29) | 29 | 86761 | — | PASS (byte-identical) |
| R1 via verify_receipt(m,n,expected,d=16) | — | 86761 | — | PASS |
| R1 via verify_law(m, C, n) | — | 86761 | — | PASS |

Extra: JSONL mode on `state/world/goals_receipts.jsonl` → 5/5 PASS (exit 0).

## Receipt 2a (record line 14): UNPROVEN from record bytes
n=58947, hash 00003bc3644ba1438e6bbcd82b010c68c50f964ded9ed51cc8e6a6f7ee926039.
Its M used the ellipsis door_id (audit trail: fault "ellipsis key... corrected by
appending"), and the exact ellipsis bytes are NOT in the record — M is not
reconstructible, so it is rightly excluded from the byte-faithful selftest. No
DISPUTED bytes: every table entry matches the record byte-for-byte (checked
programmatically against all four n/hash pairs and all three C values in the md).

## Fixes applied (tests failed before these; nothing else touched)
Found state: the three receipts verified, but the COMMISSIONED INTERFACE failed —
1. `python state/world/door_verifier.py selftest` errored (treated "selftest" as a
   JSONL filename, exit 1).
2. `verify_law(m, c, n)` did not exist.
3. `verify_receipt(m, n, expected_prefix, d=16)` did not exist (only a dict-based
   `verify_receipt`).
Changes, exactly:
- `main()`: built-in mode now also fires on `selftest` (`args.jsonl in (None, "selftest")`).
- Added `leading_zero_bits(digest)` (the d-bit rule), `verify_law(m, c, n, d=16)`
  (commitment c must be m's final field + PoW meets d bits), commissioned
  `verify_receipt(m, n, expected_prefix, d=16)` (hash prefix + d bits).
- Added `FOUNDING_M_R1` — the record's unabridged receipt-1 M (AUDIT TRAIL,
  record line 29) transcribed byte-faithfully; selftest asserts the computed
  table-M equals it (pins every field against transcription drift).
- `compute_digest` now accepts (m, n) or a receipt dict; dict-based verifier
  renamed `verify_receipt_record` (threshold re-expressed via leading_zero_bits);
  `report()` call updated. Behavior of all pre-existing paths unchanged.

## Negative controls (verifier can actually fail — tamper detected)
Tampered nonce → FAIL-detected. Tampered content_hash → FAIL-detected. Wrong
commitment in verify_law → FAIL-detected. d=20 (stricter) → FAIL-detected.

## Verdict
**SUPPORTED** — door_verifier.py is the Astra world capsule's small verifier;
selftest PASSES on the founding record exactly as written. Record untouched
(read-only respected). $0, no network, no daemons.

Witness: verifier (concurrency probe group 2, slot codingplan.max-flash-5x.6).
