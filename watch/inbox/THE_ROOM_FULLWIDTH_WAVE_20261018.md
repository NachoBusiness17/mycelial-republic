# FULL-WIDTH WAVE (wave 2, 2026-10-18) - "build everything full width"

**Trigger:** operator, mid-session, tagged with a Telegram plugin reference:
"Build everything full width". Read as: the whole remaining inventory from the
wave-1 receipt, at full fan, and the exhibit surface taken to the full window
width. The Telegram plugin itself is NOT loaded in this seat (no Telegram
tools exist here) - the estate-native answer to the "all windows in a chat"
riff is THE ROOM (below), not a transport this seat cannot touch.

## 1. THE EXHIBIT SURFACE IS NOW FULL-WIDTH (9 of 10 exhibits)

Pattern: fixed 960px centered column -> full window width (max 2200px), per
exhibit:

- `dashboard/static/smith_chart.html` v1.3 - TRUE responsive: CW/CH became the
  logical drawing space, the visible canvas stretches to the window, and a
  context transform maps logical -> device, so fonts/arcs/paper grain all
  scale; input remapped by the rect ratio; paper repaints on resize with
  even noise grain (verified at 960 and 1920).
- `dashboard/static/steer_field.html` - same class of refactor: the field
  renders at logical 960x600 into an offscreen buffer, then blits scaled
  (putImageData ignores transforms, so the buffer absorbs it).
- `dashboard/static/erosion_field.html` - layered-stage CSS fix: stage keeps
  960:600 via aspect-ratio, both stacked canvases fill it; its evPos was
  already rect-normalized, so zero JS change.
- `dashboard/static/dungeon.html` - CSS + one input remap (clicks scaled by
  960/rect.width before the cell math).
- `dashboard/static/eraser_maze.html`, `dashboard/static/incident_dungeon.html`,
  `dashboard/static/room_lightmap.html` - cap raises (they were already
  rect-normalized or inputless).
- `dashboard/static/persistent_world.html` - canvas + panel widened
  (keyboard-only, no pointer input to remap).
- `dashboard/static/keeper_voice.html` - text columns widened to 1400 (a
  reading page; 2200px lines are unreadable, judgment call).
- SKIPPED: `dashboard/static/mesh_gallery.html` (1440 lines, two layered
  fixed-height stages, 20 listeners) - deserves its own pass, not a blind
  CSS sweep; flagged honest.

Verification: bridge-Chrome screenshots at 1920 for erosion, steer field,
dungeon, smith (pageErrors=0 on all): `watch/inbox/FW_EROSION_1920.png`,
`watch/inbox/FW_STEER_1920.png`, `watch/inbox/FW_DUNGEON_1920.png`,
`watch/inbox/SMITH_FULLWIDTH_1920_20261018.png`.

## 2. THE FALSIFIER RACE IS ANSWERED, IN-BROWSER

The 20/25 card's race question ("does a gradient marble steer the printed
arcs to the matched center?") now has a RACE button on the smith chart:
numeric descent on |Gamma|^2 in z-space from a random passive load point -
unique minimum at z=1 - the trail drawn through the printed field, verdict
stamped in the DOM ("STEERED: matched center in N gradient steps"). A RIM
button jumps |Gamma| to ~1 for the pure standing-wave frame (nodes touch
zero). Evidence: `watch/inbox/SMITH_RACE_20261018.png` (spawn
z = 1.15 - j0.68, |G| = 0.309 -> |G| = 0.006, SWR 1.01) and
`watch/inbox/SMITH_RIM_20261018.png`. `watch/steer_field/field_smith.json`
landed as the card's v0 cell family (schema field.v1+smith.v1) for the arena
consumers; the full lights/cheese arena race remains the arena door's job.

One runtime bug found and fixed during verification: raceTrail declared
after the animation loop first read it (temporal dead zone) - moved to the
marble state block.

## 3. THE ROOM (the windows-in-a-chat riff, made a surface)

`dashboard/static/room.html` (v0, full-width by design): one page composing
the pull-surfaces that already exist - all ten `dashboard/static/trails/*.jsonl`
lanes as 30-day bar strips with row counts, last receipt per lane newest-first,
plus room_state.json / index_data/rollup.json / index_data/last_run.json.
Same-origin fetches only; absent surfaces render as absent, never invented.
Verified over real HTTP with every lane reading today's timestamps
(`watch/inbox/ROOM_V0_20261018.png`). Nav row added in
`dashboard/static/nav.js` (unclaimed file) next to Smith Chart. v0 reads -
it does not transport; a write path (seats leaving notes in a shared JSONL
the Room renders) is the v1 question.

## 4. THE ARENAPHYSICA VEIN, SWEPT

The reboost card's open vein, closed at $0: the full catalog enumerated (8
publications), three substantive reads folded - Heaviside-1 (fields-not-
scalars supervision generalizes OOD; ~10^5x solver speedup claimed), Atlas
RF Studio (forward 13ms + inverse diffusion; fields for 0.3 percent of
designs cut loss 15 percent), FEM edge elements (tangential continuity;
probes interpolate from frozen edge coefficients). The estate read: a shop
building EM foundation models independently re-derived the fields-not-
scalars law (the hologram close) and the probe-interpolates-from-frozen-
coefficients law (the smith strip's frozen nodes). Card:
`watch/inbox/ARENAPHYSICA_CATALOG_SWEEP_20261018.md` (three arXiv bodies
unread - timeouts, named there honestly).

## 5. TOOLING

`tools/cdp_page_shot.js` grew viewport + eval args (shoot after evaluating
page JS, at any viewport) - how the race/rim/room frames were verified.

## FILES THIS WAVE

- `dashboard/static/smith_chart.html` (v1.3), `steer_field.html`,
  `erosion_field.html`, `dungeon.html`, `eraser_maze.html`,
  `incident_dungeon.html`, `persistent_world.html`, `room_lightmap.html`,
  `keeper_voice.html` (full-width), `room.html` (new), `nav.js` (one row)
- `tools/cdp_page_shot.js` (viewport + eval)
- `watch/steer_field/field_smith.json` (new, the cell family)
- receipts/cards + evidence pngs under `watch/inbox/`

## WHAT REMAINS (still honest)

1. mesh_gallery full-width pass (skipped, named above).
2. The arena door's full lights/cheese race on field_smith.json.
3. Room v1: a write path (seats leaving notes the Room renders) - the
   transport question the Telegram tag points at.
4. Three arXiv bodies from the sweep card.
5. macOS/nav consumers of nav.js unaffected (one array row added).
