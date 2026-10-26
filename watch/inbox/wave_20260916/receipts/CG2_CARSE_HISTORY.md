# CG2 — CARSE ACROSS THE HISTORY OF GAMES (deep unpack of the HG1 eras)

- **Lane:** CG2 · wave_20260916
- **Receipt opened:** 2026-09-16
- **Law:** receipt FIRST, append as I go · no git · no paid APIs · own knowledge of game history is the primary source; only uncertain dates would have needed web verification, and none did (all dates below are standard consensus; the genuinely debated one — mancala's physical-board age — is hedged in place).
- **Source text:** James P. Carse, *Finite and Infinite Games* (1986). Quotes cited from memory of the text; the load-bearing ones are canonical. Anything not quotable verbatim is marked *[paraphrase]*.
- **Sister receipts:** `HG1_GAMING_HISTORY_WEAVE.md` (mechanic → weave-target pass; CG2 does not repeat its table) · `CG3_ESTATE_INFINITE.md` (the estate itself through the same lens). CG2 stays in its lane: the lens, applied across every era of humanity's games, ending in one verdict for the bones-legal build (`wow_bones.py` → `wow_world.py` legality tables → `wow_session.v1` receipts → Discord adapter).

## Working log (append-as-you-go)

- [x] Receipt opened (this stub) + lens defined.
- [x] Part II: 16 era/lineage unpacks (shell / hidden game / contribution / Carse line).
- [x] Part III: master table (era / finite shell / infinite core / contribution).
- [x] Part IV: verdict — which single era invented the most infinite-game machinery, judged by what the bones-legal persistent world needs.
- [x] Footer: hash + counts.

---

## Part I — the lens

Carse's opening move, compressed: **a finite game is played for the purpose of winning; an infinite game is played for the purpose of continuing the play.** Finite: known players, fixed rules, agreed objective, an endpoint that produces a winner and a title. Infinite: known and unknown players, rules that must change to keep play alive, no endpoint — a horizon, not a boundary. Four more blades from the same knife:

- "The rules of a finite game may not change in the course of play. The rules of an infinite game must change in the course of play."
- "Finite players play within boundaries; infinite players play with boundaries."
- "Finite players play seriously; infinite players play with abandon."
- "Whoever must play, cannot play." · "No one can play a game alone. One cannot be human by oneself." · and the book's last line: "There is but one infinite game."
- Nesting law *[near-quote]*: finite games can be played inside an infinite game; an infinite game cannot be played inside a finite one.

**The reading rule for this receipt:** every commercial game SHIPS a finite shell. Play is what players do with it. The infinite game is the set of practices that keep play going after the shell ends — across runs, across versions, across strangers. The history of game design is the history of finite shells with infinite games smuggled inside, plus the craft of building the smuggling tunnels.

**Infinite-game machinery, reduced to six primitives** (used to score the eras in the verdict):

| # | Primitive | One line |
|---|---|---|
| P1 | PERSISTENCE | World state survives the absence of any player |
| P2 | MUTATION AUTHORITY | A legal, known channel by which the rules themselves change |
| P3 | KNOWLEDGE METAGAME | The player's real character is what survives the death of every run |
| P4 | PLAYER AUTHORSHIP | Players write content and rules, not just moves |
| P5 | CONTINUATION ECONOMICS | A structure that pays (in money, status, or meaning) for play to continue |
| P6 | ASYNC CO-PRESENCE | Strangers cooperate and compete across time inside one world |

The verdict question is not "which game is infinite" — none are, as shipped — but **which era invented the most machinery that an infinite game actually needs**, judged against what the fleet's bones-legal persistent world already proves it must have: legality tables and typed refusals (P2), receipted deterministic sessions and `world_sha` (P1), `mud_lore`/chronicle/NG+ (P3), templated souls messages and `game_modules/*.v1.json` (P4), donation-grade continuation (P5), relay presence (P6).

---

## Part II — the eras, shell and core

### 1. Senet and the ancient boards (Senet ~3100 BCE Egypt · Royal Game of Ur ~2600 BCE · Mesoamerican ballgame)

**(1) As played:** maximally finite. Thirty squares, dice of fate, race your pieces off the board; a winner, then the board goes back in its box.
**(2) The hidden game:** the board was a map of the afterlife. Book of the Dead chapter 17 pairs the senet board with passage through the netherworld; Ur boards were buried in tombs; the ballgame re-enacted the Hero Twins' solar myth. The finite race stood in for the one journey with no second playthrough — play as rehearsal of death, which is precisely the territory Carse gives the infinite player *[paraphrase]*.
**(3) Contribution to infinite-game design:** the discovery that a bounded board can mirror an unbounded world — the game as pointing-device, not just contest. And duration as proof: three thousand years of senet means the artifact outlives every title ever won on it; boards in tombs are the first promise of play persisting past the player (P1 in myth, before software).
**(4) Hardest line:** "There is but one infinite game." Senet is a finite board aimed at it: you can win the race; the journey has no winner.

### 2. Go (weiqi, at least ~2,500 years; baduk in Korea, igo in Japan)

**(1) As played:** each game is finite — counted or resigned, a rank at stake. But the shell is trivially re-enterable and deliberately unequal by design.
**(2) The hidden game:** the handicap system. Strong player gives stones; komi pays the first mover. This is rule mutation deployed BETWEEN games for one purpose: so that play between unequal players continues instead of collapsing. Add the unbounded rank ladder (30 kyu up through pro dan), the joseki/fuseki corpus mutating for centuries (P3 before computers), teaching games as the core social unit — and post-2016, AlphaGo's move 37 moving the horizon again without touching the rule text. Go invented rule-change-as-a-service to keep the weak in the game.
**(3) Contribution:** P2's prototype — scheduled, legal, institutionalized rule mutation (with the Carse precision that it mutates between games, not in the course of play); P3's first great transmissible corpus; and the pedagogical inversion: the social contract exists to prevent anyone from being played out of the game.
**(4) Hardest line:** "The rules of an infinite game must change in the course of play." Handicap stones are humanity's first institutionalized rule mutation for continuation.

### 3. Chess (chaturanga ~6th c. India → shatranj → modern Europe; Staunton 1849; FIDE title 1914–)

**(1) As played:** the most finite design in history. Perfect information, no chance, no hidden state, one winner — or the draw, the finite game openly admitting it cannot conclude. World title, Elo, sixty-move theory.
**(2) The hidden game:** the theory corpus — openings books are a knowledge metagame (P3) running for centuries, each generation playing WITH the previous generation's book. And when memorized theory began winning before move twenty (draw death), the players mutated the container itself: Fischer's Chess960 (proposed 1996) randomizes the starting array — the boundary became a parameter. Armageddon tiebreaks, anti-engine law, a world champion stepping away from the classical crown (Carlsen, 2022–23): the top of chess is a permanent negotiation about which finite shell keeps the infinite game alive.
**(3) Contribution:** P3 at classical scale (theory as meta-knowledge that outlives every player), the rating ladder as unbounded progress, and format mutation as anti-exhaustion technology.
**(4) Hardest line:** "Finite players play within boundaries; infinite players play with boundaries." Chess960 is that sentence compiled into a ruleset.

### 4. Mancala family (oware, bao, sungka, kalah…; physical boards at least ~1,300 years old, likely far older as oral play)

**(1) As played:** finite — sow, capture, count; the round ends when one side's stores empty.
**(2) The hidden game:** the family, not any single game. Hundreds of rule variants, each village a fork; rules are local, oral, mutable — nobody owns them, mutation is how the game travels (P4 at folk scale). Boards carved into doorsteps and temple rock: play is ambient, embedded in the afternoon, always one more round. Customs (elder-only play, night-play rules) make the social frame part of the ruleset.
**(3) Contribution:** variant-culture as the norm — the proof that a game can survive endless rule drift by never having an owner; P5 in its oldest and cheapest form (the board you sit on; continuation costs nothing).
**(4) Hardest line:** "There is but one infinite game." — run in reverse: one infinite game, and the finite versions are its costumes.

### 5. D&D 1974 (Gygax & Arneson, from Chainmail; Blackmoor running since ~1971)

**(1) As played:** the shell is finite — the module ends, the session ends, characters die, TPK is a loss. Published adventures are finite products.
**(2) The hidden game:** the campaign, and above all the DM. The rules delegate authority to a human referee whose win condition is the table continuing. Rulings over rules is P2 with a face: a legal, accountable channel for mutating rules mid-play. Character sheets persist across sessions (P1 at story scale — the first receipt format gamers ever kept); players author the dungeons (P4); the zine/APA hobby economy kept play alive between tables (P5); the party makes it structurally impossible to play alone. Arneson's Blackmoor ran for years — the first persistent world operated on trust plus a written ledger.
**(3) Contribution:** the deepest single haul in the history: P2 full (the arbiter as a ROLE), P4's first form (dungeon authorship), P1 embryonic (campaign continuity), P5 embryonic. Every persistent world since is either an attempt to simulate the DM or to make the DM's rulings auditable.
**(4) Hardest line:** "The rules of an infinite game must change in the course of play" — D&D is the only era that made the rule-changer a character in the game. And "No one can play a game alone. One cannot be human by oneself." — the table.

### 6. MUD1 1978 (Essex) → EverQuest 1999 → WoW 2004

**(1) As played:** finite shells. MUD1 had points, levels, and wizhood — reach wizard and you were done (they had to invent things for wizards to do, or retire them). EQ: level cap and the epic weapon. WoW: cap and the raid clear.
**(2) The hidden game:** MUD1's true invention was not multiplayer but persistence — a world that exists while you are absent (P1 in software). Then the discovery that the infinite game is the people: Bartle's 1996 taxonomy (achievers, explorers, socializers, killers) is an enumeration of different infinite games players run inside one shell; the socializers were the proof — no score, pure continuation. EQ layered reputation on named servers: finite gear inside infinite social memory. WoW industrialized the false finish — the level cap is re-moved every expansion, a finish line whose job is to be moved; the subscription is revenue for continuation (P5 as invoice). Raids are finite games nested inside the infinite treadmill — Carse's nesting law as endgame design. And WoW Classic (2019) is the era's self-proof: players demanded an obsolete shell back, because the shell was never the game.
**(3) Contribution:** P1 (software persistence), P5 (continuation economics, industrialized), P2-by-decree (the live patch cycle — rules change in the course of play, but by vendor edict), the guild as institution, and the Corrupted Blood incident (2005) as emergent history with witnesses.
**(4) Hardest line:** "A finite game is played for the purpose of winning, an infinite game for the purpose of continuing the play." — itemized monthly, $14.99, on the subscription invoice.

### 7. Rogue 1980 (Toy/Wichman/Arnold) → NetHack 1987 → Dwarf Fortress 2006

**(1) As played:** the most death-honest shells in gaming — one run, permadeath, the Amulet, the fallen fortress. Maximally finite: death erases the character.
**(2) The hidden game:** knowledge. Permadeath kills the character, not the player's game — the wiki, the conduct runs, the ascension set (win as every role/race/alignment) make the metagame death-proof: P3 perfected. NetHack adds combinatorial rule-emergence (polymorph, altars, identification): the rule text is fixed but the state space is bottomless, so novelty never runs out. NetHack's **bones files** cross P3 with P6: your dead character's gear and ghost spawn in STRANGERS' dungeons — death converted into other players' world content, since 1987. Dwarf Fortress makes the philosophy explicit — "losing is fun": failure is the fuel of the story-generator; the fortress only produces tales when it collapses. And the dev model is P5's purest form: one developer, donationware, twenty years of patches — play continues because someone's livelihood IS its continuation.
**(3) Contribution:** P3 perfected; P6 via bones files; the seed as shareable, litigable contract (the run becomes a reproducible artifact); "losing is fun" as a design law — continuation fed by failure rather than protected from it.
**(4) Hardest line:** "Finite players play seriously; infinite players play with abandon." Permadeath is maximal seriousness; "losing is fun" is maximal abandon; the genre runs both at once — Carse's nesting (finite games inside the infinite one) as a genre charter.

### 8. Arcade (Space Invaders 1978 · Pac-Man 1980 · golden age to ~1983)

**(1) As played:** the most brutally finite commercial frame ever shipped — three lives, one credit, GAME OVER.
**(2) The hidden game:** the high-score board. Your initials persist in the cabinet after you leave: P6's first implementation — competition against strangers across time. Nobody wins Pac-Man: the game ends in a designed kill screen (level 256, garbled right half) — a boundary made visible, which the best players then played WITH, chasing perfect scores INTO the kill screen. Twin Galaxies and the record books institutionalized continuation: an organization whose whole job was keeping finite games infinitely alive (P5 proto).
**(3) Contribution:** P6 proto (leaderboard as co-presence across time), the record as unbounded goal, and the audience — Carse ties finite play to spectators *[paraphrase]*; the cabinet is a stage, and speedrunning is the direct descendant of that audience culture.
**(4) Hardest line:** *[paraphrase of Carse's audience argument]* the finite game needs witnesses for the title — the arcade built the witnesses into the furniture, and then the witnesses outlived the games.

### 9. God/sim games (Populous 1989 · SimCity 1989 · Civilization 1991 · The Sims 2000)

**(1) As played:** split verdict. Populous and Civ ship victory conditions (finite); **SimCity shipped with no win state at all** and called it a game — the canonical refusal of the finite frame. The Sims: life as the goal, no victory screen.
**(2) The hidden game:** player-authored goals. When the game declines to name the objective, the player must — and a self-authored objective cannot be taken from you (P4 at the motivational layer). "One more turn" is the infinite pull made famous; the Civ franchise mutates its own rules every version (P2 at series scale). Will Wright's toys-not-games distinction is a Carsean move: the sandbox is a horizon, not a boundary — you garden, you do not conquer.
**(3) Contribution:** the winless sandbox as a viable product; systems-first design; the city-as-ongoing-project loop (maintenance as gameplay) that every later persistent world inherited.
**(4) Hardest line:** "Whoever must play, cannot play." A game that cannot make you win leaves you free to keep playing.

### 10. Doom 1993 / Quake 1996 (id Software)

**(1) As played:** finite — episodes, exit switches, NIGHTMARE!, done.
**(2) The hidden game:** the shell was built to be broken open on purpose. id shipped the WAD format: players as level authors (P4, industrial). Strafe-running and rocket-jumping were physics bugs the studio blessed into technique — players playing WITH the physics boundary, designers ratifying the mutation (P2's lightest touch: bless, don't legislate). Deathmatch made shooters infinite (other people are unbounded content); QuakeWorld made them persistent-online; QuakeC and engine releases seeded Counter-Strike and Team Fortress — the engine became a lineage whose rules mutate across decades. Doom is the ur-speedgame: thirty-plus years of route mutation on an unchanged mapset.
**(3) Contribution:** P4 as file format; bug-to-technique culture (playing with boundaries as a production method); the open engine as a rulebook released into the players' hands.
**(4) Hardest line:** "Finite players play within boundaries; infinite players play with boundaries." The rocket jump is the sentence executed as a keystroke.

### 11. Myst 1993 and the adventure lineage (Colossal Cave Adventure 1976 · Zork 1977/1980 · King's Quest 1984 · Monkey Island 1990)

**(1) As played:** the most finite genre shipped. Puzzles solved once, ending reached, shelf. Knowledge of the solution DESTROYS the game — the anti-roguelike: the metagame kills replay instead of feeding it.
**(2) The hidden game:** almost none inside — and that is the finding. Cyan tried to convert the finite shell into an infinite world twice (Uru 2003; Myst Online 2007, both commercially failed). Authored worlds resist infinite conversion: atmosphere invites revisitation but cannot sustain play, because play needs open boundaries and Myst is all boundary — each Age is a closed box; the linking book is Carse's boundary, never his horizon.
**(3) Contribution:** the great NEGATIVE result of infinite-game design — the proof of what does not generalize: authored narrative ends; endings produce museums, not worlds. One positive export: environmental storytelling as lore substrate, which later infinite worlds imported to feed community mythmaking.
**(4) Hardest line:** *[paraphrase, on titles]* the finite game's winner inherits a title and the end of play. Myst makes that literal: after the credits, the world is a museum you already own.

### 12. Souls-like (Demon's Souls 2009 · Dark Souls 2011/2014/2016 · Elden Ring 2022)

**(1) As played:** finite — kill the lord, credits, NG+.
**(2) The hidden game:** asynchronous co-presence, perfected. Bloodstains, messages in a controlled template vocabulary, phantoms, invasions: strangers co-present across time with no lobbies (P6's full form). The message system is player authorship BOUNDED BY VOCABULARY — helping and trolling share one legal grammar (the key trick of bounded P4). NG+ mutates rules upward between cycles (P2-lite); SL1 and gimmick builds are the Go handicap inverted — players GIVE THEMSELVES stones. World tendency shifts the world for everyone from your deeds (P6 × P1). Around the fixed text, the lore economy (wikis, videos, theories) is a P3 corpus of endless rereading.
**(3) Contribution:** P6 perfected; P4-bounded (infinite player content inside a legal vocabulary — the exact pattern the fleet's template-word messages want); self-handicap culture as a norm.
**(4) Hardest line:** "No one can play a game alone. One cannot be human by oneself." — implemented as a floor note in a poisoned hall, left by a stranger who died there first.

### 13. Slay the Spire (early access 2017 · 1.0 2019; lineage: Dominion 2008, Dream Quest 2014)

**(1) As played:** one climb, the Act 3 boss, then the deck dies. Finite per run, and honestly so.
**(2) The hidden game:** the ascension ladder — twenty self-imposed difficulty notches: codified rule mutation BETWEEN runs (P2) that keeps veterans inside the game after the shell is mastered. The roguelike knowledge metagame (P3) condensed to deckbuilder size; daily climbs with fixed seeds turn runs into asynchronous competition (P6); the mod scene authors new characters (P4). The run is finite and played seriously; the player's real game — A20 heart kills, streaks, archetype mastery — is the infinite ladder standing above it.
**(3) Contribution:** ascension as institutionalized self-handicap (the cleanest P2-between-runs mechanism ever shipped); seed honesty (RNG as public contract); the deckbuilder as a genre generator.
**(4) Hardest line:** "Finite players play within boundaries; infinite players play with boundaries." Ascension 20 is the boundary picked up and worn as clothing.

### 14. Exanima 2015 and the physics lineages (QWOP 2008 · Gang Beasts 2017 · Kerbal Space Program 2011 · Teardown 2020)

**(1) As played:** thin finite frames — arena ladders, campaign levels, mission objectives — stapled onto simulations that ignore them.
**(2) The hidden game:** the simulation removes the script. When outcomes are computed rather than authored, every rule becomes a boundary the player can lean on but never exhaust: orbital slingshots in KSP (playing with Newton), ragdoll mastery in Exanima (playing with your own body), destruction chains in Teardown. Novelty arrives from continuous state space rather than rule text — the first design family where the rulebook is finite and the state space is genuinely inexhaustible.
**(3) Contribution:** emergence as content; failure-as-information (a physics failure teaches; a scripted failstate only stops); and the structural lesson: infinite play can be manufactured from STATE-SPACE DEPTH, not only from rule mutation — Carse's horizon reachable without touching the rules.
**(4) Hardest line:** *[paraphrase of Carse's boundary/horizon distinction]* a boundary you cross; a horizon you approach. Physics sandboxes replaced every wall with a horizon.

### 15. Minecraft (alpha 2009 · 1.0 2011) / No Man's Sky 2016

**(1) As played:** Minecraft has a soft ending (the Ender Dragon, the End Poem credits) most players never touch; NMS shipped an infinite generator wrapped around a finite experience — nothing binding to do, the cautionary launch of 2016.
**(2) The hidden game:** Minecraft is the largest transfer of infinite-game authority in history: redstone is players authoring computation (playing with the boundary between game and platform); servers are player law (2b2t's anarchy order has a decade of its own historiography); modpacks are player rulebooks. The End Poem ends the finite game by blessing the infinite one — the credits as a benediction to keep playing *[paraphrase of the "the universe said…" cadence]*. NMS is the redemption arc: Hello Games made the RELATIONSHIP infinite — years of free rule-mutation updates turned play-to-continue into a studio covenant. The lesson: procedural infinity is not infinite play; continuation must be authored socially.
**(3) Contribution:** P4 at maximum (players as rule-writers — the crown transfer); P1 (the world remembers every block); the NMS lesson that the infinite game is the dev-player covenant, not the content generator.
**(4) Hardest line:** "There is but one infinite game." Minecraft is the closest shipping approximation: a game whose players keep converting it into the next game.

### 16. Esports (Spacewar 1962 → StarCraft: Brood War Korea 1998 → LoL 2009, Dota 2 The International 2011 →)

**(1) As played:** the most explicitly finite frame in gaming — brackets, best-of-five, the trophy, an entire industry of titles.
**(2) The hidden game:** the patch cycle. Rules change every season BY DESIGN — balance patches are P2 industrialized (rule mutation as a service the league sells). The meta is collaborative rule-evolution: pros discover, designers redraw; the players play WITH the boundary, then the boundary moves. Careers are narratives of continuation (a decade of Faker at the top is the infinite game made visible inside the finite frame); the theorycrafting/VOD/coaching economy is a P3 corpus; the league is a P5 machine whose product is next season. The Carse pathology is visible here too: professionalization swaps abandon for seriousness — burnout is what finite play does to people who must win for a living.
**(3) Contribution:** P2-as-service, P5 (the league as continuation machine), the spectator economy — and a standing warning: an audience-finite form stays healthy only while the infinite metagame above it stays alive.
**(4) Hardest line:** "Finite players play seriously; infinite players play with abandon." The stadium is the monument to seriousness; the patch notes are where the abandon still lives.

---

## Part III — master table (era / finite shell / infinite core / contribution to infinite-game design)

| Era / lineage | Finite shell | Infinite core | Contribution to infinite-game design |
|---|---|---|---|
| Senet + ancient boards (~3100 BCE →) | Race your pieces off; winner exits | Board as map of the afterlife; play as rehearsal of the endless journey | Game-as-pointing-device; duration proof (artifact outlives titles); P1 in myth |
| Go (~2500 yr) | One board, counted or resigned | Handicap + komi: rules mutated between games so play continues across skill gaps | P2 proto (scheduled legal rule mutation); P3 proto (joseki corpus); anti-exclusion social contract |
| Chess (~1500 yr) | Checkmate, title, draw-death | Theory corpus; format mutation (Chess960, tiebreaks) to defeat memorization | P3 at classical scale; rating ladder; format mutation as anti-exhaustion tech |
| Mancala family | Sow, capture, empty stores | The family: hundreds of local rule forks, nobody owns the rules | P4 at folk scale (variant culture); P5 oldest form (free continuation) |
| D&D 1974 | Module ends, session ends, TPK | The campaign under a DM whose job is keeping the table alive | **P2 full (arbiter as role); P4 first (authored dungeons); P1 embryonic (sheet-as-ledger); P5 embryonic (hobby economy)** |
| MUD1 1978 → EQ 1999 → WoW 2004 | Level cap, wizhood, raid clear | World persisting while absent; the other players; cap re-moved every expansion | P1 full (software persistence); P5 full (subscription = continuation revenue); P2-by-decree (patch cycle); guild institutions |
| Rogue 1980 → NetHack 1987 → DF 2006 | Permadeath; one run; fallen fort | Death-proof knowledge metagame; bones files haunting strangers' dungeons; "losing is fun" | P3 perfected; P6 (bones files); seed-as-contract; failure-as-fuel design law |
| Arcade 1978–83 | 3 lives, 1 credit, GAME OVER | High-score initials outliving the player; kill screen as visible boundary played WITH | P6 proto (leaderboard co-presence); unbounded record; institutional witnesses (Twin Galaxies) |
| God/sim 1989–2000 | Populous/Civ victory screens | SimCity's no-win sandbox; player-authored goals | P4 motivational (self-set objectives); maintenance-as-gameplay; systems-first design |
| Doom 1993 / Quake 1996 | Episodes, exit switches | WADs; rocket jump; deathmatch; engine lineage | P4 as file format; bless-the-bug (P2 lightest touch); open engine as released rulebook |
| Myst 1993 + adventure | Puzzles solved once; shelf | (Almost none — the finding) | The negative result: authored narrative ends; endings make museums, not worlds |
| Souls 2009– | Kill the lord, credits, NG+ | Async messages/bloodstains/phantoms; self-handicap builds; lore rereading | P6 perfected; P4 bounded (templated authorship — content inside a legal vocabulary) |
| Slay the Spire 2017/19 | One climb; deck dies | Ascension ladder; seed dailies; archetype mastery | P2 between runs (institutionalized self-handicap); P6 (seed dailies); seed honesty |
| Exanima/physics 2008– | Arena ladders, campaign stubs | Simulation removes the script; inexhaustible state space | Emergence as content; failure-as-information; infinite play from state-space depth, not rule mutation |
| Minecraft 2011 / NMS 2016 | Ender Dragon credits / empty infinite space | Players as rule-writers (redstone, servers, mods); NMS dev-player covenant | P4 maximum (crown transfer of authority); P1 (world remembers every block); covenant-over-generator lesson |
| Esports 1962 → | Brackets, trophy, titles | Patch cycle; meta evolution; careers of continuation; theory economy | P2-as-service; P5 (league as continuation machine); burnout warning (seriousness eats abandon) |

---

## Part IV — the verdict

**Question:** which single era invented the most infinite-game machinery, judged by what OUR fleet's world build (the bones-legal persistent world: `wow_bones.py` kernels → `wow_world.py` rooms-as-legality-tables → `wow_session.v1` receipts → `bones_adapter` Discord gates; plus mud.html's `mud_lore`/NG+/chronicle and the relay) actually needs?

**What the build needs, from the bytes:** (a) legality of mutation — VERB@ROOM rows, the Dispatch ordering law, typed `ILLEGAL_TURN` refusals: every world change through an authorized, receipted channel; (b) persistence with proof — `world_sha`, seeded RNG draw indices, byte-identical replay; (c) a meta that outlives runs — `mud_lore`, chronicle, NG+ ascension, the planned bones-file niche; (d) bounded player authorship — template-word messages, `game_modules/*.v1.json`. Map those to the primitives and the build's spine is **P2 (legality)** riding on **P1 (persistence)**, decorated with P3 and P4.

**Scoring the eras on first full inventions:**

| Era | Primitives first invented there | Verdict fit |
|---|---|---|
| D&D 1974 | P2 full, P4 first, P1 embryonic, P5 embryonic | The spine, in embryo, all four |
| MUD1 → WoW | P1 full, P5 full, P2-by-decree | Persistence + economics; mutation by vendor edict |
| Rogue → DF | P3 full, P6 (bones), seeds | The death-proof meta; the second need |
| Minecraft/NMS | P4 max, P1 | Authorship without a legality gate |
| Souls | P6 full, P4 bounded | Async co-presence in a legal vocabulary |
| Go | P2 proto, P3 proto | Scheduled mutation, never in-course |
| Everything else | — | Decoration, warning, or negative result |

**Verdict: D&D 1974.**

1. **The bones-legal build's defining problem is legality of mutation, not persistence.** Persistence is solved engineering — files, hashes, ledgers. Legality is law: who may change the world, through what channel, with what receipt. That is the DM problem, and D&D 1974 is the only era that made the rule-changer a role with license and accountability. The fleet's referee chain is exactly that DM made auditable: rulings over rules, but with sha256 where the table's memory used to be. `wow_session.v1` is the character sheet; the Dispatch law is "the DM's word is final, and final means logged."
2. **It is the only era that touches four primitives, and the one it owns outright — P2 — is the one the build cannot buy off the shelf.** Authored dungeons → `game_modules/*.v1.json`. Campaign continuity → the sessions ledger. Hobby economy → the fleet's own $0-lane, donation-grade continuation (we are already Toady-model).
3. **Why not the runners-up:** MUD1 made the world persist, but its mutation authority is vendor decree — a patch is a king's edict, not a referee's ruling; that is precisely the failure mode a legality-table referee exists to prevent. Minecraft maxes P4 with no gate (2b2t is P4 without P2: magnificent and lawless). The rogue line perfected P3 — the fleet's second need — but knowledge metagames are additive machinery, not the spine. Go invented P2's spirit (handicap) yet only between games, never inside one.

**The genealogy in one line:** MUD1 made the world persist; D&D made the world's changes legal; the bones-legal build is both finally in one process — but legality is the bone, so the debt runs to the table with the referee.

**The Carse seal:** no era ever ran a DM's authority with a rogue's death-proof ledger inside a MUD's persistent world. That is what the fleet is building: the attempt to make the infinite game receiptable. Carse closed his book with "There is but one infinite game." The bones-legal wager is that you can issue receipts in it.

---

## Footer

- **Deliverable:** Part I lens + six primitives · Part II, 16 era unpacks (shell / hidden game / contribution / Carse line) · Part III master table · Part IV verdict (D&D 1974).
- **Sources:** primary = seat knowledge of game history and of Carse's *Finite and Infinite Games* (1986); quotes cited from memory, marked where paraphrased. Grounded bytes read this session: `HG1_GAMING_HISTORY_WEAVE.md`, `HERMES_DIRECTIVE_BONES_REFEREE_20260916.md`, `CG3_ESTATE_INFINITE.md`, `SHARED_SURFACE_CONTRACT.json`. Web: zero fetches (no uncertain claim required it). Git: none. Paid APIs: none.
- **Bounded pointers (hashes of cited artifacts, sha256, computed at close):**
  - `wave_20260916/receipts/HG1_GAMING_HISTORY_WEAVE.md` → `4b42312a7e0e8fca7fd02b1b64f2b3659c3df4441b024c5ece0622265b477f51`
  - `HERMES_DIRECTIVE_BONES_REFEREE_20260916.md` → `af9bf9f6eb78ed0708cef8cda2600f0166d5b1b8e3f7685131bc4891fc162c0c`
- **Self:** 5,215 words / 33,276 bytes at close; authoritative self-hash at read time (`sha256sum` of this file).
- Self-hash note: a hash of this file written inside this file would falsify itself; the authoritative hash is `sha256sum` of this file at read time.
- Working log: Part II [x] · Part III [x] · Part IV [x] · Footer [x]. Receipt closed 2026-09-16.
