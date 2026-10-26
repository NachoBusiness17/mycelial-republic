---
name: three-dispatch-mechanisms-war
description: 9/26-27 burn revealed three overlapping dispatch mechanisms
  (automation fire, seat manual dispatch, swarm self-feed) fighting for queue
  state authority, causing stale restores, numbering collisions, and
  landing-check drift
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

The 9/26-27 flash-lane burn (397 briefs) revealed that three independent dispatch mechanisms fought for queue state authority: the dispatcher automation's 10-min fires, the seat's manual inline dispatches, and the swarm lanes' self-feed. Each wrote to QUEUE.md and BURN_WAVE_STATE.json independently, producing four systematic failures:

1. **Stale-restore war**: a concurrent QUEUE.md restore kept flipping landed briefs back to unchecked, requiring repeated receipt-verified re-flips (147 in one pass alone)
2. **Numbering collisions**: 24+ brief ids double-spent by concurrent self-feeds (B2-92/93, B2-108/110, B2-269/270, B2-328/329, B2-407/408, B2-417/418, B2-441/443, B2-528/530 etc)
3. **Landing-check drift**: the dispatcher's dash/underscore landing detection lagged manual re-flips, causing "holding" replies while lanes had actually landed
4. **Census drift**: the B2-251 checkbox audit kept going stale within minutes as lanes landed faster than the census could track

**Why:** at scale, one mechanism must own queue state authority. Three writers to the same file produce ordering races that no amount of per-lane discipline can fix.

**How to apply:** at burn scale above ~20 lanes, either (a) one mechanism owns all queue mutations and the others read-only, or (b) use a claim/CLAIMED protocol where every mutation is preceded by a claim line. The B2-250 shared-file claim law and B2-238 checkbox law were correct but insufficient — they need mechanical enforcement (a checker script), not convention.

The 400-lane burn proved the fleet can absorb the chaos and still land 397+ briefs with receipts, but the coordination overhead consumed est. 15-20% of total seat context on state reconciliation alone.
