# GWAP AS BACKEND — RESEARCH FOR THE WOW CLONE AND THE GAME PLATFORM (2026-09-29)

Operator directive, decoded: "we want to make a wow clone. go through your gaming corpus and research how do we make our gwap as a backend for people making games. kind of like roblox but not child predators. godot is a training engine think of it as our early grok days. we can build things and own them they dont need to be perfacet and then buy use we reveal what we are missing and make an informed choice."

The epistemology clause is the load-bearing one: **build, own, imperfect; use reveals the missing piece; the informed choice comes AFTER use.** His own Hermes story is the UX law: he hated using it because he was intimidated; he needed to go through all the interfaces to know what he liked. Nobody picks-and-goes. The platform must be learnable by touching it.

Three corpus digs were run this session (census, GWAP receipts, systems inventory), all findings path-cited below.

---

## PART 1 — WHAT WE ALREADY OWN (the digs)

### 1.1 A complete WoW-class server core sits in the library

`corpus/library/mod-playerbots` is NOT the AzerothCore module its remote URL advertises — the checkout is **CMaNGOS "mangos-wotlk"**, the full World of Warcraft: WotLK server emulation core: `src/mangosd` (worldserver), `src/realmd` (auth/login), `src/game` (24MB: AI, Arena, BattleGround, AuctionHouse, Loot, LFG, Guilds, Maps), full CMake build, **GPL-2 licensed**. 235MB working tree, ~4,200 files, ~943 .cpp / 788 .h / 1,916 .sql. The `sql/` tree (136MB) carries complete world/characters/realmd schemas with seed data, DBC data as SQL, and map-extraction tooling (`contrib/vmap_extractor`, `vmap_assembler`, `mmap`).

Missing to runnable: (a) the playerbots submodule is an empty gitlink (`.gitmodules` -> celguar/mangosbot-bots — one `git submodule update --init` away), (b) client-derived binary data (maps/vmaps/DBC) must be extracted from an owned 3.3.5 client — tooling included, (c) nobody here has ever built it. Same disease as the Godot port yesterday: **owned-but-never-executed.**

### 1.2 The estate already wrote the ramp

`corpus/game_estate/FROM_MUD_TO_WOW_20260914.md` (53KB, tri-state verified, witnesses annexed): the thesis is Barnes-Hut — "a distant cluster is one thing"; treat WoW as one center of mass standing for twenty years of engineering, approximable long before reproducible. The MUD itself (Mirror Sea) already runs torch-occlusion, a Barnes-Hut quadtree, SUPERHOT time, dragon cascades, an ascension ladder, a learning horde, D&D class enemies, boon drafts. `tests/test_wow_bones.py`, `test_wow_player.py`, `test_wow_world.py`, `test_wow_manifest.py`, `test_wow_family.py`, `test_wow_bones_session.py` — six suites of WoW-shaped character/world architecture already exist estate-side (the UF-117 line). A handoff note in the nacho archaeology even specifies "BUILD: emulator (MaNGOS/TrinityCore lineage) on k8s" as standing intent.

### 1.3 The GWAP design is already on paper

`watch/inbox/noir_gwap_steal_20260926/SUBSTRATE_DECISION_20260926.md`: **agreement-as-anti-cheat** (Robber files sealed intent, Cop files independent incident report, Witness answers templated clues; agreement score = the verified label = the GWAP payload, append-only JSONL `{scene_id, intent_struct, report_struct, agreement_score, blocker_taboo_list, witness_clue_chain, verdict}`), **KissKissBan blocker** (the HCOMP'09 literature-proven fix for match-early collusion: ban the N most common words per scene), **shader-channel doctrine** (rain = drift alert, posters = queue rows, one master uniform = round clock — "the environment is the dashboard"). Staged substrate was DECIDED as Teardown -> FiveM -> UE5 on 9/26 — a time-bound best idea this research reopens (see Part 5).

### 1.4 The grader harness is the actual moat

Frozen-tape replay verification is built and green: mud replay 41/41 + mud fifty 63/63 + toy 15/15 + frontier 51/51 + swarm 32/32 = **202/202** (Q-020_FW01 receipt): fixed 1/60 timestep, seeded RNG, byte-identical replay, sha256 run receipts, one-entry input flip = INPUT_FORK at the exact frame. Plus the MAST judge-lane + CLUSTER_REPORT organ (three-axis verdicts with evidence quotes, failure-class taxonomy, spot-check samplers). **This machinery — deterministic replay + hashed receipts + agreement payloads — is what "GWAP as a backend" actually sells.** Nobody else's game platform verifies play.

### 1.5 The platform vision is the operator's own, from August

`queue/handoff/TOKENOMICS_MYTH_GAME_API_20260810.md`: wallet-as-a-service, a marketplace for headless AI swarms ("cheap AIs answer for pay, right-sized, token-metered"), a **GAME-API PLATFORM** where people build games on the estate engine — "gives NPCs MEANING and HOPE... their worlds, our brain." `docs/PLAN_THE_GAME_VERTICAL_ADOPTION.md`: "once you're a game it goes vertical with adoption"; player signals = training data; play = use. The Jain & Parkes steal (`watch/inbox/play_as_work_20260926/`) supplies the economics law: meters going up is not work — meter credit weighted toward rare, byte-backed, falsifiable artifacts, never match-early volume.

### 1.6 Backend-grade parts already in the house

- `dashboard/mud_relay.py` — working hand-rolled RFC6455 WebSocket presence relay, 8Hz broadcast, in production with `mud.html` lanterns. Admits its own gaps: no authority, no persistence, no rooms, no auth.
- `mag/game_campaign.py` (4,838 lines) — server-authoritative turn resolver, schema `mag_game_campaign.v1`, "engine owns truth; LLM narrates after."
- `mag/water_graph.py` + `water_computer.py` — deterministic integer physics engines with pytest suites and chain-anchored proof folds; the Godot slice runs one of these tonight.
- `memory/game/world/world_state.json` — content-addressed verkle world store (`game_world.v1`), the authority `game_ramp.py` builds on.
- `mag/api_server.py` (FastAPI, key-gated) + `lan_proxy.py` — hardened HTTP plumbing.

Missing for a real backend: authoritative simulation in the relay, persistence, rooms/accounts/matchmaking, sync between the browser world and the mag world (two disconnected truths today), and JS-side graders (`test_swarm.js`/`test_toy.js` named in receipts do not exist repo-wide — the tape machinery lives in `scripts/`, a naming debt, not a capability gap).

---

## PART 2 — THE ARCHITECTURE: THREE LAYERS

**L1 — GAME SHELLS (what players touch).** Godot clients, browser HTML games, any engine later. The shells are disposable and numerous — that is the "backend for people making games" premise: the platform does not own the shell.

**L2 — THE GWAP BACKEND (the product).** Five services, each with an existing seed:
1. **Session server** — mud_relay evolved: server authority, persistence, rooms, accounts. Seed exists (RFC6455 relay + fail-closed relay patterns).
2. **Agreement engine** — the noir payload schema: intent/report/witness with KissKissBan blockers. Turns play into verified labels. Design done; needs an implementation host.
3. **Verification service** — frozen-tape replay + sha256 receipts + MAST judge-lane. Already green at 202/202. **This is the moat: a platform where play is provable.**
4. **Ledger** — append-only payload JSONL folding into the verkle world store/chain. Pattern exists estate-wide.
5. **Credit rails** — honest metering per play-as-work law: meters weighted to rare byte-backed artifacts; visible to players; no match-early volume farming.

**L3 — WORLD CORE (what devs build on).** The deterministic engines as loadable modules (water_graph first — it already runs in two languages), the content pipeline, the world store. "Their worlds, our brain."

Dev experience definition (the Roblox inversion): a developer brings a shell, integrates L2, and gets — players whose play is verified, anti-cheat by agreement rather than kernel drivers, honest meters, and export-everything ownership. The estate's seats can also BE players: the swarm marketplace from the August doc (headless AIs answering for pay) slots into L2 as bot-shaped clients of the same verification service.

---

## PART 3 — THE WOW CLONE AS FORCING PROJECT

A WoW clone is the perfect training engine exactly because it forces every L2 service to exist under load: movement authority, persistence, accounts, anti-cheat, content pipeline. And we start with half of it already owned (CMaNGOS server + world DB).

The build-to-learn ladder (each rung exists to reveal the next missing piece; none needs to be perfect):

- **B0 (DONE tonight):** The Mountain slice — Godot learned; two estate systems as one loop; solvability verified on the original engine.
- **B1 — REVIVE THE SERVER:** `git submodule update --init` (playerbots), build mangosd + realmd from `corpus/library/mod-playerbots`, load the world SQL, extract maps/vmaps/DBC from an owned 3.3.5 client. Deliverable: a running WoW server on estate hardware, and a logged list of everything that was missing. (Legal note: GPL-2 server code stays GPL — fine for sovereign and platform use; client data extraction is standard mod-server practice from an owned client; the client binary itself is never redistributed.)
- **B2 — GODOT SPEAKS WOW:** auth against realmd, then a movement/opcode subset client in Godot. Deliverable: you walk in Azeroth from our engine, next to playerbots. This is the wow-clone bootstrap and the protocol lesson in one.
- **B3 — GWAP PAYLOAD v0:** implement the noir agreement schema on the MUD (it already has multiplayer presence via mud_relay): one scene, one intent/report/witness round, payload lands as append-only JSONL. The backend then EXISTS before the first external developer arrives.
- **B4 — FIRST EXTERNAL DEV:** Adam. The disclosed invariant, which is the Roblox-killer test: the backend must be usable without estate help. Whatever B4 reveals missing IS the platform roadmap.
- **B5 (the informed choice):** only after B1-B4 does the engine/netcode/DB choice get made — with use-data instead of vibes. Godot was never the commitment; it is the training engine, the early-Grok rung.

What use will reveal (the deferred choices, named now so we recognize them): netcode ownership vs. fork-and-keep CMaNGOS's; MySQL vs. own store; whether bots are the product (playerbots + estate seats = AI-populated worlds — nobody sells that); UE5 vs. Godot for the noir endgame; content pipeline shape; and whether the verification service is the actual business.

---

## PART 4 — ROBLOX WITHOUT THE PREDATION (design constraints, not sermon)

1. **Child safety by architecture:** federated small servers (LAN/Tailscale scale, like mud_relay's LAN-first intent) instead of one giant attention-mining estate; no ad-monetization of minors; no engagement-optimization loops aimed at kids; account ownership by guardians.
2. **Creator economics:** splits metered by the receipt ledger — the estate's cost-truth obsession applied to payouts. No scrip squeeze (the Robux/DevEx discount model is the baseline to invert: creators get real value, visible meters, byte-backed accounting).
3. **Ownership:** worlds export in open formats (Godot projects are the dev's; payloads export as JSONL; the verkle store is content-addressed by design). The estate's own Roblox-lock-in trauma is the founding constraint — the platform that cannot trap its devs.
4. **Consent:** players know their play is verification work; the meters are visible; the payload schema is public. Play-as-work with the work named.

---

## PART 5 — STANDING DECISIONS REVISITED (no sacred cows)

The noir GWAP substrate decision (2026-09-26: Teardown -> FiveM -> UE5) was made before the Godot frame existed. This research reopens it without overturning it: the staged logic (cheap imperfect now, sovereign later) is identical — only the first rung changes. Godot + CMaNGOS becomes the phase-0 training engine; FiveM/UE5 remain the noir endgame candidates if use demands them. The B3 agreement payload is substrate-agnostic by design (JSONL schema), so nothing in the noir design is wasted.

## PART 6 — HONEST UNKNOWS

- Nobody has ever built or run the corpus CMaNGOS checkout; the bots module is unpopulated; build toolchain (CMake/mysql/deps) untested on this box.
- CMaNGOS-wotlk is a 2021 snapshot: security and compat debt unknown until B1 compiles it.
- GPL-2: fine sovereign, constrains any future closed-source pivot of server-derived code. Godot (MIT) and Evennia (BSD-3) are clean.
- Roblox critique figures (safety record, DevEx economics) are cited from knowledge, not re-verified today — flagged PLAUSIBLE per the ramp doc's tri-state law.
- The platform has zero external developers today; every "dev experience" claim is a hypothesis until B4.

## Filing

Receipt: watch/inbox/GWAP_BACKEND_RESEARCH_20260929.md (this file), registered in index_events.jsonl. Research digs: three Explore sweeps (corpus census, GWAP receipts, systems inventory), session-local. Em-dash count: 0.
