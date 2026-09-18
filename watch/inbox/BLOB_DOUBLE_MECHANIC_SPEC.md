# BLOB DOUBLE — engine v1.2 mechanic spec (2026-09-18)

*Operator: "maybe the blob doubling is a mechanic we can play with, sort of mapped
to dumb kubernetes."*

## The mechanic

When the player pushes a block, the block does NOT slide. Instead it DUPLICATES:
the original stays, and a copy appears in the target cell (if that cell is walkable
floor at the same height). Copies inherit no special properties — they are regular
blocks. The corridor can fill. The player must manage which copies to keep.

## Kubernetes mapping (the design lens)

| K8s | Blob Double |
|---|---|
| Pod | Block (the blob) |
| ReplicaSet scale | Push = spawn a copy |
| Node drain | Collapse cell burns the blob |
| Service healthy when enough replicas | Bridge opens when the plate has enough weight |
| CrashLoopBackOff | Block pushed into a corner is stuck forever |
| Orphan pod | Copy that drifted away from the corridor is useless |

## Engine changes needed (v1.2)

1. `loadLevel()`: add `st.blobMode = def.blobMode || false`
2. `step()` L3 push branch: if `blobMode` and target cell is walkable at same height,
   spawn a NEW block at the push target instead of moving the old one. Original stays.
3. Win condition: unchanged (exit still wins). But the puzzle design must ensure the
   player doesn't fill the corridor with useless copies before reaching the plate.

## Level design constraint

Blob-doubling levels must be designed so the player pushes the block 2-3 times maximum.
Each push doubles the blob count. After 3 pushes there are 8 blobs. The corridor must
have collapse cells or pits that the player can use to REMOVE unwanted blobs — otherwise
the room fills and becomes unsolvable. The interesting puzzle is: which copies to keep,
which to burn, and in what order.

## Falsifier

A blob-double level is VALID iff: BFS finds a solution where the number of live blobs
never exceeds the corridor capacity (no cell has more than 1 blob) and the solution
path passes through at least one plate held by a blob copy. If the gate can solve it
without ever touching the blobs, the level is a push-decorated corridor, not a
blob-doubling puzzle.
