# Reasoning Ledger — implementation plan by ox-alpha (steal #2, 2026-08-22)

Free frontier seat (stealth/ox-alpha), cost $0. Build plan for the reasoning-continuation ledger
on our verkle-commit + cache-mined shared-prefix seam.

## 3 design invariants (buy dollar-zero)
1. **Append-only records** -> the rendered prompt is *prefix-stable* byte-for-byte across turns.
   Provider cache hits cover everything except the appended tail.
2. **Per-task verkle trie** -> the whole ledger collapses to a 32-byte root carried in the tail.
   Verifiers audit any record with an O(log n) multiproof, not O(n) replay.
3. **COMPACT rollups + <=512-token CONT block** -> prefix growth bounded (amortized single-miss
   rewrites) and the mutable tail hard-capped, so full-price tokens/turn are constant.

KEY CACHE TRICK: the verkle root must NEVER appear before the tail — it lives inside the CONT
block (rewritten each turn anyway).

## Smallest buildable slice
One task, one writer + one verifier, N turns. Record types: THOUGHT, DECISION, COMPACT, CONT.
Cut from v0: ARTIFACT records, cross-task tries, async compaction, cross-task proof aggregation.

## Data model (canonical deterministic CBOR; sorted keys, fixed-width ints)
```
Record { v:1, seq:u64, type: THOUGHT|DECISION|COMPACT|CONT, ts:u64 (tail only, never frozen),
         parent_root:[u8;32], payload:bytes }
key = blake3("ox-ledger/v1" || task_id || seq)[..32]   # hash-spread stems -> O(1) new-stem/append
```
COMPACT payload: { supersedes:[a,b], summary:<=1024tok, digest:blake3(concat(rec_a..rec_b)),
                   multiproof }  (v0: digest-only, proof in phase 3).
CONT payload: goal, state, open_questions[], next_action, root@seq, seq — token-counted at write,
hard-reject >512.

## Prompt layout (the seam wiring)
```
R0 [SYSTEM+TOOLS+SCHEMA]   frozen forever
R1 [TASK HEADER]           frozen at task start
R2 [LEDGER TAIL records]   append-only since last compaction
R3 [CONT BLOCK @t + root@t] rewritten each turn, <=512 tok, ALWAYS LAST
```
- Turn t+1: R0-R2 byte-identical -> cache hit; only rec_{t+1} + new CONT full-price.
- Compaction: when |R2| > B (start B=4096 tok), emit COMPACT for [c..t], rewrite prefix once.
  One full-price miss per ~B/avg_rec turns, amortized.
- Cross-agent: same R0-R2 head shared across the swarm -> mined prefix shared across agents.
- Idempotency: append seq=head+1, CAS on head; retries reuse seq -> identical bytes -> cache-safe.

## File layout (Rust; Python port trivial)
```
ledger/
  Cargo.toml
  src/ record.rs trie.rs ledger.rs rollup.rs cont.rs prompt.rs store.rs verify.rs
  tests/ test_append_root_chain.rs test_prompt_byte_stability.rs
         test_compact_amortization.rs test_cache_hit_ratio.rs
  bin/  ledgerd.rs   # CLI: append / head / prove / compact / emit-prompt
```

## Build order
- Phase 0 (day 1): record.rs + store.rs (JSONL append) + trie wrapper insert/root. Test: append 100
  records, root chain verifies.
- Phase 1 (day 1-2): cont.rs token-budget enforce + prompt.rs frozen-prefix byte test.
- Phase 2 (day 2-3): rollup.rs minimal COMPACT (summary+digest) + compaction trigger + amortization test.
- Phase 3 (day 3-5): verify.rs + multiproof for COMPACT ranges; emit-prompt endpoint; cache-hit counter.
- Phase 4 (optional): cross-agent shared-prefix mining; measure cross-turn + cross-agent hit ratio.

## Acceptance criteria
- byte-stability test green (prefix identical turn-over-turn)
- root chain verifies; tampering one record breaks verify
- per-turn uncached tokens <= 512 + |rec| + slack; measured cache hit >= 95% after turn 2
- compaction every B tokens; amortized overhead < 10% of naive full-replay

## Pitfalls
- Non-deterministic serialization breaks cache (canonicalize: no map-iteration order, fixed float
  format, no timestamps in R0/R1).
- Provider cache eviction (TTL ~ minutes) -> keep turns tight or re-mine.
- Verkle proof size fine: O(log n) with multiproof amortization.

## Dollar-zero math
per-turn marginal full-price tokens = new record + CONT (<=512) ~ constant, independent of history
length; everything else cache-priced. If provider cache is free, marginal cost is literally $0
except the tail. Verifiers get root + multiproofs only -> their prompt is tiny.
