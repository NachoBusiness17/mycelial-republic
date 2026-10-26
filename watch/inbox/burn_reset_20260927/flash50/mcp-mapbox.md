# mcp-mapbox: Mapbox MCP tool dogfood (2026-09-28)

Item mcp-mapbox, flash50 lane. All checks below ran live in this session via the
session's Mapbox MCP tools on 2026-09-28. No subprocess was spawned for any check;
every result is a direct MCP tool call. Bank file written by the Write tool, then
scanned for em/en dashes (result at the bottom).

## What was asked

1. Geocode a real address (geocoding tool).
2. Plan a real route (directions tool).
3. Compute a 15-minute walkshed from a real address (isochrone tool).
4. Document what works, what's missing, integration patterns.

## 1. Geocoding (search_and_geocode_tool) - WORKS

Call A: `search_and_geocode_tool(q="350 5th Ave, New York, NY 10118", country=["US"], language="en", proximity={longitude:-73.9857, latitude:40.7484})`

- Top hit: "350 5th Avenue, New York, New York 10118, United States", feature_type
  `address`, rooftop accuracy, coordinates (-73.985663, 40.748554), distance 17 m
  from the proximity point.
- `routable_points` present on the hit: Address point (40.748866, -73.985532) plus an
  entrance point. This is the field that should feed routing, not the rooftop point.
- Full context hierarchy returned: neighborhood Koreatown, locality Manhattan, place
  New York City, district New York County, region US-NY, postcode 10118.
- `mapbox_id` returned (base64 `urn:mapbox:address:...`), reusable for
  place_details_tool (see section 4).

Call B: `search_and_geocode_tool(q="10 Columbus Circle, New York, NY 10019", ...same filters)`

- Top hit correct: rooftop (-73.983135, 40.768228), routable point
  (40.76812, -73.982382), full context (Hell's Kitchen, Manhattan, 10019).

Noise found (honest negatives):

- Query A hits 2-10 drift far: POIs in Murray Hill, Midtown East, two "The Gyro
  Project" POIs in Brooklyn at 7.7 and 9.6 km. Ranking did not stay tight to the
  address-shaped query.
- Query B hit #7 is a "Paper Source" in Corry, Pennsylvania, 491,227 m away, despite
  the `country=["US"]` filter (which limits country, not distance). An agent that
  takes result N instead of result 1 can silently route across a state line.

## 2. Directions (directions_tool) - WORKS, with profile constraints

Call: `directions_tool(coordinates=[{longitude:-73.985532, latitude:40.748866},
{longitude:-73.982382, latitude:40.76812}], routing_profile="mapbox/walking",
geometries="none", alternatives=false)` - ran 3 times, identical results:

- Distance 2,434 m, duration 1,824 s = 30.4 min, leg_summaries
  ["West 34th Street, Broadway"], average_speed_kph 5, num_legs 1.
- Waypoints snapped with names and snap_distance: "West 34th Street" (0 m) and
  "Columbus Circle" (2 m). Snap distances confirm the routable-point chaining worked.
- congestion_information all-zero object is present even for walking (length_low/
  moderate/heavy/severe = 0): dead weight for non-driving profiles.

Second call with `geometries="geojson", exclude="ferry"`: accepted; returns the full
vertex-level LineString for the 2.43 km walk (hundreds of vertices, eyeballed, not
machine-counted) plus the same summary fields.

Constraints proven by runtime errors (each verified by an actual failed call):

- `arrive_by` with walking profile: rejected, "The arrive_by parameter is only
  available for the 'driving' profile".
- `depart_at` with walking profile: rejected, "The depart_at parameter is only
  available for 'driving' and 'driving-traffic' profiles". Confirmed on 3 separate
  calls. The tool schema documents this; the runtime enforces it fail-loud with a
  specific message. Good failure shape.
- max_height/max_width/max_weight are documented driving-only; not exercised.

NOT exercised, reported as not run: `steps=true` turn-by-turn mode. Four attempts to
send it failed because my own argument serialization kept re-injecting stale
`arrive_by`/`depart_at` fields and dropping `steps` (see Pattern P7). The tool never
received the param; the schema documents `steps` (default false) and `language` for
instruction locale. This is an agent-side miss, not a tool miss.

## 3. Isochrone (isochrone_tool) - WORKS

Call: `isochrone_tool(coordinates={longitude:-73.985663, latitude:40.748554},
profile="mapbox/walking", contours_minutes=[15], polygons=true, generalize=100)`
from the geocoded rooftop of 350 5th Avenue.

- Returned 1 Polygon contour, contour=15, metric=time, render color #bf4040 at
  fill-opacity 0.33.
- Geometry after generalize=100: 8 vertices, spanning roughly lng -73.9991 to
  -73.9719, lat 40.7387 to 40.7583 (Koreatown up through Midtown around the start
  point). At generalize=100 the shape is coarse; treat any derived area as a floor
  approximation of the true walkshed.
- API note: `generalize` is a REQUIRED tool parameter (the agent must know the
  walking guidance of 50-200 m from the tool description; there is no default).

Offline composition: fed the returned polygon ring straight into the offline
`area_tool(geometry=<isochrone ring>, units="kilometers")` -> "Area: 3.4 square
kilometers". No API call; the offline geometry tier composes cleanly with API tier
output.

## 4. Bonus chain: place_details via mapbox_id, and the final render

`place_details_tool(mapbox_id=<id from geocode call A>, attribute_sets=
["basic","visit","venue"])` - succeeds, returns the same address feature (named
"350 Fifth Avenue" vs the geocode's "350 5th Avenue": a small naming drift between
endpoints for the same id). For an address (non-POI) feature the visit/venue sets
return nothing: no hours, rating, photos, phone. Fail-soft silence, not an error;
the agent must notice absence. For POIs the same chain should return them (not
verified on a POI; not run).

`render_map_tool(payload_refs=[<directions ref>, <isochrone ref>], markers=[A,B],
summary=...)` - rendered=true, layer_count 0, marker_count 2, and the two refs ride
along as `selfFetch` entries. The map client will re-run the directions and isochrone
queries itself on load. The tool's stated contract (invoke as the FINAL step, pass
refs from earlier tool results) worked exactly as documented.

## Patterns for agent-tool integration

- P1 Dual-channel responses. Every API tool returns a human-readable digest AND a
  machine `structuredContent` GeoJSON payload. Quote the text for the human, chain on
  the JSON. No parsing of prose needed.
- P2 Refs are replayable queries, not stored results. The `mapbox://selffetch/...`
  URIs are base64-encoded tool PARAMETERS, not cached outputs; the render client
  re-executes them. Stateless and cheap, but it means a ref is not an artifact: an
  agent banking results must bank the GeoJSON itself (as done here), never just the
  ref.
- P3 Composability contract held. Multiple payload_refs (route + walkshed) plus
  inline markers merged into one map in a single final call. The orchestration order
  is encoded in tool descriptions (render says "invoke as the FINAL step"; the
  ground_location description says use it FIRST for nearby questions). The surface
  self-documents its own call graph.
- P4 Identity chaining. geocode -> mapbox_id -> place_details works, with the caveats
  that address features carry only basic attributes and the display name can drift
  between endpoints.
- P5 Two failure modes to verify differently. Profile-constraint violations fail
  LOUD with exact messages (depart_at on walking); attribute absence fails SOFT with
  a clean empty result (visit/venue on an address). Loud failures are self-correcting
  for agents; soft ones are where silent wrongness lives.
- P6 Offline tier vs API tier. bbox/area/centroid/buffer/union/difference tools run
  with zero API calls and accept the API tools' GeoJSON directly. Derived stats
  (3.4 km2 walkshed) cost no quota and no network.
- P7 The real hazard is agent-side argument contamination. Across four retries my
  call builder kept re-injecting stale fields (arrive_by/depart_at) and dropping the
  intended one (steps). Runtime validation caught every bad call, but an agent that
  does not read errors will loop. Practical rule for this harness: build each retry
  from the minimal fresh argument set, never mutate the previous call.
- P8 Dual usage of coordinates. Rooftop points are for display; `routable_points`
  are for routing. Directions snapped cleanly (0 m and 2 m) when fed routable points.

## What's missing

- No persistence or batching tier: calls are independent; no batch geocode; refs
  carry params, not results (P2).
- steps=true turn-by-turn: documented but not exercised here (agent-side failure,
  four attempts, reported above).
- Address features have no photos/hours/rating via place_details; POI-only.
- Geocode ranking leaks far-field POIs (9.6 km in-query, 491 km cross-state) into
  address-shaped queries; `types=["address"]` exists to tighten and should be used.
- Isochrone generalize is required with no default; wrong scale silently coarsens
  the shape (8 vertices at 100 m here).
- Directions compact mode omits both geometry and steps by default; there is no
  single "give me everything" mode; congestion fields ride along uselessly on
  walking profiles.

## Verdict

The three asked checks all pass as run: geocode (2 addresses, rooftop accuracy,
routable points), directions (2,434 m / 30.4 min walking route, named waypoints,
geojson geometry mode), isochrone (15-min walking polygon, 3.4 km2 via offline
area_tool). The toolset is agent-shaped: dual-channel output, replayable refs, an
offline math tier, loud profile-constraint errors. The gap that bit was on the agent
side: argument hygiene across retries.

## Process notes

- Bank target: watch/inbox/burn_reset_20260927/flash50/mcp-mapbox.md (this file;
  the ask's shorter pointer "flash50/mcp-mapbox-dogfood.md" resolves to the same
  flash50 bank; the full path given in the ask was used).
- Tool call census this item: 2 geocode, 6 directions attempts (3 success walking
  compact, 1 success geojson mode, 4 failures: 1 missing-coordinates validation, 3
  walking-profile time-param rejections), 1 isochrone, 1 place_details, 1 area, 1
  render = 13 calls.
- No files read from the repo for the checks themselves; all evidence is live tool
  output quoted above. AGENTS.md house laws applied: no fabrication (steps=true and
  POI place_details reported as not run), no em/en dashes, no subprocess spawns.
- Follow-up worth a future item: exercise steps=true with language, a POI
  place_details chain with photos/visit, and tilequery against mapbox-streets for
  road-level context under the walkshed.
