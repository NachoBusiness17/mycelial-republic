# Burn lane substrate: test_substrate_identity root-cause fix

Date: 2026-09-27 · Lane: 6/10 burn reset evening · File: `tests/test_substrate_identity.py::test_identity_persistence`

## Root cause (byte-backed)

The failure was NOT a missing real artifact. `mag/state.py` has never existed in this repo:

- `git log --oneline --all -- mag/state.py` → empty (zero commits ever touched that path).
- The test (landed in d575bc168, Codex checkpoint 2026-09-14) built its fixture path as
  `Path(__file__).parents[2] / "mag" / "state.py"`. Two compounding defects:
  1. **Wrong parents index**: `parents[2]` from `tests/test_substrate_identity.py` resolves to
     `Documents/projects/` (one level ABOVE the repo root); the repo root is `parents[1]`.
  2. **Imagined module**: `mag/state.py` with a module-level `IDENTITY` dict never existed.
     The observed failure was `FileNotFoundError: ... Documents\projects\mag\state.py`.

The real identity record is the canonical `{session_id, provider, model}` run-identity triple in
`mag/agent_cli.py`: `load_run()` (resolves env `MAG_AGENT_SESSION` / `MAG_PROVIDER` / `MAG_MODEL`,
falling back to the persisted seat session) and `normalize_seat()` (coerces to the canonical
shape) at `mag/agent_cli.py:1855` and `:1875`.

## Fix (same intent, real API, not weakened)

Rewrote the test to keep its documented intent (identity constant across a simulated substrate
migration via module re-init) but target the real recorder:

- `_load_identity()` pins the three env inputs, calls `agent_cli.load_run()`, restores env in a
  `finally` (hermetic: the disk-fallback branch of `load_run` is never consulted since
  `MAG_PROVIDER` is set; `load_session()` is itself deterministic, returning a fixed dict when no
  session file exists).
- Migration simulation is `importlib.reload(mag.agent_cli)` before re-reading identity.
- Reload safety checked before landing: agent_cli's module level is constant/env-read/lock setup
  only (no threads, no file writes at import), and a live probe showed `load_run()` returns the
  identical triple before and after reload.

No production code changed. The assertion strength is unchanged (full dict equality).

## Real numbers

- Before: `1 failed in 0.62s` (FileNotFoundError on `Documents\projects\mag\state.py`).
- After, file alone: `1 passed in 0.50s`.
- After, neighbors (14 files touching agent_cli/identity: agent_desk, agent_repack, agent_live,
  context_freeze, prompt_steering, repack_integration, resume_contract, run_worth,
  seat_crash_guard, session_route, substrate_identity, t1_steering, tool_dispatch_shape,
  write_strip): **75 passed in 114.25s**.

## One-writer note

`watch/inbox/burn_reset_20260927/substrate.md` created by this lane only (dir existed with
all_seat/dirac_loops45/healthz/no_win; substrate.md absent before this write).
