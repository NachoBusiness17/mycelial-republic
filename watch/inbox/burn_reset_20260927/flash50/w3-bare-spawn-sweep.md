# w3-bare-spawn-sweep

ITEM: fix ALL subprocess.run calls in tests/test_freshness_gate.py AND
tests/test_warning_monitor.py to carry creationflags. Prove both green. Then
run pytest tests/test_headless_law.py and report the new census total.

## Fix landed

- tests/test_freshness_gate.py: 4 subprocess.run sites carried no
  creationflags (census named all 4). Added module constant at
  tests/test_freshness_gate.py:26-29
  `HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0`
  (same pattern as tools/prepush_paths_changed.py:34-35) and
  `creationflags=HEADLESS,` on all 4 spawn sites (the parametrized CLI
  exit-code run, the --self-test run, and the two hash match/mismatch runs
  in test_cli_hash_match_exit0_mismatch_exit2). Comment text is em/en-dash
  clean; the file's own check test_module_has_no_em_dash_in_filed_text
  passed.
- tests/test_warning_monitor.py: ZERO subprocess.run call sites exist. The
  only `run(` hits (lines 39, 44, 49, 57) are `from mag.warning_monitor
  import ... run` called in-process, not spawns. Nothing to fix; vacuous
  half of the item, reported as such.

## Checks run this ask

1. `.venv/Scripts/python.exe -m pytest tests/test_freshness_gate.py
   tests/test_warning_monitor.py -q` -> `34 passed in 2.20s`. BOTH GREEN.
2. AST scan of the edited file (regex equivalent of the ratchet's
   _spawn_call) -> 0 bare spawn matches remain, 4
   `creationflags=HEADLESS` occurrences.
3. `.venv/Scripts/python.exe -m pytest tests/test_headless_law.py -v`
   -> `2 passed, 2 warnings in 5.61s` (ratchet + os.system ban). GREEN.

## New census total: 41

The ask expected "lower than 91". The 91 is the conftest-era figure
(tests/conftest.py:30 "the 91-site debt"); the live baseline on disk at ask
start was already 42 (state/fuel/headless_census.json,
"bare_spawn_total": 42, sibling descent had already run). Measured with the
law's own instrument (tests/test_headless_law.py `_scan()` invoked via
importlib): 42 -> 41 after my fix.

Lineage: 91 (conftest-era) -> 42 (baseline at ask start) -> 41 (this ask).

Re-baseline executed per the law's named acceptance
(tests/test_headless_law.py:8-10: "re-baseline by editing that file"):
state/fuel/headless_census.json rewritten with the scanner's fresh dict,
{"bare_spawn_total": 41, ...}, same mint format (json.dumps indent=1) as the
test's own self-mint at tests/test_headless_law.py:72-75. File is
gitignored (git check-ignore exit 0), lives on disk only.

### Drift named (not mine, not silently accepted)

42 - 4 (my fixed sites) should read 38, but the scan says 41. Three new
bare-spawn sites landed in the tree since the 42 baseline was minted:

- tools/derived_dag.py:62 `subprocess.run(cmd, **kw)` (+1): FALSE POSITIVE
  of the instrument. kw is seeded by the helper's
  `kw.setdefault("creationflags", ...)` at tools/derived_dag.py:61, so the
  spawn IS headless at runtime; the AST scanner cannot see through the
  **kwargs passthrough. Owner can silence it by inlining the flag or the
  fleet can teach the ratchet kwargs awareness.
- tools/fossil_check.py:73 and tools/fossil_check.py:89 (+2): genuinely
  bare, both `shell=True` (`subprocess.run(..., shell=True,
  capture_output=True, text=True, timeout=300)`). tools/fossil_check.py is
  in a sibling lane's working-tree modified set (M in git status). Not my
  item; left for its owner. Until fixed, any further census GROWTH above 41
  still fails the ratchet, so these two hold the ratchet floor.

## Not run / out of scope

- Full `pytest -q` suite NOT run: the ask names three checks at named scale,
  all executed; a full-suite run on this shared sibling-dirty tree (Q-008
  precedent attributes red to sibling-lane tree state) is outside this item.
- tests/test_warning_monitor.py spawn fixes: none exist (see above).

## Files of record

- tests/test_freshness_gate.py (committed, this item only)
- state/fuel/headless_census.json (re-baselined on disk, gitignored)
- this receipt
