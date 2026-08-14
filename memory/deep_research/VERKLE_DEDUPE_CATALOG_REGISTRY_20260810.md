# Deep Research — Verkle-encoding the software catalog (dedupe + catalog registry)
2026-08-10 · method: internal-corpus synthesis (ghost, no external web, no PowerShell)

## Question
How do we verkle-encode the software catalog (skills / agents / memories / modules / surfaces) so it
dedupes by content-address and compresses to one verifiable Merkle–Verkle root? Design the
catalog-registry module.

## What the internal corpus already establishes (grounded, not hand-waving)
- **Verkle knot = content-addressed commit** (`mag/verkle_knot.py`): a leaf's `leaf_hash` IS its address
  (sha256 content-addressed); filename = address; `verkle_tip.json` = Merkle–Verkle root over ALL leaf
  hashes; change one leaf → root changes. Immutable. (verkle-knot-real-structure)
- **The substrate is already one system**: stateless versioning (local) == verkle lattice (global);
  hermetic_id ~ leaf_hash; commit_stateless ~ one knot; checkpoint ~ chain tip. NO second system.
  (verkle-dirac-knot-topology)
- **Memweave / memlang token already carries a 32B verkle anchor**; memweave = structures-not-prose,
  content-addressed, resolves against shared RIB. (memweave-mindweave-tested)
- **Verkle bus = CAS, Event Sourcing**: accept_knot writes a self-contained knot; parent_verkle_root
  ties back; derived state = replay; bus syncs all agents. (verkle-bus-research-project)
- **Ghost = the local harness/touchpoint**: reads the deterministic surfaces registry (~30 surfaces) as
  ground truth of what exists; never a hand-written tool list. (ghost-harness-touchpoint)
- **10 silo clusters climb uncoordinated** (steal/acquire, research/idea, gap, audit, rightsize/quantize,
  gates, cost/economy, loop trails, afk self-advance, narrative/biography). (ghost-surfaces-audit)

## External grounding (steal, mechanism-only)
- **mem0 hash-dedup**: exact dupes collapsed by content hash (md5) on write, skip-if-seen.
- **mem0 near-dup**: same category + >60% significant-noun overlap → merge; both skip pinned.
- Verkle content-address subsumes the exact-hash tier (stronger: collision-resistant, tree-anchored);
  noun-overlap stays the near-dup fallback for reworded-but-same items.

## Design principle (the "quantization")
Catalog growth is a QUANTIZATION problem: encode every item as a content-addressed knot so
duplicates share an address and compress away; the whole catalog is one Merkle–Verkle tree whose root
is the honest, compact, replayable count. Deterministic registry = ground truth; stochastic (LLM)
output is honed against it, never trusted over it.

## Proposed module: `mag/catalog_registry.py` (schema catalog_registry.v1, deterministic $0)
**Invariants (contract-only):**
1. `catalog:item-addressed-by-content` — every skill/agent/memory/module/surface has a
   `catalog_id = sha256(canonical_content)`. Same content → same address → COLLAPSE.
2. `catalog:anchor-first` — before adding, resolve the item's memlang/verkle anchor; on collision
   merge into the existing knot, never create a sibling silo.
3. `catalog:near-dup-merge` — same category + >60% significant-noun overlap → merge (mem0 rule),
   skip pinned; reworded-but-same collapses.
4. `catalog:root-is-truth` — expose the Merkle–Verkle root over all catalog knots as the honest count;
   stochastic output is a projection, never authoritative.
5. `catalog:replayable` — the chain/ledger is the record; derived state = replay (Event Sourcing).

**Functions:**
- `register(item, category)` — compute catalog_id → anchor check → collapse | merge | add knot.
- `catalog()` — list with addresses; `root()` — the Merkle–Verkle root (honest count).
- `near_dupes(category)` — noun-overlap pairs for review/merge.
- `dedupe()` — mem0-dream-style pass: merge near-dup, prune stale, collapse exact.
- `register_as_surface()` — expose the catalog via `ghost.sense_surfaces()` so ghost sees it.

**Wiring (self-steal, no rebuild):** reuse `verkle_knot.append_verkle_knot` (leaf_hash/merkle/root),
`memlang.resolve` (32B anchor), `ghost.sense_surfaces` (surface), and the existing rightsize/
quantize workers instead of adding new machinery.

## Honest caveats
- Near-dup thresholds are heuristics — a wrong merge collapses distinct items. Keep pinned/identity
  exempt; show a diff before destructive merge (mem0 dream does diff-first).
- Do NOT claim this is a new primitive — it is a sharp productization of content-addressing we already
  run (CAS, verkle knots, memweave), plus the mem0 near-dup rule.

## Next
Build `mag/catalog_registry.py` against these invariants, register its surface, and let ghost's
dedupe directive execute it by default on new items.
