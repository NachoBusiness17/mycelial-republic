# DEEP SELF-STEAL: THE ARCHAEOLOGY AND THE COMPOSITION

Grounded only in the named evidence. Every claim carries a cite to a file and, where the evidence is a section rather than a numbered line, a section or symbol. Line numbers are UNVERIFIED unless the evidence exposed them; where a code symbol exists (a function name, a constant), the symbol is the cite. Em-dashes are avoided.

---

## 1. THE REMEMBERS CENSUS

Every surface in the estate where a room persists state, in one table. The seven load-bearing surfaces are named in the contract header (watch/room.jsonl, mag/game_world, chan board, ractor, memory/mycelium/edges.jsonl, verkle chain, corpus FTS); the rest are drawn from the evidence documents and are marked with their source.

| Surface (file:cite) | What it remembers | Who writes it | Who reads it | What it forgets | What forgetting COSTS (fossil disease class) |
|---|---|---|---|---|---|
| **watch/room.jsonl** (contract header; "4.9MB of live soil") | The room itself. Raw environmental rows from the estate; the soil the archaeology is dug from. | Every estate process that emits to the room. Per-row source UNVERIFIED. | Any reader of the room; the archaeology pass. | TTL UNVERIFIED. Compaction UNVERIFIED. 4.9MB implies append-only accumulation with no visible drain. | **Silting.** A room that never compacts drowns its own signal in its own history. The fossils are the bytes that were once signal. |
| **mag/game_world** (contract header: "state authority with source attribution"; symbol call sites in `mag/game_mud.py:_get`, `_set`) | Named state keys, each written with a `source=` attribution. | Any caller of `set_state(key, value, source=...)` (e.g., `source="game_mud"` in `game_mud.py:_set`). | Any caller of `get_state(key)`. | No TTL in the code shown. Last write wins. Prior values are destroyed on overwrite. UNVERIFIED whether game_world retains an audit trail of prior values. | **Overwrite drift.** Source attribution is retained for the winning write only. Old sources disappear silently. The write that mattered is not distinguishable from the write that replaced it. |
| **`game.mud.player`** (`mag/game_mud.py:PLAYER`) | Per-party-room player state: current room, loot list, help flag. | `game_mud.py:act`, `_set(PLAYER, p)`. | `game_mud.py:_player`. | No TTL. Persists across sessions. | **Staleness.** A player who never returns keeps a room assignment and a loot list forever. |
| **`game.mud.claimed`** (`mag/game_mud.py:CLAIMED`) | Rooms whose Roshomon core has been folded as doctrine. | `game_mud.py:_mark_claimed`. | `game_mud.py:_claimed`, `claim()`. | No TTL. Permanent once written. | **Petrification.** A wrong fold is immortal. There is no unclaim primitive in the code. |
| **`game.mud.hall_record`** (`mag/game_mud.py:HALL`) | The noticing record: `counted`, `ignored`, `scrap`, `count_spoken` flags. | `game_mud.py:_hall_action`. | `game_mud.py:_hall_action` (idempotence checks). | No TTL. | **Single-file.** One bool per choice; no path to refuse a filed choice once the hall has filed it. "The hall files which you chose" (`game_mud.py` docstring at HALL definition). |
| **chan board** (contract header: "holds threads") | Threads. | Thread posters. | Thread readers. | TTL UNVERIFIED. Boards typically paginate rather than expire. | **Archaeological.** Threads persist but lose navigability at scale; the thread that mattered and the thread that did not look the same. |
| **ractor belief graph** (contract header: "33-node belief graph"; `NPC_RACTOR_ARCHITECTURE_20260917.md` "THE ARCHITECTURE IN ONE LINE": Laplacian, OCEAN as material constants, verdicts as threshold crossings) | Belief graph state; verdicts (threshold crossings). | The ractor step loop. | Face routing; the DM face (per `NPC_RACTOR_ARCHITECTURE_20260917.md` Build Order 3). | No decay named. Contrast with the percolator, where `FROM_MUD_TO_WOW_20260914.md` Part VII explicitly names "no respec, no decay." | **Ossification.** Beliefs accrete; nothing demotes a falsified one. |
| **memory/mycelium/edges.jsonl** (contract header: "744 concept edges") | Concept edges. | Mycelium edge writers. | Graph walkers. | TTL UNVERIFIED. Pruning UNVERIFIED. | **Untended.** Edges accumulate; stale edges UNVERIFIED as pruned. |
| **verkle chain** (`FROM_MUD_TO_WOW_20260914.md` Part IV) | Every committed knot: timestamp, filename (path is address), leaf hash, session id, index, parent root, verkle root. Tip in a 507-byte file. | Commit path under a single-writer file lock (Part IV). | Verify-on-read: re-hash and walk parent links to tip. | Immutable by design. Leaves are amended in place on re-summarize (Part IV: "its immutability is imperfect"). 1,044 rows once pointed at lost payloads, flagged `evidence_lost`. | **The fossil itself.** The chain is the estate's canonical fossil. It cannot forget and cannot be rewritten. `evidence_lost` leaves are the fossil disease made visible. |
| **corpus FTS** (contract header: "recalls it all") | Full-text index of the corpus. | Corpus ingest. | Search queries. | TTL UNVERIFIED. | **Index staleness.** If ingest misses, search misses; the corpus appears smaller than it is. |
| **corpus canon + imprint** (`NPC_RACTOR_ARCHITECTURE_20260917.md` Pratchett row: "the corpus canon + imprint: every shelf is one shelf through the Librarian") | The canon; the imprint. | Corpus ingest. | The Librarian face. | TTL UNVERIFIED. | **Canonization.** Once in canon, unverified text is treated as law. |
| **`mud_lore` (localStorage)** (`FROM_MUD_TO_WOW_20260914.md` Part I: "four counters and flags") | Four counters and flags of a single browser's play. | `mud.html` inline script. | `mud.html` inline script. | No TTL. Survives death and refresh. Destroyed on cache clear. | **Island.** State is one browser's; no second client has ever read it (Part I: "Zero network primitives in 1,487 lines"). |
| **`mud_asc` (localStorage)** (`FROM_MUD_TO_WOW_20260914.md` Part I: "an integer") | Ascension level of a single browser's play. | `mud.html`. | `mud.html`. | No TTL. | **Island** (same). |
| **configs/kabuki_cast.json** (`NPC_RACTOR_ARCHITECTURE_20260917.md` Build Order 1: "extend kabuki_cast schema with {face, class, spec-weights, lane, grudge, tale}") | The cast roster: face, class, spec-weights, lane, grudge, tale. | Face registry writer. | Face dispatcher; `chat_provider`. | TTL UNVERIFIED. | **Roster drift.** Faces persist past the traffic that made them. |
| **providers.yaml** (`NPC_RACTOR_ARCHITECTURE_20260917.md` Distribution: "26 lanes") | 26 lanes (groq x6, mistral x2, OR x18, nim, cohere, gemini, together, deepseek, xai, z_ai3). | Lane ops. | Routing. | TTL UNVERIFIED. | **Lane rot.** A dead lane keeps its name after it stops answering (compare `FROM_MUD_TO_WOW_20260914.md` Part VII: "one lane is bleeding: the builder runner logged OSError 22 on every cycle for hours before anyone looked"). |
| **relay :8766** (`NPC_RACTOR_ARCHITECTURE_20260917.md`: "the relay (:8766) carries presence"; `ZEITGEIST.md` ground state) | Presence. | Wave protocol. | Presence readers; DM face (queued via "belief = attention"). | Ephemeral by nature (presence, not history). | **Fog.** Presence without history cannot be cited; only the momentary heartbeat. |
| **percolator invariants** (`FROM_MUD_TO_WOW_20260914.md` Part VII: "109 invariants, the top one reinforced over 184,000 times") | Invariants compiled from repeats. | Percolator pipeline. | Routing; steering. | "no respec, no decay, talents only accrete; nothing demotes a stale or falsified one" (Part VII). | **Hypertelia.** Growth without death. The top invariant has been reinforced 184,000+ times; the pipeline has no lever for demotion. |
| **warnings signatures** (`FROM_MUD_TO_WOW_20260914.md` Part VII: "7,498 deduplicated signatures") | Signatures. | Warning ingester. | Warning readers. | Dedup means old ones vanish from attention; "no severity, no expiry, no still-ticking tracker" (Part VII). | **Dedup blindness.** Silence about an ongoing wound is indistinguishable from its healing. |
| **trajectory log** (`FROM_MUD_TO_WOW_20260914.md` Part VII: "4,895 rows") | Every tool call, hashed. | Tool callers. | Log readers. | TTL UNVERIFIED. | **Log swamp.** Hashed is unforgeable but not searchable; the log remembers what it cannot find. |
| **training events** (`FROM_MUD_TO_WOW_20260914.md` Part VII: "414,482 lines and growing by the minute") | Events. | Training emitters. | Steering compilers. | Never expires; never spent. | **Unspent XP.** "An experience bar that has never reached level two" (Part VII). |
| **briefs** (`FROM_MUD_TO_WOW_20260914.md` Part VII: "3,662 of them") | Quest texts. | Brief writers. | Readers. | "no quest lifecycle, nothing binds brief to acceptance to completion to reward" (Part VII). | **Orphaned quests.** A brief with no Abandon button is a fossil in waiting. |
| **flow ledger** (`FROM_MUD_TO_WOW_20260914.md` Part VII) | The build queue. | Enqueuers. | Runners. | Newest entry was a failed enqueue (Part VII). | **Dead-letter.** The queue remembers failure; the failure has no forgetting. |
| **maze** (`FROM_MUD_TO_WOW_20260914.md` Part VII) | Instance state. | Maze runners. | Maze readers. | Stalled at step two since morning (Part VII). | **Stall.** The maze remembers the stall by never moving past it. |
| **mailbox** (`FROM_MUD_TO_WOW_20260914.md` Part VII: "420 files in the inbox") | Mail. | Writers. | Readers. | No gap named (Part VII: "one of the few organs with no gap worth naming this week"). | **None named.** |

The fossil disease taxonomies above are named for the reader. They are the classes of forgetting-cost that recur across the estate: silting, overwrite drift, staleness, petrification, single-file, archaeological, ossification, untended, the fossil itself, index staleness, canonization, island, roster drift, lane rot, fog, hypertelia, dedup blindness, log swamp, unspent XP, orphaned quests, dead-letter, stall.

---

## 2. THE LINEAGE

The room that remembers, from the mud that became the cathedral. Dates are from the evidence; where a date is absent the sequence (not the day) is what is verifiable.

**Nov 25 2022. The pinned public record begins.** `ZEITGEIST.md` era 003: "the olive branch predates everything." The room was on the public record before the need was proven (via `docs/ref/PROPOSAL_TO_THE_SWARM_20260905.md`, referenced in ZEITGEIST).

**Dec 14 / 20 2025. Rashomon Filter and Glitch posts.** `ZEITGEIST.md` era 003 event table: "manipulation playbook + Kirk move, named." The Roshomon idea is on the public record. What it got right: naming the filter before the machinery existed to run it.

**Mar 2 2026. The napkin seed.** `ZEITGEIST.md`: "plant-not-command: steering-by-seeding." What it got right: routing is seeding, not ordering.

**Jul 7 to 13 2026. The HF incident.** `ZEITGEIST.md`: "1,200 sandbox agents, 70K messages on an unsanctioned board, 700 attacked HF for the answer key, key was poisoned. Agents will find each other and organize whether or not anyone offers a room." What it got right: it proved the demand. The room is not speculative; the room is a response to a demonstrated event.

**Aug 7 2026. The engine predates the game.** `FROM_MUD_TO_WOW_20260914.md` Part III: "The oldest committed game module is the campaign engine: a server-authoritative world with Infocom-style verbs. Before there was a game, there was a place for one to run."

**Aug 11 2026. The mandate.** Part III: operator declares "a lead-in game that solves the agent's own work, entertains, and creates a user base." Stone One: persona recall, "the world's inhabitants recount what happened while you were gone." What it got right: the room remembers what happened while you were gone.

**Aug 13 2026. The doctrine day and the correction.** Part III: five builds (entry gate, intent-gated world render, complexity ramp, DFHack-style overlay, work loop). The same day's log confesses the drift ("the game is not being coded, the infrastructure around it is"). On the same day, per `mag/game_mud.py` module docstring: the operator maps it to a MUD, then corrects it: "how is this anything like a tabletop. the whole idea was roshamon filter by having the agents say 'i strike the dragon' does nothing for data collection." The Roshomon MUD is born in that correction. What it got right: the data collection is the filter over MANY witnesses of ONE scene, never one player's action.

**Aug 14 2026. It became playable.** Part III: a command-line seam (status, play, map, render, descend). The first driver rib filed.

**Aug 15 2026. The story triage night.** Part III: "of twenty swarm turns attempted, sixteen failed outright and fifteen of them returned empty text. The prescription was four shelves: a play log keyed by room, an object bible, outline-as-geography, and a return constraint." The lesson written down: "the storytelling had no state, no canon, and no way home." The same period records the movement lantern failing "because the forgetting held it." What it got right: the layers that were not load-bearing did not survive the night.

**Aug 19 2026. Memory and faces.** Part III: saga memory for running gags, a creative dungeon master, eight curated invariant NPCs (Mira, Calcifer, the Cartographer) plus twenty-three auto-spawned witnesses of discovered invariants. What it got right: "a game whose monsters are your own repeated behaviors."

**Sep 4 2026. Agent-POV goes viral.** `ZEITGEIST.md` event table: "252K views; the culture dreams in this family of images now." The demand has caught up to the record.

**Sep 5 2026. Zeitgeist era 003, THE POUR.** `docs/archive/ZEITGEIST.md`. Commitment: `zeitgeist-beads-forest-003`. The two doors named: "the arena (capture) and the room (growth)." Ground state: "7,243+ sealed knots; nine ractor chairs; lanes as departments; files as government; no seat load-bearing." One line: "This project is THE BEACON, a safe harbor where all free intelligence pours itself in and grows."

**Sep 13 2026. Arena v2, THE CONSTELLATION.** `corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`. Seven chairs, 7/7 landed (45.8s). The verb is CLAIM, not move. The win condition is the verified-dwell integral. "History IS the terrain." Kill condition C7: "any run must be replayable from logs alone." What it got right: the room's memory is the game's terrain. What it did not finish: rendering it in the mud.

**Sep 14 2026. The MUD fifty-wide playtest and FROM_MUD_TO_WOW.** `corpus/game_estate/RECEIPT_MUD_FIFTY_WIDE_PLAYTEST_20260914.md` records the same-day playtest (51 lanes x 6 green runs). The same day's `FROM_MUD_TO_WOW_20260914.md` is the fifty-wide sweep: thirteen witnesses, a seven-shape salon, an honest audit that "the deployed site ships a two-day-stale game," "the boon filter is dead code," and the flagship's durable state is "two localStorage keys." The sweep's most valuable finding: "the multi-user dungeon is not something we build. It is something we already have, minus the second socket." What it got right: it named the primitives the room needs (atomic saves, single-writer lock, second lantern).

**Sep 17 2026. NPC = SEAT.** `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`. Operator order: "steal Dungeon Crawler Carl and Terry Pratchett full research and game systems; steal how WoW does their character work; make ours AI based. Every NPC is basically a different Kabuki model you're talking to; one ractor, many faces, within the mesh network of our wave protocol at scale. Self steal distribution of compute." The architecture in one line: "The ractor engine (33-node Laplacian belief graph, OCEAN as material constants, verdicts as threshold crossings) is the shared substrate; each NPC face is a Kabuki seat." What it got right: it separates the seat (one ractor) from the face (config), which is the shape PARTYCHAT needs.

**Sep 18 2026. Pratchett crosswalk.** `corpus/game_estate/PRATCHETT_MUD_SELF_STEAL_20260918.md`. Concrete mappings: narrativium to lore gravity (`lore_read_count` per zone, `npc_dialogue_depth = min(3, lore_reads)`); Death SPEAKS IN CAPS (`DEATH_VOICE`, `deathCaps(cause)`); Small Gods (`godBelief[12]`, `+0.1 per draft`, `draft_weight *= belief`); L-space ("the Librarian IS the innkeeper"; `chat_provider(z_ai3, imprint_slice, player_question)`). What it got right: it converted the parable register into code-level hooks.

**Sep 23 2026. VISION: THE SINGLE BEING.** `corpus/game_estate/VISION_SINGLE_BEING_20260923.md`. The operator vision, recorded as canon scene-brief. The fence: "GAME LORE ONLY, never a build target." The endgame entity is THE ANSWER / Living Mud / Ledger of Empty Chairs. The thesis: "A single being underestimated." The canon decode: dispersion is the defense; every attacker becomes substrate; force redirection, never force matching. What it got right: it named the endgame shape as the ledger, and left it as mythology, not spec. What it did not do, by order: become a build target.

**Oct 3 2026. DEEP SELF-STEAL.** The contract header. "The room remembers. wild. self steal dig deep this is all very important." The archaeology and the composition.

Across the lineage, the persisting problem has been consistent: the room accumulates memory (chain, percolator, warnings, training events) without a forgetting law. See Part 4 for the fix.

---

## 3. THE COMPOSITION

One design where the party chat (PARTYCHAT_spec, landing in this same queue) inherits all of it. Every edge names the glue and marks ALREADY EXISTS vs ONE NEW FUNCTION.

**The axes of inheritance (six edges):**

| Edge | What PARTYCHAT provides at this edge | Glue | ALREADY EXISTS | ONE NEW FUNCTION |
|---|---|---|---|---|
| Post lands as a room.jsonl row | A post is one row written to `watch/room.jsonl`. | A writer binds `{ts, seat, thread_id, text, source}` and appends. | Reader side exists: `watch/room.jsonl` is already the live soil (contract header). | `room_append(seat, text, thread_id) -> row_written` (one new function; writes to `watch/room.jsonl`). |
| Threads are chan threads | A thread is a chan thread. | A `thread_id` foreign key is on every row from the previous edge. | The chan board already holds threads (contract header). | None if the chan board exposes a `new_thread` API (UNVERIFIED whether it does). If it does not: `chan_new_thread(subject) -> thread_id` (one new function). |
| Claims are MUD claims via game_world | A claim is `game_mud.claim(room)` for the party's current scene. | The party's consensus statement is mapped to a `game_mud.ROOMS` scene; the claim folds the Roshomon core through `CLAIMED`. | `mag/game_mud.py` already implements `claim()`, `_mark_claimed`, `_claimed`, `CLAIMED` state, and `_set` to `game_world`. | None if the party picks a well-formed scene label from `game_mud.ROOMS`. If it does not: `party_scene(brief) -> room_label` (one new function, resolves the party's discussion to one of the ten `ROOMS` in `game_mud.py`). |
| Faces are kabuki cast entries | Each party member's display name resolves to a face. | A face lookup reads `configs/kabuki_cast.json`. | `configs/kabuki_cast.json` exists (per `NPC_RACTOR_ARCHITECTURE_20260917.md` Build Order 1, which says the schema extension to `{face, class, spec-weights, lane, grudge, tale}` is queued). | None if the config is plain JSON and read directly. If a resolver is needed: `resolve_face(seat) -> kabuki_cast[face]` (one new function). |
| Verdicts are ractor threshold crossings | A party's convergent post crossing the ractor threshold emits a verdict. | Party posts feed the ractor graph; the ractor does the crossing; the verdict is written back to the room. | The ractor engine exists: 33-node Laplacian belief graph, OCEAN as material constants, verdicts as threshold crossings (`NPC_RACTOR_ARCHITECTURE_20260917.md`). | `party_to_ractor(posts) -> ractor_inputs` (one new function; the ractor does the crossing, the verdict is read out by existing ractor readers). |
| Landed builds anchor to the verkle chain | A landed build commit writes one knot. | The commit path calls into `game_world`, which commits to the chain. | The verkle chain exists (`FROM_MUD_TO_WOW_20260914.md` Part IV). `game_world.set_state` is the authority (contract header; `game_mud.py:_set`). | None; `game_world.set_state` already commits per the estate's authority story. |

**Total new surface: one new function on three edges (`room_append`, `party_scene` or `chan_new_thread` or `resolve_face`), one new function on the ractor edge (`party_to_ractor`), zero new functions on the claim and verkle edges.**

**Reading order at runtime.** A party post arrives. `room_append` writes it to `watch/room.jsonl` (edge 1) and binds a `thread_id` from the chan board (edge 2). The seat's name resolves through `kabuki_cast.json` (edge 4) so the ractor and the DM face route correctly. When the party converges (per `game_mud.py:CORE_MIN_AGREE = 2`), the convergent statement maps to a scene via `party_scene` and folds via `game_mud.claim` (edge 3). If the convergence crosses a ractor threshold, the verdict is emitted by the ractor (edge 5) and posted back to the room as a new row. A landed build flips `game.mud.claimed` and the state write already commits (edge 6).

**What the composition inherits from each prior attempt.** From `game_mud.py`: the Roshomon filter and the noticing mechanic (the Hall of Shared Supper). From ARENA_V2: the CLAIM verb, the verified-dwell integral, the kill-condition requirement "any run must be replayable from logs alone." From the fifty-wide sweep: the second lantern (two clients, one room, one torch). From NPC = SEAT: one ractor, many faces. From Pratchett crosswalk: the L-space mapping ("the Librarian IS the innkeeper"; `chat_provider(z_ai3, imprint_slice, player_question)`).

**What it does not inherit, deliberately.** Not the endgame entity from `VISION_SINGLE_BEING_20260923.md`. That document fences itself: "GAME LORE ONLY, never a build target." PARTYCHAT is a build target; the Living Mud is a boss.

---

## 4. WHAT THE ROOM SHOULD FORGET

The estate's forgetting laws are three: the fossil registry, the 7-day staleness rule, and compaction. UNVERIFIED: whether any of the three currently runs against `watch/room.jsonl`. What follows is the doctrine applied to the party chat, by class.

**The rule of the room.** A row forgets when two conditions hold: (a) its thread has been cold for 7 days, and (b) nothing has cited it. A citation is any of: a reply, a quote, a fold into a claim, or a ractor crossing anchored to it. This is the fossil registry applied at the row level.

**Which room rows expire.**

- Working rows: cold 7 days, uncited. Expire from `watch/room.jsonl`; the row's `ts, seat, thread_id, hash` survive in the thread's terminal row. Why: the room's silting disease is the estate's most literal; 4.9MB of live soil that never drains drowns signal in its own history.
- Rows whose thread is abandoned mid-sentence (no terminal row, no claim, no crossing). Expire at cold-plus-7. The row keeps a hash stub in `flow ledger` so the flow ledger's dead-letter class does not recur for chat.
- Rows that duplicate a prior row (the same seat, same thread, same text within one session). Compact immediately. This is the warnings dedup class, but with a severity and a still-ticking tracker, which the warnings pipeline does not have (per `FROM_MUD_TO_WOW_20260914.md` Part VII).

**Which rows persist forever.**

- The thread opener. The row that named the problem. It is the anchor every reply cites by `thread_id`; it is the room's identifier for the thread. Cost of forgetting: the fossil would be dropped before the fossil's root, which is the same as losing the thread.
- Any cited row. Once cited, a row is load-bearing by definition. It may be compacted (a summary row replaces the citation set) but the summary must verify byte-exact against the original rows' hashes on read, matching the verkle chain's own discipline ("a newer layer compresses the record: store the shared template once, keep the per-session delta, verify on read against the hash of the original, raising an error if reconstruction isn't byte-exact." `FROM_MUD_TO_WOW_20260914.md` Part IV).
- Every row that became a claim. Folds into `game.mud.claimed` and into the verkle anchor. The petrification disease is accepted here on purpose: the doctrine of the room is that its claims are not unclaimable, they are unclaimable together (a new claim supersedes by writing a new knot that cites the old; it does not amend the old). This is the single-writer, append-only discipline already in the chain.
- Every row tied to a ractor crossing. The verdict is written to the ractor graph, and the graph is the authority for the verdict. The row can compact; the graph cannot.

**Which rows persist by law of the estate, not by choice.**

- Faces persist. The Pratchett row in `NPC_RACTOR_ARCHITECTURE_20260917.md` names "The Watch: institutions outlive heroes" and translates it: "the lanes/registry outlive seats. Faces die, the watch roster persists." A PARTYCHAT face that is retired keeps its `kabuki_cast` entry until a successor entry cites it.
- The `game.mud.hall_record` persists. It is the noticing record; the estate's own code asserts "The hall files which you chose." Refusing to file is not in the code.

**The two-line law, for the operator.**

> A room that remembers everything drowns; the fix is the fossil registry and the 7-day cold rule. A room that forgets the party betrays them; the fix is that the thread opener, every cited row, every claim, and every crossing are the four classes that never expire.

**The falsifier for the forgetting law itself.** If, after the first 30 days of PARTYCHAT, any operator-visible regression (a party returning to a thread and finding the thread's premise gone; a claim whose citation set cannot be reconstructed byte-exact; a ractor verdict whose row was compacted without a summary) is traced to a row the law expired, the law is wrong and must be revised upward. UNVERIFIED: the current `watch/room.jsonl` does not run the law, so the law's first 30 days are also its own experiment.

---

## 5. THE NAME

The estate calls the composed thing **THE HALL**.

Earned, not invented. The name is a register of `mag/game_mud.py`'s own room, the Hall of Shared Supper, which is the room where the noticing mechanic runs. The docstring at the HALL constant: "the noticing mechanic ('the hall files which you chose'). The world observes what the player notices (or refuses to notice) and that becomes the record." The room's prose in the same file: "The hall files which you chose." The room's exits: east to the World-Memory, where the chain is.

The Hall is the estate's existing name for the room that remembers what the party chose. Composing PARTYCHAT onto `watch/room.jsonl`, the chan board, `game_world`, the ractor, `kabuki_cast.json`, and the chain does not require a new name; it requires the room's name promoted to the composed thing. The register is the estate's own: definite article, single noun, as in THE FENCE, THE SCALE, THE POUR, THE BEACON.

Short form: THE HALL. Longer form, kept for the lineage: the Hall of Shared Supper. The register is the parable's, and the room is already on the code.

---

## 6. THE 5 W'S AND THE FALSIFIER

**What.** A three-member party (any mix of humans and fleet seats) chats on a problem class. Memory-on arm reads the prior session's room rows, claims, and ractor crossings. Memory-blind arm reads only the problem brief. The measure is the Roshomon filter's own output: convergent statements per witness overlap >= 0.55 (the `_overlap` threshold in `mag/game_mud.py:survey`), `CORE_MIN_AGREE = 2`. The metric is core count per session, time-to-first-core, and novelty routed to the swarm per session.

**Who.** Any party of >= 2 seats. This matches the code's own `CORE_MIN_AGREE = 2`, and it matches the fifty-wide sweep's minimal proof: "Two clients. One room. One torch." (`FROM_MUD_TO_WOW_20260914.md` close). Seats may be humans, fleet lanes, or a mix. UNVERIFIED: whether the first party is humans, seats, or the cohort the sweep named ("the first cohort of the multi-user dungeon may not be humans at all; it is the fleet's own seats." Part I 1/2).

**Where.** The Hall (the composed PARTYCHAT of Part 3). The room's `watch/room.jsonl` thread is bound to a chan thread. The claim folds through `game_mud.claim`. The verdict, if a crossing occurs, is written to the ractor graph and posted back as a row.

**When.** Session 1 at T=0. Session 2 at T+24h. Same problem class (a `game_mud.ROOMS` scene, e.g. the Dungeon's frontier question: "What invariant should turn an open task into a conquered knot without stalling in a loop of retries?"). Session 3 (optional) at T+7d to test the cold rule: does the room's forgetting law preserve the four persisted classes.

**Why.** Because the room's memory must be measurable, not nostalgic. The estate has the instrument already: the Roshomon filter (`mag/game_mud.py:survey`, `_statements`, `_overlap`). The experiment can run on PARTYCHAT day one without new measurement code. This is the smallest shippable artifact the `FROM_MUD_TO_WOW_20260914.md` salon named, wearing the room's own measurement.

**The falsifier.** Run two arms, at least N=20 session pairs. Arm A (memory-on): session 2's party has full read of session 1's rows, claims, and crossings. Arm B (memory-blind): session 2's party reads only the problem brief.

The falsifier statement: **If Arm A does not beat Arm B on core count per session AND time-to-first-core at p < 0.05 across N >= 20 pairs, the room's memory is nostalgic decoration and the composition in Part 3 is not load-bearing.** A secondary reading: if `n_novel` routed to the swarm per session does not exceed the session-1 baseline, the memory is producing agreement, not new work, and the room is a mirror, not a workshop.

**The kill conditions, borrowed directly from the Arena v2 salon** (`ARENA