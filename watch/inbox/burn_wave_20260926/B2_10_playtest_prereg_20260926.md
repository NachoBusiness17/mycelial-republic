# B2-10 Sep-29 Roblox playtest prereg (2026-09-26)

## Verdict
PREREG BUILT, RESET-DAY RUN GATED. One red finding: the shipped place file
`roblox/the_mountain.rbxlx` (mtime 2026-09-26 01:10) predates the final src
edits of commit 790145ab1 (01:11 to 01:20) and provably lacks four landed
fixes: t74 ShadowLedger UpdateAsync, t67 derived join, t63 garden signals,
t72 GalleryZone annotations. Proven against build bytes by grep, not mtimes.
Sep-29 opens with P0 (rebuild gate) before any play. This lane modified no
roblox server code.

## Evidence
- Build stale by content: grep "UpdateAsync" in the_mountain.rbxlx = 0 hits;
  "GetAsync(key)" = 1 hit (the old two-call write). Current
  `src/server/ShadowLedger.luau:59`: `store:UpdateAsync(key, function(old)`
  with copy-then-append transform :60-65. The t74 receipt
  (afterparty/lanes/t74.check.txt) admits "NOT verified against a live
  DataStore (no Studio publish from this lane)".
- "annotation exactness" = 0 hits in the rbxlx; live at
  `zones_extra/GalleryZone.luau:41,56` (t42/t72 mk returns Part).
- t46 tint IS in the build: "Gate_" = 11 hits (= 11 WAVE zones).
  `ZoneGate.luau:49` gsub("%W","_") matches `init.client.luau:116` same gsub;
  tint table `init.client.luau:108-111`.
- leaderstats t56 in build ("Sole Summit_ writer" = 1 hit):
  `init.server.luau:233-240` signals; Summit_ census: only
  `LightMazeZone.luau:155-156` writes Summit_ (grep over src).
- Candy cap in build: `OssuaryZone.luau:241`
  `local CANDY_PER_FLOOR_DAILY_CAP = 6` (t2 receipt).
- Alliance check from generated data only (RegionSpheres.luau +
  SphereKinship.luau): 130 spheres x 11 regions = 1430 pairs, opposed = 0,
  allied = 162. `ZoneGate.luau:17-22` "opposed is unreachable today" holds.
- Deterministic draws (SeedRng uid*7919, one xorshift32 step, int(1,130)):
  uid1=LOYALTY, uid2=WAR, uid3=LOYALTY, uid4=TREACHERY.

## Work done (prereg wave: test / pass / falsifier per item)
- P0 rebuild gate. Run `bash tools/mountain_check` from repo root. PASS =
  "GATE PASS" line + rbxlx rebuilt. Falsifier: after rebuild grep rbxlx for
  "UpdateAsync" (expect >= 1) and "GetAsync(key)" (expect 0); either miss =
  stale build shipped.
- P1 tint. Solo (uid 1, LOYALTY): soul chip reads "Sphere: LOYALTY
  (independent)" and ZERO wave pads tint (independent tints nothing, a
  negative is a fact). Clients-and-Servers client 2 (uid 2, WAR): INCIDENT
  DUNGEON pad leans green (RGB 90,230,130 at lerp 0.45), the other 10 do
  not. Falsifier: any other tinted pad; a red pad anywhere (data-proven
  unreachable).
- P2 leaderstats. Player list shows Virtue Marks / Rebirths / Invariants /
  Summits. Count chairs -> Virtue Marks +1 same frame (no 1s poll lag);
  tower summit -> Summits +1 once per round. Falsifier: a stat updates one
  visible tick late = the t56 poll crept back.
- P3 ledger race. Two clients cross one portal; stop, rejoin: both "took
  the portal" rows persist under key p<uid>_<UTCday>. Falsifier: a row gone
  = lost update, t74 absent from the running build.
- P4 Basecamp. Plant a plot -> "growing... 30 min left"; label flips at the
  deadline wakeup or on prompt re-engage; death prints the DEATH-CAPS line.
  Falsifier: countdown frozen through its deadline.
- P5 Gallery. "Walk the doors" cycles 12 named doors with banner seed
  change; fish orbit; field flips; Pause holds a frame. Falsifier: repeated
  seed or static fish.
- P6 candy cap. 7th CandyBone on one floor, same day: +0 VM. Falsifier: it
  pays.
- P7 `roblox/docs/PLAYTEST.md` full pass remains the Sep-29 script; this
  prereg gates it; failures land in queue/todo.md P0.

## Falsifier
Whole prereg falsifies if P0 passes but P1-P6 drift from the numbers above
(computed from generated data, not guessed): more than 2 drifted items with
no named cause means the afterparty fixes were parades; the run receipt
says so.

## Bibliography closed
AFTERPARTY_CLOSE_20260926.md; GALA_MORNING_AFTER_PREREG_20260926.md;
roblox/README.md; roblox/docs/{PLAYTEST,WORLDGEN_MINE}.md; the_mountain.rbxlx;
src/server/{init.server,ZoneGate,ShadowLedger,MudBasecamp,OssuaryZone,
LightMazeZone}.luau; zones_extra/GalleryZone.luau; src/client/init.client.luau;
src/shared/{Config,SeedRng,Worldgen,RegionSpheres,SphereKinship}.luau;
tools/mountain_check; afterparty lanes t1a,t2,t42,t46,t56,t59,t63,t67,t74;
memory/burns/LEDGER.jsonl tail.
