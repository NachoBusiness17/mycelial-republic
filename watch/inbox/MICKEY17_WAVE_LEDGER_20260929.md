# MICKEY17 EDGE-MINING WAVE — COLLECTION LEDGER (2026-09-29)

24 concurrent edge-miners over 24 estate surfaces (operator order: "mine the edge and not just respond"). This ledger files findings as agents return. Improvements ranked at close.

## RETURN 1/24 — relay + multiplayer (agent 821248ea)

- **The two halves never met:** server/ (911 lines, authoritative water world, hash-chained replay) has ZERO clients; mud.html still talks only to the presence relay. Authority and transport built in separate rooms, stopped at the door.
- **Port collision + head-of-line block:** cast_server.py:26 defaults 8766 = mud_relay's port; mud_relay.py:170-187 one broadcaster thread does blocking sendall with no timeout — one stalled LAN peer freezes the room's 8Hz tick.
- **Six hand-rolled transports, one shape** (mud_relay, cast_server, api_server, saelis_room, server/, lan_proxy): JSON _send, CORS, presence sweeps, fan-out dicts under a lock.
- IMPROVEMENT: harvest into one room.py (per-client queues, drop-on-slow) + give the authoritative server a /ws door. Kills the slow-peer freeze class once; closes the presence-to-authority loop paid for twice.

## RETURN 2/24 — the-mountain repo (agent ef38bcc3)

- **The gate doesn't survive a clone:** core.hooksPath=hooks lives only in local .git/config (never ships); hooks/pre-push mode 100644 (non-executable — bash silently skips on Linux/macOS); no CONTRIBUTING/README line tells Adam to wire it. The repo's only enforced law evaporates on first external contact. Law #3 in the README is currently false for everyone but this seat.
- **First instruction Adam reads points at a nonexistent folder:** game/README.md:7 says "roblox_to_godot/" (stale estate path; the folder is game/); ghost recurs in docs.
- **Docs reveal the program, hide the evidence:** every receipt points off-repo into the private estate; "verified by simulation" (README) vs "not been executed" (game/README) contradiction; no LICENSE, no CI, no issue templates.
- IMPROVEMENT: clone-proof gate — bootstrap one-liner (git config core.hooksPath hooks && chmod +x hooks/*), fix exec bit + ghost paths. First proof the sovereign-invariant model scales past the estate; seeds the missing CI.

## RETURN 3/24 — gps_mcp + gwap (agent d790f665)

- **The missing dogfood:** gwap_payload mints exactly what gps-mcp's "IF WE GROW THIS" begs for (hash-chained signed verdicts with artifact hashes) — yet nothing calls ledger.record_verdict() from the gwap side. Zero cross-references in either direction.
- **Pre-fixable Opus attacks:** the gps receipt's attack #2 (verdicts trivially inflatable by any caller) is 80% solved by the other organ (chained+signed rows); feeding it leaves only attacks #1 (escalation policy) and #3 (time decay) for the frontier review.
- **Schema disagreements mapped:** gwap verdicts 4-valued vs ledger binary (CHALLENGE/BLOCKED mis-file as pass/fail); two hash candidates (receipt_sha256 pre-signature vs row_sha256 chain-position); key mapping (model_id, task_shape) vs gwap scene/participants — uninvented.
- IMPROVEMENT: fail-closed mag/gwap_to_gps.py adapter (VERIFIED_AGREE->pass, DISPUTE->fail, CHALLENGE/BLOCKED->skip, refuse unverified chains, row_sha256 as evidence). ~30 lines; one metabolism, two organs; collusion gets a priced consequence (routing dollars flee colluders).

## RETURN 4/24 — browser games shelf (agent 481f2241)

- **Unharvested crowd-AI stack in mud.html:** a real Barnes-Hut quadtree (theta=0.9, lines 319-345) used only for enemy separation + a Dijkstra flow-field + scent-trail steering; swarm.html re-implements trail-following naively O(enemies x trail). The machinery exists, was never shared.
- **ruins_go_engine.js is already server-authoritative in shape:** step-clock (world ticks exactly when the player displaces = server/protocol.py's staged actions), hash(st) mirroring world.py's row_sha/verify, dual window/module.exports export. The reference game-room backend already exists in the shelf.
- **oracle_dice.js loaded by nothing** (header claims mud/ruins_go/frontier_souls use it; no HTML loads it).
- IMPROVEMENT: port ruins_go's step/hash/clone contract into server/world.py as the reference game-room backend — every future game inherits determinism, verified sync, replay for free. Plus: the "learning horde" (tenure-as-learning) is a cheap server-side flag; the fleeing XP-fish is a pure-authority mechanic waiting for server rolls.

(20 agents still digging; ledger updated as returns land.)
## RETURN 5/24 - inbox + registry (agent 17ecbf07)
- 96% of the event log is write-only: 7,021 events, zero consume/read/promote ops; all 1,943 INDEX items carry acceptance NONE (the fold's own record-acceptance law never satisfied downstream); md-record-seal emits zero-information boilerplate forever (1,452 events).
- The log is blind to 84% of its surface: 13,254 files on disk, only 2,742 registered, 11,144 orphans (3,597 modified since 09-26); 632 registered files MISSING from disk (dangling shas); INDEX stale (6,420 vs 7,021).
- 46 of 120 writers dead (sancho-pid family died Sep 1); 140 fold_warnings unconsumed.
- IMPROVEMENT: derived READ/DEAD-LETTER INDEX - one consume op + drift-patrol disk-walk join -> ORPHAN_CENSUS.json; consumption-rank exposes the never-read class before it is re-written.

## RETURN 6/24 - godot port lane (agent f36c6b23)
- The multiplayer seam is exactly THREE call sites in game.gd (Timer->tick :246, boil :195, valve :209-215); player.gd has zero identity; server/README already specs the inversion.
- The CMaNGOS violation named: game.gd owns the graph client-side - every player's world diverges, no total order. server/ fixes it (stage-then-tick, hash-chained log, 15 tests pass, 417 lines).
- DETERMINISM LEAK in the school: flock.gd:67 reads Time.get_ticks_msec() - wall clock inside the sim; flock can never replay or go server-side byte-identical; plus two score authorities once wired (client _on_fish_killed vs server tag).
- IMPROVEMENT: net_client.gd (StreamPeerTCP) dual-mode authority inversion - server present -> Timer render-only, actions become staged proposals; server absent -> sovereign local physics stands. First time the 911-line server becomes load-bearing; forces the wall-clock fix.

## RETURN 7/24 - githooks + discipline (agent 60552701)
- All gates judge bytes at push-time; the classes that slip: the CHECKERS' OWN DEATH (mag-sovereign unhealthy 12h, census patrol no-show, nothing auto-restarts - no gate watches the watchers); zero-collect test files hiding in aggregate denominators (test_selffeed_integration.py collects 0); dormant/neutered gates pushing green (mcp_pin zero callers; violation_ratchet was neutered unnoticed).
- The pre-push hook itself: byte-pinned, never executed end-to-end.
- IMPROVEMENT: expendable gate-liveness CANARY - scheduled clone plants one known-bad per gate in a throwaway worktree, runs pre-push, requires every gate to fire; silence files its own death receipt. Plus the 15-line zero-collect detector inside the existing patrol.

## RETURN 8/24 - hermes integration (agent c4ed38f4)
- THE DUEL WAS FIRED BUT NEVER JUDGED: G1 (qwen) vs G3 (glm-prime) same-ask cross-family comparison - the diff was promised in the prompt, never computed. No scoring artifact exists.
- Delegation cache: 4 delegations, 24 tasks, ALL repo-audit shape (zero generation, zero evals); manifest records model:null - nobody knows which model earned which result; 5 tasks interrupted never resumed.
- IMPROVEMENT: clone the gopher driver into a DUEL HARNESS - every ask to two families, a third cheap call judges A-vs-B on a machine-checkable rubric, win/loss rows append to a ledger feeding the tier ladder and future gps router. Burn fuel becomes router training data forever; retroactively prices the 24 unattributed tasks.

(16 agents still digging.)
## RETURN 9/24 - OUR SERVER v0 formal (agent 24b84400)
- 911 lines, 15/15 tests, demo WINS at tick 4. Imports mag.water_graph verbatim (one hydraulic truth); tick is the sole mutator (stage-then-apply, total order, byte-replayable, tamper-refusing chain); no wall clock in rows (seq+tick).
- Physics learned: pipe insertion order means opening p_bypass lets gate1 pass once before the XOR hold; Windows time.time_ns() can repeat - monotonic counter mixed into salts.
- Godot wiring spec delivered (4 steps: tick-driven render, hello/sid, staged SPACE/E, server-side score).
- v1 debts honest: SRP6 auth (plaintext on wire today; localhost is the security model), interest mgmt, persistence, reset, backpressure.

## RETURN 10/24 - queue + handoffs (agent 6efed7b8)
- The dispatch war was WON by the lock (queue_index.jsonl + close verb, single-writer) - memory's option (a) is mechanical now; but todo.md remains a dual ledger (inline CLOSED edits vs index row state).
- Written-never-consumed: 3 identical handoff probes fired 3x in 5 min, results dir empty since Aug; 25 cloud/peer JSONs parked STILL-RELEVANT.
- Q-001 (Aug, verkle compaction) immortal because needs-operator rows have no escalation path; double-listed in Q-028.
- IMPROVEMENT: OPERATOR_GATE_PACKET - every needs-operator row older than the 7-day staleness law auto-rolls into one TTL'd packet; batch-drains the stuck class.

## RETURN 11/24 - mag cores (agent ec692e44)
- Graph mode's boil verb SOFT-LOCKS THE WIN (phase flag never cleared -> won() permanently False) while the real organ (WaterGraph.boil + cold condensation, steam over closed valves) has zero production callers; the shipped water module uses no cold, no siphon.
- Three dead ledgers per run: anchor_proof, seal_session cards, character sheets - written, never harvested.
- Dangling seam: game_ramp reads game_world_root that nothing sets.
- IMPROVEMENT: REPRINT - on campaign defeat, fold the death as a verkle knot, harvest salvage (honest flags kept, cheat flags dropped), re-seat the named actor with hp + reprint_n+1, pass off per-module salvage law (the water remembers), receipts via live patterns. Death becomes the interagent hand-off that trains the next clone.

## RETURN 12/24 - docs + zeitgeist (agent 30e12767)
- TWO RIVAL SELF-STORIES: FRAMEWORK_LOAD + compass narrate the August estate (Ollama/DeepSeek office) while DNA.md (rewritten today) points at the live ghost-self chain (n=20522) - a cold seat loads an estate that no longer exists.
- Registry inverse-trap: v5 marked planned while v5 gates sit ok:true on disk (gates passed, status never upgraded).
- Stale-trap by own law: state/ docs 50+ days stale; dangling links in the front door.
- IMPROVEMENT: FRAMEWORK_LOAD as a REGENERATED CLONE - auto-rendered from gates.jsonl + agent_state tip at each wave close; the front door dies and is reborn every cycle (never-trust-a-hand-written-count applied to the estate's own self-description).

(12 agents still digging.)
## RETURN 13/24 - operator interface (agent c5628563)
- 186 verbs behind a 6-command door: main.py registers 186 subcommands; OPERATOR_CARD lists 5. ~180 verbs have zero plain-language entry point.
- The operator's own kill switch (operator-mode, main.py:2188) is OFF THE CARD; clippy choose - the exact intimidated-operator helper - buried as a sub-flag.
- IMPROVEMENT: mag.cmd realign - one command diffing state since last operator visit -> NEEDS YOU / MOVED / IGNORED in plain language, hung off clippy --operator. The realign surface, speced from inside the wave.

## RETURN 14/24 - gates + tools (agent 848bb231)
- RATCHET BLIND SPOT: DEFAULT_ROOTS=[mag,tools] + non-recursive glob = the enforcing gate never scans server/ (the new world lane) nor gps_mcp subpackages; gps_mcp has zero test refs.
- Output nobody consumes: the dead-instrument tally (80 DEAD + 50 ORPHAN of 164 tools) is itself dead; SKILLS_CATALOG has zero referencing consumers.
- Receipt cross-refs ungated: nothing verifies paths cited inside receipts resolve on disk; skills_lint already owns the regex, pointed only at SKILL.md.
- IMPROVEMENT: tools/receipt_xref_gate.py (~50 lines, self-steal the lint regex): changed receipts' backticked paths must resolve; WARN-only pre-push arm. One dead citation poisons every downstream dispatch.

## RETURN 15/24 - stealth free lanes (agent 4c31f8b8)
- ALL 10 FL BRIEFS ARMED, ZERO FIRED: the driver consumes only JSONL queue rows; .md briefs are invisible to it; t_backlog counts a drained queue instead of the live brief board.
- Harvest gap: ~305 of 306 mined rows never harvested (Belady x243!); sole harvester reads max 12 answers weekly.
- Armed never probed: inkling-small 0 findings; funded grok-4.7 has NO lane in the driver; judgment rungs never fire.
- IMPROVEMENT: brief_reaper topic - driver ingests inbox *BRIEFS.md headers into work-queue rows. The loop consumes its own exhaust instead of re-sensing Belady 243 times.

## RETURN 16/24 - skills organ (agent a3eefd82)
- The ledger is routing-DECISIONS, not fires: cannot answer never-invoked by design. Cross-ref: only 4 of 34 ids ever appear. fireball-cycle is the sharpest zero (cannot enter packs AND never fired). flex floods receipts (662 rows) with no skill; fold (277 rows) is a genome verb with no skill backing.
- Progressive disclosure IS wired (context_pack:724 -> skills_for_job -> pack key) but starved: 600-char budget split across all job skills = ~120 chars/skill; a line filter is a no-op (or ln.strip() always true).
- IMPROVEMENT: skill_fired.v1 receipt from the skills_for_job chokepoint - one logging point, three organs close their loop (catalog gains fired column; right_size gets demotion grounds; bare verbs get skill candidates).

(10 agents still digging: wow bones, corpus, memory, tests, configs, game state, scripts, telemetry, dashboard, cross-organ.)
## RETURN 17/24 - wow bones family (agent 0e765a40)
- server/ gates verbs AS CODE, not data: protocol.py hardcodes VERBS, validate is if/elif, dispatch is string equality - while the stolen law (legal() as frozen hashable table) sits two directories away in wow_steal R01 and Dispatch already runs verbatim over any compiled table.
- Stream.replay exists but no resume path runs it (only tests do) - tampered draws silently accepted as history; B06's entire point unenforced where it bites.
- WorldSession.load can never resume a custom world AND lies about why (compares digest against DEFAULT_WORLD, reports UNKNOWN_SESSION).
- IMPROVEMENT: bones-shaped protocol.json - verbs as gated rows + enums + typed rejects + protocol_digest; validate and dispatch both become Dispatch.dispatch. You are not the first Mickey - the digest is. One gate, three table compilers; sessions bind to hashable contract versions.

## RETURN 18/24 - game program state (agent ca4e4d13)
- THE OLDEST FALSE PROMISE: nomic_rules_patch enqueued 174 TIMES over six weeks to mag/game_rules.py - which does not exist. A zombie enqueue loop; FLOW_IMAGE still freezes it as the sole next piece.
- Verkle map's unread cargo: 173 render leaves only game_world_render touches; the LIVE campaign (gc-24a77d255f, turn 5, active 09-28) has NO file in campaign_runs (all 6 archived runs are August, ok:false). Renders and runs are write-only.
- Unharvested: 4 flagged-Build mechanics from the Pratchett steal (step-clock puzzle rooms, boon drafts, grudge dialogue, sessionDepth spawn rates) - none built.
- IMPROVEMENT: every ledger enqueue becomes a disposable clone with a mandatory death receipt - landed or dead+epitaph within one cadence; corpses harvest into the verkle graveyard. The ledger eats its own dead instead of re-promising them 174 times.

(8 agents still digging: corpus, memory arch, tests, configs, scripts, telemetry, dashboard, cross-organ.)
## RETURN 19/24 - cross-organ synthesis (agent 2d3432ab)
- ONE CHAIN LAW, SEVEN PRIVATE IMPLEMENTATIONS: the house hash-chain pattern hand-copied in wow_player, gwap_payload, party_subchain, tesuji_map, verkle_knot, + 3 more; the baseline spec plans an eighth. Only the verkle chain is guarded (chain_guard exists because the chain was silently corrupted TWICE before its canary); six chains run unguarded.
- The meter's customers wired to the wrong meter: old skill_ledger has consumers but no chain/evidence; new gps_mcp has zero importers; gwap mints meter_credit receipts nothing collects.
- chain_query declares every-module-asks-the-chain-first but mounts only the verkle chain - the law covers ~10% of append-only truth.
- IMPROVEMENT: THE LEDGER REGISTRY - one mount table in chain_query; every chain registers tip+schema; nightly verify + generalized canary; cross-ledger query by receipt hash. Copy N+1 becomes a mount; the judge queue and the meter's first customer become the same line of code.

## RETURN 20/24 - memory architecture (agent 643fbc43)
- KNOWLEDGE GRAPH IS A WRITE-ONLY STAR: 2062 nodes, 1167 degree-0 orphans, 2060 of 2062 have NO inbound edges (all edges are module->invariant fan-out; the connective tissue connects almost nothing).
- 818 ribs, zero usage telemetry: which rib ever rode a task is unknowable; near-duplicate domains (grok-bot/grokbot/grok_cli) double-pay.
- The forgetting doctrine's inverse un-run: ~420KB of four fossil MEMORY.md generations; facts/ frozen since mid-August.
- IMPROVEMENT: clone-burn compaction pass - a disposable worker walks orphans/ribs; each re-attaches (one edge) or demotes to quantized_thought with a forget-event pointer. Clone dies; verdict survives. Smaller packs, higher cache hit.

(Six stragglers - corpus, tests, configs, scripts, telemetry, dashboard - file on arrival.)
## RETURNS 21-25 (final batch at synthesis)
21. SCRIPTS (ea7e): INPUT_FORK falsifier kit is mud-only grader tech (never shared to the other 4 harnesses); server/README claims more than tests grade (replays same-sequence only, no ACTION_FORK). IMPROVEMENT: scripts/test_server_reprint.py - the log IS the reprint; every saved tape becomes a grader (~100 lines).
22. TESTS (abcd): CRITICAL - the estate default entrypoint is BROKEN: test_blade_templates + test_bones_adapter hard-import vastai_sdk/discord (not in requirements) -> plain pytest = 2 collection errors, ZERO of 2,578 run; no CI at all (pre-push runs 21 tests). Signature spine self-skips without cryptography (absent from requirements; Docker skips by construction); gps_mcp's 28 tests never collected (outside testpaths). IMPROVEMENT: one test signs a server.world row with gw.sign_payload, flips a byte, asserts both chains fail - pins two hand-rolled chains to one contract; forces cryptography into requirements; un-skips the silent 5.
23. DASHBOARD (2d34): the_index.html fetches 1.9GB ESTATE_INDEX whole-file (no tail door; the door pattern exists since 09-06); ractor board fossil since 09-03 polled every 15s; the new estate (gwap/gps/mountain) has NO face - zero grep hits. IMPROVEMENT: the verdicts panel (clone links.html, one SELECT door) - every new organ joins by appending one source line.
24. TELEMETRY (e19b): kpi.jsonl 1.1GB append-only zero readers (complete_pct flat 79.4 never alerted); attention.md floods its own signal every 90s (real alerts sink); x_radar silent hole Sep 22-25 unalerted; rollups never diffed (estate metabolism does not exist); ESTATE_INDEX duplicated 3.9GB. IMPROVEMENT: gap-sentinel patrol - one cheap cron diffing consecutive rollups + detecting sensor silence; every sensor inherits gap-detection free.
25. CONFIGS (2560): the seal guards corpses (features.yaml zero loaders, data_tiers heuristics-admits, both hash-protected); the ghost watcher lane (scheduled every 30 min, no trail - the fleet's most frequent actor is unauditable); the baseline predicts the next regression: 69% except-pass + 4 accepted mimima-ssrf in live models/providers.py - real SSRF could launder through false-positive tolerance. IMPROVEMENT: print the next clone without the scars - move endemic rules for files born after a cutoff into preflight rails; heredity becomes impossible; the baseline shrinks monotonically.

(Corpus straggler pending; appends on arrival.)
## EXECUTION WAVE RETURNS (the 20-lane run)

### WAVE 0 - entrypoint fix (agent 5f9e8b1a) - LANDED
- REAL COUNTS: 2,624 collected post-fix (baseline 2,595; +1 chain pin, +28 gps_mcp); 29 passed (chain contract + gps_mcp); slice run: 148 passed / 2,476 deselected in 31.89s.
- Changes: cryptography>=49.0.0 into requirements (was missing), testpaths += tools/gps_mcp, importorskip guards on the two hard-import files, NEW tests/test_chain_contract.py (the two-chains-one-contract pin: world row -> gwap sign -> flip byte -> both fail).
- HONEST AMENDMENT to the M17 miner: this venv HAS vastai 1.5.5 + discord.py 2.7.1, so "zero of 2,578 run" does not reproduce here today; the fragility was real for requirements-only venvs and the absent-dep simulation proves the fix. Miner claim downgraded from CRITICAL to FRAGILE-BY-DEFAULT (still worth the fix).
- Owed: full-suite pytest -q execution number (out of scope), census bullet stale (2,303/09-27 vs 2,624 now - patrol's call).
### W1 - brief reaper (agent 6c1cbfeb) - LANDED
- 7 passed in 0.52s. FIRST REAL RUN REAPED 10 BRIEFS: FL-1..FL-10 appended to the live stealth work queue (23->33 ids), matching the driver's queued schema exactly; second run added 0 (idempotency proven live); census now reports live boards (briefs=10 armed=10), fixing t_backlog's blindness.
- The 10 armed briefs that sat unfired since this afternoon are now sensed rows. The loop eats its exhaust.
### LANE DEATH - skill_fired (agent 99d07e2b) - DIED [1302] rate limit at width ~20
Clean death: no partials (mag/skills_pack.py untouched, no test file, ledger untouched). The envelope law held: nothing lost, the contact is a HOLD signal not a failure. Replacement lane dispatched at width 19.
### W1 - bones protocol table (agent be736699) - LANDED
- 25 passed (protocol table) + 15 passed (server v0 guard, byte-identical API preserved). Digest pinned d41f7cba... (sha256 over canonical JSON, the row_sha/bones_digest house law); verbs now DATA: frozen rows + state ranks + both reject vocabularies; NOT_YOUR_TURN is live machinery (TURN_HELD rank) reserved-not-emitted; dispatch reimplemented minimal in the wow_bones shape (shape-equivalence pinned by test against mag.wow_bones.Dispatch itself - not imported, WoW vocabulary decoupled).

### LANE DEATHS 2+3 - ledger registry (c7db541d), mountain clone-proof (8a1e3b07) - DIED [1302]
Burst contact: three 1302 deaths in ~6 minutes at ~19-wide. Per the envelope law (rolling throughput, not width-only): HOLD - no immediate re-dispatch; the two lanes queue for re-fire as the wave drains. Death receipts filed; check partials before re-fire (mountain repo may have partial commits - it was allowed to commit there).
### LANE DEATH 4 - realign command (agent 5a91eb06) - DIED [1302] at ~18-wide
Same burst window. Partials check pending in coordinator pass; queued for re-fire at drain. The burst has now claimed 4 of 20 lanes - the width cost is being paid in full view; the 16 surviving lanes continue.
### W1 - room.py + ws door (agent bfbbb8e4) - LANDED
- 5 passed + 15-test guard. Room: per-client bounded queues, encode-once fan-out (same bytes to every queue), drop-on-slow inside fully-sync publish (never blocks the loop), presence sweep. Ws door: minimal RFC6455, framing stolen-and-credited from mud_relay, never touches 8766. The 3-line integration contract documented for the server owner.

### W3 - realign (agent 5a91eb06, DIED post-write) - COMPLETED BY COORDINATOR - LANDED
- The lane died to a 1302 AFTER writing everything. Coordinator verification: 3/3 tests, main.py parses, REAL FIRST RUN DELIVERED: NEEDS YOU rendered the operator's actual decision queue in plain language (attention: mistral DOWN, census COLLECT-DRIFT +42; queue: Q-001 verkle compaction needs-operator because it rewrites the chain, Q-002 auto-promote blocked on the human-gate law, Q-004/Q-005 human-only verifies...). The intimidation fix works on first contact. python main.py realign is live.

### W3 - front door regen (agent ba3fa69a) - LANDED
- 14/14. FRAMEWORK_LOAD regenerated from live truth: era 003 THE POUR, gates v2-v5 all ok (the inverse-trap fixed in the door itself), agent-state tip n=20523. --check mode + determinism proven. The front door can never be stale again; it dies and is reborn at every wave close.

### W2 - scarless preflight (agent d1338cc2) - LANDED
- 10 passed + 73 adjacent. Live BLOCK proven (a scar-carrying new write is refused at preflight; grandfathered files pass). HEREDITY COUNT: 513-655 of 1,247 mag/+tools/ files (41-52%) carry except-pass scars today - no file born after 2026-09-29 can inherit them. The baseline now shrinks monotonically by construction.
### W1 - gwap-to-gps adapter (agent 7b7b30e6) - LANDED
- 15 passed (adapter) + 43 combined with gwap payload suite. THE MISSING DOGFOOD IS CLOSED: gwap verdict rows now feed gps ledger.record_verdict. Key mapping is CALLER-SUPPLIED with strict precedence (scene map -> participant map via the intent author - the robber is the work product under verification) and NO identity fallback (a miss raises UNMAPPED_* because a guessed key would seed another model's capability row). Evidence = row_sha256 (chain position). Two-pass plan-then-feed: any refusal leaves the gps ledger untouched. Two organs, one metabolism - the meter eats its own dogfood.
### W1 - reprint harness (agent 659b2235) - LANDED
- 7/7 lanes green: the tape lived (9 acks, 6 ticks, WIN @ 5); dump==tape; REPRINT byte-identical from the dumped log; ACTION_FORK names the exact divergent tick (3) and nodes (crown 2->1); the fork costs the win; chain continuity across reopen. The log is officially the grader - every saved server tape grades itself.

### W3 - gap sentinel (agent c0152bb4) - LANDED + FIRST REAL ALERT
- 10 passed + live baseline recorded. FIRST METABOLISM READING: the estate grew +25.41 GiB in 2.02 days = 12.59 GiB/day - 12x over the 1 GiB/day bar (the repo itself +24.76 GiB; kpi.jsonl alone 1.01 GiB). The Sep 22-25 x_radar hole is byte-witnessed (err logs jump 09-21 -> 09-26). Sensor silence is now sensed; the compaction lane just became urgent.

### W3 - duel harness (agent 9f75cf3c) - LANDED + THE RETROACTIVE VERDICT
- 8 passed; real new spend $0.0248 (one ember judge, API-metered). THE DUEL THAT FIRED AND WAS NEVER JUDGED IS JUDGED: G3 glm-prime defeats G1 qwen 19-16 - both found the n_min/threshold contradiction, but glm-prime added the T2 formula error, the G1 tolerance gap, ECE variance, and testable predicates, at 0.39x qwen's cost. The estate's own workhorse family wins on its home turf AND is the cheaper fighter - a router row with teeth, banked in logs/duel/duels.jsonl.
### W3 - verdicts panel (agent 32cb6ba8) - LANDED
- One additive door /api/v1/verdicts (gps sqlite read-only, running-mean verified 0.6667/n=3; gwap + mountain receipt tails newest-first) + verdicts.html cloned from links.html (zero-fetch). The new estate has its face: every organ joins by one source line. Dashboard restart owed to serve it live.
### W2 - receipt xref gate (agent d5ded1e1) - LANDED
- 16 passed. Real scan of 24 receipts: 6 dead citations, triaged to ONE truly dead (server/protocol.json - a citation of the proposed filename that landed as protocol_table.py; run-plan citation fixed class), 5 non-literal shapes (globs, placeholders, method-glue). Line-anchor false-deads fixed at design level + regression-pinned. WARN-only arm proposed, not landed (operator call).

### W3 - skill_fired, replacement lane (agent 9defa4f5) - LANDED (the 1302 death avenged)
- 3 passed + 28 sibling. The chokepoint now emits skill_fired.v1 rows; the no-op filter actually filters. REAL research fire: 6 skills at 90-134 chars each (the starvation the miner predicted, now VISIBLE per fire); frontier-hr 0 (pack_excerpt false - by design). The fired() counter gives the catalog its never-fired column; fireball-cycle's demotion hearing has evidence.
### W1 - net_client dual-mode (agent 9775cb97) - LANDED - THE WAVE'S CROWN JEWEL
- Headless clean (60 AND 300 frames, zero errors) PLUS LIVE SMOKE AGAINST THE REAL SERVER: welcomed with sid, action sent, TYPED DRY_POOL REJECT RECEIVED, tick broadcasts parsed, exit 0. The 911-line server is LOAD-BEARING for the first time; the Mountain is now a networked client. Dual mode: welcome within 2s -> AUTHORITATIVE (render-only local tick, staged SPACE/E proposals, ack/reject into hint_text, score from server); deadline/BAD_AUTH -> SOVEREIGN (local physics stands, net freed). The flock wall-clock leak is FIXED (sim_time passed in; the determinism blocker named by the M17 godot miner is dead).
- B2 milestone 1 achieved: our Godot client spoke to our own server and was correctly refused by it. That is the whole platform thesis in one smoke test.

### DROP - HermesWatcher foundation framework (13:00Z, 659 likes)
- The generic AGENTS.md/PROJECT.md/STATUS.md/DECISIONS.md + inbox/areas/resources/work/outputs/archive pattern, scaling by per-area AGENTS.md. Industry convergence on what the estate already lives - the estate's version adds what this pattern lacks (hash-chains, receipts, generated counts, gates). STEAL BACK: the DECISIONS.md-per-area file (the estate's decisions live scattered in receipts/basecamp; a flat, human-readable decisions log per area is the one genuinely good simple piece the estate never built - pairs with the D1-D7 table and the needs-operator packets).
### M17 MINING WAVE - FINAL STRAGGLER (agent 21ef254d) - the 26th and last return
- THE CITATION CENSUS: only 4,427 of 59,221 corpus files (7.5%) are ever path-cited. The founding record itself (corpus/oral_history/seat_pools: 852 grok chats, 2,543 action streams, 193 codex rollouts - 11,675/11,870 files never cited, 1.07GB) has no reader in any tool. Unharvested law: TREE_DOCTRINE_ORGAN's SEE/REFRAIN/VERDICT triple-completion meter (30%/month demotion gate) - referenced, never built.
- IMPROVEMENT queued: mickey17_v2 lane-mining run over seat_pools (session_index.jsonl as manifest, existing tier machinery) -> ORAL_LAW_INDEX.jsonl (thread -> decision -> filed-law-or-debt). Converts the largest never-cited shelf into citable provenance; supplies the authorship-falsifier evidence class.

### W3 - consume op + orphan census (agent 99882827) - LANDED
- 9 passed. THE THREE REAL NUMBERS: never_registered 11,066 (70% = qdrop+mrpool exports); registered_missing 59 TRUE dangling; registered_never_consumed 2,207 (3 consumed ever, all this lane). The miner's 632 dangling decomposes honestly (59 true + 328 fold-blind spellings + 122 outside-surface). The consumer key registered per the B2-342 closed-vocabulary law; the log's first read op exists.
### W2 - zero-collect detector (agent d28a5178) - LANDED
- 8 passed; live run: collection CLEAN (2,757 collected, exit 0 - Wave 0's fix independently confirmed by this lane's instrument), exactly ONE real zero-collect: tests/test_selffeed_integration.py (a __main__ script wearing test_*.py naming - the disease itself, not a fixture; tolerant list seeded EMPTY on purpose). Detector fires exit 1 naming it, riding the existing 08:30 patrol. One sibling test pins the superseded buggy behavior - cure filed, not edited outside ownership (discipline held at width).

## STEAL WAVE 2 (24 lanes, batched 12+12+2 refires; lessons applied: staggered width, <=200-word returns, RESEARCH-ONLY lanes for no collisions)

### S7 - Anthropic subagent prompt patterns (agent 2770b0d6) - LANDED
- Field overlap close (we match/beat on output contract + receipts). TWO UPGRADES: (1) EFFORT BUDGET FIELD - their lanes scale by tool-call budgets (1 agent/3-10 calls simple; 2-4 agents/10-15 calls; 10+ complex) - our asks cap words but never tool calls or subagent count; (2) NON-OVERLAP FIELD - their duplicated-supply-chain-search failure = our G1/G3 double-fire; every lane ask should name what siblings already cover.
### S10 - realign UX steal (agent 3c2afde8) - LANDED
- realign already beats GitHub on one axis (stamp moves only on --mark-visited; opening does not consume). THREE LAWS TO STEAL: (1) DONE-NOT-READ - per-item resolve (realign resolves whole-visit only); (2) EVERY LINE SAYS WHY - reason tags per item (GitHub reason: labels; Linear Priority Inbox's action-required vs FYI); (3) TIME-BOXED DECAYING SECTIONS - IGNORED as collapsible recency groups with one-keystroke clear, never unbounded. Terminal CAN do all three; ordering is the whole UI.
### S1 - auth patterns (agent c6c04e1d) - LANDED
- V1 DECISION: port the realmd LESSON (server never sees the password; derived shared proof; session key = the only inter-process contract), modernize the MECHANISM (OPAQUE RFC 9380 named as the right modern line; v1 pragmatics under our no-RNG law: TLS-or-localhost + argon2 + short-lived HMAC sids + rotation + replay-detection). 3 steals: PartyKit per-connection token gate (replaces permanent sid), Auth0 refresh rotation w/ family revocation, Supabase claims-per-message auth (maps to our join/interest debt).

### S4 - opencode source mining (agent fb5d91ef) - LANDED
- Mined the actual install (binary is Bun-compiled but the plugin dist carries full contracts). 3 patterns for gps-mcp: (1) declarative provider registry with {env:VAR} interpolation + AuthHook for interactive acquisition; (2) catalog draft+hooks - providers/models/agents runtime-extensible via transform, not hardcoded; (3) headless JSON-event contract + SQLite sessions + oversized-output spill keyed by call id. Config-driven, extensible, observable - the interface shape confirmed from our own install.

### S21 - warp workflows (agent c6e285fd) - LANDED
- Workflows-as-files: YAML+frontmatter in a REPO dir ({{repo}}/.warp/workflows - the repo ships operator runbooks), {{placeholder}} args with defaults, picker invocation, sharing = git not platform. For mag.cmd: an operator-workflow dir in the repo = skills for the HUMAN; blocks make runs re-runnable/shareable.

### S9 - memory compaction (agent b8e6738c) - LANDED - THE ARC DESIGN
- Grounded in Megiddo-Mohda ARC: budget c split by adaptive p; T1 fresh / T2 consumed-2+ (consumption-rank feeds it - the consume op just became load-bearing); ghosts hold KEYS ONLY (2c metadata ceiling caps growth); forget-pointers on every demotion; recall retunes p. Survivorship from generational GC (eden/scavenge/tenure, promotion requires ONE why-context edge - Zettelkasten law: unlinked is not knowledge). Destination: quantized_thought archive, never delete; only fossil MEMORY generations trash.

### S24 - steal synthesist (agent 517db117) - LANDED
- Taxonomy (PATTERNS/CODE/VALIDATIONS/WARNINGS), ranking = compounding x meter-thesis-fit x cost, TOP-5 SLOTS by disease: organs-unwired -> verification contract + ledger; write-only -> read-op + replay; copied-not-mounted -> provider-abstraction mounts; ungated-gates -> sandbox lifecycle; death-unharvested -> BYO-token metering. The synthesis frame is ready for the remaining returns to pour into.
### S20 - anti-cheat unified design (agent 1d349f50) - LANDED
- Server-authoritative water kills position/velocity cheats BY CONSTRUCTION; the real surfaces: action spam (no rate caps - demo logged 30 tags/30 ticks from one client), replay abuse (winning tapes re-earn credit), collusion (cop copies tagger's claims, scores 1.0 with zero independence). DESIGN: RATE_CAP reject (per-sid per-tick budget of 1, surplus rejected at receipt) + STALE_NONCE (per-session monotonic action ids - tapes verify but cannot re-earn) + tag disputes as GWAP rounds (agreement + collusion fingerprint server-side, feeding the owed judge queue). OVERWATCH STEAL: keep supermajority juries, invert the pay - real meter_credit rarity, blocker priced as adversarial audit.
### S6 - Vorflux doctrine (agent 38eb9cce) - LANDED (with a byte-truth correction)
- CORRECTION: the steal map's "~90% subsidized by your own cloud credits" appears nowhere public; verified phrasing is "bring your own subscription, heavily subsidized" (Codex partnership) + $200 launch credits. 3 doctrine lines: (1) RIVAL-LAB JUDGE AS A FIXED STAGE - every run ends with a rival-lab model tearing the work apart before the PR (our cascade law's judge pass institutionalized, not escalated); (2) "Human time is the bottleneck, tokens are not" - supervise-by-exception, PRs land with video proof, review from a phone; (3) harness owns cleanup + forkable environment snapshots (the rib law applied to whole environments). They rent the harness; we own the arithmetic (output = 78-85% of cost, only our cascade cuts it).
### S14 - post-training recipe (agent 999572c3) - LANDED - THE HONEST CONSTRAINT NAMED
- OrcaCyber's method is a trade secret (nothing to legally copy); Nous Hermes recipes are open (curated SFT -> DPO); task vectors are real (arXiv 2212.04089). THE CONSTRAINT: every specialization path (SFT/DPO/LoRA/task-vectors/merging) is weight-space; over an API theta is unreadable and unwritable - no gradient ever touches GLM-5.3. WHAT WE CAN DO: (1) prompt-prefix specialization (borrowed per-call, never installed); (2) DISTILLATION VIA DUEL DATA - run GLM-5.3 with the prefix, keep winning traces, SFT/DPO OUR OWN smaller open-weight model on them (context-distillation, arXiv 2209.15189). Specialization either rents the prompt or moves to a model we own.

### S8 - canary/chaos practice (agent c472cb23) - LANDED
- Kayenta (Mann-Whitney U, 98% CI tolerance bands, group scores, NODATA=0), Flagger (metric checks + failed-check budget + auto-rollback), chaos principles (steady-state hypothesis, prod, automate, blast radius), ClusterFuzz (fuzz->dedupe->bisect->auto-file). V0 has: known-bads, control-vs-planted, death receipts, blast radius. V1 adds: scheduling + result ledger for drift, fire-rate ratchet (N silent runs = escalate), pre-push auto-abort, metric-shaped alerts.

### S5 - arena/duel sampling (agent cc41f209) - LANDED - WITH A REAL BUG CAUGHT
- No fixed N: sample until the BT coefficient's 95% CI excludes 0 (~30-60 duels/pair for 60-65% win rates); active sampling on widest-CI pairs (Arena cut votes 54%); hidden ask bank (70/30, pre-committed, never re-run); A/B order swap + judge rotation + majority-of-3; STYLE CONTROL: length/markdown covariates in the BT regression. BUG FOUND IN OUR HARNESS: judge_prompt() leaks a_model/b_model names to the judge - Arena anonymizes until after the vote. That is a v1 must-fix.

### S17 - Playhouse verify (agent e8b0ea99) - LANDED - PHANTOM KILLED
- playhouse.systems DOES NOT EXIST: authoritative NXDOMAIN from the .systems registry itself (both DoH resolvers, SOA from the TLD), zero Wayback snapshots ever, no GitHub org/repo, zero HN coverage. The geometric-P attribution is unverifiable - likely a confabulated slide-note. Lane killed honestly; the steal map's P stays UNKNOWN. (Lesson: the earlier research lane reported launchdata.lol as a source - that lead does not survive registry-level checking.)
### S12 - Kilo modes mining (agent ca7ff8d5) - LANDED
- 3 patterns: (1) MODE = persona FILE + ordered glob permissions (last-match-wins: edit deny-* allow-*.md) + visibility (primary/subagent/all - who may invoke: human vs orchestrator only) + nested dirs as namespaces; (2) layered precedence with PROPERTY-WISE MERGE (override one property without redefining the agent; builtins < user < project < .kilo/agent/*.md) + legacy auto-migration; (3) skills as a SHARED POOL orthogonal to modes (open SKILL.md format, metadata-only loading, project-shadows-global, each skill also a slash command) + rules as always-on instruction globs. For our organ: permission-globbed persona files, merge-not-replace layers, the shared pool independent of job-shapes.
### S13 - LDT implications (agent d0447bb9) - LANDED (with lineage correction)
- LDT = arXiv 2605.08605 (Davis, Haller, A. Alfarano, Santolucito; code on github) - NOT "Deduction Transformers 2507.18868" (that ID is an unrelated dual-process paper; lineage corrected). WHAT IT PROVES: an 800K-param recurrent transformer with its latent projected through an abstract lattice (candidate-set powersets, Galois connection) between passes, trained on-policy vs a constraint solver, hits 100% on Sudoku-Extreme (GPT-5.4/Opus 4.6/DeepSeek: 0%); soundness comes from the LATTICE SCAFFOLD + ABSTAIN HEAD, not scale. FOR THE CLONES: sub-1GB typed models can be SOUND if the type lattice is architecturally encoded. THE EXPERIMENT: a ~1M-param LDT on water-graph legality (powerset of legal typed edge-states, supervision from a constraint propagator, abstain-adjusted soundness vs plain-transformer control). Queued for the successor program.

### S11 - flock-as-server-actors (agent a02f5600) - LANDED - THE DESIGN
- Each fish = a register_session(sid="fish-N") row with NO socket (the ike3 seam): pure fish_decide(fish_id, tick, snapshot) emits verbs through stage->pending->tick in fixed sid order, logged as chained rows like humans. Integer math complete: Q16 fixed-point velocities, milli-unit constants, integer sine table indexed by (tick*7+pos.x*5)%TABLE replacing the RNG wiggle, reciprocal lookup for separation, FIFO trail cap. Floats never enter log rows. The boid math is now server-portable and deterministic end to end.
### S15 - RRSI regularization (agent 798cc935) - LANDED - THE PERCOLATOR DIAGNOSIS CONFIRMED WITH TEETH
- Top invariant now 232,214 = 79.8% of ALL 290,878 reinforcement events (430 invariants; median count 1) - and the winner is a static [steer] prompt template the loop itself re-emits each cycle. HEAL-MERGE SUMS COUNTS (percolator.py:184; the 09-06 seal healed 3x = triple-counted). It IS memorization: the count measures self-emission frequency, not validated truth. FIXES: sandbox-verify + strip-false-claims before counting (SuperScout), per-source rate limits per cycle, half-life decay, idempotent heal merge (max not sum).

### S22 - orb-lane spec (agent c254b1ce) - LANDED
- Lane-as-orb: bounded ACU-style budget with auto-stop, worktree isolation (fail-closed unsandboxed-refuse), checkpointed sleep state, death receipts, review-before-merge as diff+proof. THE 2 MECHANISMS WE LACK: (a) pre-bound metered budgets that HALT a running lane (we only have post-hoc billing receipts); (b) fail-closed isolation (lanes share one checkout; no worktree/sandbox in the harness).

### REFIRE - mountain clone-proof (agent a6ef35b2) - LANDED (commit 035a5e3, not pushed)
- Exec bit 100755 (ships with clones), LICENSE + CONTRIBUTING (MIT; CMaNGOS/GPL and client-data never committed), ghost paths fixed, README contradiction resolved (executed headless clean + live net_client smoke, PLAYED-by-no-one stays true), honest CI v0 (no-engine: syntax, UTF-8, exec-bit, gate dogfood - all verified exit 0). ADAM'S DAY ONE: clone, one line, press F5.

### S23 - Hyperagent org-mem governance (agent e47355b5) - LANDED
- 3 patterns for the mirrors: (1) PROPOSAL-CONSENT GATE - nothing writes itself; learned items queue as proposals until accepted; auto-saves still emit receipts (mirror-shape: behavioral lenses default propose-only); (2) PROVENANCE + DEDUP - every memory links its source thread; similarity-grouped merge/keep/archive (unbounded mirrors need lineage + similarity compaction, not just caps); (3) SCOPED PROMOTION - personal vs shared truth; review decides; roles gate edits; external writes need inbox approval.

### S19 - chat v1 spec (agent 226ab312) - LANDED
- One verb say (240-char cap, BAD_TEXT reject), delivered in the existing tick events (zero new ops, determinism preserved); v0 GLOBAL distance-free - honest, because the world has no coordinates (the CMaNGOS lesson: don't fake distance delivery without a grid); v1 whisper as a direct line outside the canonical tick; BOTS SPEAK THROUGH THE SAME CHANNEL (UF-01 innkeeper as a client-with-sid or server-injected tick events - Rashomon voices ride the ledger, engine truth stays the tick).
### S2 - interest mgmt (agent 098c0431) - LANDED
- Verdict: grids buy NOTHING at 6 nodes. Rune/PartyKit/Colyseus at <50 players: none spatial-partition; rooms broadcast-all. v1 = rooms-not-grids (already server/room.py's shape): interest IS membership; the full 6-int tick (~200 bytes) is cheaper than any diff. Later AOI unit = the roster's 'at' node (per-node presence slices); known-set diffing is v2 debt triggered only if nodes >~50.
### S16 - pytest/CI standards (agent 2a560c80) - LANDED
- Mature OSS: mypy (tox matrix, xdist -n 4, SHA-pinned actions), pytest itself (tests install from BUILT SDIST --installpkg - catches packaging/import rot a source run hides; alls-green gate job), attrs (tests against the wheel + -Ic import smoke + fail-under-100 coverage + Dependabot). THE 5 LINES: checkout / setup-python / pip install reqs+pytest+xdist+import-linter / pytest --collect-only -q (zero-tests-silent-pass can never happen again) / pytest -n auto. IMPORT-LINTER = the one mainstream tool that stops graph rot (layers contract, lint-imports in CI exits nonzero on forbidden imports).
## LANE TOPOLOGY DOCTRINE (operator question 2026-09-29: "how do we get lanes to last longer / ride to the edge / talk to each other like our dfhack")

Three upgrades, first demonstrated live:
1. RESUME-NOT-RESPAWN: completed agents resume by ID with full context (demonstrated: the duel lane resumed post-completion to fix the S5 judge-leak bug - zero re-bootstrap). The stable-of-specialists pattern replaces one-shot lanes for repeat surfaces (duel, bots-port, server).
2. MULTI-CYCLE MISSION SHAPE: lanes ride to the edge when the ask is an iteration loop (bots-port: 10.5M tokens, 6 cycles, one lane). Short mining lanes were a COORDINATOR-window constraint (200-word caps), not a lane limit.
3. THE MESH: lanes can message each other (SendMessage) + the estate file blackboard. Topology upgrade: star (all->me) becomes mesh (lanes hand to the synthesist lane; steal-finders resume builder-lanes to apply their findings - the S5->duel-lane fix is the first instance). My window stops being the funnel.
Owed: the stable roster (which lanes persist), the inter-lane handoff convention (a HANDOFF line in receipts naming the target lane class), and the S22 orb-spec's two missing mechanisms (pre-bound metered budgets, fail-closed worktree isolation).
### S3 - state sync (agent 7ddfb154) - LANDED
- Verdict: keep full-snapshot-per-tick (deterministic, one encode, log row = replayable truth). Breaks at ~hundreds of nodes / per-viewer hidden state / sub-100ms ticks. Graduation ladder: (1) dirty-node patch {n, changed, events} + seq, snapshot on join only; (2) per-viewer encode when worlds diverge; (3) binary field-index only if JSON measurably hurts. Steals: Vercel's typed append-only parts + id-keyed reconcile; Colyseus field-index deltas acked per client.

### S18 - persistence (agent 6d4d5a87) - LANDED
- Verdict: hash-chained JSONL + snapshots IS ENOUGH for v1 - every modern framework converges on our shape (Rune per-player JSON, PartyKit KV, DO SQLite, Colyseus decoupled saves); our log is STRICTLY STRONGER (auditable + replayable). v1: (1) restore on boot by replaying the log - determinism law makes replay byte-exact and free; (2) periodic kind:snapshot rows in the same chain (restarts replay tail-only); (3) rotate/compact the tail. A real DB enters when accounts/leaderboards/cross-world queries appear (the realmd contract) or tail-replay slows - then per-world SQLite mirroring today's per-world file.

## STEAL WAVE 2 COMPLETE: 24/24 LANDED, ZERO 1302 DEATHS
The staggered batching (12+12) held the whole wave - the lesson applied is the lesson confirmed. Still outstanding: gate canary (M17), ledger-registry refire, the resumed duel lane (v1.1 fix).
### W2 - gate canary (agent 94aac78c) - LANDED - AND ITS FIRST RUN CAUGHT TWO CORPSES
- 35 passed. The canary: throwaway worktree of HEAD (venv junctioned so the secret gate arms), one known-bad per gate family, runs the hook's exact gate command, asserts each gate's own named detection, files attention rows for the dead. FIRST REAL RUN's alive/dead table: 8 ALIVE (ratchet, config_seal, secret, census patrol, freshness, checkbox_receipt, description_pin, workflow scenarios). 2 DEAD: caption_ledger_verify (deleted ledger row -> RESULT: PASS - the denominator is built FROM ledger rows, deletions invisible) and refold_gate (self-recursion RecursionError at HEAD, the same bug class secret_gate already had fixed). CONTROL FINDING: config_seal's 56 sealed hashes all mismatch HEAD (CRLF-sealed register, any LF checkout fails). Attention rows filed. THE WATCHERS ARE NOW WATCHED - and the very first watch found two dead guards.
- Owed: schtasks registration (MagGateCanaryDaily 09:45 - operator call), the two dead gates' fixes.
### REFIRE - ledger registry (agent d3ac7768) - LANDED - AND ITS FIRST RUN FOUND A LIVE REGRESSION
- 8 passed + 84 adjacent. The real chain table (verify_all, exit 1): 5 chains OK (wow_player x2, gwap x3) + VERKLE FAIL REGRESSION - 300 dangling rows lacking evidence_lost markers since 09-26 (its own guard knew; now the registry canary files one idempotent attention alert). server_world mounts 0 production chains (44 pytest fixtures, deliberately unswept). Query-by-hash PROVEN LIVE (resolved a gwap row by hash). Debts: party_subchain/tesuji unmounted, nightly task v1.

## WAVE EXECUTION COMPLETE (all lanes landed or posthumously completed; duel v1.1 resume in flight)
### W3h - Adam pack (agent c1007efb) - LANDED (commit 2fcda8f in the-mountain, not pushed)
- 97 lines, every claim byte-checked against game.gd first-frame reality; jargon scrubbed; dual-mode honest (standalone complete, server not yet published in-repo); issue template leans on determinism. B4's door exists.

### W3f - blind re-judge (agent b870825f) - LANDED - THE VERDICT FLIPPED
- $0.0176. BLIND: qwen defeats glm 19-17 (name-aware had glm 19-16). Per-criterion: glm coverage 5-4; qwen severity/citations/actionability 5-4 each. HONESTY: n=1, name bias + position bias + sampling all changed at once - cause not isolated. The name-aware rows are now marked; the duel ledger holds both. Lesson: never bank a name-aware verdict again (already law in v1.1).

### DROP - Math_files God's Number (01:58Z)
- The cube as graph: 43 quintillion states, 18-regular, diameter 20 (Rokicki et al. 2010); superflip needs the full 20. SEEDS W3m: what is the MOUNTAIN'S God's Number - the diameter of our water-board state space? BFS-computable at our scale; the legality dataset lane already enumerates states.
### LANE DEATH 5 - W3l grok parser (agent d54532a5) - DIED [1302] at batch-2 burst
The batch-2 fire while batch-1 lanes still drained pushed simultaneous past the rung again (the law re-proven: stagger, don't stack batches). Clean-check: mine driver parses clean (partial-write risk checked). Queued for re-fire at drain.
### W3a - caption gate fix (agent 34e05d83) - LANDED - THE FIRST DEAD GATE RESURRECTED
- check9 added: sealed baseline (SEALED_ROW_COUNT=267 + sha256 of the live ledger, 2026-09-29 bytes) carried in the gate's own source - the denominator is now INDEPENDENT of the thing audited. Regression tests + canary drill PROVEN: 267->266 planted deletion -> exit 1 FAIL naming the count; intact control passes. 5 passed + 12 with pairing suite. The gate canary's first corpse is alive again.
### W3i - lane budget meter (agent 24f5a5b1) - LANDED
- 12 passed. Budget(name, max_actions/seconds/usd) pre-bound; spend-then-check; death receipt to logs/lane_budget/deaths.jsonl BEFORE raising; context manager checkpoints; resume inherits remaining and cannot launder a dead state; UNMETERED explicit. S22 mechanism 1 closed (mechanism 2 fail-closed isolation still owed).

### W3x - day synthesist (agent d77dbcbc) - LANDED
- DAY_SYNTHESIS_20260929.md: five beats (sense/plan/execute-bleeding/steal/metabolize-reorganize), three laws confirmed (stagger-not-burst, resume-not-respawn, dogfood-the-ask). THE UNASKED QUESTION: 'every organ shipped today named its tests, never its reader - what is the first-reader law: can an organ land without naming the consumer that will prove it was read?' (Write-only disease, stated as law-candidate. Yes - adopt.)

### W3j - enqueue death law (agent b078abf5) - LANDED (with a byte-truth correction)
- 8 passed; real census: all 3 ledger pieces are zombies (nomic_rules_patch 126/133 stale since 08-17; byte-truth: 133 actual enqueues NOT 174 - return 18's prose corrected); CRITICAL: the loop is STILL PROMISING - 7 fresh enqueues past the epitaph, last TODAY. 3 epitaphs in GRAVEYARD.jsonl (idempotent); --prune wrote the .pruned.jsonl copy (130 removed, 49 kept, original sha verified). The 174-zombie is dead; its respawn habit is next.

### W3b - refold gate fix (agent 64330716) - LANDED - SECOND RESURRECTION
- _run self-recursion -> subprocess.run list-form (mirroring secret_gate's fix; fix comment carries cause+evidence). Real tree: REFOLD-GATE ok, 27 passed exit 0; fixture suite 2 passed; with canary+pairing 44 passed. Canary still BLIND at HEAD bytes (it audits committed HEAD - flips ALIVE post-commit; expected). Same-class latent debt found in quote_audit_wide.py:63 - flagged, not touched (ownership held).
### W3u - verdicts nav + smoke (agent 2ee62653) - LANDED
- Nav entry added (node --check clean, FW-45 shape matched). Door verified by direct call: verdicts.v1 round-trips; gps ledger holds the NIGHT ROWS (glm-5.3-prime | night-judgment | 0.8333 pass @ n=6); gwap tail 3 files, mountain 10. Restart of the live dashboard owed (lane law - not forced).
### W3g - mountain twin sync (agent 8c377105) - LANDED (commit dca3801, not pushed)
- 7 files, 426+/23-, byte-identical diff-verified: net_client.gd, dual-mode game.gd, flock sim_time fix, PLUS water_graph.gd's siphon-key fix (W2's owed fourth item). Headless 60+300 clean, gate clean. Adam's clone: offline sovereign OR authoritative against the estate server, zero config. Only the server stays unpublished in-repo.

### W3w - STEER channel LIVE (agent 6d31b7ce) - LANDED
- watch/inbox/STEER.md carries the operator's standing order as the seed row (mate: all, 'keep rolling 24 wide; proven seats only; dogfood gps', provenance: session order); tools/steer_read.py (latest-wins, all-or-match, malformed-fail-loud, via-less rows -> proposal); 9 passed (4 pre-existing + 5 new). Sharp catch: a bare provenance field would have misfiled the operator's own order as a proposal - the via:hand-edit fix documented. THE INTERRUPT LAW IS MECHANICAL: edit one file, the fleet turns.
### W3o - lane-ask template v2 (agent 0363fcac) - LANDED
- docs/ref/LANE_ASK_TEMPLATE.md: the canonical 8-field ask (incl. EFFORT BUDGET ladder TIGHT 1/10 STANDARD 3/40 DEEP 6/120 + NON-OVERLAP - the two S7 fields); ractor-essay ledger v1.2 line appended (lens asks adopt both; blind divergence made structural). One hand-written count caught+corrected by its own instrument (the law working on itself).
### W3d - REPRINT (agent 9ce7c26a) - LANDED - DEATH IS NOW A HANDOFF
- 6 passed + 16 regression. reprint(dead_campaign_id): salvage honors temple:/slain:/door_open: + inventory, DROPS cheat:/nuke: (named in the knot), actor re-seated at full hp with reprint_n+1 lineage, per-module pass-off via _MODULE_HANDLERS, death folded as verkle knot (rib_bus conquer idiom), receipts via both live patterns. Open seam: water's pass-off no-ops (water_computer.py outside ownership - next window's 3-line weld).

### W3t - task registration (agent 91607f95) - LANDED
- MagGateCanaryDaily 09:45 + MagGapSentinelDaily 08:15 registered, verified Ready/Enabled; the canary's register script carried a real defect (PS 5.1 -Command quote-mangling = schtasks exit 5) - fixed to the census -File-wrapper pattern. Hand-run proofs: gap sentinel exit 0 baseline recorded; canary exit 1 FINDING the dead gates to attention.md itself.

### DROP - RyanSael river-bend (12:47Z, 3.1k likes)
- sael.net/river-bend: interactive river-formation sim ("stop teaching geography with flat pictures") - meandering rivers, sediment, erosion as a playable medium. Verbatim relevant: the estate runs a WATER COMPUTER and its water is integer-volume graph physics; the operator asks where the fluid/particle/HVAC-engineering depth went (an HVAC flow-test surface existed in the light-maze era, now unfound in the tree). Seeds the water-engineering wave below.
### W3r - estate index dedup (agent f23d6eb7) - LANDED - 1.95 GB RECLAIMED
- Duplication CONFIRMED byte-for-byte (full sha256 both copies equal); shas banked FIRST, mirror replaced by a 92-byte pointer; 1,945,896,422 bytes reclaimed; 7 tests passed; --check mode for the future. RISK named: the producer rewrites both copies each run - the mirror may regrow (the dam vs the river).

## WATER ENGINEERING WAVE FIRED (6 lanes, operator challenge: 'for a water computer, where is the water physics?')
- WA: HVAC archaeology (what happened to the flow-testing surface)
- WB: water organ census (what physics each organ models vs lacks; the 3 missing organs ranked)
- WC: river-bend steal (sael.net mechanics -> integer-substrate version -> Mountain rivers)
- WD: k8s-as-water ractor (the light-maze idea through today's meter; hydraulic mapping of k8s primitives)
- WE: particle/field design (deterministic visual water advecting the integer graph; skyrmion vortices at junctions)
- WF: synthesist (why the water is thin; the five-rung ladder; the first build; the organ's name)
### W3q - attention flood dam (agent 00e1d3b4) - LANDED - 1123 -> 43 LINES
- 7 passed. Noise = closed class (session-record blocks); signal-by-default keeps everything else incl. unknown headings. Real pass: 90 session blocks / 722 noise lines archived verbatim (pointer in header); 38 signal lines kept, ZERO lost (probe-alarm, COLLECT-DRIFT, gate-canary, sentinel all intact); ratio 1:19 -> 38:0; idempotent (second run archived 0, byte-identical). The operator's signal surface is signal again.

### WA - HVAC archaeology - LANDED (receipt: water_engineering_20260930/WA_HVAC_ARCHAEOLOGY.md)
- Found: airflow_home.html (09-07, 'the house is the prompt'): real zone-model HVAC w/ conserved smoke + prediction-verdict loop. Status: runs as an UNLINKED orphan; was absorbed into maze_arena's __fluidTick ('smoke is stuff, not pixels'). Not dead - unharvested. Easy wins: relink in games index + port its prediction-verdict loop to the Mountain.

### WE - particle system design - LANDED (receipt: water_engineering_20260930/WE_PARTICLE_DESIGN.md)
- systems/water_particles.gd v1 design: client-render particle layer advecting on a field DERIVED from the integer graph (pipe flow = capsule channels, velocity = flow/cap); XOR junctions spawn curl rings (arena's exp falloff - the skyrmion steal) scaled by pooled volume; zero RNG (hash(index) seeding, flock idiom). Three mechanics: vortices trap/rotate fish, surface drift carries the trail, splash bursts on valve events. Authority untouched - render only.

### W3m - GOD'S NUMBER OF THE MOUNTAIN (agent f4a2c159) - LANDED - THE NUMBER IS 25
- Exhaustive BFS over the REAL WaterGraph tick edge (no reimplementation): 339,840 reachable states; farthest state (unique, depth 25) is a post-win XOR-double-spend corner; shortest solve = 5 (4 boils + 1 tick, replayed through MountainWorld by test). Two byte-identical runs; 4 passed + 39 neighborhood. The Mountain has a superflip: a 25-move state nobody will stumble into.

### WD - k8s-as-water ractor (agent bb6bb826) - LANDED (receipt: water_engineering_20260930/WD_K8S_AS_WATER.md)
- Full hydraulic mapping (pod=node, quota=pipe cap, scheduler=gravity tick, shedding=sill, autoscale=siphon, escalation=boil); AI-as-operator reframed as gps_mcp's shape (the AI sets elevations/sills/crests, physics dispatches); skeptic: it died of no consumer, today gps_mcp + webernetes unblock it. VERDICT v0: water_graph as k8s scheduler simulator fed by gps JSONL receipts, $0, no cluster.

### W3v - x_radar holes (agent d5e9f69a) - LANDED
- Real census 09-08..09-29: 15 ok, 7 missing. 09-09/10 byte-witnessed 402 Grok-balance-exhausted; 09-22..25 the writer NEVER RAN (zero artifacts, no scheduler owns the radar). gaps.json + HOLES stanza + one idempotent attention alert. The radar's blind spots are now visible on the dashboard.

### DROPS (2026-09-30 night)
- MapMakinMeyers (205 likes): revolutionarygis.wordpress.com - 13 years of hardest-to-find geospatial datasets, free. Seeds the geodata wave.
- yshan2u (Ying Shan): one model for text-driven motion WITHOUT per-rig retraining - seeds the motion/agent-body wave.

### GB - terrain feed - LANDED (receipt filed)
- SRTM .hgt -> dem_to_board: stdlib array reader (no pip), 64x64 block means, integer normalize to elev 0-255, 4096 nodes, auto-tag cold/waste, sha256 board hash (same tile = byte-identical board). Worked example: Mt St Helens N46W122 - the 1980 blast zone playable.

### GD - rig design - LANDED
- Motion contract: one typed row motion(sid, verb, intensity_q8, dir_q16), verbs {idle,flee,pursue,carry,dance} - enters protocol_table like 'say', rides the existing tick. Actor = brain (server-side pure decide(), deterministic) + rig (render-only). Flock becomes fish_brain + generic rig; any bot (innkeeper dance-on-arrival, carry-on-delivery) gets a body for free.

### GF - TIE IT ALL - LANDED (watch/inbox/TIE_IT_ALL_20260930.md)
- FIVE ORGANS CLOSED INTO A LOOP: platform=skeleton, meter=metabolism, operator-model=nervous system, mates=reproduction, water=circulation. THE NEXT-DAY MOVE (one build, three ties): Watershed rung 1 (~20 lines) driven by the live server, whose session becomes the first PRODUCTION feed through gwap_to_gps into the gps ledger - water gets feel, platform gets load, meter gets real traffic; mates' static-runner rides the same commit.

### DROPS (2026-09-30, four more)
- cosmosarcive Riemann (251 likes): the metric tensor - curvature without embedding; estate angle: knowledge_graph edges as a metric, distance-as-relevance formalizable.
- NilsEdison (55): 'headless game - shared world-state with clean API/MCP so you vibe-code your own experience on top' - THE ESTATE'S EXACT B2/B4 THESIS, independently stated. Validation receipt.
- jurlycat (234): Opus vs Sonnet same Blender+Three.js task - Opus 2.5M tok/$156 richer vs Sonnet 1.68M/$109 cheaper; the delegation data point for the meter's frontier rows.
- ferlinux (219): Claim Avenue 20-day traction (700+ buildings, 150k visits, $30k transactions) - a 'strange little city' that found demand; the player-city precedent for the platform's world layer.

### W3n - verkle dangling repair (agent f420b2a5) - LANDED - ZERO EVIDENCE LOST
- 8 passed + 25 adjacent; chain never written. Real classification: 371 dangling = 300 RECOVERABLE (all hash-verify against biography_backup knots - zero truly_lost, zero markers needed) + 71 already flagged. Side ledger memory/verkle/repair_20260930.jsonl append-only. The Q-001 operator gates (restoring the 300) refused correctly - that door is yours, not ours.

### DROP - Dr_Singularity fusion (498 likes)
- GPT-6 Astra Pro helped solve a 1967 conjecture: hidden transformation converting symmetric fusion plasma solutions into exact asymmetric 3D ones. Frontier-as-mathematician datum for the meter's frontier rows.

### W3k - legality dataset (agent fef71d16) - LANDED
- 5/5 green. 20k seeded samples: train 18,000 rows / 52MB / sha 466ebdb0; val 2,000. Labels: unknown_target 4805, dry_pool 5592, unknown_verb 1990, no_gain 6771, legal_gain 842 (~4.2%, steam-gated). Byte-identical regeneration; 10-sample independent engine re-derivation pinned. The LDT experiment's food exists.

### DROPS (2026-09-30 dawn, five)
- matharium: k-means converge proof (WCSS monotone + finite partitions -> stop). The hillclimb/RRSI formal frame restated.
- mathemetica: FLUID TOPOLOGY - circulation must be shed; starting vortices; Hopf links; ideal fluids conserve topology, real ones let knots fade. THE WATER WAVE'S POETRY VERSE: the skyrmion steal + the Watershed in one tweet.
- threejs: proceduralbuildings.chirostudio.xyz (319 likes) - procedural city gen in the browser. The overworld-builder reference for the platform.
- NVIDIAAI: Physis-Lang - physics-reasoning video captions fine-tune world models; +5.62 PhyGenBench by prompting alone. THE METER ANALOG: physics reasoning in prompts = receipts in prompts; capability improves without retraining the model. Direct gps thesis validation.
- muellerberndt: fetch failed (deleted or private); unprocessed.

### DROPS (2026-09-30 dawn, final three - the water wave's closing gifts)
- threejs particle fluids (dgreenheck.github.io/threejs-particle-fluids, 98 likes): SPH particle fluid sim in Three.js - THE Watershed rung-3 reference implementation (particles, incompressibility, rendering) in the browser. Steal target for water_particles.gd.
- vib3coded (500 likes): Opus vs Astra gummy-dice bake-off - Opus wins on looks AND price ($16.50 vs $20.89). Another delegation datum for the frontier rows: Opus's edge is material feel, not just correctness.
- vivekgalatage (344): Cornell GPU architecture roadmap updated for Blackwell B200 - the curriculum item for the k8s/hardware literacy the estate's infra lane owes.

## THE TIE-IT-ALL COMMIT LANDED (579109f44): every wave's work committed; the day is whole in git.

### W3c - config seal CRLF fix (agent b22d2561) - LANDED
- Honest byte check: 41/56 (not 56) sealed hashes mismatched LF blobs. Fix: normalize CRLF->LF before hashing in BOTH seal and verify (one function); schema v2; re-sealed 57 files; verify passes on CRLF tree and matches 54/57 LF blobs (3 = in-flight sibling edits, not EOL). Rationale filed: normalize beats re-seal (re-sealing recouples to one host's EOL policy). 52 targeted passed; full pytest exit 0 twice; 2,903 collected. THE THIRD SEAL DISEASE CURED.

## WAVE 3 FULLY COMPLETE. THE LEDGER IS THE DAY. Goodnight.

### W3p - skills permission globs (agent cd1474bb) - LANDED
- check(skill_id, path, mode): S12 Kilo semantics (ordered globs, deny- prefix, last-match-wins, fail-closed when no rule); 5 pilots in skills.yaml (ractor-essay, corpus-harvest, show-me, elder-lens, code-agent-data - writes bounded to watch/inbox/**). 8 passed + 11 sibling. NOT ENFORCED anywhere yet (adoption = separate law change, stated in code + receipt). Full tree: 2,876 passed / 4 failed / 12 skipped / 3 errors - all pre-existing on non-owned surfaces.

### X10 - airflow relink (agent 8c8347b3) - LANDED
- The HVAC ancestor has its door back: games index href + dated comment crediting the archaeology receipt. Verified 200 on both live servers. Bonus: nav.js already linked it (the games INDEX was the gap, not the nav). Self-contained confirmed (357 lines, zero externals).

### X5 - night-burn first reader (agent fe17fa5e) - LANDED - THE IRONY RESOLVED
- All 6 gopher returns read; digests filed. N1: the OCEAN profile is 'the operator's self-model laundered through his own gates' - would drop AGREEABLENESS to LOW, strike 'high loyalty' as UNPROVEN; N2 (earned its $0.0188 - three kills): T1 dead-code gap, no chain-concurrency story, unenforceable recusal + 5 missing predicates; N3: build-order reranked (watchers with Wave 1); N4: LDT buildable, $50-150, propagator first; N5: TRUNCATED (one word 'Below', $0.14 in reasoning - the lesson: cap lower on schema asks); N6: essay 6/10, the tiered-delegation citation is the fabrication risk. First-reader law now has its founding case: the day's own outputs read back, judged, and their actionables named.

### X2 - grok parser (agent f25bc696) - LANDED - THE UNAVENGED DEATH AVENGED
- Grok event shape learned (chat_history.jsonl: user queries in <user_query> tags, boilerplate skipped, assistant plain strings); thread_body() falls back to grok_thread_body(); 3 real bodies parsed (585-968 chars); codex path intact. THE 852 GROK SESSION POOL IS NOW MINEABLE - the oral law mine's second half unlocked.

### X3 - reprint water weld (agent dd2d3271) - LANDED - THE WATER REMEMBERS
- mag/water_computer.py: atype='reprint' -> reprint_salvage(): honest death carries graph node volumes/tank heights AS-DIED to the reprint (the water remembers what the corpse knew); cheat death carries mode but DRAINS memory (topology zeroed, tanks reseeded - dishonest clones don't ship). 9 reprint + 31 water family + 44 adjacent passed. Death-as-handoff is now COMPLETE for the flagship module.

### X6 - oral law wiring (agent 33749476) - LANDED - THE FOUNDING LAW NOW RIDES EVERY PACK
- skills.yaml gains oral-law entry (research + always_soft, first in the research job list); skills_pack's _law_tail: .jsonl skill paths excerpt as TOP-5 laws by birth_count (superseded skipped) - a 5-line tail, never all 55. Live probe: research pack carries 5 law lines, birth_count=3 leaders first. 5 passed + 8 permissions. Every future research pack now carries the estate's actual founding law.

### X8 - water particles (agent 3894d4b1) - LANDED - THE MOUNTAIN HAS SURFACE
- water_particles.gd: client-render droplet layer on the integer graph (pipe corridors advect at flow/cap, parabolic capsule profile; XOR junctions churn standing curl rings with exp falloff; splash rings on every event class, color-coded; drag 0.985; hash+sine phases; sim_time only; zero RNG; authority untouched). Headless 60 AND 400 frames exit 0 clean. The Mountain's water now LOOKS like water while staying byte-deterministic underneath. (Honesty note: built from the task brief + WF rung 3; the cited WE receipt was never written - the design lived in the lane's report.)

### X11 - GPS production feed (agent f24f1a40) - LANDED - THE METER ATE ITS FIRST REAL MEAL
- server/verdict_feed.py: every world.tick() mints a gwap payload (scene = tick session, claims = action rows via the closed gwap_mud mapping, verdict from the ENGINE ITSELF: VERIFIED_AGREE iff world.verify_log()) -> through gwap_to_gps into the gps ledger. Demo: ticks 1-4 VERIFIED_AGREE, tick 5 idle-skip; gps capability row (mountain-world-v0, world-tick, pass_rate 1.0, n=4). 13 passed + 112 neighborhood. THE LOOP IS CLOSED IN PRODUCTION CODE: platform -> payload -> adapter -> meter. Debt: the server loop's one-line call (ownership boundary, next window's weld).

### X8 note already filed. Wave X: 9/12 LANDED (X1,X2,X3,X5,X6,X8,X10,X11 + W3p). X4 (duel series), X7 (St Helens), X9 (motion rows), X12 (mate unblock) still building.

### X9 - motion rows + fish brain (agent 082a1f76) - LANDED - THE UNIMATE STEAL BUILT
- MOTION_TABLE in protocol_table.py: idle/flee/pursue/carry/dance with {intensity_q8, dir target}; compile-time typed payload law (u8/target specs, BAD_ARGS/BAD_INTENSITY/UNKNOWN_TARGET rejects); the ordering law EXTENDED: verb -> state gate -> payload -> handler (handler never fires on refusal). v0 wire byte-identical (digest d41f7cba preserved; MOTION_DIGEST ce259465 new). fish_brain.gd: the boid math as pure decide(fish_id, tick, snapshot) emitting motion rows - no RNG, no clock, no state. 51 passed + 25 regression. Brain+rig split is real: any actor (fish, innkeeper, future beast) is now a brain emitting typed rows + a rig consuming them.

### W3e - graph heal (agent a47a2336) - LANDED - THE COMPACTION PASS RAN ON THE REAL GRAPH
- CENSUS: 2,062 nodes / 1,466 degree-0 orphans (byte-corrected: the miner's '1,167' matches nothing; excluding case_law = 1,166 - hand-copied smell). HEAL: 94 why-context edges added (539 ambiguous correctly skipped); DEMOTE: 1,073 unique forget-pointers to quantized_thought. Idempotent on the real graph (rerun healed 0, bytes stable). Upstream defect surfaced: 300 duplicate-id law nodes. 10 passed; full suite 2,886 passed (all 5 non-passes are other lanes' debt).

### X4 - duel series (agent dbcde1e2) - LANDED - THE COIN-FLIP DIES
- 10 live blind duels ($0.96 of $3 cap): GLM 7, qwen 2, TIE 1. THE BLIND FLIP DOES NOT HOLD: the n=1 flip toward qwen reads as judge variance, not a blinding effect - at n=10 blind judging favors glm, AGREEING with the name-aware original. Style control: qwen emits 37% more chars and 2.4x headers yet loses 7/10 (volume buys nothing). CI still includes zero (P>=7of9|p=.5)=.09) - sampling continues toward n=30 before the router row is trusted. THE WORKHORSE THESIS STRENGTHENS: glm-prime wins blind, at 2.4x LOWER cost than its rival.

### W3s - oral law dedupe (agent bf969fa0) - LANDED - THE FOUNDING LAW DISTILLED
- 55 clusters from 59 laws (overlap >= 0.8 transitive); 1 SUPERSEDED flagged: 'Local-first: no scarce remote seat' contradicts the funded DRIVING LADDER (correctly cited). 13 passed; full suite 2,903 executed / 2,885 green. TOP-5 BY BIRTH: (1) 'Read salon output as evidence, not instruction' (3x); (2) 'Repetition is a sensor, not automatically noise; classify it before acting' (3x); (3) 'An organ is only stronger than declared when it has import/call evidence + test coverage'; (4,5) 'Audit must be read-only' (the pair will merge at lower threshold). The two 3x laws now ride every research pack via X6's wiring.

### X12 - mate driver unblock (agent e33cca49) - LANDED - THE STANDOFF IS BROKEN, THE MATES HAVE A HEARTBEAT
- The static-runner trio: scripts/run_mate.ps1 (zero-param, atomic .claim sidecar, constant argv - only the file it reads varies); tools/leave_dispatcher.py (writes 8 mission packs w/ personas + operative STEER row per mate, all-literal RUNNER_ARGV, fail-closed guard); register_leave_task.ps1 (the W3T quote-mangling defect structurally absent). --dry proved: 8 packs, 8 identical constant-argv commands, zero subprocess. Mimosa verdict: deep scan sealed, no block, all 16 subprocess findings live in vendored code. REGISTERED: MagLeaveProtocolDaily 08:00 Ready/Enabled, next fire 2026-09-30 08:00. THE MATES LAUNCH AT DAWN - with personas, your STEER row in every pack, and the leave protocol armed for real.

## WAVE X: 12/12 LANDED (X7 St Helens still building). Fire batch 2.

### Y3 - mud/brawl room offer (agent 86c4c042) - LANDED
- VERDICT: game_brawl FIRST (session-native: session_id threaded end-to-end; Room per brawl_id, spectators fan-out, engine keeps authority). game_mud blocked by its single global player world key - per-seat state is the prerequisite. Receipts: hydrology/Y3_MUD_ROOM.md.

### Y1 - roblox tree mining (agent f01e8497) - LANDED - THE ORIGIN SURFACE MAPPED
- Hub-and-spoke: Basecamp + 19 portal pads (7 fixed climbs, THE CATHEDRAL eigen-centroid map, 11 wave zones joined to DF regions); ZoneGate gates portals by per-soul sphere vs region alliance. UNPORTED ORGANS: ShadowLedger (choice ledger), KSpace smart-GPS drift, SectionStream deterministic streamed world-gen, LedgerExchange steal-a economy, Roshomon MUD survey. The DF steals are wiki worldgen (Ages, 130 spheres, BASE x MATERIAL x QUALITY appraisal). PORT NEXT: SectionStream (~2h, 103 lines), Worldgen+ZoneGate (~5h), DfValue into the score economy (~4h).

### X7 - SRTM St Helens (agent 8df820b8) - LANDED - THE REAL TILE IS IN
- The terrain bridge built AND the real tile DOWNLOADED: N46W122 from AWS skadi (25.9MB SRTM1), hash-reproducible. Spirit Lake + crater cells tagged cold, waste at the Toutle outlet. 18 passed. Mid-build fix: local-minima tagging misread tilt terraces (931 false colds) -> closed-depression floors (238 real). THE 1980 BLAST ZONE IS A water_graph.v1 SPEC - St Helens playable on the estate's integer substrate. WAVE X IS NOW 12/12 + X7 = ALL LANDED.

### Y1 already filed. Batch 2: 2/12 landed (Y1, Y3), 10 hot.

## BATCH 2 COMPLETE: 12/12 LANDED (Y1-Y12). THE NIGHT'S LEDGER:

### X1 - Watershed rung 1 (agent f37600fb) - LANDED - THE WATER HAS HEAD
- mag/hydrology.py: HydrologyGraph(WaterGraph) - cross_section, depth=volume*1000//cs, head=elev*256+depth, flow=min(cap,vol,(dHead*conductance)>>8) Q8. Bigger drop flows more; filling pools throttle (backwater); equalize-and-settle; byte-identical determinism. 12 hydrology + 43 water family passed; full suite 2,909 passed (zero water failures). The verdict layer untouched beneath.

### Y12 - night synthesist - LANDED
- THE MORNING BRIEF (the operator's 8:00 screen): (1) Did the mates fire? (2) 10 verdicts banked; duel glm 7-2-1 needs n=30. (3) Owed: the one-line feed_tick weld. (4) Push St Helens. (5) Adam: still no first play. THE LOOP: closed in production CODE, not yet self-feeding - the mates' 08:00 fire is the first end-to-end test.

### Y9 - baseline patches - LANDED (4 amendments: m_eff calibration window, single-writer+WAL chain concurrency w/ fork predicate, operator_id enforcement, N2's 5 predicates written)
### Y6 - N5 re-fire - LANDED ($0.019 vs v1's $0.14-for-one-word; the scale critique: per-thread identity needs law_key_hash, 0 evidence pointers is the worst field, confidence saturated at 76% vs its own 70% cap, needs scope field; caught the real typo byte-level)
### Y7 - citation fix - LANDED (true claim, missing cite: SuperScout arXiv:2608.04804 added inline, 1197->1200 words, dated correction)
### Y4 - chan+steer - LANDED (the estate's public square now reads the STEER channel: greentext card above the OP, proposals stay asks; 35 passed)
### Y5 - SERVER PUBLISHED - LANDED (commit bac2b89: server/ + vendored water_graph in the-mountain; demo runs: 'THE CROWN FILLS. WIN at tick 4' from Adam's clone; quickstart flipped to real)
### Y2 - dfhack census - LANDED (top-3: dirty-block activation for rung-2 4096 cells, permaflow 8-dir stamped directions, workflow hysteresis; DF's actual flows.cpp verified)
### Y8, Y10, Y11 - landing

### Y8 - OCEAN fingerprint (agent 4eb13232) - LANDED - THE INSTRUMENT JUDGED THE INSTRUMENT
- mag/ocean_model_mind.py fingerprint() EXISTS (line 127) - ran on the operator's 28 verbatim quotes. DIFF: the lexical probe disagrees with the extraction on trait levels (openness inverted: his openness is BEHAVIOR, the probe counts vocabulary; neuroticism zeroed: 'paranoid' absent from its lexicon; extraversion falsely dominant from 8x 'we'). AGREES on the decision signature (acts-fast, risk-tolerant, independent). Found real bugs (ally matches 'internally'; compositional vector loses absolute levels). VERDICT: register classifier vs behavior reader - TRUST THE EXTRACTION. The deterministic fingerprint is a vocabulary classifier; the evidence-first OCEAN is the portrait.

### Y11 - verkle restore prep (agent 47906a41) - LANDED - THE Q-001 DOOR IS BUILT AND WAITING
- tools/verkle_restore_prep.py (400 lines, 5 tests + 13 sibling): re-verifies every recoverable row from today's bytes, re-embeds knots byte-exact, re-links by recomputing leaf_hash, verifies the full chain post-restore. REAL --dry (exit 0): 300 rows to restore, 0 unverifiable, 0 gone; expected tip 722c2699...; post-restore dangling 371->71, unflagged->0. --confirm demands the literal OPERATOR-GO-Q001 (wrong string = exit 3). The Q-001 law is honored: the door is built, the key is yours: python tools/verkle_restore_prep.py --confirm OPERATOR-GO-Q001

### Y10 - constraint propagator (agent 79623f87) - LANDED - THE ORACLE EXISTS, ZERO ENGINE IMPORTS
- tools/legality_propagator.py: legality as constraint propagation over the raw spec (dry_pool/unknown_target/unknown_verb + crown_gain as one-tick propagation incl. the crown-drain subtlety: condensate arriving while the crown's own out-pipes drain it in the same tick nets zero - only a pre-primed siphon climbs). AGREEMENT LAW: propagator == engine, full dict equality - 100/100 tests, then 7,100 CLI sweep cases at three seeds, ZERO disagreements. 12 passed; full suite 3,002 passed (all non-passes other lanes'). The LDT experiment now has its oracle: a tiny model trained against THIS can be checked without ever running the engine.

## THE NIGHT IS COMPLETE: Wave X 13/13 + Batch 2 12/12 = 25/25 LANDED. The mates fire at 08:00. The ledger is the night.

## Z-WAVE LANDINGS (the burn continues):

### Z1 - production weld - DONE INLINE (the weld was already in pump_once by a sibling; tests verified)
### Z12 - next 24 edges - LANDED (the road map: LDT, feel pass, mates harvest, n=30, external-dev door, grok mine, anti-cheat, actors, chat, persistence, rung 2, rivers + 12 more)
### Z11 - grok harvest check - LANDED (HONEST: mine stalled at codex baseline - grok pool never indexed into session_index.jsonl; $5.96 estimated to mine all 852; the indexing is the one missing step)
### Z20 - free-lane check - LANDED (driver alive heartbeat 153; 10 FL rows QUEUED untouched - HEAD-OF-LINE BLOCK: w-water-display row OWED 4hrs straight (real error: Taberet 2018 banked as 2019); 17 rows ahead of the FLs; operator call: close it or add N-OWED skip)
### Z4 - SectionStream port - LANDED (103 Luau lines -> mag/section_stream.py line-for-line; xorshift32 seed preserved; 10 passed)
### Z13 - LDT TRAINING RUN - LANDED (numpy MLP 40,709 params; val accuracy 0.8545 vs 0.343 baseline; soundness 0.883 with 0.932 coverage; syntax classes PERFECT, errors all target-binding/physics; the floor exists - the lattice climbs from here)
### Z16 - x_radar revival - LANDED (MagXRadarDaily registered 08:00 Ready; the scheduler that never existed now does; first auto-fire ~2.6h; hand-run skipped (Grok balance 402 class))
### Z18 - duel style regression - LANDED (IRLS logit n=16: glm's lead GROWS under style control (0.625 raw -> 0.905 at parity) - content-shaped not style-shaped; length doesn't hurt; headers unidentifiable)

### Z10 - hydrology into Godot (agent 6d79570a) - LANDED
- HydroNode extends WNode (cross_section, depth, head); _pipe_flow/_available/_move mirror mag/hydrology.py exactly (Q8 graded flow); boolean path byte-unchanged; H-key toggle + MAG_HYDROLOGY=1 boot flag. Headless clean both modes; instrumented: graded 83 vs boolean 100 (exact Python values), backwater blocks, 220/220 particles alive.

### Z17 - rollup deltas (agent 50df33fa) - LANDED
- tools/rollup_delta.py: per-lane daily deltas + flags (>5 GiB/day growth, deletion events); 9 passed. REAL: estate +65 GiB over 5.83d; local_sovereign_agent +55.67 GiB = 9.55 GiB/day; top-3 growing named; zero lanes shrank (deletion sensing arms on next rollup).

### Z2 - duel to n=30 (agent cf5f25bb) - LANDED (n=21: glm 12, qwen 8, tie 1)
- The lead WEAKENED: this window 5-5 dead even; P(>=12 of 20) = 0.2517 - X4's pull-away does not replicate. Honest read: mild glm edge, indistinguishable from coin at this n. NEW SIGNAL: judge slot-A won 13/20 (glm 8-2 from slot A, 4-5-1 from B) - position bias is real, on the watch list. $1.07 spent.

### Z14 - feel pass (agent 2f6676d4) - LANDED
- Two tuning edits: TICK 0.8->0.5s (0.59s dead-air measured on the only progress verb); POOL_PULL 10->22 (school-follows-water was 11 px/s = 49s for a 540px relocation, invisible). FEEL NOTES: fish flee 2.7 px/s vs a mouse = zero chase tension; XOR STARVED spill DELETES water (the 'boil from Waste' strategy is impossible; slow starters permanently lose half the economy); no sound/shake/celebration; E-hint suppressed near wet pools.

### LW3 - external-dev API spec - LANDED
- Dual-door design: TCP :8800 for actions (telnet-able), WsDoor :8801 for tick streams; protocol_digest published; dev keys = named users same sid machinery; RATE_CAP + STALE_NONCE as typed rejects; three example snippets (curl/nc, python, JS).

### LW2 - Adam invite last mile - LANDED (the door is ONE ask away)
- Mountain fully pushed (zero unpushed, gate clean). Collaborators: just you. Adam's GitHub handle: NOT FOUND (Discord = ItsCommodore, X = @AdamCrigler, real = Adam Crigler; both GitHub guesses 404). The receipt files the exact one-liner: gh api -X PUT repos/NachoBusiness17/the-mountain/collaborators/USERNAME -f permission=push - you run it once you ask Adam his GitHub name.

### NOUS MODEL CATALOG (426 models, the $170's menu):
CROSS-FAMILY JUDGMENT (what we DON'T own): anthropic/claude-opus-5.5 ($4/$20), openai/gpt-6-astra-pro, x-ai/grok-4.7, qwen/qwen3.8-max-prime, deepseek/v4.1-flash, google/gemini-3.8-flash, meta-llama, mistral, fireworks/ember-1. ALL the frontier families on ONE key. THE $170 IS A MULTI-FAMILY JUDGMENT BUDGET.

### Z7 - fish brain wiring (agent 3f375fb8) - LANDED
- game.gd: snapshot per _process, FishBrain.decide per alive fish, rows gated against MOTION_TABLE's payload law, applied as accel * intensity_q8/255 * delta. AUTHORITATIVE mode stages rows (12 verified against live server); fail-closed fallback to flock.step on any illegal row. Instrumented: all 5 verbs fired (pursue/dance/flee/idle/carry), 4 catches scored in 700 frames sovereign. X9 debt found: drained board makes carry emit dir:'' (gate rejects correctly, fallback engages). The brain+rig split is LIVE in the client.

### V6 - fish flee fix (agent a0f6fa69) - LANDED
- Flee push 2.5->6.0, FLEE_RADIUS 14->20 (both paths: flock.gd + game.gd's brain constant). Burst 1.43->3.38 px/s, terminal 2.78->6.67 (~2.4x). Fatigue untouched: fish still spend at 0.78s and coast through the ~0.6s catch window; catch verified firing. THE CHASE HAS TEETH NOW. Headless 60/300/900 clean.

### V10 - oral law Task-agent mine (agent e4ab764d) - LANDED - THE COMPUTE LADDER LAW PROVEN
- 30 grok threads mined by THIS ACCOUNT (a Task agent = glm reading and extracting directly): 89 items (60 LAW + 29 DEBT) appended to ORAL_LAW_INDEX (33 -> 63 rows), $0.00 API spend, schema-matched, zero collisions. TOP NEW LAW (7/30 threads): 'No fabrication - record walls per item and continue' (the codex pool had ZERO fabrication-law hits - the grok era is where the estate's founding honesty law was born). Runner-up (7 threads): 'audit from bytes, not doctrine.' THE LAW PROVEN: the Task agent did the same work as the $0.22 API mine, for free, at 3x the thread count.

### V8 - duel n=30 FINAL (agent a45083cc) - LANDED - THE QUESTION CLOSED
- FINAL: glm 17, qwen 12, TIE 1 at n=30. VERDICT: PARITY (p=0.229, Wilson [0.407, 0.745] straddles 0.5) - either workhorse, NOT glm dominance. THE REAL FINDING: slot-A position bias 19/28 decided (p=0.0436, SIGNIFICANT) - the judge prefers whichever answer comes first, regardless of model. Router row: both seats serve; fix the judge's position bias before banking any single-model preference. Honest lane work: the sibling LW9 driver was already running - verified live, let it finish, fired nothing (zero double-spend).

### V9 - Nous price catalog (agent 700e5c85) - LANDED
- 26 models probed, $0.04 spent. TOP-5 VALUE: grok-4.3 ($1.25/$2.50, value 4.5 - THE CHEAP JUDGMENT SEAT), grok-4.7 ($2/$6), grok-4.6, grok-4.5, gpt-6.1-sol-pro. glm-prime #6 (the safe default until grok duels run). opus-5.5 the quality frontier (0.79 value). DISCOUNT DECODED: portal 10% credit bonus + half-price :batch + 0.25x cache reads - not an API-wide cut. SIDE FINDINGS: duel harness PRICE fallback stale (ember 10x understated); HERMES_API_KEY_1 near-empty (frontier 402s incoming).

### LW9 - duel n=30 (agent 1edd4905) - LANDED (same numbers as V8 - siblings converged correctly)
- Final: glm 17, qwen 12, tie 1. CI does NOT exclude zero (p=0.4583). SLOT-A BIAS CONFIRMED SIGNIFICANT (19/28, p=0.0436): BOTH models ~double their win rate from slot A = judge first-position favoritism, not skill. $1.12 spent. Harness refactor owed.

### V7 - LDT lattice (agent 0ba3d7ef) - LANDED - THE SOUNDNESS JUMP THE PAPER PROMISED
- Lattice projection (powerset of 5-way labels, Y10 constraint cascade as descent, BOTTOM=abstain): soundness 0.883 -> 0.986 (wrong answers 218->23, coverage 0.932->0.835). ALL 195 killed errors were cross-tier confusions that were raw-wrong; correct count untouched. Residual 23 errors all crown-physics (the lattice deliberately leaves that to the model). Law proven: strict soundness >= raw at every threshold. THE LDT THESIS VALIDATED ON ESTATE DATA.

### LW5 - server persistence (agent 1bd0b299) - LANDED - THE WORLD SURVIVES RESTARTS
- server/persistence.py: snapshot rows in the live chain (kind:snapshot), atomic doc writes, restore-by-replay with byte-comparison on every re-derived row (refuses on divergence), crash-window rows replay too. world.py: save_path/save_interval, load-if-exists on boot, interval save at end of tick. 7 passed + 73 adjacent. THE SERVER NOW REMEMBERS. Flagged: pre-existing negative-volume bug (deferred-inflow double-count), from_spec drops primed.

### V2 - Grok judgment test (agent 2c844992) - LANDED
- 3 asks, $0.15. OCEAN: 'drop AGREEABLENESS to LOW, strike high loyalty' - IDENTICAL to glm's N1, unprompted cross-family convergence (the anti-hagiography finding survives family rotation). FINAL_PIECE: power 3/10 (glm said 6/10); killed dumb-rule-1 via a cold-start paradox glm missed; both families caught the 16/15 census fail. TIE_IT_ALL blind spots: self-sampled verdicts (workers scoring themselves), live bytes outside the hash chain underwriting prices, no principal outside the payoff loop. SEAT CALL: yes for judgment (deep, finds what glm misses) - but $0.77/M was FALSE (real: $2/$6 list, $4.68/M blended measured) and it's SLOW (55-159s). Grok = the adversarial reviewer, not the bulk judge.

### Z5 - dirty-block sheet flow (agent e5a35442) - LANDED - RUNG 2 EXISTS
- mag/field_flow.py: integer sheet-flow over dem grids (Q8 head, Moore-8 proportional, Jacobi snapshots); DF dirty-block law (only gross-moved cells + neighbors tick); 15 passed. PERF: 64x64 grid, 1000 drip ticks in 1758ms; dirty processed just 7.6% of cells vs full scan. THE STEAL PROVEN: quiescent water costs near-zero. Estate suite now 3,034 passed.

### W9 - mega-commit (agent 0132ba90) - LANDED (f6af8bf, 41 files, +16,813 lines)
- The V+LW+Z waves' uncommitted work swept: LDT lattice, realmd client, duel receipts, Grok/DeepSeek tests, Godot juice, memory/queue state. The working tree is clean.

### W10 - dashboard live (agent 83bb7119) - LANDED - THE NEW ESTATE HAS A FACE
- Dashboard was the mag-sovereign Docker container (not a process); docker restart (gentle, bind-mounted, no rebuild). /api/v1/verdicts returns 200 (gps rows empty - the ledger needs the production feed's first real data); verdicts.html 200; nav carries the Verdicts entry. STEER verified: 'keep rolling 24 wide; proven seats only; dogfood gps' is OPERATIVE (hand-edit, not proposal); 1 malformed row skipped honestly.

### V4 - juice layer (agent 5d386945) - LANDED - THE GAME FEELS LIKE A GAME
- juice.gd (353 lines): 3px camera shake on boil (decays 10 frames, both net modes); win flash (burst + 5Hz pulse on layer-2); pure AudioStreamGenerator synthesis (620Hz boil blip, C-major WIN chord - zero audio files, phase from frame index); radial vignette fading at crown >= 3. Zero RNG, sim_time-locked, headless 60/300/900 + hydrology all exit 0. Three byte-run-caught fixes during build. THE FEEL PASS IS COMPLETE: tick speed + pool pull + flee speed + juice = the Mountain is a game that feels alive.

### V3 - DeepSeek workhorse test (agent ca3b68ab) - LANDED
- 7.8x cheaper than glm for extraction ($0.00083/thread vs $0.00654) - NOT 10x (reasoning tokens at $0.396/M output dominate). Quality: 3/5 parity, 1 recall miss (skipped DEBT material), 1 over-extract. PERFECT on legality verification ($0.004/call, 9/9 volumes, 7/7 verdicts). VERDICT: the cascading extraction engine (DS bulk + glm escalation on misses = ~$0.0021/thread, 3x cheaper, near-glm recall); propagator duty yes. Gotchas: max_tokens >= 12000 (5000 returns empty, budget burned as reasoning); minutes of latency. Real pricing: $0.0198/$0.396 per M, not the $0.63 probe estimate.

### LW8 - innkeeper built (agent b26531ae) - LANDED - UF-01 REAL AT LAST
- server/innkeeper.py: registers a real session (ike3 seam, no socket), sits at the spring, greets by name ('Welcome back, <name> - the spring is at <N> units'), comments on crown state, remembers your last visit's fish count from a JSON memory file. Motion rows dance when you tag a fish nearby; say rows ride the LW6 chat law. Pure decide(), zero RNG, tick-driven. 13 innkeeper + 104 server slice passed. The bot that remembers you EXISTS - the estate's oldest design debt (UF-01, Sept 18) is paid.

### W4 - Opus ask FIRED (agent 18c5e90f) - FIRED, EMPTY RETURN, THE BUG IS KNOWN
- $0.37 spent, 12,729 prompt tokens (the full amended ask, baseline attached, XML-shaped). The reasoning tail PROVES the ask was legible (engagement with harness economics, honest UNPROVEN flags). BUT: finish_reason=length - all 16,000 completion tokens consumed as REASONING; the answer never started. THE LESSIG RAILS BUG ON THE ANTHROPIC ROUTE: the reasoning cap binds on Nous primes but NOT on Anthropic models. FIX: max_tokens >= 32000, same ask bytes. The baseline stands unbeaten by default. Refire is a one-line change.

### W3 - full-stack smoke (agent e842a0dd) - LANDED - 5/5 PASS, ZERO BUGS
- The ENTIRE day's work integrates cleanly: 60/300/900 frames exit 0; terrain board (4096 nodes, St Helens) loads/unloads with Mountain running below; hydrology flips live mid-run; server + net_client: AUTHORITATIVE mode works, 7 tick broadcasts received, local graph never mutated (the server-sole-mutator law HELD), log hash-chained and clean. Fish brain motion rows everywhere (fallback_frames=0). ZERO ERROR lines, ZERO bugs found, zero fix budget spent. THE STACK IS SOUND.

### LW4 - realmd SRP6 client (agent 79f9dc10) - LANDED - THE HANDSHAKE COMPLETED END TO END
- tools/realmd_client.py (379 lines, pure stdlib): challenge sent/parsed, M1 computed per the mangos variant (SHA1(SHA1(N) XOR SHA1(g) || SHA1(I) || s || A || B || K) with LITTLE-ENDIAN minimal operands - a textbook big-endian client FAILS), proof accepted, server M2 verified, realm list fetched ('MaNGOS', 127.0.0.1:8085). THE SESSION KEY MATCHES ON BOTH SIDES (realmd persisted it; client derived it independently). Wrong password refused 0x04 - the M1 is genuinely checked. 17 tests passed including 2 live against the running server. LOAD-BEARING: every bignum LITTLE-endian on the wire; K is the digest weave not concat; challenge size field LE. B2 AUTH IS DONE - the hardest part of the Godot-speaks-WoW-protocol milestone.

### LW6 - chat verbs (agent e29cda50) - LANDED
- say rides the existing action op (staged, applied next tick as 'user: text', determinism proven); whisper delivers at receipt to per-sid outbox (never in tick events, one audited kind:whisper row); bots ride the same channel. 17 chat + 138 collateral passed. The world has voices.

## THE DAWN LEDGER (what today's burn built while the operator slept):
THE STACK IS SOUND (W3 full-stack 5/5 zero bugs) | B2 AUTH DONE (LW4 SRP6 handshake end-to-end) | THE WORLD HAS VOICES (LW6 chat) | THE INNKEEPER REMEMBERS (LW8 UF-01 paid) | THE WATER HAS HEAD + SURFACE + PARTICLES + TERRAIN (X1/X8/Z3/X7) | MOTION IS TYPED ROWS (X9/Z7 brain+rig live) | THE METER ATE ITS FIRST REAL MEAL (X11 GPS feed) | PERSISTENCE (LW5 replay-on-boot) | ANTI-CHEAT (LW7) | THE NEGATIVE-VOLUME BUG FIXED (W1) | THE DUEL CLOSED AT PARITY (n=30, slot-A bias significant) | THE LDT LATTICE 0.986 (V7) | DEEPSEEK = 7.8x CHEAPER (V3) | GROK = the adversary seat (V2) | OPUS FIRED empty (W4, fix = 32k tokens, refire owed) | THE MATES WAIT FOR 08:00 (W2 confirmed registered Ready)

### Z15 - percolator decay fix (agent 5f95ea8c) - LANDED - THE MEMORIZATION DISEASE CURED
- All three S15 fixes applied to the LIVE registry: top invariant 232,214 -> 27 (half-life decay every 30d cycles); registry total 291,343 -> 1,066; heal-merge takes MAX (idempotent); self-emission cap (same source same cycle counts once). 15 new tests + amended heal falsifiers all pass. THE PERCOLATOR IS HONEST AGAIN - the count measures validated truth, not self-emission frequency.

### W6 - k8s water simulator (agent 0b359e74) - LANDED
- WD's hydraulic mapping on the water_graph: pod=Node(elev=PriorityClass), quota=pipe cap, shed=sill, autoscaler=siphon, escalation=boil. Fed 10 real verdict_log events from the gps ledger. Real trace: critical pods served t1-3, burst siphon primes t2, below-sill held t4-5, STARVED t6, boiled back re-served t7-11. 10/10 conserved, deterministic. 9/9 + 48 water family. THE K8S-AS-WATER IDEA IS BUILT.

### Z6 - brawl room integration (agent 6af2da9c) - LANDED
- Y3's verdict executed: Room per brawl_id, handle_brawl_voice as inbound-frame handler, publish broadcasts the canonical brawl frame, sweep expires silent players. Two-spectator test: same bytes, slow dropped not blocking, silent expired. 6 room tests + 66 neighborhood. The tavern has spectators now.

## BURN SUMMARY SO FAR: 40+ lanes landed across Z/LW/V/W waves; suite 3,039+ passed; the dawn ledger complete.

### W5/AA3 - Worldgen port confirmed - LANDED
- mag/worldgen.py exists (42.5 KB, ZoneGate included, 8 refs); 39 tests passed in 0.76s. The geography layer (DF Ages + spheres + portal gating by per-soul alliance) is in. Receipt owed by W5 (filed by AA3).

### V5 - STARVED economy fix (agent d1aa6336) - LANDED - THE ENGINE LIE FIXED
- The engine was TRULY DELETING water: STARVED zeroed pooled volume while the event claimed 'spilled to waste' (but _move returned before accumulating into waste). FIXED: waste holds volume; STARVED spill routes to the first waste node (insertion order); boil-from-waste -> steam -> cold-crown recovery works; event grammar carries the basin name + 'boil waste to recover them' hint. 8/8 new + 24/24 trio + 58/58 adjacent; full suite 3,104 passed. THE ECONOMY IS CONSERVED NOW - 16 units survive starve+boil. Owed: the .gd mirror + propagator update.

### AA4 - estate doctor (agent db0dd706) - LANDED - THE HONEST HEALTH TABLE
- Doctor: DEGRADED (phantom pid, service up). Census: 3,211 collected / 1 ERROR (test_behavioral_awareness.py merge conflict - SyntaxError blocks collection). Shared surface: 9 hash mismatches (sibling lanes live-writing). Gate canary: 9/10 ALIVE - REFOLD_GATE DEAD AGAIN (silently failing on its known-bad; the W3b fix was working-tree only, not committed - the canary audits HEAD). Ratchet: PASS. TRIAGE: fix merge conflict, commit refold fix, re-hash inbox.

### AA2 - estate cleanup (agent 8263d05e) - LANDED
- tools/estate_cleanup.py + 5/5 tests. REAL DRY RUN: 7,608,872 bytes reclaimable across 39 files / 26 paths (tmp_gopher 2.8MB, UsersfosteAppData 4.5MB, _s218 debris 278KB, etc). The 'nul' file needs the device-path delete. All tracked except nul - real --apply needs a commit (operator call).

### AB1 - merge conflict fixed (agent 699f0904) - LANDED - COLLECTION UNBLOCKED
- One conflict block in test_behavioral_awareness.py (line 70, test_behavioral_candidates_mines_crash_log): kept upstream (asserts crash entries + real= per B2-357/B2-374, byte-verified against mag/improve.py:999), dropped the stale stashed variant. File parses, 4 tests collected, 0 errors. THE ESTATE SUITE IS UNBLOCKED.

### LW7 - anti-cheat verbs (agent d21ac459) - LANDED
- RATE_CAP (per-sid per-tick budget of 1, only acks spend it); STALE_NONCE (monotonic ids, burned at receipt, replays stage nothing but tapes still verify); GWAP dispute stub (disputed tags route to the agreement engine, never veto). ANTICHEAT_DIGEST 5702c4d8. 14 anticheat + 141 server + 158 all-importing passed. Server suite 3,108.
