# LIVING MUD v1.1 — THE CARTOGRAPHY UPDATE (deployed, playtested, judged)

**Date:** 2026-09-23
**Live:** https://world-games-corpus-mag-d961.vercel.app/livingmud.html
**Desk:** https://world-games-corpus-mag-d961.vercel.app/cartographer.html
**Deploy dir:** Documents/projects/world-games-corpus (Vercel project `world-games-corpus`, team `mag-d961`, deploy with `npx vercel deploy --prod --yes --scope mag-d961`)

## THE HEADLINE: the deployed game was unwalkable

Read the engine closely and v1 had TWO dead chains:

1. **No movement.** `ROOMS.threshold.actions` listed `go rsvp` / `go corridor` /
   `go valves`, but `ACTIONS` had no `go` handlers at all. The parser fell
   through to "No door to 'x'." You could never leave the threshold.
2. **The tank never filled.** Nothing incremented `S.flags.tank`. The valve
   room was unwinnable, and there was no win state anywhere.

"Engine owns truth" owned a truth you couldn't walk through. Classic
claimed-without-delivering — caught this time by *reading our own game*.

## What v1.1 ships

- **Movement** from a legal table (`EXITS`), with gated doors:
  - threshold → vesper requires `rsvpOpen` (the corded door; "the stacks admit
    those who read the two-sided door from both seats")
  - corridor → valves requires `corridorOpen` (beam latched; eraser stone
    flattens the signal and re-seals it)
- **Valve room is a real water computer:** valve A pours +2 (measured, seats
  itself), valve B drains −2, bucket = +3 but the record prints DISPUTED
  forever. Tank to 6/6 → gate opens → WIN. Two endings: DELIVERED UNDISPUTED
  or DISPUTED-forever ("the gate opened anyway — that is the point of receipts").
- **Scene stills** for all 5 rooms + gate hero, generated on the xAI lane
  (`grok-imagine-image-2.0`, ~$0.42 total, inside the iron circle) via
  `tools/stills_xai.py` (guard() public-IP check, literal host/port, key from
  .env only). Wired with graceful fallback if assets missing.
- **Fog-of-war minimap** rendered BY THE ENGINE from its own EXITS graph —
  unvisited rooms are "?", current room highlighted, gated doors dashed,
  nodes clickable (engine still validates the walk — map is a view of state,
  never a second source of truth).
- **Cartographer's desk** (cartographer.html): tldraw infinite canvas via
  esm.sh (react 18 + tldraw 3.15.6, deps pinned), auto-seeded with the same
  room graph — bound arrows anchor to card borders, red dashed = gated doors,
  persistenceKey `livingmud-desk` (IndexedDB — localStorage.clear() does NOT
  wipe it; wipe via indexedDB.deleteDatabase when re-seeding).
- **Link repairs:** /work.html was a 404 on prod from three pages → routed to
  living.html / living_mud.html; corpus deep-cut links now carry the
  `corpus/` prefix; the hub features the playable mud + desk at the top.

## Verification (the house way)

- Live playthrough via browser input-pump against prod: gated refusal →
  mirrors 30+30 → beam latches → valves 2/4/6 → § THE GATE OPENS § +
  DELIVERED, UNDISPUTED → gate OPEN in HUD. Second run: both plates → cord
  drops → stacks admitted → Vesper voice lines → map-click walks back.
  NOTE: IAB's Playwright `press("Enter")` does not reach the page; pump with
  synthetic KeyboardEvent dispatch — native keydown (real players) is
  unaffected.
- Visual gate: livingmud / hub / cartographer all PASS. First-round "fail"s
  on the game + hub were fullPage-stitch ARTIFACTS (duplicated columns,
  repeated tiles) contradicted by DOM measurement (single .wrap, all sections,
  no horizontal overflow) — re-captured as single tall-viewport rasters.
  Desk needed real fixes: tldraw auto-grows cards on create (clamp with
  updateShapes BEFORE creating arrows), shape ids need `shape:` prefix,
  binding ids need `binding:` prefix, line points need id+index, and
  `external=react` on esm.sh serves un-resolvable bare specifiers.

## Estate mirrors

watch/corpus/{livingmud,cartographer,living_mud,living}.html + stills/*.jpg
kept in sync with the deploy dir.
