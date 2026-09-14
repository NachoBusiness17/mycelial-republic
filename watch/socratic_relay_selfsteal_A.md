# Lane A — ground (deepseek)

**Receipts prelude:** `/patches/*.json` is EMPTY (verified: glob fails, only `/patches/applied/` holds `.json` archives: self_steal_* 4x + ask_router.json + swarm_cycle.json). `/mag/mag/` contains all 4 of effect_broker.py/markdown policy_engine.py/switchboard_v2.py/harness.py. Grep `swarm_cycle_v2|ask_router_v2` across `/mag/mag/**/*.py` returns zero hits. No `python3`/`python` binary on this host, so byte-compile/import is unavailable — all import claims below are **reasoned** from grep.

## The deploy is not pending — it is half-done
Ground truth reframes the demo question: 6 modules were to deploy; only 4 landed. The two missing ones — `swarm_cycle_v2.py`, `ask_router_v2.py` — do not exist in the target venv, and more importantly **nothing references them**.

## Single most likely failure mode at deploy time
**A silent dead-import hole, not an ImportError.** The 4 deployed modules form a closed, self-consistent graph that imports cleanly WITHOUT the 2 missing modules:
- `harness.py` imports only `effect_broker as eb`, `policy_engine as pe`, `switchboard_v2 as sb` (lines 34–36).
- `switchboard_v2.py` imports only policy_engine (line 39).
- The name "swarm_cycle" appears only as an `eligible_organ` string label (harness.py:477, switchboard_v2.py:652) and "swarm_worker" as a blackboard path (effect_broker.py:107, switchboard_v2.py:42) — never a module import. [grep receipt]

So deploy won't crash with a missing-module error. The likely failure is **operational**: the two orchestration/ask-routing layers the broker/policy/switchboard were designed to feed (see the `lane_spawn`/cycle suggestions at switchboard_v2.py:652) are absent, so the deployed half runs and passes its own happy-path tests while the self-steal loop silently never converges — a "deploy succeeds, behavior missing" failure that surfaces late, not at import.

## The ONE test that catches it earliest
A **module-inventory/integrity test** asserting set-equality of the expected control-surface modules (the 6 from /patches/applied/) against what `inspect`-import shows in the target venv. It fails the instant the deploy completes on the missing 2. It beats any behavior test because behavior tests implicitly assume the full graph and would take several cycle iterations to notice the gap. A harness `run_once` test would pass on the truncated graph [reasoned: harness.py has test_scenario_* entrypoints but none reference the missing modules], which is exactly why the count-check is the earliest signal.

**Bottom line:** the deploy already half-succeeded; the single risk is that a reduced-function surface looks healthy. Test file-set completeness first.
