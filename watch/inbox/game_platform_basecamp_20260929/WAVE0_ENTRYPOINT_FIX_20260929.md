# WAVE0 ENTRYPOINT FIX -- 2026-09-29 (Mickey17 run plan)

Plan: `watch/inbox/MICKEY17_RUN_PLAN_20260929.md` WAVE 0 (fix the test entrypoint).
Executor: ZCode subagent, account zai individual coding plan.

## What changed (minimal diffs, all byte-verified by the runs below)

1. `requirements.txt` -- added `cryptography>=49.0.0` (49.0.0 verified present in
   the venv via `pip show cryptography`; it was missing from the file while the
   venv had it, so gwap signature tests silently self-skipped on any fresh
   requirements-only venv). Fix comment carries the receipt inline.
2. `tests/test_blade_templates.py` -- module-level `pytest.importorskip("vastai_sdk")`
   before `import blade_buyer` (blade_buyer hard-imports the vastai SDK at
   `state/vast/blade_buyer.py:33`; pip distribution name is `vastai` 1.5.5, module
   `vastai_sdk`, NOT in requirements.txt). Dated M17 comment.
3. `tests/test_bones_adapter.py` -- module-level `pytest.importorskip("discord")`
   BEFORE the `import discord` line (discord.py 2.7.1 is in this venv but NOT in
   requirements.txt). Dated M17 comment.
4. `pytest.ini` -- `testpaths = tests tools/gps_mcp` so gps_mcp's 28 tests collect
   through the default entrypoint (root `conftest.py` already puts ROOT on
   sys.path, so the package imports resolve).
5. `tests/test_chain_contract.py` -- NEW chain pin (1 test): builds a
   `MountainWorld` (server/world.py), registers a session, stages boil@spring,
   ticks (row appended, chain green), builds a gwap payload whose
   `replay_tape_ref.sha256` IS the tick row's sha, seals it with a fresh
   `gw.author_keypair` via `gw.sign_payload`, asserts `verify_signature` True
   (and the unsigned original False), flips ONE byte of the sealed payload ->
   signature False, flips ONE byte of the world's action row ->
   `verify_log_rows` False and `world.verify_log()` False. Gated
   `skipif(not gw.HAS_CRYPTO)` matching the house pattern in test_gwap_payload.py.

## Real counts (exactly what pytest printed; no fabrication)

- PRE-FIX baseline (before any edit, this venv):
  `pytest --collect-only -q` -> **2595 tests collected**.
  NOTE: this venv already holds `vastai` 1.5.5 (module vastai_sdk) and
  discord.py 2.7.1, so the M17 miner's "collection ERRORS / zero tests run"
  state does not reproduce HERE today; the hard-import fragility is real for
  any requirements-only venv, which the fix below proves by simulation.
- POST-FIX full collection (root, testpaths now tests + tools/gps_mcp):
  `pytest --collect-only -q` -> **2624 tests collected** (= 2595 + 1 chain pin
  + 28 gps_mcp).
- `pytest tests/ -q --co` -> **2596 tests collected** (tests dir alone:
  baseline 2595 + 1 chain pin).
- `pytest tests/test_chain_contract.py tools/gps_mcp/test_gps_mcp.py -q` ->
  **29 passed in 3.40s**.
- `pytest tests/test_blade_templates.py tests/test_bones_adapter.py -q` ->
  **21 passed in 1.62s** (guards skip nothing in this venv; real coverage kept).
- ABSENT-DEP SIMULATION (sys.modules['vastai_sdk']=None, sys.modules['discord']=None,
  same two files): **2 skipped** in 0.70s, collection green, zero errors -- the
  importorskip path works; previously this state was a collection ERROR.
- Keyword slice `pytest -k "chain or server or gwap or gps" -q` ->
  **148 passed, 2476 deselected, 1 warning in 31.89s**.

## Census note (B2-216 denominator law)

Collected counts above are `--collect-only -q` snapshots at distinct moments on
2026-09-29; the M17 plan's "2,578" and "~2,606+" were estimates from an earlier
tree. Name instrument and moment: 2595 collected pre-fix, 2624 collected
post-fix, both this repo this day. The AGENTS.md carrier bullet still carries the
2026-09-27 census (2,303 / 352) and is now 2 days stale with tests/ grown
(+test_chain_contract.py); refreshing that bullet is an operator census-patrol
call, not silently done here.

## What stays owed

- vastai SDK and discord.py remain deliberately NOT in requirements.txt (heavy
  optional runtime deps per the wave order); their tests skip on a lean venv.
  If the operator wants them pinned, that is a separate decision.
- The gwap signature tests' silent self-skip risk is fixed only at the
  requirements level (cryptography pinned); v1 of anything else that grows a
  crypto dependency should follow the same pin-on-land law.
- AGENTS.md census bullet refresh (see census note) + `pytest -q` full-suite
  execution number (only collection + slices were run here; the full run was
  out of WAVE0 scope per the plan).
- gps_mcp README still documents running its tests by explicit path; now they
  ride the default entrypoint (left as is -- doc polish, not entrypoint).
