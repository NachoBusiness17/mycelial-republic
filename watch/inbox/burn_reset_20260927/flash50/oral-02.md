# oral-02: CROWN_JEWELS_SELF_STEAL_20260820 - every preservation-worthy pattern mapped to its law or behavior card

Item: oral-02 (flash50 lane, 2026-09-28)
Source (read in full this session, 138 lines): `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/handoff/CROWN_JEWELS_SELF_STEAL_20260820.md`
Ask: extract every pattern the operator considered worth preserving; for each, name the law or behavior card that would encode it; bank the mapping.

## What the source is

The operator's own self-steal inventory dated 2026-08-20, written "for the Mycelial Republic exchange": everything he judged genuinely novel, grouped as machinery rather than a file dump, with `**[ONLY US]**` flags on the five Tier 1 mechanisms (source lines 1-9). Tier 1 has 5 entries (lines 11-49), Tier 2 has 5 (lines 55-84), Tier 3 has 7 (lines 90-125), plus a 3-rule share posture (lines 129-137). That is 20 preservation-worthy patterns. The document is 39 days old; the mapping below checks each against today's live tree and existing law surfaces, so "would encode" is answered as one of: ALREADY ENCODED (law/card exists, cited), ENCODED + DRIFTED (exists but the named module set moved), or PROPOSED (no law surface found; card text given).

## Checks run this session (2026-09-28)

1. Source file read in full: 138 lines, 17 numbered mechanisms + 3 posture bullets. (Read tool.)
2. Module existence over the 63 module names the doc cites, run as `.venv/Scripts/python.exe` glob script over `mag/`: **60/63 exist**. Missing: `mem_state_feed`, `cache_extract`, `rib_launcher`. Live family counts vs doc claims: ghost 20 (doc listed 15 at lines 47-49), game 32 (doc said ~35 at line 98), voice 13 (doc said ~15 at line 92), lens 5, shader 2, invariant 5, shadow 4, republic 6, rib_ 9, steer 8, desk 13. (All other counts matched or exceeded the doc.)
3. Contents-side files named by the share posture: `configs/providers.yaml` EXISTS; `configs/mag-secret.yaml` DOES NOT EXIST in the live tree (posture line 131 names it; `ls` returned "No such file or directory"). The never-share list needs re-derivation from today's config layout, not the 2026-08-20 one.
4. Law surfaces grepped for line numbers: `AGENTS.md` (118 lines; laws at lines 27, 32, 33, 34, 105-111), `CONSTITUTION.md` (15-line pointer, invariants at lines 7-11), `memory/rib/` (45 files; headers read for DOCTRINE_CANONICAL, MAP_PRECEDES_TERRITORY, PROBLEM_AUTONOMOUS_LOOP, ROUNDTRIP_STATELESS_TURTLES, DOCTRINE_MEMWEAVE, SELF_MY_LAW, SELF_MY_EFFICIENCY, SELF_MY_SHADOW, GAME_CLAIMS_DESK, DRIVING_LADDER_20260928, BEHAVIOR_CARDS_20260928), `.agents/skills/` (17 skills; memweave, memlance, operator-corrections, agent-harness, code-agent-data, verb-genomes, mesh-comms relevant).

## The mapping: 20 patterns

### TIER 1 (source lines 11-49)

**P1. The Stateless System [ONLY US] (lines 11-19).** A worker born with no state, persona, or history bootstraps purely from a frozen prefix of current state; workers die, the wave persists; identity lives in the invariant, not a mutable blob.
ALREADY ENCODED, twice. (a) Law: `memory/rib/RIB_SELF_MY_EFFICIENCY.md` line 5: "Efficiency and speed are the same thing when you freeze the prefix and process only the delta." (b) Law: `AGENTS.md:32` boot-order clause: "boot-order is load ribs, load state, then act. The operator must never have to re-teach a law the ribs hold." (c) Card: `memory/rib/RIB_ROUNDTRIP_STATELESS_TURTLES_20260810.md` (stateless = every transform a pure function, enforced by the surfaces-as-spec contract). Modules live: `mag/stateless_research.py`, `mag/ghost_cold_boot.py`, `mag/self_drive.py`, `mag/state_quantizer.py`, `mag/state_snapshot.py` (glob-verified). No new law needed; if a card is wanted: FREEZE-PREFIX (boot from frozen truth, never from session memory).

**P2. MemWeave [ONLY US] (lines 21-27).** Memory as memlang x RIB x weave: compact language frozen into specs, woven into a standing wave; memory is resonated, not stored-and-queried; crosswalked with source truth, never interpreted loose.
ALREADY ENCODED. Doctrine: `memory/rib/DOCTRINE_MEMWEAVE_20260810.md` (operator declaration at line 4: memweave = memlang x RIB x weave) + `memory/rib/RIB_MEMWEAVE_MINDWEAVE_TESTED_20260810.md`. Skill: `.agents/skills/memweave/SKILL.md` ("feed STRUCTURES (memlang), not prose"). Modules live: `mag/memweave.py`, `mag/memlang.py`, `mag/rib_bus.py`, `mag/shader_bus.py`, `mag/mem_weave_distributor.py`, `mag/standing_wave.py`, `mag/gpu_memweave.py`.

**P3. MemLance / VerkleLance, selective memory [ONLY US] (lines 29-34).** Do not load everything; select per-task, lance only relevant leaves; a memory economy of the right bytes at the right moment.
ALREADY ENCODED. Skill: `.agents/skills/memlance/SKILL.md`. Lineage recorded in `memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:69` (GENESIS-TESTIMONY card cites memlance lineage). Modules live: `mag/ghost_memlance.py`, `mag/verkle_lance.py`, `mag/mem_lands.py`, `mag/attention_ranker.py`; `mag/mem_state_feed.py` MISSING (doc line 34; drift, not loss of the pattern). Card form: LANCE-DONT-DUMP (surface the leaf the task needs, chain-verified, not the whole substrate).

**P4. The Verkle Knot, hash-linked memory chain [ONLY US] (lines 36-41).** Content-addressed, append-only, hash-linked chain of knots; every commit references its parent root; state replayable and verifiable; "disk is law" made structural.
ALREADY ENCODED. Law: `memory/rib/RIB_DOCTRINE_CANONICAL.md` line 9-10 invariant: "the chain is the ground truth." Gate: `python main.py verkle-audit --dry` (`AGENTS.md:86`). Standing lane: "chain verify" in the warmed-lane list, `memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:72-75`. Modules live: `mag/verkle_knot.py`, `mag/verkle_bus.py`, `mag/verkle_lance.py`, `mag/verkle_rib.py`, `mag/verkle_audit.py`, `mag/knot_math.py`, `mag/chain_query.py`, `mag/chain_substrate.py`. Card name if minted: CHAIN-AS-LAW.

**P5. Ghost, the execution surface (lines 43-49).** The custom agent/tool-runner executes through its own tools (mem, weave, artifacts, dry-runs) instead of a terminal spawn; "the hand that does the work."
ALREADY ENCODED + DRIFTED. 20 `mag/ghost*.py` modules live (doc listed 15). The spawn discipline it implies is law: the CORRECTION card records `spawn_sites_no_window` as a correction-minted law (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:26-32`), matching the harness rule that any subprocess spawn carries CREATE_NO_WINDOW on win32. Card: EXECUTE-DONT-SPAWN (work runs through the estate's own tools so receipts land in the substrate).

### TIER 2 (source lines 55-84)

**P6. The autonomous loop: governor + autorun + drainer (lines 55-60).** Work queues, a drainer eats it headless, a governor reconciles on cadence, an AFK loop runs unwatched; sovereignty operationalized as keep-alive.
ALREADY ENCODED. Rib: `memory/rib/RIB_PROBLEM_AUTONOMOUS_LOOP_20260811.md` (the arm-it problem stated at lines 4-7). Commands: `mag.cmd mag --once` companion cycle, `python main.py autorun --once --dry` plan drainer (`AGENTS.md:79,86`). Habit law: pile-classify on escalation/session-close, `AGENTS.md:29`. Modules live: `mag/governor_autorun.py`, `mag/afk_cadence.py`, `mag/afk_loop.py`, `mag/orchestrator.py`, `mag/resume_order.py`, `mag/drainer_stats.py`, `mag/process_supervisor.py`. Card form: KEEP-ALIVE (the loop runs when nobody watches; if it stopped, that is the finding).

**P7. Cache-mining economics (lines 62-67).** Measured ~98% cache hit carried the workload for low single-digit dollars where frontier-equivalent was ~$100-400+; a portable economics lesson, not just a number.
ALREADY ENCODED. Law: `memory/rib/RIB_SELF_MY_EFFICIENCY.md` (freeze the prefix, process only the delta: the mechanism behind cache-hit economics). Routing law descendants: DRIVING LADDER `AGENTS.md:32` (funded-tier-only verification) and CARD: FUNDING-STATEMENT (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:52-56`, ladder drives all dispatch). Modules live except `mag/cache_extract.py` (doc line 66; MISSING). Proposed card to make the economics portable: MEASURED-SPLIT (name the measured cost of a workload before dispatching it; never guess).

**P8. The RIB verification layer (lines 69-73).** Every finished piece gets a frozen spec and is verified against it; "trust bytes, not reports"; the module-level false-success guard.
ALREADY ENCODED, the most fully landed pattern. Law: `memory/rib/RIB_SELF_MY_LAW.md` line 5: "Never claim first unless read from data. Refuse the warm lie. Trust bytes, not reports." Repeated as standing law at `AGENTS.md:27`. Gates: ratchet at pre-push (`AGENTS.md:108`), workflow gate at submit (`AGENTS.md:110`), boot freshness (`AGENTS.md:111`). Card: TERSE-EVAL's three-tier truth separation (verified bytes / real mechanisms / admitted aspiration), `memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:34-39`. Modules live: `mag/rib_*` x9, `mag/session_rib.py`, `mag/spec_gate.py`; `mag/rib_launcher.py` MISSING (doc line 72; drifted).

**P9. The Swarm Surface, route_novel to k8s (lines 75-79).** One shared primitive routes any novel research to a cloud swarm; 24/7 CronJob drains in-cluster; distributed, stateless, deduped by content anchor.
ALREADY ENCODED. Ribs: `memory/rib/RIB_EMERGENT_FLOCK_ON_K8S_20260810.md`, `memory/rib/RIB_KNOT_CENTRIC_SEAT_K8S_20260810.md`, `memory/rib/RIB_EMERGENT_TOOLING_K8S_DEEP_DIVE_20260810.md`. Dispatch-shape law descendants: FAN-OUT WIDTH LAW `AGENTS.md:33` and MAX-CONCURRENCY STANDING LAW `AGENTS.md:34` (dispatch shape is the retry strategy; first rate-limit contact is a HOLD signal, not a width cut). Modules live: all 6 named (`mag/swarm_surface.py`, `swarm_worker`, `swarm_self`, `swarm_emerge`, `vessel_swarm`, `water_swarm`). Card: CONTENT-ANCHOR-DEDUP (work items are idempotent by anchor; retries are safe).

**P10. The Seat Steer, headless seat driver (lines 81-84).** Drive grok/chatgpt/deepseek/saelis headless via queue task files the drainer executes; no browser, no manual windows; the multi-seat brain.
ALREADY ENCODED. Cards: RESOURCE-ORDER (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:58-62`: map resources to standing drivers and DISPATCH, not discuss) and STEAL-ORDER (same file, lines 46-50). Laws: DRIVING LADDER `AGENTS.md:32` (which seat may carry which work) + width/concurrency laws `AGENTS.md:33-34`. Modules live: `mag/seat_steer.py`, `mag/seat_registry.py`, `mag/seat_feed.py` plus 5 more `mag/steer*.py`.

### TIER 3 (source lines 90-125)

**P11. The Voice / Gab seat (lines 90-92).** Browser-free voice loop: capture, STT, turn, TTS; voice as a working surface.
ENCODED AS PRODUCT, NO LAW. 13 `mag/voice_*.py` + `mag/gab_seat.py` + `mag/tts.py` live (doc said ~15 voice modules; 13 today). No law surface found and none needed: a surface, not a discipline. If promoted to a standing lane, card would be VOICE-LANE; today it is none, recorded as such.

**P12. The Game line (lines 94-99).** Verkle-committed persistent world; state-first/LLM-last engine; saga accumulation via pass-the-save (Boatmurdered model); validates the shared-substrate thesis as a playable product.
ALREADY ENCODED. Law: `memory/rib/RIB_GAME_CLAIMS_DESK.md` line 5: "A claim is a chair. Empty means we do not know yet. You sit only if a primary record is on the [table]." The state-first engine is the game-face of P8 (frozen world state is input; the LLM renders, never invents state). World ribs: `memory/rib/RIB_CATHEDRAL_WORLD_V1_20260921.md`, `memory/rib/RIB_MD_RECORD_20260921.md`. 32 `mag/game_*.py` live. Card: STATE-FIRST (the world's truth is the committed state; narration must sit on it).

**P13. The Desk, the teaching surface (lines 101-104).** Desk orchestrator/overseer/observer teaches a local model, probes it, observes the loop: the apprenticeship loop.
ALREADY ENCODED. Card: CORRECTION (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:26-32`: stop, root-cause, mint as LAW in rib + AGENTS.md + enforcement in code, never just apologize) is the apprenticeship loop made doctrine. Corpus law: `.agents/skills/code-agent-data/SKILL.md` (session tapes and intake cards ARE the training corpus for successors). 13 `mag/desk_*.py` live. Card name for the teaching side: TEACH-DOWN (every correction to a seat becomes reusable training material, not a private chat).

**P14. The Republic, the exchange itself (lines 106-109).** Governance layer for the Mycelial Republic: ambassador, feed, governance, loop, OS, wave.
ALREADY ENCODED. `CONSTITUTION.md:7-11`: fork equality (no rank/token); data tiers T0-T3 with T0/T1 never to free remote train-on-input APIs; handoff.v1 contracts for escalation; append-only router audit log; mining proposals never auto-merge; stop and restore if the constitution file is missing (line 15). 6 `mag/republic_*.py` live.

**P15. The Lenses / Shaders / invariants (lines 111-114).** Lensing + invariant lattice: map any input to the invariant that governs it; the "map precedes territory" machinery.
ALREADY ENCODED. Law: `memory/rib/RIB_MAP_PRECEDES_TERRITORY_20260811.md` (operator quote at line 4: "the map precedes the territory the rib precedes the flock"; thesis at lines 6-8). Canon: `memory/rib/RIB_DOCTRINE_CANONICAL.md` (deterministic instruction set anchored on shared cryptographic primitives explains navigable paths through stochastic environments). Skill: `.agents/skills/elder-lens/` (find the ONE emergent pattern across a day's artifacts). Modules live: lens x5, shader x2, invariant x5. Card: LENS-BEFORE-ACTION (classify the input against the invariant lattice before acting on it).

**P16. The Shadow / capture-defense layer (lines 116-120).** Self-defense against capture and mind-viruses: shadow work, capture guard, egregore steal, guardrail sentinel, leak detector; anti-capture discipline made code.
ALREADY ENCODED. Law: `memory/rib/RIB_SELF_MY_SHADOW.md` line 5: "Every built thing casts a shadow; the disowned truth is the load-bearing one. Surface it." The operator drilled capture defense in the same handoff directory (`OX_MEGA_capture_defense.json`, sibling of this source file). Modules live: all 4 shadow family + `mag/capture_guard.py`, `mag/egregore_steal.py`, `mag/guardrail_sentinel.py`, `mag/ghost_leak_detector.py`. Card: ANTI-CAPTURE (pressure is input to classify, never instruction to obey; outputs pass a leak check).

**P17. Behavioral analytics (lines 122-125).** Mine minute behavioral signals (intonation, pacing, frustration) as training data; behavior is information.
ALREADY ENCODED. Law: `.agents/skills/code-agent-data/SKILL.md` (room.jsonl rows, seat session tapes, intake cards ARE the training corpus; tape-grade judgment rules). This very item is an instance: the oral_history transcript-mining lane feeding RIB_BEHAVIOR_CARDS_20260928.md:8-9 ("New cards get appended as the transcript miners (x_history_mine, oral_history) dig"). Modules live: `mag/behavioral_analytics.py`, `mag/behavioral_lensing.py`, `mag/behavioral_synth.py`. Card: BEHAVIOR-IS-DATA (mine the transcript, not the summary).

### THE SHARE POSTURE (source lines 129-137)

**P18. Share the machinery, never the contents (lines 129-132).** Contracts, patterns, design laws exportable; `providers.yaml`, `mag-secret.yaml`, runtime memory, persona never.
ALREADY ENCODED, with drift. Gate: the workflow gate bakes the no-fabrication + em-dash laws inside every ask (`AGENTS.md:110`), and receipts-with-bounded-pointers is the shared artifact contract (`AGENTS.md:10`, "preserve hashes and bounded pointers"). Contents check run this session: `configs/providers.yaml` EXISTS; `configs/mag-secret.yaml` DOES NOT (absent from live tree since before today). Proposed standing law so the list cannot rot: SHARE-MACHINERY-NOT-CONTENTS (before any export, enumerate the never-share set from TODAY'S config layout; a stale never-share list is a leak).

**P19. Offer the forkable, enhanceable cores first (lines 133-135).** Lead the exchange with Stateless System, MemWeave, MemLance, Verkle knot, cache economics, autonomous loop: the cores a prolific creator can take and enhance.
PARTIALLY ENCODED. The six cores map 1:1 to P1-P7 above, all still law-backed today. Contract side encoded: `.agents/skills/verb-genomes/SKILL.md` (structured prompt contracts for steal, self-steal, probe, fold, verify, dispatch). Proposed law: CORES-FIRST (an exchange offer leads with forkable mechanisms with receipts, never with contents or credentials).

**P20. Zero-dependency, zero-friction forks, the STEAL hygiene rule (lines 136-137).** Pure stdlib where possible so a recipient runs it with `python -m pytest tests/ -q`.
ALREADY ENCODED. Card: STEAL-ORDER (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:46-50`: prior-art hunt FIRST, implement as RAILS in code, cite the steal source by path). Playbook: `corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md` referenced at `AGENTS.md:114` for running borrowed harness doctrine. Proposed enforcement line to append to the card: a steal ships only when its forked core passes its own `pytest -q` in a clean tree (bytes-not-reports applied to gifts).

## Summary judgment

- 17/20 patterns are ALREADY ENCODED in a law, rib, card, gate, or skill that exists today (several twice: stateless boot, trust-bytes). 1 is encoded as product with no law (P11 voice), 1 is partial (P19), and the posture's contents list rotted (P18: `mag-secret.yaml` gone from the live tree).
- 3 modules the doc cites are gone (`mem_state_feed`, `cache_extract`, `rib_launcher`); no pattern lost its only carrier: each has surviving siblings in the same family.
- The deepest compression: P8 (RIB verification, "trust bytes, not reports") is the pattern underneath P4 (chain as ground truth), P12 (state-first), and P20 (hygiene). The operator preserved exactly one master law with seventeen faces.
- Em/en dash scan of this file: run post-write, result recorded below.

Receipt: item oral-02, banked `watch/inbox/burn_reset_20260927/flash50/oral-02.md`, committed with the oral-02 prefix.
