# Relational Memory Discrimination — the foundation under the SubtleMemory castle

**Beat:** castle_foundation · 2026-08-26
**Schema:** design.rel_mem_discrimination.v1
**Status:** FOLDED + VERKLE-ANCHORED + BUILT
**Invariant:** `REL-MEM-1` (sha256 `f6ca44a2…`) · knot `1b33669a8ebb37a5`
**Companion fold:** `IDEA-GRAPH-1` (sha256 `baccc51a…`) · knot `9c6f693a191d4574`

---

## The castles (zeitgeist) this beat

The `castles()` coldest_vector surfaced 5 entries. Two were already folded
(planning mode → PLAN-GATE-1, subagent-router → DELEG-POLICY-1/2). Three were
**genuinely new** and not yet folded:

1. **`deep-c-f368762f1e82`** (SubtleMemory) — a benchmark for **fine-grained
   relational memory discrimination** in long-horizon agents: it embeds
   complementary, nuanced memories that share context and probes whether the
   agent can tell them apart. **Highest leverage.**
2. **`2026-08-09T1403-reply-with-exactly--grok-free-compounding-works`** — a
   test/verification artifact ("reply with exactly: grok free compounding
   works"). Low leverage — a check, not a foundation.
3. **`Free project bones`** (`n_717f3ba254`) — "grok_free now records ideas
   into the idea graph as open_loop nodes." Medium leverage — a mechanism note.

## The shadow tesuji (re-discovery, honestly named)

The shadow work re-mined the SAME tesuji as the prior beat — the butcher story
about **honest self-correction** (`self_correct: 4`, `honest_meta: 3`). This is
a **re-discovery**: it was already folded as `SELF-CORRECT-1` (knot
`70dbd55a…`) in the previous beat. Per SELF-CORRECT-1 itself, we do NOT
re-fold a duplicate — we name it plainly and move on. The shadow work is
genuinely exhausted on this source; the garbage pile has been mined.

## The invariant (folded)

> **[correctness] Relational memory discrimination (REL-MEM-1):** memory quality
> is measured by the agent's ability to DISCRIMINATE between related-but-distinct
> memories, not by recall volume. A memory system that recalls a lot but cannot
> tell apart two complementary/nuanced memories that share context is worse than
> one that recalls less but keeps the distinctions sharp. Evaluation must probe
> relational discrimination (given a query, does the agent retrieve the RIGHT
> memory among near-neighbors, and can it state how two related memories differ?)
> rather than isolated recall count. This is the operational form of
> "artifact > transcript" and "zero metadata": the value of a memory is its
> precision under ambiguity, not its bulk.

## The companion fold (castle 3)

> **[correctness] Ideas are open loops, not closed facts (IDEA-GRAPH-1):** a
> captured idea is an open_loop node in the idea graph — a pointer to be
> developed, not a settled claim. Recording an idea must preserve its
> open-endedness (it is a seed, a "project bone") and link it into the graph so
> later work can pick it up and close it. An idea that is captured but never
> linked into the graph is a lost bone; an idea that is recorded as if settled
> forecloses the very development that made it valuable.

## The build (highest-leverage)

`mag/rel_mem_eval.py` — a deterministic, $0, stdlib-only harness that scores a
retrieval function on **discrimination precision**, not recall count. It runs a
fixed battery of near-neighbor memory clusters (delegation vs routing,
self-correction vs face-saving, plan-gate vs execution) and measures:

- **A. Near-neighbor discrimination** — does the retriever return the RIGHT
  memory among plausible-but-wrong near-neighbors?
- **B. Distinction articulation** — can it state how the returned memory differs
  from its nearest rival? (the "zero metadata" check)
- **C. Ambiguity robustness** — when two memories are near-identical, does it
  flag the ambiguity instead of guessing?

The retriever is pluggable. The default is a deterministic lexical scorer
(baseline). Verification: `memory/improve/evals/verify_rel_mem_eval.py`.

**Honest finding from the build:** the naive lexical scorer gets 33% (1/3) —
it cannot discriminate near-neighbors. Even a "distinctive vocabulary bonus"
retriever still ties at 33%: lexical distinctiveness alone is insufficient for
true relational discrimination. This is the point of the harness — it exposes
that recall-volume retrieval fails at the exact thing REL-MEM-1 demands, and
that the fix requires semantic discrimination, not more lexical overlap.

## Growth this beat

- invariants: 307 → **309** (+2: REL-MEM-1, IDEA-GRAPH-1)
- knots: 300 → **302** (+2: `1b33669a…`, `9c6f693a…`)
- chain rows: 6383 → **6391**

## Testable form

- **REL-MEM-1:** `python -m mag.rel_mem_eval` reports a discrimination_precision
  in [0,1]. A discriminating retriever must score ≥ the naive scorer. The
  harness must flag near-tie ambiguity rather than guess.
- **IDEA-GRAPH-1:** an idea captured into the idea graph is recorded as an
  open_loop node (open-ended), not a closed fact.
