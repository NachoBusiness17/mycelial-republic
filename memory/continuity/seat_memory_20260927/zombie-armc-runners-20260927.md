---
name: zombie-armc-runners-20260927
description: 6 duplicate Arm C runner processes deadlocked on problem 2/30 for
  12.5 hours, killed 9/27; pattern = relaunch attempts create zombies that hold
  memory without producing
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Arm C interference replication runner (run_armC.py, budget 200, gemma:2b judge) had 6 duplicate processes running simultaneously on 9/26-27, all launched within seconds of each other from relaunch attempts. All stuck on problem 2 of 30 since 07:07, after solving problem 1 in 20 seconds. Output file frozen at 1/30 rows for 12.5 hours.

**Killed all 6 on 9/27** (PIDs 12940, 17380, 20084, 2920, 17952, 24340). One relaunch exec also died to 1302 during the width-24 experiment.

**Why:** multiple relaunch attempts during the day created duplicate processes. The runner's own design (one call to ollama's /api/generate with a 600s timeout per round) means a hung ollama call deadlocks the entire run with no timeout recovery at the script level.

**How to apply:** before relaunching a long-running compute lane, check for existing processes with the same script name (wmic or tasklist). One relaunch = kill the old first. The script itself should have a per-call timeout and a deadlock recovery arm.
