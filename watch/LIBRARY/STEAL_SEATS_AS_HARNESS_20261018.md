# STEAL - SEATS AS HARNESS (self-steal: is Roster Swap just Mag's harness?) - 2026-10-18

Verb: fleet/self_steal. Seat: Grok Bot executor, Sun 2026-10-18 ~10:10-10:40 ET (UTC-4).
Operator question (Nacho, verbatim): "don't we already have this capability in zcode, isn't this just our harness, can't we just do the shit we do elsewhere here, can't we map the interfaces?"
Companion to: watch/LIBRARY/STEAL_ROSTER_SWAP_20261018.md (same day; this file corrects two of its Unprovens, see Corrections).
Rules kept: $0, no git, no code changes, no paid calls, no process touched, no .env / keys / secret_gate_results/ / free_keys/ / memory/trajectory/steps.jsonl opened. Box store.db files opened READ-ONLY (sqlite mode=ro) for table names, row counts and one kv key (conversationPartners). Writes: this file + one INDEX.md line.

Evidence tiers, never mixed:
- **[BYTES-PC]** read today on DESKTOP-7C70KSC, repo root, path:line.
- **[BYTES-BOX]** read today on the Grok Bot box, /home/box/agent-data/...
- **[REC]** my recommendation. Not built. Operator authorizes.

---

## Verdict (plain)

**Mostly yes.** Roster Swap's verbs (enroll, verify, revoke, hand off, quorum on change, never delete, periodic patrol) all already exist as Mag harness organs. A Grok Bot seat is structurally "one more seat" the same way `mate:cartographer` is. **But not literally "just the harness" today, for three byte-proven reasons:**
1. **Zero Grok Bot seats are registered.** configs/seat_allowlist.json:11-89 holds only 11 `mate:*` GLM rows. The harness cannot revoke, quorum, or lease something it has never enrolled.
2. **The Grok Bot "body" is on the box, not the PC.** Profile, memory, routines, skills, transcripts live under /home/box/agent-data/ (Linux, separate filesystem). No Mag organ reads that tree. Mag's harness touches Grok Bot only through messages it can see (receipts, feeds), not its state.
3. **App-side verbs have no Mag equivalent.** Creating, renaming, pausing a Grok Bot, and toggling a routine's `enabled` are Grok Bot app actions. Mag can record and gate them, not perform them.

ZCode specifically: the ZCode steal (corpus/steal/ZCODE_RATCHET_LANDED_20260924.md:17-22; AGENTS.md:109-123) is **code/workflow discipline** (violation ratchet, workflow gate, spec-before-behavior). It is the *shape* Roster Swap needs for its YES gates and its "register grows only by a named act" law, but it is not a seat lifecycle organ. The lifecycle organs are seat_handshake / seat_allowlist / proposals / leases / fleet_report / leave_dispatcher (all landed 2026-10-17).

So: **roster swap = harness + a thin box-side adapter + a few app clicks.** Not a separate process.

---

## Inventory read today

**[BYTES-BOX] Grok Bot seats** (/home/box/agent-data/agents/<id>/profile.json name; store.db `transcript_entries` row count, read-only; automations/*/automation.json):

| Seat | id (prefix) | memory/ entries | automations | transcript_entries (box store) | audit.jsonl lines |
|---|---|---|---|---|---|
| Grok Bot (primary router) | fa681c21 | none | none | 0 | none |
| mag | 27002d7d | none | none | 0 | none |
| Ghost | 4a30dd44 | 31 | `AFK game chord`, schedule `57 9-19 * * 1-5`, **enabled: False** | 1,133 | 2,926 |
| Research | 3d371c13 | 2 | dir present, empty | 168 | 212 |
| New Bot | 86431fab | none | none | 0 | none |
| Archival Bot | ae78a844 | none | none | 0 | none |
| RefreshBot | d55732f8 | none | none | 0 | none |

- active-agent.json -> 3d371c13 (Research) at read time.
- Skills: /home/box/agent-data/workflows/ holds exactly one skill, `archival/` (SKILL.md + archive_guard.py).
- store.db tables (all seats): `kv, blobs, transcript_entries, automation_completion_inbox`. Transcript = `transcript_entries(seq, id, entry)`.
- SendToAgent trace: Ghost kv `conversationPartners` = ["3d371c13..."] (Research); Research's = ["4a30dd44..."] (Ghost). Only that pair has messaged each other on this box.
- 0 transcript rows for New Bot / Archival Bot / RefreshBot / Grok Bot / mag in the box store. Whether their histories exist server-side only: Unproven.
- Profile fields (all seats): name, description, title, avatarShape, avatarColor, serverId, harness ("temporal"). settings.json: only `notifyOnAgentUpdates`.

**[BYTES-PC] Mag harness organs** (repo C:\Users\foste\Documents\projects\local_sovereign_agent):

| Organ | Key lines | What it is |
|---|---|---|
| configs/seat_allowlist.json | :3 note (revoked:true cuts a seat), :5-9 quorum default 2 + require_non_glm_approval, :10 operator_seats [], :11-89 seats (11 mate:* rows, kind mate, model_family glm) | the seat register (public Ed25519 keys only) |
| mag/seat_handshake.py | :69 SEAT_RE `^(?:mate:)?[A-Za-z0-9][A-Za-z0-9_.-]{0,31}$`, :147 default_key_path (~/.mag_seat/<seat>.key, outside repo), :195-200 seat_public returns None if `revoked`, :304 verify_envelope | signed seat identity for warm MCP doors |
| scripts/seat_keygen.py | :70-87 keygen (exclusive create, refuses in-repo path, never prints seed), :122-150 merge_allowlist (**hardcodes kind "mate", model_family "glm" at :144**) | enroll |
| mag/proposals.py | :1-37 protocol; :25-30 quorum; :32-36 non-GLM rule; :282-286 is_non_glm_seat; :240 submit; :289 tally | seat-to-seat change + quorum, append-only, "a revoked seat's votes stop counting" (:22-23) |
| mag/leases.py | :254 acquire, :292 renew, :307 release, :321 transfer | holder-keeps leases on the restricted list |
| configs/restricted_leases.json | resources: chain:biography, file:mag/verkle_knot.py, proc:lab, file:docker-compose.yml, keys:names, proc:desktop | what takes a lease (no seat/roster resource) |
| mag/fleet_report.py | :13, :45 KINDS = SPOTREP/SITREP/NOTICE/RELIEF/ACK; :197 file_report; :252 notices | RELIEF = "I stand relieved" watch turnover |
| mag/auto_handoff.py | :77 run() -> memory/handoffs/latest.md; state memory/handoff_state.json (exists) | handoff assembly |
| mag/peer_handoff.py | :37 file_peer_handoff -> queue/handoff/peer-*.json | seat-to-seat instructions on disk |
| tools/leave_dispatcher.py | :60 RUNNER_ARGV constant; :142 write_missions; :183 harness_probe enabled gate | daily mate wave driver |
| scripts/register_leave_task.ps1 | :37 MagLeaveProtocolDaily, :60 /SC DAILY /ST 08:00 | the cron |
| configs/mates.yaml | :33-127 mates (8 personas); :141-167 harness_probe enabled:false + 3 roles | persona/routine manifest |
| mag/harness_probe.py | :142 mate_seat, :146 mate_key_path, :396 file_verdict_proposal, :406 file_review | signs host-side for mates; proposes harness deltas |
| mag/warm_surface.py | :59 SEATS = grok, gemini, deepseek, zcode, hermes, codex, cursor, claude, free; :297 preamble(seat) raises on unknown seat | shared warm boot surface (fixed seat set) |
| mag/rib_bus.py | :140 publish_rib, :185 mount, :193 inject_for | RIB instruction layer on the verkle bus |
| mag/skill_seat.py | :13 SKILL_WEAVES (ponytail, caveman -> docs/ref/weaves/) | skill-as-agent-mode |
| mag/seat_registry.py | :26-38 _SEAT_PLATFORM incl. `grok_bot: grok-desktop`, `chatgpt_bot`, `cursor`; :63 register, :98 heartbeat, :120 unregister | external-seat liveness registry (orchestrator mesh, heartbeat, reap at 300 s :24) |
| mag/seats.py | :211-270 inbound seats (cursor, grok_tui via watch/*_feed.jsonl) | Body-tab view of seats |
| mag/seat_steer.py | :43-45 SURFACE_DRIVERS chatgpt/grok -> chatgpt_bot/grok_bot | send a message into an external seat |
| mag/grok_bot.py | :1-4, :35 SEAT = "grok-bot" | **the Aug-2026 "Ghost desktop" SuperGrok front-end driver via browser**, not the box Grok Bot agents (name collision, see Surprises) |
| tools/backup_brain.py | :103 inventory() EXISTS/MISSING + age | organ inventory |
| tools/census_drift_patrol.py | :333 run(), exit 0/1/2 contract | freshness tripwire pattern |
| tools/violation_ratchet.py | :241 check, :284 baseline-update --by, :319 prune | register grows only by named act |
| tools/workflow_gate.py | :684 main; registers every check row in memory/workflows/REGISTRY.jsonl (AGENTS.md:119) | gate-before-submit |

Not present: `skills\` folder at repo root; tools/leave_protocol.py (still cited by configs/mates.yaml:2; same drift STEAL_ROSTER_SWAP flagged).

---

## INTERFACE MAP

Grok Bot concept [BYTES-BOX] -> Mag harness organ [BYTES-PC] -> verdict. EXISTS = organ does this job for a seat today; PARTIAL = right organ, needs a row/field/adapter; MISSING = no organ.

| Grok Bot concept | Where it lives (box) | Mag harness organ | Verdict | Gap in one line |
|---|---|---|---|---|
| **Agent / seat identity** | agents/<uuid>/profile.json (name, serverId) | configs/seat_allowlist.json:11 seats + seat_handshake.py:195 seat_public + seat_keygen.py:70 | **PARTIAL** | organ exists; zero Grok Bot rows; SEAT_RE (:69) forbids colons except `mate:`, so ids must be like `grokbot-ghost`, not `grokbot:ghost` |
| Seat liveness / presence | (none on disk besides audit.jsonl, store mtime) | seat_registry.py:63/98/120 register/heartbeat/unregister (has `grok_bot` platform :31) | **PARTIAL** | platform slot exists but means the old desktop driver; no heartbeat source from box agents |
| **Profile** (name, description, persona) | profile.json + memory/profile.md | configs/mates.yaml mates[].persona/hunting_ground (:33-127); warm_surface.preamble(seat) :297 | **PARTIAL** | persona manifest shape exists for mates; Grok Bot profiles are not mirrored; warm SEATS (:59) is a fixed tuple without grokbot |
| **Memory** | agents/<id>/memory/ (profile.md, log/, notes) | warm_surface mag://warm/* (tip, state, zknot, laws); rib_bus.mount :185; memory/handoffs | **PARTIAL** | Mag has shared memory a Grok Bot seat can READ via warm MCP if enrolled; per-seat Grok Bot memory is not mirrored or archived by any Mag organ |
| **Routine** (automation) | automations/<slug>/automation.json {name, prompt, schedule cron, enabled, provenance, lastRunAt} + runs.json | leave_dispatcher.py:142 mission files + register_leave_task.ps1:60 schtasks + mates.yaml `enabled` (:142) | **PARTIAL** | same shape (prompt + schedule + enabled flag); but box routines run in the Grok Bot app scheduler, Mag's run on Windows schtasks. Mapping = record, not execute |
| **Skill** | /home/box/agent-data/workflows/<name>/SKILL.md (+ scripts) | rib_bus.publish_rib :140 / memory/rib_boot.json (exists); skill_seat.py:13 SKILL_WEAVES; warm laws mag://warm/laws | **PARTIAL** | skill == RIB in shape (instruction layer for a flock); no sync either direction; archival SKILL.md is not on the bus |
| **Transcript** | store.db transcript_entries (Ghost 1,133, Research 168, others 0) + /workspace/transcripts-export/*.md | archive_guard.py manifest/verify (box skill); backup_chain.py verify; seat_corpus.py / corpus oral_history (cited by mates.yaml:39) | **PARTIAL** | verify/never-delete organs exist; export from store.db or app is outside Mag |
| **SendToAgent message** | kv conversationPartners (Ghost<->Research only) | proposals.py (signed proposal/review), peer_handoff.py:37, fleet_report.py NOTICE/ACK, seat_steer.py send | **PARTIAL** | Mag messages are signed + receipted; Grok Bot SendToAgent is unsigned and box-internal; no bridge writes it to watch/receipts |
| **Handoff / primary-role transfer** | Grok Bot profile description ("routes to the right bot") | fleet_report RELIEF (:13,:45, stand_relieved=true), auto_handoff.run :77, leases.transfer :321 | **EXISTS** (organ) | needs only the seat to be enrolled so its RELIEF receipt validates |
| **Change approval / YES gate** | owner YES in chat (approval cards) | proposals.py quorum (:25-36), operator_seats override (:27), workflow_gate / violation_ratchet "named act" law | **EXISTS** (organ) | operator_seats is empty (:10); the YES gate maps to an operator-seat approve |
| **Retire** | app-side delete/rename (no disk flag) | seat_allowlist `"revoked": true` (:3) enforced seat_handshake.py:197 and proposals tally (:22-23); seat_registry.unregister :120 | **PARTIAL** | revoke switch exists; nothing to revoke until enrolled; the app-side retirement is not mirrored |
| **Rename / label** | profile.json name/title (app writes) | none (allowlist rows have `note`, not a label lifecycle) | **MISSING** | label "RETIRED-<date>" lives only in app; Mag could hold it as a row `note` + `retired` date [REC] |
| **Roster census / bloat check** | (none) | backup_brain.inventory :103 pattern, census_drift_patrol :333 exit 0/1/2 pattern | **MISSING** (as a roster metric) | pattern exists, no roster-size meter |
| **Lease on shared resource** | (none; box seats share one machine) | leases.py + restricted_leases.json | **EXISTS** (organ) | no roster resource on the restricted list; would need e.g. `roster:grokbot` [REC] if two seats ever swap concurrently |

Highlights:
- **Every Grok Bot concept has a Mag organ of the right shape. None has a row.** That is the whole gap.
- Two shapes match almost field for field: Grok Bot `automation.json {prompt, schedule, enabled}` vs mates.yaml mission + schtasks + `enabled`; and Grok Bot `SKILL.md` vs RIB instruction cards.
- Revocation is free once enrolled: one `"revoked": true` flips handshake (:197) and quorum (:22-23) together.

---

## Roster Swap steps mapped onto the harness

| Roster Swap step | Harness organ that already does it | What's missing |
|---|---|---|
| 0. Inventory | backup_brain.inventory (:103) pattern; seat_allowlist seats list | a roster census that reads box agents/ (the table above was done by hand) |
| 1. Archive history | archive_guard.py manifest (box skill); corpus oral_history shelf | export from store.db / app (app-side or read-only sqlite dump) |
| 2. Verify | archive_guard.py verify + confirm; backup_chain verify | none (do not use `gate` on transcripts: PROTECTED regex, per STEAL_ROSTER_SWAP Surprise 1) |
| 3. YES gate | proposals.py: propose "retire grokbot-research" -> operator-seat approve marks ready (:27) | operator_seats empty (:10); YES today lives in chat, not a receipt |
| 4. Fresh copies | seat_keygen.py --seat (enroll new seat), merge row | creating the bot itself = app action |
| 5. Restore only enabled routines | mates.yaml `enabled` + leave_dispatcher pattern | routines run in the Grok Bot scheduler; Mag only records them. Box shows only one routine (Ghost AFK game chord) and it is **disabled**, so for this swap the restore set is **empty** [BYTES-BOX] |
| 6. Label / retire old bots | `"revoked": true` + row note; seat_registry.unregister | rename = app action |
| 7. Hand off primary role | fleet_report RELIEF + auto_handoff + leases.transfer | none once enrolled |
| Never deletes | proposals append-only exclusive-create (:12); archive_guard; seat_keygen never overwrites (:79-82) | backup_chain rmtree exception (STEAL_ROSTER_SWAP Surprise 4) |
| Monthly bloat check | census_drift_patrol exit 0/1/2 pattern | roster meter |

---

## Answer: is roster swap just the harness?

**Yes in shape, no in wiring.** The lifecycle verbs are Mag's: enroll (seat_keygen), identity (seat_handshake), retire (revoked:true), relieve (fleet_report RELIEF), hand off (auto_handoff / leases.transfer), approve (proposals quorum / operator seat), never delete (append-only receipts), patrol (census pattern). A separate "Roster Swap process" would duplicate them. What makes it not-yet-the-harness is that Grok Bot seats were never enrolled and their bodies live on the box where no Mag organ reads.

## Smallest adapter [REC, report only, no code]

1. **Enroll each kept Grok Bot seat as a Mag seat.** One allowlist row each, ids without colons (SEAT_RE :69): `grokbot-grok` (primary router), `grokbot-mag`, `grokbot-ghost` if kept. Row: `{public_hex, added, kind: "grokbot", model_family: "grokbot", box_agent_id: "<uuid>", note}`. Key minted by `scripts/seat_keygen.py --seat grokbot-<name>` on the machine that will sign (box: ~/.mag_seat, outside any repo; or host-side signing like mates, harness_probe.py:142-146). The `--mates --write-allowlist` path hardcodes kind mate / glm (:144), so for now the operator pastes the printed row by hand (the documented flow, allowlist :3). No code needed.
2. **Retire = row with `"revoked": true` + `retired: "2026-10-18"` + `archive_receipt: <path to archive_guard result.json>`.** For retirees that were never enrolled (Research, New Bot, Archival Bot, RefreshBot) the honest minimal record is a revoked row with no key (or a NOTICE receipt via fleet_report) so the roster has a tombstone. A revoked row with no valid key is inert: seat_public returns None either way (:197-200).
3. **Routines = recorded, not run, by Mag.** Mirror each box automation.json (name, schedule, enabled) into the archive/ROUTINES.md; restore only `enabled: true`. Leave the Grok Bot scheduler as executor. Do not port to leave_dispatcher (Windows schtasks cannot reach the box agents).
4. **Skills = RIBs.** Publish each box SKILL.md's hard rules via rib_bus.publish_rib (domain e.g. `archival`) so Mag-side seats get the same law; keep the SKILL.md as the box copy.
5. **YES gate = proposal + operator-seat approve.** Retire/enroll filed as a proposals.py proposal; Nacho's own seat added to `operator_seats` (:10) makes his approve the YES. Optional; chat YES + archive receipt is acceptable for v0.
6. **Handoff = one fleet_report RELIEF** from the outgoing primary (stand_relieved=true).
7. **Bloat check = read-only roster census** (box agents/ dirs + allowlist rows + revoked count), census_drift_patrol exit contract. Already recommended in STEAL_ROSTER_SWAP; here it doubles as the drift check "box seat exists but has no allowlist row".

Power note for the operator [REC]: proposals.is_non_glm_seat (:282-286) treats any non-`mate:` seat whose model_family lacks "glm" as non-GLM. An enrolled `grokbot-*` seat would therefore satisfy `require_non_glm_approval` and could co-adopt mate harness changes. Decide that deliberately; set operator_seats explicitly rather than by accident.

---

## Surprises

1. **Name collision.** mag/grok_bot.py (:1-4, :35 SEAT="grok-bot") and seat_registry `_SEAT_PLATFORM["grok_bot"] = "grok-desktop"` (:31) mean the **August SuperGrok browser front-end called "Ghost/grok bot"**, steered via browser_driver, not today's box Grok Bot agents. Any adapter should use a distinct id family (`grokbot-*`) and kind, or the two will be confused in seats.py / seat_steer.
2. **SEAT_RE forbids `grokbot:` ids** (:69 allows only the `mate:` prefix). The adapter must use hyphen ids, or a code change to the regex (not recommended for v0).
3. **The only box routine is already off.** Ghost `AFK game chord` enabled: False. "Restore only enabled routines" restores nothing for this swap.
4. **4 of 7 box seats have no local transcript rows** (New Bot, Archival Bot, RefreshBot, Grok Bot, mag show 0). Their archive step may be trivially empty or server-side only. Unproven which.
5. **Warm surface seat set is closed.** warm_surface.SEATS (:59) has no grokbot entry and preamble() raises on unknown seats (:299). Enrolling a Grok Bot seat for warm MCP needs either reuse of the `grok` or `free` preamble or a code change.

## Corrections to STEAL_ROSTER_SWAP_20261018.md

- Its inventory said routine enabled state was "NOT readable this way, Unproven". **Wrong: automation.json carries `enabled`** (Ghost AFK game chord = False) [BYTES-BOX].
- Its inventory omitted that store.db holds transcripts (`transcript_entries`); counts above.

---

## Receipt

- Artifact: watch/LIBRARY/STEAL_SEATS_AS_HARNESS_20261018.md + one INDEX.md line.
- Tri-state: organ lines = Supported (bytes, today). Server-side history for 0-row seats = Unproven. Adapter = Recommendation, not built.
- Falsifiable by: a `grokbot-*` row appearing in seat_allowlist.json; a Mag organ found reading /home/box/agent-data; a box automation with enabled:true.
- Cost: $0. No git, no code changes, no paid calls, no secrets opened, no process touched.
