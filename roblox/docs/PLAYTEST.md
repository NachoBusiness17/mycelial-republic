# PLAYTEST.md — the Studio session script

**2026-09-25 · Headless pass done (tools/luau_lint.py; audit
fixed the Ossuary solid-rock maze bug, the double-sided border gaps, the
misaligned Court gate, the sentinel CFrame:Lerp static-call, the Swarm
nine-pellets-per-pull spam). REFRESHED 2026-09-26 (burn lane B2-120, trust
bytes not hand-written counts): the live run reads "checked 43 files, 3 with
findings" (was 21 files clean at the 2026-09-25 pass); the 3 are the
zones_extra block-balance advisories (FrontierSoulsZone 39 vs 36,
HardwarePrimerZone 25 vs 24, IncidentDungeonZone 26 vs 25), classification
owed to B2-119 triage (real imbalance vs the python-heuristic
keyword-in-string false positive). This is the human pass: 20 minutes, in
order, pass/fail every line. Failures go straight to queue/todo.md.**

## Headless tripwire (spec 2026-09-26, B2-31; filed BEFORE the luau_lint change)

tools/luau_lint.py carries two advisory disease checks so the two cured
classes cannot silently return. Both run on comment/string-stripped source,
both are advisory output in mountain_check step 1 (the gate prints them;
luau-lsp stays the authoritative parser):

1. POLL (t56/t63 disease): a while/for loop body containing both a
   GetAttribute call and a task.wait(n) with n <= 10 at the same closure
   depth (neither read nor wait nested in an inner function, so event
   closures like Touched handlers do not trip). Cures to mirror:
   init.server.luau leaderstats signal bindings (t56), MudBasecamp garden
   label signal bindings plus deadline wakeups (t63). Receipts:
   watch/inbox/gala_20260925/afterparty/lanes/t56.check.txt, t63.check.txt.
2. RMW (t74 disease): GetAsync and SetAsync called in the same function
   body; the lost-update shape t74 cured. Durable writes go through one
   UpdateAsync (roblox/README.md ShadowLedger durable write law).
   HeadMuseum flushSoul/restoreSoul are separate write-only/read-only
   functions and must stay clean. Receipt:
   watch/inbox/gala_20260925/afterparty/lanes/t74.check.txt.

Zero findings expected on the cured tree 2026-09-26; verified before the
check landed and named in the B2-31 receipt.

## Setup (once)

1. `rojo serve` in `roblox/` → Studio → Rojo plugin → Connect.
2. Game Settings → Security → Allow HTTP Requests ON; API Services ON.
3. `python tools/roblox_npc_gateway.py` in a terminal (heads alive).
4. Play (F5). Keep the Output window open — server "speech" prints there in v1.

## The pass (in order; every line is a check)

### Spawn + Basecamp
- [ ] You spawn at Basecamp; the room ring is visible; plaques read room names.
- [ ] Hall of Shared Supper: 6 chairs, Vellum ball present.
- [ ] "Sign the Grant" prompt → Output prints Vellum's offer. VirtueMarks attr unchanged.
- [ ] "Count the empty chairs" → VirtueMarks +1, red wisps spawn and chase; they kill on touch.
- [ ] Death → Output prints the DEATH-CAPS line. Respawn is ~1s (Tower law).

### Head Museum
- [ ] 7 skulls on pedestals, nameplates correct, seat plaques behind them.
- [ ] "Speak" on THE ELDER → gateway answers live (in persona, 1-3 sentences).
- [ ] Stop the gateway process → "Speak" again → first line + "(a recording)".
- [ ] Restart gateway → live again. (No fabrication law, verified both ways.)

### Ledger Exchange (Steal-a wheel)
- [ ] Marble Run rail south of camp; artifacts ride it left→right with price billboards.
- [ ] Buy a common (50 VM) → it lands in a Slot attribute; VM deducted.
- [ ] Wait 10s → ExchangeIncome ticks; VirtueMarks grows by slot income.
- [ ] Steal: run to another player's alcove (needs 2 clients: Test → Clients and Servers, 2 players) → "Borrow" only when their lock is off → your speed drops, abilities stop (fire Z: nothing), their alcove announces the theft.
- [ ] Run home, touch your pad → loot stashed; victim's lock timer +10s.
- [ ] Counting Circle locks your alcove for 60s → Borrow prompt does nothing while locked.

### Swarm
- [ ] Arena light pulses at 122 BPM (visibly "breathes" twice per second).
- [ ] Horde fills the floor; density ramps; touch = death.
- [ ] Z fires ONE pellet per press (not a stream) → kills a unit, unit vanishes.
- [ ] Gems spawn; walk into one → SwarmScore jumps; with the pet orb (after rebirth) gems collect from ~12 studs.
- [ ] 5-kill streak → the plaque announces a taunt line.

### Arrakis
- [ ] Board seat works; speed feels fast; spice chains build a multiplier.
- [ ] Crest ramp at speed → you fly; land clean.
- [ ] The Maker hunts the fastest rider, and ALWAYS telegraphs first: red column ~2s, then breach knock-up at that exact spot.
- [ ] X (ThumperToss) drops a thumper → the Maker retargets it.
- [ ] Gate touch banks chain × speed into ArrakisBanked.

### Flicker Tower (was Light Maze)
- [ ] 8 sections, seeded; the tower differs next round (hourly seed).
- [ ] No checkpoints: fall → 1s respawn at the BASE (this is the Tower law; feel the rage).
- [ ] Flicker bridges: solid 60% of their cycle; kill arms rotate; arms kill on touch.
- [ ] At the 4:00 mark → a bully wisp per player.
- [ ] Summit touch → +50 VM, ledger records "topped the Flicker Tower".

### THE OSSUARY (the seasonal spearhead — most eyes here)
- [ ] Darkness is real: your torch radius is most of what you see; fog close.
- [ ] Maze is OPEN: corridors exist, walls have gaps, every cell reachable (the
      pre-fix build was solid rock; walk 3 corridors to confirm).
- [ ] Sentinel in view → bone-white and STILL. Look away (turn camera) → it
      turns hunting-red and glides at you. Turn back → freezes again.
- [ ] Pumpkin braziers light pockets; Candy Bones give +2 VM (×2 with doubler).
- [ ] Floor 2: bone lever flips two wall positions (corridor state change).
- [ ] Floor 2: boulder rolls down a corridor every ~20s; touch = death.
- [ ] Bone Key pickup → Court gate (wood, in the border gap) opens for you.
- [ ] Skeleton King: key-holders fell him → +500 VM, candy rain, he rises after 30s.
- [ ] Without the key, touching the King kills you.

### The Answer (summit)
- [ ] 5 phases, prose advances per phase.
- [ ] Fold wave: jump it (airborne = untouched) or C (Wing Chun Redirect, 1.5s
      window) → the wave turns around, boss loses a phase, label says so.
- [ ] Phase 3+: the strike telegraphs a 15° lean.

### ShadowLedger crossing probe (B2-174 2026-09-26; replaces the B2-10 P3 two-uid falsifier)

The B2-10 P3 as originally written (two uids cross one portal, stop, rejoin,
both rows persist) cannot detect the t74 lost-update class at all: two uids
are two different keys, so there is no per-key race and even the pre-t74
GetAsync+SetAsync bytes pass it (B2-30 sim S4,
watch/inbox/burn_wave_20260926/B2_30_shadowledger_live_20260926.md). The
Sep-29 run gates on this sharpened probe instead:

- [ ] SAME-UID probe: one player uid crosses one portal on server A, stop,
      rejoin on a DIFFERENT server (server B) the SAME UTC day, cross the
      portal again; then read `p<uid>_<UTCday>` in ShadowLedger_v1: BOTH
      "took the portal" rows must persist (2 rows). One row = lost update =
      t74 absent from the running build. (This is the only shape that puts
      two writers on one key.)
- [ ] Mixed-fleet residual (S4b): while ANY server still runs pre-t74 code,
      its late SetAsync can clobber the fixed server's row; until the whole
      fleet is on the 08:28-or-newer build, a missing row is not proof of a
      client bug, it is the S4b clobber. Check the server build banner
      before scoring a failure.

## Score the session

| Gate | Target | Your number |
|---|---|---|
| Median minutes in the Ossuary | ≥ 3 | |
| "I knew why I died" moments | every death | |
| Clip-worthy beats seen | ≥ 2 (freeze flip, candy rain) | |

Anything broken: one line per failure into queue/todo.md P0, then fix, then
re-run just the failed section. The Sept 29 soft-launch gate is this whole
page passing once, clean.

### The Wave (zones_extra — one pass per zone, 2 minutes each)
- [ ] Each of the 11 wave portals teleports and the zone builds (a warn in Output = that zone's build fault-isolated, file it).
- [ ] GALLERY: Voronoi doors re-seed on prompt; fish orbit; tile field flips.
- [ ] FRONTIER SOULS: boss tells ~0.5s before lunges; soul timer drains on death.
- [ ] TOY BOX: bite telegraph ~0.35s; roll through → walker stuns; riposte window.
- [ ] HARDWARE PRIMER: predict-then-measure console; beacon obeys the brightness law.
- [ ] INCIDENT DUNGEON: correct diagnosis opens each room's barrier; 4/4 opens THE RUN.
- [ ] MAZE ARENA: 4 rounds escalate (moving walls, walking light, dwell scoring).
- [ ] SPECTRAL MAZE: riddle gates accept the answer via chat; 2 misses reveal hint.
- [ ] RIDDLE MAZE: sight collapses the twin-slit field; eraser pad re-mixes; prism pays +50.
- [ ] LIGHTMAP ROOMS: five lights orbit casting real shadows; FOLD ring records you.
- [ ] EROSION FIELD: brush paints, marbles roll and abrade, banked grain counts.
- [ ] STEER FIELD: sagents climb the gradient toward your lamp on the 66ms tick.
