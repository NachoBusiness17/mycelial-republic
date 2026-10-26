# ROUTE_COUNTER: touch reality first (Phase 1 free lens #3)

Date: 2026-09-30 · Owner seat: ZCode (free lens #3, the adversarial read of ROUTE_V0) · File: `watch/inbox/mountain_climb/ROUTE_COUNTER.md` · No commit (per plan).

Inputs read whole before drafting: `ROUTE_V0.md`, `GOALS_DOSSIER.md`, `GAP_ANALYSIS.md`, `BIBLIOGRAPHY.md` (all this directory), `PLAYER_ONE.md` (landed this session by a sibling lane), `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md`. Byte-checks done this session: the-mountain repo HEAD `7d5dbe2`; `game/network/` has 0 entries AND `game/scripts/net_client.gd` exists (the wire v0, quoted below); `server/auth.py` HONEST SCOPE header; `server/server.py` `--host` default 127.0.0.1 (line 480, flag present); `scripts/build_game.ps1` does not exist (PLAYER_ONE §2 says so in plain text). Em-dash count: 0 (house law).

**What this file is:** the counter-route the Phase 2 ask explicitly demands ("the counter-route: what would YOU climb first and why", plan Phase 2). It rides into the Opus brief BESIDE the route, not behind it: the frontier lens sees the disagreement, not just our consensus. It attacks the route where attack is honest and names the three places the route won (§5).

---

## 0. Reading law

The route is well built. This counter does not claim its pitches are wrong; it claims the SEQUENCE buys information last. The route's own thesis names the disease ("nothing has met a stranger") and then prescribes four windows of estate-priced engineering before the stranger can arrive (ROUTE_V0 §3: the stranger sits in window 5). The counter's position: reality is touchable today; every lane-day of building before touching it is a lane-day priced by the same instrument that has never been corrected by an outsider.

## 1. Counter thesis

Two of the three "missing mile" legs already exist at sufficient strength for first contact, and the route prices both as bigger than the bytes show:

1. **The wire exists.** The route prices P4 as the deepest unknown ("fill the empty `game/network/` directory", 2-3 lanes, 4-6 lane-days). Byte truth: the client transport already lives at `game/scripts/net_client.gd`, landed in W3 (commit dca3801f). Its own header: "NetClient - the Godot half of the estate's world-server wire v0 (server/protocol.py: line-delimited JSON over TCP; ops out: hello/action, ops in: welcome/tick/ack/reject)... Owns no world state and predicts nothing; game.gd's mirror graph stays render-only and every mutation authority stays server-side." Plus the `MOUNTAIN_SERVER` env retarget "so a packed client can be retargeted without a rebuild." What is MISSING is prediction, reconciliation, and delta compression: the machinery a continuous twitch-paced sim needs. The Mountain is not that sim. It is whole units, no decimals, no randomness, human-paced puzzle moves (PLAYER_ONE §1, §4). For a deterministic turn-paced water puzzle, a no-prediction server-authoritative mirror over TCP is not a stopgap; it is the correct netcode rung, and it is already built. The route imported a twitch-physics bibliography (Fiedler decision tree, Quake 3 snapshots, Overwatch ECS, Valve interpolation; bib §1) for a game whose fidelity budget spends almost nothing. The gap analysis's row 2 ("the client's netcode layer does not exist yet") is byte-true of the DIRECTORY and byte-false of the client.
2. **The player door for stranger #1 exists.** The route prices P3 as 3-5 lane-days of rail (channel, manifests, delta patches, CI export gate) before a stranger can touch anything. Byte truth: PLAYER_ONE.md documents the clone-and-F5 door end to end: five minutes, clean machine, no account, no installer, sovereign mode is "the default and the complete game." True, it is a DEV door, not a player door. But B4's gate is a DEV (Adam) by the route's own definition, and the route's P3 falsifier (a clean machine downloads an artifact from a channel) prices a player-shaped door for a dev-shaped gate. The rail is for strangers at WIDTH; stranger number one has an open door today.
3. **Auth at v0 is honestly scoped and sufficient for a friend.** `server/auth.py` HONEST SCOPE: "The password crosses the wire in PLAINTEXT inside hello... Until then this server binds to 127.0.0.1 and that is the whole security model," and `server/server.py` ships `--host`. For ONE bounded session with ONE named friend through a tunnel, plaintext v0 is the operator's own law applied honestly: "we can build things and own them they dont need to be perfacet" (09-29 order, GOALS_DOSSIER §1). SRP6 is identity for strangers at width, not for Adam's Tuesday. The route's own P2 attack surface half-agrees ("is SRP6 the right rung for a LAN training engine at all") and then swallows the doubt.

So the sharp claim: **first contact is possible TODAY on bytes that exist, and the route queues it behind roughly 7-11 serial lane-days of spine (P2 + P4 + P5 by the route's own estimates) plus the parallel rail.**

## 2. Attack one: the faster path to THE STRANGER (route §6 assumption c, attacked from the arrival side)

The route treats the stranger as the summit reward. The counter treats the stranger as the basecamp INSTRUMENT. Three arguments:

- **Adam's attention is the only perishable resource on the route.** P6 admits it: "the only pitch whose gate is a human calendar." Goals dossier 3.2 wants "a playable beta the operator and Adam actually walk." Willingness is a decaying asset; queueing contact behind 7-11 lane-days of spine risks arriving after it cools. The route's own mitigation (72h anonymous fallback) replaces a warm stranger with a cold one.
- **Attribution.** A B4 that fires only after P2+P3+P4+P5 have landed produces ONE missing-list that conflates four frictions: onboarding, auth, netcode, and build. A stranger contacted now on the minimal surface (clone+F5, sovereign mode, PLAYER_ONE) prices onboarding friction ALONE, while it is still separable. Then each later pitch can carry its own contact gate: SRP6 lands, Adam touches it; the wire grows, Adam touches it. Contact early, contact often beats contact once, contact perfectly.
- **The netcode unknown is mis-sized, so the longest tail is shorter than priced.** Route risk 1 fears "the wire breaks on water." But the water board is discrete and deterministic; the client owns no state; the server cannot diverge from itself. The state-size measurement the route wants (P4 attack surface) is worth one instrumented session, not a 4-6 lane-day transport build before any stranger exists. P4's real scope after first contact may shrink to "lag polish," and the missing-list will say so.

## 3. Attack two: GWAP-live before strangers is theater by construction (and it poisons the instrument)

Von Ahn and Dabbish's three templates (output-agreement, input-agreement, inversion; bib §5.3) all REQUIRE at least two parties whose agreement is informative BECAUSE they are independent and untrusted. With zero strangers, P5's falsifier accepts "operator through the client" as the unscripted participant (ROUTE_V0 P5). The operator IS the estate; the innkeeper bot is estate code. An agreement round between the estate and itself has zero verification content, and wiring the gwap-to-gps bridge to take "its first production routing rows" from such rounds manufactures live-traffic credentials from self-play. Two laws break in spirit:

- The estate's own meter law: credit the rare byte-backed artifact, never match-early volume (GOALS_DOSSIER §3.3, play_as_work steal).
- Trust bytes, not reports: after a self-play flip, the GPS ledger permanently contains rows nobody can later prove were real. The instrument is blurred on day one of its life.

The route's own P5 attack surface names this ("at 1 event/day, live routing may be premature theater for the meters") and then proceeds anyway. Counter position, and it is a SPLIT, not a cut: the payload must be ARMED before any stranger session (schema and adapter are built and tested; a stranger's play must never land un-instrumented, because stranger sessions are non-renewable evidence: you cannot replay the signal you failed to record). But the LIVE flip of production GPS routing rows gates on the first agreement event with at least one non-estate participant. Self-play rounds land in a flagged staging ledger, honestly labeled. Installed now; activated by reality.

## 4. The two-pitch week (the minimal climb) and what it forfeits

**Pitch C1, FIRST CONTACT (day one, near-zero code):** hand PLAYER_ONE plus the clone link to Adam. He plays sovereign mode with zero estate help. Separately, the operator exposes one bounded shared session (tunnel preferred over open bind; `--host` exists; one users.json row, created and retired with the session; the plaintext exposure is named in the session receipt the same way auth.py's own header names it). Falsifier: external bytes the estate did not author (issue, say line, screenshot, replay tape) within days, not windows; missing-list v0 filed in the inbox. This is B4-LITE: it does not claim the full B4 invariant ("usable without estate help" at width); it claims the first external price tag on onboarding.

**Pitch C2, THE ZIP (about 1 lane-day):** land `scripts/build_game.ps1` exporting `dist/` (PLAYER_ONE §2 already points at this exact door and honestly marks it closed; the paragraph "goes live unchanged the day the artifact lands"). NOT the rail: no butler, no Wharf channels, no delta patches, no CI export gate. Just the artifact that makes the NEXT stranger a link instead of a tutorial. The full rail re-prices itself against missing-list evidence.

Everything else waits for the missing-list: SRP6, prediction netcode, the GWAP live-flip (already gated by §3), worldgen (P7, which the route already correctly holds back), B5.

**What the two-pitch week forfeits, named and not hidden:**

1. **The deep unknown starts late.** P4 is the longest-tail item, and its state-size measurement does NOT need a stranger; pure two-pitch ordering delays discovery of route risk 1. The counter accepts this only because the v0 wire already bounds the downside (online play exists today; prediction is polish, not existence). If Adam's missing-list screams latency, the measurement happens the same week.
2. **Un-instrumented stranger risk.** If C1 fires before the GWAP payload is armed, Adam's session produces no verification rows and that signal is unrecoverable. Mitigated: arming the already-built adapter is part of C1's server session (§3's split).
3. **Weak anonymous fallback.** If Adam flakes, the two-pitch week has no channel link to publish, only a zip that must be handed to someone. The route's rail keeps a general stranger door climbing. This is the counter's weakest flank.
4. **Same N=1 blindness.** The route's own P6 attack surface: "Adam is a friend, not a market." Contacting him earlier does not make him a market; the two-pitch week buys speed with the same existential-proof ceiling.
5. **Auth debt compounds.** Every plaintext session is one more thing SRP6 must later displace. Bounded by naming the v0.5 plaintext era in receipts, the same way auth.py's honest-scope header already does.
6. **No calendar is saved.** Both shapes ride "dates are meaningless, just go" (non-goal 6); the two-pitch week wins information ordering, not dates.

## 5. Steelman: where the route wins (named, three places the counter could NOT beat it)

1. **SRP6 before the wire grows (P2 before P4).** "Porting is cheapest while the protocol surface is small" is a real dependency-order argument: retrofitting a handshake into a moving, prediction-bearing transport is the classic second-system trap. The counter narrows it (the v0 wire's plaintext era is already receipted as v1 debt in TWO headers: `server/auth.py` and `net_client.gd` "killing that is v1 debt"), but for the REAL wire the route's order is right. Not beaten.
2. **The rail as day-one parallel, IF the anonymous fallback is the true gate.** If Adam is unavailable, only an artifact reaches a genuine stranger, and "a player-gettable artifact converts every other row from working to load-bearing" (route thesis) holds for the PLATFORM claim. The counter beat this only for the first-contact signal, not for strangers at width. Not beaten for the platform.
3. **B5 last, P7 after the stranger.** Deferring all final picks until evidence exists, and content until the missing-list asks for it: agreed, not attacked. The counter also concedes the route's stagger discipline and risk ledger wholesale; it attacks ordering, not shape. And P1 (mate repair) the counter would cut outright, but the route already flags that exact doubt in its own attack surface, so it is consensus, not disagreement.

## 6. VERDICT: REORDER (stranger-first), not replace

**The one paragraph Opus will judge:** The route's engineering is sound but its sequencing spends 7-11 serial lane-days of estate-priced work before the only external pricing signal (a stranger's bytes) can arrive, and its two costliest premises are contradicted by bytes that exist today: `game/scripts/net_client.gd` is already a working server-authoritative wire for a game whose whole-unit, no-randomness, human-paced determinism does not need prediction yet, and PLAYER_ONE documents a five-minute stranger door that is open now, while plaintext v0 auth is honestly scoped and one `--host` flag from a bounded shared session. Reorder: contact first (C1, day one, on existing bytes), the zip (C2, one lane-day), the GWAP payload armed but its live flip gated on a non-estate participant, then SRP6, prediction netcode, the full rail, and B5, each re-priced against an actual missing-list instead of the estate's guesses. Keep the route's dependency logic everywhere the counter could not beat it: SRP6 before the grown wire, the rail before strangers at width, B5 last. The climb's own brutal one-liner said the estate lacks proofs that touch reality; the counter's whole point is that reality is touchable today, and the route's order is the last remaining excuse to build in the dark.

## 7. Source ledger (load-bearing claims, one line each)

| Claim | Path |
|---|---|
| Client wire v0 exists, speaks the protocol, predicts nothing, render-only mirror | `the-mountain/game/scripts/net_client.gd` header (byte-read this session, HEAD 7d5dbe2) |
| `game/network/` empty as a directory (gap row 2 true literally, false in spirit) | GAP_ANALYSIS row 2; byte-check this session |
| MOUNTAIN_SERVER env retargets a packed client without rebuild | `net_client.gd` header; PLAYER_ONE §2 |
| Server binds 127.0.0.1 by design; `--host` flag ships | `the-mountain/server/server.py:51,480`; `server/auth.py` HONEST SCOPE |
| Plaintext v0 honestly scoped; "v1 owes exactly that" (SRP6) | `the-mountain/server/auth.py` HONEST SCOPE |
| Five-minute stranger door documented; one-click build honestly not landed; solo is the complete game | `watch/inbox/mountain_climb/PLAYER_ONE.md` §1-§2 (landed this session) |
| Stranger seated in window 5; P2/P4/P5 estimates 1-2 / 4-6 / 2-3 lane-days | ROUTE_V0 §2, §3 |
| P5 falsifier accepts operator-through-client; P5 attack surface names the theater doubt | ROUTE_V0 P5 |
| GWAP templates require independent parties (the prematurity argument) | BIBLIOGRAPHY §5.3 (von Ahn and Dabbish, CACM 2008) |
| Meter law: never match-early volume; rare byte-backed artifacts | GOALS_DOSSIER §3.3; `watch/inbox/play_as_work_20260926/` |
| "they dont need to be perfacet" (plaintext-era legitimacy) | operator 09-29, GOALS_DOSSIER §1 |
| Phase 2 asks for the counter-route by name | `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md` Phase 2 |
| Route's three named load-bearing assumptions this lens maps onto | ROUTE_V0 §6 |
| Determinism of the game (whole units, no randomness, human pace) | PLAYER_ONE §1, §4; `server/auth.py` no-RNG note |

**Filing:** this file is the receipt; register in `watch/inbox/index_events.jsonl` (sibling shape, lens 3). It rides into the Opus brief beside ROUTE_V1 per plan Phase 2. Owner: this seat. No commit. Em-dash count: 0.
