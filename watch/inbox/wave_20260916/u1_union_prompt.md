# U1 worker prompt — union-alpha drafts toy.html

You are drafting a single-file browser game, `toy.html`, ~200 lines, no external dependencies.
It is a minimal strip of a larger game whose "souls grammar" is already shipped. The core verb
is the i-frame roll: READ a telegraph → ROLL through the swing → PUNISH the recovery.
Everything below is law. Output ONLY the full contents of toy.html in one fenced code block.

## Constants (exact, do not tune)

- Player: hp 100, stamina 100 max, regen 25/s (x0.5 while moving/rolling, x1.5 while still, regen only when attackT<=0 and rollT<=0), speed 160 px/s, r 12.
- Roll: key ShiftLeft held (edge-checked internally so one press = one roll), costs 30 stamina, sets rollT=0.28, rollCd=0.5, iframes=0.35, moves 420 px/s in movement direction (or facing if no movement key), cancels nothing else. No roll unless stamina>=30, rollT<=0, rollCd<=0.
- Swing: Space (just-pressed), costs 15 stamina, attackT=0.18, attackCd=0.35, arc range 55+r in facing direction (90-degree arc). No swing unless stamina>=15, attackCd<=0, rollT<=0. Damage 14 * (0.9 + 0.2*rng()).
- Walker (the only enemy): hp 40, speed 70, dmg 14, r 14. Chases the player when aggro (aggro from spawn). At distance < e.r+player.r+4 with attackCd<=0 and no live windup: set windup=0.35, attackCd=1.2, telegraph=0.35 AND log a "telegraph" event. While windup>0: windup-=dt, velocity *= 0.12 (it plants); when windup hits <=0: if distance < e.r+player.r+10 then if player.rollT>0 log "hit_dodged" + walker.stun=0.8 + player.riposte=1.0, else log "hit" and hurtPlayer(dmg). attackCd ticks down always.
- Riposte: if player.riposte>0, swing damage is doubled, then riposte=0.
- Walker stun: while stun>0 it does not move or attack.
- Player death: hp<=0 -> state "dead". Win: walker hp<=0 -> state "win", log "kill".
- Arena: 480x300 world, walls at the borders (player and walker clamp inside with radius). No other geometry.

## RNG law (replaces Math.random entirely)

Seeded LCG, no Math.random anywhere: `state = (Math.imul(state, 1664525) + 1013904223) >>> 0`.
Seed: an integer chosen at start. Every draw increments drawIndex. First draw has drawIndex 1.
Expose rng() returning state/4294967296.

## Determinism law

- Fixed timestep only: the simulation advances ONLY via pump(n) calls, dt fixed at 1/60 per step. No requestAnimationFrame in the simulation path (rendering via rAF is allowed but must be skippable headlessly).
- No Date.now, no performance.now, no Math.random in any simulation-affecting path.
- Input tape: `TOY.tape` is an array of [frameIndex, code, isDown] applied at the START of the pump step whose 0-based frame index matches. Both tape input and live keyboard go through the SAME internal press(code)/release(code) functions. Log an event {t, e:"input", code, down} for every applied input (tape or live).
- Just-pressed flags (like mud's keys[CODE+'_p']) must clear at end of each pump step.

## Event log (order-preserving, every entry {t, e, ...})

- {t, e:"input", code, down}
- {t, e:"telegraph", enemy}
- {t, e:"roll"}
- {t, e:"swing", riposte:boolean}
- {t, e:"hit", dmg}            // player took damage
- {t, e:"hit_dodged", enemy}
- {t, e:"kill", enemy}
- {t, e:"end", verdict}        // "win" or "dead"
t is simulation seconds (frame * dt), rounded to 3 decimals.

## P-LEGAL law (the invariant)

You are never hit without a telegraph you could have rolled through.
The receipt field hits_no_telegraph counts "hit" events with no immediately preceding matching
telegraph (same enemy, telegraph.t + 0.35 == hit.t within 0.001). It must be 0 for every run.
Implement the check inside the receipt builder, not by hand.

## Receipt (toy_play.v1)

TOY.receipt() returns an object:
{schema:"toy_play.v1", seed, draw_index, frames, inputs:[[frame,code,down]...], events:[...],
 hits_taken, hits_no_telegraph, verdict, duration_s, sha256}
- sha256: include a compact synchronous sha256 implementation (hex string) hashing the canonical
  JSON of the receipt WITHOUT the sha256 field, keys in the fixed order listed above,
  JSON.stringify with no spaces. Expose TOY.sha256(str) too.
- TOY.canonical() returns that canonical JSON string (receipt minus sha256 field).

## Headless contract (CI drives this — exact names required)

Expose window.TOY with: start(seed), pump(n), keys (the live key object), tape (settable array),
player, enemies, G (state incl. time, state), events, draws (draw index), receipt(), canonical(),
sha256(str). start(seed) fully resets the world and the LCG and clears events.

## Browser shell

Minimal canvas (scaled x2), one walker at x=360 y=150 aggroed, player at x=120 y=150,
walker hp bar, stamina bar, red flash on the walker while telegraph>0, dark arena.
Keyboard listeners call the same press/release internals as the tape. No tutorial, no text walls.

## Style

~200 lines, dense, terse comments only where the souls grammar lives. No frameworks, no build.
