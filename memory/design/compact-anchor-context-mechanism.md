# Compact-Anchor Context Mechanism: Full Design

**Task:** `redundant_process_elimination`
**Schema:** design.compact_anchor_context.v1
**Date:** 2026-08-26
**Status:** DESIGN (not yet implemented)
**Purpose:** eliminate the redundant process of re-prefilling unchanged context prefixes on every
provider call, by anchoring the stable prefix to a compact token that the provider's KV cache can
reuse bit-for-bit.

---

## 1. What the anchor actually is (and the invariant that makes it work)

Provider-side KV caches (vLLM/SGLang block tables, Anthropic/OpenAI prompt caches) key on **exact
token sequences**. A cache hit happens only when the *prefix* of the current request is byte-for-byte
identical to a prefix that was already pre-filled and cached. Any edit — even one token inserted
mid-prefix — invalidates everything after it, forcing a full re-prefill of the tail.

The **compact-anchor** is a single, stable, content-addressed token that stands in for a large,
slowly-changing context block. It is the *identity* of that block, not its content. The invariant
that makes it work:

> **The anchor is a pure function of the block's canonical content.** `anchor = H(block)` where `H`
> is a deterministic content hash (BLAKE3-256 / verkle knot hash). Two calls that reference the same
> anchor are guaranteed to reference the same bytes, so the provider can cache the *resolved* block
> once and reuse it across every call that carries the anchor — without re-sending or re-prefilling
> the block.

This is the same content-addressing invariant the verkle chain already enforces (a knot is addressed
by its content hash; re-running a transform on the same inputs produces the same hash). The
compact-anchor extends that invariant from *storage* to *transport*: the anchor is what travels in
the prompt, and the block it names is what the KV cache holds.

### Why this eliminates a redundant process

Without the anchor, every turn re-sends the full stable prefix (system prompt, constitution, doctrine
RIBs, world state, session memory). The provider re-prefills those tokens every time — a redundant
process that costs latency and money even when the bytes never changed.

With the anchor, the stable prefix is sent **once**, resolved, and cached. Subsequent turns send only
the anchor token plus the *delta* (the new suffix). The provider's KV cache serves the prefix from
its block table; only the delta is newly pre-filled. The redundant re-prefill process is eliminated.

---

## 2. The mechanism, end to end

```
   STABLE BLOCK (system prompt, constitution, doctrine RIBs, world state)
        |  canonicalize (deterministic serialization)
        v
   anchor = H(block)          -- content-addressed identity (BLAKE3-256 / verkle knot)
        |
        v
   PROMPT = [anchor-token] + [delta suffix]        -- only the delta is new
        |
        v
   PROVIDER KV CACHE
        |- prefix block already cached under anchor  -> HIT: serve from block table, $0 re-prefill
        |- prefix block not cached (cold / evicted)  -> MISS: resolve block, prefill once, cache
        |
        v
   OUTPUT (delta's completion)  -- folded back as a new knot, next anchor covers it
```

### 2.1 The anchor token format

Reuse the memlang token shape (opcode + content hash) so the anchor is a first-class citizen of the
existing grammar, not a new silo:

```
MEM1  <opcode>  <32-byte verkle/anchor hash>
```

- `opcode` names the block *kind* (e.g. `SYS` system prompt, `CON` constitution, `DOC` doctrine RIB,
  `WLD` world state, `MEM` session memory).
- The 32-byte hash is the content-addressed identity of the block's canonical bytes.
- Total token ~69 bytes — a compact stand-in for a block that may be tens of thousands of tokens.

### 2.2 Resolution (the resolver)

A deterministic resolver maps `anchor -> canonical block bytes`:

- **Local fast-path:** the block is in the in-memory corpus (ram_cache). Resolve in microseconds, $0.
- **Disk fallback:** the block is a verkle knot / RIB / research pack on disk. Load + canonicalize.
- **Miss:** the anchor names a block that no longer exists or was never materialized -> treat as a
  cache miss, rebuild the block, re-anchor.

The resolver is a **pure function** (same anchor -> same bytes), preserving the round-trip/stateless
invariant from the RIB protocol. It never mutates; it only resolves.

### 2.3 Staleness (the failure mode the RAM-cache RIB taught us)

The RAM-cache RIB (`RIB_RAM_CACHE_STALE_SNAPSHOT`) proved the danger: a cached snapshot silently goes
stale and the system reasons over an old corpus. The compact-anchor must not repeat that.

- The anchor is content-addressed, so a *changed* block produces a *different* anchor. Staleness is
  impossible by construction: if the block's bytes change, the anchor changes, and the old cached
  prefix is simply not referenced anymore.
- The resolver must **auto-invalidate** its local block cache via an mtime fingerprint (the same
  fix shipped for ram_cache): if disk is newer than the cached block, reload before resolving.
- The anchor is never trusted as truth — it is a *pointer*. The block it names is re-verified against
  its hash on every resolve (cheap, deterministic).

### 2.4 The delta (what actually changes)

The compact-anchor only pays off if the *stable* prefix is genuinely stable. The design therefore
separates the prompt into:

1. **Stable prefix** — system prompt, constitution, doctrine RIBs, world state, session memory.
   Anchored. Sent once, cached, reused.
2. **Delta suffix** — the current turn's steer, tool results, new observations. Sent fresh every turn.

The split is deterministic: a block is "stable" if its content hash is unchanged since the last
anchor; otherwise it is re-anchored (new hash) and the delta absorbs the change.

---

## 3. The invariant, stated precisely

> **Anchor-consistency invariant:** for every block `B` and every anchor `a` in the prompt,
> `resolve(a) == canonical(B)` and `a == H(canonical(B))`. Equivalently: the anchor is a bijective
> content-addressed pointer — `a` names exactly one block, and that block's bytes are exactly what
> `H` committed to. No two distinct blocks share an anchor; no anchor resolves to two different
> byte-sequences.

This is a **correctness invariant** (the cache is an optimization, never a source of truth — the
anchor must always resolve to the exact committed bytes). It is enforced by:

- **Deterministic canonicalization** — same logical block -> same bytes -> same hash (contract-tested).
- **Hash verification on resolve** — the resolver recomputes `H(block)` and rejects a mismatch.
- **Content-addressed identity** — the anchor IS the hash; there is no separate mutable id to drift.

---

## 4. Integration with existing machinery (no new silo)

The compact-anchor composes three already-built pieces:

| Piece | Role in the mechanism | Existing |
|---|---|---|
| **verkle chain** | content-addressed identity of blocks (knot hash = anchor) | built, proven |
| **memlang tokens** | the anchor token format (opcode + 32B hash) | built, proven |
| **ram_cache** | local fast-path resolution + mtime auto-invalidation | built, proven |
| **context_pack / party_subchain** | the stable prefix that gets anchored | built |

The mechanism adds **one new seam**: the resolver (`anchor -> bytes`) and the prompt splitter
(`stable prefix vs delta`). Everything else reuses what exists. This honors the RIB doctrine:
"reuse memlang (tokens), verkle (anchors), guard_registry (enforcement) — no new silo."

### 4.1 Where the seam lives

- **Resolver** — a pure module `mag/anchor_resolver.py`: `resolve(anchor) -> bytes`, `anchor(block) -> hash`,
  `split_prompt(full) -> (stable_prefix, delta)`. Deterministic, contract-tested, $0.
- **Prompt assembly** — `context_pack.py` emits the anchor token for the stable prefix instead of the
  full prefix bytes, and appends the delta. The provider sees `[anchor][delta]`.
- **Fold-back** — the delta's completion is folded as a new knot; the next turn's anchor covers the
  grown stable prefix (turtles all the way down).

### 4.2 Provider reality check (honest)

The compact-anchor's payoff depends on the provider actually caching the *resolved* prefix. This is
true for **self-hosted** vLLM/SGLang (we control the block table and can pin the prefix). For
**remote** Anthropic/OpenAI prompt caches, the cache keys on the exact token prefix of the *sent*
request — so the anchor token must be *expanded* to the full block bytes before sending, and the
cache hit then depends on the provider's own prefix-cache policy. Two modes:

- **Local mode (self-hosted):** send the anchor token; the resolver on the serving side expands it.
  Maximal savings (the block is never re-sent).
- **Remote mode (API):** expand the anchor to full bytes client-side, send the full prefix once, and
  rely on the provider's prefix cache for subsequent identical prefixes. Savings = the provider's
  cache-hit discount + reduced latency, not zero re-send.

The design must support both; the honest claim is that **local mode eliminates the redundant
process**, remote mode *reduces* it to the provider's cache policy.

---

## 5. Guardrails

- **Anchor is a pointer, never truth.** The block it names is re-verified against its hash on every
  resolve. A mismatch is a hard error, not a silent fallback.
- **Deterministic core.** Canonicalization, hashing, resolution, and prompt-splitting are all pure
  functions ($0, no LLM). The LLM may draft, never execute, the invariant.
- **T0/T1 never remote.** Anchored blocks that are T0/T1 (constitution, doctrine, session memory)
  never leave the machine in remote mode; only the delta travels.
- **No new state.** The anchor is derived from content; there is no separate mutable registry to
  drift. The only cache is the resolver's block cache, which auto-invalidates via mtime.
- **Idempotent.** Re-running the same transform on the same content produces the same anchor and the
  same delta — no duplication, no drift (the round-trip/stateless invariant).

---

## 6. Acceptance criteria (how to verify)

1. **Anchor determinism:** `anchor(block)` returns the same hash for the same canonical bytes across
   processes and restarts.
2. **Resolve round-trip:** `resolve(anchor(block)) == canonical(block)` for every block kind.
3. **Staleness:** change a block's bytes -> `anchor(block)` changes -> the old prefix is no longer
   referenced (no stale reasoning).
4. **Delta split:** `split_prompt(full)` returns a stable prefix whose hash is unchanged across turns
   when nothing changed, and a delta that absorbs the new turn's content.
5. **Local-mode savings:** with a self-hosted vLLM/SGLang, two turns sharing a stable prefix show a
   KV-cache hit on the prefix (measured via block-table hit rate) and no re-prefill of the prefix.
6. **Remote-mode correctness:** with an API provider, the expanded prefix is byte-identical across
   turns so the provider's prefix cache can hit (measured via reported cache-hit tokens).

---

## 7. Honest boundaries

- **Not a capability cheat.** The compact-anchor does not make the model smarter; it makes the same
  reasoning cheaper and faster by not re-doing unchanged work. It is a cost/latency optimization.
- **Payoff is workload-dependent.** It pays off when the stable prefix is large and the delta is
  small (long sessions, heavy doctrine). It is neutral-to-negative for short, stateless calls where
  the prefix is tiny.
- **Remote-mode savings are bounded by the provider's cache policy.** We cannot force a remote cache
  hit; we can only make the prefix stable enough that the provider *can* hit it.
- **The delta is the real work.** Anchoring the stable prefix does not reduce the tokens the model
  must generate; it reduces the tokens it must re-read. Generation cost is unchanged.

---

## 8. Next steps (ranked)

**P0 — build the seam:**
- `mag/anchor_resolver.py`: `anchor()`, `resolve()`, `split_prompt()` — pure, contract-tested.
- Wire `context_pack.py` to emit the anchor token for the stable prefix (local mode first).

**P1 — measure the payoff:**
- Local-mode KV-cache hit-rate test on self-hosted vLLM/SGLang (acceptance #5).
- Remote-mode cache-hit-token measurement on an API provider (acceptance #6).

**P2 — fold into the loop:**
- Auto-re-anchor when a stable block's hash changes (staleness handling).
- Emit the anchor/delta split into the cost/cache map so the savings are visible in telemetry.
