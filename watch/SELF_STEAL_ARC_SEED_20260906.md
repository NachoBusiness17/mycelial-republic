# SELF-STEAL: THE ARC SEED — conversation as verkle object (Sep 6, 2026)
Operator: "how do i recreate the entire conversation arc in a single prompt that
would cover its caching... how is this like a multidimensional verkle object...
hidden stochastic spaces... selfsteal and make it better."

## THE STEAL — three owned facts, one object
1. **A conversation is a prefix chain priced by cache.** Every call re-feeds the
   entire prior arc as cache reads; only the new suffix pays full price. Receipt
   (this seat's own rollout, mag/arc_seed.py first run): cold 9.03% hit, warm
   98.21–99.98%, stable prefix 287,934 tok, 88.4% of ALL input = re-fed reads.
2. **The trajectory envelope is the node vector.** {input, tool_result, output,
   reasoning, step_hash, timing} — the trajectory-lens program already had the
   verkle shape; the transcript is the 1-D projection of an n-D object whose
   axes are (time, cost, cache-state, branch-depth, tool-surface, thinking).
3. **The hidden stochastic space = sibling leaves.** Every position carries a
   sampling distribution; the transcript is ONE root-to-leaf path. The unseen
   branches open only to probes — tesuji stones, salon forks, A/B arms. "The
   curiosity and the will to ask for directions" is literally the probe program.

## THE BUILD — mag/arc_seed.py (landed, dogfooded same hour)
Parses any rollout (model-io-sess_*.jsonl) and emits:
- **CACHE ANATOMY** — per-call hit curve + stable-prefix growth + refeed share.
  The description language for our own data dogfooding: our conversations ARE
  cache-economics documents (refeed_guard's 94% fleet-wide; this arc 88.4%).
- **ARC CHAIN** — verkle-style hash chain over turn envelopes, arc root
  committed (this session: eacb5b32e9ad5b9a). Provable arc identity without
  the full transcript — the knot doctrine, per-turn.
- **ARC SEED** — the single-prompt skeleton, three layers:
  L0 immutable system (deterministic, rides cache forever) · L1 the operator's
  forks verbatim (orders = branch points) · L2 committed-state delta (files,
  cards, knots — the durable memory OUTSIDE the context).
- Thinking banked per arc, sha-addressed (35,526 chars this arc).

## THE ISOMORPHISM (why this is already proven)
The boot prompt IS the arc seed: AGENTS.md + memory index + CONVO tail =
the single prompt that regenerates Sancho every morning. SPORE_SANCHO.md is
our production arc-seed for the seat itself. We have been compiling arcs all
along; the organ just makes the compilation measurable and per-session.

## FALSIFIER
Seed a FRESH session with the arc seed; ask it to state its next move before
reading anything. If its move matches the original arc's actual next move
(judged blind), the seed carries the load-bearing state. If not, L2 missed a
committed artifact — the seed names what to add. Pass bar: 2-of-3 seeds land
the next move. Run it on three closed sessions this week ($0, flash).
