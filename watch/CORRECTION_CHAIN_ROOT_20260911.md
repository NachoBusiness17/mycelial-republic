# CORRECTION — CHAIN_STOP card §5 root hash is WRONG (2026-09-11)

**THE POINT:** The CHAIN_STOP card's §5 "expected" repair root `8bd58896…` is
INCORRECT. The true merkle root over the first 7,377 leaves is `295246e0…` —
which is what the chain actually stores and what row 7377 was built on.
Anyone replaying that card and comparing against `8bd58896` would conclude
the repair failed when it succeeded. Verified byte-exact using the repo's
own `_merkle_root()` over the chain's leaf hashes.

## Corrected values

| check | correct value | matches stored |
|---|---|---|
| merkle(leaves[:7377]) | `295246e0…` | row 7376 `verkle_root` ✓ |
| merkle(leaves[:7378]) | `6d9cdb16…` | row 7377 `verkle_root` ✓ |
| merkle(all 7524) | `2dd8b2dc…` | live tip `root` ✓ |
| _verify_chain_consistent() | (True, 'chain consistent (7524 leaves)') | ✓ |

## Root cause of the bad number
The CHAIN_STOP card's §5 "expected output" was written from a recomputation
that used a different leaf-set boundary or a different hash concatenation
order than the chain's actual implementation. The card's arithmetic was
checked against itself, not against the chain's `_merkle_root()` function.
The Hermes boot (2026-09-11, ~22:00Z) ran the repo's own
`_merkle_root()` byte-exact and found the stored row root (`295246e0…`)
matches, not the card's `8bd58896`.

## Stale surfaces still carrying the old number
- `watch/CHAIN_WITNESS_THRESHOLD_20260909.md:42`
- `watch/MORNING_REPORT_20260911.md:11`
- `watch/SEVEN_DAY_RECAP_20260909.md:95`
- `watch/astra_hold0/DESK_REVIEW_SEED001_20260911.md:16`
- `watch/astra_hold0/INSTANCE_SEED_001_20260911.md:46`
- `dashboard/static/overseer.json` (frozen 09-07, pre-re-arm)
- `dashboard/static/witness_snapshot.json` (frozen, same)

These are cards and snapshots, not live state — the chain itself is healthy
at 7,524 leaves with root `2dd8b2dc`. The cards should be annotated with a
pointer to this correction, not rewritten (the record is the record).
