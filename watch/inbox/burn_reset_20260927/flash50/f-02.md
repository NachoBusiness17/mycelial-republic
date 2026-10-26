# f-02 - SKILL LIVENESS CENSUS: .agents/skills/*/SKILL.md (2026-09-28)

Scope: all 18 SKILL.md files under `.agents/skills/` in this repo. Every skill's file was read in full this session. Classification: ACTIVE / DORMANT / DEAD per the rubric below. Every number in this file comes from a command run on 2026-09-28 (commands listed inline).

## Headline

- 18 skills, 56,713 bytes, 824 lines total (`wc -c -l .agents/skills/*/SKILL.md`).
- Tests: **0 of 18**. `grep -rln "agents/skills" tests/` = zero files; `grep -rln "SKILL.md" tests/` = zero files. No test in tests/ touches any skill file.
- Callers in mag/ or tools/: **1 of 18** (operator-corrections only). Bulk indexer touching all 18 by directory name: `mag/worldline_seed.py:86-90` (SKILL_ROOTS includes `ROOT/.agents/skills`, genome slab lists names only, never reads bodies, `mag/worldline_seed.py:132-141`).
- Invoked per the ask's instrument (grep logs/): **0 of 18**. `grep -rlo -E "agents/skills/[a-z-]+" logs/` over 5,536 files / 1.7G returned zero hits. All name-level log hits are incidental (details below).
- Real-file-use verdict: **1 ACTIVE, 15 DORMANT, 2 DEAD.**

## Rubric (declared before classifying)

- ACTIVE = file-level use after creation is evidenced: mag/ or tools/ code reads the file at runtime, or an automated instrument verified against it, or a seat-side durable artifact cites its path post-creation.
- DORMANT = no post-creation file-level use, but a loader exposes it or its subject machinery is verifiably alive today (engine module, runner, tests on sibling organs, live docs target), so it can fire with no code change.
- DEAD = no post-creation file-level use AND subject machinery also dark (cadence lapsed or absent, no organ, no export, no trace beyond the creation receipt).

Note on limits: these are prompt-doctrine skills. A seat that loads one leaves no trace in logs/ unless it cites the path in a durable artifact. logs/ absence is therefore evidence of "no recorded invocation," not proof of "never loaded." Session tapes live outside logs/ (memory/runs, ~/.zcode); this census is file-level use evidence, not seat-memory forensics.

## The census table

| skill | bytes | last touch (git) | test | caller in mag/ or tools/ | invoked (logs/) | class |
|---|---|---|---|---|---|---|
| operator-corrections | 14,048 | 2026-09-14 d575bc168 | no | **YES** | no (but cite_gate verify 09-07) | **ACTIVE** |
| chan | 719 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| salon | 2,358 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| fireball-cycle | 3,005 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| agent-harness | 3,203 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| frontier-researcher | 3,114 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| frontier-hr | 5,522 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| light-operator | 2,799 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| verb-genomes | 537 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| zai-reference | 2,081 | 2026-09-14 d575bc168 | no | no | no | DORMANT |
| show-me | 3,934 | 2026-09-14 d575bc168 | no | no | no | **DEAD** |
| code-agent-data | 2,677 | 2026-09-14 d575bc168 | no | no | no | **DEAD** |
| memweave | 1,499 | 2026-09-18 e692b2259 | no | no | no | DORMANT |
| memlance | 2,270 | 2026-09-18 e692b2259 | no | no | no | DORMANT |
| mesh-comms | 1,875 | 2026-09-18 e692b2259 | no | no | no | DORMANT |
| retrocausal-steering | 1,661 | 2026-09-18 e692b2259 | no | no | no | DORMANT |
| corpus-harvest | 3,191 | 2026-09-18 5cf6a650a | no | no | no | DORMANT |
| elder-lens | 2,220 | 2026-09-18 45c66ee42 | no | no | no | DORMANT |

Last-touch source: `git log -1 --format="%ad %h" --date=short -- .agents/skills/<name>` per skill. 12 skills last touched by the 2026-09-14 checkpoint (d575bc168 "Zenodo capstone mined + forge-window recovery receipt"), 6 by the 2026-09-18 wave (e692b2259 created memweave/memlance/mesh-comms/retrocausal-steering, insertions only, per `git show --stat`; 5cf6a650a created corpus-harvest; 45c66ee42 created elder-lens).

## Per-skill evidence (only the non-obvious rows)

**operator-corrections - ACTIVE.** The only skill wired into mag/ code:
- `mag/chord.py:66` - `_corrections()` probes `.agents/skills/operator-corrections/SKILL.md` with `is_file()`; result feeds the `fidelity: FULL` verdict in `strike()` (mag/chord.py:92-96).
- `mag/invariant.py:197-200` - `INSTRUCTION_SOURCES` includes `("operator-corrections.SKILL", ... read_text ...)`; the skill body is hashed into `instruction_sha()` (the instruction-epoch fingerprint).
- Caveat found while tracing: `instruction_sha()` has exactly one caller (mag/chord.py:79), `chord.strike()` is a seat-ritual CLI (`python -m mag.chord strike`), and `grep -rl "struck_by" logs/ memory/attention.md memory/rib queue state watch/room.jsonl` = zero hits, so no recorded run of the ritual exists. Its ACTIVE status rests on the cite-gate instrument next.
- `state/cite_gate_latest.json` (mtime Sep 7 03:17) holds 4 citation rows with `"raw": ".agents/skills/operator-corrections/SKILL.md"` - mag/cite_gate.py verified cards' citations against the skill file's text on 09-07. cite_gate is NOT scheduled (no hit in scripts/*.ps1 or scripts/*.cmd; no schtasks row), so this was ad hoc or a single run.
- Seat-surface references: `state/world/PRIMER.md` (1), `state/_astra_triangulation.md` (3), `queue/handoff/zcode/CONVO.md` (2 path mentions) - `grep -o -E "agents/skills/[a-z-]+" <file>` counts.
- Also the most-parsed skill outside mag/tools: `scripts/lattice_render.py:26` parses its numbered laws into JSON; `scripts/build_fleet_imprint.py:264` reads it.

**chan - DORMANT.** The skill file is a 17-line browser-open card (`http://127.0.0.1:8765/chan`, `user-invocable: true`). No test/caller/invocation of the FILE, but the engine it points at is alive: `mag/chan.py` exists, `tests/test_chan.py` exists (word-boundary grep hit), the `/chan` route renders `dashboard/static/chan.html` (existence verified), and `logs/dashboard_sv.log` mentions the page. Kill the file and the board loses its user-facing instruction card, not its engine.

**salon - DORMANT.** The skill is Door-B intake for the salon runner (write one JSON to `watch/salon_inbox/`). Runner machinery is alive: `mag/salon_50.py`, `mag/frontier_salon.py` exist; `tests/test_frontier_salon.py` exists; `logs/queue_events.jsonl` and orchestrator logs carry salon drain rows (sampled: "drain_start qsaloncouncil001", "frontier_salon.roundtable"). No evidence the intake protocol file itself was ever loaded.

**fireball-cycle - DORMANT.** Creation receipt 2026-08-29 (watch/room.jsonl line 1864, "skill_filed"). The only skill besides operator-corrections NAMED in a loader surface: `deploy/openclaw/workspace/AGENTS.md:18` instructs openclaw seats to LOAD it, and `deploy/openclaw/workspace/TOOLS.md:45` lists it; `deploy/openclaw/openclaw.container.json:114-119` mounts `/mag/.agents/skills` as skills extraDirs. Subject machinery live: `mag/water_computer.py`, the chan board.

**frontier-researcher - DORMANT.** Describes the percolator/invariants/verkle loop, and that loop is alive TODAY: `memory/percolator/invariants.json` (109,231 B) and `explore.jsonl` (1,700,201 B) both mtime 2026-09-28 13:50 (`ls -la`). The skill is the loop's doc layer, never itself invoked by path.

**elder-lens - DORMANT (borderline).** Forged 09-18; its grounding ledger `watch/inbox/SELF_STEAL_DEEP_20260918.md` exists (find verified). But the elder lane it reads is nearly dark: `queue/lanes/elder/inbox.jsonl` is 0 bytes, manifest.md frozen 09-04. The skill's own falsifier ("a lens is dead if no organ acts on its question within one week") starts its clock 09-18; if no lens lands by ~09-25..10-02 with an organ acting on it, this flips to DEAD by its own terms.

**corpus-harvest - DORMANT.** Forged 09-18 (5cf6a650a) as the convert-once of harvests that had already run: `watch/inbox/bearableguy_export`, `watch/inbox/mrpool_export`, `watch/inbox/qdrop_export` all exist (ls verified). Pairs with `tools/drift.py`. No post-forge invocation trace.

**memweave / memlance / mesh-comms / retrocausal-steering - DORMANT.** All four forged in one commit 09-18 (e692b2259, 133 insertions, files new). Youngest files in the set. Live sibling organs: `mag/memweave.py`, `mag/ghost_memlance.py`, `tests/test_memlance_wave.py` (tests the mag organ, not the skill); mesh-comms' channels (room.jsonl typed rows, 13,865 lines; memory/rib_bus/) are in daily use. All four indexed by `scripts/build_knowledge_graph.py:63-65` in the "skills-engine" cluster.

**agent-harness - DORMANT.** Creation receipt 09-04 (room.jsonl line 5523, "3 DeepSeek-gap skill scaffolds, files only"). Subject surfaces exist: `watch/INTAKE_RUBRIC_20260903.md` and INTAKE_* cards on the shelf; cross-cited by frontier-researcher's SKILL.md ("SCORE - intake rubric, 5 axes (see the agent-harness skill)"). No code caller, no test, no invocation trace of its own.

**frontier-hr - DORMANT.** Standing advice column seated 09-05 (room.jsonl line 5891 build receipt); its data shelf (watch/MEGA_DIGEST_SKILLS_DEMAND_20260904.md, FRONTIER_MAP_DEEPSEEK_20260904.md) and the operator_board.html ADVISORS summons surface exist. No invocation trace.

**light-operator - DORMANT.** CANDIDATE doctrine with its own promotion gate unmet (SKILL.md:26-29: held-out reproduction "Not yet run"). All 10 section files present; structural enforcement targets exist (`dashboard/static/fleet_symbols.html` verified).

**verb-genomes - DORMANT.** 12-line index; its docs target `docs/ref/verb_genomes/` is real (L0_contract.md, steal.md, self_steal.md, research_socratic.md verified by ls). Note: `grep -c "verb_genomes" AGENTS.md` = 0, so nothing in the boot doc routes a seat there; the genome path is cited inside other skills (agent-harness SKILL.md line 26).

**zai-reference - DORMANT.** Lazy index of a live subject (the fleet routes through z.ai lanes daily per AGENTS.md); index + 12 verbatim sections receipted 09-04 (room.jsonl line 5650). No invocation trace of the index file.

**show-me - DEAD.** Pure doctrine (prompt-only by its own design, SKILL.md line 9), no machinery to be alive, zero repo-side trace beyond its 09-03 creation receipt (room.jsonl line 5341 "organ.built"): no path reference anywhere in mag/, tools/, scripts/, tests/, configs/, or logs/; no name-level code reference; no test. It is exposed to every session by the seat CLI's auto-discovery (this session's own skill list shows all 18 repo skills injected with descriptions), so "DEAD" here means "no evidence of any use in the estate since creation," not "unreachable."

**code-agent-data - DEAD.** The clearest corpse. Its own text admits the failure ("mining lapsed since Aug and the corpus starved while the fleet kept working", SKILL.md lines 16-17). Subject machinery dark: `memory/train_data/` holds exactly one file, `resident_actor_seed.jsonl`, mtime Aug 18 (ls verified); no Stage 2/3 packer runs found; no caller, no test, no invocation trace anywhere (word-boundary grep = zero files in logs/ and tests/). The cadence organ it prescribes never ran.

## Cross-cutting findings

1. **Zero test coverage for the entire layer.** tests/ has no reference to any `.agents/skills` path and no reference to "SKILL.md" at all (both greps empty). The closest things - tests/test_chan.py, test_memlance_wave.py, test_frontier_salon.py - test the mag ENGINES the skills point at, never the skill files.
2. **The repo's own skill machinery serves a DIFFERENT skill set.** `configs/skills.yaml` (schema mag_skills.v1) and `mag/skill_lifecycle.py` (the one-turn ephemeral tool loader, gated by ADK_ENABLE_SKILL_LIFECYCLE, default off) serve `~/.grok/skills/*` and `docs/` weaves (ponytail, caveman) - none of the 18 repo skills is loadable through them. `mag/skill_ledger.py` is unrelated despite the name (a decisions/labeled-rows ledger).
3. **Loader surfaces that DO reach these 18:** (a) the seat CLI auto-discovers `.agents/skills/*/SKILL.md` and injects name+description into every session - observed directly in this session's context; (b) the openclaw container mounts the whole dir (`deploy/openclaw/openclaw.container.json:114-119`) and its workspace docs name fireball-cycle + operator-corrections as LOAD targets (AGENTS.md:18, TOOLS.md:45); (c) `mag/worldline_seed.py` indexes all 18 by name into the worldline genome. AGENTS.md itself references none of the 18 (`grep -ciw <name> AGENTS.md` = 0 for all 18).
4. **Room mentions are creation receipts, not invocations.** All 9 room.jsonl path mentions are skill_filed / organ.built / build-receipt rows from 08-29 to 09-05 (lines 1864, 5341, 5523, 5650, 5663, 5891). No post-creation load evidence on any durable surface except the operator-corrections citations in section above.
5. **Log hits are all noise, itemized:** `agent-harness` in logs = the third-party repo `ollama-agent-harness` (Bradliebs) in steal-scan rows (logs/failure_kb.jsonl, logs/orchestrator/t32f4829a00.out.log, logs/tesuji_shells.jsonl); `memlance`/`memweave` in logs/tesuji_shells.jsonl = doctrine prose; `chan` in logs = the /chan dashboard page (the engine); `salon` in logs = salon module runs and strike-the-chord searches; the only two literal `SKILL.md` strings in logs/ are a steal-report about another repo's `agent/skill_utils.py` (logs/claims.jsonl line 312) and an orchestrator read of `reference/gstdcoin/gstdbot/skills/agency-ad-creative-strategist/SKILL.md` (logs/orchestrator/te72b4571fd.out.log line 19) - neither is ours.
6. **Frontmatter defect:** `corpus-harvest/SKILL.md` has no YAML frontmatter at all (file begins `# corpus-harvest`); a frontmatter-driven selector would skip it. The other 17 all carry name/description frontmatter (chan additionally `user-invocable: true`).
7. **watch/inbox/SKILL_FORGE_20260918.md exists** (the skill-forge card named by build_knowledge_graph.py:75) but contains zero `.agents/skills` path strings - the forge card and the forged files are not cross-linked by path.

## Operator-facing bottom line

If triage is wanted: code-agent-data and show-me are the prune candidates (DEAD, no evidence of any use or live subject); elder-lens flips to DEAD by its own falsifier within days unless a lens lands; the 09-18 doctrine quartet (memweave/memlance/mesh-comms/retrocausal-steering) is 10 days old with live organs - give them a window before judging. operator-corrections is the only skill with structural teeth (instruction-epoch hash + existence probe + cite-gate verification) but its own caller (chord strike) has zero recorded runs - arming that ritual or wiring cite_gate onto cadence would convert its ACTIVE from historical to current.

## Instrument receipt (commands run this session)

- `find .agents/skills -name SKILL.md | sort` -> 18 files; `find .agents/skills -type f` -> 41 files (2 skills carry sections/ subtrees).
- `wc -c -l` over all 18 -> 56,713 B / 824 lines.
- Read tool on all 18 SKILL.md files (full contents).
- `grep -rl -- ".agents/skills/<name>" mag tools scripts tests main.py mag.cmd` per skill (mimosa/pycache excluded) -> only build_knowledge_graph.py (5 skills), lattice_render.py + chord/invariant/build_fleet_imprint (operator-corrections).
- `grep -rln "agents/skills" tests/` and `grep -rln "SKILL.md" tests/` -> empty.
- `grep -rlo -E "agents/skills/[a-z-]+" logs/` -> empty; `grep -rl -w <name> logs/` per skill -> incidental hits only (itemized above); logs/ = 5,536 files, 1.7G (find | wc -l; du -sh).
- Supplementary seat-surface greps (memory/attention.md, memory/rib, queue, state, watch/room.jsonl, deploy/openclaw) as cited per skill.
- `git log -1 --format="%ad %h"` per skill dir; `git show --stat` on e692b2259 / 5cf6a650a / 45c66ee42.
- Existence ls checks: mag/chan.py, mag/salon_50.py, mag/water_computer.py, mag/memweave.py, mag/ghost_memlance.py, tools/drift.py, dashboard/static/chan.html, docs/ref/verb_genomes/L0_contract.md, watch/INTAKE_RUBRIC_20260903.md, watch/inbox/SELF_STEAL_DEEP_20260918.md, memory/percolator/{invariants.json,explore.jsonl}, memory/train_data/, watch/inbox/*_export x3, dashboard/static/fleet_symbols.html.

Mirror: this content is banked byte-identical at `watch/inbox/burn_reset_20260927/flash50/f-02.md` and `watch/inbox/burn_reset_20260927/flash50/skill-liveness.md`.
