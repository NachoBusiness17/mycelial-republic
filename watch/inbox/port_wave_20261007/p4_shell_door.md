# P4 shell door (the contained door) - landed 2026-10-08

Port-order lane P4 from the day-7 mine fold, closing the gap the 2026-10-07
steal round measured. Evidence first, then the build.

## The measured gap (before)

Steal 2 of `watch/inbox/frontier_olm_2026-10-07/steal/open-local-language-models via reddit.md`
(NVIDIA OpenShell thread, lines 54-95) executed a probe against the estate's own
door: `run_python` fired a snippet using only `open()` with a literal absolute
path and wrote a marker OUTSIDE its tempdir; the door returned ok=True, exit 0,
and the marker landed on disk. The probe's own artifacts sit in the same steal
dir: runner at `watch/inbox/frontier_olm_2026-10-07/steal/shell_escape_probe_runner.py`,
banked marker text at `watch/inbox/frontier_olm_2026-10-07/steal/shell_escape_probe.txt`.
The old door's entire containment was a five-pattern substring ban it
self-described as "still not a full sandbox" (the ban text and its confession
are preserved, demoted, at `tools/code_execution.py:109-116`), and the probe
snippet used plain `open()`, which the ban was structurally blind to. The
falsifier the steal named: "any lane's shell must FAIL to write outside its
declared root" (steal doc lines 92-94).

## The build (after): enforcement moved into the spawn, four layers

- L1 pre-exec static allowlist, `tools/exec_gate.py:186` (`static_path_gate`)
  with the resolve + normalize helper at `tools/exec_gate.py:36`: parses the
  snippet AST before any process exists, folds literal string parts
  (Constant, all-literal f-strings, Add chains, all-literal `os.path.join`,
  single-binding variable assignment), resolves + normalizes with
  normcase/realpath, and refuses any absolute write path outside the declared
  writable root. The declared root is the owned run root
  (`tools/code_execution.py:72-76`), deliberately NOT the whole OS temp
  prefix: during gate bring-up a live attack run proved a marker dropped as a
  sibling OF the run root sailed a temp-prefix allowlist, so the root was
  tightened and the attack is now a standing test
  (`tests/test_shell_door_containment.py:146`).
- L2 demoted lint, `tools/code_execution.py:115-123`: the old five-pattern ban
  kept as a cheap redundancy layer (exit 126), commented as "not the
  containment".
- L3 spawn containment: the Job Object wrapper is the class at
  `tools/exec_job.py:35` (pywin32 first, ctypes otherwise) and the ctypes job
  fallback test is `tests/test_shell_door_containment.py:200`. The cap is a
  per-call cap with a floor that a test or lane can tighten
  (`tools/exec_job.py:17-22`), plus UI restrictions (`tools/exec_job.py:16`).
  The run entry point is `run_python` (`tools/code_execution.py:181`). It
  spawns with CREATE_NO_WINDOW plus the historical filtered env (TEMP/TMP
  added so the child's own tempdir resolves to the audited root), assigns the
  child to the job immediately, terminates the whole job tree on timeout, and
  closes the handle in a finally so kill-on-close is the hang and crash
  backstop.
- L4 post-exec audit + loud failure, `tools/code_execution.py:154`
  (`_audit_run`): a random-byte canary placed beside the run is hash-checked
  after the run and the run-root top level is walked; any tamper, missing
  canary, or unexpected sibling entry fails the door with exit 125, a
  structured violation row in the result, and an append to
  `tools/code_execution.py:78` (`logs/exec_shell_violations.jsonl`), with the
  post-audit sweep at `tools/code_execution.py:295-304` (docstring: audit
  already banked the violation, the sweep removes the escape bytes) so one
  caught attack cannot poison later audits.

## Exploit, before and after (live, this seat, this session)

- Before (steal round, byte-banked artifacts): ok=True, exit 0, marker on disk.
- After: the same attack in the steal runner's variable-bound literal form was
  re-run live against the new door: ok=False, exit 125, error
  "containment violation: static_path_gate", marker never on disk. The
  computed-path variants trip the audit layer the same way, encoded as
  standing falsifier tests. The steal round's attack shape: a literal absolute
  marker path outside the run root must be refused pre-exec with a violation
  row (`tests/test_shell_door_containment.py:53-79`). A computed-path write to
  the canary beside the run is caught by the post-exec hash check
  (`tests/test_shell_door_containment.py:82-90`). A marker written to a
  sibling of the tempdir lands in the owned run root, flagged by the audit
  walk; the sweep removes it (`tests/test_shell_door_containment.py:92-108`).

## What Job Objects give and do not give on Windows (honest limits)

Give: process memory cap (a 96MB-capped child allocating 512MB dies with
MemoryError, `tests/test_shell_door_containment.py:164`), tree-wide kill on
timeout/handle close (grandchildren included), and UI restrictions (clipboard
read/write, global atoms, exit windows). Do NOT give: filesystem, network, or
registry isolation; Windows without a container has no child-FS sandbox, so
filesystem containment here is app-level by design (L1 literal gate + L4 canary
and audit), and three limits are stated in the module contract
(`tools/code_execution.py:38-45`): the Popen-then-assign race leaves a
microseconds window before the job binds (L1 runs before any process exists, so
the proven exploit class is refused regardless); the static gate sees only
literal paths (computed paths fall to L4 and the caps); the canary proves its
own path and the run root, not arbitrary far-field writes. On non-win32 there
is no Job Object; gate + audit still run (platform guard in
`tools/exec_job.py:42-43`).

## Integration (read, not modified)

`mag/effect_broker.py` stays the authorization layer on top, untouched by this
lane: model_call and lane_spawn are the effect classes policy-forbidden to
dispatch headless and board_write is the one production-legal headless class
(`mag/effect_broker.py:374-380`). That range authorizes effects one level
above this door; the door's own job is narrower, constraining where a
dispatched shell can reach. Caller census for the door: the gopher
fleet's TOOL_MAP and signature registry in `tools/__init__.py` (run_python
wired as a tool callable), the agent CLI dispatch in `mag/agent_cli.py`, the
MCP tool table in `mag/mcp_server.py`, and the CRITICAL_TOOLS flag in
`backend/server.py` all keep working unchanged because the public signature
(code, timeout=30) and result shape (ok, exit_code, output, error) are
preserved; the violation row is additive. Verified through the real caller
path this session: TOOL_MAP["run_python"] ran a clean snippet ok=True, exit 0.

## Gates

- `pytest tests/test_shell_door_containment.py -q` (venv python): 12 passed.
- Related existing suites re-run after the split (`tests/test_tool_dispatch_shape.py`,
  `tests/test_write_strip.py`, `tests/test_failure_kb.py`): 35 passed.
- `pytest ... --collect-only -q` on the new suite: zero collection errors.
- `tools/violation_ratchet.py check --changed`: PASS, NEW=0 (final read,
  scope 34 changed files). Two mid-build debts were fixed, not accepted: an
  except-pass in the sweep (errors now returned and surfaced on the result)
  and a file-too-long on `tools/code_execution.py` (652 lines) cured by the
  L1/L3 split into `tools/exec_gate.py` and `tools/exec_job.py` (323 + 217 +
  140 lines). One transient NEW file-too-long on `mag/llama_cpp_bridge.py`
  during bring-up was a sibling lane's uncommitted drift, not this lane's.
- Em/en-dash scan over the four touched files: zero hits.
- No git commit (lane law).

## Files

- Rewritten: `tools/code_execution.py` (the door).
- New: `tools/exec_gate.py` (L1), `tools/exec_job.py` (L3),
  `tests/test_shell_door_containment.py` (12 falsifiers), this receipt.
- Violation ledger seeded: `logs/exec_shell_violations.jsonl` (bring-up rows,
  including the two false-positive rows from the temp-prefix tightening that
  produced the standing sibling test).

## Blockers / handoff

None for this lane. Two named follow-ups: the microseconds job-assign race
could be closed with a Win8+ PROC_THREAD_ATTRIBUTE_JOB_LIST spawn attribute
(not built; L1 already covers the proven class); `run_shell` (the sibling door
in tools/shell.py) still has prompt-era containment and is the natural P5.
