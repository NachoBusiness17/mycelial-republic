# THE ROUTE v0: the climb from where we stand to the summit (MC5)

Date: 2026-09-30 · Owner seat: ZCode (MC5, mountain climb) · File: `watch/inbox/mountain_climb/ROUTE_V0.md` · No commit (per plan).
Inputs read whole before drafting: `SHERPA_DOSSIER.md`, `GOALS_DOSSIER.md`, `GAP_ANALYSIS.md`, `BIBLIOGRAPHY.md` (all in this directory), `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md`. Byte-checks done this session: the-mountain repo HEAD `7d5dbe2` (past the `cf2ec7d` the gap analysis cited), `server/auth.py` HONEST SCOPE header ("v1 owes exactly that"), `game/network/` empty (0 entries), CI self-declared no-engine, estate `tests/test_realmd_client.py` present (17 test functions). Em-dash count: 0 (house law).

**For the fleet's adversarial read and then Opus: this route is written to be attacked.** Every pitch names its ATTACK SURFACE: the assumption most worth trying to break. Phase 1 (plan) exists to break these; Phase 2 prices what survives.

---

## 0. Reading laws

- A **pitch** = a bounded stretch with a belay point: it lands, it is verified, the rope is safe there, the next pitch starts from it. No pitch depends on an unfinished pitch.
- **ESTIMATE units are lane-days** (one lane, one focused window of work at the measured shapes) plus lanes. They are effort, not dates: "dates are meaningless, just go" (operator, 2026-09-19, `memory/scrum/backlog.json:299`; goals dossier non-goal 6). No calendar promise is made or implied anywhere below.
- Measured shapes used (sherpa dossier organ 8): Task lanes clean at width 3/6/10/12 (109.4M tok/h at width 10); sustained shape 8-12 staggered per the climb plan's own Gates; workflow children at most 50 concurrent; mates 12-16 simultaneous cap; free lanes are sensing only; only Nous/Hermes is funded.
- Verification law: every VERIFICATION clause is a falsifier a stranger could check from bytes, not a feeling (compass §8: no "shipped" claim without gate artifact).

---

## 1. The route thesis

The gap analysis's brutal one-liner is the anchor: **everything exists and passes its own tests, and nothing has met a stranger. The missing mile is SRP6 port + one real build + one external player (Adam).** Distribution (row 6) is the narrowest critical path because a player-gettable artifact converts every other row from working to load-bearing.

So the route is a last-mile route, not a foundation route. The estate does not need new organs; it needs three proofs that touch reality (auth that never sees the password, an artifact a clean machine can run, a session authored by someone outside the estate), then the ladder the goals dossier already owns: B1 (server, mostly done) → B2 (client speaks the protocol) → B3 (GWAP payload live) → B4 (first external dev) → B5 (informed choices). Eight pitches: P2, P3, and P6 ARE the missing mile; the rest either mend the carrier, deepen the world, or close the ladder.

The summit this serves (goals dossier §1-2): a sovereign estate where the operator's own game runs on his own backend, the platform's product is verification, and losing any vendor or seat is recoverable.

---

## 2. THE PITCHES

### P1. BASECAMP REPAIR: mend the carrier's broken leg

- **WHAT:** Fix the mates' execution layer. The dispatch machinery is PROVEN (scheduled task, `tools/leave_dispatcher.py`, atomic claims, STEER injection) but the first 08:00 fire failed honestly: all 8 mates exited 1 in ~65s on mate-model auth ("Authentication parameter not received in Header", opencode → glm-5v-turbo; `logs/mates/runs/run_20260930_01_cartographer.log`). Fix the auth path, get one full green fire.
- **WHY NOW:** The sherpa dossier names this fix "owed next window"; it is the estate's reproductive system (mission packs, JOURNEY receipts, oral-law rotation). It serves every later pitch by multiplying lanes at zero paid cost. It is deliberately NOT on the critical path: Phase 1's adversarial read rides Task agents, which are proven, so this pitch never blocks the spine.
- **HOW:** Debug the opencode auth header path against the free lane; one hardening cycle of the leave dispatcher if the header fix reveals a second layer (the register note survived three hardenings; the static-runner indirection was the fourth and it worked). No bibliography entry: this is estate-internal surgery.
- **VERIFICATION (falsifier):** the next scheduled 08:00 fire produces at least 1 of 8 mate runs exiting 0 with a JOURNEY section in its run log (`logs/mates/runs/`), and the auth cause is named in a one-line fix receipt.
- **ESTIMATE:** 1 lane, at most 1 lane-day. Free-lane work.
- **ATTACK SURFACE:** is mate repair actually load-bearing for THIS climb, or sentimental deck-work? If Phase 1 and the pitches never consume a mate output, this pitch should be cut without guilt.

### P2. SRP6 PORT: the missing mile, part one (B1 close-out)

- **WHAT:** Port the estate's PROVEN SRP6 client (`tests/test_realmd_client.py`, 17 tests, proven against mangos realmd) into a server-side v1 auth in the-mountain `server/auth.py`, whose own header says "v1 owes exactly that": server never sees the password, client and server derive a shared proof, the session key falls out of the exchange. Delete the plaintext `hello` path.
- **WHY NOW:** Missing mile part one, and the smallest well-defined unit on the route. Every later pitch inherits identity from it: wire sessions (P4), agreement events (P5), and Adam's account (P6). Porting is cheapest while the protocol surface is small (the hello → welcome → sid shape already exists and is tested). Goals served: verification (L2 session server), sovereignty (our own realm, our own proof, GPL-2 CMaNGOS lineage per the named 09-29 override).
- **HOW:** Steal from ourselves: the estate realmd client plus mangos realmd protocol knowledge; keep the existing protocol table shape; add property tests asserting the password never crosses the wire (grep the wire log) and that exchange replay fails. Bibliography: EQEmu (bib §2.2) for login/world separation patterns; MUD-Dev archive (bib §2.1) for account-model arguments.
- **VERIFICATION (falsifier):** a scripted stranger client (fresh venv, zero estate imports) completes the SRP6 exchange against the-mountain server and is rejected on a wrong password; `grep -ri "plaintext" server/auth.py` finds only the honest-history docstring; the full estate + mountain test suites pass.
- **ESTIMATE:** 1-2 lanes, 1-2 lane-days. The protocol is proven; this is a port, not research.
- **ATTACK SURFACE:** is SRP6 the right rung for a LAN training engine at all, versus boring TLS + salted hash? Counter-position held: TLS still ships the password to our server and rents a certificate authority; SRP6 is the realmd lesson and the moat story. Attack it.

### P3. THE BUILD RAIL: the missing mile, part two (distribution v0)

- **WHAT:** Make the artifact a stranger can run. Extend the honest no-engine CI into an engine-present rail: CI runs the server test suite on every push (red blocks merge, ratchet-shaped), plus a headless Godot export producing a versioned artifact (zip with exported project), pushed to a channel with delta-patch mechanics. First artifact is offline-capable (the dual-mode client already works offline); the online leg arrives with P4.
- **WHY NOW:** Gap row 6 is THE gap and the narrowest critical path: "a player today must install Godot and clone." It converts rows 1, 3, 4, 7, 8 from working to load-bearing, and P6 (the stranger) has nothing to touch until it exists. It has zero dependency on P2/P4, so it climbs in parallel from day one. Goals served: platform (a backend people make games on needs a door) and continuity (portability proven, not claimed).
- **HOW:** Bibliography §7 is the teacher: itch butler + the Wharf open spec (bib §7.2) for channels, manifests, versioned delta patches, third-party implementations (the only open A/B-patching stack in wide game use); GOG offline installers (§7.4) as the ownership-maximal shape (the installer itself a durable artifact); SteamPipe (§7.1) as "know exactly what you are refusing." Dual-use move: the clean-machine falsifier run doubles as the PREPAREDNESS_AUDIT actions 3-5 second-machine join (off-machine pack key, Drive-sync verify, ONE real join: "until one does, portable is a claim, not a proof"), one receipt proving two claims.
- **VERIFICATION (falsifier):** on a machine that never had Godot or either repo: download one artifact from the channel, run it, reach the water board, play one move, exit; and CI shows a run where the server tests executed and the export step produced a hash-named artifact. Both receipts filed.
- **ESTIMATE:** 2-3 lanes, 3-5 lane-days. The export-template toolchain is the honest unknown; that is why this starts day one, not last.
- **ATTACK SURFACE:** does a build without the online leg teach anything real, or hand the stranger a dead toy? Position held: the RAIL is the deliverable of this pitch (depot, channel, delta, CI gate); the artifact's fun is P4+P6's business. Attack the ordering.

### P4. THE WIRE (B2): the client speaks the protocol

- **WHAT:** Fill the empty `game/network/` directory with a real client transport speaking the server's existing protocol (`server/ws_door.py`, protocol table, verdict feed already exist server-side). Decision made upfront, from the bibliography: authoritative state sync with client-side prediction, NOT deterministic lockstep, because the water sim is continuous state-heavy physics; keep the proven dual-mode (online/offline) shape.
- **WHY NOW:** B2 is the ladder rung between the built server and the live backend; the stranger's session is meaningless online without it; P5's unscripted human round rides it. It is the route's deepest technical unknown, so it starts as early as parallelism allows (after P2's handshake contract stabilizes) and carries slack.
- **HOW:** Bibliography §1 in full: Fiedler's decision tree (lockstep vs state sync; the fight this settles), Fiedler "Networking for Physics Programmers" (why physics resists lockstep; authority + prediction split), Quake 3 source review (snapshots, delta compression against acknowledged baselines, read from shipped code), Valve wiki (entity interpolation, lag compensation, tickrate as fidelity budget), Overwatch GDC (ECS as replicable substrate). GGPO/rollback (bib §4.4) noted as the future discipline determinism buys for the verification layer, not this pitch.
- **VERIFICATION (falsifier):** two clients on two different physical machines (not two windows) see the same world; an injected divergence reconciles to server truth within a bounded tick count; the session's hash-chained action log passes `verify_tail`; a replay receipt reproduces the session byte-identically from the frozen tape (the 202/202 machinery pointed at a real network session for the first time).
- **ESTIMATE:** 2-3 lanes, 4-6 lane-days. Deepest unknown on the route; if anything overruns, it is this.
- **ATTACK SURFACE:** the per-tick state size of the water board is ASSUMED small enough for snapshot+delta at LAN tickrates, without measurement. The attack: measure first (one instrumented session), because if state is huge, baseline-delta assumptions (Quake 3) may not save us without interest management.

### P5. GWAP LIVE (B3): one real agreement round, append-only

- **WHAT:** Land one live intent/report/witness round on the MUD as append-only JSONL: Robber intent, Cop report, Witness clues, KissKissBan blockers (per `noir_gwap_steal_20260926/SUBSTRATE_DECISION`). Wire the built-but-trafficless gwap→gps bridge (`mag/gwap_to_gps.py`, 15 tests, zero live traffic; TIE_IT_ALL §3 thin spot 1) so the GPS ledger takes its first production routing rows.
- **WHY NOW:** Goals dossier 3.3: "the backend then EXISTS before the first external developer arrives." B3 must land before P6 so the stranger's play produces verification value on day one, which is the platform's entire product claim ("nobody else's game platform verifies play"). Payload wiring can start mid-P4 using server-side sessions (innkeeper bot, scripted clients); the unscripted-human falsifier gates on P4.
- **HOW:** Bibliography §5: von Ahn and Dabbish's three templates (output-agreement, input-agreement, inversion; the design menu, CACM 2008) to pick the round's verification template deliberately; Foldit and Eyewire as existence proofs of play-as-instrument. Bibliography §4: Baughman and Levine commit-then-reveal for cheat-resistant exchange; Yan and Randell taxonomy, threat model first. Play-as-work meter law (Jain & Parkes steal): credit the rare byte-backed artifact, never match-early volume.
- **VERIFICATION (falsifier):** at least one agreement event in the JSONL whose participants include a session the seat did not script move-by-move (operator through the client, or two humans), the tail verifies through the existing chain code, and the GPS ledger logs a live routing decision sourced from that event (test_double stays honestly flagged until a live key exists; rows name which).
- **ESTIMATE:** 1-2 lanes, 2-3 lane-days (engine, adapter, and tests exist; this is welding, not building).
- **ATTACK SURFACE:** is ONE round "the backend exists," or theater? The route defines the minimum viable agreement payload BEFORE building; the adversarial read should try to shrink it further. Also attack the GPS live-flip: at 1 event/day, live routing may be premature theater for the meters.

### P6. THE STRANGER (B4): first external dev (Adam)

- **WHAT:** Adam (or whoever the fallback stranger is) gets the artifact plus a one-file quickstart, runs it, plays, breaks things. The seat does NOT drive his session: "the backend must be usable without estate help. Whatever B4 reveals missing IS the platform roadmap" (goals dossier 3.1). ADAM_QUICKSTART is rewritten from what actually broke, not what we guessed.
- **WHY NOW:** Missing mile part three; the row-5 truth is "onboarding PENDING, not done" and zero external developers today. This converts P2-P5 from estate theater to load-bearing. It is the only pitch whose gate is a human calendar, so the route arms a fallback: if no Adam bytes within 72 hours of artifact-ready, publish the channel link to one external surface and count an anonymous first-run. A stranger is a stranger.
- **HOW:** Almost no code; it is discipline. Hand over, then be quiet; collect the missing list as receipts. Bibliography: MUD-Dev archive (bib §2.1) for onboarding/trust/admin-tooling arguments from a decade of operators; Veloren (bib §2.5) for how an owned community onboards contributors now.
- **VERIFICATION (falsifier):** receipt of external bytes the estate did not author: a say line, a move, an agreement event, or a commit/issue from a non-estate identity in the repo or session logs; plus the B4 missing-list filed in the inbox with index rows.
- **ESTIMATE:** 1 support lane, 1-2 lane-days of prep; the wait is human and unbounded (fallback clock: 72h after P3+P4 artifact-ready).
- **ATTACK SURFACE:** Adam is a friend, not a market. N=1 proves onboarding works once; it does not prove demand or usability at any width. Route position held: B4 is an existence proof, explicitly not a demand curve; anyone reading B4 evidence as market signal is wrong.

### P7. THE SECOND BOARD: content pipeline becomes real

- **WHAT:** Weld the tested worldgen toys (`mag/worldgen.py`, `mag/river.py`) into the server+client loop: boards #2..N generated rather than hand-built; same seed yields the same world, receipted by hash; WaveFunctionCollapse used where constraint layout pays.
- **WHY NOW (and not sooner):** Gap row 7 is a toy precisely because worldgen has never fed the loop. It is deliberately ordered AFTER the stranger: content built before B4's missing-list risks polishing what nobody asked for (the attack line below exists because this ordering is a judgment call, not a dependency). It gives the stranger's day-two a reason to return and opens the RL-content door later without committing to it.
- **HOW:** Bibliography §3: Dwarf Fortress philosophy (simulation-first worldgen that produces histories and meaning, not assets; Bay 12 primary corpus), WaveFunctionCollapse (constraint propagation owned completely in ~1k lines), Procgen (seed-split content streams; content as curriculum) and POET (difficulty as a searched dimension) as the later RL door.
- **VERIFICATION (falsifier):** two generated boards live in one server process simultaneously; identical seed on two machines produces byte-identical board JSON (hash receipt); the hand-built N46W122 board remains as a regression fixture.
- **ESTIMATE:** 1-2 lanes, 2-4 lane-days. Can START mid-P4 (needs only the world schema), lands after P6 by discipline.
- **ATTACK SURFACE:** if B4's missing-list screams content (e.g., Adam bounced because one board is boring), this pitch was ordered too late; if it screams auth/onboarding friction, this pitch is early. The ordering is falsifiable by the missing-list itself.

### P8. THE INFORMED CHOICE (B5): decide with receipts, then the paid lens

- **WHAT:** The deliberate-ask that closes the route: engine, netcode stack, and persistence DB chosen from evidence (B1-B4 logs, GPS pass-rates, duel verdicts, cost rollup) instead of vibes. "We can build things and own them they dont need to be perfacet and then buy use we reveal what we are missing and make an informed choice" (operator, 09-29 verbatim). This pitch is also where Phase 2 (the Opus lensing, operator GO, $5 cap, AA1 gate) lands as input.
- **WHY NOW:** Every earlier pitch deliberately avoided final picks (non-goal 5: no pick-and-go; choices deferred to B5 BY DESIGN). Only after the stranger has revealed the missing-list does an informed choice exist to make. Goals served: the platform becomes a choice with a receipt; sovereignty (an owned choice is the only sovereign choice).
- **HOW:** Bibliography §6 prices the counterparty risk: the Unity runtime-fee walkback (the engine vendor is a counterparty; terms changed retroactively per-install, then reversed under revolt), Muratori's Thirty Million Line Problem (what owning your bottom layers buys, argued from measurements), the Godot 12-month studio post-mortem and the Dastardly solo-ship post-mortem (where the open engine pays and where it bills). Bibliography §2 (EVE single-shard operations, EQEmu's 25-year database-driven world) prices the persistence options. The ask rides the frozen-RIB deliberate-ask shape (system + bootloader + manifest + verkle tip, small ask, output contract, quantize target; AGENTS.md).
- **VERIFICATION (falsifier):** one decision receipt per choice naming: the evidence rows used, the rejected alternative and why, the counterparty risk priced, and the falsifier that would flip the decision. Reversible picks with named flip-conditions, not ships-burned.
- **ESTIMATE:** 1 lane, 1-2 lane-days of packaging; the paid ask itself is Phase 2 and fires only on operator GO.
- **ATTACK SURFACE:** B5 at N=1 stranger may be premature; counter held: outputs are reversible picks with flip-falsifiers, and deferring ALL picks again is its own failure mode (the perfectionism non-goal cuts both ways).

---

## 3. SERIALIZATION: what climbs in parallel, what cannot

**The strictly serial spine (each pitch consumes its predecessor's output):**

P2 (SRP6 handshake contract) → P4 (wire integrates the real handshake from day one) → P5-falsifier (unscripted human round needs the wire; P5 WIRING can start mid-P4 on server-side sessions) → P6 (stranger needs artifact + wire + agreement round) → P8 (informed choice needs the stranger's missing-list).

**What climbs in parallel (the sherpa's width, from day one):**

- P1 (basecamp repair): free lane, never blocks anything.
- P3 (build rail): parallel from day one; its first offline artifact deliberately precedes P4; the rail is the deliverable.
- P7 (second board): can start mid-P4 (needs the world schema, not Adam); LANDS after P6 by discipline, not dependency.
- P5 wiring: mid-P4, on innkeeper/scripted sessions.
- Standing metabolism (never a pitch, always climbing): stealth driver sensing, improve cycle, cost rollup, anomaly flagger, verkle chain, census patrol.

**Concrete windows at the measured shape (8-12 staggered lanes, never 19-at-once; mates at most 12-16):**

| Window | Spine | Parallel |
|---|---|---|
| 1 | P2 SRP6 | P1 repair + P3 rail start |
| 2 | P4 wire (deep) | P3 rail tail (clean-machine receipt) + P1 green fire |
| 3 | P4 tail + P5 wiring | P7 start (worldgen weld) |
| 4 | P5 falsifier round | P6 prep (quickstart rewrite) + P7 |
| 5 | P6 the stranger (human wait; 72h fallback clock) | P7 land |
| 6 | P8 packaging → Phase 2 ask (operator GO) | meters fold evidence |

**Total effort:** roughly 12-16 serial lane-days on the spine plus 8-10 parallel lane-days beside it; 4-6 focused windows at width 8-10. Effort, not calendar.

---

## 4. RISK LEDGER: top 5 ways the route fails, each with its early-warning signal

1. **TECHNICAL: the wire (P4) breaks on water.** Continuous state-heavy physics resists lockstep (Fiedler, bib §1.2); snapshot+delta is assumed sufficient without measurement. EARLY WARNING: the first instrumented two-machine session shows reconciliation storms, divergence receipts per bounded-tick breach, or a per-tick state size that dwarfs the tick budget. RESPONSE: measure before building the transport; fall back to interest management and baseline deltas (Quake 3/Valve lineage).
2. **ATTENTION: pitch sprawl and the 19-at-once reflex.** Eight pitches invite firing everything; the estate's measured failure mode is burst deaths (1302s at 19-20 simultaneous; AGENTS.md fan-out law). EARLY WARNING: simultaneous lane burst above 12, mates above 16, stealth-driver heartbeat gaps, or census drift left unparsed for a day. RESPONSE: 8-12 staggered is law; a 429/1302 is a HOLD signal, never a width cut.
3. **QUOTA-ECONOMICS: paid rungs go dry.** Only Nous/Hermes is funded ($180); Anthropic keys are unfunded; the Phase 2 Opus ask ($5 cap) depends on a credited pool that has read 402-dry (AJ9 diagnosis); free lanes are sensing-only and their outputs are findings, never done work. EARLY WARNING: cost-rollup trailing trend rises while inbox landings and verkle knots stay flat (paying without landing); duel rows grow with no decision changed by them. RESPONSE: every pitch above is local/free-lane by design; the funded tier is reserved for verification and the P8 ask; the ask waits for credits, it does not force keys.
4. **THIRD-PARTY DEPENDENCE: humans, pools, and toolchains we do not own.** Adam's calendar gates B4→B5; the Nous pool can go dry mid-route; Godot export-template churn can break the rail. EARLY WARNING: artifact-ready for more than 72h with zero external bytes; pool 402 on preflight; a CI export step that breaks on a template version bump. RESPONSE: the anonymous-stranger fallback (P6) keeps B4 moving without Adam; pinned export-template versions in the rail; AA1 keeps the paid ask parked until credits exist.
5. **OPERATOR-BURNOUT: the fear moment was the proof of load-bearing, and overload shows as silence.** The 09-27 "take you away from me" moment marks the operator at maximum emotional stake (goals dossier 3.5); the modal operator message is a neutral dispatch, so distress will not announce itself. EARLY WARNING: no operator GO or STEER words for 48h+, the daily digest unanswered, the decisions-owed queue (D-owes) growing while pitches stall at human gates. RESPONSE: the belay-point design is the mitigation: every pitch lands independently and nothing mid-pitch is load-bearing, so any window can stop at a safe stance; one digest per day, zero calendar pressure, GO words never manufactured by the seat.

---

## 5. WHAT THIS ROUTE DELIBERATELY DEFERS (mapped to the non-goals)

1. Token/scrip economics, wallet, marketplace, MYTH: deferred until B4 reveals demand (D1/D7 defaults; non-goal 3).
2. 3D, content volume, graphics polish: "we do not compete on graphics/content volume; we compete on VERIFIABLE PLAY" (blueprint law).
3. Final engine/netcode/DB picks before B5: the training-engine clause; use precedes choice (non-goal 5).
4. Server scale story: multi-room, TLS-everywhere, a real DB: server v1 owes exactly SRP6 (its own header); scale is chosen at B5 with evidence.
5. Predation economics of any kind: no engagement loops aimed at kids, no scrip squeeze (non-goal 2); stranger telemetry, if ever added, must be consent-visible.
6. JetBrains seat and phone-body agent embodiment: sherpa DORMANT/PLAN items, not organs; they do not climb this route.
7. The v3-blockers list: L-conductor train, resonance, mobile voice, GSTD implement, XRPL tools, riddle packs (direction artifact §5.2); GSTD/Vast/XRPL stay optional scored seats.
8. Perfection-before-use anywhere: "they dont need to be perfacet" (operator, 09-29).
9. Anti-state framing: the danger is to the dependency settlement, not states; stay on the demonstration side of the taking-knowledge line (non-goal 7).
10. Auto-irreversible effects and unilateral paid asks: the human seal and the AA1 gate stay on every rung (non-goal 8).
11. The M4 LoRA replication arm (AI5 spec): a different expedition sharing the range, not this route; the M4 appears here only as the optional clean-machine receipt machine for P3.

---

## 6. THE SINGLE NEXT CONCRETE ACTION

Register this file in the inbox index, then fire Phase 1 today: three adversarial Task lanes (width at most 10, staggered) attacking the route's three load-bearing assumptions, namely (a) state-sync-not-lockstep for the water sim (P4), (b) build-rail-before-wire ordering (P3 before P4), and (c) Adam-as-B4-gate with the 72h anonymous fallback (P6). Each lane files its attack as an amendment receipt in `watch/inbox/mountain_climb/`; the surviving amendments fold into ROUTE_V1.md, which is what the MC6 Opus brief packs.

---

## 7. Source ledger (load-bearing claims, one line each)

| Claim | Path |
|---|---|
| Missing mile = SRP6 port + one build + one stranger; distribution narrowest critical path | `watch/inbox/mountain_climb/GAP_ANALYSIS.md` rows 3, 5, 6 + brutal one-liner |
| auth.py v0 plaintext, "v1 owes exactly that" (byte-verified this session) | `the-mountain/server/auth.py` HONEST SCOPE header |
| `game/network/` empty (byte-verified this session); client dual-mode works | GAP_ANALYSIS row 2; commit dca3801f |
| Estate SRP6 proven vs mangos realmd, 17 tests (byte-verified this session) | `tests/test_realmd_client.py` |
| CI is honestly no-engine (byte-verified this session) | `the-mountain/.github/workflows/ci.yml` |
| B0-B5 ladder, B4 invariant "usable without estate help", B5 informed choice | `docs/ref/GAME_PLATFORM_BASECAMP.md`; `watch/inbox/GWAP_BACKEND_RESEARCH_20260929.md` |
| Mates first fire red at auth; fix owed next window | `watch/inbox/mountain_climb/SHERPA_DOSSIER.md` §2 |
| GPS ledger live-traffic thin spot; gwap→gps bridge built, unwired in production | SHERPA_DOSSIER §6; `watch/inbox/TIE_IT_ALL_20260930.md` §3 |
| Width/mate/economics laws (8-12 staggered, 12-16 mates, 429=HOLD, Nous-only funded, $5 Opus cap, AA1 gate) | AGENTS.md; `memory/rib/RIB_DRIVING_LADDER_20260928.md`; `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md` |
| PREPAREDNESS actions 3-5 (second-machine join; "portable is a claim, not a proof") | `watch/inbox/PREPAREDNESS_AUDIT_20260927.md` |
| Operator canon (wow clone order, training-engine clause, dates meaningless, verifiable play, fear moment) | GOALS_DOSSIER §1, §3, §5 source ledger |
| Bibliography teachings cited per pitch | `watch/inbox/mountain_climb/BIBLIOGRAPHY.md` §1-§7 |
| Agreement engine substrate (intent/report/witness, KissKissBan) | `watch/inbox/noir_gwap_steal_20260926/SUBSTRATE_DECISION_20260926.md` |

**Filing:** this file is the receipt; register in `watch/inbox/index_events.jsonl` (sibling shape, MC5). Owner: this seat, per THE_MOUNTAIN_CLIMB_PLAN MC5. No commit. Em-dash count: 0.
