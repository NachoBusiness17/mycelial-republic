# coldhot-cold-kimi-mag__training_events (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Non-atomic write to shared JSONL surface violates crash-safety | EVIDENCE: mag/training_events.py:73-74 | FIX: Write to tmp file then atomic rename with Path.replace()
DEFECT 2: Silent OSError suppression hides disk-full and permission failures | EVIDENCE: mag/training_events.py:75-76 | FIX: Log exception details before returning row, or propagate to caller
DEFECT 3: _redact_t2 returns empty dict for non-exportable rows which pollutes export list with falsy entries filtered later | EVIDENCE: mag/training_events.py:91-92,98 | FIX: Return None and filter with [r for r in exported if r is not None] to avoid double-traversal
DEAD-CODE: tier_max parameter in export_jsonl is unused after signature | EVIDENCE: mag/training_events.py:104 | FIX: Remove parameter or pass to _redact_t2 for tier filtering
ONE-SITTING FIX: Replace direct append with atomic tmp+replace in emit() | EVIDENCE: mag/training_events.py:73-74
