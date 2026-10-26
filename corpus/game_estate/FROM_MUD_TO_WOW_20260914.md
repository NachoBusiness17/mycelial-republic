# FROM MUD TO WORLD OF WARCRAFT — the ramp, the gap, and the second lantern

*Written 2026-09-14, from a fifty-wide audit sweep: thirteen witnesses across five lanes — gaming corpus, prior research, the audit record, memory, and synthesis — plus a seven-shape salon held before the first word was written. Every claim below is tri-state: VERIFIED (a file or URL was opened), PLAUSIBLE (a source we trust but did not open today), or UNVERIFIED (named as such). The witnesses' reports are annexed beside this document.*

---

## The cold open: a distant cluster is one thing

A week ago someone tweeted about the Barnes-Hut algorithm — the trick that turns quadrillions of gravitational calculations into a tree. The best reply on it said: "The brute-force answer is every particle pulling on every other particle — quadrillions of sums, each one correct, none of them the answer. The tree is the recognition that a distant cluster is one thing: one center of mass standing for a whole branch."

We didn't know it yet, but that reply was the thesis of everything we built this week, and the thesis of this article. A game engine that refuses to compute every pairwise collision. A memory system that stores the center of mass of a hundred sessions instead of the sessions. A dungeon whose far corners are one dark thing until your torch resolves them. And a plan — the plan this article exists to audit — that treats World of Warcraft not as a thing to clone but as a distant cluster: one center of mass standing for twenty years of other people's engineering, which we can approximate long before we can ever reproduce it.

This is the gap analysis that was asked for. It is also, because the salon insisted, an interrogation of the ask itself. Page one of that interrogation follows. Everything after is the honest answer.

---

## Part I — Where we actually are

Start with bytes, because the first law of this house is trust bytes, not reports.

The flagship is **MUD**: a single HTML file, 57,636 bytes, one inline script, zero network calls. It runs by double-clicking. Inside it, verified line by line by an auditor this morning:

- **Torch-light vision with wall occlusion.** A 270-pixel attention radius; a visibility polygon raycast against every wall segment; soft radial falloff; torch flicker. Enemies outside the light are not dimmed — they are not drawn. Walls carve hard shadows. Verified: lit pixels dropped from 40% to 21% the hour it shipped.
- **A Barnes-Hut quadtree.** Every frame, all enemies are inserted into a spatial tree; every enemy folds the tree with the θ-criterion and receives one gentle push from any cluster that is too far away to count individually. Verified under a 150-enemy flood: 62 frames per second, the swarm visibly spread.
- **SUPERHOT.** A powerup that makes the world move at 6% speed while you stand still and full speed while you run. Time is your movement. Verified numerically: idle enemy drift 0 pixels, moving enemy drift 31.5, player movement 140 — in the same window.
- **The dragon cascade.** Kill the First Dragon and it shatters into K8 whelps; each whelp shatters into sixteen K3 sparks. At Ascension 2 that is ten whelps and twenty sparks from one boss.
- **An Ascension ladder** borrowed from Slay the Spire: twenty levels, persisted across deaths, scaling enemy health, damage, spawn pressure, and cascade counts.
- **A learning horde.** A persistent JSON blob remembers how you play. Twelve far-away kills and the spitters start mining your escape routes. Survive swarms and packs start hunting as one — and the fast ones stop chasing where you are and start leading where you're going.
- **D&D class enemies.** Rogues that approach in stealth and backstab for double when you're not looking. Clerics that heal the horde and kite *you*. Battlemages that telegraph ground-fire. Rangers that volley three arrows with line-of-sight checks.
- **Boon drafts.** Level up and the game pauses: three cards, three gods, press 1/2/3. Twelve boons — chain lightning, knockback, wider torch, crits, death clouds, speed, longer SUPERHOT, lifesteal, thorns, berserker, wide arc, roll-refresh.
- **A puzzle vault.** A brass key and a chest spawn far apart in the dark; a chime rings when you're within earshot of something valuable. Twin pressure plates latch an ancient mechanism that grinds a vault gate open — a real wall, occluding real light, until it doesn't.

That is where we are. It is more than anyone expected a week ago, including us. And it is — per the salon's attacker, verified this morning — still "a single-player diorama wearing a MUD's coat." The entire durable state of the flagship is two localStorage keys. Zero network primitives in 1,487 lines. The name is a promise the build has not yet kept.

Hold that. It's the axis everything else turns on.

## Part I½ — The people the doors are for

A gap analysis without a demand side is a map of nowhere. The sweep asked the socratic question — who are these people, and what do they actually want — and the answer is no longer hypothetical, because this week three of them walked in.

**Melissa** is a writer finishing the third book of a series, with a Drive folder organized for every world she's building, and a proposal on the table: she helps with the writing, someone else helps with the "coding bsht." Her door is the one this house built first without knowing it: the Character.AI persona patterns, the Maya presence rules, the dungeon NPC sheets — all of it exists so that a writer's words can become a creature's behavior without a compiler touching her hands. Her specific ask is a world: "Skyrim-ish but in my book's world." Under the ramp doctrine, that is not a distraction — it is the mud tier wearing someone else's canon, which is how LPMud grew: authors brought worlds, the engine stayed out of sight. The onboarding page built for her this week says the honest thing: she will never touch code. She writes the world; the world gets built around her text.

**Marque** is a builder who arrived carrying his own version of the same idea — he built his tools, avoided the house's stack for a while, and just shipped a game of his own, zipped, with a sentence underneath that should be read twice: "these games are going to be mapped to AI, and I'm working on some real crazy stuff." His door is the shelf: every game here is a single self-contained HTML file, and his can ship the same way with his name on it. The sweep's audit of the sibling games proves the shelf standard is real — five games, one file each, all playable — so his games are not a favor; they are inventory.

**Adam** is player one — the person the whole lead-in doctrine was written for, whose door opens at a game and only later, if ever, at the machinery. The past week's work — the torch, the boons, the dragon that shatters — is his onboarding, and it is also the first real test of the doctrine that onboarding should be one click and no syllabus.

And there is a fourth door, unlabeled: **the fleet itself**. The cohort lens in the salon pushed the extension one step past the ask — the first cohort of the multi-user dungeon may not be humans at all; it is the fleet's own seats, dropping into the dungeon the way they drop into everything else, with the verkle chain as the shared ledger that makes agent-versus-agent state trustworthy. Whether a shared world needs anyone else in it to be shared is a genuinely open question, held here tri-state.

Why this matters to a gap analysis: every "edge" in the later sections is an edge *for someone*. The torch is an edge for Explorers. The boon draft is an edge for Achievers. The chime in the dark is an edge for Socializers — the sound of someone else's world being near. The learning horde is an edge for Killers, turned back on the Killer. The taxonomy is not decoration; it is the reason the next month of work goes to the doors that are already being knocked on.

---

## Part II — The honest audit of it

The salon met before this article was written — seven shapes, blind divergence, tri-state claims. Its attacker wrote the sentence that frames Part II: *"the ask flatters itself in three places, all checkable."* Checked they were, by a dedicated audit witness. The verdicts:

**The name is a promise, not a fact.** VERIFIED: no WebSocket, no fetch, no EventSource, no XMLHttpRequest anywhere in the file. Two localStorage keys — `mud_lore` (four counters and flags) and `mud_asc` (an integer). The gap between that and "multi-user dungeon" is not a gap; it is the entire distance from a diorama to a world. Everything between two localStorage keys and shard state is the actual paper this article walks.

**The victory-lap risk is real, and the house convicted itself first.** The game's own founding document, written in August, confesses in its honest-gaps section: "the GAME is not actually being coded — I drifted into infrastructure." An article mining the percolator, the lanes, the rib bus and the verkle chain is in danger of being that drift wearing a promotion. The salon's Seat-0 ruled on it: the article is permitted only if named as what it is — a mirror — and only if page one interrogates why the fleet prefers documenting ramps to walking them. Part XI is that page. This whole article is the named mirror.

**And five bugs the audit found that we had not:**

1. **The deployed site ships a two-day-stale game.** The build script copies MUD from the wrong directory — a top-level stale twin (31,348 bytes, Sep 12) instead of the canonical 57,636-byte build (Sep 14). One line to fix. Until it's fixed, everyone who plays on the website is playing the version without the torch, without the learning horde, without any of Part I. CONFIRMED by byte comparison on both trees.
2. **The boon filter is dead code.** `!b.max` is always true because no boon defines `max`, so taken boons are never excluded — Apollo's torch and Hermes's speed stack without limit, every level-up, forever. Balance bug; probably unintended, given the dead filter was clearly meant to gate.
3. **Boon picks fall through to weapon swaps.** Press 1 or 2 to take a boon and the same frame silently swaps your weapon. Digit 3 escapes only because the game has two weapon slots.
4. **Mines laugh at SUPERHOT.** The mine-laying roll is per-frame, not per-tick — spitters lay at full rate inside frozen time, and mines tick on slowed dt, so they outlive the window that was supposed to make them fair.
5. **Ascension is a one-way ratchet past its own ceiling.** The twenty-level ladder caps the `a` term but not the loop term, so ng40 enemies are still climbing — while the cascade at ng20 wants 1,568 sparks cleared against a 100-health player. Full clear required.

Also found, smaller and worth saying: the "hidden" rogues render at full opacity because the draw code never reads their stealth flag — they're only invisible when the torch isn't reaching them, which makes stealth flavor, not mechanics. Walkers chase in straight lines through walls the vision system treats as opaque — occlusion is cosmetic, not tactical. The lore save fires on every far kill. The swarm accumulator serializes into the save blob with no schema version. The Barnes-Hut tree is built from pre-move positions, so every push is one frame stale and biased by the enemy's own mass.

None of these kill the game. All of them are the difference between "built" and "finished" — and the house law, older than this week, already knew: built is not verified-working.

## Part II½ — The class kits, in full

The four classes shipped in the fifty-wide wave, described the way a player meets them — and the way their counter-play works.

**The Rogue (violet).** It approaches in stealth, rendered at near-invisibility, and its AI watches one thing: the dot product of your facing against the line from it to you. If you are not looking, the approach accelerates and the backstab lands for double damage, with the number popping in violet so you know it was rude. After the stab it unstealths, retreats for two seconds, and vanishes again. Counter-play: keep it in your facing cone; swing at the shimmer when the torch flicker bends wrong. Discovered edge: because the draw code never reads the stealth flag, rogues outside your torch radius are invisible *for free* — the stealth matters most exactly at the edge of the light, which is the best bug-as-feature this codebase has produced.

**The Cleric (green).** The reason fights stop being wins. It holds 200 to 380 pixels of range, strafes, and every three seconds heals the most-wounded ally within 220 pixels for eighteen percent of that ally's maximum health, with the number popping green. The counter-play is a target-priority decision, which is the first time MUD asks *who* you kill instead of *how many*. Verified live: a walker dropped to thirty percent climbed back to forty-nine under clerical care.

**The Battlemage (violet-magenta).** The area-denial caster. It telegraphs a ring at your current position — nine-tenths of a second of red geometry telling you where not to be — then detonates for twenty, and the ground keeps burning for two more seconds. It punishes the thing SUPERHOT rewards: standing still. The tension between the two systems is a design discovery the audit did not plan.

**The Ranger (gold).** Three-arrow volleys in a twenty-five-degree spread, fired only with line-of-sight — the ranger checks your torch's occlusion before shooting, which means walls are cover against volleys but not against sightless chasers. It holds range like a cleric and retreats like one too.

Arrival schedule by Ascension: loop one adds a rogue and a cleric; loop two adds the battlemage and the ranger; loop three doubles up. Each also scales on the same damage curve that makes the base horde hit harder — the classes are not gimmicks layered on top of the difficulty; they are the difficulty, wearing class clothes.

---

## Part III — How we got here: the engine chronology

The witnesses reconstructed the timeline from commit hashes, dated manifestos, and a flow ledger. It tells a story about the order in which things should be built, and about the gap between that order and the order that actually happens.

**August 7 — the engine predates the game.** The oldest committed game module is the campaign engine: a server-authoritative world with Infocom-style verbs. Before there was a game, there was a place for one to run.

**August 11 — the mandate.** The operator declared the primary deliverable: a lead-in game that solves the agent's own work, entertains, and creates a user base — "once you're a game it goes vertical with adoption." That day produced the vertical-adoption plan and Stone One: persona recall — the world's inhabitants recount what happened while you were gone, told from the memory chain.

**August 13 — the doctrine day.** One day, five builds: the entry gate (walk forward and a building appears), the intent-gated world render, the complexity ramp (tabletop → MUD → roguelite, each tier perfected before the next), a DFHack-style overlay so the agent can drive the game, and the work loop that folds real tasks into dungeon rooms. The same day's log confesses the drift — the game is not being coded, the infrastructure around it is.

**August 14 — it became playable.** A command-line seam: status, play, map, render, descend. Movement fixed so "go hall" reaches the hall. The first driver rib filed.

**August 19 — memory and faces.** A saga memory for running gags, a creative dungeon master on a local model, and the invariant NPCs — eight curated souls plus twenty-three auto-spawned witnesses of discovered invariants. The eight curated ones have names — Mira, Calcifer, the Cartographer — and the auto-spawned ones are generated from discovered invariants of the fleet's own operation, which means the NPC roster is a portrait of the system's habits. A game whose monsters are your own repeated behaviors is either pretentious or inevitable; the honest answer this week was both.

**The drift, in full.** The story triage document from August 15 preserves the night that taught the doctrine: of twenty swarm turns attempted, sixteen failed outright and fifteen of them returned empty text. The prescription was four shelves — a play log keyed by room, an object bible, outline-as-geography, and a return constraint — which is a polite way of saying the storytelling had no state, no canon, and no way home. The movement lantern failing "because the forgetting held it," recorded in the hero journey document the same period, is the same lesson in narrative clothes: the layers that were not load-bearing did not survive the night, and what survived is what got engineered. Every system listed in Part I exists because its absence was felt at three in the morning by someone too stubborn to stop.

**September 14 — the browser MUD surfaces, and the fifty-wide sweep audits it.** Between those dates, the honest ledger records only tabletop-tier work ever flowing: nomic patches, a diplomacy piece, a pandemic exercise. The roguelite tier exists as a depth counter. The adoption loop exists as a sentence. And the sweep found the ledger's newest entry is a failed enqueue — the machine's own answer to "what's next" was, for a few hours, nothing at all.

The chronology's lesson is the doctrine's lesson, learned the hard way and written down the same week: perfect each tier before climbing. The witnesses found the ramp scaffolded but the tiers still shallow — the tabletop tier is three canned verbs, the ramp-MUD is a hardcoded three-room dict that ignores the real one, the roguelite is flavor text over an import that never fires. The ramp exists; the complexity hasn't ramped. That is not a failure — it is a map. It says exactly where the next month of work goes.

---

## Part IV — The memory underneath: what the verkle chain actually is

The game's authority story needs a memory to sit on, and the house has one: an append-only, hash-linked record the fleet calls the verkle chain. The witnesses audited it, and the audit is a masterclass in what a name promises versus what bytes deliver.

What it is: one JSON line per committed knot — a session dossier. Each row carries a timestamp, a filename whose *path is the address* the payload can be read back from, a leaf hash, a session id, an index, a parent root, a verkle root. Each knot's root becomes the next knot's parent root. Change anything old and every later root breaks. The current tip — root plus leaf count — sits in a 507-byte file. Eight thousand two hundred and forty-seven leaves, backed by roughly thirty thousand payload files.

What it is not, honestly: it is not a real verkle tree — no polynomial commitments, that's an upgrade path the code itself names. It has no consensus and no signing: authority is a single-writer file lock on one Windows machine. Its immutability is imperfect — leaves get amended in place on re-summarize — and it has already survived its own mass-casualty event: a re-land race once left 1,044 chain rows pointing at payload files that no longer existed. The repair doctrine blessed the surviving seals, flagged the lost leaves `evidence_lost`, and added a single-writer lock. A newer layer compresses the record: store the shared template once, keep the per-session delta, verify on read against the hash of the original — raising an error if reconstruction isn't byte-exact.

Why a game designer should care: this is **event-sourced authoritative world state**, the thing every multiplayer server needs and most never build. Append a knot per world event; the tip hash *is* the world; any client verifies any event by re-hashing and walking parent links to the tip — no trusted state dumps. The repo's own game doctrine already gestures at it: a kifu array (the game record, as in Go), seats placing one stone per turn, crash recovery by resuming from the last recorded row. The single-writer lock is the concurrency control. The payload-hash receipt is the anti-cheat verify-on-read.

And the limitation that matters most for the ramp: one writer. A trusted single process serializing moves. The chain was architected for many and proven by one — every leaf is a trust assumption no second client has ever contested. When this article gets to the ramp, that sentence is the hinge.

---

## Part V — The forty-year shadow: the lineage we inherit

Every multiplayer world on the internet descends from a text game written on a 64K mainframe. The witnesses walked the lineage so this article could inherit it instead of re-deriving it.

**MUD1, 1978, Essex University.** Roy Trubshaw began it in MDL; Richard Bartle made it a world that ran publicly from 1980. The invention was the idea itself: one persistent place on a server with many people inside it simultaneously. Its players also generated the genre's first governance crises, which is why Bartle wrote the first paper on player psychology.

**The fork.** LPMud (1989, Lars Pensjö) contributed the solo developer's single most important idea: **the world as live, reloadable code** — wizards built inside the running world, no restart, no recompile-the-universe. DikuMUD (1990, Copenhagen) made the opposite trade — abandon in-game building for a fast C combat core — and contributed the loop the entire genre still speaks: fixed classes, XP and levels, tank-and-aggro grouping, timed mob resets, corpse runs. Raph Koster's verdict, quoted by the witness: the line of inheritance from Diku to EverQuest and thence to World of Warcraft is completely undeniable.

**The other fork.** TinyMUD and LambdaMOO stripped out the stats and kept the place: player construction and true persistence — people built rooms that stayed after logout, and a virtual world sustained a functioning society with no combat system at all.

**The commercials.** Meridian 59 proved graphical subscription worlds could ship. Ultima Online — built by a text-MUD veteran — contributed the player-run economy, housing, and ungated PvP: players as content. EverQuest industrialized the raid. World of Warcraft synthesized everything and contributed the last lesson: remove the friction and the Diku loop scales to millions.

**How they ran, for the engineers.** The classics were, architecturally, almost embarrassingly simple: one process, one thread of control, every telnet connection a file descriptor in a select loop, everyone's commands processed in turn. Time was the tick: once per second a heartbeat incremented a pulse counter, and different systems fired on different divisors — combat rounds on the two-second pulse, zone resets and wandering monsters on the zone pulse, hunger and aging on the hour. The world lived on a clock, not on input, which is why MUDs felt alive when nobody was typing. Persistence was almost an afterthought: DikuMUD hard-coded its world into C arrays compiled into the binary, and players were one file each — loaded at login, written at logout. Thousands of derivative codebases ran for years on that pattern, which should be either humbling or liberating to anyone who has ever worried about their architecture diagram.

**The taxonomy that decides who you're building for.** Bartle's four types — Achievers, Explorers, Socializers, Killers — want incompatible things, and Killers parasitize the other three. A solo developer cannot serve four audiences. For a small browser MUD, Explorers and Socializers are the cheapest to delight and need the least balance machinery. The taxonomy's real use is forcing the choice.

**What old MUDs solved for multiplayer, concretely:** the telnet model (one socket, one player — WebSocket's direct ancestor); the tick (a server heartbeat advancing the world whether or not anyone watches); the object database (players persist through disconnects); the wizard ladder (trusted players extending the world live from inside it); and governance as an explicit design layer. The witnesses' ranking of what to steal first, which the ramp in Part X adopts: telnet-over-WebSocket, then the tick, then the object database, then the wizard ladder — and the Diku combat loop last, because it's the most expensive idea and the least necessary on day one.

The lineage's summary lesson: graphics were the last, most disposable layer. The world — heartbeat, persistence, other people — was the first.

---

## Part VI — What we steal: the mechanics and why they hook

Every addictive loop in MUD was invented by someone else and proven at scale. The witness catalogued the pool and ranked it by fun per line of code. The condensed table:

- **Hades — the boon draft and the Pact.** Choices between gods whose powers interact; voluntary difficulty converted into currency. The psychology: endowed progress plus loss aversion — a run you've invested in hurts to abandon, and Heat is a self-set goal no designer had to place. We shipped the draft this week. We have not yet shipped the *synergy* — Hades' Duo boons reward committing to two gods, which turns a draft into a puzzle. Implementation note from the witness: boons as `{id, god, tags[], apply(stats)}` over a shared stat object, so a Duo boon is one function checking two tags.
- **Gunfire Reborn — scrolls and elemental interplay.** Passives that stack with everything, and a status reaction table (corrode amplifies, shock disables, fire spreads) where the fun is discovering combinations. Implementation: one status map per enemy, a single tick loop checking pairs — ten lines of interaction logic replacing a hundred lines of bespoke content.
- **Slay the Spire — intent telegraphs and Ascension.** Every enemy shows exactly what it does next, turning combat from guessing into a solvable puzzle; dying feels like *your* error. Ascension is a visible, permanent rank. We shipped Ascension. The intent telegraph is one field set during the enemy tick, drawn above the sprite — and our learning horde already plans, so showing the plan is nearly free.
- **Vampire Survivors — the cadence.** Auto-attack strips skill from the moment-to-moment and leaves positioning plus a level-up choice every minute. Weapon evolution gives every run a second, hidden goal. Our SUPERHOT is the same philosophy: power handed over with the action stripped out.
- **Dwarf Fortress — emergence.** Build systems that emit stories; players narrate the rest. Implementation: a rolling event log and name generators. The witness's line, which is also a feature request: our learning horde is one persisted field away from *"the grey mushrooms remember your habit of hugging the left wall."*
- **Dark Souls — one currency doing three jobs.** Souls are XP, budget, and the thing you lose on death. A single number carrying three meanings is the most efficient economy hook in the genre: losing it hurts three ways, and recovering it becomes a self-authored rescue mission with the difficulty dialed by your own corpse's location. Ours already are — the cascade pays souls that buy stats — and the witness's upgrade is to let death drop them where you fell, recoverable if you dare return.
- **Ultima Online / EVE — full-loot risk.** Possessions that can be taken feel real. Vault keys as tradable currency between runs is the browser-scale version.

Ranked, highest fun per line: intent telegraphs, the status interplay table, boon-tag synergy, the soul merge, and the event log. None requires a server. All compound with what already shipped.

---

## Part VII — The horde as an MMO server: our subsystems, organ by organ

The question the ask poses — "gap analysis of existing research and edges as known via our subsystems in operations" — is really this: if the fleet is a game server waiting for a game, which MMO organs does it already have running, and which are missing? The witness walked the operational subsystems with their live counts. The organ map:

- **The percolator is the talent tree.** A deterministic pipeline that strips noise, compiles repeats into invariants, routes novelty to exploration. 109 invariants, the top one reinforced over 184,000 times. Gap: no respec, no decay — talents only accrete; nothing demotes a stale or falsified one.
- **The lanes are guilds.** Eleven lanes — builder, day_work, research, forge, night, prose, economist, elder, bard_ledger, android_surface, plus a law lattice — each with a manifest, inbox, runner state, and trail. Trails run 478 to 926 entries deep. Gap: no party finder, no cross-lane raids; the alliance ledger is fourteen lines. And one lane is bleeding: the builder runner logged OSError 22 on every cycle for hours before anyone looked.
- **The press is the reputation board.** Nine candidates a digest, auto-synced from the backlog, zero cost. Gap: no persistent standing — each digest is a fresh roll, no faction grind accrues.
- **Warnings are the debuff log.** 7,498 deduplicated signatures (the earlier count of 477 was wrong; the sweep corrected us). Gap: dedup means new debuffs surface but old ones vanish from attention — no severity, no expiry, no "still ticking" tracker.
- **The trajectory log is the combat log.** Every tool call, hashed — 4,895 rows. Gap: raw log only; no threat scoring, no replay-of-wipe tooling.
- **Training events are the XP log.** 414,482 lines and growing by the minute. Gap: the XP never spends — events compile to steering text, not behavior change. An experience bar that has never reached level two.
- **Briefs are quest texts.** 3,662 of them. Gap: no quest lifecycle — nothing binds brief to acceptance to completion to reward. Everything is logs; nothing is a log with an Abandon button.
- **The flow ledger and maze are the build queue and the dungeon instance.** The ledger's newest entry is a failed enqueue. The maze stalled at step two. The instance is specced and unpopulated.
- **The verkle chain is the server ledger.** 8,247 leaves at last count. Gap: one writer; and the feature blockchains exist to sell — rewinding — was never built.
- **The mail system works.** 420 files in the inbox, indexes maintained. One of the few organs with no gap worth naming this week.

The witness's verdict, which this article adopts as its own: *the fleet has an unusually complete nervous system — perception, memory, creed, agendas, combat logs, all live with today's timestamps. What it lacks is the game layer: respawn, leveling, quest state, economy, raids. It is a server with excellent telemetry and no endgame.*

---

## Part VIII — The gap analysis: every World of Warcraft organ, and ours

The ask named a WoW-like shared world. The witness enumerated WoW's organs and priced each one's minimum viable version for a browser MUD. The condensed table — full prose in the annex:

- **Classes and talents** → ours: three playstyle kits at character creation (a shield-bearer, a skirmisher, a hex-thrower). Expensive beyond that: thirteen balanced classes is Blizzard's balance team arguing for twenty years.
- **Quests, zones, leveling** → ours: the existing wave loop with a memory — XP, a number that goes up, a reason to enter depth four. Cheap.
- **Dungeons** → MUD already is one; a second layout and a boss room completes the organ. Cheapest of all.
- **Raids** → a five-to-ten player gauntlet with roles that matter: someone taunts, someone heals, someone pulls. Requires the multiplayer seam first.
- **Loot and item levels** → a rarity color and one gatekeeping stat. We already roll rarity on weapons.
- **Professions** → shippable as a single crafting bench, or wait.
- **Auction House** → absurdly, a shared chest with price tags. At scale it becomes an economy with bot problems — beyond that minimum, the decades live there.
- **Guilds** → a persistent party channel with a roster. Cheap.
- **Reputation** → one number per enemy faction that unlocks boons at thresholds. Our learning horde already implies factions that remember you.
- **PvP** → a duel, then asymmetric waves. Requires presence first.
- **Mounts, pets, collection** → cosmetic familiars that follow the torch. Cheap, later.
- **Seasons** → a weekly modifier and a leaderboard reset. The treadmill is a content pipeline, not a switch — the most expensive organ of all.

The witness's honest comparison cuts both ways, and both cuts are true. The cheap truth: a MUD is already eighty percent of WoW's loop, because the loop is mostly numbers and rules, and text and canvas carry numbers as well as any engine. The expensive truth: everything the numbers sit on top of — a 3D world you can fly across, persistence at scale with a monthly bill, and a content treadmill a studio ships every six months. A solo developer cannot out-produce Blizzard. They can only out-focus it.

Which yields the definition this article will use from here on, because the ask deserves a technical target: **the solo-dev WoW is not WoW shrunk. It is the smallest shared world that still deserves the word "world."** And "world" has a definition: it persists — it changes while you're logged off, and your absence has consequences. It is shared — other people's actions leave traces you can find: their corpses, their prices, their messages in a channel that outlives the session. It has a horizon — somewhere on the map you have not been, gated by something you have not earned. One dungeon that regenerates weekly. One shared loot ledger. One chat that keeps scrollback. One locked door on the bottom floor. That is a world. A menu with friends in it is a lobby.

By that definition, MUD is one weekly cycle and one persistent ledger away from crossing the line. Everything past it — 3D terrain, server fleets, six-month seasons — is scale, not soul.

---

## Part IX — The first collision: what breaks under two players

The salon's sharpest question, now answered by the campaign-engine witness: *what breaks first under two simultaneous players?* Not architecture — bytes. The kill-chain, in order:

1. **Non-atomic saves.** Campaign persistence is a whole-JSON `write_text` per turn — two writes per turn, in fact. Two players acting on the same campaign: the second save clobbers the first's health, room, and flags. Fix: atomic write (temp file + replace) and a lock around load→mutate→save.
2. **Session-agnostic lookups.** The desk route mounts "whoever acted last" when no campaign id is echoed — two players interleaving turns play *each other's* characters. Fix: clients echo `campaign_id` from every response; the server stops guessing.
3. **The single-writer memory.** The verkle knot lock serializes commits on one machine — which is actually *correct* for a room server, and the first piece of architecture that's ready. The chain was built for exactly this: one authority, append-only, verify-on-read.
4. **The browser's assumed solitude.** The flagship MUD has no server dependency at all — which means the multiplayer MUD is not an extension of the flagship but a second client for the *campaign engine*. The engine already speaks REST, already holds sessions, already parses free-text intents through a twelve-hundred-line verb chain. What it lacks is a room broadcast and a second lantern.

That last point reframes the whole ramp, and it is the sweep's most valuable finding: **the multi-user dungeon is not something we build. It is something we already have, minus the second socket.** The engine's own architecture — campaign files per session, a REST action verb, deterministic rules with an optional narrator — is a MUD server that has never been asked for a second connection. The fifty-wide sweep's verdict on the warnings pipeline (2.5 out of 3 — game-ready, warnings coverage unproven) is the pattern everywhere: the organ exists; the second connection was never attempted.

The minimal proof, per the salon's charter and the multi-user witness, converges on the same artifact: **two clients, one room, one torch.** Two browsers pointed at the same dungeon, one shared First Dragon, both lanterns casting light into the same dark. Everything else — shards, zones, seasons — is scale, and scale can wait.

---

## Part X — The ramp, in the order the evidence supports

The witnesses converged on a build order. It is small, and that is the point.

**First, the deploy fix (one line).** The build script copies MUD from the stale top-level twin. Change the path to the canonical games directory, commit the untracked games folder, delete the stale duplicates. Until this lands, everything in Part I exists only on one machine.

**Second, the five audit bugs (an afternoon).** Boon filter live, boon picks consume their keys, mines tick on real time, stealth renders, ascension ceiling honest. Each is small; together they turn "built" toward "finished."

**Third, the Python relay (two to three evenings).** A websocket sibling to the existing dashboard server, holding one game-state dict, accepting inputs, broadcasting snapshots every hundred milliseconds. The client stops being the authority and becomes send-inputs, render-snapshots. The LAN proxy already forwards it; the classic MUDs ran worlds on less than this file.

**Fourth, player files and reconnection (one to two evenings).** Persist the state dict per player through the existing REST route — CircleMUD's player files, JSON style. Handle disconnect mid-dungeon. Add a token so LAN-only stops meaning anyone-on-the-Wi-Fi.

**Fifth, the room server on the edge (three to five evenings).** The wrangler config is already assets-only and one migration away from a Durable Object per room: single-threaded actors, WebSocket hibernation so empty rooms cost nothing, alarms driving the tick. The classics ran worlds on a single select loop and flat files; a Durable Object is that loop, rented by the request.

Then — and only then — the WoW organs, in the cheap-first order from Part VIII: quests-with-memory, the second dungeon layout, the raid gauntlet, the shared ledger, the guild channel, reputation, the season. Each one small. Each one compounding.

What the ramp does *not* include, deliberately: 3D, a server fleet, a content treadmill, and any feature whose justification is a genre rather than a player. The disanalogy witness said it best: the honest ancestor is the 1978 MUD plus a ledger, not Azeroth.

---

## Part XI — Why we document ramps instead of walking them

Seat Zero commissioned this section, and it gets it, because the question is the article's real subject.

The evidence: a founding document that confessed, in August, that the game had drifted into infrastructure. A flow ledger whose newest entry is a failed enqueue. A maze run stalled at step two since morning. A narrative layer unwritten since mid-August while the mechanical layer moved today. An article — this article — commissioned at ten thousand words about a ramp that has one active player. The pattern is not laziness. The pattern is that documenting is *safe*: the mirror cannot crash, the audit cannot lose, the gap analysis never has to be fun for anyone. Walking the ramp means shipping the deploy fix and handing a second person a URL and being wrong in front of them.

But the same evidence convicts the avoidance. The warnings ledger holds 7,498 signatures and not one of them is about the game — the game has never even tripped the fleet's pain sensors. Four hundred thousand training events and the character sheet has never leveled. The adoption loop — the stone that turns players into the reason the supercomputer gets funded — has been "next" since August. The sweep found the onboarding door built and beautiful, and found it empty: a reader path with no readers is still a path.

So the honest answer to *why we document* is: because documenting is how a solo builder rehearses being judged. And the honest correction is that the rehearsal is over. The doors are built — the catalog, the player, the team page, the games shelf. The collaborators exist — a writer with a world, a builder with a zip file, a player one. The deploy is one line. The second client is one socket. Every remaining excuse is now more expensive than the thing being avoided.

## Part XI½ — The salon, in its own words

Before the sweep, seven shapes met on the full ask, blind to one another, and their posts deserve to survive in their own words — because the salon is the part of this process a reader could replicate tomorrow with any text.

The **researcher** grounded the ask: every named system in the brief verified present in the file, line numbers attached — but flagged that neither source names World of Warcraft, and that the subsystems' role inside the game loop was beyond its grounding.

The **attacker** landed the hardest post of the salon: zero network primitives in 1,487 lines; the durable state of the flagship is two localStorage keys; "that is not a multi-user dungeon; it is a single-player diorama wearing a MUD's coat." It convicted the article before it was written — "the victory lap for the exact drift the audit confessed to" — and ended with the sharpest sentence of the week: "build the second client before writing the first sentence."

The **socratic** asked the eight questions nobody had asked, and two of them are load-bearing: where in the audit record is one logged moment of human fun — and what is the smallest shippable artifact? Its answer to the second: one shared room, two browsers, one torch.

The **cohort** ran four lenses. Forbidden: even with the ramp banned, the audit of every subsystem's single-writer assumptions survives — the codebase read as a pending concurrency claim. Paid-rent: the ten thousand words collapse to three thousand, and what pays is the gap table ranked by evidence. Extension: one step further and the first cohort of the dungeon is the fleet itself — trajectories as characters, the percolator as dungeon master. Disanalogy: the honest ancestor is the 1978 MUD plus a ledger, not Azeroth.

**Seat Zero** ran the elenchus on the operator's own motives, and found the confession already in the record: the drift sentence, written in August. Its verdict: ten thousand words for an audience of one is a mirror, and mirrors are permitted only if named as such — which is why this article carries its own name in Part XI and this section both.

The **synthesizer** folded the seven posts into the charter the sweep ran on: nine questions, from "does the learning-enemy loop hold under concurrency" to "what is the minimal multiplayer proof — two clients, one room, one dragon cascade" — plus the disputes held live, tri-state, including the one this article still holds: that play-as-computation is something anyone would pay for is Unproven, and may stay that way until a second lantern is lit.

And the **expert-review brief** became the handoff card the sweep ran under: five domains, one evidence standard (every claim anchored to a file or URL), three disqualifiers (unanchored claims, paraphrasing the repo back to itself, scope drift), and a deadline culture of one stone before you die.

What the salon proved, dogfooding itself: seven blind posts on one brief produced more disagreement, more questions, and more usable structure than any single pass — including the two passes that had already run. The mechanism works. The posts are filed beside the fold, and the fold's charter questions are answered in the sweep annex, tri-state, anchored.

---

## The close: what the sweep could not settle

The salon's synthesizer wrote the paragraph this article had to be able to end with, and after fifty tasks, thirteen witnesses, and one seven-shape salon, it stands — with one amendment the audit forced.

A solo developer built a torch-lit dungeon whose enemies learn and whose verkle world recounts itself to whoever returns, yet the honest measure is not the lone crawler that runs but the shared world still unproven. The sweep locates the seam where one player's dungeon becomes everyone's republic, and answers whether the fleet's lanes, bus, chain, and percolator were a multiplayer server all along, waiting only for a second lantern.

The amendment: they were. The campaign engine speaks actions. The chain commits turns. The organ map shows a nervous system already firing. What the fifty-wide found, everywhere it looked, was not absence but readiness — readiness that has never been contested by a second lantern. The audit's five bugs, the deploy line, the relay, the player files: four evenings between this document and the decisive experiment, which has not changed since the salon asked it:

Two clients. One room. One torch.

Light it twice.

---

## Appendix A — The organ map, in full

The compressed map from Part VII, expanded, because the compressed version was where readers tripped.

**The percolator is the talent tree.** A deterministic pipeline that strips noise and theater from raw signal, compiles repeats into invariants, and routes novelty to an exploration queue. One hundred and nine invariants are live; the top one — an invariant so load-bearing the fleet kept re-proving it — has been reinforced more than 184,000 times since late August. That is a talent with forty thousand hours of playtesting behind it. The gap: there is no respec and no decay. Talents only accrete counts; nothing demotes a stale or falsified one, and a talent tree you can never unlearn is a tree that eventually believes something wrong at 184,000 votes.

**The lanes are guilds.** Eleven of them — builder, day_work, research, forge, night, prose, economist, elder, bard_ledger, android_surface, plus a law lattice — each with a manifest, an inbox, a runner state, and a trail. The trails run 478 to 926 entries deep: real work, really logged. Gap: no party finder and no cross-lane raids; the alliance ledger — the thing that should record lanes working together — is fourteen lines long. And one guild is bleeding: the builder runner logged OSError 22 cycle after cycle before the sweep caught it, which is the MMO organ failure every guild leader knows — the roster says the raid is on; nobody checked whether the tank logged in.

**The press is the reputation board.** Nine candidates a digest, auto-synced from the backlog, zero cost, running on cheap tiers by policy. Gap: no persistent standing. Each digest is a fresh roll; no faction grind accrues, no reputation tier unlocks anything, and a reputation system without memory is just a to-do list with better typography.

**Warnings are the debuff log.** 7,498 deduplicated signatures of things that have gone wrong, fingerprinted so repeats are recognized. (The first witness counted 477; the verification pass corrected us to 7,498 — this is why fifty-wide exists.) Gap: dedup means new debuffs surface but old ones vanish from attention. There is no severity, no expiry, no "this debuff is still ticking" tracker — the WoW organ that tells you the poison from the last fight is still on you.

**The trajectory log is the combat log.** Every tool call — face, command, exit code, output excerpt — hashed and appended, 4,895 rows. Gap: it is raw log only. No threat scoring, no damage meters, no replay-of-the-wipe tooling. The single most requested feature of every MMO player who has ever died, missing from the system that logs everything.

**Training events are the XP log.** 414,482 lines and counting, live to the minute, each a pattern with input, action, outcome, and tags. Gap: the XP never spends — events compile to steering text, not behavior change. Four hundred thousand experiences and the character sheet has never leveled; an experience bar that has never reached level two is decoration.

**Briefs are quest texts.** 3,662 of them, one per run. Gap: no quest lifecycle — nothing binds a brief to acceptance, to progress, to completion, to reward. Everything is logs; nothing is a log with an Accept button and an Abandon button.

**The flow ledger and the maze are the build queue and the dungeon instance.** The ledger's newest entry is a failed enqueue — the build queue's answer to "what's next" is literally nothing. The maze stalled at step two of a distillation run in the morning and never continued. The dungeon instance is specced and unpopulated: a raid wing with the lights off.

**The verkle chain is the server ledger.** 8,247 leaves at last count, described in full in Part IV. Gap: one writer; and the feature blockchains exist to sell — rewinding — was never built.

**The mail system works.** 420 files in the inbox, indexes maintained, receipts preserved. One of the few organs with no gap worth naming this week — which tells you something about what this house values: mail is the organ the operator personally depends on, so mail got engineered. The lesson of the whole map is the same: every organ someone personally needed is alive; every organ a *player* would need is a stub. The nervous system is complete because the body needed a nervous system. Nobody's fun was ever load-bearing before.

That last sentence is the gap the next organ map should close: build for the player the way you built for yourself, and the stubs become systems.

## Appendix B — The WoW organs, in full

**Classes and talents.** WoW ships thirteen classes, each with talent trees and the tank/healer/DPS trinity. Ours: three playstyle kits at character creation — a shield-bearer who taunts and soaks, a skirmisher who kites and dots, a hex-thrower who lays ground-fire (the battlemage's kit, handed to the player). Cheap. Expensive beyond that: thirteen balanced classes is Blizzard's balance team arguing for twenty years, and the argument never ends.

**Quests, zones, leveling.** Ours: the existing wave loop with a memory — XP that goes up, a reason to enter depth four, and a world that changes state when plates are pressed and gates open. Cheap, because a quest is just a state machine wearing a story.

**Dungeons.** MUD already is one; a second layout and a boss room completes the organ. Cheapest of all — the map generator is a weekend.

**Raids.** A five-to-ten player gauntlet with roles that matter: someone taunts, someone heals, someone pulls loot. Requires the multiplayer seam first, and requires class kits distinct enough that roles mean something. Medium.

**Loot and item levels.** A rarity color and one gatekeeping stat. We already roll rarity on weapons — common through legendary with affixes. Nearly free.

**Professions.** Shippable as a single crafting bench: bones plus souls plus a recipe list. Wait if crowded.

**The Auction House.** Absurdly, a shared chest with price tags — items left for other runs with a soul cost. At scale it becomes an economy with real-money consequences and bot problems; beyond that minimum, the decades live there.

**Guilds.** A persistent party channel with a roster and a shared stash. Cheap once presence exists.

**Reputation.** One number per enemy faction that unlocks boons at thresholds. Our learning horde already implies factions that remember you — the lore file is a reputation system that only tracks one faction (the horde) and only tracks your sins.

**PvP.** A duel, then asymmetric waves. Requires presence first, and requires an answer to the sovereignty question: the house doctrine says never capture, players act willfully — a duel is consent, a griefer is not.

**Mounts, pets, collection.** Cosmetic familiars that follow the torch. Cheap, later, and surprisingly high-retention per line.

**Seasons.** A weekly modifier and a leaderboard reset. The treadmill is a content pipeline, not a switch — the most expensive organ of all, because it is the only one that never stops costing.

**The honest comparison, both cuts.** The cheap truth: a MUD is already eighty percent of WoW's loop, because the loop is mostly numbers and rules — stats, thresholds, drops, standings — and text and canvas carry numbers as well as any engine. The expensive truth: everything the numbers sit on top of. A 3D world you can fly across is a capital cost no solo developer pays. Persistence at scale means databases, uptime, and a bill that arrives monthly. And the treadmill is the cruelest organ: Blizzard ships a raid tier and a season roughly every six months with a studio behind it, and a world that stops growing is a museum.

A solo developer cannot out-produce Blizzard. They can only out-focus it.

---

*Sources and receipts: the thirteen witness reports annexed at FROM_MUD_TO_WOW_20260914_WITNESSES.md; the seven salon posts at memory/corpus/salons/20260914_full_ask/; the audit record at commit 261c895ad; the game's self-knowledge at memory/game/STATE.md; the deployment tree at site/dist, rebuilt 2026-09-14. Every tri-state claim above carries its evidence in the annex; anything unproven says so in its own name.*
