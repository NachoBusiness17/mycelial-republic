# coldhot-hot-deepseek-scripts__descent_driver (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: `pending_items.jsonl` is never cleared when its consumer fails, so a failed batch is re-run every cycle and output preserved under a colliding `%H%M` name | EVIDENCE: scripts/descent_driver.sh:23-27 | FIX: gate the `mv` on `ds_workhorse.py` exit status and route out-file through an `mktemp` name keyed to cycle.
DEFECT 2: The `%H%M` minute-stamp output name reuses an existing file across a 24h loop, silently overwriting a prior cycle's ledger | EVIDENCE: scripts/descent_driver.sh:25 | FIX: append `_c$cycle` to `pending_out_$(date -u +%H%M)`.
DEFECT 3: Log rotation/append to `driver.log` and per-cycle stdout append grow unbounded in an infinite loop with no size cap | EVIDENCE: scripts/descent_driver.sh:16,26 | FIX: truncate `$LOG` when it exceeds a byte threshold at cycle start.
DEAD-CODE: none groundable; every path and variable (`STOP`, `LOG`, `cycle`, `q`, `PY`) is referenced within the 30 lines, so no dead candidate can be cited to real bytes.
ONE-SITTING FIX: Check `ds_workhorse.py` exit status before the `mv`, so a crashed batch is not retried forever against an unrotated output name | EVIDENCE: scripts/descent_driver.sh:24-27
