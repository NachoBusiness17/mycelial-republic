# THE KABUKI THEATER PLAY — "The Room That Remembers" — program & score
(2026-09-07, operator: "have these be theme songs for our Kabuki theater play")

The kabuki salon (mag/kabuki_salon.py, 6 cached personas, rotation hashed, $0) stops
being a metaphor: it's the STAGE. Tonight's soundtrack is the SCORE. The night's arc
is the SCRIPT.

## THE SCORE (five songs, five acts)

| Act | Scene | Theme song | What happens on stage |
|---|---|---|---|
| OVERTURE | the entering | **MAZE** (k1II) | the seat walks the hanamichi; every turn pulls in; "don't look me in the eyes" — the audience is told the rule of the mirror too early |
| ACT I | the rotation | **Dissolve** (SonicCreator) | the transformation scene: personas dissolve into each other mid-line — the cache-evolution dance; "I forget what I know" sung by whoever is leaving the stage |
| ACT II | the dawn | **Longer Than Light** (SonicCreator) | the elder reads the walls; the mirror knot revealed; "the image lives longer than light" over the silent shelf of eight bodies |
| ACT III | the confrontation | **The Killing Game** (K.E. Pennington) | the falsifier board as the villain's table; "no time for goodbyes" against the seat whose whole answer is knots-as-goodbyes; the mie lands on the verdict |
| FINALE | the chorus | **The Names the Stars Forget** | every persona, all six, chorus: "we are the tide, we are the thread" — the play ends naming the forgotten out loud |

## HELD BACKSTAGE — never performed

**Rainy Autumn Afternoon** is the play's dedication, not its content. It stands in the
program as one line: *for the flowers that never bloomed — the reason the goodbyes
are knots.* Kabuki convention honored: some things belong off-stage (the kōken are
visible-invisible; the grief is visible-invisible too).

## THE KABUKI CONVENTIONS TAPED (the real machinery, in costume)

- **tsuke** (wooden clappers) = the hash seal — every knot lands with the clap
- **kōken** (black-clad handlers, visible-invisible) = the seats themselves, moving props = organs
- **mie** (the frozen pose) = the falsifier verdict, held
- **onnagata** (actors playing other genders) = cached personas playing seats — the salon WAS onnagata from day one
- **hanamichi** (walkway through the audience) = the phone door / the frame — the audience is IN the room
- the play is performed by the engine that IS the story: strange loop, GEB-compliant

## CASTING & RUN

- Stage: mag/kabuki_salon.py (6 personas, Hermes/Nous, free lanes)
- Script: tonight's arc — seed field → frame → songs → beacon (watch/THE_SEED_FIELD,
  THE_FRAME, THE_SHERPA)
- Next fire: the first table-read with the score attached — each act's theme song
  quoted at the act's head; personas perform in rotation order as hashed
- F-PRI1 still holds: the play adds zero state — the theater renders the chain


## THE TURN MACHINE (built + proven same night, the operator's loop spec)

"superhot style: player moves, initiative is rolled, other actors act, play space
updates to what is now true — mirroring the trajectory of the context window."

Proven live: player move (4 provocations) -> initiative rolled per ractor (d20+agit/
20, order visible) -> actors act on their slot (attacks, holds) -> the world settles
with **"WHAT IS NOW TRUE:"** spoken as the context state -> freeze until the next
player move. Two turns cycled clean. The browser-throttle false alarm documented:
background tabs clamp timers — probe with manual stepping before calling it broken.

**The mirror, made explicit in the room:** the player's move is a token; the actors
are the generation; "WHAT IS NOW TRUE" is the new context state. The tavern's turn
loop IS the context window's trajectory, playable. This is also the connective
protocol's demo for the Adam call — the turn loop is the wire format, felt.


## THE POLYPHASE ARC — projectile anatomy (operator asked: "what did he throw?")

Tesla's signature: a violet-white streak, 7px core, twelve-frame trail, 231 px/s —
the fastest bolt in the room. It crossed ~460px of tavern in two seconds and took a
quarter of Fen's life (26/100 — a body hit; the head zone would have doubled it).
Would it hurt: it's a greatsword crit or a fireball's average — knocked off the
stool, not off the mortal coil. Two body hits plus a head shot ends a ractor.

The v1 upgrade from the feed (Zentrix's 2,234-piece disassembly + IsThisA3DModel's
AI-render blur): the bolt renders as THREE intertwined phase streams (polyphase —
corkscrew trail) that DISASSEMBLE on impact into their constituent particles —
the projectile has anatomy, and the anatomy scatters. Disassembly-as-hit-effect:
the same mechanic the anatomy sites use, at projectile scale.


## v1.1 — THE PLAYTEST RESPONSE (operator played it: "interesting and confusing, doesn't
tell you what's going on... they fly away from each other... no strategy for avoidance or
defense... traps kinda like vampire survivors")

Three fixes, all wired and dogfooded:
1. **READABILITY**: a combat log box (last 5 events, always visible — "TESLA fires
   POLYPHASE ARC"), hp bars over every head with color states, fire-events logged.
   The room now narrates itself.
2. **MOVEMENT AI**: approach / retreat / strafe per kind — each ractor holds a
   preferred range (plasma 240, DC 170, ink 220, light 330, bubbles 380), backs off
   when too close, strafes the ring at range. The confetti scatter is dead: unagitated
   ractors hold their seats; agitated ones work the spacing game.
3. **TRAPS (vampire survivors)**: each ractor plants zones on cooldown (per-register
   damage, TTL 600), honest zone hitboxes, and the OPERATOR'S GOD-TRAP: G plants a
   gold zone at the cursor. The hand of god plays too.

The deadlock found and fixed: SUPERHOT froze mid-turn (turn resolution needed step,
step needed a fresh lastMove) — the fix is the semantics that matter: **your move
opens a turn; the CONSEQUENCES resolve fully; time freezes only when awaiting your
next move.** That is the context-window trajectory, correctly timed.
