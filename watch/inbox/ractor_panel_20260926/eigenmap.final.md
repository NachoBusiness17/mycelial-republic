# eigenmap final (card eigenmap, ractor panel 2026-09-26, revision 2026-09-27)

Survivor: eigenmap-two. Judge ruling honored: every prong of the judge-run
position/distance/bearing check passed on two's shipped bytes (worst
render-vs-bearing deviation 0.0 deg) while eigenmap-one died on the mirrored
minimap. This revision addressed all four critique bullets; every check below
was run this session and its raw output is cited.

## Final

THE MOUNTAIN now carries exactly ONE cathedral map: the CathedralMap build
(eigenmap-two). The killed build's tree files are pruned, its record bytes
are preserved, the falsifier is repo-owned under tools/, the runtime
execution leg is landed headless, and the one thing this seat cannot do (a
live Studio smoke) is filed as a named debt with an owner and dates.

State of the tree after this pass:

- roblox/src/shared/CathedralMap.luau (header updated: sibling note became
  the fold record; falsifier citations now point at tools/)
- roblox/src/server/CathedralPlate.luau, roblox/src/client/CathedralMapHud.client.luau (unchanged bytes)
- roblox/src/server/init.server.luau: EigenMapZone require + build + the
  "EIGEN MAP" portal row removed; CathedralPlate wiring (require, build,
  entry-derived portal, heartbeat tick) is the only cathedral hook set
- roblox/README.md: mesh layer documents one build + its two repo falsifiers
  + the fold
- queue/todo.md: RUNG CLIMBED names eigenmap-two; the Studio smoke debt is
  filed under P0 THE MOUNTAIN
- tools/eigenmap_two_check.py + tools/eigenmap_two_luau_test.luau (relocated
  falsifier), tools/eigenmap_two_smoke.py + tools/eigenmap_two_smoke.luau +
  tools/eigenmap_two_smoke_env.luau (new execution smoke)
- watch/inbox/ractor_panel_20260926/cands/killed/: EigenMap.luau,
  EigenMapZone.luau, EigenMapHud.client.luau (byte-identical mv),
  eigenmap_overlay_check.py + gen_eigenmap_luau.py (original code bytes plus
  a dated [RECORD COPY] annotation), README.md (the kill record and the
  path table)
- roblox/the_mountain.rbxlx: rebuilt twice this session, final sha256
  957ef487afd2974881c2677250fe5afa62cc17281027edb3809a21aaa33e6bed,
  413,852 bytes (443,339 before the fold)

Checks run this session (commands + outcomes, receipts cited):

1. `.venv/Scripts/python.exe tools/eigenmap_two_check.py` run twice (once at
   relocation, once after all edits): VERDICT: PASS (0 failure(s)), exit 0
   both times, 36 assertions. Receipt:
   watch/inbox/ractor_panel_20260926/eigenmap-two-check.txt (the frozen
   build-time receipt cands/eigenmap-two-check.txt is untouched).
2. `.venv/Scripts/python.exe tools/eigenmap_two_smoke.py` (final run against
   the final rbxlx bytes): VERDICT: PASS (0 failure(s)), exit 0, 36
   assertions. Receipt:
   watch/inbox/ractor_panel_20260926/eigenmap-two-smoke.txt. The smoke
   EXECUTES the real CathedralPlate.luau and CathedralMapHud.client.luau
   under tools/bin/luau/luau.exe inside a stub Roblox API (staged copies
   verified: prelude + UNCHANGED tree bytes, tree sha256 identical) and
   proves: build() completes on the real path; entry() lands at the derived
   north-of-floor point (-258.6, 8.0, 387.2) matching an independent Python
   recompute; 2 chain + 2 hub strips aimed mid-edge at their far beacon;
   50 ticks breathe the chain from 0.1 to 0.148566 (inside [0.1, 0.34]);
   two beacon touches file ShadowLedger rows carrying the live eigen
   position (on-beacon: dist 0.0000; cross-beacon: 0.0066 away at bearing
   121.3, both Python-recomputed); the HUD's static map places all five
   region labels at the exact render-equation pixels with water (most -ey)
   ABOVE fractal (max ey) and the "^ N (-y)" marker pinned to the top edge;
   the heartbeat readout reads "POS eigen (-0.0236, -0.0124) nearest water"
   with the 0.0000 "<-- HERE" row. Honest scope: the on-beacon self-bearing
   is the degenerate point-to-itself direction; the receipt documents that
   0.0 vs 180.0 is the same undefined direction (atan2 signed-zero) and the
   load-bearing assertions are POS + dist + the cross-beacon bearing.
3. `bash tools/mountain_check` run twice (once mid-pass, once as the final
   receipt): both GATE PASS, exit 0, parse-level failures 0, unique findings
   8, all pre-existing LocalUnused in other files (SwarmZone,
   FrontierSouls, HardwarePrimer, IncidentDungeon, LightmapRooms, RiddleMaze,
   SpectralMaze), zero in the survivor's files. Final receipt:
   watch/inbox/ractor_panel_20260926/eigenmap-fold-mountain-gate.txt.
   Built-artifact verification (grep on the final rbxlx): instance names
   carry only CathedralMap / CathedralMapHud / CathedralPlate
   (name="Name">EigenMap count 0; the only 2 EigenMap byte-occurrences are
   the survivor's own fold-note comment in its embedded source);
   "EIGEN MAP" portal 0; "THE CATHEDRAL" portal present; sourcemap.json:
   EigenMap 0, CathedralMap 1.
4. `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`:
   FAIL overall with 7 NEW hits, ALL in other lanes' concurrently modified
   files (tools/ledger_lock.py:136, tools/openrouter_free_gate.py:84,
   tools/probe20_run.py:421, tools/queue_dupes_check.py:33,
   tools/secret_gate.py:570, tools/transport_precheck.py:134,
   tools/visor.py:250); zero hits in this pass's files. That debt belongs to
   the lanes that own those files; not accepted here.
5. Byte-preservation proof for the killed tools: Python compare of record
   copies vs originals before removal - eigenmap_overlay_check.py code body
   identical after an 11-line annotation, gen_eigenmap_luau.py after 7 lines
   (originals then removed from tools/).

Not run, and said so: a live Roblox Studio smoke. This seat has no Studio
and the estate has no Studio automation (tools/cathedral_smoke.js is a
static parse of an HTML page, not Studio execution). That leg is the filed
debt below. The full `pytest -q` suite was launched and its outcome is
recorded in the Critique addressed section, debt bullet.

## Critique addressed

Bullet 1 (in-Studio runtime leg unverified; land a Studio smoke test or file
the debt with an owner and a date): BOTH, split honestly. Filed:
queue/todo.md P0 THE MOUNTAIN gains "- [ ] [roblox] THE CATHEDRAL live
Studio smoke" with OWNER (the operator's Studio session, the only Studio in
the estate, same gate as the Studio publish item), filed date 2026-09-27,
re-check by 2026-10-04 (the repo's 7-day staleness convention), and the
exact closing procedure (portal, HUD render, beacon touch, ledger row in
Studio output). Landed: the headless execution smoke (check 2 above) that
converts "parsed but never executed" into "executed under stubs" for every
named surface: BillboardGui creation (billboards and labels are real
instance trees the driver counts and reads), CFrame strips (lookAt from/to
verified against JSON-recomputed world anchors), portal landing (entry()
diffed against the derived formula), and ShadowLedger touch rows (two rows
with live eigen position/dist/bearing diffed against Python). What stubs
cannot cover (real GUI layout, physics Touched, DataStore durability) is
named in the debt, in the smoke's docstring, and in its receipt scope note.

Bullet 2 (fold the tree; prune the killed candidate's files; rebuild so the
estate carries exactly one cathedral map): pruned EigenMap.luau,
EigenMapZone.luau, EigenMapHud.client.luau from roblox/src (moved
byte-identical into cands/killed/, not deleted: the killed candidate's rows
are records); removed one's init.server.luau hook lines (the EigenMapZone
require, the EigenMapZone.build() block with its comment, and the "EIGEN
MAP" PORTALS row with its comment) and one's README bullet; rebuilt
the_mountain.rbxlx via the gate (check 3) and verified the built artifact
carries zero EigenMap instances and the survivor's three. Two judgment calls
inside this bullet, both annotated: (a) one's tools (eigenmap_overlay_check.py,
gen_eigenmap_luau.py) were also taken off the repo surface - they
hard-reference the pruned module, so keeping them in tools/ would leave a
permanently broken repo check; their bytes live in cands/killed/ with a
dated annotation. (b) the rbxlx rebuild leaves exactly 2 EigenMap byte
occurrences, both inside the survivor's own fold-note comment; that is the
annotation law working, not a missed prune (the tripwire asserts on
instance names, not comment bytes).

Bullet 3 (re-author the shared surfaces; RUNG CLIMBED must name the
survivor): roblox/README.md's mesh-layer section now has ONE eigen-map
bullet (the CathedralMap build) citing both repo falsifiers with their
commands and receipt paths, the Studio debt pointer, and the killed build's
record location; the EigenMap bullet is gone; the world tree diagram already
described only THE CATHEDRAL and stays. queue/todo.md's RUNG CLIMBED
(line 171) now reads "(ractor eigenmap-two, 2026-09-26/27)" and the block
carries the fold annotation (one was the originally named climber, killed on
the mirrored minimap, bytes preserved in cands/killed/) plus the new
falsifier paths; the stale "both are in the rebuilt rbxlx" sentence is gone
because it is no longer true. Repo-wide sweep (grep EigenMap / EIGEN MAP /
eigenmap_overlay_check / gen_eigenmap over roblox/, tools/, queue/todo.md):
only the survivor's fold-note comment, the smoke's own tripwire code, and
nothing functional.

Bullet 4 (move the falsifier into the repo the way candidate one did):
eigenmap-two-check.py relocated from
watch/inbox/ractor_panel_20260926/cands/ to tools/eigenmap_two_check.py
(snake_case, the tools/ convention; the only deltas are the ROOT/TEST/RECEIPT
paths and a provenance note in the docstring) and its driver to
tools/eigenmap_two_luau_test.luau with the require path fixed for the new
location. Rerunnable from the repo and rerun: PASS twice (check 1). The
README, the CathedralMap.luau header, and the RUNG line all cite the
tools/ path; the receipt now lands at
watch/inbox/ractor_panel_20260926/eigenmap-two-check.txt. The panel's frozen
build-time receipts in cands/ are untouched.

Debt / not done, stated plainly:

- Live Studio smoke: NOT RUN (no Studio in this seat; see bullet 1). Filed
  with owner and dates.
- `pytest -q` (the repo's run-before-claiming-done law): launched this
  session on the shared, heavily-concurrent working tree; finished in
  2548.87s (0:42:28) with 34 failed, 2260 passed, 9 skipped (sum 2,303 =
  the 2026-09-27 census denominator). Attribution is bounded and stated:
  the command's output capture kept only the final summary plus 4 FAILED
  lines (tests/test_water_computer.py x3, tests/test_wave_driver.py x1,
  none eigenmap-related); the .pytest_cache lastfailed read 12 entries from
  a CONCURRENT lane's interleaved run (the box runs several pytest
  workloads; two instruments at two moments, per the census denominator law
  never differenced) - zero entries in either set touch eigenmap, the
  roblox tree, mountain_check, or any file this pass changed (also
  grep-verified against tests/ before the run). The 34 failures are
  pre-existing/concurrent-lane state, not claimed as mine or fixed.
- The ratchet's 7 NEW hits are other lanes' concurrent debt (check 4); this
  pass registers no baseline updates.
- The panel cands INDEX registration remains the panel runner's surface
  (the survivor card's own Owed note); this pass did not write INDEX.json.

## Decision for the estate

The fold is now machine-checked, not just ruled: eigenmap-two's CathedralMap
is THE cathedral map, and any future second build trips a rerunnable
tripwire (`tools/eigenmap_two_smoke.py` fails if an EigenMap instance
re-enters roblox/src or the built rbxlx, if init.server.luau rewires an
EigenMap module, or if the killed build's tools reappear on the repo
surface). Concretely, this card closes:

1. The two-build ambiguity under roblox/ is closed: one map, one portal,
   one HUD, one falsifier pair in tools/.
2. The card's pre-registered risk (c) is narrowed to exactly the Studio-only
   residual (GUI rendering, physics Touched, DataStore durability), owned
   and dated in queue/todo.md; the headless-executable part of that risk is
   discharged by the smoke.
3. The RUNG (queue/todo.md ladder rung "eigen-map = the world map") is
   climbed by the surviving build and the todo no longer credits the killed
   one.

One decision this card does NOT make: whether the estate ever builds Studio
automation so debts like this stop needing an operator session. That is an
operator-scope call (it implies a Roblox Studio install + tooling on a fleet
box), recorded here as a question, not a change.
