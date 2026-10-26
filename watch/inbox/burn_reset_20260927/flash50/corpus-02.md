# corpus-02: compass vs reality - the v1-v10 arc mapped against the disk

**Item:** corpus-02 · **Source:** docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md (read in full, 258 lines)
**Date:** 2026-09-28 · **Seat:** mirror-corpus-02 (flash50)
**Bank:** watch/inbox/burn_reset_20260927/flash50/corpus-02.md

## Method - what was read and what was run

Read: docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md (258 lines, full); configs/version_roadmap.yaml (313 lines, full); configs/releases.yaml (174 lines, full); docs/ref/releases/VERSION_REGISTRY.md (127 lines, full); memory/improve/releases/gates.jsonl (all 19 rows); state/CURRENT.md (live truth); docs/ref/releases/RELEASE_NOTES_v1.md (full); heads of RELEASE_NOTES_v3.md, RELEASE_NOTES_v4.md; seed/SEED_VERSION + seed/CHANGELOG.md head; mag/release_registry.py status path; two v5 gate evidence JSONs.

Ran (exact commands):
- `./.venv/Scripts/python.exe main.py release status` and `--json` variant (live, this session)
- `ls docs/ref/releases/` (8 files; RELEASE_NOTES_v5.md does not exist)
- `ls memory/factory/` (exactly 1 build_audit JSON, 2,316 B, Aug 5)
- `ls memory/steward/daily/ | wc -l` = 29 leaves, last 2026-09-12
- `wc -l memory/training/cost_ledger.jsonl` = 2,316 rows; tail row ts 2026-09-28T23:58:22
- `ls memory/runs/orchestrator/tasks | wc -l` = 6,034
- `tail -1 memory/runs/conductor_trail.jsonl` = last row 2026-09-07T03:05
- `grep -ril xrpl mag/ tools/` = no files
- `grep -c release_milestone memory/training/events.jsonl` = 21
- `cat seed/SEED_VERSION` = "seed 3.3.0 - the harness stack..."
- `MSYS_NO_PATHCONV=1 schtasks /Query /TN MagImproveDaily|MagCensusPatrolDaily|MagFtsIndexDaily /FO LIST` = all three Status Ready, next run 9/29/2026
- `curl -s -o /dev/null -w %{http_code} --max-time 4 http://127.0.0.1:8765/api/v1/stack?limit=1` = 000 (no listener)
- `ls pyproject.toml setup.py setup.cfg dist/ build/` = none exist
- `ls tests/test_tier_refuse.py` = exists
- `tail -3 memory/improve/candidates.jsonl` = live rows at 2026-09-29T00:17/00:38

## Verdict table - vision row vs disk row

| v | Compass says (line) | Machine truth says | Verdict | Evidence |
|---|---|---|---|---|
| v1 | shipped (124) | shipped, 0 gates, 3 X witness posts | **LANDED** (origin era) | RELEASE_NOTES_v1.md; strike_origin.md on disk; X posts not fetchable from this seat (unverifiable here) |
| v2 | shipped, hardening (125) | shipped, 3/3 gates green | **LANDED**, liveness caveat | gates.jsonl rows 1,5,6 (run_a false 08-05 then true 08-06 12:07); desk :8765 returned 000 at check time |
| v3 | **in_progress** (126) | shipped 2026-08-06, 5/6 gate rows | **LANDED with bookkeeping gap** | version_roadmap.yaml:110, RELEASE_NOTES_v3.md:6; gates.jsonl has factory_pilot, freeze_gate, chat_preflight, deepseek_run, witness_filed; run_a defined for v3 (releases.yaml:79-81) never recorded under v3 |
| v4 | **planned** (127) | shipped 2026-08-06, 4/4 gates | **LANDED, organs partially dark** | gates.jsonl rows 11-14; conductor_trail last row 09-07; steward leaves stop 09-12; one training export (08-06) never repeated; cost_ledger alive today |
| v5 | planned (128) | planned, **2/3 gates green**, era pointer moved here | **IN PROGRESS, mislabeled as future** | gates.jsonl rows 15-16 (gstd_t0_probe, vast_train_dry) + 3 regime rows; xrpl_read_tools defined, zero implementation (grep xrpl mag/ tools/ = nothing); no RELEASE_NOTES_v5.md; VERSION_REGISTRY.md:107 "active version era (currently v5)" |
| v6 | curriculum TBD (129) | curriculum_tbd, 0 gates | **NOT STARTED**; precursors everywhere | releases.yaml:127-132; workflow_gate dogfooding, seed_init.py scaffolder (seed/CHANGELOG 3.2.0), orchestrator 6,034 tasks |
| v7 | curriculum TBD (130) | curriculum_tbd; **split-realized outside the arc** | **PARTIALLY REALIZED** | 3 Windows tasks Ready (MagImproveDaily 08:00, MagCensusPatrolDaily 08:30, MagFtsIndexDaily 09:00) while the named organ steward_daily is dark since 09-12; "No crons law" CURRENT.md:22 |
| v8 | curriculum TBD (131) | curriculum_tbd | **NOT STARTED** (code surfaces only: bus_cadence.py, agent_knot.py, mesh-comms skill) | releases.yaml:143-150 |
| v9 | curriculum TBD (132) | curriculum_tbd | **NOT STARTED**; zero packaging | no pyproject.toml/setup.py/dist/build; install = clone + scripts/ensure_venv.ps1 + mag.cmd doctor |
| v10 | curriculum TBD (133) | curriculum_tbd | **NOT STARTED**; economics instrument alive | cost_ledger.v1 live rows (price_band_usd 0.0 local seats, last 2026-09-28T23:58); GSTD join absent; reference/gstdcoin/ material on disk |

**Scorecard:** 4 of 10 landed (v1-v4), v5 is the half-landed live frontier wearing a "planned" badge, v6-v10 are untouched and honestly marked TBD. The estate's actual September motion (seed 3.3.0, burn waves, 580,599 training-event rows) bypassed the version arc entirely and was reconciled only through the regime_ milestone patch (VERSION_REGISTRY.md:103-113).

## Patterns (the drift map)

1. **The compass is the stalest file in the load order.** Its own §3.2 table says v3 in_progress and v4 planned; every machine file (version_roadmap.yaml:110,117, releases.yaml:70,95, VERSION_REGISTRY.md:31-32, both release notes, all 9 gate rows) says both shipped 2026-08-06. Compass as-of is still 2026-08-05.
2. **The freeze stamped the drift instead of fixing it.** The 09-26 §4 freeze note (COMPASS.md:141) says "Vision prose (§1-3, §5+) untouched this turn - freeze stamp only, no compass rewrite." A known false table is now load-order doctrine that every new seat reads before the machine files.
3. **Amend protocol half-executed.** Compass §8 requires on gate pass: release record + update VERSION_REGISTRY. The registry was updated (as-of 2026-09-26); the compass table was not. Downstream docs obeyed the protocol; the upstream vision doc did not.
4. **v5 is the era without the ship.** 2 of 3 gates green, the third (xrpl_read_tools) has zero implementation on disk, release notes absent - yet the registry names v5 the active era (line 107) and files September's regime milestones against it. The arc's pointer moved to v5; v5 never shipped.
5. **v3 shipped 5/6.** run_a is defined for v3 as "requires v2.run_a" (releases.yaml:79-81) but was never recorded as a v3 row in gates.jsonl; `release status --json` live shows v3 defined=6 passed=5 on a shipped version. Inherited-gate bookkeeping gap, not a gate failure.
6. **The status instrument counts "TBD" as three gates.** `gates_defined: len(gates)` (mag/release_registry.py:70) takes len() of the YAML scalar string `gates: TBD`, so v6-v10 all print gates=3 in text mode (live run). gate_ids is correctly empty; display defect only.
7. **Arc organs went dark while the estate boomed.** gates.jsonl gap 2026-08-10 to 09-26 (admitted at VERSION_REGISTRY.md:105: "the version-gate trail went dark 2026-08-10 while fleet motion continued (468K+ training events since)"); conductor_trail.jsonl last row 2026-09-07; steward daily leaves stop 2026-09-12. The real September engine was the seed arc (seed 3.3.0, seed/SEED_VERSION) plus burn waves, outside the v-arc.
8. **One arc organ still has a pulse: the cost ledger.** 2,316 cost_ledger.v1 rows through 2026-09-28T23:58 - the pennies-not-dollars instrument is the only v4 organ alive today. The estate measures itself even where it no longer graduates versions.
9. **The loop diagram's seat names are fossils.** Compass §2.1 loop is Grok strategist / Cursor materializer / Ollama planner / DeepSeek judge. The 2026-09-28 DRIVING LADDER (AGENTS.md) replaced the economics: only Hermes funded ($180 Nous), free lanes sensing-only, Anthropic keys UNFUNDED, Grok not on the ladder at all. The vision's loop is a diagram of August seats.
10. **v7 steward autonomy is split-realized.** The gate organ (v4 steward_daily) is dark, but daily soil without asking exists for three surfaces via Windows scheduled tasks, all queried live and Ready for 2026-09-29. Meanwhile "No crons law holds: scheduling is operator-gated" (CURRENT.md:22) freezes any new scheduled autonomy on the operator - v7's defining promise is exactly what the no-crons law now reserves to the operator.
11. **v6 precursors are everywhere; the version has not happened.** Workflow-gated fan-out builds (tools/workflow_gate.py, AGENTS.md build discipline), seed_init.py one-command estate scaffolder (seed/CHANGELOG 3.2.0), orchestrator at 6,034 task jsons (grew from the 6,032 cited 2 days ago). Mag-assisted-Mag is routine; Mag-built-Mag ("loop produces next version without hand-merge") has not occurred.
12. **v9 packaging reality is zero.** No pyproject.toml, setup.py, setup.cfg, dist/, build/. Install remains clone + ensure_venv.ps1 + doctor. The curriculum slot is accurate.
13. **Desk liveness is snapshot-true, not now-true.** Compass §4 (frozen) lists "Mag Agent Desk Live :8765"; live curl returned 000, and the estate's own scout corroborated it minutes later: memory/improve/candidates.jsonl filed "lifecycle_gap:lab: should be on but actual off" at 2026-09-29T00:38.
14. **Gate evidence is real but single-shot.** v3's factory pilot is exactly one build_audit JSON (2,316 B, Aug 5); v4's training export is one manifest (08-06) never repeated; v5's vast_train_dry verifier ran "480 passed" on 2026-08-06 vs today's census of 2,303/352 - the same gate run today would exercise a 4.8x larger suite. Old gates are snapshots of one tree at one moment (B2-216 applies to release gates too).
15. **Witness spine unverifiable from this seat.** v1's X post URLs (releases.yaml:30-38) cannot be fetched or authenticated here; the local canonical ref strike_origin.md exists on disk. The v1 claim rests on disk artifacts, not on the posts.
16. **Sovereignty pillars are the most-real part of the vision.** T0/T1 never-remote has tests/test_tier_refuse.py plus the v2 tier_refuse gate row; forkability is structural (plain repo, no service); pennies/day has a live cost ledger with price_band_usd 0.0 local rows. Device-fuels-network is the weakest pillar: probe artifact + reference/gstdcoin/ material, no DePIN join.
17. **The honest-TBD discipline held.** No fake dates for v6-v10 anywhere in yaml, registry, or roadmap ("no calendar dates" version_roadmap.yaml:6; "no fake dates" VERSION_REGISTRY.md:40). The one place the arc could have quietly lied, it did not.

## Bottom line

The compass's two-era story (hand-built v1-v2, loop-trained v3-v10) is half-true: v1-v4 landed as documented (v3 with a 5/6 row gap, v4 with dark organs), v5 is the live era but 1 gate and its release notes short of shipping, and v6-v10 are untouched slots honestly marked TBD. September reality (seed 3.3.0, burn waves, regime milestones) outran the arc, and the compass's own table was frozen stale by choice. The next seat reading the compass as doctrine will believe v3 is unfinished and v4 unstarted - both false in the opposite, flattering direction. Owed: a compass §3.2 rewrite (5-line edit) and a v3 run_a gate row, both cheap; the xrpl_read_tools gate is either build-or-descope.
