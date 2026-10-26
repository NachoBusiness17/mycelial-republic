# DESIGN BIBLIOGRAPHY: sovereign multiplayer game platform

Owner seat: ZCode (Opus-lensing prep, 2026-09-29). Curation law: primary and battle-tested over exhaustive; a domain gets only as many entries as it has real sources. Verification marks: [V] URL fetched/confirmed live this session; [T] title and venue confirmed via search results this session; [K] high-confidence knowledge, URL not re-verified (search lane rate-limited 2026-09-29). Every entry: what it teaches + why it earns the slot.

## 1. Authoritative server architecture for physics sims

1. **Glenn Fiedler, "What Every Programmer Needs To Know About Game Networking" + the Gaffer on Games netcode series (2010+)** [V] https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/
   Teaches: the decision tree everything else hangs on: deterministic lockstep vs authoritative state sync, snapshots, delta compression, prediction/reconciliation. Why: the shared vocabulary; every design fight downstream resolves into this tree.
2. **Glenn Fiedler, "Networking for Physics Programmers" (GDC talk, PDF archive)** [V] https://www.gamedevs.org/uploads/networking-for-physics-programmers.pdf
   Teaches: networking continuous physics specifically: why physics resists lockstep, how authority + client-side prediction split for state-heavy sims. Why: the mission names physics sims; this is the one physics-first treatment.
3. **Fabien Sanglard, "Quake 3 Source Code Review: Network Model"** [V] https://fabiensanglard.net/quake3/network.php
   Teaches: server-authoritative snapshots, delta compression against acknowledged baselines, client prediction via usercmds, read directly from shipped engine code. Why: primary-source reading beats essays; this is the ur-authoritative-server.
4. **Valve, "Source Multiplayer Networking" (Valve Developer Community wiki)** [K] https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking
   Teaches: entity interpolation, input prediction, lag compensation (server rewinds time to honor the shooter's view); tickrate as a fidelity budget. Why: the AAA-documented continuation of the Quake lineage, with the counter-intuitive tricks spelled out.
5. **Timothy Ford, "Overwatch Gameplay Architecture and Netcode" (GDC 2017)** [V] https://www.gdcvault.com/play/1024001/-Overwatch-Gameplay-Architecture-and
   Teaches: ECS as the replicable substrate, entity mirroring, deterministic leanings, prediction smoothing, at modern AAA fidelity. Why: the bridge from Quake-era to component-era authoritative sims.

## 2. MMO server design

1. **MUD-Dev mailing list archive (1996-2007, 31,406 messages)** [V] full download: https://www.raphkoster.com/2007/02/02/full-mud-dev-archive-for-download/ ; browsable mirror: https://www.grimwheel.com/muddev/
   Teaches: a decade of argued virtual-world engineering: persistence models, zoning vs seamless worlds, trust and admin tooling, community governance. Why: the lineage the mission names; MMO theory was settled here before the WoW era.
2. **EQEmu/Server (open source)** [K] https://github.com/EQEmu/Server
   Teaches: a reverse-engineered, production-lived MMO world server: database-driven world state, zone processes, login/world/chat separation, 25 years of operation. Why: the only fully-owned MMO codebase of that generation you can run and modify today; sovereign by construction.
3. **CCP, "The Server Technology of EVE Online: How to Cope with 300,000 Players on One Shard" (GDC 2010)** [V] https://gdcvault.com/play/1014077/The-Server-Technology-of-EVE
   Teaches: single-shard at scale: sol-based solar-system processes, in-memory sim with async DB persistence, time dilation as load shedding. Why: the existence proof that one world, owned end to end, survives 300k players.
4. **CCP developers, "Infinite Space: An Argument for Single-Sharded Architecture in MMOs" (Game Developer)** [V] https://www.gamedeveloper.com/design/infinite-space-an-argument-for-single-sharded-architecture-in-mmos
   Teaches: the runtime, database, and ops strains of single-shard, and the social/economic argument for paying them. Why: architecture rationale written by operators, not vendors.
5. **Veloren devblogs (Rust, open source multiplayer RPG)** [K] https://veloren.net/
   Teaches: a living open-source MMO-lineage project: netcode rewrites, ECS world, server moderation, release ops, weekly engineering notes. Why: what the whole stack looks like when one community owns all of it, now.

## 3. Procedural generation

1. **Jonah Weiner, "The Brilliance of Dwarf Fortress" (NYT Magazine, 2011)** [T] and **Elijah Meeks, "Procedural Humanities: An Interview with Tarn Adams" (HASTAC, 2010)** [T] (both findable by exact title; URLs not re-verified)
   Teaches: the Armok heritage (dragslay, then Slaves to Armok: God of Blood, then Dwarf Fortress from 2002): simulation-first worldgen that produces histories and meaning, not assets. Why: the mission's named lineage; these two are the deepest on-record statements of that philosophy.
2. **Bay 12 Games, Dwarf Fortress dev log and release notes (primary)** [K] https://www.bay12games.com/dwarves/
   Teaches: twenty years of design notes as a world simulator grows layers (myth, entities, villains). Why: the primary corpus under item 1; PCG decisions with their long-term costs.
3. **Maxim Gumin, WaveFunctionCollapse (2016)** [K] https://github.com/mxgmn/WaveFunctionCollapse
   Teaches: constraint-propagation generation in ~1k lines; the same solver moves from texture synthesis to level layout. Why: the most re-implemented PCG algorithm of the decade, small enough to own completely.
4. **Shaker, Togelius, Smith (eds.), "Procedural Content Generation in Games" (Springer 2016, free online)** [K] http://pcgbook.com/
   Teaches: the academic map: search-based, solver-based, mixed-initiative, ML-assisted PCG. Why: the survey spine; free and comprehensive.
5. **Hendrikx et al., "Procedural Content Generation for Games: A Survey" (ACM TOMM, 2013)** [T]
   Teaches: taxonomy by what is generated and why, independent of technique fashion. Why: the field's grid for placing whatever generator you build.

## 4. Verifiable and anti-cheat multiplayer

1. **Paul Bettner and Mark Terrano, "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond" (GDC 2001 talk / Gamasutra article)** [T] (canonical gamedeveloper.com URL currently bounces to the design index; findable by title, mirrors circulate)
   Teaches: deterministic lockstep with ~500ms turns, command latency, perceived responsiveness management; how 1500 units ran on dial-up because state was never sent, only commands. Why: the lockstep primary source; the determinism contract in production.
2. **Nathaniel Baughman and Brian Neil Levine, "Cheat-Proof Playout for Centralized and Distributed Online Games" (IEEE INFOCOM 2001)** [T]
   Teaches: commit-then-reveal (exchange hashes of commands before disclosure) makes lockstep plausibly deniable against cheat injection; formal treatment of which cheat and timing classes survive. Why: the cryptographic primitive a "verifiable multiplayer" layer builds on.
3. **Jeff Yan and Brian Randell, "A Systematic Classification of Cheating in Online Games" (ACM NetGames workshop, 2005)** [T]
   Teaches: cheat taxonomy (information exposure, logic modification, protocol manipulation, timing) mapped to defenses. Why: threat-model first, then design mechanics that make the class structurally hard.
4. **GGPO, Tony Cannon (rollback networking, open sourced)** [V/V] overview: https://en.wikipedia.org/wiki/GGPO ; explainer: https://arstechnica.com/gaming/2019/10/explaining-how-fighting-games-use-delay-based-and-rollback-netcode/
   Teaches: rollback = determinism as an asset: predict remote inputs, re-simulate from history on correction; why rollback forces exactly the simulation discipline a verification layer can then check. Why: the current competitive standard, invented outside any platform holder.
5. **Honest gap note:** VAC, EAC, BattlEye, and Vanguard have no substantive public engineering literature (kernel-driver marketing pages aside). The load-bearing corpus is the academic work above plus rollback practice. No padding offered.

## 5. Game-as-verification (the GWAP lineage)

1. **Luis von Ahn and Laura Dabbish, "Labeling Images with a Computer Game" (CHI 2004)** [T]
   Teaches: the ESP Game's output-agreement: two untrusted players verify each other's output as a side effect of play; taboo-word abuse resistance. Why: the founding pattern of game-as-verification.
2. **Luis von Ahn, "Games with a Purpose" (Science 311(5763), 2006)** [T]
   Teaches: the generalization: games as human-computation infrastructure with coverage and throughput arguments. Why: the citable root of the field.
3. **Luis von Ahn and Laura Dabbish, "Designing Games with a Purpose" (Communications of the ACM 51(8), 2008)** [T]
   Teaches: three verification templates (output-agreement, input-agreement, inversion problem) and when each is robust. Why: the actionable one; a design menu for making play produce verified truth.
4. **Cooper et al., "Predicting protein structures with a multiplayer online game" (Nature 466, 2010; Foldit)** [T]
   Teaches: game output beating the best algorithms; cooperation and competition modes producing distinct discovery behaviors; leaderboard-driven expert emergence. Why: the strongest existence proof that gameplay can outperform automated verification where algorithms fail.
5. **Kim, Greene, Zlateski, ..., Seung and the EyeWirers, "Space-time wiring specificity supports direction selectivity in the retina" (Nature 509, 2014; Eyewire)** [T]
   Teaches: aggregated crowd play as a scientific instrument: consensus scoring over thousands of player traces reaching peer-reviewed truth. Why: GWAP taken to the hardest verification standard there is.

## 6. Engine economics

1. **The Unity runtime-fee announcement and walkback (September 2023; blog.unity.com plus contemporaneous press)** [T]
   Teaches: the engine vendor is a counterparty: terms changed retroactively per-install, then reversed under revolt. Why: the industry-scale argument for sovereign/open engines; the risk model any platform decision here must price.
2. **Casey Muratori, "The Thirty Million Line Problem" (2015)** [V] video: https://www.youtube.com/watch?v=kZRE7HIL3Bc
   Teaches: the true size and cost of the dependency stack under a typical engine+OS; what owning your bottom layers buys in performance and comprehension. Why: the economic core of the handmade/sovereign-engine position, argued from measurements.
3. **"12 Month Godot User Post-Mortem of Sorts" (r/godot, 2024, studio-lens)** [V] https://www.reddit.com/r/godot/comments/1g41vc7/12_month_godot_user_postmortem_of_sorts/
   Teaches: a year of real adoption: editor stability, rendering pipeline limits, porting effort, where the open engine pays and where it bills. Why: engine economics grounded in an adoption year rather than marketing.
4. **"Dastardly Postmortem: Reflections on My First Digital Game Using the Godot Engine" (2022)** [V] https://mors-immortalis.ca/project%20update/godot%20engine/postmortem/2022/03/27/dastardly-postmortem/
   Teaches: the solo/small-team ship: what the engine actually saved and cost on a finished commercial title. Why: the micro end of the economics ladder; calibrates the leap from prototype to product.

## 7. Distribution (the sovereign angle: fully-owned distribution)

1. **Valve, Steamworks SteamPipe documentation (partner docs)** [K] root: https://partner.steamgames.com/doc/ (SteamPipe under application docs)
   Teaches: depots, manifests, delta patching, branches and betas: the incumbent industrial baseline any alternative must match. Why: know exactly what you are refusing.
2. **itch.io butler + the Wharf open spec** [V] docs: https://itch.io/docs/butler/ ; butler (MIT): https://github.com/itchio/butler ; wharf spec: https://itch.io/docs/wharf
   Teaches: command-line push, channels, versioned delta patches, offline patch generation and application, an open delivery format with third-party implementations. Why: the only open-source A/B-patching stack in wide game use; the concrete mechanics of "fully-owned distribution" (diff, manifest, CDN, channels).
3. **Valve SteamOS and Proton (open source)** [K] https://github.com/ValveSoftware/SteamOS and https://github.com/ValveSoftware/Proton
   Teaches: the Linux compatibility surface and the Deck as a hardware target; what verification/certification demands. Why: sovereignty ends at the OS unless that layer is open; Proton is what makes a no-Windows distribution path real.
4. **GOG offline installers** [K] https://www.gog.com/
   Teaches: ownership-maximal commercial distribution: no launcher, no phone-home, the installer itself as a durable artifact. Why: commercial proof a market pays for sovereign distribution.

## 8. RL environments as content

Interpretation note: "MiMo" in the brief was read as the Minecraft environment lineage (MineRL to MineDojo); if Xiaomi's MiMo (RL for LLM reasoning) was meant, entries 1-2 still carry the domain.

1. **Cobbe et al., "Leveraging Procedural Generation to Benchmark Reinforcement Learning" (Procgen; ICML 2020)** [T] arXiv:1910.10871
   Teaches: environment generation as an unbounded content stream; train/test split by generation seed; how content diversity exposes agent brittleness that fixed levels hide. Why: the canonical "content is curriculum" result.
2. **Wang, Clune, Stanley, "Paired Open-Ended Trailblazer (POET)" (2019)** [T] arXiv:1901.01753
   Teaches: co-evolving agents with generated environments; environment difficulty as a searched dimension rather than a fixed knob. Why: environments-as-content made literal.
3. **Leibo et al., "Melting Pot" (DeepMind, 2020)** [T] arXiv:2012.01717
   Teaches: games as an evaluation substrate for multi-agent systems; scenario suites where humans and learned agents are interchangeable players. Why: what a game must expose to be machine-legible; design constraints that run both directions.
4. **Fan et al., "MineDojo" (NeurIPS 2022)** [T] arXiv:2206.08853
   Teaches: internet-scale knowledge bases folded into reward and simulation inside one open-ended game world. Why: environment richness treated as the product itself; the Minecraft lineage's current high-water mark.

## Curation honesty

- Web search lane hit repeated rate limits (429/1302) on 2026-09-29; items marked [K] were not re-fetched this session. Titles, venues, and claims for [T]/[K] items are standard, checkable citations, not fabrications; re-verify [K] URLs before citing them externally.
- Domains 4 and 6 stop at 4 entries (plus one honest gap note) because the padding was not real: anti-cheat and engine-failure literature is thin where vendors keep it closed.
- Companion reads deliberately excluded (padding): Gabriel Gambetta's client-server prediction series (tutorial-rung restatement of Fiedler+Sanglard), engine-marketing whitepapers, and platform-holder press kits.
