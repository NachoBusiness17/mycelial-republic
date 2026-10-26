# garden-v1-B3 | gemma4:latest | series local-20261001-a | instrument=lane-local-script
# finish=length prompt_tokens=3429 completion_tokens=2048 wall_s=74.2 tok_s=27.6 checks=4/5 {'SHAPE': 1, 'CITES-RESOLVE': 1, 'LINES-IN-RANGE': 1, 'NO-EM-DASH': 1, 'DISTINCT-EVIDENCE': 0}

IMPROVEMENT 1: The driver loop must use temporary files and atomic rename operations instead of in-place moves (`mv`) to guarantee state integrity following a task execution failure or crash. | EVIDENCE: scripts/descent_driver.sh:21-22 | FIX: Use `process_output_temp()` function for intermediate results and rename atomically at the end of the conditional block.
IMPROVEMENT 2: The execution block for core tasks (e.g., running `hermes_burn.py`) must check the exit code of the Python interpreter and log a critical failure if the task failed, rather than silently logging only stdout/stderr. | EVIDENCE: scripts/descent_driver.sh:14-15 | FIX: Replace `"$PY" ... >> "$LOG" 2>&1` with an explicit check of the script's exit status code.
IMPROVEMENT 3: The driver relies on global glob expansion for all task queues (`for q in memory/plans/hermes_burn_*;`) which could fail if a non-directory file matches the pattern, leading to unexpected behavior. | EVIDENCE: scripts/descent_driver.sh:13 | FIX: Implement a find command with `-maxdepth 1 -mindepth 1 -type d` to strictly restrict iteration to directories only.

DIFFERENT-BUILD: I would build a persistent, verifiable state machine model external to the runner, forcing explicit inputs and outputs for every stage (e.g., a YAML manifest).
