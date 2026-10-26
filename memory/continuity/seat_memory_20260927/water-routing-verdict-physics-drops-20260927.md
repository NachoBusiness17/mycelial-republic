---
name: water-routing-verdict-physics-drops-20260927
description: Water routing 9/27 fully BUILT+WIRED — water_graph engine (check valves, siphons, XOR/SILL junctions, steam) + campaign graph mode (22/22); operator verdict "not a sacred cow, under-built"; shape_map FAMILY_CLAIMS granted; physics-pair drops filed
  there" 9/27 — verdict NOT a sacred cow, under-built (VALVE_AT has 2 entries,
  no graph); water_graph engine + campaign wiring BUILT same day (22/22);
  + underwater-plasma and vortex-street-latent-loop drops filed
metadata:
  node_type: memory
  type: project
  originSessionId: sess_bb9913b3-7c0e-45ff-9e15-d94e98cdb6aa
---

Operator question 9/27 (after the water_computer seam was wired same-day):
"why doesn't our water routing work, is that a sacred cow, I really think
it's useful using the physics instead of fighting them."

**Verdict (byte-read of mag/water_computer.py):** NOT a sacred cow — the
opposite, nobody ever fought for it. The routing graph was literally
`VALVE_AT` with 2 entries: a fixed 3-tank line, 1 unit/tick, nothing to
route WITH. Under-built, not defended (bucket-cheat law = good doctrine).

**BUILT same day, two commits:**
1. **mag/water_graph.py** (f1bceeb3a): flow-graph engine — one-way check
   valves (never uphill by construction), integer capacities, siphons
   (prime at crest, break when intake dries — hydro_xor_sim laws
   generalized), XOR junction (delivers only on exactly-one inlet; both →
   overflow = hydraulic XOR), SILL junction (threshold = hydraulic AND),
   steam condenses at highest cold node (steam = second routing medium
   ignoring pipes), deterministic 3-phase tick, spec roundtrip. 7 physics
   tests + legacy = 14/14. First-cut gate bug caught by tests (gated
   outflow raced its own inflows → deferred-gate restructure). Live demo:
   hydraulic AND delivered 2/tick, XOR refused both-inlets — water is a
   wire. shape_map FAMILY_CLAIMS landed (operator grant "Family
   extension": verkle_chain claims the archived knot family, 4 path rules;
   mimosa hook-state + ghost leak-reports deliberately unclaimed).
2. **Campaign wiring** (31f966dc2, lane): water_computer graph mode —
   water:graph flag carries the spec; wait/work/rest/janitor tick +
   open/close/use valve + sight glass all delegate to WaterGraph; legacy
   3-tank path byte-identical without a spec. Room→pipe contract (spec map
   first, src-name fallback, unmapped refuses); spec persists in
   _flag_map with overlay-on-roundtrip; win honesty inherited (win_node
   mirrors water:out, bucket still cheat). Lane caught its own
   silent-drop bug (pipes overlay never attached on save).
   **Water family 22/22 at -n 4.**

**Drops filed same turn (LINKS, physics-as-ally pair = the design's
epigraph):** SocraticScribe underwater plasma (kV flash-vaporizes water
into sun-surface plasma; collapse sterilizes — using the medium, not
fighting it) + mathelirium vortex street (NN compresses flow into an
8-value latent loop; "fluid dynamics organized themselves into geometry").

**Why:** operator's design philosophy stated as preference — physics as
ally, never adversary; instruments should derive behavior from conditions,
not animate hardcoded paths.

**How to apply:** when told something "doesn't work," check for
VALVE_AT-style hardcoded tables first; "use the physics" = build the real
mechanics, not the animation. Owed: in-world pipe-building verb (topology
is spec-authored; open/close suffices for now). Related:
[[no-sacred-cows-execution-20260927]], [[the-mountain-roblox-20260924]].
