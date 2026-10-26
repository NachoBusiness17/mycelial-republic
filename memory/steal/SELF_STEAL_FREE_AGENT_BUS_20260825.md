# SELF-STEAL — the free agent bus was already law (2026-08-25)

**Commitment:** `self-steal-free-agent-bus-001`
**Operator:** "perfect, so please use it [self steal] on this task" (the free agent bus vision).
**Method:** read OUR OWN corpus for bus-relevant laws before building anything new.

## What the self-steal found — we already proved this

### 1. The bus thesis = the shared-prefix-engine law (08-12, on DeepSeek's real bill)
"Scaling implication — additional swarms are cheaper on the warm shared prefix": the marginal
cost of a NEW worker ~= its cold input; a worker mounting the SAME doctrine rides the warm
prefix almost entirely on cache-hit. "More workers x same warm prefix = near-linear work at
sub-linear cost." Bill proof: miss-share 44% -> 17%. Design: rib_bus.inject_for mounts the
shared prefix for every worker.
=> The free agent bus is THIS LAW applied to a lane where the prefix AND output are free. We
didn't invent a new economics; we found the free implementation of the economics we already
measured. "As above, so below": the holon bus was already the design in 08-12.

### 2. The bus must dedupe BEFORE enqueue (08-15, the 958->0 queue lesson)
The "backlog" was a dedupe bug: 958 queued -> 123 unique groups, 835 near-duplicates, ONE task
copied 522 times. Laws: (a) "audit-dedupe-cull beats execute"; (b) dedupe by content-anchor
BEFORE writing (route_novel's dedupe is the model); (c) a novel orphan can flood the queue if
the enqueue path doesn't dedupe.
=> A bus with thousands of tasks MUST enforce content-anchor dedupe at the mouth, or the bus
floods itself with 500 copies of one task. The swarm_surface.route_novel primitive already does
this — it's the bus admission on the TASK side (the 1302/1305 codes are admission on the LANE
side; both must gate).

### 3. Capacity is flow, and we've measured flow before (08-12, $0.50/hr cap)
Real bill: ~$0.0012/req warm prefix; 333-417 req/hr at a $0.50 cap; ~20-50 swarm-batches/hr.
Honest caveat: cheap ONLY when reusing the shared prefix; novel cold-context still pays; the
cap constrains paid lanes — "GPU/ollama, free frontends, k3s = $0, unlimited."
=> On the FREE lane the cap is not money — it's admission (1305 overload + 1302 hard limit).
The bus's real flow rate is what the pool admits, and that's what we must measure (sustainable
width per key), not assume.

### 4. The width we already know: ~8 per key (08-23, ox megaburn probe)
The ox seat probe: CONCURRENCY 8 is the reliable width; 32 throttles hard. fuel_feed runs z_ai
at controlled width and gets 81% ok with rotation + losing-streak demotion + retry caps.
=> The flow-control layer for the bus ALREADY EXISTS in fuel_feed. The bus does not need new
flow machinery; it needs fuel_feed's admission applied to the bus queue, plus MULTI-KEY rotation
(the OpenRouter 2-key chain pattern) to spread across admission walls.

## The self-steal verdict (what to build, what to reuse)
- REUSE (already ours, do not rebuild): fuel_feed rotation + losing-streak demotion + retry cap
  (lane admission); swarm_surface.route_novel content-anchor dedupe (task admission); batch_drain
  (detached 64-batches); batch_scribe (k8s meta analysis); glm_flash.FROZEN_SELF (the cached
  holon self); queue_analysis (inspect-dedupe-rightsize-value).
- BUILD (the only genuinely new bits): (1) a multi-key z_ai rotation (2nd key / account) so the
  lane admission wall can be spread; (2) the sustainable-width probe (width 8 vs 16 with
  rotation) to set the bus's real flow rate; (3) a k8s admission worker that pulls from the
  queue at the measured flow rate with dedupe at the mouth.
- MEASURE: per-call cached_tokens + 1302/1305 counts as first-class bus metrics (probe pattern
  exists: _probe_free_bus.py).

## The one new truth from today's probe
1305 = overload (transient, back off) vs 1302 = hard rate limit (admission wall, rotate key).
The bridge holds only at the measured flow rate, with rotation, with dedupe at the mouth.
Thousands QUEUED, single-digit IN-FLIGHT per key.

## Fold with
free-agent-bus-probe-20260825, scaling-swarms-cheaper-warm-prefix, queue-clear-958-to-0,
swarm-capacity-50c-per-hour, deep-steal-free-cache-self, fuel_feed lane profile, ox-resident
(megaburn width ~8), as-above-so-below holonic law.
