# LAW: living-file hash registration (2026-09-26, B2-156)

This note is the owning spec for how the shared-inbox hash law treats
append-heavy living files (queues, ledgers, boards). It amends the fold
contract of `scripts/index_fold_host.mjs` and the validate gate of
`mag/shared_surface.py`. Spec landed before the code that implements it.

## Problem

The fold registers a file as one sha256 point-in-time seal. Verify
(`index_fold_host.mjs verify`, lines 271-305) and validate
(`mag/shared_surface.py`, items loop) re-hash the WHOLE file and call any
difference a HASH MISMATCH. For living files that is wrong by design:

- `burn_wave_20260926/QUEUE.md` was registered 13:15:42Z, self-feed appends
  staled it by 13:19:02Z (one hash-refresh register), and it is stale again
  the same evening (verify 2026-09-26: 973 clean, 1 mismatch = QUEUE.md).
- `LINKS.jsonl` took 4 hash-refresh registers in about 2 hours on 09-26
  (index_events.jsonl 11:35:54Z, 12:40:34Z, 12:47:37Z, 13:21:20Z). The last
  refresh names a receipt `B2_41_hash_freshness_20260926.md` that does not
  exist on disk (filed as owed, never synthesized).

Every concurrent append makes the two busiest boards count as hash
failures. Verify cries wolf; real tampering hides in the noise; writers
burn registers papering over the design. Repeated re-registers are the
forbidden fix (B2-156 brief): they treat the symptom and still leave the
file stale between refreshes.

## Law

Two declared living shapes, chosen by the writer at registration. They exist
because growth has two real byte shapes, discovered by testing the first
design against a real self-feed append on 09-26:

- Append-only originals (LINKS.jsonl, phone_relay_log.jsonl, EVENTS.jsonl)
  grow at the end, so a prefix seal is verifiable.
- Edit-shaped working boards (burn_wave_20260926/QUEUE.md) grow by
  INSERTION under their `## Open` anchor near the top, so every insertion
  shifts bytes inside any prefix; the first design (prefix seal only)
  false-failed exactly there 30 minutes after landing.

1. SEALED LIVING (`add --living`): the event carries `"living": true`,
   `"size": N` where N is the file's byte length at registration and
   `sha256` is the sha256 of exactly those first N bytes. The pair
   (sha256, size) is the SEAL; bytes after N are unsealed growth. `add`
   reads the file once so the pair is internally consistent. Verify:
   - file shorter than N: LIVING TRUNCATED, hard fail.
   - sha256(first N bytes) != sealed sha: LIVING PREFIX MISMATCH, hard
     fail. The sealed prefix was mutated; that is tampering, not growth.
   - prefix matches (with or without appended bytes): LIVING OK. Counted
     and printed, never a failure, never a reason to re-register.
2. OPEN LIVING (`add --living-open`): the event carries `"living": true`
   and `"seal": "open"`, no byte seal. For edit-shaped boards whose bytes
   change by design and whose integrity is carried by the event log and
   per-row receipts, not by whole-file bytes (QUEUE.md is a projection of
   filed receipts; LINKS.jsonl is an original ledger and must use the
   sealed shape). Verify counts LIVING OPEN, never a failure.
3. A register WITHOUT a living flag seals the whole file; the exact-match
   rule is unchanged for it. Living is writer-asserted per registration,
   never inferred from class. Class stays provenance (QUEUE.md is class
   BOARD/RECEIPT, LINKS.jsonl class data); hash law is orthogonal to
   class, so class-based exclusion is rejected.
4. A living item with neither a usable `size` nor `seal: "open"` (rows
   registered before this law existed) is LIVING UNVERIFIED: a warning in
   validate, a counted line in verify, not a hard fail. Steady state is
   empty; it is a migration residue, not a target shape.
5. Last-register-wins is unchanged: a later plain `add` re-seals the
   whole file and drops the living flag; a later `add --living` or
   `add --living-open` re-classifies. Re-seal is for semantic content
   changes (rewrites, schema fixes, reclassification), never for mere
   growth.
6. No other writer changes: `md_record_seal.py` autoseal registers stay
   whole-file (one-off receipts are not living); the drift patrol must
   stop daily whole-file refreshes of living rows and may use this law
   instead.

## Rationale for prefix-seal over the alternatives

- Skip-and-count (verify ignores living files): loses tamper-evidence of
  everything ever written to the board. Rejected.
- Class-based exclusion: class is already overloaded; QUEUE.md proves a
  board can carry any class. Rejected.
- Close-pass refresh (re-register at session end): the forbidden
  re-register papering; the file is stale in between anyway. Rejected.
- Prefix-seal (chosen): append-only growth is PROVABLE (the sealed bytes
  still hash true), staleness stops being a failure, and any mutation or
  truncation of sealed history still fails hard. Cost: one stored integer.

## Implementation contract

- `scripts/index_fold_host.mjs`: `add [--living|--living-open] <file>
  [class] [purpose...]`; fold carries `living`/`size`/`seal` into items;
  `verify` prints `X hash-clean, Y living-ok, Z living-open, W mismatched,
  M missing, U living-unverified` and lists hard failures as LIVING
  PREFIX MISMATCH / LIVING TRUNCATED.
- `mag/shared_surface.py`: same rule in the items loop; grown sealed
  living items and open living items are not errors; the result reports
  `living_ok`, `living_open`, and `living_unverified` counts; unverified
  rows warn.
- Tests in `tests/test_index_fold_host.py` and the python-side suite
  cover: append growth passes, prefix mutation fails, truncation fails,
  insertion growth passes only in the open shape, static behavior
  unchanged, legacy living-without-seal warns.

## Migration (executed 2026-09-26)

`burn_wave_20260926/QUEUE.md` and `LINKS.jsonl` re-registered through
`add --living` under writer `zcode-b2-156-living-hash-law`, one event
each, after the code landed; `phone_relay_log.jsonl` followed as the
third append-only original. The QUEUE.md self-feed append (B2-197/198/199
inserted under `## Open`) then false-failed the prefix seal, which
amended this spec with the open shape; QUEUE.md re-registered as
`add --living-open`. Receipt:
`burn_wave_20260926/B2_156_living_hash_law_20260926.md`.
