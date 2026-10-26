# B2-336 suite-wide gap-log pollution gate (2026-09-26)

## Verdict

LANDED. tests/conftest.py now exists (it did not before this lane) with an
autouse fixture setting MAG_GAPS_LOG to a tmp_path file for every test, so
pollution of memory/training/loop_gaps.jsonl is structurally impossible
rather than per-test discipline. The fixture targets the exact seam the
B2-79 fix built (mag/temperature_stack.py _gaps_log reads the env before the
module constant), so any test calling track_loop_gap without a local
monkeypatch lands in tmp; tests that deliberately exercise the seam
(test_env_redirect_tripwire.py) set their own env in the test body, which
runs after the fixture and wins.

## Evidence file:line quotes

- tests/conftest.py (new, this lane): autouse fixture _isolate_gap_log
  (tmp_path, monkeypatch) setting MAG_GAPS_LOG to tmp_path/loop_gaps.jsonl;
  docstring names the B2-79 cause, the seam, and the sibling-env policy for
  future REDIRECT_VARS seams (mag/env_redirect.py).
- Seam being aimed, mag/temperature_stack.py:44-59 _gaps_log(): "env =
  os.environ.get('MAG_GAPS_LOG', '').strip(); if env: return Path(env)".
- Falsifier run (this lane): a probe test calling
  track_loop_gap("b2336_falsifier_probe", detail=..., force=True) with NO
  local monkeypatch PASSES its assertion that _gaps_log() resolves into tmp,
  and memory/training/loop_gaps.jsonl is byte-still across the run
  (sha256 unchanged, size 103,301 bytes before and after). Probe file
  removed after the run. Two probe-signature corrections mid-lane, named:
  track_loop_gap takes (name, *, detail, ...) - the first draft guessed a
  summary kwarg, the second a note kwarg.
- No-regression: .venv/Scripts/python.exe -m pytest
  tests/test_temperature_stack.py tests/test_env_redirect_tripwire.py -q ->
  "18 passed" with the conftest live (the B2-79/B2-86 monkeypatched test
  still passes with the suite-wide fixture present).

## Work done

1. Read the seam (_gaps_log), the B2-79/B2-86 monkeypatch test, and
   tests/test_env_redirect_tripwire.py's use of the same var.
2. Confirmed tests/conftest.py did not exist; wrote it with the autouse
   fixture and the sibling-seam policy docstring.
3. Ran the falsifier: unguarded track_loop_gap under the conftest resolves
   to tmp; production log byte-still (sha before == sha after).
4. Ran the affected suites: 18 passed. Removed the probe test file.
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This gate is inverted if any of the following holds: (a) a test calling
track_loop_gap with no local monkeypatch appends to
memory/training/loop_gaps.jsonl (the fixture is not autouse, is shadowed by
a local conftest, or the seam stops reading the env); (b) the tripwire tests
break because the fixture fights their own env writes (fixture ordering
regressed); (c) a future sibling seam (MAG_SEAT_CRASH_LOG or the next
REDIRECT_VARS entry) pollutes and the conftest docstring's policy section
was never extended (documented debt, named here as the obligation).

## Bibliography closed

tests/test_temperature_stack.py (B2-79/B2-86 test read in full); mag/temperature_stack.py
(_gaps_log, track_loop_gap signature); mag/env_redirect.py (REDIRECT_VARS
shape, sibling seams); watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md
(accepted from the brief and the test's docstring); tests/test_env_redirect_tripwire.py
read for fixture-ordering compatibility. No network calls.
