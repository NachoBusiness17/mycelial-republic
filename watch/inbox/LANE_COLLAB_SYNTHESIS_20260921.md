# LANE COLLAB SYNTHESIS — genre steal wave, gophers + ractors per lane (2026-09-21 night)
**Schema:** lane.collab.v1 · **Run:** dwfrun-90c648ff · 7 lanes × (1 gopher research + 1 ractor adversarial rank)
**Honesty note:** gophers researched from model knowledge (no web fetch, per ask); ractors could not read game source from their workspace — plug-ins anchor to the ask's state surface (score, spice, lineMult, thump, thumpers, P.vx/vy, worm.segs, gates, kifu). Licenses mostly "unknown" (recalled) except where marked. Final implementation happens against the real files in games-site/ + memory/game_modules/.

## swarm-arena (Vampire Survivors / Geometry Wars / Downwell / Nex Machina / Crimsonland / Brotato / Devil Daggers / Robotron)
1. (S) **Decaying kill multiplier** (Downwell + Nex Machina): kill sets lineMultT = 2.5 + depth*0.25; decay to 0 resets lineMult; contact zeroes it. Converts turtling into forward pressure.
2. (S) **Dash + i-frames** (Nex Machina): 3x impulse 0.15s, P.inv 0.25s, enemy contact skipped while inv; renders as a fading streak.
3. (M) **Door-gated perk drops** (Crimsonland): rare spiceCache behind breakable doors; Kabuki guaranteed to drop one. Speed decision, not friction.
Rejected: Brotato shop (UI/currency treadmill, rewards hoarding); Geometry Wars spring grid (polish, no mastery, O(cells) cost).

## arrakis-ride (THPS2 / Tiny Wings / OlliOlli / Alto / SSX / Excitebike / Burnout / Tux Racer)
1. (S) **OlliOlli landing-angle window**: flat landing keeps speed, lineMult +1, spice bonus; nose-dive scrubs P.vx ×0.55 and drops the chain. Every landing a skill check.
2. (S) **Burnout near-miss = wormriding**: within 90px of worm.segs or a thumper shockwave at speed → boost chunk + 25×lineMult (per-source cooldown). The optimal line threads the danger — the Dune fantasy.
3. (S) **SSX spins-fuel-boost + Excitebike overheat**: air spin progress charges boost; heat rises while boosting, bogs the board when overheated (soft scrub, not stall). Closes the self-charging exploit.
Rejected: Tux Racer wholesale GPL port (viral license + L-effort duplication — skeleton already exists).

## ruins-tomb (Into the Breach / Tomb of the Mask / NecroDancer / Chip's Challenge / Hoplite / Sokoban / SSR / HLD)
1. (M) **Hoplite movement-as-attack**: move into an enemy = kill; tile beyond free = leap-kill. Routing IS combat; feeds lineMult + kifu.
2. (S) **Chip's Challenge K-of-N gates + ice tiles**: gates demand a spice count (route economy: full-board sweep); ice re-issues velocity until a wall (~10 lines).
3. (S) **Into the Breach telegraphs**: damage number + shove arrow drawn one turn ahead; shove-into-hazard = damage-free kill; worm.segs segments become shove-able.
Rejected: Sausage Roll orientation blocks (design-time scope creep — kills the speed/chain loop).

## mud-text (Zork / Colossal Cave / Achaea / DF adventure / ADOM / MUSHclient / NetHack / Evennia)
1. (S) **Zork compound commands**: split on ';' and ' and ', expand all/except, loop through the existing executor — typing density becomes the core skill, each clause pays lineMult.
2. (S) **MUSHclient speedwalk**: '3n 2e d u' expands into a queued move list drained one per tick through the gates lookup; wrong step clears the queue.
3. (S) **ADOM corruption**: spice-burning increments a corruption counter; tier 1 tints text, tier 2 raises worm homing, tier 3 stamps 'tainted' on the run's kifu — power as a wager.
Rejected: MUSHclient regex triggers (auto-fire removes typing = the lane's core loop; degenerate lineMult farm).

## arena-field (Marble Madness / Neverball / Osmos / Particle Mace / Zuma / Log!cal / Powder Toy / Oscilloscope)
1. (S) **Oscilloscope phosphor trails**: translucent fade fill instead of clear — every marble path stays visible; the readability layer that makes all chaining judgeable.
2. (S) **Marble Madness fall-line bonus**: marbles aligned with the field gradient gain speed + score×lineMult — tilt itself becomes the scored skill.
3. (M) **Particle Mace comet leader**: the whipped head marble shatters steppers above a speed threshold — tilt skill becomes an earned weapon.
Rejected: Osmos feed-the-well (steering spends your own payout — taxes the win condition).

## cathedral-world (The Witness / Outer Wilds / Majora's Mask / Riven / Baba Is You / Tunic / A-LttP / NetHack)
1. (M) **The Witness one-stroke kifu-trace glyph gates**: pointerdown→stroke buffer→resample; compare order-sensitively against the gate glyph; refusal routes through the bucket-refusal path; clean trace = score += 100×lineMult, trace polyline appended to kifu.
2. (S) **A-LttP world-toggle**: doctrine.waterFeedsField as a flippable world boolean; one mid-chain gate tests it at door-time — flipping forces a route back, recontextualizing earlier rooms (~30 lines).
3. (S) **Majora's Mask kifu-cycle speedruns**: the loop-closes gate pays 250/cycles against your own recorded best chain — replaying known routes faster is the mastery economy.
Rejected: Baba Is You pushable rule-tiles (a second game: 150-300 lines of push-resolution edge cases; the reversible clause is captured 1/20th the code by #2).

## slope-skifree (SkiFree canon / Alto / Tiny Wings / Tux Racer / Doodle Jump / Ski Master / Dune! / SSX)
1. (S) **Ski Master gate-thread combo**: threaded paired gate → lineMult +0.25 (cap ×4) + 0.8s speed surge ×1.3; pole hit or miss resets — two existing systems fused into one risk line.
2. (S) **Alto/Dune! tree near-miss credit**: under skim radius without collision → lineMult +0.1, score bump, one-frame "CLOSE!" — every obstacle becomes a risk/reward bead.
3. (S) **Milestone yeti chase waves**: at each score threshold the chaser's speed = player speed × 1.1 + 40×wave, decaying after you outrun it 5s — panic sprints on schedule.
Rejected: Tiny Wings heightfield pump (needs a terrain/camera/collision rewrite before the first point of fun — the seductive one dies).

## Cross-lane notes
- lineMult is the load-bearing state: five lanes' best grafts pay through it.
- Every winner is S-effort except two M's (swarm door-perks, cathedral trace gates, ruins Hoplite, arena comet).
- Rejections recorded with reasons — the ractors' kill list is part of the value.
- Coverage gap: gophers researched from model knowledge; license fields unverified; ractors judged against described mechanics, not source. Implementation pass happens against the real files in games-site/ + memory/game_modules/.
