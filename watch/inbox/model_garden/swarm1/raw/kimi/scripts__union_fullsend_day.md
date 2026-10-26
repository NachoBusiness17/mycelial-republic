# swarm1-kimi-scripts__union_fullsend_day (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: RAW.jsonl appends lack atomic tmp+replace, risking corruption on crash | EVIDENCE: scripts/union_fullsend_day.py:585 | FIX: Write to RAW.tmp.<pid>, then os.replace to RAW
DEFECT 2: STATE.json written non-atomically, same corruption risk as known violation (c) | EVIDENCE: scripts/union_fullsend_day.py:300 | FIX: Write to STATE.tmp, then os.replace to STATE
DEFECT 3: PACK.md written non-atomically, same corruption risk | EVIDENCE: scripts/union_fullsend_day.py:635 | FIX: Write to PACK.tmp, then os.replace to PACK
DEAD-CODE: _random import is unused (only `random` imported locally in jitter_sleep_seconds) | EVIDENCE: scripts/union_fullsend_day.py:191
ONE-SITTING FIX: Wrap all jsonl/json writes in atomic tmp+replace pattern | EVIDENCE: scripts/union_fullsend_day.py:585-590
