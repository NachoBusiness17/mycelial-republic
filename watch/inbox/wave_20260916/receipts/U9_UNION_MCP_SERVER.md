# U9 — UNION MCP SERVER (ractor-salon real stdio server)

- **Date:** 2026-09-16
- **Lane:** wave_20260916 / U9
- **Worker law:** stealth/union-alpha drafts (OPENROUTER_API_KEY via `mag.flight_recorder.load_env`, never printed); ZCode is editor. $0 spend target.
- **Target repo:** `C:\Users\foste\Documents\projects\ractor-salon\` (standalone, v0.1.0) — P1 left a dependency-free stdio MCP stub (`src/ractor_salon/mcp_server.py`) + `mcp.json`. U9 replaces the stub with a REAL server.
- **Contract:** three tools over JSON-RPC/stdio (`initialize`, `tools/list`, `tools/call`):
  1. `salon_run` — `{question, lanes?, seeds?}` → probe lanes, fan out, return the fold (reuses `src/ractor_salon/salon.py`)
  2. `salon_lanes` — `{}` → lane registry + last probe status
  3. `salon_fold` — `{tape_path}` → Rashomon fold of an existing tape
- **Test law:** OFFLINE only — pipe initialize + tools/list + one tools/call (fake-lane transport) as JSON lines via stdin; `tests/test_mcp_server.py`; pytest via `.venv\Scripts\python.exe`.
- **Commit law:** commit NOTHING — standalone repo's next commit is a grouped pass after operator scrub.

## Log

### STEP 1 — read stub + src (done)

- `src/ractor_salon/mcp_server.py`: dependency-free JSON-RPC/stdio stub — tools `probe_lanes` / `run_salon` / `salon_status` (old contract), handshake only.
- `salon.py`: `run(questions, *, lanes, env, out_dir, mode, workers, timeout, retries, opener, …)` — probe-first, append-only tape, retry appends, `pack.md` fold, `receipt.json`. `status(out_dir)`.
- `lanes.py`: `Lane(id, base, model, key_env, role)`, `DEFAULT_LANES` (11 lanes), `merge_env`, `probe_lanes(opener=…)` — injectable transport exists at every layer.
- `receipts.py`: `Tape` (append-only, sha256 digest), `fold_markdown` (Rashomon, deterministic).
- `pyproject.toml`: `ractor-salon-mcp = ractor_salon.mcp_server:main` console script already bound; `mcp.json` command `ractor-salon-mcp` — entry points stay valid, the module behind them becomes real.
- Harness venv has pytest 9.1.1 / Py 3.11.15; `ractor_salon` NOT installed there → adding `tests/conftest.py` src-path shim instead of `pip install -e` (no build artifacts before the operator's scrub).
- Existing `tests/test_salon.py` gives the fake-transport pattern (`FakeOpener`, `RACTOR_SALON_DNS_CHECK=0`, `RACTOR_EXTRA_BASES`).
- U9 contract decision: `salon_run{question, lanes?, seeds?}` — `seeds` = cap on live lanes seeded into the fan (registry order) → needs a minimal additive `max_lanes` param on `salon.run` + `summary["probe"]` exposure so `salon_lanes` can report last probe status. `question` is a single string (fold of one question, every live lane).
- Tool set REPLACES the stub trio: `salon_run` / `salon_lanes` / `salon_fold`.

### STEP 2 — union-alpha prompt (exact JSON-RPC contracts)

- Prompt: `drafts/u9_union_prompt.md`; caller: `u9_union_call.py` (u1 pattern; key via `mag.flight_recorder.load_env`, never printed; stream; 3-attempt degrade law).
- Draft target: `drafts/u9_union_draft_server.py`.

### STEP 3 — editor pass (the real server)

- `src/ractor_salon/mcp_server.py` — REPLACED. Full JSON-RPC 2.0 stdio frame:
  `initialize` (protocol negotiation: echo client version if in `{2024-11-05, 2025-03-26, 2025-06-18}`, else `2024-11-05`), `notifications/initialized` (never answered), `ping`, `tools/list`, `tools/call`, `-32700` parse (id null), `-32600` invalid request, `-32601` method-not-found, `-32602` unknown tool. Tool failures are NORMAL results with `isError: true` (a failure is a row, not an exception — package law mirrored at the protocol layer).
  - `salon_run{question, lanes?, seeds?}` → filters `DEFAULT_LANES` by `lanes` (unknown ids reported in `summary.unknown_lanes`, never dropped), `seeds` → `salon.run(max_lanes=…)` cap on live lanes seeded (registry order), calls `salon.run([question], env=merge_env(None), opener=<injected>)`, caches `summary["probe"]` into `_LAST_PROBE`, returns `{ok, summary, fold}` (fold read from `summary["pack"]`), `isError = not ok`.
  - `salon_lanes{}` → registry rows `{id, model, role, key_env, keyed}` from env + `last_probe` (or null + note).
  - `salon_fold{tape_path}` → `Tape.rows()` + `fold_markdown` + digest; missing tape = isError result. Fully offline.
  - Test seams: `serve(stdin, stdout, opener=…)` transport injection; `REGISTRY` module attr for fake lanes; keys env-only, never echoed.
- `src/ractor_salon/salon.py` — minimal additive edit: `run(..., max_lanes: int | None = None)` caps `live` after probe; summary gains `"max_lanes"` + `"probe"`. Backwards compatible; existing suite untouched behavior.
- `tests/conftest.py` — NEW: src-layout path shim so the suite runs from a checkout without `pip install -e` (no build artifacts before the operator's scrub; harness venv does not have the package installed).
- `tests/test_salon.py` — removed the superseded stub-handshake test (old tool names `probe_lanes`/`run_salon`/`salon_status`); MCP coverage moved to the dedicated file.
- `tests/test_mcp_server.py` — NEW, 18 offline tests: in-process stdio sessions over StringIO (initialize negotiation + fallback, notification silence, ping, tools/list exact-three-with-schemas, salon_run end-to-end over a scripted fake transport incl. preserved 429 retry, seeds cap, lanes restriction + unknown reporting, no-keys error result, empty question, salon_lanes registry→last_probe transition, salon_fold refold + missing tape, −32602 old stub name rejected, −32601, −32700, plus a REAL `python -m ractor_salon.mcp_server` subprocess stdio smoke).

### STEP 4 — pytest (harness venv, offline) — VERBATIM

```
$ cd C:\Users\foste\Documents\projects\ractor-salon
$ C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe -m pytest -q

...................................                                      [100%]
35 passed in 0.51s
```

New file verbose (same run conditions, earlier pass — names for the census):

```
tests/test_mcp_server.py::test_initialize_echoes_supported_version PASSED
tests/test_mcp_server.py::test_initialize_falls_back_on_unknown_version PASSED
tests/test_mcp_server.py::test_notification_gets_no_response PASSED
tests/test_mcp_server.py::test_ping_answered PASSED
tests/test_mcp_server.py::test_tools_list_exposes_exactly_the_three_tools_with_schemas PASSED
tests/test_mcp_server.py::test_tools_call_salon_run_folds_offline_end_to_end PASSED
tests/test_mcp_server.py::test_tools_call_salon_run_seeds_caps_live_lanes PASSED
tests/test_mcp_server.py::test_tools_call_salon_run_restricts_lanes_and_reports_unknown PASSED
tests/test_mcp_server.py::test_tools_call_salon_run_unknown_only_lanes_is_error_result PASSED
tests/test_mcp_server.py::test_tools_call_salon_run_no_keys_is_error_result PASSED
tests/test_mcp_server.py::test_tools_call_salon_run_empty_question_is_error_result PASSED
tests/test_mcp_server.py::test_salon_lanes_registry_then_last_probe_after_run PASSED
tests/test_mcp_server.py::test_salon_fold_refolds_existing_tape_offline PASSED
tests/test_mcp_server.py::test_salon_fold_missing_tape_is_error_result PASSED
tests/test_mcp_server.py::test_unknown_tool_is_invalid_params_not_a_crash PASSED
tests/test_mcp_server.py::test_unknown_method_is_method_not_found PASSED
tests/test_mcp_server.py::test_parse_error_line_answers_with_null_id PASSED
tests/test_mcp_server.py::test_subprocess_stdio_smoke_initialize_and_tools_list PASSED
============================= 18 passed in 0.46s ==============================
```

Census: 35 passed / 0 failed / 0 skipped (ractor-salon repo; 17 test_salon.py + 18 test_mcp_server.py). Bytes, not reports — run command above reproduces.

### STEP 5 — mcp.json / docs

- `mcp.json`: unchanged by decision — its `ractor-salon-mcp` command already binds (pyproject console script) to `ractor_salon.mcp_server:main`, which is now the real server; adding non-standard keys or a bare `python` (Hermes-venv hazard on this machine) would weaken it. The pointing was correct; the server behind it changed.
- `README.md`: feature bullet now says real server + tool names; new "## MCP server" section (tool table, JSON-RPC surface, keys-env-only posture, `ractor-salon-mcp` invocation); security-posture paragraph de-stubbed.
- `CHANGELOG.md`: `[Unreleased]` section — Changed (real server, tool contract, `salon.run` `max_lanes` + `probe` in summary) and Added (18-test MCP suite, conftest shim). The 0.1.0 entry is left as history.
- Stale-reference sweep: no `probe_lanes`/`run_salon`/`salon_status`/`stub` mentions remain in skills/, docs/, README, mcp.json, plugin.json.

## Union-alpha grade

**DNF — seat unavailable (429 storm), $0 spent, nothing landed.** Two windows (≈8 min apart), 3 streaming attempts each, all `HTTP 429 — stealth/union-alpha is temporarily rate-limited upstream`. Degrade law executed (back off twice, then file what landed — nothing). The exact contract prompt is filed at `drafts/u9_union_prompt.md` with the caller `u9_union_call.py` for a re-run when the free window opens. The server was therefore written editor-direct from that same frozen contract (the prompt IS the spec); when a union-alpha draft eventually lands, grade it by diffing against `src/ractor_salon/mcp_server.py` + the 18-test suite as ground truth.

## `hermes plugins install` smoke expectation (exact)

Prereq: the package must be importable in the Hermes plugin env — `pip install -e .` (or install from the git URL) so the `ractor-salon-mcp` console script exists; without it the MCP host logs `command not found: ractor-salon-mcp` and the server shows as failed/unhealthy.

```bash
hermes plugins install C:\Users\foste\Documents\projects\ractor-salon
hermes plugins enable ractor-salon
```

Expected: manifest `agent-plugins-v1.0.0` accepted → plugin registers the `run-a-salon` skill + the `ractor-salon` MCP server from `mcp.json` (command `ractor-salon-mcp`, empty env, no keys in the file). Smoke, in order:
1. Host connects over stdio → `initialize` answers `{"protocolVersion": <negotiated>, "serverInfo": {"name": "ractor-salon", "version": "0.1.0"}}`.
2. `tools/list` returns EXACTLY `salon_run`, `salon_lanes`, `salon_fold` with the documented schemas.
3. With NO keys exported: `salon_lanes` returns the 11-lane registry, every row `keyed: false`, `last_probe: null` + note — a clean result; `salon_run` returns `isError: true` with `no lanes with keys in env`.
4. With one lane key exported (e.g. `GROQ_API_KEY`): `salon_run {"question": "..."}` probes first, fans the live lanes, and returns `{ok, summary, fold}` with tape/`receipt.json`/`pack.md` under the host CWD's `salon_run/`.

## Commit law

Nothing committed — the standalone repo's next commit is the operator's grouped pass after the scrub. Files touched in `ractor-salon`: `src/ractor_salon/mcp_server.py` (replaced), `src/ractor_salon/salon.py` (additive), `tests/test_mcp_server.py` (new), `tests/conftest.py` (new), `tests/test_salon.py` (stub test removed), `README.md`, `CHANGELOG.md`, `mcp.json` (unchanged by decision). Harness artifacts: `watch/inbox/wave_20260916/drafts/u9_union_prompt.md`, `watch/inbox/wave_20260916/u9_union_call.py`, this receipt.

