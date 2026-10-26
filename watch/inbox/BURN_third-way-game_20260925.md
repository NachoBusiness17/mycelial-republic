# BURN receipt: third-way-game — 2026-09-25

## Verdict
steal

## Evidence
- "Resolution stays 2d6, pass on 7: the grace distribution lives in the same curve the whole game already rolls." (STORYTELLER_SIX_RACTOR_20260925.md)
- "Optimizable faith is failed faith." (same file, F6)
- The existing playtest's score currency is VM, and its gates are a table: "Summit touch → +50 VM", "key-holders fell him → +500 VM", "Median minutes in the Ossuary ≥ 3". (roblox/docs/PLAYTEST.md)
- Stub canon: "Total ≥7 succeeds at ordinary tasks"; river_ford north is "a glass door, impossible, leading into a keep of clear pipes", invariant loops to water_computer.gallery. (adventure_2d6_stub.v1.json)
- Web read (IndieKlem, 2025-02-06): standard mitigations are marble bag ("The final results will always be the same, but the order in which they appear will vary"), streak breakers ("may exploit it to their advantage"), hidden rerolls, seeds. The Unpeeked Seed must use NONE of the first three or the pure 2d6 curve is broken.
- OWED: gamedev.net "Luck in Games: Why RNG Isn't the Answer" returned HTTP 403. Not read, not synthesized.

## Steal or Vacuous
Steal. PLAYTEST ADDENDUM, appended after "The Wave" in roblox/docs/PLAYTEST.md:

### Third Way Initiation (one pass, 20 minutes)
- 0-3 Act I entry: spawn at the Guttered Lantern (six chairs), sit the Administrator chair, hear the war-is-a-service telling, sign one faction, temple broadcast plays, sentiment meter visible.
- 3-8 war loop: kills feed the shared VM pool, broadcast repeats, author one counter-media post; the meter must visibly move (F5).
- 8-12 the Wall: both faction passes refused; the walk option appears; toll paid, no fight offered.
- 12-15 the Door: glass door at river_ford north; the riddle's answer is 42 and asks for the question; open on 2d6, pass on 7.
- 15-20 Act III: grace shrine rents the Drive (visible Improbability spent), take the Vow, receive the Unpeeked Seed, walk the Pilgrim path, die once ("so it goes"), endgame ledger shows the pool abolished for all players (F7).

Score gates (the pattern's actual metric is session VirtueMarks, the number its gates table already scores):

| Gate | Target | Your number |
|---|---|---|
| Pilgrim net VM vs war net VM, two seed-matched runs | within 15% (F1) | |
| Counter-media sentiment delta | > 0 (F5) | |
| Grace roll sequence, run A vs run B, same seed | identical | |
| Vow log lines in Output | every Vow | |

Vow instrumentation, printed to Output and appended to the ledger row (DEATH-CAPS precedent):
`VOW-TAKEN seat=<name> t=<mm:ss> vow=<id> price=<vm> improbable_spent=<n> seed=peeked|unpeeked`

Seed audit: run the session twice on the same hourly seed (Flicker Tower precedent); log every grace roll as `GRACE t=<mm:ss> d1= d2= total= pass=`; the two sequences must match roll for roll, and totals ≥7 must sit at the 2d6 rate (15/36, about 41.7%) with no smoothing. Marble bags, hidden rerolls, and streak breakers inside the Seed each break the canon curve and count as peeking.

## Falsifier
Pre-registered: F1-playtest: in two seed-matched 20-minute runs, if Pilgrim net VM falls outside plus-or-minus 15% of war net VM, the Pilgrim economy is re-priced before any expansion. Seed falsifier: any divergence between the two same-seed roll sequences voids the Unpeeked Seed claim; the shrine ships as peeked until fixed.

## Bibliography
- watch/inbox/STORYTELLER_SIX_RACTOR_20260925.md (read)
- corpus/game_estate/FROM_MUD_TO_WOW_20260914.md (read)
- memory/game_modules/adventure_2d6_stub.v1.json (read)
- memory/game/FLOW_IMAGE.json (read)
- roblox/docs/PLAYTEST.md (read)
- https://indieklem.substack.com/p/18-how-to-design-better-randomness (fetched 2026-09-25)
- https://gamedev.net/tutorials/game-design/game-design-and-theory/luck-in-games-why-rng-isnt-the-answer-r3877 (OWED, HTTP 403)
