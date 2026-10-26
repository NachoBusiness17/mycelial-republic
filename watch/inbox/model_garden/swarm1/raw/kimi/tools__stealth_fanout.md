# swarm1-kimi-tools__stealth_fanout (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Hardcoded api.llm7.io bypasses SSRF check, allowing non-public IP resolution for that host | EVIDENCE: tools/stealth_fanout.py:87-88 | FIX: Remove the `if host != "api.llm7.io":` guard so _assert_public_host runs for all hosts

DEFECT 2: Empty key sends Authorization header with literal "Bearer " exposing malformed auth | EVIDENCE: tools/stealth_fanout.py:108-109 | FIX: Only add Authorization header when key is truthy, omit entirely when empty

DEFECT 3: HEARTBEAT jsonl append lacks atomic tmp+replace, corruptible on crash | EVIDENCE: tools/stealth_fanout.py:138-139 | FIX: Write to temp file in same dir, fsync, then atomic rename to HEARTBEAT

DEAD-CODE: WORK_BASES set defined but never used (superseded by inline set in _check_base) | EVIDENCE: tools/stealth_fanout.py:78-81

ONE-SITTING FIX: Remove api.llm7.io SSRF bypass to enforce public-host validation for all lanes | EVIDENCE: tools/stealth_fanout.py:87-88
