# Reasoning-Continuation Ledger — design by ox-alpha (steal #2, 2026-08-22)

Captured from the free frontier reasoning seat (stealth/ox-alpha), cost $0. This is the concrete
design for carry-a-frontier-seat's-reasoning-across-turns (steal #2), matching our deterministic
verkle-committed architecture.

## Design constraints (what drives every choice)
1. **Determinism**: no wall-clock fields; all ordering is logical (`seq`, `turn`). Canonical
   serialization: fixed field order, big-endian ints, sorted keys, no floats.
2. **Append-only**: immutable records; corrections are new `INVALIDATE` records pointing backward,
   never edits.
3. **Dollar-zero**: the cost vector is *tokens carried across turns*. Hard cap per turn, independent
   of history length. Storage holds only hashes on the committed path; payloads are off-ledger refs.

## Ledger schema (append-only, task_id-keyed)
One Verkle trie per `(task_id)`, per-seat subpaths. Record:
```
v              : u8        // schema version = 1
task_id        : bytes32   // H("oxa/task/v1" || canonical_task_descriptor)
seat_id        : bytes32   // frontier seat id
seq            : u64       // monotone per (task_id, seat_id), starts 0
parent_seq     : u64       // seq this entry continues from -> fork detection
turn           : u64       // logical turn counter
kind           : enum      // REASONING_DELTA | DECISION | COMPACT | CONTINUATION_SEAL | INVALIDATE
folded         : bool      // true once consumed by a COMPACT rollup
payload_hash   : bytes32   // H(canonical(payload))
payload_ref    : {scheme, loc}  // verkle path or external blob ref; empty => inline
commit_root    : bytes32   // verkle root AFTER inserting this record
prev_rec_hash  : bytes32   // H(prev_record_bytes || payload_hash)
sig            : bytes64   // seat signature over canonical(record minus sig)
```
Verkle key: `key(task_id, seat_id, seq) = H("oxa/ledger/v1" || task_id || seat_id || be_u64(seq))`.
Root recomputed each turn; proofs are small (~32 bytes per sibling group).

## Dollar-zero compression rule
- Per-turn **continuation block** has a hard token budget (e.g. ≤512 tokens).
- Anything beyond gets compressed into a fixed-size digest + pointer to the verkle proof, retrieved
  on demand.
- Old reasoning is never re-shipped in full; only its hash commitment rides along.
- `COMPACT` rollup records squash consumed entries into fixed-size summaries.

## Continuation block (seeds the next turn)
Carry forward ONLY: (a) the invariant goal, (b) committed decisions as facts, (c) open questions.
Drop raw transcripts. Block format: `{next_action, assumptions[], unresolved[], goal, facts[]}` —
becomes the seed of the next turn's prompt. Ledger beats the model on conflict (deterministic
sovereignty).

## Standing
This is steal #2 realized. Merge with the seat-contract (handoff/OX_SEAT_AND_SEAT_CONTRACT) + the
swarm's deeper research when it files back. Reuse our verkle-commit + cache-mined prefix seam to
implement it.
