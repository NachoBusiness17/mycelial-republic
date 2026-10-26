# eigenmap-one (card eigenmap, ractor panel 2026-09-26)

Candidate: eigenmap-one. Status at file time: BUILD LANDED UNDER roblox/, gate
pass, overlay falsifier pass. Nothing committed (nobody asked; branch
mag/run-beta1-factory-build-audi-20260806T231709Z).

## Approach

The world map IS the data. The latest curvature scan's eigen_centroids become
beacon world positions through ONE documented affine transform (20000 studs
per eigen unit, plaza at world (600, 8, -100) east of every existing zone,
north = eigen -ey = world -Z, the same bearing law as the HTML map in
tools/cathedral_eigen_map.py), and the walker HUD reads distance and bearing
in the data's own units (milli-eigen and degrees 0 = N clockwise) from the
same shared module. Because the transform has no rotation and no axis flip,
the numbers a walker sees standing on a beacon are literally the scan's pair
numbers, so the judge's position/distance/bearing sanity check is a diff
against the JSON, and I shipped that diff as a rerunnable tool that executes
the REAL module under the plain Luau interpreter rather than a reimplementation.

Data anchor: watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json (the newest
scan; its eigen_centroids are identical to 20260926's across two independent
runs 26 h apart). The 0921 scan the HTML map used has drifted centroids
(e.g. water_computer [-0.025, 0.0141] then vs [-0.0236, -0.0124] now), so the
freshest self-consistent pair is the data of record; the module header and
GENERATED block carry the exact source file, ts and sha256
(ca62fec2214c713fe8d6714127d0ac4687e4d88a6fcfd3f0c3a3dbb639cc5ada), and one
generator command re-anchors the whole build to any other scan.

Design details that came from the estate, not invention:
- water_first chain rendering pairs with the referee lean (operative lean,
  RIB CONTESTED, watch/inbox/REFEREE_VERDICT_20260926.md); wired/missing
  stamped by the wired graph from tools/cathedral_walk.py (same edge source
  as the HTML map), missing stitches drawn dotted and named, never narrated
  away (build-debt law).
- off-map regions (adventure_2d6_stub, dnd_classic_stub) and the beta0
  3-islands finding are plaques: a negative is a fact.
- face drift to the nearest beacon rides the existing KSpace.drift smart-GPS
  pair (README mesh layer), dogfooding the estate's own instrument.
- the pure-number math in the shared module never touches Roblox globals
  (Vector3/Color3 adapters are separated) so the falsifier can require the
  module in tools/bin/luau/luau.exe and exercise the real code paths.

## Moves with estate paths

1. roblox/src/shared/EigenMap.luau (new, the single authorship site):
   GENERATED block (5 region rows with ex/ey/class/cos/hops, water_first
   chain with kinds, off-map list, beta0 wired 3 vs intended 1, scan ts +
   sha256) written by tools/gen_eigenmap_luau.py (new, idempotent: rerun
   printed "unchanged"); hand-written transform constants + pure API
   (distEigen, bearingEigen, distFromEigen, bearingFromEigen, nearestEigen,
   worldFromEigen, eigenFromWorld, span, center, chain, offMap, beta0,
   scanStamp, studsPerMilli) + Vector3 adapters (worldPos, distFrom,
   bearingFrom, nearest) + the HTML map's class palette.
2. roblox/src/server/EigenMapZone.luau (new): east plaza floor over the
   centroid bounding box + 40 margin, neon beacons at worldPos with labels
   (class cos, hops from water, eigen coords, studs per milli-eigen), the
   water_first chain (wired = solid rust beam, missing = dotted stones + a
   named missing-stitch marker per segment), north needle + N post,
   3 plaques (THE MAP with scan sha, WHAT IT LACKS with off-map + beta0,
   THE LEAN with the referee verdict), ShadowLedger rows on beacon touch
   (10 s debounce per player+region).
3. roblox/src/client/EigenMapHud.client.luau (new): the walker-view overlay,
   top-right panel: minimap (chain solid/dotted, class-colored dots, N up),
   live player marker via eigenFromWorld (clamped, honest "[off-window]" tag
   when projected outside), per-region rows "bearing deg / dist milli-eigen /
   dist studs" sorted by distance, nearest-beacon line, KSpace.drift face
   drift, footer with off-map + beta0. Throttled to ~6.5 Hz on Heartbeat.
4. roblox/src/server/init.server.luau: require + EigenMapZone.build() after
   OssuaryZone.build(), and a PORTALS row "EIGEN MAP" at the plaza (ungated:
   no region join, ZoneGate.portalGate returns true for fixed climbs, a
   fact). roblox/README.md: mesh-layer bullet naming the exact three files.
   queue/todo.md: RUNG CLIMBED line on the 2026-09-21 candidate-build block.
5. tools/eigenmap_overlay_check.py (new): the falsifier below. The gate
   rebuilt roblox/sourcemap.json and roblox/the_mountain.rbxlx; the built
   rbxlx contains my three scripts (EigenMap x99, EigenMapZone x8,
   EigenMapHud x5 mentions; verified by grep over the built bytes), and the
   UpdateAsync/GetAsync source counts stay 2/2 (baseline-verified: git
   show HEAD:roblox/the_mountain.rbxlx counts 2/2, the rebuilt worktree
   rbxlx counts 2/2, and my three files contain neither string; the B2-108
   annotation surface is unperturbed).

## Falsifier

Everything below was run during this ask; raw outputs are saved beside this
file and cited.

1. Overlay sanity check (the card's kill condition, executed):
   `.venv/Scripts/python.exe tools/eigenmap_overlay_check.py`
   -> PASS, exit 0. Raw: eigenmap-one.overlay_check.txt (regenerated on the
   final tree state). What it proved, at full scale:
   - trace: sha256 over the actual scan bytes == the sha embedded in the
     module's GENERATED block (MATCH);
   - data: 5/5 region rows equal the JSON's eigen_centroids, classes, cos,
     hops exactly;
   - math: the REAL module loaded under tools/bin/luau/luau.exe; all 10
     unordered pairs distEigen/bearingEigen equal a Python reference
     recomputed from the JSON: worst |ddist| 0.00e+00 eigen units, worst
     |dbearing| 5.68e-14 deg;
   - walker case: 20/20 standing-on-beacon readouts (distFromEigen +
     bearingFromEigen to every other region) equal the pair data;
   - nearest-at-beacon returns itself at 0; world distance == eigen distance
     x 20000 for all pairs (studs invariant); 3 eigen<->world roundtrips
     exact; chain segs, off-map list, beta0 verified through the module API.
   Reference table (scan 20260927, for any judge recompute; bearing 0 = N,
   clockwise, from -> to):
   | pair | dist (eigen) | bearing deg |
   |---|---|---|
   | audit_dungeon -> fractal_maze | 0.012331 | 247.6 |
   | audit_dungeon -> riddler_engram | 0.004701 | 113.8 |
   | audit_dungeon -> riddler_optics | 0.002059 | 119.1 |
   | audit_dungeon -> water_computer | 0.006551 | 301.3 |
   | fractal_maze -> riddler_engram | 0.015948 | 79.9 |
   | fractal_maze -> riddler_optics | 0.013709 | 74.3 |
   | fractal_maze -> water_computer | 0.009962 | 35.6 |
   | riddler_engram -> riddler_optics | 0.002657 | 289.8 |
   | riddler_engram -> water_computer | 0.011229 | 298.2 |
   | riddler_optics -> water_computer | 0.008609 | 300.7 |
   (HUD convention: at 20000 studs per unit, 1 milli-eigen = 20 studs; e.g.
   water_computer to fractal_maze reads 9.96 mE / 199 st / 215.6 deg from
   the water beacon.)
2. Build gate (README's named gate), run on the FINAL tree state:
   `bash tools/mountain_check`
   -> GATE PASS, exit 0 ("parse-level failures: 0 ... Built project to
   the_mountain.rbxlx"). Raw: eigenmap-one.mountain_check.txt (last of three
   runs, regenerated after all sibling edits I observed). Honest history:
   the FIRST run FAILED on a real syntax error of mine
   (EigenMapZone.luau:59, a malformed ("...":format()) wrapper; both parse
   errors mine), fixed, re-run passed. The second run showed 12 findings
   (4 from the sibling candidate's in-flight files: CathedralMap.luau
   math.atan 2-arg TypeError x2, CathedralPlate.luau LocalUnused,
   init.server.luau CathedralPlate.entry TypeError on their line, plus 8
   pre-existing LocalUnused in other zones); by the final run the sibling
   had fixed their TypeErrors and the count is 9: NONE in my files, 1 from
   their CathedralPlate.luau (LocalUnused 'pillar'), 8 pre-existing noise.
3. Parse-compile of my four touched Luau files:
   `tools/bin/luau/luau-compile.exe --binary <file>` -> PARSE OK x4
   (EigenMap, EigenMapZone, EigenMapHud.client, init.server).
4. Placement sanity (no world collision): my plaza spans world
   x in [403, 797], z in [-221, 21] (beacons at x in [443, 757],
   z in [-181, -19]); prior content max worldX = 300 (init.server WAVE
   table), basecamp rooms within radius 174. The sibling's plate (read from
   their CathedralMap.luau: ORIGIN (0,8,560), SCALE 12000) spans
   x in [-353, -164], z in [411, 508]: no overlap. Their HUD is top-left,
   mine top-right: no overlap.

## Owed

- No live Studio playtest: this seat has no Studio, so the in-world render
  (beacons, chain, HUD layout) is verified headless only (parse, semantic
  gate, rbxlx build, module math). First Studio open should eyeball the
  plaza once; the falsifier already covers the numbers a playtest would
  check.
- Data-anchor ambiguity: if the judge's sanity check anchors the 0921 scan
  (the HTML map's data) instead of 20260927, every number differs because
  the corpus moved between epochs (0926 == 0927 agree with each other). My
  build self-documents its anchor (source + ts + sha in the module) and
  re-anchoring is one command:
  `.venv/Scripts/python.exe tools/gen_eigenmap_luau.py --scan <file>`
  followed by the overlay check.
- Sibling contention (eigenmap-two) in the same worktree, live during my
  run: their CathedralMap.luau / CathedralPlate.luau /
  CathedralMapHud.client.luau landed 23:35-23:38 and were still being edited
  at 00:09; shared artifacts (init.server.luau, README.md, sourcemap.json,
  the_mountain.rbxlx) now carry BOTH builds. I did not touch their files.
  Their README "EigenMap" bullet cites file names that do not exist in the
  tree (CathedralZone.luau, EigenMapOverlay.client.luau) and in the version I
  read stated "0° = north = eigen +y, clockwise", which contradicts both
  their own CathedralMap.luau:12 header (north = -Z with worldZ growing for
  +ey) and tools/cathedral_eigen_map.py's bearing law (north = eigen -y);
  their earlier math.atan 2-arg calls were flagged by the gate's analyzer
  (the Luau runtime ignores the second argument, so those bearings would be
  wrong at runtime; they have since been edited, latest state unverified by
  me). Left to their lane and
  the judge; recorded here because it is the same card's evidence surface.
- Commit not made (not asked). The README bullet is in the working tree for
  whoever lands the commit; the rung line is in queue/todo.md, which is a
  git-ignored local file by a pre-existing rule (.gitignore:41), so it lives
  on disk only, like every todo edit in this estate.
- tools/cathedral_eigen_map.py itself still renders from the 0921 scan to
  CATHEDRAL_EIGEN_MAP_20260926.html; refreshing the HTML artifact to the
  0927 scan was not in this card's scope (the card is the in-game map) and
  is one SCAN constant edit away when wanted.

Self-rated kill risk: the judge anchoring a different scan epoch than
20260927 for the position/distance/bearing check. Everything else the kill
condition names is executed and passing on the record above.
