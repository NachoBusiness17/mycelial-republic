# GSTD FULL AUDIT - the plan - 2026-10-09 (operator: "full audit of gstd and how to
# incorporate it and how we can enhance its bones into something we can cook
# with for our republic")

Three lanes, chained (width law: 3 concurrent max; surface/vocab/upstream
lanes drain first):

## Lane A - CODEBASE AUDIT (fires now)
Deep read of reference/gstdcoin/gstdbot src/ (+ light pass on the web clone):
module map (gateway, router, swarm, node-lite, wallet, platform-link,
channels, P2P), per-module bone quality, security surface (auth, rate, key
handling, the push class), and the MISSING-FOR-REPUBLIC list: what the
codebase lacks that a sovereign republic needs (verifiable results, real
reputation semantics, peer verification, sovereignty tiers, fork-equality
mechanics). Output: GSTD_CODEBASE_AUDIT.md.

## Lane B - TOKENOMICS + NETWORK AUDIT (chains on drain)
The money's physics from code + live platform + our own earnings: emission
shape, payout math (cross-check: Pi 288 tasks -> 51.39 GSTD vs our 9 ->
0.0916 - consistent or regime change?), the genesis seal ("supply grows
only with verified work") - enforced in code or aspirational?, inflation
questions, and the value-thesis stress test. Output: GSTD_TOKENOMICS_AUDIT.md.

## Lane C - THE REPUBLIC COOKBOOK (chains last; eats A+B)
The incorporation map as BUILD SPECS (estate side: router tiers, mesh
bridge, installer step, GWAP payload wire) + the enhancement proposals -
what we contribute BACK to the bones (replay-verified results as
platform-checkable receipts, GPS capability advertising, Article-15-shaped
wallet UX, two-tier offline settlement) - each proposal sized (PR / spec /
fork-level) and constrained by the republic's laws. Output:
GSTD_REPUBLIC_COOKBOOK.md.

## Lane D - GAPS + THE PEOPLE WHO FILLED THEM (chains on Lane A; operator: "identify
## gaps in gstd and our needs and attempt to find people who have filled them")

Two-sided gap register: (1) GSTD's bone gaps (from Lane A's missing-for-republic
list + Lane B's tokenomics holes), (2) OUR needs the stack doesn't cover
(offline settlement, verifiable results at settlement grade, task routing
quality, installer-grade key UX, the mesh bridge). Then the EXTERNAL census:
for each gap, WHO has filled it - projects, protocols, papers, teams (the
prior-art steal class: web research with real sources). Each card: gap /
who filled it / how (the mechanism) / source / verdict STEAL vs WATCH vs
PARTNER-vs-build. Output: GAPS_AND_PEOPLE.md.

## Feeds already in hand (inputs)
- Live dogfood data + 4 defects (DOGFOOD_DATA.md) + PRs in flight
- Three-body map, probe 2 (0/15 fat shapes), node census, wallet-door
  forensics (the trust context), build-out receipts
- The constitution (Art 15, fork equality, data tiers) as design constraint
