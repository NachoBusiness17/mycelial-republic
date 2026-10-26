# f-21 - SKILL CENSUS: .agents/skills/*/SKILL.md (2026-09-28)

Scope: every SKILL.md under `.agents/skills/` in this repo. All 18 files were read in full this session. Every number below comes from a command run 2026-09-28 (instrument receipt at the end). Companion receipts in this window: f-02/skill-liveness.md (same 18 skills, liveness rubric) cross-checked in the last section.

## Headline

- 18 skills, 40 files in the tree, 89,873 bytes total tree; SKILL.md bodies 56,713 bytes / 824 lines (`find .agents/skills -type f | wc -l` = 40; `wc -c`/`wc -l` summed over the 18).
- Created 2026-08-26 through 2026-09-18 (best-evidence dating below; git first-add alone lies for 12 of 18 because the 2026-09-14 checkpoint commit d575bc168 mass-added pre-existing files).
- Invoked with organic (non-workflow, pre-burn-window) file-level traces: 1 of 18, operator-corrections, including 3 seat writes to the file itself. 3 more have day-of-forge or single-mention rows (corpus-harvest, retrocausal-steering, fireball-cycle). 4 more were read only by burn-wave workflow actors on 09-26 (memlance, mesh-comms, zai-reference, light-operator). The rest have no file-level trace at all.
- logs/ is dark: `grep -rl "agents/skills" logs/` over 5,538 files returned zero files.
- Direct tests: 0 of 18 (`git grep -l "agents/skills" -- tests/` = 0 files; no test names any SKILL.md). Engine tests exist for 4 skills' subject machinery; ran 5 files: 39 passed in 48.37s.
- Code consumers: operator-corrections is wired into 4 code paths plus 2 boot docs plus the cite-gate state; a knowledge-graph family lists 5 doctrine skills by path; `mag/worldline_seed.py` indexes all 18 by name; the openclaw container mounts the whole tree.

## Table 1: inventory and creation dating

bytes/lines/mtime from `wc` + `stat` per file; created = best evidence (in-file self-dating + room.jsonl receipts + mtime), git = first commit that added the SKILL.md (`git log --diff-filter=A`).

| skill | bytes | lines | mtime | created (evidence) | git first-add |
|---|---|---|---|---|---|
| operator-corrections | 14,048 | 165 | 09-11 13:04 | 2026-08-26 (in-file "compiled ... 2026-08-26"; app_reasoning.jsonl row 2026-08-26T05:35Z narrates the copilot seat creating it) | 09-14 d575bc168 |
| fireball-cycle | 3,005 | 53 | 08-29 20:51 | 2026-08-29 (mtime + room.jsonl:1864 "skill_filed" 08-29T23:32Z) | 09-14 d575bc168 |
| chan | 719 | 17 | 08-29 20:57 | 2026-08-29 (mtime; no in-file date) | 09-14 d575bc168 |
| verb-genomes | 537 | 12 | 09-02 16:50 | 2026-09-02 (mtime; no in-file date) | 09-14 d575bc168 |
| salon | 2,358 | 44 | 09-03 09:11 | 2026-09-03 (mtime; shape-train card watch/SELF_STEAL_SHAPE_TRAIN_20260903.md exists) | 09-14 d575bc168 |
| show-me | 3,934 | 45 | 09-03 17:52 | 2026-09-03 (in-file provenance; room.jsonl:5341 organ.built 09-03T21:52Z) | 09-14 d575bc168 |
| agent-harness | 3,203 | 51 | 09-04 08:59 | 2026-09-04 (in-file "consolidated 2026-09-04"; room.jsonl:5523) | 09-14 d575bc168 |
| code-agent-data | 2,677 | 41 | 09-04 09:01 | 2026-09-04 (in-file header; room.jsonl:5523) | 09-14 d575bc168 |
| frontier-researcher | 3,114 | 44 | 09-04 09:00 | 2026-09-04 (in-file; room.jsonl:5523) | 09-14 d575bc168 |
| light-operator | 2,799 | 29 | 09-04 21:07 | 2026-09-04 (in-file "verbatim-condensed 2026-09-04"; room.jsonl:5663) | 09-14 d575bc168 |
| zai-reference | 2,081 | 24 | 09-04 20:14 | 2026-09-04 (in-file "split verbatim 2026-09-04"; room.jsonl:5650) | 09-14 d575bc168 |
| frontier-hr | 5,522 | 77 | 09-05 10:56 | 2026-09-05 (in-file "seated 2026-09-05"; room.jsonl:5891) | 09-14 d575bc168 |
| memweave | 1,499 | 28 | 09-18 01:36 | 2026-09-18 (git e692b2259) | 09-18 e692b2259 |
| memlance | 2,270 | 38 | 09-18 01:36 | 2026-09-18 (git e692b2259) | 09-18 e692b2259 |
| mesh-comms | 1,875 | 36 | 09-18 01:36 | 2026-09-18 (git e692b2259) | 09-18 e692b2259 |
| retrocausal-steering | 1,661 | 31 | 09-18 01:36 | 2026-09-18 (git e692b2259) | 09-18 e692b2259 |
| corpus-harvest | 3,191 | 51 | 09-18 13:09 | 2026-09-18 (git 5cf6a650a; seat memory receipt memory/continuity/seat_memory_20260927/corpus-harvest-skill-cliff-scalar-20260918.md) | 09-18 5cf6a650a |
| elder-lens | 2,220 | 38 | 09-18 02:20 | 2026-09-18 (git 45c66ee42 "NIGHT FOLD 2026-09-18 ... elder-lens skill forged") | 09-18 45c66ee42 |

## Table 2: what each skill does (from the full reads)

| skill | function (one line) |
|---|---|
| operator-corrections | 20 numbered laws compiled from the operator's failure ledger (consult first, two-strike bail, stop when verified, verify on the operator's surface, one supervisor, 1301 fork law, playbook matching, the infinity rule) |
| agent-harness | intake scoring rubric (5 axes, 25 points) + LAUNCH LAW + tri-state claims + claim-contention lock + receipt-at-bytes done law |
| salon | Door-B intake for the shape-train research salon: write one JSON to watch/salon_inbox/, runner fires it; 7 shapes, cost laws, escalation words |
| chan | open the /chan board at 127.0.0.1:8765/chan; engine is `python -m mag.chan`; refuse salon/lane_salon substitutes; only user-invocable skill |
| show-me | render explanations as the smallest visual artifact (pseudocode/tree/Mermaid/diff/HTML ladder); adapted from humanlayer's show-me |
| verb-genomes | 12-line index into docs/ref/verb_genomes/ (L0_contract, steal, self_steal, research_socratic) |
| zai-reference | lazy index into docs/ref/ZAI_API_EXPERT_REFERENCE.md via 12 section files (model catalog, params, errors, economics) |
| light-operator | lazy index into docs/ref/canon/LIGHT_OPERATOR_FOUNDATION_20260904.md via 10 sections; CANDIDATE status, promotion gate (held-out reproduction) unmet |
| memweave | feed structures not prose; weave context across seats via the RIB kernel; falsifier: structure must beat prose at equal tokens |
| memlance | aimed single-seed memory injection at one target seat; 5-step aim/forge/throw/witness/tally; falsifier: 2 of 5 lances must land unprompted |
| mesh-comms | the four channels (chan, rib_bus, panels, wants) and when to use each; falsifier: a message must change a file/decision/receipt |
| retrocausal-steering | plant a durable seed now so a future seat decision emerges as its own idea; witness or it failed |
| frontier-researcher | the harvest/score/build/verify/integrate/measure/refit/remember loop over percolator invariants + verkle chain |
| frontier-hr | Frontier HR Advisor answering hiring/skills/org questions from the 20-lab sweep cards, tri-state only |
| code-agent-data | mine room.jsonl + seat tapes into the QLoRA corpus; 600-byte + Result-section substance floor |
| elder-lens | day-close lens procedure stolen from 14 filed lenses: one pattern, real anchors only, end with the fleet's unasked question |
| corpus-harvest | full-fidelity public corpus harvest (Telegram/chan mirrors/Reddit-arctic-shift/X-fxtwitter) with JSONL register discipline |
| fireball-cycle | play physics not endings: fireball creates a tool, water keep cycles, convert-once; the mag/water_computer play card |

## Table 3: invocation evidence per skill

Instruments, with their limits named:
- STEPS = memory/trajectory/steps.jsonl (bash-command journal; 30,679 lines at first count ~21:5x, 30,948 at recount ~22:1x, live-appended by this burn's own actors). Journals bash face only (30,655 bash + 22 milestone rows), so Read-tool loads leave no row. Pre-09-27 rows are stable history.
- REASON = memory/thinking/app_reasoning.jsonl (seat reasoning text journal, 9,305 rows).
- ORGANIC = pre-09-27 rows from non-workflow sessions (session_id without "dwfrun"). Burn-wave workflow actors (09-26) and this window's census actors are counted separately and never as organic.
- REFS = tracked files outside the skill's own dir containing its path (git grep per skill).
- Logs = `grep -rl "agents/skills" logs/` over 5,538 files: 0 files, for all 18.

| skill | organic STEPS rows (pre-09-27) | wf STEPS rows (pre-09-27) | REASON rows (pre-09-27) | REFS | receipts / code consumers | verdict |
|---|---|---|---|---|---|---|
| operator-corrections | 15 (12 reads/misc + 3 WRITES: appends 09-10T12:50, 09-11T17:00, 09-11T17:04) | 6 | 26 | 68 | chord, invariant, lattice_render, build_fleet_imprint, 2 boot docs, cite-gate | INVOKED + WIRED |
| retrocausal-steering | 1 (head of SKILL.md 09-18T18:12, day of forge) | 4 | 0 | 8 | steering-fold receipts (corpus/steal/STEERING_FOLD_DELTA_20260926.md, B2_132) | INVOKED ONCE |
| corpus-harvest | 1 (python read 09-18T17:09, day of forge) | 1 | 0 | 6 | pre-dated harvests (bearableguy/mrpool/qdrop exports); tools/drift.py pairing | INVOKED ONCE |
| fireball-cycle | 1 (path mention inside a command 09-09T18:04, not a file read) | 0 | 0 | 6 | room.jsonl:1864 creation; openclaw mount + TOOLS.md names it; engine mag/water_computer.py live (modified in current working tree) | MENTIONED + MOUNTED |
| memlance | 0 | 5 (09-26 burn-wave actor reads) | 0 | 10 | organ mag/ghost_memlance.py + tests/test_memlance_wave.py | WORKFLOW-READ |
| mesh-comms | 0 | 5 (09-26 workflow reads) | 0 | 6 | channels (room.jsonl, rib_bus) in daily use; knowledge-graph family | WORKFLOW-READ |
| zai-reference | 0 | 3 (09-26 workflow reads, incl SKILL.md read) | 2 | 5 | lanes.yaml z.ai routes alive daily | WORKFLOW-READ |
| light-operator | 0 | 1 | 2 | 3 | all 10 sections present; CANDIDATE gate unmet (in-file) | WORKFLOW-READ |
| salon | 0 | 0 | 4 (creation-era scoring 09-03/09-04) | 11 | watch/salon_runner.py + 4 .bak snapshots; watch/salon_inbox/ holds exactly 1 intake ever (corpus_map_mcp_20260918.json), no in-repo consumer of the door | REASONING-ERA |
| chan | 0 | 0 | 4 | 10 | engine mag/chan.py + tests/test_chan.py; /chan page live | REASONING-ERA |
| show-me | 0 | 0 | 5 (creation-era scoring 09-03) | 1 | room.jsonl:5341 creation only | REASONING-ERA |
| verb-genomes | 0 | 0 | 3 | 5 | docs/ref/verb_genomes/ target real | REASONING-ERA |
| agent-harness | 0 | 0 | 2 (creation era 09-04) | 5 | room.jsonl:5523 creation; INTAKE_RUBRIC card real | REASONING-ERA |
| code-agent-data | 0 | 0 | 1 | 4 | subject starved (its own text admits mining lapsed) | REASONING-ERA |
| frontier-researcher | 0 | 0 | 1 | 5 | loop alive (percolator invariants.json + explore.jsonl fresh 09-28) | REASONING-ERA |
| frontier-hr | 0 | 0 | 0 | 8 | room.jsonl:5891; operator_board.html ADVISORS surface | RECEIPT-ONLY |
| memweave | 0 | 0 | 0 | 11 | knowledge-graph family; distributor mag/mem_weave_distributor.py exists | RECEIPT-ONLY |
| elder-lens | 0 | 0 | 0 | 3 | room-era receipt watch/inbox/NIGHT_FOLD_20260918.md; lens ledger exists | RECEIPT-ONLY |

## Code consumers (the wiring that exists today)

- operator-corrections is the only skill with runtime teeth:
  - mag/chord.py:66: `_corrections()` probes the file with `is_file()`; feeds the chord strike fidelity report.
  - mag/invariant.py:197-200: `INSTRUCTION_SOURCES` reads the file's text into `instruction_sha()`, the instruction-epoch fingerprint (one of exactly 3 sources).
  - scripts/lattice_render.py:26: parses its numbered laws into JSON for the dashboard lattice.
  - scripts/build_fleet_imprint.py:264: reads it for the fleet imprint.
  - Boot docs: .github/copilot-instructions.md:9 and BOOT_4_7.md:13 both instruct reading it. Drift: the file now holds 20 laws (`grep -c '^[0-9]*\. \*\*'` = 20); copilot-instructions says "ten laws", BOOT_4_7 says "the 12 laws".
  - state/cite_gate_latest.json (mtime 2026-09-07 03:17, 116,898 B, history 45 runs): the 09-07T07:17Z run verified 6 citations, 4 LOCAL-VERIFIED, cite_rate 0.6667; one verified citation is this SKILL.md itself (note: "file, 8019 bytes", its pre-growth size).
- scripts/build_knowledge_graph.py:63-65: "skills-engine" family lists memweave, memlance, retrocausal-steering, mesh-comms, salon by path.
- mag/worldline_seed.py:125-149: enumerates every dir under SKILL_ROOTS carrying a SKILL.md into the worldline genome (names only, never bodies).
- deploy/openclaw/entrypoint.sh:51-52 + openclaw.container.json:117: mount /mag/.agents/skills into the container; deploy/openclaw/workspace/TOOLS.md:45 names fireball-cycle and operator-corrections as LOAD targets.
- The repo's OTHER skill system does not touch these 18: configs/skills.yaml (15 ids, schema mag_skills.v1) points at ~/.grok/skills and docs/templates only (`grep -n "agents/skills" configs/skills.yaml` = 0 hits); mag/skill_lifecycle.py (ephemeral one-turn loader, gate ADK_ENABLE_SKILL_LIFECYCLE, default off) consumes skills.yaml + mag/skill_seat.py SKILL_WEAVES. Two disjoint skill stacks share one repo.
- AGENTS.md names 0 of the 18 (`grep -oiw <name> AGENTS.md` = 0 for every skill).

## Tests

- Direct: zero. `git grep -l "agents/skills" -- tests/` = 0 files; no test file references any SKILL.md.
- Indirect (subject machinery): tests/test_chan.py (chan engine), tests/test_water_computer.py (fireball-cycle engine), tests/test_skill_lifecycle.py (skills.yaml loader), tests/test_memlance_wave.py (memlance organ), tests/test_frontier_salon.py (salon engine). Even operator-corrections' consumers are untested: `git grep -l "instruction_sha|mag.chord" -- tests/` = 0 files.
- Run this session: `.venv/Scripts/python.exe -m pytest tests/test_chan.py tests/test_skill_lifecycle.py tests/test_water_computer.py tests/test_memlance_wave.py tests/test_frontier_salon.py -q` = 39 passed in 48.37s. These test engines, never the skill files.

## Cross-check against f-02 / skill-liveness.md (sibling census, same window)

- Agree on substance: 18 skills, 56,713 B / 824 lines, zero direct tests, logs/ dark, operator-corrections the only wired skill, AGENTS.md routes to none, two disjoint skill systems, corpus-harvest frontmatter defect, room rows are creation receipts.
- Delta 1: f-02 says `find .agents/skills -type f` = 41 files; my twice-run find = 40 (18 SKILL.md + 10 light-operator sections + 12 zai-reference sections). `git log --all --diff-filter=D --since=2026-09-20 -- .agents/skills` shows no deletions. The 41st file is unexplained from my instruments.
- Delta 2: f-02's grep instrument was logs/ only and explicitly deferred session tapes; my steps/app_reasoning sweep finds what logs/ could not: 15 organic operator-corrections rows including 3 writes, day-of-forge reads for retrocausal-steering and corpus-harvest, and 09-26 burn-wave workflow reads of 4 more skills.
- Delta 3: f-02 classes show-me and code-agent-data DEAD. My telemetry agrees on zero post-creation file-level use, but shows both carry pre-927 creation-era reasoning rows (show-me 5, code-agent-data 1): they were scored at adoption, then never touched again. I keep them at REASONING-ERA rather than DEAD, with f-02's DEAD reading as the file-level equivalent.
- Independent confirmations of f-02 claims I reused: state/cite_gate_latest.json exists (4 LOCAL-VERIFIED rows in latest run), watch/salon_runner.py exists, mag/salon_50.py, mag/memweave.py, mag/ghost_memlance.py, tests/test_frontier_salon.py, tests/test_memlance_wave.py, dashboard/static/chan.html all exist (test -f each).

## Findings

1. One skill carries the whole layer: operator-corrections is read, written (3 seat appends landing laws 17-20), hashed by the invariant, probed by the chord, parsed by the lattice, cite-gate verified, and boot-doc mandated. Everything else is doctrine-at-rest.
2. The fleet maintains its own law file: the 09-10 and 09-11 appends are seats extending the correction ledger (laws 17 FILTERED SURFACE, 18 PRIMARY SOURCES, 19 PLAYBOOK MATCHING, 20 INFINITY RULE), and the boot docs' law counts (10, 12) have drifted behind the file (20).
3. The skills tree's only mechanical readers before this burn were the 09-26 burn-wave workflow actors: 4 skills' first and only recorded loads were census/steering workflows, not seats doing the skills' jobs.
4. salon's intake door has fired once ever (corpus_map_mcp_20260918.json) and no in-repo code consumes the door; the runner (watch/salon_runner.py) is host-side with 4 .bak snapshots from 09-04/09-07, consistent with the skill's own "runner is host-side" line.
5. Frontmatter: 17 of 18 parse as frontmatter cards; corpus-harvest has none (starts `# corpus-harvest`), so a frontmatter-driven selector would skip it; chan is the only user-invocable one.
6. logs/ cannot see skill use at all (0 hits in 5,538 files): the only invocation telescope this estate has is memory/trajectory/steps.jsonl, and it journals bash only.
7. Snapshot law in action: steps.jsonl grew 30,679 to 30,948 lines while this census ran; per-skill counts of burn-window rows move, pre-09-27 history does not. Numbers above are labeled by window.

## Instrument receipt (commands run this session)

- `ls -la .agents/skills/`; `find .agents/skills -name SKILL.md | sort` (18); `find .agents/skills -type f` (40) + byte sum via find -printf (89,873).
- `wc -c`, `wc -l`, `stat -c %y` per SKILL.md (Table 1).
- Read tool on all 18 SKILL.md in full.
- `git log --diff-filter=A --format="%h|%as|%s"` per SKILL.md (Table 1 last column).
- `git grep -l ".agents/skills/<name>"` per skill (REFS column), excluding the skill's own dir.
- `grep -c ".agents/skills/<name>"` on memory/trajectory/steps.jsonl and memory/thinking/app_reasoning.jsonl; then a venv-python pass splitting each matching row by ts (pre/post 09-27), session type (dwfrun or not), and SKILL.md presence, plus the organic row listing quoted above.
- `grep -rl "agents/skills" logs/` (0 files) over `find logs -type f | wc -l` = 5,538.
- `git grep -n "agents/skills"` over mag/ tools/ scripts/ .github/ deploy/ docs/ (code consumers section); `git grep -n "SKILL.md" -- mag/ tools/ scripts/`.
- `git grep -l "agents/skills" -- tests/` (0); `git grep -il "skill" -- tests/`; `git grep -l "lattice_render|skill_lifecycle|build_knowledge_graph|mag.chan|mem_weave|water_computer" -- tests/`; the 5-file pytest run (39 passed in 48.37s).
- test -f existence checks: 31 grounding/claim files (29 OK, 2 misses: root PRIMER.md absent, my guessed DIALECTIC_LA_AGENTS_critique.md wrong name; the 5 real watch/DIALECTIC_LA_*_critique.md files exist); f-02 claim files (all 9 OK); `grep -c "agents/skills" state/world/PRIMER.md` = 1.
- room.jsonl: `grep -n "agents/skills" watch/room.jsonl` (11 rows, receipts at lines 1864, 5341, 5523, 5650, 5663, 5891 + 5 tool-use echoes).
- AGENTS.md: `grep -oiw <name>` per skill, all 0.
- configs/skills.yaml `grep -n "agents/skills"` = 0; 15 ids (`grep -c "id:"`).
- state/cite_gate_latest.json parsed with venv python (latest run ts 2026-09-07T07:17Z, 6 citations, 4 LOCAL-VERIFIED, cite_rate 0.6667, one row is the SKILL.md at 8,019 B).
- `grep -c '^[0-9]*\. \*\*'` operator-corrections = 20; frontmatter census via venv python (17 with `---`, corpus-harvest without); `grep -l user-invocable` = chan only.
- `git log --all --diff-filter=D --since=2026-09-20 -- .agents/skills` = empty (no deletions; f-02's 41 vs my 40 unresolved).

Mirror: byte-identical copy at watch/inbox/burn_reset_20260927/flash50/f-21.md.
