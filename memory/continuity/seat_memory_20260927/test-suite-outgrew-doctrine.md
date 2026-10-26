---
name: test-suite-outgrew-doctrine
description: AGENTS.md still says "39 deterministic green" but the suite is
  ~1348 tests (~12 min) with 34 pre-existing failures — verify diff-cleanliness
  with targeted runs, never claim "suite green"
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

description: "2026-09-16 — full suite now 1331 pass / 32 fail / 9 skip (~17 min);
  up from 1305/34 baseline — verify diff-cleanliness with targeted runs, never
  claim suite green; 26 new tests from bones+salon landed overnight"
metadata:
  node_type: memory
  type: project
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

As of 2026-09-16, full `pytest -q` collects 1331+ tests (baseline was 1305 pass
/ 34 fail / 9 skip on 2026-09-14). The Sep-15/16 overnight sprint added the
wow_bones suite (24 tests), salon_50 pipeline, and estate catalog tests, pushing
passes up to 1331 while total failures *dropped* from 34 to 32 (the SHELL_ALLOW
powershell fix killed 2). The 32 remaining are pre-existing in
water_computer/wave_driver and other fleet domains untouched by recent diffs.

**Why:** A future session obeying the repo law ("run pytest -q before claiming
done") will see failures and either misattribute them to its own diff or burn a
fix session on unrelated fleet churn. The baseline MOVES — re-census before
comparing.

**How to apply:** Run targeted tests for touched domains instead (surface/inbox
contract tests = 23 tests in ~9s: `tests/test_surface*.py`), confirm the
full-run failure count didn't grow, and claim "my diff is clean" — never "suite
green." Triaging the 32 failures is its own fix session. Note: bare `pytest -q`
in this repo must run from repo root with `.venv/Scripts/python.exe`; `-k`
filters over nonexistent test names silently run 0 tests, so verify the
selection matched. Related: [[repo-git-hygiene-checkpoint-20260914]].
