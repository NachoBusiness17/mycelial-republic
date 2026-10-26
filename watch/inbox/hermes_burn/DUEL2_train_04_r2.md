# DUEL2_train_04_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Finding: the equivocation gate has no stated atomic, total admission rule

## 0. Citation and measurement conditions

- The evidence block has no line numbers, so every `file:line` is **UNVERIFIED**. Each claim below cites the section heading plus quoted bytes instead.
- The file is `docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.md`, sha256 `fc3d0686...8ca1` as given.
- I rely on no measurement. All reasoning is over document text.
- `mag/anchor_registry.py` is not in evidence, so anything about the real implementation is **UNPROVEN**.

## 1. The forgotten safeguard

**The spec never states that the equivocation check and the append happen in one `verkle_lock` critical section, evaluated over every row and kind for that `v1_leaf_hash`.**

Three quoted facts, taken together, leave the gap:

| Where | Quoted bytes | What it fixes | What it leaves open |
|---|---|---|---|
| Invariant 1 | `integrity = tail-append under verkle_lock` | The lock covers the **append**. | Says nothing about the read that precedes it. |
| Module paragraph | `jsonl append under verkle_lock, the four verbs, invariant checks pure/deterministic` | Checks are pure functions. | A pure check is a function of bytes read earlier. Nothing ties it to the lock hold. |
| Invariant 2 | `at most one row may be in status: claimed at a time` | Gates only `claimed` rows. | Does not mention `committed` rows. Does not mention `gap` rows. |

The workflow section also says gap rows are `committed immediately`. Those rows never enter `claimed`, so the gate never looks at them.

## 2. Attack/accident path A: two seats race (no malice needed)

Setup: v1 row `H`. Seats A and B both run `claim --v1 H --claim repair` with different `--derive-spec` values.

1. **A reads the registry and finds no live claim for `H`.**
   - Hides behind invariant 2. Nothing is refused because, at read time, A is first.
2. **B reads the same bytes and reaches the same verdict.**
   - Same cover. The checks are `pure/deterministic`, so equal input gives an equal "admit".
3. **A takes `verkle_lock`, appends `status: claimed`, and releases.**
   - Hides behind invariant 1. The lock was held for the append, so the file is well-formed.
4. **B takes `verkle_lock` and appends a second `status: claimed` row for `H`.**
   - Also hides behind invariant 1. The append is serialized and valid JSONL.
   - Nothing in the text requires B to re-check inside the lock.
5. **The compiler runs.** The workflow says `compile -> ... reads ONLY claimed rows`.
   - It regenerates two surrogates and writes two v2 leaves with MEM1 anchors to `H`.
6. **Invariant 3 passes for both leaves.** Its test is `unless a claimed row exists that predates the leaf's ts`.
   - That test is existential. It is not bound to the leaf's author or to one specific claim.
7. **Both commit.** Invariant 4 demands only that `v2_leaf_hash` and `proof_sha256` be non-null.
   - `verify` re-derives each row against its own proof and sees no mismatch, so there is no alarm.
8. **`audit` reports an invariant-2 violation, but the spec gives that report no consequence.**
   - Invariant 1 forbids removing the row.
   - No tie-break rule exists.
   - Two valid, conflicting v2 testimonies for one frozen v1 row now exist.
   - This is the exact failure the spec's own "Why a registry exists" section says the registry exists to stop: `two seats could append competing repairs for the same v1 row (equivocation)`.

## 3. Path B: same hole, no timing needed (the gate is not total)

- **Reclaim after commit.**
  - A's row goes `claimed → committed`. The gate is keyed on `status: claimed`, so B's fresh `claim: repair` for `H` meets no live claim.
  - B claims, compiles, and commits a second v2 leaf. Invariant 3 is satisfied by B's own new `claimed` row.
- **Gap bypass.**
  - A holds a live repair claim. B appends `claim: "gap"` with status `committed`, which the workflow allows "immediately".
  - Invariant 2 does not fire, because B's row is not `claimed`.
  - Invariant 6 then makes B's gap row permanent: `A gap committed row never transitions`.
  - A later commits the repair, leaving a committed repair and an irrevocable gap on the same row.
- **Non-owner transition.**
  - Invariant 4 never says the committing row must come from the claimant.
  - Any seat can append `committed` against A's claim.
- **Literal-reading ambiguity.**
  - Rows are never edited (invariant 1), so A's `claimed` row stays "in status claimed" forever.
  - Read literally, no second claim is ever admitted, even after `refuted
