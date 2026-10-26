# HERMES JOB — run_shell loop fix (2026-09-11)

- ts: `2026-09-11T11:35:03Z` (07:35 EDT)
- seat: hermes (Sancho) — session `20260911_064814_d0a72d`, profile default
- trigger: operator "do it", following the new-day boot receipt (`20260911T1057Z-new-day-boot.md`)
- scope: fix the swallowed-error defect behind FKB signature `run_shell:c73866f2f1b5`

## What was wrong — three seams, one loop

1. `backend/server.py` `/run_task` → `tools.dispatch` **already** returns an actionable refusal:

   `{"ok": false, "exit_code": 2, "error": "bad arguments for run_shell: unexpected keyword argument 'cmd'. Expected flat named parameters: command, timeout=60", "expected_params": [...]}`

   but it lands in the envelope's `result`; the envelope's own `error` stays `null`.
2. `mag/agent_cli.py::_run_tool_http` read only `body.get("error")` → `null` → literal fallback `"backend reported failure"`.
   The remedy was written into `tools/dispatch` on **2026-08-03**, three days before the first failure row; the model never saw it.
3. `tools/_normalize_args` had no `cmd` → `command` alias, so the invented OpenAI-style name was fatal on every call.

## Evidence

- FKB `logs/failure_kb.jsonl`: 27,859,321 bytes. Last-3MB window = 10,198 rows, **7,435** of them `run_shell:c73866f2f1b5`,
  **2,046** `run_python:2e689948ccfa`; newest row `2026-09-11T11:26:31Z` — the loop was live nine minutes before the fix.
- Live repro (backend unchanged): `POST 127.0.0.1:8000/run_task {"tool":"run_shell","args":{"kommand":"echo x"}}`
  → `200 {"ok":false,"ok_error":null,"result_error":"bad arguments for run_shell: ... command, timeout=60"}`.

## Change

| file | hunk | what |
|---|---|---|
| `mag/agent_cli.py` | +701..708, 711..712 (`_run_tool_http`) | surface `result.error` before the literal fallback |
| `tools/__init__.py` | +76, +84 (`_normalize_args`) | nested-blob unwrap falls through instead of early-returning |
| `tools/__init__.py` | +86..95 (`_ARG_ALIASES`) | run_shell: `cmd`/`command_line`/`shell_command`/`script` → `command`; run_python: `python`/`source`/`code_str`/`snippet`/`script` → `code` |
| `tests/test_tool_dispatch_shape.py` | +4 tests | alias; alias∘unwrap; no-clobber; refusal-is-not-a-raise (stubbed `httpx.Client`, no network) |

The alias is a **fallback only**: applied when the advertised name is absent, so an explicit `command` still wins.

## Verification (real output, this session)

- `pytest tests/test_tool_dispatch_shape.py -q` → **13 passed in 0.52s**
- `pytest` across 9 neighbouring suites → **50 passed, 3 failed**. The failures are
  `tests/test_switchboard.py::test_hypervisor_{2,4,5}`, which exercise `mag/switchboard_v2.py` and `mag/policy_engine.py` —
  both **untracked files from another seat's in-flight work** (`git status`: `?? mag/policy_engine.py`, `?? mag/switchboard_v2.py`,
  `M mag/switchboard.py`, `M tests/test_switchboard.py`). Neither is referenced by the code I touched. **Pre-existing, not mine.**
- End-to-end through the patched CLI against the live backend: `_run_tool("run_shell", {"cmd": "echo hermes_probe_alias"})`
  → `{"ok": true, "exit_code": 0, "output": "hermes_probe_alias\n"}` — the call signature that failed 25,007× now succeeds.
- `py_compile` clean on both edited modules.

## Not done (deliberately)

- **No restart.** The running backend (port 8000) still holds the old `tools/__init__.py` in memory; CLI-side normalization
  happens *before* the HTTP call, so worker calls are fixed now, but a direct API caller needs a backend restart to get the alias.
  Sessions already in flight keep their old `agent_cli` copy. Not restarted — operator's call.
- No chain write (no `publish()`), no board/tape write, no Docker action.

## Open findings handed back

1. **The collapse detector cannot see this class of loop.** `mag/agent_cli.py:1501-1522` fires only on 5 *consecutive* identical
   calls within one turn and allows 2 nudges. Failures spread 1-3 per turn across 21 sessions never trip it — which is why a
   five-week loop left no alert. A per-signature counter across the run would catch it.
2. **Another seat's authority gate fails open** (their in-flight code, untouched by me): `policy_engine.validate_authority`
   accepts `granted_capabilities` as a bare string (`"board_write"`) and returns `ok: True`, while its own tests assert fail-closed.
3. `run_python:2e689948ccfa` (2,046 rows in window) will surface its real argument message on the next occurrence; the alias
   covers the likely invented names, but the actual name was never recorded before the fix.

## Files touched this session

`mag/agent_cli.py` (117,861 B) · `tools/__init__.py` (7,960 B) · `tests/test_tool_dispatch_shape.py` (7,113 B)
