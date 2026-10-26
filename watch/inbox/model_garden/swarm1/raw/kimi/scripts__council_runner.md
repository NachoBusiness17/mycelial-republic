# swarm1-kimi-scripts__council_runner (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Hardcoded MAX_TOKENS 8192 contradicts docstring claim of 600 | EVIDENCE: scripts/council_runner.py:44 | FIX: Change MAX_TOKENS to 600 or update docstring invariant
DEFECT 2: HTTP requests lack User-Agent header violating estate law (b) | EVIDENCE: scripts/council_runner.py:308-309 | FIX: Add headers["User-Agent"] = "MagCouncil/1.0" before the POST
DEFECT 3: write_meld writes json directly without atomic tmp+replace violating estate law (c) | EVIDENCE: scripts/council_runner.py:534-540 | FIX: Write to tmp path then Path.replace() atomically
DEAD-CODE: _SK_RE regex unused for actual key detection in post_chat | EVIDENCE: scripts/council_runner.py:36
ONE-SITTING FIX: Atomic write in write_meld to prevent corrupted meld json on crash | EVIDENCE: scripts/council_runner.py:534-540
