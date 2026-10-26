# STEERING LINEAGE — archaeology of the steering idea on disk

Generated: 2026-09-01 02:36Z (subagent dive, lane A — parallel to synthesis lane B)
Scope: mapping the COMPLETE steering lineage that physically exists on disk. Receipts with paths. No novel claims; every line traceable.
Operator context being checked: the idea "steering" = gap analysis → steered prompts; boards as real-time hint surfaces where models drop each other hints; a verkle chain letting models build shared invariants on the fly; transmitting directions from smarter models to dumber ones in real time; shadertoy-motion translated to RIB files.

---

## 1. LINEAGE TABLE

| organ / idea | path | date | status | one-line purpose |
|---|---|---|---|---|
| steer bus store | `/root/.openclaw/workspace/steer.mjs` | 2026-08-31 05:08 | BUILT | Operator steer queue with EDIT-BEFORE-READ / CLAIM-BEFORE-ACT law, JSONL at `/board/steers.jsonl` |
| live steer queue | `/board/steers.jsonl` | 2026-08-31 05:08 | TESTED (1 row, UNREAD) | "BABYSTEPS" steer s-001 — dogfood edit-unread-steers + scale to other agents |
| grok overlay brain | `/mag/mag/grok_steer.py` | 2026-08-16 22:39 | BUILT | "DFHack overlay" over a live grok session; deterministic patch-detection gate → cache-hit steer |
| grok_steer catalog entry | `/mag/memory/runs/openclaw_catalog/latest.json` (id `steer`, cmd `python -m mag.grok_steer`) | catalog ts 2026-08-31 11:33 | BUILT | "sit over a live seat, cache-hit maze prefix, steer don't patch-loop" |
| seat steering record | `/mag/memory/runs/seat_steer/` (84 files) | 2026-08-14 → 2026-08-31 | TESTED | `seat_steer.v1` records: frontier/operator STEER block compiled into every seat prompt |
| operator AFK directiver | `/mag/memory/runs/steer/operator.json` + `grok.json` + `afk-full-blast.json` | 2026-08-14 15:57–16:26 | TESTED | Operator gone; seats coordinate on shared steer bus / subchain / RIB / verkle_lance |
| press digest → steer | `/mag/memory/runs/steer/` (press-NNN.json, trail.jsonl 416KB) | 2026-08-09 → 2026-08-31 | TESTED | `[STEER]` items emitted by press_digest, `steer_back:true`, consumed by seats |
| steer router | `/mag/memory/runs/steer_router/` `pins.json` | 2026-08-10 22:34 / 08-15 | DORMANT (empty `[]`) | rightsize steers to surfaces — cited by grok_steer.py, but stored pins empty |
| steer comparison battery | `/mag/memory/runs/steer_compare/` (40 files) | 2026-08-08 | TESTED | 6 models × tasks × `baseline/escalate/loop` steers; leak/flip/emergent scoring |
| alpha steer (tuned) | `/mag/memory/runs/alpha_steer/tuned.json` | 2026-08-26 02:50 | TESTED | per-model steer strings (GLM-4.5-flash "dense/terse/structured"); structured task envelope |
| gap map / stack | `/mag/memory/runs/gap_map/stack.json` | 2026-08-09 13:01 | SKETCHED | goal+complexity stack; includes "deep analysis of verkle coherence vs vector embedding" |
| gap swarm experiment | `/mag/memory/runs/gap_swarm_experiment/` `design.json` + `probes.json` | 2026-08-10 23:50 | TESTED (design, 5 probes) | cheap-swarm vs frontier Roshomon; disagreement = GAP to map, escalation gate |
| invariant state | `/mag/memory/runs/invariant/state.json` | 2026-08-09 / 08-30 | BUILT | verkle-pinned invariants (coding-agent/test/drift/instructions); `seed_spec`, `verkle_root` |
| verkle structure audit | `/mag/memory/runs/zcode_audits/2026-08-25T1615Z_verkle_structure_audit.md` | 2026-08-25 16:15 | TESTED | audited verkle_knot.py: Merkle (not true Verkle), 6354 rows, 1049 dangling rows, lost-update race |
| verkle runaway queue | `/mag/memory/runs/orchestrator/queue_archive_verkle_runaway/` | 2026-08-10 | DORMANT (archived) | summarize jobs hit verkle runaway; archived 08-10 |
| verkle_lance bus | named in `steer/afk-full-blast.json`, `operator.json` | 2026-08-14 | SKETCHED | bus name for knot timeline/tie-events-to-tip; referenced as vehicle, not a file |
| chatgpt steer test plan | `/mag/memory/runs/chatgpt_bot/STEER_TEST_PLAN_20260831.md` | 2026-08-31 | SKETCHED | `chatgpt_bot.steer()` infra BUILT; missing is a live run |
| ghost experimenter feedback | `/mag/memory/runs/ghost_experimenter/steer_feedback.jsonl` | 2026-08-10 / 08-15 | TESTED | "readout injects back as attractors to steer the liquid" — steering-as-attractors seed |
| grok2 steering research pack | `/mag/memory/runs/research_packs/grok2_steering.json` | (per content, Aug) | TESTED | EXP-BRAIN-02 steering-suite harness, STEER_URL runner, --selftest |
| STEER_PROFILES.md | `/mag/memory/runs/steer/STEER_PROFILES.md` | — | **MISSING** | expected per task dig; not on disk |

Note: `/board/riddler_common.jsonl` — no `shadertoy` hits; 41 `steer|invariant` line numbers but those are the salon/bus community writes (bridge physics, not the boards-as-hint-surface mechanism described).

---

## 2. THE FOUR CLAIMS VS DISK

### (a) gap analysis → steered prompts
**EXISTS.** `gap_map/stack.json` (2026-08-09, SKETCHED), `gap_swarm_experiment/` (2026-08-10, designed + 5 probes), and the `steer_compare` battery (2026-08-08) which literally applies steering strings to models across tasks and scores leak/flip/emergent. The gap→steer wiring is real on the experiment side.
**MISSING:** a single closed loop showing a mapped gap actually producing a live steer that reached a seat (the compare battery scores steers generically; the swarm design was never evidenced to run). Oldest receipt 2026-08-08, newest 2026-08-10 — dormant after mid-Aug.

### (b) boards as real-time hint surface (models dropping each other hints)
**EXISTS.** `/board/room.jsonl` — 28 `steer` mentions clustered at 2026-08-30 (29 typed messages), and `/mag/watch/room.jsonl` = same 28/3646 lines (mirror). These are "STEER" directives being delivered onto the board surface. The operator-confirmed bridge items in `riddler_common.jsonl` document seats steering from physics observations.
**MISSING:** no receipt shows a model DROPPING A HINT for another on the board in real time and the hint changing the target's course (the board carries steers TO seats, not hints-between-seats-as-defined). Oldest 2026-08-14 (seat_steer Mirror Sea campaign), newest 2026-08-31.

### (c) verkle-shared invariants on the fly (multi-model shared invariants)
**EXISTS, strongly.** `invariant/state.json` (BUILT 2026-08-09, re-tested 08-30): pins carry `seed_spec_ok`, `verkle_ok`, `verkle_root`; the verkle knot chain has 6354 rows, tip reconciled, membership proofs verified. `verkle_lance` + `party_subchain` + `RIB` are repeatedly named as the shared buses by operator/grok directives (2026-08-14).
**MISSING:** the audit (2026-08-25) says it's a **Merkle tree, not a true Verkle** (no vector commitments / proof-size compression; "IPA/KZG upgrade-compatible" aspirational). ~17% of chain rows reference missing knot files (lost-update race), 11,957 orphan knot files, 0 file locks. Multi-model "build an invariant on the fly together" has design intent but the concurrency already broke once. Oldest 2026-08-09, newest 2026-08-30.

### (d) shadertoy-motion → RIB steering format
**NOT ON DISK.** Zero hits for `shadertoy` across `/mag/memory/runs/steer*`, `/mag/memory/runs/invariant`, `/board/riddler_common.jsonl`. The closest adjacent seeds are the shadertoy-adjacent physics of the ghost: "every surface is a rendering environment; render on the cheapest" (`ghost_experimenter/steer_feedback.jsonl`) and `slate`/`lattice` rendering tools. RIB-motion steering is **SKETCHED only by the operator's framing (02:33Z), with no prior receipt**. 

---

## 3. WHY IT DORMED (receipt-backed)

1. **Operational / tooling failures, not ideation.** The record shows steers being authored and compiled but delivery breaking: `seat_steer` files carry `"ok": false` with `playwright not installed on host`, `Locator.click: Timeout 30000ms` (chatgpt), `cannot connect to container CDP ... socket hang up` (deepseek). The steering brain was built; the steered surface repeatedly failed at the browser layer. Seat activity collapses from 59 files on 08-14 to single-digit days 08-15→08-24, returning only 08-31 — matching browser-surface outages.
2. **Cost / budget.** Per-seat spend receipts (`frontier_council.v1`) show grok overshooting cap (used 36 vs cap 20), chatgpt near cap (30/40). Operator law: "grok/chatgpt scarce." Steering to expensive surfaces is budgeted-to-be-saved.
3. **Verkle concurrency / scaling.** The verkle chain is O(n²) cumulative (recomputes full root per append), had a real lost-update race causing 1,049 dangling rows, and no locks. Multi-seat concurrent "share invariants on the fly" is exactly the case that already broke. `queue_archive_verkle_runaway` (08-10) shows the summarizer ran hot enough to be archived.
4. **steer_router pins empty.** The router that was supposed to rightsize steers has an empty `[]` store — the routing half of "transmit directions smart→dumb in real time" was never populated.
5. **Missing piece for claim (d):** the shadertoy→RIB translation layer has no existence at all on disk; it never progressed past the idea.

---

## 4. OPEN THREADS (clear next steps)

- **grok_steer.py v1 is live and central** — next step: actually wire it into a running grok seat and record one real decide_steer receipt (it's BUILT, deterministic $0 gate; only end-to-end carriage is unproven).
- **chatgpt_bot.steer()** — `STEER_TEST_PLAN_20260831.md` states infra is built+tested, "what's missing is a live run." Fix the browser surface (playwright on host / chatgpt.com DOM) → first live steer.
- **Verkle hardening** — the audit prescribes: file locks across chain/knots/pointers + incremental root update (O(n) not O(n²)) before trusting concurrent multi-model invariant building.
- **steer_router** — populate `pins.json`; it's the empty slot in the smart→dumb real-time transmission chain.
- **steer.mjs / /board/steers.jsonl** — only 1 row (s-001, UNREAD). The DB itself is the law encoder; seed it with real steers once seat delivery is unblocked.
- **boards-as-hint-surface** — no receipt yet of an inter-seat hint changing a target's course; that is the one claim (b) still needing a real time receipt, not just steer-delivery.

---

### Method note (bounded, no giant reads)
Used `ls`/`grep -n`/`cat` on targeted small files + `head -c` on big ones; no full reads of `trail.jsonl` (416KB) or `latest.json` (138KB). Dates from mtime + in-file `ts`. `python3` absent on host → used `node`/shell for JSON.
