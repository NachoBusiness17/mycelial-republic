# eigenmap-two (candidate two, card eigenmap, ractor panel 2026-09-26)

Built, checked, gated. Everything below cites bytes I read or commands I ran
this session.

## Approach

The card: render the in-game world map FROM CATHEDRAL_CURVATURE_SCAN
eigen_centroids, overlaying position, distance and bearing on the walker
view. My reading: the map must be generated from the data (not hand-placed),
the walker's live readout must be the same math as the data, and one compass
must hold everywhere.

- Data source: `watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json` (ts
  2026-09-27T01:07:39.278044+00:00, the freshest on disk; its
  eigen_centroids are byte-identical to the 0926 23:01Z scan). Five regions
  carry centroids; adventure_2d6 is OFF-MAP BY CONSTRUCTION in every scan
  (its module_id is adventure_2d6_stub, so curvature_scan's
  mods.get("adventure_2d6") misses, tools/curvature_scan.py:230-244) and is
  named on the HUD, never silently dropped.
- One convention, held in three places: bearing 0 deg = north = eigen -y,
  clockwise, `atan2(dx, -dy)` - numerically the estate's own HTML-map law
  (tools/cathedral_eigen_map.py:45-47); the HUD minimap draws -y up
  (no Y flip); `toWorld` maps eigen -y to world -Z, so walking world north
  walks map-up and the compass you read is the compass you walk.
- Referee-lawful edges (watch/inbox/REFEREE_VERDICT_20260926.md missing-edge
  ruling): the water_first chain renders only its SADDLE-SADDLE legs
  (water_computer->fractal_maze, fractal_maze->riddler_optics); NO edge of
  any kind - built, drawn or dashed - anchors on the DARK riddler_engram;
  the vote text (chain 0.031 vs star 0.036, "a VOTE, not a verdict") stands
  on the plate itself.
- The falsifier is the build: `eigenmap-two-check.py` recomputes every
  number from the JSON in Python and EXECUTES the real shipped Luau module
  under tools/bin/luau/luau.exe (sha256-verified staged copy), diffing all
  36 assertions. It caught two real bugs mid-flight before the judge ever
  ran: (1) my first cut used `math.atan(y, x)`, which IGNORES its second
  argument in Luau (verified: the CLI prints atan(1,2)=45 deg,
  atan(-1,-2)=-45 deg), collapsing every bearing toward 0/360 - fixed to
  `math.atan2`; (2) my `nearest()` broke an exact distance tie by pairs()
  hash order - fixed with a documented alphabetical tie-break.
- Sibling race named: candidate one landed EigenMap.luau + EigenMapZone.luau
  + EigenMapHud.client.luau in this same tree mid-flight. I built under
  name-disjoint files with additive init.server hooks; both builds compile
  and ship together (gate PASS, both instance sets confirmed inside
  the_mountain.rbxlx). Measured sibling fact, checkable by anyone:
  EigenMapHud.client.luau:110 (`(py1 - ey) / (py1 - py0)`) renders max +ey
  at the TOP of their minimap while their own bearing law defines north as
  -ey (EigenMap.luau:107-111, and their README bullet says
  "north = eigen -y = world -Z"), so their drawn map is 180-deg rotated
  against their own bearing readouts. Mine is coherent by construction and
  by receipt.

## Moves with estate paths

1. NEW `roblox/src/shared/CathedralMap.luau` - single authorship site:
   byte-copied 0927 centroids/class/cos/spectrum/vote; pure
   dist/bearing/compass/nearest/pairwise/chainLen/starLen (Luau-CLI
   runnable; top level touches no Roblox globals); chainEdges/hubEdges edge
   policy; toWorld/worldToEigen + plate geometry (Vector3 adapters only).
2. NEW `roblox/src/server/CathedralPlate.luau` - the walkable south plate
   (extent X -352.8..-164.4, Z 411.2..508.4; ground verified clear by
   grepping all server Vector3 positions with |Z| > 380): five beacons at
   their toWorld positions with class-colored pillar/orb + billboard (name,
   class, cos-or-null, eigen coords), chain strips breathing on tick, faint
   hub strips, vote plaque, entry() derived portal landing, beacon Touched
   filing ShadowLedger rows carrying the walker's live eigen position,
   distance and bearing.
3. NEW `roblox/src/client/CathedralMapHud.client.luau` - the walker-view
   overlay (top-left, under the sphere chip): live "POS eigen (x, y)" line,
   nearest line, five rows of dist (4dp eigen) + bearing (1dp) + 16-wind
   compass sorted by distance, "<-- HERE" within 0.0015 of a beacon (the
   position sanity anchor made player-visible), edge-clamped marker with an
   honest [edge] tag, off-map + vote footer. All numbers computed by the
   shared module; no client re-authorship.
4. `roblox/src/server/init.server.luau` - additive only: require +
   CathedralPlate.build() beside the sibling's EigenMapZone lines, one
   table.insert PORTALS row ("THE CATHEDRAL", pos derived from
   CathedralPlate.entry(), never hand-set), CathedralPlate.tick(dt) in the
   heartbeat. The sibling's lines untouched.
5. `roblox/README.md` - tree row for THE CATHEDRAL + a mesh-layer bullet
   documenting BOTH candidates (spec before behavior; single authorship
   note, falsifier path).
6. Check harness + receipts:
   `watch/inbox/ractor_panel_20260926/cands/eigenmap-two-luau-test.luau`
   (runs the real module),
   `eigenmap-two-check.py` (rerunnable judge-grade check), raw receipt
   `eigenmap-two-check.txt` (36/36 PASS, exit 0), gate receipt
   `eigenmap-two-gate.txt`.
7. Gate: `bash tools/mountain_check` run twice this session, final exit 0:
   parse-level failures 0, unique findings 8 (all pre-existing in other
   files; zero in my three), "GATE PASS: the_mountain.rbxlx rebuilt"
   (443,339 bytes). Instance names confirmed in the built artifact:
   CathedralMap, CathedralMapHud, CathedralPlate (mine) + EigenMap,
   EigenMapHud, EigenMapZone (sibling's).

## Falsifier

The judge's stated kill: an overlay position/distance/bearing sanity check
on the data. Mine is that check, run at full scale and rerunnable in one
command:

    .venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/cands/eigenmap-two-check.py

(today: exit 0, "VERDICT: PASS (0 failure(s))", 36 assertions: 5 region rows,
10 pairs x (dist + both bearings), vote chain/star reproduction vs the scan's
own descent_vote (0.0310 vs 0.031, 0.0364 vs 0.036), edge policy (exactly the
two SADDLE-SADDLE legs, nothing touches riddler_engram), 5 on-beacon zero
probes, 1 midpoint probe incl. the documented tie rule, 5 world-anchor
round-trips, staged-copy sha256 identity).

Inversion conditions, pre-registered:

- (a) A future scan moves the eigen_centroids while the module keeps the
  0927 block: the map renders stale data. Tripwire: SCAN_TS inside
  CathedralMap.luau and the SCAN constant in the check; any new
  CATHEDRAL_CURVATURE_SCAN_*.json must be diffed against them.
- (b) A judge recomputes bearing with the opposite axis (north = +y): every
  bearing then differs by 180 deg from mine. The receipt pins the formula
  (atan2(dx, -dy), the estate's own HTML-map law) with the exact per-pair
  numbers; my map and world orientation MATCH the formula, so a mismatch
  there is a convention dispute, not a data error. My build would survive a
  formula-convention check and die only under a +y-north ruling that also
  contradicts tools/cathedral_eigen_map.py.
- (c) In-Studio runtime behavior (GUI layout, CFrame.lookAt strips,
  BillboardGui, portal landing) is NOT verifiable headless; the gate's 0
  findings is type-level only. A runtime error in the HUD or plate script is
  the kill condition my bytes cannot exclude. That is the one I rate most
  likely to fire.
- Sibling inversion, for the judge's other candidate: coupling rendered-map
  orientation to bearing numbers fires on EigenMapHud.client.luau:110 (see
  Approach); their `tools/eigenmap_overlay_check.py` checks module math, not
  HUD orientation.

## Owed

- Live Studio smoke test: portal lands on the plate, HUD renders, beacon
  touches write ShadowLedger rows. Headless-verified only; named under
  Falsifier (c).
- Fold decision: two parallel eigen-map builds now ship in one tree (two
  shared data modules, two HUDs, two portals, two plates). The judge's
  kill/fold should prune the loser; my files are name-disjoint and my
  init.server hooks are four additive lines, so pruning mine (or theirs) is
  mechanical.
- queue/todo.md candidate-build block (line 164) still says the rung is
  next: two builds now exist; marking the rung done is the winner's/runner's
  pen, not mine mid-panel.
- adventure_2d6 stays off-map until curvature_scan v2 (the B2-230
  schema-version law already owns that change; renaming the stub module_id
  would silently re-baseline filed cosines).
- watch/inbox INDEX registration of these five cands-dir receipts (panel
  runner surface; not written by me).
