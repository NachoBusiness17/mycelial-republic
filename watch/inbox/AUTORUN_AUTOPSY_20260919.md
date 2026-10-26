# AUTORUN AUTOPSY 2026-09-19 — verdict: obedience mislabeled as death

**Symptom:** supervisor state showed `autorun` crashed 4x at 17:31Z, crash-looping since the `state/DOCKER_ONLY` marker landed Aug 30.

**Root cause chain:** on Windows with the Docker-only marker present (and no `MAG_ALLOW_HOST_RUNTIME=1`), `governor_autorun._host_runtime_blocked()` prints `[autorun] blocked: Docker-only runtime is active` and exits at startup, by design, so the host never competes with the containers. `process_supervisor.reap()` treated every fast exit as a crash and respawned under crashLoopBackOff forever. Result: 5,708 blocked lines, 20 days of false "crashed" status, false `crash_loop` failure_kb entries, and a supervisor politely fighting a policy gate it could not see.

**Not dead:** the drainer is alive where policy wants it. `docker ps`: mag-sovereign, mag-worker, mag-redis all up 7 days healthy; the training ledger shows a container-side `autorun_cycle` event at 19:14Z. The plan drainer was never dark.

**Fix (carried into commit 96b5f4b4e by a concurrent fleet sweep; content verified at HEAD):**
- `process_supervisor._policy_blocked()`: default loops whose cmd is the drainer are marked `blocked_by_policy` (not crashed), never respawned under the gate, and auto-resume when the marker lifts or the override env is set.
- Test fixture made hermetic (`_container_mode` forced False + marker isolation): 3 pre-existing test failures that red-flagged whenever mag_launch was live are now deterministic greens.
- 16/16 supervisor + autorun tests pass (`test_process_supervisor.py`, `test_governor_autorun.py`, `test_autorun_v1.py`). Full-census numbers on file from 2026-09-14; targeted run only here, stated honestly.

**Residue:** `logs/supervisor_autorun.out.log` holds the 20-day storm history (492 KB); keep or rotate at will. The supervisor will flip the live state entry to `blocked_by_policy` on its next reap.
