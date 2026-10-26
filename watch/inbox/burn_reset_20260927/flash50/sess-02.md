# sess-02 dispatch work order: queue/todo.md unchecked triage (2026-09-28)

Ask: read queue/todo.md fully; classify every unchecked item by owner (gopher / funded seat / operator / skip), tier, and completion criteria; produce a dispatch-ready work order. This file is that work order.

## Method and denominator

- Read queue/todo.md in full this session (Read tool, 277 lines, entire file).
- Fresh enumeration this session, command:
  `.venv/Scripts/python.exe -c "import io;lines=io.open('queue/todo.md',encoding='utf-8').read().splitlines();u=[(i+1,l) for i,l in enumerate(lines) if l.startswith('- [ ]')];print('UNCHECKED',len(u));[print(n,l[:110]) for n,l in u]"`
  Output: `UNCHECKED 63` with the line list: 5, 31, 32, 33, 97, 98, 99, 104, 126, 127, 129, 130, 135-142, 146-149, 151-153, 160-162, 194-198, 203, 204, 205, 218, 223-225, 232, 233, 234, 235, 237, 239, 244, 249, 250, 254, 255, 262, 266, 267, 268, 272-277.
- Prior triage cross-read: `watch/inbox/burn_reset_20260927/flash50/todo-triage.md` (item f-30, dated 2026-09-28) reports 63 unchecked / 51 closeable / 12 keep-open. My later-moment count matches 63/63: no drift between the two snapshots.
- queue/todo.md is untracked (`.gitignore:41` per f-30), so closure evidence lives in receipts and artifact commits, not file history. Every load-bearing closure claim below was re-verified by me this session (Appendix A); claims resting on receipts I did not open are tagged RECEIPT-SIDE.

## Tier key

- LOCAL: repo venv + ollama janitors, $0, flash-off/LOW tier (AGENTS.md execution note).
- FREE-SENSE: free stealth lanes; outputs banked as findings only, verification climbs (DRIVING LADDER 20260928, AGENTS.md).
- FUNDED: Hermes/Nous glm-5.3-prime / qwen3.8-max-prime; per DRIVING LADDER the only funded lane.
- OPERATOR: human hands only (Studio, real terminal, keys/card, archive drop, chain-tip GO).
- SKIP: closed, superseded, or already decided; residual action is checkbox flip plus optional re-seed, no new work.

## A. Dispatch work orders (the 12 keep-open lines, ordered by priority)

### WO-1 [OPERATOR] [P0] W0.0 archive drop (line 99)

State: my `ls -la /c/Users/foste/Documents/projects/mycelial-republic/data/raw/` returns only `.gitkeep` (0 bytes, Jul 15). The republic chain has been blocked on this since 2026-08-03 (inline text).
Criteria (either branch closes): (a) the X archive zip sits in that directory (non-zero bytes, filename recorded) and `memory/working_unroll_threads.py` gets a run receipt; or (b) operator writes the "use exports only" waiver into the line, and a FUNDED seat then files the synthetic-row plan for the starved themes (sovereign_mirror / verkle_lattice / republic_governance). W0.3 stays gated per the inline BOOT_SOIL note (line 61: no claim until --min 800 green).

### WO-2 [OPERATOR] [P0, deadline 2026-10-04] Studio publish + THE CATHEDRAL smoke (lines 204, 205)

State: both operator-gated by design; line 205 sets RE-CHECK BY 2026-10-04 (7-day staleness convention). Headless coverage already passes (eigenmap two smoke 36/36 per inline text; not re-run by me).
Criteria: (1) rojo serve -> connect -> publish from `roblox/the_mountain.rbxlx`; SKU ids filled in Config.luau (id != 0), HTTP + API services enabled. (2) Cathedral walk: take the portal, confirm walker HUD renders live position/distance/bearing top-left, step on a beacon, confirm the ShadowLedger row in Studio output. (3) One receipt banked under watch/inbox/ naming both items, dated on or before 2026-10-04.

### WO-3 [OPERATOR GO, then GOPHER LOCAL] [P0] verkle noise compaction live fold (line 31)

State: Q-001 receipt (head read this session): plan-only banked, execute NOT executed; escalation ruling quoted in the receipt: "NO GO on execute. Correct call: a workflow dispatch is NOT operator GO... the operator must personally authorize chain-tip rewrites." Real numbers are 247 folded / 790 kept, not the 99 in the line text.
Criteria: operator GO recorded by name against the banked plan; gopher then executes: fold per plan, Merkle chain recomputed, chain verify green (`python main.py verkle-audit` after a --dry pass), chain_guard healthy, tests/test_verkle_compaction.py green, checkbox flipped citing the real numbers.

### WO-4 [OPERATOR] [P1] manual REPL verify (line 97)

State: operator-hands by definition; no receipt substitutes (f-30 concurs).
Criteria: in a real terminal run `python main.py agent`; mid-turn exercise `!steer`, `!pause`, `!continue`, `!escape`; confirm the B4 status line per round and governor precedence by eye; append findings to `memory/runs/20260803-12h-sovereign-run/final-report-2026-08-03.md`.

### WO-5 [OPERATOR ruling, GOPHER edit] [P2] attention.md review habit (line 98)

State: Q-005 receipt (head read): all 127 pings triaged 2026-09-28, RESOLVED not stale; writer verified by me at mag/biography.py:509-515 (pings only on first write or force, noise control).
Criteria: close the line; re-seed at most one standing-habit line ("review memory/attention.md when Mag pings") if and only if the operator wants the ritual kept. The edit itself rides the WO-12 sweep.

### WO-6 [FUNDED] [P1] Stone 3 deep-read + Cooper synthesis (line 233)

State: the paced FullScan drain fired 09-25 (inline); ledger is live and failing lanes: my `tail -c 250 state/fuel/full_scan_ledger.jsonl` -> last row lane `nvidia-glm53`, `"ok": false`, `[fail:TimeoutError: The read operation timed out]`; file is 4,184,386 bytes; f-30 saw rows through 2026-09-28T13:39Z.
Criteria: (1) read the ledger to a terminal state (budget window ended or row cadence stopped) and state the row count; (2) rerun the GLM deep-read over the drained corpus on the FUNDED lane (the free lane is the one timing out, so do not retry there); (3) bank the Cooper synthesis; (4) receipt cites the ledger tail and row counts.

### WO-7 [FUNDED or box-time lane, operator picks] [P1] Arm C-200 rerun + Sunday close (line 239)

State: `watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md` exists (3,304 bytes, verified): Arm C-200 killed at 1/30 after 66 minutes, bars frozen, rerun "Owed for the next lane with box time" (content per f-30 read, existence verified by me). Close receipt `watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md` is a running close.
Criteria: fire the 200-budget arm with the frozen bars quoted pre-run; complete it or document the kill with numbers; update the closeout addendum; line 239 closes only when Arm C lands AND the MiMo/Grok last-burn disposition is named (coordinate with WO-8's lane ruling).

### WO-8 [OPERATOR ruling; execution GOPHER or FUNDED] [P1] Stone 5 Grok asks, lines 235 + 237 (same item twice; merge)

State: packet on disk (GROK_LANE_PACKET_20260925.md, 2,463 bytes; GROK_ASK4_SCOPE_FREEZE_20260926.md, 5,872 bytes; both verified); no execution receipts for any of the 4 asks. DRIVING LADDER 2026-09-28 funds only Hermes; free lanes are sensing-only.
Criteria: operator rules the lane: (a) Grok seat still reachable -> run the 4 asks there per the frozen scope, or (b) dissolved -> re-route: asks 1-3 (adversarial falsifier pass, W4 rerun design review, October reading list) to FUNDED; ask 4 (BURN_* filings audit) is repo-byte auditing, gopher LOCAL. Then 4 receipts + one merged todo line (kill the duplicate).

### WO-9 [GOPHER build, OPERATOR GO on first fire] [P2] box burn nightly driver + GPU unlock + whisper locate (line 234)

State: instrument exists (`tools/box_burn_watch.py` 4,927 bytes; `state/fuel/box_burn_watch.jsonl` 93,157 bytes; both verified). My `ls scripts/ | grep -i burn` returns nothing: no burn driver registered. GPU unlock wiring (llama-server Vulkan for estate lanes) not landed; Mr Pool 340-video whisper transcriber lives outside the repo, not found.
Criteria: (1) gopher writes the nightly grounding_chain burn driver: read backlogs (pile, briefs, whisper, training) -> fire top-N local jobs -> hard stop 07:00 (family-box law); (2) register the scheduled task plus log path; (3) operator sets target utilization N and GOes the first fire (state-changing on the family box, so this is an operator gate, not a gopher call); (4) one night's box_burn_watch.jsonl shows the load curve reaching target and then stopping; (5) transcriber located or declared OWED with an operator-pointer ask.

### WO-10 [GOPHER LOCAL] [P2] shared_surface INDEX fold rebuild CLI (line 232, sub-item 7 only)

State: my `grep -c rebuild mag/shared_surface.py` -> 0; f-30: single `def main` at :407, no rebuild verb; commit 383fed94f ran a one-time fold rebuild + 58 register heals but landed no standing CLI; 85 truly-invisible files. Sub-items (1)-(6) are done per the inline status text.
Criteria: idempotent rebuild verb landed in mag/shared_surface.py (mirroring the 383fed94f behavior), post-run INDEX delta = 0 truly-invisible files, `.venv/Scripts/python.exe -m mag.shared_surface validate` passes, then flip the whole line 232 (nothing re-seeded; all 7 sub-items closed).

### WO-11 [GOPHER design, consumer-gated] [P3] ratchet enablement dials from the DF fix taxonomy (line 250)

State: my `grep -icE "enablement|manual-only|opt-in|always-on" tools/violation_ratchet.py configs/violation_baseline.json` -> 0 and 0. Design idea only, nothing landed.
Criteria: spec card first (spec-before-behavior-change law): dial classes always-on / default-on / opt-in / manual-only mapped over registered debts, plus delete-when-X retirement receipt format; operator GO before any gate change; if workflow_gate.py is touched, `python tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios` must stay green. LOW priority: gate this on an operator-named consumer (no-bulk-self-processing law).

### WO-12 [GOPHER bookkeeping] [P3, run first, minutes] flip + re-seed sweep over the 51 SKIP lines

State: 51 of 63 lines are closed by receipts, inline decisions, or supersession (Section B).
Criteria: (1) pre-edit recount of unchecked lines = 63 (drift law: f-10 proved sibling lanes race this live tree; recount immediately before editing); (2) flip the 51 boxes, each with a one-line receipt pointer taken from Section B; (3) re-seed as new lines: the line 249 residuals (supernatural villain plots, per-class attack triggers beyond scorpion-force, Ages of Powers branch), the merged Stone 5 line per WO-8, and the WO-5 habit line only if ruled in; (4) keep the 12 open lines untouched (WO-1..WO-11 own them); (5) post-edit recount shows 12 unchecked plus the new re-seeds; (6) leave the resulting file untracked as it is today (no git add of queue/todo.md; it is gitignored).

## B. Skip ledger (51 lines, no new work)

Evidence tags: MINE = I verified the bytes/artifact this session; QREAD = I read the receipt head this session; RECEIPT-SIDE = receipt verified by the f-30 read, file existence verified by me this session, content not re-read.

| Line(s) | Item | Disposition | Evidence |
|---|---|---|---|
| 5 | Cerebras card gate | DECIDED inline 2026-09-26: PARKED until a use is found (stated twice, lines 3 and 5). Flip, keep lane dormant. | MINE: configs/providers.yaml cerebras block reads "card-gated 30-day trial, dormant pending operator GO" (lines 694-704 viewed). |
| 32 | Auto-promote gate | DONE (Q-002). | MINE: tools/auto_promote.py 7,432B + tests/test_auto_promote.py 5,920B exist. Wiring details RECEIPT-SIDE. |
| 33 | Session cards dir | DONE (Q-003). | MINE: memory/biography/cards/ holds 15 .card.json files (listed). |
| 98 | attention.md review | TRIAGED (Q-005). Close; optional habit re-seed per WO-5. | QREAD + MINE (writer mag/biography.py:509-515). |
| 104 | Hand-annotate rows | DONE (Q-007): 11 rows banked, anchor-verified. | RECEIPT-SIDE; Q_007_rows.jsonl + Q_007_validate.py exist (dir listing). |
| 126 | Spider thresholds | DONE (Q-008): thresholds fixed, suite green; the todo source stays as a deliberate tripwire. | QREAD. |
| 127 | comms_trail into routing | DONE: carried since checkpoint d575bc168. | MINE: mag/comms_trail.py:223 `"schema": "comms_consumption.v1"`. |
| 129 | Derived DAG index | DONE (Q-010). | MINE: tools/derived_dag.py 16,221B; memory/derived/derived_dag_index.json 30,772,308B. |
| 130 | Huang gate | DONE (Q-011). | MINE: mag/frontier_salon.py:180 `def roundtable(..., why="", baseline=None...)`; gate text at :26 and :205. |
| 135-142 | FIFTY WIDE 09-15 board (8 lines) | SUPERSEDED inline (line 133, re-seeded as FW-37..49). Flip all 8. | MINE (inline marker) + RECEIPT-SIDE (Q-021 verified dead memory/runs paths). |
| 146 | FW-01..05 morning verification | DONE (Q-020 + 5 per-item receipts). | RECEIPT-SIDE; receipts dir-listed. |
| 147 | FW-06..14 census debt | DONE (Q-021). | RECEIPT-SIDE. |
| 148 | FW-15..18 tide machinery | DONE (Q-022 + tide baseline txt). | RECEIPT-SIDE; Q-022_tide_prompt_v1_baseline.txt dir-listed. |
| 149 | FW-19..21 patrol debt | DONE (Q-023). | RECEIPT-SIDE. |
| 151 | FW-27..31 operator gate packets | DONE (Q-025). | RECEIPT-SIDE. |
| 152 | FW-32..36 wave stones | DONE (Q-026 + per-item receipts). | RECEIPT-SIDE; FW32..FW36 files dir-listed. |
| 153 | FW-37..42 game estate | DONE (Q-027 + per-item receipts + probes). | RECEIPT-SIDE; FW38..FW42 + Q_037/Q_038 probes dir-listed. |
| 160 | Catalog scanner v3 | LANDED. | MINE: mag/catalog_rebuild.py:1 "idempotent full-estate catalog rebuild (v3, landed 2026-09-26)". |
| 161 | Freshness budget + FTS5 decision | LANDED: C6 rescan policy + freshness module; FTS5 decided YES. | MINE: mag/catalog_rescan.py + mag/catalog_freshness.py exist; catalog/catalog_fts.sqlite 161,345,536B. |
| 162 | Tags v2 owner + 50q eval | DONE (Q-031); mining correctly NOT done (constitution law stands). | MINE: mag/catalog_tags.py:27-31 documents the v2 owner field; Q_031_retrieval_eval_results.json dir-listed. |
| 194 | Swarm Roblox port | DONE (games wave + Q-037 input wiring). | MINE: roblox/src/server/SwarmZone.luau 14,782B; line 243 games wave is checked inline. |
| 195 | 3-key comparative audit | DONE (Q-033). | QREAD. |
| 196 | First video-input burn | DONE (Q-034): bison.mp4 through stealth/space-bunny-alpha with control; receipt names the standing task closed. | QREAD. |
| 197 | mirrors.json per-host diff | LANDED. | MINE: configs/mirrors.json 468B; tools/stealth_driver.py:67 MIRRORS path, :605-607 per-host diff load. |
| 198 | Reasoning-effort dial policy | DONE (Q-036). | RECEIPT-SIDE. |
| 203 | Roblox client pass | DONE (Q-037). | RECEIPT-SIDE + Q_037_ws_probe.py dir-listed. |
| 218 | Public gateway host | DONE (Q-039): non-localhost bind + shared-secret + proof. | RECEIPT-SIDE + Q_039_bind_proof.py dir-listed. |
| 223 | v1.1 client polish | DONE (Q-040). | RECEIPT-SIDE. |
| 224 | Leaderstats page | DONE (Q-041). | RECEIPT-SIDE. |
| 225 | Pet orb model + trail | DONE (Q-042). | RECEIPT-SIDE. |
| 244 | Games polish backlog | DONE (Q-043): all three landed. | RECEIPT-SIDE + Q_043_sectionstream_check.luau dir-listed. |
| 249 | DF fold owed | LANDED 2026-09-25; flip and re-seed the inline residuals. | MINE: roblox/src/shared/SphereKinship.luau 19,063B, DfValue.luau 3,086B, Temptation.luau 2,703B, ProceduralBody.luau 11,913B. |
| 254 | Play-as-work citation layer | RESOLVED by the v6 master (inline UPDATE, line 257). | MINE: watch/inbox/play_as_work_20260926/VERIFICATION_v6_20260926.md 3,814B. |
| 255 | factorioctl go/no-go | SUPERSEDED into the U1 substrate decision (line 257 UPDATE; line 261 substrate is checked inline). Flip. | MINE (inline text). |
| 262 | Next-window handoff read | CONSUMED: the smoke eval log post-dates the 09-26-night handoff. | MINE: ../fle_u1/.fle/inspect_logs/2026-09-27T11-56-56-00-00_iron-plate-throughput_VQixYXHmjgry7Rhi9yCrkB.eval exists. |
| 266 | Thought Quantizer v0.3 + recompile | DONE: v0.3 compiled today with the owed two-pass fix. | MINE: memory/corpus/quantized_thought/compile_report.json: "v": "0.3", compiled 2026-09-28T16:19:05Z, v3_amendment two-pass over-refuse fix, packs 24/12/12. |
| 267 | Gene-pool regenerator or tombstone | TOMBSTONED 2026-09-27. | MINE: mag/gene_pool_feeder.py:3-4 "TOMBSTONED 2026-09-27 ... DORMANT, do not run, do not feed"; GENE_POOL_TOMBSTONE_20260927.md 2,716B. |
| 268 | FOSSIL-IN-FEED law teeth | LANDED: tools/fossil_check.py IS the freshness arm, WARN-only, registry-driven, wired into the 08:30 census patrol. | MINE: tools/fossil_check.py docstring (lines 6-18) + configs/fossil_registry.json 2,323B. |
| 272-277 | Dirac open loops (6 lines) | ALL CLOSED by the 09-27/28 lanes; the structural complaint is answered in behavior. | MINE: my own rerun `.venv/Scripts/python.exe -m mag.dirac_loop scan` at 2026-09-28T23:43:14Z returned ok=true, betti1=8, n_loops=6, closed_solved=6, open_gaps=0; watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl = exactly 6 rows (wc -l). Note: flash50/w3-dirac-loop7.md is a NEW unlanded proposal, not a reason to keep these open. |

Count check: 9 (singles through line 130) + 8 (135-142) + 7 (146-153) + 3 (160-162) + 5 (194-198) + 5 (203-225) + 5 (244-262) + 3 (266-268) + 6 (272-277) = 51. Keep-open: 31, 97, 99, 204, 205, 232, 233, 234, 235, 237, 239, 250 = 12. 51 + 12 = 63.

## C. Dispatch order

1. WO-12 bookkeeping sweep (gopher, minutes, unblocks the signal; recount first).
2. WO-2 Studio publish + Cathedral smoke (operator, only deadline-bound item, 2026-10-04).
3. WO-1 archive drop (operator, longest-blocked chain).
4. WO-3 verkle GO (operator one-liner, then gopher LOCAL execution).
5. WO-6 deep-read (FUNDED), WO-7 Arm C-200 (box-time), WO-8 lane ruling (operator, then gopher/FUNDED).
6. WO-9 burn driver build (gopher, operator GO before first fire), WO-10 shared_surface rebuild CLI (gopher).
7. WO-11 dials spec (gopher, P3, consumer-gated). WO-5 rides WO-12.

## Appendix A: checks I ran this session (command -> outcome)

1. Read tool on queue/todo.md: 277 lines, full file.
2. Python unchecked enumeration (command in Method): UNCHECKED 63, line list captured.
3. Existence + size loop over 28 artifact paths (auto_promote, derived_dag index, catalog modules, fts.sqlite, SwarmZone.luau, mirrors.json, fossil_check + registry, tombstone + ledger files, VERIFICATION_v6, Grok packet + scope freeze, B2_140 closeout, box_burn_watch pair, full_scan_ledger, quantizer compile_report, stealth_driver, 4 roblox fold files): all EXISTS with byte sizes as cited above; zero MISSING.
4. `ls memory/biography/cards/*.card.json | wc -l` -> 15.
5. `ls -la /c/Users/foste/Documents/projects/mycelial-republic/data/raw/` -> only .gitkeep, 0 bytes.
6. `ls ../fle_u1/.fle/inspect_logs/ | tail -3` -> the 2026-09-27T11-56-56 iron-plate-throughput .eval file.
7. `ls scripts/ | grep -i burn` -> no output (no burn driver scripts).
8. `tail -c 250 state/fuel/full_scan_ledger.jsonl` -> last row nvidia-glm53 ok:false TimeoutError.
9. `cat memory/corpus/quantized_thought/compile_report.json` -> v 0.3, compiled 2026-09-28T16:19:05Z, v3_amendment, packs 24/12/12.
10. `wc -l < watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` -> 6.
11. `grep -n dormant configs/providers.yaml | head -4` + `sed -n '694,704p' configs/providers.yaml` -> cerebras block "card-gated 30-day trial, dormant pending operator GO".
12. `grep -in tombstone mag/gene_pool_feeder.py | head -3` -> TOMBSTONED header at lines 3-4.
13. `grep -n comms_consumption mag/comms_trail.py | head -3` -> line 223 schema row.
14. `grep -n MIRRORS tools/stealth_driver.py | head -3` -> line 67 + 605/607.
15. `grep -c rebuild mag/shared_surface.py` -> 0.
16. `grep -icE "enablement|manual-only|opt-in|always-on" tools/violation_ratchet.py configs/violation_baseline.json` -> 0 and 0.
17. `grep -n v3 mag/catalog_rebuild.py | head -3` -> v3 docstring lines 1, 13.
18. `grep -n owner mag/catalog_tags.py | head -4` -> Tags v2 owner field, lines 27-31.
19. `grep -n "def roundtable" mag/frontier_salon.py` + gate greps -> line 180 signature with why + baseline; gate text lines 26, 205.
20. `grep -n "warn\|WARN" tools/fossil_check.py | head -5` -> WARN-only registry arm, census patrol wiring.
21. `sed -n '505,515p' mag/biography.py` -> attention ping-once writer.
22. Receipt heads read: Q-001, Q-005, Q-008, Q-033, Q-034 (watch/inbox/burn_reset_20260927/queue/).
23. `.venv/Scripts/python.exe -m mag.dirac_loop scan` -> ok=true, betti1=8, n_loops=6, closed_solved=6, open_gaps=0 (2026-09-28T23:43:14Z).
24. `ls` of watch/inbox/burn_reset_20260927/queue/ and flash50/ -> receipt inventory backing the RECEIPT-SIDE tags.

## Limits

- I did not edit queue/todo.md; WO-12's executor does that with the pre-edit recount (shared untracked file, live-tree drift proven by f-10).
- RECEIPT-SIDE verdicts were not re-executed: Q-002 wiring details, Q-007, Q-020..Q-027 contents, Q-036/037/039/040/041/042/043 contents, and f-30's own test runs (9 verkle compaction tests) were accepted from receipts whose files I verified exist but did not re-read in full.
- I did not re-run the video burn, the 3-key audit, or any provider call; those $0 burns are accepted as banked receipts, not re-executed.
- I did not search for the Mr Pool whisper transcriber (outside the repo; WO-9 owns it).
- Deadlines (2026-10-03 cerebras staleness note, 2026-10-04 Studio re-check) are taken from the todo file text, not re-derived.
- Em/en dash scan of this file: run post-write (see receipt line in the commit message); the target is 0 and 0.
