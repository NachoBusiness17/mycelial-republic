# WRITE-STRIP AT FAN-OUT: chore discharge receipt + spec row (2026-09-26)

The MICKEY-17 owed chore "strip write tools at fan-out" (GO_LIST_EXECUTION_20260925.md:33, "needs the runner layer"; still-owed marker MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md:75) is DISCHARGED RUNNER-SIDE. The ZCode-harness change itself stays SPEC-ONLY (Section 4 below), exactly as the chore scoped it.

## 1. Sources of record (read this session)

- `memory/runs/mickey17_v2/lanes/write-delegation.json` row 0: schema-level omission over runtime veto; quote on file: "read-only tools run in parallel via a thread pool (up to five concurrent calls), while write tools run sequentially". Row 1: lanes return proposed writes to the orchestrator as data.
- `memory/runs/mickey17_v2/lanes/orchestrator-war-stories.json` row 0: quote on file: "But we've found a narrower class of patterns that do: setups where multiple agents contribute intelligence to a task while writes stay single-threaded."
- Estate seam of record: `mag/orchestrator.py spawn_task()` builds the fan-out child cmd `[python, main.py, agent, --query, goal, --provider]` (orchestrator.py:838 pre-patch) and the child seat attaches `TOOL_SCHEMAS` (mag/agent_cli.py:275) to every provider call. That tool grant was the enforcement gap: write_file rode in every fan-out child's schema.

## 2. What landed (all seams cited at post-patch lines)

| File | Seam | What it does |
|---|---|---|
| `mag/write_strip.py` (new, 165 lines) | `strip_write_tools()` :119, `classify_tool()` :86, `WRITE_TOOL_NAMES` :44, `DUAL_USE_TOOL_NAMES` :67, `READ_ONLY_ARG` :40, `read_only_from_env()` :157 | The compiler. Name-classified schema strip (OpenAI-function and flat formats); write tools always stripped, dual-use (run_shell/run_python/bash) stripped only under strict=True; input schemas never mutated; every strip lands in a `write_strip.v1` receipt. |
| `mag/agent_cli.py` | `activate_read_only()` :537, `_schemas()` :555, `_read_only_notice()` :560, `_DENIED_TOOL_NAMES` :534 | The one tool grant (`_schemas()`) now feeds all three provider call sites: freeze :997, degenerate-retry chat :1424, main chat :2145. Backstop: `_run_tool` refuses any name in the denied set :797 with a "return the proposed write to the orchestrator" error. `run_agent(read_only=)` :2523 resolves flag then env (`MAG_READ_ONLY`, `MAG_READ_ONLY_STRICT`) and activates before turn 1; the static read-only notice rides the frozen prefix :994 and the initial system :2594 (static bytes, prompt-cache law preserved). `restore_full_grant()` :547 is the test/REPL escape. `main_argv` grew `--read-only`. |
| `mag/orchestrator.py` | `spawn_task(..., read_only=True)` :628, cmd append :844, record stamp :858 | FAN-OUT DEFAULT IS NOW READ-ONLY. Every spawned one-shot child gets `--read-only` on its cmd and `read_only` stamped in the task record. Escape: a caller that must write passes `read_only=False` and owns the exception. The compact `research_worker` branch is tool-less by construction and correctly takes no flag (flag append sits before the branch swap). |
| `main.py` | parser flag :1292, handler pass-through :4676 | `main.py agent --read-only` forwards into `run_agent`. |
| `tests/test_write_strip.py` (new, 12 tests) | whole file | See Section 3. |

Estate grant measured this session: 16 tool schemas; read-only compile strips 3 (write_file, pheromone_drop, blackboard_post; the last two are shared-state writers per Law 6), keeps 13 including run_shell/run_python (dual-use kept by default so lanes keep their fetch/compute path; strict mode strips them too).

## 3. Checks actually run this session (exact commands)

1. `./.venv/Scripts/python.exe -m py_compile mag/write_strip.py mag/agent_cli.py mag/orchestrator.py main.py` -> COMPILE_OK.
2. `./.venv/Scripts/python.exe -m pytest tests/test_write_strip.py -v` -> **12 passed in 4.58s**. Covers: name classification; the real estate grant (write_file gone, list_dir/read_file/search_files/run_shell/run_python kept, receipt names every strip); input non-mutation; harness-style OpenAI-function fixture (Read/Grep/Glob/Bash/Task kept, Write/Edit/NotebookEdit omitted, kept entries are the same objects); strict mode strips Bash; flat format + empty list + unnamed-schema tolerance; env resolution; activation + backstop refusal (a refused write_file call never touches disk); repack freeze built from the compiled grant; `spawn_task` signature default read_only=True; `--read-only` parses on the real `main.py agent --help`.
3. Regression on the two patched modules: `./.venv/Scripts/python.exe -m pytest tests/test_agent_repack.py tests/test_orchestrator_queue.py tests/test_context_freeze.py` -> **14 passed in 30.35s**.
4. Live child-side smoke (no model call, no spend): env MAG_READ_ONLY=1 -> `read_only_from_env()` = (True, False); `activate_read_only()` stripped ['write_file', 'pheromone_drop', 'blackboard_post'], kept 13 of 16, notice renders, `restore_full_grant()` returns to 16.

Not run (honest gaps): no live fan-out wave was fired under the new flag (spend + a fresh burn are outside this chore); no ZCode-harness test exists because no harness code was touched. Also still owed from the source rows: write-delegation#4's pre-registered ablation (one write-tools-present wave vs one schema-stripped wave, corrupted/duplicated writes counted) is a wave-scale experiment and remains open; this discharge builds its schema-stripped arm and its receipt format.

## 4. SPEC ROW: the ZCode-harness change (spec-only, NOT built here)

The estate runner patch enforces write-strip only over seats the estate itself spawns (`main.py agent` children). Lanes fanned out by the ZCode harness (dynamic-workflow `agent()` spawns, e.g. `.zcode/workflows/mickey17-v2.dwf.ts`) get their tool schemas from the harness, which the estate does not own. The spec'd change, filed for the harness owner and deliberately not implemented in this repo:

- **Spec:** the `agent()` spawn facade accepts a tool-schema restriction at spawn time (runner-side compile of the child's visible tool list, write tools omitted before the child's first model call, per "the LLM never sees tool definitions it cannot use", arXiv:2603.05344v3 via write-delegation#0), plus a denied-name backstop that refuses an invented write with a typed error instead of a permission prompt. Pinned model + typed results already exist harness-side (ZCODE_REPO_STEAL_MAP_20260924.md, persist-before-spawn + pinned-ModelSelection convergences); this adds the fourth leg: pinned SCHEMA.
- **Why spec-only:** the harness is not estate-owned; patching it from here would be out-of-repo mutation. The runner-side patch keeps the estate's own fan-out law-complete today.
- **Adoption test for whoever takes it:** one harness `agent()` spawn with the restriction returns tool definitions lacking Write/Edit; a forced write call returns the typed refusal; the spawn receipt records the stripped names.

## 5. Falsifier

- `git diff mag/orchestrator.py` shows `read_only: bool = True` on spawn_task; any call site that flips it to False and then mutates shared state is the exception the record must name.
- If a future agent_cli grant renames write_file, `WRITE_TOOL_NAMES` must gain the new name or the strip silently narrows; the receipt's `stripped_names` per spawn is the audit hook.
- tests/test_write_strip.py failing on the estate-grant precondition ("estate grant carries write_file") means the grant changed shape; reclassify before trusting the strip.
