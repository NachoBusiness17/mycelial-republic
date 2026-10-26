# MOUNTAIN_build (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# THE MOUNTAIN build-out pack, wave 2 + Primer v0

**Citation convention.** The evidence carries no line numbers. Every code claim below is cited as a quoted byte-run with its file (README = `roblox/README.md`, FINAL = `watch/inbox/ractor_panel_20260926/eigenmap.final.md`). Anything I could not quote is marked **UNVERIFIED**.

**Run state.** Nothing in this pack has been run. Every number is either an analytic identity or something the smoke recomputes independently (Python or JSON recompute, same method as the existing check). No measured number is relied on except one: the plate entry point `(-258.6, 8.0, 387.2)`, cited from FINAL (instrument: `tools/eigenmap_two_smoke.py`, final run 2026-09-27, headless stub env under `tools/bin/luau/luau.exe`, tree sha256 identical to the built artifact). The smokes recompute it, so it is context only.

## 0. Common frame

**Tree (README layout).** Cathedral modules sit at `roblox/src/shared/CathedralMap.luau`, `roblox/src/server/CathedralPlate.luau` and `roblox/src/client/CathedralMapHud.client.luau`. Services sit at `src/server/ShadowLedger.luau`, `src/server/NpcGateway.luau` and `src/shared/KSpace.luau`. The five zones follow the CathedralPlate precedent: `roblox/src/server/<Name>Zone.luau`. Where the existing Wave zones live is **UNVERIFIED** (README names `zones_extra` but quotes no path). Requires are by name, so a folder move costs no code.

**Evidenced organ surface (the only calls this pack assumes exist):**
- `CathedralMap.pairwise()`: "freezes the 10-pair distance/bearing table".
- `CathedralMap.toWorld`: "maps eigen -y to world -Z".
- `CathedralPlate.build()` and `CathedralPlate.entry()` (FINAL: "entry() lands at the derived north-of-floor point").
- `KSpace.nearest(pos)` and `KSpace.drift()`: "`drift()` is the angular error between a claimed heading and the beacon".
- `ShadowLedger.disposition()`: "SESSION-SCOPED by design".
- Beacon Touched handlers "filing ShadowLedger rows" (FINAL). The row-writing function name is **UNVERIFIED**.

**Unverified organs.** `LedgerExchange` and `SphereKinship` appear in the CONTRACT but in none of the evidence bytes. Zone 5 consumes them only through an injected adapter (below). The landing seat must grep their real signatures first and edit only the adapter.

**Dependency injection rule.** Every zone is `build(deps)` where `deps = {CathedralMap, CathedralPlate, ShadowLedger, KSpace, ...}`. Zones never `require` organs at module top-level paths the stub cannot resolve. This is what makes the headless smoke possible.

**Row-filing adapter.** `deps.file(player, kind, payload)`. In production it calls the same function the CathedralPlate beacon handler calls (**UNVERIFIED name**, must be mirrored byte-for-byte). In the smoke it appends to a list.

**Unlock chain.** The Primer sets the Player attribute `PrimerUnlock_<ZoneModuleName> = true`. Session-scoped only, consistent with the disposition law. The durable record is the ShadowLedger row. An unlock does not survive a rejoin; the page is shown again.

**Smoke harness (shared).**
- `tools/wave2_smoke.py` is one driver.
- `tools/wave2_<zone>_smoke.luau` is one test per zone.
- All reuse the prelude `tools/eigenmap_two_smoke_env.luau` (file name evidenced; its full stub surface is **UNVERIFIED** beyond what FINAL names: BillboardGui, CFrame lookAt, Touched, ShadowLedger rows). Each test appends a zone-local stub block and never edits the shared prelude.
- The driver stages prelude + unchanged zone bytes, runs `luau.exe`, and prints `PASS/FAIL` per assertion plus `VERDICT: PASS (0 failure(s))`.
- Receipts go to `watch/inbox/mountain_wave2/<zone>-smoke.txt`, in the style of the existing receipt.

## 1. FIVE ZONE SPECS

### ZONE 1: THE SCRIPTORIUM (the Primer's in-world reader)

**Module:** `roblox/src/server/ScriptoriumZone.luau`. It reads `roblox/src/shared/PrimerPages.luau` (data, section 2).

**[MECHANIC]**
- A lectern stands 8 studs south (+Z) of `CathedralPlate.entry()`, so it is anchored to data and not hand-placed. The plate is entered from the north of the floor, and `toWorld` maps eigen -y to world -Z.
- `build()` creates a RemoteEvent `PrimerShow` and the lectern part.
- A player (the operator, in v0) sends a page code `Pnn-cc`.
- `show(player, code)` does the following:
  1. Parse and validate against `PrimerPages`. Reject bad checksum, unknown page, or a locked-out sender.
  2. Resolve region: a fixed region key, or for `@walker` pages `deps.KSpace.nearest(walker position)`.
  3. Compute the page coordinate with `toWorld(region centroid)`. The centroid comes from CathedralMap; the page table never stores eigen numbers (no second truth).
  4. Spawn a marker Part 12 studs above that coordinate with a BillboardGui caption.
  5. File a ledger row `primer_page` carrying `{page, region, walker eigen, dist, bearing}`, using the same dist/bearing function the HUD readout uses. If that function is local to `CathedralMapHud.client.luau` (**UNVERIFIED**), the seat lifts it into `CathedralMap` as a move, not a rewrite.
  6. Set `PrimerUnlock_<zone>` from the table.
- Rate limit: 5 bad codes inside 10 s locks that player out for 30 s, so a RemoteEvent cannot be brute-forced.
- Page `P00` (title) draws `CathedralMap.pairwise()` as a billboard and unlocks nothing.

**Positive:** `P01-xx` valid -> marker at the water centroid, row filed, `PrimerUnlock_TideStairZone` set.
**Negative:** a code with a good page number and a wrong checksum -> no marker, no row, no attribute.

**[SMOKE] `wave2_scriptorium_smoke.luau`, 8/8**
1. `build()` creates RemoteEvent `PrimerShow` and a lectern whose Position equals `entry() + (0,0,8)`.
2. A valid fixture code for page 1 returns ok with region `water`.
3. A bad checksum is rejected: zero rows, zero attributes.
4. An unknown page is rejected: zero rows.
5. A valid page 1 sets `PrimerUnlock_TideStairZone == true` on the stub player.
6. The `primer_page` row's dist and bearing equal an independent Python recompute using `tools/cathedral_eigen_map.py`'s formula (README: "bearing 0° = north = eigen -y (the `tools/cathedral_eigen_map.py` formula"). Fixture walker eigen and centroid are passed by the driver.
7. Showing page 1 twice files 2 rows and leaves the attribute true, not toggled.
8. With the stub clock injected, 5 bad codes then a valid code inside 30 s is rejected. After 31 s it is accepted.

**[STUBS CANNOT COVER]**
- The real lectern TextBox GUI and ProximityPrompt rendering.
- RemoteEvent network behavior and client spoofing.
- DataStore durability of the row.
- The real marker's look at distance.

### ZONE 2: THE TIDE STAIR (water region)

**Module:** `roblox/src/server/TideStairZone.luau`

**[MECHANIC]**
- Nine slabs climb from the plate entry toward the water centroid, along the line `entry -> toWorld(water)`. Water is the northmost region, so slab Z strictly decreases with k.
- Tide `L(t) = 4.5*(1 + sin(2*pi*t/24))`, a 24 s period, range 0 to 9.
- Slab k is dry iff `L(t) < k`. Low slabs are flooded most of the time and high slabs are almost always dry.
- Stepping on a flooded slab files `tide_drown` and `PivotTo(entry())`.
- Slabs 1-5 are open to all. Slabs 6-9 require `PrimerUnlock_TideStairZone` (page P01). The top slab files `tide_summit` once per session.
- Reuses `deps.CathedralMap.toWorld` and `deps.CathedralPlate.entry`. Feeds ShadowLedger rows.

**Positive:** hop slab 5 at t=0 (L=4.5 < 5, dry).
**Negative:** slab 4 at t=0 is flooded (4.5 is not < 4), so the player is returned to entry.

**[SMOKE] `wave2_tidestair_smoke.luau`, 7/7**
1. `build()` makes `Slab1..Slab9` with Y ascending and Z strictly descending, and slab 9's offset from the line toward `toWorld(water)` is 0.
2. `tideLevel(0)=4.5`, `tideLevel(6)=9`, `tideLevel(18)=0`, each within 1e-9.
3. `dry(5,0)==true` and `dry(4,0)==false`.
4. Over 24000 samples, `dryFraction(k)` for k=1..8 matches the analytic `(asin(2k/9-1)+pi/2)/pi` within 0.002.
5. Slab 6 `onStep` returns "locked" without the attribute and allows with it.
6. Stepping slab 9 while dry files exactly one `tide_summit` row, and a second step in the same session files none.
7. Stepping a flooded slab files `tide_drown` and the stub character's pivot equals `entry()`.

**[STUBS CANNOT COVER]**
- Physics Touched actually firing on slab contact.
- Real humanoid fall and respawn feel.
- Tween smoothness of rising and sinking slabs.
- DataStore rows.
- Jump-reach feasibility between slabs (Studio playtest only).

### ZONE 3: THE FRACTAL DESCENT (fractal region)

**Module:** `roblox/src/server/FractalDescentZone.luau`

**[MECHANIC]**
- Five rooms in descent at `toWorld(fractal centroid)`; fractal is the southmost region (max ey), so it sits at +Z.
- Each room has radius 64 and a door ring with `8 * 2^(d-1)` doors (8, 16, 32, 64, 128). Arc spacing therefore halves each depth, and depth 5 is about 3.14 studs.
- At depth d the target bearing is `(base + 137.5*(d-1)) mod 360`. `base` is the bearing from the plate entry to the fractal centroid, on the HUD compass.
- The player claims a heading by passing through a door. The verdict is `KSpace.drift(claimed, target)` if its signature matches (**UNVERIFIED**), else a 3-line local angular difference.
- Pass iff drift <= half the door spacing, i.e. only the nearest door. A slip files `fractal_slip` and resets to depth 1.
- Depths 4-5 require `PrimerUnlock_FractalDescentZone` (page P02). Completing depth 5 files one `fractal_floor` row carrying the five drifts.

**Positive:** the door at index `round(bearing/(360/count))` passes.
**Negative:** the adjacent door is exactly 2x the tolerance, so it always fails, at every depth.

**[SMOKE] `wave2_fractal_smoke.luau`, 7/7**
1. `build()` yields 5 rooms, all radius 64.
2. `doorCount(d)` is 8, 16, 32, 64, 128.
3. `arcSpacing(d+1)/arcSpacing(d) == 0.5` within 1e-12 for d=1..4.
4. `targetBearing(d)` matches the Python recompute for a fixture base, for d=1..5.
5. The truth door passes and the +1 and -1 doors fail, at every depth.
6. Depths 4 and 5 deny without the attribute and allow with it.
7. A slip resets to depth 1 and files `fractal_slip` with `{d, drift}`. A full clean run files exactly one `fractal_floor`, whose 5 drifts are each <= half spacing.

**[STUBS CANNOT COVER]**
- Door Touched physics.
- Whether a 2-stud avatar can pass a 3.14-stud arc gap at depth 5 (Studio-only; if not, the cap is depth 4 and only constants change).
- Real room collision geometry.
- DataStore rows.

### ZONE 4: THE ISOLATE (riddler_engram, the DARK anchor)

**Module:** `roblox/src/server/IsolateZone.luau`

**[MECHANIC]**
- A sealed chamber sits at `toWorld(riddler_engram centroid)`, with four pylons for the other regions placed at their real world positions.
- The README law is "No edge - drawn or built - anchors on the DARK riddler_engram (referee ruling; it stands isolated)". The zone builds no bridge or beam to the chamber. This is a design pillar, and the smoke enforces it.
- The puzzle comes from data: touch the four pylons in ascending order of `CathedralMap.pairwise()` distance to riddler_engram. A wrong touch resets progress (`isolate
