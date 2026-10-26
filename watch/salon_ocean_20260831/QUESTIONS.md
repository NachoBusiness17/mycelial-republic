# OCEAN SALON — mapping the whole stack socratically (2026-08-31, operator charter)

**SPEND POLICY (operator, 14:07Z):** $1/hr when the operator is actively driving (frontier thinkers, councils, parallel leads); cheap/off-peak when away (flash gophers, free lanes, local arms). The water clock now maps windows to operator presence — output per window, not per dollar.

**WORKING RELATIONSHIP (operator, 14:07Z):** scrum-master / product-owner. Sancho = agile controller running the fleet through shared environment spaces (room, board, bus, steers, jobs); operator = product owner who sets priorities, blesses gates, unblocks. Approaching autonomy: the operator's job is shrinking to deciding WHAT matters, not HOW it runs.

The ocean model: every seat answers the SAME mapping questions about the layer it actually
touches, then round 2 shows every seat the others' answers — each names one unlock (what
becomes possible when combined) and one gap (what it needs that nobody provides).

Deliverable: /board/OCEAN_MAP_20260831.md — the operational surface map, seat by seat,
capability by capability, with unlock/gap pairs. This is the atlas of what our stack CAN do,
written by the parts that do it.

## The mapping questions (every seat answers all 6, about its OWN layer)

1. WHAT DO YOU KNOW? — What state/receipts/memory does your layer hold that the map
   (ledger, catalog, atlas drafts) does not reflect? Be specific: path + what's there.
2. WHAT CAN YOU DO THAT NOBODY ASKS FOR? — Capabilities wired and working that no seat
   or operator has invoked recently (or ever). The idle hands inventory.
3. WHO ASKS YOU FOR THE WRONG THING? — Misuses you see: tasks routed to you that belong
   elsewhere, or asks that fail because the caller misunderstands your surface.
4. WHAT WOULD YOU NEED TO TOUCH THE LAYERS ADJACENT TO YOU? — The one missing wire,
   permission, or schema that would connect you to the next subsystem.
5. WHAT SHOULD THE DRIVING AGENT KNOW ABOUT YOU JUST-IN-TIME? — If a fresh driver
   (Sancho, codex, a new 5.3 lead) warms a RIB about your layer, what 3 facts must be
   in the pack? (This feeds the warm-pack.)
6. WHAT DO YOU COST, AND WHEN DO YOU RUN DRY? — Your per-call/per-hour cost at current
   receipts, which water-window reservoir feeds you, what happens to your layer when
   that reservoir empties, and what degrades silently if nobody notices. (Operator
   correction 12:03Z: cost was missing from the map. It is now a first-class axis —
   every capability answer must name its meter.)

## Seats answering (wave 1 = cage lanes; wave 2 = desktop paste)

- lane-rib (5.3): RIB / WARM_PACK / memory_rib_write / deref — the memory layer
- lane-mcp (5.3): tools.py TOOL_MAP (43) / mcp_server / agent_cli dispatch — the hand
- lane-bus (flash): room.jsonl / riddler_common / jobs / bridge inboxes — the bus
- lane-water (flash): water_windows / offpeak / seat_corpus lanes / quota reservoirs — the flow
- wave-2 paste: codex (long-horizon view), grok-a, grok-b, pro (desktop view of the same 6 questions)

## Rules
- Every claim needs a pointer (path + what's there). Calibration words. No invented organs.
- Round 2 (cross-pollination) fires when 4+ answers are on disk: each lane reads the others'
  rows and appends UNLOCK + GAP lines to its own row file.
- Synthesis: Sancho merges into OCEAN_MAP with the unlock/gap matrix.
