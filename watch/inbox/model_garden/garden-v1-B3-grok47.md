# garden-v1-B3-grok47 (grok-4.7 @ xai, turn 1, channel: content)

IMPROVEMENT 1: pending_items.jsonl is moved to pending_last.jsonl with no check of the ds_workhorse.py exit status, so a failed pass still retires the only queue copy | EVIDENCE: scripts/descent_driver.sh:23-26 | FIX: run the python under an explicit status test and mv only on exit 0
IMPROVEMENT 2: --out is pending_out_HHMM.jsonl while the loop sleeps 45s, so a later cycle in the same UTC minute reopens and truncates the earlier out file | EVIDENCE: scripts/descent_driver.sh:25-28 | FIX: put cycle and seconds in the out name and do not overwrite an existing file
IMPROVEMENT 3: the paid loop has no lock or pid file, so a second process can enter the same hermes_burn_* dirs and invoke hermes_burn.py at the same time | EVIDENCE: scripts/descent_driver.sh:14-20 | FIX: take an exclusive flock on memory/runs/hermes_burn/driver.lock before the while and exit if it is held
DIFFERENT-BUILD: One supervisor that holds that lock, records each child exit code, and names artifacts with cycle plus full timestamp. This script treats every child as fire-and-forget, then drops or reuses the only queue and out copies.
