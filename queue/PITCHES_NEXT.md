# PITCHES_NEXT: the merged climb queue (R12 synthesis)

Date: 2026-10-01 · Owner: R12 lane (this seat), per last-mile dispatch · File: `queue/PITCHES_NEXT.md` · Receipt twin: `watch/inbox/last_mile_20260930/R12_PITCHES.md` · No commit.

Inputs read whole before synthesizing (sha256-8 / bytes, read this session):

| File | sha256-8 | Bytes |
|---|---|---|
| `watch/inbox/mountain_climb/ROUTE_V0.md` | 1fef52ee | 27,945 |
| `watch/inbox/mountain_climb/ROUTE_COUNTER.md` | 4c42c4b4 | 16,045 |
| `watch/inbox/mountain_climb/ROUTE_ATTACK_DEPENDENCY.md` | aa426db0 | 10,828 |
| `watch/inbox/mountain_climb/ROUTE_ATTACK_ECONOMICS.md` | 6b821a3b | 8,326 |
| `watch/inbox/mountain_climb/THE_LENSING.md` | bbb78aae | 27,194 |
| `watch/inbox/frontier_asks/volley2/results/V2ASK1.md` | 8d04eebe | 13,226 |
| `watch/inbox/frontier_asks/volley2/results/V2ASK2.md` | 273d37c3 | 2,792 |
| `watch/inbox/frontier_asks/volley2/results/V2ASK3.md` | 2593a6ca | 18,168 |

Reading laws: THE_LENSING ordering governs where it diverges from ROUTE_V0 (it is the paid judgment both attacks and the counter feed); lane-days are effort, never dates; every falsifier is bytes a stranger could check; XP-numbers are this queue's IDs, each block names its source verdict. Em-dash count: 0.

Spec-truth notes carried into the queue: V2ASK2 is TRUNCATED (finish: content_filter, ends mid-sentence in Spec W1; the Q08 continuity and Q09 artifact build specs never landed; the Q07 witness verdict is complete). V2ASK1's Q19 spec is complete through the writer-task rules and cuts off before the visible-degradation tail. Both gaps are named in the pitches that consume them.

---

## 1. EXECUTION ORDER (the queue the mates and next windows execute)

Order = the lensing's priority (its section 4), amended by the dependency verdict (P2a close-out shape) and with the four build pitches R3-R8 already carry marked IN FLIGHT. 11 pitches plus a floor. Status legend: IN FLIGHT (R3-R8 building now, per dispatch), ARM (start this window), WAIT (dependency or human gate), HELD (gate named, do not flip), CUT.

### XP0. HYGIENE FLOOR (hours, precedes everything; not a pitch, the stance)

- WHAT: (a) commit and push the uncommitted SRP6/rooms/protocol server bytes to a remote off this disk; (b) rotate the 7 secrets in `memory/trajectory/steps.jsonl` and begin the history purge; (c) fix `requirements.txt` merge markers on any stranger install path; (d) one digest row queueing the three operator gates (Adam invite + GitHub username ask, Nous portal top-up, Phase-2-class GO if any further paid ask fires).
- SOURCE: THE_LENSING section 4 Floor 1-4 ("I rank this above every route pitch"); ROUTE_ATTACK_DEPENDENCY D1/D7 (uncommitted bytes are the silent single point of loss); ROUTE_ATTACK_ECONOMICS F5.5 (one operator-queue card, price attention upfront).
- FALSIFIER: a remote off this disk resolves the B-wave server bytes at a named commit; a rotation receipt names all 7 keys rotated; the digest row appears in today's GATE_DIGEST.
- LANES: 1, hours.
- DEPENDENCIES: none. This is the root.
- OPERATOR GATES: new-key custody (rotation), the digest itself is the gate card.
- STATUS: ARM, first thing tomorrow.

### XP1. THE STRANGER, identity-bound (C1 first contact)

- WHAT: operator sends the Discord invite and gets Adam's GitHub username; Adam clones the-mountain at a tag and runs sovereign mode per PLAYER_ONE; then one shared session over TLS with a pinned cert, server-side tape capture armed BEFORE he connects, and a server-issued challenge signed with the SSH key published at `github.com/<user>.keys` (wire `server/identity_binding.py` onto the hello path, Q05). Contact log with timestamps; pre-registered silence rules for the seat.
- SOURCE: THE_LENSING section 4 ranking 1 + section 5 C1; ROUTE_COUNTER C1 and section 2 (Adam's attention is the only perishable resource; attribution: price onboarding friction alone while separable).
- FALSIFIER: within 7 days of the invite, a session tape exists containing moves from a connection whose challenge signature verifies against Adam's published key, and the tape replays byte-identically. A 7-day no-show is itself the finding: the bottleneck is recruitment, not engineering; reprice toward a second named human, then the public link.
- LANES: 1 support lane; hours of prep; the wait is human.
- DEPENDENCIES: XP0 (tag + committed bytes); XP10 capture-arm MUST land before contact (stranger sessions are non-renewable evidence).
- OPERATOR GATES: the Adam Discord ask (operator-only; LW2 proved the estate cannot send it), username retrieval.
- STATUS: WAIT on operator gate + XP0. First divergence from ROUTE_V0: stranger moves from window 5 to the front.

### XP2. THE ZIP + CI GATE (P3 reduced; C2 the zip) · IN FLIGHT

- WHAT: land `scripts/build_game.ps1` exporting `dist/`; build from a TAGGED the-mountain commit with the commit sha embedded in the artifact and printed at boot (Q09 artifact identity; the exe+pck pair must detect a swapped pck); CI runs server tests red-blocking on merge; ship via GitHub Release or itch butler as the hired courier; one clean-machine run receipt (doubles as the PREPAREDNESS second-machine join). NO custom delta rail, NO Wharf channel stack.
- SOURCE: THE_LENSING section 1 P3 verdict ("do not build it": the rail is polishing what nobody asked for) + ranking 2; ROUTE_COUNTER C2 (about 1 lane-day); FIFTY_QUESTIONS Q09.
- FALSIFIER: on a machine that never had Godot or either repo, download one artifact, run, reach the water board, play one move, exit; boot prints the source commit; a swapped-pck run is detected; a CI row shows server tests blocking red.
- LANES: 1-2, 1-2 lane-days (the 3-5 estimate died with the rail).
- DEPENDENCIES: XP0 (tagged commit exists to build from); clean machine (shares XP8's box).
- OPERATOR GATES: publication-channel pick (convenience, not a blocker).
- STATUS: IN FLIGHT (R3-R8 artifact lanes).

### XP3. AUTH TRINITY (P2 re-scoped to the V2ASK1 migration) · IN FLIGHT

- WHAT: three phases, keyed by whatever auth produces. Phase 1 (days): K-MAC on the existing SRP6, `server/frame_mac.py` + `client/net/frame_mac.gd`, M1 wire format (exact-bytes HMAC-SHA256 tag, HKDF-derived per-direction keys + sid), caps/caps_tag in auth-success with the sticky no-downgrade client rule, receipts visibly carry `"i":"none"|"mac1"` so the chain stops certifying what it cannot see. Phase 2 (weeks): pinned TLS on both doors (`server/tls.py` ECDSA P-256 self-signed 10y, `pin.gd`). Phase 3: `server/auth_v2.py` scrypt (n=2^15) + server-random K' over TLS, SRP legacy renamed with a hard sunset; Option B is the recommendation, and the F4.2 benchmark (GDScript 2048-bit modexp timing) is the named flip to Option A. Plus the D1 close-out residue: sync estate server bytes into the-mountain, flip the `allow_plaintext_hello` default, delete the v0 plaintext path in BOTH trees.
- SOURCE: V2ASK1 Q03/Q04 full spec (Q04 undermines Q03: a 256-bit discrete log is cheap, so a K-MAC alone only raises the bar to "run a DLP solver"); THE_LENSING section 1 P2 (right to exist, wrong parameters and wrong guarantee: password-secrecy sold as identity); ROUTE_ATTACK_DEPENDENCY D1 (the port already exists uncommitted; P2 was priced as fresh work) and D6 (GDScript has no bigint; Option B deletes client crypto instead of adding it).
- FALSIFIERS: F3.1 bit-flip (every byte position, 8 flips each, open() must raise); F3.5 cross-language vectors (python + headless godot reproduce every tag); F4.1 pin actually pins (client must refuse a valid public-CA cert); F4.3 legacy break demo (run a DLP solver against a captured 256-bit login, recover K, file it); F4.4 zero password hits at rest; a fresh-venv stranger client completes the exchange and is rejected on wrong password; `grep -ri plaintext server/auth.py` finds only the honest-history docstring.
- LANES: 2-3, 2-4 lane-days phased (Phase 1 lands inside a window).
- DEPENDENCIES: XP0 commit first (the substrate is the untracked B-wave); XP4 door freeze in the same window (D7: front-load the decision so P4/P5 start against a frozen contract).
- OPERATOR GATES: SRP_SUNSET date is a policy pick; name it in the receipt.
- STATUS: IN FLIGHT (R3-R8 auth lanes).

### XP4. ONE LOOP, TWO DOORS (Q19: freeze the door, then unify liveness) · IN FLIGHT

- WHAT: freeze the D4 door decision (TCP door holds the world authority, ws door holds the room fan-out law; the client speaks TCP today), then convert the blocking TCP door to `asyncio.start_server` behind thin framing adapters; `Session` gains a bounded outbox, `last_rx`/`last_tx_ok`, and state LIVE/LAGGING/SILENT/EVICTED; a writer task per session with a 2.0s drain timeout; the tick never awaits a peer (`put_nowait`; QueueFull sets LAGGING and drops the oldest state frame, never event frames).
- SOURCE: V2ASK1 Q19 spec (complete through the writer-task rules; the visible-degradation tail was cut by content_filter and must be re-specced locally if the lane needs it); ROUTE_ATTACK_DEPENDENCY D4 (P4 names the wrong door: two doors exist and the client speaks neither one's choice... it speaks the TCP one); THE_LENSING P4 step 1 ("freeze the door").
- FALSIFIER: fault-injection test: kill/hang the ws task mid-broadcast and the TCP door or room pump notices (the head-of-line inverse); a slow peer evicts visibly, never silently.
- LANES: 1, 1 lane-day.
- DEPENDENCIES: none (bytes exist in both trees); XP3 and XP5 both consume its frozen contract.
- OPERATOR GATES: none.
- STATUS: IN FLIGHT (R3-R8 auth family).

### XP5. THE WIRE, MEASURED (P4 re-scoped)

- WHAT: prediction and reconciliation are DROPPED as design (a twitch bibliography for a whole-unit, no-randomness, human-paced puzzle; the v0 mirror over TCP is the correct rung and is built). Measure instead: snapshot bytes per tick and move-echo latency over a real WAN link (Adam's XP1 shared session is the instrument); add delta encoding only if the measurement demands it; prediction only on a receipt that demands it.
- SOURCE: THE_LENSING section 1 P4 verdict (4-6 lane-days becomes roughly 1-2) + ranking 4; ROUTE_COUNTER section 1.1/2.3; V2ASK3's transport discipline feeds any delta work.
- FALSIFIER: a measurement receipt naming bytes/tick and echo RTT over a real tunnel; any delta or prediction code lands only beside a receipt that demanded it. Reinstatement bar (named): echo RTT above roughly 150 ms over a real tunnel that a playtester reports as bad feel, or per-tick state too large for full snapshots at the observed link rate.
- LANES: 1, 1-2 lane-days.
- DEPENDENCIES: XP4 (frozen door); XP1 (the WAN session produces the data).
- OPERATOR GATES: none. The two-physical-machines demand is DOWNGRADED per economics F5.4 (one machine plus one CI/VM runner is enough for "two clients see the same world").
- STATUS: WAIT on XP4 + XP1 session.

### XP6. PARITY, CONSTANTS, INTEGER DOMAIN (C3 build half; Q15 then Q16 then Q14) · IN FLIGHT

- WHAT: build order is V2ASK3's own cross-link law. (a) Q15: `tuning/flock.toml` as the one human-edited source, `tools/gen_constants.py` emitting all trees plus CONSTANTS_HASH, regen-diff CI check, literal lint; Step 0 is a HUMAN decision: flock.gd FLEE_RADIUS=20.0 vs fish_brain.gd=14.0 may be two concepts that collided on a name (rename, do not unify). (b) Q16: integer-domain policy for the twin engines: INT_DOMAIN limits in the generated constants, exact q/r decomposition formulas replacing naive overflow-prone products, sticky+hashed `sat_add`/`sat_mul`, `fdiv`/`fmod` helpers only, must-match vs may-diverge split enforced structurally, the 7-test overflow family. (c) Q14: the flock parity harness, roughly 400 lines: GDScript paired against numpy first (then JS, then Luau), `flockframe/1` hex-float frames, injected randomness, teacher-forced single-step comparison (Tier D exact with the threshold band; Tier C 4-ulp tolerance), plus the GDScript-rules-vs-Python-rules per-tick hash compare THE_LENSING section 3 demands.
- SOURCE: V2ASK3 full spec (Q14/Q15/Q16); THE_LENSING section 3 (rule parity between the two implementations is unverified and sits directly under "verifiable play"); FIFTY_QUESTIONS Q11-Q18 family.
- FALSIFIERS: the mutation-sensitivity list (radius +1.0, `<` for `<=`, dropped dt, negated separation, stale velocity) must turn the harness red in every case; a 1-ulp position perturbation must stay green; a runner with a mismatched constants_hash must exit 3; reverting the depth formula to the naive product must turn overflow tests 2 and 6 red (else the family tests nothing).
- LANES: 2, 2-3 lane-days.
- DEPENDENCIES: Q14 consumes Q15 + Q16 outputs (hash guard, domain limits).
- OPERATOR GATES: Step 0 concept call (rename vs unify, and which value is canonical, decided by playtest, not by lane seniority).
- STATUS: IN FLIGHT (R3-R8 parity lanes).

### XP7. CONTINUITY + WITNESS (C2 floor, proven by a restore drill)

- WHAT: encrypted offsite backup including the biography; a pre-commit/append-time secret scanner wired to every `steps.jsonl` writer (Q10: the leak is a pipeline, not an incident); the effect broker put on the real effect path or its doctrine retracted (the empty-string denylist denies everything while 24,939 metered calls happened outside it); a verkle checkpoint log in C2SP form with the tip anchored in Rekor (hashedrekord) and OpenTimestamps, published somewhere the estate does not control; then the drill: restore the estate on the M4 from offsite bytes alone.
- SOURCE: THE_LENSING section 5 C2 + section 3 (the chain is tamper-evident only to its writer; 618 evidence_lost and 2,821 amended rows are a laundering channel; a gist alone is still writer-controlled); V2ASK2 Q07 verdict (complete: transparency log core layer, countersigning is the upgrade path not day one). NOTE: V2ASK2's Q08/Q09 build specs were cut by content_filter and never landed; build Q08 from THE_LENSING C2 falsifier, which is complete, and refire Q09's spec only if XP2 needs more than its own falsifier.
- FALSIFIER: on the M4, from offsite bytes only, `_verify_chain_consistent()` returns True at the published tip root; the 6.4-style audit rerun flips the four FAIL rows (secrets, backup, requirements, denylist) to PASS with no new secret hits; a planted fake key in a step row is caught by the gate.
- LANES: 1-2, 1-2 lane-days plus operator hands.
- DEPENDENCIES: XP0 rotation; XP8 shares the M4 session (this drill is the first M4 run receipt D5 wants).
- OPERATOR GATES: offsite target/account choice; M4 physical hands.
- STATUS: ARM, parallel with XP1 (the lensing's own C2 placement).

### XP8. M4 VERIFIABLE PLAY (C3 machine half; Q06)

- WHAT: run the full frozen-tape replay suites (202/202 baseline) on the M4 (ARM macOS) and on the clean Windows machine, from offsite bytes; replay Adam's XP1 tape on a machine he did not play on.
- SOURCE: THE_LENSING section 2 (the M4 matters for cross-architecture determinism: float and libm classes surface between x86 and ARM; here the lensing sides WITH dependency D5 against economics) + C3 step 1/3; FIFTY_QUESTIONS Q06.
- FALSIFIER: 202/202 on both machines, or the first divergent tick named; Adam's tape reproduces its hash elsewhere. A single divergence falsifies portability and becomes the top engineering item (which is real work, better than a prediction layer).
- LANES: 1, plus operator hands.
- DEPENDENCIES: XP7 offsite bytes; XP1 tape.
- OPERATOR GATES: M4 physical hands.
- STATUS: WAIT on XP7 drill + XP1 tape.

### XP9. PRE-REGISTERED INFORMED CHOICE (P8/B5)

- WHAT: TODAY, before Adam plays, write the decision the estate would make now for engine, netcode, and DB, and the observation that would flip each (pre-registration). P8 then passes only if a recorded flip-condition was actually evaluated against stranger bytes. Decisions are reversible picks with named flip-falsifiers, never ships-burned.
- SOURCE: THE_LENSING section 1 P8 verdict ("cannot fail as specified": any receipt passes even at N=1 or zero; pre-registration is the fix) + ranking 5; ROUTE_ATTACK_DEPENDENCY D3 (anonymous first-run yields telemetry, not a missing-list; split the evidence grades and time-box the upgrade).
- FALSIFIER: one decision receipt per choice naming evidence rows used, the rejected alternative, the counterparty risk priced, and the flip-falsifier; at least one flip-condition evaluated against actual Adam bytes.
- LANES: 1, 0.5-1 lane-day; evaluation lands after XP1.
- DEPENDENCIES: pre-registration has none (write it now); evaluation gates on XP1 bytes; the paid-ask half of P8 (if fired) gates on credits + operator GO.
- OPERATOR GATES: Phase-2-class GO + Nous top-up for any paid ask; local packaging needs none.
- STATUS: ARM (the pre-registration half lands this week, before contact).

### XP10. GWAP CAPTURE-ARMED, FLIP HELD (P5 reduced; B3)

- WHAT: arm the append-only tape, hash-chain capture, and the gwap-to-gps adapter on every session BEFORE first contact (a stranger's play must never land un-instrumented). Agreement rounds run only with two or more key-bound non-estate participants. The GPS live flip is HELD until `record_verdict` binds verdicts to checkable artifacts. Self-play rounds land in a flagged staging ledger, honestly labeled.
- SOURCE: THE_LENSING section 1 P5 verdict (the falsifier cannot fail in the way that matters: an agent launched with a goal satisfies "not scripted move-by-move"; that is identity-as-label rebuilt) + ranking 6; ROUTE_COUNTER section 3 (the split: installed now, activated by reality); ROUTE_ATTACK_DEPENDENCY verdict 3 (HOLD, from the dependency side: no identity fallback by design); ROUTE_ATTACK_ECONOMICS F5.3.
- FALSIFIER (rewritten per the lensing): an agreement event whose participants hold keys the estate does not hold, producing a disagreement the estate did not predict. Capture-arm check: Adam's XP1 session lands a full tape plus chain row.
- LANES: 0.5-1, 0.5-1 lane-day (schema, adapter, tests exist; welding only).
- DEPENDENCIES: HARD ordering: lands before XP1 contact. The flip gates on non-estate participants (HELD).
- OPERATOR GATES: none.
- STATUS: ARM now; HELD half do-not-flip.

### XP11. THE SECOND BOARD (P7; content pipeline)

- WHAT: weld the tested worldgen (`mag/worldgen.py`, `mag/river.py`) into the server+client loop; boards 2..N generated, same seed yields byte-identical JSON receipted by hash; N46W122 stays a regression fixture. FIRST: re-estimate the multi-world server work D2 exposed (server.py owns exactly one world and never touches Room; multi-world has never existed in any tree; an unpriced architecture item ordered last).
- SOURCE: ROUTE_V0 P7; THE_LENSING ranking 7 (after the stranger, as the route already says); ROUTE_ATTACK_DEPENDENCY D2 (P7 mispriced); ROUTE_ATTACK_ECONOMICS F5.2 (cut the mid-P4 start; polishing before the stranger speaks).
- FALSIFIER: two generated boards live in one server process simultaneously; identical seed on two machines produces byte-identical board JSON (hash receipt). The ordering itself is falsified by the missing-list: if it screams content, XP11 was late; if it screams auth/onboarding friction, XP11 is early.
- LANES: 1-2, 2-4 lane-days after the D2 re-estimate.
- DEPENDENCIES: XP1 missing-list (discipline, not dependency).
- OPERATOR GATES: none.
- STATUS: WAIT (after the stranger).

### CUT: P1 BASECAMP REPAIR

All three lenses plus the counter agree: no pitch consumes a mate output; it becomes an opportunistic 20-minute auth-header fix when a lane touches the dispatcher. ROUTE_V0's own attack surface conceded it; THE_LENSING section 1: "It should not be a pitch."

---

## 2. ALREADY IN FLIGHT (R3-R8, per dispatch)

Four pitches are being built by the R3-R8 lanes right now and this queue does NOT re-dispatch them; it feeds them their falsifiers and dependencies:

| Pitch | Built by | What this queue adds |
|---|---|---|
| XP2 THE ZIP + CI GATE (artifact) | R3-R8 artifact lanes | the Q09 identity falsifiers (tagged commit, boot sha, pck-swap) and the rail cut |
| XP3 AUTH TRINITY (auth) | R3-R8 auth lanes | the V2ASK1 three-phase spec order (MAC before TLS before retirement), F3.x/F4.x falsifiers, the D1 close-out residue (sync, flip flag, delete plaintext in both trees) |
| XP4 ONE LOOP TWO DOORS (auth family) | R3-R8 auth lanes | the D4 freeze decision and the Q19 fault-injection falsifier |
| XP6 PARITY/CONSTANTS/INTEGER (parity) | R3-R8 parity lanes | the Q15 to Q16 to Q14 build order and the Step 0 human gate |

The single most load-bearing service this queue owes the in-flight lanes: XP0a commits their substrate off-disk. R3-R8 are building on a working tree whose auth bytes exist nowhere else.

## 3. SERIAL vs PARALLEL (per the lensing's order)

**The serial spine (each step consumes its predecessor's bytes):**

XP0 floor (hours) → XP10 capture-arm + XP1 the stranger (first contact; gated on the operator invite, NOT on any build pitch; the clone+F5 door already exists) → XP9 flip-evaluation against Adam's bytes → XP11 second board after the missing-list.

**Parallel from day one (the lensing's own placement):**

- XP2, XP3, XP4, XP6: already in flight (R3-R8); continue.
- XP7 continuity+witness: explicitly parallel with XP1 (lensing C2: "Why second (parallel with C1)").
- XP8 M4 proof: after XP7's offsite bytes exist (same M4 session).
- XP5 wire-measured: after XP4's frozen door; uses XP1's WAN session as the instrument.
- XP9 pre-registration half: lands now, before contact (its evaluation half is the spine).
- Standing metabolism (improve cycle, meters, census, quota ledger) climbs beside everything, never as a pitch.

**Held (named gates, do not flip):** XP10's agreement rounds and GPS live flip (until 2+ key-bound non-estate participants exist and record_verdict binds verdicts to artifacts).

**Window sketch (effort, not dates):** W1: XP0 + operator digest, R3-R8 continue. W2: XP1 invite out and contact; XP2 first tagged artifact + clean-machine receipt; XP3 phase-1 MAC tests. W3: XP7 restore drill + XP8 202/202 on M4; XP5 measurement on the live session. W4: XP9 flip-evaluation; XP11 re-estimate and build if the missing-list asks. Lane discipline throughout: 6-8 staggered per the refire law, never 19-20; a 429/1302 is a HOLD, never a width cut.

## 4. FIRST ACTION (tomorrow morning's first lane; one item)

**XP0a: commit and push the uncommitted B-wave server bytes (estate `server/auth_srp6.py` untracked; `server/protocol.py`, `server/protocol_table.py`, `server/server.py` modified) to a remote off this disk.**

Why this and not the invite: D1/D7 name these bytes the silent single point of loss; the R3-R8 auth/parity/artifact lanes are building directly on top of a working tree whose first leg of the missing mile exists nowhere else; a disk incident or careless checkout erases the in-flight substrate. It also mints the tagged commit XP2 builds from and the handshake contract XP3 closes out, so one lane unblocks three. One lane, under an hour. Falsifier: a remote off this disk shows the server bytes at a named commit, and `git status` no longer lists auth_srp6.py as untracked. The operator-gate digest row (XP0d) files in the same window; the invite itself fires when the operator answers it.

## 5. Source ledger (one line each)

| Claim | Path |
|---|---|
| Lensing priority order, floor, P1 cut, P4/P2/P5/P8/P3 re-scopes, C1/C2/C3 counter-route | `watch/inbox/mountain_climb/THE_LENSING.md` sections 1, 4, 5 |
| MAC/TLS/SRP-retirement spec, F3.x/F4.x falsifiers, Q19 one-loop design | `watch/inbox/frontier_asks/volley2/results/V2ASK1.md` |
| Q07 witness verdict (Rekor/OTS/checkpoint); Q08/Q09 specs cut by content_filter | `watch/inbox/frontier_asks/volley2/results/V2ASK2.md` (truncated, 2,792 bytes) |
| Q14/Q15/Q16 parity specs, build order Q15 to Q16 to Q14, mutation falsifiers | `watch/inbox/frontier_asks/volley2/results/V2ASK3.md` |
| D1 uncommitted port, D2 multi-world, D3 evidence grades, D4 door, D5 M4, D6 bigint, D7 commit-first | `watch/inbox/mountain_climb/ROUTE_ATTACK_DEPENDENCY.md` |
| F1 multipliers, F2 operator gates, F3 quota currency, F5 cuts | `watch/inbox/mountain_climb/ROUTE_ATTACK_ECONOMICS.md` |
| C1/C2 two-pitch week, stranger-first reorder, GWAP split | `watch/inbox/mountain_climb/ROUTE_COUNTER.md` |
| Original P1-P8 pitches, estimates, serialization | `watch/inbox/mountain_climb/ROUTE_V0.md` |
| Q05 identity wiring, Q06 M4 replay, Q09 artifact identity, Q10 secret pipeline, Q19 liveness check | `watch/inbox/mountain_climb/FIFTY_QUESTIONS.md` |
| R3-R8 in-flight scope (auth/parity/artifact) | last-mile dispatch briefing to this lane (R12) |

**Filing:** receipt twin at `watch/inbox/last_mile_20260930/R12_PITCHES.md`; registered in `watch/inbox/index_events.jsonl`. Owner: R12 lane. No commit. Em-dash count: 0.
