# FRONTIER SOULS — buildable canon v1 (from Adam's bible, 2026-09-15)

Full intake: `watch/inbox/FRONTIER_SOULS_INTAKE_20260915.md`. Spike: `dashboard/static/games/frontier_souls.html` (+ `scripts/test_frontier_souls.js`, 49 lanes).

## Souls messages (2026-09-16, THE WEAVE W3): the dead leave words
Async template-word messages, bounded by legal vocabulary — that is what makes them trustable. A message = 3 indexes into 3 fixed pools (`SOULS_LEX`: danger / verb / tail, 8 words each → 512 legal messages, zero free text; the save format itself cannot carry prose, so there is no moderation surface and no invention). Compose UI on `C` during play (world holds, like the sign draft): A/D or 1/2/3 pick the slot, W/S cycles the word, E posts — **costs nothing**, binds player x/y/facing/run into the ledger (`fs_souls` localStorage; entries validated by `validSouls` on load; FIFO cap 60). Signs seed into **later runs only** (`m.run < G.runs`) at the exact recorded spot, plank leaning along the author's facing; which signs appear (cap 12/run) and their order come from the W1A fleet seed stream (`hash2(id*7 + runSeed*131, cell)`), so **same seed → same words in the same order**. Standing with a sign reads it: glowing text, a chronicle line, +4s of soul timer. Harness lanes 43–49.

## Mud-steals round (2026-09-15, "this is pretty basic — steal our mud stuff")
Chronicle panel (DF log writes itself) · procedural names + grudges (named survivors hunt faster) · THE DESERT REMEMBERS (fs_lore localStorage: rolls→snakes read your roll, range-kills→cowboys strafe, close-kills→packs grow) · SIGNS level-up draft (8 omens, world pauses; Dead Man's Hand, Preacher's Last Word, Rattlesnake's Secret…) · dynamite-tossing gang leaders · THE COMBINE (two wounded cowboys → THE DEPUTY, mud's ractor-tavern rule) · whiskey bullet-time orb · one rewind per run (T on death) · prospector's cache (key → box → mod+essence+whiskey) · quicksand patches · damage numbers · wake-on-sight + linked pack wake · pairwise separation.

## The two clocks (Adam's law)
| clock | drives | implementation |
|---|---|---|
| **radial distance** | level ring (1–6) + rim | rings every 420px from world center (0,0); canyon pit = ring 1 (r<420, 4 passes); rim r≥2520 = Death arena |
| **total steps** | event scheduler + pressure | 24px walked = 1 step; event thresholds roll `rng < chance` (FTL rule: may not appear at all) |

Direction never matters — only distance from center and steps from start.

## Constitution (from Adam, non-negotiable)
1. PERMADEATH — death = wake in canyon with a scrap of soul (keep ~12 essence, nothing else; unlocks persist only).
2. EVERY ENEMY CAN BE THE END — all damage through one `hurt()`; tumbleweed kills the careless.
3. MAKE THE PLAYER FEEL SMART — unreachable items, closing paths, chest seen from afar.
4. Gritty + bloody, NOT cartoonish; Arizona hue (grays/browns); minimal audio — wind, rattles, shots, one boss sting.
5. Death timer — soul fades constantly; Soul Essence is the only fuel (and XP, and currency → real choices).

## Tables (v0 numbers, Adam-tunable)
Fauna: tumbleweed (invulnerable, contact 6) · rat (invulnerable, bite 4, **steals essence orbs**) · scorpion (hp14, lunge-sting 8, jinks) · rattlesnake (rattle warn ≤170, strike ≤60: 50% instakill / 26, dodge i-frames save, hp12 tiny) · coyote pack ×4 (surround slots → pounce, hp10) · cowboys (leader hp55 or 3× lackeys hp16, telegraphed shots) · lone gunman (5% events, duel, drops fire-rate mod).
Events (step-keyed): oasis (safe r90, heal + full timer) · wishing well (free level, once) · merchant (mod 60 SE / essence pack 25 SE) · stranger's grave → journal → hermit (+25 maxHp) = storyline chain 1 of 4.
Mods recolor shots: fire #e05038 burn · storm #bcd8f0 chain · heavy #d8c890 ×1.6.
Starters: ALLZABAN (fast 7dmg/0.22s/235spd/90hp) · MARROW (mid 16/0.45/195/120) · NELL (heavy 34/0.8/160/150 — strongest, slowest). Names MARROW/NELL provisional.
Death: hp550, scythe sweep (0.7s telegraph, 34), daggers at range, coyote summons at 66/33%.

## Open for Adam (blockers on his word, not code)
starter names · meta-progression ruling (instinct: no / StS: yes — spike keeps unlocks only) · 3 more storylines · faction mechanics · gun frames vs mod slots · jump as distinct verb?
