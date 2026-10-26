# CONTEXT WINDOW HOP — RIGHTSIZING STEAL (2026-08-10)

**Question:** what can we learn from long-running AI processes, and how can hopping our calls
through new windows (to exploit context length) enhance our rightsizing value?

## Grounding (external, cited)
- **Anthropic, "Effective context engineering for AI agents"** (2025-09-29):
  - *Context rot*: as tokens in the window grow, recall degrades — context is a finite
    "attention budget" with diminishing marginal returns, across ALL models. Waiting for bigger
    windows is not the fix.
  - Three levers for long-horizon tasks: **compaction** (summarize a near-full window and
    reinitiate a NEW window with the summary), **structured note-taking / agentic memory**
    (persist notes OUTSIDE the window, pull back later), **sub-agent architectures** (each
    subagent runs a clean window and returns only a ~1-2k-token distilled summary).
  - Just-in-time context retrieval: keep lightweight identifiers, load only what's needed.
- **LangGraph persistence docs**: *checkpointer* = short-term, thread-scoped state snapshots
  (fault tolerance, resume, time-travel); *store* = long-term, cross-thread memory. Both needed.
  Lesson: persist state OUTSIDE the window so a hop is resumable.

## Why our system is ALREADY a window-hopping machine
- `ghost_auto` / `afk_cadence`: bounded stateless DeepSeek agents (each a fresh window).
- `whisper_route`: deniable swarm — front -> riddler -> memlang(opcode+anchor) -> corpus -> sync.
  Memlang carries ONLY an anchor hash, never the tier/state → external memory, deniable.
- `verkle knots` (4,601 leaves) + `verkle_chain`: content-addressed external memory / chain.
- `RIB` memory handoffs: frozen handoff files written by one agent, read by the next.
- `cache_router`: stable prefix + append -> DeepSeek cache-HIT economics (50x).
- `one_sizer`: cheapest-capable tier per (domain, shape, skill), learned across domains.

## The synthesis: window-hopping is a RIGHTSIZING lever, not just a cost lever
Pricing model (`mag/window_hop.py`, real deepseek-v4-flash rates: hit $0.0028/M, miss $0.14/M, out $0.28/M):
- Hopped 20-hop task: **$0.02997**, input-hit-ratio 0.39, **max window 13.5K tokens**.
- Naive one growing context: **$0.03367**, **max window 192.5K tokens** (overflows typical 128K + rots).

So the honest numbers:
1. **$ savings is real but modest (~1.1-1.2x)** — because the fresh delta per hop still bills at miss.
2. **The bounded window is the big win (~14x)** — max hop window 13.5K vs naive 192K. This is the
   rightsizing value: length no longer forces a bigger tier/window. `one_sizer` can hold the
   cheapest-capable tier for arbitrarily-long tasks because no window ever grows large.
3. **Quality** — bounded high-signal windows dodge context rot (better recall/reasoning per hop).

## Invariants folded (organ: economics / loop)
1. **context-rot-is-real** — treat context as a finite attention budget; never grow one window unbounded.
2. **hop-not-grow** — long tasks = sequence of bounded windows, passing only distilled state forward.
3. **externalize-memory** — persist notes outside the window (knots/RIB/corpus/sync); a hop must be resumable.
4. **stable-prefix-for-cache** — keep system+invariant+anchor byte-stable so the reused prefix bills at hit.
5. **length≠tier** — bounded windows let one_sizer keep the cheapest tier regardless of total task length.
6. **distill-don't-dump** — each hop returns a ~1-2k-token note, not raw tool output (sub-agent pattern).

## Build
- `mag/window_hop.py` (schema window_hop.v1) — deterministic $0 pricing of hop-vs-naive under real rates;
  surfaces savings_x + bounded window so the cadence can decide when to hop.
- This sharpens the 24/7 test: add a window-rot check (max window stays << limit) + hop-metering to dogfood.
