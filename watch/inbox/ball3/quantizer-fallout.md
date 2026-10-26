# quantizer-fallout (division B, ball3-suite-green) - receipt

Date: 2026-09-29. Lane: quantizer-fallout. Owed work as dispatched: repair nine
downstream tests allegedly still encoding OLD (pre-v0.4) pack shapes after the
quantizer-hygiene lane's compile change (L1 shell-error refusal tightening, L3
PACK_STALE_DAYS unification, L4 kept==packed linker).

## Verdict

**The premise did not hold at byte level. All nine named tests are already
green; zero edits were needed or made by this lane.** The v0.4 expectation
repairs were banked by the quantizer-hygiene lane's own commit 93f85e0dd
(BALL 20260929, 2026-09-29 13:32:26 EDT), which updated
`tests/test_thought_quantizer.py` IN the same commit as the code:

- `test_compile_end_to_end`: expectation strengthened `compiled-v0.3` ->
  `compiled-v0.4` (no assertion weakened; shape + flash-cap assertions kept),
  `git show 93f85e0dd -- tests/test_thought_quantizer.py`.
- Added and passing: 5 L1 refuse pins
  (`test_shell_error_fragment_refuses[...]`), `test_shell_error_with_genuine_norm_keeps`,
  `test_decay_constant_defined_once_and_imported_at_three_sites` (L3: identity
  `is DEFINED` across producer `tools/thought_quantizer.py:55`, consumer
  `mag/context_pack.py:14`, boot meter `tools/freshness_check.py:39`, value 7),
  `test_linker_kept_equals_packed_with_remainder` +
  `test_linker_fails_loud_when_caps_undercover` + `test_linker_flash_takes_top_rank`
  (L4 disjoint bands, kept==packed).

The other five named files never encoded pack shapes at all (coupling audit by
read + grep, recorded in the lane JSON): test_seat_corpus compiles
providers.yaml, test_openclaw_catalog scans CLIs, test_roadmap_runner writes
build docs, test_token_chain reads memory/improve files. Whatever made them
fail in the 42:05 snapshot, it was not quantizer fallout and does not
reproduce. No receipt of the 42:05 run (19F/2529P) exists anywhere I searched
(watch/inbox/gala_20260925/, watch/inbox/ball2/, logs/) - the failure modes at
that moment cannot be named from evidence, only the current byte truth can.

Corroborating receipt from the prior ball:
`watch/inbox/gala_20260925/ball-20260929/lanes/quantizer-hygiene.json` CHECK 5
already recorded `pytest tests/test_mcp_bridge_r1.py -q` = 22 passed, so the
bridge test named in the dispatch was green before this ball started.

## Checks run this ask (raw output cited)

1. Finish line (the named check): `.venv/Scripts/python.exe -m pytest
   tests/test_thought_quantizer.py tests/test_context_pack_quantized_laws.py
   tests/test_mcp_quantized.py
   tests/test_seat_corpus.py::test_compile_has_deepseek_thinking_off
   tests/test_openclaw_catalog.py tests/test_roadmap_runner.py
   tests/test_token_chain.py tests/test_mcp_bridge_r1.py -v`
   -> **62 passed, exit 0**. All nine named tests verified PASSED by name.
   Raw: `watch/inbox/gala_20260925/ball3-suite-green/lanes/quantizer-fallout.check.txt`
2. Authoritative full suite, same instrument as the dispatch's snapshot:
   `.venv/Scripts/python.exe -m pytest -q` (serial) -> **2 failed, 2566
   passed, 12 skipped, 47:01, exit 1**. Raw:
   `watch/inbox/gala_20260925/ball3-suite-green/lanes/quantizer-fallout.fullsuite.txt`
   Neither failure is one of the nine; the six lane files are green inside the
   full run.
3. `grep -rn "compiled-v0.3" tests/ mag/ tools/` -> zero hits: no stale
   pack-shape encoding survives anywhere.
4. `git status --short` on all lane-scope files (six test files + contract
   files + tools/thought_quantizer.py + mag/constants.py + mag/context_pack.py
   + tools/freshness_check.py) -> clean: this lane edited nothing.

## The two REAL remaining suite failures (not this lane's files - for the orchestrator to route)

Both reproduce against the current working tree, which carries uncommitted
sibling-lane work (mag/game_campaign.py, tools/stealth_driver.py +49,
tests/test_stealth_tools_wave5_repair.py are modified by siblings):

1. `tests/test_game_world_render_optics.py::test_internal_node_grows_after_enough_leaves`
   - `assert saw_grok is not None` fails: 8-direction grove reveal produced no
     grok (game/B0 lane territory; mag/game_campaign.py is mid-flight in the
     tree). Full-suite raw lines: test body at
     tests/test_game_world_render_optics.py:60.
2. `tests/test_stealth_tools_wave5_repair.py::test_instance_lock_refuses_second_acquire`
   - `stealth_driver.InstanceLocked` on acquire at
     tests/test_stealth_tools_wave5_repair.py:128: the test calls
     `acquire_instance_lock()` without the `namespace` arg, so it contends
     with the LIVE driver's production mutex `Local\MagStealthDriverInstance`.
     The namespace escape exists and its own docstring names "ball3
     driver-meter 2026-09-29" as the adder - the driver-meter lane holds the
     active claim on this file (it is modified, uncommitted, in the tree).

## Ratchet

Step 3 of the dispatch is conditional on touching code under mag/ or tools/:
this lane touched none (check 4 above), so the conditional does not fire and
`tools/violation_ratchet.py check --changed` was not run as a lane check. Note
the working tree also carries sibling modifications under mag/ and tools/, so
a `--changed` run from this seat would measure sibling debt, not this lane's.

## Uncommitted pack state (inherited, flagged, not smoothed)

The v0.4 recompile of the REAL packs is working-tree-only, uncommitted:
`memory/corpus/quantized_thought/compile_report.json` at HEAD is still v0.3
(2026-09-27) while the tree holds v0.4 (2026-09-29T15:18:39Z, kept 374 ==
packed 374, packs 24/12/338). Flagged here because the 93f85e0dd commit
message says "fresh compile_report committed" - at HEAD that claim does not
hold for the report bytes. Not this lane's file to commit.

## Decision ledger

Closes: the quantizer-fallout owed work from the 42:05 post-ball suite - by
byte-verification rather than by repair: the fallout was already healed in the
hygiene lane's own commit, and the nine are green at both isolation and
full-suite scale. Changes: no law, no expectation, no code. The ball's
"authored suite-green" claim should carry the 2 real failures named above with
their owning lanes.
