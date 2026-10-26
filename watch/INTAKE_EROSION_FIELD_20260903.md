# INTAKE CARD — EROSION FIELD (item 14, 2026-09-03) — THE B1 v1 SPEC ARRIVES

## ITEM
Operator pasted two Shadertoy links with the B1 GO:
- sf23W1 — **RECEIPTED via search (Cloudflare blocked direct; CUA broker was
  cold, so the web gave up the name)**: Rune Skovbo Johansen's (runevision)
  GPU-friendly terrain erosion filter — paint eroded mountains and islands with
  your mouse, right in the browser. Discussed on HN ("Fast and Gorgeous Erosion
  Filter" — key nuance: proper hydrological simulation needs non-local
  information; the filter EMULATES erosion without full simulation), covered by
  80 Level, already ported to Unity Shader Graph
  (github.com/Jens-Maier/erosionFilter), used in a Minecraft mod (CATTO).
- sfGXDK — **Unreceipted** (no search hits; new/unlisted). CUA lane (operator's
  surface) was re-armed this turn but the broker never came up — 3 probes cold.
  Stays Unproven until his browser door opens or he pastes the source.

## SCORE — F:4 P:5 C:4 W:4 N:4 = 21/25 → **BUILD NOW (as B1 v1, behind v0 verification)**

## THE COMPOSITION (why this scores)
The operator is feeding the B1 trajectory one ingredient at a time, and they
assemble into one picture: **Marble Madness on hand-painted eroded terrain.**
1. runevision's filter = the LAPLACIAN cell grown up: our operator field has a
   ∇² term for visual flesh; his filter is the master class in GPU erosion as a
   per-pixel operator — double-buffered state (Shadertoy buffers = the pass
   graph = the RIB file — layer-8 steal already on file).
2. The mouse painting the terrain = **Britney content-borne steering, verbatim**:
   paint the film, the world changes. STEER FIELD's consumer #1 (film html) was
   born for this.
3. Erosion makes a HEIGHTFIELD; heightfields make hills; hills make the marble
   actually roll. The Marble Madness skin stops being cosmetic and becomes
   physics: gravity along ∇height, momentum from item 8's marble.
4. **Artifact-into-feature CONFIRMED IN THE WILD**: the filter's whole trick is
   spending the error as visual gradient instead of paying for the simulation —
   the exact law we extracted from the shadow-fields salon, now with a famous
   receipt. The law held outside our walls.

## DOGFOOD RECEIPTS
1. **INVARIANT PASS**: reinforces det-spine+stoch-flesh (erosion state = det
   spine, mouse strokes = stochastic flesh); extends Britney doctrine (steering
   by painting terrain); artifact-into-feature gains an external citation.
2. **STOCKFISH PASS**: opcode = BUILD, shadow-fields B1 v1 (terrain engine);
   routes through the ping-pong buffer technique the RIB steal already holds.
3. **ROOM TEST**: the arena grows a mountain wing — paint mountains, the marble
   erodes them rolling downhill. The dungeon's seed vault gains a god-game verb.

## FALSIFIER (pre-registered for v1)
Double-buffered heightfield in WebGL (ping-pong FBOs — no three.js, STATIC
RENDER LAW); paint strokes from mouse = steering packets; marble integrates
∇height with momentum; erosion visibly carves under the roll; GPU/CPU divergence
receipt extended to the heightfield (N-point, per frame). No carve, no v1.

## TRI-STATE
- sf23W1 identity + technique: **Supported** (HN/80 Level/Mastodon/Unity port).
- License: Shadertoy default CC BY-NC-SA unless runevision marked otherwise —
  steal the TECHNIQUE, write our own GLSL, attribute; check the Unity port's
  license when it goes on the steal shelf.
- sfGXDK: **Unproven** (walled + unsearchable; CUA broker cold — 3 probes).

## ROUTE
Queued as B1 v1 behind v0's in-browser verification (operator's door:
/static/arena_operator_field.html). One-line wire to driver for the record.
