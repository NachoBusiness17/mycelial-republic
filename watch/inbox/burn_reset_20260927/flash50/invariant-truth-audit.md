# Invariant Truth Audit - percolator invariants with count > 100 (item f-06, 2026-09-28)

## Census frame

- Instrument: `memory/percolator/invariants.json`, parsed 2026-09-28 with the repo venv python
  (`.venv\Scripts\python.exe`). Writer of that file: `mag/percolator.py:264`
  (`_compile_invariant`: bumps `count` + `last_seen` on repeat, stores text on first sight).
- Totals measured this session: **352 invariants total, 13 with count > 100** (3.7%). All 13 have
  `domain: "behavioral"`.
- The percolator stores signal text TRUNCATED mid-word (e.g. `http://127.`, `(<=N words, shape`,
  `W0. 3`), so exact-string matching against code is lossy; verdicts below rest on the emitting
  code plus live probes, not on naive string equality.
- Note on denominators (B2-216 habit): registry `count`, behavioral.jsonl row greps, and
  pro-library move copies are three different instruments taken at different moments; both
  numbers are reported where both were measured, never differenced.

## Live probe

One probe script ran this session: `watch\inbox\burn_reset_20260927\flash50\_f06_probe.py`, invoked as
`.venv\Scripts\python.exe watch\inbox\burn_reset_20260927\flash50\_f06_probe.py` (exit 0). It used
only in-process fake HTTP servers (shut down before exit); no real backend was started; no state
was written except the probe's own stdout. Probe outputs are cited below as t1..t9.

## Truth-audit table

| # | id | count | first / last seen | claim (abridged) | verdict | evidence (what I read or ran) |
|---|----|-------|-------------------|------------------|---------|-------------------------------|
| 1 | 212719f4b54d06e9 | 232,214 | 08-30 / 09-27 | `[steer] Elevate with a deliberate ask: frozen prefix (cache-shared) + tight ask (~207 chars) + output contract` | **TRUE, ACTIVE** (with a dedup defect) | Emitter `mag/elevate.py:102-106` builds this exact text into a pro-library move. Live probe t8: `shape_ask("review the embassy packet")` returned `ask_chars=207` (exact match to the "~207 chars" in the text) and a frozen-prefix prompt; `should_elevate` fired True. Live store `memory/improve/pro_library.json`: 26 moves total, **25 are duplicate copies** of this one move (only 1 has `last_used`, 2026-09-27T06:17:52Z, matching the invariant's last_seen). The move is alive; the add path never dedupes. |
| 2 | f0879ec09c3ac3ce | 38,042 | 08-31 / 09-27 | `backend reported failure` | **TRUE, NARROWED to last-resort** | Fallback still in code at `mag/agent_cli.py:772` (`body.get("error") or nested or "backend reported failure"`). Probe t4 against an in-process fake backend returning `{"ok": false, "error": null, "result": null}` reproduced the exact string. Against `{"result": {"error": "bad arguments for run_python: ..."}}` the probe returned the REAL nested error instead, so the 09-28 comment at `mag/agent_cli.py:767-771` (opaque-fallback fix) holds: the message now fires only when both error slots are empty. |
| 3 | 1cfaa99384eef05a | 8,377 | 09-11 / 09-19 | `command not allowlisted: powershell` | **FALSE against current code (fixed)** | Emitter is `tools/shell.py:25`. But `config.py:34-43` `SHELL_ALLOW` now contains `"powershell"` (line 42). Probe t1: `'powershell' in SHELL_ALLOW` -> True, and `run_shell("powershell -NoProfile -Command Write-Output invariant_probe_ok")` returned `ok: true, exit_code: 0, output: "invariant_probe_ok\n"`. The guard no longer rejects powershell; the invariant describes a past guard state. The string emitter itself still exists for genuinely non-allowlisted commands. |
| 4 | ae3af609ff99f27b | 4,027 | 09-19 / 09-26 | `[Errno 2] No such file or directory: 'powershell'` | **FALSE against current code (fixed by B2-85 + B2-375)** | The fix is landed and receipt-carrying: `tools/shell.py:48-65` resolves `shutil.which("powershell")/which("powershell.exe")` with a System32 fallback (comment names sig `run_shell:e566037def80` and "7,964 rows into logs/failure_kb.jsonl since 2026-09-19"); `mag/win_powershell.py:31-50` (`powershell_exe`, B2-375) does the same with fail-closed messaging. Probe t1 ran `run_shell` through that path successfully; probe t2: `powershell_exe()` returned `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.EXE`. Same B2-85 pattern also landed in mag/gpu_ghost.py:85-91, mag/icon_drop.py:193-199, mag/legacy_audit.py:182-188, mag/loop_breaker.py:100-106 (grep-checked). |
| 5 | 78b999e99fa1e05f | 3,473 | 09-26 / 09-27 | `[steer] STOP asking permission / defaulting to operator for clear asks; route decisions not questions.` | **TRUE, ACTIVE** | Live in `memory/improve/pro_library.json` as `pro-1403d46b5d`, kind=steer, effect `"deployed 254x, consumed"`, `last_used 2026-09-27T23:49:49.103346+00:00` (13 ms before the invariant's last_seen 2026-09-27T23:49:49.111344Z: the deploy emits the event the percolator compiles). Backed by `memory/operator_directives.md` (file exists; the operator-guidance template quoting this line is in memory/agent_sessions/orc-*.json). The quantized-thought compiler already flagged the count as "inflated echo - provenance only" (memory/corpus/quantized_thought/instructions_flash.jsonl:10) - the LAW is true, the 3,473 count is echo-inflated. |
| 6 | 1182ee5e2bc05248 | 836 | 08-30 / 08-31 | `backend not reachable at http://127. Start it with: python -m backend.` | **SPLIT: message TRUE, remediation hint STALE** | Probe t4 with `BACKEND_URL` pointed at a closed port reproduced the message verbatim - but current code says `Start it with: python -m backend.server` (`mag/agent_cli.py:780-782`), not `python -m backend`. The invariant's stored hint is a truncation-era text: `backend/__main__.py` does not exist (probe t3: `find_spec("backend.__main__")` -> None), so the literal advice in the invariant would fail; the current hint is correct. Default URL `http://127.0.0.1:8000`, timeout 300s (`mag/agent_cli.py:49-50`, probe t3). |
| 7 | 4f9c02234f4c31a5 | 592 | 08-31 / 09-28 | `source=swarm_health_law improve_queued=0 handoffs=5` | **EMITTER TRUE / LITERAL STALE SNAPSHOT** | The text is one cadence's interpolated log line, format at `mag/improve_loop.py:217` (`detail=f"source={source} improve_queued={n_imp} handoffs={len(handoffs)}"`), called from the health law at `mag/swarm_health.py:209` on `overall in ("degraded", "down")`. Probe t6 (`mag.swarm_health.status()`, probe-only, no law apply): `overall="degraded", agents_up=2, agents_total=7` at 2026-09-28T21:55:13Z - the law path is live and would fire the same emitter on the next applied cadence. `improve_queued=0 handoffs=5` were the values of one 2026-08-30 run, not standing truths. |
| 8 | ff96a7ed10d26da8 | 544 | 08-31 / 09-12 | `[steer] Training rows are accumulating. The pipeline is built but W0.3 is blocked. Surface the gate status before starting new work.` | **TRUE, still blocked today** | The seed vector is unconditional in code: `mag/ghost.py:3369-3371` (`seed_default_vectors`). The W0.3 gate it names is still closed: probe t7 replicated `mag/governor_autorun.py:539-544` read-only - archive dir `C:\Users\foste\Documents\projects\mycelial-republic\data\raw` exists but contains **zero** .zip/.tar/.gz files, verdict `blocked`. `queue/todo.md:61` still says "W0.3 remains BLOCKED on governance decision (archive drop OR 'use exports only' waiver)". |
| 9 | a77444ced5abc2e7 | 446 | 08-31 / 09-28 | `[steer] Verify with git diff / actual file bytes before declaring done. Trust bytes, not reports.` | **NOT STILL TRUE as a deployed steer (SPLIT / superseded)** | Zero copies in the live `memory/improve/pro_library.json` (grep: 0 hits in 26 moves). The text survives only in the gauntlet harness `tools/pupeteer_gauntlet.py:421` and `:944`, where it is added inside `isolated()` (ephemeral test state, never persisted). Today's emissions (last_seen 2026-09-28T17:40:50Z) are learn-fail echo rows `pro-26c919ce5a -> fail (Verify with git diff ...)` from `mag/pro_library.py:254` against move ids absent from the live library (290 rows in memory/facts/behavioral.jsonl by grep, vs 446 in the registry: different instruments, both named here). Additionally the current build-task hint at `mag/steer_telemetry.py:63` prescribes the OPPOSITE instrument: "verify via OUR systems (get_errors + read the actual file bytes on disk). Do NOT use git diff." The trust-bytes principle is alive; this particular git-diff phrasing is no longer a served move. |
| 10 | 15ab53aafd718f09 | 364 | 09-13 / 09-22 | `write_file missing path=[U+2014 in stored text] emit flat JSON {"path": ...} (sibling keys, not nested arguments blob)` | **TRUE** | Guard at `mag/agent_cli.py:708-714` (msg at 711), remedy-card join at 735-738 via `mag/remedy.py:120` (`prevent`, pure lookup, read-only). Probe t5 called `ac._preflight_tool("write_file", {"content": "x"})` and got the exact message plus the `[REMEDY write_file sibling params]` card appended. (Stored invariant text contains one U+2014 em-dash; sanitized here per repo law.) |
| 11 | d5c42653281b6828 | 171 | 08-31 / 09-26 | `5x identical run_python calls` | **TRUE (mechanism intact)** | Collapse detector `mag/agent_cli.py:1642-1662`: window of 5, fires when `len(collapse_window) == 5 and len(set(collapse_window)) == 1`, logs `detail=f"5x identical {name} calls"` (generic over tool name, so run_python and run_shell variants come from the same line), injects a `[COLLAPSE DETECTOR]` nudge, capped at 2 nudges (`collapse_nudges < 2`). Probe t9 confirmed both the threshold expression and the detail format are present in the imported module source. Not end-to-end exercised (it sits inside the agent turn loop, not a callable unit); verified by source read + source-presence probe, stated as such. |
| 12 | 0d01815e2fb9d5ca | 165 | 08-31 / 09-22 | `5x identical run_shell calls` | **TRUE (same detector as #11)** | Same `mag/agent_cli.py:1655` emitter, `{name}` = `run_shell`. Same verification limits as #11. |
| 13 | ddf94e08b17b9c92 | 114 | 09-22 / 09-22 | `run_python snippet too short - likely a degenerate loop, not a real task` | **TRUE** | Guard at `mag/agent_cli.py:727-730`, threshold `len(code) < 12` (probe t9 confirms). Probe t5 called `ac._preflight_tool("run_python", {"code": "print()"})` and reproduced the exact message plus the `[REMEDY dim NameError silent swallow]` card. |

## Scoreboard

| Verdict | n | ids |
|---|---|-----|
| TRUE (active or mechanism intact) | 8 | 212719f4b54d06e9, f0879ec09c3ac3ce (narrowed to last-resort), 78b999e99fa1e05f, ff96a7ed10d26da8, 15ab53aafd718f09, d5c42653281b6828, 0d01815e2fb9d5ca, ddf94e08b17b9c92 |
| FALSE against current code (fixed) | 2 | 1cfaa99384eef05a, ae3af609ff99f27b (both powershell, both closed by the 2026-09-26 B2-85/B2-375 landings) |
| Split / stale | 3 | 1182ee5e2bc05248 (hint stale), 4f9c02234f4c31a5 (literal is a one-run snapshot), a77444ced5abc2e7 (no longer a served move; superseded text) |

8 + 2 + 3 = 13 = all invariants over the count>100 line.

## Findings worth folding

1. **Counts are echoes, not prevalence.** The top invariant (232,214) is a steer move recompiled on
   every deploy; the quantized-thought compiler already labeled the #5 law "inflated echo -
   provenance only". Registry counts must never be read as failure frequencies (B2-216 habit
   applies inside the percolator itself).
2. **The percolator never deletes.** Both FALSE invariants (powershell pair) keep counting 0 new
   rows since their fixes landed (last_seen 09-19 / 09-26 vs today 09-28), but nothing marks them
   fixed or retires them; they will sit at count>100 forever as fossils unless a truth-audit like
   this one retires them by name.
3. **Dedup defect at the move store.** 25 of 26 pro-library moves are byte-identical copies of one
   Elevate move (`mag/elevate.py:102` -> `mag/pro_library.py` add path never checks for an existing
   identical move). The invariant for it is one canonical text; the store behind it is 25 copies.
4. **Truncated storage loses verifiability.** Invariant texts are cut mid-token (about 128 chars),
   which is why #6's remediation hint and #8's "W0. 3" are garbled; the fix would be to store the
   emitter path alongside the text in `_compile_invariant` (`mag/percolator.py:264-288`).

## Receipts

- Ask: item f-06, "read memory/percolator/invariants.json, test each count>100 invariant against
  current code, bank a truth-audit table".
- Commands run this session (all via repo venv, no bare python):
  - `.venv\Scripts\python.exe` inline parses of invariants.json + pro_library.json (352 total, 13
    over 100; 26 moves, 25 Elevate copies, 0 git-diff copies)
  - `git grep` sweeps for each invariant's emitting string (hits cited per row)
  - `.venv\Scripts\python.exe watch\inbox\burn_reset_20260927\flash50\_f06_probe.py` (exit 0,
    outputs t1-t9 cited above)
  - `sed -n` reads of mag/agent_cli.py (690-800, 1630-1680), mag/swarm_health.py (190-230),
    mag/ghost.py (3355-3385), tools/pupeteer_gauntlet.py (415-430, 938-950),
    mag/improve_loop.py (180-240), mag/governor_autorun.py (530-560), mag/percolator.py (240-300),
    tools/shell.py, mag/win_powershell.py, mag/steer_telemetry.py, mag/elevate.py, mag/remedy.py
- Not run: the full pytest suite (not asked); end-to-end firing of the collapse detector inside a
  live agent turn (not callable as a unit; verified by source read + source-presence probe only).
