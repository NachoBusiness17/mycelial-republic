# FLEET COORDINATION DOCTRINE - naval/military/maritime C2 mapped onto Mag organs (2026-10-17)

Classification: CARD (research + read-only self-steal + design proposal). No code written, nothing restarted.
Producer: Grok Bot executor, 2026-10-17 ~15:43-16:20 ET (UTC-4).
Survey method on DESKTOP-7C70KSC: file headers via Get-Content/Read, rg on mag/ tools/ scripts/ server/,
Get-Item mtimes, Get-ScheduledTask, `docker ps` (read-only). No git. Not opened: .env, key files,
memory/trajectory/steps.jsonl, secret_gate_results, free_keys. Only file written: this one.
Companion card (read first, not repeated here): `watch/LIBRARY/SHARED_SURFACE_SELFSTEAL_20261017.md`.

---

## 0. HEADLINE

Navies and armies fixed the same problem we have (many units, intermittent comms, nobody sees
everything) with five structural moves, not with a supervisor watching everyone:

1. **One shared picture** that every unit feeds and reads (Link 16 / COP; blackboard systems).
2. **Intent instead of instructions**, so units act without asking (mission command; command by negation).
3. **Fixed report formats**, so a report from any unit is machine-mergeable (SALUTE/SPOTREP/SITREP).
4. **Space and time reserved before you act**, so friendly units cannot collide (fire-support
   coordination measures, EMCON, track-number blocks, convoy stations, COLREGs give-way rules).
5. **Formal hand-offs and hazard broadcasts** (relief of the watch, deck log, Notices to Mariners, NAVAREA warnings).

Mag already owns the parts for all five. They are scattered, several are dormant, and two of them
(pheromones, briefs) exist twice. Today's failures map exactly: the OpenCode breach and 2 unused
OpenCode keys = **no Notice-to-Mariners channel**; seats rewriting each other's chain rows =
**no deconfliction measure above the byte-level lock**; the lab restarted/frozen by unknown seats =
**no lease on processes and no AIS-style position report**. The 2026 multi-agent coding papers
(AgentRoom, Claim Plane, MPAC) independently land on the same answer: an explicit claim/intent
layer, enforced by the state store rather than by agents reading chat, is what carries the gain.

The design below is "code is law" (Lessig): the coordination lives in the structure every seat
must pass through (the warm MCP door, the receipt writer, the lease store, the chain writer), not in
a watcher that polices after the fact.

---

## 1. RESEARCH DIGEST (sources in section 6; nothing here is invented)

### 1.1 Naval

- **Composite Warfare Commander (CWC) and command by negation.** The officer in tactical command
  delegates warfare areas (air, surface, undersea, strike, EW) to subordinate warfare commanders.
  JP 3-32: "Once missions and functions are assigned, the subordinate commander is expected to take
  required actions without delay, keeping the superior commander informed... The superior commander
  retains the authority to negate any particular action." Coordinators manage shared sensors and
  assets. Limitation noted by FAS/RFS: multiple tasking of one platform without clear priorities. [S1-S4]
  - *Mag reading:* each seat owns a lane/area; acts without asking; reports; the operator (or a
    proposal quorum) can veto. Avoid one seat holding many areas with no priority order.
- **Distributed Maritime Operations (DMO).** "Dispersing the fleet while concentrating effects";
  distributing people, platforms, munitions and data "across time, spectrum, and space"; Maritime
  Operations Centers treated as warfighting platforms; information dominance as the enabler;
  backup C2 nodes when networks degrade. Critics (Atlantic Council) say DMO lacks specificity. [S5-S7]
  - *Mag reading:* ~600 free models are the dispersed fleet; the effect is concentrated only if they
    share one picture and one intent. Any seat must be able to take over the coordinator role
    from files alone (no single brain).
- **Link 16 / tactical data links / COP.** TDMA time slots (128/s) assigned per unit; every unit
  reports tracks with a **track number from a pre-assigned block** so two units never mint the same
  ID; multilink forwarding "provides a common tactical picture to all units"; duplicate track
  numbers when networks bridge are a known top engineering problem. Nets are planned in an
  OPTASKLINK message (who transmits in which slot, which TN block). [S8-S11]
  - *Mag reading:* (a) the COP is one merged board; (b) each seat gets its own ID namespace for
    rows it mints (no two seats write the same row key); (c) the "net plan" is a file every seat reads at join.
- **ATP-1 Vol II / EXTAC signalling, flag hoist.** Allied navies share one signal book: a small fixed
  vocabulary of coded signals usable over flag, light, voice or data; the tackline separates groups to
  avoid ambiguity; emergency signals are a separate short chapter. The code "groups... are a simple
  unchanging code." [S12-S14]
  - *Mag reading:* a short fixed verb vocabulary for fleet messages (CLAIM, RELEASE, SPOT, SITREP,
    NOTICE, RELIEF, VETO), the same on every carrier (MCP, room.jsonl, receipts).
- **EMCON.** "The selective and controlled use of electromagnetic, acoustic, or other emitters to
  optimize command-and-control capabilities while minimizing... mutual interference among friendly
  systems." Graded conditions ("a dimmer, not a switch"); an EMCON bill names who controls each
  emitter, keeps a status board, and requires permission before activating radiating equipment. [S15-S17]
  - *Mag reading:* graded quiet levels for the fleet; every "emitter" (process, lab, writer of a hot
  file) has a named controller on a status board; activating it needs a lease.
- **Convoy doctrine.** WWII US convoys split authority: the Convoy Commodore controlled merchant ship
  formation, station keeping, signals and darkening; the Escort Commander was the tactical commander
  of the escort. Pre-sailing conferences issued written orders covering formation, routes, signals,
  radio discipline and emergencies. [S18-S20]
  - *Mag reading:* separate "who keeps formation" (the board/leases) from "who fights" (seats doing
    work); a pre-sailing brief (warm preamble) is mandatory before a seat joins.

### 1.2 Military C2

- **Mission command / Auftragstaktik.** ADP 6-0 principles: competence, mutual trust, shared
  understanding, commander's intent, mission orders, disciplined initiative, risk acceptance.
  Intent = purpose, key tasks, end state. Mission orders state results, not methods, plus
  "minimum essential coordination instructions." [S21-S22]
- **OODA.** Boyd's Patterns of Conflict: Observe-Orient-Decide-Act; orientation is the hub; the edge
  comes from cycling faster than the environment changes. [S23]
- **JADC2.** Linking sensors, data and weapons across services through shared data so commanders
  "understand the battlespace and act faster"; open issues are resilience, interoperability, authority,
  and human control. [S24]
- **Mosaic warfare / kill webs (DARPA STO).** Disaggregated sensors, deciders and effectors that
  compose into many alternative "kill paths" instead of one brittle chain; decision-centric
  operations that preserve optionality. [S25-S27]
  - *Mag reading:* any seat can be sensor, decider or effector for a task; the board links them;
    losing one seat must not break the path.
- **Report formats.** SPOTREP mnemonic SALUTE (Size, Activity, Location, Unit, Time, Equipment);
  current Army SPOTREP has 11 lines incl. report DTG, reporter, assessment, narrative,
  authentication. SITREP reports own status, readiness, problems, recommendations. [S28-S29]
- **Relief of the watch.** OPNAVINST 3120.32D: the relief reviews the log and situation before
  taking over; the outgoing watch briefs unusual conditions, outstanding orders, equipment status,
  upcoming evolutions; formal "I am ready to relieve you" / "I relieve you" / "I stand relieved";
  the outgoing OOD signs the log before leaving. [S30]
- **Rules of engagement.** "Directives issued by competent military authority that delineate the
  circumstances and limitations under which forces initiate or continue engagement"; the Standing ROE
  always preserve the unit's inherent right of self-defense. [S31-S32]
- **Deconfliction / fire-support coordination measures.** The FSCL is a *permissive* measure:
  beyond it, targets may be engaged expeditiously but affected commanders must be informed;
  *restrictive* measures (no-fire / restricted-fire areas) require coordination before fires. [S33-S35]
  - *Mag reading:* most of the estate is permissive (act, then report); a short list of hot assets
    (verkle_knot.py, the chain, the lab/containers, key files) is restrictive (lease first).

### 1.3 Maritime civil

- **COLREGs.** Rule 2: nobody is excused from ordinary prudence; departures allowed only to avoid
  immediate danger. Rule 15 crossing: one vessel is give-way and must take early substantial action;
  the other stands on but must act if the give-way vessel does not. "Stand-on is an obligation, not a
  right of way." [S36-S37]
  - *Mag reading:* deterministic tie-break when two seats want the same asset: the holder of the
    live lease stands on; the newcomer gives way; but a stand-on seat that sees danger still acts.
- **AIS.** SOLAS V/19: ships automatically broadcast identity, type, position, course, speed,
  navigational status; static/voyage data every 6 min or on change; dynamic data every 2-10 s
  underway, 3 min at anchor. [S38-S40]
  - *Mag reading:* every seat broadcasts a heartbeat: who, which lane/model, what it is on, which leases
  it holds, status (underway/at anchor/not under command). Cadence scales with activity.
- **VTS.** IMO A.1158(32) (2021): a shore service that provides information, advice, warnings and
  instructions to traffic; older A.857(20) split information / traffic organisation / navigational
  assistance. [S41-S42]
- **Notices to Mariners / navigational warnings.** NGA's NtM corrected charts and publications;
  NtM 11/2026 was the final US issue, while NGA navigational warnings (NAVAREA IV/XII, HYDROLANT/PAC/ARC)
  continue, updated every 15 minutes, broadcast via GMDSS. [S43-S45]
  - *Mag reading:* two channels: standing corrections (law/config changes) and in-force hazard
    warnings that stay up until cancelled.
- **Bridge resource management.** Closed-loop communication (order, read-back, confirm, report done);
  challenge-and-response with graded assertiveness; any member may raise a factual safety concern
  and the person in charge must answer it. [S46-S47]
- **Ship's log.** The Navy deck log is the official watch-by-watch chronological record and may be
  legal evidence; OPNAVINST 3100.7C governs entries (movements, course/speed changes, sightings,
  accidents, inspections, significant events). [S48-S49]

### 1.4 Swarm and multi-agent research

- **DARPA OFFSET.** Swarms of 250+ small air/ground robots; a Swarm Tactics Exchange where tactics
  are composed from collective behaviours; final FX-6 used 300+ platforms with shared telemetry. [S50-S51]
- **Stigmergy.** Grasse (1959): coordination through traces left in the shared environment;
  pheromone deposits attract more deposits (positive feedback) and decay prevents runaway.
  Theraulaz & Bonabeau distinguish quantitative (gradient) from qualitative stigmergy. ACO adds
  evaporation to avoid premature convergence and keep exploration. [S52-S53]
- **Blackboard systems.** Hearsay-II / Nii: independent knowledge sources communicate only via a
  shared blackboard; a control component schedules who acts next by focus of attention. [S54-S55]
- **2025-2026 LLM multi-agent papers (all fetched or abstract-verified):**
  - *Why Do Multi-Agent LLM Systems Fail? (MAST, NeurIPS 2025)* - 14 failure modes over 1,600+ traces;
    inter-agent misalignment includes conversation resets, information withholding, ignored peer
    input; failures are mostly organisational design, not base-model weakness. [S56]
  - *LbMAS (arXiv 2507.01701)* - shared blackboard replaces per-agent memory; a control unit picks agents. [S57]
  - *Blackboard for data discovery (arXiv 2510.01285)* - main agent posts requests, specialists
    volunteer by capability; separate response board. [S58]
  - *AgentRoom (arXiv 2608.23740)* - MCP tools room_claim / room_release / room_state / room_broadcast /
    room_read over a shared workspace. "Coordination, not parallelism or CRDT-merge, bears the load."
    Uncoordinated parallel agents scored *below a single agent* because one silently overwrote the
    other's file; free-text claims in chat failed where a system-level claim conflict error succeeded;
    quality peaked at 2 agents per room and broadcast traffic rose super-linearly past 3 (single channel). [S59]
  - *Claim Plane (arXiv 2607.21909)* - concurrent change as a pre-write admission problem: versioned
    ChangeIntent, leases, fencing tokens, fail closed on ambiguous authority; "separating
    probabilistic planning from deterministic authority." Small feasibility sample only. [S60]
  - *MPAC (arXiv 2604.09744)* - intent-before-action, structured CONFLICT_REPORT objects, TTL'd intents,
    INTENT_CLAIM to take over a dead agent's work, frozen scopes on unresolved conflict, Lamport
    watermarks, optimistic concurrency with state_ref_before/after hashes. One-run benchmark only. [S61]

---

## 2. SELF-STEAL: COORDINATION ORGANS THAT ALREADY EXIST

Live = state file written today/yesterday or scheduled task firing. Times ET. Repo-relative paths.

| # | Organ | What it does | Live? (evidence) |
|---|---|---|---|
| 1 | `watch/room.jsonl` (writers incl. `mag/board_directive.py`, `mag/board_tailer.py`, `mag/read_receipts.py`, `mag/chan.py`) | De facto fleet log: one JSON row per event `{ts, kind, seat, verb, detail}` | **LIVE** - 6.1 MB, 18,327 rows, last row 15:42 today (seat zcode, monitor.lane) |
| 2 | `mag/warm_surface.py` + `mag/mcp_server.py` profile `warm` | Fixed `mag://warm/*` resources (tip, warm_state, zknot, LIBRARY index, law cards, per-seat preamble), redacted, read-only; tools estate_warm_read / estate_chain_verify / estate_shared_receipt | **BUILT TODAY** (14:50 / 15:04). Container `mag-mcp` up 42 h, i.e. started before this code; per the shared-surface card it runs profile archivist, so warm is probably not served yet (not verified) |
| 3 | `mag/estate_bridge.py::shared_receipt_append` | Seat write-back: `watch/receipts/seat_<utc>_<seat>_<sha12>.json`, exclusive-create, redacted, no caller path | Built; **zero traffic** (no `seat_*` files in watch/receipts yet) |
| 4 | `mag/proposals.py` + `scripts/proposals.py` + `configs/seat_allowlist.json` | Ed25519-signed seat proposals/reviews/promotions, quorum 2 or operator override, never touches git | **BUILT TODAY** (15:04-15:10); `watch/receipts/proposals/` does not exist yet = zero proposals |
| 5 | `tools/pheromone.py` | Attention bus: deposit / reinforce / exponential decay (half-life such that 24 h = 1/16, i.e. 6 h) / hottest / non-exclusive claim / solved collapses heat | Built 10-07; **dormant** - `memory/pheromone/pheromones.jsonl` has 7 rows, last 10-07 |
| 6 | `mag/swarm_tools.py` pheromone_drop / pheromone_trail + blackboard_post / blackboard_read | Content-addressed marks of kind trail/fruitful/dead/here/danger/signal/drift; a pinned blackboard; exposed on several mcp_server profiles and in `mag/swarm_worker.py` | **Semi-dormant** - 174 marks, last 10-01; blackboard last 10-11 |
| 7 | `mag/verkle_knot.py` LOCK (`memory/biography/.verkle.lock`) | Single-writer O_EXCL lock with JSON heartbeat record (5 s beat, 120 s stale), the lost-update fix | **LIVE** (tip rewritten 14:44 today). Serialises *bytes*; does not decide *whose rows* a seat may rewrite |
| 8 | `tools/instance_guard.py` | Pidfile singleton (exit 3) + O_EXCL per-ask claim + doubled-key tripwire | Built 10-02; adoption breadth not measured here |
| 9 | `tools/ledger_lock.py` | Single-writer lock + fsync append for JSONL ledgers; identity stamp; stale break logged | Built 09-26; header says "nothing here is wired into a live writer at landing" |
| 10 | `mag/concurrency_gate.py` | Cross-process lease-file slots per model, stale-steal after LEASE_SECS | Built 08-25; used by z.ai lanes |
| 11 | `mag/seat_registry.py` | Seat register / heartbeat / unregister; 300 s stale = died; REST `/api/v1/seats/*` | **Dormant** - trail last 09-26 |
| 12 | `mag/seat_steer.py` | Architecture path to send a message into a seat surface; enqueue for drainer | **LIVE** - `memory/runs/seat_steer/` 856 items, last 09:08 today |
| 13 | `mag/peer_handoff.py` | Seat-to-seat handoff files `queue/handoff/peer-*.json` + trail | **Dormant** - trail 09-01, queue last 09-29 |
| 14 | `mag/rib_bus.py` | Frontier instruction layer as verkle knots + per-domain memory mount + inject_for() | **Dormant** - `memory/rib_bus/` last 09-30 |
| 15 | `mag/hermes_steering.py` | Dispatch/steer Hermes; receipts `memory/runs/hermes_dispatch_log.jsonl` | Recent (log 10-11); task MagHermesBurn247 running |
| 16 | `mag/lane_supervisor.py` | Lane probe state machine UP/FLAKING/DOWN/RECOVERED + failover chains | **DISABLED** - task "Estate LaneSupervisor" disabled, last run 09-28 result 1 |
| 17 | `tools/leave_dispatcher.py` + `configs/mates.yaml` | Mates leave protocol: constant argv, mission files, atomic claim of next mission, concurrency law 16 (24 staggered) | **LIVE** - MagLeaveProtocolDaily 08:12 today, result 0; 249 mission files |
| 18 | `tools/nightcrew.py` | Drains `queue/ds_overflow/INBOX.jsonl` by lane (ds/opencode/grok/ollama); ONE-WRITER by moving claimed rows; free-lane results bank as FINDINGS | **LIVE but idle** - MagNightCrew every 30 min (15:41 result 0); INBOX empty since 10-10 |
| 19 | `tools/task_wall.py` | Concurrent chore engine that ramps per-lane concurrency to the provider wall and records ceilings | Ledger written 10-16 20:02; file edited 08:24 today |
| 20 | `server/room.py`, `server/rooms.py` | Transport library: encode-once fan-out, drop-on-slow, presence/expiry sweep; explicitly no authority | Library; listener not checked |
| 21 | `memory/briefs/latest.md` | Old session brief | **FROZEN fossil** since 09-26, OS read-only by design |
| 22 | `state/START_BRIEF.md` (`mag.state_brief`) | Deterministic boot brief | Regenerated 08:06 today; itself reports "No framework loops alive", queue 100 |
| 23 | `watch/LIBRARY/INDEX.md` (librarian) | Library index, served as `mag://warm/library-index` | LIVE (15:35 today) |
| 24 | `mag/claims_desk.py`, `mag/claims_verify.py`, `mag/claim_repair.py` | Claims (assertion) desk/verification | Present; not read in this pass |

Other observations: `MagBootRegenDaily` (feeds warm_state) last result 2 today though warm_state.json
was written 07:15; `MagTipWitnessDaily` result 2. Container `mag-sovereign` shows "Up 2 hours" at
survey time (restarted roughly 13:45-14:15 ET); this pass could not tell who restarted it, which is
itself the gap proposal P2 closes.

**Duplications to fold, not rebuild:** two pheromone stores (#5 heat/decay vs #6 typed marks); two
handoff paths (#13 peer_handoff vs receipts); three lock shapes (#7, #8/#9, #10) that are one idea.

---

## 3. DOCTRINE -> ORGAN MAP (reuse first)

| Doctrine idea | Rides on | Tag |
|---|---|---|
| COP / Link 16 common picture | `mag/warm_surface.py` new fixed URI `mag://warm/cop` composed from #1, #3, #5/#6, #7, #11, #16 | small adapter |
| Track-number blocks (no two units mint one ID) | chain-row keys prefixed by seat id; verkle writer refuses a rewrite of a row whose seat prefix differs unless a promoted proposal names it | small adapter on #7 + #4 |
| OPTASKLINK / pre-sailing conference | `mag://warm/preamble/<seat>` (#2) carries the net plan: verbs, restricted list, current intent | reuse |
| Commander's intent + mission orders | new law card `INTENT` in `memory/rib_boot.json`, served via `mag://warm/laws` + `mag://warm/intent` | reuse + 1 URI |
| Command by negation (CWC) | `mag/proposals.py` reject / operator override = the veto; absence of veto within TTL = go | reuse |
| EMCON + restrictive FSCMs | lease store: generalise #10's lease-file slot + #7's heartbeat record into resource leases; `configs/restricted.yaml` lists restrictive assets | small adapter |
| COLREGs give-way / stand-on | lease rule: live holder stands on; newcomer gets a refusal naming holder + expiry; Rule 2 exception = self-defense clause | in lease adapter |
| AIS | revive #11 heartbeat, add fields `on`, `leases`, `status`, `lane`; COP shows "lost contact" after 300 s | reuse + small adapter |
| SPOTREP / SITREP (SALUTE) | `shared_receipt_append` (#3) with body schema `fleet_report.v1` | small adapter |
| Relief of the watch / deck log | RELIEF report kind via #3; latest relief embedded in the preamble; replaces the frozen #21 role | small adapter |
| Notice to Mariners / NAVAREA warnings | NOTICE report kind via #3, in-force list at `mag://warm/notices`; auto-drops a `danger` mark (#6) that does not decay until cancelled | small adapter |
| Stigmergy | fold #5 + #6 into one gradient fed automatically by every report | small adapter |
| Blackboard control / focus of attention | COP's "hottest" section = what to pick next; nightcrew (#18) and mates (#17) read it to pick missions | small adapter |
| BRM closed loop + challenge | every CLAIM returns an ack id (read-back); `review: reject + reason` in #4 = challenge that must be answered | reuse |
| ROE / self-defense | intent card section "ROE": permissive by default; restrictive list; self-defense = any seat may stop a runaway spend or kill a looping process but must file SPOTREP within the same window | reuse (text) |
| Lane status (VTS info service) | re-enable #16; its state appears on COP | reuse (operator toggles task) |
| Mosaic / kill web | nightcrew `lane` field (#18) already lets any carrier take a row; COP lists alternatives when a lane is DOWN | reuse |

---

## 4. PROPOSALS, RANKED BY VALUE / EFFORT

Value: H/M/L for sustained coherence. Effort: S = under a day for one seat, M = 1-3 days.

### P1. Fleet COP board at `mag://warm/cop` - value H, effort S - **small adapter**
One read-only resource every seat pulls at boot through the warm door (and that the preamble embeds
in short form). Fixed sections, each capped:
1. `TIP` - live chain tip (already in warm_surface).
2. `INTENT` - current commander's intent card (P3).
3. `NOTICES IN FORCE` - open hazards (P4), newest first, never truncated.
4. `LEASES` - who holds what restrictive asset, until when (P2).
5. `UNITS` - AIS table from seat_registry heartbeats: seat, lane/model, on, status, last seen; stale > 300 s = LOST CONTACT.
6. `LANES` - lane_supervisor state (UP/FLAKING/DOWN).
7. `HOTTEST` - top 10 pheromone gradient (P6).
8. `LAST RELIEF` - latest RELIEF report (P5).
9. `ROOM TAIL` - last 20 room.jsonl rows that are not routine monitor polls.
Code-is-law hook: `estate_shared_receipt` and the lease tool return the COP's `cop_sha` and refuse a
write whose caller passes a `cop_sha` older than N minutes (seat must have looked before acting).
Win metric: % of receipts that cite a fresh cop_sha.

### P2. Leases = EMCON + restrictive fire-support measures - value H, effort S-M - **small adapter**
- Store: `state/leases/<sha256(resource)>.json`, created with O_EXCL (the instance_guard/verkle shape),
  body = `{resource, seat, purpose, acquired, ttl_s, heartbeat, fence}` (heartbeat record lifted from
  `verkle_knot.lock_record`; `fence` = monotonic counter as in Claim Plane).
- Resources are strings: `file:mag/verkle_knot.py`, `chain:biography`, `proc:mag-sovereign`,
  `proc:lab`, `key:opencode` (name only, never a value).
- `configs/restricted.yaml` = the restrictive list (no-fire areas). Everything not listed is permissive:
  act, then report.
- MCP tools on the warm profile: `estate_lease_claim(resource, purpose, ttl_s)`,
  `estate_lease_release(resource, fence)`, `estate_lease_list()`. Conflict answer is structured
  (MPAC CONFLICT_REPORT shape): holder, purpose, expires, how to request handover.
- COLREGs rule: live holder stands on; newcomer gives way; expired heartbeat (120 s, as verkle) =
  lease breakable, and the break is logged as a room row.
- **Code-is-law enforcement (the important part):** the verkle chain writer and whatever script
  restarts/stops the lab containers call `lease.require(resource, fence)` and refuse without it. This
  is the same move the estate already made with the Mimosa argv gate and the verkle O_EXCL lock:
  structure, not a watcher. (The lab restart entrypoint was not identified in this pass; locate it first.)
- Track-number blocks: chain rows carry their author seat; a rewrite of another seat's row is refused
  unless a promoted proposal (P7) names that row.
Win metric: blind restarts and cross-seat row rewrites per week -> 0; lease refusals logged instead.

### P3. Commander's intent / mission orders card - value H, effort S - **reuse + 1 URI**
One card, operator-owned, changed only through a promoted proposal (P7) or operator edit, served at
`mag://warm/intent` and inside every preamble. Fields (ADP 6-0):
- PURPOSE (why this week matters), KEY TASKS (3-5), END STATE (what done looks like).
- CONSTRAINTS: the restrictive list (P2), spend caps, "NO NEW BUILDS" style rulings (START_BRIEF
  shows the 2026-10-13 foundations-week ruling - that belongs here, not buried in a goal string).
- DECISION RIGHTS (command by negation): inside intent and outside the restrictive list, act without
  asking and report; restrictive assets need a lease; changes to shared structure need a proposal.
- ROE: self-defense clause (any seat may halt a runaway spend/loop, then must SPOTREP).
Win metric: questions-to-operator per day falls while veto count stays low.

### P4. Notice to Mariners channel - value H, effort S - **small adapter**
- Kind `NOTICE` through `shared_receipt_append`; fields: `notice_id`, `category`
  (breach | key_rotation | lane_down | hazard_file | law_change), `affects` (resources), `action_required`,
  `in_force_until` or `until_cancelled`, `cancels` (prior notice id).
- `mag://warm/notices` lists in-force notices only (NAVAREA style); a cancellation is a new notice, never an edit.
- Each NOTICE auto-drops a `danger` pheromone mark on the affected resources that does not decay
  until cancelled (P6).
- Seats acknowledge with a one-line SPOTREP `ack: <notice_id>` (BRM read-back); the COP shows unacked counts.
- First entries to file (by the operator or the seat that found them): the OpenCode breach; the 2 unused
  OpenCode keys (names/locations only, no key material, `action_required: rotate or revoke`).
Win metric: time from discovery to fleet-wide ack.

### P5. Watch turnover (RELIEF) brief - value H, effort S - **small adapter**
- Kind `RELIEF` via `shared_receipt_append`, written by a seat at window end (OPNAVINST 3120.32D order):
  unusual conditions; outstanding orders; leases held (each must be RELEASED or TRANSFERRED - the
  lease tool refuses a RELIEF while the seat holds untransferred leases: structure again); work in
  progress with paths; notices raised; upcoming evolutions; "I stand relieved."
- The next seat's preamble carries the latest RELIEF; its first receipt says "I relieve you" + cop_sha.
- This replaces the role of the frozen `memory/briefs/latest.md` without unfreezing it.
Win metric: % of windows that end with a RELIEF; orphan leases per week.

### P6. One pheromone gradient (stigmergy) - value M-H, effort S - **small adapter**
Fold `tools/pheromone.py` (heat, reinforce, decay, solved) and `mag/swarm_tools.py` marks (kinds) into
one store keyed by item, read by the COP's HOTTEST section:
- **Deposit** automatically from every SPOTREP (`activity` + `location` = item key), not by hand -
  that is why both stores went dormant.
- **Reinforce** only from a *different* seat or lane (independent confirmation, the "triple-arm"
  idea already in pheromone.py); same-seat repeats do not add heat.
- **Decay**: keep the existing 6 h half-life for work trails; `danger` marks from NOTICEs do not
  decay until cancelled; `dead` marks (dead ends) decay slowly (24-48 h) so seats stop re-walking them.
- **Trail strength** = sum of decayed deposits x distinct-seat count; **solved** collapses heat
  and writes evidence path.
- ACO lesson: keep evaporation, so the swarm keeps exploring instead of converging on one stale item.
Win metric: duplicate effort (same item worked by 2+ seats without reinforce) per week.

### P7. Proposals as the only door for shared-structure changes - value M-H, effort S - **reuse**
`mag/proposals.py` already does signed proposals + quorum + operator override + no git. Make it the
required path for: rewriting another seat's chain rows, editing the intent card, editing
`configs/restricted.yaml`, editing law cards. Reject + reason = BRM challenge that must be answered.
Win metric: proposals filed vs silent overwrites.

### P8. SITREP / SPOTREP receipt format `fleet_report.v1` - value H, effort S - **small adapter**
(Listed after P1-P7 only because P4/P5 depend on it; build it first.) Body schema validated inside
`shared_receipt_append` (refuse if required lines are missing):

```
schema: fleet_report.v1
kind: SPOTREP | SITREP | NOTICE | RELIEF | ACK
dtg: 2026-10-17T19:55:00Z          # report time (UTC)
seat: zcode   model: glm-5.3   lane: opencode
cop_sha: <sha of COP read before acting>
# SALUTE lines (SPOTREP)
size: what scope (files / rows / processes / dollars)
activity: what was observed or done (one line)
location: repo paths, process names, URLs (no secrets)
unit: which seat / organ / provider is involved
time: when observed (UTC)
equipment: tools / lanes used
assessment: what it means, confidence
action: taken / recommended
leases: held / released
narrative: free text, capped
```
SITREP adds `status`, `readiness`, `problems`, `recommendations`. ACK carries `ack_of`.

### P9. AIS heartbeat from seat_registry - value M, effort S - **reuse + small adapter**
Revive `mag/seat_registry.py` heartbeat (dormant since 09-26) through one warm-profile tool
`estate_heartbeat(seat, on, status)`; status vocabulary from AIS: underway / at anchor / restricted /
not under command. Cadence like AIS: every few minutes when working, on change, slow when idle.

### P10. Re-enable lane_supervisor - value M, effort S (operator toggle) - **reuse**
The task has been disabled since 09-28 (last result 1). Its state feeds COP `LANES` and gives
nightcrew/mates a failover (mosaic kill-web alternatives) instead of silent lane death.

### P11. Fixed signal book (EXTAC-style verbs) - value M, effort S - **reuse (text)**
Seven verbs used identically on room.jsonl `verb`, receipts `kind`, and MCP tools: CLAIM, RELEASE,
SPOT, SITREP, NOTICE, RELIEF, VETO. Publish as a law card. Keep room.jsonl as the deck log; route
routine monitor polls to their spool so the log stays readable (18k rows today, mostly monitor.lane).

### P12. Room size discipline - value M, effort S - **reuse (rule)**
AgentRoom found quality peaked at 2 agents per shared room and one broadcast channel saturated past 3.
Map: at most 2-3 seats on one restrictive asset or task at once (lease `max_holders`), the rest work
elsewhere on the gradient. mates.yaml already carries the analogous concurrency law (16 / 24 staggered).

### Build order (dependencies)
P8 (format) -> P2 (leases) -> P1 (COP) -> P4 (notices) -> P5 (relief) -> P3 (intent card) -> P6 (gradient)
-> P7 (proposal door) -> P9/P10/P11/P12. P3 and P10 can happen any time (text / toggle).

### What NOT to build
- No new supervisor or watcher process (Lessig: put the rule in the path, not a cop on the corner).
- No new transport: warm MCP door + receipts + room.jsonl cover it.
- No new pheromone or lock module: fold the existing two/three.

---

## 5. WIN CONDITION: SUSTAINED COHERENCE, MEASURED

Track weekly from receipts and room.jsonl (all deterministic, $0):
1. Blind restarts / cross-seat chain rewrites (target 0) vs lease refusals (expected > 0 at first).
2. Notice discovery-to-ack time; unacked notices in force.
3. % receipts in `fleet_report.v1` with a fresh `cop_sha`.
4. % windows ending in RELIEF; orphan leases.
5. Duplicate work without reinforce; hottest-item age.
6. Questions to operator per day vs vetoes per day (mission command working = first falls, second stays low).

---

## 6. SOURCES (all retrieved 2026-10-17)

Naval
- [S1] JP 3-32, Command and Control for Joint Maritime Operations - http://edocs.nps.edu/2012/December/jp3_32.pdf
- [S2] Australian Army Research Centre, "Mission Command at Sea and Command by Veto" - https://researchcentre.army.gov.au/library/australian-army-journal-aaj/mission-command-sea-and-command-veto
- [S3] FAS, "Battlegroup Commanders & the CWC Concept" - https://irp.fas.org/doddir/navy/rfs/part03.htm
- [S4] NWP 3-56 Composite Warfare Doctrine (Sep 2010), copy - https://studylib.net/doc/26041719/nwp-3-56-sep-2010-cwc-1
- [S5] CRS In Focus IF12599, Navy Distributed Maritime Operations - https://www.congress.gov/crs_external_products/IF/PDF/IF12599/IF12599.12.pdf
- [S6] CNO Navigation Plan 2024 - https://www.navy.mil/Portals/1/CNO/NAVPLAN2024/Files/CNO-NAVPLAN-2024.pdf
- [S7] Atlantic Council, Executing distributed operations - https://www.atlanticcouncil.org/in-depth-research-reports/report/executing-distributed-operations-in-an-increasingly-contested-maritime-environment/
- [S8] FM 6-24.8 TADIL J introduction - https://www.globalsecurity.org/military/library/policy/army/fm/6-24-8/tadilj.pdf
- [S9] AFMAN TDL planning and operations (JCS) - https://www.jcs.mil/Portals/36/Documents/Doctrine/training/jid/afman_116tdl_plan_ops.pdf?ver=2020-09-14-144621-023
- [S10] SISO-STD-002-2021 Link 16 - https://cdn.ymaws.com/www.sisostandards.org/resource/resmgr/standards_products/siso-std-002-2021_link_16.pdf
- [S11] Corvus, Link 16 integration and COP track management - https://corvusintell.com/blog/interoperability/link-16-tactical-data-links/
- [S12] ATP-1(D) Vol II Allied Maritime Tactical Signal and Maneuvering Book - https://www.ftc.navy.mi.th/e-books/594.pdf
- [S13] NRTC 14244 ch.5 Allied Flaghoist Procedures - https://www.globalsecurity.org/military/library/policy/navy/nrtc/14244_ch5.pdf
- [S14] NATO Archives, ACP 175 / ATP 1 - https://archives.nato.int/acp-175-allied-naval-signal-book-atp-1-allied-naval-manoeuvring-instructions
- [S15] USNI Proceedings June 2023, "Drill Emission Control as a Main Battery" - https://www.usni.org/magazines/proceedings/2023/june/drill-emission-control-main-battery
- [S16] NRTC 14226 ch.3 Emission Control - https://www.globalsecurity.org/military/library/policy/navy/nrtc/14226_ch3.pdf
- [S17] SWOS EMO course, EMCON bill - https://man.fas.org/dod-101/navy/docs/swos/e1/MOD1LES2.html
- [S18] HyperWar, Anti-Submarine and Escort of Convoy - https://www.ibiblio.org/hyperwar/USN/ref/ASW-Convoy/ASW-Convoy-4.html
- [S19] HyperWar, History of Convoy and Routing ch.III - https://www.ibiblio.org/hyperwar/USN/Admin-Hist/011-Convoy/011-Convoy-3.html
- [S20] NRTC 14243 ch.7 Convoy Communications - https://www.globalsecurity.org/military/library/policy/navy/nrtc/14243_ch7.pdf

Military C2
- [S21] ADP 6-0 Mission Command - https://armypubs.army.mil/epubs/dr_pubs/dr_a/arn47032-adp_6-0-000-web-1.pdf
- [S22] Army University Press, Philosophy of Mission Command - https://www.armyupress.army.mil/Journals/NCO-Journal/Archives/2018/February/Philosophy-of-Mission-Command/
- [S23] Boyd, Patterns of Conflict - http://projectwhitehorse.com/pdfs/boyd/patterns%20of%20conflict.pdf
- [S24] CRS IF11493, Joint All-Domain Command and Control - https://www.everycrsreport.com/files/2020-10-23_IF11493_010f8b4da8bbfc645be3c35b4c65fd6a42b2fcbc.html
- [S25] DARPA STO, Mosaic Warfare vision - https://www.darpa.mil/news/2017/sto-mosaic-warfare
- [S26] Mitchell Institute, Restoring America's Military Competitiveness: Mosaic Warfare - https://www.mitchellaerospacepower.org/restoring-americas-military-competitiveness-mosaic-warfare/
- [S27] CSBA, Mosaic Warfare and decision-centric operations - https://csbaonline.org/research/publications/mosaic-warfare-exploiting-artificial-intelligence-and-autonomous-systems-to-implement-decision-centric-operations/publication/1
- [S28] FM 6-99.2 Report and Message Formats - https://www.globalsecurity.org/military/library/policy/army/fm/6-99-2/fm6-99-2_c1.pdf
- [S29] FM 6-99 - https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN34470-FM_6-99-000-WEB-1.pdf
- [S30] OPNAVINST 3120.32D (relieving the watch, ch.4) - https://www.secnav.navy.mil/doni/Directives/03000%20Naval%20Operations%20and%20Readiness/03-100%20Naval%20Operations%20Support/3120.32D%20W%20CH-1.pdf
- [S31] JP 1-02 DoD Dictionary (ROE definition) - https://jitc.fhu.disa.mil/jitc_dri/pdfs/jp1_02.pdf
- [S32] Operational Law Handbook ch.5 Rules of Engagement - https://sites.duke.edu/lawfire/files/2020/10/ROEOperational-Law-Handbook-2020.pdf
- [S33] MCWP 3-16 App.B Fire Support Coordinating Measures - https://www.globalsecurity.org/military/library/policy/usmc/mcwp/3-16/appb.pdf
- [S34] FM 3-52 ch.4 - https://www.globalsecurity.org/military/library/policy/army/fm/3-52/ch4.htm
- [S35] JP 3-09 Joint Fire Support - https://www.govinfo.gov/content/pkg/GOVPUB-D5-PURL-gpo29331/pdf/GOVPUB-D5-PURL-gpo29331.pdf

Maritime civil
- [S36] USCG Navigation Rules Handbook - https://www.navcen.uscg.gov/sites/default/files/pdf/navRules/Nav%20Rules%20Handbook_27OCT2022_85%20FR%2058268.pdf
- [S37] USCG Navigation Rules FAQ - https://navcen.uscg.gov/navigation-rules-faqs
- [S38] SOLAS V/19 (USCG copy) - https://www.navcen.uscg.gov/sites/default/files/pdf/AIS/SOLAS.V.19.2.1-5.pdf
- [S39] IMO, AIS transponders - https://www.imo.org/en/ourwork/safety/navigation/ais.aspx
- [S40] ITU-R M.1371-5 - https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-5-201402-S!!PDF-E.pdf
- [S41] IMO Resolution A.1158(32) Guidelines for VTS - https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.1158(32).pdf
- [S42] IMO Resolution A.857(20) - https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.857(20).pdf
- [S43] NGA Notice to Mariners (final issue 11/2026, page fetched) - https://msi.nga.mil/NTM
- [S44] NGA Navigational Warnings - https://msi.nga.mil/NavWarnings
- [S45] USCG Marine Safety Information Broadcasts - http://navcen.uscg.gov/marine-safety-information-broadcasts
- [S46] Swedish Club, Bridge Instructions 2024 - https://www.swedishclub.com/uploads/2024/02/TSC-Bridge-Instructions-2024.pdf
- [S47] BRIDGE procedures guide - https://maritimesafetyinnovationlab.org/wp-content/uploads/2020/10/BRIDGE_PROCEDURE_GUIDE_FIFTH_EDITION.pdf
- [S48] OPNAVINST 3100.7C Deck Log - https://www.secnav.navy.mil/doni/Directives/03000%20Naval%20Operations%20and%20Readiness/03-100%20Naval%20Operations%20Support/3100.7C.pdf
- [S49] NHHC, What is a deck log - https://www.history.navy.mil/research/archives/Collections/deck-logs/what-is-a-deck-log.html

Swarm / multi-agent
- [S50] DARPA OFFSET program - https://www.darpa.mil/research/programs/offensive-swarm-enabled-tactics
- [S51] DARPA, OFFSET swarms final field experiment - https://www.darpa.mil/news/2021/offset-swarms-take-flight
- [S52] Theraulaz & Bonabeau, A Brief History of Stigmergy (Artificial Life 1999) - https://doi.org/10.1162/106454699568700
- [S53] Bonabeau et al., Inspiration for optimization from social insect behaviour - https://lia.disi.unibo.it/corsi/2007-2008/SMA-LS/papers/9/bonabeau2000a.pdf
- [S54] Erman et al., The Hearsay-II Speech-Understanding System - https://doi.org/10.1145/356810.356816
- [S55] Nii, Blackboard Systems (Stanford CS-TR-86-1123) - http://i.stanford.edu/pub/cstr/reports/cs/tr/86/1123/CS-TR-86-1123.pdf
- [S56] Cemri et al., Why Do Multi-Agent LLM Systems Fail? - https://arxiv.org/abs/2503.13657
- [S57] Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture - https://arxiv.org/abs/2507.01701
- [S58] LLM-Based Multi-Agent Blackboard System for Information Discovery in Data Science - https://arxiv.org/abs/2510.01285
- [S59] Cho & Lee, AgentRoom: Concurrent Multi-Agent Coding in a CRDT-Backed Shared Workspace - https://arxiv.org/abs/2608.23740
- [S60] Nikolaev, Claim Plane: Enforceable Change Intents and Dynamic Scope for Parallel Coding Agents - https://arxiv.org/abs/2607.21909
- [S61] Qian, Fang, Li, MPAC: A Multi-Principal Agent Coordination Protocol - https://arxiv.org/abs/2604.09744

Caveats: S4 is a third-party copy of NWP 3-56; S11 is a vendor blog; S59-S61 are preprints and two
of them say their samples are small. Search results also surfaced "CoAgent" (arXiv 2606.15376) and
"Multi-agent Collaboration with State Management" (arXiv 2605.20563); not opened, so not relied on.
Lessig's "code is law" (Code and Other Laws of Cyberspace, 1999) is cited from the brief, not re-fetched.
