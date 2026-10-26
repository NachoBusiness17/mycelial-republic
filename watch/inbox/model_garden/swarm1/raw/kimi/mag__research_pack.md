# swarm1-kimi-mag__research_pack (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Race condition on latest.json writes: concurrent builds corrupt shared file | EVIDENCE: mag/research_pack.py:265-266 | FIX: Use atomic tmp+replace pattern: write to temp file then rename over target
DEFECT 2: Missing timeout on httpx.Client context manager allows indefinite hang | EVIDENCE: mag/research_pack.py:82 | FIX: Add timeout parameter to Client constructor (already present) but verify request-level timeout enforcement
DEFECT 3: _fetch_url returns raw bytes for failed responses (status >=400) which bypasses downstream None checks | EVIDENCE: mag/research_pack.py:102 | FIX: Set raw=None unconditionally when status_code >= 400, not just in exception handler
DEAD-CODE: Exception-swallowing bare pass in _save_web_copy | EVIDENCE: mag/research_pack.py:125-126
ONE-SITTING FIX: Atomic writes for all shared jsonl/json surfaces via tmp+rename pattern | EVIDENCE: mag/research_pack.py:265-266,283-284,303-304,320-321,334-335
