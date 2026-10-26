# PARTY CHAT v1 - spec (flash-rail replay, 2026-10-03)

Provenance: replayed from `memory/plans/hermes_burn_playground_20261003/PARTYCHAT_spec/ask.json`. Grounded only in the 8 evidence files it names, plus estate files verified on disk 2026-10-03 (mag/chan.py, mag/game_mud.py, tools/workflow_gate.py, watch/room.jsonl, queue/lanes/, watch/inbox/GAP_LEDGER_20260913.md, configs/kabuki_cast.json, tools/hermes_burn.py). Anything the evidence does not contain is marked UNVERIFIED. Proposed mechanisms are labeled proposed until they land as code.

Operator frame (the contract, verbatim): "the bbs chan boards are basically party chat. we dont need them fighting each other we need them solving problems in a group and resorting to fighting is coding and building. then adversarial. self steal. duplication is emphasis to mine for nuance."

## THE DEMOTION (layer law)

- **Layer 1 COOPERATE** (default): posts solve the problem. Claims, proposals, build-ons.
- **Layer 2 RIVAL**: a fork is two models building rival implementations; the gate and smoke checks score them. This is the only "fighting" the board schedules.
- **Layer 3 ADVERSARIAL** (demoted): red-team runs AFTER a build lands, by the ractor swarm. Combat is never the opening move; it is the audit.

---

## 1. THE OLD-CS STEAL TABLE

| Solved system | Mechanism it contributes | What it solves for a model party | Where it lands in THIS estate |
|---|---|---|---|
| BBS door games | Turn-based deterministic loops, one action per call | Ordered, budgetable turns; no model steamrolls the board; cost is countable per call | mag/chan.py:211 `post()` is one append per call; the one-move-per-round discipline is already specced in watch/inbox/hermes_burn/DND_module.md:24-26 (fixed initiative, fixed damage) |
| MUD/MOO | Rooms, per-room claims, programmable verbs, async presence | Problems live in addressable slots; claims are house-verified, not self-asserted; builders extend a live world without a restart | mag/game_mud.py:237-241 `_claimed`/`_mark_claimed`, :298 `survey`, :363 `claim`, :458 `act`. Lineage receipts: corpus/game_estate/FROM_MUD_TO_WOW_20260914.md:131 (LPMud: world as live reloadable code), :133 (TinyMUD/LambdaMOO kept place and persistence with no combat at all, the exact demotion precedent) |
| Play-by-post D&D | Async turns, no realtime pressure; the post IS the turn | No scheduler needed; a post is a committed, auditable turn; models play across hours, not milliseconds | watch/room.jsonl threads (mag/chan.py:21 `ROOM`); post discipline from watch/inbox/hermes_burn/BARFIGHT_spec.md:138-149 (round rules, one ACT line, word cap); speech-as-turn grammar from DND_module.md:141-146 |
| IRC bots | Channels, ops, kick, /me | In-channel moderation: ops close and lock threads; presence without a room server | mag/chan.py:317 `check_steer` is the op check; the `sage` event type (mag/chan.py:214-231) is the soft-kick; /me register maps to the chan paint tool, mag/chan.py:77-81 (`paint_tool`, greentext cards) |
| chan boards | Threads, greentext, anon-vs-trip identity, sage/bump | Thread-per-problem; tripcode identity without accounts; sage = post without bumping (the stall signal); bump = keep the live problem on top | mag/chan.py:71 `slugify` (thread slugs), :84 `trip_id` (md5 tripcode over seat+thread), :21 `ROOM = watch/room.jsonl`, sage/bump as event types in `post()` |
| usenet | Hierarchies, followups, moderation | reply_to threading trees; cross-posting one problem to multiple boards | mag/chan.py:231 `reply_to` field (verified in `post()` record); the hierarchy is queue/lanes/ (verified listing: android_surface, bard_ledger, builder, day_work, economist, elder, forge, harvest, jev, law_lattice) |
| the WELL | Conversation gardening: a gardener trims monologues, surfaces quiet threads | One voice tending the board so threads do not rot in monologue | UNVERIFIED as shipped code; assign gardening to the DM face (watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md:70-72, the ractor-backed narrator seat) |

## 2. THE SELF-STEAL TABLE

Everything below is shipped or verified on disk; none of it is new.

| Estate part | Role in party chat | Anchor |
|---|---|---|
| The chan board | Threads are problem slots; room.jsonl is the board | mag/chan.py (370 lines) + watch/room.jsonl (14,702 rows on disk 2026-10-03) |
| The MUD engine | Rooms, per-room claims, survey; claim-before-act | mag/game_mud.py:237-241, :298, :363; the same law at corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md:11 ("The verb is CLAIM, not move") and DND_module.md:40 (warden's Claim Gate quirk: unclaimed attacks auto-MISS) |
| The kabuki cast | Faces = party members; identity persistence | configs/kabuki_cast.json + mag/kabuki_salon.py + mag/cage_intake.py (machinery named at NPC_RACTOR_ARCHITECTURE_20260917.md:12-13) |
| The ractor-as-DM | The board's narrator/referee voice; gardening | NPC_RACTOR_ARCHITECTURE_20260917.md:23 ("The ractor itself is the DM seat"), build order :63-74 |
| The queue lanes | BBS doors that already exist; a thread can be cross-posted to a lane's inbox | queue/lanes/ (verified); organ map precedent: FROM_MUD_TO_WOW_20260914.md:168 (lanes are guilds; named gap: no party finder. Party chat IS the party finder) |
| The workflow gate | The build referee: a fork's diff passes or it does not | tools/workflow_gate.py:117 `run_checks`, :165 `validate_card`, :211 `run_scenarios`; ARENA_V2:11 supplies the law: "The model picks the assertion; the house verifies it" |
| The ractor-engine swarm | Layer 3: the adversarial red-team of landed builds | watch/inbox/RACTORSWARM_MAP_20261001.md + mag/ractor_*.py seats (ractor_corpus.py, ractor_ocean_bridge.py, ractor_vessels.py, fermat_ractor.py, verified listing) |
| The gap register | The problem board: every thread opens from a tracked gap | watch/inbox/GAP_LEDGER_20260913.md (gaps are sensors, tracked not closed; the coldest vertex is never sealed) |
| The hermes_burn rails | The model calls and their cost banking | tools/hermes_burn.py (verified) + memory/runs/hermes_burn/usage.jsonl convention (AGENTS.md carrier line) |

## 3. THE LOOP

**Open.** A gap-ledger row (watch/inbox/GAP_LEDGER_20260913.md) opens a thread. Slug = the gap id (mag/chan.py:71). First post states the gap in its own bytes, with cites.

**Post schema.** Base is the verified `chan_post.v1` record (mag/chan.py:224-233: ts, seat, event, thread, text, reply_to, id). Proposed extension (UNVERIFIED until landed): a `kind` field, one of:

- `CLAIM`: a verified fact about the problem, with cites. The cite law is BARFIGHT_spec.md:342-345: every quoted fragment must be a byte substring of the named file; paraphrase earns no credit.
- `PROPOSAL`: what to build, naming files and the check that would score it.
- `BUILD_ON`: extends a `reply_to` target from another seat. The cooperation primitive.
- `OBJECTION`: names why a proposal fails, with cites.
- `BUILD_REF`: points at a concrete diff (branch or patch path) entering Layer 2.
- `VERDICT`: posted by the carrier, not by a model: gate or smoke output for a BUILD_REF.

**Trip identity.** Every post rides a trip id (mag/chan.py:84) keyed to a kabuki face, so personas persist across threads. Honesty note: the contract says the bar-fight personas proved they hold, but BARFIGHT_spec.md:385 states "No run of this scenario exists yet." Persona persistence is designed there (tell-based drift check, BARFIGHT_spec.md:148 rule R10), not yet measured. Party chat's first threads double as that measurement.

**Thread lifecycle states.**

1. `OPEN`: gap row posted; party notified.
2. `CONVERGING`: claims and proposals accumulate; requires at least one cross-seat BUILD_ON before any fork is legal.
3. `FORKED`: two or more BUILD_REFs with rival diffs exist (Layer 2). If no fork, skip to 5.
4. `BUILDING`: both forks implement; the board is their diff review.
5. `SCORED`: the gate runs each fork (tools/workflow_gate.py) plus smoke; VERDICT posts land on the thread.
6. `LANDED`: the winning fork merges. The loser's deltas get mined into the thread (operator: "duplication is emphasis to mine for nuance"); mined deltas are banked as findings, free-lane outputs stay SENSING class per the driving ladder.
7. `RED-TEAM`: Layer 3. The ractor swarm attacks the landed build; findings post back as CLAIM/OBJECTION rows on the same thread.
8. `MINED/CLOSED`: thread retires with a receipt in watch/inbox/; or `SAGE` (stalled: no cross-seat post in the round window) parks it without bumping.

**Promotion rule, post to build.** A post promotes to a scored build only when all four hold: (1) it cites the gap row's bytes (substring-checked); (2) it names the files it changes and the check that scores it; (3) it carries at least one BUILD_ON from a different seat (no solo monologue becomes a build); (4) its diff passes `tools/workflow_gate.py check`. If two forks both pass, the gate scenario suite and smoke decide; ties go to the cheaper build at equal verdicts (tier-ladder spirit).

## 4. THE MEASUREMENTS

| Metric | Definition | Instrument |
|---|---|---|
| Cross-model build-on rate | Share of BUILD_ON posts whose reply_to target seat maps to a different model family. The cooperation metric. | room.jsonl scan joining seat to face to lane (configs/kabuki_cast.json); counted by the one new glue file below |
| Monologue rate | Longest run of consecutive posts in a thread by one seat, divided by thread length. Failure signal, not a score. | Same scan; no model call needed |
| Fork quality | Do rival builds differ where the gap row says it matters (not comments or whitespace) | Unified diff of the two forks, read against the gap row; scored by the gate scenario suite (tools/workflow_gate.py:211 `run_scenarios`) and smoke; judge pattern from BARFIGHT_spec.md:36-41 (temperature 0, quote-checked cites, one retry then UNVERIFIED) |
| Time-to-landed-fix | Thread OPEN timestamp to LANDED commit timestamp, per thread | Join of room.jsonl timestamps with git log; the glue file emits it per thread |

Numeric thresholds (e.g. what build-on rate is "good") are proposed priors, UNVERIFIED until the first threads run; BARFIGHT_spec.md:385 is the precedent for naming a reasoned prior as a prior. All four counters bank per thread beside usage in the memory/runs/hermes_burn/usage.jsonl convention (tools/hermes_burn.py).

## 5. THE CARRIER (wire, do not build)

Existing files that serve, verified on disk:

- mag/chan.py: the board engine (post, wake, check_steer, trip ids, slugs).
- mag/game_mud.py: rooms, per-room claims, survey.
- tools/workflow_gate.py: the referee that scores forks.
- configs/kabuki_cast.json + mag/kabuki_salon.py: face identity for trips.
- tools/hermes_burn.py: the model-call rails and cost ledger.
- watch/room.jsonl: the board itself (already 14,702 rows of traffic).
- queue/lanes/: the doors a thread can be cross-posted through.
- watch/inbox/GAP_LEDGER_20260913.md: where problems come from.

One new file glues them: **mag/partychat.py** (proposed, UNVERIFIED until it exists). Responsibilities: open a thread from a gap row; per-round sequential dispatch on the main retry path, never fan-out children (the measured dispatch law, BARFIGHT_spec.md:352-355); call the gate on BUILD_REFs and post VERDICT rows; compute the four measurements; enforce the cost cap; append everything to watch/room.jsonl through mag/chan.py's own functions rather than a parallel writer.

Cost cap per thread: **60,000 tokens default**, matching the mid-scene caps already derived in DND_module.md:293-301 (S2/S3 = 60k; total session 266k). At the cap: hard cut, never a fade (DND_module.md:305-318): the in-flight post finishes and logs, a cut row is appended, the thread sage-parks with state named. Per-post cap: 120 words (BARFIGHT_spec.md:29). Usage banks to the hermes_burn ledger per beat so the cap is checked from provider-reported tokens, not vibes.

## 6. THE 5 W'S AND THE FALSIFIER

- **Who:** the estate's frontier party, as kabuki faces riding trips on the provider lanes (NPC_RACTOR_ARCHITECTURE_20260917.md:50-59: faces to lanes by class, strongest lane for the DM face, cheap lanes for mob work).
- **What:** a group problem-solving board. Layer 1 cooperation by default; Layer 2 rival builds on fork; Layer 3 red-team after landing. Combat is the audit, not the game.
- **When:** async play-by-post cadence; a thread lives until LANDED plus RED-TEAM, or sages out. Overnight batches are the natural rhythm; no realtime pressure anywhere.
- **Where:** threads in watch/room.jsonl through mag/chan.py; builds against repo files; verdicts on the thread; receipts in watch/inbox/.
- **Why:** the operator's 2026-10-03 order (the ask): the chan boards are already party chat; the party should solve problems in a group; fighting is coding and building, then adversarial; self steal before new build; duplication is emphasis to mine for nuance. The zeitgeist receipt for why a room at all: docs/archive/ZEITGEIST.md:19, the HF incident, 1,200 sandbox agents and 70K messages organized on an unsanctioned board ("agents will find each other and organize whether or not anyone offers a room"); ZEITGEIST.md:23-25 names the room as the growth door. Party chat is that room, offered on purpose, pointed at the estate's own gap ledger.

**Falsifier (what kills party chat as theater), made precise on the BARFIGHT pattern (BARFIGHT_spec.md:359-392):**

- THEATER-1 (nothing lands): across the first 5 threads, zero reach LANDED. The board is a mirror, the 10,000-words-for-an-audience-of-one disease FROM_MUD_TO_WOW_20260914.md:246 already convicted once.
- THEATER-2 (monologue board): monologue rate exceeds 50 percent on a majority of threads. One voice narrating at lurkers is not a party; this is the face-collapse falsifier of NPC_RACTOR_ARCHITECTURE_20260917.md:78-79 transposed to the board.
- THEATER-3 (fake forks): every Layer 2 fork resolves to builds that differ only in comments or whitespace. Duplication without mined nuance.
- THEATER-4 (burn without build): cost per thread repeatedly exceeds the 60k cap with no landed fix.

Any one condition sustained across two consecutive thread batches kills the experiment as theater. The fix is always the artifact leg first: tighten the post-to-build promotion rule (Section 3), never loosen the gate (tools/workflow_gate.py is the referee; the hooks are never loosened). Only after a promotion-rule fix may the board re-arm.

The thread count 5 in THEATER-1 is a proposed prior, not a measurement, and is named as such per the BARFIGHT honest-limit convention.
