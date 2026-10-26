# THE VISLAB: REPRESENTATIVE + NAVIGABLE (2026-10-18)

**Trigger:** operator: "we're finally using the vislab now if only we could
make it representitive and navigatable" - then, with the 3D Smith chart
references (Muller, Moldoveanu, Asavei et al. 2011, "The 3D Smith Chart and
Its Practical Applications", Microwave Journal; 3dsmithchart.com): "show me
mag and our codebase in a representitive smith geodesic volume sphere. for a
map of ourselves."

## REPRESENTATIVE - the exhibits stop being fossils

Root cause found: `watch/steer_field/build.py` (the organ that reads real
fleet state) had also been the GENERATOR of `dashboard/static/steer_field.html`
and was run exactly once, on 2026-09-03 - the page has worn that September
inline ever since. Running it again would have overwritten the full-width
refactor. Fixed at the design level, not guarded:

- **FEED LAW**: build.py is now a data feed only - it writes
  `watch/steer_field/FIELD.json` + TAILS.md plus a served copy
  `dashboard/static/steer_field/FIELD.json`; the html template generation is
  deleted, not commented out. The page is a durable consumer that fetches the
  served field same-origin, keeps its inline snapshot as offline fallback,
  and LABELS the data's age on the page ("field ts ... LIVE" vs "SNAPSHOT
  FALLBACK").
- First live feed ran immediately: 8 lights, 8 seats from today's bay state
  (`dashboard/static/steer_field/FIELD.json`), and it surfaced a standing
  operational finding for the operator: seat-g1 is STILL failing on wing
  sp_60400550 - the same turn-fail the September snapshot carried. That
  oscillator has been running for six weeks.
- Cadence: `MagSteerFieldDaily` registered (08:40 daily;
  `scripts/register_steer_field_task.ps1`, action `scripts/steer_field_daily.ps1`,
  log `logs/steer_field.log`) - the film gets fed every morning now.
- `erosion_field.html` wears the same feed (fetch with fallback).
- Bug fixed en route: steer_field's walker phase `F.t` was never initialized
  (undefined + 0.05 = NaN) - the walkers have been frozen since the page was
  generated. Seeded now.

## NAVIGABLE - the vislab floor

- `dashboard/static/vislab.html`: one full-width grid of EVERY exhibit the
  dashboard serves, parsed live from nav.js (one source of truth - new
  exhibits appear automatically when they join the nav), with honesty chips:
  DATA-FED (pulls live estate JSON) / HANDS (takes input) / SNAPSHOT
  (inlined bytes). Verified render: `watch/inbox/VISLAB_20261018.png` - the
  catalog is far bigger than the smith thread knew (Arrakis, Kabuki Tavern,
  Ractor Board, Viz Lab, Falsifiers, Chain Check...).
- Nav rows added: Vislab + Smith Globe (nav.js, unclaimed).

## THE GLOBE - the map of ourselves (`dashboard/static/smith_globe.html`)

Our own zero-dependency canvas implementation of the 3D Smith chart: unit
sphere, stereographic from the south pole, the constant-r / constant-x
families preprojected onto it, drag to steer (yaw/pitch), wheel to zoom,
paper-and-ink grammar matching the planar chart. The sphere completes the
fold: Gamma = 0 is the north pole, |Gamma| = 1 the equator, negative
resistance the whole south hemisphere, Gamma = infinity the south pole -
nothing is off the map.

The estate weather on it (same-origin pulls, embedded fallbacks, ages
labeled): FROZEN files at the north pole - the frozen leaves, checkpoints
and verkle root, the standing-wave nodes (592,109 files per
`dashboard/static/index_data/rollup.json` at build time); HOT files at the
equator - churn re-minted every frame; engines north by intensity (routed =
matched); TURN-FAIL seats in the SOUTH hemisphere - a retry loop is a
negative-resistance element, an oscillator, and the RF word for a turn-fail
is oscillation (OSC A.1 renders there today). RACE draws the 2D chart's
matching walk as a geodesic on the sphere: navigation toward the north pole,
per the RF literature's own Google-Earth analogy. Verified:
`watch/inbox/GLOBE_20261018.png` (LIVE weather line, zero page errors),
`watch/inbox/STEER_LIVE_20261018.png`.

## FILES

- `watch/steer_field/build.py` - FEED LAW refactor (page generation deleted)
- `dashboard/static/steer_field.html`, `erosion_field.html` - fed consumers
- `dashboard/static/smith_globe.html`, `vislab.html` - new
- `dashboard/static/nav.js` - two rows
- `scripts/steer_field_daily.ps1`, `scripts/register_steer_field_task.ps1` - new
- `dashboard/static/steer_field/FIELD.json` - served data (tracked; churns daily)
- evidence: `watch/inbox/GLOBE_20261018.png`, `VISLAB_20261018.png`,
  `STEER_LIVE_20261018.png`

## WHAT REMAINS

1. The operator owes seat-g1 a look: sp_60400550 has been turn-failing since
   at least 2026-09-03 (same wing id across both snapshots).
2. Curated one-liners for the long tail of vislab cards (most say "estate
   exhibit" - honest, but the floor deserves labels).
3. mesh_gallery full-width pass (still skipped from wave 2).
4. Room v1 write path (the transport question behind the Telegram tag).
