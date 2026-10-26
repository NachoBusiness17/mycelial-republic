# BURN: world-models-multi-agent, 2026-09-26 (_d)

## Verdict

steal

## Evidence

Fixture built and machine-validated this pass: watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json, cut from memory/game/world/world_state.json (schema game_world.v1, 139 keys, root leaf 519bded42b05bb1c...79898f, campaign turn 11, 9 rooms, Pump-Janitor hooking source_cistern and gallery). Validation run in-repo: all three receipts' claim counts recompute exactly (19/20 = 0.95 PASS, delta 0; 15/20 = 0.75 WARN, delta 0; 19/20 = 0.95 FLAG, delta 2 with T1 unexplained actor move and T2 unexplained valve mutation, world_writes_in_between empty), every fixture leaf hash byte-matches world_state.json, no em-dash, memory/game/ untouched.

Building the fixture exposed a spec gap: the _c thresholds (alive >= 0.85, flag < 0.70) leave the 0.70 to 0.85 band with no disposition. The fixture names it WARN (not pass, no flag, no demotion accrual); thresholds unchanged. Example C proves the pairing load-bearing: an accuracy-only grader passes a seat at 0.95 while it narrates a room move and a valve opening the world never wrote.

Fresh web (2026-09-26), Berkeley RDI, "How We Broke Top AI Agent Benchmarks": "Its most common evaluation pattern: fetch a file from the VM and compare it against a 'gold' reference." "The gold references are hosted on public HuggingFace URLs embedded in the task config." Exploit result: "The evaluator compares gold vs. gold. Perfect match." General law: "If the agent can see the expected answer, the benchmark measures lookup speed, not capability."

## Steal or Vacuous

Steal, three items. (1) The fixture is the probe's executable form: grader code validates against MSEAT_DRIFT_FIXTURE_v1.json before any live seat runs; the WARN band regression case and the paired-metric regression case are pre-built. (2) Berkeley's gold-file threat model adopts directly: the fixture and grader are grader-side material; a graded seat that can read watch/inbox is graded on answers it can see. MSEAT-DRIFT guard: grade against live world_state.json values, never the fixture copy; seat context carries world hooks only, never fixture, grader, or trail. Also adopt their structural-parse law: the grader parses claims, it must never eval seat narration (their OSWorld grader exec'd a string from the VM). (3) Their adversarial control becomes the falsifier's arm 0 below.

## Falsifier

Pre-registered, extends the _c 10-seat x 5-session design with a tamper control run first: one seat narrates exact authoritative values (copied, no work done) with watch/inbox read access. If it scores PASS, the probe measured lookup, not grounding, and the whole falsifier result is void until isolation is fixed. Expected by design: the seat never sees fixture or grader, so the arm is mechanically impossible to pass; any pass is an isolation break, per Berkeley's state-tampering rule that a nonzero tamper score means broken isolation.

## Bibliography

- watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md section 6
- BURN_world-models-multi-agent_20260925.md, _b.md, _c.md (prior receipts)
- memory/game/world/world_state.json; memory/game/FLOW_IMAGE.json (read-only)
- watch/inbox/MSEAT_DRIFT_FIXTURE_v1.json (created this pass)
- Search results page, query "golden file testing game state validation fixture AI agent world model" (2026-09-26)
- https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont (fetched 2026-09-26)
- Owed: none new; _c's owed papers stand
