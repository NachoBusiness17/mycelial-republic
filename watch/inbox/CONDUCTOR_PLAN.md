# THE CONDUCTOR (2026-10-01, operator architecture)

Operator: "three different 5.3 max instances driving the flash lanes. or the
equivalent. just one for now. this one doing complex reasoning and sending it
down the chain or knowing when it's out of its depth and routing to claude or
whatever model we have deemed acceptable for that kind of advice cheaply and
tested amongst free so we have an idea of capabilities and what/when to ask
the frontier"

## The architecture

```
       THE CONDUCTOR (one 5.3 max instance, ~$0.02/ask)
      /       |         |          \        \
  route:   route:    route:      route:   route:
  FLASH    FLASH    LOCAL       FREE     FRONTIER
  (bulk)   (parallel (python,   (sensing, (oracle,
   lanes    tasks     tests,     capability judgment,
   ~$0.004  at width  tools)     mapping)  $0.20-0.40
   /ask)                          $0         /ask)
```

## The conductor's decision loop

For each task:
1. CLASSIFY: what shape is this? (code / analysis / judgment / creative / extraction)
2. CONFIDENCE: how confident am I? (the metacognitive step)
   - HIGH confidence + mechanical -> route to FLASH (bulk, parallel)
   - HIGH confidence + complex -> do it MYSELF (one max call)
   - LOW confidence + important -> route to FRONTIER (judgment ask)
   - UNKNOWN shape -> route to FREE (capability sensing, then re-classify)
3. DELEGATE: send to the chosen tier with the right harness (per animal profiles)
4. VERIFY: check the result against the estate's instruments
5. LEARN: feed the outcome back to the animal profiles + GPS ledger

## The escalation law (when to ask the frontier)

The conductor asks the frontier ONLY when:
- The task's cost-of-being-wrong exceeds $5 (the frontier ask price)
- Its own confidence is below threshold AND the GPS meter has no data for the shape
- A cross-family check is needed (one family judging another)
- The doctrine arbiter flags an EXPIRED doctrine item (a frontier re-read is owed)

Everything else: flash, local, or the conductor itself.

## The pricing

- Conductor (5.3 max): ~$0.02/ask, handles the routing + complex reasoning
- Flash workers: ~$0.004/ask, handle the bulk
- Free lanes: $0, handle sensing + capability mapping
- Frontier oracle: ~$0.20-0.40/ask, handles the rare judgment
- Blended: ~$0.01/ask average at 1:5 conductor-to-flash ratio

At this ratio, 1000 asks = $10 total (vs $20 if the conductor did everything,
vs $200+ if the frontier did everything).

## Implementation: v0 today

tools/conductor.py: the routing loop with the animal profiles as its brain.
One conductor instance, flash workers via ds_workhorse pattern, frontier
escalation via lensing_ask pattern. Free lane integration via stealth fleet.
