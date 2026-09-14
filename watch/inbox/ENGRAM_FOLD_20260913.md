# ENGRAM FOLD — THE CHAIN IS ALREADY THE ENGRAM (2026-09-13)

**The ask:** DeepSeek uses engram-style memory — compress against templates, share between siblings, prefetch before the model asks. Can the fleet do this?

**The verdict (7/7 converged):** the chain already IS the engram. The engram is not a new system — it is a **pure function of the chain**: `engram(chain) → resident template layer`. The fleet doesn't need to build a memory system. It needs to build the VIEW that recognizes the chain already IS one.

## The architecture (7/7 converged on the same three tiers)

| Tier | What | Persistence | Size |
|---|---|---|---|
| **Chain** | The permanent engram — hash-chained leaves, the sole record | Frozen forever | 7,930 leaves, growing |
| **Engram layer** | Template-compressed claims derived from the chain | RAM-resident, rebuilt from chain | ~200 bytes per compressed claim |
| **Working set** | Active session context — spore + boot + current task | Volatile, dies with the seat | 3KB (the bobbin) |

## The key insight (7/7)

**~95% of every session context is identical to every other.** The parable, the 20 laws, the boot memory, the doctrine — all shared. The engram stores only the DELTA — what's new this session — and references the template for everything else. This drops session memory from ~100K tokens to ~3KB.

## The build (one week)

1. Define the engram leaf type: `{template_id, delta, verdict, payload_hash}` — a new leaf type on the chain
2. Build the compression function: takes full session context → template-compressed delta
3. Build the decompression: takes template_id + delta → full context restored
4. Wire into fanout.py: every wave lane reads from the engram layer instead of raw context
5. The bobbin (3KB warm-load) becomes the active tier of the engram — already designed

## The ponytail verdict

**Passes.** The engram SIMPLIFIES the system: fewer files (one chain instead of parallel stores), fewer lookups (template_id + delta instead of full context), fewer special cases (one compression function instead of per-organ memory). The net simplification is positive because it replaces N parallel memory systems with 1 chain + 1 compression function.

## The lessig verdict

**Passes.** The engram is stated as law: `engram = compress(chain, template)` — what it enforces (compression), what it preserves (hash integrity), what it loses (nothing — deltas are lossless against the template). The docs match the code because the engram IS the code.

## The falsifier

If the compressed sessions, when decompressed, fail to reproduce the original context at ≥95% fidelity, the engram compression is lossy and the design fails. Test: compress 10 sessions, decompress, diff, measure.
