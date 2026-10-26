# AG6 — CURRENT.md probe-stub + stale-ANCHOR guards (audit finding #5)

- **date:** 2026-09-30 (operator clock; UTC stamps in artifacts say 2026-09-30)
- **seat:** ZCode subagent, execution lane
- **scope:** guards only — content refresh of `memory/plans/ANCHOR.md` deliberately NOT done (operator call)

## Cause (audit finding #5)

1. `watch/inbox/gala_20260925/wave5-repair/lanes/old-files.escalate_probe.py` ran `agents/escalate_grok.py::escalate_grok_node` against a fake harness; its runtime `audit.sync_current` write landed **"probe run (fake harness)" / "old-files probe"** in the LIVE brief `state/CURRENT.md`, which every seat reads as truth.
2. `memory/plans/ANCHOR.md` carries a `## Status 2026-08-03` block; `mag/agent_cli.py _system_prompt()` injected it into EVERY agent session for 58 days.

## Guards landed

### 1. Scratch routing — probe/test writers leave the live brief alone

- `config.py`: `current_scratch()` / `current_md()` — `MAG_CURRENT_SCRATCH=1` resolves the writer to `state/CURRENT.scratch.md`; readers keep `CURRENT_MD`.
- `audit.py`: `_current_target()` — scratch env outranks everything (a leaked probe can never reach production); with no env, production writers and the pre-AG6 `audit.CURRENT_MD` test-override seam (tests/test_resume_contract.py) behave exactly as before. Scratch writes append a `current-scratch-write` row to `logs/router.jsonl`.
- Precedence: scratch env > explicit override > production `CURRENT.md`.
- `--scratch` flag decision: the env at the `audit.sync_current` choke point covers ALL writers past and future (router graph, agent_cli `_sync_current`, any probe invoking graph nodes); the gala probe script itself is a receipt artifact under `watch/inbox/` and was NOT edited — rerun it with `MAG_CURRENT_SCRATCH=1`.

### 2. ANCHOR freshness guard — staleness is loud, not injected

- `mag/agent_cli.py`: `_anchor_age_days()` parses `## Status YYYY-MM-DD` from the FULL file; `_anchor_injection()` REFUSES to inject when the stamp is older than `PACK_STALE_DAYS` (7 — same bar as `tools/freshness_check.py`, imported, not redefined) or absent (`ANCHOR-STALE -1`).
- Instead of the anchor it injects an in-band marker: `## Anchored plan withheld (ANCHOR-STALE <days>)` naming the file, the age, and that refresh/re-stamp is an operator call; plus ONE `{"event": "ANCHOR-STALE", "days": N}` row in `logs/router.jsonl` (latched per process).
- `memory/plans/ANCHOR.md` untouched (content refresh = operator call; stamp-only also declined — a stamp without content re-verification would lie).

### 3. Sanctioned one-time write of `state/CURRENT.md`

Replaced the probe stub with the honest one-liner via the production writer (`audit.sync_current`, route `operator`): goal **sovereign game platform last-mile**, latest result → `watch/inbox/last_mile_20260930/AC_WAVE_SYNTHESIS.md`.

## Evidence

- Live-fire against the real anchor (2026-09-30): `age_days: 58` → refused, marker injected, router row logged: `{"event": "ANCHOR-STALE", "days": 58, "anchor": "memory\\plans\\ANCHOR.md"}`.
- `pytest -q` executed (repo venv): `tests/test_current_anchor_guards.py` + `tests/test_resume_contract.py` = **13 passed**; neighbors (`test_realign`, `test_session_route`, `test_agent_repack`, `test_agent_desk`, `test_write_strip`, `test_tool_dispatch_shape`, `test_env_redirect_tripwire`) = **54 passed**. Instruments: `pytest -q` outcome sums, 2026-09-30, venv `.venv/Scripts/python.exe`.
- Ratchet: `tools/violation_ratchet.py check --changed` → PASS, NEW=0 (scope 6 changed files).
- New tests: scratch routing (stub text lands in scratch, live brief untouched, log fires), production keeps CURRENT.md, override seam intact, fresh/stale/unstamped anchor fixtures, single-log latch.

## Files

- `config.py` — `current_scratch()` / `current_md()`
- `audit.py` — `_current_target()` + scratch log row
- `mag/agent_cli.py` — `_ANCHOR_STALE_DAYS`, `_anchor_age_days()`, `_anchor_injection()` wired into `_system_prompt()`
- `tests/test_current_anchor_guards.py` — new (8 tests)
- `state/CURRENT.md` — one sanctioned honest write
